#!/usr/bin/env python3
"""Targeted recovery for vcfpy_vcf reps 1/2/3.

Why a second recovery script:
  - The original recovery (biotest_recover_failed_reps.py) reused the full
    1442-seed cascaded corpus and a 4500s outer budget. Profiling rep 1's
    log showed Phase D iter 1 needs >75 min just to cross-execute every
    seed across htsjdk/pysam/vcfpy/noodles/reference. The outer kill
    fired before coverage.py atexit could flush, so we got fake zeros.

Fixes:
  - Subsample the seeds dir to a bounded but representative set:
    * ALL non-kept seeds (curated/external/synthetic) — these are the
      high-coverage shapes
    * A deterministic sample of N kept_* seeds (BioTest-generated cascade
      seeds), seeded by rep so each rep sees a different sample (gives
      meaningful std)
  - Outer budget = 9000s (150 min); biotest internal timeout_minutes=120.
    Outer > inner so coverage.py atexit fires before the kill.
  - Sequential reps (no parallelism — only one cell to recover).

Strategy preserves the spirit of the cascade: rep N still sees the
full curated/external corpus + the synthetics + a slice of the
1404 kept_* mutations. Bounded count keeps wall time reasonable.
"""
from __future__ import annotations

import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CELL_DIR = (
    REPO_ROOT
    / "compares" / "results" / "coverage"
    / "biotest_4rep_cascade_20260427" / "vcfpy_vcf"
)
WORK_DIR = CELL_DIR / "work"
SEEDS_DIR = WORK_DIR / "seeds" / "vcf"
SEEDS_BACKUP = WORK_DIR / "seeds" / "vcf_full_backup"
TARGET_KEPT = 250  # subsample this many kept_* per rep
REPS = [1, 2, 3]
BUDGET_S = 9000  # 150 min outer
INNER_TIMEOUT_MIN = 120  # biotest's own feedback timeout — fires before outer kill


def log(msg: str, fh) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)
    fh.write(line + "\n")
    fh.flush()


def backup_full_seeds(fh) -> list[str]:
    """One-time: snapshot the full vcfpy seeds corpus so we can restore later."""
    if not SEEDS_BACKUP.exists():
        log(f"snapshotting full seeds -> {SEEDS_BACKUP}", fh)
        SEEDS_BACKUP.mkdir(parents=True)
        for f in SEEDS_DIR.glob("*.vcf"):
            shutil.copy2(f, SEEDS_BACKUP / f.name)
    full = sorted(p.name for p in SEEDS_BACKUP.glob("*.vcf"))
    log(f"full corpus has {len(full)} files (backup)", fh)
    return full


def stage_subsample(full_names: list[str], rep: int, fh) -> int:
    """Wipe SEEDS_DIR and stage curated+synthetic + per-rep sample of kept_*."""
    for f in SEEDS_DIR.glob("*.vcf"):
        f.unlink()
    SEEDS_DIR.mkdir(parents=True, exist_ok=True)

    non_kept = [n for n in full_names if not n.startswith("kept_")]
    kept = [n for n in full_names if n.startswith("kept_")]

    rng = random.Random(42 + rep)
    sample = rng.sample(kept, min(TARGET_KEPT, len(kept)))
    selected = non_kept + sample

    for name in selected:
        src = SEEDS_BACKUP / name
        dst = SEEDS_DIR / name
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            log(f"copy fail {name}: {e}", fh)
    log(
        f"rep {rep}: staged {len(non_kept)} non-kept + {len(sample)} kept = "
        f"{len(selected)} seeds",
        fh,
    )
    return len(selected)


def write_config(rep: int, cfg_out: Path) -> None:
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))

    src.setdefault("phase_a", {})["enabled"] = False
    src.setdefault("phase_b", {}).setdefault("llm", {})["model"] = "deepseek-chat"
    src["phase_b"]["llm"]["temperature"] = 0.0
    src["phase_b"]["llm"]["max_retries"] = 3
    src["phase_b"]["registry_path"] = str(WORK_DIR / "data" / "mr_registry.json")

    pc = src.setdefault("phase_c", {})
    pc["format_filter"] = "VCF"
    pc["seeds_dir"] = str(WORK_DIR / "seeds")
    pc["output_dir"] = str(WORK_DIR / "bug_reports")
    pc["det_report_path"] = str(WORK_DIR / "data" / "det_report.json")
    pc["corpus_keeper"] = {"enabled": True, "max_files_per_format": 600}

    cov = src.setdefault("coverage", {})
    cov["enabled"] = True
    cov["jacoco_report_dir"] = str(WORK_DIR / "coverage_artifacts" / "jacoco")
    cov["coveragepy_data_file"] = str(WORK_DIR / "coverage_artifacts" / ".coverage")
    cov["pysam_coverage_dir"] = str(WORK_DIR / "coverage_artifacts" / "pysam")
    cov["gcovr_report_path"] = str(WORK_DIR / "coverage_artifacts" / "gcovr.json")
    cov["noodles_report_path"] = str(
        WORK_DIR / "coverage_artifacts" / "noodles" / "llvm-cov.json"
    )
    cov["noodles_profile_dir"] = str(WORK_DIR / "coverage_artifacts" / "noodles")

    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = "vcfpy"
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


def reset_data_and_cov() -> None:
    for sub in ("data", "coverage_artifacts", "bug_reports"):
        d = WORK_DIR / sub
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "jacoco").mkdir(exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "noodles").mkdir(exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "pysam").mkdir(exist_ok=True)


def run_biotest(cfg: Path, log_path: Path) -> tuple[int, float]:
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg), "--phase", "D", "--verbose",
    ]
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
            try:
                proc.wait(timeout=120)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=15)
    elapsed = time.time() - started
    return (proc.returncode if proc.returncode is not None else -1, elapsed)


def measure() -> dict:
    src = WORK_DIR / "coverage_artifacts" / ".coverage"
    out = {"line_pct": 0.0, "covered": 0, "total": 0, "status": "missing"}
    if not src.exists():
        return out
    dest = WORK_DIR / "coverage_artifacts" / ".coverage.json"
    if dest.exists():
        try: dest.unlink()
        except OSError: pass
    conv = subprocess.run(
        [sys.executable, "-m", "coverage", "json",
         "--data-file", str(src), "-o", str(dest)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT),
    )
    if conv.returncode != 0 or not dest.exists():
        out["status"] = "convert_failed"
        return out
    proc = subprocess.run(
        [sys.executable,
         str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
         "--report", str(dest), "--sut", "vcfpy", "--format", "VCF"],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT),
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


def restore_full_seeds(full_names: list[str], fh) -> None:
    log("restoring full seed corpus from backup", fh)
    for f in SEEDS_DIR.glob("*.vcf"):
        f.unlink()
    for name in full_names:
        shutil.copy2(SEEDS_BACKUP / name, SEEDS_DIR / name)
    log(f"restored {len(full_names)} seeds to {SEEDS_DIR}", fh)


def main():
    out_root = (
        REPO_ROOT / "compares" / "results" / "coverage" / "biotest_4rep_cascade_20260427"
    )
    log_path = out_root / "recovery_vcfpy.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("=== vcfpy-only recovery start ===", fh)
    full_names = backup_full_seeds(fh)

    started = time.time()
    try:
        for rep in REPS:
            log(f"--- rep {rep} ---", fh)
            reset_data_and_cov()
            staged = stage_subsample(full_names, rep, fh)

            rep_dir = CELL_DIR / f"run_{rep}"
            cfg = rep_dir / f"biotest_config.recover_v2_rep{rep}.yaml"
            write_config(rep, cfg)

            biotest_log = rep_dir / "biotest_recover_v2.log"
            log(f"  cmd: biotest --phase D (max_iter=1, budget={BUDGET_S}s)", fh)
            rc, elapsed = run_biotest(cfg, biotest_log)
            log(f"  exit={rc} elapsed={elapsed:.0f}s", fh)

            cov = measure()
            rec = {
                "cell": "vcfpy_vcf", "sut": "vcfpy", "format": "VCF",
                "rep": rep, "exit_code": rc, "elapsed_s": round(elapsed, 1),
                "max_iterations": 1, "phases": "D",
                "rep_kind": "recovery_v2_subsampled",
                "seeds_count_at_start": staged,
                **cov,
            }
            (rep_dir / "measurement.json").write_text(
                json.dumps(rec, indent=2), encoding="utf-8",
            )
            log(
                f"  -> line={cov['line_pct']}% covered={cov['covered']}/"
                f"{cov['total']} status={cov['status']}",
                fh,
            )
    finally:
        restore_full_seeds(full_names, fh)
        elapsed_min = (time.time() - started) / 60
        log(f"=== vcfpy-only recovery complete in {elapsed_min:.1f} min ===", fh)
        fh.close()


if __name__ == "__main__":
    main()
