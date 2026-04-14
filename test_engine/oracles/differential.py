"""
Differential Oracle: HTSJDK(x) == pysam(x) == Biopython(x) == SeqAn3(x)

Given the same input file, all applicable parsers must produce
equivalent canonical JSON output. Any disagreement (a DET — Difference
Exposing Test) indicates a cross-implementation bug.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from ..runners.base import ParserRunner, RunnerResult
from .deep_equal import deep_equal

logger = logging.getLogger(__name__)


@dataclass
class DifferentialResult:
    """Result of a differential oracle check."""
    all_agree: bool
    file_path: str
    format_type: str
    parser_results: dict[str, RunnerResult] = field(default_factory=dict)
    pairwise_diffs: dict[str, list[str]] = field(default_factory=dict)
    # key is "parser_a vs parser_b"


class DifferentialOracle:
    """
    Oracle 2: Cross-parser comparison.

    For VCF: HTSJDK vs pysam
    For SAM: HTSJDK vs Biopython vs pysam vs SeqAn3
    """

    def __init__(self, runners: list[ParserRunner]):
        self.runners = runners

    def check(
        self,
        file_path: Path,
        format_type: str,
        float_tol: float = 1e-6,
    ) -> DifferentialResult:
        """
        Parse the input file with all applicable runners and compare pairwise.

        Args:
            file_path: Path to the input file.
            format_type: "VCF" or "SAM".
            float_tol: Float comparison tolerance.

        Returns:
            DifferentialResult with agreement status and pairwise diffs.
        """
        fmt = format_type.upper()

        # Run all applicable parsers
        results: dict[str, RunnerResult] = {}
        for runner in self.runners:
            if runner.supports(fmt) and runner.is_available():
                results[runner.name] = runner.run(file_path, fmt)

        if len(results) < 2:
            logger.warning(
                "Only %d parser(s) available for %s differential testing",
                len(results), fmt,
            )
            return DifferentialResult(
                all_agree=True,  # Can't disagree with < 2 parsers
                file_path=str(file_path),
                format_type=fmt,
                parser_results=results,
            )

        # Pairwise comparison
        pairwise: dict[str, list[str]] = {}
        all_agree = True
        names = sorted(results.keys())

        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a_name, b_name = names[i], names[j]
                a_res, b_res = results[a_name], results[b_name]
                pair_key = f"{a_name} vs {b_name}"

                # If either failed, record as disagreement
                if not a_res.success or not b_res.success:
                    diff_msg = []
                    if not a_res.success:
                        diff_msg.append(f"{a_name} failed: {a_res.stderr}")
                    if not b_res.success:
                        diff_msg.append(f"{b_name} failed: {b_res.stderr}")
                    pairwise[pair_key] = diff_msg
                    all_agree = False
                    continue

                # Compare canonical outputs
                eq, diffs = deep_equal(
                    a_res.canonical_json,
                    b_res.canonical_json,
                    float_tol=float_tol,
                )
                pairwise[pair_key] = diffs

                if not eq:
                    all_agree = False
                    logger.info(
                        "DET found: %s — %d differences",
                        pair_key, len(diffs),
                    )

        return DifferentialResult(
            all_agree=all_agree,
            file_path=str(file_path),
            format_type=fmt,
            parser_results=results,
            pairwise_diffs=pairwise,
        )
