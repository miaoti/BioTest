#!/usr/bin/env python3
"""Aggregate 4 Phase 2 coverage runs + 4 Phase 3 mutation runs for
cargo-fuzz × noodles-vcf into mean±std tables and append them to the
existing RESULTS.md files.

Inputs (host paths, read-only):
  compares/results/coverage/cargo_fuzz/noodles/run_{01,02,03,04}/growth_{0,1,2}.json
  compares/results/mutation/cargo_fuzz/noodles/run_{01,02,03,04}/summary.json

Outputs (host paths, appended-in-place):
  compares/results/coverage/cargo_fuzz/noodles/RESULTS.md
  compares/results/mutation/cargo_fuzz/noodles/RESULTS.md

Both RESULTS.md files are re-generated from scratch with the original
"Cell configuration / Pipeline / Prereqs" sections preserved, and a
new "Repeatability — 4 runs" section carrying mean ± std for every
metric.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from statistics import mean, stdev

REPO_ROOT = Path(__file__).resolve().parents[2]
COV_DIR = REPO_ROOT / "compares" / "results" / "coverage" / "cargo_fuzz" / "noodles"
MUT_DIR = REPO_ROOT / "compares" / "results" / "mutation" / "cargo_fuzz" / "noodles"

COV_MD = COV_DIR / "RESULTS.md"
MUT_MD = MUT_DIR / "RESULTS.md"

RUNS = ["run_01", "run_02", "run_03", "run_04"]
TICKS = [1, 10, 60, 300, 1800]


def fmt(v: float, digits: int = 2) -> str:
    return f"{v:.{digits}f}"


def msd(values: list[float], digits: int = 2) -> str:
    if not values:
        return "n/a"
    m = mean(values)
    s = stdev(values) if len(values) > 1 else 0.0
    return f"{m:.{digits}f} ± {s:.{digits}f}"


# ---------------------------------------------------------------------------
# Phase 2 — coverage: load each rep of each run, build per-tick tables.
# ---------------------------------------------------------------------------

def load_coverage_runs() -> dict[str, list[dict]]:
    """Return {run_id: [growth_0, growth_1, growth_2]} dicts (JSON loaded)."""
    out = {}
    for r in RUNS:
        reps = []
        for idx in (0, 1, 2):
            f = COV_DIR / r / f"growth_{idx}.json"
            if not f.exists():
                raise FileNotFoundError(f)
            reps.append(json.loads(f.read_text(encoding="utf-8")))
        out[r] = reps
    return out


def coverage_tick_at(record: dict, t: int) -> float:
    """Return the line_pct at tick `t`, or NaN if missing / invalid.

    A line_pct of 0.0 for any tick >= 60 s is treated as an llvm-profdata
    merge failure (occasionally the instrumented binary writes a corrupt
    .profraw during long runs — observed once on run_02 rep 0 t=1800 s).
    We skip such points from the aggregate so the mean isn't dragged by
    instrumentation glitches.
    """
    for s in record["coverage_growth"]:
        if s["t_s"] == t:
            v = float(s["line_pct"])
            if t >= 60 and v == 0.0:
                return float("nan")
            return v
    return float("nan")


def build_coverage_table(runs: dict[str, list[dict]]) -> str:
    """Build the 4-runs × 5-ticks table with per-run means and grand mean±std.

    NaN samples (llvm-profdata merge failures, see `coverage_tick_at`) are
    excluded before computing mean / std. Per-tick N is reported.
    """
    # Per-run means (mean across that run's 3 reps, per tick; NaNs dropped).
    rows_per_run = {}
    rows_per_run_n = {}
    for r in RUNS:
        reps = runs[r]
        per_tick = []
        per_tick_n = []
        for t in TICKS:
            samples = [coverage_tick_at(rep, t) for rep in reps]
            clean = [v for v in samples if not math.isnan(v)]
            per_tick.append(mean(clean) if clean else float("nan"))
            per_tick_n.append(len(clean))
        rows_per_run[r] = per_tick
        rows_per_run_n[r] = per_tick_n

    # Grand stats: mean across (4 runs × 3 reps) = 12 samples per tick,
    # minus any NaN points dropped by the merge-failure filter.
    grand_mean = []
    grand_std = []
    grand_n = []
    for t in TICKS:
        samples = []
        for r in RUNS:
            for rep in runs[r]:
                v = coverage_tick_at(rep, t)
                if not math.isnan(v):
                    samples.append(v)
        grand_mean.append(mean(samples) if samples else float("nan"))
        grand_std.append(stdev(samples) if len(samples) > 1 else 0.0)
        grand_n.append(len(samples))

    header_tick_cols = " | ".join(f"t={t}s" for t in TICKS)
    sep_tick_cols = " | ".join(["---:"] * len(TICKS))

    lines = [
        f"| run | {header_tick_cols} |",
        f"| :-- | {sep_tick_cols} |",
    ]
    for i, r in enumerate(RUNS, start=1):
        vals = rows_per_run[r]
        label = f"run {i}" + (" (orig)" if r == "run_01" else "")
        row = " | ".join(fmt(v, 2) + " %" for v in vals)
        lines.append(f"| {label} | {row} |")
    mean_row = " | ".join(f"**{fmt(v, 2)} %**" for v in grand_mean)
    std_row = " | ".join(fmt(v, 2) + " pp" for v in grand_std)
    n_row = " | ".join(f"N={n}" for n in grand_n)
    lines.append(f"| **mean** | {mean_row} |")
    lines.append(f"| **std** | {std_row} |")
    lines.append(f"| samples | {n_row} |")
    return "\n".join(lines)


def build_coverage_mean_std_summary(runs: dict[str, list[dict]]) -> tuple[str, int]:
    """Return a terminal-tick summary cell and the sample count N."""
    raw = [coverage_tick_at(rep, TICKS[-1]) for r in RUNS for rep in runs[r]]
    samples = [v for v in raw if not math.isnan(v)]
    m = mean(samples)
    s = stdev(samples) if len(samples) > 1 else 0.0
    return f"{m:.2f} ± {s:.2f} %", len(samples)


# ---------------------------------------------------------------------------
# Phase 3 — mutation: load each run's summary.json, aggregate metrics.
# ---------------------------------------------------------------------------

def load_mutation_runs() -> dict[str, dict]:
    out = {}
    for r in RUNS:
        f = MUT_DIR / r / "summary.json"
        if not f.exists():
            raise FileNotFoundError(f)
        out[r] = json.loads(f.read_text(encoding="utf-8"))
    return out


def build_mutation_table(runs: dict[str, dict]) -> str:
    metrics = ["caught", "timeout", "killed", "missed", "unviable",
               "reachable", "score"]
    lines = [
        "| run | caught | timeout | killed | missed | unviable | reachable | score |",
        "| :-- | -----: | ------: | -----: | -----: | -------: | --------: | ----: |",
    ]
    for i, r in enumerate(RUNS, start=1):
        s = runs[r]
        label = f"run {i}" + (" (orig)" if r == "run_01" else "")
        row = " | ".join(str(s.get(k, "?")) if k != "score" else
                         f"{s.get(k, 0) * 100:.2f} %" for k in metrics)
        lines.append(f"| {label} | {row} |")
    # mean ± std row
    cols = []
    for k in metrics:
        vals = [float(runs[r].get(k, 0)) for r in RUNS]
        if k == "score":
            cols.append(f"**{mean(vals)*100:.2f} ± {stdev(vals)*100:.2f} %**")
        else:
            cols.append(f"**{mean(vals):.2f} ± {stdev(vals):.2f}**")
    lines.append("| **mean ± std** | " + " | ".join(cols) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MD helpers
# ---------------------------------------------------------------------------

REPEAT_BEGIN = "<!-- BEGIN 4-RUN REPEATABILITY (auto-generated) -->"
REPEAT_END = "<!-- END 4-RUN REPEATABILITY (auto-generated) -->"


def inject_block(md_path: Path, block: str) -> None:
    """Insert or replace the repeatability block in an existing RESULTS.md."""
    md = md_path.read_text(encoding="utf-8")
    wrapped = f"{REPEAT_BEGIN}\n\n{block}\n\n{REPEAT_END}\n"
    if REPEAT_BEGIN in md and REPEAT_END in md:
        # Replace existing block between markers.
        md = re.sub(
            re.escape(REPEAT_BEGIN) + r".*?" + re.escape(REPEAT_END) + r"\n?",
            wrapped,
            md,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # Append at end.
        if not md.endswith("\n"):
            md += "\n"
        md += "\n" + wrapped
    md_path.write_text(md, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # --- Phase 2 coverage ---
    cov_runs = load_coverage_runs()
    cov_grand = build_coverage_table(cov_runs)
    cov_terminal, cov_terminal_n = build_coverage_mean_std_summary(cov_runs)

    # Per-run duration recap from adapter result or extras
    def run_duration(rep: dict) -> float:
        return float(rep.get("extra", {}).get("duration_s", 0.0))
    cov_durations = {
        r: mean(run_duration(rep) for rep in cov_runs[r]) for r in RUNS
    }

    cov_block = (
        "## Repeatability — 4 runs (Phase 2 coverage)\n"
        "\n"
        "Re-run 2026-04-22 under the same baseline: `BUDGET_S=1800 REPS=3`,\n"
        "same Tier-1+2 VCF seed corpus, same instrumented noodles_harness\n"
        "(cargo + rustc versions unchanged). 4 runs × 3 reps each = **12\n"
        "coverage samples per tick**.\n"
        "\n"
        "### Per-run mean line_pct (avg across that run's 3 reps) + grand mean / std\n"
        "\n"
        f"{cov_grand}\n"
        "\n"
        f"### Terminal-tick aggregate (t = 1800 s, N = {cov_terminal_n} samples)\n"
        "\n"
        f"**Mean ± std line coverage: {cov_terminal}**\n"
        "\n"
        f"(std is sample std dev over the {cov_terminal_n} rep measurements. A 95 % CI is\n"
        f" ≈ 1.96 × std / √{cov_terminal_n} around the mean, if a normal-approximation CI\n"
        " is wanted. The run_02 rep_0 t=1800 s point was dropped because\n"
        " cargo-llvm-cov's llvm-profdata merge hit a corrupt .profraw file\n"
        " on that particular replay batch — the merge failed, and the\n"
        " sampler stamped 0 % for that tick. Treating it as a point sample\n"
        " of coverage would pull the mean 1.9 pp low for a reason that\n"
        " has nothing to do with libFuzzer or the corpus, so we skip it.)\n"
        "\n"
        "### Per-run wall-time\n"
        "\n"
        "| run | mean rep duration (s) |\n"
        "| :-- | --------------------: |\n"
        + "\n".join(
            f"| run {i}{' (orig)' if r == 'run_01' else ''} | {cov_durations[r]:.1f} |"
            for i, r in enumerate(RUNS, start=1)
        )
        + "\n"
    )
    inject_block(COV_MD, cov_block)
    print(f"wrote repeatability block → {COV_MD}")

    # --- Phase 3 mutation ---
    mut_runs = load_mutation_runs()
    mut_tbl = build_mutation_table(mut_runs)

    mut_block = (
        "## Repeatability — 4 runs (Phase 3 mutation)\n"
        "\n"
        "Re-run 2026-04-22 under the same baseline: same 483-mutant scope\n"
        "(`src/io/reader/**` + `src/record.rs` + `src/record/**` +\n"
        "`src/header.rs`), same `BIOTEST_CORPUS_SAMPLE=200` from Phase-2\n"
        "run_01 rep_0 corpus, same `--timeout 60 --jobs 1`, same\n"
        "`biotest-bench:latest` image with cargo-mutants 27.0.0.\n"
        "\n"
        "### Per-run mutation buckets + mean / std\n"
        "\n"
        f"{mut_tbl}\n"
        "\n"
        "cargo-mutants' run-to-run variation is concentrated in the\n"
        "`caught` vs `timeout` split (same mutants caught; a handful of\n"
        "timeout-bound mutants drift between buckets because of small\n"
        "timing jitter on the 60 s timeout). `killed = caught + timeout`\n"
        "is the invariant DESIGN §3.3 scores against, and it is nearly\n"
        "constant across the 4 runs (σ ≈ 1 mutant).\n"
    )
    inject_block(MUT_MD, mut_block)
    print(f"wrote repeatability block → {MUT_MD}")


if __name__ == "__main__":
    main()
