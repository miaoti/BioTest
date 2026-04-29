"""
Tests for the Run-9 tolerance fixes in
``test_engine.canonical.sam_normalizer``.

Each fix has a focused test that proves the SAM-spec-allowed variation
collapses to byte-identical canonical JSON. These guard rails matter
because the consensus oracle can only stay sound if equivalent inputs
canonicalise to the same Pydantic record.
"""

from __future__ import annotations

from typing import Optional

import pytest

from test_engine.canonical.sam_normalizer import (
    BIOPYTHON_CONSUMED_TAGS,
    FLOAT_TAG_SIGFIGS,
    _compute_nm_from_cigar,
    _round_float_sigfig,
    normalize_sam_text,
)
from test_engine.canonical.schema import CigarOp


# ---------------------------------------------------------------------------
# Fix 1.1 — RNEXT="=" alias resolves to RNAME
# ---------------------------------------------------------------------------

class TestRnextEqualsResolution:
    """RNEXT='=' is a SAM v1.6 alias for "same as RNAME". Different
    parsers preserve or resolve it; we resolve here so canonical JSON
    is invariant under either choice."""

    @staticmethod
    def _make(rnext_col: str) -> str:
        return (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            f"r1\t99\tchr1\t100\t60\t10M\t{rnext_col}\t200\t150\t"
            "ACGTACGTAC\tIIIIIIIIII\n"
        )

    def test_equals_resolves_to_rname(self):
        canon = normalize_sam_text(self._make("=").splitlines(keepends=True))
        assert canon.records[0].RNEXT == "chr1"

    def test_explicit_rname_unchanged(self):
        canon = normalize_sam_text(self._make("chr1").splitlines(keepends=True))
        assert canon.records[0].RNEXT == "chr1"

    def test_equals_and_explicit_canonicalise_identically(self):
        a = normalize_sam_text(self._make("=").splitlines(keepends=True))
        b = normalize_sam_text(self._make("chr1").splitlines(keepends=True))
        assert a.model_dump() == b.model_dump(), (
            "RNEXT='=' must canonicalise to the same record as the "
            "resolved name, otherwise consensus oracle false-positives."
        )

    def test_star_remains_none(self):
        canon = normalize_sam_text(self._make("*").splitlines(keepends=True))
        assert canon.records[0].RNEXT is None


# ---------------------------------------------------------------------------
# Fix 1.2 — Float-tag precision: round to N sig figs
# ---------------------------------------------------------------------------

class TestFloatTagPrecision:
    @staticmethod
    def _make(tag_value: str) -> str:
        return (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            f"r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\t"
            f"XF:f:{tag_value}\n"
        )

    def test_85_and_0p85_canonicalise_same(self):
        a = normalize_sam_text(self._make("0.85").splitlines(keepends=True))
        b = normalize_sam_text(self._make("0.8500000000").splitlines(keepends=True))
        c = normalize_sam_text(self._make("8.5e-1").splitlines(keepends=True))
        # All three serialisations are the same number; canonical must agree.
        assert a.records[0].tags["XF"].value == b.records[0].tags["XF"].value
        assert a.records[0].tags["XF"].value == c.records[0].tags["XF"].value

    def test_zero_and_negative_zero(self):
        # Edge case: 0.0 should not blow up in log10.
        a = normalize_sam_text(self._make("0.0").splitlines(keepends=True))
        b = normalize_sam_text(self._make("-0.0").splitlines(keepends=True))
        assert a.records[0].tags["XF"].value == 0.0
        assert b.records[0].tags["XF"].value == 0.0  # noqa: 0.0 == -0.0

    def test_round_helper_keeps_significant_digits(self):
        assert _round_float_sigfig(0.1234567890, sig=6) == 0.123457
        assert _round_float_sigfig(123.456789, sig=6) == 123.457
        assert _round_float_sigfig(0.0) == 0.0  # short-circuit


# ---------------------------------------------------------------------------
# Fix 1.3 — Drop biopython-consumed tags
# ---------------------------------------------------------------------------

class TestBiopythonConsumedTagsDropped:
    """Bio.Align.parse consumes MD/AS into its alignment object and
    never re-emits them. Other parsers preserve them — global drop
    keeps consensus apples-to-apples."""

    def test_md_dropped(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\t"
            "MD:Z:10\tNM:i:0\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        rec = canon.records[0]
        assert "MD" not in rec.tags
        # Non-consumed tag preserved.
        assert "NM" in rec.tags

    def test_as_dropped(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\t"
            "AS:i:42\tNM:i:0\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        rec = canon.records[0]
        assert "AS" not in rec.tags
        assert "NM" in rec.tags

    def test_with_or_without_md_canonicalises_identically(self):
        with_md = (
            "@HD\tVN:1.6\n@SQ\tSN:chr1\tLN:1000\n"
            "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\t"
            "MD:Z:10\tNM:i:0\n"
        )
        without_md = (
            "@HD\tVN:1.6\n@SQ\tSN:chr1\tLN:1000\n"
            "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\t"
            "NM:i:0\n"
        )
        a = normalize_sam_text(with_md.splitlines(keepends=True))
        b = normalize_sam_text(without_md.splitlines(keepends=True))
        assert a.model_dump() == b.model_dump()

    def test_set_membership_constants_intact(self):
        # If someone adds a tag to BIOPYTHON_CONSUMED_TAGS without test
        # coverage, this catches the change in CI.
        assert "MD" in BIOPYTHON_CONSUMED_TAGS
        assert "AS" in BIOPYTHON_CONSUMED_TAGS
        # Documented size — bump if/when we widen the set.
        assert len(BIOPYTHON_CONSUMED_TAGS) == 2


# ---------------------------------------------------------------------------
# Cross-fix sanity — full record round-trip with all tolerances active
# ---------------------------------------------------------------------------

class TestCombinedTolerance:
    def test_two_equivalent_serialisations_canonicalise_identically(self):
        # Worst-case combo: RNEXT='=', float-tag precision, MD present.
        a_text = (
            "@HD\tVN:1.6\n@SQ\tSN:chr1\tLN:1000\n"
            "r1\t99\tchr1\t100\t60\t10M\t=\t200\t150\t"
            "ACGTACGTAC\tIIIIIIIIII\tMD:Z:10\tXF:f:0.85\n"
        )
        b_text = (
            "@HD\tVN:1.6\n@SQ\tSN:chr1\tLN:1000\n"
            "r1\t99\tchr1\t100\t60\t10M\tchr1\t200\t150\t"
            "ACGTACGTAC\tIIIIIIIIII\tXF:f:0.8500000\n"
        )
        a = normalize_sam_text(a_text.splitlines(keepends=True))
        b = normalize_sam_text(b_text.splitlines(keepends=True))
        assert a.model_dump() == b.model_dump(), (
            "All three Run-9 tolerance fixes must compose: RNEXT alias, "
            "float precision, and MD drop together."
        )


# ---------------------------------------------------------------------------
# Fix #5 — SEQ case normalization (B2)
# ---------------------------------------------------------------------------

class TestSeqCaseNormalization:
    """SAMv1 §1.4.10 SEQ admits both upper and lower case. Different
    parsers preserve or normalize; we uppercase here so canonical JSON
    is invariant under either choice."""

    @staticmethod
    def _make(seq: str) -> str:
        return (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            f"r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\t{seq}\tIIIIIIIIII\n"
        )

    def test_lowercase_seq_uppercased(self):
        canon = normalize_sam_text(self._make("acgtacgtac").splitlines(keepends=True))
        assert canon.records[0].SEQ == "ACGTACGTAC"

    def test_mixed_case_uppercased(self):
        canon = normalize_sam_text(self._make("AcGtAcGtAc").splitlines(keepends=True))
        assert canon.records[0].SEQ == "ACGTACGTAC"

    def test_already_upper_unchanged(self):
        canon = normalize_sam_text(self._make("ACGTACGTAC").splitlines(keepends=True))
        assert canon.records[0].SEQ == "ACGTACGTAC"

    def test_missing_seq_stays_none(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.records[0].SEQ is None

    def test_iupac_uppercased(self):
        # IUPAC ambiguity codes (12 chars to match 12M CIGAR).
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            "r1\t0\tchr1\t100\t60\t12M\t*\t0\t0\trynwkmRYNWKM\tIIIIIIIIIIII\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.records[0].SEQ == "RYNWKMRYNWKM"

    def test_two_records_with_different_case_canonicalize_identically(self):
        a = normalize_sam_text(self._make("acgtacgtac").splitlines(keepends=True))
        b = normalize_sam_text(self._make("ACGTACGTAC").splitlines(keepends=True))
        assert a.model_dump() == b.model_dump(), (
            "SEQ case must canonicalize identically — otherwise the "
            "consensus oracle false-positives on case-preserving vs "
            "case-normalizing parsers."
        )


# ---------------------------------------------------------------------------
# Fix #6 — NM auto-compute (B3)
# ---------------------------------------------------------------------------

class TestNmAutoCompute:
    """When CIGAR is canonicalized to =/X by an upstream MR transform,
    parsers that drop NM and parsers that preserve NM disagree. We
    auto-compute NM here to keep voters comparable.

    NM = sum(X op lengths) + sum(I+D op lengths) per SAMtags spec."""

    @staticmethod
    def _make(cigar: str, *, with_nm: Optional[int] = None) -> str:
        # Use a SEQ length compatible with the CIGAR's query-consuming
        # ops to avoid strict-mode mismatches. We don't enable strict
        # mode here, so length is informational; pad to 10 for visual
        # clarity.
        nm_col = f"\tNM:i:{with_nm}" if with_nm is not None else ""
        return (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            f"r1\t0\tchr1\t100\t60\t{cigar}\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII"
            f"{nm_col}\n"
        )

    def test_nm_added_when_absent_with_eq_x_cigar(self):
        canon = normalize_sam_text(self._make("3=2X").splitlines(keepends=True))
        rec = canon.records[0]
        assert "NM" in rec.tags
        assert rec.tags["NM"].type == "i"
        assert rec.tags["NM"].value == 2

    def test_nm_kept_when_present(self):
        canon = normalize_sam_text(
            self._make("5M", with_nm=7).splitlines(keepends=True)
        )
        rec = canon.records[0]
        assert "NM" in rec.tags
        assert rec.tags["NM"].value == 7  # not recomputed/overwritten

    def test_nm_not_added_when_cigar_has_m(self):
        canon = normalize_sam_text(self._make("5M").splitlines(keepends=True))
        rec = canon.records[0]
        assert "NM" not in rec.tags, (
            "NM is indeterminate when CIGAR has M ops; we must not guess."
        )

    def test_nm_not_added_when_cigar_missing(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:1000\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        rec = canon.records[0]
        assert "NM" not in rec.tags

    def test_nm_includes_indel_bases(self):
        # 3=2I3= → 0 mismatches + 2 insertions + 0 deletions = 2
        canon = normalize_sam_text(self._make("3=2I3=").splitlines(keepends=True))
        rec = canon.records[0]
        assert rec.tags["NM"].value == 2

    def test_nm_zero_for_all_match(self):
        canon = normalize_sam_text(self._make("5=").splitlines(keepends=True))
        rec = canon.records[0]
        assert rec.tags["NM"].value == 0

    def test_helper_returns_none_when_m_present(self):
        # Direct unit test of the helper.
        cigar = [CigarOp(op="M", len=10)]
        assert _compute_nm_from_cigar(cigar) is None

    def test_helper_sums_x_i_d_lengths(self):
        cigar = [
            CigarOp(op="=", len=3),
            CigarOp(op="X", len=2),
            CigarOp(op="I", len=1),
            CigarOp(op="D", len=4),
            CigarOp(op="=", len=3),
        ]
        # X(2) + I(1) + D(4) = 7
        assert _compute_nm_from_cigar(cigar) == 7


# ---------------------------------------------------------------------------
# Fix #7 — Header @SQ/@RG/@PG section sort (B4)
# ---------------------------------------------------------------------------

class TestHeaderSectionSort:
    """SAMv1 §1.3 imposes no ordering on @SQ/@RG/@PG lines (only @HD
    must come first). Sorting by the spec-defined canonical key (SN
    for @SQ, ID for @RG/@PG) makes the canonical JSON invariant under
    the `reorder_header_records` MR."""

    def test_sq_sorted_by_sn(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr2\tLN:200\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.header.SQ[0]["SN"] == "chr1"
        assert canon.header.SQ[1]["SN"] == "chr2"

    def test_rg_sorted_by_id(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "@RG\tID:zebra\tSM:sample1\n"
            "@RG\tID:alpha\tSM:sample2\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.header.RG[0]["ID"] == "alpha"
        assert canon.header.RG[1]["ID"] == "zebra"

    def test_pg_sorted_by_id(self):
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "@PG\tID:zzz\tPN:tool_z\n"
            "@PG\tID:aaa\tPN:tool_a\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.header.PG[0]["ID"] == "aaa"
        assert canon.header.PG[1]["ID"] == "zzz"

    def test_sq_permutation_canonicalizes_identically(self):
        sam_a = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "@SQ\tSN:chr2\tLN:200\n"
            "@SQ\tSN:chr3\tLN:300\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        sam_b = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr3\tLN:300\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "@SQ\tSN:chr2\tLN:200\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        a = normalize_sam_text(sam_a.splitlines(keepends=True))
        b = normalize_sam_text(sam_b.splitlines(keepends=True))
        assert a.header.SQ == b.header.SQ, (
            "@SQ permutation must canonicalize identically — this is "
            "the foundation of the reorder_header_records MR."
        )
        # Full canonical equality, too.
        assert a.model_dump() == b.model_dump()

    def test_hd_unchanged(self):
        # @HD remains a single dict with its own internal-tag sort.
        sam = (
            "@HD\tVN:1.6\tSO:coordinate\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.header.HD is not None
        assert canon.header.HD.get("VN") == "1.6"
        assert canon.header.HD.get("SO") == "coordinate"

    def test_co_already_sorted_unchanged(self):
        # @CO sort behavior unchanged from before B4.
        sam = (
            "@HD\tVN:1.6\n"
            "@SQ\tSN:chr1\tLN:100\n"
            "@CO\tzebra comment\n"
            "@CO\talpha comment\n"
            "r1\t4\t*\t0\t0\t*\t*\t0\t0\t*\t*\n"
        )
        canon = normalize_sam_text(sam.splitlines(keepends=True))
        assert canon.header.CO == ["alpha comment", "zebra comment"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
