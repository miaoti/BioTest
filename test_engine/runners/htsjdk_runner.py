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

    def __init__(
        self,
        jar_path: Optional[Path] = None,
        java_cmd: str = JAVA_CMD,
        coverage_jvm_args: Optional[str] = None,
        coverage_exec_dir: Optional[Path] = None,
    ):
        self._jar_path = jar_path or HARNESS_JAR
        self._java_cmd = java_cmd
        self._coverage_jvm_args = coverage_jvm_args
        self._coverage_exec_dir = coverage_exec_dir

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

        _cov_exec_tmp = None  # Track temp exec file for post-run merge
        cmd = [self._java_cmd]
        # Inject coverage JVM args (e.g., JaCoCo agent) BEFORE -jar
        if self._coverage_jvm_args:
            import re
            # Write exec to ASCII temp dir (avoids Unicode path issues),
            # then merge back to persistent dir after the run
            tmp_exec = Path(tmp_dir) / "jacoco.exec"
            # Copy JaCoCo agent JAR to temp dir (same Unicode workaround as harness JAR)
            agent_match = re.search(r'-javaagent:([^\s=]+)', self._coverage_jvm_args)
            jvm_arg = self._coverage_jvm_args
            if agent_match:
                agent_src = Path(agent_match.group(1))
                if agent_src.exists():
                    tmp_agent = Path(tmp_dir) / "jacocoagent.jar"
                    shutil.copy2(agent_src, tmp_agent)
                    jvm_arg = jvm_arg.replace(agent_match.group(1), str(tmp_agent))
            jvm_arg = jvm_arg.replace("{destfile}", str(tmp_exec))
            cmd.extend(jvm_arg.split())
            _cov_exec_tmp = tmp_exec
        cmd.extend(["-jar", str(tmp_jar), format_type.upper(), str(tmp_input)])

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
            # Merge JaCoCo exec data to persistent dir before cleanup
            if _cov_exec_tmp and _cov_exec_tmp.exists() and self._coverage_exec_dir:
                try:
                    dest = self._coverage_exec_dir.resolve()
                    dest.mkdir(parents=True, exist_ok=True)
                    dest_exec = dest / "jacoco.exec"
                    if dest_exec.exists():
                        # Append: read both and concatenate (JaCoCo exec format is appendable)
                        with open(dest_exec, "ab") as out, open(_cov_exec_tmp, "rb") as inp:
                            out.write(inp.read())
                    else:
                        shutil.copy2(_cov_exec_tmp, dest_exec)
                except OSError as e:
                    logger.warning("Failed to merge JaCoCo exec: %s", e)
            shutil.rmtree(tmp_dir, ignore_errors=True)
