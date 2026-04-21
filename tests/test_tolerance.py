"""
Tests for ``test_engine.oracles.tolerance.strip_to_strict`` + its
integration with the consensus oracle.

Fix #3 (Run 9 lesson, 2026-04-20). Two invariants:
  (1) ``strip_to_strict`` removes ONLY optional fields — never rewrites
      mandatory values, never drops them.
  (2) Consensus oracle with ``field_tolerance=True`` buckets voters
      that agree on mandatory fields together, even when their tags
      / INFO differ.
"""

from __future__ import annotations

import pytest

from test_engine.oracles.tolerance import (
    SAM_RECORD_STRICT_FIELDS,
    VCF_RECORD_STRICT_FIELDS,
    strip_to_strict,
)
from test_engine.oracles.consensus import get_consensus_output
from test_engine.runners.base import RunnerResult


# ---------------------------------------------------------------------------
# Strict-field constants — guards against silent churn
# ---------------------------------------------------------------------------

class TestStrictFieldConstants:
    def test_sam_has_exactly_11_mandatory_columns(self):
        # SAM v1.6 §1.4 — 11 mandatory columns per alignment record.
        assert len(SAM_RECORD_STRICT_FIELDS) == 11

    def test_sam_core_keys_present(self):
        for k in ("QNAME", "FLAG", "RNAME", "POS", "CIGAR"):
            assert k in SAM_RECORD_STRICT_FIELDS

    def test_vcf_has_8_mandatory_columns(self):
        # VCF v4.5 §1.4 — 8 mandatory (+ FORMAT for genotyped records).
        assert len(VCF_RECORD_STRICT_FIELDS) == 8

    def test_vcf_core_keys_present(self):
        for k in ("chrom", "pos", "ref", "alt"):
            assert k in VCF_RECORD_STRICT_FIELDS


# ---------------------------------------------------------------------------
# strip_to_strict behaviour
# ---------------------------------------------------------------------------

class TestStripToStrict:
    def _sam_doc(self, tags=None):
        rec = {
            "QNAME": "r1", "FLAG": 0, "RNAME": "chr1", "POS": 100,
            "MAPQ": 60, "CIGAR": [{"op": "M", "len": 10}],
            "RNEXT": None, "PNEXT": None, "TLEN": 0,
            "SEQ": "ACGTACGTAC", "QUAL": "IIIIIIIIII",
        }
        if tags is not None:
            rec["tags"] = tags
        return {"header": {"HD": {"VN": "1.6"}}, "records": [rec]}

    def test_removes_tags_from_sam_record(self):
        doc = self._sam_doc(tags={"NM": {"type": "i", "value": 0}})
        out = strip_to_strict(doc, "SAM")
        assert "tags" not in out["records"][0]

    def test_keeps_mandatory_sam_fields(self):
        doc = self._sam_doc(tags={"NM": {"type": "i", "value": 0}})
        out = strip_to_strict(doc, "SAM")
        rec = out["records"][0]
        for k in SAM_RECORD_STRICT_FIELDS:
            assert k in rec, f"mandatory {k} must survive strip"
        assert rec["QNAME"] == "r1"
        assert rec["POS"] == 100

    def test_header_untouched(self):
        doc = self._sam_doc()
        out = strip_to_strict(doc, "SAM")
        assert out["header"] == doc["header"]

    def test_vcf_strip(self):
        doc = {
            "header": {"fileformat": "VCFv4.5"},
            "records": [{
                "chrom": "chr1", "pos": 100, "id": ".",
                "ref": "A", "alt": ["T"], "qual": 30,
                "filter": ["PASS"], "format": "GT",
                "info": {"DP": 10, "AC": 1},
                "samples": [{"GT": "0/1"}],
            }],
        }
        out = strip_to_strict(doc, "VCF")
        rec = out["records"][0]
        # Mandatory kept.
        assert rec["chrom"] == "chr1"
        assert rec["pos"] == 100
        # Optional stripped.
        assert "info" not in rec
        assert "samples" not in rec

    def test_unknown_format_returns_unchanged(self):
        doc = {"records": [{"foo": 1}]}
        out = strip_to_strict(doc, "FASTA")
        assert out == doc

    def test_non_dict_input_returned_unchanged(self):
        assert strip_to_strict(None, "SAM") is None  # type: ignore[arg-type]
        assert strip_to_strict("not a dict", "SAM") == "not a dict"  # type: ignore[arg-type]

    def test_strip_is_non_destructive(self):
        doc = self._sam_doc(tags={"NM": {"type": "i", "value": 0}})
        original = dict(doc)
        _ = strip_to_strict(doc, "SAM")
        # Original still has tags.
        assert "tags" in doc["records"][0]


# ---------------------------------------------------------------------------
# Consensus integration — field_tolerance=True buckets tag-differing voters
# ---------------------------------------------------------------------------

def _R(name: str, value: dict | None) -> RunnerResult:
    return RunnerResult(
        success=value is not None,
        canonical_json=value,
        parser_name=name,
        format_type="SAM",
    )


def _rec(tags: dict) -> dict:
    return {
        "header": {"HD": {"VN": "1.6"}},
        "records": [{
            "QNAME": "r1", "FLAG": 0, "RNAME": "chr1", "POS": 100,
            "MAPQ": 60, "CIGAR": [{"op": "M", "len": 10}],
            "RNEXT": None, "PNEXT": None, "TLEN": 0,
            "SEQ": "ACGTACGTAC", "QUAL": "IIIIIIIIII",
            "tags": tags,
        }],
    }


class TestConsensusFieldTolerance:
    def test_tag_difference_splits_buckets_without_tolerance(self):
        a = _rec({"NM": {"type": "i", "value": 0}})
        b = _rec({"NM": {"type": "i", "value": 1}})
        outputs = {
            "htsjdk": _R("htsjdk", a), "pysam": _R("pysam", a),
            "biopython": _R("biopython", b), "seqan3": _R("seqan3", b),
        }
        c = get_consensus_output(outputs, format_context="SAM",
                                 field_tolerance=False)
        # 2-2 split, no htslib → inconclusive.
        assert c.is_inconclusive is True

    def test_tag_difference_merges_bucket_with_tolerance(self):
        a = _rec({"NM": {"type": "i", "value": 0}})
        b = _rec({"NM": {"type": "i", "value": 1}})
        outputs = {
            "htsjdk": _R("htsjdk", a), "pysam": _R("pysam", a),
            "biopython": _R("biopython", b), "seqan3": _R("seqan3", b),
        }
        c = get_consensus_output(outputs, format_context="SAM",
                                 field_tolerance=True)
        # All 4 voters agree on mandatory fields; tag difference ignored.
        assert c.is_inconclusive is False
        assert len(c.winning_voters) == 4

    def test_mandatory_difference_still_splits_with_tolerance(self):
        """Safety rail: tolerance must NOT mask real bugs. If voters
        disagree on POS, that's a semantic difference and bucket split
        should still occur."""
        a = _rec({"NM": {"type": "i", "value": 0}})
        b = _rec({"NM": {"type": "i", "value": 0}})
        # Mutate mandatory field on b.
        b["records"][0]["POS"] = 200
        outputs = {
            "htsjdk": _R("htsjdk", a), "pysam": _R("pysam", a), "biopython": _R("biopython", a),
            "seqan3": _R("seqan3", b),
        }
        c = get_consensus_output(outputs, format_context="SAM",
                                 field_tolerance=True)
        # 3-1 split on mandatory field, majority wins as expected.
        assert c.is_inconclusive is False
        assert len(c.winning_voters) == 3

    def test_tolerance_false_on_vcf_unchanged(self):
        """Default (False) must reproduce the legacy consensus behaviour
        on VCF — this guards historical Run-6 etc. numbers."""
        vcf_a = {
            "header": {"fileformat": "VCFv4.5"},
            "records": [{
                "chrom": "chr1", "pos": 100, "id": ".", "ref": "A",
                "alt": ["T"], "qual": 30, "filter": ["PASS"],
                "format": "GT", "info": {"DP": 10}, "samples": [{"GT": "0/1"}],
            }],
        }
        outputs = {
            "htsjdk": _R("htsjdk", vcf_a), "pysam": _R("pysam", vcf_a),
        }
        c = get_consensus_output(outputs, format_context="VCF",
                                 field_tolerance=False)
        assert c.is_inconclusive is False
        assert c.consensus_value == vcf_a


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
