"""
SAM format atomic transform functions.

Each function operates on plain Python types and uses `random.Random(seed)`
for reproducibility.
"""

from __future__ import annotations

import re
import random
from typing import Optional

from . import register_transform


# ---------------------------------------------------------------------------
# Helper: parse and unparse CIGAR strings
# ---------------------------------------------------------------------------
def _parse_cigar(cigar: str) -> list[tuple[int, str]]:
    """Parse CIGAR string into [(length, op), ...]."""
    return [(int(m.group(1)), m.group(2)) for m in re.finditer(r"(\d+)([MIDNSHP=X])", cigar)]


def _unparse_cigar(ops: list[tuple[int, str]]) -> str:
    """Reconstruct CIGAR string from [(length, op), ...]."""
    return "".join(f"{length}{op}" for length, op in ops)


# Ops that consume query (SEQ) — used for length invariant assertions
_QUERY_CONSUMING = {"M", "I", "S", "=", "X"}


def _query_consumed(ops: list[tuple[int, str]]) -> int:
    """Total bases consumed from SEQ by the given CIGAR ops."""
    return sum(length for length, op in ops if op in _QUERY_CONSUMING)


# ---------------------------------------------------------------------------
# 1. permute_optional_tag_fields
# ---------------------------------------------------------------------------
@register_transform(
    "permute_optional_tag_fields",
    format="SAM",
    description="Shuffle the optional TAG:TYPE:VALUE fields (columns 12+) of a SAM alignment line while keeping the 11 mandatory fields fixed.",
)
def permute_optional_tag_fields(
    sam_line: str,
    seed: Optional[int] = None,
) -> str:
    """
    Shuffle the optional TAG:TYPE:VALUE fields (columns 12+) in a SAM
    alignment line while preserving the 11 mandatory fields.

    Args:
        sam_line: A single SAM alignment line (tab-separated).
        seed: RNG seed.

    Returns:
        The SAM line with optional tags in shuffled order.
    """
    rng = random.Random(seed)
    fields = sam_line.rstrip("\n").split("\t")
    if len(fields) <= 11:
        return sam_line  # no optional tags

    mandatory = fields[:11]
    optional = fields[11:]

    # Verify TAG uniqueness
    tags = [f.split(":", 1)[0] for f in optional]
    if len(tags) != len(set(tags)):
        raise ValueError(f"Duplicate optional tags detected: {tags}")

    rng.shuffle(optional)
    return "\t".join(mandatory + optional)


# ---------------------------------------------------------------------------
# 2. split_or_merge_adjacent_cigar_ops
# ---------------------------------------------------------------------------
@register_transform(
    "split_or_merge_adjacent_cigar_ops",
    format="SAM",
    description="Split one CIGAR op into two identical ops (10M -> 4M6M) or merge adjacent identical ops (4M6M -> 10M); total query-consumed length is always preserved.",
)
def split_or_merge_adjacent_cigar_ops(
    cigar: str,
    mode: str = "split",
    seed: Optional[int] = None,
) -> str:
    """
    Split or merge adjacent identical CIGAR operations.

    Split mode:  10M -> randomly split into (x)M + (10-x)M where 1 <= x < 10
    Merge mode:  4M6M -> 10M

    The total query-consumed length is always preserved (asserted).

    Args:
        cigar: CIGAR string, e.g. "10M5I3M".
        mode: "split" to split one random op, "merge" to merge adjacent same ops.
        seed: RNG seed.

    Returns:
        Transformed CIGAR string.

    Raises:
        ValueError: If mode is invalid or invariant is violated.
    """
    rng = random.Random(seed)
    ops = _parse_cigar(cigar)
    original_consumed = _query_consumed(ops)

    if mode == "merge":
        merged: list[tuple[int, str]] = []
        for length, op in ops:
            if merged and merged[-1][1] == op:
                merged[-1] = (merged[-1][0] + length, op)
            else:
                merged.append((length, op))
        result_ops = merged

    elif mode == "split":
        # Pick a random op with length > 1 to split
        splittable = [i for i, (length, _) in enumerate(ops) if length > 1]
        if not splittable:
            return cigar  # nothing to split

        idx = rng.choice(splittable)
        length, op = ops[idx]
        split_at = rng.randint(1, length - 1)
        new_ops = list(ops)
        new_ops[idx:idx + 1] = [(split_at, op), (length - split_at, op)]
        result_ops = new_ops

    else:
        raise ValueError(f"Invalid mode: {mode!r}. Must be 'split' or 'merge'.")

    # Invariant: query-consumed length must not change
    assert _query_consumed(result_ops) == original_consumed, (
        f"CIGAR invariant violated: consumed {_query_consumed(result_ops)} "
        f"!= original {original_consumed}"
    )

    return _unparse_cigar(result_ops)


# ---------------------------------------------------------------------------
# 3. reorder_header_records
# ---------------------------------------------------------------------------
@register_transform(
    "reorder_header_records",
    format="SAM",
    description="Shuffle SAM header lines of one type (e.g. all @SQ or all @RG lines) while keeping @HD mandatory as the first line.",
)
def reorder_header_records(
    header_lines: list[str],
    record_type: str = "@SQ",
    seed: Optional[int] = None,
) -> list[str]:
    """
    Shuffle SAM header records of a given type while keeping @HD as the
    first line (if present).

    Args:
        header_lines: List of SAM header lines (starting with @).
        record_type: The record type to shuffle, e.g. "@SQ" or "@RG".
        seed: RNG seed.

    Returns:
        Header lines with the specified record type shuffled.
    """
    rng = random.Random(seed)

    # Separate records by type, preserving order of non-target types
    target_lines: list[str] = []
    other_with_positions: list[tuple[int, str]] = []

    for i, line in enumerate(header_lines):
        tag = line.split("\t", 1)[0]
        if tag == record_type:
            target_lines.append(line)
        else:
            other_with_positions.append((i, line))

    rng.shuffle(target_lines)

    # Rebuild: @HD must be first
    result: list[str] = []
    hd_line: str | None = None
    non_hd_others: list[str] = []

    for _, line in other_with_positions:
        if line.startswith("@HD"):
            hd_line = line
        else:
            non_hd_others.append(line)

    if hd_line is not None:
        result.append(hd_line)

    # Interleave: place shuffled target records where they originally appeared
    # For simplicity, put all target records together after @HD, then the rest
    result.extend(target_lines)
    result.extend(non_hd_others)

    return result


# ---------------------------------------------------------------------------
# 4. toggle_cigar_hard_soft_clipping
# ---------------------------------------------------------------------------
@register_transform(
    "toggle_cigar_hard_soft_clipping",
    format="SAM",
    description="Convert H<->S clipping in CIGAR and synchronize SEQ/QUAL (H->S: pad dummy bases; S->H: trim those bases); used to test clipping-representation equivalence.",
)
def toggle_cigar_hard_soft_clipping(
    cigar: str,
    seq: str,
    qual: str,
    dummy_base: str = "N",
    dummy_qual: str = "!",
) -> tuple[str, str, str]:
    """
    Convert between Hard (H) and Soft (S) clipping in a CIGAR string,
    synchronizing SEQ and QUAL fields.

    H -> S: Prepend/append dummy bases and quality values.
    S -> H: Truncate the corresponding bases from SEQ and QUAL.

    Args:
        cigar: CIGAR string.
        seq: SEQ field.
        qual: QUAL field.
        dummy_base: Base character to insert for H->S conversion.
        dummy_qual: Quality character to insert for H->S conversion.

    Returns:
        Tuple of (new_cigar, new_seq, new_qual).
    """
    ops = _parse_cigar(cigar)
    new_ops: list[tuple[int, str]] = []
    prepend_bases = 0
    append_bases = 0
    trim_front = 0
    trim_back = 0

    for i, (length, op) in enumerate(ops):
        is_leading = i == 0
        is_trailing = i == len(ops) - 1

        if op == "H":
            # H -> S: mark how many dummy bases to add
            new_ops.append((length, "S"))
            if is_leading:
                prepend_bases += length
            elif is_trailing:
                append_bases += length
        elif op == "S":
            # S -> H: mark how many bases to trim
            new_ops.append((length, "H"))
            if is_leading:
                trim_front += length
            elif is_trailing:
                trim_back += length
        else:
            new_ops.append((length, op))

    # Apply SEQ/QUAL modifications
    new_seq = seq
    new_qual = qual

    if prepend_bases > 0:
        new_seq = dummy_base * prepend_bases + new_seq
        new_qual = dummy_qual * prepend_bases + new_qual
    if append_bases > 0:
        new_seq = new_seq + dummy_base * append_bases
        new_qual = new_qual + dummy_qual * append_bases
    if trim_front > 0:
        new_seq = new_seq[trim_front:]
        new_qual = new_qual[trim_front:]
    if trim_back > 0:
        new_seq = new_seq[:-trim_back]
        new_qual = new_qual[:-trim_back]

    return _unparse_cigar(new_ops), new_seq, new_qual
