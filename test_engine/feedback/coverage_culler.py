"""Per-file coverage measurement for the corpus-keeper culler (Rank 8b).

`CorpusKeeper.cull_by_coverage` accepts a ``measure_lines(path) ->
frozenset[(file, line)]`` callback. This module builds that callback
for each supported primary-target SUT.

MVP scope: Python SUTs (vcfpy, biopython) only — coverage.py supports
in-process programmatic ``Coverage()`` instances cheaply, so per-file
measurement adds ~50-200 ms per file (acceptable: the full Phase D
iteration is minutes).

Future work: JaCoCo (htsjdk), gcovr (seqan3), llvm-cov (noodles) would
each need a per-file driver — feasible but each requires spawning an
instrumented subprocess with a fresh coverage destination per file
(~hundreds of ms per file from subprocess overhead alone). Those
backends raise ``NotImplementedError`` here; callers should check
``primary_target`` against ``SUPPORTED_PYTHON_SUTS`` before invoking
the culler.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Primary-target SUT names for which a measurer is implemented today.
SUPPORTED_PYTHON_SUTS = frozenset({"vcfpy", "biopython"})

# Source-package whitelist per SUT. Mirrors what
# `coverage_collector.CoveragePyCollector` uses for batch reporting,
# kept narrow so the measurer doesn't trace third-party imports.
_SUT_SOURCE_PACKAGES: dict[str, tuple[str, ...]] = {
    "vcfpy": ("vcfpy",),
    "biopython": ("Bio.AlignIO", "Bio.SeqIO"),
}


MeasureLinesFn = Callable[[Path], "frozenset[tuple[str, int]]"]


def build_python_measurer(
    sut_name: str,
    fmt: str,
    timeout_s: float = 30.0,
) -> MeasureLinesFn:
    """Return a callable that runs ``sut_name``'s parser on one file
    under a fresh ``coverage.Coverage()`` instance.

    The callable returns a ``frozenset`` of ``(absolute_source_file,
    line_number)`` pairs.

    Failure semantics:
      * Runner raised inside ``runner.run()`` → return whatever
        coverage was collected before the raise. A parse error that
        executes some parser code before failing is real signal — those
        lines DID get exercised.
      * The coverage backend (``cov.start()``/``stop()``/``get_data()``)
        itself raised → re-raise. ``CorpusKeeper.cull_by_coverage``
        catches measurer exceptions and KEEPS the file (sensible default
        — a measurement bug must not be conflated with "the file
        covered nothing").

    Thread-safety: coverage.py's ``Coverage.start()`` swaps the
    interpreter's C-level trace function globally. Calling ``measure``
    concurrently from multiple threads is undefined. ``CorpusKeeper.
    cull_by_coverage`` invokes the callback sequentially, which is the
    only supported use.

    Args:
        sut_name: One of ``SUPPORTED_PYTHON_SUTS``. Anything else
            raises ``NotImplementedError`` so the caller can fall back
            to "no culling for this primary target".
        fmt: ``"VCF"`` or ``"SAM"`` — passed to the runner's ``run``
            method. The chosen runner must support this format.
        timeout_s: Per-file timeout passed to the underlying runner.
            Bounded so a pathological seed can't stall the culler.

    Returns:
        A picklable closure suitable for ``cull_by_coverage``.
    """
    if sut_name not in SUPPORTED_PYTHON_SUTS:
        raise NotImplementedError(
            f"build_python_measurer: SUT '{sut_name}' has no per-file "
            f"coverage measurer yet. Supported: "
            f"{sorted(SUPPORTED_PYTHON_SUTS)}. JaCoCo/gcovr/llvm-cov "
            f"backends are future work."
        )

    sources = _SUT_SOURCE_PACKAGES[sut_name]
    runner = _build_runner(sut_name)

    def measure(path: Path) -> "frozenset[tuple[str, int]]":
        # Local import — coverage is a heavy dep at module-load time.
        # An ImportError here is a setup bug; let the caller's defensive
        # handler keep the file rather than silently culling it.
        import coverage  # type: ignore

        cov = coverage.Coverage(
            data_file=None,        # in-memory only
            source_pkgs=list(sources),
            messages=False,
        )
        cov.start()
        try:
            try:
                runner.run(path, fmt, timeout_s=timeout_s)
            except Exception as e:
                # A parse failure is data, not an error — the file
                # exercised whatever code paths it could before
                # crashing. Don't propagate; the lines collected so
                # far are still real signal.
                logger.debug(
                    "measure_lines: %s.run() raised on %s: %s",
                    sut_name, path.name, e,
                )
        finally:
            cov.stop()

        # If the coverage backend itself fails, propagate — the caller
        # (CorpusKeeper.cull_by_coverage) catches and KEEPS the file,
        # which is the sensible default for a measurement bug.
        data = cov.get_data()
        lines: set[tuple[str, int]] = set()
        for filename in data.measured_files() or []:
            for line in (data.lines(filename) or []):
                lines.add((filename, line))
        return frozenset(lines)

    return measure


def _build_runner(sut_name: str):
    """Late-bind runner imports so the module loads cheaply for tests
    that monkeypatch ``build_python_measurer`` and never construct a
    real runner."""
    if sut_name == "vcfpy":
        from test_engine.runners.vcfpy_runner import VcfpyRunner
        return VcfpyRunner()
    if sut_name == "biopython":
        from test_engine.runners.biopython_runner import BiopythonRunner
        return BiopythonRunner()
    raise AssertionError(f"unreachable: unsupported SUT {sut_name}")


def measure_corpus_baseline(
    measurer: MeasureLinesFn,
    seeds: list[Path],
) -> "frozenset[tuple[str, int]]":
    """Compute the union of per-file coverage across a list of seeds.

    Use this to build the ``baseline_lines`` argument for
    ``CorpusKeeper.cull_by_coverage`` — it tells the culler which lines
    the EXISTING corpus already covers, so a candidate file only counts
    as "novel" if it adds something beyond that union.

    The work is O(n × measure_cost). For 33 curated VCF seeds at
    ~100 ms each that's ~3.3 s — acceptable as a once-per-iteration
    cost.
    """
    accum: set[tuple[str, int]] = set()
    for p in seeds:
        try:
            accum |= measurer(p)
        except Exception as e:
            logger.warning(
                "measure_corpus_baseline: skipping %s after failure: %s",
                p.name, e,
            )
    return frozenset(accum)
