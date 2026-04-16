"""
Pysam Docker runner: subprocess parser for VCF and SAM via Docker container.

When pysam cannot be pip-installed (e.g., on Windows where HTSlib won't
compile), this runner invokes the pysam harness inside a Docker container.

The container image must be pre-built:
    python harnesses/pysam/build_docker.py

CRITICAL: pysam uses 0-based coordinates for ALL formats (including VCF).
The Docker harness adds +1 to POS for both VCF and SAM.
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

logger = logging.getLogger(__name__)

DOCKER_IMAGE = "biotest-pysam:latest"


class PysamDockerRunner(ParserRunner):
    """Parser runner using pysam via Docker subprocess.

    When coverage_dir is set, passes --coverage to the container harness,
    which runs under coverage.py and writes .coverage.<pid> files to the
    mounted volume. The host combines them after Phase C completes.
    """

    def __init__(self, image: str = DOCKER_IMAGE, coverage_dir: Optional[Path] = None):
        self._image = image
        self._available: Optional[bool] = None
        self._coverage_dir = coverage_dir

    @property
    def name(self) -> str:
        return "pysam"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available

        # Check Docker is on PATH
        if not shutil.which("docker"):
            self._available = False
            return False

        # Check Docker daemon is running and image exists
        try:
            proc = subprocess.run(
                ["docker", "image", "inspect", self._image],
                capture_output=True, timeout=10,
            )
            self._available = proc.returncode == 0
        except Exception:
            self._available = False

        if not self._available:
            logger.warning(
                "pysam Docker image '%s' not found. "
                "Build with: python harnesses/pysam/build_docker.py",
                self._image,
            )
        return self._available

    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = 60.0,
    ) -> RunnerResult:
        if not self.is_available():
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=(
                    f"pysam Docker image '{self._image}' not available. "
                    f"Build with: python harnesses/pysam/build_docker.py"
                ),
            )

        fmt = format_type.upper()

        # Copy input to temp dir with ASCII path (avoids Windows Unicode issues)
        tmp_dir = tempfile.mkdtemp(prefix="biotest_pysam_")
        tmp_input = Path(tmp_dir) / f"input.{fmt.lower()}"
        try:
            tmp_input.write_bytes(input_path.read_bytes())
        except OSError as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="crash",
                stderr=f"Failed to copy input file: {e}",
            )

        # Docker bind mount path (forward slashes for Docker on Windows)
        mount_path = str(tmp_dir).replace("\\", "/")

        cmd = [
            "docker", "run", "--rm",
            "-v", f"{mount_path}:/data",
        ]

        # Mount coverage output dir if coverage is enabled
        if self._coverage_dir:
            self._coverage_dir.mkdir(parents=True, exist_ok=True)
            cov_mount = str(self._coverage_dir.resolve()).replace("\\", "/")
            cmd.extend(["-v", f"{cov_mount}:/cov"])

        cmd.append(self._image)

        # Pass --coverage flag to harness if coverage dir is set
        if self._coverage_dir:
            cmd.extend(["--coverage", "/cov"])

        cmd.extend([fmt, f"/data/input.{fmt.lower()}"])

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
                stderr=f"pysam Docker timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except json.JSONDecodeError as e:
            harness_stderr = (proc.stderr or "")[:2048] if "proc" in dir() else ""
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=f"Invalid JSON from pysam Docker harness: {e}\n--- harness stderr ---\n{harness_stderr}",
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
