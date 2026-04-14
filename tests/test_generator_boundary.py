"""
T4-T5: Z3 constraint boundary tests + Hypothesis shrink hook sanity.

Tests that Z3 constraint guards correctly reject invalid states,
and that shrink hooks preserve critical structural invariants.
"""

import pytest

from test_engine.generators.z3_constraints import (
    check_cigar_seq_constraint,
    check_info_number_a,
    check_info_number_r,
    check_flag_type_number,
    generate_extreme_vcf_params,
    generate_extreme_sam_params,
)
from test_engine.generators.shrink import shrink_vcf_lines, shrink_sam_lines


# ===========================================================================
# T4: Z3 constraint boundary tests
# ===========================================================================

class TestZ3CigarConstraint:
    """CIGAR sum(query_consuming) must equal len(SEQ)."""

    def test_valid_cigar_passes(self):
        """10M with SEQ length 10 must satisfy."""
        ops = [(10, "M")]
        assert check_cigar_seq_constraint(ops, 10) is True

    def test_complex_valid_cigar_passes(self):
        """5M2I3M = 10 query-consumed, with 2D non-consuming."""
        ops = [(5, "M"), (2, "I"), (3, "M"), (2, "D")]
        assert check_cigar_seq_constraint(ops, 10) is True

    def test_soft_clip_counted(self):
        """S ops consume query: 2S5M3S = 10."""
        ops = [(2, "S"), (5, "M"), (3, "S")]
        assert check_cigar_seq_constraint(ops, 10) is True

    def test_hard_clip_not_counted(self):
        """H ops do NOT consume query: 3H5M = 5, not 8."""
        ops = [(3, "H"), (5, "M")]
        assert check_cigar_seq_constraint(ops, 5) is True
        assert check_cigar_seq_constraint(ops, 8) is False

    def test_invalid_cigar_mismatch_rejected(self):
        """10M with SEQ length 7 must fail."""
        ops = [(10, "M")]
        assert check_cigar_seq_constraint(ops, 7) is False

    def test_empty_cigar_zero_seq(self):
        """No ops, zero-length SEQ = valid edge case."""
        assert check_cigar_seq_constraint([], 0) is True

    def test_empty_cigar_nonzero_seq_rejected(self):
        """No ops but non-zero SEQ = invalid."""
        assert check_cigar_seq_constraint([], 5) is False

    def test_all_non_consuming_ops(self):
        """Only D and N ops = 0 query consumed, needs SEQ=0."""
        ops = [(5, "D"), (3, "N")]
        assert check_cigar_seq_constraint(ops, 0) is True
        assert check_cigar_seq_constraint(ops, 1) is False

    def test_eq_and_x_ops_counted(self):
        """= and X are query-consuming: 3=2X = 5."""
        ops = [(3, "="), (2, "X")]
        assert check_cigar_seq_constraint(ops, 5) is True


class TestZ3InfoConstraints:
    """Number=A and Number=R field length constraints."""

    def test_number_a_correct_length(self):
        assert check_info_number_a(3, [0.1, 0.2, 0.3]) is True

    def test_number_a_wrong_length(self):
        assert check_info_number_a(3, [0.1, 0.2]) is False

    def test_number_a_zero_alts(self):
        assert check_info_number_a(0, []) is True

    def test_number_r_correct_length(self):
        """Number=R has REF + n ALT values = n+1."""
        assert check_info_number_r(2, [100, 10, 20]) is True

    def test_number_r_wrong_length(self):
        assert check_info_number_r(2, [100, 10]) is False

    def test_flag_type_must_be_zero(self):
        assert check_flag_type_number(0) is True
        assert check_flag_type_number(1) is False
        assert check_flag_type_number(-1) is False


class TestZ3SeedGeneration:
    """Z3-based extreme parameter generation."""

    def test_extreme_vcf_params_solvable(self):
        result = generate_extreme_vcf_params(min_alts=0, max_alts=5)
        assert result is not None
        assert 0 <= result["alt_count"] <= 5
        assert result["pos"] >= 1

    def test_extreme_vcf_unsatisfiable(self):
        """Contradictory constraints: min_alts > max_alts."""
        result = generate_extreme_vcf_params(min_alts=10, max_alts=5)
        assert result is None

    def test_extreme_sam_params_solvable(self):
        result = generate_extreme_sam_params(max_cigar_ops=10, max_tags=20)
        assert result is not None
        assert result["seq_len"] >= 1


# ===========================================================================
# T5: Hypothesis shrink hook invariant tests
# ===========================================================================

class TestVcfShrinkHook:
    """VCF shrink must preserve ##fileformat as absolute first line."""

    BLOATED_VCF = [
        "##fileformat=VCFv4.3\n",
        "##source=TestSuite\n",
        "##reference=file:///dev/null\n",
        "##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Depth\">\n",
        "##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Freq\">\n",
        "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
        "##FORMAT=<ID=GQ,Number=1,Type=Integer,Description=\"GQ\">\n",
        "##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Sample DP\">\n",
        "##contig=<ID=chr1,length=100000>\n",
        "##contig=<ID=chr2,length=200000>\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\tS2\tS3\tS4\tS5\n",
        "chr1\t100\t.\tA\tC\t30\tPASS\tDP=10\tGT:GQ:DP\t0/1:30:5\t0/0:40:8\t0/1:35:6\t0/0:45:10\t1/1:50:12\n",
        "chr1\t200\t.\tG\tT\t25\tPASS\tDP=15\tGT\t0/0\t0/1\t0/0\t0/1\t0/0\n",
        "chr2\t300\t.\tC\tA\t40\tPASS\tDP=20\tGT\t0/1\t0/0\t0/1\t0/0\t0/1\n",
    ]

    def test_fileformat_is_first_line(self):
        shrunk = shrink_vcf_lines(self.BLOATED_VCF)
        assert shrunk[0].startswith("##fileformat=VCFv4.3")

    def test_fileformat_never_removed(self):
        shrunk = shrink_vcf_lines(self.BLOATED_VCF)
        has_ff = any(l.startswith("##fileformat") for l in shrunk)
        assert has_ff, "##fileformat must survive shrinking"

    def test_reduces_meta_lines(self):
        original_meta = sum(1 for l in self.BLOATED_VCF
                           if l.startswith("##") and not l.startswith("##fileformat"))
        shrunk_meta = sum(1 for l in shrink_vcf_lines(self.BLOATED_VCF)
                         if l.startswith("##") and not l.startswith("##fileformat"))
        assert shrunk_meta < original_meta

    def test_reduces_data_records(self):
        original_data = sum(1 for l in self.BLOATED_VCF
                           if not l.startswith("#") and l.strip())
        shrunk_data = sum(1 for l in shrink_vcf_lines(self.BLOATED_VCF)
                         if not l.startswith("#") and l.strip())
        assert shrunk_data <= 1

    def test_keeps_header_line(self):
        shrunk = shrink_vcf_lines(self.BLOATED_VCF)
        has_chrom = any(l.startswith("#CHROM") for l in shrunk)
        assert has_chrom, "#CHROM header must survive"

    def test_keeps_essential_meta_only(self):
        """Only INFO and FORMAT meta lines should survive (not source, reference, contig)."""
        shrunk = shrink_vcf_lines(self.BLOATED_VCF)
        non_ff_meta = [l for l in shrunk
                       if l.startswith("##") and not l.startswith("##fileformat")]
        for m in non_ff_meta:
            assert "##INFO=" in m or "##FORMAT=" in m, f"Non-essential meta survived: {m.strip()}"


class TestSamShrinkHook:
    """SAM shrink must preserve @HD as first line."""

    BLOATED_SAM = [
        "@HD\tVN:1.6\tSO:coordinate\n",
        "@SQ\tSN:chr1\tLN:248956422\n",
        "@SQ\tSN:chr2\tLN:242193529\n",
        "@SQ\tSN:chr3\tLN:198295559\n",
        "@RG\tID:rg1\tSM:sampleA\n",
        "@PG\tID:bwa\tPN:bwa\n",
        "@CO\tThis is a comment\n",
        "r001\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\tNM:i:0\tMD:Z:10\tRG:Z:rg1\tAS:i:60\tXS:i:0\n",
        "r002\t16\tchr2\t200\t30\t5M2I3M\t*\t0\t0\tACGTAACCGT\tIIIIIIIIII\tNM:i:2\tMD:Z:5^AC3\tRG:Z:rg1\tXS:i:25\tXA:Z:alt\n",
        "r003\t0\tchr3\t300\t40\t8M\t*\t0\t0\tACGTACGT\tIIIIIIII\tNM:i:1\n",
    ]

    def test_hd_is_first_line(self):
        shrunk = shrink_sam_lines(self.BLOATED_SAM)
        assert shrunk[0].startswith("@HD")

    def test_hd_never_removed(self):
        shrunk = shrink_sam_lines(self.BLOATED_SAM)
        has_hd = any(l.startswith("@HD") for l in shrunk)
        assert has_hd, "@HD must survive shrinking"

    def test_reduces_sq_lines(self):
        original_sq = sum(1 for l in self.BLOATED_SAM if l.startswith("@SQ"))
        shrunk_sq = sum(1 for l in shrink_sam_lines(self.BLOATED_SAM) if l.startswith("@SQ"))
        assert shrunk_sq <= 1

    def test_drops_rg_pg_co(self):
        shrunk = shrink_sam_lines(self.BLOATED_SAM)
        for line in shrunk:
            assert not line.startswith("@RG"), "@RG should be dropped"
            assert not line.startswith("@PG"), "@PG should be dropped"
            assert not line.startswith("@CO"), "@CO should be dropped"

    def test_reduces_alignment_records(self):
        original_aligns = sum(1 for l in self.BLOATED_SAM
                             if not l.startswith("@") and l.strip())
        shrunk_aligns = sum(1 for l in shrink_sam_lines(self.BLOATED_SAM)
                           if not l.startswith("@") and l.strip())
        assert shrunk_aligns <= 1

    def test_trims_optional_tags(self):
        """Alignment records should keep at most 2 optional tags (cols 12-13)."""
        shrunk = shrink_sam_lines(self.BLOATED_SAM)
        for line in shrunk:
            if not line.startswith("@") and "\t" in line:
                cols = line.rstrip("\n").split("\t")
                optional_tags = cols[11:]  # cols 12+ are optional
                assert len(optional_tags) <= 2, f"Too many tags survived: {optional_tags}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
