"""Run mutation + bug_bench across all (config, rep) cells of the 4-rep study.

Drives 3 config × 4 reps × 6 cells = 72 cell-mutation invocations and
3 config × 4 reps bug_bench invocations.

Per config layout (different shapes):
  E0_baseline/results_4big_runs/run_{a,b,c,d}/<cell>/work/seeds/...
  E1S_strict/results_4big_runs/run_{a,b,c,d}/<cell>/work/seeds/...
  E2_no_phase_d/results_4rep/<cell>/work/seeds/...   (each cell has 4 reps under work/, but seeds is shared snapshot)

For E2 (cumulative=False), each rep has its OWN coverage_artifacts but
SAME seeds dir (cumulative=False does not wipe seeds). For mutation
purposes, just take the final seed corpus per cell (after all 4 reps).

Mutation engines:
  htsjdk → phase3_jazzer_pit.sh (TOOL=biotest_<config>)
  vcfpy / noodles / seqan3 → mutation_driver.py
  biopython → phase3_atheris_biopython.sh (TOOL=biotest_<config>)

Output:
  compares/ApplicationStudy/<config>/results_metrics/<rep_or_run>/<cell>/
    {summary.json, stdout.txt, stderr.txt}
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
E1_DIR = ROOT / "E1_no_phase_a"
sys.path.insert(0, str(E1_DIR))

# Reuse helpers from run_metrics.py
from run_metrics import (  # type: ignore
    _bash_exe,
    _msys_path,
    _run_mutation_subproc,
    MUTATION_CELLS,
)

CONFIGS = {
    "E0":  {"sub": "E0_baseline",     "layout": "big_runs", "ids": ["a", "b", "c", "d"]},
    "E1S": {"sub": "E1S_strict",      "layout": "big_runs", "ids": ["a", "b", "c", "d"]},
    "E2":  {"sub": "E2_no_phase_d",   "layout": "reps",     "ids": [0, 1, 2, 3]},
    "E3":  {"sub": "E3_no_a_no_d",    "layout": "reps",     "ids": [0, 1, 2, 3]},
}


def _log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] [metrics_4rep] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((line + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()


def _corpus_for(config: str, run_id, cell: str) -> Path:
    """Return path to the cell's seed corpus for a given config + run/rep."""
    cfg = CONFIGS[config]
    sub = cfg["sub"]
    if cfg["layout"] == "big_runs":
        return (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                "results_4big_runs" / f"run_{run_id}" / cell / "work" / "seeds")
    return (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
            "results_4rep" / cell / "work" / "seeds")


def _combined_corpus_dir(config: str, run_id, cell: str, fmt: str) -> Path:
    """Stage the cell's primary + Phase E aug into a single dir for mutation."""
    seeds = _corpus_for(config, run_id, cell)
    fmt_lower = fmt.lower()
    out_dir = (
        PROJECT_ROOT / "compares" / "ApplicationStudy" / CONFIGS[config]["sub"] /
        "results_metrics" / f"{run_id}" / cell / "combined_corpus"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    sources = [
        seeds / fmt_lower,
        seeds / f"{fmt_lower}_struct",
        seeds / f"{fmt_lower}_rawfuzz",
    ]
    n = 0
    for src in sources:
        if not src.is_dir():
            continue
        for f in src.iterdir():
            if not f.is_file() or not f.name.endswith(f".{fmt_lower}"):
                continue
            target = out_dir / f.name
            if not target.exists():
                try:
                    shutil.copy2(f, target)
                    n += 1
                except OSError:
                    pass
    return out_dir


def run_mutation_for_config(config: str, budget_s: int = 3600) -> None:
    """Run mutation 4-rep for all 6 cells × 4 reps of a config."""
    cfg = CONFIGS[config]
    for run_id in cfg["ids"]:
        for sut, fmt in MUTATION_CELLS:
            cell = f"{sut}_{fmt.lower()}"
            corpus_dir = _combined_corpus_dir(config, run_id, cell, fmt)
            files = list(corpus_dir.glob(f"*.{fmt.lower()}"))
            if not files:
                _log(f"{config}[{run_id}] {cell}: skip — empty corpus")
                continue

            out_dir = (PROJECT_ROOT / "compares" / "ApplicationStudy" /
                       cfg["sub"] / "results_metrics" / f"{run_id}" / cell)
            out_dir.mkdir(parents=True, exist_ok=True)

            # Skip if summary already exists (idempotent restart).
            existing = out_dir / "summary.json"
            if existing.exists():
                _log(f"{config}[{run_id}] {cell}: skip — already has summary")
                continue

            _run_one_mutation_cell(
                config=config, run_id=run_id, sut=sut, fmt=fmt,
                cell=cell, corpus_dir=corpus_dir, out_dir=out_dir,
                budget_s=budget_s,
            )


def _run_one_mutation_cell(
    config: str, run_id, sut: str, fmt: str, cell: str,
    corpus_dir: Path, out_dir: Path, budget_s: int,
) -> None:
    """Dispatch to the right mutation backend per SUT."""
    tool_name = f"biotest_{config}_{run_id}"

    if sut == "htsjdk":
        # phase3_jazzer_pit.sh
        stage_dir = (PROJECT_ROOT / "compares" / "results" / "coverage" /
                     tool_name / f"htsjdk_{fmt.lower()}" / "run_0" / "corpus")
        stage_dir.mkdir(parents=True, exist_ok=True)
        for f in corpus_dir.iterdir():
            if not f.is_file():
                continue
            target = stage_dir / f.name
            if not target.exists():
                try:
                    shutil.copy2(f, target)
                except OSError:
                    pass
        script = _msys_path(PROJECT_ROOT / "compares" / "scripts" / "phase3_jazzer_pit.sh")
        local_bin = _msys_path(E1_DIR / "bin")
        pit_dir = _msys_path(E1_DIR / "bin" / "pit")
        cmd = [_bash_exe(), script]
        env = {
            **os.environ,
            "PATH": local_bin + ":" + os.environ.get("PATH", ""),
            "PIT_DIR": pit_dir,
            "TOOL": tool_name,
            "REPS": "0",
            "FORMATS": fmt,
            "OUT_ROOT": _msys_path(out_dir.parent),
            "COVERAGE_ROOT": _msys_path(
                PROJECT_ROOT / "compares" / "results" / "coverage" / tool_name
            ),
            "CORPUS_MAX": "500",
            "PYTHONIOENCODING": "utf-8",
        }
    elif sut == "biopython":
        script = _msys_path(PROJECT_ROOT / "compares" / "scripts" / "phase3_atheris_biopython.sh")
        cmd = [_bash_exe(), script]
        env = {
            **os.environ,
            "TOOL": tool_name,
            "BUDGET_S": str(budget_s),
            "CORPUS_DIR": _msys_path(corpus_dir),
            "OUT_DIR": _msys_path(out_dir),
            "PYTHONIOENCODING": "utf-8",
        }
    else:
        cmd = [
            "py", "-3.12",
            str(PROJECT_ROOT / "compares" / "scripts" / "mutation_driver.py"),
            "--tool", "biotest",
            "--sut", sut,
            "--format", fmt,
            "--corpus", str(corpus_dir),
            "--budget", str(budget_s),
            "--out", str(out_dir),
        ]
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}

    _log(f"{config}[{run_id}] {cell}: launching ({len(list(corpus_dir.iterdir()))} files, budget {budget_s}s)")
    results = {fmt: {}}
    _run_mutation_subproc(cmd, env, out_dir, results, fmt, cell, budget_s)
    _log(f"{config}[{run_id}] {cell}: done — {results[fmt].get(cell, {})}")


def run_bug_bench_for_config(config: str, budget_s: int = 600) -> None:
    """Run bug_bench against each rep's final corpus for the config."""
    cfg = CONFIGS[config]
    sub = cfg["sub"]
    manifest = PROJECT_ROOT / "compares" / "bug_bench" / "manifest.json"
    if not manifest.exists():
        _log("bug_bench manifest missing — skip")
        return

    for run_id in cfg["ids"]:
        out_dir = (PROJECT_ROOT / "compares" / "ApplicationStudy" /
                   sub / "results_metrics" / f"{run_id}" / "bug_bench")
        out_dir.mkdir(parents=True, exist_ok=True)
        if (out_dir / "aggregate.json").exists():
            _log(f"{config}[{run_id}] bug_bench: skip — already done")
            continue

        # Use the cell-level combined corpus dirs for vcf+sam.
        vcf_dir = (PROJECT_ROOT / "compares" / "ApplicationStudy" /
                   sub / "results_metrics" / f"{run_id}" / "htsjdk_vcf" / "combined_corpus")
        sam_dir = (PROJECT_ROOT / "compares" / "ApplicationStudy" /
                   sub / "results_metrics" / f"{run_id}" / "htsjdk_sam" / "combined_corpus")
        if not vcf_dir.exists() or not sam_dir.exists():
            _log(f"{config}[{run_id}] bug_bench: skip — corpus dirs missing")
            continue

        cmd = [
            "py", "-3.12",
            str(PROJECT_ROOT / "compares" / "scripts" / "bug_bench_driver.py"),
            "--manifest", str(manifest),
            "--out", str(out_dir),
            "--time-budget-s", str(budget_s),
            "--seed-corpus-vcf", str(vcf_dir),
            "--seed-corpus-sam", str(sam_dir),
            "--only-tool", "biotest",
        ]
        _log(f"{config}[{run_id}] bug_bench: launching")
        try:
            r = subprocess.run(
                cmd, cwd=str(PROJECT_ROOT),
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                timeout=budget_s * 200,
                capture_output=True, text=True,
                encoding="utf-8", errors="replace",
            )
            (out_dir / "stdout.txt").write_text(r.stdout, encoding="utf-8", errors="replace")
            (out_dir / "stderr.txt").write_text(r.stderr, encoding="utf-8", errors="replace")
            _log(f"{config}[{run_id}] bug_bench: done (exit {r.returncode})")
        except Exception as e:
            _log(f"{config}[{run_id}] bug_bench: FAIL {e}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, choices=list(CONFIGS.keys()) + ["ALL"])
    p.add_argument("--step", choices=("mutation", "bug_bench", "all"), default="all")
    p.add_argument("--mutation-budget-s", type=int, default=1800)
    p.add_argument("--bug-bench-budget-s", type=int, default=600)
    args = p.parse_args()

    configs = list(CONFIGS.keys()) if args.config == "ALL" else [args.config]

    for cfg in configs:
        _log(f"=== config {cfg} ===")
        if args.step in ("mutation", "all"):
            run_mutation_for_config(cfg, budget_s=args.mutation_budget_s)
        if args.step in ("bug_bench", "all"):
            run_bug_bench_for_config(cfg, budget_s=args.bug_bench_budget_s)

    _log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
