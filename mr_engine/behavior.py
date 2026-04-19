"""
B3: Behavior Target Classification

Defines the six categories of metamorphic relation targets and maps each
to its relevant atomic transforms and system prompt descriptions.
"""

from __future__ import annotations

from enum import Enum


class BehaviorTarget(str, Enum):
    """The seven target fault-mode categories for MR mining."""

    ORDERING_INVARIANCE = "ordering_invariance"
    SEMANTICS_PRESERVING_PERMUTATION = "semantics_preserving_permutation"
    NORMALIZATION_INVARIANCE = "normalization_invariance"
    REJECTION_INVARIANCE = "rejection_invariance"
    COORDINATE_INDEXING_INVARIANCE = "coordinate_indexing_invariance"
    ROUND_TRIP_INVARIANCE = "round_trip_invariance"
    # Rank 5 lever — API-level MRs: compare scalar results of public query
    # methods on the parsed object across x and T(x). Covers library
    # query-API code paths that file→file MRs structurally cannot reach.
    # Grounded in Chen-Kuo-Liu-Tse 2018 §3.2 (API MRs) + MR-Scout
    # (Xu et al., TOSEM 2024, arXiv:2304.07548).
    API_QUERY_INVARIANCE = "api_query_invariance"


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
        # Spec-rule-targeted malformed-input transforms (Rank 3 lever).
        # Each mutates a valid seed to violate one CRITICAL spec rule.
        # Paired with the error-consensus oracle, they hit parser
        # rejection branches that semantics-preserving MRs never reach.
        # Grounded in Gmutator (Donaldson et al., TOSEM 2025).
        "violate_info_number_a_cardinality",
        "violate_required_fixed_columns",
        "violate_fileformat_first_line",
        "violate_gt_index_bounds",
        "violate_cigar_seq_length",
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
    BehaviorTarget.API_QUERY_INVARIANCE: [
        # Rank 5 — query-method MRs. A single runtime-dispatched transform
        # (query_method_roundtrip) that invokes the primary SUT's public
        # query methods on x and T(x) and compares scalar outputs.
        # Reflection-based; which methods exist is discovered per SUT at
        # mine time (see mr_engine/agent/engine.py) — no hardcoded list.
        # Grounded in MR-Scout (Xu et al., TOSEM 2024, arXiv:2304.07548)
        # and Chen-Kuo-Liu-Tse (ACM CSUR 2018) §3.2.
        "query_method_roundtrip",
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
        "  - SAM TAG:VALUE pair order WITHIN a single header line — "
        "@HD, @SQ, @RG, @PG records have no spec-imposed order among "
        "their subtags (SAMv1 §1.3). Use shuffle_hd_subtags, "
        "shuffle_sq_record_subtags, shuffle_rg_record_subtags, "
        "shuffle_pg_record_subtags.\n"
        "  - SAM @CO comment-line order: @CO lines are free-text "
        "comments with no ordering semantics. Use shuffle_co_comments.\n"
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
        "parser MUST reject (raise a validation error, crash, or refuse to emit "
        "the record) these inputs; silent acceptance or silent record-drop is "
        "a conformance bug.\n\n"
        "Concrete mutators available in the transform menu:\n"
        "  - violate_info_number_a_cardinality: append extra value to an "
        "INFO Number=A field (biallelic record — v4.5 §1.6.2).\n"
        "  - violate_required_fixed_columns: drop a mandatory VCF column "
        "(v4.5 §1.6.1 requires first 8 columns).\n"
        "  - violate_fileformat_first_line: move `##fileformat` away from "
        "line 1 (v4.5 §1.2).\n"
        "  - violate_gt_index_bounds: set GT index > len(ALT) (v4.5 §1.6.3).\n"
        "  - violate_cigar_seq_length: grow CIGAR M-count without "
        "extending SEQ (SAMv1 §1.4.6).\n"
        "  - violate_tlen_sign_consistency: flip TLEN sign so both "
        "reads of a paired template share a sign, breaking the "
        "opposite-signed pairing rule (SAMv1 §1.4).\n"
        "  - violate_optional_tag_type_character: replace the type char "
        "of an optional tag with an illegal letter outside `AifZHB` "
        "(SAMtags §2.1).\n"
        "  - violate_flag_bit_exclusivity: set FLAG 0x4 (segment "
        "unmapped) on a record that still carries a real RNAME and "
        "POS — spec-forbidden mapped/unmapped contradiction (SAMv1 §1.4.1).\n"
        "Each mutator targets ONE specific spec rule. Pair with the "
        "error-consensus oracle so voters tag `ACCEPT / REJECT / CRASH / "
        "SILENT_SKIP` instead of comparing canonical JSON."
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
        "  - SAM⇄BAM codec round-trip (SAMv1 §4). BAM is the binary "
        "equivalent of SAM. Use sam_bam_round_trip on any valid SAM; the "
        "transform shells out to `samtools view -b | samtools view -h`, so "
        "the samtools_available runtime precondition must hold.\n"
        "  - SAM⇄CRAM codec round-trip. CRAM is reference-compressed (loses "
        "=/X distinction by default per Bonfield CRAM 3.1 2022; the "
        "canonical normalizer accounts for this). Use sam_cram_round_trip; "
        "requires samtools_available + cram_reference_available.\n"
        "  - Missing-value round-trip (equivalent FORMAT fields, deprecated "
        "tags), handled by inject_equivalent_missing_values.\n"
        "  - CIGAR Hard/Soft clipping toggle (SAM).\n"
        "Pick transforms only when the SUT supports the target encoding."
    ),
    BehaviorTarget.API_QUERY_INVARIANCE: (
        "API QUERY INVARIANCE: Parsing-equivalent inputs must yield identical "
        "results from the parser's PUBLIC QUERY METHODS. For a semantics-"
        "preserving transform T, the MR is:\n"
        "    P(parse(x)) == P(parse(T(x)))\n"
        "where P is any public scalar-returning query method on the parsed "
        "record — e.g. `vc.isStructural()`, `vc.getNAlleles()`, "
        "`rec.isProperPair()`. The framework DISCOVERS which methods each "
        "primary SUT exposes via runtime reflection (see "
        "`mr_engine/agent/engine.py::mine_mrs`), so method names that appear "
        "in the prompt are actually available. This brings library-API code "
        "paths into scope that `parse → canonical JSON` oracles miss.\n\n"
        "Use the single runtime-dispatched transform `query_method_roundtrip`; "
        "pair it with any semantics-preserving transform (shuffle_meta_lines, "
        "permute_optional_tag_fields, trim_common_affixes, etc.) so the "
        "outer transform changes x but the query methods must still return "
        "the same scalar values.\n\n"
        "Reference: Chen, Kuo, Liu, Tse (ACM CSUR 2018) §3.2 API MRs; "
        "MR-Scout (Xu, Terragni, Zhu, Wu, Cheung — TOSEM 2024, arXiv:2304.07548) "
        "mined 11,000 query-method MRs from 701 OSS projects and reports "
        "+13.5 pp line coverage; MeMo (Blasi et al., JSS 2021) auto-mines "
        "equivalence MRs from Javadoc."
    ),
}


def get_system_prompt_fragment(target: BehaviorTarget) -> str:
    """Return the human-readable prompt description for a behavior target."""
    return _BEHAVIOR_DESCRIPTIONS[target]


def get_all_targets() -> list[BehaviorTarget]:
    """Return all behavior targets."""
    return list(BehaviorTarget)
