"""
Hypothesis strategies for SAM transforms.
"""

from __future__ import annotations

from hypothesis import strategies as st, assume
from hypothesis.strategies import composite

from .seeds import SeedCorpus


@composite
def st_permute_optional_tags(draw, corpus: SeedCorpus):
    """Strategy for permute_optional_tag_fields."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    align_lines = [l for l in lines if not l.startswith("@") and "\t" in l]
    has_tags = any(len(l.split("\t")) > 11 for l in align_lines)
    assume(has_tags)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "permute_optional_tag_fields", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_reorder_header(draw, corpus: SeedCorpus):
    """Strategy for reorder_header_records."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    header_lines = [l for l in lines if l.startswith("@")]
    sq_count = sum(1 for l in header_lines if l.startswith("@SQ"))
    assume(sq_count >= 2)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "reorder_header_records", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_cigar_split_merge(draw, corpus: SeedCorpus):
    """Strategy for split_or_merge_adjacent_cigar_ops."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    align_lines = [l for l in lines if not l.startswith("@") and "\t" in l]
    has_cigar = any(l.split("\t")[5] != "*" for l in align_lines if len(l.split("\t")) > 5)
    assume(has_cigar)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "split_or_merge_adjacent_cigar_ops", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_toggle_clipping(draw, corpus: SeedCorpus):
    """Strategy for toggle_cigar_hard_soft_clipping."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    align_lines = [l for l in lines if not l.startswith("@") and "\t" in l]
    has_clip = any(("H" in l.split("\t")[5] or "S" in l.split("\t")[5])
                   for l in align_lines if len(l.split("\t")) > 5)
    assume(has_clip)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "toggle_cigar_hard_soft_clipping", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_sut_write_roundtrip(draw, corpus: SeedCorpus):
    """SAM-flavored strategy for sut_write_roundtrip.

    Twin of the VCF-flavored strategy in vcf_strategies — the router
    picks which of the two to use based on the MR's primary format.
    The runner called from dispatch handles the actual SAM writer
    (htsjdk SAMFileWriterFactory, pysam AlignmentFile, ...).
    """
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(any(l.startswith("@HD") or l.startswith("@SQ") for l in lines))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "sut_write_roundtrip", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_query_method_roundtrip(draw, corpus: SeedCorpus):
    """SAM-flavored strategy for query_method_roundtrip (Rank 5).

    Twin of the VCF-flavored strategy in vcf_strategies. Method names
    come from the MR's `query_methods` field; the strategy just supplies
    a valid SAM seed."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(any(l.startswith("@HD") or l.startswith("@SQ") for l in lines))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "query_method_roundtrip", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


# ---------------------------------------------------------------------------
# Phase 2 — header-subtag shuffles. Each picks a seed whose header
# carries at least one line of the target record type with at least
# two subtags (so the shuffle has something to permute).
# ---------------------------------------------------------------------------


def _record_with_multiple_subtags(lines: list[str], record_type: str) -> bool:
    """True if the header contains >=1 line of `record_type` with >=2 subtags."""
    for l in lines:
        stripped = l.rstrip("\n\r")
        if not stripped.startswith(record_type):
            continue
        if len(stripped.split("\t")) >= 3:  # record-tag + at least 2 subtag fields
            return True
    return False


@composite
def st_shuffle_hd_subtags(draw, corpus: SeedCorpus):
    """Strategy for shuffle_hd_subtags — @HD must have >=2 subtags."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(_record_with_multiple_subtags(lines, "@HD"))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_hd_subtags", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_shuffle_sq_record_subtags(draw, corpus: SeedCorpus):
    """Strategy for shuffle_sq_record_subtags — >=1 @SQ line with >=2 subtags."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(_record_with_multiple_subtags(lines, "@SQ"))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_sq_record_subtags", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_shuffle_rg_record_subtags(draw, corpus: SeedCorpus):
    """Strategy for shuffle_rg_record_subtags — >=1 @RG line with >=2 subtags."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(_record_with_multiple_subtags(lines, "@RG"))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_rg_record_subtags", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_shuffle_pg_record_subtags(draw, corpus: SeedCorpus):
    """Strategy for shuffle_pg_record_subtags — >=1 @PG line with >=2 subtags."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(_record_with_multiple_subtags(lines, "@PG"))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_pg_record_subtags", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_shuffle_co_comments(draw, corpus: SeedCorpus):
    """Strategy for shuffle_co_comments — seed must have >=2 @CO lines."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    co_count = sum(1 for l in lines if l.startswith("@CO"))
    assume(co_count >= 2)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_co_comments", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


# ---------------------------------------------------------------------------
# Phase 3 — SAM↔BAM↔CRAM round-trip strategies.
# ---------------------------------------------------------------------------


@composite
def st_sam_bam_round_trip(draw, corpus: SeedCorpus):
    """Strategy for sam_bam_round_trip — any valid SAM seed with a header."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(any(l.startswith("@HD") or l.startswith("@SQ") for l in lines))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "sam_bam_round_trip", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_sam_cram_round_trip(draw, corpus: SeedCorpus):
    """Strategy for sam_cram_round_trip — seed must have @SQ lines and
    at least one SN name matching the committed toy reference."""
    from pathlib import Path as _P
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)

    # Collect @SQ SN names from the seed.
    sq_names: list[str] = []
    for ln in lines:
        if not ln.startswith("@SQ"):
            continue
        for field in ln.rstrip("\r\n").split("\t"):
            if field.startswith("SN:"):
                sq_names.append(field[3:])
                break
    assume(len(sq_names) > 0)

    # Seed must overlap the toy reference's sequence set.
    repo_root = _P(__file__).resolve().parent.parent.parent
    ref_fa = repo_root / "seeds" / "ref" / "toy.fa"
    assume(ref_fa.exists())
    ref_names: set[str] = set()
    with ref_fa.open("r", encoding="utf-8", errors="replace") as f:
        for rline in f:
            if rline.startswith(">"):
                ref_names.add(rline[1:].split()[0].strip())
    assume(any(n in ref_names for n in sq_names))

    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "sam_cram_round_trip", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}
