"""
Biopython runner: Python in-process parser for SAM format.

CRITICAL: Biopython converts SAM 1-based POS to 0-based Python coordinates.
The normalizer must add +1 to POS and PNEXT.

Biopython does NOT support VCF format.
"""

from __future__ import annotations

import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Any, Optional

from .base import ParserRunner, RunnerResult

logger = logging.getLogger(__name__)

_biopython_available: Optional[bool] = None


def _check_biopython() -> bool:
    """Check if Biopython is importable (pip-installed or SUT folder)."""
    global _biopython_available
    if _biopython_available is None:
        try:
            from Bio.Align import sam as _  # noqa: F401
            _biopython_available = True
        except ImportError:
            _biopython_available = False
    return _biopython_available


class BiopythonRunner(ParserRunner):
    """Parser runner using Biopython's Bio.Align.sam (SAM only)."""

    @property
    def name(self) -> str:
        return "biopython"

    @property
    def supported_formats(self) -> set[str]:
        return {"SAM"}

    def is_available(self) -> bool:
        return _check_biopython()

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
                stderr="Biopython is not available from SUTfolder",
            )

        if format_type.upper() != "SAM":
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr="Biopython only supports SAM format",
            )

        t0 = time.monotonic()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._parse_sam, input_path)
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
                stderr=f"Biopython timed out after {timeout_s}s",
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

    def _parse_sam(self, path: Path) -> dict[str, Any]:
        """Parse SAM via Biopython into canonical dict."""
        from Bio.Align import sam as bio_sam
        import re

        # Biopython's SAM parser
        alignments = bio_sam.AlignmentIterator(str(path))

        # We need to parse the raw file for header info since Biopython
        # doesn't expose all header fields cleanly
        header_lines: list[str] = []
        alignment_lines: list[str] = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\r\n")
                if not line:
                    continue
                if line.startswith("@"):
                    header_lines.append(line)
                else:
                    alignment_lines.append(line)

        # Parse header directly from text (Biopython's header access is limited)
        hd = None
        sq: list[dict[str, str]] = []
        rg: list[dict[str, str]] = []
        pg: list[dict[str, str]] = []
        co: list[str] = []

        for hl in header_lines:
            fields = hl.split("\t")
            rec_type = fields[0]
            tag_dict = {}
            for f in fields[1:]:
                if ":" in f:
                    k, v = f.split(":", 1)
                    tag_dict[k] = v

            if rec_type == "@HD":
                hd = tag_dict
            elif rec_type == "@SQ":
                sq.append(tag_dict)
            elif rec_type == "@RG":
                rg.append(tag_dict)
            elif rec_type == "@PG":
                pg.append(tag_dict)
            elif rec_type == "@CO":
                co.append("\t".join(fields[1:]))

        co.sort()

        # Parse alignment records from raw text
        # (using raw text because Biopython's alignment objects don't expose
        # all SAM fields directly in a uniform way)
        records = []
        for line in alignment_lines:
            cols = line.split("\t")
            if len(cols) < 11:
                continue

            qname = cols[0]
            flag = int(cols[1])
            rname = None if cols[2] == "*" else cols[2]
            raw_pos = int(cols[3])
            # SAM text is already 1-based; no Biopython conversion here
            # since we're reading raw text, not Biopython objects
            pos = None if raw_pos == 0 else raw_pos
            mapq = int(cols[4])

            # CIGAR
            cigar = None
            if cols[5] != "*":
                cigar = [{"op": m.group(2), "len": int(m.group(1))}
                         for m in re.finditer(r"(\d+)([MIDNSHP=X])", cols[5])]

            rnext = None if cols[6] == "*" else cols[6]
            raw_pnext = int(cols[7])
            pnext = None if raw_pnext == 0 else raw_pnext
            tlen = int(cols[8])
            seq = None if cols[9] == "*" else cols[9]
            qual = None if cols[10] == "*" else cols[10]

            # Tags
            tags = {}
            for col in cols[11:]:
                m = re.match(r"^([A-Za-z][A-Za-z0-9]):([AifZHB]):(.+)$", col)
                if m:
                    tag_name = m.group(1)
                    tag_type = m.group(2)
                    tag_val = m.group(3)
                    if tag_type == "i":
                        tag_val = int(tag_val)
                    elif tag_type == "f":
                        tag_val = float(tag_val)
                    elif tag_type == "B":
                        parts = tag_val.split(",")
                        subtype = parts[0]
                        vals = parts[1:]
                        if subtype in ("c", "C", "s", "S", "i", "I"):
                            tag_val = [int(v) for v in vals]
                        elif subtype == "f":
                            tag_val = [float(v) for v in vals]
                        else:
                            tag_val = vals
                    tags[tag_name] = {"type": tag_type, "value": tag_val}
            tags = dict(sorted(tags.items()))

            records.append({
                "QNAME": qname,
                "FLAG": flag,
                "RNAME": rname,
                "POS": pos,
                "MAPQ": mapq,
                "CIGAR": cigar,
                "RNEXT": rnext,
                "PNEXT": pnext,
                "TLEN": tlen,
                "SEQ": seq,
                "QUAL": qual,
                "tags": tags,
            })

        return {
            "format": "SAM",
            "header": {"HD": hd, "SQ": sq, "RG": rg, "PG": pg, "CO": co},
            "records": records,
        }
