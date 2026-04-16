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

logger = logging.getLogger(__name__)

# Maximum lines of source code to include per uncovered region
MAX_SLICE_LINES = 15
# Maximum total source code lines across all regions in one ticket
MAX_TOTAL_SLICE_LINES = 80


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
    """Context payload for steering Phase B mining toward uncovered rules."""
    uncovered_rules: list[dict[str, str]] = field(default_factory=list)
    uncovered_code_hints: list[str] = field(default_factory=list)
    code_slices: list[CodeSlice] = field(default_factory=list)
    previous_mr_ids: list[str] = field(default_factory=list)
    primary_target: str = ""
    iteration: int = 0

    def to_prompt_fragment(self) -> str:
        """Render as a string appendable to the Phase B system prompt."""
        if not self.uncovered_rules and not self.code_slices:
            return ""

        target_label = f" (primary target: {self.primary_target})" if self.primary_target else ""

        lines = [
            "",
            "=" * 60,
            f"BLINDSPOT GUIDANCE{target_label} (iteration {self.iteration})",
            "=" * 60,
            "",
            "The following spec rules are NOT YET successfully validated",
            f"against the PRIMARY TARGET parser ({self.primary_target or 'unknown'}).",
            "Focus your mining on triggering these uncovered constraints:",
            "",
        ]

        # Section 1: Uncovered spec rules (top 10, CRITICAL first)
        for i, rule in enumerate(self.uncovered_rules[:10], 1):
            severity = rule.get("severity", "?")
            section = rule.get("section_id", "?")
            text = rule.get("spec_text", rule.get("text_snippet", ""))
            chunk_id = rule.get("chunk_id", "?")
            lines.append(f"  {i}. [{severity}] {section}")
            lines.append(f"     chunk_id: {chunk_id}")
            if text:
                lines.append(f'     Spec text: "{text[:200]}"')
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
            for hint in self.uncovered_code_hints[:5]:
                lines.append(f"  - {hint}")
            lines.append("")

        # Section 3: Historical MR avoidance
        if self.previous_mr_ids:
            lines.append(
                "Do NOT re-mine these existing MR IDs (already explored):"
            )
            for mr_id in self.previous_mr_ids[:20]:
                lines.append(f"  - {mr_id}")
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
) -> BlindspotTicket:
    """
    Build a blindspot ticket from SCC gaps and code coverage gaps.

    Target-Centric: Only the primary target's code coverage contributes.
    Source Slicing: Extracts actual source code at uncovered line ranges
    so the LLM sees concrete branch logic, not just opaque line numbers.

    Args:
        scc_report: SCC computed with primary-target awareness.
        coverage_results: Code coverage from all SUTs.
        existing_mr_ids: MR IDs already in the registry.
        spec_index: Optional EphemeralSpecIndex for full text retrieval.
        iteration: Current iteration number.
        primary_target: Name of the primary SUT (e.g., "htsjdk").
        source_roots: Directories to search for SUT source code.

    Returns:
        BlindspotTicket with enriched context for Phase B.
    """
    # 1. Enrich blind spots with full spec text from ChromaDB
    uncovered_rules = []
    for detail in scc_report.blind_spot_details[:15]:
        rule = dict(detail)

        if spec_index is not None:
            chunk_id = detail.get("chunk_id", "")
            try:
                result = spec_index._collection.get(
                    ids=[chunk_id],
                    include=["documents"],
                )
                if result and result["documents"]:
                    rule["spec_text"] = result["documents"][0]
            except Exception:
                pass

        uncovered_rules.append(rule)

    # 2. Extract code coverage hints + source slices — PRIMARY TARGET ONLY
    code_hints = []
    all_uncovered_regions: list[str] = []

    for cov in coverage_results:
        if not cov.available or not cov.uncovered_regions:
            continue
        if primary_target and cov.parser_name != primary_target:
            continue
        for region in cov.uncovered_regions[:10]:
            code_hints.append(f"{cov.parser_name} ({cov.language}): {region}")
            all_uncovered_regions.append(region)

    # 3. Extract actual source code at uncovered ranges
    code_slices = []
    if source_roots and all_uncovered_regions:
        code_slices = extract_code_slices(
            uncovered_regions=all_uncovered_regions,
            source_roots=source_roots,
        )
        if code_slices:
            logger.info(
                "Extracted %d code slices (%d total lines) from %s",
                len(code_slices),
                sum(len(s.source_lines) for s in code_slices),
                [r for r in source_roots if r.exists()],
            )

    # 4. Package
    ticket = BlindspotTicket(
        uncovered_rules=uncovered_rules,
        uncovered_code_hints=code_hints,
        code_slices=code_slices,
        previous_mr_ids=existing_mr_ids,
        primary_target=primary_target,
        iteration=iteration,
    )

    logger.info(
        "Blindspot ticket built (target=%s): %d rules, %d code slices, %d existing MRs",
        primary_target or "all", len(uncovered_rules), len(code_slices), len(existing_mr_ids),
    )

    return ticket
