"""
Reference runner: Python-native parser using the canonical normalizers.

This runner uses the built-in VCF/SAM text normalizers (no external library).
It serves as the baseline "reference implementation" for testing:
- Metamorphic oracle: compare parse(x) vs parse(T(x)) using this runner
- Can always run regardless of external dependencies

This is NOT a SUT (System Under Test) — it's the test framework's own parser.
For differential testing you need at least one real SUT runner (htsjdk, pysam, etc).
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .base import ParserRunner, RunnerResult
from ..canonical.vcf_normalizer import normalize_vcf_text
from ..canonical.sam_normalizer import normalize_sam_text


class ReferenceRunner(ParserRunner):
    """Parser runner using built-in Python normalizers."""

    @property
    def name(self) -> str:
        return "reference"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        return True  # Always available (no external deps)

    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        t0 = time.monotonic()
        try:
            lines = input_path.read_text(encoding="utf-8").splitlines(keepends=True)
            fmt = format_type.upper()

            if fmt == "VCF":
                canonical = normalize_vcf_text(lines)
            elif fmt == "SAM":
                canonical = normalize_sam_text(lines)
            else:
                return RunnerResult(
                    success=False,
                    parser_name=self.name,
                    format_type=format_type,
                    error_type="ineligible",
                    stderr=f"Reference runner does not support format {format_type!r}",
                )

            duration = (time.monotonic() - t0) * 1000
            return RunnerResult(
                success=True,
                canonical_json=canonical.model_dump(),
                parser_name=self.name,
                format_type=format_type,
                duration_ms=duration,
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
