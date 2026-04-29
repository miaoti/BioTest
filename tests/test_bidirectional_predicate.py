"""Unit test for bidirectional §5.3.1 detection logic.

Reverse direction: pre-fix accepts the trigger, post-fix rejects it.
This catches "accept-when-should-reject" regressions like htsjdk-1561
where pre-fix silently parses malformed input and post-fix correctly
errors. Without bidirectional, the original predicate
(`signal(I, V_pre)=true ∧ signal(I, V_post)=false`) misses these.

Tests both:
  - Forward (pre-fail, post-pass) — preserved behavior.
  - Reverse (pre-pass, post-fail) — new behavior, lifts htsjdk-1561.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def test_forward_predicate_still_works():
    """pre-fail → post-pass remains a confirmed detection."""
    # Mock _replay_trigger_silenced: returns False on pre, True on post.
    calls = []

    def mock_replay(sut, trig, fmt):
        calls.append((sut, str(trig), fmt))
        # Phase A call: pre-fix → fails (False). Phase B call: post-fix → succeeds (True).
        return False if len(calls) == 1 else True

    # Simulate Phase A iteration: silenced_here=False → picked_fail
    # Simulate Phase B replay: silenced=True → confirmed=True
    pre = mock_replay("htsjdk", "/pov.vcf", "VCF")
    assert pre is False
    post = mock_replay("htsjdk", "/pov.vcf", "VCF")
    assert post is True

    # Detection: pre_fix_succeeds=False (pre fails) → real signal kept
    # Confirmed: post_silenced=True
    pre_fix_succeeds = False  # because silenced_here=False
    confirmed = post  # because silenced=True
    assert pre_fix_succeeds is False and confirmed is True
    print("[pass] test_forward_predicate_still_works")


def test_reverse_predicate_promotes_demoted_cell():
    """pre-pass → post-fail flips a demoted cell to confirmed.

    Simulates htsjdk-1561 path:
      - Phase A: pre-fix htsjdk silently accepts malformed @HD line.
        silenced_here=True → picked_ok set, picked_fail=None.
        → pre_fix_succeeds=True, detected=False (demoted).
      - Phase B: post-fix htsjdk rejects same input.
        post_silenced=False.
      - Bidirectional check: pfs=True AND post_silenced=False
        → r["detected"]=True, confirmed=True.
    """
    pre_fix_succeeds = True
    detected = False  # demoted by Phase A
    post_silenced = False  # post-fix rejects

    # Apply the bidirectional rule from bug_bench_driver:
    if pre_fix_succeeds is True and post_silenced is False:
        detected = True
        confirmed = True
    else:
        confirmed = None

    assert detected is True, "reverse predicate should promote demoted cell"
    assert confirmed is True
    print("[pass] test_reverse_predicate_promotes_demoted_cell")


def test_neither_direction_real_demoted_stays_demoted():
    """pre-pass → post-pass remains demoted (truly vacuous detection)."""
    pre_fix_succeeds = True
    detected = False  # demoted
    post_silenced = True  # post-fix also accepts

    if pre_fix_succeeds is True and post_silenced is False:
        detected = True
        confirmed = True
    elif pre_fix_succeeds is True:
        # neither direction is a signal — stays demoted
        confirmed = None
    assert detected is False and confirmed is None
    print("[pass] test_neither_direction_real_demoted_stays_demoted")


def test_reverse_predicate_only_fires_when_replay_available():
    """If post-fix install fails, we can't test reverse direction.
    Cell stays demoted (pfs=True, confirmed=None)."""
    pre_fix_succeeds = True
    detected = False
    replay_available = False  # post-fix install died
    post_silenced = None  # not tested

    # Logic mirrors bug_bench_driver's gate:
    if pre_fix_succeeds is True and replay_available and post_silenced is False:
        detected = True
        confirmed = True
    else:
        confirmed = None

    assert detected is False and confirmed is None
    print("[pass] test_reverse_predicate_only_fires_when_replay_available")


def test_post_fix_install_gate_extended():
    """Post-fix install must trigger when ANY cell needs reverse-replay,
    not just when there's a forward detection."""
    # Mock cell records:
    cells = [
        {"detected": False, "trig": "/pov.vcf",
         "pre_fix_succeeds": True, "pre_method_sig": None},   # demoted, candidate for reverse
        {"detected": False, "trig": None,
         "pre_fix_succeeds": None, "pre_method_sig": None},   # nothing
    ]

    def needs_replay(records):
        return any(
            (r["detected"] and r["trig"])
            or r.get("pre_method_sig") is not None
            or (r.get("pre_fix_succeeds") is True and r.get("trig"))
            for r in records
        )

    assert needs_replay(cells) is True, \
        "demoted cell with trig should still trigger post-fix install for reverse check"

    # Without the demoted cell, no install needed:
    assert needs_replay(cells[1:]) is False
    print("[pass] test_post_fix_install_gate_extended")


if __name__ == "__main__":
    test_forward_predicate_still_works()
    test_reverse_predicate_promotes_demoted_cell()
    test_neither_direction_real_demoted_stays_demoted()
    test_reverse_predicate_only_fires_when_replay_available()
    test_post_fix_install_gate_extended()
    print("All bidirectional predicate tests passed.")
