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
RETRIEVAL RULES
=========================================================
1. Call `query_spec_database` with `format_filter="{spec_format}"`.
2. Trust ONLY results where `above_threshold` is false (distance < 0.39).
3. If no results pass the threshold, rephrase your query and retry.
4. Keep querying until you have at least one CRITICAL-severity chunk per MR.
5. Copy the `chunk_id` VERBATIM from the result.  Real example:
       "VCFv4.5.tex::Meta-information lines::p122"
   Do NOT paraphrase, abbreviate, or invent chunk_ids.

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


def _render_compound(members: list[tuple[str, TransformMeta]]) -> str:
    """Render the compound ALT-permutation group as an indented block."""
    lines: list[str] = [f"  {COMPOUND_HEADER}"]
    for name, meta in members:
        lines.append(f"    {name}")
        wrapped = textwrap.fill(meta.description, width=68)
        # 8-space indent under the function name
        lines.append("\n".join("        " + ln for ln in wrapped.splitlines()))
    lines.append(
        "      NOTE: ALL FOUR names must appear in transform_steps together."
    )
    return "\n".join(lines)


def _render_single(name: str, meta: TransformMeta) -> str:
    """Render one standalone transform as a name + indented description."""
    wrapped = textwrap.fill(meta.description, width=70)
    desc = "\n".join("      " + ln for ln in wrapped.splitlines())
    return f"  [{meta.format}] {name}\n{desc}"


def build_transforms_menu(spec_format: str | None = None) -> str:
    """
    Generate the human-readable ATOMIC_TRANSFORMS_LIST menu string.

    Parameters
    ----------
    spec_format : str | None
        "VCF" or "SAM" to show only relevant transforms.
        None (default) shows all transforms.

    Returns
    -------
    str
        Multi-line menu.  All { } characters are escaped so the string
        can safely be embedded in a LangChain or Python format template.
    """
    compound_members: list[tuple[str, TransformMeta]] = []
    standalone:       list[tuple[str, TransformMeta]] = []

    for name in sorted(TRANSFORM_REGISTRY.keys()):
        meta = TRANSFORM_REGISTRY[name]
        # Format filter: pass if no filter, or if filter matches the entry
        if spec_format and spec_format not in meta.format:
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

    # Machine-readable name list at the end (copy-paste anchor for the LLM)
    all_names = ", ".join(get_whitelist())
    sections.append(
        f"Valid names (copy exactly, case-sensitive):\n  {all_names}"
    )

    raw_menu = "\n\n".join(sections)
    return _escape_menu(raw_menu)   # safe to embed in any format template


# ---------------------------------------------------------------------------
# LangChain ChatPromptTemplate integration
# ---------------------------------------------------------------------------

def build_system_prompt_template(spec_format: str | None = None) -> ChatPromptTemplate:
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

    Returns
    -------
    ChatPromptTemplate
        Expects three runtime variables at format_messages() call time:
          spec_format          str   "VCF" | "SAM"
          behavior_target      str   BehaviorTarget.value
          behavior_description str   get_system_prompt_fragment(target)

    Example
    -------
        from mr_engine.behavior import BehaviorTarget, get_system_prompt_fragment

        template = build_system_prompt_template(spec_format="VCF")

        messages = template.format_messages(
            spec_format="VCF",
            behavior_target=BehaviorTarget.ORDERING_INVARIANCE.value,
            behavior_description=get_system_prompt_fragment(
                BehaviorTarget.ORDERING_INVARIANCE
            ),
        )
        system_text = messages[0].content   # pass to create_react_agent
    """
    menu = build_transforms_menu(spec_format=spec_format)

    # partial_variables fills {transforms_menu} before LangChain's parser
    # inspects the remaining placeholders — no double-parsing, no escaping clash.
    prompt = PromptTemplate(
        template=_SYSTEM_TEMPLATE,
        input_variables=["spec_format", "behavior_target", "behavior_description"],
        partial_variables={"transforms_menu": menu},
    )
    system_message = SystemMessagePromptTemplate(prompt=prompt)
    return ChatPromptTemplate.from_messages([system_message])
