#!/usr/bin/env python3
"""Aggregate VCF coverage stats across 4 big runs.

Each big run has 4 small reps (0-3). Per-big-run mean = mean of small reps.
Cross-big-run std = std of the 4 big-run means (n=4, sample std with ddof=1).

Outputs a SUMMARY-style markdown table comparing the 4 big runs.

Usage:
    py -3.12 compares/scripts/aggregate_4bigrun_vcf_stats.py [-o SUMMARY_VCF_4bigrun.md]
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COVERAGE_ROOT = REPO_ROOT / "compares" / "results" / "coverage"

BIG_RUNS = [
    ("run1", "biotest_4rep_cascade_20260427"),
    ("run2", "biotest_4rep_cascade_run2_20260429"),
    ("run3", "biotest_4rep_cascade_run3_20260429"),
    ("run4", "biotest_4rep_cascade_run4_20260429"),
]
CELLS = ["htsjdk_vcf", "vcfpy_vcf", "noodles_vcf"]
REPS = [0, 1, 2, 3]


def load_rep_line_pct(out_root: Path, cell: str, rep: int) -> float | None:
    f = out_root / cell / f"run_{rep}" / "measurement.json"
    if not f.exists():
        return None
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return None
    if d.get("status") != "ok":
        return None
    pct = d.get("line_pct")
    if pct is None:
        return None
    try:
        return float(pct)
    except Exception:
        return None


def big_run_mean(out_root: Path, cell: str) -> tuple[float | None, list]:
    pcts = []
    rep_records = []
    for rep in REPS:
        v = load_rep_line_pct(out_root, cell, rep)
        rep_records.append({"rep": rep, "line_pct": v})
        if v is not None:
            pcts.append(v)
    if not pcts:
        return None, rep_records
    return sum(pcts) / len(pcts), rep_records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--out", type=Path,
        default=COVERAGE_ROOT / "SUMMARY_VCF_4bigrun.md",
        help="Output markdown path",
    )
    args = ap.parse_args()

    rows: dict[str, dict] = {}
    for cell in CELLS:
        rows[cell] = {"means": {}, "reps": {}}

    for run_key, run_dir in BIG_RUNS:
        out_root = COVERAGE_ROOT / run_dir
        for cell in CELLS:
            mean, reps = big_run_mean(out_root, cell)
            rows[cell]["means"][run_key] = mean
            rows[cell]["reps"][run_key] = reps

    md = []
    md.append("# BioTest 4-big-run VCF coverage — SUMMARY")
    md.append("")
    md.append("- Each big run = 4 small reps (rep 0 fresh, reps 1-3 cascade-from-prev)")
    md.append("- 6 SUTs in DESIGN.md but this analysis focuses on the **3 VCF cells only**")
    md.append("- LLM: deepseek-chat (forced via per-cell config override)")
    md.append("- Phase D (which internally runs B+C with coverage)")
    md.append("- Per-big-run mean = arithmetic mean of small reps' line%")
    md.append("- Cross-big-run std (n=4) = sample std of the 4 big-run means")
    md.append("")
    md.append("## Big-run means (line %)")
    md.append("")
    md.append("| Cell           | Run 1  | Run 2  | Run 3  | Run 4  | Mean(4)  | Std(4) |")
    md.append("|----------------|-------:|-------:|-------:|-------:|---------:|-------:|")
    for cell in CELLS:
        means_dict = rows[cell]["means"]
        cells_vals = [
            f"{means_dict.get(r):.2f}" if means_dict.get(r) is not None else "  --  "
            for r in ("run1", "run2", "run3", "run4")
        ]
        valid = [v for v in means_dict.values() if v is not None]
        agg_mean = statistics.mean(valid) if valid else None
        agg_std = statistics.stdev(valid) if len(valid) >= 2 else None
        agg_mean_s = f"{agg_mean:.2f}" if agg_mean is not None else "  --  "
        agg_std_s = f"{agg_std:.2f}" if agg_std is not None else "  --  "
        md.append(f"| {cell:<14} | {cells_vals[0]:>6} | {cells_vals[1]:>6} | {cells_vals[2]:>6} | {cells_vals[3]:>6} | {agg_mean_s:>8} | {agg_std_s:>6} |")
    md.append("")
    md.append("## Per-big-run × per-rep matrix (line %)")
    md.append("")
    md.append("Rep numbers in column header. Each cell shows line% (status=ok), or `--` if status was missing/empty.")
    md.append("")
    for cell in CELLS:
        md.append(f"### {cell}")
        md.append("")
        md.append("| Big run | rep 0  | rep 1  | rep 2  | rep 3  | mean   |")
        md.append("|---------|-------:|-------:|-------:|-------:|-------:|")
        for run_key, _ in BIG_RUNS:
            reps = rows[cell]["reps"].get(run_key, [])
            cells_vals = []
            for rep in REPS:
                v = next((r["line_pct"] for r in reps if r["rep"] == rep), None)
                cells_vals.append(f"{v:.2f}" if v is not None else "  --  ")
            mean = rows[cell]["means"].get(run_key)
            mean_s = f"{mean:.2f}" if mean is not None else "  --  "
            md.append(f"| {run_key:<7} | {cells_vals[0]:>6} | {cells_vals[1]:>6} | {cells_vals[2]:>6} | {cells_vals[3]:>6} | {mean_s:>6} |")
        md.append("")
    md.append("## Source dirs")
    md.append("")
    for run_key, run_dir in BIG_RUNS:
        md.append(f"- **{run_key}**: `compares/results/coverage/{run_dir}/`")
    md.append("")
    md.append("## Methodology notes")
    md.append("")
    md.append("- Each big run starts FRESH (no cascade across big runs).")
    md.append("- Within a big run, rep N inherits rep N-1's seed corpus (`kept_*`/`synthetic_*` accumulate).")
    md.append("- All 4 big runs use the same protocol: `max_iterations=2`, 5400s wall cap per rep.")
    md.append("- vcfpy_vcf reps that hit Windows `TerminateProcess` at the wall cap (status=missing) are recovered with `max_iter=1` against the cascaded seed corpus, matching run 1's recovery protocol.")
    md.append("- htsjdk_vcf and noodles_vcf cells reliably produce `status=ok` measurements without recovery.")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
