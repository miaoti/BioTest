"""
Tests for Phase C: Canonical JSON schema and normalizers.
"""

import pytest
from pathlib import Path

from test_engine.canonical.schema import (
    CanonicalVcf, CanonicalVcfHeader, CanonicalVcfRecord,
    CanonicalSam, CanonicalSamHeader, CanonicalSamRecord,
    CigarOp,
)
from test_engine.canonical.vcf_normalizer import normalize_vcf_text
from test_engine.canonical.sam_normalizer import normalize_sam_text

SEEDS_DIR = Path(__file__).parent.parent / "seeds"


class TestVcfNormalizer:
    def test_parse_minimal_vcf(self):
        lines = (SEEDS_DIR / "vcf" / "minimal_single.vcf").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_vcf_text(lines)
        assert result.format == "VCF"
        assert result.header.fileformat == "VCFv4.3"
        assert result.header.samples == ["SAMPLE1"]
        assert len(result.records) == 1
        rec = result.records[0]
        assert rec.CHROM == "chr1"
        assert rec.POS == 100
        assert rec.REF == "A"
        assert rec.ALT == ["C"]
        assert rec.QUAL == 30.0

    def test_parse_multisample_vcf(self):
        lines = (SEEDS_DIR / "vcf" / "minimal_multisample.vcf").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_vcf_text(lines)
        assert len(result.header.samples) == 2
        assert "SAMPLE1" in result.header.samples
        assert len(result.records) == 2

    def test_parse_spec_example(self):
        lines = (SEEDS_DIR / "vcf" / "spec_example.vcf").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_vcf_text(lines)
        assert result.header.fileformat == "VCFv4.3"
        assert len(result.header.samples) == 3
        assert len(result.records) == 5

    def test_info_flag_type(self):
        lines = (SEEDS_DIR / "vcf" / "spec_example.vcf").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_vcf_text(lines)
        # First record has DB and H2 flags
        rec = result.records[0]
        assert rec.INFO.get("DB") is True
        assert rec.INFO.get("H2") is True

    def test_missing_qual(self):
        """QUAL='.' should become None."""
        lines = [
            "##fileformat=VCFv4.5\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tA\tC\t.\t.\t.\n",
        ]
        result = normalize_vcf_text(lines)
        assert result.records[0].QUAL is None

    def test_no_alt(self):
        """ALT='.' should become empty list."""
        lines = [
            "##fileformat=VCFv4.5\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tA\t.\t30\t.\t.\n",
        ]
        result = normalize_vcf_text(lines)
        assert result.records[0].ALT == []

    def test_filter_sorted(self):
        """FILTER values should be sorted."""
        lines = [
            "##fileformat=VCFv4.5\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tA\tC\t30\tq10;low\t.\n",
        ]
        result = normalize_vcf_text(lines)
        assert result.records[0].FILTER == ["low", "q10"]


class TestSamNormalizer:
    def test_parse_minimal_sam(self):
        lines = (SEEDS_DIR / "sam" / "minimal_tags.sam").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_sam_text(lines)
        assert result.format == "SAM"
        assert result.header.HD is not None
        assert result.header.HD.get("VN") == "1.6"
        assert len(result.header.SQ) == 2
        assert len(result.records) == 2

    def test_cigar_parsing(self):
        lines = (SEEDS_DIR / "sam" / "spec_example.sam").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_sam_text(lines)
        # First record: 8M2I4M1D3M
        cigar = result.records[0].CIGAR
        assert cigar is not None
        assert len(cigar) == 5
        assert cigar[0].op == "M" and cigar[0].len == 8
        assert cigar[1].op == "I" and cigar[1].len == 2

    def test_tags_sorted(self):
        lines = (SEEDS_DIR / "sam" / "spec_example.sam").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_sam_text(lines)
        for rec in result.records:
            tag_keys = list(rec.tags.keys())
            assert tag_keys == sorted(tag_keys), f"Tags not sorted: {tag_keys}"

    def test_unmapped_pos_is_none(self):
        """POS=0 in SAM should be None in canonical."""
        lines = [
            "@HD\tVN:1.6\n",
            "@SQ\tSN:ref\tLN:100\n",
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n",
        ]
        result = normalize_sam_text(lines)
        assert result.records[0].POS is None
        assert result.records[0].RNAME is None

    def test_comments_sorted(self):
        lines = [
            "@HD\tVN:1.6\n",
            "@SQ\tSN:ref\tLN:100\n",
            "@CO\tSecond comment\n",
            "@CO\tFirst comment\n",
        ]
        result = normalize_sam_text(lines)
        assert result.header.CO == ["First comment", "Second comment"]

    def test_b_type_tag(self):
        lines = (SEEDS_DIR / "sam" / "spec_example.sam").read_text(encoding="utf-8").splitlines(keepends=True)
        result = normalize_sam_text(lines)
        # r001 has XX:B:S,12561,2,20,112
        r001 = result.records[0]
        assert "XX" in r001.tags
        assert r001.tags["XX"].type == "B"
        assert isinstance(r001.tags["XX"].value, list)


class TestSchemaValidation:
    def test_cigar_op_invalid(self):
        with pytest.raises(Exception):
            CigarOp(op="Z", len=10)

    def test_cigar_op_valid(self):
        op = CigarOp(op="M", len=10)
        assert op.op == "M"
        assert op.len == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
