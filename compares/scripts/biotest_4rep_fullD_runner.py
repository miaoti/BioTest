#!/usr/bin/env python3
"""Full-pipeline 4-rep BioTest coverage sweep (Phase B + C + D).

Unlike `biotest_4rep_runner.py` (which ran Phase C only against a pinned
registry), this script runs the FULL canonical pipeline for each rep:

    biotest.py --phase A,B,C,D
      Phase A (spec ingest — reuses cached chroma_db after first ingest)
      Phase B (LLM-driven MR mining, fresh each rep)
      Phase C (cross-execution testing, wrapped in coverage.py ctx)
      Phase D (iterative feedback loop, max_iterations from config)

Each rep is INDEPENDENT: the orchestrator deletes `data/mr_registry.json`,
`data/feedback_state.json`, and `data/rule_attempts.json` before the run
so Phase B mines fresh and Phase D starts from iteration 0. The coverage
artefact for the cell's primary SUT is reset in the same step so the
per-rep reading reflects only that rep's work.

Cells are restricted to those with working coverage instrumentation on
this machine:
    - htsjdk / VCF  (JaCoCo)
    - vcfpy / VCF   (coverage.py)
    - htsjdk / SAM  (JaCoCo)
    - biopython / SAM (coverage.py)
pysam (Cython .so → coverage.py blind), seqan3 (harness doesn't link
seqan3 on Windows/MinGW), and noodles (no cargo-llvm-cov build present)
are excluded from this sweep. All three have documented structural zeros
in `coverage_notes/` or the README.
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
    max_iterations: int  # Phase D iteration cap
    reset_paths: list[str]
    report_path: str
    report_kind: str
    extra_reset_globs: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.sut}_{self.fmt.lower()}"


CELLS: list[Cell] = [
    # max_iterations=30 across the board — biotest's natural Phase D
    # loop with seed_synthesis off finishes 4 iters in ~21 min, far
    # below the 7200 s DESIGN parity budget. Setting 30 lets the loop
    # run until biotest's internal `timeout_minutes=110` fires the
    # graceful between-iter exit. Each iter does its own Phase B
    # re-mining (LLM) + Phase C testing, so Hypothesis RNG has
    # many more opportunities to diverge between reps → real std.
    Cell(
        sut="htsjdk",
        fmt="VCF",
        max_iterations=30,
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        report_path="coverage_artifacts/jacoco/jacoco.xml",
        report_kind="jacoco",
    ),
    Cell(
        sut="vcfpy",
        fmt="VCF",
        max_iterations=30,
        reset_paths=["coverage_artifacts/.coverage"],
        report_path="coverage_artifacts/.coverage.json",
        report_kind="coveragepy",
    ),
    Cell(
        sut="htsjdk",
        fmt="SAM",
        max_iterations=30,
        reset_paths=[
            "coverage_artifacts/jacoco/jacoco.exec",
            "coverage_artifacts/jacoco/jacoco.xml",
        ],
        report_path="coverage_artifacts/jacoco/jacoco.xml",
        report_kind="jacoco",
    ),
    Cell(
        sut="biopython",
        fmt="SAM",
        max_iterations=30,
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str, fh) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)
    fh.write(line + "\n")
    fh.flush()


def reset_cell(cell: Cell, fh) -> None:
    for rel in cell.reset_paths:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                log(f"    reset artefact: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)
    for glob_pat in cell.extra_reset_globs:
        for p in REPO_ROOT.glob(glob_pat):
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
            except OSError:
                pass


def reset_state(fh) -> None:
    """Delete mr_registry + feedback_state + rule_attempts so Phase D
    treats this rep as a fresh run."""
    for rel in STATE_FILES:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                p.unlink()
                log(f"    reset state: {rel}", fh)
            except OSError as e:
                log(f"    reset-skip ({e}): {rel}", fh)


def build_small_seeds_dir(tmp_root: Path, max_per_fmt: int = 0) -> Path:
    """Stage `tmp_root/{vcf,sam}/` with a curated, NON-BioTest-generated
    seed subset. Excludes `kept_*` (corpus_keeper output) and
    `synthetic_*` (Phase D seed_synthesis output) so cross-tool
    coverage comparisons aren't biased by seeds BioTest authored in
    prior runs. Tier-1 curated seeds + external-tool seeds (jazzer_*,
    bcftools_*, htsjdk_*, real_world_*, etc.) are kept.

    `max_per_fmt=0` means "use ALL eligible seeds" — required for
    DESIGN.md §3 compute parity (Jazzer × htsjdk fuzzes for 7200 s
    against its own coverage-guided corpus; biotest needs a
    correspondingly rich starting corpus to use the same budget)."""
    for fmt in ("vcf", "sam"):
        dst = tmp_root / fmt
        dst.mkdir(parents=True, exist_ok=True)
        src_dir = REPO_ROOT / "seeds" / fmt
        if not src_dir.exists():
            continue
        files = sorted(src_dir.glob(f"*.{fmt}"))
        # Strictly exclude BioTest-generated seeds (kept_* from corpus
        # keeper, synthetic_* from Phase D seed synthesis). Anything
        # else is curated or sourced from another tool's corpus.
        eligible = [
            p for p in files
            if not p.name.startswith("kept_")
            and not p.name.startswith("synthetic_")
        ]
        chosen = eligible if max_per_fmt <= 0 else eligible[:max_per_fmt]
        for src in chosen:
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


def write_temp_config(cell: Cell, rep: int, out_dir: Path,
                      seeds_root: Path) -> Path:
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))
    phase_c = src.setdefault("phase_c", {})
    phase_c["format_filter"] = cell.fmt
    phase_c["seeds_dir"] = str(seeds_root)
    # Keep corpus_keeper off so reps don't cross-pollute via kept_* accretion.
    phase_c["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}
    fb = src.setdefault("feedback_control", {})
    fb["enabled"] = True
    fb["primary_target"] = cell.sut
    fb["max_iterations"] = cell.max_iterations
    # Each rep is independent — no prior state to honor; turn off early-stops
    # that don't matter on short reps.
    # Disable plateau-based early stops (would otherwise fire when
    # coverage flatlines for a few iters; we WANT biotest to keep
    # iterating until timeout_minutes fires so it uses the full
    # DESIGN parity budget).
    fb["plateau_patience"] = cell.max_iterations + 1
    fb["coverage_plateau_patience"] = cell.max_iterations + 1
    fb["min_coverage_delta_pp"] = 0.0  # don't require minimum growth per iter
    # timeout_minutes lets biotest self-terminate cleanly between
    # iterations BEFORE the orchestrator's wall cap fires (so
    # coverage.py's __exit__ runs). 110 min sits 10 min below the
    # 7200 s (120 min) DESIGN parity cap.
    fb["timeout_minutes"] = 110
    # Bound Phase E (Rank 12 structural + Rank 13 rawfuzz) — defaults
    # (200/10 per seed) are sized for canonical full-corpus runs.
    # Coverage is already collected in Phase D; Phase E only writes
    # auxiliary seeds/<fmt>_struct/ and seeds/<fmt>_rawfuzz/ corpora
    # that Phase-3 mutation testing reads downstream.
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


def run_biotest_full(cfg_path: Path, budget_s: int,
                     log_path: Path, fh) -> int:
    """Run `biotest.py --phase A,D,E` with a strict wall-time cap.

    `--phase D` internally runs Phase B + Phase C for each iteration
    (with coverage.py wrapping). `--phase E` then augments the seed
    corpus (Rank 12 structural + Rank 13 lenient byte fuzz) — added
    to the pipeline 2026-04-25, runs AFTER coverage is already
    collected so it doesn't change the coverage number we report,
    but it IS the canonical pipeline so we run it for completeness.
    Phase E is bounded via `phase_e.{structural_max_per_seed,
    rawfuzz_n_per_seed}` knobs in the temp config so it doesn't push
    rep wall time past the cap.
    """
    cmd = [
        sys.executable, str(REPO_ROOT / "biotest.py"),
        "--config", str(cfg_path),
        "--phase", "A,D,E",
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
        # Phase D's coverage_collector.collect_all() normally regenerates
        # jacoco.xml from jacoco.exec at end of each iteration. Re-run
        # jacococli explicitly in case a mid-iter timeout left the XML stale.
        exec_path = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacoco.exec"
        cli = REPO_ROOT / "coverage_artifacts" / "jacoco" / "jacococli.jar"
        jar = REPO_ROOT / "harnesses" / "java" / "build" / "libs" / "biotest-harness-all.jar"
        xml = REPO_ROOT / cell.report_path
        if exec_path.exists() and cli.exists() and jar.exists():
            proc = subprocess.run(
                ["java", "-jar", str(cli), "report", str(exec_path),
                 "--classfiles", str(jar),
                 "--xml", str(xml)],
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
        sys.executable, str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
        "--report", str(report),
        "--sut", cell.sut,
        "--format", cell.fmt,
    ]
    if cell.report_kind == "jacoco":
        proc_l = subprocess.run(base + ["--metric", "LINE"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        proc_b = subprocess.run(base + ["--metric", "BRANCH"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        out_l = proc_l.stdout.decode(errors="replace")
        out_b = proc_b.stdout.decode(errors="replace")
        result["line_pct"], result["covered"], result["total"] = _parse_overall(out_l)
        result["branch_pct"], _, _ = _parse_overall(out_b)
    else:
        proc = subprocess.run(base, capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        out = proc.stdout.decode(errors="replace")
        result["line_pct"], result["covered"], result["total"] = _parse_overall(out)
    result["status"] = "ok"
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", type=Path,
                    default=REPO_ROOT / "compares" / "results" / "coverage"
                    / "biotest_4rep_fullD_20260423")
    ap.add_argument("--vcf-budget-s", type=int, default=7200,
                    help="Wall-time cap for VCF reps (default 7200 s = "
                    "DESIGN §3 cross-tool parity, matches Jazzer × htsjdk).")
    ap.add_argument("--sam-budget-s", type=int, default=7200,
                    help="Wall-time cap for SAM reps (default 7200 s = "
                    "DESIGN §3 cross-tool parity).")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--seeds-per-fmt", type=int, default=0,
                    help="0 (default) = use ALL non-BioTest seeds "
                    "(33 VCF, 67 SAM). >0 caps per-format count.")
    ap.add_argument("--only", action="append", default=[])
    args = ap.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    log_path = args.out_root / "run.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("===== 4-rep BioTest FULL-pipeline sweep (A,B,C,D) =====", fh)
    log(f"out_root = {args.out_root}", fh)
    log(f"vcf_budget_s = {args.vcf_budget_s}s   sam_budget_s = {args.sam_budget_s}s", fh)
    log(f"reps = {args.reps}   seeds_per_fmt = {args.seeds_per_fmt}", fh)

    seeds_small = args.out_root / "seeds_small"
    build_small_seeds_dir(seeds_small, max_per_fmt=args.seeds_per_fmt)

    cells = [c for c in CELLS if (not args.only or c.label in args.only)]
    log(f"cells = {[c.label for c in cells]}", fh)

    results: list[dict[str, Any]] = []
    sweep_started = time.time()
    for cell in cells:
        cell_dir = args.out_root / cell.label
        cell_dir.mkdir(parents=True, exist_ok=True)
        log(f"\n### cell: {cell.label} ({cell.sut}/{cell.fmt}, max_iter={cell.max_iterations})", fh)
        for rep in range(args.reps):
            rep_dir = cell_dir / f"run_{rep}"
            rep_dir.mkdir(parents=True, exist_ok=True)
            log(f"  -- rep {rep} --", fh)
            reset_state(fh)
            reset_cell(cell, fh)
            cfg_path = write_temp_config(cell, rep, rep_dir, seeds_small)
            biotest_log = rep_dir / "biotest.log"
            budget = args.vcf_budget_s if cell.fmt == "VCF" else args.sam_budget_s
            t0 = time.time()
            exit_code = run_biotest_full(cfg_path, budget, biotest_log, fh)
            elapsed = time.time() - t0
            cov = measure_cell(cell, fh)
            rec = {
                "cell": cell.label,
                "sut": cell.sut,
                "format": cell.fmt,
                "rep": rep,
                "exit_code": exit_code,
                "elapsed_s": round(elapsed, 1),
                "max_iterations": cell.max_iterations,
                "phases": "A,B,C,D",
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
