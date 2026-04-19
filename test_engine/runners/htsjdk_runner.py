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

    # Opt-in to the base class write-roundtrip contract. The implementation
    # below (run_write_roundtrip) shells out to BioTestHarness.jar's
    # `--mode write_roundtrip` CLI — see harnesses/java/BioTestHarness.java
    # (writeRoundtripVcf + forceVcfVersionToV42).
    supports_write_roundtrip: bool = True

    # Rank 5 — opt in to query-method MRs. Both branches dispatch to
    # BioTestHarness.jar's `--mode discover_methods` and `--mode query`,
    # which use java.lang.reflect to enumerate / invoke public scalar
    # getters on VariantContext (VCF) or SAMRecord (SAM).
    supports_query_methods: bool = True

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
        try:
            shutil.copy2(self._jar_path, tmp_jar)
            shutil.copy2(input_path, tmp_input)
        except OSError as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="crash",
                stderr=f"Failed to stage harness/input in temp dir: {e}",
            )

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

    def run_write_roundtrip(
        self,
        input_path: Path,
        format_type: str = "VCF",
        timeout_s: float = SUBPROCESS_TIMEOUT_S,
    ) -> RunnerResult:
        """Parse + re-serialize via htsjdk's native writer.

        Supports both VCF (VCFWriter / VariantContextWriterBuilder) and
        SAM (SAMFileWriterFactory / SAMTextWriter). Returns a
        RunnerResult whose `canonical_json["rewritten_text"]` holds the
        rewritten file text. Writer / encoder classes hit here are
        invisible to parse-only flows.
        """
        fmt = format_type.upper()
        if fmt not in ("VCF", "SAM"):
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="ineligible",
                stderr=f"HTSJDKRunner.run_write_roundtrip: unknown format {fmt}",
            )

        if not self.is_available():
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=fmt,
                error_type="parse_error",
                stderr="HTSJDK harness not available (check Java and JAR)",
            )

        ext = ".vcf" if fmt == "VCF" else ".sam"
        tmp_dir = tempfile.mkdtemp(prefix="biotest_rt_")
        tmp_jar = Path(tmp_dir) / "harness.jar"
        tmp_input = Path(tmp_dir) / f"input{ext}"
        try:
            shutil.copy2(self._jar_path, tmp_jar)
            shutil.copy2(input_path, tmp_input)
        except OSError as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=fmt,
                error_type="crash",
                stderr=f"Failed to stage harness/input in temp dir: {e}",
            )

        _cov_exec_tmp = None
        cmd: list[str] = [self._java_cmd]
        if self._coverage_jvm_args:
            import re
            tmp_exec = Path(tmp_dir) / "jacoco.exec"
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
        cmd.extend([
            "-jar", str(tmp_jar),
            "--mode", "write_roundtrip",
            fmt,
            str(tmp_input),
        ])
        # VCF writer variant rotation: htsjdk's VariantContextWriterBuilder
        # has two code paths we care about — the minimal clearOptions() path
        # ("standard") and the defaults+buffered() path ("advanced"). The
        # harness exposes both via --writer-variant. We deterministically
        # pick one per input by hashing the file bytes so repeated runs on
        # the same seed use the same variant (stable coverage attribution)
        # but different seeds spread evenly across both paths.
        if fmt == "VCF":
            import hashlib
            try:
                with open(input_path, "rb") as _f:
                    h = hashlib.sha1(_f.read(8192)).hexdigest()
                variant = "advanced" if (int(h[:2], 16) & 1) else "standard"
            except OSError:
                variant = "standard"
            cmd.extend(["--writer-variant", variant])

        t0 = time.monotonic()
        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                timeout=timeout_s, creationflags=creation_flags,
            )
            duration = (time.monotonic() - t0) * 1000

            if proc.returncode != 0:
                return RunnerResult(
                    success=False,
                    parser_name=self.name,
                    format_type=fmt,
                    exit_code=proc.returncode,
                    stderr=proc.stderr,
                    error_type="crash",
                    duration_ms=duration,
                )

            return RunnerResult(
                success=True,
                # Embed raw text in canonical_json["rewritten_text"] so
                # the signature still returns a RunnerResult.
                canonical_json={"rewritten_text": proc.stdout},
                parser_name=self.name,
                format_type=fmt,
                exit_code=0,
                stderr=proc.stderr,
                duration_ms=duration,
            )
        except subprocess.TimeoutExpired:
            return RunnerResult(
                success=False, parser_name=self.name, format_type=fmt,
                error_type="timeout",
                stderr=f"HTSJDK write_roundtrip timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False, parser_name=self.name, format_type=fmt,
                error_type="crash", stderr=str(e),
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        finally:
            if _cov_exec_tmp and _cov_exec_tmp.exists() and self._coverage_exec_dir:
                try:
                    dest = self._coverage_exec_dir.resolve()
                    dest.mkdir(parents=True, exist_ok=True)
                    dest_exec = dest / "jacoco.exec"
                    if dest_exec.exists():
                        with open(dest_exec, "ab") as out, open(_cov_exec_tmp, "rb") as inp:
                            out.write(inp.read())
                    else:
                        shutil.copy2(_cov_exec_tmp, dest_exec)
                except OSError as e:
                    logger.warning("Failed to merge JaCoCo exec (roundtrip): %s", e)
            shutil.rmtree(tmp_dir, ignore_errors=True)

    # ------------------------------------------------------------------
    # Rank 5 — query-method MRs (delegated to BioTestHarness.jar)
    # ------------------------------------------------------------------
    def discover_query_methods(self, format_type: str) -> list[dict]:
        """Subprocess wrapper around `--mode discover_methods <FORMAT>`."""
        if not self.is_available():
            return []
        fmt = format_type.upper()
        if fmt not in ("VCF", "SAM"):
            return []
        cmd = [self._java_cmd, "-jar", str(self._jar_path),
               "--mode", "discover_methods", fmt]
        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                timeout=30.0, creationflags=creation_flags,
            )
            if proc.returncode != 0:
                logger.debug(
                    "htsjdk discover_methods failed (rc=%d): %s",
                    proc.returncode, proc.stderr[:200],
                )
                return []
            import json as _json
            payload = _json.loads(proc.stdout)
            return payload.get("methods", [])
        except Exception as e:
            logger.debug("htsjdk discover_methods raised: %s", e)
            return []

    def run_query_methods(
        self,
        input_path: Path,
        format_type: str,
        method_names: list[str],
        timeout_s: float = SUBPROCESS_TIMEOUT_S,
    ) -> RunnerResult:
        """Subprocess wrapper around `--mode query <FORMAT> <PATH> --methods …`.

        Runs the JaCoCo agent alongside the query so htsjdk's invocation
        of `isStructural()`, `isBiallelic()`, `getNAlleles()`, etc.
        actually shows up in the coverage report. Without the agent the
        query methods execute invisibly to measurement and the Rank 5
        lever looks like a no-op even when it's exercising real library
        code paths.

        The Java side (`queryVcf` / `querySam`) parses the file, takes
        the first record, invokes each method via
        `java.lang.reflect.Method`, and prints
        `{"method_results": {…}}`. We pack that into a
        RunnerResult.canonical_json so the query-consensus oracle can
        compare it against other voters."""
        fmt = format_type.upper()
        if fmt not in ("VCF", "SAM"):
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="ineligible",
                stderr=f"HTSJDKRunner.run_query_methods: unknown format {fmt}",
            )
        if not self.is_available():
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=fmt, error_type="parse_error",
                stderr="HTSJDK harness not available",
            )
        if not method_names:
            return RunnerResult(
                success=True, parser_name=self.name,
                format_type=fmt, exit_code=0,
                canonical_json={"method_results": {}},
            )

        # Stage harness JAR + input in an ASCII temp dir (same Unicode-path
        # workaround as run / run_write_roundtrip).
        tmp_dir = tempfile.mkdtemp(prefix="biotest_query_")
        tmp_jar = Path(tmp_dir) / "harness.jar"
        tmp_input = Path(tmp_dir) / f"input.{fmt.lower()}"
        try:
            shutil.copy2(self._jar_path, tmp_jar)
            shutil.copy2(input_path, tmp_input)
        except OSError as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=fmt, error_type="crash",
                stderr=f"Failed to stage harness/input: {e}",
            )

        _cov_exec_tmp: Optional[Path] = None
        cmd: list[str] = [self._java_cmd]
        if self._coverage_jvm_args:
            import re
            tmp_exec = Path(tmp_dir) / "jacoco.exec"
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
        cmd.extend([
            "-jar", str(tmp_jar),
            "--mode", "query", fmt, str(tmp_input),
            "--methods", ",".join(method_names),
        ])

        t0 = time.monotonic()
        try:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                timeout=timeout_s, creationflags=creation_flags,
            )
            duration = (time.monotonic() - t0) * 1000
            if proc.returncode != 0:
                return RunnerResult(
                    success=False, parser_name=self.name,
                    format_type=fmt, exit_code=proc.returncode,
                    error_type="crash", stderr=proc.stderr[:500],
                    duration_ms=duration,
                )
            import json as _json
            payload = _json.loads(proc.stdout)
            return RunnerResult(
                success=True, parser_name=self.name,
                format_type=fmt, exit_code=0,
                canonical_json=payload,
                duration_ms=duration,
            )
        except subprocess.TimeoutExpired:
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=fmt, error_type="timeout",
                stderr=f"htsjdk query timed out after {timeout_s}s",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=fmt, error_type="crash", stderr=str(e),
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        finally:
            # Merge the JaCoCo exec data from this query run into the
            # persistent coverage dir so the Phase D report reflects the
            # query-method code paths we just exercised.
            if _cov_exec_tmp and _cov_exec_tmp.exists() and self._coverage_exec_dir:
                try:
                    dest = self._coverage_exec_dir.resolve()
                    dest.mkdir(parents=True, exist_ok=True)
                    dest_exec = dest / "jacoco.exec"
                    if dest_exec.exists():
                        with open(dest_exec, "ab") as out, open(_cov_exec_tmp, "rb") as inp:
                            out.write(inp.read())
                    else:
                        shutil.copy2(_cov_exec_tmp, dest_exec)
                except OSError as e:
                    logger.warning("Failed to merge JaCoCo exec (query): %s", e)
            shutil.rmtree(tmp_dir, ignore_errors=True)
