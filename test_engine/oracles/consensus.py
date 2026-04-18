"""
Majority-voting consensus across parser outputs.

Given N parsers' canonical JSON for the *same* input file, decide the
"correct answer" by vote, not by pairwise diff. A 3-of-4 majority means
the 1 dissenter has a conformance bug — we should NOT punish the MR.

Roles (authoritative when present, regular vote otherwise):
  - "htslib"   → samtools/bcftools, the upstream hts-specs reference CLI.
                 Treated as TIE-BREAKER (Gold Standard).
  - "htsjdk"   → Broad's JVM library. Independent implementation; regular vote.
  - "pysam"    → Python bindings over libhts. Regular vote.
  - "biopython"→ Pure-Python parser. Regular vote.
  - "seqan3"   → SeqAn3 C++ library (SAM-only). Regular vote.
  - "reference"→ Our own text normalizer. EXCLUDED from consensus voting so
                 we never let the framework's own parser vote for itself;
                 it remains useful for the metamorphic per-parser oracle.

Decision rules:
  1. Group outputs by deep-equal semantic equivalence → vote buckets.
  2. The bucket with strictly > N/2 votes wins → consensus = its value.
  3. On a tie (no strict majority):
       a. If htslib is in one of the tied buckets, that bucket wins.
       b. Otherwise, result is INCONCLUSIVE — do NOT fail the test.
  4. If any voter produced an error/crash, it does NOT vote but is
     recorded in `failing_parsers`. If htslib specifically errors AND
     returned a parse_error with stderr mentioning "invalid",
     `htslib_rejected_as_invalid` is set — strong signal the input is
     semantically malformed (used by quarantine to demote the MR).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from ..runners.base import RunnerResult
from .deep_equal import deep_equal


# Parsers whose vote is considered authoritative in a tie.
AUTHORITATIVE_PARSERS: tuple[str, ...] = ("htslib",)

# Parsers excluded from consensus voting entirely (framework-internal).
# Historically "reference" (our Python text normalizer) was listed here
# to avoid it "voting for itself". But the reference normalizer is a
# genuinely independent implementation — SUTs like htsjdk/pysam/htslib
# don't share its code path. The user-facing verification spec (Step 4)
# explicitly requires reference to vote on VCF runs alongside the real
# SUTs, so the exclusion set is empty by default. If a new *truly*
# framework-internal runner ever appears (e.g. the canonical harness
# used as an internal sanity check), add its name here.
EXCLUDED_FROM_CONSENSUS: frozenset[str] = frozenset()


@dataclass
class ConsensusResult:
    """Outcome of a majority-voting consensus across parser outputs."""
    consensus_value: Optional[dict[str, Any]]     # canonical JSON, or None if inconclusive
    is_inconclusive: bool
    winning_voters: list[str] = field(default_factory=list)     # parsers that produced consensus_value
    dissenting_voters: list[str] = field(default_factory=list)  # parsers that disagreed
    failing_parsers: list[str] = field(default_factory=list)    # crashed/errored (didn't vote)
    ineligible_parsers: list[str] = field(default_factory=list) # format-incompatible — SILENT, no vote
    vote_buckets: list[list[str]] = field(default_factory=list) # each bucket = list of parser names
    htslib_rejected_as_invalid: bool = False                     # htslib errored with "invalid" — MR likely malformed
    reason: str = ""

    @property
    def total_voters(self) -> int:
        return len(self.winning_voters) + len(self.dissenting_voters)

    def parser_matches_consensus(self, parser_name: str) -> Optional[bool]:
        """Return True/False if parser voted and matched consensus, None if it didn't vote.

        Ineligible and failing parsers BOTH return None — only parsers
        that successfully produced canonical JSON have a binary verdict.
        """
        if parser_name in self.winning_voters:
            return True
        if parser_name in self.dissenting_voters:
            return False
        return None

    def parser_is_ineligible(self, parser_name: str) -> bool:
        """True when the parser was dropped before voting (format mismatch)."""
        return parser_name in self.ineligible_parsers


def get_consensus_output(
    outputs: dict[str, RunnerResult],
    format_context: str = "",
    eligibility_map: Optional[dict[str, set[str]]] = None,
    float_tol: float = 1e-6,
) -> ConsensusResult:
    """
    Compute majority-vote consensus across FORMAT-ELIGIBLE parser outputs.

    Format-Aware Eligibility (the "silent voter" rule):
      Before anything else, we drop any parser whose output cannot
      legitimately vote on the current format. A parser is INELIGIBLE
      when ANY of these is true:
        (a) Its RunnerResult carries `error_type="ineligible"` — the
            runner itself knew it couldn't handle the format.
        (b) `format_context` is set AND `eligibility_map` explicitly
            declares this parser does NOT support that format.
      Ineligible parsers appear under `ineligible_parsers` for logging
      but contribute zero to vote buckets, majorities, or tie-breaking.
      A SAM-only parser like biopython or seqan3 is therefore SILENT
      during VCF runs — it cannot accidentally flip a 3/4 consensus
      into a 3/5 no-majority by adding a phantom "different" vote.

    Args:
        outputs: {parser_name: RunnerResult}. Names in
                 EXCLUDED_FROM_CONSENSUS are also ignored (framework
                 parsers like "reference" that must not vote for
                 themselves).
        format_context: "VCF" or "SAM" — the format of the current
                        input file. Omit to disable the capability
                        filter and let every provided runner vote.
        eligibility_map: {parser_name: {"VCF", "SAM", ...}} — the
                         capability declarations. Built from the
                         runner pool's `supported_formats` attribute
                         (see test_engine/oracles/consensus.py
                         `build_eligibility_map`).
        float_tol: Float tolerance used by deep_equal when bucketing
                   votes.

    Returns:
        ConsensusResult. Always non-null, but `consensus_value` is None
        when `is_inconclusive=True`.
    """
    fmt = (format_context or "").upper()
    caps = eligibility_map or {}

    failing: list[str] = []
    ineligible: list[str] = []
    voters: dict[str, dict[str, Any]] = {}
    htslib_invalid = False

    for name, res in outputs.items():
        if name in EXCLUDED_FROM_CONSENSUS:
            continue

        # ---- Eligibility gate (two ways to be ineligible) ----
        # 1. The runner self-reported ineligibility.
        if res.error_type == "ineligible":
            ineligible.append(name)
            continue
        # 2. Capability map says this parser doesn't support the format.
        if fmt and name in caps and fmt not in caps[name]:
            ineligible.append(name)
            continue

        if not res.success or res.canonical_json is None:
            failing.append(name)
            # Reliability guard: htslib saying "invalid format" → MR likely malformed.
            # htslib-specific, so only evaluated for the htslib SUT.
            if name == "htslib":
                err = (res.stderr or "").lower()
                if res.error_type == "parse_error" or "invalid" in err or "malformed" in err:
                    htslib_invalid = True
            continue
        voters[name] = res.canonical_json

    if not voters:
        return ConsensusResult(
            consensus_value=None,
            is_inconclusive=True,
            failing_parsers=failing,
            ineligible_parsers=sorted(ineligible),
            htslib_rejected_as_invalid=htslib_invalid,
            reason="no successful voters",
        )

    # Bucket voters by semantic equivalence.
    bucket_values: list[dict[str, Any]] = []
    bucket_voters: list[list[str]] = []
    for name, value in voters.items():
        placed = False
        for idx, existing in enumerate(bucket_values):
            eq, _ = deep_equal(existing, value, float_tol=float_tol)
            if eq:
                bucket_voters[idx].append(name)
                placed = True
                break
        if not placed:
            bucket_values.append(value)
            bucket_voters.append([name])

    # Sort buckets by size desc, with authoritative parsers as tiebreaker.
    def _rank(bucket: list[str]) -> tuple[int, int]:
        return (len(bucket), sum(1 for n in bucket if n in AUTHORITATIVE_PARSERS))

    order = sorted(range(len(bucket_voters)), key=lambda i: _rank(bucket_voters[i]), reverse=True)
    top_idx = order[0]
    top_voters = bucket_voters[top_idx]
    top_value = bucket_values[top_idx]
    total = len(voters)

    # Strict majority wins outright.
    if len(top_voters) * 2 > total:
        dissenting = [n for i, bucket in enumerate(bucket_voters) if i != top_idx for n in bucket]
        return ConsensusResult(
            consensus_value=top_value,
            is_inconclusive=False,
            winning_voters=sorted(top_voters),
            dissenting_voters=sorted(dissenting),
            failing_parsers=failing,
            ineligible_parsers=sorted(ineligible),
            vote_buckets=[sorted(b) for b in bucket_voters],
            htslib_rejected_as_invalid=htslib_invalid,
            reason=f"majority {len(top_voters)}/{total}",
        )

    # No strict majority. Check for authoritative tie-breaker.
    authoritative_buckets = [
        i for i, b in enumerate(bucket_voters)
        if any(n in AUTHORITATIVE_PARSERS for n in b)
    ]
    if len(authoritative_buckets) == 1:
        idx = authoritative_buckets[0]
        winners = bucket_voters[idx]
        dissenting = [n for i, b in enumerate(bucket_voters) if i != idx for n in b]
        return ConsensusResult(
            consensus_value=bucket_values[idx],
            is_inconclusive=False,
            winning_voters=sorted(winners),
            dissenting_voters=sorted(dissenting),
            failing_parsers=failing,
            ineligible_parsers=sorted(ineligible),
            vote_buckets=[sorted(b) for b in bucket_voters],
            htslib_rejected_as_invalid=htslib_invalid,
            reason=f"htslib tie-breaker ({len(winners)}/{total})",
        )

    # No authoritative tie-breaker — inconclusive.
    return ConsensusResult(
        consensus_value=None,
        is_inconclusive=True,
        winning_voters=[],
        dissenting_voters=sorted(voters.keys()),
        failing_parsers=failing,
        ineligible_parsers=sorted(ineligible),
        vote_buckets=[sorted(b) for b in bucket_voters],
        htslib_rejected_as_invalid=htslib_invalid,
        reason=f"no majority, no tie-breaker ({len(bucket_voters)}-way split)",
    )


def build_eligibility_map(runners: list) -> dict[str, set[str]]:
    """Build a {parser_name: supported_formats} map from a runner pool.

    Convenience helper so callers can pass the map straight into
    `get_consensus_output(eligibility_map=...)`. Any runner without a
    `supported_formats` property is silently skipped (the eligibility
    filter then falls back to RunnerResult.error_type==ineligible).
    """
    caps: dict[str, set[str]] = {}
    for r in runners:
        name = getattr(r, "name", None)
        formats = getattr(r, "supported_formats", None)
        if name and formats:
            caps[name] = {f.upper() for f in formats}
    return caps
