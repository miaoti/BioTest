"""
Pysam runner: facade that tries native pysam first, then Docker fallback.

CRITICAL: pysam uses 0-based coordinates for ALL formats (including VCF).
The normalizer must add +1 to POS for both VCF and SAM.

On Linux/macOS, pysam can be pip-installed and runs in-process.
On Windows, pysam requires HTSlib (C library) which won't compile natively.
In that case, the runner falls back to PysamDockerRunner which invokes
a pre-built Docker container.
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Any, Optional

from .base import ParserRunner, RunnerResult

logger = logging.getLogger(__name__)

_pysam_available: Optional[bool] = None


def _check_pysam() -> bool:
    """Check if pysam is importable (pip-installed)."""
    global _pysam_available
    if _pysam_available is None:
        try:
            import pysam  # noqa: F401
            _pysam_available = True
        except ImportError:
            _pysam_available = False
    return _pysam_available


def _get_docker_runner(coverage_dir=None):
    """Lazy-load the Docker runner to avoid circular imports."""
    from .pysam_docker_runner import PysamDockerRunner
    return PysamDockerRunner(coverage_dir=coverage_dir)


class PysamRunner(ParserRunner):
    """
    Facade runner: native pysam in-process if available, Docker fallback otherwise.
    """

    # Opt-in to write_roundtrip contract. Routes to native pysam's
    # VariantFile writer when available, otherwise to the Docker
    # harness's `--mode vcf_write_roundtrip` CLI (see
    # harnesses/pysam/pysam_harness.py::vcf_write_roundtrip).
    supports_write_roundtrip: bool = True

    # Rank 5 — opt in to query-method MRs. Native path uses Python
    # introspection (test_engine.runners.introspection) on the first
    # parsed VariantRecord / AlignedSegment; Docker path delegates to
    # `--mode discover_methods` / `--mode query` in pysam_harness.py.
    supports_query_methods: bool = True

    def __init__(self, coverage_dir: Optional[Path] = None):
        self._docker_runner: Optional[ParserRunner] = None
        self._coverage_dir = coverage_dir

    @property
    def name(self) -> str:
        return "pysam"

    @property
    def supported_formats(self) -> set[str]:
        return {"VCF", "SAM"}

    def _use_native(self) -> bool:
        """Check if native pysam is importable."""
        return _check_pysam()

    def _use_docker(self) -> bool:
        """Check if Docker fallback is available."""
        if self._docker_runner is None:
            self._docker_runner = _get_docker_runner(coverage_dir=self._coverage_dir)
        return self._docker_runner.is_available()

    def is_available(self) -> bool:
        return self._use_native() or self._use_docker()

    def run(
        self,
        input_path: Path,
        format_type: str,
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        if format_type.upper() not in self.supported_formats:
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="ineligible",
                stderr=f"pysam runner does not support format {format_type!r}",
            )

        if not self.is_available():
            return RunnerResult(
                success=False,
                parser_name=self.name,
                format_type=format_type,
                error_type="parse_error",
                stderr=(
                    "pysam is not available. Either pip install pysam (Linux/macOS) "
                    "or build Docker image: python harnesses/pysam/build_docker.py"
                ),
            )

        # Dispatch to Docker if native pysam not available
        if not self._use_native():
            return self._docker_runner.run(input_path, format_type, timeout_s)

        t0 = time.monotonic()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    self._parse, input_path, format_type.upper()
                )
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
                stderr=f"pysam timed out after {timeout_s}s",
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

    def run_write_roundtrip(
        self,
        input_path: Path,
        format_type: str = "VCF",
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        """Parse + re-serialize via pysam's VariantFile / AlignmentFile writer.

        VCF routes through `pysam.VariantFile` (native) or
        `--mode vcf_write_roundtrip` (Docker); SAM routes through
        `pysam.AlignmentFile` (native) or `--mode sam_write_roundtrip`
        (Docker). Returns a RunnerResult whose
        `canonical_json["rewritten_text"]` is the rewritten file text.
        """
        fmt = format_type.upper()
        if fmt not in ("VCF", "SAM"):
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="ineligible",
                stderr=f"PysamRunner.run_write_roundtrip: unknown format {fmt}",
            )

        if not self.is_available():
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=fmt, error_type="parse_error",
                stderr="pysam runtime (native or Docker) not available",
            )

        import os
        import subprocess
        import sys
        import tempfile

        t0 = time.monotonic()
        ext = ".vcf" if fmt == "VCF" else ".sam"

        # --- Native pysam in-process (fast path) ---
        if self._use_native():
            try:
                import pysam
                with tempfile.TemporaryDirectory(prefix="biotest_pysam_rt_") as tmpdir:
                    out_path = os.path.join(tmpdir, f"out{ext}")
                    if fmt == "VCF":
                        src = pysam.VariantFile(str(input_path))
                        writer = pysam.VariantFile(out_path, "w", header=src.header)
                    else:  # SAM
                        src = pysam.AlignmentFile(str(input_path), "r", check_sq=False)
                        writer = pysam.AlignmentFile(out_path, "wh", template=src)
                    try:
                        for rec in src:
                            writer.write(rec)
                    finally:
                        writer.close()
                        src.close()
                    with open(out_path, "r", encoding="utf-8") as f:
                        text = f.read()
                return RunnerResult(
                    success=True,
                    canonical_json={"rewritten_text": text},
                    parser_name=self.name, format_type=fmt, exit_code=0,
                    duration_ms=(time.monotonic() - t0) * 1000,
                )
            except Exception as e:
                return RunnerResult(
                    success=False, parser_name=self.name, format_type=fmt,
                    error_type="crash", stderr=f"native pysam roundtrip: {e}",
                    duration_ms=(time.monotonic() - t0) * 1000,
                )

        # --- Docker fallback (Windows) ---
        mode_flag = "vcf_write_roundtrip" if fmt == "VCF" else "sam_write_roundtrip"
        with tempfile.TemporaryDirectory(prefix="biotest_pysam_rt_") as tmpdir:
            in_path = os.path.join(tmpdir, f"in{ext}")
            out_path = os.path.join(tmpdir, f"out{ext}")
            import shutil as _sh
            _sh.copy2(input_path, in_path)

            mount = tmpdir.replace("\\", "/")
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{mount}:/data",
                "biotest-pysam:latest",
                "--mode", mode_flag,
                f"/data/in{ext}", f"/data/out{ext}",
            ]
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            try:
                proc = subprocess.run(
                    cmd, capture_output=True, text=True,
                    encoding="utf-8", timeout=timeout_s,
                    creationflags=creation_flags,
                )
            except subprocess.TimeoutExpired:
                return RunnerResult(
                    success=False, parser_name=self.name, format_type=fmt,
                    error_type="timeout",
                    stderr=f"pysam docker roundtrip timed out after {timeout_s}s",
                    duration_ms=(time.monotonic() - t0) * 1000,
                )
            if proc.returncode != 0 or not os.path.exists(out_path):
                return RunnerResult(
                    success=False, parser_name=self.name, format_type=fmt,
                    exit_code=proc.returncode, error_type="crash",
                    stderr=(proc.stderr or "")[:500],
                    duration_ms=(time.monotonic() - t0) * 1000,
                )
            with open(out_path, "r", encoding="utf-8") as f:
                text = f.read()
            return RunnerResult(
                success=True,
                canonical_json={"rewritten_text": text},
                parser_name=self.name, format_type=fmt, exit_code=0,
                stderr=proc.stderr,
                duration_ms=(time.monotonic() - t0) * 1000,
            )

    def _parse(self, input_path: Path, format_type: str) -> dict[str, Any]:
        import pysam

        if format_type == "VCF":
            return self._parse_vcf(input_path, pysam)
        elif format_type == "SAM":
            return self._parse_sam(input_path, pysam)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _parse_vcf(self, path: Path, pysam: Any) -> dict[str, Any]:
        """Parse VCF via pysam into canonical dict."""
        vcf = pysam.VariantFile(str(path))
        header = vcf.header

        # Header
        meta: dict[str, Any] = {}
        for rec in header.records:
            if rec.type == "GENERIC":
                continue
            key = rec.key
            if hasattr(rec, "items") and callable(rec.items):
                fields = dict(rec.items())
                entry_id = fields.get("ID", "")
                if key not in meta:
                    meta[key] = {}
                if isinstance(meta[key], dict):
                    meta[key][entry_id] = fields

        samples = list(header.samples)

        # Records
        records = []
        for rec in vcf:
            # CRITICAL: pysam rec.pos is 0-based! Add +1 for 1-based canonical.
            pos = rec.pos + 1

            rec_id = None if rec.id is None else rec.id
            alt = list(rec.alts) if rec.alts else []
            qual = None if rec.qual is None else float(rec.qual)

            # FILTER
            filt = sorted(list(rec.filter.keys())) if rec.filter else []

            # INFO
            info: dict[str, Any] = {}
            for key in rec.info:
                val = rec.info[key]
                if isinstance(val, tuple):
                    val = list(val)
                info[key] = val
            info = dict(sorted(info.items()))

            # Samples
            sample_data: dict[str, dict] = {}
            for sample_name in samples:
                sample = rec.samples[sample_name]
                fields: dict[str, Any] = {}
                for key in sample.keys():
                    val = sample[key]
                    if isinstance(val, tuple):
                        val = list(val)
                    fields[key] = val
                sample_data[sample_name] = fields

            fmt = list(rec.format.keys()) if rec.format else None

            records.append({
                "CHROM": rec.chrom,
                "POS": pos,
                "ID": rec_id,
                "REF": rec.ref,
                "ALT": alt,
                "QUAL": qual,
                "FILTER": filt,
                "INFO": info,
                "FORMAT": fmt,
                "samples": sample_data if sample_data else None,
            })

        vcf.close()

        return {
            "format": "VCF",
            "header": {
                "fileformat": str(header.version) if hasattr(header, "version") else "",
                "meta": meta,
                "samples": samples,
            },
            "records": records,
        }

    def _parse_sam(self, path: Path, pysam: Any) -> dict[str, Any]:
        """Parse SAM via pysam into canonical dict."""
        sam = pysam.AlignmentFile(str(path), "r")
        header = sam.header

        # Header
        hd = dict(header.get("HD", {})) if "HD" in header else None
        sq = [dict(s) for s in header.get("SQ", [])]
        rg = [dict(r) for r in header.get("RG", [])]
        pg = [dict(p) for p in header.get("PG", [])]
        co = sorted(header.get("CO", []))

        # Records
        records = []
        for read in sam:
            # CRITICAL: pysam reference_start is 0-based! Add +1.
            pos = None if read.is_unmapped else read.reference_start + 1
            pnext = None
            if read.next_reference_start is not None and read.next_reference_start >= 0:
                pnext = read.next_reference_start + 1

            # CIGAR
            cigar = None
            if read.cigartuples:
                op_map = {0: "M", 1: "I", 2: "D", 3: "N", 4: "S", 5: "H", 6: "P", 7: "=", 8: "X"}
                cigar = [{"op": op_map.get(op, "?"), "len": length}
                         for op, length in read.cigartuples]

            # Tags
            tags = {}
            for tag_name, tag_val in read.get_tags(with_value_type=True):
                tag_type = tag_val[0] if isinstance(tag_val, tuple) else "Z"
                val = tag_val[1] if isinstance(tag_val, tuple) else tag_val
                tags[tag_name] = {"type": tag_type, "value": val}
            tags = dict(sorted(tags.items()))

            records.append({
                "QNAME": read.query_name,
                "FLAG": read.flag,
                "RNAME": None if read.reference_name is None else read.reference_name,
                "POS": pos,
                "MAPQ": read.mapping_quality,
                "CIGAR": cigar,
                "RNEXT": None if read.next_reference_name is None else read.next_reference_name,
                "PNEXT": pnext,
                "TLEN": read.template_length,
                "SEQ": None if read.query_sequence is None else read.query_sequence,
                "QUAL": None if read.query_qualities is None else "".join(
                    chr(q + 33) for q in read.query_qualities
                ),
                "tags": tags,
            })

        sam.close()

        return {
            "format": "SAM",
            "header": {"HD": hd, "SQ": sq, "RG": rg, "PG": pg, "CO": co},
            "records": records,
        }

    # ------------------------------------------------------------------
    # Rank 5 — query-method MRs
    # ------------------------------------------------------------------
    def discover_query_methods(self, format_type: str) -> list[dict]:
        """Introspect the first parsed record's class for scalar query
        methods. Tries native pysam first; falls back to a tiny seed
        file when Docker-only paths are in play."""
        from .introspection import get_scalar_query_methods
        if not self._use_native():
            return []
        try:
            import pysam
        except ImportError:
            return []
        # Use pysam's class hierarchy without needing a real file.
        if format_type.upper() == "VCF":
            try:
                # VariantRecord can't easily be instantiated standalone
                # — peek at any seed if available, else introspect
                # pysam.VariantRecord directly via attribute walk on
                # the class itself.
                cls = pysam.VariantRecord
                return get_scalar_query_methods(cls)
            except Exception:
                return []
        if format_type.upper() == "SAM":
            try:
                cls = pysam.AlignedSegment
                return get_scalar_query_methods(cls)
            except Exception:
                return []
        return []

    def run_query_methods(
        self,
        input_path: Path,
        format_type: str,
        method_names: list[str],
        timeout_s: float = 30.0,
    ) -> RunnerResult:
        """Parse `input_path`, invoke each named method on the first
        record, return RunnerResult with method_results dict."""
        from .introspection import run_methods_on_record
        if not self._use_native():
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="ineligible",
                stderr="PysamRunner.run_query_methods needs native pysam",
            )
        try:
            import pysam
        except ImportError as e:
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="crash",
                stderr=f"pysam import failed: {e}",
            )
        t0 = time.monotonic()
        try:
            if format_type.upper() == "VCF":
                f = pysam.VariantFile(str(input_path))
                rec = next(f, None)
                f.close()
            elif format_type.upper() == "SAM":
                f = pysam.AlignmentFile(str(input_path), "r", check_sq=False)
                rec = next(f, None)
                f.close()
            else:
                return RunnerResult(
                    success=False, parser_name=self.name,
                    format_type=format_type, error_type="ineligible",
                    stderr=f"unsupported format {format_type}",
                )
            if rec is None:
                return RunnerResult(
                    success=True, parser_name=self.name,
                    format_type=format_type.upper(), exit_code=0,
                    canonical_json={"method_results": {}},
                    duration_ms=(time.monotonic() - t0) * 1000,
                )
            results = run_methods_on_record(rec, method_names)
            return RunnerResult(
                success=True, parser_name=self.name,
                format_type=format_type.upper(), exit_code=0,
                canonical_json={"method_results": results},
                duration_ms=(time.monotonic() - t0) * 1000,
            )
        except Exception as e:
            return RunnerResult(
                success=False, parser_name=self.name,
                format_type=format_type, error_type="crash",
                stderr=f"native query: {e}",
                duration_ms=(time.monotonic() - t0) * 1000,
            )
