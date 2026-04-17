"""
Strategy Router: maps transform names to Hypothesis @composite strategies.

This is the bridge between Phase B's MR output (transform name strings)
and Phase C's Hypothesis-driven test generation. The orchestrator uses
this map to look up the right strategy for each MR.

For transforms with no dedicated strategy (or when Hypothesis is not
desired), the orchestrator falls back to the static seed loop.
"""

from __future__ import annotations

from typing import Callable, Optional

from .seeds import SeedCorpus

# Lazy import to avoid circular dependencies — strategies reference SeedCorpus
# which references config which references project root.
_STRATEGY_MAP: Optional[dict[str, Callable]] = None


def _build_map() -> dict[str, Callable]:
    """Build the transform-name -> strategy-factory map on first access."""
    from .vcf_strategies import (
        st_shuffle_meta_lines,
        st_permute_structured_kv,
        st_shuffle_info_kv,
        st_permute_sample_columns,
        st_alt_permutation,
        st_inject_missing_values,
        st_trim_common_affixes,
        st_left_align_indel,
        st_split_multi_allelic,
        st_vcf_bcf_round_trip,
        st_permute_bcf_header_dictionary,
        st_permute_csq_annotations,
    )
    from .sam_strategies import (
        st_permute_optional_tags,
        st_reorder_header,
        st_cigar_split_merge,
        st_toggle_clipping,
    )

    return {
        # VCF transforms
        "shuffle_meta_lines": st_shuffle_meta_lines,
        "permute_structured_kv_order": st_permute_structured_kv,
        "shuffle_info_field_kv": st_shuffle_info_kv,
        "permute_sample_columns": st_permute_sample_columns,
        "inject_equivalent_missing_values": st_inject_missing_values,

        # VCF compound group — all 4 members map to the compound strategy
        "choose_permutation": st_alt_permutation,
        "permute_ALT": st_alt_permutation,
        "remap_GT": st_alt_permutation,
        "permute_Number_A_R_fields": st_alt_permutation,

        # VCF variant normalization (Tan 2015)
        "trim_common_affixes": st_trim_common_affixes,
        "left_align_indel": st_left_align_indel,
        "split_multi_allelic": st_split_multi_allelic,

        # VCF BCF codec transforms (VCF v4.5 §6)
        "vcf_bcf_round_trip": st_vcf_bcf_round_trip,
        "permute_bcf_header_dictionary": st_permute_bcf_header_dictionary,

        # VCF CSQ/ANN annotation ordering (VEP/SnpEff)
        "permute_csq_annotations": st_permute_csq_annotations,

        # SAM transforms
        "permute_optional_tag_fields": st_permute_optional_tags,
        "reorder_header_records": st_reorder_header,
        "split_or_merge_adjacent_cigar_ops": st_cigar_split_merge,
        "toggle_cigar_hard_soft_clipping": st_toggle_clipping,
    }


def get_strategy(transform_name: str) -> Optional[Callable]:
    """
    Get the Hypothesis strategy factory for a transform name.

    Returns a callable that accepts (corpus: SeedCorpus) and returns
    a Hypothesis SearchStrategy, or None if no strategy is registered.
    """
    global _STRATEGY_MAP
    if _STRATEGY_MAP is None:
        _STRATEGY_MAP = _build_map()
    return _STRATEGY_MAP.get(transform_name)


def has_strategy(transform_name: str) -> bool:
    """Check whether a Hypothesis strategy exists for this transform."""
    return get_strategy(transform_name) is not None
