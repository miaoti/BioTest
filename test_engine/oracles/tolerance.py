"""
Field-level strict/lenient separation for the consensus oracle.

Purpose (Run-9 lesson, 2026-04-20)
----------------------------------
BioTest's consensus oracle compares canonical JSON across voters. When
6 SAM parsers produce JSON that agrees on every MANDATORY field but
disagrees on an OPTIONAL tag (e.g., one computes ``NM`` differently,
another emits an extra informational tag), the whole record is bucketed
as "different" and the MR gets quarantined.

That's a false positive: the SAM v1.6 spec makes a clear distinction
between the **11 mandatory alignment columns** (QNAME / FLAG / RNAME /
POS / MAPQ / CIGAR / RNEXT / PNEXT / TLEN / SEQ / QUAL) and **optional
tag fields** (columns 12+). Mandatory columns carry the record's
identity; optional tags carry derived or auxiliary metadata that
different parsers may compute or omit without violating the spec.

This module exposes a ``strip_to_strict(canonical, format)`` helper
that returns a copy of the canonical dict with optional tags stripped.
``consensus.py`` calls it before bucketing voter outputs when
``feedback_control.consensus_field_tolerance`` is true. Strict-field
agreement then defines consensus, and tag-level disagreement is
recorded separately (the MR is not quarantined for it).

References
----------
- Hoffmann et al., *Assessing and assuring interoperability of a
  genomics file format*, Bioinformatics 2022 — formal spec oracle for
  BED (75/80 tools fail field-level agreement; same structural issue).
- "Differential Testing Overview" 2023+ literature — lenient oracles
  with field-level tolerance rules.

Design principles
-----------------
* **Constants live in code, not config.** The strict/lenient field
  sets are derived from the file-format spec, not from user judgment,
  so keeping them in code prevents per-SUT drift.
* **Default behaviour is unchanged.** Callers must explicitly opt in
  via ``strip_to_strict`` or the matching consensus flag. Existing
  tests that compare full canonical JSON continue to pass.
* **Only strip, never rewrite.** The helper removes fields; it never
  changes values. If a voter's strict fields differ, that's a real
  disagreement and the bucket split is correct.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


# ---------------------------------------------------------------------------
# SAM v1.6 §1.4 — mandatory alignment columns (11 fields).
# The CanonicalSamRecord Pydantic model uses uppercase keys to mirror
# the spec column names verbatim. "tags" is the dict holding optional
# columns (12+) and is NOT in the strict set.
# ---------------------------------------------------------------------------
SAM_RECORD_STRICT_FIELDS: frozenset[str] = frozenset({
    "QNAME", "FLAG", "RNAME", "POS", "MAPQ",
    "CIGAR", "RNEXT", "PNEXT", "TLEN", "SEQ", "QUAL",
})


# ---------------------------------------------------------------------------
# VCF v4.5 §1.4 — mandatory record columns (8 fields + one FORMAT
# column shared across samples). The CanonicalVcfRecord keys mirror
# these; "info" and "samples" hold the variable content. We keep the
# core 8 strict so per-parser differences in how they render INFO
# numeric precision / sample ordering get bucketed as a separate
# "lenient" signal instead of flipping consensus.
# ---------------------------------------------------------------------------
VCF_RECORD_STRICT_FIELDS: frozenset[str] = frozenset({
    # Variant identity: CHROM+POS+REF+ALT uniquely identifies a variant
    # per VCF spec §1.4.1. Keep this narrow for consensus bucketing —
    # FORMAT / INFO / QUAL / FILTER / samples all vary across voters for
    # spec-compliant reasons (precision, reordering, implicit PASS,
    # FORMAT field pruning on fully-missing columns) and their
    # differences don't signal parser bugs. ID is optional in VCF
    # ("." = missing) and voters disagree on how to represent that.
    "CHROM", "POS", "REF", "ALT",
})


def strip_to_strict(canonical: dict[str, Any], format_: str) -> dict[str, Any]:
    """Return a deep copy of ``canonical`` with optional fields removed.

    ``format_`` picks the strict-field set:
      * ``'SAM'`` → keeps the 11 mandatory columns per record,
        discards the ``tags`` dict and any future extensions.
      * ``'VCF'`` → keeps the 4 variant-identity columns per record
        (CHROM+POS+REF+ALT).
    Unknown formats return the input unchanged — the caller should
    handle this path by falling back to full-record comparison.

    Also drops ``header.meta`` (free-form ##KEY=VALUE lines from the
    VCF header that per-voter APIs expose differently — htsjdk drops
    ``ALT`` entries, vcfpy drops empty FILTER / PL, pysam adds
    implicit PASS, GATK-produced files carry command-line keys like
    ``LeftAlignVariants`` that survive some parsers but not others).
    Variant identity doesn't depend on those keys, so excluding them
    from the bucket-comparison key lets the oracle reach consensus on
    records that the voters actually agree on.
    """
    if not isinstance(canonical, dict):
        return canonical
    fmt_u = format_.upper()
    if fmt_u == "SAM":
        strict = SAM_RECORD_STRICT_FIELDS
    elif fmt_u == "VCF":
        strict = VCF_RECORD_STRICT_FIELDS
    else:
        return canonical

    out = deepcopy(canonical)

    # Drop header entirely for strict bucketing. For VCF:
    # header.meta (free-form ## keys) and header.fileformat
    # (htsjdk/others disagree on version-string encoding) always
    # dominated the bucket key on correct seeds. For SAM: header.HD
    # (version/sort order/group), header.SQ (per-ref M5/SP/AS
    # annotations voters emit inconsistently), and header.CO
    # (comments) behave the same way. Variant / alignment identity
    # doesn't need the header to agree — records[*] is what we care
    # about.
    if "header" in out:
        out.pop("header", None)

    records = out.get("records")
    if not isinstance(records, list):
        return out
    out["records"] = [_strip_record(r, strict) for r in records]
    return out


def _strip_record(record: Any, strict: frozenset[str]) -> Any:
    """Drop every key in ``record`` that is not in ``strict``.

    Keys that ARE strict are kept with their values untouched. If
    ``record`` is not a dict (e.g., the callers passed something
    unexpected), it is returned unchanged.
    """
    if not isinstance(record, dict):
        return record
    return {k: v for k, v in record.items() if k in strict}
