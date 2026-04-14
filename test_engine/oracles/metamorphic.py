"""
Metamorphic Oracle: semantic(parse(x)) == semantic(parse(T(x)))

For a single parser, the original seed and the semantics-preserving
transformed variant must produce equivalent canonical JSON output.
If they differ, the parser has a bug in handling that invariant.
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
class OracleResult:
    """Result of a single metamorphic oracle check."""
    passed: bool
    mr_id: str
    mr_name: str
    parser_name: str
    differences: list[str] = field(default_factory=list)
    error_type: Optional[str] = None    # "crash" | "timeout" | None
    original_result: Optional[RunnerResult] = None
    transformed_result: Optional[RunnerResult] = None


class MetamorphicOracle:
    """
    Oracle 1: For a single parser, verify that semantics-preserving
    transforms produce equivalent canonical output.
    """

    def __init__(self, runner: ParserRunner):
        self.runner = runner

    def check(
        self,
        seed_path: Path,
        transformed_path: Path,
        mr_id: str,
        mr_name: str,
        scope: str,
        float_tol: float = 1e-6,
    ) -> OracleResult:
        """
        Parse both seed and transformed file, compare canonical JSON.

        Args:
            seed_path: Path to original seed file.
            transformed_path: Path to transformed file T(x).
            mr_id: The MR's deterministic hash ID.
            mr_name: Human-readable MR name.
            scope: "VCF.header" | "VCF.record" | "SAM.header" | "SAM.record"
            float_tol: Tolerance for float comparison.

        Returns:
            OracleResult with pass/fail and difference details.
        """
        fmt = scope.split(".")[0]  # "VCF" from "VCF.header"

        result_x = self.runner.run(seed_path, fmt)
        result_Tx = self.runner.run(transformed_path, fmt)

        # If either parse failed, report as crash/error
        if not result_x.success:
            return OracleResult(
                passed=False,
                mr_id=mr_id,
                mr_name=mr_name,
                parser_name=self.runner.name,
                error_type=result_x.error_type or "crash",
                differences=[f"Original parse failed: {result_x.stderr}"],
                original_result=result_x,
                transformed_result=result_Tx,
            )

        if not result_Tx.success:
            return OracleResult(
                passed=False,
                mr_id=mr_id,
                mr_name=mr_name,
                parser_name=self.runner.name,
                error_type=result_Tx.error_type or "crash",
                differences=[f"Transformed parse failed: {result_Tx.stderr}"],
                original_result=result_x,
                transformed_result=result_Tx,
            )

        # Compare canonical outputs
        is_equal, diffs = deep_equal(
            result_x.canonical_json,
            result_Tx.canonical_json,
            float_tol=float_tol,
        )

        if not is_equal:
            logger.info(
                "Metamorphic violation: MR %s (%s) on %s — %d differences",
                mr_id, mr_name, self.runner.name, len(diffs),
            )

        return OracleResult(
            passed=is_equal,
            mr_id=mr_id,
            mr_name=mr_name,
            parser_name=self.runner.name,
            differences=diffs,
            original_result=result_x,
            transformed_result=result_Tx,
        )
