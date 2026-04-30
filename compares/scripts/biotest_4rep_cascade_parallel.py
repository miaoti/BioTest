#!/usr/bin/env python3
"""4-rep BioTest coverage sweep with corpus cascade across reps, all
cells running in parallel with isolated working directories.

Per-cell rep cascade (within one cell):
    Rep 0: starts with curated/external seeds only (no kept_*/synthetic_*).
    Rep 1: starts with the seed corpus AS LEFT BY rep 0 (curated +
           rep 0's kept_* + rep 0's synthetic_iter*_*).
    Rep 2: starts with rep 1's leftover corpus (= curated + rep 0 + rep 1).
    Rep 3: starts with rep 2's leftover corpus.

Cross-cell isolation (across the 6 primary SUTs in DESIGN.md §1):
    Each cell runs in its own working tree under
    `<out_root>/<cell>/work/{seeds,data,coverage_artifacts,bug_reports}/`.
    Cell A's kept_*/synthetic_* never enter cell B's view, so we get a
    fair cross-tool comparison even though the corpus accumulates
    within each cell.

LLM enforcement: the user's local biotest_config.yaml may temporarily
point at a local Ollama model. This orchestrator OVERRIDES
`phase_b.llm.model = "deepseek-chat"` in every per-rep temp config so
parallel runs are reproducibly DeepSeek-driven.

Phase E (Rank 12 structural + Rank 13 lenient byte fuzz) is DISABLED
because it writes to global `seeds/<fmt>_struct/` and `seeds/<fmt>_rawfuzz/`
paths that are NOT per-cell — running 6 cells with Phase E in parallel
would race on those paths. Phase E only feeds downstream Phase-3
mutation testing; it does not affect the Phase-D coverage we report.

Cells (5 primary SUTs, 6 cells per DESIGN §1):
    htsjdk × VCF      (host, JaCoCo)
    vcfpy × VCF       (host, coverage.py)
    noodles × VCF     (biotest-bench container, llvm-cov)
    htsjdk × SAM      (host, JaCoCo)
    biopython × SAM   (host, coverage.py)
    seqan3 × SAM      (biotest-bench container, gcovr)

Run:
    py -3.12 compares/scripts/biotest_4rep_cascade_parallel.py
        [--out-root <dir>] [--vcf-budget-s 5400] [--sam-budget-s 5400]
        [--reps 4] [--only htsjdk_vcf ...]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_LOCK = threading.Lock()


@dataclass
class Cell:
    sut: str
    fmt: str
    where: str  # "host" or "container"
    coverage_kind: str  # "jacoco" | "coveragepy" | "noodles" | "gcovr"
    max_iterations: int = 2

    @property
    def label(self) -> str:
        return f"{self.sut}_{self.fmt.lower()}"


CELLS: list[Cell] = [
    Cell("htsjdk",    "VCF", "host",      "jacoco",     max_iterations=2),
    Cell("vcfpy",     "VCF", "host",      "coveragepy", max_iterations=2),
    Cell("noodles",   "VCF", "container", "noodles",    max_iterations=2),
    Cell("htsjdk",    "SAM", "host",      "jacoco",     max_iterations=2),
    Cell("biopython", "SAM", "host",      "coveragepy", max_iterations=2),
    Cell("seqan3",    "SAM", "container", "gcovr",      max_iterations=2),
]


def log(cell: Cell, msg: str, fh) -> None:
    with LOG_LOCK:
        line = f"[{time.strftime('%H:%M:%S')}] [{cell.label:14s}] {msg}"
        try:
            print(line, flush=True)
        except UnicodeEncodeError:
            print(line.encode("ascii", "replace").decode("ascii"), flush=True)
        fh.write(line + "\n")
        fh.flush()


# ---------------------------------------------------------------------------
# Per-cell working tree setup
# ---------------------------------------------------------------------------

def setup_initial_seeds(seeds_root: Path) -> tuple[int, int]:
    """Stage the curated/external seed corpus (no BioTest-generated)
    under <seeds_root>/{vcf,sam}/. Returns (vcf_count, sam_count)."""
    vcf_n = sam_n = 0
    for fmt in ("vcf", "sam"):
        dst = seeds_root / fmt
        dst.mkdir(parents=True, exist_ok=True)
        src_dir = REPO_ROOT / "seeds" / fmt
        if not src_dir.exists():
            continue
        for src in sorted(src_dir.glob(f"*.{fmt}")):
            if src.name.startswith("kept_") or src.name.startswith("synthetic_"):
                continue  # Strictly fresh: no BioTest-generated input
            dst_path = dst / src.name
            if dst_path.exists():
                continue
            try:
                os.symlink(src.resolve(), dst_path)
            except OSError:
                shutil.copy2(src, dst_path)
        n = len(list(dst.glob(f"*.{fmt}")))
        if fmt == "vcf":
            vcf_n = n
        else:
            sam_n = n
    # Also carry the toy CRAM reference for sam_cram_round_trip.
    ref_src = REPO_ROOT / "seeds" / "ref"
    if ref_src.exists():
        ref_dst = seeds_root / "ref"
        if not ref_dst.exists():
            try:
                shutil.copytree(ref_src, ref_dst)
            except OSError:
                pass
    return vcf_n, sam_n


def reset_data_and_coverage(work_dir: Path, cell: Cell, fh) -> None:
    """Wipe data/ and coverage_artifacts/ between reps (but NOT seeds —
    seeds CASCADE across reps within a cell)."""
    data_dir = work_dir / "data"
    if data_dir.exists():
        shutil.rmtree(data_dir, ignore_errors=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    cov_dir = work_dir / "coverage_artifacts"
    if cov_dir.exists():
        shutil.rmtree(cov_dir, ignore_errors=True)
    cov_dir.mkdir(parents=True, exist_ok=True)
    (cov_dir / "jacoco").mkdir(parents=True, exist_ok=True)
    (cov_dir / "noodles").mkdir(parents=True, exist_ok=True)
    (cov_dir / "pysam").mkdir(parents=True, exist_ok=True)
    bug_dir = work_dir / "bug_reports"
    if bug_dir.exists():
        shutil.rmtree(bug_dir, ignore_errors=True)
    bug_dir.mkdir(parents=True, exist_ok=True)
    log(cell, "    reset data/ + coverage_artifacts/ (seeds unchanged)", fh)


def snapshot_seeds_count(seeds_root: Path) -> dict[str, int]:
    out = {}
    for fmt in ("vcf", "sam"):
        d = seeds_root / fmt
        if not d.exists():
            out[f"{fmt}_total"] = 0
            out[f"{fmt}_kept"] = 0
            out[f"{fmt}_synthetic"] = 0
            continue
        files = list(d.glob(f"*.{fmt}"))
        out[f"{fmt}_total"] = len(files)
        out[f"{fmt}_kept"] = sum(1 for f in files if f.name.startswith("kept_"))
        out[f"{fmt}_synthetic"] = sum(
            1 for f in files if f.name.startswith("synthetic_")
        )
    return out


# ---------------------------------------------------------------------------
# Per-rep config builder
# ---------------------------------------------------------------------------

def to_container_path(p: Path) -> str:
    """Convert a host (Windows) path under REPO_ROOT to its /work-bind
    equivalent inside the biotest-bench container.

    Handles both absolute and relative `p`. Relative paths are resolved
    against REPO_ROOT first; otherwise a relative `out-root` produced
    paths like `/workcompares/...` (missing slash between /work and the
    rest), which gcovr/biotest then failed to open.
    """
    abs_p = Path(p) if Path(p).is_absolute() else (REPO_ROOT / p)
    s = str(abs_p).replace("\\", "/")
    repo_str = str(REPO_ROOT).replace("\\", "/")
    if s.startswith(repo_str):
        suffix = s[len(repo_str):]
        if not suffix.startswith("/"):
            suffix = "/" + suffix
        return "/work" + suffix
    # Path outside REPO_ROOT — fall through (caller error; container
    # bind-mount won't see it anyway).
    return s


def write_temp_config(
    cell: Cell, rep: int, work_dir: Path, cfg_out: Path,
) -> Path:
    """Build per-cell, per-rep biotest_config.yaml that pins all paths
    into work_dir, forces deepseek-chat, and disables Phase E.

    For container cells, paths are translated from Windows host paths
    to Linux /work-bind paths so the container's biotest.py reads its
    own per-cell state, not the global /work/data/feedback_state.json
    that has stale state from prior runs."""
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))

    is_container = (cell.where == "container")
    def P(host_path: Path) -> str:
        return to_container_path(host_path) if is_container else str(host_path)

    # ----- Phase A — skip when running in parallel because ChromaDB
    # serializes concurrent embedding requests. The chroma_db at
    # data/chroma_db/ is shared and already populated from prior runs;
    # parallel cells just READ it during Phase B's RAG retrieval.
    src.setdefault("phase_a", {})["enabled"] = False

    # ----- LLM override (user might be running ollama locally) -----
    src.setdefault("phase_b", {}).setdefault("llm", {})["model"] = "deepseek-chat"
    src["phase_b"]["llm"]["temperature"] = 0.0
    src["phase_b"]["llm"]["max_retries"] = 3
    src["phase_b"]["registry_path"] = P(work_dir / "data" / "mr_registry.json")

    # ----- Phase C — per-cell seeds_dir, output_dir, det_report -----
    pc = src.setdefault("phase_c", {})
    pc["format_filter"] = cell.fmt
    pc["seeds_dir"] = P(work_dir / "seeds")
    pc["output_dir"] = P(work_dir / "bug_reports")
    pc["det_report_path"] = P(work_dir / "data" / "det_report.json")
    pc["corpus_keeper"] = {"enabled": True, "max_files_per_format": 2000}

    # ----- Per-SUT path overrides for coverage instrumentation -----
    for sut_cfg in pc.get("suts", []):
        name = sut_cfg.get("name")
        if name == "htsjdk":
            sut_cfg["coverage_exec_dir"] = P(
                work_dir / "coverage_artifacts" / "jacoco"
            )
            destfile = P(
                work_dir / "coverage_artifacts" / "jacoco" / "jacoco.exec"
            )
            agent = ("/work/coverage_artifacts/jacoco/jacocoagent.jar"
                     if is_container else
                     str(REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacocoagent.jar"))
            sut_cfg["coverage_jvm_args"] = (
                f"-javaagent:{agent}=destfile={destfile},append=true"
            )
        elif name == "noodles":
            sut_cfg["llvm_profile_dir"] = P(
                work_dir / "coverage_artifacts" / "noodles"
            )
            # Container path for the cov-instrumented binary built via
            # RUSTFLAGS=-C instrument-coverage cargo build --release.
            sut_cfg["adapter"] = (
                "/work/harnesses/rust/noodles_harness/target/release/noodles_harness"
            )
            sut_cfg["coverage_binary"] = (
                "/work/harnesses/rust/noodles_harness/target/release/noodles_harness"
            )
        elif name == "seqan3":
            # USE_SEQAN3 cov harness baked into the bench container at
            # build/biotest_harness_cov_seqan3 (clang++-18 + -fprofile-arcs).
            sut_cfg["adapter"] = (
                "/work/harnesses/cpp/build/biotest_harness_cov_seqan3"
            )
            sut_cfg["coverage_binary"] = (
                "/work/harnesses/cpp/build/biotest_harness_cov_seqan3"
            )
        elif name == "pysam":
            sut_cfg["coverage_dir"] = P(work_dir / "coverage_artifacts" / "pysam")

    # ----- Coverage block (per-cell paths for backend artefacts) -----
    cov = src.setdefault("coverage", {})
    cov["enabled"] = True
    cov["jacoco_report_dir"] = P(work_dir / "coverage_artifacts" / "jacoco")
    cov["coveragepy_data_file"] = P(
        work_dir / "coverage_artifacts" / ".coverage"
    )
    cov["pysam_coverage_dir"] = P(work_dir / "coverage_artifacts" / "pysam")
    cov["gcovr_report_path"] = P(work_dir / "coverage_artifacts" / "gcovr.json")
    cov["noodles_report_path"] = P(
        work_dir / "coverage_artifacts" / "noodles" / "llvm-cov.json"
    )
    cov["noodles_profile_dir"] = P(work_dir / "coverage_artifacts" / "noodles")

    # ----- Phase D — per-cell state files, max_iter, primary, etc. -----
    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = cell.sut
    fb["max_iterations"] = cell.max_iterations
    fb["plateau_patience"] = cell.max_iterations + 1
    fb["coverage_plateau_patience"] = cell.max_iterations + 1
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = 80  # graceful self-stop before 90-min wall cap
    fb["state_path"] = P(work_dir / "data" / "feedback_state.json")
    fb["attempts_path"] = P(work_dir / "data" / "rule_attempts.json")
    fb["coverage_report_path"] = P(work_dir / "data" / "coverage_report.json")
    fb["scc_report_path"] = P(work_dir / "data" / "scc_report.json")
    # Seed synthesis enabled — this is what makes the corpus grow across
    # reps. Without it, rep N would have the same seeds as rep N-1, so
    # std would collapse to ~0 (deterministic Phase C).
    fb.setdefault("seed_synthesis", {})["enabled"] = True
    fb["seed_synthesis"]["max_seeds_per_iteration"] = 5
    fb["seed_synthesis"]["max_file_bytes"] = 524288

    # ----- Phase E disabled (would race on global seeds/<fmt>_struct/) -----
    src["phase_e"] = {"enabled": False}

    # ----- Per-rep RNG seed (varies Hypothesis exploration) -----
    src.setdefault("global", {})["seed_rng"] = 42 + rep

    cfg_out.parent.mkdir(parents=True, exist_ok=True)
    cfg_out.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")
    return cfg_out


# ---------------------------------------------------------------------------
# biotest.py launcher (host or container)
# ---------------------------------------------------------------------------

def run_biotest_host(
    cfg_path: Path, budget_s: int, log_path: Path, cell: Cell, fh,
) -> tuple[int, float]:
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path),
        "--phase", "D",  # Phase A disabled (chroma serializes); Phase E disabled
        "--verbose",
    ]
    log(cell, f"    cmd: python biotest.py --config {cfg_path.name} --phase D", fh)
    log(cell, f"    budget: {budget_s}s (host)", fh)
    started = time.time()
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(
            cmd, stdout=lf, stderr=subprocess.STDOUT,
            env=os.environ.copy(), cwd=str(REPO_ROOT),
        )
        try:
            proc.wait(timeout=budget_s)
        except subprocess.TimeoutExpired:
            log(cell, f"    timeout after {budget_s}s — terminating", fh)
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    pass
    elapsed = time.time() - started
    rc = proc.returncode if proc.returncode is not None else -1
    return rc, elapsed


def run_biotest_container(
    cfg_path: Path, budget_s: int, log_path: Path, cell: Cell, fh,
) -> tuple[int, float]:
    """Launch biotest inside biotest-bench-setup. cfg_path is the host-
    side absolute path under /work/... — the container sees the same
    path because /work is a bind mount of the repo root."""
    container_cfg = to_container_path(cfg_path)
    container_log = to_container_path(log_path)
    # Ensure log dir exists on host (== /work in container).
    log_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "docker", "exec",
        "biotest-bench-setup",
        "bash", "-lc",
        f"timeout --kill-after=60 {budget_s} python3.12 /work/biotest.py "
        f"--config {container_cfg} --phase D --verbose "
        f"> {container_log} 2>&1 || true",
    ]
    log(cell, f"    cmd: docker exec biotest-bench-setup python3.12 biotest.py …", fh)
    log(cell, f"    budget: {budget_s}s (container)", fh)
    started = time.time()
    # Buffer = 600s. The container `timeout --kill-after=60 ${budget_s}` already
    # bounds biotest at budget_s + 60s; the extra ~10 min margin gives docker
    # exec time to flush coverage.py/gcovr atexit + return, especially when the
    # MR menu is large enough to slow Phase D into bumping the wall cap.
    proc = subprocess.run(cmd, capture_output=True, timeout=budget_s + 600)
    elapsed = time.time() - started
    return proc.returncode, elapsed


def run_biotest(
    cfg_path: Path, budget_s: int, log_path: Path, cell: Cell, fh,
) -> tuple[int, float]:
    if cell.where == "container":
        return run_biotest_container(cfg_path, budget_s, log_path, cell, fh)
    return run_biotest_host(cfg_path, budget_s, log_path, cell, fh)


# ---------------------------------------------------------------------------
# Coverage measurement (post-rep)
# ---------------------------------------------------------------------------

def regenerate_jacoco_xml(work_dir: Path, fh, cell: Cell) -> None:
    exec_path = work_dir / "coverage_artifacts" / "jacoco" / "jacoco.exec"
    if not exec_path.exists():
        return
    cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
    jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
    xml = work_dir / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    if not (cli.exists() and jar.exists()):
        return
    proc = subprocess.run(
        ["java", "-jar", str(cli), "report", str(exec_path),
         "--classfiles", str(jar), "--xml", str(xml)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT),
    )
    if proc.returncode != 0:
        log(cell, f"    jacoco regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)


def regenerate_gcovr_json(work_dir: Path, fh, cell: Cell) -> None:
    """Run gcovr inside the container against the seqan3 build dir, write
    JSON to the cell's coverage_artifacts/gcovr.json."""
    out_json = work_dir / "coverage_artifacts" / "gcovr.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    container_out = to_container_path(out_json)
    proc = subprocess.run(
        ["docker", "exec", "biotest-bench-setup", "bash", "-lc",
         f"python3.12 -m gcovr --json -o {container_out} "
         f"--root /opt/seqan3/include --filter '.*seqan3.*' "
         f"--gcov-executable 'llvm-cov-18 gcov' "
         f"/work/harnesses/cpp/build"],
        capture_output=True, timeout=180,
    )
    if proc.returncode != 0:
        log(cell, f"    gcovr regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)


def regenerate_noodles_llvm_cov(work_dir: Path, fh, cell: Cell) -> None:
    """Run llvm-cov export against accumulated profraw under work_dir's
    noodles cov dir, write llvm-cov.json. Bypasses cargo-llvm-cov 0.8.5
    report regression that misses external crates (matches the patched
    NoodlesCoverageCollector)."""
    profile_dir = work_dir / "coverage_artifacts" / "noodles"
    out_json = profile_dir / "llvm-cov.json"
    container_profile = to_container_path(profile_dir)
    container_out = to_container_path(out_json)
    cmd = (
        "LLVM=/root/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/"
        "rustlib/x86_64-unknown-linux-gnu/bin && "
        f"$LLVM/llvm-profdata merge -sparse {container_profile}/*.profraw "
        f"-o {container_profile}/merged.profdata 2>/dev/null && "
        f"$LLVM/llvm-cov export "
        "/work/harnesses/rust/noodles_harness/target/release/noodles_harness "
        f"-instr-profile={container_profile}/merged.profdata "
        f"> {container_out}"
    )
    proc = subprocess.run(
        ["docker", "exec", "biotest-bench-setup", "bash", "-lc", cmd],
        capture_output=True, timeout=180,
    )
    if proc.returncode != 0:
        log(cell, f"    llvm-cov regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)


def _parse_overall(stdout: str) -> tuple[float, int, int]:
    for line in stdout.splitlines():
        if "OVERALL" in line and "weighted" in line:
            try:
                tail = line.split(")", 1)[1].strip()
                frac, pct = tail.split("(")
                covered_s, total_s = frac.strip().split("/")
                pct = pct.replace("%", "").replace(")", "").strip()
                return float(pct), int(covered_s), int(total_s)
            except Exception:
                continue
    return 0.0, 0, 0


def measure_cell(work_dir: Path, cell: Cell, fh) -> dict[str, Any]:
    out: dict[str, Any] = {
        "line_pct": 0.0, "branch_pct": 0.0,
        "covered": 0, "total": 0, "status": "missing",
    }

    # Per-coverage-kind: regenerate JSON/XML report from raw artefacts.
    if cell.coverage_kind == "jacoco":
        regenerate_jacoco_xml(work_dir, fh, cell)
        report = work_dir / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    elif cell.coverage_kind == "coveragepy":
        src = work_dir / "coverage_artifacts" / ".coverage"
        if not src.exists():
            return out
        dest = work_dir / "coverage_artifacts" / ".coverage.json"
        if dest.exists():
            try:
                dest.unlink()
            except OSError:
                pass
        conv = subprocess.run(
            [sys.executable, "-m", "coverage", "json",
             "--data-file", str(src), "-o", str(dest)],
            capture_output=True, timeout=120, cwd=str(REPO_ROOT),
        )
        if conv.returncode != 0 or not dest.exists():
            log(cell, f"    coveragepy conv failed", fh)
            out["status"] = "convert_failed"
            return out
        report = dest
    elif cell.coverage_kind == "gcovr":
        regenerate_gcovr_json(work_dir, fh, cell)
        report = work_dir / "coverage_artifacts" / "gcovr.json"
    elif cell.coverage_kind == "noodles":
        regenerate_noodles_llvm_cov(work_dir, fh, cell)
        report = work_dir / "coverage_artifacts" / "noodles" / "llvm-cov.json"
    else:
        return out

    if not report.exists():
        return out

    base = [
        sys.executable,
        str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
        "--report", str(report),
        "--sut", cell.sut, "--format", cell.fmt,
    ]
    if cell.coverage_kind == "jacoco":
        proc_l = subprocess.run(base + ["--metric", "LINE"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        proc_b = subprocess.run(base + ["--metric", "BRANCH"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        out["line_pct"], out["covered"], out["total"] = _parse_overall(
            proc_l.stdout.decode(errors="replace")
        )
        out["branch_pct"], _, _ = _parse_overall(
            proc_b.stdout.decode(errors="replace")
        )
    else:
        proc = subprocess.run(base, capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        out["line_pct"], out["covered"], out["total"] = _parse_overall(
            proc.stdout.decode(errors="replace")
        )
    out["status"] = "ok" if out["total"] else "empty"
    out["source"] = str(report.relative_to(work_dir))
    return out


# ---------------------------------------------------------------------------
# Container-side cov-binary builder (one-time, idempotent)
# ---------------------------------------------------------------------------

def ensure_container_cov_binaries(fh) -> None:
    """Make sure both the seqan3 USE_SEQAN3 cov harness and the noodles
    RUSTFLAGS-instrumented binary exist inside biotest-bench-setup
    (idempotent — skips if already built)."""
    setup_cmd = (
        "set -e; export PATH=/root/.cargo/bin:$PATH; "
        # seqan3 cov harness
        "if [ ! -x /work/harnesses/cpp/build/biotest_harness_cov_seqan3 ]; then "
        "  cd /work/harnesses/cpp; mkdir -p build; "
        "  rm -f build/*.gcda build/*.gcno; "
        "  clang++-18 -std=c++23 -O0 -g -DNDEBUG -DUSE_SEQAN3 "
        "    -DSEQAN3_DISABLE_COMPILER_CHECK -isystem /opt/seqan3/include "
        "    -fprofile-arcs -ftest-coverage biotest_harness.cpp "
        "    -o build/biotest_harness_cov_seqan3; "
        "fi; "
        # noodles cov binary
        "cd /work/harnesses/rust/noodles_harness; "
        "RUSTFLAGS='-C instrument-coverage' cargo build --release --locked "
        "  --manifest-path /work/harnesses/rust/noodles_harness/Cargo.toml; "
        # Python 3.12 deps
        "python3.12 -c 'import yaml,rich,hypothesis,chromadb,gcovr' || "
        "  python3.12 -m pip install --quiet --no-warn-script-location "
        "    -r /work/requirements.txt gcovr lxml; "
    )
    proc = subprocess.run(
        ["docker", "exec", "biotest-bench-setup", "bash", "-lc", setup_cmd],
        capture_output=True, timeout=600,
    )
    if proc.returncode != 0:
        msg = proc.stderr.decode(errors="replace")[:500]
        with LOG_LOCK:
            print(f"[setup] container build FAILED:\n{msg}", flush=True)
            fh.write(f"[setup] container build FAILED: {msg}\n")
            fh.flush()
        raise RuntimeError("container setup failed")
    with LOG_LOCK:
        print("[setup] container cov binaries ready", flush=True)
        fh.write("[setup] container cov binaries ready\n")
        fh.flush()


# ---------------------------------------------------------------------------
# Per-cell cascade (4 reps, sequential within cell)
# ---------------------------------------------------------------------------

def run_cell_cascade(
    cell: Cell, out_root: Path, master_log: Path,
    vcf_budget_s: int, sam_budget_s: int, reps: int,
) -> dict[str, Any]:
    cell_dir = out_root / cell.label
    cell_dir.mkdir(parents=True, exist_ok=True)
    cell_log = cell_dir / "cell.log"
    fh = cell_log.open("a", encoding="utf-8", buffering=1)
    log(cell, f"=== cascade start ({cell.where}, max_iter={cell.max_iterations}) ===", fh)

    work_dir = cell_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Initial seed corpus: curated/external only (no kept_*/synthetic_*).
    vcf_n, sam_n = setup_initial_seeds(work_dir / "seeds")
    log(cell, f"    initial seeds: VCF={vcf_n}  SAM={sam_n}", fh)

    cell_results: list[dict[str, Any]] = []
    for rep in range(reps):
        log(cell, f"--- rep {rep} ---", fh)
        # Seed corpus snapshot BEFORE this rep starts (input to this rep).
        seeds_before = snapshot_seeds_count(work_dir / "seeds")
        log(cell, f"    seeds entering rep: {seeds_before}", fh)

        # Reset data + coverage_artefacts (but keep seeds — they cascade).
        reset_data_and_coverage(work_dir, cell, fh)

        # For seqan3, also reset the global .gcda files — only this cell
        # writes them, so safe to wipe between its own reps.
        if cell.coverage_kind == "gcovr":
            for p in (REPO_ROOT / "harnesses" / "cpp" / "build").glob("*.gcda"):
                try:
                    p.unlink()
                except OSError:
                    pass

        # Per-rep config.
        rep_dir = cell_dir / f"run_{rep}"
        rep_dir.mkdir(parents=True, exist_ok=True)
        cfg_path = write_temp_config(
            cell, rep, work_dir,
            cfg_out=rep_dir / f"biotest_config.rep{rep}.yaml",
        )

        # Wall-time budget per cell format.
        budget = vcf_budget_s if cell.fmt == "VCF" else sam_budget_s

        biotest_log = rep_dir / "biotest.log"
        rc, elapsed = run_biotest(cfg_path, budget, biotest_log, cell, fh)
        log(cell, f"    rep {rep} exit={rc} elapsed={elapsed:.0f}s", fh)

        cov = measure_cell(work_dir, cell, fh)
        seeds_after = snapshot_seeds_count(work_dir / "seeds")
        rec = {
            "cell": cell.label, "sut": cell.sut, "format": cell.fmt,
            "rep": rep, "exit_code": rc, "elapsed_s": round(elapsed, 1),
            "max_iterations": cell.max_iterations,
            "phases": "A,D",
            "rep_kind": "fresh" if rep == 0 else f"cascade_from_rep_{rep-1}",
            "seeds_before": seeds_before,
            "seeds_after": seeds_after,
            **cov,
        }
        cell_results.append(rec)
        (rep_dir / "measurement.json").write_text(
            json.dumps(rec, indent=2), encoding="utf-8",
        )
        log(cell,
            f"    -> line={cov['line_pct']:.2f}% covered={cov['covered']}/{cov['total']} "
            f"status={cov['status']} seeds_after={seeds_after}",
            fh)
        # Persist incremental cell aggregate.
        (cell_dir / "cell_results.json").write_text(
            json.dumps(cell_results, indent=2), encoding="utf-8",
        )

    log(cell, f"=== cascade complete ({len(cell_results)} reps) ===", fh)
    fh.close()
    return {"cell": cell.label, "results": cell_results}


# ---------------------------------------------------------------------------
# Master
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", type=Path,
                    default=REPO_ROOT / "compares" / "results" / "coverage"
                    / "biotest_4rep_cascade_20260427")
    ap.add_argument("--vcf-budget-s", type=int, default=5400,
                    help="Per-rep wall cap (VCF cells). Default 90 min.")
    ap.add_argument("--sam-budget-s", type=int, default=5400,
                    help="Per-rep wall cap (SAM cells). Default 90 min.")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--only", action="append", default=[],
                    help="Run only these cell labels (e.g. htsjdk_vcf).")
    ap.add_argument("--max-workers", type=int, default=6)
    args = ap.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    master_log = args.out_root / "master.log"
    mfh = master_log.open("a", encoding="utf-8", buffering=1)

    cells = [c for c in CELLS if (not args.only or c.label in args.only)]
    needs_container = any(c.where == "container" for c in cells)

    print(f"[master] cells: {[c.label for c in cells]}", flush=True)
    mfh.write(f"[master] cells: {[c.label for c in cells]}\n")
    print(f"[master] vcf_budget_s={args.vcf_budget_s}  sam_budget_s={args.sam_budget_s}  reps={args.reps}", flush=True)
    mfh.write(f"[master] budgets: vcf={args.vcf_budget_s}s sam={args.sam_budget_s}s reps={args.reps}\n")

    if needs_container:
        print("[setup] preparing container cov binaries...", flush=True)
        mfh.write("[setup] preparing container cov binaries...\n")
        ensure_container_cov_binaries(mfh)

    started = time.time()
    print(f"[master] launching {len(cells)} cells in parallel...", flush=True)
    mfh.write(f"[master] launching {len(cells)} cells in parallel...\n")

    workers = min(args.max_workers, len(cells))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {
            ex.submit(
                run_cell_cascade, cell, args.out_root, master_log,
                args.vcf_budget_s, args.sam_budget_s, args.reps,
            ): cell
            for cell in cells
        }
        for fut in as_completed(futures):
            cell = futures[fut]
            try:
                fut.result()
                mfh.write(f"[master] [{cell.label}] CASCADE OK\n")
                print(f"[master] [{cell.label}] CASCADE OK", flush=True)
            except Exception as e:
                mfh.write(f"[master] [{cell.label}] CASCADE FAILED: {e}\n")
                print(f"[master] [{cell.label}] CASCADE FAILED: {e}", flush=True)

    total_min = (time.time() - started) / 60
    mfh.write(f"\n[master] all cells complete in {total_min:.1f} min\n")
    print(f"\n[master] all cells complete in {total_min:.1f} min", flush=True)
    mfh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
