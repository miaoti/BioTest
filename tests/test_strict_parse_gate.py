"""Smoke tests for the STRICT-stringency gate added 2026-04-21.

Verifies:
  1. HTSJDKRunner.run_strict_parse exits 0 on a valid SAM, exits 2 with
     stderr on a SAMException-rejected SAM (e.g. comma in @SQ SN:).
  2. _replay_trigger_silenced returns False on a SAM that the bundled
     (post-fix) htsjdk rejects under STRICT, even when SILENT-default
     parse would have succeeded.

These are smoke tests against the bundled htsjdk-with-deps fatjar
(post-fix for all 3 new bugs); the per-version pre-fix vs post-fix
differential is exercised in the Docker bench run, not here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "compares" / "scripts"))


@pytest.fixture(scope="module")
def runner():
    from test_engine.runners.htsjdk_runner import HTSJDKRunner
    r = HTSJDKRunner()
    if not r.is_available():
        pytest.skip("htsjdk harness JAR not built — bash harnesses/java/build.sh")
    return r


def test_strict_parse_accepts_valid_sam(runner, tmp_path):
    sam = tmp_path / "valid.sam"
    sam.write_text(
        "@HD\tVN:1.6\tSO:coordinate\n"
        "@SQ\tSN:chr1\tLN:1000\n"
        "r1\t0\tchr1\t1\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
        encoding="utf-8",
    )
    res = runner.run_strict_parse(sam, "SAM")
    assert res.success, f"STRICT should accept a valid SAM: {res.stderr}"
    assert res.exit_code == 0


def test_strict_parse_rejects_comma_in_sn(runner):
    """htsjdk-1238 trigger — comma in @SQ SN: violates RNAME regex."""
    pov = ROOT / "compares" / "bug_bench" / "triggers" / "htsjdk-1238" / "original.sam"
    assert pov.exists(), f"PoV missing: {pov}"
    res = runner.run_strict_parse(pov, "SAM")
    assert not res.success, "post-fix htsjdk should reject comma in SN"
    assert res.exit_code == 2
    assert "doesn't match regex" in res.stderr or "SAMException" in res.stderr


def test_strict_parse_format_validation(runner, tmp_path):
    res = runner.run_strict_parse(tmp_path / "anything.sam", "BAM")
    assert not res.success
    assert res.error_type == "ineligible"


def test_replay_silenced_uses_strict_gate(runner):
    """Verify _replay_trigger_silenced inherits the STRICT rejection."""
    from bug_bench_driver import _replay_trigger_silenced
    pov = ROOT / "compares" / "bug_bench" / "triggers" / "htsjdk-1238" / "original.sam"
    assert pov.exists()
    # bundled htsjdk is post-fix for htsjdk-1238 → STRICT throws → not silenced
    silenced = _replay_trigger_silenced("htsjdk", pov, "SAM")
    assert silenced is False, (
        "post-fix htsjdk rejects htsjdk-1238 trigger under STRICT — predicate "
        "must not return True/None")


def test_replay_silenced_passes_when_strict_accepts(runner):
    """For triggers where the bundled htsjdk IS post-fix (already passes
    STRICT), the predicate must return True (silenced)."""
    from bug_bench_driver import _replay_trigger_silenced
    # htsjdk-1410's post-fix accepts |TLEN| > 2^29 under STRICT
    pov = ROOT / "compares" / "bug_bench" / "triggers" / "htsjdk-1410" / "original.sam"
    assert pov.exists()
    silenced = _replay_trigger_silenced("htsjdk", pov, "SAM")
    assert silenced is True, (
        "post-fix htsjdk accepts htsjdk-1410 trigger under STRICT — predicate "
        "must return True")
