"""
Tests for B5: DSL Models & Compiler.

Tests whitelist enforcement, deterministic hashing, JSON extraction,
and error message formatting.
"""

import json
import pytest

from mr_engine.dsl.models import (
    RawMRFromAgent,
    RawEvidence,
    HydratedEvidence,
    MetamorphicRelation,
    compute_mr_id,
)
from mr_engine.dsl.compiler import _extract_json, CompilationResult
from pydantic import ValidationError


# ===========================================================================
# Model validation tests
# ===========================================================================

class TestRawMRFromAgent:
    VALID_DATA = {
        "mr_name": "VCF Header Shuffle",
        "scope": "VCF.header",
        "preconditions": ["has meta lines"],
        "transform_steps": ["shuffle_meta_lines"],
        "oracle": "header semantics preserved",
        "evidence": [{"chunk_id": "c1", "quote": "spec says so"}],
        "ambiguity_flags": [],
    }

    def test_valid_mr(self):
        mr = RawMRFromAgent.model_validate(self.VALID_DATA)
        assert mr.mr_name == "VCF Header Shuffle"

    def test_unknown_transform_rejected(self):
        data = {**self.VALID_DATA, "transform_steps": ["nonexistent_op"]}
        with pytest.raises(ValidationError) as exc_info:
            RawMRFromAgent.model_validate(data)
        assert "nonexistent_op" in str(exc_info.value)
        assert "whitelist" in str(exc_info.value).lower()

    def test_empty_transform_rejected(self):
        data = {**self.VALID_DATA, "transform_steps": []}
        with pytest.raises(ValidationError):
            RawMRFromAgent.model_validate(data)

    def test_empty_evidence_rejected(self):
        data = {**self.VALID_DATA, "evidence": []}
        with pytest.raises(ValidationError):
            RawMRFromAgent.model_validate(data)

    def test_invalid_scope_rejected(self):
        data = {**self.VALID_DATA, "scope": "FASTQ.record"}
        with pytest.raises(ValidationError):
            RawMRFromAgent.model_validate(data)

    def test_valid_scopes(self):
        for scope in ["VCF.header", "VCF.record", "SAM.header", "SAM.record"]:
            data = {**self.VALID_DATA, "scope": scope}
            mr = RawMRFromAgent.model_validate(data)
            assert mr.scope == scope


class TestCompoundStepValidator:
    """Enforce all-or-nothing rule for the ALT permutation compound group."""

    # All four compound members present — must pass
    ALL_FOUR = [
        "choose_permutation",
        "permute_ALT",
        "remap_GT",
        "permute_Number_A_R_fields",
    ]

    BASE = {
        "mr_name": "ALT Permutation",
        "scope": "VCF.record",
        "preconditions": [],
        "oracle": "semantics preserved after ALT reorder",
        "evidence": [{"chunk_id": "c1", "quote": "spec says so"}],
        "ambiguity_flags": [],
    }

    def test_all_four_present_passes(self):
        data = {**self.BASE, "transform_steps": list(self.ALL_FOUR)}
        mr = RawMRFromAgent.model_validate(data)
        assert set(mr.transform_steps) == set(self.ALL_FOUR)

    def test_all_four_in_any_order_passes(self):
        data = {**self.BASE, "transform_steps": list(reversed(self.ALL_FOUR))}
        mr = RawMRFromAgent.model_validate(data)
        assert len(mr.transform_steps) == 4

    def test_single_compound_member_rejected(self):
        """Only permute_ALT without its companions must fail."""
        data = {**self.BASE, "transform_steps": ["permute_ALT"]}
        with pytest.raises(ValidationError) as exc_info:
            RawMRFromAgent.model_validate(data)
        err = str(exc_info.value)
        assert "Compound-step violation" in err
        assert "choose_permutation" in err
        assert "remap_GT" in err
        assert "permute_Number_A_R_fields" in err

    def test_two_of_four_rejected(self):
        """permute_ALT + remap_GT without the other two must fail."""
        data = {**self.BASE, "transform_steps": ["permute_ALT", "remap_GT"]}
        with pytest.raises(ValidationError) as exc_info:
            RawMRFromAgent.model_validate(data)
        err = str(exc_info.value)
        assert "choose_permutation" in err
        assert "permute_Number_A_R_fields" in err
        # The two present ones should NOT be listed as missing
        assert "missing ['choose_permutation', 'permute_Number_A_R_fields']" in err

    def test_three_of_four_rejected(self):
        """Missing just one member must still fail."""
        data = {**self.BASE, "transform_steps": [
            "choose_permutation", "permute_ALT", "remap_GT"
        ]}
        with pytest.raises(ValidationError) as exc_info:
            RawMRFromAgent.model_validate(data)
        err = str(exc_info.value)
        assert "permute_Number_A_R_fields" in err

    def test_non_compound_transforms_unaffected(self):
        """Standalone transforms should not trigger compound validation."""
        data = {
            **self.BASE,
            "scope": "VCF.header",
            "transform_steps": ["shuffle_meta_lines"],
        }
        mr = RawMRFromAgent.model_validate(data)
        assert mr.transform_steps == ["shuffle_meta_lines"]

    def test_compound_plus_extra_transforms_passes(self):
        """All four compound members + extra non-compound transforms must pass."""
        data = {**self.BASE, "transform_steps": [
            *self.ALL_FOUR, "shuffle_info_field_kv",
        ]}
        mr = RawMRFromAgent.model_validate(data)
        assert len(mr.transform_steps) == 5

    def test_error_message_lists_all_required_members(self):
        """The error must include the full required set so the LLM can fix it."""
        data = {**self.BASE, "transform_steps": ["choose_permutation"]}
        with pytest.raises(ValidationError) as exc_info:
            RawMRFromAgent.model_validate(data)
        err = str(exc_info.value)
        # All four names must appear in the error for the LLM retry loop
        for name in self.ALL_FOUR:
            assert name in err, f"Expected '{name}' in error message"


class TestHydratedEvidence:
    def test_valid_severities(self):
        for sev in ["CRITICAL", "ADVISORY", "INFORMATIONAL"]:
            ev = HydratedEvidence(
                chunk_id="c1", quote="q", rule_severity=sev, section_id="s1"
            )
            assert ev.rule_severity == sev

    def test_invalid_severity_rejected(self):
        with pytest.raises(ValidationError):
            HydratedEvidence(
                chunk_id="c1", quote="q", rule_severity="HIGH", section_id="s1"
            )


# ===========================================================================
# Deterministic hashing tests
# ===========================================================================

class TestComputeMrId:
    def test_deterministic(self):
        id1 = compute_mr_id("VCF.record", ["permute_ALT", "remap_GT"])
        id2 = compute_mr_id("VCF.record", ["permute_ALT", "remap_GT"])
        assert id1 == id2

    def test_order_independent(self):
        """Same transforms in different order produce same hash (sorted internally)."""
        id1 = compute_mr_id("VCF.record", ["remap_GT", "permute_ALT"])
        id2 = compute_mr_id("VCF.record", ["permute_ALT", "remap_GT"])
        assert id1 == id2

    def test_different_scope_different_id(self):
        id1 = compute_mr_id("VCF.record", ["shuffle_meta_lines"])
        id2 = compute_mr_id("SAM.record", ["shuffle_meta_lines"])
        assert id1 != id2

    def test_different_transforms_different_id(self):
        id1 = compute_mr_id("VCF.record", ["shuffle_meta_lines"])
        id2 = compute_mr_id("VCF.record", ["shuffle_info_field_kv"])
        assert id1 != id2

    def test_hash_length(self):
        mr_id = compute_mr_id("VCF.record", ["shuffle_meta_lines"])
        assert len(mr_id) == 12
        assert all(c in "0123456789abcdef" for c in mr_id)


# ===========================================================================
# JSON extraction tests
# ===========================================================================

class TestExtractJson:
    def test_raw_array(self):
        text = '[{"key": "value"}]'
        assert _extract_json(text) == text

    def test_raw_object(self):
        text = '{"relations": []}'
        assert _extract_json(text) == text

    def test_markdown_fenced(self):
        text = 'Here is the result:\n```json\n[{"key": "value"}]\n```\nDone.'
        result = _extract_json(text)
        assert result == '[{"key": "value"}]'

    def test_markdown_no_lang(self):
        text = '```\n{"key": "value"}\n```'
        result = _extract_json(text)
        assert result == '{"key": "value"}'

    def test_no_json_returns_none(self):
        assert _extract_json("no json here") is None

    def test_whitespace_around_json(self):
        text = "  \n  [1, 2, 3]  \n  "
        assert _extract_json(text) == "[1, 2, 3]"


# ===========================================================================
# Run
# ===========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
