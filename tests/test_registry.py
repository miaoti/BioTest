"""
Tests for B6: Triage Registry.

Tests classification logic (enforced vs quarantine) and deduplication by mr_id.
"""

import json
import os
import tempfile

import pytest

from mr_engine.dsl.models import MetamorphicRelation, HydratedEvidence
from mr_engine.registry import triage, export_registry, MRRegistry


def _make_mr(
    mr_id: str = "abc123",
    mr_name: str = "Test MR",
    scope: str = "VCF.record",
    severities: list[str] | None = None,
    ambiguity_flags: list[str] | None = None,
) -> MetamorphicRelation:
    """Helper to build a MetamorphicRelation with specified characteristics."""
    if severities is None:
        severities = ["CRITICAL"]
    evidence = [
        HydratedEvidence(
            chunk_id=f"chunk_{i}",
            quote=f"spec quote {i}",
            rule_severity=sev,
            section_id=f"section_{i}",
        )
        for i, sev in enumerate(severities)
    ]
    return MetamorphicRelation(
        mr_id=mr_id,
        mr_name=mr_name,
        scope=scope,
        preconditions=["test"],
        transform_steps=["shuffle_meta_lines"],
        oracle="test oracle",
        evidence=evidence,
        ambiguity_flags=ambiguity_flags or [],
    )


class TestTriage:
    def test_all_critical_no_flags_is_enforced(self):
        mr = _make_mr(severities=["CRITICAL", "CRITICAL"])
        reg = triage([mr])
        assert mr.mr_id in reg.enforced
        assert mr.mr_id not in reg.quarantine

    def test_any_advisory_is_quarantine(self):
        mr = _make_mr(severities=["CRITICAL", "ADVISORY"])
        reg = triage([mr])
        assert mr.mr_id in reg.quarantine
        assert mr.mr_id not in reg.enforced

    def test_informational_is_quarantine(self):
        mr = _make_mr(severities=["INFORMATIONAL"])
        reg = triage([mr])
        assert mr.mr_id in reg.quarantine

    def test_ambiguity_flags_force_quarantine(self):
        mr = _make_mr(
            severities=["CRITICAL"],
            ambiguity_flags=["spec says MAY"],
        )
        reg = triage([mr])
        assert mr.mr_id in reg.quarantine

    def test_dedup_by_mr_id(self):
        mr1 = _make_mr(mr_id="same_id", mr_name="First")
        mr2 = _make_mr(mr_id="same_id", mr_name="Second")
        reg = triage([mr1, mr2])
        assert reg.total == 1
        # First one wins
        assert list(reg.enforced.values())[0].mr_name == "First"

    def test_mixed_tiers(self):
        enforced = _make_mr(mr_id="e1", severities=["CRITICAL"])
        quarantine = _make_mr(mr_id="q1", severities=["ADVISORY"])
        reg = triage([enforced, quarantine])
        assert len(reg.enforced) == 1
        assert len(reg.quarantine) == 1
        assert reg.total == 2

    def test_empty_input(self):
        reg = triage([])
        assert reg.total == 0


class TestExportRegistry:
    def test_export_creates_valid_json(self):
        mr = _make_mr(mr_id="test_export")
        reg = triage([mr])

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            path = f.name

        try:
            export_registry(reg, path)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert "enforced" in data
            assert "quarantine" in data
            assert "summary" in data
            assert data["summary"]["enforced_count"] == 1
            assert data["summary"]["quarantine_count"] == 0
            assert data["summary"]["total"] == 1
            assert data["enforced"][0]["mr_id"] == "test_export"
        finally:
            os.unlink(path)


class TestMRRegistry:
    def test_total_property(self):
        reg = MRRegistry()
        assert reg.total == 0
        reg.enforced["a"] = _make_mr(mr_id="a")
        assert reg.total == 1
        reg.quarantine["b"] = _make_mr(mr_id="b")
        assert reg.total == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
