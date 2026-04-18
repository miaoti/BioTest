"""
T8: Mocked E2E orchestrator loop.

Injects DummyRunners (no real Java/pysam) to verify the entire pipeline:
MR load -> transform -> oracle -> triage -> DET report.

Must complete in < 1 second with exact DET rate verification.
"""

import json
import time
import tempfile
from pathlib import Path
from typing import Any

import pytest

from test_engine.orchestrator import run_test_suite
from test_engine.runners.base import ParserRunner, RunnerResult


SEEDS_DIR = Path(__file__).parent.parent / "seeds"


@pytest.fixture
def fixture_seeds(tmp_path):
    """Hermetic 3-seed corpus. The live `seeds/` dir grew to ~30 VCF
    files when Tier-2 real-world seeds were fetched; orchestrator tests
    count `total_tests = MRs * seeds * runners` so a moving seed corpus
    would keep breaking them. Copy just the 3 hand-crafted Tier-1 VCF
    seeds into a fresh tmp directory."""
    live = Path(__file__).parent.parent / "seeds"
    dst = tmp_path / "seeds"
    (dst / "vcf").mkdir(parents=True, exist_ok=True)
    (dst / "sam").mkdir(parents=True, exist_ok=True)
    for name in ("minimal_single.vcf", "minimal_multisample.vcf", "spec_example.vcf"):
        src = live / "vcf" / name
        if src.exists():
            (dst / "vcf" / name).write_bytes(src.read_bytes())
    return dst


@pytest.fixture
def fixture_registry(tmp_path):
    """Hermetic 3-MR registry so tests don't depend on the live data file,
    which mutates across Phase D runs (quarantine may empty `enforced`).

    Uses simple text-level VCF transforms whose dispatch is always
    registered — `no_op`-equivalents aren't available, but
    `shuffle_info_field_kv` / `shuffle_meta_lines` / `permute_structured_kv_order`
    are all VCF-scoped and present in test_engine/generators/dispatch.py.
    """
    reg = tmp_path / "fixture_registry.json"
    reg.write_text(json.dumps({
        "enforced": [
            {
                "mr_id": "fixture01",
                "mr_name": "MR1 — shuffle INFO kv",
                "scope": "VCF.record",
                "preconditions": [],
                "transform_steps": ["shuffle_info_field_kv"],
                "oracle": "Order of INFO key=value pairs is semantically insignificant.",
                "evidence": [],
            },
            {
                "mr_id": "fixture02",
                "mr_name": "MR2 — shuffle meta lines",
                "scope": "VCF.header",
                "preconditions": [],
                "transform_steps": ["shuffle_meta_lines"],
                "oracle": "Order of ## meta lines is insignificant.",
                "evidence": [],
            },
            {
                "mr_id": "fixture03",
                "mr_name": "MR3 — permute structured kv",
                "scope": "VCF.header",
                "preconditions": [],
                "transform_steps": ["permute_structured_kv_order"],
                "oracle": "Order of structured KV pairs inside a ##INFO line is insignificant.",
                "evidence": [],
            },
        ],
        "quarantine": [],
        "summary": {"total": 3, "enforced_count": 3, "quarantine_count": 0},
    }), encoding="utf-8")
    return reg


# ---------------------------------------------------------------------------
# Dummy runners that return pre-canned results (no external deps)
# ---------------------------------------------------------------------------

class AgreeingRunner(ParserRunner):
    """A dummy runner that always returns the same canonical JSON.
    Used to simulate a conformant parser that passes all metamorphic checks."""

    def __init__(self, runner_name: str = "dummy_agree"):
        self._name = runner_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        return True

    def run(self, input_path: Path, format_type: str, timeout_s: float = 30.0) -> RunnerResult:
        # Always return the same canonical JSON regardless of input
        # This means parse(x) == parse(T(x)) for metamorphic oracle
        canonical = {
            "format": format_type,
            "header": {"fileformat": "VCFv4.3", "meta": {}, "samples": []},
            "records": [],
        }
        return RunnerResult(
            success=True,
            canonical_json=canonical,
            parser_name=self._name,
            format_type=format_type,
            duration_ms=1.0,
        )


class DisagreeingRunner(ParserRunner):
    """A dummy runner that returns different output for every call.
    Used to simulate a non-conformant parser that fails metamorphic checks."""

    _call_count = 0

    def __init__(self, runner_name: str = "dummy_disagree"):
        self._name = runner_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        return True

    def run(self, input_path: Path, format_type: str, timeout_s: float = 30.0) -> RunnerResult:
        DisagreeingRunner._call_count += 1
        canonical = {
            "format": format_type,
            "header": {"fileformat": "VCFv4.3", "meta": {}, "samples": []},
            "records": [{"POS": DisagreeingRunner._call_count}],
        }
        return RunnerResult(
            success=True,
            canonical_json=canonical,
            parser_name=self._name,
            format_type=format_type,
            duration_ms=1.0,
        )


class CrashingRunner(ParserRunner):
    """A dummy runner that always crashes."""

    @property
    def name(self) -> str:
        return "dummy_crasher"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        return True

    def run(self, input_path: Path, format_type: str, timeout_s: float = 30.0) -> RunnerResult:
        return RunnerResult(
            success=False,
            parser_name=self.name,
            format_type=format_type,
            error_type="crash",
            stderr="java.lang.NullPointerException\n\tat FakeClass.fakeMethod(Fake.java:42)",
        )


# ===========================================================================
# T8: Mocked E2E orchestrator tests
# ===========================================================================

class TestMockedOrchestratorLoop:
    """Full pipeline with dummy runners — no real parsers needed."""

    def test_all_agreeing_runners_zero_failures(self, tmp_path, fixture_registry, fixture_seeds):
        """Two agreeing runners should produce 0 metamorphic and 0 differential failures."""
        runner_a = AgreeingRunner("parser_a")
        runner_b = AgreeingRunner("parser_b")

        t0 = time.monotonic()
        result = run_test_suite(
            runners=[runner_a, runner_b],
            registry_path=fixture_registry,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
            format_filter="VCF",
        )
        elapsed = time.monotonic() - t0

        # Must complete in < 1 second (no real subprocess)
        assert elapsed < 1.0, f"Mocked orchestrator too slow: {elapsed:.2f}s"

        # 3 MRs x 3 seeds x 2 runners = 18 metamorphic + 3x3=9 differential = 27 tests
        assert result.total_tests == 27
        assert result.metamorphic_failures == 0
        assert result.differential_failures == 0
        assert result.det_tracker.det_rate == 0.0
        assert len(result.bug_reports) == 0

    def test_disagreeing_runner_catches_all_violations(self, tmp_path, fixture_registry, fixture_seeds):
        """A disagreeing runner should be flagged for every metamorphic test."""
        DisagreeingRunner._call_count = 0
        runner = DisagreeingRunner()

        result = run_test_suite(
            runners=[runner],
            registry_path=fixture_registry,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
            format_filter="VCF",
        )

        # Single runner: 3 MRs x 3 seeds = 9 metamorphic tests, 0 differential (need 2+)
        assert result.total_tests == 9
        # Every metamorphic test should fail (parse(x) != parse(T(x)))
        assert result.metamorphic_failures == 9
        assert result.det_tracker.det_rate == 1.0
        assert len(result.bug_reports) == 9

    def test_crashing_runner_reports_all_crashes(self, tmp_path, fixture_registry, fixture_seeds):
        """A crashing runner should produce crash-type failures."""
        runner = CrashingRunner()

        result = run_test_suite(
            runners=[runner],
            registry_path=fixture_registry,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
            format_filter="VCF",
        )

        assert result.total_tests == 9
        assert result.metamorphic_failures == 9
        # All bug reports should exist
        assert len(result.bug_reports) == 9
        # Verify bug report content
        for bp in result.bug_reports:
            summary = json.loads((bp / "summary.json").read_text(encoding="utf-8"))
            assert summary["failure_type"] == "crash"

    def test_det_rate_exact_with_mixed_runners(self, tmp_path, fixture_registry, fixture_seeds):
        """Mixed agreeing+disagreeing runners: verify exact DET rate calculation."""
        agree = AgreeingRunner("conformant")
        DisagreeingRunner._call_count = 0
        disagree = DisagreeingRunner("nonconformant")

        result = run_test_suite(
            runners=[agree, disagree],
            registry_path=fixture_registry,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
            format_filter="VCF",
        )

        # 2 runners: 3 MRs x 3 seeds x 2 metamorphic + 3x3 differential = 27
        assert result.total_tests == 27
        # Agreeing runner: 0 metamorphic failures
        # Disagreeing runner: 9 metamorphic failures (every parse different)
        assert result.metamorphic_failures == 9
        # All 9 differential tests should fail (agree != disagree)
        assert result.differential_failures == 9
        # DET rate: (9 meta + 9 diff) / 27 = 18/27 = 0.6667
        assert abs(result.det_tracker.det_rate - (18 / 27)) < 0.001

    def test_det_report_json_structure(self, tmp_path, fixture_registry, fixture_seeds):
        """Exported DET report must have correct JSON structure."""
        runner = AgreeingRunner()

        result = run_test_suite(
            runners=[runner],
            registry_path=fixture_registry,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
            format_filter="VCF",
        )

        det_path = tmp_path / "det_report.json"
        result.det_tracker.export(str(det_path))

        report = json.loads(det_path.read_text(encoding="utf-8"))
        assert "total_tests" in report
        assert "disagreements" in report
        assert "det_rate" in report
        assert "by_mr" in report
        assert "by_type" in report
        assert "timestamp" in report

        # All 3 MR IDs should appear in by_mr
        assert len(report["by_mr"]) == 3

    def test_empty_registry_produces_zero_tests(self, tmp_path, fixture_seeds):
        """Empty enforced list should produce 0 tests without crashing."""
        empty_reg = tmp_path / "empty_registry.json"
        empty_reg.write_text(json.dumps({
            "enforced": [], "quarantine": [], "summary": {"total": 0}
        }), encoding="utf-8")

        runner = AgreeingRunner()
        result = run_test_suite(
            runners=[runner],
            registry_path=empty_reg,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
        )

        assert result.total_tests == 0
        assert result.det_tracker.det_rate == 0.0

    def test_format_filter_restricts_tests(self, tmp_path, fixture_registry, fixture_seeds):
        """format_filter='SAM' should skip all VCF MRs (our registry has only VCF MRs)."""
        runner = AgreeingRunner()
        result = run_test_suite(
            runners=[runner],
            registry_path=fixture_registry,
            seeds_dir=fixture_seeds,
            output_dir=tmp_path / "bugs",
            format_filter="SAM",
        )

        # All 3 MRs are VCF-scoped, so SAM filter skips everything
        assert result.total_tests == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
