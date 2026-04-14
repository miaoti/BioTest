"""
HTSJDK runner: Java subprocess parser for VCF and SAM.

Invokes BioTestHarness.jar via subprocess. The harness outputs
canonical JSON to stdout.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Optional

from .base import ParserRunner, RunnerResult
from ..config import HARNESSES_DIR, JAVA_CMD, SUBPROCESS_TIMEOUT_S

logger = logging.getLogger(__name__)

# Expected location of the built harness JAR (fat JAR with HTSJDK bundled)
HARNESS_JAR = HARNESSES_DIR / "java" / "build" / "libs" / "biotest-harness-all.jar"


class HTSJDKRunner(ParserRunner):
    """Parser runner using HTSJDK via Java subprocess."""

    def __init__(self, jar_path: Optional[Path] = None, java_cmd: str = JAVA_CMD):
        self._jar_path = jar_path or HARNESS_JAR
        self._java_cmd = java_cmd

    @property
    def name(self) -> str:
        return "htsjdk"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        # Check Java is on PATH
        if not shutil.which(self._java_cmd):
            logger.warning("Java not found on PATH")
            return False
        # Check harness JAR exists
        if not self._jar_path.exists():
            logger.warning("HTSJDK harness JAR not found at %s", self._jar_path)
            return False
        return True

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
                stderr="HTSJDK harness not available (check Java and JAR)",
            )

        # Copy files to temp dir with ASCII path (avoids Windows Unicode issues)
        tmp_dir = tempfile.mkdtemp(prefix="biotest_")
        tmp_jar = Path(tmp_dir) / "harness.jar"
        tmp_input = Path(tmp_dir) / f"input.{format_type.lower()}"
        shutil.copy2(self._jar_path, tmp_jar)
        shutil.copy2(input_path, tmp_input)

        cmd = [
            self._java_cmd,
            "-jar", str(tmp_jar),
            format_type.upper(),
            str(tmp_input),
        ]

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
                stderr=f"HTSJDK timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except json.JSONDecodeError as e:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=f"Invalid JSON from HTSJDK harness: {e}",
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
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
