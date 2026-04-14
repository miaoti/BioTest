"""
Tests for B2: Atomic Transforms Library.

Tests each transform for:
  (a) Deterministic output with same seed
  (b) Structural validity of output
  (c) Domain invariants (e.g. SEQ length for CIGAR ops)
"""

import pytest

from mr_engine.transforms import get_whitelist, TRANSFORM_REGISTRY
from mr_engine.transforms.vcf import (
    choose_permutation,
    inject_equivalent_missing_values,
    permute_alt,
    permute_number_a_r_fields,
    permute_sample_columns,
    permute_structured_kv_order,
    remap_gt,
    shuffle_info_field_kv,
    shuffle_meta_lines,
)
from mr_engine.transforms.sam import (
    permute_optional_tag_fields,
    reorder_header_records,
    split_or_merge_adjacent_cigar_ops,
    toggle_cigar_hard_soft_clipping,
)


# ===========================================================================
# Registry tests
# ===========================================================================

class TestRegistry:
    def test_whitelist_has_13_transforms(self):
        wl = get_whitelist()
        assert len(wl) == 13

    def test_all_transforms_are_callable(self):
        for name, fn in TRANSFORM_REGISTRY.items():
            assert callable(fn), f"{name} is not callable"


# ===========================================================================
# VCF transforms
# ===========================================================================

class TestChoosePermutation:
    def test_deterministic(self):
        assert choose_permutation(5, seed=42) == choose_permutation(5, seed=42)

    def test_length(self):
        pi = choose_permutation(4, seed=1)
        assert len(pi) == 4
        assert sorted(pi) == [0, 1, 2, 3]

    def test_zero_length(self):
        assert choose_permutation(0) == []


class TestShuffleMetaLines:
    LINES = [
        "##fileformat=VCFv4.5\n",
        "##INFO=<ID=DP>\n",
        "##FORMAT=<ID=GT>\n",
        "##contig=<ID=chr1>\n",
        "#CHROM\tPOS\tID\n",
        "chr1\t100\t.\n",
    ]

    def test_deterministic(self):
        r1 = shuffle_meta_lines(self.LINES, seed=42)
        r2 = shuffle_meta_lines(self.LINES, seed=42)
        assert r1 == r2

    def test_fileformat_stays_first(self):
        result = shuffle_meta_lines(self.LINES, seed=99)
        assert result[0].startswith("##fileformat=VCFv4.5")

    def test_non_meta_lines_unchanged(self):
        result = shuffle_meta_lines(self.LINES, seed=99)
        assert result[-2] == "#CHROM\tPOS\tID\n"
        assert result[-1] == "chr1\t100\t.\n"

    def test_same_set_of_meta_lines(self):
        result = shuffle_meta_lines(self.LINES, seed=7)
        meta_orig = set(l for l in self.LINES if l.startswith("##"))
        meta_result = set(l for l in result if l.startswith("##"))
        assert meta_orig == meta_result


class TestPermuteStructuredKV:
    def test_deterministic(self):
        line = "##INFO=<ID=DP,Number=1,Type=Integer>"
        r1 = permute_structured_kv_order(line, seed=42)
        r2 = permute_structured_kv_order(line, seed=42)
        assert r1 == r2

    def test_preserves_all_kvs(self):
        line = '##INFO=<ID=DP,Number=1,Type=Integer,Description="Read depth">'
        result = permute_structured_kv_order(line, seed=1)
        # All original k=v pairs should still be present
        assert "ID=DP" in result
        assert "Number=1" in result
        assert "Type=Integer" in result
        assert 'Description="Read depth"' in result

    def test_non_structured_line_unchanged(self):
        line = "##reference=file:///ref.fa"
        assert permute_structured_kv_order(line) == line


class TestPermuteAlt:
    def test_basic(self):
        assert permute_alt("A,C,T", [2, 0, 1]) == "T,A,C"

    def test_single_alt(self):
        assert permute_alt("G", [0]) == "G"

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError):
            permute_alt("A,C", [0, 1, 2])


class TestRemapGT:
    def test_ref_stays_zero(self):
        """REF (index 0) must never change regardless of permutation."""
        assert remap_gt("0/0", [1, 0]).startswith("0")

    def test_basic_remap(self):
        # pi=[1,0]: ALT0->pos1, ALT1->pos0
        # old 1 (ALT0) -> pi.index(0)+1 = 1+1 = 2
        # old 2 (ALT1) -> pi.index(1)+1 = 0+1 = 1
        assert remap_gt("0/1", [1, 0]) == "0/2"
        assert remap_gt("0/2", [1, 0]) == "0/1"

    def test_missing_values(self):
        assert remap_gt("./.", [1, 0]) == "./."

    def test_phased_separator_preserved(self):
        result = remap_gt("0|1", [1, 0])
        assert "|" in result


class TestPermuteNumberAR:
    def test_number_a(self):
        assert permute_number_a_r_fields("10,20,30", [2, 0, 1]) == "30,10,20"

    def test_number_r_ref_stays(self):
        # Number=R: first value is REF, rest are ALT
        result = permute_number_a_r_fields("100,10,20,30", [2, 0, 1], is_number_r=True)
        assert result.startswith("100,")  # REF value preserved
        assert result == "100,30,10,20"


class TestPermuteSampleColumns:
    LINES = [
        "##fileformat=VCFv4.5\n",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSA\tSB\tSC\n",
        "chr1\t100\t.\tA\tT\t30\tPASS\tDP=10\tGT\t0/1\t0/0\t1/1\n",
    ]

    def test_deterministic(self):
        r1 = permute_sample_columns(self.LINES, seed=42)
        r2 = permute_sample_columns(self.LINES, seed=42)
        assert r1 == r2

    def test_fixed_columns_unchanged(self):
        result = permute_sample_columns(self.LINES, seed=42)
        # Header and data fixed cols should be unchanged
        for line in result:
            if line.startswith("#CHROM") or not line.startswith("#"):
                fields = line.strip().split("\t")
                if len(fields) > 9:
                    assert fields[:9] == self.LINES[-1].strip().split("\t")[:9] or \
                           fields[0] == "#CHROM"

    def test_same_set_of_samples(self):
        result = permute_sample_columns(self.LINES, seed=42)
        orig_header = self.LINES[1].strip().split("\t")[9:]
        new_header = result[1].strip().split("\t")[9:]
        assert sorted(orig_header) == sorted(new_header)


class TestShuffleInfoKV:
    def test_deterministic(self):
        info = "DP=10;AF=0.5;MQ=30"
        assert shuffle_info_field_kv(info, seed=42) == shuffle_info_field_kv(info, seed=42)

    def test_missing_value_unchanged(self):
        assert shuffle_info_field_kv(".") == "."

    def test_same_kvs(self):
        info = "DP=10;AF=0.5;MQ=30"
        result = shuffle_info_field_kv(info, seed=1)
        assert sorted(result.split(";")) == sorted(info.split(";"))


class TestInjectMissingValues:
    def test_adds_field(self):
        fmt, samples = inject_equivalent_missing_values(
            "GT:DP", ["0/1:30", "0/0:25"], "GQ"
        )
        assert fmt == "GT:DP:GQ"
        assert samples == ["0/1:30:.", "0/0:25:."]


# ===========================================================================
# SAM transforms
# ===========================================================================

class TestPermuteOptionalTags:
    def test_deterministic(self):
        line = "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\tNM:i:0\tMD:Z:10\tXS:A:+"
        r1 = permute_optional_tag_fields(line, seed=42)
        r2 = permute_optional_tag_fields(line, seed=42)
        assert r1 == r2

    def test_mandatory_fields_unchanged(self):
        line = "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\tNM:i:0\tMD:Z:10"
        result = permute_optional_tag_fields(line, seed=42)
        orig_mandatory = line.split("\t")[:11]
        result_mandatory = result.split("\t")[:11]
        assert orig_mandatory == result_mandatory

    def test_no_optional_tags(self):
        line = "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert permute_optional_tag_fields(line, seed=42) == line


class TestCIGAROps:
    def test_split_deterministic(self):
        r1 = split_or_merge_adjacent_cigar_ops("10M5I3M", mode="split", seed=42)
        r2 = split_or_merge_adjacent_cigar_ops("10M5I3M", mode="split", seed=42)
        assert r1 == r2

    def test_merge_basic(self):
        assert split_or_merge_adjacent_cigar_ops("4M6M5I", mode="merge") == "10M5I"

    def test_split_preserves_query_length(self):
        cigar = "10M5I3M"
        result = split_or_merge_adjacent_cigar_ops(cigar, mode="split", seed=42)
        # Total M+I+S bases must be the same
        import re
        def query_len(c):
            return sum(int(m.group(1)) for m in re.finditer(r"(\d+)[MIS=X]", c))
        assert query_len(result) == query_len(cigar)

    def test_merge_then_split_preserves_semantics(self):
        """Merge then split should preserve total query consumption."""
        import re
        cigar = "3M2M5I1M2M"
        merged = split_or_merge_adjacent_cigar_ops(cigar, mode="merge")
        assert merged == "5M5I3M"
        def query_len(c):
            return sum(int(m.group(1)) for m in re.finditer(r"(\d+)[MIS=X]", c))
        assert query_len(merged) == query_len(cigar)

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError):
            split_or_merge_adjacent_cigar_ops("10M", mode="invalid")


class TestReorderHeaderRecords:
    HEADER = [
        "@HD\tVN:1.6\tSO:coordinate",
        "@SQ\tSN:chr1\tLN:248956422",
        "@SQ\tSN:chr2\tLN:242193529",
        "@RG\tID:sample1",
        "@SQ\tSN:chr3\tLN:198295559",
    ]

    def test_hd_stays_first(self):
        result = reorder_header_records(self.HEADER, "@SQ", seed=42)
        assert result[0].startswith("@HD")

    def test_deterministic(self):
        r1 = reorder_header_records(self.HEADER, "@SQ", seed=42)
        r2 = reorder_header_records(self.HEADER, "@SQ", seed=42)
        assert r1 == r2

    def test_same_set_of_sq_lines(self):
        result = reorder_header_records(self.HEADER, "@SQ", seed=42)
        orig_sq = sorted(l for l in self.HEADER if l.startswith("@SQ"))
        result_sq = sorted(l for l in result if l.startswith("@SQ"))
        assert orig_sq == result_sq


class TestToggleClipping:
    def test_h_to_s(self):
        cigar, seq, qual = toggle_cigar_hard_soft_clipping(
            "5H10M3H", "ACGTACGTAC", "IIIIIIIIII"
        )
        assert cigar == "5S10M3S"
        assert len(seq) == 18  # 5 + 10 + 3
        assert len(qual) == 18

    def test_s_to_h(self):
        cigar, seq, qual = toggle_cigar_hard_soft_clipping(
            "3S10M2S", "NNNACGTACGTACNN", "!!!IIIIIIIIII!!"
        )
        assert cigar == "3H10M2H"
        assert len(seq) == 10
        assert len(qual) == 10

    def test_no_clipping_unchanged(self):
        cigar, seq, qual = toggle_cigar_hard_soft_clipping("10M", "ACGTACGTAC", "IIIIIIIIII")
        assert cigar == "10M"
        assert seq == "ACGTACGTAC"


# ===========================================================================
# Run
# ===========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
