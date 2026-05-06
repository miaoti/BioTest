#!/usr/bin/env python3
"""biopython_sam recovery v6 — curated-only seed corpus.

v5 (217 seeds) still hit outer kill because biotest's Phase B inside Phase D
mines additional MRs each iter, and timeout_minutes only fires at iter
boundaries (which never fires with max_iter=1). v5 ran 9000s = exactly the
outer budget = SIGKILL before coverage.py atexit.

v6 reverts to JUST the 67 curated/external/synthetic seeds — the same shape
that the original cascade rep 0 used and finished in 5193s (87 min) with
status=ok. Per-rep RNG variation comes from `seed_rng = 42 + rep` only;
seeds are byte-identical across reps. We accept lower std (corpus-driven
variance is gone) in exchange for reliable status=ok measurements.
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
    REPO_ROOT / "compares" / "results" / "coverage"
    / "biotest_4rep_cascade_sam_20260429" / "htsjdk_sam"
)
WORK_DIR = CELL_DIR / "work"
SEEDS_DIR = WORK_DIR / "seeds" / "sam"
SEEDS_BACKUP = WORK_DIR / "seeds" / "sam_full_backup"
TARGET_KEPT = 0  # curated/external/synthetic only — no kept_* (BioTest-generated)
TARGET_SUT = "htsjdk"
TARGET_FMT = "SAM"
REPS = [1]  # only rep 1 needs recovery — rep 0/2/3 succeeded in the cascade
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

    # Per-SUT JaCoCo override — without this biotest's htsjdk runner writes
    # jacoco.exec to the GLOBAL coverage_artifacts/jacoco/ (the path baked
    # into biotest_config.yaml), NOT to the per-cell work_dir. The cascade
    # orchestrator (compares/scripts/biotest_4rep_cascade_parallel.py:243-255)
    # patches `coverage_jvm_args` and `coverage_exec_dir` per htsjdk SUT
    # entry to redirect the JaCoCo agent's destfile to the per-cell path.
    # Recovery script must do the same or measure() finds an empty dir.
    work_jacoco_dir = WORK_DIR / "coverage_artifacts" / "jacoco"
    work_jacoco_exec = work_jacoco_dir / "jacoco.exec"
    agent = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacocoagent.jar"
    for sut_cfg in pc.get("suts", []):
        if sut_cfg.get("name") == "htsjdk":
            sut_cfg["coverage_exec_dir"] = str(work_jacoco_dir)
            sut_cfg["coverage_jvm_args"] = (
                f"-javaagent:{agent}=destfile={work_jacoco_exec},append=true"
            )

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
    fb["max_iterations"] = 2  # match cascade rep 0 (succeeded in 5193s)
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


def backup_full_seeds(fh) -> list[str]:
    """One-time snapshot of the full SAM seed corpus so it can be restored."""
    if not SEEDS_BACKUP.exists():
        log(f"snapshotting full seeds -> {SEEDS_BACKUP}", fh)
        SEEDS_BACKUP.mkdir(parents=True)
        for f in SEEDS_DIR.glob("*.sam"):
            shutil.copy2(f, SEEDS_BACKUP / f.name)
    full = sorted(p.name for p in SEEDS_BACKUP.glob("*.sam"))
    log(f"full corpus has {len(full)} files (backup)", fh)
    return full


def stage_subsample(full_names: list[str], rep: int, fh) -> int:
    """Wipe SEEDS_DIR; stage all non-kept + a per-rep sample of kept_*."""
    for f in SEEDS_DIR.glob("*.sam"):
        f.unlink()
    SEEDS_DIR.mkdir(parents=True, exist_ok=True)

    non_kept = [n for n in full_names if not n.startswith("kept_")]
    kept = [n for n in full_names if n.startswith("kept_")]

    rng = random.Random(42 + rep)
    sample = rng.sample(kept, min(TARGET_KEPT, len(kept)))
    selected = non_kept + sample

    for name in selected:
        try: shutil.copy2(SEEDS_BACKUP / name, SEEDS_DIR / name)
        except Exception as e: log(f"copy fail {name}: {e}", fh)
    log(
        f"  rep {rep}: staged {len(non_kept)} non-kept + {len(sample)} kept "
        f"= {len(selected)} seeds",
        fh,
    )
    return len(selected)


def restore_full_seeds(full_names: list[str], fh) -> None:
    log("restoring full seed corpus from backup", fh)
    for f in SEEDS_DIR.glob("*.sam"):
        f.unlink()
    for name in full_names:
        shutil.copy2(SEEDS_BACKUP / name, SEEDS_DIR / name)
    log(f"restored {len(full_names)} seeds to {SEEDS_DIR}", fh)


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
    """JaCoCo measurement for htsjdk: jacoco.exec → jacoco.xml → measure_coverage."""
    out = {"line_pct": 0.0, "covered": 0, "total": 0, "status": "missing"}
    exec_path = WORK_DIR / "coverage_artifacts" / "jacoco" / "jacoco.exec"
    if not exec_path.exists():
        return out
    cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
    jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
    xml = WORK_DIR / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    if not (cli.exists() and jar.exists()):
        out["status"] = "missing_tools"
        return out
    proc = subprocess.run(
        ["java", "-jar", str(cli), "report", str(exec_path),
         "--classfiles", str(jar), "--xml", str(xml)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT))
    if proc.returncode != 0:
        out["status"] = "jacoco_regen_failed"
        return out
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
         "--report", str(xml), "--sut", TARGET_SUT, "--format", TARGET_FMT],
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
                / "biotest_4rep_cascade_sam_20260429")
    log_path = out_root / "recovery_htsjdk_rep1.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)
    log("=== htsjdk_sam rep 1 recovery (max_iter=2 curated-only) start ===", fh)

    full_names = backup_full_seeds(fh)
    started_total = time.time()
    try:
        for rep in REPS:
            log(f"--- rep {rep} ---", fh)
            log("  reset data/+coverage_artifacts/+bug_reports/...", fh)
            t0 = time.time()
            reset_data_cov()
            log(f"  reset done in {time.time()-t0:.1f}s", fh)
            staged = stage_subsample(full_names, rep, fh)

            rep_dir = CELL_DIR / f"run_{rep}"
            cfg = rep_dir / f"biotest_config.recover_htsjdk_rep1_rep{rep}.yaml"
            log(f"  writing config -> {cfg.name}", fh)
            write_config(rep, cfg)

            biotest_log = rep_dir / "biotest_recover_htsjdk_rep1.log"
            log(f"  starting biotest --phase D (max_iter=2, budget={BUDGET_S}s, inner timeout={INNER_TIMEOUT_MIN}min)", fh)
            rc, elapsed = run_biotest(cfg, biotest_log)
            log(f"  exit={rc} elapsed={elapsed:.0f}s", fh)

            cov = measure()
            rec = {
                "cell": "htsjdk_sam", "sut": TARGET_SUT, "format": TARGET_FMT,
                "rep": rep, "exit_code": rc, "elapsed_s": round(elapsed, 1),
                "max_iterations": 2, "phases": "D",
                "rep_kind": "recovery_htsjdk_rep1_max_iter_2",
                "seeds_count_at_start": staged,
                **cov,
            }
            (rep_dir / "measurement.json").write_text(
                json.dumps(rec, indent=2), encoding="utf-8")
            log(f"  -> line={cov['line_pct']}% covered={cov['covered']}/{cov['total']} status={cov['status']}", fh)
    finally:
        restore_full_seeds(full_names, fh)
        log(f"=== complete in {(time.time()-started_total)/60:.1f} min ===", fh)
        fh.close()


if __name__ == "__main__":
    main()
