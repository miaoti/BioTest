"""
Tests for the error-consensus oracle (Rank 3 lever).
"""

from __future__ import annotations

import pytest

from test_engine.runners.base import RunnerResult
from test_engine.oracles.error_consensus import (
    ErrorVote,
    get_error_consensus,
)


def _ok(name: str, record_count: int = 1) -> RunnerResult:
    return RunnerResult(
        success=True,
        canonical_json={"records": [{} for _ in range(record_count)]},
        parser_name=name,
        format_type="VCF",
    )


def _reject(name: str) -> RunnerResult:
    return RunnerResult(
        success=False,
        parser_name=name,
        format_type="VCF",
        error_type="parse_error",
        stderr="validation failed",
    )


def _crash(name: str) -> RunnerResult:
    return RunnerResult(
        success=False,
        parser_name=name,
        format_type="VCF",
        error_type="crash",
        stderr="segfault",
    )


def _ineligible(name: str) -> RunnerResult:
    return RunnerResult(
        success=False,
        parser_name=name,
        format_type="SAM",
        error_type="ineligible",
    )


class TestVoteMapping:
    def test_accept_vote_for_matching_record_count(self):
        verdict = get_error_consensus(
            {"p": _ok("p", record_count=3)}, input_record_count=3,
        )
        assert verdict.per_voter_vote["p"] is ErrorVote.ACCEPT

    def test_silent_skip_when_records_drop(self):
        verdict = get_error_consensus(
            {"p": _ok("p", record_count=1)}, input_record_count=3,
        )
        assert verdict.per_voter_vote["p"] is ErrorVote.SILENT_SKIP

    def test_reject_vote_for_parse_error(self):
        verdict = get_error_consensus(
            {"p": _reject("p")}, input_record_count=1,
        )
        assert verdict.per_voter_vote["p"] is ErrorVote.REJECT

    def test_crash_vote_for_segfault(self):
        verdict = get_error_consensus(
            {"p": _crash("p")}, input_record_count=1,
        )
        assert verdict.per_voter_vote["p"] is ErrorVote.CRASH

    def test_ineligible_excluded_from_total(self):
        verdict = get_error_consensus(
            {"p": _ineligible("p"), "q": _reject("q")},
            input_record_count=1,
        )
        assert verdict.total_voters == 1


class TestMajorityVerdict:
    def test_majority_reject_with_silent_acceptor(self):
        """3 parsers reject, 1 silently accepts → silent_acceptor is a bug."""
        verdict = get_error_consensus(
            {
                "a": _reject("a"),
                "b": _reject("b"),
                "c": _crash("c"),
                "bad": _ok("bad", record_count=1),
            },
            input_record_count=1,
        )
        assert verdict.majority_vote in (ErrorVote.REJECT, ErrorVote.CRASH)
        assert "bad" in verdict.silent_acceptors
        assert "bad" in verdict.dissenting_voters

    def test_majority_accept_with_over_strict_dissenter(self):
        """3 accept, 1 rejects → the dissenter is over-strict, not a silent acceptor."""
        verdict = get_error_consensus(
            {
                "a": _ok("a"),
                "b": _ok("b"),
                "c": _ok("c"),
                "strict": _reject("strict"),
            },
            input_record_count=1,
        )
        assert verdict.majority_vote is ErrorVote.ACCEPT
        assert "strict" in verdict.dissenting_voters
        assert "strict" not in verdict.silent_acceptors

    def test_inconclusive_on_even_split(self):
        """2 reject vs 2 accept → no majority, no tie-breaker in this oracle."""
        verdict = get_error_consensus(
            {
                "a": _reject("a"),
                "b": _reject("b"),
                "c": _ok("c"),
                "d": _ok("d"),
            },
            input_record_count=1,
        )
        assert verdict.is_inconclusive
        assert verdict.majority_vote is None

    def test_crash_counts_with_reject_in_majority(self):
        """CRASH and REJECT both mean 'parser refused the input' — they
        pool together for majority counting."""
        verdict = get_error_consensus(
            {
                "a": _reject("a"),
                "b": _crash("b"),
                "bad": _ok("bad"),
            },
            input_record_count=1,
        )
        assert verdict.majority_vote in (ErrorVote.REJECT, ErrorVote.CRASH)
        assert "bad" in verdict.silent_acceptors


class TestEmptyVoters:
    def test_no_eligible_voters_returns_inconclusive(self):
        verdict = get_error_consensus(
            {"p": _ineligible("p")}, input_record_count=1,
        )
        assert verdict.is_inconclusive
        assert verdict.total_voters == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
