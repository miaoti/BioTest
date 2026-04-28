"""Aggregate 4-run tables for the atheris × biopython cell.

Consumes:
  compares/results/coverage/atheris/biopython/growth_{0..3}.json     (Phase 2)
  compares/results/mutation/atheris/biopython/rep_{0..3}_run/summary_scoped.json  (Phase 3)

Emits:
  compares/results/coverage/atheris/biopython/growth_aggregate.json  (4-rep)
  compares/results/mutation/atheris/biopython/summary_aggregate.json (4-run)

Both carry mean + std + per-rep raw values so the results MD files can
table them side-by-side.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import statistics
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
logger = logging.getLogger("aggregate_atheris_biopython")


def _mean_std(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    m = statistics.mean(values)
    if len(values) == 1:
        return m, 0.0
    return m, statistics.stdev(values)


def aggregate_coverage(cell_dir: Path, n_reps: int = 4) -> dict:
    """Aggregate Phase-2 growth_{0..N-1}.json into a mean+std record."""
    per_rep: list[dict] = []
    for i in range(n_reps):
        p = cell_dir / f"growth_{i}.json"
        if not p.exists():
            logger.warning("missing %s (rep %d)", p, i)
            continue
        per_rep.append(json.loads(p.read_text(encoding="utf-8")))
    if not per_rep:
        raise RuntimeError(f"no growth_*.json found under {cell_dir}")

    # Union of tick sets across reps (normal case: all match, but be defensive)
    ticks: list[int] = sorted({
        p["t_s"]
        for rep in per_rep
        for p in rep["coverage_growth"]
    })

    aggregate_rows = []
    for t in ticks:
        lines = [
            p["line_pct"]
            for rep in per_rep
            for p in rep["coverage_growth"]
            if p["t_s"] == t and p.get("line_pct") is not None
        ]
        branches = [
            p["branch_pct"]
            for rep in per_rep
            for p in rep["coverage_growth"]
            if p["t_s"] == t and p.get("branch_pct") is not None
        ]
        lm, lsd = _mean_std(lines)
        bm, bsd = _mean_std(branches)
        n = len(lines)
        ci_l = 1.96 * lsd / math.sqrt(n) if n > 1 else 0.0
        ci_b = 1.96 * bsd / math.sqrt(n) if n > 1 else 0.0
        aggregate_rows.append({
            "t_s": t,
            "line_pct_mean": round(lm, 3),
            "line_pct_std": round(lsd, 3),
            "line_pct_ci_lo": round(lm - ci_l, 3),
            "line_pct_ci_hi": round(lm + ci_l, 3),
            "line_pct_n": n,
            "line_pct_per_rep": lines,
            "branch_pct_mean": round(bm, 3),
            "branch_pct_std": round(bsd, 3),
            "branch_pct_ci_lo": round(bm - ci_b, 3),
            "branch_pct_ci_hi": round(bm + ci_b, 3),
            "branch_pct_n": len(branches),
            "branch_pct_per_rep": branches,
        })

    return {
        "tool": per_rep[0]["tool"],
        "sut": per_rep[0]["sut"],
        "format": per_rep[0]["format"],
        "phase": "coverage",
        "time_budget_s": per_rep[0]["time_budget_s"],
        "reps": len(per_rep),
        "seed_corpus_hash": per_rep[0]["seed_corpus_hash"],
        "ticks": ticks,
        "coverage_growth_aggregate": aggregate_rows,
    }


def aggregate_mutation(cell_dir: Path, n_runs: int = 4) -> dict:
    """Aggregate rep_{0..N-1}_run/summary_scoped.json into mean+std."""
    per_run: list[dict] = []
    for i in range(n_runs):
        p = cell_dir / f"rep_{i}_run" / "summary_scoped.json"
        if not p.exists():
            logger.warning("missing %s (run %d)", p, i)
            continue
        per_run.append(json.loads(p.read_text(encoding="utf-8")))
    if not per_run:
        raise RuntimeError(f"no rep_*_run/summary_scoped.json under {cell_dir}")

    # Scoped (reached-lines-only) scores
    scoped_scores = [r["mutation_score"]["score"] for r in per_run]
    scoped_killed = [r["mutation_score"]["killed"] for r in per_run]
    scoped_survived = [r["mutation_score"]["survived"] for r in per_run]
    scoped_reachable = [r["mutation_score"]["reachable"] for r in per_run]

    full_scores = [r["mutation_score_unfiltered"]["score"] for r in per_run]
    full_killed = [r["mutation_score_unfiltered"]["killed"] for r in per_run]
    full_survived = [r["mutation_score_unfiltered"]["survived"] for r in per_run]
    full_reachable = [r["mutation_score_unfiltered"]["reachable"] for r in per_run]

    baseline_success = [r["baseline"]["parse_success"] for r in per_run]
    baseline_total = [r["baseline"]["total_files"] for r in per_run]

    reached_lines = [r["scope"]["reached_lines"] for r in per_run]
    total_generated = [r["total_generated"] for r in per_run]
    durations = [r["duration_s"] for r in per_run]

    def pack(label: str, vals: list) -> dict:
        mean, std = _mean_std(vals)
        return {
            f"{label}_mean": round(mean, 4),
            f"{label}_std": round(std, 4),
            f"{label}_min": min(vals),
            f"{label}_max": max(vals),
            f"{label}_per_run": vals,
        }

    out = {
        "tool": per_run[0]["tool"],
        "sut": per_run[0]["sut"],
        "format": per_run[0]["format"],
        "phase": "mutation",
        "target": per_run[0]["target"],
        "runs": len(per_run),
        "scoped_scope_description": per_run[0]["scope"]["mode"],
        # Headline: reached-lines scoped scores
        "scoped": {
            **pack("score", scoped_scores),
            **pack("killed", scoped_killed),
            **pack("survived", scoped_survived),
            **pack("reachable", scoped_reachable),
        },
        # Companion: full-file scores
        "full_file": {
            **pack("score", full_scores),
            **pack("killed", full_killed),
            **pack("survived", full_survived),
            **pack("reachable", full_reachable),
        },
        "baseline": {
            **pack("parse_success", baseline_success),
            **pack("total_files", baseline_total),
        },
        "reached_lines": pack("count", reached_lines),
        "total_generated": pack("count", total_generated),
        "duration_s": pack("seconds", durations),
        # Per-run pointer so the MD can cite source files
        "per_run_paths": [
            {"run": i, "corpus": r["corpus_dir"],
             "summary_scoped": str(Path(r["target"]).parent.parent / "MUTATION_RESULTS.md"),
             "baseline_parse_success": r["baseline"]["parse_success"]}
            for i, r in enumerate(per_run)
        ],
    }
    return out


def _cli() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--coverage-cell", type=Path,
                   default=REPO_ROOT / "compares/results/coverage/atheris/biopython")
    p.add_argument("--mutation-cell", type=Path,
                   default=REPO_ROOT / "compares/results/mutation/atheris/biopython")
    p.add_argument("--reps", type=int, default=4)
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # --- Coverage ---
    try:
        cov = aggregate_coverage(args.coverage_cell, n_reps=args.reps)
    except Exception as exc:
        logger.error("coverage aggregate failed: %s", exc)
        cov = None
    if cov:
        out = args.coverage_cell / "growth_aggregate.json"
        out.write_text(json.dumps(cov, indent=2), encoding="utf-8")
        print(f"[aggregate] wrote {out.name} — {cov['reps']}-rep coverage")
        for row in cov["coverage_growth_aggregate"]:
            print(f"  t={row['t_s']:>4}s  "
                  f"line={row['line_pct_mean']:>6.2f}% ± {row['line_pct_std']:>4.2f}  "
                  f"branch={row['branch_pct_mean']:>6.2f}% ± {row['branch_pct_std']:>4.2f}")

    # --- Mutation ---
    try:
        mut = aggregate_mutation(args.mutation_cell, n_runs=args.reps)
    except Exception as exc:
        logger.error("mutation aggregate failed: %s", exc)
        mut = None
    if mut:
        out = args.mutation_cell / "summary_aggregate.json"
        out.write_text(json.dumps(mut, indent=2), encoding="utf-8")
        print(f"\n[aggregate] wrote {out.name} — {mut['runs']}-run mutation")
        s = mut["scoped"]
        f = mut["full_file"]
        print(f"  Scoped score:    mean={s['score_mean']:.4f} ± {s['score_std']:.4f}  "
              f"per-run={s['score_per_run']}")
        print(f"  Full-file score: mean={f['score_mean']:.4f} ± {f['score_std']:.4f}  "
              f"per-run={f['score_per_run']}")
        print(f"  Killed (scoped): mean={s['killed_mean']:.1f} ± {s['killed_std']:.1f}  "
              f"per-run={s['killed_per_run']}")
        print(f"  Reachable:       mean={s['reachable_mean']:.1f} ± {s['reachable_std']:.1f}  "
              f"per-run={s['reachable_per_run']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
