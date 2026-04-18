"""
HTSlib runner: shells out to the samtools/bcftools CLI — the upstream
reference implementation of hts-specs.

Why this exists separately from PysamRunner / SeqAn3Runner:
  - pysam is a Python BINDING over libhts. Same C library under the hood
    as samtools, but a different code path (Cython wrappers + Python
    object construction). Bugs in those wrappers are orthogonal to the
    CLI's round-trip.
  - SeqAn3 is an independent C++ library — not related to htslib at all.
  - samtools / bcftools are the reference CLIs maintained by the same
    group that owns the SAM/VCF specs (github.com/samtools). When they
    emit output, that output is the closest thing to "ground truth" we
    have without running the spec's formal grammar.

In the consensus oracle (test_engine/oracles/consensus.py), HTSlib is
the `AUTHORITATIVE_PARSERS` tie-breaker — if three parsers produce three
different outputs, HTSlib's vote picks the winner. It does NOT outweigh
a simple majority; it only resolves ties.

Strategy per format:
  - VCF: `bcftools view <file>` → canonical VCF text (header + records)
         → fed through normalize_vcf_text() to produce canonical JSON.
  - SAM: `samtools view -h <file>` → canonical SAM text
         → fed through normalize_sam_text().

This is a PARSE + RE-EMIT round-trip: we're asking htslib to read the
file and print its own canonical serialization. Any bug in htslib's
understanding of the spec will surface in that output, which is exactly
what we want a reference SUT to expose.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from .base import ParserRunner, RunnerResult
from ..canonical.vcf_normalizer import normalize_vcf_text
from ..canonical.sam_normalizer import normalize_sam_text
from ..config import SUBPROCESS_TIMEOUT_S

logger = logging.getLogger(__name__)


class HTSlibRunner(ParserRunner):
    """CLI-based runner over bcftools (VCF) and samtools (SAM).

    Gold-standard reference implementation — see module docstring.
    """

    def __init__(
        self,
        bcftools_path: Optional[str] = None,
        samtools_path: Optional[str] = None,
    ):
        self._bcftools = bcftools_path or shutil.which("bcftools")
        self._samtools = samtools_path or shutil.which("samtools")

    @property
    def name(self) -> str:
        return "htslib"

    @property
    def supported_formats(self) -> set[str]:
        formats: set[str] = set()
        if self._bcftools:
            formats.add("VCF")
        if self._samtools:
            formats.add("SAM")
        return formats

    def is_available(self) -> bool:
        return bool(self._bcftools or self._samtools)

    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = SUBPROCESS_TIMEOUT_S,
    ) -> RunnerResult:
        fmt = format_type.upper()

        # Ineligibility path #1: format is outside this runner class's
        # supported surface entirely (BAM/CRAM/FASTA/...). The consensus
        # oracle discards "ineligible" results — they do NOT count as a
        # vote at all.
        if fmt not in ("VCF", "SAM"):
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=fmt,
                error_type="ineligible",
                stderr=f"HTSlibRunner does not support format {format_type!r}",
            )

        if fmt == "VCF":
            binary = self._bcftools
            # `bcftools view` prints the full VCF (header + records) after
            # parsing + re-serializing through libhts.
            cmd = [binary, "view", str(input_path)] if binary else []
        else:  # SAM
            binary = self._samtools
            # `-h` includes the header; without it we lose @HD/@SQ/@PG.
            cmd = [binary, "view", "-h", str(input_path)] if binary else []

        if not binary:
            # Ineligibility path #2: the correct CLI isn't installed for
            # this format (bcftools for VCF, samtools for SAM). Flag as
            # INELIGIBLE rather than "parse_error" — there's no evidence
            # the file is malformed; the SUT simply can't vote.
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=fmt,
                error_type="ineligible",
                stderr=f"HTSlib CLI for {fmt} not found in PATH "
                       f"({'bcftools' if fmt == 'VCF' else 'samtools'} missing)",
            )

        t0 = time.monotonic()
        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_s,
                creationflags=creation_flags,
            )
            duration = (time.monotonic() - t0) * 1000

            if proc.returncode != 0:
                # Reliability guard: classify as parse_error when stderr
                # mentions invalid/malformed — upstream rejection signal.
                err = (proc.stderr or "").lower()
                is_invalid = any(
                    kw in err
                    for kw in ("invalid", "malformed", "parse error", "truncated", "could not parse")
                )
                error_type = "parse_error" if is_invalid else "crash"
                return RunnerResult(
                    success=False,
                    parser_name=self.name,
                    format_type=fmt,
                    exit_code=proc.returncode,
                    stderr=proc.stderr,
                    error_type=error_type,
                    duration_ms=duration,
                )

            # Re-emitted text → canonical JSON via our own normalizer.
            text = proc.stdout or ""
            lines = text.splitlines(keepends=True)

            if fmt == "VCF":
                canonical = normalize_vcf_text(lines)
            else:
                canonical = normalize_sam_text(lines)

            return RunnerResult(
                success=True,
                canonical_json=canonical.model_dump(),
                parser_name=self.name,
                format_type=fmt,
                exit_code=0,
                stderr=proc.stderr,
                duration_ms=duration,
            )

        except subprocess.TimeoutExpired:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=fmt,
                error_type="timeout",
                stderr=f"HTSlib CLI timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=fmt,
                error_type="crash",
                stderr=f"{type(e).__name__}: {e}",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
