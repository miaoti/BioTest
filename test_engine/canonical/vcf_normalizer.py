"""
VCF normalizer: parse raw VCF text into CanonicalVcf.

This is the Python-native parser used as a reference normalizer.
It reads raw VCF text lines and produces a CanonicalVcf object.
Parser-specific adapters (pysam, htsjdk) produce their own output
which is then compared against this canonical form.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from .schema import CanonicalVcf, CanonicalVcfHeader, CanonicalVcfRecord


def normalize_vcf_text(lines: list[str]) -> CanonicalVcf:
    """
    Parse raw VCF text lines into a CanonicalVcf object.

    This is the reference normalizer — it reads the VCF text directly
    and produces canonical output. Used for generating golden files
    and for the metamorphic oracle when no external parser is needed.
    """
    meta_lines: list[str] = []
    header_line: Optional[str] = None
    data_lines: list[str] = []

    for line in lines:
        stripped = line.rstrip("\r\n")
        if not stripped:
            continue
        if stripped.startswith("##"):
            meta_lines.append(stripped)
        elif stripped.startswith("#CHROM") or stripped.startswith("#"):
            header_line = stripped
        else:
            data_lines.append(stripped)

    if header_line is None:
        raise ValueError("No #CHROM header line found in VCF")

    header = _parse_header(meta_lines, header_line)
    records = [_parse_record(dl, header) for dl in data_lines]
    return CanonicalVcf(header=header, records=records)


def _parse_header(meta_lines: list[str], header_line: str) -> CanonicalVcfHeader:
    """Parse VCF meta lines and #CHROM header into CanonicalVcfHeader."""
    fileformat = ""
    meta: dict[str, Any] = {}

    for line in meta_lines:
        if line.startswith("##fileformat="):
            fileformat = line.split("=", 1)[1]
            continue

        # Structured meta: ##KEY=<ID=...,Number=...,Type=...,Description="...">
        m = re.match(r"^##(\w+)=<(.+)>$", line)
        if m:
            key = m.group(1)
            fields = _parse_structured_fields(m.group(2))
            entry_id = fields.get("ID", "")
            if key not in meta:
                meta[key] = {}
            if isinstance(meta[key], dict):
                meta[key][entry_id] = fields
            continue

        # Simple meta: ##KEY=VALUE
        m2 = re.match(r"^##(\w+)=(.+)$", line)
        if m2:
            key = m2.group(1)
            val = m2.group(2)
            if key not in meta:
                meta[key] = val
            elif isinstance(meta[key], list):
                meta[key].append(val)
            else:
                meta[key] = [meta[key], val]

    # Extract sample names from #CHROM line
    cols = header_line.split("\t")
    samples = cols[9:] if len(cols) > 9 else []

    return CanonicalVcfHeader(
        fileformat=fileformat,
        meta=meta,
        samples=samples,
    )


def _parse_structured_fields(text: str) -> dict[str, str]:
    """Parse key=value pairs from a structured meta line (inside <>)."""
    fields: dict[str, str] = {}
    # Handle quoted values with commas inside
    i = 0
    while i < len(text):
        # Find key
        eq = text.find("=", i)
        if eq == -1:
            break
        key = text[i:eq].strip()

        # Find value (may be quoted)
        val_start = eq + 1
        if val_start < len(text) and text[val_start] == '"':
            # Quoted value — find closing quote
            close = text.find('"', val_start + 1)
            if close == -1:
                close = len(text)
            fields[key] = text[val_start + 1 : close]
            i = close + 2  # skip closing quote and comma
        else:
            # Unquoted value — find next comma
            comma = text.find(",", val_start)
            if comma == -1:
                fields[key] = text[val_start:]
                break
            fields[key] = text[val_start:comma]
            i = comma + 1

    return fields


def _parse_record(line: str, header: CanonicalVcfHeader) -> CanonicalVcfRecord:
    """Parse a VCF data line into a CanonicalVcfRecord."""
    cols = line.split("\t")
    if len(cols) < 8:
        raise ValueError(f"VCF record has fewer than 8 columns: {line[:80]}")

    chrom = cols[0]
    pos = int(cols[1])
    rec_id = None if cols[2] == "." else cols[2]
    ref = cols[3]
    alt = [] if cols[4] == "." else cols[4].split(",")
    qual = None if cols[5] == "." else float(cols[5])
    filt = [] if cols[6] == "." else sorted(cols[6].split(";"))
    info = _parse_info(cols[7], header.meta.get("INFO", {}))

    fmt = None
    samples = None
    if len(cols) > 8 and cols[8] != ".":
        fmt = cols[8].split(":")
        if len(cols) > 9:
            samples = {}
            for i, sample_name in enumerate(header.samples):
                if 9 + i < len(cols):
                    samples[sample_name] = _parse_sample(
                        cols[9 + i], fmt, header.meta.get("FORMAT", {})
                    )

    return CanonicalVcfRecord(
        CHROM=chrom,
        POS=pos,
        ID=rec_id,
        REF=ref,
        ALT=alt,
        QUAL=qual,
        FILTER=filt,
        INFO=info,
        FORMAT=fmt,
        samples=samples,
    )


def _parse_info(info_str: str, info_defs: dict[str, Any]) -> dict[str, Any]:
    """Parse INFO column into typed dict."""
    if info_str == ".":
        return {}

    result: dict[str, Any] = {}
    for kv in info_str.split(";"):
        if "=" in kv:
            key, val = kv.split("=", 1)
            # Type the value based on INFO definition
            defn = info_defs.get(key, {})
            result[key] = _type_info_value(val, defn)
        else:
            # Flag type
            result[kv] = True

    return dict(sorted(result.items()))


def _type_info_value(val: str, defn: dict[str, str]) -> Any:
    """Convert an INFO value string to its typed representation."""
    if val == ".":
        return None

    info_type = defn.get("Type", "String")
    number = defn.get("Number", "1")

    # Multi-value fields
    if "," in val or number in ("A", "R", "G", "."):
        parts = val.split(",")
        return [_cast_single(p, info_type) for p in parts]

    return _cast_single(val, info_type)


def _cast_single(val: str, info_type: str) -> Any:
    """Cast a single value to its VCF type."""
    if val == ".":
        return None
    if info_type == "Integer":
        return int(val)
    if info_type == "Float":
        return float(val)
    return val


def _parse_sample(sample_str: str, fmt: list[str], fmt_defs: dict) -> dict[str, Any]:
    """Parse a sample column into typed dict keyed by FORMAT fields."""
    values = sample_str.split(":")
    result: dict[str, Any] = {}
    for i, key in enumerate(fmt):
        if i < len(values):
            raw = values[i]
            defn = fmt_defs.get(key, {})
            if raw == ".":
                result[key] = None
            elif "," in raw:
                result[key] = [_cast_single(v, defn.get("Type", "String")) for v in raw.split(",")]
            else:
                result[key] = _cast_single(raw, defn.get("Type", "String"))
        else:
            result[key] = None
    return result
