"""
Tests for Phase C: Transform dispatch wrapper.
"""

import pytest
from pathlib import Path

from test_engine.generators.dispatch import apply_transform, apply_mr_transforms
from test_engine.canonical.vcf_normalizer import normalize_vcf_text
from test_engine.canonical.sam_normalizer import normalize_sam_text

SEEDS_DIR = Path(__file__).parent.parent / "seeds"


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


class TestVcfDispatch:
    def test_shuffle_meta_lines(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("shuffle_meta_lines", lines, seed=42)
        # fileformat must still be first
        assert result[0].startswith("##fileformat")
        # Same number of lines
        assert len(result) == len(lines)
        # Still valid VCF
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5

    def test_permute_structured_kv(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("permute_structured_kv_order", lines, seed=42)
        # All structured meta lines still present and valid
        structured = [l for l in result if l.startswith("##") and "=<" in l]
        assert len(structured) > 0
        # Still parseable
        canonical = normalize_vcf_text(result)
        assert canonical.header.fileformat == "VCFv4.3"

    def test_shuffle_info_kv(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("shuffle_info_field_kv", lines, seed=42)
        # Still parseable, same number of records
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5

    def test_permute_sample_columns(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("permute_sample_columns", lines, seed=42)
        canonical = normalize_vcf_text(result)
        # Same 3 samples (possibly reordered)
        assert set(canonical.header.samples) == {"NA00001", "NA00002", "NA00003"}

    def test_inject_missing_values(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "minimal_multisample.vcf")
        result = apply_transform("inject_equivalent_missing_values", lines, seed=42)
        canonical = normalize_vcf_text(result)
        # FORMAT should have extra field
        assert len(canonical.records[0].FORMAT) > 3

    def test_compound_alt_permutation(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        # Apply the compound group
        result = apply_mr_transforms(
            lines,
            ["choose_permutation", "permute_ALT", "remap_GT", "permute_Number_A_R_fields"],
            seed=42,
        )
        # Still parseable
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5
        # Mono-ALT records should be unchanged
        # Multi-ALT records should have reordered ALT


class TestSamDispatch:
    def test_permute_optional_tags(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "spec_example.sam")
        result = apply_transform("permute_optional_tag_fields", lines, seed=42)
        canonical = normalize_sam_text(result)
        assert len(canonical.records) == 4

    def test_reorder_header(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "spec_example.sam")
        result = apply_transform("reorder_header_records", lines, seed=42)
        canonical = normalize_sam_text(result)
        # @HD must still be first
        assert result[0].startswith("@HD")
        assert len(canonical.header.SQ) == 2

    def test_cigar_split_merge(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "minimal_tags.sam")
        result = apply_transform("split_or_merge_adjacent_cigar_ops", lines, seed=42)
        canonical = normalize_sam_text(result)
        assert len(canonical.records) == 2

    def test_toggle_clipping(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "complex_cigar.sam")
        result = apply_transform("toggle_cigar_hard_soft_clipping", lines, seed=42)
        canonical = normalize_sam_text(result)
        assert len(canonical.records) >= 2


class TestDispatchMRTransforms:
    def test_single_step_mr(self):
        """Simulate MR: shuffle_meta_lines."""
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_mr_transforms(lines, ["shuffle_meta_lines"], seed=42)
        assert result[0].startswith("##fileformat")

    def test_unknown_transform_raises(self):
        lines = ["test\n"]
        with pytest.raises(ValueError, match="No dispatch wrapper"):
            apply_transform("nonexistent_transform", lines, seed=42)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
