"""E1 metrics runner — coverage / validity / mutation / bug bench.

Runs after the E1 wrapper (run_e1.py) completes both VCF and SAM.
Each metric step shells out to existing scripts in compares/scripts/
with E1's isolated corpus paths so no main-line state is touched.

Steps (each independent; failures are logged but don't stop the chain):
  1. Build combined corpus per format (primary + Phase E struct + rawfuzz)
  2. Validity probe per (SUT, format)
  3. Coverage summary from already-captured artifacts
  4. Mutation per scored cell (htsjdk PIT, vcfpy/biopython mutmut,
     noodles cargo-mutants, seqan3 mull) via mutation_driver.py
  5. Bug bench via bug_bench_driver.py (--only-tool biotest, with E1
     corpus paths supplied via --seed-corpus-{vcf,sam})

Usage:
    py -3.12 compares/ApplicationStudy/E1_no_phase_a/run_metrics.py
        [--skip-validity] [--skip-coverage]
        [--skip-mutation] [--skip-bug-bench]
        [--no-precheck]
        [--mutation-budget-s 7200]  [--bug-bench-budget-s 1800]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

E1_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = E1_ROOT.parents[2]
RESULTS_ROOT = E1_ROOT / "results"
METRICS_ROOT = RESULTS_ROOT / "metrics"

# Per DESIGN.md §4.1 — Mutation-scored cells. Reference voters (pysam,
# htslib, reference) appear in validity probe but not mutation/bug-bench
# (no mutation tool, or not scored against other fuzzers).
MUTATION_CELLS = [
    # (sut, format)
    ("htsjdk",    "VCF"),
    ("htsjdk",    "SAM"),
    ("vcfpy",     "VCF"),
    ("noodles",   "VCF"),
    ("biopython", "SAM"),
    ("seqan3",    "SAM"),
]

# Voters get validity probe only.
ALL_VALIDITY_CELLS = MUTATION_CELLS + [
    ("pysam",     "VCF"), ("pysam",     "SAM"),
    ("htslib",    "VCF"), ("htslib",    "SAM"),
    ("reference", "VCF"), ("reference", "SAM"),
]


def _log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    # Force UTF-8 stdout on Windows where the default cp1252 codec can't
    # encode arrows / accents that show up in path strings or summaries.
    line = f"[{ts}] [metrics] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((line + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()


def _bash_exe() -> str:
    """Return path to Git Bash, NOT WSL bash.

    On Windows, subprocess.run(['bash', ...]) often resolves to WSL's
    /usr/bin/bash, which requires /mnt/c/... paths and breaks our
    Windows-style script paths. Prefer the Git Bash binary explicitly.
    Falls back to plain 'bash' on non-Windows or when Git Bash isn't
    installed in the canonical location.
    """
    candidates = [
        r"C:\Program Files\Git\usr\bin\bash.EXE",
        r"C:\Program Files\Git\bin\bash.exe",
    ]
    for c in candidates:
        if Path(c).is_file():
            return c
    return "bash"


def _msys_path(p) -> str:
    """Convert a Windows path to MSYS / Git Bash form.

    `C:\\Users\\miaot\\foo` -> `/c/Users/miaot/foo`
    so phase3_*.sh's REPO_ROOT-prefix-stripping (e.g.
    `${OUT_DIR#${REPO_ROOT}/}`) and Docker mount path math line up
    with what the script computes from `BASH_SOURCE[0]`.
    """
    s = str(Path(p).resolve()).replace("\\", "/")
    if len(s) >= 2 and s[1] == ":":
        return f"/{s[0].lower()}{s[2:]}"
    return s


def _check_e1_done() -> tuple[bool, str]:
    vcf_log = RESULTS_ROOT / "vcf" / "run.log"
    sam_log = RESULTS_ROOT / "sam" / "run.log"
    if not vcf_log.exists():
        return False, f"VCF log missing: {vcf_log}"
    if not sam_log.exists():
        return False, f"SAM log missing: {sam_log}"
    if "===VCF DONE===" not in vcf_log.read_text(errors="replace"):
        return False, "VCF run did not reach DONE marker"
    if "===SAM DONE===" not in sam_log.read_text(errors="replace"):
        return False, "SAM run did not reach DONE marker"
    return True, "E1 complete"


def _build_combined_corpus(fmt: str) -> Path:
    """Stage primary + Phase E struct + rawfuzz into one dir for mutation."""
    fmt_lower = fmt.lower()
    src_root = RESULTS_ROOT / fmt_lower / "corpus"
    out_dir = METRICS_ROOT / "combined_corpus" / fmt_lower
    out_dir.mkdir(parents=True, exist_ok=True)

    sources = [
        src_root / fmt_lower,
        src_root / f"{fmt_lower}_struct",
        src_root / f"{fmt_lower}_rawfuzz",
    ]

    n_copied = 0
    for src in sources:
        if not src.is_dir():
            continue
        for f in src.iterdir():
            if not f.is_file() or not f.name.endswith(f".{fmt_lower}"):
                continue
            target = out_dir / f.name
            if target.exists():
                continue
            try:
                shutil.copy2(f, target)
                n_copied += 1
            except OSError as e:
                _log(f"  copy fail {f.name}: {e}")

    total = len(list(out_dir.glob(f"*.{fmt_lower}")))
    _log(f"combined corpus {fmt}: {total} files ({n_copied} newly copied)")
    return out_dir


# ---------------------------------------------------------------------------
# Step 1 — Validity
# ---------------------------------------------------------------------------

def step_validity(combined_corpora: dict[str, Path]) -> dict:
    out_root = METRICS_ROOT / "validity"
    out_root.mkdir(parents=True, exist_ok=True)
    results = {"VCF": {}, "SAM": {}}

    for sut, fmt in ALL_VALIDITY_CELLS:
        out_json = out_root / f"{sut}_{fmt.lower()}.json"
        cmd = [
            "py", "-3.12",
            str(PROJECT_ROOT / "compares" / "scripts" / "validity_probe.py"),
            "--corpus", str(combined_corpora[fmt]),
            "--sut", sut, "--format", fmt,
            "--out", str(out_json),
        ]
        _log(f"validity: {sut} × {fmt}")
        try:
            r = subprocess.run(
                cmd, cwd=str(PROJECT_ROOT), timeout=3600,
                capture_output=True, text=True,
            )
            if out_json.exists():
                results[fmt][sut] = json.loads(out_json.read_text())
            else:
                results[fmt][sut] = {
                    "status": "no_output",
                    "exit_code": r.returncode,
                    "stderr_tail": r.stderr[-500:],
                }
        except subprocess.TimeoutExpired:
            results[fmt][sut] = {"error": "timeout"}
        except Exception as e:
            results[fmt][sut] = {"error": str(e)}

    return results


# ---------------------------------------------------------------------------
# Step 2 — Coverage summary (no re-collection; just inventory artifacts)
# ---------------------------------------------------------------------------

def step_coverage() -> dict:
    out = {"VCF": {}, "SAM": {}}
    for fmt in ("VCF", "SAM"):
        cov_dir = RESULTS_ROOT / fmt.lower() / "coverage"
        if not cov_dir.exists():
            out[fmt] = {"error": f"missing {cov_dir}"}
            continue
        artifacts = {}
        for item in cov_dir.rglob("*"):
            if item.is_file():
                rel = str(item.relative_to(cov_dir))
                artifacts[rel] = item.stat().st_size
        out[fmt] = {
            "coverage_dir": str(cov_dir),
            "artifact_count": len(artifacts),
            "total_bytes": sum(artifacts.values()),
            "artifacts": artifacts,
        }

    summary_path = METRICS_ROOT / "coverage" / "summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(out, indent=2))
    _log(f"coverage summary: {summary_path}")
    return out


# ---------------------------------------------------------------------------
# Step 3 — Mutation
# ---------------------------------------------------------------------------

def step_mutation(combined_corpora: dict[str, Path], budget_s: int) -> dict:
    """Per-SUT mutation runs. Three backends:

    * htsjdk -> compares/scripts/phase3_jazzer_pit.sh (PIT inside Docker
      biotest-bench:latest). Corpus staged at OUT_ROOT/<sut>_<fmt>/run_0/corpus/.
    * biopython -> compares/scripts/phase3_atheris_biopython.sh (mutmut-AST
      inside Docker). Corpus passed via CORPUS_DIR env var.
    * vcfpy / noodles / seqan3 -> compares/scripts/mutation_driver.py
      (--tool biotest --sut <name> --format <fmt>). PYTHONIOENCODING=utf-8
      added so the driver's print('->') doesn't crash on Windows cp1252.

    All script paths are passed via .as_posix() because the bash on
    Windows interprets backslashes as escape sequences.
    """
    import os as _os

    results = {"VCF": {}, "SAM": {}}
    for sut, fmt in MUTATION_CELLS:
        cell = f"{sut}_{fmt.lower()}"
        out_dir = METRICS_ROOT / "mutation" / cell
        out_dir.mkdir(parents=True, exist_ok=True)

        # Skip cells that already have a valid summary.json (from a prior
        # rerun). Saves time on Docker-heavy htsjdk/biopython runs.
        existing_summary = out_dir / "summary.json"
        if existing_summary.exists():
            try:
                results[fmt][cell] = json.loads(existing_summary.read_text(encoding="utf-8"))
                _log(f"mutation: {cell} -- skipped (existing summary.json)")
                continue
            except (json.JSONDecodeError, OSError):
                pass  # fall through to rerun

        if sut == "htsjdk":
            stage_dir = (
                PROJECT_ROOT / "compares" / "results" / "coverage" / "biotest_E1"
                / f"htsjdk_{fmt.lower()}" / "run_0" / "corpus"
            )
            stage_dir.mkdir(parents=True, exist_ok=True)
            n_staged = 0
            for f in combined_corpora[fmt].iterdir():
                if not f.is_file():
                    continue
                target = stage_dir / f.name
                if not target.exists():
                    try:
                        shutil.copy2(f, target)
                        n_staged += 1
                    except OSError:
                        pass
            _log(f"mutation: {cell} (PIT) -- staged {n_staged} new files at {stage_dir}")

            script = _msys_path(
                PROJECT_ROOT / "compares" / "scripts" / "phase3_jazzer_pit.sh"
            )
            local_bin = _msys_path(E1_ROOT / "bin")
            pit_dir = _msys_path(E1_ROOT / "bin" / "pit")
            cmd = [_bash_exe(), script]
            env = {
                **_os.environ,
                # Prepend our project-local bin so the script's
                # `python3.12 ...` invocations resolve to a shim.
                "PATH": local_bin + ":" + _os.environ.get("PATH", ""),
                # PIT JARs were extracted from biotest-bench:/opt/pit
                # to bin/pit/ — point the script there instead of the
                # absent host-side /opt/pit.
                "PIT_DIR": pit_dir,
                "TOOL": "biotest_E1",
                "REPS": "0",
                "FORMATS": fmt,
                "OUT_ROOT": _msys_path(METRICS_ROOT / "mutation"),
                "COVERAGE_ROOT": _msys_path(
                    PROJECT_ROOT / "compares" / "results" / "coverage" / "biotest_E1"
                ),
                "CORPUS_MAX": "500",
                "PYTHONIOENCODING": "utf-8",
            }
            _run_mutation_subproc(cmd, env, out_dir, results, fmt, cell, budget_s)
            continue

        if sut == "biopython":
            # phase3_atheris_biopython.sh expects CORPUS_DIR + OUT_DIR.
            # Both must be in MSYS form so the script's REPO_ROOT-prefix
            # strip (which yields a Docker /work-relative path) works.
            script = _msys_path(
                PROJECT_ROOT / "compares" / "scripts" / "phase3_atheris_biopython.sh"
            )
            cmd = [_bash_exe(), script]
            env = {
                **_os.environ,
                "TOOL": "biotest_E1",
                "BUDGET_S": str(budget_s),
                "CORPUS_DIR": _msys_path(combined_corpora[fmt]),
                "OUT_DIR": _msys_path(out_dir),
                "PYTHONIOENCODING": "utf-8",
            }
            _log(f"mutation: {cell} (atheris/mutmut, budget={budget_s}s)")
            _run_mutation_subproc(cmd, env, out_dir, results, fmt, cell, budget_s)
            continue

        # vcfpy / noodles / seqan3 -> mutation_driver.py
        cmd = [
            "py", "-3.12",
            str(PROJECT_ROOT / "compares" / "scripts" / "mutation_driver.py"),
            "--tool", "biotest",
            "--sut", sut,
            "--format", fmt,
            "--corpus", str(combined_corpora[fmt]),
            "--budget", str(budget_s),
            "--out", str(out_dir),
        ]
        env = {**_os.environ, "PYTHONIOENCODING": "utf-8"}
        _log(f"mutation: {cell} (mutation_driver, budget={budget_s}s)")
        _run_mutation_subproc(cmd, env, out_dir, results, fmt, cell, budget_s)

    return results


def _run_mutation_subproc(cmd, env, out_dir, results, fmt, cell, budget_s):
    """Shared subprocess + summary collection for all three mutation backends."""
    try:
        r = subprocess.run(
            cmd, cwd=str(PROJECT_ROOT), env=env,
            timeout=budget_s + 1800,
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        (out_dir / "stdout.txt").write_text(r.stdout, encoding="utf-8", errors="replace")
        (out_dir / "stderr.txt").write_text(r.stderr, encoding="utf-8", errors="replace")
        summary = out_dir / "summary.json"
        if summary.exists():
            results[fmt][cell] = json.loads(summary.read_text(encoding="utf-8"))
        else:
            results[fmt][cell] = {
                "status": "no_summary",
                "exit_code": r.returncode,
                "stderr_tail": r.stderr[-500:],
            }
    except subprocess.TimeoutExpired:
        results[fmt][cell] = {"error": "timeout"}
    except Exception as e:
        results[fmt][cell] = {"error": str(e)}


# ---------------------------------------------------------------------------
# Step 4 — Bug bench
# ---------------------------------------------------------------------------

def step_bug_bench(
    combined_corpora: dict[str, Path],
    budget_s: int,
) -> dict:
    out_dir = METRICS_ROOT / "bug_bench"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = PROJECT_ROOT / "compares" / "bug_bench" / "manifest.json"
    if not manifest.exists():
        return {"error": f"manifest missing: {manifest}"}

    cmd = [
        "py", "-3.12",
        str(PROJECT_ROOT / "compares" / "scripts" / "bug_bench_driver.py"),
        "--manifest", str(manifest),
        "--out", str(out_dir),
        "--time-budget-s", str(budget_s),
        "--seed-corpus-vcf", str(combined_corpora["VCF"]),
        "--seed-corpus-sam", str(combined_corpora["SAM"]),
        "--only-tool", "biotest",
    ]
    _log(f"bug_bench: --only-tool biotest, budget={budget_s}s/bug")
    try:
        r = subprocess.run(
            cmd, cwd=str(PROJECT_ROOT),
            timeout=budget_s * 200,
            capture_output=True, text=True,
        )
        (out_dir / "stdout.txt").write_text(r.stdout)
        (out_dir / "stderr.txt").write_text(r.stderr)
        return {"exit_code": r.returncode, "out_dir": str(out_dir)}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def write_summary(metrics: dict) -> None:
    out = METRICS_ROOT / "SUMMARY.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# E1 Metrics Summary",
        "",
        "Generated by `compares/ApplicationStudy/E1_no_phase_a/run_metrics.py`.",
        "",
        f"E1 results root: `{RESULTS_ROOT}`",
        "",
    ]

    for fmt in ("VCF", "SAM"):
        lines += [f"## {fmt}", ""]

        if "validity" in metrics:
            lines += ["### Validity Ratio", ""]
            for sut, data in metrics["validity"].get(fmt, {}).items():
                if isinstance(data, dict) and "validity_ratio" in data:
                    ps = data.get("parse_success", "?")
                    tot = data.get("generated_total", "?")
                    lines.append(f"- **{sut}**: {data['validity_ratio']:.3f} ({ps}/{tot})")
                else:
                    lines.append(f"- **{sut}**: ❌ {data}")
            lines.append("")

        if "coverage" in metrics:
            cov = metrics["coverage"].get(fmt, {})
            lines += [
                "### Coverage Artifacts",
                f"- coverage_dir: `{cov.get('coverage_dir', 'n/a')}`",
                f"- artifact_count: {cov.get('artifact_count', 'n/a')}",
                f"- total_bytes: {cov.get('total_bytes', 'n/a')}",
                "",
            ]

        if "mutation" in metrics:
            lines += ["### Mutation Score", ""]
            for cell, data in metrics["mutation"].get(fmt, {}).items():
                if isinstance(data, dict) and "score" in data:
                    k = data.get("killed", "?")
                    r = data.get("reachable", "?")
                    lines.append(f"- **{cell}**: {data['score']} ({k}/{r})")
                else:
                    lines.append(f"- **{cell}**: ❌ {data}")
            lines.append("")

    if "bug_bench" in metrics:
        lines += ["## Bug Bench", ""]
        lines.append(f"- {metrics['bug_bench']}")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    _log(f"SUMMARY -> {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="E1 metrics runner")
    p.add_argument("--skip-validity", action="store_true")
    p.add_argument("--skip-coverage", action="store_true")
    p.add_argument("--skip-mutation", action="store_true")
    p.add_argument("--skip-bug-bench", action="store_true")
    p.add_argument("--no-precheck", action="store_true",
                   help="Skip checking ===VCF DONE=== / ===SAM DONE=== markers")
    p.add_argument("--mutation-budget-s", type=int, default=7200,
                   help="Per-cell mutation budget in seconds (default 7200 = 2h)")
    p.add_argument("--bug-bench-budget-s", type=int, default=1800,
                   help="Per-bug bug_bench budget in seconds (default 1800 = 30m)")
    args = p.parse_args()

    if not args.no_precheck:
        ok, msg = _check_e1_done()
        if not ok:
            _log(f"PRECHECK FAILED: {msg}")
            return 1
        _log(f"precheck: {msg}")

    METRICS_ROOT.mkdir(parents=True, exist_ok=True)

    combined = {
        "VCF": _build_combined_corpus("VCF"),
        "SAM": _build_combined_corpus("SAM"),
    }

    metrics: dict = {}

    if not args.skip_validity:
        _log("=== STEP: validity ===")
        metrics["validity"] = step_validity(combined)

    if not args.skip_coverage:
        _log("=== STEP: coverage ===")
        metrics["coverage"] = step_coverage()

    if not args.skip_mutation:
        _log("=== STEP: mutation ===")
        metrics["mutation"] = step_mutation(combined, args.mutation_budget_s)

    if not args.skip_bug_bench:
        _log("=== STEP: bug_bench ===")
        metrics["bug_bench"] = step_bug_bench(combined, args.bug_bench_budget_s)

    (METRICS_ROOT / "metrics.json").write_text(
        json.dumps(metrics, indent=2, default=str, ensure_ascii=False)
    )
    write_summary(metrics)
    _log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
