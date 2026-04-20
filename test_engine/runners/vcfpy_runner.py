"""
vcfpy runner: pure-Python VCF parser (bihealth/vcfpy), in-process.

Independent reimplementation of VCF — NOT a wrapper around htslib —
so it exercises a distinct codepath from pysam/htslib and surfaces
bugs the C-stack voters cannot reveal. Fully traceable by coverage.py
since 100% of the parse logic lives in .py files.

CRITICAL: vcfpy uses 1-based POS natively (matches the canonical
schema). No +1 adjustment required.

vcfpy does NOT support SAM.
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Any, Optional

from .base import ParserRunner, RunnerResult

logger = logging.getLogger(__name__)

_vcfpy_available: Optional[bool] = None


def _check_vcfpy() -> bool:
    """Check if vcfpy is importable (pip-installed)."""
    global _vcfpy_available
    if _vcfpy_available is None:
        try:
            import vcfpy as _  # noqa: F401
            _vcfpy_available = True
        except ImportError:
            _vcfpy_available = False
    return _vcfpy_available


def _coerce_value(v: Any) -> Any:
    """Flatten vcfpy-specific types into plain JSON-able scalars."""
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, (list, tuple, set)):
        return [_coerce_value(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _coerce_value(x) for k, x in v.items()}
    return str(v)


class VcfpyRunner(ParserRunner):
    """Parser runner using vcfpy's Reader API (VCF only)."""

    @property
    def name(self) -> str:
        return "vcfpy"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF"}

    def is_available(self) -> bool:
        return _check_vcfpy()

    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        if not self.is_available():
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr="vcfpy not importable — run `py -3.12 -m pip install vcfpy`",
            )

        if format_type.upper() != "VCF":
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="ineligible",
                stderr="vcfpy only supports VCF format",
            )

        t0 = time.monotonic()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._parse_vcf, input_path)
                result = future.result(timeout=timeout_s)
            duration = (time.monotonic() - t0) * 1000
            return RunnerResult(
                success=True,
                canonical_json=result,
                parser_name=self.name,
                format_type=format_type,
                duration_ms=duration,
            )
        except FuturesTimeout:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="timeout",
                stderr=f"vcfpy timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="crash",
                stderr=f"{type(e).__name__}: {e}",
                duration_ms=(time.monotonic() - t0) * 1000,
            )

    def _parse_vcf(self, path: Path) -> dict[str, Any]:
        import vcfpy

        reader = vcfpy.Reader.from_path(str(path))
        header = reader.header

        fileformat = ""
        meta: dict[str, Any] = {}
        for line in header.lines:
            key = getattr(line, "key", None)
            if not key:
                continue
            if key == "fileformat":
                fileformat = str(getattr(line, "value", "") or "")
                continue
            mapping = getattr(line, "mapping", None)
            if isinstance(mapping, dict):
                entry_id = mapping.get("ID", "")
                fields = {str(k): _coerce_value(v) for k, v in mapping.items()}
                if key not in meta:
                    meta[key] = {}
                if isinstance(meta[key], dict):
                    meta[key][entry_id] = fields
            else:
                val = getattr(line, "value", None)
                if val is not None:
                    meta.setdefault(key, []).append(_coerce_value(val))

        samples = list(header.samples.names) if header.samples else []

        records: list[dict[str, Any]] = []
        try:
            for rec in reader:
                alt = [str(a.value) for a in (rec.ALT or [])]

                rec_id = None
                if rec.ID:
                    ids = rec.ID if isinstance(rec.ID, list) else [rec.ID]
                    rec_id = ";".join(str(x) for x in ids) if ids else None

                qual = None if rec.QUAL is None else float(rec.QUAL)

                filt = sorted([str(x) for x in (rec.FILTER or [])])

                info: dict[str, Any] = {}
                for key, val in (rec.INFO or {}).items():
                    info[str(key)] = _coerce_value(val)
                info = dict(sorted(info.items()))

                fmt_keys: Optional[list[str]] = None
                if rec.FORMAT:
                    fmt_keys = [str(k) for k in rec.FORMAT]

                sample_data: dict[str, dict] = {}
                for call in rec.calls:
                    sname = str(call.sample)
                    fields: dict[str, Any] = {}
                    for k, v in (call.data or {}).items():
                        fields[str(k)] = _coerce_value(v)
                    sample_data[sname] = fields

                records.append({
                    "CHROM": str(rec.CHROM),
                    "POS": int(rec.POS),
                    "ID": rec_id,
                    "REF": str(rec.REF),
                    "ALT": alt,
                    "QUAL": qual,
                    "FILTER": filt,
                    "INFO": info,
                    "FORMAT": fmt_keys,
                    "samples": sample_data if sample_data else None,
                })
        finally:
            reader.close()

        return {
            "format": "VCF",
            "header": {
                "fileformat": fileformat,
                "meta": meta,
                "samples": samples,
            },
            "records": records,
        }
