"""
Tests for the Run-9 tolerance fixes in
``test_engine.canonical.sam_normalizer``.

Each fix has a focused test that proves the SAM-spec-allowed variation
collapses to byte-identical canonical JSON. These guard rails matter
because the consensus oracle can only stay sound if equivalent inputs
canonicalise to the same Pydantic record.
"""

from __future__ import annotations

import pytest

from test_engine.canonical.sam_normalizer import (
    BIOPYTHON_CONSUMED_TAGS,
    FLOAT_TAG_SIGFIGS,
    _round_float_sigfig,
    normalize_sam_text,
)


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
