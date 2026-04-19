"""
Spec-rule-targeted malformed-input transforms (Rank 3 coverage lever).

The module also exposes `MALFORMED_TRANSFORM_NAMES` — the closed set of
transform names that trigger the error-consensus oracle branch in
`_run_single_test`. Keep this list in sync with the `@register_transform`
decorators below.

Each transform takes a VALID VCF or SAM seed and produces a version that
VIOLATES one specific CRITICAL spec rule. Paired with the MALFORMED_INPUT_RESILIENCE
behavior target and the `error_consensus` oracle, this lets MRs exercise parser
rejection / error-handling paths that semantics-preserving transforms never
reach.

Each mutator is deterministic given the seed RNG. Preconditions declared in
`@register_transform` gate the LLM prompt menu so the framework never proposes
a mutator that can't apply to the current seed.

Per ADR: we chose spec-rule-targeted mutation over ANTLR grammar mutation.
Leverages Phase A's already-structured spec metadata; ~400 LOC vs weeks of
grammar engineering. Grounded in:
  Gmutator (Donaldson et al., TOSEM 2025) — grammar mutation for error-path MRs.
"""

from __future__ import annotations

import random
from typing import Optional

from . import register_transform


# Registered names — used by `_run_single_test` to route these MRs
# through the error-consensus oracle instead of the normal deep_equal
# consensus. Must match the decorators below.
MALFORMED_TRANSFORM_NAMES: frozenset[str] = frozenset({
    "violate_info_number_a_cardinality",
    "violate_required_fixed_columns",
    "violate_fileformat_first_line",
    "violate_gt_index_bounds",
    "violate_cigar_seq_length",
    # Phase 2 of SAM coverage plan — 3 new SAM-side malformed mutators
    # targeting REJECTION_INVARIANCE. Each breaks exactly one CRITICAL
    # spec rule so the error-consensus oracle (accept / silent_skip /
    # reject / crash) can surface parsers that silently tolerate the
    # violation.
    "violate_tlen_sign_consistency",
    "violate_optional_tag_type_character",
    "violate_flag_bit_exclusivity",
})


# ---------------------------------------------------------------------------
# VCF mutators
# ---------------------------------------------------------------------------


@register_transform(
    "violate_info_number_a_cardinality",
    format="VCF",
    group="malformed_vcf_info",
    description=(
        "Break VCF spec rule: an INFO field declared `Number=A` MUST "
        "have exactly `len(ALT)` comma-separated values. The mutator "
        "finds a biallelic record with a Number=A INFO value and "
        "appends an extra value so cardinality becomes 2 for len(ALT)=1."
    ),
    contextual_hint=(
        "the header declares at least one `##INFO=<ID=X,Number=A,…>` "
        "field AND the data rows include at least one biallelic record "
        "that carries that INFO key."
    ),
    preconditions=("header_has_info_number_a", "alt_count=1"),
)
def violate_info_number_a_cardinality(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Append a bogus extra value to the first Number=A INFO field found
    on a biallelic record. If no such record exists, return the input
    unchanged (transform is a no-op — framework treats that as inapplicable).
    """
    info_a_keys = _collect_info_number_a_keys(seed_lines)
    if not info_a_keys:
        return list(seed_lines)

    rng = random.Random(seed)
    bogus_values = ["9", "99", "999"]

    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("#") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 8:
            out.append(line)
            continue
        alt = cols[4]
        if "," in alt or alt == "." or not alt:
            # Multi-allelic or unknown ALT — skip; precondition asked for
            # biallelic specifically.
            out.append(line)
            continue
        # biallelic: try to mutate the INFO column
        new_info = _append_extra_to_info_key(cols[7], info_a_keys, rng, bogus_values)
        if new_info is None:
            out.append(line)
            continue
        cols[7] = new_info
        new_line = "\t".join(cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True

    return out


@register_transform(
    "violate_required_fixed_columns",
    format="VCF",
    group="malformed_vcf_columns",
    description=(
        "Break VCF spec rule: data records MUST carry the 8 mandatory "
        "columns (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO). The "
        "mutator drops the QUAL column from the first data record, "
        "shortening the row to 7 columns."
    ),
    contextual_hint=(
        "the seed has at least one data row with the full 8 mandatory "
        "columns — any valid VCF will satisfy this."
    ),
    preconditions=("has_data_row",),
)
def violate_required_fixed_columns(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Drop the QUAL (column 6) from the first data row."""
    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("#") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 8:
            out.append(line)
            continue
        # Drop column index 5 (QUAL) — shortens the row by one column.
        new_cols = cols[:5] + cols[6:]
        new_line = "\t".join(new_cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True

    return out


@register_transform(
    "violate_fileformat_first_line",
    format="VCF",
    group="malformed_vcf_header",
    description=(
        "Break VCF spec rule: the `##fileformat=VCFv…` pragma MUST be "
        "the first line of the file. The mutator swaps it with a later "
        "`##` line so the first non-blank line is no longer fileformat."
    ),
    contextual_hint=(
        "the seed has at least 2 meta-information lines — any valid "
        "non-trivial VCF satisfies this."
    ),
    preconditions=("has_two_meta_lines",),
)
def violate_fileformat_first_line(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Swap ##fileformat with the next ## meta line."""
    # Find the fileformat line and the next ## line (different key).
    format_idx = -1
    other_idx = -1
    for i, line in enumerate(seed_lines):
        stripped = line.rstrip("\r\n")
        if stripped.startswith("##fileformat="):
            format_idx = i
        elif format_idx >= 0 and stripped.startswith("##"):
            other_idx = i
            break
    if format_idx < 0 or other_idx < 0:
        return list(seed_lines)

    out = list(seed_lines)
    out[format_idx], out[other_idx] = out[other_idx], out[format_idx]
    return out


@register_transform(
    "violate_gt_index_bounds",
    format="VCF",
    group="malformed_vcf_gt",
    description=(
        "Break VCF spec rule: a GT allele index MUST satisfy "
        "`0 <= idx <= len(ALT)` (0 means REF). The mutator edits the "
        "first diploid GT on a biallelic record to `2/0`, referencing "
        "an ALT allele that does not exist (only idx 0 and 1 are valid)."
    ),
    contextual_hint=(
        "the seed has at least one biallelic record with a diploid GT "
        "sample (FORMAT contains GT)."
    ),
    preconditions=("alt_count=1", "format_has_gt"),
)
def violate_gt_index_bounds(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Set the first sample's GT on the first biallelic record to `2/0`."""
    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("#") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 10:
            out.append(line)
            continue
        alt = cols[4]
        if "," in alt or alt == "." or not alt:
            out.append(line)
            continue
        fmt_keys = cols[8].split(":")
        if "GT" not in fmt_keys:
            out.append(line)
            continue
        gt_idx = fmt_keys.index("GT")
        sample_vals = cols[9].split(":")
        if gt_idx >= len(sample_vals):
            out.append(line)
            continue
        # Replace the GT with an out-of-range index. Preserve phasing if any.
        original_gt = sample_vals[gt_idx]
        separator = "|" if "|" in original_gt else "/"
        sample_vals[gt_idx] = f"2{separator}0"
        cols[9] = ":".join(sample_vals)
        new_line = "\t".join(cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True
    return out


# ---------------------------------------------------------------------------
# SAM mutators
# ---------------------------------------------------------------------------


@register_transform(
    "violate_cigar_seq_length",
    format="SAM",
    group="malformed_sam_cigar",
    description=(
        "Break SAM spec rule: sum of query-consuming CIGAR operators "
        "(M, I, S, =, X) MUST equal `len(SEQ)` unless SEQ=='*'. The "
        "mutator appends `5M` to the first alignment's CIGAR without "
        "extending SEQ — producing a mismatch the parser must reject "
        "(or silently accept → differential bug)."
    ),
    contextual_hint=(
        "the seed has at least one alignment record with CIGAR != '*' "
        "and SEQ != '*' — any non-trivial SAM satisfies this."
    ),
    preconditions=("has_cigar", "has_seq"),
)
def violate_cigar_seq_length(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Append `5M` to the first alignment's CIGAR while leaving SEQ alone."""
    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("@") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 11:
            out.append(line)
            continue
        cigar = cols[5]
        seq = cols[9]
        if cigar == "*" or seq == "*":
            out.append(line)
            continue
        # Append `5M` — consumes query but SEQ is untouched, so sum no
        # longer equals len(SEQ).
        cols[5] = cigar + "5M"
        new_line = "\t".join(cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True
    return out


# ---------------------------------------------------------------------------
# Phase 2 SAM mutators — REJECTION_INVARIANCE coverage lever
# ---------------------------------------------------------------------------


@register_transform(
    "violate_tlen_sign_consistency",
    format="SAM",
    group="malformed_sam_tlen",
    description=(
        "Break SAM spec rule: for a paired read whose mate is mapped, "
        "the two reads of a template MUST carry equal-magnitude "
        "opposite-signed TLEN values (SAMv1 §1.4). The mutator picks "
        "the first record with non-zero TLEN, keeps its magnitude, and "
        "flips its sign to match what its mate would have (creating "
        "two same-signed TLENs across the template)."
    ),
    contextual_hint=(
        "the seed has at least one alignment record with a non-zero "
        "TLEN (column 9) — any paired-read SAM satisfies this."
    ),
    preconditions=("has_nonzero_tlen",),
)
def violate_tlen_sign_consistency(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Flip the sign of the first non-zero TLEN. Leaves mate records
    untouched so the two reads of the same template now share a sign.
    """
    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("@") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 11:
            out.append(line)
            continue
        try:
            tlen = int(cols[8])
        except ValueError:
            out.append(line)
            continue
        if tlen == 0:
            out.append(line)
            continue
        # Flip the sign. The mate record carries +/- TLEN for a normal
        # pair, so negating this read's TLEN creates a same-signed pair
        # across the template — the spec-forbidden state.
        cols[8] = str(-tlen)
        new_line = "\t".join(cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True
    return out


@register_transform(
    "violate_optional_tag_type_character",
    format="SAM",
    group="malformed_sam_tags",
    description=(
        "Break SAMtags §2.1: an optional tag's type character MUST be "
        "one of `AifZHB` (plus numeric subtypes inside `B`). The mutator "
        "replaces the type of the first optional tag on the first "
        "alignment with an illegal character (`X`), producing a field "
        "like `NM:X:0` that spec-compliant parsers must reject."
    ),
    contextual_hint=(
        "the seed has at least one alignment record carrying at least "
        "one optional TAG:TYPE:VALUE field."
    ),
    preconditions=("has_optional_tag",),
)
def violate_optional_tag_type_character(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Replace the type character of the first optional tag on the
    first alignment with the illegal character `X`."""
    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("@") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 12:  # must have at least one optional tag
            out.append(line)
            continue
        tag_field = cols[11]
        tag_parts = tag_field.split(":", 2)
        if len(tag_parts) != 3:
            out.append(line)
            continue
        tag_name, _tag_type, tag_val = tag_parts
        cols[11] = f"{tag_name}:X:{tag_val}"  # illegal type char
        new_line = "\t".join(cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True
    return out


@register_transform(
    "violate_flag_bit_exclusivity",
    format="SAM",
    group="malformed_sam_flag",
    description=(
        "Break SAMv1 §1.4.1: when flag 0x4 (segment unmapped) is set, "
        "RNAME MUST be `*` and POS MUST be 0; conversely a record with "
        "RNAME != `*` and POS > 0 implies the segment is mapped, so "
        "0x4 MUST NOT be set. The mutator sets 0x4 on a mapped record "
        "while leaving RNAME and POS intact, producing the flag-bit "
        "inconsistency the spec forbids."
    ),
    contextual_hint=(
        "the seed has at least one alignment with RNAME != `*` and "
        "POS > 0 (any normal mapped read satisfies this)."
    ),
    preconditions=("has_mapped_read",),
)
def violate_flag_bit_exclusivity(
    seed_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Set bit 0x4 (unmapped) on the first mapped record, creating a
    mapped-yet-flagged-unmapped contradiction."""
    out = []
    mutated = False
    for line in seed_lines:
        stripped = line.rstrip("\r\n")
        if mutated or stripped.startswith("@") or "\t" not in stripped:
            out.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) < 11:
            out.append(line)
            continue
        rname = cols[2]
        try:
            pos = int(cols[3])
            flag = int(cols[1])
        except ValueError:
            out.append(line)
            continue
        if rname == "*" or pos == 0 or (flag & 0x4):
            out.append(line)
            continue
        cols[1] = str(flag | 0x4)  # force unmapped bit on mapped record
        new_line = "\t".join(cols)
        if line.endswith("\n"):
            new_line += "\n"
        out.append(new_line)
        mutated = True
    return out


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _collect_info_number_a_keys(lines: list[str]) -> list[str]:
    """Return the IDs of every ##INFO=<…> meta-line with Number=A."""
    keys: list[str] = []
    for line in lines:
        s = line.rstrip("\r\n")
        if not s.startswith("##INFO=<"):
            continue
        if "Number=A" not in s:
            continue
        # Extract ID
        idx = s.find("ID=")
        if idx < 0:
            continue
        after = s[idx + 3:]
        # ID ends at comma or closing angle bracket
        end = min(
            (p for p in (after.find(","), after.find(">")) if p >= 0),
            default=len(after),
        )
        keys.append(after[:end])
    return keys


def _append_extra_to_info_key(
    info_str: str,
    info_a_keys: list[str],
    rng: random.Random,
    bogus_values: list[str],
) -> Optional[str]:
    """Find the first key in info_a_keys present in info_str and append
    a spurious extra comma-value. Returns the new INFO string, or None
    if no matching key found."""
    if info_str == "." or not info_str:
        return None
    parts = info_str.split(";")
    mutated = False
    for i, part in enumerate(parts):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        if k in info_a_keys:
            parts[i] = f"{k}={v},{rng.choice(bogus_values)}"
            mutated = True
            break
    if not mutated:
        return None
    return ";".join(parts)
