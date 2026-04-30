#!/usr/bin/env python3
"""Sequential biopython_sam recovery for biotest_4rep_cascade_sam_20260428.

Same logic as biotest_recover_biopython_sam_20260428.py but no ThreadPoolExecutor
and no LOCK — simple synchronous flow per rep. The threaded version hung
silently (write_recovery_config or subprocess.Popen race) so this strips it
back to imperative.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CELL_DIR = (
    REPO_ROOT / "compares" / "results" / "coverage"
    / "biotest_4rep_cascade_sam_20260428" / "biopython_sam"
)
WORK_DIR = CELL_DIR / "work"
TARGET_SUT = "biopython"
TARGET_FMT = "SAM"
REPS = [0, 1, 2, 3]
INNER_TIMEOUT_MIN = 70  # < outer 9000s = 150 min so atexit fires before kill
BUDGET_S = 9000


def log(msg: str, fh) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    try: print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)
    fh.write(line + "\n")
    fh.flush()


def write_config(rep: int, cfg_out: Path) -> None:
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))
    src.setdefault("phase_a", {})["enabled"] = False
    src.setdefault("phase_b", {}).setdefault("llm", {})["model"] = "deepseek-chat"
    src["phase_b"]["llm"]["temperature"] = 0.0
    src["phase_b"]["llm"]["max_retries"] = 3
    src["phase_b"]["registry_path"] = str(WORK_DIR / "data" / "mr_registry.json")

    pc = src.setdefault("phase_c", {})
    pc["format_filter"] = "SAM"
    pc["seeds_dir"] = str(WORK_DIR / "seeds")
    pc["output_dir"] = str(WORK_DIR / "bug_reports")
    pc["det_report_path"] = str(WORK_DIR / "data" / "det_report.json")
    pc["corpus_keeper"] = {"enabled": True, "max_files_per_format": 2000}

    cov = src.setdefault("coverage", {})
    cov["enabled"] = True
    cov["jacoco_report_dir"] = str(WORK_DIR / "coverage_artifacts" / "jacoco")
    cov["coveragepy_data_file"] = str(WORK_DIR / "coverage_artifacts" / ".coverage")
    cov["pysam_coverage_dir"] = str(WORK_DIR / "coverage_artifacts" / "pysam")
    cov["gcovr_report_path"] = str(WORK_DIR / "coverage_artifacts" / "gcovr.json")
    cov["noodles_report_path"] = str(WORK_DIR / "coverage_artifacts" / "noodles" / "llvm-cov.json")
    cov["noodles_profile_dir"] = str(WORK_DIR / "coverage_artifacts" / "noodles")

    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = TARGET_SUT
    fb["max_iterations"] = 1
    fb["plateau_patience"] = 2
    fb["coverage_plateau_patience"] = 2
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = INNER_TIMEOUT_MIN
    fb["state_path"] = str(WORK_DIR / "data" / "feedback_state.json")
    fb["attempts_path"] = str(WORK_DIR / "data" / "rule_attempts.json")
    fb["coverage_report_path"] = str(WORK_DIR / "data" / "coverage_report.json")
    fb["scc_report_path"] = str(WORK_DIR / "data" / "scc_report.json")
    fb.setdefault("seed_synthesis", {})["enabled"] = True
    fb["seed_synthesis"]["max_seeds_per_iteration"] = 5
    fb["seed_synthesis"]["max_file_bytes"] = 524288

    src["phase_e"] = {"enabled": False}
    src.setdefault("global", {})["seed_rng"] = 42 + rep

    cfg_out.parent.mkdir(parents=True, exist_ok=True)
    cfg_out.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")


def reset_data_cov() -> None:
    for sub in ("data", "coverage_artifacts", "bug_reports"):
        d = WORK_DIR / sub
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "jacoco").mkdir(exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "noodles").mkdir(exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "pysam").mkdir(exist_ok=True)


def run_biotest(cfg: Path, log_path: Path) -> tuple[int, float]:
    cmd = [sys.executable, str(REPO_ROOT / "biotest.py"),
           "--config", str(cfg), "--phase", "D", "--verbose"]
    started = time.time()
    with log_path.open("wb") as lf:
        proc = subprocess.Popen(
            cmd, stdout=lf, stderr=subprocess.STDOUT,
            env=os.environ.copy(), cwd=str(REPO_ROOT),
        )
        try:
            proc.wait(timeout=BUDGET_S)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try: proc.wait(timeout=120)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=15)
    elapsed = time.time() - started
    return proc.returncode if proc.returncode is not None else -1, elapsed


def measure() -> dict:
    src = WORK_DIR / "coverage_artifacts" / ".coverage"
    out = {"line_pct": 0.0, "covered": 0, "total": 0, "status": "missing"}
    if not src.exists(): return out
    dest = WORK_DIR / "coverage_artifacts" / ".coverage.json"
    if dest.exists():
        try: dest.unlink()
        except OSError: pass
    conv = subprocess.run(
        [sys.executable, "-m", "coverage", "json",
         "--data-file", str(src), "-o", str(dest)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT))
    if conv.returncode != 0 or not dest.exists():
        out["status"] = "convert_failed"
        return out
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
         "--report", str(dest), "--sut", TARGET_SUT, "--format", TARGET_FMT],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT))
    for line in proc.stdout.decode(errors="replace").splitlines():
        if "OVERALL" in line and "weighted" in line:
            try:
                tail = line.split(")", 1)[1].strip()
                frac, pct = tail.split("(")
                c, t = frac.strip().split("/")
                pct = pct.replace("%", "").replace(")", "").strip()
                out["line_pct"], out["covered"], out["total"] = float(pct), int(c), int(t)
                break
            except Exception: continue
    if out["total"] > 0:
        out["status"] = "ok"
    return out


def main():
    out_root = (REPO_ROOT / "compares" / "results" / "coverage"
                / "biotest_4rep_cascade_sam_20260428")
    log_path = out_root / "recovery_biopython_v4.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)
    log("=== biopython_sam sequential recovery start ===", fh)

    seeds_count = sum(1 for _ in (WORK_DIR / "seeds" / "sam").glob("*.sam"))
    log(f"seeds_dir has {seeds_count} files", fh)

    started_total = time.time()
    for rep in REPS:
        log(f"--- rep {rep} ---", fh)
        log("  reset data/+coverage_artifacts/+bug_reports/...", fh)
        t0 = time.time()
        reset_data_cov()
        log(f"  reset done in {time.time()-t0:.1f}s", fh)

        rep_dir = CELL_DIR / f"run_{rep}"
        cfg = rep_dir / f"biotest_config.recover_v4_rep{rep}.yaml"
        log(f"  writing config -> {cfg.name}", fh)
        write_config(rep, cfg)

        biotest_log = rep_dir / "biotest_recover_v4.log"
        log(f"  starting biotest --phase D (max_iter=1, budget={BUDGET_S}s, inner timeout={INNER_TIMEOUT_MIN}min)", fh)
        rc, elapsed = run_biotest(cfg, biotest_log)
        log(f"  exit={rc} elapsed={elapsed:.0f}s", fh)

        cov = measure()
        rec = {
            "cell": "biopython_sam", "sut": TARGET_SUT, "format": TARGET_FMT,
            "rep": rep, "exit_code": rc, "elapsed_s": round(elapsed, 1),
            "max_iterations": 1, "phases": "D",
            "rep_kind": "recovery_v4_sequential",
            "seeds_count_at_start": seeds_count,
            **cov,
        }
        (rep_dir / "measurement.json").write_text(
            json.dumps(rec, indent=2), encoding="utf-8")
        log(f"  -> line={cov['line_pct']}% covered={cov['covered']}/{cov['total']} status={cov['status']}", fh)

    log(f"=== complete in {(time.time()-started_total)/60:.1f} min ===", fh)
    fh.close()


if __name__ == "__main__":
    main()
