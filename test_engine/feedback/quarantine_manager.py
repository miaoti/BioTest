"""
Dynamic MR quarantine manager (Layer 4).

After Phase C execution, evaluates each enforced MR's crash rate.
If an MR causes mass crashes across all parsers (>threshold), it is
auto-demoted from Enforced to Quarantine in the registry.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..oracles.det_tracker import DETTracker

logger = logging.getLogger(__name__)


@dataclass
class QuarantineDecision:
    """Decision for a single MR."""
    mr_id: str
    mr_name: str
    total_tests: int
    failure_count: int
    crash_count: int
    failure_rate: float
    demoted: bool
    reason: str


def evaluate_quarantine(
    det_tracker: DETTracker,
    registry_data: dict[str, Any],
    crash_threshold: float = 0.5,
    primary_target: str = "",
) -> list[QuarantineDecision]:
    """
    Evaluate each enforced MR for potential quarantine demotion.

    An MR is demoted if its failure rate exceeds crash_threshold.
    Failure rate = (tests where passed=False) / total_tests for that MR.

    Per Flow.md Phase D §1.3, when primary_target is set the decision is
    driven ONLY by events involving the primary target (metamorphic
    failures on that SUT, or differential failures where it crashed).
    Auxiliary SUT failures are reported in bug reports but do NOT demote
    MRs — a good MR that merely exposes a biopython bug shouldn't be
    removed from the htsjdk-focused feedback loop.

    Args:
        det_tracker: DETTracker with recorded events from Phase C.
        registry_data: Loaded registry JSON dict.
        crash_threshold: Fraction of failures that triggers demotion.
        primary_target: If set (e.g. "htsjdk"), restrict counting to
                        events where this SUT is among the parser_names
                        and the failure involves that SUT.

    Returns:
        List of quarantine decisions (one per enforced MR).
    """
    decisions = []

    # Filter events to primary-target-relevant ones when primary_target set.
    if primary_target:
        relevant_events = [
            e for e in det_tracker.events
            if primary_target in (e.parser_names or [])
        ]
    else:
        relevant_events = list(det_tracker.events)

    # Recompute per-MR stats over the filtered event set.
    stats_by_mr: dict[str, dict[str, int]] = {}
    for e in relevant_events:
        bucket = stats_by_mr.setdefault(e.mr_id, {"total": 0, "failures": 0, "crashes": 0})
        bucket["total"] += 1
        if not e.passed:
            bucket["failures"] += 1
            if getattr(e, "failure_type", None) == "crash":
                bucket["crashes"] += 1

    for mr_dict in registry_data.get("enforced", []):
        mr_id = mr_dict.get("mr_id", "")
        mr_name = mr_dict.get("mr_name", "")
        stats = stats_by_mr.get(mr_id, {"total": 0, "failures": 0, "crashes": 0})

        total = stats["total"]
        failures = stats["failures"]
        crash_count = stats["crashes"]

        failure_rate = failures / total if total > 0 else 0.0
        demoted = total > 0 and failure_rate > crash_threshold

        scope_label = f"primary={primary_target}" if primary_target else "all SUTs"
        decisions.append(QuarantineDecision(
            mr_id=mr_id,
            mr_name=mr_name,
            total_tests=total,
            failure_count=failures,
            crash_count=crash_count,
            failure_rate=failure_rate,
            demoted=demoted,
            reason=(
                f"failure_rate={failure_rate:.2f} > {crash_threshold} ({scope_label})"
                if demoted
                else f"failure_rate={failure_rate:.2f} <= {crash_threshold} ({scope_label})"
            ),
        ))

    return decisions


def apply_quarantine(
    decisions: list[QuarantineDecision],
    registry_path: Path,
) -> int:
    """
    Move demoted MRs from enforced to quarantine in the registry JSON.

    Args:
        decisions: Quarantine decisions from evaluate_quarantine.
        registry_path: Path to mr_registry.json.

    Returns:
        Number of MRs demoted.
    """
    demoted_ids = {d.mr_id for d in decisions if d.demoted}
    if not demoted_ids:
        return 0

    # Load registry
    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    enforced = data.get("enforced", [])
    quarantine = data.get("quarantine", [])

    # Move demoted MRs
    new_enforced = []
    for mr in enforced:
        if mr.get("mr_id") in demoted_ids:
            quarantine.append(mr)
            logger.warning(
                "QUARANTINE: demoted MR %s (%s)",
                mr.get("mr_id"), mr.get("mr_name"),
            )
        else:
            new_enforced.append(mr)

    data["enforced"] = new_enforced
    data["quarantine"] = quarantine
    data["summary"]["enforced_count"] = len(new_enforced)
    data["summary"]["quarantine_count"] = len(quarantine)

    # Save atomically: write to tmp file then os.replace to avoid
    # leaving a truncated mr_registry.json on crash/power-loss.
    import os
    tmp_path = registry_path.with_suffix(registry_path.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, registry_path)

    demoted_count = len(demoted_ids)
    logger.info("Quarantine applied: %d MRs demoted", demoted_count)
    return demoted_count
