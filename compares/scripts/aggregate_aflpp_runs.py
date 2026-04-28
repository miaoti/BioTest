"""Aggregate 4 invocations of AFL++ × seqan3 Phase-2 (coverage) and
Phase-3 (mutation) into side-by-side mean ± std tables + a pair of
JSON / CSV summary files that the existing MD reports can link to.

Invokes:
    py -3.12 compares/scripts/aggregate_aflpp_runs.py

Reads each `invocation_<i>/summary.json` under
`compares/results/coverage/aflpp/seqan3/` and
`compares/results/mutation/aflpp/seqan3/`, writes:

    compares/results/coverage/aflpp/seqan3/aggregate_4runs.json
    compares/results/coverage/aflpp/seqan3/aggregate_4runs.csv
    compares/results/mutation/aflpp/seqan3/aggregate_4runs.json
    compares/results/mutation/aflpp/seqan3/aggregate_4runs.csv

`std` is the **sample** standard deviation (ddof=1) — what you want
for "how precise is the mean across independent runs" style reporting.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COV_DIR = REPO_ROOT / "compares" / "results" / "coverage" / "aflpp" / "seqan3"
MUT_DIR = REPO_ROOT / "compares" / "results" / "mutation" / "aflpp" / "seqan3"
INVOCATIONS = (1, 2, 3, 4)


def _stats(xs: list[float]) -> dict[str, float]:
    if not xs:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "n": 0}
    mean = statistics.fmean(xs)
    std = statistics.stdev(xs) if len(xs) > 1 else 0.0
    return {"mean": round(mean, 3), "std": round(std, 3),
            "min": round(min(xs), 3), "max": round(max(xs), 3),
            "n": len(xs)}


def aggregate_coverage() -> dict:
    per_inv_per_tick = {t: [] for t in (1, 10, 60)}
    per_inv_per_tick_branch = {t: [] for t in (1, 10, 60)}
    per_inv_means = []
    all_reps_per_tick_line = {t: [] for t in (1, 10, 60)}
    all_reps_per_tick_branch = {t: [] for t in (1, 10, 60)}

    inv_rows = []
    for i in INVOCATIONS:
        summary = COV_DIR / f"invocation_{i}" / "summary.json"
        d = json.loads(summary.read_text(encoding="utf-8"))
        # Per-invocation per-tick mean (across 3 reps).
        by_tick = {}
        for g in d["coverage_growth_aggregate"]:
            by_tick[g["t_s"]] = g
        inv_final = by_tick[60]
        per_inv_means.append(inv_final["line_pct_mean"])
        inv_rows.append({
            "invocation": i,
            "line_pct_t1_mean": by_tick[1]["line_pct_mean"],
            "line_pct_t10_mean": by_tick[10]["line_pct_mean"],
            "line_pct_t60_mean": by_tick[60]["line_pct_mean"],
            "branch_pct_t1_mean": by_tick[1]["branch_pct_mean"],
            "branch_pct_t10_mean": by_tick[10]["branch_pct_mean"],
            "branch_pct_t60_mean": by_tick[60]["branch_pct_mean"],
            "reps": 3,
        })
        for t in (1, 10, 60):
            per_inv_per_tick[t].append(by_tick[t]["line_pct_mean"])
            per_inv_per_tick_branch[t].append(by_tick[t]["branch_pct_mean"])

        # Also pull all 3 reps from each growth_<i>.json so we can
        # report the total-12-rep aggregate as well.
        for rep_idx in range(3):
            g = json.loads((COV_DIR / f"invocation_{i}" /
                            f"growth_{rep_idx}.json").read_text(encoding="utf-8"))
            for tick_rec in g["coverage_growth"]:
                t_s = tick_rec["t_s"]
                if t_s in all_reps_per_tick_line:
                    all_reps_per_tick_line[t_s].append(tick_rec["line_pct"])
                    all_reps_per_tick_branch[t_s].append(tick_rec["branch_pct"])

    agg_invocation_level = {
        t: {
            "line_pct": _stats(per_inv_per_tick[t]),
            "branch_pct": _stats(per_inv_per_tick_branch[t]),
        }
        for t in (1, 10, 60)
    }
    agg_rep_level = {
        t: {
            "line_pct": _stats(all_reps_per_tick_line[t]),
            "branch_pct": _stats(all_reps_per_tick_branch[t]),
        }
        for t in (1, 10, 60)
    }

    out = {
        "tool": "aflpp", "sut": "seqan3", "format": "SAM",
        "phase": "coverage",
        "invocations": INVOCATIONS,
        "reps_per_invocation": 3,
        "per_invocation": inv_rows,
        "aggregate_invocation_level": agg_invocation_level,
        "aggregate_rep_level": agg_rep_level,
    }
    (COV_DIR / "aggregate_4runs.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")

    # CSV: flat view for report ingestion.
    with (COV_DIR / "aggregate_4runs.csv").open("w", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["level", "t_s", "metric", "mean", "std", "min", "max", "n"])
        for t in (1, 10, 60):
            for metric, key in (("line_pct", "line_pct"),
                                ("branch_pct", "branch_pct")):
                s = agg_invocation_level[t][key]
                w.writerow(["invocation", t, metric, s["mean"], s["std"],
                            s["min"], s["max"], s["n"]])
                s = agg_rep_level[t][key]
                w.writerow(["rep", t, metric, s["mean"], s["std"],
                            s["min"], s["max"], s["n"]])
    return out


def aggregate_mutation() -> dict:
    rows = []
    scores = []
    killed_list = []
    for i in INVOCATIONS:
        d = json.loads((MUT_DIR / f"invocation_{i}" / "summary.json")
                       .read_text(encoding="utf-8"))
        rows.append({
            "invocation": i,
            "mutants_generated": d["mutants_generated"],
            "compile_failed": d["compile_failed"],
            "reachable": d["reachable"],
            "killed": d["killed"],
            "survived": d["survived"],
            "score": d["score"],
        })
        scores.append(d["score"])
        killed_list.append(d["killed"])

    agg_score = _stats(scores)
    agg_killed = _stats([float(x) for x in killed_list])
    out = {
        "tool": "aflpp", "sut": "seqan3", "format": "SAM",
        "phase": "mutation",
        "invocations": INVOCATIONS,
        "per_invocation": rows,
        "aggregate": {
            "score": agg_score,
            "killed": agg_killed,
            "reachable": rows[0]["reachable"],   # same across invocations
            "compile_failed": rows[0]["compile_failed"],
        },
    }
    (MUT_DIR / "aggregate_4runs.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")

    with (MUT_DIR / "aggregate_4runs.csv").open("w", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["invocation", "mutants_generated", "compile_failed",
                    "reachable", "killed", "survived", "score"])
        for r in rows:
            w.writerow([r["invocation"], r["mutants_generated"], r["compile_failed"],
                        r["reachable"], r["killed"], r["survived"], r["score"]])
        w.writerow([])
        w.writerow(["aggregate", "metric", "mean", "std", "min", "max", "n"])
        w.writerow(["", "score", agg_score["mean"], agg_score["std"],
                    agg_score["min"], agg_score["max"], agg_score["n"]])
        w.writerow(["", "killed", agg_killed["mean"], agg_killed["std"],
                    agg_killed["min"], agg_killed["max"], agg_killed["n"]])
    return out


def _fmt(s: dict[str, float]) -> str:
    return f"{s['mean']:.3f} ± {s['std']:.3f}"


def main() -> int:
    cov = aggregate_coverage()
    mut = aggregate_mutation()
    print("=== COVERAGE (4 invocations × 3 reps = 12 total reps) ===")
    for i in cov["per_invocation"]:
        print(f"  inv {i['invocation']}: t60 line={i['line_pct_t60_mean']:.3f}%  "
              f"branch={i['branch_pct_t60_mean']:.3f}%")
    for t in (1, 10, 60):
        s = cov["aggregate_invocation_level"][t]
        print(f"  t={t}s invocation-level: line {_fmt(s['line_pct'])}%  "
              f"branch {_fmt(s['branch_pct'])}%  (n={s['line_pct']['n']})")
    for t in (1, 10, 60):
        s = cov["aggregate_rep_level"][t]
        print(f"  t={t}s rep-level:        line {_fmt(s['line_pct'])}%  "
              f"branch {_fmt(s['branch_pct'])}%  (n={s['line_pct']['n']})")
    print()
    print("=== MUTATION (4 invocations × 20 mutants, fixed mutant set) ===")
    for r in mut["per_invocation"]:
        print(f"  inv {r['invocation']}: killed={r['killed']}/{r['reachable']}  "
              f"score={r['score']:.4f}")
    s = mut["aggregate"]["score"]
    ks = mut["aggregate"]["killed"]
    print(f"  score  mean ± std: {_fmt(s)}  (min {s['min']:.4f} max {s['max']:.4f})")
    print(f"  killed mean ± std: {_fmt(ks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
