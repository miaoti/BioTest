"""
Post-normalization layer for per-voter canonical JSON.

Each voter (htsjdk, vcfpy, pysam, noodles, reference, htslib, biopython,
seqan3) emits canonical JSON with per-implementation quirks: different
``fileformat`` string formats, CSV-`Description` quoting, `IDX` fields
from pysam, `Number` as int vs str, list-vs-str header metadata,
missing optional sample columns, etc. The consensus oracle buckets by
deep-equal — on correct input, those quirks produce one bucket per
voter, so consensus is impossible (see
``coverage_notes/phase4/oracle_and_detection_audit.md`` for the 46/47
sanity-check evidence).

This module applies a single post-normalization pass that strips those
quirks so same-input-same-semantics → same canonical JSON across
voters. Called once per voter output by
``test_engine.oracles.consensus.get_consensus_output`` before the
bucketing step.

Rules (VCF):

- ``fileformat`` is coerced to ``"VCFv<MAJOR>.<MINOR>"`` regardless of
  source: htsjdk ``"VCF4_3"``, noodles ``"FileFormat { major: 4, minor: 3 }"``,
  pysam/vcfpy/reference ``"VCFv4.3"``, dict ``{"major": 4, "minor": 3}``.
- Top-level schema is coerced to ``{format, header: {fileformat, meta,
  samples}, records: [...]}``. Voters that emit incompatible shapes
  (e.g. noodles' current stub with ``records_read`` count and no
  records list) have an ``_unusable`` marker attached — the oracle
  ignores ``_unusable`` voters.
- ``header.meta.<TYPE>.<ID>`` entries: drop implementation-specific
  ``IDX`` field, strip double-quote wrapping from ``Description``,
  coerce ``Number`` to string (``"1"``, ``"A"``, ``"R"``, ``"G"``,
  ``"."``).
- ``header.meta.<scalar>`` (``fileDate``, ``source``, ``reference``,
  ``phasing``, ...): coerce to single string (list → first element).
- Records: pad missing sample-column values with ``None`` per the
  record's ``FORMAT`` list so a voter that drops blank fields doesn't
  split from one that keeps them as null. ``QUAL`` is coerced to
  ``float`` or ``None``.
"""

from __future__ import annotations

import re
from typing import Any


# ---------------------------------------------------------------------------
# VCF
# ---------------------------------------------------------------------------

_VCF_SIMPLE_META_SCALAR_KEYS = {
    "fileDate", "source", "reference", "phasing",
}
_VCF_DROP_META_ENTRY_KEYS = {"IDX"}

# Voters inject/drop the implicit PASS filter differently:
# pysam auto-adds ``header.meta.FILTER.PASS`` (htslib default); reference
# and vcfpy only list what the file declares. Consensus should not
# split on that.
_VCF_META_FILTER_DROP_IMPLICIT_IDS = {"PASS"}

# Top-level meta keys that some voters don't surface at all (htsjdk
# drops ``contig`` and simple scalars ``fileDate``/``source``/etc.).
# These are annotative metadata — their presence or absence doesn't
# change parse semantics, so dropping them from the bucket key lets
# the oracle still reach consensus on the record content.
_VCF_META_DROP_FROM_BUCKET = {
    "contig", "fileDate", "source", "reference", "phasing",
}


def _vcf_sort_format(fmt: Any) -> Any:
    """Put GT first (it must be by spec), then alphabetical. Voters
    differ on declared order (htsjdk reshuffles to GT,HQ,GQ,DP while
    the file declared GT,GQ,DP,HQ) — since sample dicts are keyed by
    name not position, canonicalizing the FORMAT list order is safe.
    """
    if not isinstance(fmt, list):
        return fmt
    rest = sorted(k for k in fmt if k != "GT")
    return (["GT"] + rest) if "GT" in fmt else rest


def _vcf_norm_fileformat(ff: Any) -> str:
    """Coerce any voter's fileformat repr to ``VCFv<major>.<minor>``."""
    if isinstance(ff, dict):
        major = ff.get("major", "?")
        minor = ff.get("minor", "?")
        return f"VCFv{major}.{minor}"
    if isinstance(ff, str):
        # "FileFormat { major: 4, minor: 3 }"  — noodles Rust Debug
        m = re.search(r"major\s*:\s*(\d+).*?minor\s*:\s*(\d+)", ff)
        if m:
            return f"VCFv{m.group(1)}.{m.group(2)}"
        # "VCF4_3"  — htsjdk enum name
        m = re.match(r"^VCF(\d+)_(\d+)$", ff)
        if m:
            return f"VCFv{m.group(1)}.{m.group(2)}"
        # "VCFv4.3" — canonical, keep
        return ff
    return str(ff)


def _vcf_strip_quotes(s: Any) -> Any:
    if isinstance(s, str) and len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def _vcf_norm_meta_entry(fields: dict) -> dict:
    """Normalize a structured-meta entry (INFO/FORMAT/FILTER/contig row).

    Strips quotes from every string field (pysam keeps CSV quotes on
    Description / species / assembly etc.), drops IDX, coerces Number
    to string. Non-string values pass through.
    """
    out = {}
    for k, v in fields.items():
        if k in _VCF_DROP_META_ENTRY_KEYS:
            continue
        if k == "Number":
            out[k] = "" if v is None else str(v)
            continue
        out[k] = _vcf_strip_quotes(v)
    return out


def _vcf_norm_meta(meta: dict, drop_volatile: bool = True) -> dict:
    """Build the oracle-facing header.meta view.

    When ``drop_volatile=True`` (default for bucketing) keys in
    ``_VCF_META_DROP_FROM_BUCKET`` are omitted so voters that parse
    ``contig`` / ``fileDate`` / etc. still bucket with voters that
    don't. INFO / FORMAT definitions are kept because the record
    normalization needs them for type coercion.
    """
    out: dict[str, Any] = {}
    for key, val in meta.items():
        if drop_volatile and key in _VCF_META_DROP_FROM_BUCKET:
            continue
        if key in _VCF_SIMPLE_META_SCALAR_KEYS:
            if isinstance(val, list):
                out[key] = str(val[0]) if val else ""
            else:
                out[key] = "" if val is None else str(val)
            continue
        if isinstance(val, dict):
            entries: dict[str, Any] = {}
            for eid, f in val.items():
                if (
                    key.upper() == "FILTER"
                    and eid in _VCF_META_FILTER_DROP_IMPLICIT_IDS
                ):
                    continue
                entries[eid] = (
                    _vcf_norm_meta_entry(f) if isinstance(f, dict) else f
                )
            out[key] = entries
            continue
        out[key] = val
    return out


def _vcf_round_float(v: Any) -> Any:
    """Round floats to 6 sig-figs so pysam's float32-rehydrated values
    (0.017000000923871994) agree with the text form (0.017) that
    other voters emit."""
    if isinstance(v, float):
        try:
            return float(f"{v:.6g}")
        except (TypeError, ValueError):
            return v
    return v


def _vcf_norm_sample_value(v: Any) -> Any:
    """Coerce per-sample field values to a shared representation.

    pysam emits tuples for multi-value fields; we already list-ify in
    the runner, but safe to re-handle. Floats get rounded to kill
    pysam's 32-bit->64-bit precision noise.
    """
    if isinstance(v, list):
        return [_vcf_round_float(x) for x in v]
    if isinstance(v, tuple):
        return [_vcf_round_float(x) for x in v]
    return _vcf_round_float(v)


def _vcf_norm_gt(v: Any) -> Any:
    """Normalize GT across voters.

    pysam: tuple/list of ints ``(0, 0)`` or ``[0, 1]``, plus separate
      ``phased`` flag on the sample object — we don't see the flag in
      the canonical JSON, so we can only pick a consistent string form.
    vcfpy/reference/htslib: string ``"0|0"`` / ``"0/0"``.
    htsjdk: string of allele letters ``"G|G"`` — NOT translatable to
      indices without REF+ALT context, so we leave htsjdk-style GT
      alone and accept one-bucket-per-htsjdk on GT-present records.
    """
    if isinstance(v, (list, tuple)):
        parts = [str(x) if x is not None else "." for x in v]
        # Cannot recover phasing from list form — use "/" conservatively.
        return "/".join(parts)
    return v


def _vcf_norm_sample(sdata: Any) -> Any:
    if not isinstance(sdata, dict):
        return sdata
    out = {}
    for k, v in sdata.items():
        if k == "GT":
            out[k] = _vcf_norm_gt(v)
        else:
            out[k] = _vcf_norm_sample_value(v)
    return out


def _vcf_coerce_typed(s: Any, type_: str) -> Any:
    if s is None or s == "." or s == "":
        return None
    if type_ == "Integer":
        try:
            return int(s)
        except (TypeError, ValueError):
            pass
    if type_ == "Float":
        try:
            return _vcf_round_float(float(s))
        except (TypeError, ValueError):
            pass
    if type_ == "Flag":
        return True
    return _vcf_strip_quotes(s) if isinstance(s, str) else s


def _vcf_norm_info_value(v: Any, defn: dict | None = None) -> Any:
    """Normalize a single INFO value using its schema definition.

    - htsjdk emits every INFO value as a string; typed voters emit
      int/float/list.
    - For ``Number=1`` keys we want a scalar; for ``Number=A/R/G/<N>``
      a list even when len == 1 (so ``"0.5"`` from htsjdk agrees with
      ``[0.5]`` from reference).
    """
    defn = defn or {}
    type_ = defn.get("Type", "String")
    number = str(defn.get("Number", "1"))

    # Produce a list of items regardless of input shape.
    if isinstance(v, (list, tuple)):
        items = [_vcf_coerce_typed(x, type_) for x in v]
    elif isinstance(v, str) and "," in v:
        items = [_vcf_coerce_typed(p, type_) for p in v.split(",")]
    elif isinstance(v, bool):
        items = [v]
    else:
        items = [_vcf_coerce_typed(v, type_)]

    if type_ == "Flag":
        return True
    if number == "0":
        return True
    if number == "1":
        return items[0] if items else None
    # A / R / G / N / "." / numeric N → list form
    return items


def _vcf_norm_alt_token(a: Any) -> Any:
    """Strip the enclosing ``<>`` from symbolic ALT alleles so every
    voter's representation of ``<DEL>`` / ``<NON_REF>`` / ``<*>`` ends
    up as the same inner identifier. htsjdk (with our harness fix) and
    reference keep brackets; vcfpy + pysam strip them — normalize
    everyone to the stripped form here.
    """
    if isinstance(a, str) and len(a) >= 2 and a.startswith("<") and a.endswith(">"):
        return a[1:-1]
    return a


def _vcf_norm_record(rec: dict, info_defs: dict | None = None,
                     format_defs: dict | None = None) -> dict:
    if not isinstance(rec, dict):
        return rec
    out: dict[str, Any] = dict(rec)
    info_defs = info_defs or {}
    format_defs = format_defs or {}

    # ALT: strip angle brackets on symbolic alleles, keep order.
    alt = out.get("ALT")
    if isinstance(alt, list):
        out["ALT"] = [_vcf_norm_alt_token(a) for a in alt]

    # Pad missing sample fields against FORMAT; coerce per-field values.
    # FORMAT itself is sorted canonically so voters that reorder the
    # declared list (htsjdk) bucket with ones that preserve order.
    fmt = out.get("FORMAT")
    samples = out.get("samples")
    if isinstance(fmt, list):
        canonical_fmt = _vcf_sort_format(fmt)
        out["FORMAT"] = canonical_fmt
    else:
        canonical_fmt = fmt
    if isinstance(canonical_fmt, list) and isinstance(samples, dict):
        new_samples = {}
        for sname, sdata in samples.items():
            if isinstance(sdata, dict):
                padded = {
                    k: _vcf_norm_info_value(
                        sdata.get(k), format_defs.get(k)
                    ) if k != "GT" else _vcf_norm_gt(sdata.get(k))
                    for k in canonical_fmt
                }
                new_samples[sname] = padded
            else:
                new_samples[sname] = sdata
        out["samples"] = new_samples
    elif isinstance(samples, dict):
        out["samples"] = {
            sname: _vcf_norm_sample(s) for sname, s in samples.items()
        }

    # INFO: coerce with schema.
    info = out.get("INFO")
    if isinstance(info, dict):
        out["INFO"] = {
            k: _vcf_norm_info_value(v, info_defs.get(k))
            for k, v in info.items()
        }

    # QUAL -> float | None
    if "QUAL" in out:
        q = out["QUAL"]
        if q is None:
            out["QUAL"] = None
        else:
            try:
                out["QUAL"] = _vcf_round_float(float(q))
            except (TypeError, ValueError):
                out["QUAL"] = None

    # Missing ID -> None
    if out.get("ID") in ("", "."):
        out["ID"] = None

    # Missing FILTER -> []; sort.
    filt = out.get("FILTER")
    if filt in (".", "", None):
        out["FILTER"] = []
    elif isinstance(filt, list):
        # Drop implicit PASS + sort.
        out["FILTER"] = sorted(
            f for f in filt if f not in _VCF_META_FILTER_DROP_IMPLICIT_IDS
        )

    return out


def vcf_post_normalize(raw: Any) -> dict:
    """Fold per-voter VCF canonical-JSON quirks into a shared schema.

    Returns a dict that always has the top-level keys ``{format,
    header, records}`` or ``{_unusable}`` when the input shape is
    unrecognizable (e.g. noodles' current count-only stub). The oracle
    drops ``_unusable`` voters from bucketing.
    """
    if not isinstance(raw, dict):
        return {"_unusable": f"not-a-dict ({type(raw).__name__})"}

    # noodles stub: {records_read: N, header: {sample_count: N}, ...}
    if "records" not in raw and "records_read" in raw:
        return {"_unusable": "stub-output-no-records"}

    header_in = raw.get("header") or {}
    if not isinstance(header_in, dict):
        header_in = {}

    samples = header_in.get("samples")
    if not isinstance(samples, list):
        samples = []

    records_in = raw.get("records") or []
    if not isinstance(records_in, list):
        records_in = []

    raw_meta = header_in.get("meta") or {}
    meta_normalized = _vcf_norm_meta(raw_meta, drop_volatile=True)
    # Use full meta (including contig) to resolve INFO/FORMAT defs for
    # typed record normalization even though we drop volatile keys from
    # the bucket view.
    full_meta = _vcf_norm_meta(raw_meta, drop_volatile=False)
    info_defs = full_meta.get("INFO") or {}
    format_defs = full_meta.get("FORMAT") or {}
    return {
        "format": "VCF",
        "header": {
            "fileformat": _vcf_norm_fileformat(header_in.get("fileformat", "")),
            "meta": meta_normalized,
            "samples": list(samples),
        },
        "records": [
            _vcf_norm_record(r, info_defs, format_defs) for r in records_in
        ],
    }


# ---------------------------------------------------------------------------
# SAM
# ---------------------------------------------------------------------------

def _sam_norm_header(header: dict) -> dict:
    """Normalize SAM header. Keys we care about: HD, SQ, RG, PG, CO."""
    if not isinstance(header, dict):
        return {"HD": None, "SQ": [], "RG": [], "PG": [], "CO": []}
    out = {
        "HD": header.get("HD"),
        "SQ": list(header.get("SQ") or []),
        "RG": list(header.get("RG") or []),
        "PG": list(header.get("PG") or []),
        "CO": sorted(list(header.get("CO") or [])),
    }
    return out


def _sam_norm_record(rec: dict) -> dict:
    if not isinstance(rec, dict):
        return rec
    out: dict[str, Any] = dict(rec)

    # Normalize "*" markers to None.
    for col, missing in (
        ("RNAME", "*"), ("CIGAR", "*"), ("RNEXT", "*"),
        ("SEQ", "*"), ("QUAL", "*"),
    ):
        if out.get(col) == missing:
            out[col] = None

    # RNEXT "=": SAM spec §1.4.7 says "=" means "same as RNAME".
    # Resolve it so voters that normalize ("htslib" tends to keep it
    # literal; htsjdk / reference resolve it) land in the same bucket.
    if out.get("RNEXT") == "=" and out.get("RNAME"):
        out["RNEXT"] = out["RNAME"]

    # Coerce POS / PNEXT / FLAG / MAPQ / TLEN to int (voters vary
    # between int and str representations).
    for col in ("POS", "PNEXT", "FLAG", "MAPQ", "TLEN"):
        v = out.get(col)
        if isinstance(v, str):
            try:
                out[col] = int(v)
            except ValueError:
                pass

    # POS / PNEXT: SAM uses 0 as unmapped; canonical schema says None.
    for col in ("POS", "PNEXT"):
        if out.get(col) == 0:
            out[col] = None

    # SEQ / QUAL case-normalize. SAM spec §1.4.10 says SEQ is
    # case-insensitive. biopython returns as-is; htslib uppercases.
    seq = out.get("SEQ")
    if isinstance(seq, str):
        out["SEQ"] = seq.upper()

    # RNAME string coercion (int→str when contig name is numeric).
    for col in ("RNAME", "RNEXT"):
        v = out.get(col)
        if isinstance(v, int):
            out[col] = str(v)

    # Ensure tags dict.
    if "tags" not in out or out["tags"] is None:
        out["tags"] = {}

    return out


def sam_post_normalize(raw: Any) -> dict:
    """Fold per-voter SAM canonical-JSON quirks into a shared schema."""
    if not isinstance(raw, dict):
        return {"_unusable": f"not-a-dict ({type(raw).__name__})"}

    header_in = raw.get("header") or {}
    records_in = raw.get("records") or []
    if not isinstance(records_in, list):
        records_in = []

    return {
        "format": "SAM",
        "header": _sam_norm_header(header_in),
        "records": [_sam_norm_record(r) for r in records_in],
    }


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def post_normalize(raw: Any, format_: str) -> dict:
    """Apply the per-format post-normalizer. Safe no-op for unknown
    formats (returns raw as-is).
    """
    f = (format_ or "").upper()
    if f == "VCF":
        return vcf_post_normalize(raw)
    if f == "SAM":
        return sam_post_normalize(raw)
    return raw if isinstance(raw, dict) else {"_unusable": f"unknown-format: {format_}"}
