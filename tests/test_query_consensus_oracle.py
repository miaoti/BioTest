"""
Tests for test_engine/oracles/query_consensus.py — the query-method
consensus oracle that powers Rank 5 API_QUERY_INVARIANCE MRs.

Per Chen-Kuo-Liu-Tse (ACM CSUR 2018) §3.2 + MR-Scout
(Xu et al., TOSEM 2024, arXiv:2304.07548).
"""

from __future__ import annotations

import pytest

from test_engine.runners.base import RunnerResult
from test_engine.oracles.query_consensus import (
    get_query_consensus,
    QueryConsensusResult,
)


def _ok(name: str, methods: dict) -> RunnerResult:
    return RunnerResult(
        success=True, parser_name=name, format_type="VCF",
        canonical_json={"method_results": methods},
    )


def _fail(name: str) -> RunnerResult:
    return RunnerResult(
        success=False, parser_name=name, format_type="VCF",
        error_type="crash", stderr="boom",
    )


class TestGetQueryConsensus:
    def test_all_methods_invariant_passes(self):
        x = {"a": _ok("a", {"isStructural": False, "getNAlleles": 2})}
        tx = {"a": _ok("a", {"isStructural": False, "getNAlleles": 2})}
        verdict = get_query_consensus(x, tx, ["isStructural", "getNAlleles"])
        assert verdict.passed is True
        assert verdict.methods_invariant == ["isStructural", "getNAlleles"]
        assert verdict.methods_changed == []
        assert verdict.dissenting_voters == []

    def test_method_changed_across_t_marks_failure(self):
        # All voters say isStructural changed across T → MR is wrong (or
        # SUTs all have the same bug). methods_changed records it; the
        # verdict is NOT passing.
        x = {"a": _ok("a", {"isStructural": True})}
        tx = {"a": _ok("a", {"isStructural": False})}
        verdict = get_query_consensus(x, tx, ["isStructural"])
        assert verdict.passed is False
        assert verdict.methods_changed == ["isStructural"]

    def test_cross_sut_disagreement_marks_failure(self):
        # 2 voters say invariant holds, 1 voter says it broke under T.
        x = {
            "a": _ok("a", {"isStructural": False}),
            "b": _ok("b", {"isStructural": False}),
            "c": _ok("c", {"isStructural": False}),
        }
        tx = {
            "a": _ok("a", {"isStructural": False}),
            "b": _ok("b", {"isStructural": False}),
            "c": _ok("c", {"isStructural": True}),  # dissenter
        }
        verdict = get_query_consensus(x, tx, ["isStructural"])
        assert verdict.passed is False
        assert verdict.methods_cross_sut_disagreement == ["isStructural"]
        assert "c" in verdict.dissenting_voters

    def test_method_unavailable_excluded_from_voting(self):
        # b returns __error__ for the method; should be excluded, not
        # counted as a disagreement.
        x = {
            "a": _ok("a", {"isStructural": False}),
            "b": _ok("b", {"isStructural": {"__error__": "NoSuchMethod"}}),
        }
        tx = {
            "a": _ok("a", {"isStructural": False}),
            "b": _ok("b", {"isStructural": {"__error__": "NoSuchMethod"}}),
        }
        verdict = get_query_consensus(x, tx, ["isStructural"])
        assert verdict.passed is True
        assert verdict.per_voter["b"]["isStructural"] is None  # excluded

    def test_runner_failure_excludes_voter(self):
        x = {"a": _ok("a", {"m": True}), "b": _fail("b")}
        tx = {"a": _ok("a", {"m": True}), "b": _fail("b")}
        verdict = get_query_consensus(x, tx, ["m"])
        assert verdict.passed is True
        assert verdict.per_voter["b"]["m"] is None

    def test_no_voters_no_methods(self):
        verdict = get_query_consensus({}, {}, [])
        assert verdict.passed is True
        assert verdict.methods_invariant == []
        assert verdict.methods_changed == []

    def test_int_vs_float_compares_via_deep_equal(self):
        """deep_equal handles int/float equivalence; the oracle must
        not flag 2 vs 2.0 as a disagreement."""
        x = {"a": _ok("a", {"score": 2})}
        tx = {"a": _ok("a", {"score": 2.0})}
        verdict = get_query_consensus(x, tx, ["score"])
        assert verdict.passed is True

    def test_list_scalar_results_compared(self):
        x = {"a": _ok("a", {"alts": ["A", "C"]})}
        tx = {"a": _ok("a", {"alts": ["A", "C"]})}
        verdict = get_query_consensus(x, tx, ["alts"])
        assert verdict.passed is True
        x2 = {"a": _ok("a", {"alts": ["A", "C"]})}
        tx2 = {"a": _ok("a", {"alts": ["A", "G"]})}
        verdict2 = get_query_consensus(x2, tx2, ["alts"])
        assert verdict2.passed is False
