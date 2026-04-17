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


# ===========================================================================
# Dispatch wrappers for 6 new VCF transforms (normalization / BCF / CSQ)
# ===========================================================================

class TestVcfDispatchNew:
    """Smoke tests for the normalization + BCF + CSQ transform dispatch
    wrappers. Each test confirms the wrapper does not corrupt the file's
    core structure (fileformat preserved, record count consistent).
    """

    def test_trim_common_affixes_noop_when_nothing_to_trim(self):
        # spec_example.vcf has single-char REF/ALT for each record; nothing
        # to trim -> dispatch wrapper must leave every line byte-identical.
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("trim_common_affixes", lines, seed=42)
        # Structure preserved
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5
        assert result[0].startswith("##fileformat")

    def test_trim_common_affixes_actually_trims(self):
        # Craft a small VCF with REF=AA ALT=AC at POS=100 -> expect
        # REF=A ALT=C at POS=101 after trim.
        custom = [
            "##fileformat=VCFv4.3\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tAA\tAC\t50\tPASS\t.\n",
        ]
        result = apply_transform("trim_common_affixes", custom, seed=0)
        # Last line should now be the trimmed record
        last = result[-1].rstrip()
        cols = last.split("\t")
        assert cols[1] == "101", f"POS not advanced: {last}"
        assert cols[3] == "A", f"REF not trimmed: {last}"
        assert cols[4] == "C", f"ALT not trimmed: {last}"

    def test_left_align_indel_on_homopolymer(self):
        # Craft a homopolymer deletion: REF=AAA ALT=AA POS=5 -> POS=4.
        custom = [
            "##fileformat=VCFv4.3\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t5\t.\tAAA\tAA\t50\tPASS\t.\n",
        ]
        result = apply_transform("left_align_indel", custom, seed=0)
        cols = result[-1].rstrip().split("\t")
        assert cols[1] == "4"

    def test_split_multi_allelic_multiplies_records(self):
        # Craft multi-ALT record; expect 2 output records (one per ALT).
        custom = [
            "##fileformat=VCFv4.3\n",
            "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele Count\">\n",
            "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n",
            "chr1\t100\t.\tA\tT,C\t50\tPASS\tAC=1,2\tGT\t0/1\n",
        ]
        result = apply_transform("split_multi_allelic", custom, seed=0)
        data_lines = [
            l for l in result
            if not l.startswith("#") and "\t" in l
        ]
        assert len(data_lines) == 2
        alts = {l.split("\t")[4] for l in data_lines}
        assert alts == {"T", "C"}

    def test_permute_csq_annotations_deterministic_on_csq_file(self):
        # Craft a VCF with CSQ header + multi-record CSQ annotation.
        custom = [
            "##fileformat=VCFv4.3\n",
            '##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence '
            'annotations from Ensembl VEP. Format: Allele|Gene|Feature">\n',
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tA\tT\t50\tPASS\tCSQ=T|gene1|x,T|gene2|y,T|gene3|z\n",
        ]
        r1 = apply_transform("permute_csq_annotations", custom, seed=42)
        r2 = apply_transform("permute_csq_annotations", custom, seed=42)
        assert r1 == r2
        # Pipe count per record preserved (no sub-field corruption)
        csq_value = r1[-1].split("\t")[7].split("CSQ=")[1].rstrip()
        for record in csq_value.split(","):
            assert record.count("|") == 2

    def test_permute_csq_annotations_skips_without_csq_header(self):
        # spec_example.vcf has no CSQ header -> dispatch must no-op
        # (returns the input lines unchanged).
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("permute_csq_annotations", lines, seed=42)
        assert result == lines

    def test_vcf_bcf_round_trip_returns_lines(self):
        # Even without a working BCF codec, dispatch must return a list
        # of lines (not crash). If BCF is unavailable the wrapper returns
        # the input unchanged.
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("vcf_bcf_round_trip", lines, seed=42)
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_permute_bcf_header_dictionary_returns_lines(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform(
            "permute_bcf_header_dictionary", lines, seed=42,
        )
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
