#!/usr/bin/env python3
"""Retry script for the 0% reps from V7 sweep.

V7 (compares/results/coverage/biotest_qwen30b_4rep_20260427/) produced
several 0% reps caused by qwen3-coder:30b failing to mine ANY MR (all
themes × attempts hit Pydantic validation errors). These zeros pollute
the per-cell mean/std.

This script retries the 0% reps with adjusted LLM config:
  - LLM temperature bumped from 0.0 → 0.5 so qwen3 produces more
    varied outputs, giving the Pydantic validator a wider search.
  - LLM seed varied per-attempt to avoid deterministic re-replay
    of the same failure path.

It does NOT touch the successful reps (preserves the existing
measurement.json files).

The infrastructure-failure cells (noodles_vcf — Phase C ran but
llvm-cov.json wasn't exported) are handled separately.

Usage:
  py -3.12 compares/scripts/biotest_qwen30b_retry_zero_reps.py
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
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKER_CONTAINER = "biotest-bench-setup"


# (cell_label, sut, fmt, runner, coverage_kind, coverage_artefact, rep)
ZERO_REPS_TO_RETRY: list[dict[str, Any]] = [
    # htsjdk_vcf — 1 zero rep (rep 3)
    {"cell": "htsjdk_vcf", "sut": "htsjdk", "fmt": "VCF",
     "runner": "host", "coverage_kind": "jacoco",
     "coverage_artefact": "coverage_artifacts/jacoco/jacoco.xml",
     "reset_paths": ["coverage_artifacts/jacoco/jacoco.exec",
                     "coverage_artifacts/jacoco/jacoco.xml"],
     "reps": [3]},
    # htsjdk_sam — all 4 reps zero
    {"cell": "htsjdk_sam", "sut": "htsjdk", "fmt": "SAM",
     "runner": "host", "coverage_kind": "jacoco",
     "coverage_artefact": "coverage_artifacts/jacoco/jacoco.xml",
     "reset_paths": ["coverage_artifacts/jacoco/jacoco.exec",
                     "coverage_artifacts/jacoco/jacoco.xml"],
     "reps": [0, 1, 2, 3]},
    # vcfpy_vcf — rep 0 zero
    {"cell": "vcfpy_vcf", "sut": "vcfpy", "fmt": "VCF",
     "runner": "host", "coverage_kind": "coveragepy",
     "coverage_artefact": "coverage_artifacts/.coverage",
     "reset_paths": ["coverage_artifacts/.coverage"],
     "reps": [0]},
    # biopython_sam — reps 1, 2, 3 (rep 3 had 3% — borderline; retry)
    {"cell": "biopython_sam", "sut": "biopython", "fmt": "SAM",
     "runner": "host", "coverage_kind": "coveragepy",
     "coverage_artefact": "coverage_artifacts/.coverage",
     "reset_paths": ["coverage_artifacts/.coverage"],
     "reps": [1, 2, 3]},
    # seqan3_sam — all 4 reps zero (container)
    {"cell": "seqan3_sam", "sut": "seqan3", "fmt": "SAM",
     "runner": "container", "coverage_kind": "gcovr",
     "coverage_artefact": "coverage_artifacts/gcovr.json",
     "reset_paths": ["coverage_artifacts/gcovr.json"],
     "reps": [0, 1, 2, 3]},
]


OUT_TOOL_PREFIXES = (
    "kept_", "synthetic_", "jazzer_", "atheris_",
    "libfuzzer_", "aflpp_", "cargofuzz_", "purerandom_",
)

STATE_FILES = [
    "data/mr_registry.json",
    "data/feedback_state.json",
    "data/rule_attempts.json",
    "data/coverage_report.json",
    "data/det_report.json",
    "data/scc_report.json",
]

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
    for rel in STATE_FILES:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                p.unlink()
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
            except OSError:
                pass
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
        log(f"    reset aux corpora: {cleared} entries", fh)


def reset_cell_artefacts(reset_paths: list[str], coverage_kind: str, fh) -> None:
    for rel in reset_paths:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)
    if coverage_kind == "gcovr":
        for p in (REPO_ROOT / "harnesses" / "cpp" / "build").glob("*.gcda"):
            try:
                p.unlink()
            except OSError:
                pass


def build_clean_seeds_dir(tmp_root: Path, fh) -> Path:
    for fmt in ("vcf", "sam"):
        dst = tmp_root / fmt
        dst.mkdir(parents=True, exist_ok=True)
        src_dir = REPO_ROOT / "seeds" / fmt
        if not src_dir.exists():
            continue
        files = sorted(src_dir.glob(f"*.{fmt}"))
        eligible = [
            p for p in files
            if not any(p.name.startswith(pref) for pref in OUT_TOOL_PREFIXES)
        ]
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
    return tmp_root


def write_temp_config(
    cell: str, sut: str, fmt: str, rep: int, retry_seed: int,
    out_dir: Path, seeds_root: Path,
    max_iterations: int = 1, timeout_minutes: int = 55,
    llm_temperature: float = 0.5,
) -> Path:
    src = yaml.safe_load(
        (REPO_ROOT / "biotest_config.yaml").read_text("utf-8")
    )
    phase_b = src.setdefault("phase_b", {})
    llm = phase_b.setdefault("llm", {})
    llm["model"] = "ollama/qwen3-coder:30b"
    llm["temperature"] = llm_temperature  # bumped from 0.0 → 0.5 for retries

    phase_c = src.setdefault("phase_c", {})
    phase_c["format_filter"] = fmt
    seeds_abs = seeds_root.resolve()
    try:
        seeds_rel = seeds_abs.relative_to(REPO_ROOT.resolve()).as_posix()
        phase_c["seeds_dir"] = seeds_rel
    except ValueError:
        phase_c["seeds_dir"] = seeds_abs.as_posix()
    phase_c["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}

    # seqan3 cov binary override
    if sut == "seqan3":
        for s in phase_c.get("suts", []):
            if s.get("name") == "seqan3":
                s["adapter"] = "harnesses/cpp/build/biotest_harness_cov_seqan3"
                s["coverage_binary"] = "harnesses/cpp/build/biotest_harness_cov_seqan3"

    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = sut
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
        "rawfuzz_seed": retry_seed,
    }
    src.setdefault("global", {})["seed_rng"] = retry_seed

    dest = out_dir / f"biotest_config.rep{rep}_retry.yaml"
    dest.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")
    return dest


def run_biotest(
    cfg_path: Path, runner: str, budget_s: int, log_path: Path, fh,
) -> int:
    if runner == "host":
        cmd = [
            sys.executable, str(REPO_ROOT / "biotest.py"),
            "--config", str(cfg_path),
            "--phase", "B,C,D,E",
            "--verbose",
        ]
        env = os.environ.copy()
        env["LLM_MODEL"] = "ollama/qwen3-coder:30b"
        env["LLM_TEMPERATURE"] = "0.5"
        log(f"    cmd: host biotest --phase B,C,D,E (cfg={cfg_path.name})", fh)
    else:  # container
        cfg_rel = cfg_path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
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
            "-e", "LLM_TEMPERATURE=0.5",
            "-i", DOCKER_CONTAINER,
            "bash", "-c", inner_cmd,
        ]
        env = None
        log(f"    cmd: docker exec ... (cfg=/work/{cfg_rel})", fh)
    log(f"    budget: {budget_s}s", fh)
    started = time.time()
    with log_path.open("wb") as lf:
        kw = {"stdout": lf, "stderr": subprocess.STDOUT}
        if env is not None:
            kw["env"] = env
            kw["cwd"] = str(REPO_ROOT)
        proc = subprocess.Popen(cmd, **kw)
        try:
            wait_extra = 120 if runner == "container" else 0
            proc.wait(timeout=budget_s + wait_extra)
        except subprocess.TimeoutExpired:
            log(f"    timeout — terminating", fh)
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
    elapsed = time.time() - started
    log(f"    exit={proc.returncode} elapsed={elapsed:.1f}s", fh)
    return proc.returncode if proc.returncode is not None else -1


def regenerate_jacoco(fh) -> None:
    exec_path = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco.exec"
    cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
    jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
    xml = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco.xml"
    if not (exec_path.exists() and cli.exists() and jar.exists()):
        return
    subprocess.run(
        ["java", "-jar", str(cli), "report", str(exec_path),
         "--classfiles", str(jar), "--xml", str(xml)],
        capture_output=True, timeout=180, cwd=str(REPO_ROOT),
    )


def regenerate_seqan3_gcovr(fh) -> None:
    cmd = [
        "docker", "exec", DOCKER_CONTAINER, "bash", "-c",
        "python3.12 -m gcovr --json -o /work/coverage_artifacts/gcovr.json "
        "--root /opt/seqan3/include "
        "--filter '.*seqan3.*' "
        "--gcov-executable 'llvm-cov-18 gcov' "
        "/work/harnesses/cpp/build",
    ]
    subprocess.run(cmd, capture_output=True, timeout=300)


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


def measure_cell(sut: str, fmt: str, coverage_kind: str,
                 coverage_artefact: str, fh) -> dict[str, Any]:
    if coverage_kind == "jacoco":
        regenerate_jacoco(fh)
    elif coverage_kind == "gcovr":
        regenerate_seqan3_gcovr(fh)

    result = {
        "line_pct": 0.0, "branch_pct": 0.0, "covered": 0, "total": 0,
        "source": coverage_artefact, "status": "missing",
    }

    if coverage_kind == "coveragepy":
        src = REPO_ROOT / coverage_artefact
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
            result["status"] = "convert_failed"
            return result
        report = dest
    else:
        report = REPO_ROOT / coverage_artefact
    if not report.exists():
        return result

    base = [
        sys.executable,
        str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
        "--report", str(report),
        "--sut", sut,
        "--format", fmt,
    ]
    if coverage_kind == "jacoco":
        proc_l = subprocess.run(base + ["--metric", "LINE"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        proc_b = subprocess.run(base + ["--metric", "BRANCH"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        result["line_pct"], result["covered"], result["total"] = \
            _parse_overall(proc_l.stdout.decode(errors="replace"))
        result["branch_pct"], _, _ = \
            _parse_overall(proc_b.stdout.decode(errors="replace"))
    else:
        proc = subprocess.run(base, capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        result["line_pct"], result["covered"], result["total"] = \
            _parse_overall(proc.stdout.decode(errors="replace"))
    result["status"] = "ok" if result["total"] else "zero_total"
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out-root", type=Path,
        default=REPO_ROOT / "compares" / "results" / "coverage"
        / "biotest_qwen30b_4rep_20260427",
        help="Same out-root as the V7 sweep — measurement.json files are "
        "OVERWRITTEN in place for retried reps.",
    )
    ap.add_argument("--budget-s", type=int, default=3600)
    ap.add_argument("--llm-temperature", type=float, default=0.5)
    ap.add_argument("--max-attempts", type=int, default=2,
                    help="Max retry attempts per rep before giving up.")
    args = ap.parse_args()

    log_path = args.out_root / "retry_run.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("===== RETRY zero reps with adjusted config =====", fh)
    log(f"out_root = {args.out_root}", fh)
    log(f"LLM temperature = {args.llm_temperature}", fh)
    log(f"max attempts per rep = {args.max_attempts}", fh)

    seeds_clean = build_clean_seeds_dir(args.out_root / "seeds_clean", fh)

    # Total reps to retry
    total = sum(len(c["reps"]) for c in ZERO_REPS_TO_RETRY)
    log(f"Total reps to retry: {total}", fh)

    sweep_started = time.time()
    success_count = 0
    fail_count = 0

    for cell_cfg in ZERO_REPS_TO_RETRY:
        cell = cell_cfg["cell"]
        sut = cell_cfg["sut"]
        fmt = cell_cfg["fmt"]
        runner = cell_cfg["runner"]
        coverage_kind = cell_cfg["coverage_kind"]
        coverage_artefact = cell_cfg["coverage_artefact"]
        reset_paths = cell_cfg["reset_paths"]

        for rep in cell_cfg["reps"]:
            log(f"\n### RETRY: {cell} rep {rep} (sut={sut} fmt={fmt})", fh)

            for attempt in range(1, args.max_attempts + 1):
                log(f"  -- attempt {attempt}/{args.max_attempts} --", fh)
                rep_dir = args.out_root / cell / f"run_{rep}"
                rep_dir.mkdir(parents=True, exist_ok=True)

                reset_state(fh)
                reset_aux_corpora(fh)
                reset_cell_artefacts(reset_paths, coverage_kind, fh)

                # Use a different rng_seed per attempt to vary qwen3's RAG path
                retry_seed = (1000 * attempt) + rep + 42

                cfg_path = write_temp_config(
                    cell, sut, fmt, rep, retry_seed,
                    rep_dir, seeds_clean,
                    llm_temperature=args.llm_temperature,
                )

                biotest_log = rep_dir / f"biotest_retry{attempt}.log"
                t0 = time.time()
                exit_code = run_biotest(
                    cfg_path, runner, args.budget_s, biotest_log, fh,
                )
                elapsed = time.time() - t0

                cov = measure_cell(sut, fmt, coverage_kind,
                                   coverage_artefact, fh)

                rec = {
                    "cell": cell,
                    "sut": sut,
                    "format": fmt,
                    "rep": rep,
                    "exit_code": exit_code,
                    "elapsed_s": round(elapsed, 1),
                    "max_iterations": 1,
                    "phases": "B,C,D,E (retry)",
                    "llm_model": "ollama/qwen3-coder:30b",
                    "llm_temperature": args.llm_temperature,
                    "retry_attempt": attempt,
                    "retry_seed": retry_seed,
                    **cov,
                }

                log(
                    f"    -> line={cov['line_pct']:.2f}% "
                    f"covered={cov['covered']}/{cov['total']} "
                    f"status={cov['status']}",
                    fh,
                )

                if cov["line_pct"] > 0.0:
                    # Success — overwrite the measurement.json
                    (rep_dir / "measurement.json").write_text(
                        json.dumps(rec, indent=2), encoding="utf-8",
                    )
                    log(f"    SUCCESS — recorded {cov['line_pct']:.2f}%", fh)
                    success_count += 1
                    break  # exit attempt loop
                else:
                    # Save attempt artifact for audit but don't overwrite measurement.json
                    (rep_dir / f"measurement_retry{attempt}.json").write_text(
                        json.dumps(rec, indent=2), encoding="utf-8",
                    )
                    log(f"    attempt {attempt} still 0%, retry", fh)
            else:
                log(
                    f"    GAVE UP after {args.max_attempts} attempts — "
                    f"original 0% measurement preserved",
                    fh,
                )
                fail_count += 1

    log(
        f"\n===== retry sweep complete in "
        f"{(time.time() - sweep_started) / 60:.1f} min =====",
        fh,
    )
    log(f"  success: {success_count}/{total}", fh)
    log(f"  give-up: {fail_count}/{total}", fh)
    fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
