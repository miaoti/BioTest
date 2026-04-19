"""
Tests for Rank 3 malformed-input transforms. Each mutator should:
  - apply only when its structural precondition holds,
  - produce a seed that carries the exact spec violation,
  - be detected by `strict_mode=True` normalization (round-trip check).
"""

from __future__ import annotations

import pytest

from mr_engine.transforms.malformed import (
    violate_info_number_a_cardinality,
    violate_required_fixed_columns,
    violate_fileformat_first_line,
    violate_gt_index_bounds,
    violate_cigar_seq_length,
    MALFORMED_TRANSFORM_NAMES,
)

from test_engine.canonical.vcf_normalizer import normalize_vcf_text
from test_engine.canonical.sam_normalizer import normalize_sam_text


# ---------------------------------------------------------------------------
# Test fixtures — tiny valid seeds each mutator can operate on.
# ---------------------------------------------------------------------------


def _vcf_with_number_a() -> list[str]:
    return [
        "##fileformat=VCFv4.3\n",
        "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele count\">\n",
        "##contig=<ID=chr1,length=248956422>\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
        "chr1\t100\t.\tA\tT\t30\tPASS\tAC=1\n",
    ]


def _vcf_with_gt() -> list[str]:
    return [
        "##fileformat=VCFv4.3\n",
        "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
        "##contig=<ID=chr1,length=248956422>\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE1\n",
        "chr1\t100\t.\tA\tT\t30\tPASS\t.\tGT\t0/1\n",
    ]


def _sam_with_cigar() -> list[str]:
    return [
        "@HD\tVN:1.6\tSO:unsorted\n",
        "@SQ\tSN:chr1\tLN:248956422\n",
        "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
    ]


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_closed_set_matches_transform_registry(self):
        from mr_engine.transforms import TRANSFORM_REGISTRY
        for name in MALFORMED_TRANSFORM_NAMES:
            assert name in TRANSFORM_REGISTRY, (
                f"{name} listed in MALFORMED_TRANSFORM_NAMES but not in registry"
            )
        # No stale entries.
        assert len(MALFORMED_TRANSFORM_NAMES) == 5


# ---------------------------------------------------------------------------
# VCF mutators
# ---------------------------------------------------------------------------


class TestInfoNumberACardinality:
    def test_appends_extra_value(self):
        out = violate_info_number_a_cardinality(_vcf_with_number_a(), seed=0)
        text = "".join(out)
        # biallelic → len(ALT)=1 → Number=A expects 1 value; we appended
        # one, so AC now has 2 comma-values on a 1-ALT record.
        assert "AC=1," in text

    def test_strict_mode_catches_mutation(self):
        mutated = violate_info_number_a_cardinality(_vcf_with_number_a(), seed=0)
        with pytest.raises(ValueError, match="Number=A"):
            normalize_vcf_text(mutated, strict_mode=True)
        # Non-strict mode silently accepts.
        normalize_vcf_text(mutated, strict_mode=False)

    def test_no_op_when_no_number_a_field(self):
        # No Number=A field in header → transform leaves input unchanged.
        plain = [
            "##fileformat=VCFv4.3\n",
            "##contig=<ID=chr1,length=100>\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t50\t.\tA\tT\t30\tPASS\tDP=5\n",
        ]
        assert violate_info_number_a_cardinality(plain, seed=0) == plain


class TestRequiredFixedColumns:
    def test_drops_qual_column(self):
        out = violate_required_fixed_columns(_vcf_with_number_a(), seed=0)
        # Find the data line; it should have one fewer column.
        data_line = next(l for l in out if not l.startswith("#") and "\t" in l)
        cols = data_line.rstrip("\n").split("\t")
        # Original had 8 columns (CHROM…INFO). Mutator drops QUAL → 7.
        assert len(cols) == 7


class TestFileformatFirstLine:
    def test_swaps_fileformat_with_next_meta(self):
        seed = _vcf_with_number_a()
        out = violate_fileformat_first_line(seed, seed=0)
        # First non-blank should no longer be ##fileformat=
        first = next(l for l in out if l.strip())
        assert not first.startswith("##fileformat="), first

    def test_strict_mode_catches_mutation(self):
        mutated = violate_fileformat_first_line(_vcf_with_number_a(), seed=0)
        with pytest.raises(ValueError, match="first non-blank line"):
            normalize_vcf_text(mutated, strict_mode=True)
        # Non-strict still parses fine.
        normalize_vcf_text(mutated, strict_mode=False)


class TestGtIndexBounds:
    def test_sets_out_of_range_gt(self):
        out = violate_gt_index_bounds(_vcf_with_gt(), seed=0)
        data = next(l for l in out if not l.startswith("#") and "\t" in l)
        cols = data.rstrip("\n").split("\t")
        # Sample column is last, GT is the only FORMAT field here.
        assert cols[9].startswith("2")  # out-of-range (only idx 0,1 valid)

    def test_strict_mode_catches_mutation(self):
        mutated = violate_gt_index_bounds(_vcf_with_gt(), seed=0)
        with pytest.raises(ValueError, match="GT index"):
            normalize_vcf_text(mutated, strict_mode=True)
        normalize_vcf_text(mutated, strict_mode=False)


# ---------------------------------------------------------------------------
# SAM mutator
# ---------------------------------------------------------------------------


class TestCigarSeqLength:
    def test_appends_5M_to_cigar(self):
        out = violate_cigar_seq_length(_sam_with_cigar(), seed=0)
        data = next(l for l in out if not l.startswith("@") and "\t" in l)
        cols = data.rstrip("\n").split("\t")
        # Original CIGAR was 10M, SEQ is 10 bases. After mutation CIGAR is
        # 10M5M, SEQ still 10 bases — sum no longer equals len(SEQ).
        assert cols[5] == "10M5M"
        assert len(cols[9]) == 10

    def test_strict_mode_catches_mutation(self):
        mutated = violate_cigar_seq_length(_sam_with_cigar(), seed=0)
        with pytest.raises(ValueError, match="CIGAR"):
            normalize_sam_text(mutated, strict_mode=True)
        # Non-strict accepts quietly — that's the bug the oracle catches.
        normalize_sam_text(mutated, strict_mode=False)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
