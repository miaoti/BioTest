"""
T6-T7: Triage idempotency + evidence Markdown formatting tests.

Tests that bug report generation is robust against concurrent calls,
filesystem edge cases, and special characters in evidence text.
"""

import json
import threading
import tempfile
from pathlib import Path

import pytest

from test_engine.triage.report_builder import build_bug_report
from test_engine.triage.classifier import (
    classify_failure,
    ClassifiedFailure,
    FailureType,
)
from test_engine.triage.evidence_formatter import format_evidence
from test_engine.oracles.metamorphic import OracleResult
from test_engine.runners.base import RunnerResult


SEEDS_DIR = Path(__file__).parent.parent / "seeds"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_oracle_result(passed=False, diffs=None, error_type=None):
    """Build a minimal OracleResult for testing."""
    return OracleResult(
        passed=passed,
        mr_id="test_mr_001",
        mr_name="test_metamorphic_relation",
        parser_name="test_parser",
        differences=diffs or ["$.records[0].POS: 100 != 200"],
        error_type=error_type,
        original_result=RunnerResult(
            success=True,
            canonical_json={"format": "VCF", "records": [{"POS": 100}]},
            parser_name="test_parser",
            format_type="VCF",
        ),
        transformed_result=RunnerResult(
            success=True,
            canonical_json={"format": "VCF", "records": [{"POS": 200}]},
            parser_name="test_parser",
            format_type="VCF",
        ),
    )


def _make_mr_dict(**overrides):
    base = {
        "mr_id": "test_mr_001",
        "mr_name": "test_relation",
        "scope": "VCF.header",
        "oracle": "test oracle description",
        "transform_steps": ["shuffle_meta_lines"],
        "preconditions": ["has meta lines"],
        "evidence": [{
            "chunk_id": "VCFv4.5.tex::Meta-information::p121",
            "quote": "Implementations must not rely on field ordering.",
            "rule_severity": "CRITICAL",
            "section_id": "Meta-information lines",
        }],
        "ambiguity_flags": [],
    }
    base.update(overrides)
    return base


# ===========================================================================
# T6: Concurrent report builder — directory scaffolding
# ===========================================================================

class TestReportBuilderConcurrency:
    """Multiple concurrent calls must not crash with FileExistsError."""

    def test_concurrent_report_generation(self, tmp_path):
        """3 threads generating bug reports simultaneously must all succeed."""
        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
        oracle_result = _make_oracle_result()
        classified = ClassifiedFailure(
            failure_type=FailureType.METAMORPHIC_VIOLATION,
            severity="CRITICAL",
            mr_id="test_mr_001",
            mr_name="test_relation",
            parser_name="test_parser",
            description="test failure",
            differences=["$.POS: 100 != 200"],
        )
        mr_dict = _make_mr_dict()

        results = []
        errors = []

        def gen_report():
            try:
                path = build_bug_report(
                    classified=classified,
                    seed_path=seed,
                    transformed_path=None,
                    oracle_result=oracle_result,
                    mr_dict=mr_dict,
                    output_dir=tmp_path,
                )
                results.append(path)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=gen_report) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        assert len(errors) == 0, f"Concurrent report generation failed: {errors}"
        assert len(results) == 3
        # All directories must be distinct (timestamps differ)
        assert len(set(str(r) for r in results)) == 3

    def test_report_contains_all_artifacts(self, tmp_path):
        """Every required file must exist in the generated bundle."""
        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
        oracle_result = _make_oracle_result()
        classified = ClassifiedFailure(
            failure_type=FailureType.METAMORPHIC_VIOLATION,
            severity="CRITICAL",
            mr_id="test_mr_001",
            mr_name="test_relation",
            parser_name="test_parser",
            description="test failure",
            differences=["$.POS: 100 != 200"],
        )
        mr_dict = _make_mr_dict()

        bug_dir = build_bug_report(
            classified=classified,
            seed_path=seed,
            transformed_path=None,
            oracle_result=oracle_result,
            mr_dict=mr_dict,
            output_dir=tmp_path,
        )

        # Check required files
        assert (bug_dir / "evidence.md").exists()
        assert (bug_dir / "summary.json").exists()
        assert (bug_dir / "canonical_outputs").is_dir()
        assert (bug_dir / "logs").is_dir()
        assert (bug_dir / "minimal_single.vcf").exists()

        # summary.json must be valid JSON
        summary = json.loads((bug_dir / "summary.json").read_text(encoding="utf-8"))
        assert summary["failure_type"] == "metamorphic_violation"
        assert summary["mr_id"] == "test_mr_001"

    def test_report_with_no_canonical_output(self, tmp_path):
        """Report must still be generated even if parser produced no JSON."""
        seed = SEEDS_DIR / "vcf" / "minimal_single.vcf"
        oracle_result = OracleResult(
            passed=False,
            mr_id="crash_mr",
            mr_name="crash_test",
            parser_name="broken_parser",
            differences=["Parser crashed"],
            error_type="crash",
            original_result=RunnerResult(
                success=False, parser_name="broken_parser",
                format_type="VCF", error_type="crash",
                stderr="Segfault",
            ),
            transformed_result=None,
        )
        classified = ClassifiedFailure(
            failure_type=FailureType.CRASH,
            severity="CRITICAL",
            mr_id="crash_mr",
            mr_name="crash_test",
            parser_name="broken_parser",
            description="Parser crashed",
            differences=["Parser crashed"],
        )
        mr_dict = _make_mr_dict(mr_id="crash_mr", mr_name="crash_test")

        bug_dir = build_bug_report(
            classified=classified,
            seed_path=seed,
            transformed_path=None,
            oracle_result=oracle_result,
            mr_dict=mr_dict,
            output_dir=tmp_path,
        )

        assert bug_dir.exists()
        assert (bug_dir / "evidence.md").exists()
        assert (bug_dir / "summary.json").exists()


# ===========================================================================
# T7: Evidence Markdown formatting — special characters
# ===========================================================================

class TestEvidenceMarkdownFormatting:
    """Evidence formatter must handle special chars without breaking Markdown."""

    def test_basic_formatting(self):
        mr = _make_mr_dict()
        md = format_evidence(mr)
        assert "# Evidence Report:" in md
        assert "**MR ID**:" in md
        assert "`test_relation`" in md or "test_relation" in md
        assert "CRITICAL" in md

    def test_backticks_in_quote(self):
        """Backticks in spec quotes must not break Markdown code spans."""
        mr = _make_mr_dict(evidence=[{
            "chunk_id": "VCFv4.5.tex::test::p1",
            "quote": "The field `INFO` must contain `Number=A` entries",
            "rule_severity": "CRITICAL",
            "section_id": "test section",
        }])
        md = format_evidence(mr)
        assert "`INFO`" in md
        assert "`Number=A`" in md

    def test_newlines_in_quote(self):
        """Newlines in spec quotes must be preserved."""
        mr = _make_mr_dict(evidence=[{
            "chunk_id": "VCFv4.5.tex::test::p1",
            "quote": "Line one.\nLine two.\nLine three.",
            "rule_severity": "ADVISORY",
            "section_id": "test section",
        }])
        md = format_evidence(mr)
        assert "Line one." in md
        assert "ADVISORY" in md

    def test_unicode_in_evidence(self):
        """Unicode characters must not crash the formatter."""
        mr = _make_mr_dict(evidence=[{
            "chunk_id": "SAMv1.tex::test::p1",
            "quote": "The field \u2265 (greater-than-or-equal) is used for quality scores",
            "rule_severity": "INFORMATIONAL",
            "section_id": "Quality scores",
        }])
        md = format_evidence(mr)
        assert "\u2265" in md

    def test_empty_evidence_list(self):
        """Empty evidence must produce valid Markdown without crashing."""
        mr = _make_mr_dict(evidence=[])
        md = format_evidence(mr)
        assert "# Evidence Report:" in md
        assert "## Specification Evidence" in md

    def test_ambiguity_flags_rendered(self):
        """Ambiguity flags must appear in the output."""
        mr = _make_mr_dict(ambiguity_flags=[
            "Spec is ambiguous about empty ALT handling",
            "Implementation-defined behavior",
        ])
        md = format_evidence(mr)
        assert "Ambiguity Flags" in md
        assert "Spec is ambiguous" in md
        assert "Implementation-defined" in md

    def test_multiple_evidence_entries(self):
        """Multiple evidence entries must each get their own section."""
        mr = _make_mr_dict(evidence=[
            {"chunk_id": "c1", "quote": "Quote 1", "rule_severity": "CRITICAL", "section_id": "s1"},
            {"chunk_id": "c2", "quote": "Quote 2", "rule_severity": "ADVISORY", "section_id": "s2"},
            {"chunk_id": "c3", "quote": "Quote 3", "rule_severity": "INFORMATIONAL", "section_id": "s3"},
        ])
        md = format_evidence(mr)
        assert "### Evidence 1" in md
        assert "### Evidence 2" in md
        assert "### Evidence 3" in md


# ===========================================================================
# Classifier tests
# ===========================================================================

class TestFailureClassifier:
    """Failure type classification logic."""

    def test_crash_classified_correctly(self):
        oracle_result = _make_oracle_result(error_type="crash")
        classified = classify_failure(oracle_result, _make_mr_dict())
        assert classified.failure_type == FailureType.CRASH

    def test_timeout_classified_as_crash(self):
        oracle_result = _make_oracle_result(error_type="timeout")
        classified = classify_failure(oracle_result, _make_mr_dict())
        assert classified.failure_type == FailureType.CRASH

    def test_metamorphic_violation_classified(self):
        oracle_result = _make_oracle_result(error_type=None)
        classified = classify_failure(oracle_result, _make_mr_dict())
        assert classified.failure_type == FailureType.METAMORPHIC_VIOLATION
        assert classified.severity == "CRITICAL"

    def test_classified_preserves_parser_name(self):
        oracle_result = _make_oracle_result()
        classified = classify_failure(oracle_result, _make_mr_dict())
        assert classified.parser_name == "test_parser"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
