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
    mr_invalid_threshold: int = 3,
) -> list[QuarantineDecision]:
    """
    Evaluate each enforced MR for potential quarantine demotion.

    Cross-Validation "良民证" demotion policy (post-trust-fix):

      Before demoting an MR we ask across the ENTIRE parser pool — not
      just the primary — whether at least one parser endorsed the MR on
      at least one seed. An endorsement means a metamorphic event where
      `passed=True` (the parser produced the same canonical output on
      both x and T(x), OR it matched consensus on both).

      If ANY parser (htsjdk, pysam, biopython, seqan3, htslib, or even
      our own reference normalizer) endorsed the MR at any time, the MR
      receives a "良民证" (Citizen Card) and is KEPT in enforced. The
      rationale: a legitimate metamorphic relation is one that at least
      ONE conformant implementation honors. A primary-only failure
      under such an endorsement is a SUT non-conformance bug, not a
      refutation of the MR itself.

      An MR is demoted only when:
        1. Every parser that ran on it failed AND either (a) the primary
           crashes/times-out at rate > crash_threshold, or (b) every
           parser disagreed with consensus / with itself on every seed.
        2. `failure_cause == "mr_invalid"` events (htslib flat-out
           rejected T(x) as malformed) exceed `mr_invalid_threshold`
           AND no parser endorsed the MR on any seed. htslib's rejection
           is the strongest signal the file is malformed, but we still
           require unanimity — if even one lenient parser parsed T(x)
           successfully we retain the MR, because the MR's output may
           simply be in a gray zone of the spec rather than invalid.

    Args:
        det_tracker: DETTracker with recorded events from Phase C.
        registry_data: Loaded registry JSON dict.
        crash_threshold: Fraction above which the primary's crash rate
                         triggers demotion (when no endorsement exists).
        primary_target: Used ONLY for labeling + primary crash stats.
                        The endorsement check scans the full parser pool.
        mr_invalid_threshold: Raw count of htslib rejection events that
                              triggers demotion when no endorsement exists.

    Returns:
        List of quarantine decisions (one per enforced MR).
    """
    decisions = []

    # Endorsement pool: EVERY metamorphic event across EVERY parser.
    # This is the cross-validation set — we need the auxiliaries here,
    # so we deliberately do NOT filter to primary_target.
    all_events = list(det_tracker.events)

    endorsements_by_mr: dict[str, set[str]] = {}
    for e in all_events:
        if e.test_type == "metamorphic" and e.passed and e.parser_names:
            endorsements_by_mr.setdefault(e.mr_id, set()).update(e.parser_names)

    # Primary-scoped stats for crash-rate / invalid-count thresholds.
    if primary_target:
        primary_events = [
            e for e in all_events
            if primary_target in (e.parser_names or [])
        ]
    else:
        primary_events = all_events

    stats_by_mr: dict[str, dict[str, int]] = {}
    for e in primary_events:
        # write_roundtrip events are SUT-conformance signals — they do
        # NOT contribute to MR quarantine decisions because they depend
        # only on the seed, not on the MR transform. Counted in bug
        # reports / coverage but never against the MR.
        if e.test_type == "write_roundtrip":
            continue
        bucket = stats_by_mr.setdefault(e.mr_id, {
            "total": 0,
            "failures": 0,
            "crashes": 0,
            "against_consensus": 0,
            "mr_invalid": 0,
            "non_conformance": 0,
            "inconclusive": 0,
        })
        bucket["total"] += 1
        if not e.passed:
            bucket["failures"] += 1
            ft = getattr(e, "failure_type", None)
            fc = getattr(e, "failure_cause", None)
            if ft in ("crash", "timeout"):
                bucket["crashes"] += 1
            if fc in bucket:
                bucket[fc] += 1

    for mr_dict in registry_data.get("enforced", []):
        mr_id = mr_dict.get("mr_id", "")
        mr_name = mr_dict.get("mr_name", "")
        stats = stats_by_mr.get(mr_id, {})
        total = stats.get("total", 0)
        failures = stats.get("failures", 0)
        crash_count = stats.get("crashes", 0)
        invalid_count = stats.get("mr_invalid", 0)
        against_consensus = stats.get("against_consensus", 0)

        failure_rate = failures / total if total > 0 else 0.0
        consensus_fail_rate = against_consensus / total if total > 0 else 0.0
        crash_rate = crash_count / total if total > 0 else 0.0

        endorsers = sorted(endorsements_by_mr.get(mr_id, set()))
        has_endorsement = len(endorsers) > 0

        demoted = False
        reason_parts: list[str] = []

        if has_endorsement:
            # Citizen Card — at least one parser says the MR is sound.
            # Skip all demotion rules outright.
            pass
        else:
            if invalid_count >= mr_invalid_threshold:
                demoted = True
                reason_parts.append(
                    f"mr_invalid={invalid_count}>={mr_invalid_threshold}"
                )
            if total > 0 and consensus_fail_rate > crash_threshold:
                demoted = True
                reason_parts.append(
                    f"against_consensus_rate={consensus_fail_rate:.2f}>{crash_threshold}"
                )
            if total > 0 and crash_rate > crash_threshold:
                demoted = True
                reason_parts.append(
                    f"crash_rate={crash_rate:.2f}>{crash_threshold}"
                )

        scope_label = f"primary={primary_target}" if primary_target else "all SUTs"
        if demoted:
            reason = f"DEMOTE: {'; '.join(reason_parts)} (no endorsement; {scope_label})"
        elif has_endorsement:
            reason = (
                f"KEEP: endorsed by {endorsers} (良民证); "
                f"primary failures={failures}/{total}"
            )
        else:
            reason = (
                f"KEEP: invalid={invalid_count}, "
                f"against_consensus={against_consensus}/{total}, "
                f"crashes={crash_count}/{total} (no endorsement yet; {scope_label})"
            )

        decisions.append(QuarantineDecision(
            mr_id=mr_id,
            mr_name=mr_name,
            total_tests=total,
            failure_count=failures,
            crash_count=crash_count,
            failure_rate=failure_rate,
            demoted=demoted,
            reason=reason,
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
