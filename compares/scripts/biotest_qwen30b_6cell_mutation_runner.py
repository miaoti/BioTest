#!/usr/bin/env python3
"""6-cell BioTest MUTATION sweep using local Ollama (qwen3-coder:30b).

After the coverage sweep finishes (`biotest_qwen30b_6cell_runner.py`),
this script runs BioTest 4 more times per cell — one fresh corpus per
rep — and measures the resulting **mutation score** instead of line
coverage. Per the user's request:

    "Once the coverage is done, you will need to run the tool four times
     again to see the mutation score for each SUT."

Each rep:
  1. Reset state (mr_registry, feedback_state, etc.) so Phase B re-mines
     fresh and Phase D starts at iteration 0.
  2. Reset the auxiliary corpus dirs (seeds/<fmt>_struct/,
     seeds/<fmt>_rawfuzz/, etc.) and any kept_*/synthetic_* leftovers in
     seeds/<fmt>/ — this is the user's fairness invariant: SUT-1's
     rep-N corpus must not pollute SUT-2's rep-N+1 corpus.
  3. Run `biotest.py --phase A,D,E` with the same config the coverage
     sweep used (LLM=ollama/qwen3-coder:30b, max_iter=30, budget=1800s).
  4. Stage the resulting corpus (Tier-1+2 + Phase E aux dirs) into a
     per-rep dir and dispatch the per-cell mutation engine:
       - htsjdk_VCF / htsjdk_SAM → PIT (via Docker biotest-bench)
       - vcfpy_VCF              → mutmut
       - noodles_VCF            → cargo-mutants
       - biopython_SAM          → atheris-mutmut (via Docker)
       - seqan3_SAM             → libfuzzer/mull (via mutation_driver.py)
  5. Read killed/reachable from `summary.json`, save per-rep
     `measurement.json`.

Cells run sequentially (state collision avoidance + single Ollama
client). 4 reps × 6 cells = 24 BioTest+mutation runs.
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
DOCKER_IMAGE = "biotest-bench:latest"


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
    label: str
    sut: str
    fmt: str
    runner: str          # "host" | "container"
    biotest_runner: str  # how to invoke biotest.py for this cell
    mutation_engine: str # "pit" | "mutmut" | "cargo_mutants" | "atheris_mutmut" | "libfuzzer"
    coverage_kind: str
    reset_paths: list[str] = field(default_factory=list)
    coverage_artefact: str = ""
    adapter_override: str | None = None
    coverage_binary_override: str | None = None


CELLS: list[Cell] = [
    Cell(
        label="htsjdk_vcf", sut="htsjdk", fmt="VCF",
        runner="host", biotest_runner="host",
        mutation_engine="pit",
        coverage_kind="jacoco",
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        coverage_artefact="coverage_artifacts/jacoco/jacoco.xml",
    ),
    Cell(
        label="htsjdk_sam", sut="htsjdk", fmt="SAM",
        runner="host", biotest_runner="host",
        mutation_engine="pit",
        coverage_kind="jacoco",
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        coverage_artefact="coverage_artifacts/jacoco/jacoco.xml",
    ),
    Cell(
        label="vcfpy_vcf", sut="vcfpy", fmt="VCF",
        runner="host", biotest_runner="host",
        mutation_engine="mutmut",
        coverage_kind="coveragepy",
        reset_paths=["coverage_artifacts/.coverage"],
        coverage_artefact="coverage_artifacts/.coverage",
    ),
    Cell(
        label="biopython_sam", sut="biopython", fmt="SAM",
        runner="host", biotest_runner="host",
        mutation_engine="atheris_mutmut",
        coverage_kind="coveragepy",
        reset_paths=["coverage_artifacts/.coverage"],
        coverage_artefact="coverage_artifacts/.coverage",
    ),
    Cell(
        label="noodles_vcf", sut="noodles", fmt="VCF",
        runner="container", biotest_runner="container",
        mutation_engine="cargo_mutants",
        coverage_kind="llvmcov",
        reset_paths=["coverage_artifacts/noodles/llvm-cov.json"],
        coverage_artefact="coverage_artifacts/noodles/llvm-cov.json",
    ),
    Cell(
        label="seqan3_sam", sut="seqan3", fmt="SAM",
        runner="container", biotest_runner="container",
        mutation_engine="libfuzzer",
        coverage_kind="gcovr",
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

# Same baseline-seed strategy as the coverage runner — see comment
# there. qwen3-coder:30b cannot drive Phase B mining; the baseline
# is the only way to get non-empty corpus + non-zero mutation score.
BASELINE_REGISTRY = "data/mr_registry.pre_fullD.backup.json"


AUX_CORPUS_DIRS = (
    "seeds/vcf_struct", "seeds/sam_struct",
    "seeds/vcf_rawfuzz", "seeds/sam_rawfuzz",
    "seeds/vcf_diverse", "seeds/sam_diverse",
    "seeds/vcf_bytefuzz", "seeds/sam_bytefuzz",
)
TAINTED_SEED_GLOBS = (
    ("seeds/vcf", "kept_*.vcf"),
    ("seeds/sam", "kept_*.sam"),
    ("seeds/vcf", "synthetic_*.vcf"),
    ("seeds/sam", "synthetic_*.sam"),
)


# ---------------------------------------------------------------------------
# Logging + state helpers (shared with coverage runner)
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


def reset_state(fh) -> None:
    """Truly-fresh state for each rep — no pre-seeded registry."""
    for rel in STATE_FILES:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                p.unlink()
                log(f"    reset state: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)


def reset_aux_corpora(fh) -> None:
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
    if cell.coverage_kind == "llvmcov":
        for p in (REPO_ROOT / "coverage_artifacts" / "noodles").glob("*.profraw"):
            try:
                p.unlink()
            except OSError:
                pass
    if cell.coverage_kind == "gcovr":
        for p in (REPO_ROOT / "harnesses" / "cpp" / "build").glob("*.gcda"):
            try:
                p.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Seeds clean-dir builder (Tier-1+2 only)
# ---------------------------------------------------------------------------

def build_clean_seeds_dir(tmp_root: Path, fh) -> Path:
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
# Per-rep BioTest config
# ---------------------------------------------------------------------------

def write_temp_config(
    cell: Cell, rep: int, out_dir: Path, seeds_root: Path,
    max_iterations: int, timeout_minutes: int,
) -> Path:
    src = yaml.safe_load(
        (REPO_ROOT / "biotest_config.yaml").read_text("utf-8")
    )
    phase_b = src.setdefault("phase_b", {})
    llm = phase_b.setdefault("llm", {})
    llm["model"] = "ollama/qwen3-coder:30b"
    llm["temperature"] = 0.0

    phase_c = src.setdefault("phase_c", {})
    phase_c["format_filter"] = cell.fmt
    seeds_abs = seeds_root.resolve()
    try:
        seeds_rel = seeds_abs.relative_to(REPO_ROOT.resolve()).as_posix()
        phase_c["seeds_dir"] = seeds_rel
    except ValueError:
        phase_c["seeds_dir"] = seeds_abs.as_posix()
    phase_c["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}

    if cell.adapter_override or cell.coverage_binary_override:
        for sut_cfg in phase_c.get("suts", []):
            if sut_cfg.get("name") == cell.sut:
                if cell.adapter_override:
                    sut_cfg["adapter"] = cell.adapter_override
                if cell.coverage_binary_override:
                    sut_cfg["coverage_binary"] = cell.coverage_binary_override

    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = cell.sut
    fb["max_iterations"] = max_iterations
    fb["plateau_patience"] = max_iterations + 1
    fb["coverage_plateau_patience"] = max_iterations + 1
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = timeout_minutes
    fb.setdefault("seed_synthesis", {})["enabled"] = False
    fb.setdefault("mr_synthesis", {})["enabled"] = False

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
# BioTest invocation (host + container)
# ---------------------------------------------------------------------------

def run_biotest_host(cfg_path: Path, budget_s: int, log_path: Path, fh) -> int:
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path),
        "--phase", "B,C,D,E",
        "--verbose",
    ]
    log(f"    biotest cmd: {' '.join(cmd)}", fh)
    log(f"    budget: {budget_s}s", fh)
    env = os.environ.copy()
    env["LLM_MODEL"] = "ollama/qwen3-coder:30b"
    env["LLM_TEMPERATURE"] = "0.0"
    started = time.time()
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(
            cmd, stdout=lf, stderr=subprocess.STDOUT,
            env=env, cwd=str(REPO_ROOT),
        )
        try:
            proc.wait(timeout=budget_s)
        except subprocess.TimeoutExpired:
            log(f"    biotest timeout after {budget_s}s - terminating", fh)
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
    elapsed = time.time() - started
    log(f"    biotest exit={proc.returncode} elapsed={elapsed:.1f}s", fh)
    return proc.returncode if proc.returncode is not None else -1


def run_biotest_container(cfg_rel: str, budget_s: int, log_path: Path, fh) -> int:
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
    log(f"    biotest cmd (container): /work/{cfg_rel}", fh)
    log(f"    budget: {budget_s}s", fh)
    started = time.time()
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT)
        try:
            proc.wait(timeout=budget_s + 120)
        except subprocess.TimeoutExpired:
            log(f"    biotest timeout - killing docker exec", fh)
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
    elapsed = time.time() - started
    log(f"    biotest exit={proc.returncode} elapsed={elapsed:.1f}s", fh)
    return proc.returncode if proc.returncode is not None else -1


# ---------------------------------------------------------------------------
# Mutation corpus staging
# ---------------------------------------------------------------------------

def stage_mutation_corpus(
    cell: Cell, rep: int, rep_dir: Path, fh,
) -> Path:
    """Stage corpus for the mutation engine: Tier-1+2 + Phase E aux.

    Output dir: rep_dir/corpus/. The mutation engine reads .vcf/.sam
    files from this single directory.
    """
    corpus_dir = rep_dir / "corpus"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    # Wipe any prior staging.
    for existing in corpus_dir.glob("*"):
        try:
            if existing.is_file():
                existing.unlink()
            elif existing.is_dir():
                shutil.rmtree(existing)
        except OSError:
            pass

    ext = cell.fmt.lower()
    seed_dir = REPO_ROOT / f"seeds/{ext}"
    struct_dir = REPO_ROOT / f"seeds/{ext}_struct"
    rawfuzz_dir = REPO_ROOT / f"seeds/{ext}_rawfuzz"

    copied = 0
    # Tier-1+2 — exclude any leaked out-tool prefix.
    for f in sorted(seed_dir.glob(f"*.{ext}")):
        if any(f.name.startswith(pref) for pref in OUT_TOOL_PREFIXES):
            continue
        try:
            shutil.copy2(f, corpus_dir / f.name)
            copied += 1
        except OSError:
            pass
    # Phase E aux outputs from THIS rep (auto-cleaned per rep above).
    for src_dir in (struct_dir, rawfuzz_dir):
        if not src_dir.is_dir():
            continue
        for f in sorted(src_dir.glob(f"*.{ext}")):
            try:
                shutil.copy2(f, corpus_dir / f.name)
                copied += 1
            except OSError:
                pass
    log(f"    staged mutation corpus: {copied} files at {corpus_dir.relative_to(REPO_ROOT)}", fh)
    return corpus_dir


# ---------------------------------------------------------------------------
# Mutation engine dispatch
# ---------------------------------------------------------------------------

def run_mutation_engine(
    cell: Cell, rep: int, corpus_dir: Path, mut_out_dir: Path,
    budget_s: int, log_path: Path, fh,
) -> int:
    """Dispatch to the per-cell mutation tool. Returns exit code.

    Output dir layout (matches mutation_driver.py + phase3_jazzer_pit.sh):
      mut_out_dir/
        summary.json     # {killed, reachable, score}
        driver.log
    """
    if mut_out_dir.exists():
        shutil.rmtree(mut_out_dir)
    mut_out_dir.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}

    if cell.mutation_engine == "pit":
        # phase3_jazzer_pit.sh expects the corpus to already be staged at
        # compares/results/coverage/<TOOL>/<cell>/run_0/corpus/. Stage a
        # symlink there so it picks up THIS rep's corpus.
        tool_label = f"biotest_qwen30b_rep{rep}"
        stage_root = REPO_ROOT / f"compares/results/coverage/{tool_label}/{cell.label}/run_0/corpus"
        if stage_root.exists():
            shutil.rmtree(stage_root)
        stage_root.mkdir(parents=True, exist_ok=True)
        for f in corpus_dir.glob("*"):
            if f.is_file():
                try:
                    shutil.copy2(f, stage_root / f.name)
                except OSError:
                    pass
        # Mutation output dir matches phase3 script's expectation.
        pit_out = REPO_ROOT / f"compares/results/mutation/{tool_label}/{cell.label}"
        if pit_out.exists():
            shutil.rmtree(pit_out)
        pit_out.mkdir(parents=True, exist_ok=True)

        ctr_name = f"qwen30b-rep{rep}-{cell.label}"
        subprocess.run(["docker", "rm", "-f", ctr_name],
                       capture_output=True, check=False)
        cmd = [
            "docker", "run", "--rm", "--name", ctr_name,
            "-v", f"{REPO_ROOT}:/work", "-w", "/work",
            "-e", f"TOOL={tool_label}",
            "-e", f"FORMATS={cell.fmt}",
            "-e", "THREADS=2",
            "-e", "CORPUS_MAX=300",
            "-e", "REPS=0",
            DOCKER_IMAGE,
            "bash", "/work/compares/scripts/phase3_jazzer_pit.sh",
        ]
        env["MSYS_NO_PATHCONV"] = "1"
        log(f"    mutation cmd: docker run {DOCKER_IMAGE} ... TOOL={tool_label}", fh)
        with log_path.open("wb") as lf:
            proc = subprocess.Popen(cmd, env=env, stdout=lf, stderr=subprocess.STDOUT)
            try:
                proc.wait(timeout=budget_s + 600)
            except subprocess.TimeoutExpired:
                log("    mutation timeout - terminating", fh)
                proc.terminate()
                try:
                    proc.wait(timeout=120)
                except subprocess.TimeoutExpired:
                    proc.kill()
        # Copy summary.json into our per-rep dir so aggregation finds it.
        src_sum = pit_out / "summary.json"
        if src_sum.exists():
            shutil.copy2(src_sum, mut_out_dir / "summary.json")
        return proc.returncode or -1

    if cell.mutation_engine == "mutmut":
        cmd = [
            sys.executable, str(REPO_ROOT / "compares/scripts/mutation_driver.py"),
            "--tool", "biotest", "--sut", cell.sut,
            "--corpus", str(corpus_dir),
            "--out", str(mut_out_dir),
            "--budget", str(budget_s),
            "--corpus-sample", "80",
        ]
    elif cell.mutation_engine == "cargo_mutants":
        cmd = [
            sys.executable, str(REPO_ROOT / "compares/scripts/mutation_driver.py"),
            "--tool", "biotest", "--sut", cell.sut,
            "--corpus", str(corpus_dir),
            "--out", str(mut_out_dir),
            "--budget", str(budget_s),
            "--corpus-sample", "120",
        ]
    elif cell.mutation_engine == "atheris_mutmut":
        # phase3_atheris_biopython.sh expects TOOL + BUDGET_S env. Stage
        # the corpus at the path that script reads from.
        tool_label = f"biotest_qwen30b_rep{rep}"
        stage_root = REPO_ROOT / f"compares/results/coverage/{tool_label}/{cell.label}/run_0/corpus"
        if stage_root.exists():
            shutil.rmtree(stage_root)
        stage_root.mkdir(parents=True, exist_ok=True)
        for f in corpus_dir.glob("*"):
            if f.is_file():
                try:
                    shutil.copy2(f, stage_root / f.name)
                except OSError:
                    pass
        bp_out = REPO_ROOT / f"compares/results/mutation/{tool_label}/{cell.label}"
        if bp_out.exists():
            shutil.rmtree(bp_out)
        bp_out.mkdir(parents=True, exist_ok=True)
        cmd = [
            "bash", "-c",
            f"TOOL={tool_label} BUDGET_S={budget_s} "
            f"bash compares/scripts/phase3_atheris_biopython.sh",
        ]
        log(f"    mutation cmd: {tool_label} (atheris_mutmut)", fh)
        with log_path.open("wb") as lf:
            proc = subprocess.Popen(cmd, env=env, stdout=lf, stderr=subprocess.STDOUT,
                                     cwd=str(REPO_ROOT))
            try:
                proc.wait(timeout=budget_s + 600)
            except subprocess.TimeoutExpired:
                log("    mutation timeout - terminating", fh)
                proc.terminate()
                try:
                    proc.wait(timeout=120)
                except subprocess.TimeoutExpired:
                    proc.kill()
        src_sum = bp_out / "summary.json"
        if src_sum.exists():
            shutil.copy2(src_sum, mut_out_dir / "summary.json")
        return proc.returncode or -1
    elif cell.mutation_engine == "libfuzzer":
        cmd = [
            sys.executable, str(REPO_ROOT / "compares/scripts/mutation_driver.py"),
            "--tool", "biotest", "--sut", cell.sut,
            "--corpus", str(corpus_dir),
            "--out", str(mut_out_dir),
            "--format", cell.fmt,
            "--budget", str(budget_s),
            "--corpus-sample", "120",
        ]
    else:
        raise ValueError(f"unknown engine {cell.mutation_engine}")

    log(f"    mutation cmd: {' '.join(cmd[:6])}...", fh)
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(cmd, env=env, stdout=lf, stderr=subprocess.STDOUT,
                                 cwd=str(REPO_ROOT))
        try:
            proc.wait(timeout=budget_s + 600)
        except subprocess.TimeoutExpired:
            log("    mutation timeout - terminating", fh)
            proc.terminate()
            try:
                proc.wait(timeout=120)
            except subprocess.TimeoutExpired:
                proc.kill()
    return proc.returncode if proc.returncode is not None else -1


def read_mutation_summary(cell: Cell, rep: int, mut_out_dir: Path, fh) -> dict[str, Any]:
    """Read mutation engine output summary.json. Returns
    {killed, reachable, score, status}.

    For vcfpy/mutmut the summary may need rederivation from .meta files
    when mutmut 3.x emits the broken text-parse path."""
    summary = mut_out_dir / "summary.json"
    if not summary.exists():
        # PIT/atheris paths copy summary.json themselves; if missing,
        # check the engine-specific output too.
        log(f"    summary.json missing in {mut_out_dir}", fh)
        return {"killed": 0, "reachable": 0, "score": 0.0, "status": "missing"}
    try:
        d = json.loads(summary.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        log(f"    summary.json parse error: {e}", fh)
        return {"killed": 0, "reachable": 0, "score": 0.0, "status": "parse_error"}

    # vcfpy mutmut rederivation
    if cell.label == "vcfpy_vcf" and d.get("killed", 0) == 0:
        rederive = REPO_ROOT / "compares/scripts/mutation/rederive_from_meta.py"
        if rederive.exists():
            subprocess.run(
                [sys.executable, str(rederive), str(mut_out_dir),
                 "--package", "vcfpy"],
                check=False, capture_output=True,
            )
            try:
                d = json.loads(summary.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass

    ms = d.get("mutation_score", d)
    killed = ms.get("killed", d.get("killed", 0))
    reachable = ms.get("reachable", d.get("reachable", 0))
    if reachable == 0:
        return {"killed": killed, "reachable": reachable, "score": 0.0,
                "status": "zero_reachable"}
    return {
        "killed": killed,
        "reachable": reachable,
        "score": killed / reachable,
        "status": "ok",
    }


# ---------------------------------------------------------------------------
# Cell + rep orchestration
# ---------------------------------------------------------------------------

def run_cell(
    cell: Cell, args: argparse.Namespace, seeds_clean: Path, fh,
) -> list[dict[str, Any]]:
    cell_dir = args.out_root / cell.label
    cell_dir.mkdir(parents=True, exist_ok=True)
    log(
        f"\n### CELL: {cell.label} (sut={cell.sut} fmt={cell.fmt} "
        f"engine={cell.mutation_engine} runner={cell.runner})",
        fh,
    )
    cell_results: list[dict[str, Any]] = []

    for rep in range(args.reps):
        rep_dir = cell_dir / f"run_{rep}"
        rep_dir.mkdir(parents=True, exist_ok=True)
        log(f"  -- rep {rep} --", fh)

        # Phase 1: reset everything for fairness
        reset_state(fh)
        reset_aux_corpora(fh)
        reset_cell_artefacts(cell, fh)

        # Phase 2: run BioTest fresh
        cfg_path = write_temp_config(
            cell, rep, rep_dir, seeds_clean,
            max_iterations=args.max_iterations,
            timeout_minutes=args.timeout_minutes,
        )
        cfg_abs = cfg_path.resolve()
        cfg_rel = cfg_abs.relative_to(REPO_ROOT.resolve()).as_posix()
        biotest_log = rep_dir / "biotest.log"
        t0 = time.time()
        if cell.biotest_runner == "host":
            biotest_exit = run_biotest_host(cfg_path, args.biotest_budget_s, biotest_log, fh)
        else:
            biotest_exit = run_biotest_container(cfg_rel, args.biotest_budget_s, biotest_log, fh)
        biotest_elapsed = time.time() - t0

        # Phase 3: stage mutation corpus + dispatch engine
        corpus_dir = stage_mutation_corpus(cell, rep, rep_dir, fh)
        mut_out_dir = rep_dir / "mutation"
        mut_log = rep_dir / "mutation.log"
        t1 = time.time()
        mut_exit = run_mutation_engine(
            cell, rep, corpus_dir, mut_out_dir,
            args.mutation_budget_s, mut_log, fh,
        )
        mut_elapsed = time.time() - t1

        # Phase 4: read mutation score
        score = read_mutation_summary(cell, rep, mut_out_dir, fh)

        rec = {
            "cell": cell.label,
            "sut": cell.sut,
            "format": cell.fmt,
            "rep": rep,
            "biotest_exit": biotest_exit,
            "biotest_elapsed_s": round(biotest_elapsed, 1),
            "mutation_exit": mut_exit,
            "mutation_elapsed_s": round(mut_elapsed, 1),
            "engine": cell.mutation_engine,
            "max_iterations": args.max_iterations,
            "phases": "B,C,D,E + mutation",
            "llm_model": "ollama/qwen3-coder:30b",
            "corpus_size": len(list(corpus_dir.glob("*"))) if corpus_dir.exists() else 0,
            **score,
        }
        cell_results.append(rec)
        (rep_dir / "measurement.json").write_text(
            json.dumps(rec, indent=2), encoding="utf-8",
        )
        log(
            f"    -> mutation score={rec.get('score', 0)*100:.2f}% "
            f"(killed={rec.get('killed', 0)}/{rec.get('reachable', 0)}) "
            f"corpus={rec['corpus_size']} status={rec.get('status', '?')}",
            fh,
        )

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
        default=REPO_ROOT / "compares" / "results" / "mutation"
        / f"biotest_qwen30b_4rep_{time.strftime('%Y%m%d')}",
    )
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument(
        "--biotest-budget-s", type=int, default=1800,
        help="Per-rep wall cap for BioTest (default 1800 s = 30 min).",
    )
    ap.add_argument(
        "--mutation-budget-s", type=int, default=3600,
        help="Per-rep wall cap for the mutation engine (default 3600 s "
        "= 60 min). PIT often runs 30-60 min on htsjdk; cargo-mutants "
        "needs at least 2h on the noodles crate.",
    )
    ap.add_argument(
        "--max-iterations", type=int, default=30,
        help="biotest Phase D max iterations (default 30 — biotest "
        "self-terminates after timeout_minutes).",
    )
    ap.add_argument(
        "--timeout-minutes", type=int, default=25,
        help="biotest's between-iteration self-terminate cap.",
    )
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--skip", action="append", default=[])
    args = ap.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    log_path = args.out_root / "run.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("===== 6-cell BioTest MUTATION sweep with local Ollama qwen3-coder:30b =====", fh)
    log(f"out_root = {args.out_root}", fh)
    log(f"reps = {args.reps}  biotest_budget = {args.biotest_budget_s}s  "
        f"mutation_budget = {args.mutation_budget_s}s", fh)
    log(f"max_iter = {args.max_iterations}", fh)
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
        (args.out_root / "results.json").write_text(
            json.dumps(all_results, indent=2), encoding="utf-8",
        )

    log(
        f"\n===== mutation sweep complete in "
        f"{(time.time() - sweep_started) / 60:.1f} min =====",
        fh,
    )
    fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
