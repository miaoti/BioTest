"""
Blindspot ticket builder (Layer 3: Coverage-Steered RAG).

Constructs enriched prompts for Phase B re-mining using:
1. SCC blind spots (uncovered spec rules with full text)
2. Code coverage gaps with SOURCE CODE SLICES (not just line numbers)
3. Historical MR avoidance (prevent re-mining duplicates)

Architecture:
  - Line ranges (e.g., "105-110") are used for compact indexing
  - The builder then extracts the actual source code at those ranges
    from the primary SUT's source tree, so the LLM sees concrete
    if/else branch logic, not just opaque line numbers.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .scc_tracker import SCCReport
from .coverage_collector import CoverageResult
from .rule_attempts import RuleAttemptTracker

logger = logging.getLogger(__name__)

# Maximum number of uncovered spec rules to surface in a ticket.
# Kept intentionally small so the prompt stays under ~2 KB for local
# models — qwen3-coder chokes on anything larger. "少食多餐" principle:
# run more iterations, each with focused context, rather than dump
# hundreds of rules on the LLM and watch it hallucinate.
MAX_UNCOVERED_RULES = 5
# Maximum lines of source code to include per uncovered region
MAX_SLICE_LINES = 10
# Maximum total source code lines across all regions in one ticket
MAX_TOTAL_SLICE_LINES = 40
# Maximum uncovered code regions per SUT in one ticket
MAX_UNCOVERED_REGIONS_PER_SUT = 5
# Maximum previous MR IDs to surface for avoidance (full list bloats prompt).
MAX_PREVIOUS_MR_IDS = 10


# Severity rank: CRITICAL (MUST/SHALL upstream) gets rank 0 = highest
# priority, ADVISORY (SHOULD/RECOMMENDED) = 1, anything else = 2. Phase A
# maps the spec's "MUST/SHALL" keywords to `rule_severity="CRITICAL"`
# and "SHOULD" to `ADVISORY` (see spec_ingestor/chunker.py).
_SEVERITY_RANK: dict[str, int] = {
    "CRITICAL": 0,
    "MUST": 0,
    "REQUIRED": 0,
    "SHALL": 0,
    "MUST NOT": 0,
    "SHALL NOT": 0,
    "ADVISORY": 1,
    "SHOULD": 1,
    "SHOULD NOT": 1,
    "RECOMMENDED": 1,
    "MAY": 2,
    "OPTIONAL": 2,
}


# --- Scoring dimensions -----------------------------------------------------
#
# Lower numeric score = higher priority. We compose three dimensions
# into a single sort key; Python sorts lexicographically over the
# tuple, so the first dimension dominates (complexity), then proximity,
# then format relevance — exactly the ordering requested by the
# senior-engineer refactor brief.
#
# Format relevance is additionally treated as a HARD penalty: a rule
# whose `format` does not match `format_context` gets penalty 10 in
# the format dimension, which almost always sinks it below any
# on-format rule regardless of complexity. This is deliberate — we
# don't want VCF testing to pull in SAM rules "because they're
# complex" and vice versa.

# Words whose presence in spec_text strongly correlates with rule
# complexity (nested conditions, enumerations, exceptions).
_COMPLEXITY_KEYWORDS = (
    "must", "shall", "required", "when", "unless", "only if",
    "otherwise", "additionally", "except", "provided", "subject to",
    "number=a", "number=r", "number=g", "bcf", "dictionary",
)


def _complexity_score(rule: dict[str, Any]) -> int:
    """Return an INTEGER complexity proxy — higher = more complex.

    Phase A chunks carry the raw spec text; longer, keyword-dense
    paragraphs with tables or enumerations get higher scores. The raw
    integer is negated at sort time so complex rules sort first.
    """
    text = (rule.get("spec_text") or rule.get("text_snippet") or "").lower()
    if not text:
        return 0

    # Length bucket: 200 chars ≈ 1 point, capped at 10.
    length_score = min(len(text) // 200, 10)

    # Keyword density.
    keyword_hits = sum(text.count(kw) for kw in _COMPLEXITY_KEYWORDS)

    # Enumeration / table markers.
    enum_hits = text.count(";") + text.count("\n-") + text.count("|")

    # Cross-reference depth — nested references to other sections.
    xref_hits = text.count("§") + text.count("see section")

    chunk_type = (rule.get("chunk_type") or "").lower()
    table_bonus = 3 if chunk_type == "table" else 0

    return length_score + keyword_hits + enum_hits // 3 + xref_hits + table_bonus


_TOKEN_PATTERN = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]{3,}")
_NOISE_TOKENS = frozenset({
    "this", "that", "with", "from", "when", "then", "else", "into",
    "over", "such", "each", "more", "will", "have", "been", "must",
    "shall", "should", "value", "field", "line", "file", "record",
    "format", "parser", "return", "public", "private", "static",
    "final", "void", "class", "import", "string", "integer", "double",
    "boolean", "object", "default", "super", "throw", "throws",
    "catch", "param", "return", "override", "true", "false", "null",
})


def _tokenise(text: str) -> set[str]:
    """Extract alphanumeric tokens ≥ 4 chars and lowercase them."""
    return {
        t.lower()
        for t in _TOKEN_PATTERN.findall(text or "")
        if t.lower() not in _NOISE_TOKENS
    }


def _proximity_score(
    rule: dict[str, Any],
    slice_token_set: set[str],
) -> float:
    """Jaccard-style overlap between rule tokens and code-slice tokens.

    Higher = closer to currently uncovered code in the primary SUT.
    Returned as a float in [0, 1]; negated at sort time.
    """
    if not slice_token_set:
        return 0.0
    rule_text = (rule.get("spec_text") or rule.get("text_snippet") or "")
    if not rule_text:
        return 0.0

    rule_tokens = _tokenise(rule_text)
    if not rule_tokens:
        return 0.0

    overlap = rule_tokens & slice_token_set
    # Small-denominator Jaccard: divide by the RULE's token count so
    # concise rules that are highly-matched still score well.
    return len(overlap) / max(len(rule_tokens), 1)


def _format_penalty(rule: dict[str, Any], format_context: str) -> int:
    """0 if rule's format matches `format_context`, 10 otherwise.

    Also returns 0 when `format_context` is empty (no format filter).
    """
    if not format_context:
        return 0
    rule_fmt = (rule.get("format") or "").upper()
    return 0 if rule_fmt == format_context.upper() else 10


def _build_slice_token_set(code_slices: list["CodeSlice"]) -> set[str]:
    """Tokenise every line of every slice into one unified set.

    We don't care *which* slice a token came from for proximity — any
    overlap implies the rule is close to uncovered code somewhere.
    """
    tokens: set[str] = set()
    for cs in code_slices:
        tokens |= _tokenise(cs.file_label)
        for line in cs.source_lines:
            tokens |= _tokenise(line)
    return tokens


def _prioritise_rules(
    rules: list[dict[str, Any]],
    code_slices: list["CodeSlice"],
    format_context: str,
    attempt_tracker: Optional[RuleAttemptTracker] = None,
) -> list[tuple[dict[str, Any], dict[str, float]]]:
    """Return rules sorted by the five-dimension priority key.

    Sort key (ascending, first difference wins):
        1. fmt_pen           — 0 if on-format, 10 otherwise (hard filter).
        2. failure_count     — repeat-failures sink below first-timers.
        3. -complexity       — complex rules first among equals.
        4. -proximity        — then rules closest to uncovered code.
        5. severity_rank     — CRITICAL before ADVISORY before MAY.
        6. chunk_id          — deterministic tiebreaker.

    Each element is (rule, score_diagnostics) so callers can log why a
    particular rule landed in the Top-K.
    """
    slice_tokens = _build_slice_token_set(code_slices)
    scored: list[tuple[
        tuple[int, int, int, float, int, str],
        dict[str, Any], dict[str, float],
    ]] = []
    for rule in rules:
        chunk_id = rule.get("chunk_id") or ""
        complexity = _complexity_score(rule)
        proximity = _proximity_score(rule, slice_tokens)
        fmt_pen = _format_penalty(rule, format_context)
        sev_rank = _SEVERITY_RANK.get(
            (rule.get("severity") or "").upper().strip(), 3
        )
        failure_count = (
            attempt_tracker.failure_count(chunk_id)
            if attempt_tracker is not None else 0
        )

        key = (
            fmt_pen,
            failure_count,
            -complexity,
            -proximity,
            sev_rank,
            chunk_id,
        )
        diag = {
            "complexity": complexity,
            "proximity": round(proximity, 3),
            "format_penalty": fmt_pen,
            "severity_rank": sev_rank,
            "failure_count": failure_count,
        }
        scored.append((key, rule, diag))

    scored.sort(key=lambda entry: entry[0])
    return [(rule, diag) for _, rule, diag in scored]


# ---------------------------------------------------------------------------
# Source Code Slice Extractor
# ---------------------------------------------------------------------------

@dataclass
class CodeSlice:
    """A slice of source code from an uncovered region."""
    file_label: str      # e.g., "VCFCodec.java"
    line_start: int
    line_end: int
    source_lines: list[str]  # The actual code
    truncated: bool = False

    def render(self, indent: str = "    ") -> str:
        """Render as a formatted code block for the LLM prompt."""
        header = f"{indent}{self.file_label}:{self.line_start}-{self.line_end}"
        if self.truncated:
            header += " (truncated)"
        lines = [header]
        lines.append(f"{indent}```")
        for i, line in enumerate(self.source_lines):
            lineno = self.line_start + i
            lines.append(f"{indent}  {lineno:>4} | {line}")
        if self.truncated:
            lines.append(f"{indent}  ... (more lines omitted)")
        lines.append(f"{indent}```")
        return "\n".join(lines)


def _parse_region(region_str: str) -> tuple[str, list[tuple[int, int]]]:
    """
    Parse an uncovered_region string into (filename, [(start, end), ...]).

    Input formats:
      "VCFCodec.java:105-110"     -> ("VCFCodec.java", [(105, 110)])
      "sam.py:30-35"              -> ("sam.py", [(30, 35)])
      "__init__.py:3"             -> ("__init__.py", [(3, 3)])
      "sam.py:...+5 more"         -> ("sam.py", [])  (overflow marker, skip)
    """
    if "..." in region_str:
        # Overflow marker like "file.py:...+5 more"
        parts = region_str.split(":", 1)
        return (parts[0], [])

    parts = region_str.split(":", 1)
    if len(parts) != 2:
        return (region_str, [])

    filename = parts[0]
    range_str = parts[1]
    ranges = []

    match = re.match(r"(\d+)-(\d+)", range_str)
    if match:
        ranges.append((int(match.group(1)), int(match.group(2))))
    elif range_str.isdigit():
        ln = int(range_str)
        ranges.append((ln, ln))

    return (filename, ranges)


def _resolve_source_file(
    filename: str,
    source_roots: list[Path],
) -> Optional[Path]:
    """
    Find the actual source file by searching through source roots.

    Handles:
    - Exact match: source_root / filename
    - Recursive glob: source_root / **/ filename
    """
    for root in source_roots:
        # Direct path
        direct = root / filename
        if direct.exists():
            return direct
        # Recursive search
        matches = list(root.rglob(filename))
        if matches:
            return matches[0]
    return None


def _extract_slice(
    source_file: Path,
    start: int,
    end: int,
    context_before: int = 2,
    context_after: int = 2,
) -> CodeSlice:
    """
    Extract a code slice from a source file with surrounding context.

    Adds a few lines of context before/after the uncovered range
    so the LLM can understand the control flow.
    """
    try:
        all_lines = source_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return CodeSlice(
            file_label=source_file.name,
            line_start=start,
            line_end=end,
            source_lines=[f"(could not read {source_file})"],
        )

    # Expand range with context, clamped to file bounds
    ctx_start = max(1, start - context_before)
    ctx_end = min(len(all_lines), end + context_after)

    # Truncate if slice is too large
    truncated = False
    if (ctx_end - ctx_start + 1) > MAX_SLICE_LINES:
        ctx_end = ctx_start + MAX_SLICE_LINES - 1
        truncated = True

    lines = all_lines[ctx_start - 1 : ctx_end]  # 1-based to 0-based

    return CodeSlice(
        file_label=source_file.name,
        line_start=ctx_start,
        line_end=ctx_end,
        source_lines=lines,
        truncated=truncated,
    )


def extract_code_slices(
    uncovered_regions: list[str],
    source_roots: list[Path],
    max_total_lines: int = MAX_TOTAL_SLICE_LINES,
) -> list[CodeSlice]:
    """
    Extract actual source code for uncovered regions.

    Args:
        uncovered_regions: ["VCFCodec.java:105-110", "sam.py:30-35", ...]
        source_roots: Directories to search for source files.
        max_total_lines: Budget cap to prevent prompt bloat.

    Returns:
        List of CodeSlice objects with actual source code.
    """
    slices: list[CodeSlice] = []
    total_lines = 0

    for region_str in uncovered_regions:
        if total_lines >= max_total_lines:
            break

        filename, ranges = _parse_region(region_str)
        if not ranges:
            continue

        source_file = _resolve_source_file(filename, source_roots)
        if source_file is None:
            logger.debug("Source file not found: %s (searched %s)", filename, source_roots)
            continue

        for start, end in ranges:
            if total_lines >= max_total_lines:
                break

            code_slice = _extract_slice(source_file, start, end)
            slices.append(code_slice)
            total_lines += len(code_slice.source_lines)

    return slices


# ---------------------------------------------------------------------------
# Blindspot Ticket
# ---------------------------------------------------------------------------

@dataclass
class BlindspotTicket:
    """Context payload for steering Phase B mining toward uncovered rules.

    Iterative-Queue semantics:
      - `uncovered_rules`   holds the TOP-K rules surfaced to the LLM this
                            iteration. Fully-ordered by priority.
      - `total_uncovered`   is the size of the global queue BEFORE Top-K
                            filtering (so the operator can see how many
                            are still waiting for future iterations).
      - `shown_uncovered`   == len(uncovered_rules) (redundant, kept for
                            explicit rendering).
      - `remaining_uncovered` == total - shown (≥0). What the next
                            iteration will see after we cover the
                            current K.

    No rule is ever deleted from the queue; it's deferred. Every
    iteration re-computes the queue from the current SCC state + runs
    the full priority sort, so a rule that drops out of the top-K one
    iteration can reappear if new code coverage makes it more proximate.
    """
    uncovered_rules: list[dict[str, str]] = field(default_factory=list)
    uncovered_code_hints: list[str] = field(default_factory=list)
    code_slices: list[CodeSlice] = field(default_factory=list)
    previous_mr_ids: list[str] = field(default_factory=list)
    primary_target: str = ""
    format_context: str = ""
    iteration: int = 0
    total_uncovered: int = 0
    shown_uncovered: int = 0
    remaining_uncovered: int = 0
    cooling_count: int = 0  # rules in cooldown, held out of Top-K this round
    rule_scores: list[dict[str, float]] = field(default_factory=list)

    def to_prompt_fragment(self) -> str:
        """Render as a string appendable to the Phase B system prompt."""
        if not self.uncovered_rules and not self.code_slices:
            return ""

        target_label = f" (primary target: {self.primary_target})" if self.primary_target else ""
        fmt_label = f" [{self.format_context}]" if self.format_context else ""

        top_rules = self.uncovered_rules  # already capped by the builder

        lines = [
            "",
            "=" * 60,
            f"BLINDSPOT GUIDANCE{target_label}{fmt_label} (iteration {self.iteration})",
            "=" * 60,
            "",
            f"Queue state: "
            f"Total Blindspots = {self.total_uncovered} | "
            f"Injecting Top {self.shown_uncovered} into this ticket | "
            f"{self.remaining_uncovered} rules remaining in queue "
            f"(of which {self.cooling_count} are in cooldown from prior attempts).",
            "",
            "Sort order applied: format filter → failure_count (cold rules",
            "sink) → complexity (desc) → proximity to uncovered primary-SUT",
            "code (desc) → severity. Rules currently in cooldown are held",
            "out of the Top-K so the queue makes progress on other blindspots.",
            "",
            "╔═══════════════════════════════════════════════════════════╗",
            "║  FOCUS DIRECTIVE                                          ║",
            "╠═══════════════════════════════════════════════════════════╣",
            "║  Focus EXCLUSIVELY on the rules below. Do NOT attempt to  ║",
            "║  cover the entire spec in one go. Quality of MRs for      ║",
            "║  these specific rules is the priority. Deferred rules     ║",
            "║  will resurface in the next iteration's ticket.           ║",
            "╚═══════════════════════════════════════════════════════════╝",
            "",
        ]

        # Section 1: Top-K uncovered spec rules (priority-ordered)
        for i, rule in enumerate(top_rules, 1):
            severity = rule.get("severity", "?")
            section = rule.get("section_id", "?")
            text = rule.get("spec_text", rule.get("text_snippet", ""))
            chunk_id = rule.get("chunk_id", "?")
            lines.append(f"  {i}. [{severity}] {section}")
            lines.append(f"     chunk_id: {chunk_id}")
            if text:
                # Tighten per-rule text budget (was 200 chars, now 160)
                lines.append(f'     Spec text: "{text[:160]}"')
            lines.append("")

        # Section 2: Uncovered code with ACTUAL SOURCE SLICES
        if self.code_slices:
            lines.append("UNCOVERED CODE in the primary target parser:")
            lines.append("(These branches/functions were NOT exercised by any test.)")
            lines.append("Study the logic below to design mutations that would force")
            lines.append("the parser to enter these code paths.")
            lines.append("")
            for cs in self.code_slices:
                lines.append(cs.render(indent="  "))
                lines.append("")
        elif self.uncovered_code_hints:
            # Fallback: line references only (source not resolved)
            lines.append("Uncovered code regions (source not available):")
            for hint in self.uncovered_code_hints[:MAX_UNCOVERED_REGIONS_PER_SUT]:
                lines.append(f"  - {hint}")
            lines.append("")

        # Section 3: Historical MR avoidance (capped to keep prompt lean)
        if self.previous_mr_ids:
            lines.append(
                "Do NOT re-mine these existing MR IDs (already explored):"
            )
            for mr_id in self.previous_mr_ids[:MAX_PREVIOUS_MR_IDS]:
                lines.append(f"  - {mr_id}")
            if len(self.previous_mr_ids) > MAX_PREVIOUS_MR_IDS:
                lines.append(
                    f"  … and {len(self.previous_mr_ids) - MAX_PREVIOUS_MR_IDS} more"
                )
            lines.append("")
            lines.append(
                "If previous MRs failed to cover target rules, explore "
                "different transform combinations or edge cases."
            )

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_blindspot_ticket(
    scc_report: SCCReport,
    coverage_results: list[CoverageResult],
    existing_mr_ids: list[str],
    spec_index: Optional[Any] = None,
    iteration: int = 0,
    primary_target: str = "",
    source_roots: Optional[list[Path]] = None,
    format_context: str = "",
    max_rules_per_iteration: int = MAX_UNCOVERED_RULES,
    attempt_tracker: Optional[RuleAttemptTracker] = None,
) -> BlindspotTicket:
    """
    Build a blindspot ticket using PRIORITIZED QUEUEING.

    Flow:
      1. Extract uncovered primary-SUT source slices (for proximity scoring).
      2. Run every uncovered rule through the three-dimension scorer:
         complexity (desc) → proximity (desc) → format match.
      3. Take the Top-K and enrich them with full spec_text from ChromaDB.
      4. Emit explicit queue-state logging so the operator can see that
         no rules are dropped — they're deferred to the next iteration.

    Args:
        scc_report: SCC computed with primary-target awareness.
        coverage_results: Code coverage from all SUTs.
        existing_mr_ids: MR IDs already in the registry.
        spec_index: Optional EphemeralSpecIndex for full text retrieval.
        iteration: Current iteration number.
        primary_target: Name of the primary SUT (e.g., "htsjdk").
        source_roots: Directories to search for SUT source code.
        format_context: Active format ("VCF" or "SAM") — used to down-
                        weight off-format rules in the sort.
        max_rules_per_iteration: Top-K cap. Defaults to MAX_UNCOVERED_RULES
                                 (5). Pass a larger number on stronger LLMs.

    Returns:
        BlindspotTicket with Top-K rules + full queue-state counters.
    """
    # --- 1. Primary-SUT code hints + source slices come FIRST so the
    #        rule scorer can use them for proximity. ---
    code_hints: list[str] = []
    all_uncovered_regions: list[str] = []
    for cov in coverage_results:
        if not cov.available or not cov.uncovered_regions:
            continue
        if primary_target and cov.parser_name != primary_target:
            continue
        for region in cov.uncovered_regions[:MAX_UNCOVERED_REGIONS_PER_SUT]:
            code_hints.append(f"{cov.parser_name} ({cov.language}): {region}")
            all_uncovered_regions.append(region)

    code_slices: list[CodeSlice] = []
    if source_roots and all_uncovered_regions:
        code_slices = extract_code_slices(
            uncovered_regions=all_uncovered_regions,
            source_roots=source_roots,
        )

    # --- 2. Priority-sort every uncovered rule across all dimensions. ---
    all_blindspots = list(scc_report.blind_spot_details)
    ranked = _prioritise_rules(
        rules=all_blindspots,
        code_slices=code_slices,
        format_context=format_context,
        attempt_tracker=attempt_tracker,
    )

    # --- 3. Slice to the Top-K window. SKIP rules that are still in
    #        cooldown from a prior iteration — they're counted as
    #        "remaining in queue", not deleted. This is the "换个思路，
    #        曲线救国" rule: if a hard rule keeps failing, back off and
    #        let the queue cover easier ones, then retry it later.
    total_count = len(ranked)
    top_k_cap = max(0, int(max_rules_per_iteration))
    top_k: list[tuple[dict[str, Any], dict[str, float]]] = []
    cooling_count = 0
    for rule, diag in ranked:
        cid = rule.get("chunk_id") or ""
        if attempt_tracker and attempt_tracker.is_cooling(cid, iteration):
            cooling_count += 1
            continue
        if len(top_k) >= top_k_cap:
            continue
        top_k.append((rule, diag))
    remaining = max(0, total_count - len(top_k))

    # --- 4. Enrich ONLY the Top-K with full spec_text (saves ChromaDB
    #        round-trips on deferred rules). ---
    uncovered_rules: list[dict[str, Any]] = []
    rule_scores: list[dict[str, float]] = []
    for rule, diag in top_k:
        enriched = dict(rule)
        if spec_index is not None:
            chunk_id = rule.get("chunk_id", "")
            try:
                result = spec_index._collection.get(
                    ids=[chunk_id],
                    include=["documents"],
                )
                if result and result["documents"]:
                    enriched["spec_text"] = result["documents"][0]
            except Exception:
                pass
        uncovered_rules.append(enriched)
        rule_scores.append(diag)

    ticket = BlindspotTicket(
        uncovered_rules=uncovered_rules,
        uncovered_code_hints=code_hints,
        code_slices=code_slices,
        previous_mr_ids=existing_mr_ids,
        primary_target=primary_target,
        format_context=format_context,
        iteration=iteration,
        total_uncovered=total_count,
        shown_uncovered=len(uncovered_rules),
        remaining_uncovered=remaining,
        cooling_count=cooling_count,
        rule_scores=rule_scores,
    )

    # --- 5. Register the Top-K as "shown" in the tracker. record_outcome
    #        will be called by Phase D after this iteration's B→C→D
    #        completes, to score which of these rules actually got covered.
    if attempt_tracker is not None:
        attempt_tracker.record_attempt(
            iteration=iteration,
            chunk_ids=[r.get("chunk_id", "") for r in uncovered_rules],
        )

    # --- 6. Emit operator-visible queue-state logs. ---
    logger.info(
        "Total Blindspots: %d | Injecting Top %d into this ticket | "
        "%d rules remaining in queue (%d cooling down).",
        total_count, len(uncovered_rules), remaining, cooling_count,
    )
    if uncovered_rules:
        top_ids = [r.get("chunk_id", "?") for r in uncovered_rules]
        logger.info("Top-K chunk_ids this iteration: %s", top_ids)
        logger.info(
            "Top-K scores: %s",
            [
                {"id": r.get("chunk_id", "?"), **s}
                for r, s in zip(uncovered_rules, rule_scores)
            ],
        )

    return ticket
