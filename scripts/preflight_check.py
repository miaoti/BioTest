#!/usr/bin/env python3
"""
Pre-flight dependency check for Phase D end-to-end run.

Runs 9 checks and reports PASS/FAIL with actionable fixes.
Exits non-zero if any check fails.

Usage:
    py -3.12 scripts/preflight_check.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CheckResult:
    def __init__(self, name: str, passed: bool, detail: str = "", fix: str = ""):
        self.name = name
        self.passed = passed
        self.detail = detail
        self.fix = fix

    def render(self) -> str:
        mark = "[PASS]" if self.passed else "[FAIL]"
        out = f"{mark} {self.name}"
        if self.detail:
            out += f"\n       {self.detail}"
        if not self.passed and self.fix:
            out += f"\n       Fix: {self.fix}"
        return out


def check_ollama() -> CheckResult:
    try:
        import requests
        resp = requests.get("http://localhost:11434/v1/models", timeout=5)
        if resp.status_code != 200:
            return CheckResult("Ollama API", False, f"HTTP {resp.status_code}",
                               "Start Ollama: `ollama serve` in a separate terminal")
        data = resp.json()
        models = [m.get("id", "") for m in data.get("data", [])]
        if any("qwen3-coder:30b" in m for m in models):
            return CheckResult("Ollama API", True, f"qwen3-coder:30b loaded")
        return CheckResult("Ollama API", False, f"Available models: {models}",
                           "Pull model: `ollama pull qwen3-coder:30b`")
    except Exception as e:
        return CheckResult("Ollama API", False, str(e),
                           "Start Ollama: `ollama serve`")


def check_docker() -> CheckResult:
    if not shutil.which("docker"):
        return CheckResult("Docker", False, "docker binary not found",
                           "Install Docker Desktop")
    try:
        proc = subprocess.run(
            ["docker", "image", "inspect", "biotest-pysam:latest"],
            capture_output=True, timeout=10,
        )
        if proc.returncode == 0:
            return CheckResult("Docker image biotest-pysam:latest", True)
        return CheckResult("Docker image biotest-pysam:latest", False, "image not found",
                           "Build: `docker build -t biotest-pysam:latest harnesses/pysam/`")
    except Exception as e:
        return CheckResult("Docker", False, str(e),
                           "Ensure Docker Desktop is running")


def check_htsjdk_jar() -> CheckResult:
    jar = ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
    if jar.exists():
        size_mb = jar.stat().st_size / 1024 / 1024
        return CheckResult("htsjdk fat JAR", True, f"{size_mb:.1f} MB")
    return CheckResult("htsjdk fat JAR", False, f"not found at {jar}",
                       "Build: `cd harnesses/java && gradle shadowJar`")


def check_seqan3_binary() -> CheckResult:
    binary = ROOT / "harnesses" / "cpp" / "build" / "biotest_harness.exe"
    if binary.exists():
        size_kb = binary.stat().st_size / 1024
        return CheckResult("seqan3 binary", True, f"{size_kb:.0f} KB")
    return CheckResult("seqan3 binary", False, f"not found at {binary}",
                       "Build C++ harness via cmake + g++ (see Flow.md)")


def check_biopython() -> CheckResult:
    try:
        proc = subprocess.run(
            [sys.executable, "-c", "import Bio; from Bio.Align import sam; print(Bio.__version__)"],
            capture_output=True, text=True, timeout=10,
        )
        if proc.returncode == 0:
            return CheckResult("biopython (Bio.Align.sam)", True, "importable")
        return CheckResult("biopython (Bio.Align.sam)", False, proc.stderr.strip()[:100],
                           "Install: `py -3.12 -m pip install biopython`")
    except Exception as e:
        return CheckResult("biopython (Bio.Align.sam)", False, str(e),
                           "Install biopython")


def check_chromadb_chunks() -> CheckResult:
    vcf_chunks = ROOT / "data" / "parsed" / "VCFv4.5_chunks.json"
    sam_chunks = ROOT / "data" / "parsed" / "SAMv1_chunks.json"
    if not vcf_chunks.exists() or not sam_chunks.exists():
        return CheckResult("Phase A chunks", False, "parsed JSON missing",
                           "Run: `py -3.12 -m spec_ingestor.main`")
    try:
        vcf = json.loads(vcf_chunks.read_text(encoding="utf-8"))
        sam = json.loads(sam_chunks.read_text(encoding="utf-8"))
        total = len(vcf) + len(sam)
        if total < 1000:
            return CheckResult("Phase A chunks", False, f"only {total} chunks",
                               "Re-run Phase A")
        return CheckResult("Phase A chunks", True,
                           f"{len(vcf)} VCF + {len(sam)} SAM = {total} chunks")
    except Exception as e:
        return CheckResult("Phase A chunks", False, str(e), "Re-run Phase A")


def check_seeds() -> CheckResult:
    vcf_dir = ROOT / "seeds" / "vcf"
    sam_dir = ROOT / "seeds" / "sam"
    vcf_count = len(list(vcf_dir.glob("*.vcf"))) if vcf_dir.exists() else 0
    sam_count = len(list(sam_dir.glob("*.sam"))) if sam_dir.exists() else 0
    total = vcf_count + sam_count
    # Bar: need the 3 hand-crafted Tier-1 VCFs + at least a handful of
    # Tier-2 real-world VCFs to exercise meaningful diversity. Bumped
    # from the old ">= 6" threshold after the corpus expansion.
    if vcf_count < 15:
        return CheckResult(
            "Seed corpus",
            False,
            f"{vcf_count} VCF + {sam_count} SAM (need >=15 VCF)",
            "Run: `py -3.12 seeds/fetch_real_world.py` to populate Tier-2 seeds",
        )
    return CheckResult("Seed corpus", True,
                       f"{vcf_count} VCF + {sam_count} SAM seeds")


def check_coverage_tools() -> CheckResult:
    jacoco_agent = ROOT / "coverage_artifacts" / "jacoco" / "jacocoagent.jar"
    jacoco_cli = ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
    missing = []
    if not jacoco_agent.exists():
        missing.append("jacocoagent.jar")
    if not jacoco_cli.exists():
        missing.append("jacococli.jar")
    try:
        import coverage as _  # noqa: F401
    except ImportError:
        missing.append("coverage.py")
    if missing:
        return CheckResult("Coverage tooling", False, f"missing: {missing}",
                           "Download JaCoCo JARs or `pip install coverage`")
    return CheckResult("Coverage tooling", True, "JaCoCo + coverage.py ready")


def check_llm_smoke() -> CheckResult:
    try:
        sys.path.insert(0, str(ROOT))
        from mr_engine.llm_factory import get_llm
        llm = get_llm()
        resp = llm.invoke("Say 'ok' and nothing else.")
        content = getattr(resp, "content", "") or ""
        if content.strip():
            return CheckResult("LLM smoke test", True,
                               f"model={llm.model_name}, response={content[:50]!r}")
        return CheckResult("LLM smoke test", False, "empty response",
                           "Check Ollama model loaded: `ollama list`")
    except Exception as e:
        return CheckResult("LLM smoke test", False, str(e)[:100],
                           "Check Ollama + .env LLM_MODEL settings")


def main():
    print("Phase D pre-flight checks:\n")

    checks = [
        check_ollama(),
        check_docker(),
        check_htsjdk_jar(),
        check_seqan3_binary(),
        check_biopython(),
        check_chromadb_chunks(),
        check_seeds(),
        check_coverage_tools(),
        check_llm_smoke(),
    ]

    for c in checks:
        print(c.render())
        print()

    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    print(f"Result: {passed}/{total} checks passed")

    if passed == total:
        print("All systems go. Safe to run: py -3.12 biotest.py --phase D")
        return 0
    else:
        failed_names = [c.name for c in checks if not c.passed]
        print(f"Failed: {failed_names}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
