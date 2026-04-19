"""
Tests for the `strict_mode` flag added to vcf_normalizer and sam_normalizer
(Rank 3 lever). Non-strict must preserve backward-compatible behavior;
strict must raise on specific spec violations the malformed-input mutators
produce.
"""

from __future__ import annotations

import pytest

from test_engine.canonical.vcf_normalizer import normalize_vcf_text
from test_engine.canonical.sam_normalizer import normalize_sam_text


# ---------------------------------------------------------------------------
# Valid seeds — must parse in BOTH modes.
# ---------------------------------------------------------------------------


VALID_VCF = [
    "##fileformat=VCFv4.3\n",
    "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele count\">\n",
    "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
    "##contig=<ID=chr1,length=248956422>\n",
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE1\n",
    "chr1\t100\t.\tA\tT\t30\tPASS\tAC=1\tGT\t0/1\n",
]

VALID_SAM = [
    "@HD\tVN:1.6\tSO:unsorted\n",
    "@SQ\tSN:chr1\tLN:248956422\n",
    "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
]


class TestBackwardsCompat:
    def test_valid_vcf_parses_in_both_modes(self):
        normalize_vcf_text(VALID_VCF)
        normalize_vcf_text(VALID_VCF, strict_mode=False)
        normalize_vcf_text(VALID_VCF, strict_mode=True)

    def test_valid_sam_parses_in_both_modes(self):
        normalize_sam_text(VALID_SAM)
        normalize_sam_text(VALID_SAM, strict_mode=False)
        normalize_sam_text(VALID_SAM, strict_mode=True)


# ---------------------------------------------------------------------------
# Strict-mode violations.
# ---------------------------------------------------------------------------


class TestStrictVcf:
    def test_fileformat_not_first_line(self):
        bad = [
            "##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Depth\">\n",
            "##fileformat=VCFv4.3\n",
            "##contig=<ID=chr1,length=1000>\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t1\t.\tA\tC\t10\tPASS\tDP=5\n",
        ]
        # Non-strict accepts.
        normalize_vcf_text(bad, strict_mode=False)
        # Strict raises.
        with pytest.raises(ValueError, match="first non-blank line"):
            normalize_vcf_text(bad, strict_mode=True)

    def test_number_a_cardinality_mismatch(self):
        bad = [
            "##fileformat=VCFv4.3\n",
            "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"AC\">\n",
            "##contig=<ID=chr1,length=1000>\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t1\t.\tA\tC\t10\tPASS\tAC=1,2\n",  # 1 ALT, 2 values
        ]
        normalize_vcf_text(bad, strict_mode=False)
        with pytest.raises(ValueError, match="Number=A"):
            normalize_vcf_text(bad, strict_mode=True)

    def test_gt_index_out_of_bounds(self):
        bad = [
            "##fileformat=VCFv4.3\n",
            "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
            "##contig=<ID=chr1,length=1000>\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n",
            "chr1\t1\t.\tA\tC\t10\tPASS\t.\tGT\t2/0\n",  # idx 2 doesn't exist
        ]
        normalize_vcf_text(bad, strict_mode=False)
        with pytest.raises(ValueError, match="GT index"):
            normalize_vcf_text(bad, strict_mode=True)

    def test_valid_gt_multi_allelic(self):
        """GT=2/0 IS valid when there are 2 ALTs."""
        ok = [
            "##fileformat=VCFv4.3\n",
            "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
            "##contig=<ID=chr1,length=1000>\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n",
            "chr1\t1\t.\tA\tC,G\t10\tPASS\t.\tGT\t2/0\n",
        ]
        # Must NOT raise — idx 2 references the 2nd ALT (G).
        normalize_vcf_text(ok, strict_mode=True)


class TestStrictSam:
    def test_cigar_seq_length_mismatch(self):
        bad = [
            "@HD\tVN:1.6\n",
            "@SQ\tSN:chr1\tLN:1000\n",
            "r1\t0\tchr1\t1\t60\t10M5M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
            # CIGAR sums to 15 query bases, SEQ is 10.
        ]
        normalize_sam_text(bad, strict_mode=False)
        with pytest.raises(ValueError, match="CIGAR"):
            normalize_sam_text(bad, strict_mode=True)

    def test_unmapped_seq_star_does_not_trigger(self):
        """SEQ='*' means sequence not stored; CIGAR/SEQ length rule doesn't apply."""
        ok = [
            "@HD\tVN:1.6\n",
            "@SQ\tSN:chr1\tLN:1000\n",
            "r1\t4\tchr1\t1\t0\t*\t*\t0\t0\t*\t*\n",
        ]
        normalize_sam_text(ok, strict_mode=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
