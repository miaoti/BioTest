"""
Semantic Constraint Coverage (SCC) tracker.

Computes which spec rules (CRITICAL + ADVISORY chunks from Phase A)
are exercised by the current set of enforced MRs. The coverage gap
(blind spots) drives Phase B re-mining.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SCCReport:
    """Result of a semantic constraint coverage computation."""
    total_rules: int
    covered_count: int
    covered_rules: list[str] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    scc_percent: float = 0.0
    blind_spot_details: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_rules": self.total_rules,
            "covered_count": self.covered_count,
            "scc_percent": round(self.scc_percent, 2),
            "blind_spot_count": len(self.blind_spots),
            "blind_spot_details": self.blind_spot_details[:20],
        }

    def export(self, path: Path) -> None:
        """Export SCC report to JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("SCC report exported to %s (%.1f%%)", path, self.scc_percent)


class SCCTracker:
    """
    Tracks which spec rules are covered by exercised MRs.

    The rules database is built from Phase A parsed chunks, filtering
    to CRITICAL and ADVISORY severity only (INFORMATIONAL chunks are
    explanatory text, not testable constraints).
    """

    def __init__(self, parsed_dir: Path):
        self.rules_db = self._build_rules_db(parsed_dir)
        logger.info(
            "SCC tracker initialized: %d testable rules (CRITICAL + ADVISORY)",
            len(self.rules_db),
        )

    def _build_rules_db(self, parsed_dir: Path) -> dict[str, dict[str, str]]:
        """
        Load Phase A chunks and filter to testable rules.

        Returns:
            {chunk_id: {severity, section_id, text_snippet}}
        """
        rules: dict[str, dict[str, str]] = {}

        for chunks_file in parsed_dir.glob("*_chunks.json"):
            try:
                with open(chunks_file, "r", encoding="utf-8") as f:
                    chunks = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Failed to load %s: %s", chunks_file.name, e)
                continue

            for chunk in chunks:
                severity = chunk.get("rule_severity", "")
                if severity not in ("CRITICAL", "ADVISORY"):
                    continue

                chunk_id = chunk.get("chunk_id", "")
                if not chunk_id:
                    continue

                text = chunk.get("text", "")
                rules[chunk_id] = {
                    "severity": severity,
                    "section_id": chunk.get("section_id", ""),
                    "format": chunk.get("format", ""),
                    "text_snippet": text[:200],
                }

        return rules

    def compute_scc(
        self,
        exercised_mrs: list[dict[str, Any]],
        primary_failed_mr_ids: set[str] | None = None,
        format_context: str = "",
    ) -> SCCReport:
        """
        Compute SCC from the set of exercised (enforced) MRs.

        Target-Centric Logic:
            If primary_failed_mr_ids is provided, rules associated with
            those MRs are treated as NOT covered — the primary target
            crashed or failed the metamorphic check, so the rule was
            not successfully validated against the target we care about.

        Format-Aware Logic:
            If format_context is set (e.g., "VCF"), only rules matching
            that format contribute to the SCC denominator. This prevents
            SAM rules from inflating the blind spot count during VCF runs.

        Args:
            exercised_mrs: List of MR dicts from registry["enforced"].
            primary_failed_mr_ids: MR IDs where the primary target failed.
            format_context: If set, restrict to rules of this format only.

        Returns:
            SCCReport with coverage stats and blind spots.
        """
        failed_ids = primary_failed_mr_ids or set()
        fmt = format_context.upper()

        # Filter rules_db by format if format_context is specified
        if fmt:
            all_rules = {
                cid for cid, info in self.rules_db.items()
                if info.get("format", "").upper() == fmt
            }
        else:
            all_rules = set(self.rules_db.keys())

        # Collect all chunk_ids referenced by evidence in exercised MRs,
        # but exclude rules from MRs where the primary target failed.
        covered: set[str] = set()
        for mr in exercised_mrs:
            mr_id = mr.get("mr_id", "")
            if mr_id in failed_ids:
                # Primary target couldn't validate this MR — rule stays uncovered
                continue
            for ev in mr.get("evidence", []):
                cid = ev.get("chunk_id", "")
                if cid and cid in all_rules:
                    covered.add(cid)
        blind_spots = all_rules - covered
        total = len(all_rules)
        scc_pct = (len(covered) / total * 100) if total > 0 else 0.0

        # Build blind spot details, CRITICAL first
        details = []
        for cid in sorted(blind_spots):
            info = self.rules_db[cid]
            details.append({
                "chunk_id": cid,
                "severity": info["severity"],
                "section_id": info["section_id"],
                "format": info["format"],
                "text_snippet": info["text_snippet"],
            })
        details.sort(key=lambda d: (0 if d["severity"] == "CRITICAL" else 1, d["chunk_id"]))

        return SCCReport(
            total_rules=total,
            covered_count=len(covered),
            covered_rules=sorted(covered),
            blind_spots=sorted(blind_spots),
            scc_percent=scc_pct,
            blind_spot_details=details,
        )
