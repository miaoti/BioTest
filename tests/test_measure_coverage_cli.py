"""
Tests for ``compares/scripts/measure_coverage.py``.

Verifies that the fairness recipe stays honest: config-driven filter
rules, format-agnostic dispatch, bucket math matches what the
feedback loop uses at runtime.

All tests use fixture reports — no dependency on any real SUT run.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPT = _REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"


def _load_module():
    """Import measure_coverage.py as a module without sys.path games.

    The module uses @dataclass which reads sys.modules[cls.__module__],
    so we must register in sys.modules BEFORE exec_module runs."""
    spec = importlib.util.spec_from_file_location("measure_coverage", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["measure_coverage"] = mod
    sys.path.insert(0, str(_REPO_ROOT))
    spec.loader.exec_module(mod)
    return mod


mc = _load_module()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _write_config(tmp_path: Path, target_filters: dict) -> Path:
    """Minimal biotest_config.yaml fixture — only the coverage block matters."""
    import yaml
    cfg = {"coverage": {"target_filters": target_filters}}
    path = tmp_path / "cfg.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return path


def _write_jacoco_xml(tmp_path: Path) -> Path:
    """Tiny JaCoCo with two packages × two sourcefiles each."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<report name="fixture">
  <package name="com/example/core">
    <sourcefile name="Big.java">
      <counter type="LINE" missed="80" covered="20"/>
    </sourcefile>
    <sourcefile name="Small.java">
      <counter type="LINE" missed="2" covered="8"/>
    </sourcefile>
  </package>
  <package name="com/example/jexl">
    <sourcefile name="JEXLExpr.java">
      <counter type="LINE" missed="50" covered="50"/>
    </sourcefile>
    <sourcefile name="Other.java">
      <counter type="LINE" missed="5" covered="5"/>
    </sourcefile>
  </package>
</report>
"""
    p = tmp_path / "jacoco.xml"
    p.write_text(xml, encoding="utf-8")
    return p


def _write_coveragepy_json(tmp_path: Path) -> Path:
    data = {
        "meta": {"format": 2},
        "files": {
            "pkg/a/mod.py": {"summary": {"covered_lines": 30, "num_statements": 100}},
            "pkg/b/mod.py": {"summary": {"covered_lines": 5, "num_statements": 10}},
            "somewhere/else/mod.py": {"summary": {"covered_lines": 1, "num_statements": 2}},
        },
    }
    p = tmp_path / "cov.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def _write_gcovr_json(tmp_path: Path) -> Path:
    data = {
        "files": [
            {"file": "include/lib/a.hpp",
             "lines": [{"line_number": 1, "count": 1},
                       {"line_number": 2, "count": 0},
                       {"line_number": 3, "count": 1}]},
            {"file": "include/other/b.hpp",
             "lines": [{"line_number": 1, "count": 0}]},
        ]
    }
    p = tmp_path / "gcovr.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# JaCoCo path
# ---------------------------------------------------------------------------

def _write_jacoco_xml_with_branches(tmp_path: Path) -> Path:
    """JaCoCo fixture that ships both LINE and BRANCH counters."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<report name="fixture">
  <package name="com/example/core">
    <sourcefile name="Big.java">
      <counter type="LINE" missed="80" covered="20"/>
      <counter type="BRANCH" missed="40" covered="10"/>
    </sourcefile>
  </package>
</report>
"""
    p = tmp_path / "jacoco_branches.xml"
    p.write_text(xml, encoding="utf-8")
    return p


class TestJacocoPath:
    def test_filter_excludes_jexl_package(self, tmp_path):
        cfg = _write_config(tmp_path, {
            "VCF": {"fakesut": [
                "com/example/core",
                "com/example/jexl::-JEXL,-Jexl,-*JEXL*,-*Jexl*",
            ]},
        })
        report = _write_jacoco_xml(tmp_path)
        r = mc.measure(report_path=report, sut="fakesut",
                       format_="VCF", config_path=cfg)
        # core: Big + Small = 28 / 110
        core = next(b for b in r.buckets if b.name == "com/example/core")
        assert core.covered == 28
        assert core.total == 110
        # jexl: JEXLExpr filtered out, only Other = 5 / 10
        jexl = next(b for b in r.buckets if b.name == "com/example/jexl")
        assert jexl.covered == 5
        assert jexl.total == 10

    def test_overall_weighted_is_sum_over_buckets(self, tmp_path):
        cfg = _write_config(tmp_path, {
            "VCF": {"fakesut": ["com/example/core"]},
        })
        report = _write_jacoco_xml(tmp_path)
        r = mc.measure(report_path=report, sut="fakesut",
                       format_="VCF", config_path=cfg)
        assert r.total_covered == 28
        assert r.total_lines == 110
        assert r.weighted_pct == pytest.approx(28 / 110 * 100, abs=1e-6)

    def test_metric_branch_sums_branch_counters(self, tmp_path):
        """metric='BRANCH' returns BRANCH-counter sums instead of LINE."""
        cfg = _write_config(tmp_path, {
            "VCF": {"fakesut": ["com/example/core"]},
        })
        report = _write_jacoco_xml_with_branches(tmp_path)
        line = mc.measure(report_path=report, sut="fakesut", format_="VCF",
                          config_path=cfg, metric="LINE")
        branch = mc.measure(report_path=report, sut="fakesut", format_="VCF",
                            config_path=cfg, metric="BRANCH")
        assert line.total_covered == 20 and line.total_lines == 100
        assert branch.total_covered == 10 and branch.total_lines == 50
        assert line.weighted_pct == pytest.approx(20.0)
        assert branch.weighted_pct == pytest.approx(20.0)

    def test_metric_default_is_line(self, tmp_path):
        """Omitting metric= stays on LINE — preserves Run-6 grounding shape."""
        cfg = _write_config(tmp_path, {
            "VCF": {"fakesut": ["com/example/core"]},
        })
        report = _write_jacoco_xml_with_branches(tmp_path)
        r = mc.measure(report_path=report, sut="fakesut", format_="VCF",
                       config_path=cfg)
        assert r.total_covered == 20  # line, not 10 (branch)


# ---------------------------------------------------------------------------
# coverage.py path
# ---------------------------------------------------------------------------

class TestCoveragePyPath:
    def test_filter_by_prefix(self, tmp_path):
        cfg = _write_config(tmp_path, {
            "VCF": {"fakesut": ["pkg"]},
        })
        report = _write_coveragepy_json(tmp_path)
        r = mc.measure(report_path=report, sut="fakesut",
                       format_="VCF", config_path=cfg)
        # Both pkg/* files accepted; "somewhere/else" dropped.
        assert r.total_covered == 30 + 5
        assert r.total_lines == 100 + 10


# ---------------------------------------------------------------------------
# gcovr path
# ---------------------------------------------------------------------------

class TestGcovrPath:
    def test_filter_by_prefix(self, tmp_path):
        cfg = _write_config(tmp_path, {
            "SAM": {"fakesut": ["include/lib"]},
        })
        report = _write_gcovr_json(tmp_path)
        r = mc.measure(report_path=report, sut="fakesut",
                       format_="SAM", config_path=cfg)
        # a.hpp 2/3; b.hpp excluded by prefix.
        assert r.total_covered == 2
        assert r.total_lines == 3


# ---------------------------------------------------------------------------
# Config-resolution failures
# ---------------------------------------------------------------------------

class TestConfigResolution:
    def test_missing_format_raises(self, tmp_path):
        cfg = _write_config(tmp_path, {"VCF": {"fakesut": ["com/example"]}})
        report = _write_jacoco_xml(tmp_path)
        with pytest.raises(KeyError):
            mc.measure(report_path=report, sut="fakesut",
                       format_="SAM", config_path=cfg)

    def test_missing_sut_raises_with_hint(self, tmp_path):
        cfg = _write_config(tmp_path, {"VCF": {"fakesut": ["com/example"]}})
        report = _write_jacoco_xml(tmp_path)
        with pytest.raises(KeyError, match="fakesut"):
            mc.measure(report_path=report, sut="missing_sut",
                       format_="VCF", config_path=cfg)

    def test_missing_report_raises(self, tmp_path):
        cfg = _write_config(tmp_path, {"VCF": {"fakesut": ["com/example"]}})
        with pytest.raises(FileNotFoundError):
            mc.measure(report_path=tmp_path / "no.xml", sut="fakesut",
                       format_="VCF", config_path=cfg)


# ---------------------------------------------------------------------------
# End-to-end against a real BioTest jacoco snapshot
# ---------------------------------------------------------------------------

class TestAgainstRealSnapshot:
    """Grounding test — if this ever changes, the measurement semantics
    changed; update this test ONLY after a conscious decision."""

    @pytest.mark.skipif(
        not (_REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco_post_run6.xml").exists(),
        reason="Run 6 snapshot not present — skipping grounding test",
    )
    def test_biotest_run6_htsjdk_vcf_matches_46_9(self):
        """Run 6 htsjdk/VCF = 1765/3760 = 46.9 % (documented baseline)."""
        r = mc.measure(
            report_path=_REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco_post_run6.xml",
            sut="htsjdk", format_="VCF",
            config_path=_REPO_ROOT / "biotest_config.yaml",
        )
        assert r.total_covered == 1765
        assert r.total_lines == 3760
        assert round(r.weighted_pct, 1) == 46.9


# ---------------------------------------------------------------------------
# Side-by-side formatting
# ---------------------------------------------------------------------------

class TestSideBySideFormatting:
    def test_two_results_emit_delta_lines(self, tmp_path):
        cfg = _write_config(tmp_path, {"VCF": {"fakesut": ["com/example/core"]}})
        report = _write_jacoco_xml(tmp_path)
        r1 = mc.measure(report_path=report, sut="fakesut",
                        format_="VCF", config_path=cfg, label="A")
        r2 = mc.measure(report_path=report, sut="fakesut",
                        format_="VCF", config_path=cfg, label="B")
        lines = mc._format_comparison([r1, r2])
        text = "\n".join(lines)
        assert "Side-by-side" in text
        assert "Deltas vs A" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
