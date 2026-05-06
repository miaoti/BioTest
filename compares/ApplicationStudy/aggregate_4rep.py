"""Aggregate per-rep coverage + mutation + bug_bench across E0/E1S/E2.

Output: compares/ApplicationStudy/SUMMARY_4rep.md with E0 vs E1S vs E2
mean ± std table per metric per cell.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]

CELLS = [
    ("htsjdk", "VCF"), ("vcfpy", "VCF"), ("noodles", "VCF"),
    ("htsjdk", "SAM"), ("biopython", "SAM"), ("seqan3", "SAM"),
]

CONFIGS = [
    ("E0",  "E0_baseline",   "results_4big_runs", ["a", "b", "c", "d"], "big"),
    ("E1S", "E1S_strict",    "results_4big_runs", ["a", "b", "c", "d"], "big"),
    ("E2",  "E2_no_phase_d", "results_4rep",      [0, 1, 2, 3],         "rep"),
    ("E3",  "E3_no_a_no_d",  "results_4rep",      [0, 1, 2, 3],         "rep"),
]


def _rep_value(d):
    """Map a measurement.json dict to a coverage data point.

    Methodology: distinguish two failure modes.

    A) `status=="missing"` AND total==0 — investigated empirically: this
       is always the result of Phase B mining 0 valid MRs under the
       ablation (no Phase A → LLM emits empty arrays / Pydantic errors).
       Phase C runs 0 tests, the SUT under test never gets executed, so
       JaCoCo / coverage.py / gcovr capture nothing. This IS the legitimate
       ablation signal: the tool produced 0 useful tests, hence 0 coverage.
       Counted as line_pct=0.0 with full weight.

    B) `status=="ok"` AND total>0 AND line_pct>=0 — normal measurement,
       use line_pct as-is (including line_pct==0 cases which mean "the SUT
       binary ran but the corpus didn't exercise instrumented code", e.g.
       seqan3 cumulative=False .gcda race).

    Anything else (corrupt JSON, status=="convert_failed", etc.) is
    excluded by returning None; caller treats it as missing rep."""
    if d is None:
        return None
    status = d.get("status")
    total = d.get("total", 0)
    if status == "ok":
        return d.get("line_pct", 0.0)
    if status == "missing":
        # Genuine ablation outcome — tool produced no tests, no coverage.
        return 0.0
    return None


def _coverage_data(config_name, sub, results_root, ids, layout):
    """For each cell, return list[float] of per-run mean coverage (big runs)
    or per-rep coverage (E2)."""
    out = {}
    for sut, fmt in CELLS:
        cell = f"{sut}_{fmt.lower()}"
        per_run = []
        for run_id in ids:
            if layout == "big":
                # Per-big-run mean across 3 reps
                rep_vals = []
                for rep in range(3):
                    m = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                         results_root / f"run_{run_id}" / cell / f"run_{rep}" / "measurement.json")
                    if not m.exists():
                        continue
                    try:
                        d = json.loads(m.read_text())
                    except Exception:
                        continue
                    v = _rep_value(d)
                    if v is not None:
                        rep_vals.append(v)
                if rep_vals:
                    per_run.append(statistics.mean(rep_vals))
            else:
                # E2/E3 — single rep per id
                m = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                     results_root / cell / f"run_{run_id}" / "measurement.json")
                if not m.exists():
                    continue
                try:
                    d = json.loads(m.read_text())
                except Exception:
                    continue
                v = _rep_value(d)
                if v is not None:
                    per_run.append(v)
        out[cell] = per_run
    return out


def _mutation_data(config_name, sub, ids):
    """For each cell, return list[float] of per-run mutation score."""
    out = {}
    for sut, fmt in CELLS:
        if sut in ("pysam", "htslib", "reference"):
            continue
        cell = f"{sut}_{fmt.lower()}"
        per_run = []
        for run_id in ids:
            m = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                 "results_metrics" / f"{run_id}" / cell / "summary.json")
            if not m.exists():
                continue
            d = json.loads(m.read_text())
            score = d.get("score") if "score" in d else d.get("mutation_score", {}).get("score")
            if score is not None:
                per_run.append(score * 100)  # to pct
        out[cell] = per_run
    return out


def _bug_bench_data(config_name, sub, ids):
    """For each run, count detected bugs."""
    out = []
    for run_id in ids:
        agg = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
               "results_metrics" / f"{run_id}" / "bug_bench" / "aggregate.json")
        if not agg.exists():
            continue
        d = json.loads(agg.read_text())
        results = d.get("results", []) if isinstance(d, dict) else d
        if isinstance(results, list):
            detected = sum(1 for r in results if r.get("detected"))
            attempted = sum(1 for r in results if not (r.get("install_error")
                                                       or "install" in (r.get("notes", "") or "").lower()))
            rate = (detected / attempted * 100) if attempted else 0
            out.append({"detected": detected, "attempted": attempted, "rate": rate})
    return out


def _stats(vals):
    if not vals:
        return None, None, 0
    if len(vals) == 1:
        return vals[0], 0.0, 1
    return statistics.mean(vals), statistics.stdev(vals), len(vals)


def main():
    cov = {}
    mut = {}
    bug = {}
    for label, sub, results_root, ids, layout in CONFIGS:
        cov[label] = _coverage_data(label, sub, results_root, ids, layout)
        mut[label] = _mutation_data(label, sub, ids)
        bug[label] = _bug_bench_data(label, sub, ids)

    lines = ["# 4-Rep Application Study — E0 vs E1S vs E2 SUMMARY", ""]
    lines.append("Generated by `compares/ApplicationStudy/aggregate_4rep.py`.")
    lines.append("")
    lines.append("E0 = full BioTest (Phase A RAG + Phase D loop)")
    lines.append("E1S = no Phase A (minimal LLM prompt, no spec content anywhere)")
    lines.append("E2 = no Phase D (single-shot B+C+E, RAG enabled)")
    lines.append("E3 = no Phase A AND no Phase D (E1S + E2 patches combined)")
    lines.append("")
    lines.append("E0/E1S used 4 big runs × 3 reps cumulative=True; per-big-run score = mean(3 reps).")
    lines.append("E2 used 4 reps cumulative=False (each rep independent).")
    lines.append("All cells use 5400s wall budget per rep, internal feedback_control.timeout_minutes=60.")
    lines.append("")

    # Coverage table
    lines += ["## Line Coverage (mean ± std across 4 runs)", ""]
    lines.append("| Cell | E0 | E1S | E2 |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for sut, fmt in CELLS:
        cell = f"{sut}_{fmt.lower()}"
        row = [f"| **{cell}** |"]
        for label, *_ in CONFIGS:
            mean, std, n = _stats(cov[label].get(cell, []))
            if mean is None:
                row.append(" no data |")
            else:
                row.append(f" **{mean:.2f}%** ± {std:.2f}pp (n={n}) |")
        lines.append("".join(row))
    lines.append("")

    # Mutation table
    lines += ["## Mutation Score (mean ± std across 4 runs)", ""]
    lines.append("| Cell | E0 | E1S | E2 |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for sut, fmt in CELLS:
        cell = f"{sut}_{fmt.lower()}"
        row = [f"| **{cell}** |"]
        for label, *_ in CONFIGS:
            mean, std, n = _stats(mut[label].get(cell, []))
            if mean is None:
                row.append(" no data |")
            else:
                row.append(f" **{mean:.2f}%** ± {std:.2f}pp (n={n}) |")
        lines.append("".join(row))
    lines.append("")

    # Bug bench table
    lines += ["## Real-Bug Detection Rate (per run)", ""]
    lines.append("| Run idx | E0 | E1S | E2 |")
    lines.append("| :--- | :--- | :--- | :--- |")
    max_len = max(len(bug.get(label, [])) for label, *_ in CONFIGS)
    for i in range(max_len):
        row = [f"| run {i} |"]
        for label, *_ in CONFIGS:
            entries = bug.get(label, [])
            if i < len(entries):
                e = entries[i]
                row.append(f" {e['detected']}/{e['attempted']} ({e['rate']:.1f}%) |")
            else:
                row.append(" — |")
        lines.append("".join(row))
    # Mean
    row = ["| **mean** |"]
    for label, *_ in CONFIGS:
        rates = [e["rate"] for e in bug.get(label, [])]
        mean, std, n = _stats(rates)
        if mean is None:
            row.append(" no data |")
        else:
            row.append(f" **{mean:.1f}%** ± {std:.2f} (n={n}) |")
    lines.append("".join(row))
    lines.append("")

    out = ROOT / "SUMMARY_4rep.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"SUMMARY_4rep -> {out}")


if __name__ == "__main__":
    main()
