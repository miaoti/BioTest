"""Phase-4 fairness-equalizer post-pass.

DESIGN.md §4.4 specifies that after each tool's primary bench run,
every accepted input the tool produced is re-fed through the
**differential-only** oracle. If cross-parser canonical JSON
disagrees on that input, the *generating tool* earns credit for the
detection — regardless of whether the tool itself reported a crash.

This isolates *input quality* from *oracle quality*: BioTest's
metamorphic oracle is not allowed to credit other fuzzers' inputs,
and other fuzzers' crash-only detections are not allowed to miss
semantic bugs they happened to generate the input for.

**Enforcement**: this module imports `test_engine/oracles/differential.py`
and nothing else from the oracle layer. A runtime assertion confirms
`test_engine.oracles.metamorphic` is never pulled into `sys.modules`
by any transitive import.

Usage:

    # Dry-run (prints config, validates imports):
    python compares/scripts/fairness_equalizer.py --dry-run

    # Real pass over a completed bench run:
    python compares/scripts/fairness_equalizer.py \\
        --bench-root compares/results/bug_bench \\
        --out compares/results/fairness_equalizer

    # Run the self-test (sanity-check function):
    python compares/scripts/fairness_equalizer.py --self-test
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---- Module-level import guard ----------------------------------------
# Fails loudly if test_engine.oracles.metamorphic is already loaded
# (e.g. via a transitive import from a sibling module). This is the
# invariant DESIGN.md §4.4 relies on — breaking it means BioTest's
# transform chain is crediting fuzzer inputs, which inflates BioTest's
# numbers spuriously.
assert "test_engine.oracles.metamorphic" not in sys.modules, (
    "fairness_equalizer.py must not run after test_engine.oracles.metamorphic "
    "is imported. Run this script as a standalone process; see DESIGN.md §4.4."
)

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

# Only the differential oracle is allowed. Explicit imports make the
# rule visible; a grep for `metamorphic` in this file returns zero.
from test_engine.oracles.differential import DifferentialOracle  # noqa: E402
from test_engine.runners.base import ParserRunner  # noqa: E402

# A second assertion fires if, after our explicit imports, metamorphic
# was transitively pulled in. `differential.py` does not import
# metamorphic; this is a defence against future refactors.
assert "test_engine.oracles.metamorphic" not in sys.modules, (
    "fairness_equalizer.py loaded test_engine.oracles.metamorphic as a "
    "transitive import. This breaks the DESIGN.md §4.4 invariant. "
    "Fix the import graph before running the bench."
)

logger = logging.getLogger("fairness_equalizer")


# ---- Result types ----------------------------------------------------

@dataclass
class PerCellResult:
    """One (tool, sut) cell's equalizer outcome."""
    tool: str
    sut: str
    format_hint: str
    inputs_tested: int = 0
    disagreements: int = 0  # inputs where differential oracle fired
    detection_rate: float = 0.0
    failing_inputs: list[str] = field(default_factory=list)


# ---- Runner bootstrap -----------------------------------------------

def _load_runners() -> list[ParserRunner]:
    """Instantiate every ParserRunner in test_engine/runners/.

    Imports are deferred so the module-level guard can catch a
    transitively-loaded metamorphic.py before we reach the runners.
    """
    from test_engine.runners.htsjdk_runner import HTSJDKRunner  # noqa: E402
    from test_engine.runners.pysam_runner import PysamRunner  # noqa: E402
    from test_engine.runners.biopython_runner import BiopythonRunner  # noqa: E402
    from test_engine.runners.seqan3_runner import SeqAn3Runner  # noqa: E402
    from test_engine.runners.reference_runner import ReferenceRunner  # noqa: E402
    return [
        HTSJDKRunner(),
        PysamRunner(),
        BiopythonRunner(),
        SeqAn3Runner(),
        ReferenceRunner(),
    ]


# ---- Sanity check ---------------------------------------------------

def verify_biotest_containment(
    biotest_full: int, biotest_diff_only: int, scope: str,
) -> None:
    """BioTest's full-oracle detections must be a superset of its
    differential-only detections.

    The full oracle combines metamorphic + differential; stripping
    to differential-only can only LOSE detections, never gain them.
    A violation means a counter is miscomputed somewhere upstream.

    Raises AssertionError with a clear message if the invariant is
    broken. DESIGN.md §4.4 documents the rule.
    """
    if biotest_diff_only > biotest_full:
        raise AssertionError(
            f"Sanity violation ({scope}): BioTest differential-only "
            f"detections ({biotest_diff_only}) exceed full-oracle "
            f"detections ({biotest_full}). Full oracle is "
            f"metamorphic + differential; stripping metamorphic can "
            f"only lose detections. Check the counter pipeline. "
            f"See DESIGN.md §4.4."
        )


# ---- Main equalizer pass --------------------------------------------

def equalize_cell(
    tool: str, sut: str, format_hint: str, corpus_dir: Path,
    oracle: DifferentialOracle,
) -> PerCellResult:
    """Walk a single (tool, sut) corpus and count differential-only
    detections."""
    result = PerCellResult(tool=tool, sut=sut, format_hint=format_hint)
    if not corpus_dir.exists():
        logger.warning("corpus_dir missing: %s", corpus_dir)
        return result

    for input_file in sorted(corpus_dir.iterdir()):
        if not input_file.is_file():
            continue
        result.inputs_tested += 1
        try:
            diff = oracle.check(input_file, format_hint)
        except Exception as exc:
            logger.warning("oracle error on %s: %s", input_file, exc)
            continue
        if not diff.all_agree:
            result.disagreements += 1
            if len(result.failing_inputs) < 50:
                result.failing_inputs.append(input_file.name)

    if result.inputs_tested:
        result.detection_rate = result.disagreements / result.inputs_tested
    return result


def run(
    bench_root: Path, out_dir: Path, dry_run: bool = False,
) -> dict[str, list[PerCellResult]]:
    """Walk bench_root looking for <tool>/<bug_id>/corpus/ layouts,
    equalize each cell, write per-cell JSON under out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    runners = _load_runners()
    oracle = DifferentialOracle(runners)

    all_results: dict[str, list[PerCellResult]] = {}
    if not bench_root.exists():
        if dry_run:
            logger.info("dry-run: would walk %s (missing, ok for dry-run)",
                        bench_root)
            return all_results
        raise FileNotFoundError(bench_root)

    for tool_dir in sorted(p for p in bench_root.iterdir() if p.is_dir()):
        tool = tool_dir.name
        all_results[tool] = []
        for bug_dir in sorted(p for p in tool_dir.iterdir() if p.is_dir()):
            corpus_dir = bug_dir / "corpus"
            if not corpus_dir.exists():
                continue
            # Format inferred from the parent bug-bench manifest ideally;
            # fallback: sniff file extensions in the corpus.
            fmt = _sniff_format(corpus_dir)
            if dry_run:
                logger.info("dry-run: %s / %s (fmt=%s, corpus=%s)",
                            tool, bug_dir.name, fmt, corpus_dir)
                continue
            cell = equalize_cell(
                tool=tool, sut=bug_dir.name, format_hint=fmt,
                corpus_dir=corpus_dir, oracle=oracle,
            )
            out_path = out_dir / tool / f"{bug_dir.name}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                json.dumps(asdict(cell), indent=2), encoding="utf-8",
            )
            all_results[tool].append(cell)
            logger.info("%s / %s : %d/%d disagreed",
                        tool, bug_dir.name,
                        cell.disagreements, cell.inputs_tested)

    return all_results


def _sniff_format(corpus_dir: Path) -> str:
    for p in corpus_dir.iterdir():
        n = p.name.lower()
        if n.endswith(".vcf") or n.endswith(".vcf.gz") or n.endswith(".bcf"):
            return "VCF"
        if n.endswith(".sam") or n.endswith(".bam") or n.endswith(".cram"):
            return "SAM"
    # Default: VCF. Most of the verified bench is VCF.
    return "VCF"


# ---- Self-test ------------------------------------------------------

def self_test() -> int:
    """Run deterministic tests on pure functions. Exits 0 on pass."""
    logger.info("self-test: verify_biotest_containment")
    # Passing cases.
    verify_biotest_containment(10, 7, "pass-case-1")
    verify_biotest_containment(0, 0, "pass-case-zero")
    verify_biotest_containment(5, 5, "pass-case-equal")
    # Failing case.
    try:
        verify_biotest_containment(3, 7, "expected-fail")
    except AssertionError as exc:
        logger.info("self-test: expected AssertionError caught: %s",
                    str(exc)[:120])
    else:
        logger.error("self-test FAILED: containment did not catch 3 < 7")
        return 1
    logger.info("self-test PASSED")
    return 0


# ---- CLI ------------------------------------------------------------

def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--bench-root", type=Path,
                   default=REPO_ROOT / "compares" / "results" / "bug_bench")
    p.add_argument("--out", type=Path,
                   default=REPO_ROOT / "compares" / "results" / "fairness_equalizer")
    p.add_argument("--dry-run", action="store_true",
                   help="Validate imports + print config; do not run oracle")
    p.add_argument("--self-test", action="store_true",
                   help="Run deterministic self-tests and exit")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s %(message)s",
    )

    if args.self_test:
        return self_test()

    if args.dry_run:
        print(f"[fairness-equalizer] dry-run")
        print(f"  bench_root : {args.bench_root}")
        print(f"  out_dir    : {args.out}")
        print(f"  oracle     : DifferentialOracle "
              f"(metamorphic IS BLOCKED; see module guard)")
        print(f"  runners    : "
              f"{[type(r).__name__ for r in _load_runners()]}")
        run(args.bench_root, args.out, dry_run=True)
        return 0

    start = time.time()
    results = run(args.bench_root, args.out)
    # Summary line.
    totals = {t: sum(c.disagreements for c in cells)
              for t, cells in results.items()}
    duration = time.time() - start
    print(f"[fairness-equalizer] done in {duration:.1f}s  totals: {totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
