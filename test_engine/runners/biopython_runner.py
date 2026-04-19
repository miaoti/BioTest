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

    # Rank 5 — opt in to query-method MRs. Bio.Align Alignment objects
    # expose a handful of scalar properties (target, query, score) that
    # we introspect via stdlib reflection.
    supports_query_methods: bool = True

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
            # Ineligible, not malformed. Consensus discards this signal.
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="ineligible",
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
        """
        Parse SAM via Biopython's AlignmentIterator into canonical dict.

        Hybrid approach:
        - POS is extracted from Biopython's parsed alignment object
          (0-based coordinates[0][0]) and gets +1 for canonical 1-based.
        - FLAG, MAPQ, QNAME, RNAME, SEQ are extracted from Biopython objects.
        - CIGAR, RNEXT, PNEXT, TLEN, QUAL, and full TAGS are extracted from
          the corresponding raw text line, because Biopython's Alignment API
          does not expose these fields uniformly (it consumes MD/AS tags, and
          hides mate-pair info).

        If Biopython's AlignmentIterator fails on any record, we raise a
        RuntimeError so the runner reports it as a crash/DET.
        """
        from Bio.Align import sam as bio_sam
        import re

        # --- Pre-read raw lines for header + fallback field extraction ---
        header_lines: list[str] = []
        alignment_lines: list[str] = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.rstrip("\r\n")
                if not stripped:
                    continue
                if stripped.startswith("@"):
                    header_lines.append(stripped)
                else:
                    alignment_lines.append(stripped)

        # --- Parse header from raw text (Biopython header access is limited) ---
        hd = None
        sq: list[dict[str, str]] = []
        rg: list[dict[str, str]] = []
        pg: list[dict[str, str]] = []
        co: list[str] = []

        for hl in header_lines:
            fields = hl.split("\t")
            rec_type = fields[0]
            tag_dict = {}
            for fld in fields[1:]:
                if ":" in fld:
                    k, v = fld.split(":", 1)
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

        # --- Parse alignment records via Biopython's native iterator ---
        records: list[dict[str, Any]] = []

        try:
            for idx, alignment in enumerate(bio_sam.AlignmentIterator(str(path))):

                # ----------------------------------------------------------
                # FROM BIOPYTHON: fields that Biopython actively parses
                # ----------------------------------------------------------

                # POS: Biopython stores as 0-based in coordinates[0][0].
                # CRITICAL: add +1 to convert to canonical 1-based.
                bio_pos_0based = alignment.coordinates[0][0]
                pos = int(bio_pos_0based) + 1  # 0-based -> 1-based

                # FLAG, MAPQ, QNAME, RNAME — directly on the object
                flag = alignment.flag
                mapq = alignment.mapq
                qname = alignment.query.id
                rname = alignment.target.id

                # SEQ — from query sequence
                seq_obj = alignment.query.seq
                seq = str(seq_obj) if seq_obj is not None else None

                # ----------------------------------------------------------
                # FROM RAW TEXT: fields Biopython does not expose cleanly
                # (CIGAR, RNEXT, PNEXT, TLEN, QUAL, full TAGS)
                # ----------------------------------------------------------

                if idx < len(alignment_lines):
                    cols = alignment_lines[idx].split("\t")
                else:
                    cols = []

                # CIGAR (col 5) — Biopython consumes it into coordinates
                cigar = None
                if len(cols) > 5 and cols[5] != "*":
                    cigar = [{"op": m.group(2), "len": int(m.group(1))}
                             for m in re.finditer(r"(\d+)([MIDNSHP=X])", cols[5])]

                # RNEXT (col 6), PNEXT (col 7), TLEN (col 8)
                rnext = None
                if len(cols) > 6 and cols[6] != "*":
                    rnext = cols[6]

                raw_pnext = int(cols[7]) if len(cols) > 7 else 0
                pnext = None if raw_pnext == 0 else raw_pnext

                tlen = int(cols[8]) if len(cols) > 8 else 0

                # QUAL (col 10) — Biopython converts to phred_quality ints;
                # canonical schema expects the original ASCII string
                qual = None
                if len(cols) > 10 and cols[10] != "*":
                    qual = cols[10]

                # TAGS (cols 11+) — Biopython consumes some tags (MD -> alignment,
                # AS -> score) so we extract ALL tags from raw text for completeness
                tags: dict[str, Any] = {}
                if len(cols) > 11:
                    for col in cols[11:]:
                        m = re.match(r"^([A-Za-z][A-Za-z0-9]):([AifZHB]):(.+)$", col)
                        if m:
                            tag_name = m.group(1)
                            tag_type = m.group(2)
                            tag_val: Any = m.group(3)
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

                # Handle unmapped reads: if FLAG 0x4 is set, POS should be None
                if flag & 0x4:
                    pos = None
                    rname = None

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

        except Exception as e:
            # If Biopython crashes on a (possibly mutated) SAM file,
            # propagate as RuntimeError so the runner reports it as a
            # crash/DET — this is a legitimate finding.
            raise RuntimeError(
                f"Biopython AlignmentIterator failed on record {len(records)}: {e}"
            ) from e

        return {
            "format": "SAM",
            "header": {"HD": hd, "SQ": sq, "RG": rg, "PG": pg, "CO": co},
            "records": records,
        }

    # ------------------------------------------------------------------
    # Rank 5 — query-method MRs
    # ------------------------------------------------------------------
    def discover_query_methods(self, format_type: str) -> list[dict]:
        from .introspection import get_scalar_query_methods
        if format_type.upper() != "SAM":
            return []
        if not self.is_available():
            return []
        try:
            from Bio.Align import Alignment
            return get_scalar_query_methods(Alignment)
        except Exception:
            return []

    def run_query_methods(
        self,
        input_path: Path,
        format_type: str,
        method_names: list[str],
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        from .introspection import run_methods_on_record
        import time as _time
        if format_type.upper() != "SAM":
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="ineligible",
                stderr="BiopythonRunner.run_query_methods supports SAM only",
            )
        if not self.is_available():
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type="SAM", error_type="ineligible",
                stderr="biopython not available",
            )
        t0 = _time.monotonic()
        try:
            from Bio import Align
            it = Align.parse(str(input_path), "sam")
            rec = next(iter(it), None)
            if rec is None:
                return RunnerResult(
                    success=True, parser_name=self.name,
                    format_type="SAM", exit_code=0,
                    canonical_json={"method_results": {}},
                    duration_ms=(_time.monotonic() - t0) * 1000,
                )
            results = run_methods_on_record(rec, method_names)
            return RunnerResult(
                success=True, parser_name=self.name,
                format_type="SAM", exit_code=0,
                canonical_json={"method_results": results},
                duration_ms=(_time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type="SAM", error_type="crash",
                stderr=f"biopython query: {e}",
                duration_ms=(_time.monotonic() - t0) * 1000,
            )
