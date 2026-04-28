#!/usr/bin/env python3
"""Recover the 6 missing reps from the parallel cascade sweep.

vcfpy/VCF + biopython/SAM hit Windows TerminateProcess at the 90-min
wall cap during reps 1/2/3 — coverage.py's atexit never fired, so
.coverage SQLite was missing/corrupt. Each cell's accumulated seeds_dir
is intact (cascade preserved); only the post-rep coverage measurement
was lost.

Recovery strategy:
  - Re-run those 6 reps individually with max_iter=1 (so biotest's
    Phase D does ONE iteration only, exits naturally in ~30-50 min,
    well below the 90-min wall cap; coverage.py's atexit fires cleanly).
  - Reuse each cell's existing <cell>/work/seeds/ dir (the cascade-
    accumulated state at end of rep 3). Reps 1/2/3 will all start
    from the SAME post-rep-3 corpus, so their std measures Phase C /
    Hypothesis-RNG variance against the maximally-cascaded corpus.
  - Reset each cell's <cell>/work/data/ and <cell>/work/coverage_artifacts/
    between reps (so each rep is an independent measurement).
  - Run vcfpy_vcf and biopython_sam in parallel.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
LOCK = threading.Lock()


# Two failed cells with their failed-rep indices.
TARGETS = [
    {"cell": "vcfpy_vcf",     "sut": "vcfpy",     "fmt": "VCF",
     "reps_to_redo": [1, 2, 3], "kind": "coveragepy"},
    {"cell": "biopython_sam", "sut": "biopython", "fmt": "SAM",
     "reps_to_redo": [1, 2, 3], "kind": "coveragepy"},
]


def log(label: str, msg: str, fh) -> None:
    with LOCK:
        line = f"[{time.strftime('%H:%M:%S')}] [{label:14s}] {msg}"
        try:
            print(line, flush=True)
        except UnicodeEncodeError:
            print(line.encode("ascii", "replace").decode("ascii"), flush=True)
        fh.write(line + "\n")
        fh.flush()


def write_recovery_config(target: dict, work_dir: Path, rep: int,
                          cfg_out: Path) -> Path:
    """Same per-cell paths the cascade orchestrator used, but max_iter=1
    so biotest exits naturally before the 90-min wall cap."""
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))

    src.setdefault("phase_a", {})["enabled"] = False
    src.setdefault("phase_b", {}).setdefault("llm", {})["model"] = "deepseek-chat"
    src["phase_b"]["llm"]["temperature"] = 0.0
    src["phase_b"]["llm"]["max_retries"] = 3
    src["phase_b"]["registry_path"] = str(work_dir / "data" / "mr_registry.json")

    pc = src.setdefault("phase_c", {})
    pc["format_filter"] = target["fmt"]
    pc["seeds_dir"] = str(work_dir / "seeds")
    pc["output_dir"] = str(work_dir / "bug_reports")
    pc["det_report_path"] = str(work_dir / "data" / "det_report.json")
    pc["corpus_keeper"] = {"enabled": True, "max_files_per_format": 2000}

    cov = src.setdefault("coverage", {})
    cov["enabled"] = True
    cov["jacoco_report_dir"] = str(work_dir / "coverage_artifacts" / "jacoco")
    cov["coveragepy_data_file"] = str(
        work_dir / "coverage_artifacts" / ".coverage"
    )
    cov["pysam_coverage_dir"] = str(work_dir / "coverage_artifacts" / "pysam")
    cov["gcovr_report_path"] = str(work_dir / "coverage_artifacts" / "gcovr.json")
    cov["noodles_report_path"] = str(
        work_dir / "coverage_artifacts" / "noodles" / "llvm-cov.json"
    )
    cov["noodles_profile_dir"] = str(
        work_dir / "coverage_artifacts" / "noodles"
    )

    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = target["sut"]
    fb["max_iterations"] = 1  # KEY: 1 iter only → graceful exit before wall cap
    fb["plateau_patience"] = 2
    fb["coverage_plateau_patience"] = 2
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = 80
    fb["state_path"] = str(work_dir / "data" / "feedback_state.json")
    fb["attempts_path"] = str(work_dir / "data" / "rule_attempts.json")
    fb["coverage_report_path"] = str(work_dir / "data" / "coverage_report.json")
    fb["scc_report_path"] = str(work_dir / "data" / "scc_report.json")
    fb.setdefault("seed_synthesis", {})["enabled"] = True
    fb["seed_synthesis"]["max_seeds_per_iteration"] = 5
    fb["seed_synthesis"]["max_file_bytes"] = 524288

    src["phase_e"] = {"enabled": False}
    src.setdefault("global", {})["seed_rng"] = 42 + rep

    cfg_out.parent.mkdir(parents=True, exist_ok=True)
    cfg_out.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")
    return cfg_out


def reset_data_and_cov(work_dir: Path) -> None:
    """Wipe data/ + coverage_artifacts/ but PRESERVE seeds/ (cascade)."""
    for sub in ("data", "coverage_artifacts", "bug_reports"):
        d = work_dir / sub
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
    (work_dir / "coverage_artifacts" / "jacoco").mkdir(exist_ok=True)
    (work_dir / "coverage_artifacts" / "noodles").mkdir(exist_ok=True)
    (work_dir / "coverage_artifacts" / "pysam").mkdir(exist_ok=True)


def run_biotest(cfg_path: Path, log_path: Path,
                budget_s: int = 4500) -> tuple[int, float]:
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path), "--phase", "D", "--verbose",
    ]
    started = time.time()
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(
            cmd, stdout=lf, stderr=subprocess.STDOUT,
            env=os.environ.copy(), cwd=str(REPO_ROOT),
        )
        try:
            proc.wait(timeout=budget_s)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=15)
    elapsed = time.time() - started
    return (proc.returncode if proc.returncode is not None else -1,
            elapsed)


def measure_coveragepy(work_dir: Path, target: dict) -> dict:
    src = work_dir / "coverage_artifacts" / ".coverage"
    out = {"line_pct": 0.0, "covered": 0, "total": 0, "status": "missing"}
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
        out["status"] = "convert_failed"
        return out
    proc = subprocess.run(
        [sys.executable,
         str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
         "--report", str(dest),
         "--sut", target["sut"], "--format", target["fmt"]],
        capture_output=True, timeout=120, cwd=str(REPO_ROOT),
    )
    for line in proc.stdout.decode(errors="replace").splitlines():
        if "OVERALL" in line and "weighted" in line:
            try:
                tail = line.split(")", 1)[1].strip()
                frac, pct = tail.split("(")
                c, t = frac.strip().split("/")
                pct = pct.replace("%", "").replace(")", "").strip()
                out["line_pct"], out["covered"], out["total"] = (
                    float(pct), int(c), int(t)
                )
                break
            except Exception:
                continue
    if out["total"] > 0:
        out["status"] = "ok"
    return out


def recover_cell(target: dict, fh) -> list[dict]:
    cell_dir = REPO_ROOT / "compares" / "results" / "coverage" / "biotest_4rep_cascade_20260427" / target["cell"]
    work_dir = cell_dir / "work"
    if not work_dir.exists():
        log(target["cell"], "no work dir — skipping", fh)
        return []

    seeds_count = sum(1 for _ in (work_dir / "seeds" / target["fmt"].lower()).glob(f"*.{target['fmt'].lower()}"))
    log(target["cell"], f"=== recovery start; seeds_dir has {seeds_count} files ===", fh)

    results = []
    for rep in target["reps_to_redo"]:
        log(target["cell"], f"--- recovering rep {rep} ---", fh)
        reset_data_and_cov(work_dir)

        rep_dir = cell_dir / f"run_{rep}"
        cfg_path = rep_dir / f"biotest_config.recover_rep{rep}.yaml"
        write_recovery_config(target, work_dir, rep, cfg_path)

        biotest_log = rep_dir / "biotest_recover.log"
        log(target["cell"], f"    cmd: biotest --phase D (max_iter=1)", fh)
        rc, elapsed = run_biotest(cfg_path, biotest_log, budget_s=4500)
        log(target["cell"], f"    exit={rc} elapsed={elapsed:.0f}s", fh)

        cov = measure_coveragepy(work_dir, target)
        rec = {
            "cell": target["cell"], "sut": target["sut"], "format": target["fmt"],
            "rep": rep, "exit_code": rc, "elapsed_s": round(elapsed, 1),
            "max_iterations": 1, "phases": "D",
            "rep_kind": "recovery",
            "seeds_count_at_start": seeds_count,
            **cov,
        }
        # Overwrite the missing measurement
        (rep_dir / "measurement.json").write_text(
            json.dumps(rec, indent=2), encoding="utf-8",
        )
        results.append(rec)
        log(target["cell"],
            f"    -> line={cov['line_pct']}% covered={cov['covered']}/{cov['total']} status={cov['status']}",
            fh)

    log(target["cell"], "=== recovery complete ===", fh)
    return results


def main():
    out_root = REPO_ROOT / "compares" / "results" / "coverage" / "biotest_4rep_cascade_20260427"
    log_path = out_root / "recovery.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)
    print(f"[recovery] targets: {[t['cell'] for t in TARGETS]}", flush=True)
    fh.write(f"[recovery] targets: {[t['cell'] for t in TARGETS]}\n")

    started = time.time()
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(recover_cell, t, fh): t for t in TARGETS}
        for fut, t in futures.items():
            try:
                fut.result()
            except Exception as e:
                fh.write(f"[{t['cell']}] FAILED: {e}\n")
                print(f"[{t['cell']}] FAILED: {e}", flush=True)
    elapsed = (time.time() - started) / 60
    fh.write(f"[recovery] done in {elapsed:.1f} min\n")
    print(f"[recovery] done in {elapsed:.1f} min", flush=True)
    fh.close()


if __name__ == "__main__":
    main()
