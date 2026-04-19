"""
Prompt templates for LLM-driven MR synthesis (Rank 6 coverage lever).

While Rank 1 (``seed_synthesizer``) asks the LLM for raw VCF/SAM FILES that
exercise uncovered code, Rank 6 asks the LLM for new METAMORPHIC RELATIONS
over the existing transform whitelist that target uncovered code paths.

The output contract is a JSON array of RawMRFromAgent objects — the same
shape Phase B's ReAct agent emits — so the Rank 6 synthesizer can simply
route the response through ``mr_engine/dsl/compiler.py::compile_mr_output``
for validation and evidence hydration.

Grounded in:
  - Fuzz4All (Xia et al., ICSE 2024, arXiv:2308.04748) — coverage-steered
    LLM prompt mutation; +36.8% over language-specific fuzzers.
  - PromptFuzz (Lyu et al., CCS 2024, arXiv:2312.17677) — coverage-guided
    driver synthesis via LLM prompt mutation; 1.61x branch coverage.
  - ChatAFL (Meng et al., NDSS 2024) — LLM breaks coverage plateaus by
    synthesizing NEW test inputs (not just mutations).
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Shared output contract
# ---------------------------------------------------------------------------

def _render_output_contract(n: int) -> str:
    return (
        "OUTPUT CONTRACT:\n"
        f"- Produce a single JSON ARRAY with at most {n} MR objects.\n"
        "- Wrap it in a triple-fenced ```json block. NO prose before or after.\n"
        "- Each MR object MUST have these top-level keys EXACTLY:\n"
        '    {"mr_name", "scope", "preconditions", "transform_steps",\n'
        '     "oracle", "evidence", "ambiguity_flags"}\n'
        "  plus the optional `query_methods` key when your MR uses the\n"
        "  `query_method_roundtrip` transform (see rule below).\n"
        '- `scope` is one of "VCF.header" | "VCF.record" | "SAM.header" | "SAM.record".\n'
        "- `transform_steps` is a JSON array of STRINGS, each taken VERBATIM\n"
        "  from the ALLOWED TRANSFORMS list below. Do not invent new names.\n"
        "- `evidence` is a non-empty JSON array of `{\"chunk_id\", \"quote\"}`\n"
        "  objects. `chunk_id` values must be EXACT chunk IDs lifted from the\n"
        "  BLINDSPOT REPORT below (or from the UNCOVERED RULES section).\n"
        "  Do NOT invent chunk IDs — the compiler will reject them.\n"
        "- `oracle` is a short English sentence specifying the invariant that\n"
        "  must hold between parse(x) and parse(T(x)).\n"
        "- `preconditions` is a JSON array of short English gates. May be empty.\n"
        "- `ambiguity_flags` is a JSON array of short English flags. May be empty.\n"
        "- If your MR's `transform_steps` contains `query_method_roundtrip`,\n"
        "  you MUST also include a top-level `query_methods` JSON array of\n"
        "  2-5 method names taken VERBATIM from the AVAILABLE QUERY METHODS\n"
        "  catalog. An empty list will be rejected by the Pydantic validator.\n"
        "- Prefer MRs that touch the `UNCOVERED CODE` slices shown below.\n"
        "  If a slice references e.g. `isStructural()` or a struct field, pick\n"
        "  transforms that would exercise that code path after parse.\n"
        "- Skip any MR you are not confident about — quality beats quantity.\n"
        "  It is perfectly fine to return fewer than the target count, or an\n"
        "  empty array, if nothing new fits.\n"
    )


def _render_transforms_block(whitelist: list[str]) -> str:
    """Pretty-print the transform whitelist the LLM is allowed to compose."""
    lines = ["ALLOWED TRANSFORMS (use these names exactly, nothing else):"]
    for name in whitelist:
        lines.append(f"  - {name}")
    return "\n".join(lines)


def _render_query_methods_block(query_methods: list[dict]) -> str:
    """Render the Rank-5 query-method catalog when the primary SUT exposes
    one. Same shape as the Phase B system-prompt block built by
    ``prompts._build_query_methods_block``."""
    if not query_methods:
        return ""
    lines: list[str] = [
        "",
        "AVAILABLE QUERY METHODS on the primary SUT (Rank 5 catalog):",
        "  Use these for `query_method_roundtrip` MRs. Pick 2-5 per MR whose",
        "  scalar output should be invariant under the chosen transform.",
    ]
    for m in query_methods[:50]:
        n = m.get("name", "?")
        r = m.get("returns", "Any")
        a = ",".join(m.get("args", []))
        sig = f"{n}({a})" if a else f"{n}()"
        lines.append(f"  - {sig} -> {r}")
    return "\n".join(lines)


def _render_mutator_catalog_block(mutator_catalog: list[dict]) -> str:
    """Render the Tier-2b mutator catalog when the primary runner exposes it.

    Prompt-only: this tells the LLM which POST-PARSE API mutator methods
    exist on the parsed object so it can reason about which under-covered
    classes its MRs should aim for. The catalog is NOT a new transform —
    the framework does not dispatch mutator chains directly. Generated
    MRs must still use the allowed transforms list (``sut_write_roundtrip``
    is the natural partner: apply a transform on file bytes whose effect
    mirrors what those mutators would produce post-parse).
    """
    if not mutator_catalog:
        return ""
    lines: list[str] = [
        "",
        "AVAILABLE MUTATOR METHODS on the primary SUT (Tier 2b catalog):",
        "  These are public mutator methods reflection discovered on the",
        "  parsed-object class (setX / addX / removeX / clearX / putX, etc.).",
        "  Use them as SEMANTIC HINTS for which classes are under-covered",
        "  — e.g., if many mutators on a given type are listed, the LLM",
        "  should weight transforms that exercise that type's post-parse",
        "  state. Do NOT try to call these mutators directly in an MR;",
        "  the framework dispatches only through the ALLOWED TRANSFORMS",
        "  list above. A typical pattern: pair ``sut_write_roundtrip``",
        "  with a byte-level transform whose effect mirrors the mutator,",
        "  or use ``query_method_roundtrip`` to observe a scalar that",
        "  depends on the mutator's target state.",
        "",
        "Methods (cap 50, by name):",
    ]
    for m in mutator_catalog[:50]:
        n = m.get("name", "?")
        r = m.get("returns", "Any")
        a = ",".join(m.get("args", []))
        sig = f"{n}({a})" if a else f"{n}()"
        lines.append(f"  - {sig} -> {r}")
    return "\n".join(lines)


def _render_exemplars_block(exemplars: list[dict]) -> str:
    """Tiny in-context block of accepted MRs so the LLM gets the shape and
    style right. Caller supplies at most 3 sanitized entries."""
    if not exemplars:
        return ""
    import json
    lines = [
        "",
        "EXAMPLES of MRs the framework has already accepted (for shape only):",
    ]
    for ex in exemplars[:3]:
        lines.append("```json")
        lines.append(json.dumps(ex, indent=2))
        lines.append("```")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Format-specific builders
# ---------------------------------------------------------------------------

_FORMAT_INTRO = {
    "VCF": (
        "You are a senior test engineer designing NEW metamorphic relations "
        "(MRs) for a VCF parser differential-testing framework. Each MR you "
        "propose is of the form `P(parse(x)) == P(parse(T(x)))` where T is a "
        "composition of atomic transforms from the whitelist below. Your goal "
        "is to target SPECIFIC uncovered code paths surfaced in the blindspot "
        "report, not re-cover happy-path semantics."
    ),
    "SAM": (
        "You are a senior test engineer designing NEW metamorphic relations "
        "(MRs) for a SAM/BAM parser differential-testing framework. Each MR "
        "you propose is of the form `P(parse(x)) == P(parse(T(x)))` where T "
        "is a composition of atomic transforms from the whitelist below. "
        "Your goal is to target SPECIFIC uncovered code paths surfaced in the "
        "blindspot report, not re-cover happy-path semantics."
    ),
}


def build_prompt(
    blindspot_context: str,
    fmt: str,
    whitelist: list[str],
    n: int = 5,
    query_methods: list[dict] | None = None,
    mutator_catalog: list[dict] | None = None,
    exemplars: list[dict] | None = None,
) -> str:
    """Build the MR-synthesis prompt for a given format.

    Args:
        blindspot_context: Same text produced by
            ``BlindspotTicket.to_prompt_fragment()`` used by Phase B mining
            and Rank 1 seed synthesis. Contains Top-K uncovered spec rules +
            the "UNCOVERED CODE" block with source slices.
        fmt: "VCF" or "SAM".
        whitelist: List of ALL allowed transform names (from
            ``mr_engine.transforms.get_whitelist()``). The LLM may only
            compose MRs over this exact set — it cannot invent new names.
        n: Maximum MR count to request (the LLM may return fewer).
        query_methods: Optional Rank-5 query-method catalog from the primary
            SUT's runner. If present, the LLM is invited to use
            ``query_method_roundtrip`` with populated ``query_methods``.
        exemplars: Optional list of up to 3 accepted MRs for in-context
            shape grounding.
    """
    fmt_u = fmt.upper()
    if fmt_u not in ("VCF", "SAM"):
        raise ValueError(f"Unsupported format for MR synthesis: {fmt}")

    parts: list[str] = [
        _FORMAT_INTRO[fmt_u],
        "",
        "IMPORTANT:",
        "  - This run's Phase B ReAct agent already mined MRs from the spec "
        "catalog. The registry contains those already — do NOT re-emit them.",
        "  - Instead, pick combinations of transforms (and query methods, if "
        "available) that look like they should exercise the specific uncovered "
        "lines / branches quoted in the blindspot report below.",
        "  - Be conservative: if a slice is unreachable via parse-only paths "
        "(e.g., it lives behind a Writer or a API query), target it via the "
        "corresponding transform (`sut_write_roundtrip`, "
        "`query_method_roundtrip`). Do not invent new transform names.",
        "",
        _render_transforms_block(whitelist),
    ]

    qm_block = _render_query_methods_block(query_methods or [])
    if qm_block:
        parts.append(qm_block)

    mut_block = _render_mutator_catalog_block(mutator_catalog or [])
    if mut_block:
        parts.append(mut_block)

    ex_block = _render_exemplars_block(exemplars or [])
    if ex_block:
        parts.append(ex_block)

    parts.extend([
        "",
        "=== BLINDSPOT REPORT (uncovered rules + source slices) ===",
        blindspot_context,
        "=== END BLINDSPOT REPORT ===",
        "",
        _render_output_contract(n=n),
    ])
    return "\n".join(parts)
