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
    trim_common_affixes,
    left_align_indel,
    split_multi_allelic,
    permute_csq_annotations,
)
from mr_engine.transforms.sam import (
    permute_optional_tag_fields,
    reorder_header_records,
    split_or_merge_adjacent_cigar_ops,
    toggle_cigar_hard_soft_clipping,
    shuffle_hd_subtags,
    shuffle_sq_record_subtags,
    shuffle_rg_record_subtags,
    shuffle_pg_record_subtags,
    shuffle_co_comments,
    normalize_unmapped_record_fields,
    strip_mate_flags_if_unpaired,
    normalize_seq_case,
    cigar_zero_length_op_removal,
    canonicalize_cigar_match_operators,
    pos_shift_with_sq_ln_bound_check,
    canonicalize_rnext_equals_alias,
    bump_hd_vn_minor,
    _query_consumed,
    _parse_cigar,
)
from mr_engine.transforms.malformed import (
    violate_tlen_sign_consistency,
    violate_optional_tag_type_character,
    violate_flag_bit_exclusivity,
)


# ===========================================================================
# Registry tests
# ===========================================================================

class TestRegistry:
    def test_whitelist_has_44_transforms(self):
        # 13 originals + 6 (Tan 2015 normalization / BCF round-trip /
        # CSQ permute) + 1 SUT-agnostic writer (sut_write_roundtrip) +
        # 5 Rank-3 spec-rule-targeted malformed-input mutators +
        # 1 Rank-5 query-method MR transform (query_method_roundtrip;
        # MR-Scout TOSEM 2024) +
        # 5 Phase-2 SAM header-subtag / @CO shuffles +
        # 3 Phase-2 SAM malformed mutators (TLEN / tag-type / FLAG) +
        # 2 Phase-3 SAM round-trip MRs (SAM↔BAM, SAM↔CRAM) +
        # 5 Phase-4 SAM record-level transforms (normalize unmapped /
        # strip mate flags / normalize SEQ case / cigar zero-length op
        # removal / canonicalize CIGAR M -> =/X) +
        # 3 Round-2 SAM transforms (pos_shift_with_sq_ln_bound_check /
        # canonicalize_rnext_equals_alias / bump_hd_vn_minor).
        wl = get_whitelist()
        assert len(wl) == 44, f"Expected 44 transforms, got {len(wl)}: {wl}"

    def test_sut_write_roundtrip_is_registered_and_format_agnostic(self):
        # One writer transform forever, spanning BOTH formats — the
        # orchestrator resolves the actual SUT at Phase C time from
        # primary_target, and the runner dispatches to VCF or SAM based
        # on format_context. Guards against accidental reintroduction
        # of per-SUT or per-format writer variants.
        assert "sut_write_roundtrip" in TRANSFORM_REGISTRY
        meta = TRANSFORM_REGISTRY["sut_write_roundtrip"]
        assert meta.format == "VCF/SAM"
        assert "primary_sut_has_writer" in meta.preconditions
        # Reject any stale per-SUT / per-format writer names.
        for stale in (
            "htsjdk_write_roundtrip",
            "pysam_vcf_write_roundtrip",
            "sut_write_roundtrip_vcf",
            "sut_write_roundtrip_sam",
        ):
            assert stale not in TRANSFORM_REGISTRY, (
                f"{stale} should have been collapsed into sut_write_roundtrip"
            )

    def test_all_transforms_are_callable(self):
        for name, meta in TRANSFORM_REGISTRY.items():
            assert callable(meta.fn), f"{name} is not callable"
            assert meta.format in ("VCF", "SAM", "VCF/SAM"), f"{name} has unknown format: {meta.format}"
            assert meta.description, f"{name} has no description"


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
# Phase-4 SAM record-level transforms — Picard validation rule MRs
# ===========================================================================


class TestNormalizeUnmappedRecordFields:
    def test_deterministic(self):
        line = "r1\t4\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert normalize_unmapped_record_fields(line) == normalize_unmapped_record_fields(line)

    def test_unmapped_with_high_mapq_normalizes_to_255(self):
        line = "r1\t4\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        out = normalize_unmapped_record_fields(line)
        assert out.split("\t")[4] == "255"

    def test_unmapped_with_zero_mapq_unchanged(self):
        line = "r1\t4\tchr1\t100\t0\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert normalize_unmapped_record_fields(line) == line

    def test_unmapped_with_255_unchanged(self):
        line = "r1\t4\tchr1\t100\t255\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert normalize_unmapped_record_fields(line) == line

    def test_mapped_unchanged(self):
        line = "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert normalize_unmapped_record_fields(line) == line

    def test_unmapped_keeps_other_fields(self):
        line = "r1\t4\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        out = normalize_unmapped_record_fields(line)
        orig_cols = line.split("\t")
        new_cols = out.split("\t")
        # Only MAPQ (col 4) changed; all others byte-identical.
        for i, (o, n) in enumerate(zip(orig_cols, new_cols)):
            if i == 4:
                continue
            assert o == n, f"col {i} changed: {o!r} -> {n!r}"

    def test_unparseable_flag_unchanged(self):
        line = "r1\tNOTANUMBER\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert normalize_unmapped_record_fields(line) == line

    def test_unparseable_mapq_unchanged(self):
        line = "r1\t4\tchr1\t100\tBADMAPQ\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
        assert normalize_unmapped_record_fields(line) == line

    def test_too_few_columns_unchanged(self):
        line = "r1\t4\tchr1\t100\t60"
        assert normalize_unmapped_record_fields(line) == line

    def test_header_line_unchanged(self):
        line = "@SQ\tSN:chr1\tLN:248956422"
        assert normalize_unmapped_record_fields(line) == line

    def test_trailing_newline_preserved(self):
        line = "r1\t4\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        out = normalize_unmapped_record_fields(line)
        assert out.endswith("\n")
        assert out.split("\t")[4] == "255"


class TestStripMateFlagsIfUnpaired:
    BASE = "r1\t{flag}\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"

    def _flag_of(self, line):
        return int(line.split("\t")[1])

    def test_deterministic(self):
        line = self.BASE.format(flag=0x40)
        assert strip_mate_flags_if_unpaired(line) == strip_mate_flags_if_unpaired(line)

    def test_unpaired_with_first_of_pair_clears(self):
        line = self.BASE.format(flag=0x40)  # FIRST_OF_PAIR but not paired
        out = strip_mate_flags_if_unpaired(line)
        assert self._flag_of(out) == 0

    def test_unpaired_with_proper_pair_clears(self):
        line = self.BASE.format(flag=0x2)  # PROPER_PAIR but not paired
        out = strip_mate_flags_if_unpaired(line)
        assert self._flag_of(out) == 0

    def test_paired_unchanged(self):
        line = self.BASE.format(flag=0x1 | 0x40)  # 0x41 — paired + first
        assert strip_mate_flags_if_unpaired(line) == line

    def test_unpaired_keeps_unmapped_bit(self):
        line = self.BASE.format(flag=0x4 | 0x40)  # 0x44 — unmapped + first
        out = strip_mate_flags_if_unpaired(line)
        assert self._flag_of(out) == 0x4

    def test_unpaired_keeps_secondary_bit(self):
        line = self.BASE.format(flag=0x100 | 0x40)
        out = strip_mate_flags_if_unpaired(line)
        assert self._flag_of(out) == 0x100

    def test_unpaired_no_mate_bits_unchanged(self):
        line = self.BASE.format(flag=0x100)  # secondary, no mate bits
        assert strip_mate_flags_if_unpaired(line) == line

    def test_unparseable_flag_unchanged(self):
        line = self.BASE.format(flag="NOTANUMBER")
        assert strip_mate_flags_if_unpaired(line) == line

    def test_too_few_columns_unchanged(self):
        line = "r1\t64\tchr1\t100"
        assert strip_mate_flags_if_unpaired(line) == line

    def test_header_line_unchanged(self):
        line = "@HD\tVN:1.6"
        assert strip_mate_flags_if_unpaired(line) == line


class TestNormalizeSeqCase:
    def _make(self, seq):
        return f"r1\t0\tchr1\t100\t30\t{len(seq)}M\t*\t0\t0\t{seq}\t" + "I" * len(seq)

    def test_deterministic(self):
        line = self._make("acgt")
        assert normalize_seq_case(line) == normalize_seq_case(line)

    def test_lowercase_to_upper(self):
        line = self._make("acgt")
        out = normalize_seq_case(line)
        assert out.split("\t")[9] == "ACGT"

    def test_mixed_case(self):
        line = self._make("aCgT")
        out = normalize_seq_case(line)
        assert out.split("\t")[9] == "ACGT"

    def test_already_upper_unchanged(self):
        line = self._make("ACGT")
        assert normalize_seq_case(line) == line

    def test_missing_seq_unchanged(self):
        line = "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\t*\t*"
        assert normalize_seq_case(line) == line

    def test_iupac_codes_uppercased(self):
        line = self._make("rynwkm")
        out = normalize_seq_case(line)
        assert out.split("\t")[9] == "RYNWKM"

    def test_too_few_columns_unchanged(self):
        line = "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0"
        assert normalize_seq_case(line) == line

    def test_header_line_unchanged(self):
        line = "@SQ\tSN:chr1\tLN:1000"
        assert normalize_seq_case(line) == line

    def test_trailing_newline_preserved(self):
        line = self._make("acgt") + "\n"
        out = normalize_seq_case(line)
        assert out.endswith("\n")
        assert out.split("\t")[9] == "ACGT"


class TestCigarZeroLengthOpRemoval:
    def test_zero_in_middle(self):
        assert cigar_zero_length_op_removal("5M0D5M") == "10M"

    def test_zero_at_start(self):
        assert cigar_zero_length_op_removal("0H10M") == "10M"

    def test_zero_at_end(self):
        assert cigar_zero_length_op_removal("10M0S") == "10M"

    def test_no_zeros_no_merge(self):
        assert cigar_zero_length_op_removal("5M5I") == "5M5I"

    def test_multiple_zeros_with_merge(self):
        # 0M (drop) | 3M | 0D (drop) | 2I | 0I (drop) | 3M -> 3M2I3M
        assert cigar_zero_length_op_removal("0M3M0D2I0I3M") == "3M2I3M"

    def test_star_unchanged(self):
        assert cigar_zero_length_op_removal("*") == "*"

    def test_empty_unchanged(self):
        assert cigar_zero_length_op_removal("") == ""

    def test_query_consumed_preserved(self):
        for cigar in [
            "5M0D5M",
            "0H10M",
            "10M0S",
            "0M3M0D2I0I3M",
            "5M5I",
            "0H10M5I0M3S0H",
        ]:
            before = _query_consumed(_parse_cigar(cigar))
            after = _query_consumed(_parse_cigar(cigar_zero_length_op_removal(cigar)))
            assert before == after, f"query-consumed changed for {cigar!r}"

    def test_all_zero_collapses(self):
        # All-zero CIGAR collapses to empty (degenerate but safe).
        assert cigar_zero_length_op_removal("0M0D") == ""

    def test_adjacent_same_after_zero_drop_merges(self):
        # Confirm the merge step runs after dropping zeros.
        assert cigar_zero_length_op_removal("3M0D2M") == "5M"


class TestCanonicalizeCigarMatchOperators:
    def _line(self, cigar, seq, *tags):
        qual = "I" * len(seq)
        cols = ["r1", "0", "chr1", "100", "30", cigar, "*", "0", "0", seq, qual]
        cols.extend(tags)
        return "\t".join(cols)

    def _cigar_of(self, line):
        return line.split("\t")[5]

    def _tag_value(self, line, prefix):
        for f in line.split("\t")[11:]:
            if f.startswith(prefix):
                return f
        return None

    def test_deterministic(self):
        line = self._line("5M", "ACGTA", "MD:Z:5")
        assert canonicalize_cigar_match_operators(line) == canonicalize_cigar_match_operators(line)

    def test_all_matches(self):
        line = self._line("5M", "ACGTA", "MD:Z:5")
        out = canonicalize_cigar_match_operators(line)
        assert self._cigar_of(out) == "5="

    def test_simple_mismatch(self):
        # MD:Z:2A2 -> 2 matches, 1 mismatch, 2 matches over a 5M run
        line = self._line("5M", "ACGTA", "MD:Z:2A2")
        out = canonicalize_cigar_match_operators(line)
        assert self._cigar_of(out) == "2=1X2="

    def test_two_mismatches(self):
        # 1+1+2+1+1 = 6 ref positions, so the M op must be 6M (not 5M).
        line = self._line("6M", "ACGTAC", "MD:Z:1A2T1")
        out = canonicalize_cigar_match_operators(line)
        assert self._cigar_of(out) == "1=1X2=1X1="

    def test_with_deletion(self):
        # 3M2D2M with MD:Z:3^AG2 -> 3=2D2=
        line = self._line("3M2D2M", "ACGAC", "MD:Z:3^AG2")
        out = canonicalize_cigar_match_operators(line)
        assert self._cigar_of(out) == "3=2D2="

    def test_no_md_tag_unchanged(self):
        line = self._line("5M", "ACGTA")
        assert canonicalize_cigar_match_operators(line) == line

    def test_no_m_ops_unchanged(self):
        line = self._line("5=", "ACGTA", "MD:Z:5")
        assert canonicalize_cigar_match_operators(line) == line

    def test_no_m_ops_with_mismatch_unchanged(self):
        line = self._line("5=2X", "ACGTACGTA", "MD:Z:5C1")
        assert canonicalize_cigar_match_operators(line) == line

    def test_malformed_md_unchanged(self):
        line = self._line("5M", "ACGTA", "MD:Z:bogus!@#")
        assert canonicalize_cigar_match_operators(line) == line

    def test_md_coverage_mismatch_unchanged(self):
        # MD says 10 matches, CIGAR only covers 5
        line = self._line("5M", "ACGTA", "MD:Z:10")
        assert canonicalize_cigar_match_operators(line) == line

    def test_star_cigar_unchanged(self):
        line = "r1\t0\tchr1\t100\t30\t*\t*\t0\t0\t*\t*\tMD:Z:5"
        assert canonicalize_cigar_match_operators(line) == line

    def test_too_few_columns_unchanged(self):
        line = "r1\t0\tchr1\t100\t30\t5M"
        assert canonicalize_cigar_match_operators(line) == line

    def test_header_line_unchanged(self):
        line = "@SQ\tSN:chr1\tLN:248956422"
        assert canonicalize_cigar_match_operators(line) == line

    def test_nm_tag_recomputed(self):
        # 5M, MD:Z:2A2 (1 mismatch), NM was 0 -> recomputed to 1
        line = self._line("5M", "ACGTA", "NM:i:0", "MD:Z:2A2")
        out = canonicalize_cigar_match_operators(line)
        assert self._cigar_of(out) == "2=1X2="
        assert self._tag_value(out, "NM:i:") == "NM:i:1"

    def test_nm_with_indels_includes_indel_length(self):
        # 3M2I2M, MD:Z:5 (no mismatches in the M ops), NM should be 2 (the I bases).
        line = self._line("3M2I2M", "ACGTTAC", "NM:i:2", "MD:Z:5")
        out = canonicalize_cigar_match_operators(line)
        # CIGAR becomes 3=2I2= (no mismatches), NM = 0 (X) + 2 (I) = 2
        assert self._cigar_of(out) == "3=2I2="
        assert self._tag_value(out, "NM:i:") == "NM:i:2"

    def test_nm_recompute_with_deletion(self):
        # 3M2D2M, MD:Z:3^AG2 -> 3=2D2=, NM = 0 (X) + 2 (D) = 2
        line = self._line("3M2D2M", "ACGAC", "NM:i:2", "MD:Z:3^AG2")
        out = canonicalize_cigar_match_operators(line)
        assert self._cigar_of(out) == "3=2D2="
        assert self._tag_value(out, "NM:i:") == "NM:i:2"

    def test_trailing_newline_preserved(self):
        line = self._line("5M", "ACGTA", "MD:Z:5") + "\n"
        out = canonicalize_cigar_match_operators(line)
        assert out.endswith("\n")
        assert self._cigar_of(out) == "5="


# ===========================================================================
# Phase-2 SAM subtag shuffles — verify semantics-preserving invariants
# ===========================================================================

class TestShuffleHeaderSubtags:
    HEADER = [
        "@HD\tVN:1.6\tSO:coordinate\tGO:none",
        "@SQ\tSN:chr1\tLN:248956422\tM5:abc1234",
        "@SQ\tSN:chr2\tLN:242193529",
        "@RG\tID:sample1\tLB:libA\tSM:subject1\tPL:ILLUMINA",
        "@PG\tID:bwa\tPN:bwa\tVN:0.7.17\tCL:bwa mem ref.fa in.fq",
        "@CO\tfirst comment",
        "@CO\tsecond comment",
    ]

    def test_hd_shuffle_preserves_kv_set(self):
        out = shuffle_hd_subtags(self.HEADER, seed=42)
        # The @HD line changed order but contents are preserved
        orig_kv = set(self.HEADER[0].split("\t")[1:])
        new_kv = set(out[0].split("\t")[1:])
        assert orig_kv == new_kv
        assert out[0].startswith("@HD\t")

    def test_hd_shuffle_only_touches_hd(self):
        out = shuffle_hd_subtags(self.HEADER, seed=42)
        # Every non-@HD line is byte-identical
        for orig, new in zip(self.HEADER[1:], out[1:]):
            assert orig == new

    def test_hd_shuffle_deterministic(self):
        a = shuffle_hd_subtags(self.HEADER, seed=7)
        b = shuffle_hd_subtags(self.HEADER, seed=7)
        assert a == b

    def test_sq_shuffle_preserves_line_order(self):
        out = shuffle_sq_record_subtags(self.HEADER, seed=42)
        # @SQ chr1 still comes before @SQ chr2
        sn_order = [ln for ln in out if ln.startswith("@SQ")]
        assert "chr1" in sn_order[0]
        assert "chr2" in sn_order[1]

    def test_sq_shuffle_preserves_kv_set_per_line(self):
        out = shuffle_sq_record_subtags(self.HEADER, seed=42)
        orig_sq = [set(ln.split("\t")[1:]) for ln in self.HEADER if ln.startswith("@SQ")]
        new_sq = [set(ln.split("\t")[1:]) for ln in out if ln.startswith("@SQ")]
        assert orig_sq == new_sq

    def test_rg_shuffle_preserves_set(self):
        out = shuffle_rg_record_subtags(self.HEADER, seed=42)
        orig = set(self.HEADER[3].split("\t")[1:])
        new = set(out[3].split("\t")[1:])
        assert orig == new

    def test_pg_shuffle_preserves_set(self):
        out = shuffle_pg_record_subtags(self.HEADER, seed=42)
        orig = set(self.HEADER[4].split("\t")[1:])
        new = set(out[4].split("\t")[1:])
        assert orig == new

    def test_co_shuffle_preserves_co_multiset(self):
        out = shuffle_co_comments(self.HEADER, seed=42)
        orig_co = sorted(ln for ln in self.HEADER if ln.startswith("@CO"))
        new_co = sorted(ln for ln in out if ln.startswith("@CO"))
        assert orig_co == new_co

    def test_co_shuffle_preserves_non_co_lines(self):
        out = shuffle_co_comments(self.HEADER, seed=42)
        orig_non_co = [ln for ln in self.HEADER if not ln.startswith("@CO")]
        new_non_co = [ln for ln in out if not ln.startswith("@CO")]
        assert orig_non_co == new_non_co

    def test_single_subtag_line_is_noop(self):
        # Lines with only one TAG:VALUE can't be shuffled meaningfully.
        header = ["@HD\tVN:1.6"]
        assert shuffle_hd_subtags(header, seed=42) == header


class TestSubtagShuffleCanonicalInvariance:
    """The canonicalizer's `_parse_tag_fields` sorts dict keys, so every
    shuffle_*_subtags transform MUST produce byte-identical canonical
    JSON. Without this invariant the metamorphic oracle would fail on
    every parser and the MR would be auto-quarantined."""

    HEADER = [
        "@HD\tVN:1.6\tSO:coordinate\tGO:none",
        "@SQ\tSN:chr1\tLN:248956422\tM5:abc1234",
        "@SQ\tSN:chr2\tLN:242193529",
        "@RG\tID:sample1\tLB:libA\tSM:subject1",
    ]
    # Minimal record line so normalize_sam_text has something to parse.
    RECORD = "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"

    def _canonical(self, lines):
        from test_engine.canonical.sam_normalizer import normalize_sam_text
        return normalize_sam_text(lines).model_dump()

    def test_hd_shuffle_canonical_equal(self):
        orig = self.HEADER + [self.RECORD]
        shuffled = shuffle_hd_subtags(self.HEADER, seed=42) + [self.RECORD]
        assert self._canonical(orig) == self._canonical(shuffled)

    def test_sq_shuffle_canonical_equal(self):
        orig = self.HEADER + [self.RECORD]
        shuffled = shuffle_sq_record_subtags(self.HEADER, seed=42) + [self.RECORD]
        assert self._canonical(orig) == self._canonical(shuffled)

    def test_rg_shuffle_canonical_equal(self):
        orig = self.HEADER + [self.RECORD]
        shuffled = shuffle_rg_record_subtags(self.HEADER, seed=42) + [self.RECORD]
        assert self._canonical(orig) == self._canonical(shuffled)


# ===========================================================================
# Phase-2 SAM malformed mutators — verify each breaks exactly one rule
# ===========================================================================

class TestMalformedSamMutators:
    HEADER = [
        "@HD\tVN:1.6\tSO:coordinate",
        "@SQ\tSN:chr1\tLN:248956422",
    ]
    PAIRED_RECS = [
        "r1\t99\tchr1\t100\t30\t10M\t=\t200\t110\tACGTACGTAC\tIIIIIIIIII\tNM:i:0",
        "r1\t147\tchr1\t200\t30\t10M\t=\t100\t-110\tACGTACGTAC\tIIIIIIIIII\tNM:i:0",
    ]

    def test_violate_tlen_sign_flips_sign(self):
        lines = self.HEADER + self.PAIRED_RECS
        out = violate_tlen_sign_consistency(lines, seed=0)
        # Find the first record line (index 2)
        first_rec_cols = out[2].rstrip("\n").split("\t")
        orig_tlen = int(self.PAIRED_RECS[0].split("\t")[8])
        new_tlen = int(first_rec_cols[8])
        assert new_tlen == -orig_tlen
        # Mate record unchanged
        assert out[3] == self.PAIRED_RECS[1]

    def test_violate_tlen_noop_when_zero(self):
        lines = self.HEADER + [
            "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGT\tIIII"
        ]
        assert violate_tlen_sign_consistency(lines, seed=0) == lines

    def test_violate_optional_tag_type_injects_x(self):
        lines = self.HEADER + [
            "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\tNM:i:0\tMD:Z:10"
        ]
        out = violate_optional_tag_type_character(lines, seed=0)
        # First optional tag at col 11 (0-indexed)
        cols = out[2].rstrip("\n").split("\t")
        assert cols[11].split(":")[1] == "X", f"expected X type char, got {cols[11]}"

    def test_violate_optional_tag_noop_when_no_tags(self):
        lines = self.HEADER + [
            "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGT\tIIII"
        ]
        assert violate_optional_tag_type_character(lines, seed=0) == lines

    def test_violate_flag_bit_exclusivity_sets_unmapped(self):
        lines = self.HEADER + self.PAIRED_RECS
        out = violate_flag_bit_exclusivity(lines, seed=0)
        new_flag = int(out[2].rstrip("\n").split("\t")[1])
        orig_flag = int(self.PAIRED_RECS[0].split("\t")[1])
        assert new_flag & 0x4, "expected 0x4 (unmapped) bit to be set"
        assert new_flag == orig_flag | 0x4

    def test_violate_flag_noop_when_unmapped(self):
        lines = self.HEADER + [
            # RNAME=* implies already unmapped
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\tACGT\tIIII"
        ]
        assert violate_flag_bit_exclusivity(lines, seed=0) == lines


# ===========================================================================
# Variant normalization (Tan 2015)
# ===========================================================================

class TestTrimCommonAffixes:
    def test_suffix_trim(self):
        # REF=AA, ALT=AC at POS=100 -> REF=A, ALT=C at POS=101
        assert trim_common_affixes("AA", "AC", 100) == ("A", "C", 101)

    def test_prefix_trim(self):
        # REF=AT, ALT=GT share suffix -> trimmed REF=A, ALT=G, POS unchanged
        assert trim_common_affixes("AT", "GT", 100) == ("A", "G", 100)

    def test_snv_unchanged(self):
        # Single-base SNV has no shared affix, returns unchanged
        assert trim_common_affixes("A", "C", 100) == ("A", "C", 100)

    def test_deterministic(self):
        # Pure function — same input always gives same output
        r1 = trim_common_affixes("AAAA", "AATA", 50)
        r2 = trim_common_affixes("AAAA", "AATA", 50)
        assert r1 == r2


class TestLeftAlignIndel:
    def test_homopolymer_shift(self):
        # REF=AAA, ALT=AA at POS=5 -> shift POS to 4 (homopolymer run)
        new_ref, new_alt, new_pos = left_align_indel("AAA", "AA", 5)
        assert new_pos == 4
        assert new_ref == "AAA"
        assert new_alt == "AA"

    def test_snv_no_shift(self):
        # Equal-length (SNV) is never shifted
        assert left_align_indel("A", "T", 100) == ("A", "T", 100)

    def test_pos_boundary(self):
        # POS=1 cannot shift left
        assert left_align_indel("AAA", "AA", 1) == ("AAA", "AA", 1)

    def test_non_homopolymer_no_shift(self):
        # REF=AT, ALT=ATT — REF[0]!=REF[-1], not safe to shift
        assert left_align_indel("AT", "ATT", 5) == ("AT", "ATT", 5)


class TestSplitMultiAllelic:
    def test_two_alts_split(self):
        # ALT=T,C -> two records, each with one ALT
        rec = "chr1\t100\t.\tA\tT,C\t50\tPASS\tAC=1,2;AN=4\tGT\t0/1\t1/2".split("\t")
        info_meta = {"AC": {"Number": "A"}, "AN": {"Number": "1"}}
        fmt_meta = {"GT": {"Number": "1"}}
        result = split_multi_allelic(rec, info_meta, fmt_meta)
        assert len(result) == 2
        assert result[0][4] == "T"
        assert result[1][4] == "C"
        # Number=A field AC split: T gets 1, C gets 2
        assert "AC=1" in result[0][7]
        assert "AC=2" in result[1][7]
        # Number=1 field AN preserved in both
        assert "AN=4" in result[0][7]
        assert "AN=4" in result[1][7]

    def test_gt_remap_preserves_ref(self):
        # Sample 0/2 in multi-ALT -> "0/." in ALT=T record, "0/1" in ALT=C record
        rec = "chr1\t100\t.\tA\tT,C\t50\tPASS\t.\tGT\t0/2\t1/1".split("\t")
        info_meta = {}
        fmt_meta = {"GT": {"Number": "1"}}
        result = split_multi_allelic(rec, info_meta, fmt_meta)
        # First sample (0/2): in T record becomes 0/., in C record becomes 0/1
        assert result[0][9] == "0/."    # T record, 0=REF stays, 2 is not this ALT
        assert result[1][9] == "0/1"    # C record, 2 becomes 1

    def test_single_alt_passthrough(self):
        # Single ALT returns one record unchanged
        rec = "chr1\t100\t.\tA\tT\t50\tPASS\tAC=1\tGT\t0/1".split("\t")
        result = split_multi_allelic(rec, {"AC": {"Number": "A"}}, {"GT": {}})
        assert len(result) == 1


# ===========================================================================
# CSQ/ANN annotation ordering
# ===========================================================================

class TestPermuteCsqAnnotations:
    INFO = "DP=10;AF=0.5;CSQ=A|gene1|syn,T|gene2|missense,G|gene3|stop;AC=1"

    def test_deterministic(self):
        r1 = permute_csq_annotations(self.INFO, seed=42)
        r2 = permute_csq_annotations(self.INFO, seed=42)
        assert r1 == r2

    def test_preserves_pipe_count(self):
        # Each CSQ record's sub-field layout must stay intact
        result = permute_csq_annotations(self.INFO, seed=7)
        csq = [c for c in result.split(";") if c.startswith("CSQ=")][0]
        records = csq[len("CSQ="):].split(",")
        assert all(r.count("|") == 2 for r in records)

    def test_non_csq_fields_preserved(self):
        # DP, AF, AC are not touched
        result = permute_csq_annotations(self.INFO, seed=0)
        parts = {p.split("=")[0]: p for p in result.split(";")}
        assert parts["DP"] == "DP=10"
        assert parts["AF"] == "AF=0.5"
        assert parts["AC"] == "AC=1"

    def test_empty_info_unchanged(self):
        assert permute_csq_annotations(".") == "."
        assert permute_csq_annotations("") == ""

    def test_single_record_unchanged(self):
        # Only one comma-less record — nothing to permute
        assert permute_csq_annotations("CSQ=A|x|y") == "CSQ=A|x|y"


# ===========================================================================
# Round 2 — pos_shift, RNEXT alias, HD VN bump
# ===========================================================================

class TestPosShiftWithSqLnBoundCheck:
    HEADER = ["@HD\tVN:1.6\n", "@SQ\tSN:chr1\tLN:10000\n", "@SQ\tSN:chr2\tLN:5000\n"]

    def test_basic_shift_widens_ln_and_pos(self):
        lines = self.HEADER + [
            "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        ]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        # @SQ chr1 LN should be 10000 + 500 = 10500
        assert "LN:10500" in out[1]
        # @SQ chr2 LN should be 5000 + 500 = 5500
        assert "LN:5500" in out[2]
        # POS should be 100 + 500 = 600
        assert out[3].split("\t")[3] == "600"

    def test_no_op_when_record_overflows_new_ln(self):
        # Record at POS=9990, CIGAR=20M occupies bases 9990..10009. With LN=10000
        # the original is INVALID already (off-reference). We only widen LN by
        # shift, but the bound is on (new POS + ref_consume - 1 <= new_LN).
        # POS=9990+500=10490, ref_consume=20, end=10509. new_LN=10500. 10509 > 10500 → no-op.
        lines = self.HEADER + [
            "r1\t0\tchr1\t9990\t30\t20M\t*\t0\t0\t" + "A"*20 + "\t" + "I"*20 + "\n"
        ]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert out == lines

    def test_unmapped_records_are_skipped_but_lns_still_widen(self):
        # Unmapped record (FLAG=4, RNAME='*', POS=0) — bound check skips it.
        lines = self.HEADER + [
            "r1\t4\t*\t0\t255\t*\t*\t0\t0\tACGT\tIIII\n"
        ]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert "LN:10500" in out[1]  # @SQ still widens
        assert "LN:5500" in out[2]
        # Unmapped record's POS stays 0 (was skipped by bound check + shift loop).
        assert out[3].split("\t")[3] == "0"

    def test_unknown_rname_record_is_skipped(self):
        # Record references chr_unknown which is NOT in @SQ — function leaves
        # POS untouched (no LN to bound-check against).
        lines = self.HEADER + [
            "r1\t0\tchr_unknown\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        ]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert "LN:10500" in out[1]  # @SQ widens
        assert out[3].split("\t")[3] == "100"  # POS unchanged

    def test_shift_zero_is_no_op_copy(self):
        lines = self.HEADER + [
            "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        ]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=0)
        assert out == lines
        assert out is not lines  # but it's a fresh list

    def test_negative_shift_raises(self):
        with pytest.raises(ValueError):
            pos_shift_with_sq_ln_bound_check(self.HEADER, shift=-1)

    def test_no_sq_lines_returns_input_unchanged(self):
        lines = ["@HD\tVN:1.6\n",
                 "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGT\tIIII\n"]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert out == lines

    def test_preserves_trailing_newlines(self):
        # Mix \n and no-newline lines; transform must preserve each line's
        # original trailing newline state.
        lines = ["@HD\tVN:1.6\n",
                 "@SQ\tSN:chr1\tLN:1000\n",  # \n
                 "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGT\tIIII"]  # no \n
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert out[1].endswith("\n")
        assert not out[2].endswith("\n")

    def test_lns_exceeds_2_31_no_op(self):
        # SAMv1 §1.3 LN max = 2^31 - 1 = 2147483647. If new LN would exceed,
        # no-op rather than emit an out-of-spec value.
        lines = ["@HD\tVN:1.6\n",
                 f"@SQ\tSN:chr1\tLN:{2**31 - 100}\n",
                 "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=200)
        assert out == lines  # no-op

    def test_freshness_input_not_mutated(self):
        lines = self.HEADER + [
            "r1\t0\tchr1\t100\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        ]
        original_lines = list(lines)
        pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert lines == original_lines  # not mutated

    def test_pos_zero_record_skipped(self):
        # FLAG=0 (mapped) but POS=0 is a SAMv1 §1.4 boundary: 1-based POS, 0
        # means "no position assigned" / unmapped. We treat it as skip.
        lines = self.HEADER + [
            "r1\t0\tchr1\t0\t30\t*\t*\t0\t0\t*\t*\n"
        ]
        out = pos_shift_with_sq_ln_bound_check(lines, shift=500)
        assert out[3].split("\t")[3] == "0"


class TestCanonicalizeRnextEqualsAlias:
    @staticmethod
    def _make(rnext: str, rname: str = "chr1") -> str:
        return (f"r1\t0\t{rname}\t100\t30\t10M\t{rnext}\t200\t100\t"
                "ACGTACGTAC\tIIIIIIIIII\n")

    def test_alias_mode_collapses_rname_to_equals(self):
        line = self._make(rnext="chr1")  # RNEXT == RNAME
        out = canonicalize_rnext_equals_alias(line, mode="alias")
        assert out.split("\t")[6] == "="

    def test_alias_mode_no_change_when_rnext_already_equals(self):
        line = self._make(rnext="=")
        out = canonicalize_rnext_equals_alias(line, mode="alias")
        # alias mode only acts when RNEXT == RNAME; "=" != "chr1"
        # so this is a no-op.
        assert out == line

    def test_alias_mode_no_change_when_rnext_differs(self):
        line = self._make(rnext="chr2")  # different chr
        out = canonicalize_rnext_equals_alias(line, mode="alias")
        assert out == line

    def test_alias_mode_no_change_when_rname_star(self):
        line = self._make(rnext="*", rname="*")
        out = canonicalize_rnext_equals_alias(line, mode="alias")
        assert out == line

    def test_explicit_mode_expands_equals_to_rname(self):
        line = self._make(rnext="=")
        out = canonicalize_rnext_equals_alias(line, mode="explicit")
        assert out.split("\t")[6] == "chr1"

    def test_explicit_mode_no_change_when_rnext_already_explicit(self):
        line = self._make(rnext="chr1")
        out = canonicalize_rnext_equals_alias(line, mode="explicit")
        assert out == line

    def test_explicit_mode_no_change_when_rname_star(self):
        # RNAME='*' means the read is unmapped; resolving '=' against '*'
        # would emit "RNEXT:*" which is meaningful (unmapped mate) but the
        # transform is conservative — no-op.
        line = self._make(rnext="=", rname="*")
        out = canonicalize_rnext_equals_alias(line, mode="explicit")
        assert out == line

    def test_invalid_mode_raises(self):
        line = self._make(rnext="chr1")
        with pytest.raises(ValueError):
            canonicalize_rnext_equals_alias(line, mode="bogus")

    def test_short_record_returns_unchanged(self):
        # 5-column line (header-ish or partial). Function bails out.
        line = "r1\t0\tchr1\t100\t30\n"
        out = canonicalize_rnext_equals_alias(line, mode="alias")
        assert out == line

    def test_preserves_trailing_newline(self):
        line = self._make(rnext="chr1")
        assert line.endswith("\n")
        out = canonicalize_rnext_equals_alias(line, mode="alias")
        assert out.endswith("\n")
        line2 = line.rstrip("\n")
        out2 = canonicalize_rnext_equals_alias(line2, mode="alias")
        assert not out2.endswith("\n")


class TestBumpHdVnMinor:
    def test_1_6_to_1_5(self):
        out = bump_hd_vn_minor(["@HD\tVN:1.6\tSO:coordinate\n"])
        assert "VN:1.5" in out[0]
        assert "VN:1.6" not in out[0]

    def test_1_5_to_1_6(self):
        out = bump_hd_vn_minor(["@HD\tVN:1.5\tSO:coordinate\n"])
        assert "VN:1.6" in out[0]
        assert "VN:1.5" not in out[0]

    def test_other_vn_unchanged(self):
        # Out-of-range VN value → leave alone (don't fabricate a toggle).
        out = bump_hd_vn_minor(["@HD\tVN:1.4\tSO:coordinate\n"])
        assert out == ["@HD\tVN:1.4\tSO:coordinate\n"]

    def test_no_hd_unchanged(self):
        # @SQ alone, no @HD — nothing to toggle.
        in_lines = ["@SQ\tSN:chr1\tLN:1000\n"]
        out = bump_hd_vn_minor(in_lines)
        assert out == in_lines

    def test_hd_without_vn_unchanged(self):
        # @HD without VN field — left alone.
        in_lines = ["@HD\tSO:coordinate\n"]
        out = bump_hd_vn_minor(in_lines)
        assert out == in_lines

    def test_other_lines_unchanged(self):
        in_lines = ["@HD\tVN:1.6\n",
                    "@SQ\tSN:chr1\tLN:1000\n",
                    "@RG\tID:sample1\tSM:sample1\n"]
        out = bump_hd_vn_minor(in_lines)
        assert out[1] == in_lines[1]
        assert out[2] == in_lines[2]

    def test_preserves_trailing_newline(self):
        out = bump_hd_vn_minor(["@HD\tVN:1.6\tSO:coordinate\n"])
        assert out[0].endswith("\n")
        out2 = bump_hd_vn_minor(["@HD\tVN:1.6\tSO:coordinate"])
        assert not out2[0].endswith("\n")

    def test_idempotent_pair_returns_to_original(self):
        # Toggling twice gets back to original (1.6 → 1.5 → 1.6).
        in_lines = ["@HD\tVN:1.6\tSO:coordinate\n"]
        once = bump_hd_vn_minor(in_lines)
        twice = bump_hd_vn_minor(once)
        assert twice == in_lines


# ===========================================================================
# Run
# ===========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
