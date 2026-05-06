#!/usr/bin/env python3
"""4-rep BioTest sweep — supports both E0 (full BioTest) and E1
(no-Phase-A, naive prompt-stuffing) under one --mode flag.

Forked from compares/scripts/biotest_4rep_cascade_parallel.py with
three changes:
  1. --mode {E0, E1}: routes biotest invocation through
     harness_run.py instead of biotest.py directly. E1 mode applies
     the four runtime monkey-patches.
  2. Phase E ENABLED on both modes (the Phase E patch from
     run_e1.py redirects seeds_root to per-cell cfg paths so it no
     longer races on global seeds/<fmt>_struct/).
  3. cumulative=False by default — independent reps for honest std.

Per-cell rep cascade (within one cell, --cumulative true mode):
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
HARNESS_RUN = (Path(__file__).resolve().parent / "harness_run.py")
LOG_LOCK = threading.Lock()
MODE = "E0"  # set in main() per --mode flag


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


def reset_data_and_coverage(work_dir: Path, cell: Cell, fh, cumulative: bool = True) -> None:
    """Wipe data/ and bug_reports/ between reps. Behavior of
    coverage_artifacts/ depends on `cumulative`:

      cumulative=True (default, Refine Round 4): preserve the directory
        so JaCoCo `append=true` / coverage.py / gcovr `.gcda` counters
        accumulate across reps. rep N's measurement = union of reps
        0..N. Coverage monotonically non-decreasing.

      cumulative=False: wipe coverage_artifacts/ each rep so every rep
        is an independent trial. Std band across reps measures
        per-trial variance (apples-to-apples vs published SOTA stats
        which are also independent-trial means).

    Seeds always cascade across reps regardless of this flag.
    """
    data_dir = work_dir / "data"
    if data_dir.exists():
        shutil.rmtree(data_dir, ignore_errors=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    cov_dir = work_dir / "coverage_artifacts"
    if not cumulative and cov_dir.exists():
        # Independent-trial mode: wipe ALL prior counters so this rep
        # gets a fresh measurement.
        shutil.rmtree(cov_dir, ignore_errors=True)
    cov_dir.mkdir(parents=True, exist_ok=True)
    (cov_dir / "jacoco").mkdir(parents=True, exist_ok=True)
    (cov_dir / "noodles").mkdir(parents=True, exist_ok=True)
    (cov_dir / "pysam").mkdir(parents=True, exist_ok=True)
    bug_dir = work_dir / "bug_reports"
    if bug_dir.exists():
        shutil.rmtree(bug_dir, ignore_errors=True)
    bug_dir.mkdir(parents=True, exist_ok=True)
    if cumulative:
        log(cell, "    reset data/ + bug_reports/ (seeds + coverage_artifacts preserved — cumulative cascade)", fh)
    else:
        log(cell, "    reset data/ + bug_reports/ + coverage_artifacts/ (seeds preserved — independent trials)", fh)


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
    pc["corpus_keeper"] = {
        "enabled": True,
        "max_files_per_format": 2000,
        # Rank 8b (2026-04-30) — replay each newly-kept file under
        # coverage.py and delete files that don't add new lines vs the
        # pre-iteration corpus. MVP supports vcfpy/biopython primaries;
        # the htsjdk and noodles cells skip with a logger.warning so
        # this block is safe to enable for all cells.
        "coverage_guided_culling": {
            "enabled": True,
            "measure_baseline_against_corpus": True,
        },
    }
    # Hypothesis-driven Phase C with corpus-size-scaled budget
    # (cascade-dilution mitigation, 2026-04-30). Replaces static-mode's
    # "iterate every seed once per MR" with a bounded budget that
    # auto-grows by sqrt(corpus/baseline). Without this, rep 0 covers
    # more lines than reps 1-3 because each curated seed gets less
    # Hypothesis sampling depth as the corpus dilutes with kept_*.
    pc["hypothesis"] = {
        "enabled": True,
        "max_examples": 50,
        "max_examples_corpus_scaling": {
            "enabled": True,
            "baseline_corpus_size": 33,
            "cap": 400,
        },
    }

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
    fb["primary_target"] = cell.sut
    fb["state_path"] = P(work_dir / "data" / "feedback_state.json")
    fb["attempts_path"] = P(work_dir / "data" / "rule_attempts.json")
    fb["coverage_report_path"] = P(work_dir / "data" / "coverage_report.json")
    fb["scc_report_path"] = P(work_dir / "data" / "scc_report.json")

    if MODE in ("E2", "E3"):
        # E2/E3 = no Phase D. Disable feedback loop + cross-iter Rank levers
        # (Rank 1 seed-synth / Rank 6 mr-synth / Rank 8 corpus-keeper),
        # but KEEP `phase_c.hypothesis.enabled=True` so Phase C runs in
        # the same sampling mode E0 uses (apples-to-apples Phase C).
        # Disabling hypothesis would silently flip Phase C from sampling
        # to exhaustive — letting E2 visit deeper branches than E0 can,
        # which is a methodology confound, NOT a "Phase D" effect.
        # Rank 4 (hypothesis.target()) stays on as residual since
        # disabling it would require a runtime monkey-patch.
        # E3 also has E1S patches applied (no Phase A) at harness_run.py
        # level — config is identical to E2 here.
        fb["enabled"] = False
        fb["max_iterations"] = 1
        fb.setdefault("seed_synthesis", {})["enabled"] = False
        fb.setdefault("mr_synthesis", {})["enabled"] = False
        pc["corpus_keeper"]["enabled"] = False    # Rank 8 off
        # phase_c.hypothesis stays ON — same Phase C engine as E0.
    else:
        fb["enabled"] = True
        fb["max_iterations"] = cell.max_iterations
        fb["plateau_patience"] = cell.max_iterations + 1
        fb["coverage_plateau_patience"] = cell.max_iterations + 1
        fb["min_coverage_delta_pp"] = 0.0
        # 60 min internal timeout (was 80) — gives biotest 30 min cushion
        # before the wrapper's 90-min wall budget SIGTERMs the process.
        # Without this cushion, coverage.py atexit on Python SUTs
        # (biopython, vcfpy) can't flush before SIGKILL → coverage missing.
        fb["timeout_minutes"] = 60
        # Seed synthesis enabled — this is what makes the corpus grow
        # across reps in cumulative mode (and produces fresh
        # synthetic_* files per rep in independent-trial mode).
        fb.setdefault("seed_synthesis", {})["enabled"] = True
        fb["seed_synthesis"]["max_seeds_per_iteration"] = 5
        fb["seed_synthesis"]["max_file_bytes"] = 524288

    # ----- Phase E ENABLED in this fork. The harness_run.py wrapper
    # installs a Phase E isolation patch (cfg-driven seeds_root) before
    # launching biotest, so Rank 12 + 13 augmentation lands under
    # work_dir/seeds/<fmt>_struct,_rawfuzz/ — no race on global paths.
    src["phase_e"] = {"enabled": True}

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
    # Route through harness_run.py so the Phase E isolation patch is
    # installed (E0 + E1) and the spec-blind patches are installed (E1
    # only). Phase filter "B,C,D,E" — Phase A still disabled at the
    # cfg level (chromadb serializes); E1 mode uses spec-blind prompt
    # so the existing chroma_db is irrelevant.
    cmd = [
        sys.executable, str(HARNESS_RUN),
        "--mode", MODE,
        "--config", str(cfg_path),
        "--phase", ("B,C,E" if MODE in ("E2", "E3") else "D,E"),
        "--verbose",
    ]
    log(cell, f"    cmd: python harness_run.py --mode {MODE} --config {cfg_path.name} --phase " + ("B,C,E" if MODE in ("E2", "E3") else "D,E") + "", fh)
    log(cell, f"    budget: {budget_s}s (host)", fh)
    # Refine Round 4 — two SUT-agnostic levers, both env-var-gated:
    #   BIOTEST_MULTISHOT_K=2:
    #     `apply_mr_transforms` composes K=2 extra semantics-preserving
    #     transforms after each MR's own steps. Framework-internal,
    #     SUT-agnostic.
    #   BIOTEST_AUTO_INVOKE_PUBLIC_METHODS=1 (SAM only):
    #     The Java harness routes parses through `--mode parse_auto_invoke`,
    #     which reflectively invokes every PUBLIC NO-ARG non-mutator
    #     instance method on each parsed record (no hardcoded names —
    #     uses java.lang.Class.getMethods() with the same structural
    #     filter as the existing query-method discovery). Adding a new
    #     Java SUT's parsed-record class with public getters surfaces
    #     them automatically; no per-SUT harness edit. C++ / Rust SUTs
    #     ignore the env var (their runners don't dispatch on it).
    env = os.environ.copy()
    if cell.fmt == "SAM":
        env["BIOTEST_MULTISHOT_K"] = "2"
        env["BIOTEST_AUTO_INVOKE_PUBLIC_METHODS"] = "1"
        log(cell, f"    env: BIOTEST_MULTISHOT_K=2  BIOTEST_AUTO_INVOKE_PUBLIC_METHODS=1 (refine round 4)", fh)
    started = time.time()
    # Windows: launch in own process group so we can send CTRL_BREAK_EVENT
    # for a graceful shutdown — TerminateProcess (the default for
    # subprocess.terminate() on Windows) is SIGKILL-equivalent and skips
    # Python's atexit handlers, which means coverage.py never flushes.
    # CTRL_BREAK_EVENT raises KeyboardInterrupt-equivalent in the child,
    # so context managers exit and atexit fires.
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(
            cmd, stdout=lf, stderr=subprocess.STDOUT,
            env=env, cwd=str(REPO_ROOT),
            creationflags=creationflags,
        )
        try:
            proc.wait(timeout=budget_s)
        except subprocess.TimeoutExpired:
            log(cell, f"    timeout after {budget_s}s — sending CTRL_BREAK_EVENT (graceful)", fh)
            try:
                if sys.platform == "win32":
                    import signal as _sig
                    proc.send_signal(_sig.CTRL_BREAK_EVENT)
                else:
                    proc.terminate()
            except (OSError, ValueError) as e:
                log(cell, f"    send_signal failed: {e}; falling back to terminate", fh)
                proc.terminate()
            try:
                # 180s grace for atexit to flush coverage.py / gcovr / etc.
                proc.wait(timeout=180)
            except subprocess.TimeoutExpired:
                log(cell, f"    didn't exit in 180s — kill()", fh)
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
    path because /work is a bind mount of the repo root.

    Workaround: Docker Desktop on Windows (gRPC FUSE 9p bind mount) can
    intermittently refuse to CREATE specific filenames inside bind-mounted
    dirs, even though writing to an existing file works. Empirically
    `biotest.log` was reproducibly unwritable via container `>` redirect
    while `foo.log` in the same dir worked — likely a path-cache bug.
    Pre-touching the file from the host primes the bind mount so the
    container's redirect overwrites instead of creating.
    """
    container_cfg = to_container_path(cfg_path)
    container_log = to_container_path(log_path)
    container_harness = to_container_path(HARNESS_RUN)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    # Pre-create the log file on the host so the container's redirect
    # only has to overwrite, not create. Avoids the 0s-exit failure mode
    # where bash dies with "No such file or directory" on `> biotest.log`.
    try:
        log_path.touch(exist_ok=True)
    except OSError:
        pass
    # Refine Round 4 — propagate BIOTEST_MULTISHOT_K=2 to SAM container
    # cells (seqan3_sam, etc.). VCF cells unaffected.
    multishot_export = (
        "export BIOTEST_MULTISHOT_K=2; "
        if cell.fmt == "SAM" else ""
    )
    if cell.fmt == "SAM":
        log(cell, f"    env (container): BIOTEST_MULTISHOT_K=2 (refine round 4)", fh)
    cmd = [
        "docker", "exec",
        "biotest-bench-setup",
        "bash", "-lc",
        f"{multishot_export}"
        f"timeout --kill-after=60 {budget_s} python3.12 {container_harness} "
        f"--mode {MODE} --config {container_cfg} --phase " + ("B,C,E" if MODE in ("E2", "E3") else "D,E") + " --verbose "
        f"> {container_log} 2>&1 || true",
    ]
    log(cell, f"    cmd: docker exec biotest-bench-setup python3.12 harness_run.py --mode {MODE} ...", fh)
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
    try:
        proc = subprocess.run(
            ["java", "-jar", str(cli), "report", str(exec_path),
             "--classfiles", str(jar), "--xml", str(xml)],
            capture_output=True, timeout=900, cwd=str(REPO_ROOT),
        )
        if proc.returncode != 0:
            log(cell, f"    jacoco regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)
    except subprocess.TimeoutExpired:
        log(cell, f"    jacoco regen TIMEOUT after 900s — measurement may be incomplete, continuing cascade", fh)


def regenerate_gcovr_json(work_dir: Path, fh, cell: Cell) -> None:
    """Run gcovr inside the container against the seqan3 build dir, write
    JSON to the cell's coverage_artifacts/gcovr.json.

    Timeout extended to 900s (was 180s) — large cumulative .gcda data
    after multi-iter Phase D can take 5-10 min to process. Also catch
    TimeoutExpired so a single slow regen doesn't FAIL the entire cell
    cascade and lose subsequent reps' data.
    """
    out_json = work_dir / "coverage_artifacts" / "gcovr.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    container_out = to_container_path(out_json)
    try:
        proc = subprocess.run(
            ["docker", "exec", "biotest-bench-setup", "bash", "-lc",
             f"python3.12 -m gcovr --json -o {container_out} "
             f"--root /opt/seqan3/include --filter '.*seqan3.*' "
             f"--gcov-executable 'llvm-cov-18 gcov' "
             f"/work/harnesses/cpp/build"],
            capture_output=True, timeout=900,
        )
        if proc.returncode != 0:
            log(cell, f"    gcovr regen failed (rc={proc.returncode}): {proc.stderr.decode(errors='replace')[:200]}", fh)
    except subprocess.TimeoutExpired:
        log(cell, f"    gcovr regen TIMEOUT after 900s — measurement may be incomplete, continuing cascade", fh)


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
    try:
        proc = subprocess.run(
            ["docker", "exec", "biotest-bench-setup", "bash", "-lc", cmd],
            capture_output=True, timeout=900,
        )
        if proc.returncode != 0:
            log(cell, f"    llvm-cov regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)
    except subprocess.TimeoutExpired:
        log(cell, f"    llvm-cov regen TIMEOUT after 900s — measurement may be incomplete, continuing cascade", fh)


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
            capture_output=True, timeout=600, cwd=str(REPO_ROOT),
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
                                capture_output=True, timeout=600, cwd=str(REPO_ROOT))
        proc_b = subprocess.run(base + ["--metric", "BRANCH"],
                                capture_output=True, timeout=600, cwd=str(REPO_ROOT))
        out["line_pct"], out["covered"], out["total"] = _parse_overall(
            proc_l.stdout.decode(errors="replace")
        )
        out["branch_pct"], _, _ = _parse_overall(
            proc_b.stdout.decode(errors="replace")
        )
    else:
        proc = subprocess.run(base, capture_output=True, timeout=600, cwd=str(REPO_ROOT))
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
        # seqan3 cov harness — rebuild when missing OR when the harness
        # source has been edited (refine round 4 added a second seqan3
        # pre-pass; need the binary to pick up that source change).
        "if [ ! -x /work/harnesses/cpp/build/biotest_harness_cov_seqan3 ] "
        "   || [ /work/harnesses/cpp/biotest_harness.cpp -nt "
        "        /work/harnesses/cpp/build/biotest_harness_cov_seqan3 ]; then "
        "  cd /work/harnesses/cpp; mkdir -p build; "
        "  rm -f build/*.gcda build/*.gcno; "
        "  clang++-18 -std=c++23 -O0 -g -DNDEBUG -DUSE_SEQAN3 "
        "    -DSEQAN3_DISABLE_COMPILER_CHECK -isystem /opt/seqan3/include "
        "    -fprofile-arcs -ftest-coverage biotest_harness.cpp "
        "    -o build/biotest_harness_cov_seqan3; "
        "fi; "
        # noodles cov binary — skip --locked so a stale Cargo.lock
        # doesn't fail SAM-only runs that don't actually use noodles.
        "cd /work/harnesses/rust/noodles_harness; "
        "RUSTFLAGS='-C instrument-coverage' cargo build --release "
        "  --manifest-path /work/harnesses/rust/noodles_harness/Cargo.toml "
        "  || echo 'noodles build skipped (cell-irrelevant if not VCF)'; "
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
    cumulative: bool = True,
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

        # Reset data + bug_reports; coverage_artifacts/ behavior depends
        # on `cumulative`: True = preserve (Round 4 cumulative cascade),
        # False = wipe (independent-trial mode for honest std-band).
        reset_data_and_coverage(work_dir, cell, fh, cumulative=cumulative)

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
    ap.add_argument(
        "--mode", required=True, choices=("E0", "E1", "E1S", "E2", "E3"),
        help=(
            "E0=full BioTest (RAG via existing chromadb); "
            "E1=no Phase A, naive prompt-stuffing of full spec; "
            "E1S=STRICT no Phase A — no spec text, bare transform names, "
            "no spec rules in blindspot ticket; "
            "E2=full RAG + Phase D loop OFF (single-shot B+C+E, no Rank levers)"
        ),
    )
    ap.add_argument("--out-root", type=Path, default=None,
                    help="Output root. Default: compares/ApplicationStudy/<mode>_*/results_4rep")
    ap.add_argument("--vcf-budget-s", type=int, default=5400,
                    help="Per-rep wall cap (VCF cells). Default 90 min.")
    ap.add_argument("--sam-budget-s", type=int, default=5400,
                    help="Per-rep wall cap (SAM cells). Default 90 min.")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--only", action="append", default=[],
                    help="Run only these cell labels (e.g. htsjdk_vcf).")
    ap.add_argument("--max-workers", type=int, default=6)
    ap.add_argument(
        "--cumulative", choices=("true", "false"), default="false",
        help=(
            "false (default in this fork): wipe coverage_artifacts/ each "
            "rep so every rep is an independent trial — gives honest "
            "per-rep std. true: preserve coverage across reps (cascade "
            "mode, std collapses when a rep adds no new lines)."
        ),
    )
    args = ap.parse_args()
    args.cumulative_bool = (args.cumulative == "true")
    if args.out_root is None:
        sub = {
            "E0": "E0_baseline",
            "E1": "E1_no_phase_a",
            "E1S": "E1S_strict",
            "E2": "E2_no_phase_d",
            "E3": "E3_no_a_no_d",
        }[args.mode]
        args.out_root = (
            REPO_ROOT / "compares" / "ApplicationStudy" / sub / "results_4rep"
        )

    # Make MODE visible to per-cell launchers in this process.
    global MODE
    MODE = args.mode

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
    print(f"[master] cumulative={args.cumulative_bool}", flush=True)
    mfh.write(f"[master] cumulative={args.cumulative_bool}\n")
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {
            ex.submit(
                run_cell_cascade, cell, args.out_root, master_log,
                args.vcf_budget_s, args.sam_budget_s, args.reps,
                args.cumulative_bool,
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
