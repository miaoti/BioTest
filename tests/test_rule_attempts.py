"""
Tests for the RuleAttemptTracker + cooldown wiring into blindspot_builder.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from test_engine.feedback.blindspot_builder import build_blindspot_ticket
from test_engine.feedback.rule_attempts import (
    MAX_COOLDOWN_ITERATIONS,
    RuleAttemptTracker,
    cooldown_duration,
)
from test_engine.feedback.scc_tracker import SCCReport


# ---------------------------------------------------------------------------
# Cooldown schedule
# ---------------------------------------------------------------------------

def test_cooldown_duration_schedule():
    assert cooldown_duration(0) == 0
    assert cooldown_duration(1) == 1
    assert cooldown_duration(2) == 2
    assert cooldown_duration(3) == 4
    # Caps at MAX_COOLDOWN_ITERATIONS.
    assert cooldown_duration(4) == MAX_COOLDOWN_ITERATIONS
    assert cooldown_duration(10) == MAX_COOLDOWN_ITERATIONS


# ---------------------------------------------------------------------------
# Record / score lifecycle
# ---------------------------------------------------------------------------

def test_record_attempt_then_failure_increments_count():
    t = RuleAttemptTracker()
    t.record_attempt(iteration=1, chunk_ids=["rule_A", "rule_B"])
    outcomes = t.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    assert t.failure_count("rule_A") == 1
    assert t.failure_count("rule_B") == 1
    # Cooldown window: 1 failure ⇒ 1-iter cooldown → cooled_until = 1 + 1 = 2.
    assert t.is_cooling("rule_A", iteration=1)
    assert t.is_cooling("rule_A", iteration=2)
    assert not t.is_cooling("rule_A", iteration=3)
    assert outcomes["rule_A"]["cooldown_iterations"] == 1


def test_successful_coverage_wipes_record():
    t = RuleAttemptTracker()
    t.record_attempt(iteration=1, chunk_ids=["rule_A"])
    t.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    assert t.failure_count("rule_A") == 1

    # Next iteration, the rule IS covered → record wiped.
    t.record_attempt(iteration=3, chunk_ids=["rule_A"])
    outcomes = t.record_outcome(iteration=3, newly_covered_chunk_ids=["rule_A"])
    assert t.failure_count("rule_A") == 0
    assert outcomes["rule_A"]["outcome"] == "covered"
    assert not t.is_cooling("rule_A", iteration=3)


def test_indirect_coverage_also_wipes():
    """A rule covered NOT via the Top-K list (e.g. covered by a
    lingering MR from a previous round) should also be wiped."""
    t = RuleAttemptTracker()
    t.record_attempt(iteration=1, chunk_ids=["rule_A"])
    t.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    assert t.failure_count("rule_A") == 1

    # rule_B was never shown but got covered by a stray MR.
    outcomes = t.record_outcome(iteration=2, newly_covered_chunk_ids=["rule_A"])
    assert t.failure_count("rule_A") == 0
    assert outcomes["rule_A"]["outcome"] == "covered_indirectly"


def test_exponential_backoff_accumulates():
    """Four consecutive failures → cooldowns 1, 2, 4, 4."""
    t = RuleAttemptTracker()
    for i, expected_cd in enumerate([1, 2, 4, MAX_COOLDOWN_ITERATIONS], start=1):
        t.record_attempt(iteration=i, chunk_ids=["hard_rule"])
        outcomes = t.record_outcome(iteration=i, newly_covered_chunk_ids=[])
        assert outcomes["hard_rule"]["cooldown_iterations"] == expected_cd
        # The rule should still be cooling at iteration i + expected_cd.
        assert t.is_cooling("hard_rule", iteration=i + expected_cd)


def test_cooldown_releases_after_window():
    t = RuleAttemptTracker()
    t.record_attempt(iteration=1, chunk_ids=["rule_A"])
    t.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    # Fail #2 ⇒ cooldown=2 → cooled_until = iter 3.
    t.record_attempt(iteration=2, chunk_ids=["rule_A"])
    t.record_outcome(iteration=2, newly_covered_chunk_ids=[])
    assert t.is_cooling("rule_A", iteration=3)
    assert not t.is_cooling("rule_A", iteration=5)


def test_currently_cooled_ids():
    t = RuleAttemptTracker()
    t.record_attempt(iteration=1, chunk_ids=["A", "B", "C"])
    t.record_outcome(iteration=1, newly_covered_chunk_ids=["B"])
    # A and C stayed uncovered → cooling. B was covered → wiped.
    cooled = t.currently_cooled_ids(iteration=2)
    assert cooled == {"A", "C"}


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def test_save_load_roundtrip(tmp_path):
    t1 = RuleAttemptTracker()
    t1.record_attempt(iteration=1, chunk_ids=["A", "B"])
    t1.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    t1.record_attempt(iteration=2, chunk_ids=["B"])
    t1.record_outcome(iteration=2, newly_covered_chunk_ids=[])
    path = tmp_path / "rule_attempts.json"
    t1.save(path)

    t2 = RuleAttemptTracker.load(path)
    assert t2.failure_count("A") == 1
    assert t2.failure_count("B") == 2
    # Re-save should not corrupt the file.
    t2.save(path)
    assert json.loads(path.read_text(encoding="utf-8"))["records"]["B"]["failure_count"] == 2


def test_load_missing_file_returns_empty_tracker(tmp_path):
    t = RuleAttemptTracker.load(tmp_path / "nope.json")
    assert t.records == {}


def test_load_corrupt_file_returns_empty_tracker(tmp_path):
    path = tmp_path / "corrupt.json"
    path.write_text("{not valid json", encoding="utf-8")
    t = RuleAttemptTracker.load(path)
    assert t.records == {}


# ---------------------------------------------------------------------------
# Integration with build_blindspot_ticket — cooled rules drop from Top-K
# ---------------------------------------------------------------------------

def _rule(chunk_id: str, text: str = "MUST do thing", fmt: str = "VCF", sev: str = "CRITICAL"):
    return {
        "chunk_id": chunk_id,
        "severity": sev,
        "format": fmt,
        "section_id": "x",
        "text_snippet": text,
    }


def test_cooled_rule_is_skipped_from_top_k():
    """A rule that's in cooldown must NOT appear in the Top-K even if
    it would otherwise rank first."""
    blind = [
        _rule("hardest",  text="MUST preserve BCF dictionary order with nested conditions " * 5),
        _rule("medium_1", text="MUST parse INFO fields"),
        _rule("medium_2", text="MUST parse FORMAT fields"),
        _rule("medium_3", text="MUST handle missing values"),
    ]
    scc = SCCReport(
        total_rules=4, covered_count=0, scc_percent=0.0,
        blind_spots=[r["chunk_id"] for r in blind],
        blind_spot_details=blind,
    )
    tracker = RuleAttemptTracker()

    # Iteration 1: nothing cooled — hardest ranks first (Top-K = 1).
    ticket1 = build_blindspot_ticket(
        scc_report=scc, coverage_results=[], existing_mr_ids=[],
        spec_index=None, iteration=1, primary_target="htsjdk",
        source_roots=None, format_context="VCF",
        max_rules_per_iteration=1, attempt_tracker=tracker,
    )
    shown1 = [r["chunk_id"] for r in ticket1.uncovered_rules]
    assert shown1 == ["hardest"]

    # Iteration 1 outcome: hardest stayed uncovered → cooldown for 1 iter.
    tracker.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    assert tracker.is_cooling("hardest", iteration=2)

    # Iteration 2: hardest is cooling → a medium rule takes its spot.
    ticket2 = build_blindspot_ticket(
        scc_report=scc, coverage_results=[], existing_mr_ids=[],
        spec_index=None, iteration=2, primary_target="htsjdk",
        source_roots=None, format_context="VCF",
        max_rules_per_iteration=1, attempt_tracker=tracker,
    )
    shown2 = [r["chunk_id"] for r in ticket2.uncovered_rules]
    assert "hardest" not in shown2
    assert shown2 == ["medium_1"]
    assert ticket2.cooling_count == 1
    # Queue accounting: total=4 still present, shown=1, remaining=3 (1 cooling).
    assert ticket2.total_uncovered == 4
    assert ticket2.shown_uncovered == 1
    assert ticket2.remaining_uncovered == 3


def test_cooled_rule_resurfaces_after_cooldown():
    blind = [_rule("hardest", text="MUST x")]
    scc = SCCReport(
        total_rules=1, covered_count=0, scc_percent=0.0,
        blind_spots=["hardest"], blind_spot_details=blind,
    )
    tracker = RuleAttemptTracker()

    # Iter 1: shown + fails → cooldown=1 → cooled_until=2.
    build_blindspot_ticket(
        scc_report=scc, coverage_results=[], existing_mr_ids=[],
        iteration=1, format_context="VCF",
        max_rules_per_iteration=1, attempt_tracker=tracker,
    )
    tracker.record_outcome(iteration=1, newly_covered_chunk_ids=[])

    # Iter 2: still cooling → skipped.
    ticket2 = build_blindspot_ticket(
        scc_report=scc, coverage_results=[], existing_mr_ids=[],
        iteration=2, format_context="VCF",
        max_rules_per_iteration=1, attempt_tracker=tracker,
    )
    assert ticket2.shown_uncovered == 0

    # Iter 3: cooldown expired → rule is shown again.
    ticket3 = build_blindspot_ticket(
        scc_report=scc, coverage_results=[], existing_mr_ids=[],
        iteration=3, format_context="VCF",
        max_rules_per_iteration=1, attempt_tracker=tracker,
    )
    assert ticket3.shown_uncovered == 1
    assert ticket3.uncovered_rules[0]["chunk_id"] == "hardest"


def test_failure_count_penalises_among_uncooled_peers():
    """Two equally-complex rules. One has a history of failures. The
    clean one should rank first."""
    blind = [
        _rule("clean",  text="MUST do foo"),
        _rule("burned", text="MUST do foo"),  # same text, same scores
    ]
    scc = SCCReport(
        total_rules=2, covered_count=0, scc_percent=0.0,
        blind_spots=[r["chunk_id"] for r in blind],
        blind_spot_details=blind,
    )
    tracker = RuleAttemptTracker()
    # Pretend 'burned' already failed twice → cooldown window: 1 (after
    # iter 1) and 2 (after iter 2). Move past the cooldown so it's
    # eligible again, just with a bad failure_count.
    tracker.record_attempt(iteration=1, chunk_ids=["burned"])
    tracker.record_outcome(iteration=1, newly_covered_chunk_ids=[])
    tracker.record_attempt(iteration=2, chunk_ids=["burned"])
    tracker.record_outcome(iteration=2, newly_covered_chunk_ids=[])
    assert tracker.failure_count("burned") == 2

    # Fast-forward past the cooldown window.
    ticket = build_blindspot_ticket(
        scc_report=scc, coverage_results=[], existing_mr_ids=[],
        iteration=10, format_context="VCF",
        max_rules_per_iteration=2, attempt_tracker=tracker,
    )
    shown = [r["chunk_id"] for r in ticket.uncovered_rules]
    assert shown[0] == "clean", f"clean should rank before burned, got {shown}"
    assert shown[1] == "burned"
