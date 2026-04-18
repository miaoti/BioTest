"""
Hypothesis strategies for VCF transforms.

Each strategy draws a seed file and generates appropriate parameters
for one transform, returning a dict of parameters suitable for the
dispatch wrapper.
"""

from __future__ import annotations

from pathlib import Path

from hypothesis import strategies as st, assume
from hypothesis.strategies import composite

from .seeds import SeedCorpus


@composite
def st_shuffle_meta_lines(draw, corpus: SeedCorpus):
    """Strategy for shuffle_meta_lines: whole file + RNG seed."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    meta_count = sum(1 for l in lines if l.startswith("##"))
    assume(meta_count >= 2)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_meta_lines", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_permute_structured_kv(draw, corpus: SeedCorpus):
    """Strategy for permute_structured_kv_order: structured meta lines."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    structured = [l for l in lines if l.startswith("##") and "=<" in l]
    assume(len(structured) >= 1)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "permute_structured_kv_order", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_shuffle_info_kv(draw, corpus: SeedCorpus):
    """Strategy for shuffle_info_field_kv: data lines with multi-field INFO."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    data_lines = [l for l in lines if not l.startswith("#") and "\t" in l]
    has_multi_info = any(";" in l.split("\t")[7] for l in data_lines if len(l.split("\t")) > 7)
    assume(has_multi_info)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "shuffle_info_field_kv", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_permute_sample_columns(draw, corpus: SeedCorpus):
    """Strategy for permute_sample_columns: multi-sample VCF."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    header = [l for l in lines if l.startswith("#CHROM")]
    assume(len(header) > 0)
    n_samples = len(header[0].split("\t")) - 9
    assume(n_samples >= 2)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "permute_sample_columns", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_alt_permutation(draw, corpus: SeedCorpus):
    """Strategy for compound ALT permutation: multi-ALT records."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    data_lines = [l for l in lines if not l.startswith("#") and "\t" in l]
    has_multi_alt = any("," in l.split("\t")[4] for l in data_lines if len(l.split("\t")) > 4)
    assume(has_multi_alt)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "alt_permutation_compound", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_inject_missing_values(draw, corpus: SeedCorpus):
    """Strategy for inject_equivalent_missing_values: records with FORMAT."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    data_lines = [l for l in lines if not l.startswith("#") and "\t" in l]
    has_format = any(len(l.split("\t")) >= 10 for l in data_lines)
    assume(has_format)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "inject_equivalent_missing_values", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


# ---------------------------------------------------------------------------
# Variant normalization strategies (Tan 2015)
# ---------------------------------------------------------------------------

def _biallelic_records(lines: list[str]) -> list[list[str]]:
    out = []
    for l in lines:
        s = l.rstrip("\n\r")
        if s.startswith("#") or "\t" not in s:
            continue
        cols = s.split("\t")
        if len(cols) >= 5 and "," not in cols[4]:
            out.append(cols)
    return out


@composite
def st_trim_common_affixes(draw, corpus: SeedCorpus):
    """Precondition: biallelic record with shared prefix or suffix base."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    bi = _biallelic_records(lines)
    has_trimmable = any(
        (len(c[3]) >= 2 or len(c[4]) >= 2)
        and (c[3][0] == c[4][0] or c[3][-1] == c[4][-1])
        for c in bi
    )
    assume(has_trimmable)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "trim_common_affixes", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_left_align_indel(draw, corpus: SeedCorpus):
    """Precondition: biallelic indel with homopolymer REF and POS>=2."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    bi = _biallelic_records(lines)
    has_homopoly_indel = any(
        len(c[3]) != len(c[4])
        and len(c[3]) >= 2
        and c[3][0] == c[3][-1]
        and c[1].isdigit() and int(c[1]) >= 2
        for c in bi
    )
    assume(has_homopoly_indel)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "left_align_indel", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_split_multi_allelic(draw, corpus: SeedCorpus):
    """Precondition: at least one multi-ALT record (alt_count >= 2)."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    data_lines = [l for l in lines if not l.startswith("#") and "\t" in l]
    has_multi_alt = any(
        "," in l.split("\t")[4] for l in data_lines if len(l.split("\t")) > 4
    )
    assume(has_multi_alt)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "split_multi_allelic", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


# ---------------------------------------------------------------------------
# BCF codec strategies (VCF v4.5 §6)
# ---------------------------------------------------------------------------

@composite
def st_vcf_bcf_round_trip(draw, corpus: SeedCorpus):
    """Precondition: any valid VCF (codec availability checked at runtime)."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(any(l.startswith("##fileformat=VCF") for l in lines))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "vcf_bcf_round_trip", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


@composite
def st_permute_bcf_header_dictionary(draw, corpus: SeedCorpus):
    """Precondition: header has 2+ ##INFO or ##FORMAT or ##contig entries."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    n_info = sum(1 for l in lines if l.startswith("##INFO="))
    n_fmt = sum(1 for l in lines if l.startswith("##FORMAT="))
    n_contig = sum(1 for l in lines if l.startswith("##contig="))
    assume(n_info >= 2 or n_fmt >= 2 or n_contig >= 2)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "permute_bcf_header_dictionary",
            "seed_path": seed_path, "lines": lines, "rng_seed": rng_seed}


# ---------------------------------------------------------------------------
# SUT-agnostic write-roundtrip strategy
# ---------------------------------------------------------------------------

@composite
def st_sut_write_roundtrip(draw, corpus: SeedCorpus):
    """Precondition: any valid VCF.

    The ACTUAL SUT that performs the write is chosen by the orchestrator
    (from `primary_target`) and injected into dispatch as `runner_hook`,
    so the strategy itself stays SUT-agnostic.
    """
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    assume(any(l.startswith("##fileformat=VCF") for l in lines))
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "sut_write_roundtrip", "seed_path": seed_path,
            "lines": lines, "rng_seed": rng_seed}


# ---------------------------------------------------------------------------
# CSQ/ANN annotation ordering strategy
# ---------------------------------------------------------------------------

@composite
def st_permute_csq_annotations(draw, corpus: SeedCorpus):
    """Precondition: header declares CSQ or ANN AND at least one data line
    has a multi-record CSQ/ANN value (comma in the CSQ/ANN value)."""
    seed_path = draw(st.sampled_from(corpus.vcf_seeds))
    lines = SeedCorpus.read_lines(seed_path)
    has_csq_hdr = any(l.startswith("##INFO=<ID=CSQ") for l in lines)
    has_ann_hdr = any(l.startswith("##INFO=<ID=ANN") for l in lines)
    assume(has_csq_hdr or has_ann_hdr)
    keys = ("CSQ=", "ANN=")
    multi_record = False
    for l in lines:
        s = l.rstrip("\n\r")
        if s.startswith("#") or "\t" not in s:
            continue
        cols = s.split("\t")
        if len(cols) < 8:
            continue
        info = cols[7]
        for k in keys:
            idx = info.find(k)
            if idx == -1:
                continue
            end = info.find(";", idx)
            val = info[idx + len(k): end if end != -1 else None]
            if "," in val:
                multi_record = True
                break
        if multi_record:
            break
    assume(multi_record)
    rng_seed = draw(st.integers(0, 2**32 - 1))
    return {"transform": "permute_csq_annotations",
            "seed_path": seed_path, "lines": lines, "rng_seed": rng_seed}
