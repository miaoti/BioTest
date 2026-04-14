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
