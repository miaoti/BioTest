"""
Tests for the Tier-2a per-class blindspot helper
(``test_engine.feedback.blindspot_builder.compute_class_level_gaps``).

These tests use FIXTURE coverage reports — not a real SUT — so they run
in milliseconds and stay SUT-agnostic. They exercise:

  1. JaCoCo XML parsing with the same 3-path filter BioTest uses.
  2. coverage.py JSON parsing with a two-module fixture.
  3. gcovr JSON parsing with a two-file fixture.
  4. Graceful empty return for missing / malformed reports.
  5. BlindspotTicket renders the class-gap block only when populated.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from test_engine.feedback.blindspot_builder import (
    BlindspotTicket,
    ClassGap,
    compute_class_level_gaps,
)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------

def _write_jacoco_fixture(tmp_path: Path) -> Path:
    """A tiny JaCoCo XML with two packages × two sourcefiles each."""
    xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<report name="fixture">
  <package name="com/example/core">
    <sourcefile name="Biggie.java">
      <counter type="LINE" missed="80" covered="20"/>
    </sourcefile>
    <sourcefile name="Smallie.java">
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
    path = tmp_path / "jacoco.xml"
    path.write_text(xml, encoding="utf-8")
    return path


def _write_coveragepy_fixture(tmp_path: Path) -> Path:
    """A tiny coverage.py-style JSON with three modules."""
    data = {
        "meta": {"format": 2},
        "files": {
            "Bio/Align/sam.py": {
                "summary": {"covered_lines": 30, "num_statements": 100},
            },
            "Bio/SeqIO/FastaIO.py": {
                "summary": {"covered_lines": 40, "num_statements": 50},
            },
            "somewhere/else/module.py": {
                "summary": {"covered_lines": 5, "num_statements": 20},
            },
        },
    }
    path = tmp_path / "coverage.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _write_gcovr_fixture(tmp_path: Path) -> Path:
    """gcovr JSON: {"files": [{"file": ..., "lines": [{...}, ...]}]}"""
    data = {
        "files": [
            {
                "file": "include/seqan3/io/sam_file.hpp",
                "lines": [
                    {"line_number": 1, "count": 10},
                    {"line_number": 2, "count": 0},
                    {"line_number": 3, "count": 5},
                    {"line_number": 4, "count": 0},
                    {"line_number": 5, "count": 0},
                ],
            },
            {
                "file": "include/seqan3/unrelated.hpp",
                "lines": [{"line_number": 1, "count": 1}],
            },
        ],
    }
    path = tmp_path / "gcovr.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# JaCoCo XML
# ---------------------------------------------------------------------------

class TestJacocoClassGaps:
    def test_without_filter_ranks_by_missed_lines(self, tmp_path):
        fx = _write_jacoco_fixture(tmp_path)
        gaps = compute_class_level_gaps(fx, filter_rules_text=None, top_n=10)
        names = [g.name for g in gaps]
        # Biggie.java has 80 missed → top of the list.
        assert names[0].endswith(".Biggie")
        # JEXLExpr second (50 missed) unless filtered.
        assert any(n.endswith(".JEXLExpr") for n in names)

    def test_filter_excludes_jexl(self, tmp_path):
        fx = _write_jacoco_fixture(tmp_path)
        gaps = compute_class_level_gaps(
            fx,
            filter_rules_text=[
                "com/example/core",
                "com/example/jexl::-JEXL,-Jexl,-*JEXL*,-*Jexl*",
            ],
            top_n=10,
        )
        names = [g.name for g in gaps]
        assert any(n.endswith(".Biggie") for n in names)
        assert not any("JEXL" in n or "Jexl" in n for n in names)

    def test_top_n_truncation(self, tmp_path):
        fx = _write_jacoco_fixture(tmp_path)
        gaps = compute_class_level_gaps(fx, top_n=2)
        assert len(gaps) == 2

    def test_qualified_name_is_dotted(self, tmp_path):
        fx = _write_jacoco_fixture(tmp_path)
        gaps = compute_class_level_gaps(fx, top_n=10)
        # Expect dotted-FQN for Java: package path + class stem.
        top = gaps[0]
        assert top.name == "com.example.core.Biggie"


# ---------------------------------------------------------------------------
# coverage.py JSON
# ---------------------------------------------------------------------------

class TestCoveragePyClassGaps:
    def test_returns_per_module_entries(self, tmp_path):
        fx = _write_coveragepy_fixture(tmp_path)
        gaps = compute_class_level_gaps(fx, filter_rules_text=None, top_n=10)
        names = [g.name for g in gaps]
        # Bio/Align/sam.py has 70 missed lines → top.
        assert names[0] == "Bio/Align/sam.py"

    def test_filter_by_prefix(self, tmp_path):
        fx = _write_coveragepy_fixture(tmp_path)
        gaps = compute_class_level_gaps(
            fx, filter_rules_text=["Bio"], top_n=10,
        )
        names = [g.name for g in gaps]
        # Both Bio/* modules kept, the "somewhere/else/" one dropped.
        assert "somewhere/else/module.py" not in names

    def test_skips_zero_statements(self, tmp_path):
        path = tmp_path / "cov.json"
        path.write_text(json.dumps({
            "files": {
                "zero.py": {"summary": {"covered_lines": 0, "num_statements": 0}},
            },
        }), encoding="utf-8")
        gaps = compute_class_level_gaps(path, top_n=10)
        assert gaps == []


# ---------------------------------------------------------------------------
# gcovr JSON
# ---------------------------------------------------------------------------

class TestGcovrClassGaps:
    def test_parses_line_list(self, tmp_path):
        fx = _write_gcovr_fixture(tmp_path)
        gaps = compute_class_level_gaps(fx, top_n=10)
        names = [g.name for g in gaps]
        assert "include/seqan3/io/sam_file.hpp" in names

    def test_filter_by_include_prefix(self, tmp_path):
        fx = _write_gcovr_fixture(tmp_path)
        gaps = compute_class_level_gaps(
            fx,
            filter_rules_text=["include/seqan3/io"],
            top_n=10,
        )
        names = [g.name for g in gaps]
        assert "include/seqan3/unrelated.hpp" not in names


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_none_path_returns_empty(self):
        assert compute_class_level_gaps(None) == []

    def test_missing_path_returns_empty(self, tmp_path):
        assert compute_class_level_gaps(tmp_path / "does_not_exist.xml") == []

    def test_malformed_xml_returns_empty(self, tmp_path):
        p = tmp_path / "bad.xml"
        p.write_text("<not-a-report/>", encoding="utf-8")
        assert compute_class_level_gaps(p) == []

    def test_malformed_json_returns_empty(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{ not json", encoding="utf-8")
        assert compute_class_level_gaps(p) == []


# ---------------------------------------------------------------------------
# BlindspotTicket rendering
# ---------------------------------------------------------------------------

class TestTicketRendersClassGapBlock:
    def test_empty_class_gaps_omits_block(self):
        ticket = BlindspotTicket(
            uncovered_rules=[{"chunk_id": "c1", "severity": "CRITICAL",
                              "section_id": "s1", "spec_text": "demo"}],
            iteration=1,
            primary_target="anysut",
            format_context="VCF",
            total_uncovered=1, shown_uncovered=1, remaining_uncovered=0,
        )
        out = ticket.to_prompt_fragment()
        assert "TOP UNCOVERED CLASSES" not in out

    def test_populated_class_gaps_renders_block(self):
        gaps = [
            ClassGap(name="com.example.Big", covered=10, total=100),
            ClassGap(name="com.example.Small", covered=5, total=10),
        ]
        ticket = BlindspotTicket(
            uncovered_rules=[{"chunk_id": "c1", "severity": "CRITICAL",
                              "section_id": "s1", "spec_text": "demo"}],
            iteration=1,
            primary_target="anysut",
            format_context="VCF",
            total_uncovered=1, shown_uncovered=1, remaining_uncovered=0,
            class_gaps=gaps,
        )
        out = ticket.to_prompt_fragment()
        assert "TOP UNCOVERED CLASSES" in out
        assert "com.example.Big" in out
        # Percentages rendered with one decimal.
        assert "10.0%" in out
        assert "50.0%" in out

    def test_class_gap_post_init_computes_missed_and_pct(self):
        g = ClassGap(name="X", covered=30, total=120)
        assert g.missed == 90
        assert g.pct == 25.0

    def test_class_gap_zero_total_pct_is_zero(self):
        g = ClassGap(name="Y", covered=0, total=0)
        assert g.pct == 0.0
        assert g.missed == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
