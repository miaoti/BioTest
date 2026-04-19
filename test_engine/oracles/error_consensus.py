"""
Error-consensus oracle (Rank 3 lever): majority-vote on parser rejection
verdicts rather than canonical-JSON equivalence.

Used exclusively when the MR's behavior target is REJECTION_INVARIANCE (i.e.
the transform deliberately violates a CRITICAL spec rule). In that mode the
semantic oracle (deep_equal consensus) is meaningless — we want parsers to
REJECT, not to agree on what they emit.

Vote grammar per voter:

    ACCEPT       — parse success AND record count preserved.
    SILENT_SKIP  — parse success BUT record count < original (parser quietly
                   dropped the malformed record without raising).
    REJECT       — parse failed with a recognized validation error
                   (`error_type` in {"parse_error"} but not "crash").
    CRASH        — parse failed hard (non-zero exit, `error_type == "crash"`).

Consensus rule: a SUT whose vote differs from the majority exposes a
conformance bug. Specifically:

    - If the majority voted REJECT and some SUT voted ACCEPT/SILENT_SKIP,
      that SUT silently accepted a spec violation → REAL BUG.
    - If the majority voted ACCEPT and one SUT voted REJECT/CRASH, that
      SUT is over-strict. Logged as an inconsistency but usually not a
      bug on the SUT itself (spec is permissive here).

The oracle returns a `ErrorConsensusResult` identifying the majority verdict
and the dissenters. Quarantine / DET logic lives elsewhere.

Reference: Chen, Kuo, Liu, Tse 2018 §3.2 (differential oracle). This is the
rejection-path specialization of the same idea — voters don't compare outputs,
they compare accept/reject signals.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ..runners.base import RunnerResult


class ErrorVote(str, Enum):
    ACCEPT = "accept"
    SILENT_SKIP = "silent_skip"
    REJECT = "reject"
    CRASH = "crash"
    INELIGIBLE = "ineligible"  # format-incompatible; does not vote


@dataclass
class ErrorConsensusResult:
    """Outcome of a rejection-mode consensus across parser outputs."""
    per_voter_vote: dict[str, ErrorVote] = field(default_factory=dict)
    majority_vote: Optional[ErrorVote] = None          # None = no majority
    dissenting_voters: list[str] = field(default_factory=list)
    silent_acceptors: list[str] = field(default_factory=list)  # voted ACCEPT or SILENT_SKIP when majority REJECT
    is_inconclusive: bool = False
    reason: str = ""

    @property
    def total_voters(self) -> int:
        return sum(
            1 for v in self.per_voter_vote.values()
            if v is not ErrorVote.INELIGIBLE
        )


def _vote_for_runner(
    result: RunnerResult,
    input_record_count: int,
) -> ErrorVote:
    """Map a RunnerResult on the mutated seed to an ErrorVote.

    Args:
        result: output of runner.run(transformed_path, fmt).
        input_record_count: record count of the ORIGINAL (valid) seed — so
            we can detect "accepted but silently dropped records".
    """
    if result.error_type == "ineligible":
        return ErrorVote.INELIGIBLE
    if result.error_type == "crash":
        return ErrorVote.CRASH
    if not result.success:
        # Non-crash error: validation failure, malformed input rejection.
        return ErrorVote.REJECT

    # Success. Check whether the parser silently lost records.
    records = _record_count(result)
    if records is None:
        # Parser didn't report record count → assume full accept.
        return ErrorVote.ACCEPT
    if records < input_record_count:
        return ErrorVote.SILENT_SKIP
    return ErrorVote.ACCEPT


def _record_count(result: RunnerResult) -> Optional[int]:
    """Best-effort: extract the record count from a RunnerResult's
    canonical JSON. Returns None if the count can't be determined."""
    cj = result.canonical_json
    if not cj or not isinstance(cj, dict):
        return None
    # Canonical VCF and SAM both have a top-level "records" list.
    recs = cj.get("records")
    if isinstance(recs, list):
        return len(recs)
    # Explicit counter fallback.
    rc = cj.get("record_count")
    if isinstance(rc, int):
        return rc
    return None


def get_error_consensus(
    voter_results: dict[str, RunnerResult],
    input_record_count: int,
) -> ErrorConsensusResult:
    """Compute the rejection-mode consensus verdict.

    Args:
        voter_results: map of parser_name → RunnerResult for the mutated
            (malformed) seed.
        input_record_count: record count of the original (valid) seed.

    Returns:
        ErrorConsensusResult with per-voter vote, majority verdict, and
        dissenters.
    """
    per_voter: dict[str, ErrorVote] = {
        name: _vote_for_runner(r, input_record_count)
        for name, r in voter_results.items()
    }

    eligible_votes = {
        name: v for name, v in per_voter.items()
        if v is not ErrorVote.INELIGIBLE
    }
    total = len(eligible_votes)

    if total == 0:
        return ErrorConsensusResult(
            per_voter_vote=per_voter,
            majority_vote=None,
            is_inconclusive=True,
            reason="No eligible voters",
        )

    # Count each vote type. CRASH and REJECT both signal "parser refused the
    # malformed input" — bucket them together for the majority check so a
    # mix of CRASH + REJECT still counts as a clear "parsers rejected".
    counter = Counter(eligible_votes.values())
    refused_count = counter.get(ErrorVote.REJECT, 0) + counter.get(ErrorVote.CRASH, 0)
    accepted_count = counter.get(ErrorVote.ACCEPT, 0) + counter.get(ErrorVote.SILENT_SKIP, 0)

    majority: Optional[ErrorVote] = None
    reason = ""
    if refused_count > total / 2:
        # Majority said REJECT — pick the more frequent of REJECT vs CRASH
        # for the reported majority_vote label.
        majority = (
            ErrorVote.REJECT
            if counter.get(ErrorVote.REJECT, 0) >= counter.get(ErrorVote.CRASH, 0)
            else ErrorVote.CRASH
        )
        reason = f"{refused_count}/{total} voters rejected the malformed input"
    elif accepted_count > total / 2:
        majority = (
            ErrorVote.ACCEPT
            if counter.get(ErrorVote.ACCEPT, 0) >= counter.get(ErrorVote.SILENT_SKIP, 0)
            else ErrorVote.SILENT_SKIP
        )
        reason = f"{accepted_count}/{total} voters accepted the malformed input"

    # Dissenters: parsers whose vote doesn't match the majority.
    dissenters: list[str] = []
    silent_acceptors: list[str] = []
    if majority is not None:
        refused_set = {ErrorVote.REJECT, ErrorVote.CRASH}
        accepted_set = {ErrorVote.ACCEPT, ErrorVote.SILENT_SKIP}
        majority_set = refused_set if majority in refused_set else accepted_set
        for name, v in eligible_votes.items():
            if v not in majority_set:
                dissenters.append(name)
                if majority in refused_set and v in accepted_set:
                    silent_acceptors.append(name)

    return ErrorConsensusResult(
        per_voter_vote=per_voter,
        majority_vote=majority,
        dissenting_voters=dissenters,
        silent_acceptors=silent_acceptors,
        is_inconclusive=majority is None,
        reason=reason,
    )
