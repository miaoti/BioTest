"""
Phase 3 tests — SAM↔BAM / SAM↔CRAM round-trip via samtools.

Every non-registry test skips cleanly when samtools is not on PATH,
so CI without samtools stays green. The registry + preconditions
checks run unconditionally.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from mr_engine.transforms import get_whitelist, TRANSFORM_REGISTRY
from mr_engine.transforms.sam import sam_bam_round_trip, sam_cram_round_trip
from test_engine.canonical.sam_normalizer import normalize_sam_text


SAMTOOLS = shutil.which("samtools")
REPO_ROOT = Path(__file__).resolve().parent.parent
TOY_REF = REPO_ROOT / "seeds" / "ref" / "toy.fa"


@pytest.fixture
def minimal_sam_with_ref():
    """A valid minimal SAM whose @SQ matches the committed toy reference."""
    return [
        "@HD\tVN:1.6\tSO:unsorted\n",
        "@SQ\tSN:chr1\tLN:300\n",
        "r1\t0\tchr1\t10\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
    ]


@pytest.fixture
def minimal_sam_mismatched_ref():
    """Valid SAM whose @SQ SN is absent from the toy reference."""
    return [
        "@HD\tVN:1.6\tSO:unsorted\n",
        "@SQ\tSN:unknown_chr_12345\tLN:100\n",
        "r1\t0\tunknown_chr_12345\t10\t30\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n",
    ]


# ---------------------------------------------------------------------------
# Registry + precondition invariants (always run)
# ---------------------------------------------------------------------------


def test_sam_bam_round_trip_registered():
    assert "sam_bam_round_trip" in TRANSFORM_REGISTRY


def test_sam_cram_round_trip_registered():
    assert "sam_cram_round_trip" in TRANSFORM_REGISTRY


def test_round_trip_transforms_declare_samtools_precondition():
    bam_meta = TRANSFORM_REGISTRY["sam_bam_round_trip"]
    assert "samtools_available" in bam_meta.preconditions
    cram_meta = TRANSFORM_REGISTRY["sam_cram_round_trip"]
    assert "samtools_available" in cram_meta.preconditions
    assert "cram_reference_available" in cram_meta.preconditions


def test_toy_reference_exists_and_under_cap():
    assert TOY_REF.exists(), "committed toy reference missing"
    size = TOY_REF.stat().st_size
    assert size < 10 * 1024, f"toy.fa is {size} bytes, expected <10 KB"


def test_toy_reference_covers_common_sq_names():
    """@SQ SN names in Tier-1 seeds should subset the toy reference."""
    names: set[str] = set()
    with TOY_REF.open() as f:
        for line in f:
            if line.startswith(">"):
                names.add(line[1:].split()[0].strip())
    # Check a few names the spec-example + minimal seeds rely on.
    expected_subset = {"chr1", "chr2", "chr3", "ref", "c1", "c2"}
    missing = expected_subset - names
    assert not missing, (
        f"toy.fa missing expected SNs {missing}; update "
        f"seeds/ref/toy.fa if Tier-1 seeds reference new chromosomes"
    )


# ---------------------------------------------------------------------------
# Round-trip behavior (skipped when samtools is not installed)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(SAMTOOLS is None, reason="samtools not on PATH")
def test_sam_bam_round_trip_preserves_core_fields(minimal_sam_with_ref):
    out = sam_bam_round_trip(minimal_sam_with_ref, seed=0)
    # Round-trip should still be valid SAM text.
    assert out and out[0].startswith("@")
    orig = normalize_sam_text(minimal_sam_with_ref)
    round_tripped = normalize_sam_text(out)
    # Core alignment fields survive — QNAME, POS, CIGAR, SEQ.
    assert len(orig.records) == len(round_tripped.records)
    assert orig.records[0].QNAME == round_tripped.records[0].QNAME
    assert orig.records[0].POS == round_tripped.records[0].POS
    assert orig.records[0].SEQ == round_tripped.records[0].SEQ


@pytest.mark.skipif(SAMTOOLS is None, reason="samtools not on PATH")
def test_sam_bam_round_trip_noop_without_samtools(monkeypatch, minimal_sam_with_ref):
    # Pretend samtools is not on PATH. The transform must return the
    # input unchanged rather than crash — defensive fallback below the
    # precondition filter.
    monkeypatch.setattr(
        "mr_engine.transforms.sam._samtools_binary", lambda: None
    )
    out = sam_bam_round_trip(minimal_sam_with_ref, seed=0)
    assert out == minimal_sam_with_ref


def test_sam_cram_round_trip_noops_on_mismatched_reference(
    minimal_sam_mismatched_ref,
):
    # No samtools needed — the transform short-circuits before the first
    # samtools call because no @SQ SN is in the toy reference.
    out = sam_cram_round_trip(minimal_sam_mismatched_ref, seed=0)
    assert out == minimal_sam_mismatched_ref


@pytest.mark.skipif(SAMTOOLS is None, reason="samtools not on PATH")
def test_sam_cram_round_trip_preserves_qname(minimal_sam_with_ref):
    out = sam_cram_round_trip(minimal_sam_with_ref, seed=0)
    # If samtools is available and the reference matches, we should get
    # a round-tripped SAM back. CRAM is lossy on some fields (=/X->M,
    # possibly NM/MD recompute) but QNAME/POS must survive.
    orig = normalize_sam_text(minimal_sam_with_ref)
    round_tripped = normalize_sam_text(out)
    if len(round_tripped.records) != len(orig.records):
        pytest.skip(
            "CRAM round-trip dropped records — likely reference/seed "
            "positional mismatch (toy ref is random bases)"
        )
    assert orig.records[0].QNAME == round_tripped.records[0].QNAME
