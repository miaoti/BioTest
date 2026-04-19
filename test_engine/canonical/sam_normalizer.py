"""
SAM normalizer: parse raw SAM text into CanonicalSam.

This is the Python-native parser used as a reference normalizer.
It reads raw SAM text lines and produces a CanonicalSam object.
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
    rnext = None if cols[6] == "*" else ("=" if cols[6] == "=" else cols[6])
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

    # Optional tags (columns 12+)
    tags: dict[str, TagValue] = {}
    for col in cols[11:]:
        m = re.match(r"^([A-Za-z][A-Za-z0-9]):([AifZHB]):(.+)$", col)
        if m:
            tag_name = m.group(1)
            tag_type = m.group(2)
            tag_val = _parse_tag_value(m.group(3), tag_type)
            tags[tag_name] = TagValue(type=tag_type, value=tag_val)

    # Sort tags by key for deterministic output
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


def _parse_tag_value(val_str: str, tag_type: str) -> Any:
    """Parse a SAM tag value according to its type."""
    if tag_type == "i":
        return int(val_str)
    if tag_type == "f":
        return float(val_str)
    if tag_type == "B":
        # Array type: B:type,val1,val2,...
        parts = val_str.split(",")
        subtype = parts[0]
        values = parts[1:]
        if subtype in ("c", "C", "s", "S", "i", "I"):
            return [int(v) for v in values]
        if subtype == "f":
            return [float(v) for v in values]
        return values
    # A (char), Z (string), H (hex)
    return val_str
