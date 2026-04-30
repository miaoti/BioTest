#!/usr/bin/env python3
"""Parameterized recovery for vcfpy_vcf + biopython_sam reps that hit
Windows TerminateProcess at the 90-min wall cap (status=missing).

Same strategy as biotest_recover_failed_reps.py but takes --out-root so
it can be reused across multiple big runs (run2/run3/run4).

Usage:
    py -3.12 compares/scripts/biotest_recover_failed_reps_param.py \\
        --out-root compares/results/coverage/biotest_4rep_cascade_run2_20260429
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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
LOCK = threading.Lock()


TARGETS = [
    {"cell": "vcfpy_vcf",     "sut": "vcfpy",     "fmt": "VCF",
     "kind": "coveragepy"},
    {"cell": "biopython_sam", "sut": "biopython", "fmt": "SAM",
     "kind": "coveragepy"},
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
    fb["max_iterations"] = 1
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
    """Wipe data/ + coverage_artifacts/ but PRESERVE seeds/."""
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


def find_failed_reps(cell_dir: Path) -> list[int]:
    """Return rep indices whose measurement.json has status != 'ok'."""
    failed = []
    for rep in range(4):
        m = cell_dir / f"run_{rep}" / "measurement.json"
        if not m.exists():
            failed.append(rep)
            continue
        try:
            data = json.loads(m.read_text(encoding="utf-8"))
            if data.get("status") != "ok":
                failed.append(rep)
        except Exception:
            failed.append(rep)
    return failed


def recover_cell(target: dict, out_root: Path, fh) -> list[dict]:
    cell_dir = out_root / target["cell"]
    work_dir = cell_dir / "work"
    if not work_dir.exists():
        log(target["cell"], "no work dir — skipping", fh)
        return []

    failed = find_failed_reps(cell_dir)
    if not failed:
        log(target["cell"], "no failed reps — skipping recovery", fh)
        return []

    seeds_subdir = target["fmt"].lower()
    seeds_count = sum(
        1 for _ in (work_dir / "seeds" / seeds_subdir).glob(f"*.{seeds_subdir}")
    )
    log(target["cell"],
        f"=== recovery start; failed reps: {failed}; seeds_dir has {seeds_count} files ===",
        fh)

    results = []
    for rep in failed:
        log(target["cell"], f"--- recovering rep {rep} ---", fh)
        reset_data_and_cov(work_dir)

        rep_dir = cell_dir / f"run_{rep}"
        cfg_path = rep_dir / f"biotest_config.recover_rep{rep}.yaml"
        write_recovery_config(target, work_dir, rep, cfg_path)

        biotest_log = rep_dir / "biotest_recover.log"
        log(target["cell"], "    cmd: biotest --phase D (max_iter=1)", fh)
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", type=Path, required=True,
                    help="Root dir of the big-run cascade output (where "
                         "<cell>/work/seeds/<fmt>/ exists from the cascade).")
    args = ap.parse_args()

    out_root = args.out_root
    if not out_root.is_absolute():
        out_root = (REPO_ROOT / out_root).resolve()
    if not out_root.exists():
        print(f"[recovery] out-root does not exist: {out_root}", flush=True)
        return 1

    log_path = out_root / "recovery.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)
    print(f"[recovery] out-root: {out_root}", flush=True)
    fh.write(f"[recovery] out-root: {out_root}\n")
    print(f"[recovery] targets: {[t['cell'] for t in TARGETS]}", flush=True)
    fh.write(f"[recovery] targets: {[t['cell'] for t in TARGETS]}\n")

    started = time.time()
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(recover_cell, t, out_root, fh): t for t in TARGETS}
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
