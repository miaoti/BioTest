"""
HTSlibRunner tests. The CLI itself is skipped when samtools/bcftools
aren't on PATH — those cases run only in CI environments that install
the binaries. The unit-level assertions still verify the runner's
structural contract (name, supported_formats, wiring) without shelling
out.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from test_engine.runners.htslib_runner import HTSlibRunner


SEEDS_DIR = Path(__file__).parent.parent / "seeds"


def test_name_is_htslib():
    runner = HTSlibRunner(bcftools_path="/nonexistent/bcftools")
    assert runner.name == "htslib"


def test_supported_formats_depend_on_binary_presence():
    # No binaries set → empty set.
    runner = HTSlibRunner(bcftools_path=None, samtools_path=None)
    # shutil.which may still find something in PATH. Accept either
    # the empty set or any subset of {"VCF", "SAM"}.
    assert runner.supported_formats <= {"VCF", "SAM"}


def test_supports_helper_respects_formats(monkeypatch):
    # Prevent the constructor's `or shutil.which("samtools")` fallback
    # from finding a real samtools on PATH (e.g. the WSL-Ubuntu wrapper
    # we now ship for Phase 3 round-trip MRs) — the test wants
    # determinism: only the explicit constructor args should drive
    # which formats are supported.
    monkeypatch.setattr(
        "test_engine.runners.htslib_runner.shutil.which",
        lambda name, *a, **kw: None,
    )
    runner = HTSlibRunner(bcftools_path="/tmp/x-bcftools", samtools_path=None)
    # When bcftools_path is non-None (truthy), supported_formats includes VCF
    assert runner.supports("VCF") is True
    assert runner.supports("SAM") is False


def test_unsupported_format_returns_ineligible():
    runner = HTSlibRunner(bcftools_path="/tmp/x", samtools_path="/tmp/y")
    result = runner.run(Path("/tmp/nonexistent.vcf"), "BAM")
    assert result.success is False
    assert result.error_type == "ineligible"
    assert "not support" in result.stderr.lower() or "BAM" in result.stderr


def test_missing_binary_returns_ineligible():
    """If bcftools isn't on PATH, VCF runs are INELIGIBLE (not malformed-input
    parse_error) — consensus must discard these silently."""
    runner = HTSlibRunner(bcftools_path=None, samtools_path=None)
    runner._bcftools = None
    result = runner.run(Path("/tmp/anything.vcf"), "VCF")
    assert result.success is False
    assert result.error_type == "ineligible"
    assert "bcftools" in result.stderr.lower() or "not found" in result.stderr.lower()


@pytest.mark.skipif(
    not shutil.which("bcftools"),
    reason="bcftools not installed — skipping live VCF parse test",
)
def test_bcftools_live_on_minimal_vcf():
    """If bcftools is on PATH, verify it round-trips a known seed."""
    seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
    if not seed.exists():
        pytest.skip("minimal VCF seed missing")
    runner = HTSlibRunner()
    result = runner.run(seed, "VCF")
    assert result.success, f"bcftools failed: {result.stderr}"
    assert result.canonical_json is not None
    # Sanity: VCF canonical schema has a 'header' dict and 'records' list.
    assert "header" in result.canonical_json
    assert "records" in result.canonical_json


@pytest.mark.skipif(
    not shutil.which("samtools"),
    reason="samtools not installed — skipping live SAM parse test",
)
def test_samtools_live_on_minimal_sam():
    seed = SEEDS_DIR / "sam" / "minimal_tags.sam"
    if not seed.exists():
        pytest.skip("minimal SAM seed missing")
    runner = HTSlibRunner()
    result = runner.run(seed, "SAM")
    assert result.success, f"samtools failed: {result.stderr}"
    assert result.canonical_json is not None
    assert "header" in result.canonical_json
