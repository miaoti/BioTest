#!/usr/bin/env python3
"""4-rep coverage sweep of BioTest across every configured SUT × format.

For each (SUT, format) cell, run biotest.py four times (rep 0..3) with
the per-rep seed advanced (42+rep) so Hypothesis's strategies explore
different material each time. After each rep we measure the resulting
coverage artefact through `compares/scripts/measure_coverage.py` under
the SUT's filter from `biotest_config.yaml`, then record the number.

The script is launched in the background. Progress streams to
`compares/results/coverage/biotest_4rep/run.log`. Final aggregation
lives in `SUMMARY.md` alongside per-rep JSON.

Budget rationale: at `BUDGET_S = 300` per rep, biotest.py's Phase C
bootstrap eats most of the window — so coverage for each cell is best
read AFTER the subprocess exits (coverage.py context-exit, JaCoCo agent
dump on JVM shutdown, gcovr on gcov dump at process end). That's the
"end-of-run" snapshot the README's `COVERAGE_MATRIX.md` already uses for
BioTest cells, just repeated four times with varying seeds.

Per-cell isolation:
- Reset the relevant artefact at the start of every rep so numbers
  don't accumulate across reps of the same cell.
- Each cell writes a temp biotest_config.yaml with a per-rep seed and
  the cell's (primary_target, format_filter).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Cells + per-cell coverage wiring
# ---------------------------------------------------------------------------

@dataclass
class Cell:
    sut: str
    fmt: str  # "VCF" | "SAM"
    # Which artefact(s) to reset + read after the subprocess exits.
    # `reset` is a list of relative paths (files or dirs); `report` is the
    # single file measure_coverage.py consumes.
    reset_paths: list[str]
    report_path: str
    report_kind: str  # "jacoco" | "coveragepy" | "gcovr" | "llvmcov"
    extra_reset_globs: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.sut}_{self.fmt.lower()}"


CELLS: list[Cell] = [
    # --- VCF cells -------------------------------------------------------
    Cell(
        sut="htsjdk",
        fmt="VCF",
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
        reset_paths=["coverage_artifacts/.coverage"],
        report_path="coverage_artifacts/.coverage.json",
        report_kind="coveragepy",
    ),
    # NOTE: noodles (Rust) needs a cargo-llvm-cov instrumented binary at
    # harnesses/rust/noodles_harness/target/llvm-cov-target/release/noodles_harness.
    # That build isn't present in this checkout, so the runner falls back
    # to the standard binary and no profraw is emitted — coverage would
    # read 0 for every rep. Skip the cell to keep the sweep honest; see
    # harnesses/rust/noodles_harness/README.md for the rebuild recipe.
    Cell(
        sut="pysam",
        fmt="VCF",
        reset_paths=[],
        report_path="coverage_artifacts/pysam/summary.1.json",
        report_kind="coveragepy",
        extra_reset_globs=[
            "coverage_artifacts/pysam/.coverage*",
            "coverage_artifacts/pysam/summary.*.json",
        ],
    ),
    # --- SAM cells -------------------------------------------------------
    Cell(
        sut="htsjdk",
        fmt="SAM",
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
        reset_paths=["coverage_artifacts/.coverage"],
        report_path="coverage_artifacts/.coverage.json",
        report_kind="coveragepy",
    ),
    Cell(
        sut="seqan3",
        fmt="SAM",
        reset_paths=["coverage_artifacts/gcovr.json"],
        report_path="coverage_artifacts/gcovr.json",
        report_kind="gcovr",
        extra_reset_globs=["harnesses/cpp/build/*.gcda"],
    ),
    Cell(
        sut="pysam",
        fmt="SAM",
        reset_paths=[],
        report_path="coverage_artifacts/pysam/summary.1.json",
        report_kind="coveragepy",
        extra_reset_globs=[
            "coverage_artifacts/pysam/.coverage*",
            "coverage_artifacts/pysam/summary.*.json",
        ],
    ),
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
    """Delete artefact(s) before a rep so coverage doesn't accumulate."""
    for rel in cell.reset_paths:
        p = REPO_ROOT / rel
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                log(f"    reset: {rel}", fh)
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


def build_small_seeds_dir(
    tmp_root: Path, max_per_fmt: int = 8,
) -> Path:
    """Populate `tmp_root/{vcf,sam}/` with a small deterministic seed subset
    so each rep's Phase C executes in minutes, not hours. Seeds are symlinks
    into the repo's full `seeds/` so disk churn is negligible."""
    for fmt in ("vcf", "sam"):
        dst = tmp_root / fmt
        dst.mkdir(parents=True, exist_ok=True)
        src_dir = REPO_ROOT / "seeds" / fmt
        if not src_dir.exists():
            continue
        # Prefer the small curated seeds first (bcftools_/htsjdk_/simple_) —
        # they're small and exercise basic parse paths. Backfill with a few
        # kept_ seeds.
        files = sorted(src_dir.glob(f"*.{fmt}"))
        priority = [p for p in files if not p.name.startswith("kept_")]
        filler = [p for p in files if p.name.startswith("kept_")]
        chosen = (priority + filler)[:max_per_fmt]
        for src in chosen:
            link = dst / src.name
            if link.exists():
                continue
            try:
                os.symlink(src.resolve(), link)
            except OSError:
                shutil.copy2(src, link)
    # Carry toy reference + sibling dirs that transforms expect.
    ref_src = REPO_ROOT / "seeds" / "ref"
    if ref_src.exists():
        ref_dst = tmp_root / "ref"
        if not ref_dst.exists():
            try:
                shutil.copytree(ref_src, ref_dst)
            except OSError:
                pass
    return tmp_root


def write_temp_config(cell: Cell, rep: int, out_dir: Path, seeds_root: Path) -> Path:
    """Write a per-rep config that pins primary_target, format_filter, seed,
    and a small seeds_dir so Phase C actually finishes in-budget."""
    src = yaml.safe_load((REPO_ROOT / "biotest_config.yaml").read_text("utf-8"))
    phase_c = src.setdefault("phase_c", {})
    phase_c["format_filter"] = cell.fmt
    phase_c["seeds_dir"] = str(seeds_root)
    # Disable the coverage-growth corpus keeper so reps don't cross-
    # pollute each other via seeds/<fmt>/kept_* accretion.
    phase_c["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}
    fb = src.setdefault("feedback_control", {})
    fb["primary_target"] = cell.sut
    # Disable Phase D so we don't iterate — Phase C runs MRs once.
    fb["enabled"] = False
    # Vary the master seed per rep.
    src.setdefault("global", {})["seed_rng"] = 42 + rep
    dest = out_dir / f"biotest_config.rep{rep}.yaml"
    dest.write_text(yaml.safe_dump(src, sort_keys=False), encoding="utf-8")
    return dest


def run_biotest(
    cfg_path: Path, budget_s: int, log_path: Path, fh,
    phases: str = "C",
) -> int:
    """Invoke biotest.py with a strict wall-time cap.

    Defaults to Phase C only — re-mining MRs via Phase B each rep is an
    LLM call that costs 5-10 min per iteration, and the registry already
    has enforced MRs for the target format.
    """
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
            log(f"    timeout after {budget_s}s — terminating", fh)
            proc.terminate()
            try:
                proc.wait(timeout=30)
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
    """For artefact kinds that aren't auto-regenerated when biotest runs
    in standalone Phase C mode, rebuild the summary report from its raw
    source data (jacoco.exec -> jacoco.xml, .gcda -> gcovr.json)."""
    if cell.report_kind == "jacoco":
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
    elif cell.report_kind == "gcovr":
        build_dir = REPO_ROOT / "harnesses" / "cpp" / "build"
        src_root = REPO_ROOT / "SUTfolder" / "cpp" / "seqan3" / "include"
        out = REPO_ROOT / cell.report_path
        if any(build_dir.glob("*.gcda")):
            proc = subprocess.run(
                [sys.executable, "-m", "gcovr",
                 "--json", str(out),
                 "--root", str(src_root),
                 str(build_dir)],
                capture_output=True, timeout=180, cwd=str(REPO_ROOT),
            )
            if proc.returncode != 0:
                # Fallback: try with --object-directory layout
                proc = subprocess.run(
                    [sys.executable, "-m", "gcovr",
                     "--json", str(out),
                     "--object-directory", str(build_dir),
                     str(build_dir)],
                    capture_output=True, timeout=180, cwd=str(REPO_ROOT),
                )
            if proc.returncode != 0:
                log(f"    gcovr regen failed: {proc.stderr.decode(errors='replace')[:200]}", fh)
    elif cell.report_kind == "coveragepy" and cell.sut == "pysam":
        # pysam's Docker harness writes summary.*.json directly at exit —
        # nothing to regenerate.
        return


def measure_cell_coverage(cell: Cell, fh) -> dict[str, Any]:
    """Read the cell's final coverage artefact and return line/branch %."""
    # Rebuild derived reports from raw data (jacoco exec, gcda, etc.)
    regenerate_report(cell, fh)

    report = REPO_ROOT / cell.report_path
    result = {"line_pct": 0.0, "branch_pct": 0.0,
              "covered": 0, "total": 0, "source": cell.report_path,
              "status": "missing"}

    # coverage.py uses a SQLite .coverage; convert to JSON before measuring.
    if cell.report_kind == "coveragepy":
        src = REPO_ROOT / "coverage_artifacts" / ".coverage"
        if cell.sut == "pysam":
            # pysam writes summary.*.json directly — no conversion needed.
            candidates = sorted(
                (REPO_ROOT / "coverage_artifacts" / "pysam").glob("summary.*.json")
            )
            if not candidates:
                return result
            report = candidates[-1]
        elif src.exists():
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
                log(f"    coveragepy conversion failed: {conv.stderr.decode(errors='replace')[:300]}", fh)
                result["status"] = "convert_failed"
                return result
            report = dest
        else:
            return result

    if not report.exists():
        return result

    cmd = [
        sys.executable, str(REPO_ROOT / "compares" / "scripts" / "measure_coverage.py"),
        "--report", str(report),
        "--sut", cell.sut,
        "--format", cell.fmt,
    ]
    if cell.report_kind == "jacoco":
        # Measure BRANCH separately for jacoco.
        proc_l = subprocess.run(cmd + ["--metric", "LINE"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        proc_b = subprocess.run(cmd + ["--metric", "BRANCH"],
                                capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        out_l = proc_l.stdout.decode(errors="replace")
        out_b = proc_b.stdout.decode(errors="replace")
        # Parse "OVERALL (weighted)                   X/Y   ( P%)"
        result["line_pct"], result["covered"], result["total"] = _parse_overall(out_l)
        result["branch_pct"], _, _ = _parse_overall(out_b)
    else:
        proc = subprocess.run(cmd,
                              capture_output=True, timeout=120, cwd=str(REPO_ROOT))
        out = proc.stdout.decode(errors="replace")
        result["line_pct"], result["covered"], result["total"] = _parse_overall(out)

    result["status"] = "ok"
    return result


def _parse_overall(stdout: str) -> tuple[float, int, int]:
    """Parse the 'OVERALL (weighted)' line from measure_coverage.py output."""
    for line in stdout.splitlines():
        if "OVERALL" in line and "weighted" in line:
            # format: OVERALL (weighted)                  X/Y   ( P%)
            try:
                tail = line.split(")", 1)[1].strip()
                frac, pct = tail.split("(")
                covered_s, total_s = frac.strip().split("/")
                pct = pct.replace("%", "").replace(")", "").strip()
                return float(pct), int(covered_s), int(total_s)
            except Exception:
                continue
    return 0.0, 0, 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", type=Path,
                    default=REPO_ROOT / "compares" / "results" / "coverage" / "biotest_4rep")
    ap.add_argument("--budget-s", type=int, default=300,
                    help="Per-rep wall-time cap passed to biotest.py subprocess.")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--seeds-per-fmt", type=int, default=8,
                    help="Per-format seed count fed to Phase C (keeps runs bounded).")
    ap.add_argument("--only", action="append", default=[],
                    help="Only run these cells (format: sut_fmt, e.g. htsjdk_vcf).")
    ap.add_argument("--skip", action="append", default=[],
                    help="Skip these cells.")
    args = ap.parse_args()

    args.out_root.mkdir(parents=True, exist_ok=True)
    log_path = args.out_root / "run.log"
    fh = log_path.open("a", encoding="utf-8", buffering=1)

    log("===== 4-rep BioTest coverage sweep =====", fh)
    log(f"out_root = {args.out_root}", fh)
    log(f"budget_s = {args.budget_s}s  reps = {args.reps}", fh)

    seeds_small = args.out_root / "seeds_small"
    build_small_seeds_dir(seeds_small, max_per_fmt=args.seeds_per_fmt)
    log(
        f"seeds_small = {seeds_small} (<= {args.seeds_per_fmt} files per format)",
        fh,
    )

    cells = [c for c in CELLS
             if (not args.only or c.label in args.only)
             and c.label not in args.skip]
    log(f"cells = {[c.label for c in cells]}", fh)

    results: list[dict[str, Any]] = []
    all_started = time.time()
    for cell in cells:
        cell_dir = args.out_root / cell.label
        cell_dir.mkdir(parents=True, exist_ok=True)
        log(f"\n### cell: {cell.label} ({cell.sut}/{cell.fmt})", fh)
        for rep in range(args.reps):
            rep_dir = cell_dir / f"run_{rep}"
            rep_dir.mkdir(parents=True, exist_ok=True)
            log(f"  -- rep {rep} --", fh)
            reset_cell(cell, fh)
            cfg_path = write_temp_config(cell, rep, rep_dir, seeds_small)
            biotest_log = rep_dir / "biotest.log"
            t0 = time.time()
            exit_code = run_biotest(cfg_path, args.budget_s, biotest_log, fh)
            elapsed = time.time() - t0
            cov = measure_cell_coverage(cell, fh)
            rec = {
                "cell": cell.label,
                "sut": cell.sut,
                "format": cell.fmt,
                "rep": rep,
                "exit_code": exit_code,
                "elapsed_s": round(elapsed, 1),
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
            # Flush an incremental combined JSON so partial runs are usable.
            (args.out_root / "results.json").write_text(
                json.dumps(results, indent=2), encoding="utf-8",
            )

    total_elapsed = time.time() - all_started
    log(f"\n===== sweep complete in {total_elapsed/60:.1f} min =====", fh)
    fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
