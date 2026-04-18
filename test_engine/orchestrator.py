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
from .oracles.consensus import (
    ConsensusResult,
    build_eligibility_map,
    get_consensus_output,
)
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


def _resolve_writer_runner(
    applicable: list[ParserRunner],
    primary_target: str,
) -> Optional[ParserRunner]:
    """Pick the runner that runner-aware transforms (sut_write_roundtrip)
    should dispatch to.

    Precedence:
      1. If `primary_target` matches an applicable runner whose
         `supports_write_roundtrip` is True → that runner.
      2. Else: the first applicable runner with
         `supports_write_roundtrip=True`.
      3. Else: None (transform will gracefully no-op).

    Keeping this resolution in ONE helper means the semantics of "which
    SUT does the writing" live in exactly one place — not spread across
    every runner-aware transform.
    """
    if primary_target:
        for r in applicable:
            if (getattr(r, "name", "") == primary_target
                    and getattr(r, "supports_write_roundtrip", False)):
                return r
    for r in applicable:
        if getattr(r, "supports_write_roundtrip", False):
            return r
    return None


def _run_single_test(
    seed_path: Path,
    seed_lines: list[str],
    rng_seed: int,
    mr_dict: dict[str, Any],
    applicable: list[ParserRunner],
    result: TestSuiteResult,
    output_dir: Path,
    fmt: str,
    primary_target: str = "",
) -> None:
    """
    Execute metamorphic + differential oracles for one (seed, rng_seed) pair.

    Consensus semantics (Majority Voting Oracle):
      - We run ALL applicable parsers on both x (seed) and T(x)
        (transformed), compute a consensus output for each, then score
        the primary_target against consensus.
      - An MR is deemed VIOLATED only when consensus(x) != consensus(T(x))
        across multiple seeds — i.e. the majority thinks T does NOT
        preserve semantics. That decision is centralised in
        quarantine_manager via failure_cause tags; per-event we just
        tag "mr_invalid" when htslib rejects T(x) as malformed or when
        consensus disagrees on x vs T(x).
      - A "non_conformance" bug against the primary is logged when the
        primary disagrees with consensus on one side but matches on the
        other — this is a REAL bug report on the SUT, not on the MR.
      - An "inconclusive" tag is dropped on tests where consensus has
        no majority and no htslib tie-breaker; these do not count for
        or against anybody.
    """
    mr_id = mr_dict["mr_id"]
    mr_name = mr_dict["mr_name"]
    scope = mr_dict["scope"]
    transform_steps = mr_dict["transform_steps"]

    # Resolve the runner hook for runner-aware transforms (currently
    # only `sut_write_roundtrip`). Rules:
    #   1. Prefer the primary_target runner if it supports write_roundtrip.
    #   2. Otherwise fall back to the first applicable runner that does.
    #   3. If none, leave the hook as None — sut_write_roundtrip gracefully
    #      no-ops and returns the input unchanged.
    runner_hook = _resolve_writer_runner(applicable, primary_target)

    # Apply transforms with the drawn rng_seed. `format_context=fmt` is
    # threaded through so format-aware transforms (currently
    # `sut_write_roundtrip`) can pick the right writer — VCF or SAM —
    # without hardcoding either.
    try:
        transformed_lines = apply_mr_transforms(
            seed_lines, transform_steps, seed=rng_seed,
            runner_hook=runner_hook,
            format_context=fmt,
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
        # --- Collect every runner's output on x and T(x) once,
        #     for use by BOTH the per-parser metamorphic check AND the
        #     consensus-based differential oracle. ---
        results_x: dict[str, RunnerResult] = {}
        results_tx: dict[str, RunnerResult] = {}
        for runner in applicable:
            results_x[runner.name] = runner.run(seed_path, fmt)
            results_tx[runner.name] = runner.run(transformed_path, fmt)

        # Format-aware eligibility: consensus.py drops any parser whose
        # supported_formats excludes `fmt`, OR whose RunnerResult carries
        # error_type="ineligible". Ineligible parsers are SILENT — they
        # do not inflate the vote pool and cannot flip a majority.
        eligibility = build_eligibility_map(applicable)
        consensus_x = get_consensus_output(
            results_x, format_context=fmt, eligibility_map=eligibility,
        )
        consensus_tx = get_consensus_output(
            results_tx, format_context=fmt, eligibility_map=eligibility,
        )
        if consensus_x.ineligible_parsers or consensus_tx.ineligible_parsers:
            logger.debug(
                "Format-aware filter (%s): ineligible = %s",
                fmt, sorted(set(consensus_x.ineligible_parsers)
                            | set(consensus_tx.ineligible_parsers)),
            )

        # The MR's own validity verdict: does the majority agree that
        # T preserves semantics? If consensus exists on both sides and
        # consensus(x) != consensus(T(x)), the MR itself is the bug.
        mr_invalid_by_consensus = (
            not consensus_x.is_inconclusive
            and not consensus_tx.is_inconclusive
            and consensus_x.consensus_value is not None
            and consensus_tx.consensus_value is not None
            and not deep_equal(consensus_x.consensus_value, consensus_tx.consensus_value)[0]
        )
        mr_invalid_by_htslib = consensus_tx.htslib_rejected_as_invalid

        # --- Metamorphic oracle (per parser), scored against consensus ---
        for runner in applicable:
            res_x = results_x[runner.name]
            res_tx = results_tx[runner.name]
            result.total_tests += 1

            # Classify using already-collected results, so we don't re-run parsers.
            oracle_result, failure_cause = _classify_metamorphic(
                runner_name=runner.name,
                res_x=res_x,
                res_tx=res_tx,
                consensus_x=consensus_x,
                consensus_tx=consensus_tx,
                mr_invalid=mr_invalid_by_consensus or mr_invalid_by_htslib,
                mr_id=mr_id,
                mr_name=mr_name,
            )

            _ft = None
            if not oracle_result.passed:
                _ft = oracle_result.error_type or "metamorphic"

            result.det_tracker.record(DETEvent(
                mr_id=mr_id,
                test_type="metamorphic",
                parser_names=[runner.name],
                passed=oracle_result.passed,
                difference_count=len(oracle_result.differences),
                seed_id=seed_path.name,
                failure_type=_ft,
                failure_cause=failure_cause,
                primary_target=primary_target or None,
            ))

            if not oracle_result.passed:
                result.metamorphic_failures += 1
                logger.warning(
                    "  METAMORPHIC FAILURE [%s]: %s on %s (seed=%d) -- %d diffs",
                    failure_cause or "unknown", runner.name, seed_path.name, rng_seed,
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

                # Only raise for Hypothesis shrinking if this is a
                # primary-target failure AGAINST consensus — shrinking
                # a non-primary bug wastes budget.
                is_primary = (not primary_target) or runner.name == primary_target
                should_shrink = is_primary and failure_cause in (
                    "against_consensus", "non_conformance", "crash", "timeout",
                )
                if should_shrink and first_failure is None:
                    first_failure = _OracleFailure(
                        oracle_result.differences, oracle_result
                    )

        # --- Differential oracle (across parsers) on the ORIGINAL seed ---
        if len(applicable) >= 2:
            pairwise = {}
            names = sorted(results_x.keys())
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    a, b = names[i], names[j]
                    a_res, b_res = results_x[a], results_x[b]
                    key = f"{a} vs {b}"
                    if not a_res.success or not b_res.success:
                        msg = []
                        if not a_res.success:
                            msg.append(f"{a} failed: {a_res.stderr}")
                        if not b_res.success:
                            msg.append(f"{b} failed: {b_res.stderr}")
                        pairwise[key] = msg
                        continue
                    _, diffs = deep_equal(a_res.canonical_json, b_res.canonical_json)
                    pairwise[key] = diffs

            diff_all_agree = (
                not consensus_x.is_inconclusive
                and not consensus_x.dissenting_voters
                and not consensus_x.failing_parsers
            )

            diff_cause = None
            if not diff_all_agree:
                if consensus_x.is_inconclusive:
                    diff_cause = "inconclusive"
                else:
                    diff_cause = "against_consensus"

            result.total_tests += 1
            result.det_tracker.record(DETEvent(
                mr_id=mr_id,
                test_type="differential",
                parser_names=[r.name for r in applicable],
                passed=diff_all_agree,
                difference_count=sum(len(d) for d in pairwise.values()),
                seed_id=seed_path.name,
                failure_type="differential" if not diff_all_agree else None,
                failure_cause=diff_cause,
                primary_target=primary_target or None,
            ))

            if not diff_all_agree:
                result.differential_failures += 1
                logger.warning(
                    "  DIFFERENTIAL [%s] on %s (seed=%d): consensus=%s, dissent=%s",
                    diff_cause, seed_path.name, rng_seed,
                    consensus_x.winning_voters, consensus_x.dissenting_voters,
                )

    finally:
        try:
            transformed_path.unlink()
        except OSError:
            pass

    # If we captured a failure, raise it so Hypothesis can shrink
    if first_failure is not None:
        raise first_failure


def _classify_metamorphic(
    runner_name: str,
    res_x: RunnerResult,
    res_tx: RunnerResult,
    consensus_x: ConsensusResult,
    consensus_tx: ConsensusResult,
    mr_invalid: bool,
    mr_id: str,
    mr_name: str,
) -> tuple[OracleResult, Optional[str]]:
    """Score one parser's (x, T(x)) pair against consensus.

    Returns (oracle_result, failure_cause) where failure_cause is one of
    the values documented on DETEvent.
    """
    # Parse failures dominate.
    if not res_x.success:
        return OracleResult(
            passed=False, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
            error_type=res_x.error_type or "crash",
            differences=[f"Original parse failed: {res_x.stderr}"],
            original_result=res_x, transformed_result=res_tx,
        ), res_x.error_type or "crash"

    if not res_tx.success:
        # If htslib rejected T(x) as invalid, the MR is the bug, not the parser.
        cause = "mr_invalid" if mr_invalid else (res_tx.error_type or "crash")
        return OracleResult(
            passed=False, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
            error_type=res_tx.error_type or "crash",
            differences=[f"Transformed parse failed: {res_tx.stderr}"],
            original_result=res_x, transformed_result=res_tx,
        ), cause

    # If htslib / consensus says T is not semantics-preserving, the MR
    # itself is the bug regardless of what this parser produced.
    if mr_invalid:
        return OracleResult(
            passed=False, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
            error_type="metamorphic",
            differences=[
                "MR transform deemed non-semantics-preserving by consensus / htslib"
            ],
            original_result=res_x, transformed_result=res_tx,
        ), "mr_invalid"

    matches_cx = consensus_x.parser_matches_consensus(runner_name)
    matches_ctx = consensus_tx.parser_matches_consensus(runner_name)

    # Inconclusive consensus on either side: do not punish anyone.
    if consensus_x.is_inconclusive or consensus_tx.is_inconclusive:
        # Still check the classical invariant as a last resort: if the
        # parser itself disagrees with itself across x and T(x), that's
        # still a real metamorphic violation to report.
        is_equal, diffs = deep_equal(res_x.canonical_json, res_tx.canonical_json)
        if is_equal:
            return OracleResult(
                passed=True, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
                original_result=res_x, transformed_result=res_tx,
            ), None
        return OracleResult(
            passed=False, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
            error_type="metamorphic", differences=diffs,
            original_result=res_x, transformed_result=res_tx,
        ), "inconclusive"

    # Normal consensus path.
    if matches_cx and matches_ctx:
        return OracleResult(
            passed=True, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
            original_result=res_x, transformed_result=res_tx,
        ), None

    # Disagreed with consensus on exactly one side: conformance bug in
    # this parser specific to that input.
    if matches_cx != matches_ctx:
        # Build a diff summary against consensus for the bug report.
        bad_side = "T(x)" if not matches_ctx else "x"
        consensus_val = (
            consensus_tx.consensus_value if not matches_ctx else consensus_x.consensus_value
        )
        actual_val = res_tx.canonical_json if not matches_ctx else res_x.canonical_json
        _, diffs = deep_equal(consensus_val, actual_val)
        return OracleResult(
            passed=False, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
            error_type="metamorphic",
            differences=[f"Non-conformance on {bad_side}: {len(diffs)} diffs vs consensus"]
                + diffs[:20],
            original_result=res_x, transformed_result=res_tx,
        ), "non_conformance"

    # Disagreed with consensus on BOTH sides: against_consensus. This is
    # the strongest "this parser has a bug" signal.
    _, diffs = deep_equal(consensus_tx.consensus_value, res_tx.canonical_json)
    return OracleResult(
        passed=False, mr_id=mr_id, mr_name=mr_name, parser_name=runner_name,
        error_type="metamorphic",
        differences=[f"Disagrees with consensus on both x and T(x)"] + diffs[:20],
        original_result=res_x, transformed_result=res_tx,
    ), "against_consensus"


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
    primary_target: str = "",
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
    strategy_factory = get_strategy(primary_transform, fmt=fmt)

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
            primary_target=primary_target,
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
    primary_target: str = "",
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
                primary_target=primary_target,
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
    primary_target: str = "",
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
                primary_target=primary_target,
            )
        else:
            _run_mr_static(
                mr_dict=mr_dict,
                corpus=corpus,
                applicable=applicable,
                result=result,
                output_dir=output_dir,
                fmt=fmt,
                primary_target=primary_target,
            )

    logger.info(
        "Test suite complete: %d tests, %d metamorphic failures, "
        "%d differential failures, %d crashes, DET rate=%.4f",
        result.total_tests, result.metamorphic_failures,
        result.differential_failures, result.crashes,
        result.det_tracker.det_rate,
    )

    return result
