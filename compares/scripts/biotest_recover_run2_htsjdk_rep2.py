#!/usr/bin/env python3
"""One-off recovery: run2 htsjdk_vcf rep 2.

Why this exists: during run 2's cascade, the JaCoCo XML regeneration step
hit a Windows file lock (concurrent jacococli reads of the shared
biotest-harness-all.jar across run2/run3/run4 stamping into each other).
rep 3's .exec is intact (recovered separately), but rep 2's .exec was
already wiped by rep 3's reset. So we re-run rep 2 with max_iter=1
against the current cascaded corpus — same recovery shape as vcfpy.
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
CELL_DIR = REPO_ROOT / "compares" / "results" / "coverage" / "biotest_4rep_cascade_run2_20260429" / "htsjdk_vcf"
WORK_DIR = CELL_DIR / "work"
REP = 2
SUT = "htsjdk"
FMT = "VCF"
BUDGET_S = 4500


def write_config(rep: int, cfg_out: Path) -> Path:
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))

    src.setdefault("phase_a", {})["enabled"] = False
    src.setdefault("phase_b", {}).setdefault("llm", {})["model"] = "deepseek-chat"
    src["phase_b"]["llm"]["temperature"] = 0.0
    src["phase_b"]["llm"]["max_retries"] = 3
    src["phase_b"]["registry_path"] = str(WORK_DIR / "data" / "mr_registry.json")

    pc = src.setdefault("phase_c", {})
    pc["format_filter"] = FMT
    pc["seeds_dir"] = str(WORK_DIR / "seeds")
    pc["output_dir"] = str(WORK_DIR / "bug_reports")
    pc["det_report_path"] = str(WORK_DIR / "data" / "det_report.json")
    pc["corpus_keeper"] = {"enabled": True, "max_files_per_format": 2000}

    for sut_cfg in pc.get("suts", []):
        if sut_cfg.get("name") == "htsjdk":
            sut_cfg["coverage_exec_dir"] = str(WORK_DIR / "coverage_artifacts" / "jacoco")
            destfile = str(WORK_DIR / "coverage_artifacts" / "jacoco" / "jacoco.exec")
            agent = str(REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacocoagent.jar")
            sut_cfg["coverage_jvm_args"] = f"-javaagent:{agent}=destfile={destfile},append=true"

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
    fb["primary_target"] = SUT
    fb["max_iterations"] = 1
    fb["plateau_patience"] = 2
    fb["coverage_plateau_patience"] = 2
    fb["min_coverage_delta_pp"] = 0.0
    fb["timeout_minutes"] = 70
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
    return cfg_out


def reset_data_and_cov() -> None:
    for sub in ("data", "coverage_artifacts", "bug_reports"):
        d = WORK_DIR / sub
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "jacoco").mkdir(exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "noodles").mkdir(exist_ok=True)
    (WORK_DIR / "coverage_artifacts" / "pysam").mkdir(exist_ok=True)


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


def regenerate_jacoco_xml() -> bool:
    exec_path = WORK_DIR / "coverage_artifacts" / "jacoco" / "jacoco.exec"
    if not exec_path.exists():
        return False
    cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
    jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
    xml = WORK_DIR / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    proc = subprocess.run(
        ["java", "-jar", str(cli), "report", str(exec_path),
         "--classfiles", str(jar), "--xml", str(xml)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT),
    )
    return proc.returncode == 0 and xml.exists()


def measure_jacoco() -> dict:
    out = {"line_pct": 0.0, "branch_pct": 0.0, "covered": 0, "total": 0, "status": "missing"}
    xml = WORK_DIR / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    if not xml.exists():
        return out
    base = [sys.executable, str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
            "--report", str(xml), "--sut", SUT, "--format", FMT]
    p_l = subprocess.run(base + ["--metric", "LINE"], capture_output=True, timeout=120, cwd=str(REPO_ROOT))
    p_b = subprocess.run(base + ["--metric", "BRANCH"], capture_output=True, timeout=120, cwd=str(REPO_ROOT))

    def parse(stdout: str) -> tuple[float, int, int]:
        for line in stdout.splitlines():
            if "OVERALL" in line and "weighted" in line:
                try:
                    tail = line.split(")", 1)[1].strip()
                    frac, pct = tail.split("(")
                    c, t = frac.strip().split("/")
                    pct = pct.replace("%", "").replace(")", "").strip()
                    return float(pct), int(c), int(t)
                except Exception:
                    continue
        return 0.0, 0, 0

    out["line_pct"], out["covered"], out["total"] = parse(p_l.stdout.decode(errors="replace"))
    out["branch_pct"], _, _ = parse(p_b.stdout.decode(errors="replace"))
    if out["total"] > 0:
        out["status"] = "ok"
    return out


def main() -> int:
    rep_dir = CELL_DIR / f"run_{REP}"
    rep_dir.mkdir(parents=True, exist_ok=True)

    print(f"[recovery] resetting data + coverage_artifacts (preserving seeds)...")
    reset_data_and_cov()

    cfg = rep_dir / f"biotest_config.recover_rep{REP}.yaml"
    write_config(REP, cfg)

    log = rep_dir / "biotest_recover.log"
    print(f"[recovery] running biotest --phase D max_iter=1 (budget {BUDGET_S}s)...")
    rc, elapsed = run_biotest(cfg, log)
    print(f"[recovery] biotest exit={rc} elapsed={elapsed:.0f}s")

    print(f"[recovery] regenerating JaCoCo XML...")
    if not regenerate_jacoco_xml():
        print("[recovery] WARN: jacoco regen failed")

    cov = measure_jacoco()
    print(f"[recovery] coverage: line={cov['line_pct']}% covered={cov['covered']}/{cov['total']} status={cov['status']}")

    rec = {
        "cell": "htsjdk_vcf", "sut": SUT, "format": FMT,
        "rep": REP, "exit_code": rc, "elapsed_s": round(elapsed, 1),
        "max_iterations": 1, "phases": "D",
        "rep_kind": "recovery_max_iter_1",
        **cov,
    }
    (rep_dir / "measurement.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    print(f"[recovery] wrote {rep_dir / 'measurement.json'}")
    return 0 if cov["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
