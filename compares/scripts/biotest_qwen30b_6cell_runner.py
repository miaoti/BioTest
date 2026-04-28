#!/usr/bin/env python3
"""6-cell BioTest sweep using local Ollama (qwen3-coder:30b).

Runs the FULL canonical pipeline (Phase A,D,E) for each of 4 reps on
all 5 primary SUTs (6 cells total — htsjdk has VCF+SAM):

    htsjdk_VCF    | host    | JaCoCo
    htsjdk_SAM    | host    | JaCoCo
    vcfpy_VCF     | host    | coverage.py
    biopython_SAM | host    | coverage.py
    noodles_VCF   | docker  | cargo-llvm-cov (biotest-bench-setup)
    seqan3_SAM    | docker  | gcovr (biotest-bench-setup)

Each rep is INDEPENDENT — state files (mr_registry.json,
feedback_state.json, rule_attempts.json, coverage_report.json,
det_report.json, scc_report.json) and the cell's coverage artefact are
deleted before the run so Phase B mines fresh and Phase D starts at
iteration 0. The seed corpus is filtered to **non-out-tool-generated
seeds only** (excludes kept_*, synthetic_*, jazzer_*, atheris_*,
libfuzzer_*, aflpp_*, cargofuzz_*) so coverage / mutation comparisons
aren't biased by other tools' output.

Cells run SEQUENTIALLY because biotest.py writes to shared paths
under data/ that aren't config-parameterised (feedback_state.json,
rule_attempts.json, etc.). Within each cell, reps also run
sequentially to avoid the same collision plus to keep one Ollama
client at a time (model is 30B, served locally on
http://localhost:11434, queues concurrent requests).

Usage:
  py -3.12 compares/scripts/biotest_qwen30b_6cell_runner.py \\
      --reps 4 --budget-s 3600 --out-root compares/results/coverage/biotest_qwen30b_4rep_v1
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKER_CONTAINER = "biotest-bench-setup"


# Out-tool-generated seed prefixes. Anything matching these is excluded
# from the per-rep seed wrapper so coverage/mutation numbers reflect
# only Tier-1 + Tier-2 curated/public seeds — not BioTest's prior
# corpus_keeper/seed_synthesis output, and not other fuzzers' output.
OUT_TOOL_PREFIXES = (
    "kept_",
    "synthetic_",
    "jazzer_",
    "atheris_",
    "libfuzzer_",
    "aflpp_",
    "cargofuzz_",
    "purerandom_",
)


@dataclass
class Cell:
    label: str           # filesystem-friendly identifier (e.g., "htsjdk_vcf")
    sut: str             # config name in biotest_config.yaml: phase_c.suts
    fmt: str             # "VCF" | "SAM"
    runner: str          # "host" | "container"
    coverage_kind: str   # "jacoco" | "coveragepy" | "gcovr" | "llvmcov"
    reset_paths: list[str] = field(default_factory=list)
    # The path biotest.py writes its primary coverage artefact to.
    # Resolved to host filesystem (when running via docker, the
    # container's /work mount maps to REPO_ROOT, so the same relative
    # path applies).
    coverage_artefact: str = ""
    # Optional override for the SUT's `adapter` entry in biotest_config —
    # used by seqan3 to pin the seqan3-linked cov binary.
    adapter_override: str | None = None
    coverage_binary_override: str | None = None


CELLS: list[Cell] = [
    Cell(
        label="htsjdk_vcf", sut="htsjdk", fmt="VCF",
        runner="host", coverage_kind="jacoco",
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        coverage_artefact="coverage_artifacts/jacoco/jacoco.xml",
    ),
    Cell(
        label="htsjdk_sam", sut="htsjdk", fmt="SAM",
        runner="host", coverage_kind="jacoco",
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        coverage_artefact="coverage_artifacts/jacoco/jacoco.xml",
    ),
    Cell(
        label="vcfpy_vcf", sut="vcfpy", fmt="VCF",
        runner="host", coverage_kind="coveragepy",
        reset_paths=["coverage_artifacts/.coverage"],
        coverage_artefact="coverage_artifacts/.coverage",
    ),
    Cell(
        label="biopython_sam", sut="biopython", fmt="SAM",
        runner="host", coverage_kind="coveragepy",
        reset_paths=["coverage_artifacts/.coverage"],
        coverage_artefact="coverage_artifacts/.coverage",
    ),
    Cell(
        label="noodles_vcf", sut="noodles", fmt="VCF",
        runner="container", coverage_kind="llvmcov",
        reset_paths=[
            "coverage_artifacts/noodles/llvm-cov.json",
        ],
        coverage_artefact="coverage_artifacts/noodles/llvm-cov.json",
    ),
    Cell(
        label="seqan3_sam", sut="seqan3", fmt="SAM",
        runner="container", coverage_kind="gcovr",
        reset_paths=["coverage_artifacts/gcovr.json"],
        coverage_artefact="coverage_artifacts/gcovr.json",
        adapter_override="harnesses/cpp/build/biotest_harness_cov_seqan3",
        coverage_binary_override="harnesses/cpp/build/biotest_harness_cov_seqan3",
    ),
]


STATE_FILES = [
    "data/mr_registry.json",
    "data/feedback_state.json",
    "data/rule_attempts.json",
    "data/coverage_report.json",
    "data/det_report.json",
    "data/scc_report.json",
]

# Baseline MR registry to seed each rep with. qwen3-coder:30b cannot
# drive the BioTest ReAct agent — it outputs intermediate tool-call
# JSON instead of the final MR JSON shape, so Phase B's mining yields
# ~0 valid MRs across 4 attempts × 3 themes (verified 2026-04-27 V1+V2
# runs). Without a seeded registry, every rep ends with 0 tests / 0%
# coverage and `std` becomes meaningless.
#
# This baseline (10 VCF + 10 SAM enforced MRs, 33 quarantine) was
# mined by DeepSeek V3 in a prior canonical run and represents the
# stable MR set the tool would otherwise need to re-mine. With it
# pre-loaded, qwen3-coder:30b still drives Phase D's iterative
# feedback (blindspot tickets, Rank 1 seed synthesis if enabled) so
# the local-model contribution is measurable while Phase C has a
# meaningful corpus of MRs to apply.
BASELINE_REGISTRY = "data/mr_registry.pre_fullD.backup.json"


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def log(msg: str, fh) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)
    fh.write(line + "\n")
    fh.flush()


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def reset_state(fh) -> None:
    """Truly-fresh state: every rep begins with empty registry + empty
    feedback state. qwen3-coder:30b mines from scratch via Phase B; if
    it produces 0 valid MRs, the registry stays empty and Phase C has
    nothing to test. That is the honest measurement of the local model's
    capability — no pre-loaded MRs from any prior tool/run."""
    for rel in STATE_FILES:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                p.unlink()
                log(f"    reset state: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)


# Auxiliary corpus directories that BioTest itself writes to. Cleaning
# these between reps keeps each rep's corpus origin pure (Tier-1 + Tier-2
# only) — no cross-rep / cross-SUT contamination from Phase E
# (structural/rawfuzz), Rank-8 corpus_keeper (kept_*), Rank-1 seed
# synthesizer (synthetic_*), or older Rank-9/10/11 diversifier outputs.
# This is the user's fairness invariant: SUT-1's rep-0 corpus must not
# pollute SUT-2's rep-0 corpus.
AUX_CORPUS_DIRS = (
    "seeds/vcf_struct", "seeds/sam_struct",
    "seeds/vcf_rawfuzz", "seeds/sam_rawfuzz",
    "seeds/vcf_diverse", "seeds/sam_diverse",
    "seeds/vcf_bytefuzz", "seeds/sam_bytefuzz",
)
# File-glob patterns whose matches inside seeds/{vcf,sam}/ are deleted
# between reps (defense-in-depth — corpus_keeper is config-disabled but
# any leftover files from prior interactive runs would otherwise bias
# the per-rep input set).
TAINTED_SEED_GLOBS = (
    ("seeds/vcf", "kept_*.vcf"),
    ("seeds/sam", "kept_*.sam"),
    ("seeds/vcf", "synthetic_*.vcf"),
    ("seeds/sam", "synthetic_*.sam"),
)


def reset_aux_corpora(fh) -> None:
    """Wipe every auxiliary corpus that BioTest accretes between reps.
    Ensures the next rep starts on the same Tier-1+2 substrate."""
    cleared = 0
    for rel in AUX_CORPUS_DIRS:
        p = REPO_ROOT / rel
        if p.exists() and p.is_dir():
            try:
                shutil.rmtree(p)
                cleared += 1
            except OSError as e:
                log(f"    aux-reset-skip ({e}): {rel}", fh)
    for parent_rel, pat in TAINTED_SEED_GLOBS:
        parent = REPO_ROOT / parent_rel
        if not parent.exists():
            continue
        for p in parent.glob(pat):
            try:
                p.unlink()
                cleared += 1
            except OSError:
                pass
    # bug_reports/ — biotest writes per-test bug bundles here. Clean so
    # cross-rep timestamp collisions don't accumulate.
    bug_reports = REPO_ROOT / "bug_reports"
    if bug_reports.exists():
        for entry in bug_reports.iterdir():
            try:
                if entry.is_dir():
                    shutil.rmtree(entry)
                else:
                    entry.unlink()
                cleared += 1
            except OSError:
                pass
    if cleared:
        log(f"    reset aux corpora: {cleared} entries cleared", fh)


def reset_cell_artefacts(cell: Cell, fh) -> None:
    for rel in cell.reset_paths:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                log(f"    reset cell artefact: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)
    # noodles also accumulates .profraw fragments; clean them.
    if cell.coverage_kind == "llvmcov":
        for p in (REPO_ROOT / "coverage_artifacts" / "noodles").glob("*.profraw"):
            try:
                p.unlink()
            except OSError:
                pass
    # seqan3 gcda files accumulate across reps; clean them too.
    if cell.coverage_kind == "gcovr":
        for p in (REPO_ROOT / "harnesses" / "cpp" / "build").glob("*.gcda"):
            try:
                p.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Seed corpus filter — exclude all out-tool-generated seeds
# ---------------------------------------------------------------------------

def build_clean_seeds_dir(tmp_root: Path, fh) -> Path:
    """Stage `tmp_root/{vcf,sam}/` with ONLY Tier-1 + Tier-2 seeds.

    Excludes every prefix in OUT_TOOL_PREFIXES so the corpus reflects
    only hand-crafted (`minimal_*`, `spec_example*`, `complex_cigar*`)
    and curated public test data (`real_world_*`, `bcftools_*`,
    `htsjdk_*`).
    """
    counts: dict[str, int] = {}
    for fmt in ("vcf", "sam"):
        dst = tmp_root / fmt
        dst.mkdir(parents=True, exist_ok=True)
        src_dir = REPO_ROOT / "seeds" / fmt
        if not src_dir.exists():
            counts[fmt] = 0
            continue
        files = sorted(src_dir.glob(f"*.{fmt}"))
        eligible = [
            p for p in files
            if not any(p.name.startswith(pref) for pref in OUT_TOOL_PREFIXES)
        ]
        counts[fmt] = len(eligible)
        for src in eligible:
            link = dst / src.name
            if link.exists():
                continue
            try:
                os.symlink(src.resolve(), link)
            except OSError:
                shutil.copy2(src, link)
    # CRAM toy reference (used by sam_cram_round_trip).
    ref_src = REPO_ROOT / "seeds" / "ref"
    if ref_src.exists():
        ref_dst = tmp_root / "ref"
        if not ref_dst.exists():
            try:
                shutil.copytree(ref_src, ref_dst)
            except OSError:
                pass
    log(
        f"    clean seeds: vcf={counts.get('vcf', 0)} "
        f"sam={counts.get('sam', 0)} (excluding "
        f"{', '.join(OUT_TOOL_PREFIXES)})",
        fh,
    )
    return tmp_root


# ---------------------------------------------------------------------------
# Per-rep config builder
# ---------------------------------------------------------------------------

def write_temp_config(
    cell: Cell, rep: int, out_dir: Path, seeds_root: Path,
    max_iterations: int, timeout_minutes: int,
) -> Path:
    src = yaml.safe_load(
        (REPO_ROOT / "biotest_config.yaml").read_text("utf-8")
    )

    # Phase B: route LLM through Ollama. Use the canonical 7-theme
    # matrix from biotest_config.yaml (full pipeline run).
    phase_b = src.setdefault("phase_b", {})
    llm = phase_b.setdefault("llm", {})
    llm["model"] = "ollama/qwen3-coder:30b"
    llm["temperature"] = 0.0

    # Phase C: cell format + per-cell seeds dir + corpus_keeper off so
    # reps don't cross-pollute via kept_* accretion.
    phase_c = src.setdefault("phase_c", {})
    phase_c["format_filter"] = cell.fmt
    # Posix-style relative path resolves correctly under both Windows
    # cwd=REPO_ROOT (host runner) and Linux cwd=/work (docker exec).
    seeds_abs = seeds_root.resolve()
    try:
        seeds_rel = seeds_abs.relative_to(REPO_ROOT.resolve()).as_posix()
        phase_c["seeds_dir"] = seeds_rel
    except ValueError:
        # Out-root outside REPO_ROOT — fall back to absolute path
        # (host-only configs will work; container will fail).
        phase_c["seeds_dir"] = seeds_abs.as_posix()
    phase_c["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}

    # Apply per-cell SUT adapter overrides (for seqan3 cov binary).
    if cell.adapter_override or cell.coverage_binary_override:
        for sut_cfg in phase_c.get("suts", []):
            if sut_cfg.get("name") == cell.sut:
                if cell.adapter_override:
                    sut_cfg["adapter"] = cell.adapter_override
                if cell.coverage_binary_override:
                    sut_cfg["coverage_binary"] = cell.coverage_binary_override

    # Phase D feedback control.
    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = cell.sut
    fb["max_iterations"] = max_iterations
    fb["plateau_patience"] = max_iterations + 1  # disable plateau early-stop
    fb["coverage_plateau_patience"] = max_iterations + 1
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = timeout_minutes
    # Disable Rank 1 seed synthesis — we want pure measurement of the
    # tool's MR-driven coverage, not LLM-synthesised seeds (those are an
    # additional layer studied separately).
    fb.setdefault("seed_synthesis", {})["enabled"] = False
    fb.setdefault("mr_synthesis", {})["enabled"] = False

    # Phase E: bounded auxiliary corpus generation. Coverage was already
    # collected in Phase D; Phase E only writes seeds/<fmt>_struct/ and
    # seeds/<fmt>_rawfuzz/ (used downstream by mutation testing).
    src["phase_e"] = {
        "enabled": True,
        "structural_max_per_seed": 10,
        "rawfuzz_n_per_seed": 2,
        "rawfuzz_seed": 42 + rep,
    }

    src.setdefault("global", {})["seed_rng"] = 42 + rep

    dest = out_dir / f"biotest_config.rep{rep}.yaml"
    dest.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")
    return dest


# ---------------------------------------------------------------------------
# biotest.py invocation
# ---------------------------------------------------------------------------

def run_biotest_host(
    cfg_path: Path, budget_s: int, log_path: Path, fh,
) -> int:
    # We run --phase A,C,E (NOT A,D,E) because:
    # 1. qwen3-coder:30b cannot drive Phase B reliably (outputs intermediate
    #    tool-call JSON instead of MR JSON shape — verified V1/V2/V3 runs).
    #    Skipping Phase B saves ~12 min wasted on failed mining attempts per rep.
    # 2. The baseline registry (data/mr_registry.json, seeded by reset_state)
    #    provides 20 enforced MRs (10 VCF + 10 SAM) so Phase C has work to do.
    # 3. Standalone Phase C (line 1907 in biotest.py) wraps itself in
    #    PythonCoverageContext when Phase D is not requested, so coverage.py
    #    captures Python SUT (vcfpy, biopython, reference) coverage.
    # 4. Phase E generates per-rep auxiliary corpora (struct + rawfuzz) used
    #    by mutation testing.
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path),
        "--phase", "B,C,D,E",
        "--verbose",
    ]
    log(f"    cmd: {' '.join(cmd)}", fh)
    log(f"    budget: {budget_s}s", fh)
    env = os.environ.copy()
    env["LLM_MODEL"] = "ollama/qwen3-coder:30b"
    # Ensure pydantic-settings prefers env over .env file.
    env["LLM_TEMPERATURE"] = "0.0"
    started = time.time()
    with log_path.open("wb") as lf:
        try:
            proc = subprocess.Popen(
                cmd, stdout=lf, stderr=subprocess.STDOUT,
                env=env, cwd=str(REPO_ROOT),
            )
        except Exception as e:
            log(f"    launch-error: {e}", fh)
            return -1
        try:
            proc.wait(timeout=budget_s)
        except subprocess.TimeoutExpired:
            log(f"    timeout after {budget_s}s - terminating", fh)
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
    log(f"    exit={proc.returncode} elapsed={elapsed:.1f}s", fh)
    return proc.returncode if proc.returncode is not None else -1


def run_biotest_container(
    cfg_rel: str, budget_s: int, log_path: Path, fh,
) -> int:
    """Run biotest inside `biotest-bench-setup` container.

    `cfg_rel` is the config path RELATIVE to REPO_ROOT (the container's
    /work mount = host REPO_ROOT). LLM env is injected via -e flags.
    Note: the container reaches host Ollama via host.docker.internal,
    so OLLAMA_BASE_URL must be set accordingly inside the container.

    Same --phase A,C,E rationale as run_biotest_host above.
    """
    inner_cmd = (
        f"cd /work && "
        f"timeout --kill-after=60 {budget_s} "
        f"python3.12 /work/biotest.py "
        f"--config /work/{cfg_rel} "
        f"--phase B,C,D,E --verbose"
    )
    cmd = [
        "docker", "exec",
        "-e", "LLM_MODEL=ollama/qwen3-coder:30b",
        "-e", "OLLAMA_BASE_URL=http://host.docker.internal:11434/v1",
        "-e", "LLM_TEMPERATURE=0.0",
        "-i", DOCKER_CONTAINER,
        "bash", "-c", inner_cmd,
    ]
    log(f"    cmd: docker exec {DOCKER_CONTAINER} ... (cfg=/work/{cfg_rel})", fh)
    log(f"    budget: {budget_s}s", fh)
    started = time.time()
    with log_path.open("wb") as lf:
        try:
            proc = subprocess.Popen(
                cmd, stdout=lf, stderr=subprocess.STDOUT,
            )
        except Exception as e:
            log(f"    launch-error: {e}", fh)
            return -1
        try:
            # docker exec adds ~30s overhead between SIGTERM and the
            # inner timeout firing; pad the wait accordingly.
            proc.wait(timeout=budget_s + 120)
        except subprocess.TimeoutExpired:
            log(f"    timeout after {budget_s}s - killing docker exec", fh)
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
    elapsed = time.time() - started
    log(f"    exit={proc.returncode} elapsed={elapsed:.1f}s", fh)
    return proc.returncode if proc.returncode is not None else -1


# ---------------------------------------------------------------------------
# Coverage measurement
# ---------------------------------------------------------------------------

def regenerate_jacoco_xml(fh) -> None:
    """JaCoCo's exec→XML conversion runs at end-of-iter inside Phase D.
    If a wall-cap kill interrupted it, force a final regen here so the
    measurement reflects all instrumentation captured to disk."""
    exec_path = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco.exec"
    cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
    jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
    xml = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    if not (exec_path.exists() and cli.exists() and jar.exists()):
        return
    proc = subprocess.run(
        ["java", "-jar", str(cli), "report", str(exec_path),
         "--classfiles", str(jar),
         "--xml", str(xml)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT),
    )
    if proc.returncode != 0:
        log(
            f"    jacoco regen failed: "
            f"{proc.stderr.decode(errors='replace')[:200]}",
            fh,
        )


def regenerate_seqan3_gcovr(fh) -> None:
    """For the seqan3 cell we have to run gcovr against the gcda files
    generated by the seqan3-instrumented harness. The container has
    gcovr 8.6 + llvm-cov-18 already installed."""
    cmd = [
        "docker", "exec", DOCKER_CONTAINER, "bash", "-c",
        "python3.12 -m gcovr --json -o /work/coverage_artifacts/gcovr.json "
        "--root /opt/seqan3/include "
        "--filter '.*seqan3.*' "
        "--gcov-executable 'llvm-cov-18 gcov' "
        "/work/harnesses/cpp/build",
    ]
    proc = subprocess.run(cmd, capture_output=True, timeout=300)
    if proc.returncode != 0:
        log(
            f"    gcovr regen failed: "
            f"{proc.stderr.decode(errors='replace')[:200]}",
            fh,
        )


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


def measure_cell_coverage(cell: Cell, fh) -> dict[str, Any]:
    """Snapshot cell.coverage_artefact and run measure_coverage.py with
    the per-SUT filter."""
    if cell.coverage_kind == "jacoco":
        regenerate_jacoco_xml(fh)
    elif cell.coverage_kind == "gcovr":
        regenerate_seqan3_gcovr(fh)

    result = {
        "line_pct": 0.0, "branch_pct": 0.0, "covered": 0, "total": 0,
        "source": cell.coverage_artefact, "status": "missing",
    }

    if cell.coverage_kind == "coveragepy":
        # coverage.py SQLite → JSON via `coverage json`
        src = REPO_ROOT / cell.coverage_artefact
        if not src.exists():
            return result
        dest = REPO_ROOT / "coverage_artifacts" / ".coverage.json"
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
            log(
                f"    coveragepy conv failed: "
                f"{conv.stderr.decode(errors='replace')[:200]}",
                fh,
            )
            result["status"] = "convert_failed"
            return result
        report = dest
    else:
        report = REPO_ROOT / cell.coverage_artefact
    if not report.exists():
        return result

    base = [
        sys.executable,
        str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
        "--report", str(report),
        "--sut", cell.sut,
        "--format", cell.fmt,
    ]
    if cell.coverage_kind == "jacoco":
        proc_l = subprocess.run(
            base + ["--metric", "LINE"],
            capture_output=True, timeout=120, cwd=str(REPO_ROOT),
        )
        proc_b = subprocess.run(
            base + ["--metric", "BRANCH"],
            capture_output=True, timeout=120, cwd=str(REPO_ROOT),
        )
        result["line_pct"], result["covered"], result["total"] = \
            _parse_overall(proc_l.stdout.decode(errors="replace"))
        result["branch_pct"], _, _ = \
            _parse_overall(proc_b.stdout.decode(errors="replace"))
    else:
        proc = subprocess.run(
            base, capture_output=True, timeout=120, cwd=str(REPO_ROOT),
        )
        result["line_pct"], result["covered"], result["total"] = \
            _parse_overall(proc.stdout.decode(errors="replace"))
    result["status"] = "ok" if result["total"] else "zero_total"
    return result


# ---------------------------------------------------------------------------
# Cell-level orchestration
# ---------------------------------------------------------------------------

def run_cell(
    cell: Cell, args: argparse.Namespace, seeds_clean: Path, fh,
) -> list[dict[str, Any]]:
    cell_dir = args.out_root / cell.label
    cell_dir.mkdir(parents=True, exist_ok=True)
    log(
        f"\n### CELL: {cell.label} (sut={cell.sut} fmt={cell.fmt} "
        f"runner={cell.runner} cov={cell.coverage_kind})",
        fh,
    )
    cell_results: list[dict[str, Any]] = []

    for rep in range(args.reps):
        rep_dir = cell_dir / f"run_{rep}"
        rep_dir.mkdir(parents=True, exist_ok=True)
        log(f"  -- rep {rep} --", fh)

        reset_state(fh)
        reset_aux_corpora(fh)
        reset_cell_artefacts(cell, fh)

        cfg_path = write_temp_config(
            cell, rep, rep_dir, seeds_clean,
            max_iterations=args.max_iterations,
            timeout_minutes=args.timeout_minutes,
        )
        # cfg_path may be relative if --out-root was passed as a relative
        # path; resolve before computing the container-side /work-relative
        # path used by `docker exec`.
        cfg_abs = cfg_path.resolve()
        cfg_rel = cfg_abs.relative_to(REPO_ROOT.resolve()).as_posix()
        biotest_log = rep_dir / "biotest.log"

        t0 = time.time()
        if cell.runner == "host":
            exit_code = run_biotest_host(cfg_path, args.budget_s, biotest_log, fh)
        else:
            exit_code = run_biotest_container(
                cfg_rel, args.budget_s, biotest_log, fh,
            )
        elapsed = time.time() - t0

        cov = measure_cell_coverage(cell, fh)

        rec = {
            "cell": cell.label,
            "sut": cell.sut,
            "format": cell.fmt,
            "rep": rep,
            "exit_code": exit_code,
            "elapsed_s": round(elapsed, 1),
            "max_iterations": args.max_iterations,
            "phases": "B,C,D,E",
            "llm_model": "ollama/qwen3-coder:30b",
            **cov,
        }
        cell_results.append(rec)
        (rep_dir / "measurement.json").write_text(
            json.dumps(rec, indent=2), encoding="utf-8",
        )
        log(
            f"    -> line={cov['line_pct']:.2f}% "
            f"covered={cov['covered']}/{cov['total']} status={cov['status']}",
            fh,
        )

    # Persist per-cell summary so partial sweeps still leave audit trail.
    (cell_dir / "results.json").write_text(
        json.dumps(cell_results, indent=2), encoding="utf-8",
    )
    return cell_results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out-root", type=Path,
        default=REPO_ROOT / "compares" / "results" / "coverage"
        / f"biotest_qwen30b_4rep_{time.strftime('%Y%m%d')}",
    )
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument(
        "--budget-s", type=int, default=3600,
        help="Hard wall-time cap per rep (default 3600 s = 60 min). "
        "Local Ollama 30B model is slower than DeepSeek API; this "
        "budget gives Phase A + at least 1 full Phase D iteration.",
    )
    ap.add_argument(
        "--max-iterations", type=int, default=2,
        help="Phase D max iterations per rep.",
    )
    ap.add_argument(
        "--timeout-minutes", type=int, default=50,
        help="biotest's own self-terminate (between iterations) cap. "
        "Should sit ~10 min under --budget-s/60 so coverage.py atexit "
        "flushes cleanly before the wall cap fires.",
    )
    ap.add_argument(
        "--only", action="append", default=[],
        help="Only run cells whose label matches (repeatable).",
    )
    ap.add_argument(
        "--skip", action="append", default=[],
        help="Skip cells whose label matches (repeatable).",
    )
    args = ap.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    log_path = args.out_root / "run.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("===== 6-cell BioTest sweep with local Ollama qwen3-coder:30b =====", fh)
    log(f"out_root = {args.out_root}", fh)
    log(f"reps = {args.reps}  budget = {args.budget_s}s  max_iter = {args.max_iterations}", fh)
    log(f"LLM = ollama/qwen3-coder:30b", fh)

    seeds_clean = build_clean_seeds_dir(args.out_root / "seeds_clean", fh)

    cells = [
        c for c in CELLS
        if (not args.only or c.label in args.only)
        and c.label not in args.skip
    ]
    log(f"cells = {[c.label for c in cells]}", fh)

    all_results: list[dict[str, Any]] = []
    sweep_started = time.time()
    for cell in cells:
        cell_results = run_cell(cell, args, seeds_clean, fh)
        all_results.extend(cell_results)
        # Overwrite global results.json after each cell so partial
        # sweeps still leave usable data.
        (args.out_root / "results.json").write_text(
            json.dumps(all_results, indent=2), encoding="utf-8",
        )

    log(
        f"\n===== sweep complete in {(time.time() - sweep_started) / 60:.1f} min =====",
        fh,
    )
    fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
