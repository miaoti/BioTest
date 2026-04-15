"""
Phase C Orchestrator: main test loop.

Dual-mode execution:
  - Hypothesis mode (default): uses @given-decorated functions with random
    seed exploration and automatic shrinking on failure.
  - Static mode (fallback): iterates over fixed seed files — used by
    DummyRunners in tests or when Hypothesis strategies are unavailable.

For each enforced MR in the registry:
  1. Apply MR transforms -> T(x)  (with random or fixed seed)
  2. Metamorphic oracle: parse(x) == parse(T(x)) for each parser
  3. Differential oracle: compare all parser outputs on x
  4. On failure: raise AssertionError so Hypothesis can shrink, then triage.
"""

from __future__ import annotations

import json
import logging
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from hypothesis import given, settings, HealthCheck, Phase, assume, Verbosity
from hypothesis import strategies as st

from .config import MR_REGISTRY_PATH, BUG_REPORTS_DIR
from .generators.dispatch import apply_mr_transforms
from .generators.seeds import SeedCorpus
from .generators.strategy_router import get_strategy
from .oracles.deep_equal import deep_equal
from .oracles.det_tracker import DETEvent, DETTracker
from .oracles.metamorphic import MetamorphicOracle, OracleResult
from .oracles.differential import DifferentialOracle, DifferentialResult
from .runners.base import ParserRunner, RunnerResult
from .triage.classifier import classify_failure, ClassifiedFailure
from .triage.report_builder import build_bug_report

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Core test execution for a single (seed_lines, rng_seed) pair
# ---------------------------------------------------------------------------

class _OracleFailure(Exception):
    """Raised inside Hypothesis to trigger shrinking on oracle failure."""
    def __init__(self, diffs: list[str], oracle_result: OracleResult):
        self.diffs = diffs
        self.oracle_result = oracle_result
        super().__init__("\n".join(diffs[:5]))


def _run_single_test(
    seed_path: Path,
    seed_lines: list[str],
    rng_seed: int,
    mr_dict: dict[str, Any],
    applicable: list[ParserRunner],
    result: TestSuiteResult,
    output_dir: Path,
    fmt: str,
) -> None:
    """
    Execute metamorphic + differential oracles for one (seed, rng_seed) pair.

    This is the innermost loop extracted so both Hypothesis and static modes
    can call the same logic. Raises _OracleFailure on metamorphic failure
    when called from Hypothesis mode (so shrinking kicks in).
    """
    mr_id = mr_dict["mr_id"]
    mr_name = mr_dict["mr_name"]
    scope = mr_dict["scope"]
    transform_steps = mr_dict["transform_steps"]

    # Apply transforms with the drawn rng_seed
    try:
        transformed_lines = apply_mr_transforms(
            seed_lines, transform_steps, seed=rng_seed
        )
    except Exception as e:
        logger.error("Transform failed on %s (seed=%d): %s", seed_path.name, rng_seed, e)
        result.crashes += 1
        return

    # Write transformed file to temp
    suffix = f".{fmt.lower()}"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=suffix, delete=False, encoding="utf-8"
    ) as tmp:
        tmp.writelines(transformed_lines)
        transformed_path = Path(tmp.name)

    first_failure: Optional[_OracleFailure] = None

    try:
        # --- Metamorphic oracle (per parser) ---
        for runner in applicable:
            oracle = MetamorphicOracle(runner)
            oracle_result = oracle.check(
                seed_path, transformed_path,
                mr_id=mr_id, mr_name=mr_name, scope=scope,
            )
            result.total_tests += 1

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
                    "  METAMORPHIC FAILURE: %s on %s (seed=%d) -- %d diffs",
                    runner.name, seed_path.name, rng_seed,
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

                # Capture first failure for Hypothesis shrinking
                if first_failure is None:
                    first_failure = _OracleFailure(
                        oracle_result.differences, oracle_result
                    )

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
                    "  DIFFERENTIAL FAILURE on %s (seed=%d): %s",
                    seed_path.name, rng_seed,
                    {k: len(v) for k, v in diff_result.pairwise_diffs.items() if v},
                )

    finally:
        try:
            transformed_path.unlink()
        except OSError:
            pass

    # If we captured a failure, raise it so Hypothesis can shrink
    if first_failure is not None:
        raise first_failure


# ---------------------------------------------------------------------------
# Hypothesis-driven MR test execution
# ---------------------------------------------------------------------------

def _run_mr_with_hypothesis(
    mr_dict: dict[str, Any],
    corpus: SeedCorpus,
    applicable: list[ParserRunner],
    result: TestSuiteResult,
    output_dir: Path,
    fmt: str,
    max_examples: int = 50,
) -> None:
    """
    Run a single MR through Hypothesis with random seed exploration.

    The @given decorator draws (seed_path, lines, rng_seed) from the
    strategy, then _run_single_test does the oracle checks. If the oracle
    fails, _OracleFailure is raised and Hypothesis shrinks the input
    to find the minimal failing case.
    """
    transform_steps = mr_dict["transform_steps"]
    primary_transform = transform_steps[0]
    strategy_factory = get_strategy(primary_transform)

    if strategy_factory is None:
        logger.warning(
            "  No Hypothesis strategy for '%s' — falling back to static seeds",
            primary_transform,
        )
        _run_mr_static(mr_dict, corpus, applicable, result, output_dir, fmt)
        return

    # Build the strategy, passing our corpus
    strategy = strategy_factory(corpus)

    # Define the Hypothesis test function as a closure
    # so it captures the MR context.
    found_failure = False

    @settings(
        max_examples=max_examples,
        phases=[Phase.explicit, Phase.generate, Phase.target, Phase.shrink],
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
        verbosity=Verbosity.quiet,
        deadline=None,
    )
    @given(params=strategy)
    def _hypothesis_test(params: dict) -> None:
        nonlocal found_failure
        seed_path = params["seed_path"]
        lines = params["lines"]
        rng_seed = params["rng_seed"]

        _run_single_test(
            seed_path=seed_path,
            seed_lines=lines,
            rng_seed=rng_seed,
            mr_dict=mr_dict,
            applicable=applicable,
            result=result,
            output_dir=output_dir,
            fmt=fmt,
        )

    # Execute — Hypothesis manages the loop, shrinking, and examples
    try:
        _hypothesis_test()
    except _OracleFailure:
        # Hypothesis has already shrunk to the minimal failing example.
        # The bug report was generated inside _run_single_test.
        found_failure = True
        logger.info(
            "  Hypothesis shrunk MR %s (%s) to minimal failing case",
            mr_dict["mr_id"], mr_dict["mr_name"],
        )
    except Exception as e:
        # Unexpected error from Hypothesis internals
        if "_OracleFailure" in str(type(e).__mro__) or "_OracleFailure" in str(e):
            found_failure = True
        else:
            logger.error("  Hypothesis error for MR %s: %s", mr_dict["mr_id"], e)

    if found_failure:
        logger.info("  MR %s: Hypothesis found and shrunk a failure", mr_dict["mr_id"])
    else:
        logger.info("  MR %s: Hypothesis explored %d examples — no failures",
                     mr_dict["mr_id"], max_examples)


# ---------------------------------------------------------------------------
# Static fallback (for dummy runners and when no strategy exists)
# ---------------------------------------------------------------------------

def _run_mr_static(
    mr_dict: dict[str, Any],
    corpus: SeedCorpus,
    applicable: list[ParserRunner],
    result: TestSuiteResult,
    output_dir: Path,
    fmt: str,
) -> None:
    """
    Run a single MR against all seeds with a fixed rng_seed per seed.

    This is the fallback path used when:
    - No Hypothesis strategy is available for the transform
    - use_hypothesis=False is passed to run_test_suite
    - DummyRunners are used in tests (they need deterministic counts)
    """
    seeds = corpus.seeds_for_format(fmt)
    if not seeds:
        logger.warning("No seeds available for format %s", fmt)
        return

    for i, seed_path in enumerate(seeds):
        logger.info("  Seed: %s", seed_path.name)
        seed_lines = SeedCorpus.read_lines(seed_path)

        # Use a deterministic but varied seed per file (not hardcoded 42)
        rng_seed = hash((mr_dict["mr_id"], seed_path.name, i)) & 0x7FFFFFFF

        try:
            _run_single_test(
                seed_path=seed_path,
                seed_lines=seed_lines,
                rng_seed=rng_seed,
                mr_dict=mr_dict,
                applicable=applicable,
                result=result,
                output_dir=output_dir,
                fmt=fmt,
            )
        except _OracleFailure:
            # In static mode, failures are already recorded inside
            # _run_single_test. Just continue to the next seed.
            pass


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_test_suite(
    runners: list[ParserRunner],
    registry_path: Path = MR_REGISTRY_PATH,
    seeds_dir: Optional[Path] = None,
    output_dir: Path = BUG_REPORTS_DIR,
    format_filter: Optional[str] = None,
    use_hypothesis: bool = False,
    max_examples: int = 50,
) -> TestSuiteResult:
    """
    Run the full metamorphic + differential test suite.

    Args:
        runners: List of available parser runners.
        registry_path: Path to mr_registry.json.
        seeds_dir: Path to seeds directory (uses default if None).
        output_dir: Path for bug report output.
        format_filter: If set, only test this format ("VCF" or "SAM").
        use_hypothesis: If True, use Hypothesis-driven random exploration
                        with automatic shrinking. If False, use static
                        seed loop (deterministic, faster).
        max_examples: Number of Hypothesis examples per MR (default 50).

    Returns:
        TestSuiteResult with counts and bug report paths.
    """
    registry = load_registry(registry_path)
    corpus = SeedCorpus(seeds_dir) if seeds_dir else SeedCorpus()
    result = TestSuiteResult()
    output_dir.mkdir(parents=True, exist_ok=True)

    enforced_mrs = registry.get("enforced", [])
    logger.info("Loaded %d enforced MRs from registry", len(enforced_mrs))

    available_runners = [r for r in runners if r.is_available()]
    logger.info("Available runners: %s", [r.name for r in available_runners])

    mode = "hypothesis" if use_hypothesis else "static"
    logger.info("Execution mode: %s", mode)

    for mr_dict in enforced_mrs:
        mr_id = mr_dict["mr_id"]
        mr_name = mr_dict["mr_name"]
        scope = mr_dict["scope"]
        fmt = scope.split(".")[0]
        transform_steps = mr_dict["transform_steps"]

        if format_filter and fmt != format_filter.upper():
            continue

        logger.info("Testing MR %s (%s) -- scope=%s, transforms=%s",
                     mr_id, mr_name, scope, transform_steps)

        applicable = [r for r in available_runners if r.supports(fmt)]
        if not applicable:
            logger.warning("No runners available for format %s", fmt)
            continue

        if use_hypothesis:
            _run_mr_with_hypothesis(
                mr_dict=mr_dict,
                corpus=corpus,
                applicable=applicable,
                result=result,
                output_dir=output_dir,
                fmt=fmt,
                max_examples=max_examples,
            )
        else:
            _run_mr_static(
                mr_dict=mr_dict,
                corpus=corpus,
                applicable=applicable,
                result=result,
                output_dir=output_dir,
                fmt=fmt,
            )

    logger.info(
        "Test suite complete: %d tests, %d metamorphic failures, "
        "%d differential failures, %d crashes, DET rate=%.4f",
        result.total_tests, result.metamorphic_failures,
        result.differential_failures, result.crashes,
        result.det_tracker.det_rate,
    )

    return result
