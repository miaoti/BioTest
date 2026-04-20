"""
noodles-vcf runner: pure-Rust VCF parser via subprocess harness.

Invokes `harnesses/rust/noodles_harness` — a small Cargo binary wrapping
the noodles-vcf crate — and reads canonical JSON off stdout. Same
contract as seqan3_runner.py.

noodles-vcf uses 1-based POS natively (matches canonical schema); no
coordinate shim needed in the harness.

noodles_harness does NOT support SAM today — adding noodles-sam is a
follow-on harness binary; until then this runner reports `ineligible`
for SAM inputs.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from .base import ParserRunner, RunnerResult
from ..config import HARNESSES_DIR, SUBPROCESS_TIMEOUT_S

logger = logging.getLogger(__name__)

DEFAULT_BIN = HARNESSES_DIR / "rust" / "noodles_harness" / "target" / "release" / "noodles_harness"
if sys.platform == "win32":
    DEFAULT_BIN = DEFAULT_BIN.with_suffix(".exe")


class NoodlesRunner(ParserRunner):
    """Parser runner using noodles-vcf via a compiled Rust binary (VCF only).

    Feature parity with ``HTSJDKRunner`` for VCF:
      - ``run``                 → parse file, emit canonical JSON.
      - ``run_write_roundtrip`` → delegate to the harness's
        ``--mode write_roundtrip`` CLI, which re-serializes through
        ``noodles-vcf``'s ``io::writer::Writer``. Exercises the
        ``src/io/writer`` + ``src/variant`` writer code paths that are
        invisible to parse-only flows (mirror of what htsjdk's
        ``VariantContextWriterBuilder`` paths give us on the Java side).
      - Query methods are **intentionally not implemented** — Rust has
        no runtime reflection. Same choice as seqan3 runner. The
        framework hides query-method MRs from the LLM menu when no
        primary SUT sets ``supports_query_methods=True``.

    Supports two binaries:
    - Standard binary: ``cargo build --release`` output (default).
    - Coverage binary: ``cargo llvm-cov`` instrumented build. When the
      coverage binary is used, ``LLVM_PROFILE_FILE`` is set so each
      invocation writes a new ``.profraw`` next to the other coverage
      artifacts.
    """

    # Opt in to the write-roundtrip contract. Query methods stay off.
    supports_write_roundtrip: bool = True

    def __init__(
        self,
        binary_path: Optional[Path] = None,
        coverage_binary_path: Optional[Path] = None,
        llvm_profile_dir: Optional[Path] = None,
    ):
        self._binary_path = binary_path or DEFAULT_BIN
        self._coverage_binary_path = coverage_binary_path
        self._llvm_profile_dir = llvm_profile_dir

    @property
    def active_binary(self) -> Path:
        """Prefer the coverage-instrumented binary if it exists."""
        if self._coverage_binary_path and self._coverage_binary_path.exists():
            return self._coverage_binary_path
        return self._binary_path

    @property
    def name(self) -> str:
        return "noodles"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF"}

    def is_available(self) -> bool:
        return self._binary_path.exists() or (
            self._coverage_binary_path is not None
            and self._coverage_binary_path.exists()
        )

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
                stderr=(
                    f"noodles_harness not built at {self._binary_path} — "
                    "see harnesses/rust/noodles_harness/README.md"
                ),
            )

        if format_type.upper() != "VCF":
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="ineligible",
                stderr="noodles_harness supports VCF only",
            )

        cmd = [str(self.active_binary), "VCF", str(input_path)]

        env = os.environ.copy()
        if (
            self._coverage_binary_path
            and self.active_binary == self._coverage_binary_path
            and self._llvm_profile_dir
        ):
            self._llvm_profile_dir.mkdir(parents=True, exist_ok=True)
            profile_pattern = str(self._llvm_profile_dir / "noodles-%p-%m.profraw")
            env["LLVM_PROFILE_FILE"] = profile_pattern

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
                env=env,
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
                stderr=f"noodles_harness timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except json.JSONDecodeError as e:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=f"Invalid JSON from noodles_harness: {e}",
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
