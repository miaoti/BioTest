"""
Phase C Orchestrator: main test loop.

For each enforced MR in the registry:
  For each seed file:
    1. Apply MR transforms -> T(x)
    2. Metamorphic oracle: parse(x) == parse(T(x)) for each parser
    3. Differential oracle: compare all parser outputs on x

Reports failures via the triage system.
"""

from __future__ import annotations

import json
import logging
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from mr_engine.dsl.models import MetamorphicRelation

from .config import MR_REGISTRY_PATH, BUG_REPORTS_DIR
from .generators.dispatch import apply_mr_transforms
from .generators.seeds import SeedCorpus
from .oracles.deep_equal import deep_equal
from .oracles.det_tracker import DETEvent, DETTracker
from .oracles.metamorphic import MetamorphicOracle, OracleResult
from .oracles.differential import DifferentialOracle, DifferentialResult
from .runners.base import ParserRunner, RunnerResult
from .triage.classifier import classify_failure, ClassifiedFailure
from .triage.report_builder import build_bug_report

logger = logging.getLogger(__name__)


@dataclass
class TestSuiteResult:
    """Result of running the full test suite."""
    total_tests: int = 0
    metamorphic_failures: int = 0
    differential_failures: int = 0
    crashes: int = 0
    bug_reports: list[Path] = field(default_factory=list)
    det_tracker: DETTracker = field(default_factory=DETTracker)


def load_registry(path: Path = MR_REGISTRY_PATH) -> dict[str, Any]:
    """Load MR registry JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_test_suite(
    runners: list[ParserRunner],
    registry_path: Path = MR_REGISTRY_PATH,
    seeds_dir: Optional[Path] = None,
    output_dir: Path = BUG_REPORTS_DIR,
    format_filter: Optional[str] = None,
) -> TestSuiteResult:
    """
    Run the full metamorphic + differential test suite.

    Args:
        runners: List of available parser runners.
        registry_path: Path to mr_registry.json.
        seeds_dir: Path to seeds directory (uses default if None).
        output_dir: Path for bug report output.
        format_filter: If set, only test this format ("VCF" or "SAM").

    Returns:
        TestSuiteResult with counts and bug report paths.
    """
    registry = load_registry(registry_path)
    corpus = SeedCorpus(seeds_dir) if seeds_dir else SeedCorpus()
    result = TestSuiteResult()
    output_dir.mkdir(parents=True, exist_ok=True)

    enforced_mrs = registry.get("enforced", [])
    logger.info("Loaded %d enforced MRs from registry", len(enforced_mrs))

    # Filter available runners
    available_runners = [r for r in runners if r.is_available()]
    logger.info("Available runners: %s", [r.name for r in available_runners])

    for mr_dict in enforced_mrs:
        mr_id = mr_dict["mr_id"]
        mr_name = mr_dict["mr_name"]
        scope = mr_dict["scope"]
        fmt = scope.split(".")[0]  # "VCF" from "VCF.header"
        transform_steps = mr_dict["transform_steps"]

        if format_filter and fmt != format_filter.upper():
            continue

        logger.info("Testing MR %s (%s) — scope=%s, transforms=%s",
                     mr_id, mr_name, scope, transform_steps)

        # Get applicable runners and seeds
        applicable = [r for r in available_runners if r.supports(fmt)]
        seeds = corpus.seeds_for_format(fmt)

        if not applicable:
            logger.warning("No runners available for format %s", fmt)
            continue
        if not seeds:
            logger.warning("No seeds available for format %s", fmt)
            continue

        for seed_path in seeds:
            logger.info("  Seed: %s", seed_path.name)

            # Apply transforms
            seed_lines = SeedCorpus.read_lines(seed_path)
            try:
                transformed_lines = apply_mr_transforms(
                    seed_lines, transform_steps, seed=42
                )
            except Exception as e:
                logger.error("Transform failed on %s: %s", seed_path.name, e)
                result.crashes += 1
                continue

            # Write transformed file to temp
            suffix = f".{fmt.lower()}"
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=suffix, delete=False, encoding="utf-8"
            ) as tmp:
                tmp.writelines(transformed_lines)
                transformed_path = Path(tmp.name)

            try:
                # --- Metamorphic oracle (per parser) ---
                for runner in applicable:
                    oracle = MetamorphicOracle(runner)
                    oracle_result = oracle.check(
                        seed_path, transformed_path,
                        mr_id=mr_id, mr_name=mr_name, scope=scope,
                    )
                    result.total_tests += 1

                    # Track DET
                    result.det_tracker.record(DETEvent(
                        mr_id=mr_id,
                        test_type="metamorphic",
                        parser_names=[runner.name],
                        passed=oracle_result.passed,
                        difference_count=len(oracle_result.differences),
                        seed_id=seed_path.name,
                    ))

                    if not oracle_result.passed:
                        result.metamorphic_failures += 1
                        logger.warning(
                            "  METAMORPHIC FAILURE: %s on %s — %d diffs",
                            runner.name, seed_path.name,
                            len(oracle_result.differences),
                        )

                        classified = classify_failure(
                            oracle_result=oracle_result,
                            mr_dict=mr_dict,
                        )
                        bug_path = build_bug_report(
                            classified=classified,
                            seed_path=seed_path,
                            transformed_path=transformed_path,
                            oracle_result=oracle_result,
                            mr_dict=mr_dict,
                            output_dir=output_dir,
                        )
                        result.bug_reports.append(bug_path)

                # --- Differential oracle (across parsers) ---
                if len(applicable) >= 2:
                    diff_oracle = DifferentialOracle(applicable)
                    diff_result = diff_oracle.check(seed_path, fmt)
                    result.total_tests += 1

                    result.det_tracker.record(DETEvent(
                        mr_id=mr_id,
                        test_type="differential",
                        parser_names=[r.name for r in applicable],
                        passed=diff_result.all_agree,
                        difference_count=sum(
                            len(d) for d in diff_result.pairwise_diffs.values()
                        ),
                        seed_id=seed_path.name,
                    ))

                    if not diff_result.all_agree:
                        result.differential_failures += 1
                        logger.warning(
                            "  DIFFERENTIAL FAILURE on %s: %s",
                            seed_path.name,
                            {k: len(v) for k, v in diff_result.pairwise_diffs.items() if v},
                        )

            finally:
                # Clean up temp file
                try:
                    transformed_path.unlink()
                except OSError:
                    pass

    # Summary
    logger.info(
        "Test suite complete: %d tests, %d metamorphic failures, "
        "%d differential failures, %d crashes, DET rate=%.4f",
        result.total_tests, result.metamorphic_failures,
        result.differential_failures, result.crashes,
        result.det_tracker.det_rate,
    )

    return result
