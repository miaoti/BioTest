#!/usr/bin/env python3
"""Parameterized subsampled recovery for vcfpy_vcf reps that hit Windows
TerminateProcess at the wall cap.

Why this exists: full cascaded corpus (~700-900 seeds) × 11 enforced MRs ×
5 SUTs exceeds the 4500s outer budget for a single max_iter=1 Phase D
iteration. coverage.py's atexit doesn't fire on Windows TerminateProcess,
so any biotest hitting outer budget produces status=missing.

Mirror of run 1's v2 recovery: subsample to a deterministic ~292-seed
corpus (all non-kept curated/external/synthetic + N kept_* per rep, RNG
seeded by rep) and use a 9000s outer budget aligned with timeout_minutes=120
so the biotest internal graceful exit fires before the outer SIGKILL.

The full corpus is preserved as <work>/seeds/vcf_full_backup/; the
subsampled corpus replaces <work>/seeds/vcf/ for the duration of recovery,
then is restored from the backup.

Usage:
    py -3.12 compares/scripts/biotest_recover_vcfpy_subsampled_param.py \\
        --out-root compares/results/coverage/biotest_4rep_cascade_run2_20260429
"""
from __future__ import annotations

import argparse
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
TARGET_KEPT = 250  # back to run-1 v2's 292-seed shape; with heavy SUTs disabled, work fits in budget
BUDGET_S = 4500
INNER_TIMEOUT_MIN = 70


def log(msg: str, fh) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)
    fh.write(line + "\n")
    fh.flush()


def backup_full_seeds(work_dir: Path, fh) -> list[str]:
    seeds_dir = work_dir / "seeds" / "vcf"
    backup = work_dir / "seeds" / "vcf_full_backup"
    if not backup.exists():
        log(f"snapshotting full seeds -> {backup}", fh)
        backup.mkdir(parents=True)
        for f in seeds_dir.glob("*.vcf"):
            shutil.copy2(f, backup / f.name)
    full = sorted(p.name for p in backup.glob("*.vcf"))
    log(f"full corpus has {len(full)} files", fh)
    return full


def stage_subsample(work_dir: Path, full: list[str], rep: int, fh) -> int:
    seeds_dir = work_dir / "seeds" / "vcf"
    backup = work_dir / "seeds" / "vcf_full_backup"
    for f in seeds_dir.glob("*.vcf"):
        f.unlink()
    seeds_dir.mkdir(parents=True, exist_ok=True)

    non_kept = [n for n in full if not n.startswith("kept_")]
    kept = [n for n in full if n.startswith("kept_")]

    rng = random.Random(42 + rep)
    sample = rng.sample(kept, min(TARGET_KEPT, len(kept)))
    selected = non_kept + sample
    for name in selected:
        try:
            shutil.copy2(backup / name, seeds_dir / name)
        except Exception as e:
            log(f"copy fail {name}: {e}", fh)
    log(f"rep {rep}: staged {len(non_kept)} non-kept + {len(sample)} kept = {len(selected)} seeds", fh)
    return len(selected)


def restore_full_seeds(work_dir: Path, fh) -> None:
    seeds_dir = work_dir / "seeds" / "vcf"
    backup = work_dir / "seeds" / "vcf_full_backup"
    if not backup.exists():
        return
    log(f"restoring full corpus from {backup}", fh)
    for f in seeds_dir.glob("*.vcf"):
        f.unlink()
    for src in backup.glob("*.vcf"):
        shutil.copy2(src, seeds_dir / src.name)


def write_config(work_dir: Path, rep: int, cfg_out: Path) -> Path:
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))
    src.setdefault("phase_a", {})["enabled"] = False
    src.setdefault("phase_b", {}).setdefault("llm", {})["model"] = "deepseek-chat"
    src["phase_b"]["llm"]["temperature"] = 0.0
    src["phase_b"]["llm"]["max_retries"] = 3
    src["phase_b"]["registry_path"] = str(work_dir / "data" / "mr_registry.json")

    pc = src.setdefault("phase_c", {})
    pc["format_filter"] = "VCF"
    pc["seeds_dir"] = str(work_dir / "seeds")
    pc["output_dir"] = str(work_dir / "bug_reports")
    pc["det_report_path"] = str(work_dir / "data" / "det_report.json")
    pc["corpus_keeper"] = {"enabled": False}  # subsampled run — don't grow corpus

    # Disable heavy SUTs we're not measuring — keep only vcfpy (the
    # primary), the reference Python parser, and htslib (gold-standard
    # tie-breaker for the metamorphic oracle). Disabling the JVM
    # (htsjdk), Rust (noodles), and Docker (pysam) SUTs cuts ~70 % of
    # Phase C wall time without changing the vcfpy coverage we measure.
    keep = {"vcfpy", "htslib", "reference"}
    for sut_cfg in pc.get("suts", []):
        if sut_cfg.get("name") not in keep:
            sut_cfg["enabled"] = False

    cov = src.setdefault("coverage", {})
    cov["enabled"] = True
    cov["jacoco_report_dir"] = str(work_dir / "coverage_artifacts" / "jacoco")
    cov["coveragepy_data_file"] = str(work_dir / "coverage_artifacts" / ".coverage")
    cov["pysam_coverage_dir"] = str(work_dir / "coverage_artifacts" / "pysam")
    cov["gcovr_report_path"] = str(work_dir / "coverage_artifacts" / "gcovr.json")
    cov["noodles_report_path"] = str(work_dir / "coverage_artifacts" / "noodles" / "llvm-cov.json")
    cov["noodles_profile_dir"] = str(work_dir / "coverage_artifacts" / "noodles")

    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = "vcfpy"
    fb["max_iterations"] = 1
    fb["plateau_patience"] = 2
    fb["coverage_plateau_patience"] = 2
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = INNER_TIMEOUT_MIN
    fb["state_path"] = str(work_dir / "data" / "feedback_state.json")
    fb["attempts_path"] = str(work_dir / "data" / "rule_attempts.json")
    fb["coverage_report_path"] = str(work_dir / "data" / "coverage_report.json")
    fb["scc_report_path"] = str(work_dir / "data" / "scc_report.json")
    fb.setdefault("seed_synthesis", {})["enabled"] = False  # don't grow

    src["phase_e"] = {"enabled": False}
    src.setdefault("global", {})["seed_rng"] = 42 + rep

    cfg_out.parent.mkdir(parents=True, exist_ok=True)
    cfg_out.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")
    return cfg_out


def reset_data_and_cov(work_dir: Path) -> None:
    for sub in ("data", "coverage_artifacts", "bug_reports"):
        d = work_dir / sub
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
    (work_dir / "coverage_artifacts" / "jacoco").mkdir(exist_ok=True)
    (work_dir / "coverage_artifacts" / "noodles").mkdir(exist_ok=True)
    (work_dir / "coverage_artifacts" / "pysam").mkdir(exist_ok=True)


def run_biotest(cfg_path: Path, log_path: Path) -> tuple[int, float]:
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
            proc.wait(timeout=BUDGET_S)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=15)
    elapsed = time.time() - started
    return (proc.returncode if proc.returncode is not None else -1, elapsed)


def measure_coveragepy(work_dir: Path) -> dict:
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
        [sys.executable, str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
         "--report", str(dest), "--sut", "vcfpy", "--format", "VCF"],
        capture_output=True, timeout=120, cwd=str(REPO_ROOT),
    )
    for line in proc.stdout.decode(errors="replace").splitlines():
        if "OVERALL" in line and "weighted" in line:
            try:
                tail = line.split(")", 1)[1].strip()
                frac, pct = tail.split("(")
                c, t = frac.strip().split("/")
                pct = pct.replace("%", "").replace(")", "").strip()
                out["line_pct"], out["covered"], out["total"] = float(pct), int(c), int(t)
                break
            except Exception:
                continue
    if out["total"] > 0:
        out["status"] = "ok"
    return out


def find_failed_reps(cell_dir: Path) -> list[int]:
    failed = []
    for rep in range(4):
        m = cell_dir / f"run_{rep}" / "measurement.json"
        if not m.exists():
            failed.append(rep)
            continue
        try:
            d = json.loads(m.read_text(encoding="utf-8"))
            if d.get("status") != "ok":
                failed.append(rep)
        except Exception:
            failed.append(rep)
    return failed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", type=Path, required=True)
    args = ap.parse_args()

    out_root = args.out_root
    if not out_root.is_absolute():
        out_root = (REPO_ROOT / out_root).resolve()
    if not out_root.exists():
        print(f"out-root does not exist: {out_root}", flush=True)
        return 1

    cell_dir = out_root / "vcfpy_vcf"
    work_dir = cell_dir / "work"
    if not work_dir.exists():
        print(f"vcfpy_vcf work dir missing: {work_dir}", flush=True)
        return 1

    log_path = out_root / "recovery_subsampled.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)
    log(f"out-root: {out_root}", fh)

    failed = find_failed_reps(cell_dir)
    if not failed:
        log("no failed reps — exiting", fh)
        fh.close()
        return 0

    log(f"failed reps: {failed}", fh)
    full = backup_full_seeds(work_dir, fh)

    for rep in failed:
        log(f"--- recovering rep {rep} (subsampled) ---", fh)
        stage_subsample(work_dir, full, rep, fh)
        reset_data_and_cov(work_dir)

        rep_dir = cell_dir / f"run_{rep}"
        cfg = rep_dir / f"biotest_config.recover_subsampled_rep{rep}.yaml"
        write_config(work_dir, rep, cfg)

        biolog = rep_dir / "biotest_recover_subsampled.log"
        log(f"  biotest --phase D max_iter=1 budget={BUDGET_S}s inner_timeout={INNER_TIMEOUT_MIN}min", fh)
        rc, elapsed = run_biotest(cfg, biolog)
        log(f"  exit={rc} elapsed={elapsed:.0f}s", fh)

        cov = measure_coveragepy(work_dir)
        rec = {
            "cell": "vcfpy_vcf", "sut": "vcfpy", "format": "VCF",
            "rep": rep, "exit_code": rc, "elapsed_s": round(elapsed, 1),
            "max_iterations": 1, "phases": "D",
            "rep_kind": "recovery_v2_subsampled",
            "seeds_count_at_start": TARGET_KEPT + len([n for n in full if not n.startswith("kept_")]),
            **cov,
        }
        (rep_dir / "measurement.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
        log(f"  -> line={cov['line_pct']}% status={cov['status']}", fh)

    log("restoring full corpus...", fh)
    restore_full_seeds(work_dir, fh)
    log("=== subsampled recovery complete ===", fh)
    fh.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
