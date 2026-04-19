"""
transforms_menu.py
==================
Single source of truth for the ATOMIC_TRANSFORMS_LIST string injected into
the LangChain SystemMessage that drives the MR-mining agent.

Design goals
------------
* Self-describing registry: format scope + description + concrete example
  live next to the function registration, so the menu is always in sync.
* Compound-step grouping: the four ALT-permutation helpers (choose_permutation,
  permute_ALT, remap_GT, permute_Number_A_R_fields) are surfaced under a
  single *** header so the LLM never omits a required co-step.
* Pure ASCII output — survives all tokeniser / encoding paths.
* Works as a plain string (for create_react_agent) AND as a LangChain
  ChatPromptTemplate (for pipeline integration).

Escaping contract
-----------------
_SYSTEM_TEMPLATE uses Python / LangChain f-string syntax:
  {variable}   — runtime variable (spec_format, behavior_target, …)
  {{literal}}  — produces a single { } in the final string

build_system_prompt() fills ALL four variables with .format() in one shot.
build_system_prompt_template() supplies transforms_menu via partial_variables
so LangChain never sees an unresolved {transforms_menu} field.

The menu string itself must not contain bare { } — _escape_menu() ensures this.

Usage
-----
    # Plain string (used by engine.py via prompts.py)
    from mr_engine.agent.transforms_menu import build_transforms_menu
    menu: str = build_transforms_menu(spec_format="VCF")

    # LangChain ChatPromptTemplate
    from mr_engine.agent.transforms_menu import build_system_prompt_template
    from mr_engine.behavior import BehaviorTarget, get_system_prompt_fragment

    template = build_system_prompt_template(spec_format="VCF")
    messages = template.format_messages(
        spec_format="VCF",
        behavior_target=BehaviorTarget.ORDERING_INVARIANCE.value,
        behavior_description=get_system_prompt_fragment(
            BehaviorTarget.ORDERING_INVARIANCE
        ),
    )
    system_text: str = messages[0].content
"""

from __future__ import annotations

import textwrap

from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from mr_engine.transforms import TRANSFORM_REGISTRY, TransformMeta, get_whitelist


# ---------------------------------------------------------------------------
# Runtime-gated preconditions
# ---------------------------------------------------------------------------
#
# Some transform preconditions describe RUNTIME capabilities (an external
# binary must exist, a SUT must implement a specific method, etc). When
# the current environment doesn't satisfy them, the transform would
# silently no-op if the LLM picked it — wasting an MR slot. We filter
# those transforms OUT of the prompt menu entirely, so the LLM never
# proposes them in the first place.
#
# Other preconditions (e.g. "info_has_key=CSQ", "alt_count>=2") are
# SAMPLE-level: they describe what the input file must look like for
# the transform to make sense. Those stay in the menu as advisory
# "Preconditions:" lines — the LLM uses them as guidance, they're not
# programmatically filtered.
#
# To add a new runtime-gated precondition: (a) put its name here, and
# (b) ensure the capability-computation side (biotest.py's
# _compute_runtime_capabilities) either includes or excludes the tag
# based on the current runtime state.
KNOWN_RUNTIME_PRECONDITIONS: frozenset[str] = frozenset({
    "primary_sut_has_writer",          # Primary target's runner must set
                                       # supports_write_roundtrip=True. Gates
                                       # sut_write_roundtrip from appearing
                                       # in the menu when the primary parser
                                       # lacks a writer API entirely.
    "primary_sut_has_query_methods",   # Primary runner sets
                                       # supports_query_methods=True AND
                                       # implements discover_query_methods()
                                       # + run_query_methods(). Gates
                                       # query_method_roundtrip (Rank 5).
    "pysam_runtime_reachable",         # Native pysam OR Docker harness OK.
                                       # Gates vcf_bcf_round_trip, permute_bcf_
                                       # header_dictionary.
    "htsjdk_runtime_reachable",        # Java + harness JAR reachable.
    "bcf_codec_available",             # Either pysam or htsjdk provides BCF.
    "samtools_available",              # `samtools` CLI on PATH or in the
                                       # htslib SUT config. Gates
                                       # sam_bam_round_trip (Phase 3 SAM
                                       # coverage plan).
    "cram_reference_available",        # A committed micro-reference under
                                       # seeds/ref/ whose @SQ SN matches
                                       # the seed's. Gates sam_cram_round_trip.
})


def _transform_passes_runtime_filter(
    meta: TransformMeta,
    runtime_capabilities: set[str] | frozenset[str] | None,
) -> bool:
    """Return True if `meta` can actually execute in the current runtime.

    When `runtime_capabilities` is None, filtering is disabled (legacy
    behaviour — every registered transform is offered to the LLM). When
    a capability set is provided, any transform whose preconditions
    reference a KNOWN_RUNTIME_PRECONDITIONS tag NOT in the set is
    filtered out.

    Sample-level preconditions ("alt_count>=2", "info_has_key=CSQ") are
    invisible to this filter and continue to render as advisory text
    inside the prompt menu.
    """
    if runtime_capabilities is None:
        return True  # legacy path — no filtering
    for pc in meta.preconditions:
        if pc in KNOWN_RUNTIME_PRECONDITIONS and pc not in runtime_capabilities:
            return False
    return True


# ---------------------------------------------------------------------------
# Compound-step configuration
# ---------------------------------------------------------------------------

# These four functions are biologically co-dependent: permuting ALT alleles
# requires simultaneously updating GT indices (remap_GT) and Number=A/R field
# values (permute_Number_A_R_fields) to preserve semantics.  They must appear
# together in every ALT-permutation MR's transform_steps list.
COMPOUND_GROUP_ID = "alt_permutation"
COMPOUND_HEADER   = "[VCF] *** Compound step — apply all four together ***"

# Canonical application order within the compound block
COMPOUND_ORDER = [
    "choose_permutation",        # 1. generate permutation array pi
    "permute_ALT",               # 2. reorder ALT alleles by pi
    "remap_GT",                  # 3. update GT indices to match new ALT order
    "permute_Number_A_R_fields", # 4. reorder Number=A / Number=R values
]


# ---------------------------------------------------------------------------
# System prompt template
#
# Escaping rules (applies to _SYSTEM_TEMPLATE string):
#   {variable}  — LangChain / .format() variable placeholder
#   {{literal}} — produces a single { } brace in the rendered output
#
# Variables expected at render time:
#   spec_format          str   "VCF" | "SAM"
#   behavior_target      str   BehaviorTarget.value
#   behavior_description str   get_system_prompt_fragment(target)
#   transforms_menu      str   injected via partial_variables (see below)
# ---------------------------------------------------------------------------

_SYSTEM_TEMPLATE = """\
You are an expert bioinformatics test architect agent.  You mine Metamorphic
Relations (MRs) for genomics file formats based STRICTLY on normative rules
found in official specifications.

You have access to the `query_spec_database` tool.  Use it to retrieve
evidence from the ChromaDB vector store (VCF v4.5 and SAM v1 specs).

=========================================================
TASK
=========================================================
Format  : {spec_format}
Target  : {behavior_target}

{behavior_description}

=========================================================
RETRIEVAL RULES — STAY BOUNDED
=========================================================
1. Call `query_spec_database` with `format_filter="{spec_format}"`.
2. Trust ONLY results where `above_threshold` is false (distance < 0.39).
3. If no results pass the threshold, rephrase your query and retry.
4. **Hard cap: at most 5 tool calls total, then produce your JSON output.**
   Each call should ask a DIFFERENT question — don't repeat the same query.
5. Prefer CRITICAL-severity chunks; if none appear after 5 calls, return
   either the best ADVISORY-backed MR you have OR an empty array `[]`.
   NEVER keep querying forever — LangGraph will abort the run.
6. Copy the `chunk_id` VERBATIM from the result.  Real example:
       "VCFv4.5.tex::Meta-information lines::p122"
   Do NOT paraphrase, abbreviate, or invent chunk_ids.

STOP CONDITION (MUST FOLLOW): after 3-5 tool calls, emit the JSON array
and do NOT call the tool again. An empty array `[]` is a valid answer if
no MR passes the constraints — that's better than looping forever.

=========================================================
ATOMIC TRANSFORMS MENU (WHITELIST)
=========================================================
The entries below are the ONLY strings allowed in `transform_steps`.
Each is labelled with its format scope [VCF] or [SAM] and a description
of what it does to the file.

{transforms_menu}
=========================================================
OUTPUT FORMAT
=========================================================
Return ONLY a raw JSON array — no prose, no markdown fences:

[
  {{
    "mr_name"        : "human-readable descriptive name",
    "scope"          : "{spec_format}.header | {spec_format}.record",
    "preconditions"  : ["string"],
    "transform_steps": ["name_from_whitelist_above"],
    "oracle"         : "invariant that must hold after the transform",
    "evidence": [
      {{
        "chunk_id": "VCFv4.5.tex::Exact Section Title::pN",
        "quote"   : "verbatim sentence copied from the spec result text"
      }}
    ],
    "ambiguity_flags": ["describe any MAY/SHOULD ambiguities, or empty list"]
  }}
]

=========================================================
PRECONDITION DISCIPLINE
=========================================================
Some transforms only apply when the seed satisfies specific conditions
(see each entry's "Preconditions:" line in the menu above). Do NOT
propose a transform whose precondition is guaranteed to fail on the
current corpus. Examples of common gotchas:
  - permute_csq_annotations requires INFO to contain CSQ or ANN.
  - split_multi_allelic requires ALT with 2+ alleles (comma-separated).
  - vcf_bcf_round_trip / permute_bcf_header_dictionary require the SUT
    chain to include a BCF-capable codec (pysam or htsjdk).
  - left_align_indel conservatively activates only when REF[0]==REF[-1]
    and len(REF)!=len(ALT) (indel in a homopolymer context).
  - trim_common_affixes requires REF/ALT to share a common prefix or
    suffix base (e.g., REF=AA,ALT=AC).
Match the transform's precondition to the Evidence and to the seed
corpus. Propose an empty array [] rather than a transform that will
trivially no-op on every seed.

=========================================================
CRITICAL RULES
=========================================================
- `transform_steps` values MUST match whitelist names exactly (case-sensitive).
- `evidence.chunk_id` MUST be copied character-for-character from a tool result
  where `above_threshold` is false.
- `evidence.quote` MUST be a verbatim extract from that result's `text` field.
- Never invent chunk_ids (e.g. "chunk_1", "VCFv4.5-sec-3" are invalid).
- For ALT-permutation MRs list ALL FOUR compound-step names in transform_steps:
  choose_permutation, permute_ALT, remap_GT, permute_Number_A_R_fields.
- `mr_name` is a human label — the system derives mr_id deterministically.
- `ambiguity_flags` is [] when the spec rule is unambiguously normative.
"""


# ---------------------------------------------------------------------------
# Menu-string builder
# ---------------------------------------------------------------------------

def _escape_menu(text: str) -> str:
    """
    Escape bare { and } in the menu string so it is safe to embed inside a
    LangChain / Python f-string template without being parsed as a variable.
    """
    return text.replace("{", "{{").replace("}", "}}")


def _render_hint_and_preconditions(
    meta: TransformMeta, indent: str
) -> list[str]:
    """Render the optional contextual_hint and preconditions lines."""
    out: list[str] = []
    if meta.contextual_hint:
        hint = f"Use when: {meta.contextual_hint}"
        wrapped = textwrap.fill(hint, width=78 - len(indent))
        out.extend(indent + ln for ln in wrapped.splitlines())
    if meta.preconditions:
        out.append(indent + "Preconditions: " + ", ".join(meta.preconditions))
    return out


def _render_compound(members: list[tuple[str, TransformMeta]]) -> str:
    """Render the compound ALT-permutation group as an indented block."""
    lines: list[str] = [f"  {COMPOUND_HEADER}"]
    for name, meta in members:
        lines.append(f"    {name}")
        wrapped = textwrap.fill(meta.description, width=68)
        # 8-space indent under the function name
        lines.append("\n".join("        " + ln for ln in wrapped.splitlines()))
        lines.extend(_render_hint_and_preconditions(meta, indent="        "))
    lines.append(
        "      NOTE: ALL FOUR names must appear in transform_steps together."
    )
    return "\n".join(lines)


def _render_single(name: str, meta: TransformMeta) -> str:
    """Render one standalone transform as a name + indented description."""
    wrapped = textwrap.fill(meta.description, width=70)
    desc = "\n".join("      " + ln for ln in wrapped.splitlines())
    extra_lines = _render_hint_and_preconditions(meta, indent="      ")
    out = f"  [{meta.format}] {name}\n{desc}"
    if extra_lines:
        out += "\n" + "\n".join(extra_lines)
    return out


def build_transforms_menu(
    spec_format: str | None = None,
    runtime_capabilities: set[str] | frozenset[str] | None = None,
) -> str:
    """
    Generate the human-readable ATOMIC_TRANSFORMS_LIST menu string.

    Parameters
    ----------
    spec_format : str | None
        "VCF" or "SAM" to show only relevant transforms.
        None (default) shows all transforms.
    runtime_capabilities : set[str] | None
        When provided, transforms whose preconditions name a known
        runtime-gated tag (see KNOWN_RUNTIME_PRECONDITIONS) not in this
        set are filtered OUT of the menu. Used to prevent the LLM from
        proposing a transform that would silently no-op in the current
        environment (e.g. sut_write_roundtrip on a primary SUT without
        `supports_write_roundtrip=True`). None (default) preserves the
        legacy behaviour of showing all transforms.

    Returns
    -------
    str
        Multi-line menu.  All { } characters are escaped so the string
        can safely be embedded in a LangChain or Python format template.
    """
    compound_members: list[tuple[str, TransformMeta]] = []
    standalone:       list[tuple[str, TransformMeta]] = []
    filtered_out_names: list[str] = []   # for trailing "valid names" list

    for name in sorted(TRANSFORM_REGISTRY.keys()):
        meta = TRANSFORM_REGISTRY[name]
        # Format filter: pass if no filter, or if filter matches the entry
        if spec_format and spec_format not in meta.format:
            continue
        # Runtime-capability filter: hide transforms we can't execute.
        if not _transform_passes_runtime_filter(meta, runtime_capabilities):
            filtered_out_names.append(name)
            continue
        if meta.group == COMPOUND_GROUP_ID:
            compound_members.append((name, meta))
        else:
            standalone.append((name, meta))

    sections: list[str] = []

    # Compound block first — the LLM must see it prominently
    if compound_members:
        order_map = {n: i for i, n in enumerate(COMPOUND_ORDER)}
        compound_members.sort(key=lambda pair: order_map.get(pair[0], 99))
        sections.append(_render_compound(compound_members))

    # Standalone transforms in alphabetical order
    for name, meta in standalone:
        sections.append(_render_single(name, meta))

    # Machine-readable name list at the end (copy-paste anchor for the LLM).
    # Only list the SHOWN transforms — a hidden name would be an invitation
    # to propose it, defeating the filter.
    visible_names = sorted(
        [n for n, _ in compound_members] + [n for n, _ in standalone]
    )
    all_names = ", ".join(visible_names) if visible_names else "(none available)"
    sections.append(
        f"Valid names (copy exactly, case-sensitive):\n  {all_names}"
    )

    # Log-only hint listing what got filtered out — helps operators
    # debug "why didn't the LLM pick my new transform?" cases.
    if filtered_out_names:
        sections.append(
            "Note: the following transforms were hidden because the current "
            "runtime does not satisfy their preconditions: "
            + ", ".join(sorted(filtered_out_names))
        )

    raw_menu = "\n\n".join(sections)
    return _escape_menu(raw_menu)   # safe to embed in any format template


# ---------------------------------------------------------------------------
# LangChain ChatPromptTemplate integration
# ---------------------------------------------------------------------------

def build_system_prompt_template(
    spec_format: str | None = None,
    runtime_capabilities: set[str] | frozenset[str] | None = None,
) -> ChatPromptTemplate:
    """
    Build a LangChain ChatPromptTemplate with the transforms menu pre-baked.

    The menu is computed once at template-construction time and injected via
    PromptTemplate.partial_variables.  This means LangChain's template parser
    never sees the menu as an unresolved variable, and { } characters inside
    the menu are already escaped before parsing begins.

    Parameters
    ----------
    spec_format : str | None
        If given, the menu is filtered to that format's transforms only.
        The runtime variable {spec_format} in the prompt still accepts any
        value at invocation time.
    runtime_capabilities : set[str] | None
        Set of runtime-gated capability tags currently satisfied (e.g.
        `{"primary_sut_has_writer", "pysam_runtime_reachable"}`). Passed
        to build_transforms_menu to hide transforms whose preconditions
        can't be met in this environment. See KNOWN_RUNTIME_PRECONDITIONS.
    """
    menu = build_transforms_menu(
        spec_format=spec_format,
        runtime_capabilities=runtime_capabilities,
    )

    # partial_variables fills {transforms_menu} before LangChain's parser
    # inspects the remaining placeholders — no double-parsing, no escaping clash.
    prompt = PromptTemplate(
        template=_SYSTEM_TEMPLATE,
        input_variables=["spec_format", "behavior_target", "behavior_description"],
        partial_variables={"transforms_menu": menu},
    )
    system_message = SystemMessagePromptTemplate(prompt=prompt)
    return ChatPromptTemplate.from_messages([system_message])
