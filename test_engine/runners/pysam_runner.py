"""
Pysam runner: Python in-process parser for VCF and SAM via HTSlib.

CRITICAL: pysam uses 0-based coordinates for ALL formats (including VCF).
The normalizer must add +1 to POS for both VCF and SAM.
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Any, Optional

from .base import ParserRunner, RunnerResult

logger = logging.getLogger(__name__)

_pysam_available: Optional[bool] = None


def _check_pysam() -> bool:
    global _pysam_available
    if _pysam_available is None:
        try:
            import pysam  # noqa: F401
            _pysam_available = True
        except ImportError:
            _pysam_available = False
    return _pysam_available


class PysamRunner(ParserRunner):
    """Parser runner using pysam (HTSlib wrapper)."""

    @property
    def name(self) -> str:
        return "pysam"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        return _check_pysam()

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
                stderr="pysam is not installed",
            )

        t0 = time.monotonic()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._parse, input_path, format_type.upper()
                )
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
                stderr=f"pysam timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="crash",
                stderr=str(e),
                duration_ms=(time.monotonic() - t0) * 1000,
            )

    def _parse(self, input_path: Path, format_type: str) -> dict[str, Any]:
        import pysam

        if format_type == "VCF":
            return self._parse_vcf(input_path, pysam)
        elif format_type == "SAM":
            return self._parse_sam(input_path, pysam)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _parse_vcf(self, path: Path, pysam: Any) -> dict[str, Any]:
        """Parse VCF via pysam into canonical dict."""
        vcf = pysam.VariantFile(str(path))
        header = vcf.header

        # Header
        meta: dict[str, Any] = {}
        for rec in header.records:
            if rec.type == "GENERIC":
                continue
            key = rec.key
            if hasattr(rec, "items") and callable(rec.items):
                fields = dict(rec.items())
                entry_id = fields.get("ID", "")
                if key not in meta:
                    meta[key] = {}
                if isinstance(meta[key], dict):
                    meta[key][entry_id] = fields

        samples = list(header.samples)

        # Records
        records = []
        for rec in vcf:
            # CRITICAL: pysam rec.pos is 0-based! Add +1 for 1-based canonical.
            pos = rec.pos + 1

            rec_id = None if rec.id is None else rec.id
            alt = list(rec.alts) if rec.alts else []
            qual = None if rec.qual is None else float(rec.qual)

            # FILTER
            filt = sorted(list(rec.filter.keys())) if rec.filter else []

            # INFO
            info: dict[str, Any] = {}
            for key in rec.info:
                val = rec.info[key]
                if isinstance(val, tuple):
                    val = list(val)
                info[key] = val
            info = dict(sorted(info.items()))

            # Samples
            sample_data: dict[str, dict] = {}
            for sample_name in samples:
                sample = rec.samples[sample_name]
                fields: dict[str, Any] = {}
                for key in sample.keys():
                    val = sample[key]
                    if isinstance(val, tuple):
                        val = list(val)
                    fields[key] = val
                sample_data[sample_name] = fields

            fmt = list(rec.format.keys()) if rec.format else None

            records.append({
                "CHROM": rec.chrom,
                "POS": pos,
                "ID": rec_id,
                "REF": rec.ref,
                "ALT": alt,
                "QUAL": qual,
                "FILTER": filt,
                "INFO": info,
                "FORMAT": fmt,
                "samples": sample_data if sample_data else None,
            })

        vcf.close()

        return {
            "format": "VCF",
            "header": {
                "fileformat": str(header.version) if hasattr(header, "version") else "",
                "meta": meta,
                "samples": samples,
            },
            "records": records,
        }

    def _parse_sam(self, path: Path, pysam: Any) -> dict[str, Any]:
        """Parse SAM via pysam into canonical dict."""
        sam = pysam.AlignmentFile(str(path), "r")
        header = sam.header

        # Header
        hd = dict(header.get("HD", {})) if "HD" in header else None
        sq = [dict(s) for s in header.get("SQ", [])]
        rg = [dict(r) for r in header.get("RG", [])]
        pg = [dict(p) for p in header.get("PG", [])]
        co = sorted(header.get("CO", []))

        # Records
        records = []
        for read in sam:
            # CRITICAL: pysam reference_start is 0-based! Add +1.
            pos = None if read.is_unmapped else read.reference_start + 1
            pnext = None
            if read.next_reference_start is not None and read.next_reference_start >= 0:
                pnext = read.next_reference_start + 1

            # CIGAR
            cigar = None
            if read.cigartuples:
                op_map = {0: "M", 1: "I", 2: "D", 3: "N", 4: "S", 5: "H", 6: "P", 7: "=", 8: "X"}
                cigar = [{"op": op_map.get(op, "?"), "len": length}
                         for op, length in read.cigartuples]

            # Tags
            tags = {}
            for tag_name, tag_val in read.get_tags(with_value_type=True):
                tag_type = tag_val[0] if isinstance(tag_val, tuple) else "Z"
                val = tag_val[1] if isinstance(tag_val, tuple) else tag_val
                tags[tag_name] = {"type": tag_type, "value": val}
            tags = dict(sorted(tags.items()))

            records.append({
                "QNAME": read.query_name,
                "FLAG": read.flag,
                "RNAME": None if read.reference_name is None else read.reference_name,
                "POS": pos,
                "MAPQ": read.mapping_quality,
                "CIGAR": cigar,
                "RNEXT": None if read.next_reference_name is None else read.next_reference_name,
                "PNEXT": pnext,
                "TLEN": read.template_length,
                "SEQ": None if read.query_sequence is None else read.query_sequence,
                "QUAL": None if read.query_qualities is None else "".join(
                    chr(q + 33) for q in read.query_qualities
                ),
                "tags": tags,
            })

        sam.close()

        return {
            "format": "SAM",
            "header": {"HD": hd, "SQ": sq, "RG": rg, "PG": pg, "CO": co},
            "records": records,
        }
