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
    def test_whitelist_has_34_transforms(self):
        # 13 originals + 6 (Tan 2015 normalization / BCF round-trip /
        # CSQ permute) + 1 SUT-agnostic writer (sut_write_roundtrip) +
        # 5 Rank-3 spec-rule-targeted malformed-input mutators +
        # 1 Rank-5 query-method MR transform (query_method_roundtrip;
        # MR-Scout TOSEM 2024) +
        # 5 Phase-2 SAM header-subtag / @CO shuffles +
        # 3 Phase-2 SAM malformed mutators (TLEN / tag-type / FLAG).
        wl = get_whitelist()
        assert len(wl) == 34, f"Expected 34 transforms, got {len(wl)}: {wl}"

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
# Run
# ===========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
