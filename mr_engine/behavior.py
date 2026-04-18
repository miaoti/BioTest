"""
B3: Behavior Target Classification

Defines the six categories of metamorphic relation targets and maps each
to its relevant atomic transforms and system prompt descriptions.
"""

from __future__ import annotations

from enum import Enum


class BehaviorTarget(str, Enum):
    """The six target fault-mode categories for MR mining."""

    ORDERING_INVARIANCE = "ordering_invariance"
    SEMANTICS_PRESERVING_PERMUTATION = "semantics_preserving_permutation"
    NORMALIZATION_INVARIANCE = "normalization_invariance"
    REJECTION_INVARIANCE = "rejection_invariance"
    COORDINATE_INDEXING_INVARIANCE = "coordinate_indexing_invariance"
    ROUND_TRIP_INVARIANCE = "round_trip_invariance"


# Maps each behavior target to the atomic transforms most likely relevant.
# This helps the agent focus its search, but it is NOT restrictive — the
# agent may use any whitelisted transform.
BEHAVIOR_TRANSFORM_HINTS: dict[BehaviorTarget, list[str]] = {
    BehaviorTarget.ORDERING_INVARIANCE: [
        "shuffle_meta_lines",
        "permute_structured_kv_order",
        "permute_sample_columns",
        "shuffle_info_field_kv",
        "permute_optional_tag_fields",
        "reorder_header_records",
        # VCF BCF dictionary order (VCF v4.5 §6.2.1)
        "permute_bcf_header_dictionary",
        # VEP/SnpEff annotation record order (Cingolani 2012)
        "permute_csq_annotations",
    ],
    BehaviorTarget.SEMANTICS_PRESERVING_PERMUTATION: [
        "choose_permutation",
        "permute_ALT",
        "remap_GT",
        "permute_Number_A_R_fields",
    ],
    BehaviorTarget.NORMALIZATION_INVARIANCE: [
        "split_or_merge_adjacent_cigar_ops",
        "toggle_cigar_hard_soft_clipping",
        # VCF variant normalization (Tan et al. 2015)
        "trim_common_affixes",
        "left_align_indel",
        # Multi-allelic split per bcftools norm (Danecek & McCarthy 2017)
        "split_multi_allelic",
    ],
    BehaviorTarget.REJECTION_INVARIANCE: [
        # Rejection tests inject invalid data — handled by dedicated
        # transforms or inline logic; hints are intentionally sparse.
    ],
    BehaviorTarget.COORDINATE_INDEXING_INVARIANCE: [
        # Coordinate/indexing transforms are domain-specific and may
        # be composed from existing transforms. Variant left-alignment
        # is a coordinate adjustment bounded by the canonical variant
        # equivalence class.
        "left_align_indel",
        "trim_common_affixes",
    ],
    BehaviorTarget.ROUND_TRIP_INVARIANCE: [
        "inject_equivalent_missing_values",
        "toggle_cigar_hard_soft_clipping",
        # VCF⇄BCF codec round-trip (VCF v4.5 §6)
        "vcf_bcf_round_trip",
        # SUT-agnostic writer round-trip (Chen et al. 2018 §3.2). One
        # transform, runtime-dispatched to whichever SUT is primary.
        # Replaces the old htsjdk_write_roundtrip / pysam_vcf_write_roundtrip
        # pair. See mr_engine/transforms/vcf.py::sut_write_roundtrip.
        "sut_write_roundtrip",
    ],
}

# Human-readable descriptions for each behavior target, injected into the
# agent's system prompt to guide its spec queries.
_BEHAVIOR_DESCRIPTIONS: dict[BehaviorTarget, str] = {
    BehaviorTarget.ORDERING_INVARIANCE: (
        "ORDERING INVARIANCE: Spec rules that allow elements to appear in any "
        "order without changing biological semantics. Examples:\n"
        "  - VCF ##meta-information lines (v4.5 §1.2: any order except "
        "##fileformat first).\n"
        "  - Key-value pairs inside ##INFO=<...>, ##FORMAT=<...> structured "
        "lines (v4.5 §1.6.2).\n"
        "  - BCF dictionary order: ##contig, ##INFO, ##FORMAT, ##FILTER "
        "entries can be declared in any order; BCF codec re-indexes them "
        "(VCF v4.5 §6.2.1).\n"
        "  - CSQ / ANN annotation RECORD order (comma-separated). Per VEP "
        "docs, record order is not significant. NOTE: never permute the "
        "pipe-delimited SUB-FIELDS inside a record; those are positional.\n"
        "  - SAM optional tag order (SAMv1 §1.5); SAM @SQ / @RG header "
        "order (@HD must stay first).\n"
        "Pick a transform whose preconditions match the seed (e.g. "
        "permute_csq_annotations requires CSQ/ANN in INFO)."
    ),
    BehaviorTarget.SEMANTICS_PRESERVING_PERMUTATION: (
        "SEMANTICS-PRESERVING PERMUTATION: The ALT alleles in a VCF record can be "
        "listed in any order, as long as all dependent fields (GT, Number=A, Number=R, "
        "Number=G) are consistently remapped. Find spec rules that define the "
        "relationship between ALT ordering and these dependent fields. The REF allele "
        "(index 0) must never change."
    ),
    BehaviorTarget.NORMALIZATION_INVARIANCE: (
        "NORMALIZATION INVARIANCE: Canonical representations — multiple encodings "
        "of the same biological variant. Per Tan, Abecasis, Kang (2015) 'Unified "
        "representation of genetic variants', canonical form is parsimonious "
        "(no shared prefix/suffix) and left-aligned. Examples:\n"
        "  - Common-affix trimming: REF=AA,ALT=AC at POS=100 is equivalent to "
        "REF=A,ALT=C at POS=101 — two parsers that both normalize must accept "
        "either form as the same variant.\n"
        "  - Left alignment of indels in homopolymer runs (Tan 2015 §2.1).\n"
        "  - Multi-allelic split/join per `bcftools norm --multiallelics` "
        "(Danecek & McCarthy 2017): `chr1 100 A T,C` ⇌ two rows at the same "
        "position with synchronized Number=A/R arrays and remapped GT.\n"
        "  - CIGAR op split/merge (SAM-only): `10M` ⇌ `4M6M`.\n"
        "  - Hard/Soft clipping equivalence in CIGAR.\n"
        "Pick the transform whose preconditions match the seed; not every MR "
        "in this category applies to every file."
    ),
    BehaviorTarget.REJECTION_INVARIANCE: (
        "REJECTION INVARIANCE: The spec explicitly forbids certain patterns using "
        "MUST NOT or SHALL NOT. Find rules that define what constitutes an invalid "
        "record — illegal characters, zero-length fields, missing mandatory fields, "
        "or constraint violations. These define negative test cases: a compliant "
        "parser must reject or flag these inputs."
    ),
    BehaviorTarget.COORDINATE_INDEXING_INVARIANCE: (
        "COORDINATE & INDEXING INVARIANCE: Genomic formats use 1-based coordinates "
        "(VCF POS, SAM POS) while many programming APIs use 0-based. Find spec rules "
        "about coordinate systems, half-open vs closed intervals, and how positions "
        "relate to sequence indices. Focus on boundary conditions and off-by-one risks."
    ),
    BehaviorTarget.ROUND_TRIP_INVARIANCE: (
        "ROUND-TRIP INVARIANCE: Parse → serialize → parse must yield the same "
        "canonical content. Examples:\n"
        "  - VCF⇄BCF codec round-trip (VCF v4.5 §6 BCF specification). BCF is "
        "the binary equivalent of VCF; identical information content. A "
        "parser that loses or reorders data through the binary hop exposes "
        "a codec bug. Use vcf_bcf_round_trip on any valid VCF; the SUT "
        "chain must include a BCF-capable codec (pysam/htsjdk).\n"
        "  - Missing-value round-trip (equivalent FORMAT fields, deprecated "
        "tags), handled by inject_equivalent_missing_values.\n"
        "  - CIGAR Hard/Soft clipping toggle (SAM).\n"
        "Pick transforms only when the SUT supports the target encoding."
    ),
}


def get_system_prompt_fragment(target: BehaviorTarget) -> str:
    """Return the human-readable prompt description for a behavior target."""
    return _BEHAVIOR_DESCRIPTIONS[target]


def get_all_targets() -> list[BehaviorTarget]:
    """Return all behavior targets."""
    return list(BehaviorTarget)
