#!/usr/bin/env python3
"""4-rep coverage sweep where reps 2..4 are pinned to Run 1's state.

Unlike `biotest_4rep_fullD_runner.py` (each rep starts from empty
mr_registry/feedback_state, so std measures whole-pipeline variance
including Phase B's LLM-mining drift), this orchestrator runs:

    Rep 1 (the "canonical" run)
        biotest.py --phase A,D,E starting from EMPTY data/.
        Produces mr_registry.json + feedback_state + Phase E corpus.

    Reps 2, 3, 4 (continuation runs based on Run 1's state)
        For each rep:
          - restore Run 1's mr_registry.json + feedback_state +
            rule_attempts (so Phase B re-mining sees Run 1's MRs and
            blindspot context, mirroring "next-day continuation")
          - reset only the coverage artefact (jacoco.exec / .coverage / etc.)
          - bump global.seed_rng so Hypothesis explores differently
          - biotest.py --phase A,D,E (full pipeline, just like rep 0)
        Each rep is a full campaign — apples-to-apples with how other
        tools' reps work (each rep is its own full fuzzing run with a
        different RNG seed). Std across 4 reps reflects whole-pipeline
        variance, but rooted in Run 1's mined registry rather than
        empty state.

Output layout (per cell):
    out_root/<cell>/run_0/  -- Run 1 (full A,D,E)
    out_root/<cell>/run_1/  -- replica 1 (Phase C only)
    out_root/<cell>/run_2/
    out_root/<cell>/run_3/
    out_root/<cell>/run1_state/  -- frozen mr_registry + state files

Each run_<i>/measurement.json has the same shape as the fullD runner.
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


@dataclass
class Cell:
    sut: str
    fmt: str
    max_iterations: int
    reset_paths: list[str]
    report_path: str
    report_kind: str
    extra_reset_globs: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.sut}_{self.fmt.lower()}"


CELLS: list[Cell] = [
    Cell(
        sut="htsjdk", fmt="VCF", max_iterations=4,
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        report_path="coverage_artifacts/jacoco/jacoco.xml",
        report_kind="jacoco",
    ),
    Cell(
        sut="vcfpy", fmt="VCF", max_iterations=1,
        reset_paths=["coverage_artifacts/.coverage"],
        report_path="coverage_artifacts/.coverage.json",
        report_kind="coveragepy",
    ),
    Cell(
        sut="htsjdk", fmt="SAM", max_iterations=2,
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        report_path="coverage_artifacts/jacoco/jacoco.xml",
        report_kind="jacoco",
    ),
    Cell(
        sut="biopython", fmt="SAM", max_iterations=2,
        reset_paths=["coverage_artifacts/.coverage"],
        report_path="coverage_artifacts/.coverage.json",
        report_kind="coveragepy",
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


def log(msg: str, fh) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)
    fh.write(line + "\n")
    fh.flush()


def reset_artefacts(cell: Cell, fh) -> None:
    for rel in cell.reset_paths:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                p.unlink() if not p.is_dir() else shutil.rmtree(p)
                log(f"    reset artefact: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)
    for glob_pat in cell.extra_reset_globs:
        for p in REPO_ROOT.glob(glob_pat):
            try:
                p.unlink() if not p.is_dir() else shutil.rmtree(p)
            except OSError:
                pass


def reset_state(fh) -> None:
    for rel in STATE_FILES:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                p.unlink()
                log(f"    reset state: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)


def freeze_run1(state_dir: Path, fh) -> None:
    """Copy mr_registry + feedback_state + rule_attempts to a frozen
    snapshot directory after Run 1 finishes."""
    state_dir.mkdir(parents=True, exist_ok=True)
    for rel in STATE_FILES:
        src = REPO_ROOT / rel
        if src.exists():
            dst = state_dir / src.name
            try:
                shutil.copy2(src, dst)
                log(f"    froze: {rel} -> {dst.relative_to(REPO_ROOT)}", fh)
            except OSError as e:
                log(f"    freeze-skip ({e}): {rel}", fh)


def restore_run1(state_dir: Path, fh) -> None:
    """Restore the frozen Run 1 state files into data/ before a replica."""
    for rel in STATE_FILES:
        name = Path(rel).name
        src = state_dir / name
        if src.exists():
            dst = REPO_ROOT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(src, dst)
                log(f"    restored: {rel}", fh)
            except OSError as e:
                log(f"    restore-skip ({e}): {rel}", fh)


def build_small_seeds_dir(tmp_root: Path, max_per_fmt: int = 10) -> Path:
    for fmt in ("vcf", "sam"):
        dst = tmp_root / fmt
        dst.mkdir(parents=True, exist_ok=True)
        src_dir = REPO_ROOT / "seeds" / fmt
        if not src_dir.exists():
            continue
        files = sorted(src_dir.glob(f"*.{fmt}"))
        eligible = [
            p for p in files
            if not p.name.startswith("kept_")
            and not p.name.startswith("synthetic_")
        ]
        for src in eligible[:max_per_fmt]:
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
    cell: Cell, rep: int, out_dir: Path,
    seeds_root: Path, run1: bool,
) -> Path:
    """run1=True → full A,D,E config (rep 0). Otherwise → Phase C config
    that runs against Run 1's restored registry (no Phase B re-mine)."""
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))
    phase_c = src.setdefault("phase_c", {})
    phase_c["format_filter"] = cell.fmt
    phase_c["seeds_dir"] = str(seeds_root)
    phase_c["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}
    fb = src.setdefault("feedback_control", {})
    fb["primary_target"] = cell.sut
    # All reps run the full pipeline (A,D,E). Reps 1..N just inherit
    # Run 1's state files via the disk restore that happens before
    # each rep (see main()), so Phase D's mining + iteration starts
    # from Run 1's MR set rather than from scratch.
    fb["enabled"] = True
    fb["max_iterations"] = cell.max_iterations
    fb["plateau_patience"] = cell.max_iterations + 1
    fb["coverage_plateau_patience"] = cell.max_iterations + 1
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


def run_biotest(
    cfg_path: Path, budget_s: int, log_path: Path, fh,
    phases: str,
) -> int:
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path),
        "--phase", phases,
        "--verbose",
    ]
    log(f"    cmd: {' '.join(cmd)}", fh)
    log(f"    budget: {budget_s}s", fh)
    started = time.time()
    with log_path.open("wb") as lf:
        try:
            proc = subprocess.Popen(
                cmd, stdout=lf, stderr=subprocess.STDOUT,
                env=os.environ.copy(), cwd=str(REPO_ROOT),
            )
        except Exception as e:
            log(f"    launch-error: {e}", fh)
            return -1
        try:
            proc.wait(timeout=budget_s)
        except subprocess.TimeoutExpired:
            log(f"    timeout after {budget_s}s - terminating", fh)
            proc.terminate()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    pass
    elapsed = time.time() - started
    log(f"    exit={proc.returncode} elapsed={elapsed:.1f}s", fh)
    return proc.returncode if proc.returncode is not None else -1


def regenerate_report(cell: Cell, fh) -> None:
    if cell.report_kind == "jacoco":
        exec_path = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco.exec"
        cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
        jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
        xml = REPO_ROOT / cell.report_path
        if exec_path.exists() and cli.exists() and jar.exists():
            proc = subprocess.run(
                ["java", "-jar", str(cli), "report", str(exec_path),
                 "--classfiles", str(jar), "--xml", str(xml)],
                capture_output=True, timeout=180, cwd=str(REPO_ROOT),
            )
            if proc.returncode != 0:
                log(f"    jacoco regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)


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


def measure_cell(cell: Cell, fh) -> dict[str, Any]:
    regenerate_report(cell, fh)
    report = REPO_ROOT / cell.report_path
    result = {"line_pct": 0.0, "branch_pct": 0.0, "covered": 0, "total": 0,
              "source": cell.report_path, "status": "missing"}
    if cell.report_kind == "coveragepy":
        src = REPO_ROOT / "coverage_artifacts" / ".coverage"
        if src.exists():
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
                log(f"    coveragepy conv failed: {conv.stderr.decode(errors='replace')[:200]}", fh)
                result["status"] = "convert_failed"
                return result
            report = dest
        else:
            return result
    if not report.exists():
        return result
    base = [
        sys.executable,
        str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
        "--report", str(report),
        "--sut", cell.sut, "--format", cell.fmt,
    ]
    if cell.report_kind == "jacoco":
        proc_l = subprocess.run(base + ["--metric", "LINE"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        proc_b = subprocess.run(base + ["--metric", "BRANCH"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        result["line_pct"], result["covered"], result["total"] = _parse_overall(
            proc_l.stdout.decode(errors="replace")
        )
        result["branch_pct"], _, _ = _parse_overall(
            proc_b.stdout.decode(errors="replace")
        )
    else:
        proc = subprocess.run(base, capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        result["line_pct"], result["covered"], result["total"] = _parse_overall(
            proc.stdout.decode(errors="replace")
        )
    result["status"] = "ok"
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", type=Path,
                    default=REPO_ROOT / "compares" / "results" / "coverage"
                    / "biotest_4rep_run1based_20260426")
    ap.add_argument("--vcf-budget-s", type=int, default=5400)
    ap.add_argument("--sam-budget-s", type=int, default=3600)
    ap.add_argument("--phase-c-budget-s", type=int, default=2700,
                    help="Wall cap for Phase-C-only replica reps (defaults 45 min).")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--seeds-per-fmt", type=int, default=10)
    ap.add_argument("--only", action="append", default=[])
    args = ap.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    log_path = args.out_root / "run.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("===== 4-rep BioTest run1-based sweep =====", fh)
    log(f"out_root = {args.out_root}", fh)
    log("Per cell: rep 0 = full A,D,E; reps 1..N-1 = Phase C against frozen Run 1 state.", fh)

    seeds_small = args.out_root / "seeds_small"
    build_small_seeds_dir(seeds_small, max_per_fmt=args.seeds_per_fmt)
    log(f"seeds_small = {seeds_small}", fh)

    cells = [c for c in CELLS if (not args.only or c.label in args.only)]
    log(f"cells = {[c.label for c in cells]}", fh)

    results: list[dict[str, Any]] = []
    sweep_started = time.time()
    for cell in cells:
        cell_dir = args.out_root / cell.label
        cell_dir.mkdir(parents=True, exist_ok=True)
        state_dir = cell_dir / "run1_state"
        log(f"\n### cell: {cell.label} ({cell.sut}/{cell.fmt}, max_iter={cell.max_iterations})", fh)

        for rep in range(args.reps):
            rep_dir = cell_dir / f"run_{rep}"
            rep_dir.mkdir(parents=True, exist_ok=True)
            is_run1 = (rep == 0)
            log(f"  -- rep {rep} ({'Run 1 / canonical' if is_run1 else 'replica from Run 1'}) --", fh)

            if is_run1:
                reset_state(fh)
            else:
                # Restore Run 1's frozen state, only reset coverage artefact.
                restore_run1(state_dir, fh)
            reset_artefacts(cell, fh)

            cfg_path = write_temp_config(cell, rep, rep_dir, seeds_small, run1=is_run1)
            biotest_log = rep_dir / "biotest.log"
            # Every rep runs the full pipeline (A,D,E). Reps 1..N
            # differ from rep 0 only in the data/ files restored
            # before launch — Run 1 starts empty, replicas inherit
            # Run 1's mined MR set.
            phases = "A,D,E"
            budget = args.vcf_budget_s if cell.fmt == "VCF" else args.sam_budget_s

            t0 = time.time()
            exit_code = run_biotest(cfg_path, budget, biotest_log, fh, phases)
            elapsed = time.time() - t0

            if is_run1:
                freeze_run1(state_dir, fh)

            cov = measure_cell(cell, fh)
            rec = {
                "cell": cell.label, "sut": cell.sut, "format": cell.fmt,
                "rep": rep, "exit_code": exit_code,
                "elapsed_s": round(elapsed, 1),
                "max_iterations": cell.max_iterations,
                "phases": phases,
                "rep_kind": "run1_canonical" if is_run1 else "replica_from_run1",
                **cov,
            }
            results.append(rec)
            (rep_dir / "measurement.json").write_text(
                json.dumps(rec, indent=2), encoding="utf-8",
            )
            log(
                f"    -> line={cov['line_pct']:.2f}% covered={cov['covered']}/{cov['total']} status={cov['status']}",
                fh,
            )
            (args.out_root / "results.json").write_text(
                json.dumps(results, indent=2), encoding="utf-8",
            )

    log(f"\n===== sweep complete in {(time.time()-sweep_started)/60:.1f} min =====", fh)
    fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
