"""
Strategy Router: maps transform names to Hypothesis @composite strategies.

This is the bridge between Phase B's MR output (transform name strings)
and Phase C's Hypothesis-driven test generation. The orchestrator uses
this map to look up the right strategy for each MR.

For transforms with no dedicated strategy (or when Hypothesis is not
desired), the orchestrator falls back to the static seed loop.

A few transforms (currently: `sut_write_roundtrip`) apply to both VCF
and SAM seeds — for those, the map is format-scoped: `(name, fmt)`
selects the right seed corpus. Everything else stays single-scope.
"""

from __future__ import annotations

from typing import Callable, Optional

from .seeds import SeedCorpus

# Lazy import to avoid circular dependencies — strategies reference SeedCorpus
# which references config which references project root.
_STRATEGY_MAP: Optional[dict[str, Callable]] = None
_FORMAT_SCOPED_MAP: Optional[dict[tuple[str, str], Callable]] = None


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
        st_sut_write_roundtrip as st_sut_write_roundtrip_vcf,
        st_query_method_roundtrip as st_query_method_roundtrip_vcf,
    )
    from .sam_strategies import (
        st_permute_optional_tags,
        st_reorder_header,
        st_cigar_split_merge,
        st_toggle_clipping,
        st_sut_write_roundtrip as st_sut_write_roundtrip_sam,
        st_query_method_roundtrip as st_query_method_roundtrip_sam,
    )
    from .malformed_strategies import (
        st_violate_info_number_a_cardinality,
        st_violate_required_fixed_columns,
        st_violate_fileformat_first_line,
        st_violate_gt_index_bounds,
        st_violate_cigar_seq_length,
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

        # Generic SUT write-roundtrip (Chen et al. 2018 §3.2). Default
        # scope is VCF; the SAM variant is registered in the
        # format-scoped map below. The orchestrator picks VCF or SAM
        # at get_strategy() time based on the MR's primary format.
        "sut_write_roundtrip": st_sut_write_roundtrip_vcf,

        # Rank 5 — query_method_roundtrip (API-query MRs).
        # MR-Scout (Xu et al., TOSEM 2024). Default VCF scope; SAM
        # variant registered in the format-scoped map below.
        "query_method_roundtrip": st_query_method_roundtrip_vcf,

        # SAM transforms
        "permute_optional_tag_fields": st_permute_optional_tags,
        "reorder_header_records": st_reorder_header,
        "split_or_merge_adjacent_cigar_ops": st_cigar_split_merge,
        "toggle_cigar_hard_soft_clipping": st_toggle_clipping,

        # Rank 3 malformed-input mutators (REJECTION_INVARIANCE behavior).
        # Paired with the error-consensus oracle so voters tag
        # accept / reject / crash / silent_skip instead of deep_equal.
        "violate_info_number_a_cardinality": st_violate_info_number_a_cardinality,
        "violate_required_fixed_columns":    st_violate_required_fixed_columns,
        "violate_fileformat_first_line":     st_violate_fileformat_first_line,
        "violate_gt_index_bounds":           st_violate_gt_index_bounds,
        "violate_cigar_seq_length":          st_violate_cigar_seq_length,
    }


def _build_format_scoped_map() -> dict[tuple[str, str], Callable]:
    """Build the (name, fmt) -> strategy-factory map for format-scoped transforms.

    Only transforms that span multiple formats need to be registered
    here; the default single-scope map is consulted first.
    """
    from .vcf_strategies import (
        st_sut_write_roundtrip as st_sut_write_roundtrip_vcf,
        st_query_method_roundtrip as st_query_method_roundtrip_vcf,
    )
    from .sam_strategies import (
        st_sut_write_roundtrip as st_sut_write_roundtrip_sam,
        st_query_method_roundtrip as st_query_method_roundtrip_sam,
    )
    return {
        ("sut_write_roundtrip", "VCF"): st_sut_write_roundtrip_vcf,
        ("sut_write_roundtrip", "SAM"): st_sut_write_roundtrip_sam,
        ("query_method_roundtrip", "VCF"): st_query_method_roundtrip_vcf,
        ("query_method_roundtrip", "SAM"): st_query_method_roundtrip_sam,
    }


def get_strategy(
    transform_name: str,
    fmt: Optional[str] = None,
) -> Optional[Callable]:
    """
    Get the Hypothesis strategy factory for a transform name.

    Args:
        transform_name: Transform identifier from TRANSFORM_REGISTRY.
        fmt: Optional format ("VCF" or "SAM"). For format-scoped
             transforms (currently `sut_write_roundtrip`), this selects
             the VCF or SAM variant. Ignored for single-scope transforms.

    Returns a callable that accepts (corpus: SeedCorpus) and returns
    a Hypothesis SearchStrategy, or None if no strategy is registered.
    """
    global _STRATEGY_MAP, _FORMAT_SCOPED_MAP
    if _STRATEGY_MAP is None:
        _STRATEGY_MAP = _build_map()
    if _FORMAT_SCOPED_MAP is None:
        _FORMAT_SCOPED_MAP = _build_format_scoped_map()
    if fmt is not None:
        scoped = _FORMAT_SCOPED_MAP.get((transform_name, fmt.upper()))
        if scoped is not None:
            return scoped
    return _STRATEGY_MAP.get(transform_name)


def has_strategy(
    transform_name: str,
    fmt: Optional[str] = None,
) -> bool:
    """Check whether a Hypothesis strategy exists for this transform."""
    return get_strategy(transform_name, fmt) is not None
