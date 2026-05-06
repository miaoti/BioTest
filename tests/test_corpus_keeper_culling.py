"""Unit tests for the Rank-8b coverage-guided culling.

These tests inject a deterministic mock ``measure_lines`` callback so
the cull decisions are exercised without spinning up real coverage.py /
JaCoCo. The production wiring (Python SUT integration via
``coverage_culler.build_python_measurer``) is exercised separately
when the user sets ``phase_c.corpus_keeper.coverage_guided_culling.enabled = true``
in a real run.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from test_engine.feedback.corpus_keeper import CorpusKeeper, _FILENAME_PREFIX


@pytest.fixture
def keeper(tmp_path):
    """Fresh keeper rooted at a tmp seeds dir."""
    return CorpusKeeper(seeds_dir=tmp_path / "seeds", enabled=True)


def _seed_kept_file(keeper: CorpusKeeper, fmt: str, content: bytes,
                    canonical: str | None = None) -> Path:
    """Drive the keeper through one ``maybe_keep`` so a real file
    lands at ``seeds/<fmt>/kept_<sha8>.<fmt>`` and the keeper's
    bookkeeping is populated as production would have it."""
    src = keeper.seeds_dir / fmt / "_tmp.in"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_bytes(content)
    decision = keeper.maybe_keep(
        transformed_path=src,
        fmt=fmt.upper(),
        mr_id="fixture_mr",
        any_runner_success=True,
        canonical_json_hash=canonical,
    )
    src.unlink(missing_ok=True)
    assert decision.kept, f"setup failed — file not kept: {decision.reason}"
    return decision.path


# ---------------------------------------------------------------------------
# Lifecycle: tracking, reset, snapshot
# ---------------------------------------------------------------------------

class TestIterationTracking:
    def test_kept_paths_accumulate_across_calls(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        b = _seed_kept_file(keeper, "vcf", b"##b\n", canonical="b")
        snap = keeper.get_kept_this_iteration()
        assert snap == [a, b]

    def test_reset_clears_tracking_but_not_dedup(self, keeper):
        _seed_kept_file(keeper, "vcf", b"##x\n", canonical="x")
        keeper.reset_iteration_tracking()
        assert keeper.get_kept_this_iteration() == []
        # The byte-hash is still in the dedup set: trying to keep the
        # same bytes again must be rejected as duplicate.
        src = keeper.seeds_dir / "vcf" / "_tmp.in"
        src.write_bytes(b"##x\n")
        d = keeper.maybe_keep(
            transformed_path=src, fmt="VCF", mr_id="r",
            any_runner_success=True,
        )
        assert not d.kept and d.reason == "duplicate"


# ---------------------------------------------------------------------------
# cull_by_coverage — decision logic
# ---------------------------------------------------------------------------

class TestCullByCoverage:
    def test_files_with_no_new_lines_are_deleted(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        b = _seed_kept_file(keeper, "vcf", b"##b\n", canonical="b")

        # a covers {(f, 1)}, b covers {(f, 1)} (same lines, no novelty).
        def measure(p: Path) -> frozenset[tuple[str, int]]:
            return frozenset({("vcfpy/parser.py", 1)})

        stats = keeper.cull_by_coverage(measure, log_decisions=False)
        assert stats == {
            "total": 2, "kept": 1, "culled": 1,
            "baseline_size": 0, "final_size": 1,
        }
        # Whichever was processed first survives (insertion order).
        assert a.exists()
        assert not b.exists()

    def test_files_adding_new_lines_are_kept(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        b = _seed_kept_file(keeper, "vcf", b"##b\n", canonical="b")
        c = _seed_kept_file(keeper, "vcf", b"##c\n", canonical="c")

        per_file = {
            a.name: frozenset({("p.py", 1), ("p.py", 2)}),
            b.name: frozenset({("p.py", 2), ("p.py", 3)}),
            c.name: frozenset({("p.py", 1), ("p.py", 2)}),  # subset of a
        }

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            return per_file[p.name]

        stats = keeper.cull_by_coverage(measure, log_decisions=False)
        # a contributes {1, 2}; b contributes {3} (new); c contributes {} (cull).
        assert stats["kept"] == 2
        assert stats["culled"] == 1
        assert stats["final_size"] == 3
        assert a.exists() and b.exists() and not c.exists()

    def test_baseline_lines_filter_files_subset_of_baseline(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        baseline = frozenset({("p.py", 1), ("p.py", 2)})

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            return frozenset({("p.py", 1), ("p.py", 2)})

        stats = keeper.cull_by_coverage(measure, baseline_lines=baseline, log_decisions=False)
        assert stats["culled"] == 1
        assert stats["baseline_size"] == 2
        assert stats["final_size"] == 2  # baseline unchanged
        assert not a.exists()

    def test_baseline_does_not_block_novel_lines(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        baseline = frozenset({("p.py", 1)})

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            return frozenset({("p.py", 2)})

        stats = keeper.cull_by_coverage(measure, baseline_lines=baseline, log_decisions=False)
        assert stats["kept"] == 1
        assert stats["culled"] == 0
        assert stats["final_size"] == 2
        assert a.exists()

    def test_measure_failure_keeps_file(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            raise RuntimeError("backend exploded")

        stats = keeper.cull_by_coverage(measure, log_decisions=False)
        # Defensive: a measurement error must not delete the file.
        assert stats["kept"] == 1
        assert stats["culled"] == 0
        assert a.exists()

    def test_culled_files_removed_from_dedup(self, keeper):
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        b = _seed_kept_file(keeper, "vcf", b"##b\n", canonical="b")

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            return frozenset({("p.py", 1)})  # same lines for both

        keeper.cull_by_coverage(measure, log_decisions=False)
        assert not b.exists()
        # b's byte-hash should be removed from dedup so an identical
        # file could in principle be re-tried later.
        b_sha = b.stem[len(_FILENAME_PREFIX):]
        assert b_sha not in keeper._seen_hashes["vcf"]
        # a's byte-hash is still there.
        a_sha = a.stem[len(_FILENAME_PREFIX):]
        assert a_sha in keeper._seen_hashes["vcf"]

    def test_resets_iteration_tracking_after_cull(self, keeper):
        _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            return frozenset({("p.py", 1)})

        keeper.cull_by_coverage(measure, log_decisions=False)
        assert keeper.get_kept_this_iteration() == []

    def test_handles_already_deleted_file(self, keeper, tmp_path):
        # If a kept file is FIFO-evicted between maybe_keep and cull
        # the culler must skip it cleanly, not raise.
        a = _seed_kept_file(keeper, "vcf", b"##a\n", canonical="a")
        a.unlink()  # simulate eviction

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            raise AssertionError("should not be called for missing file")

        stats = keeper.cull_by_coverage(measure, log_decisions=False)
        # Treated as already-gone: not in either kept or culled count
        # (we drop missing files from the iteration list with no work).
        assert stats["total"] == 1
        assert stats["kept"] == 0
        assert stats["culled"] == 0

    def test_empty_iteration_returns_zero_stats(self, keeper):
        def measure(p: Path) -> frozenset[tuple[str, int]]:
            raise AssertionError("should not be called")

        stats = keeper.cull_by_coverage(measure, log_decisions=False)
        assert stats == {
            "total": 0, "kept": 0, "culled": 0,
            "baseline_size": 0, "final_size": 0,
        }

    def test_reset_then_keep_then_cull_isolates_iterations(self, keeper):
        # iteration 1 — keep one file, then reset (simulates Phase D
        # iteration boundary where we don't want to cull yet).
        i1 = _seed_kept_file(keeper, "vcf", b"##i1\n", canonical="i1")
        keeper.reset_iteration_tracking()
        # iteration 2 — keep another file, cull. Only i2 should be
        # considered; i1 is "old" and should NOT be touched.
        i2 = _seed_kept_file(keeper, "vcf", b"##i2\n", canonical="i2")

        def measure(p: Path) -> frozenset[tuple[str, int]]:
            assert p == i2, f"unexpected file: {p}"
            return frozenset()  # zero coverage → cull

        stats = keeper.cull_by_coverage(measure, log_decisions=False)
        assert stats["culled"] == 1
        assert i1.exists()      # untouched
        assert not i2.exists()  # culled


# ---------------------------------------------------------------------------
# coverage_culler — entry-point validation
# ---------------------------------------------------------------------------

class TestCoverageCullerFactory:
    def test_unsupported_sut_raises(self):
        from test_engine.feedback.coverage_culler import build_python_measurer
        with pytest.raises(NotImplementedError, match="htsjdk"):
            build_python_measurer("htsjdk", "VCF")

    def test_supported_sut_returns_callable(self):
        from test_engine.feedback.coverage_culler import (
            SUPPORTED_PYTHON_SUTS,
            build_python_measurer,
        )
        for sut in SUPPORTED_PYTHON_SUTS:
            fn = build_python_measurer(sut, "VCF" if sut == "vcfpy" else "SAM")
            assert callable(fn)
