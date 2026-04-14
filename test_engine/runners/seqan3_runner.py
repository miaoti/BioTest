"""
SeqAn3 runner: C++ subprocess parser for SAM format.

Invokes the compiled biotest_harness binary. The binary outputs
canonical JSON to stdout.

CRITICAL: SeqAn3 converts SAM 1-based POS to 0-based internally
(format_sam.hpp:420). The C++ harness must add +1 before output.

SeqAn3 does NOT support VCF format.
"""

from __future__ import annotations

import json
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from .base import ParserRunner, RunnerResult
from ..config import HARNESSES_DIR, SUBPROCESS_TIMEOUT_S

logger = logging.getLogger(__name__)

# Expected location of the compiled binary
HARNESS_BIN = HARNESSES_DIR / "cpp" / "build" / "biotest_harness.exe"


class SeqAn3Runner(ParserRunner):
    """Parser runner using SeqAn3 via C++ subprocess (SAM only)."""

    def __init__(self, binary_path: Optional[Path] = None):
        self._binary_path = binary_path or HARNESS_BIN

    @property
    def name(self) -> str:
        return "seqan3"

    @property
    def supported_formats(self) -> set[str]:
        return {"SAM"}

    def is_available(self) -> bool:
        return self._binary_path.exists()

    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = SUBPROCESS_TIMEOUT_S,
    ) -> RunnerResult:
        if not self.is_available():
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=f"SeqAn3 harness not found at {self._binary_path}",
            )

        if format_type.upper() != "SAM":
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr="SeqAn3 only supports SAM format",
            )

        cmd = [str(self._binary_path), "SAM", str(input_path)]

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
                timeout=timeout_s,
                creationflags=creation_flags,
            )
            duration = (time.monotonic() - t0) * 1000

            if proc.returncode != 0:
                return RunnerResult(
                    success=False,
                    parser_name=self.name,
                    format_type=format_type,
                    exit_code=proc.returncode,
                    stderr=proc.stderr,
                    error_type="crash",
                    duration_ms=duration,
                )

            canonical = json.loads(proc.stdout)
            return RunnerResult(
                success=True,
                canonical_json=canonical,
                parser_name=self.name,
                format_type=format_type,
                exit_code=0,
                stderr=proc.stderr,
                duration_ms=duration,
            )

        except subprocess.TimeoutExpired:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="timeout",
                stderr=f"SeqAn3 timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except json.JSONDecodeError as e:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=f"Invalid JSON from SeqAn3 harness: {e}",
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
