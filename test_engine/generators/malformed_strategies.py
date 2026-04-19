"""
Hypothesis strategies for Rank 3 malformed-input transforms.

Each strategy samples a seed from the existing corpus, checks the mutator's
structural precondition (biallelic record with Number=A, ≥2 meta lines, etc.)
via `assume()`, and returns the `{transform, seed_path, lines, rng_seed}`
tuple consumed by `_run_single_test`.
"""

from __future__ import annotations

from hypothesis import strategies as st, assume
from hypothesis.strategies import composite

from .seeds import SeedCorpus


# ---------------------------------------------------------------------------
# VCF mutator strategies
# ---------------------------------------------------------------------------


@composite
def st_violate_info_number_a_cardinality(draw, corpus: SeedCorpus):
    """Precondition: header declares at least one Number=A INFO key AND
    at least one biallelic data row uses that key."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)

    info_a_keys: list[str] = []
    for l in lines:
        s = l.rstrip("\r\n")
        if s.startswith("##INFO=<") and "Number=A" in s:
            i = s.find("ID=")
            if i >= 0:
                after = s[i + 3:]
                end = min(
                    (p for p in (after.find(","), after.find(">")) if p >= 0),
                    default=len(after),
                )
                info_a_keys.append(after[:end])
    assume(len(info_a_keys) > 0)

    # At least one biallelic record using one of the Number=A keys.
    have_target = False
    for l in lines:
        s = l.rstrip("\r\n")
        if s.startswith("#") or "\t" not in s:
            continue
        cols = s.split("\t")
        if len(cols) < 8:
            continue
        if "," in cols[4] or cols[4] == ".":
            continue
        info = cols[7]
        if info == ".":
            continue
        if any(f"{k}=" in info for k in info_a_keys):
            have_target = True
            break
    assume(have_target)

    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {
        "transform": "violate_info_number_a_cardinality",
        "seed_path": seed_path,
        "lines": lines,
        "rng_seed": rng_seed,
    }


@composite
def st_violate_required_fixed_columns(draw, corpus: SeedCorpus):
    """Precondition: at least one data row with the 8 mandatory columns."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    has_row = any(
        (not l.startswith("#")) and "\t" in l and len(l.split("\t")) >= 8
        for l in lines
    )
    assume(has_row)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {
        "transform": "violate_required_fixed_columns",
        "seed_path": seed_path,
        "lines": lines,
        "rng_seed": rng_seed,
    }


@composite
def st_violate_fileformat_first_line(draw, corpus: SeedCorpus):
    """Precondition: ≥ 2 `##` meta lines so the swap has something to
    swap with."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    meta_count = sum(1 for l in lines if l.startswith("##"))
    assume(meta_count >= 2)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {
        "transform": "violate_fileformat_first_line",
        "seed_path": seed_path,
        "lines": lines,
        "rng_seed": rng_seed,
    }


@composite
def st_violate_gt_index_bounds(draw, corpus: SeedCorpus):
    """Precondition: biallelic record whose FORMAT includes GT and has
    at least one sample column."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)

    have_target = False
    for l in lines:
        s = l.rstrip("\r\n")
        if s.startswith("#") or "\t" not in s:
            continue
        cols = s.split("\t")
        if len(cols) < 10:
            continue
        if "," in cols[4] or cols[4] == ".":
            continue
        fmt_keys = cols[8].split(":")
        if "GT" in fmt_keys:
            have_target = True
            break
    assume(have_target)

    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {
        "transform": "violate_gt_index_bounds",
        "seed_path": seed_path,
        "lines": lines,
        "rng_seed": rng_seed,
    }


# ---------------------------------------------------------------------------
# SAM mutator strategies
# ---------------------------------------------------------------------------


@composite
def st_violate_cigar_seq_length(draw, corpus: SeedCorpus):
    """Precondition: alignment with CIGAR != '*' and SEQ != '*'."""
    seed_path = draw(st.sampled_from(corpus.sam_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    have_target = False
    for l in lines:
        s = l.rstrip("\r\n")
        if s.startswith("@") or "\t" not in s:
            continue
        cols = s.split("\t")
        if len(cols) < 11:
            continue
        if cols[5] == "*" or cols[9] == "*":
            continue
        have_target = True
        break
    assume(have_target)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {
        "transform": "violate_cigar_seq_length",
        "seed_path": seed_path,
        "lines": lines,
        "rng_seed": rng_seed,
    }
