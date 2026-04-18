"""
Differential Oracle: majority-vote consensus across parser outputs.

Given the same input file, all applicable parsers must produce
equivalent canonical JSON output. This oracle does NOT naively flip
all_agree=False on any pairwise diff — that rule would demote a good
MR the moment one auxiliary SUT has a bug. Instead we compute a
majority-vote CONSENSUS (see test_engine/oracles/consensus.py) and
report per-parser conformance against it.

A primary SUT "non-conformance" bug is what it means to be in the
dissenting bucket: the primary produced a canonical JSON that the
majority (or the htslib tie-breaker) disagrees with. The MR itself is
only held responsible when the consensus is INCONCLUSIVE or when
htslib rejected the input as malformed.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ..runners.base import ParserRunner, RunnerResult
from .consensus import (
    ConsensusResult,
    build_eligibility_map,
    get_consensus_output,
)
from .deep_equal import deep_equal

logger = logging.getLogger(__name__)


@dataclass
class DifferentialResult:
    """Result of a differential oracle check.

    `all_agree` is True iff every applicable parser voted into the same
    consensus bucket (including a trivial 1-voter case). `pairwise_diffs`
    is kept for diagnostic logging — it is NOT what drives the
    pass/fail classification any more.
    """
    all_agree: bool
    file_path: str
    format_type: str
    parser_results: dict[str, RunnerResult] = field(default_factory=dict)
    pairwise_diffs: dict[str, list[str]] = field(default_factory=dict)
    consensus: Optional[ConsensusResult] = None


class DifferentialOracle:
    """Oracle 2: cross-parser agreement, scored by majority vote."""

    def __init__(self, runners: list[ParserRunner]):
        self.runners = runners

    def check(
        self,
        file_path: Path,
        format_type: str,
        float_tol: float = 1e-6,
    ) -> DifferentialResult:
        fmt = format_type.upper()

        # Run all applicable parsers.
        results: dict[str, RunnerResult] = {}
        for runner in self.runners:
            if runner.supports(fmt) and runner.is_available():
                results[runner.name] = runner.run(file_path, fmt)

        # With < 2 parsers, there's nothing to disagree about.
        if len(results) < 2:
            logger.warning(
                "Only %d parser(s) available for %s differential testing",
                len(results), fmt,
            )
            return DifferentialResult(
                all_agree=True,
                file_path=str(file_path),
                format_type=fmt,
                parser_results=results,
            )

        # Build eligibility map from the full runner pool (not just the
        # .supports(fmt)-filtered subset) so the consensus oracle can
        # double-check any unexpected cross-format result.
        eligibility = build_eligibility_map(self.runners)
        consensus = get_consensus_output(
            results,
            format_context=fmt,
            eligibility_map=eligibility,
            float_tol=float_tol,
        )

        # Keep pairwise diffs for diagnostic output — but use consensus
        # to decide all_agree, not pairwise results.
        pairwise = _pairwise_diffs(results, float_tol)

        all_agree = (
            not consensus.is_inconclusive
            and not consensus.dissenting_voters
            and not consensus.failing_parsers
        )

        if consensus.is_inconclusive:
            logger.info(
                "Differential INCONCLUSIVE on %s: %s",
                file_path.name, consensus.reason,
            )
        elif consensus.dissenting_voters:
            logger.info(
                "Differential disagreement on %s: consensus=%s, dissenting=%s",
                file_path.name, consensus.winning_voters, consensus.dissenting_voters,
            )

        return DifferentialResult(
            all_agree=all_agree,
            file_path=str(file_path),
            format_type=fmt,
            parser_results=results,
            pairwise_diffs=pairwise,
            consensus=consensus,
        )


def _pairwise_diffs(
    results: dict[str, RunnerResult],
    float_tol: float,
) -> dict[str, list[str]]:
    """Build the legacy pairwise-diff map for bug-report diagnostics.

    This is no longer the source of truth for pass/fail — consensus is.
    It remains useful for humans reading a bug report who want to see
    exactly where two parsers disagree.
    """
    pairwise: dict[str, list[str]] = {}
    names = sorted(results.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a_name, b_name = names[i], names[j]
            a_res, b_res = results[a_name], results[b_name]
            key = f"{a_name} vs {b_name}"

            if not a_res.success or not b_res.success:
                msg: list[str] = []
                if not a_res.success:
                    msg.append(f"{a_name} failed: {a_res.stderr}")
                if not b_res.success:
                    msg.append(f"{b_name} failed: {b_res.stderr}")
                pairwise[key] = msg
                continue

            _, diffs = deep_equal(
                a_res.canonical_json, b_res.canonical_json,
                float_tol=float_tol,
            )
            pairwise[key] = diffs
    return pairwise
