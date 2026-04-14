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
    ],
    BehaviorTarget.REJECTION_INVARIANCE: [
        # Rejection tests inject invalid data — handled by dedicated
        # transforms or inline logic; hints are intentionally sparse.
    ],
    BehaviorTarget.COORDINATE_INDEXING_INVARIANCE: [
        # Coordinate/indexing transforms are domain-specific and may
        # be composed from existing transforms.
    ],
    BehaviorTarget.ROUND_TRIP_INVARIANCE: [
        "inject_equivalent_missing_values",
        "toggle_cigar_hard_soft_clipping",
    ],
}

# Human-readable descriptions for each behavior target, injected into the
# agent's system prompt to guide its spec queries.
_BEHAVIOR_DESCRIPTIONS: dict[BehaviorTarget, str] = {
    BehaviorTarget.ORDERING_INVARIANCE: (
        "ORDERING INVARIANCE: The spec allows certain elements to appear in any order. "
        "Find rules where reordering header lines, key-value pairs, INFO fields, "
        "optional tags, or sample columns must not change the biological semantics. "
        "Focus on normative statements about order-independence."
    ),
    BehaviorTarget.SEMANTICS_PRESERVING_PERMUTATION: (
        "SEMANTICS-PRESERVING PERMUTATION: The ALT alleles in a VCF record can be "
        "listed in any order, as long as all dependent fields (GT, Number=A, Number=R, "
        "Number=G) are consistently remapped. Find spec rules that define the "
        "relationship between ALT ordering and these dependent fields. The REF allele "
        "(index 0) must never change."
    ),
    BehaviorTarget.NORMALIZATION_INVARIANCE: (
        "NORMALIZATION INVARIANCE: Certain representations are semantically equivalent "
        "under normalization. For example, CIGAR string '10M' is equivalent to '4M6M' "
        "(adjacent identical operations can be split or merged). Find spec rules about "
        "CIGAR operation semantics, Hard/Soft clipping equivalence, and other "
        "representations that parsers must treat identically."
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
        "ROUND-TRIP INVARIANCE: Parsing a file and re-serializing it should produce "
        "semantically equivalent output. Find rules about equivalent representations "
        "(e.g., missing values, deprecated tags, optional fields with defaults) that "
        "a compliant implementation must preserve through a parse-serialize cycle."
    ),
}


def get_system_prompt_fragment(target: BehaviorTarget) -> str:
    """Return the human-readable prompt description for a behavior target."""
    return _BEHAVIOR_DESCRIPTIONS[target]


def get_all_targets() -> list[BehaviorTarget]:
    """Return all behavior targets."""
    return list(BehaviorTarget)
