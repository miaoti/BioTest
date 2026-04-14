"""
Failure classification: categorize test failures into 4 types.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from ..oracles.metamorphic import OracleResult


class FailureType(str, Enum):
    SPEC_VIOLATION = "spec_violation"
    PARSER_DISAGREEMENT = "parser_disagreement"
    CRASH = "crash"
    METAMORPHIC_VIOLATION = "metamorphic_violation"


@dataclass
class ClassifiedFailure:
    """A classified test failure."""
    failure_type: FailureType
    severity: str               # "CRITICAL" | "WARNING"
    mr_id: str
    mr_name: str
    parser_name: str
    description: str
    differences: list[str]


def classify_failure(
    oracle_result: OracleResult,
    mr_dict: dict[str, Any],
) -> ClassifiedFailure:
    """
    Classify a metamorphic oracle failure.

    Classification logic:
    - CRASH: parser threw exception or timed out
    - METAMORPHIC_VIOLATION: same parser, different results for x and T(x)
    """
    mr_id = mr_dict["mr_id"]
    mr_name = mr_dict["mr_name"]

    if oracle_result.error_type in ("crash", "timeout"):
        return ClassifiedFailure(
            failure_type=FailureType.CRASH,
            severity="CRITICAL",
            mr_id=mr_id,
            mr_name=mr_name,
            parser_name=oracle_result.parser_name,
            description=f"Parser {oracle_result.parser_name} "
                        f"{'crashed' if oracle_result.error_type == 'crash' else 'timed out'}",
            differences=oracle_result.differences,
        )

    return ClassifiedFailure(
        failure_type=FailureType.METAMORPHIC_VIOLATION,
        severity="CRITICAL",
        mr_id=mr_id,
        mr_name=mr_name,
        parser_name=oracle_result.parser_name,
        description=f"Metamorphic violation: {oracle_result.parser_name} "
                    f"produced different output for original and transformed input "
                    f"(MR: {mr_name})",
        differences=oracle_result.differences,
    )
