"""
SAM normalizer: parse raw SAM text into CanonicalSam.

This is the Python-native parser used as a reference normalizer.
It reads raw SAM text lines and produces a CanonicalSam object.

Tolerance design (Fix #1, 2026-04-20)
-------------------------------------
SAM v1.6 admits multiple equivalent serializations for the same logical
record (RNEXT="=" alias for RNAME, optional-tag ordering, float-tag
precision, biopython-consumed tags like MD/AS that other parsers leave
in place). When the consensus oracle compared canonical JSON across 6
voters in Run 9, these spec-allowed variations triggered 26/27 MR
quarantines — false positives, not real bugs.

The fixes here resolve those variations at the canonical-JSON level so
all voters emit byte-identical JSON for the same logical record:

1. **RNEXT="=" → RNAME**: spec allows "=" as alias for "same as RNAME";
   different parsers may resolve or preserve it. We resolve it here so
   the canonical form is always the explicit reference name.
2. **Float-tag precision**: tag type "f" can be serialized as
   `0.85`, `8.5e-1`, `0.850000` etc. We round to ``FLOAT_TAG_SIGFIGS``
   significant digits before storing.
3. **Biopython-consumed tags dropped**: Bio.Align consumes MD/AS tags
   while parsing and never emits them in its canonical output. Other
   parsers preserve them. We drop them globally so the comparison
   stays apples-to-apples.
4. **Header-tag sort**: ``_parse_tag_fields`` already sorts; left
   here as a documented invariant so future header-emitting code stays
   consistent.

These fixes are SUT-agnostic — they live in the framework's canonical
normalizer, not in any per-runner code path.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from .schema import (
    CanonicalSam,
    CanonicalSamHeader,
    CanonicalSamRecord,
    CigarOp,
    TagValue,
)


# Number of significant digits to round float-typed (`f`) SAM tag values
# to before they enter canonical JSON. 6 sig digits matches the spec's
# IEEE 754 single-precision implication and is enough to keep semantic
# fidelity while suppressing per-parser printf-format drift.
FLOAT_TAG_SIGFIGS: int = 6


# SAM optional tags that Bio.Align.parse() consumes and never re-emits
# (used internally to reconstruct MD-implied alignments). Other parsers
# preserve them. We drop them from the canonical record before compare
# so consensus does not flag a false positive.
#
# Sources:
#   - Bio/Align/sam.py — `MD` and `AS` consumed by `_parse_md` / scoring
#   - SAM v1.6 §1.5 — these tags are SUMMARY/derived, not authoritative
BIOPYTHON_CONSUMED_TAGS: frozenset[str] = frozenset({"MD", "AS"})


def normalize_sam_text(
    lines: list[str],
    strict_mode: bool = False,
) -> CanonicalSam:
    """Parse raw SAM text lines into a CanonicalSam object.

    Args:
        lines: raw SAM text lines (with or without trailing newlines).
        strict_mode: when True, raise ValueError on spec violations that
            non-strict silently tolerates — specifically: sum of
            query-consuming CIGAR ops != len(SEQ) when both are non-'*'.
            Used by the error-consensus oracle (Rank 3 lever).
    """
    header_lines: list[str] = []
    alignment_lines: list[str] = []

    for line in lines:
        stripped = line.rstrip("\r\n")
        if not stripped:
            continue
        if stripped.startswith("@"):
            header_lines.append(stripped)
        else:
            alignment_lines.append(stripped)

    header = _parse_header(header_lines)
    records = [_parse_alignment(al, strict_mode=strict_mode) for al in alignment_lines]
    return CanonicalSam(header=header, records=records)


def _parse_header(header_lines: list[str]) -> CanonicalSamHeader:
    """Parse SAM header lines into CanonicalSamHeader."""
    hd: Optional[dict[str, str]] = None
    sq: list[dict[str, str]] = []
    rg: list[dict[str, str]] = []
    pg: list[dict[str, str]] = []
    co: list[str] = []

    for line in header_lines:
        fields = line.split("\t")
        record_type = fields[0]

        if record_type == "@HD":
            hd = _parse_tag_fields(fields[1:])
        elif record_type == "@SQ":
            sq.append(_parse_tag_fields(fields[1:]))
        elif record_type == "@RG":
            rg.append(_parse_tag_fields(fields[1:]))
        elif record_type == "@PG":
            pg.append(_parse_tag_fields(fields[1:]))
        elif record_type == "@CO":
            co.append("\t".join(fields[1:]))

    return CanonicalSamHeader(HD=hd, SQ=sq, RG=rg, PG=pg, CO=sorted(co))


def _parse_tag_fields(fields: list[str]) -> dict[str, str]:
    """Parse TAG:VALUE header fields into a dict.

    Keys are sorted for canonical stability: the SAMv1 spec does not
    impose an ordering on TAG:VALUE pairs within @HD/@SQ/@RG/@PG lines,
    so a permutation is semantics-preserving. Sorting here makes the
    canonical JSON invariant under within-record tag permutation — the
    basis of Phase 2's shuffle_*_record_subtags metamorphic relations.
    """
    result: dict[str, str] = {}
    for field in fields:
        if ":" in field:
            key, val = field.split(":", 1)
            result[key] = val
    return dict(sorted(result.items()))


def _parse_alignment(
    line: str,
    strict_mode: bool = False,
) -> CanonicalSamRecord:
    """Parse a SAM alignment line into CanonicalSamRecord."""
    cols = line.split("\t")
    if len(cols) < 11:
        raise ValueError(f"SAM alignment has fewer than 11 columns: {line[:80]}")

    qname = cols[0]
    flag = int(cols[1])
    rname = None if cols[2] == "*" else cols[2]
    raw_pos = int(cols[3])
    pos = None if raw_pos == 0 else raw_pos  # Already 1-based in SAM text
    mapq = int(cols[4])
    cigar = _parse_cigar(cols[5])
    # Tolerance #1 (Run 9 lesson): RNEXT="=" is a SAM v1.6-allowed alias
    # for "same as RNAME". Some parsers preserve the literal "=", others
    # resolve it to the reference name. Resolving here makes both styles
    # produce byte-identical canonical JSON.
    raw_rnext = cols[6]
    if raw_rnext == "*":
        rnext = None
    elif raw_rnext == "=":
        rnext = rname  # may itself be None for unmapped reads — that's fine
    else:
        rnext = raw_rnext
    raw_pnext = int(cols[7])
    pnext = None if raw_pnext == 0 else raw_pnext
    tlen = int(cols[8])
    seq = None if cols[9] == "*" else cols[9]
    qual = None if cols[10] == "*" else cols[10]

    # Strict-mode guard: sum of query-consuming CIGAR ops must equal
    # len(SEQ) per SAM v1 spec. Only applies when both CIGAR and SEQ
    # are non-'*'.
    if strict_mode and cigar is not None and seq is not None:
        query_len = sum(op.len for op in cigar if op.op in ("M", "I", "S", "=", "X"))
        if query_len != len(seq):
            raise ValueError(
                "SAM spec violation: sum of query-consuming CIGAR ops "
                f"({query_len}) != len(SEQ) ({len(seq)}) on record "
                f"{qname!r}"
            )

    # Optional tags (columns 12+).
    # Tolerance #3 (Run 9 lesson): Bio.Align consumes MD/AS during parse
    # and never re-emits them; other parsers preserve them. Drop the set
    # globally so the consensus oracle does not mark the resulting MD/AS
    # absence as a cross-voter disagreement.
    tags: dict[str, TagValue] = {}
    for col in cols[11:]:
        m = re.match(r"^([A-Za-z][A-Za-z0-9]):([AifZHB]):(.+)$", col)
        if m:
            tag_name = m.group(1)
            if tag_name in BIOPYTHON_CONSUMED_TAGS:
                continue
            tag_type = m.group(2)
            tag_val = _parse_tag_value(m.group(3), tag_type)
            tags[tag_name] = TagValue(type=tag_type, value=tag_val)

    # Sort tags by key for deterministic output (header-tag sort already
    # handled by `_parse_tag_fields`; this enforces the same invariant
    # for record-level tags so MR-induced reorderings normalise away).
    sorted_tags = dict(sorted(tags.items()))

    return CanonicalSamRecord(
        QNAME=qname,
        FLAG=flag,
        RNAME=rname,
        POS=pos,
        MAPQ=mapq,
        CIGAR=cigar,
        RNEXT=rnext,
        PNEXT=pnext,
        TLEN=tlen,
        SEQ=seq,
        QUAL=qual,
        tags=sorted_tags,
    )


def _parse_cigar(cigar_str: str) -> Optional[list[CigarOp]]:
    """Parse CIGAR string into list of CigarOp."""
    if cigar_str == "*":
        return None
    ops = []
    for m in re.finditer(r"(\d+)([MIDNSHP=X])", cigar_str):
        ops.append(CigarOp(op=m.group(2), len=int(m.group(1))))
    return ops if ops else None


def _round_float_sigfig(value: float, sig: int = FLOAT_TAG_SIGFIGS) -> float:
    """Round ``value`` to ``sig`` significant figures.

    Used to suppress per-parser printf-format drift on `f`-typed SAM
    tags (Tolerance #2). 0.0 is preserved as-is so we don't divide by
    zero in log10. Returns a Python float that JSON-serialises stably.
    """
    if value == 0.0 or value != value:  # zero or NaN
        return value
    import math
    digits = sig - int(math.floor(math.log10(abs(value)))) - 1
    return round(value, digits)


def _parse_tag_value(val_str: str, tag_type: str) -> Any:
    """Parse a SAM tag value according to its type.

    Float-typed (`f`) values are rounded to ``FLOAT_TAG_SIGFIGS`` sig
    digits — a Run-9 tolerance fix that suppresses ``0.85`` vs
    ``0.8500000`` vs ``8.5e-1`` per-parser printf-format drift.
    """
    if tag_type == "i":
        return int(val_str)
    if tag_type == "f":
        return _round_float_sigfig(float(val_str))
    if tag_type == "B":
        # Array type: B:type,val1,val2,...
        parts = val_str.split(",")
        subtype = parts[0]
        values = parts[1:]
        if subtype in ("c", "C", "s", "S", "i", "I"):
            return [int(v) for v in values]
        if subtype == "f":
            return [_round_float_sigfig(float(v)) for v in values]
        return values
    # A (char), Z (string), H (hex)
    return val_str
