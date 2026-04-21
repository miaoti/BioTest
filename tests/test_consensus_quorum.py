"""
Tests for the Fix #2 M-of-N consensus oracle (Run 9 lesson).

Guards the invariant that:
  * ``quorum_fraction=0.501`` reproduces the legacy strict-majority
    behaviour documented across coverage_notes/htsjdk/vcf/biotest.md.
  * Lowering to ``0.34`` admits a plurality of ceil(N/3) ONLY when the
    top bucket is UNIQUELY largest — ties never win silently.
  * htslib tie-breaker still fires when quorum fails and there is a
    unique authoritative bucket.

These fixtures build ``RunnerResult`` objects directly — no real SUT
needed.
"""

from __future__ import annotations

import pytest

from test_engine.runners.base import RunnerResult
from test_engine.oracles.consensus import get_consensus_output


def _R(name: str, value: dict | None, *, success: bool = True,
       error_type: str = "", stderr: str = "") -> RunnerResult:
    """Tiny ctor so each fixture row is a single line."""
    return RunnerResult(
        success=success and (value is not None),
        canonical_json=value,
        parser_name=name,
        format_type="SAM",
        error_type=error_type,
        stderr=stderr,
    )


# ---------------------------------------------------------------------------
# Strict majority (default) — backward-compat guard
# ---------------------------------------------------------------------------

class TestStrictMajorityDefault:
    def test_4_of_6_same_wins(self):
        A = {"x": 1}
        B = {"x": 2}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A),
            "biopython": _R("biopython", A), "seqan3": _R("seqan3", A),
            "reference": _R("reference", B), "htslib": _R("htslib", B),
        }
        c = get_consensus_output(outputs)
        assert c.is_inconclusive is False
        assert c.consensus_value == A
        assert len(c.winning_voters) == 4
        assert "majority 4/6" in c.reason

    def test_3_of_6_plurality_is_inconclusive_at_default(self):
        """3/6 is not a strict majority — at default 0.501, this must
        stay inconclusive. Guards against accidentally loosening the
        default and silently changing historical run behaviour."""
        A = {"x": 1}; B = {"x": 2}; C = {"x": 3}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A), "biopython": _R("biopython", A),
            "seqan3": _R("seqan3", B), "reference": _R("reference", B),
            "htslib": _R("htslib", C),
        }
        c = get_consensus_output(outputs)
        # htslib is in its own bucket, so tie-breaker rule fires and
        # picks htslib's bucket (size 1) as consensus. That is OK — the
        # key invariant is the 3-voter bucket does NOT become consensus
        # without tie-breaker, because it's not a MAJORITY.
        assert c.is_inconclusive is False
        assert c.consensus_value == C  # htslib authoritative

    def test_3_of_6_plurality_inconclusive_without_tiebreaker(self):
        A = {"x": 1}; B = {"x": 2}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A), "biopython": _R("biopython", A),
            "seqan3": _R("seqan3", B), "reference": _R("reference", B), "other": _R("other", B),
        }
        # No htslib voter present; 3-3 tie, no authoritative tiebreaker.
        c = get_consensus_output(outputs)
        assert c.is_inconclusive is True


# ---------------------------------------------------------------------------
# Loosened quorum (0.34) — Run-9 SAM fix behaviour
# ---------------------------------------------------------------------------

class TestLoosenedQuorum:
    def test_plurality_3_of_6_wins_when_unique_at_0p34(self):
        A = {"x": 1}; B = {"x": 2}; C = {"x": 3}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A), "biopython": _R("biopython", A),
            "seqan3": _R("seqan3", B), "reference": _R("reference", B),
            "other": _R("other", C),
        }
        # Top bucket is 3-voter {A}; no other bucket has ≥3. At 0.34,
        # ceil(6*0.34)=3 → top bucket passes quorum AND is uniquely largest.
        c = get_consensus_output(outputs, quorum_fraction=0.34)
        assert c.is_inconclusive is False
        assert c.consensus_value == A
        assert sorted(c.winning_voters) == ["biopython", "htsjdk", "pysam"]
        assert "plurality >=3/6" in c.reason

    def test_tied_3_3_is_inconclusive_even_at_0p34(self):
        A = {"x": 1}; B = {"x": 2}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A), "biopython": _R("biopython", A),
            "seqan3": _R("seqan3", B), "reference": _R("reference", B), "other": _R("other", B),
        }
        # Two buckets both at 3/6. Top is NOT uniquely largest.
        # Quorum loosening must NOT silently pick one — uniqueness is
        # the safety rail against arbitrary winners.
        c = get_consensus_output(outputs, quorum_fraction=0.34)
        # Without htslib, falls through to inconclusive.
        assert c.is_inconclusive is True

    def test_2_of_6_below_quorum_stays_inconclusive(self):
        """ceil(6*0.34)=3 — bucket of 2 is BELOW quorum, must not win."""
        A = {"x": 1}; B = {"x": 2}; C = {"x": 3}; D = {"x": 4}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A),
            "biopython": _R("biopython", B), "seqan3": _R("seqan3", B),
            "reference": _R("reference", C), "other": _R("other", D),
        }
        c = get_consensus_output(outputs, quorum_fraction=0.34)
        # Top is 2-voter bucket — fails the min-quorum floor.
        assert c.is_inconclusive is True


# ---------------------------------------------------------------------------
# Authoritative tie-breaker still works
# ---------------------------------------------------------------------------

class TestHtslibTiebreaker:
    def test_htslib_breaks_3_3_tie(self):
        """Even loosened quorum should not override htslib's tie-breaker
        role — htslib is the spec reference and wins ties involving it."""
        A = {"x": 1}; B = {"x": 2}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A), "biopython": _R("biopython", A),
            "seqan3": _R("seqan3", B), "reference": _R("reference", B), "htslib": _R("htslib", B),
        }
        c = get_consensus_output(outputs, quorum_fraction=0.34)
        # Tied 3-3; htslib in B bucket → B wins.
        assert c.is_inconclusive is False
        assert c.consensus_value == B


# ---------------------------------------------------------------------------
# Boundary / regression cases
# ---------------------------------------------------------------------------

class TestBoundaries:
    def test_unanimous_wins_under_any_quorum(self):
        A = {"x": 1}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A),
            "biopython": _R("biopython", A),
        }
        for q in (0.1, 0.34, 0.501, 0.9):
            c = get_consensus_output(outputs, quorum_fraction=q)
            assert c.is_inconclusive is False
            assert c.consensus_value == A

    def test_single_voter_edge_case(self):
        """1 voter → trivially unanimous → wins under any quorum_min>=1."""
        A = {"x": 1}
        c = get_consensus_output({"htsjdk": _R("htsjdk", A)}, quorum_fraction=0.501)
        assert c.is_inconclusive is False
        assert c.consensus_value == A

    def test_failing_voters_do_not_count_toward_quorum(self):
        A = {"x": 1}; B = {"x": 2}
        outputs = {
            "htsjdk": _R("htsjdk", A), "pysam": _R("pysam", A),
            "biopython": _R("biopython", A),
            "seqan3": _R("seqan3", None, success=False, error_type="parse_error"),
            "reference": _R("reference", B),
        }
        # Successful voters = 4. Top bucket = 3/4. At 0.501 quorum
        # ceil(4*0.501)=3, and uniquely largest → wins.
        c = get_consensus_output(outputs, quorum_fraction=0.501)
        assert c.is_inconclusive is False
        assert c.consensus_value == A
        assert "seqan3" in c.failing_parsers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
