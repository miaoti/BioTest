"""Post-hoc re-grader for `growth_<idx>.json` files under
`compares/results/coverage/<tool>/<cell>/`.

Use this when `coverage_sampler.py` has already landed a set of growth
files but the coverage %'s were computed against stale (hardcoded or
drifted) filter rules. This script walks each `growth_<idx>.json`,
finds the sibling per-tick JaCoCo XML snapshots the sampler left under
`run_<idx>/jacoco_exec/tick_<T>.xml`, and re-computes line + branch %
via `measure_coverage.measure(...)` — i.e. applying
`biotest_config.yaml:coverage.target_filters[<fmt>][<sut>]` (the single
source of truth, see `compares/scripts/README.md`).

The rewrite preserves every other field in the growth JSON (`tool`,
`sut`, `format`, `phase`, `run_index`, `time_budget_s`,
`seed_corpus_hash`, `mutation_score`, `bug_bench`, `extra`) — only
`coverage_growth[i].{line_pct, branch_pct}` changes. An `extra.regrade`
block is appended so the provenance of any re-baselined number is
auditable.

Usage::

    py -3.12 compares/scripts/recompute_growth.py \\
        --growth-dir compares/results/coverage/jazzer/htsjdk_vcf \\
        --sut htsjdk --format VCF

    # Rewrite both Phase-2 Jazzer cells back-to-back:
    for CELL in htsjdk_vcf htsjdk_sam; do
        FMT=$(echo ${CELL##*_} | tr a-z A-Z)
        py -3.12 compares/scripts/recompute_growth.py \\
            --growth-dir compares/results/coverage/jazzer/${CELL} \\
            --sut htsjdk --format ${FMT}
    done

Idempotent — re-running with the same inputs produces the same output.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger("recompute_growth")

_HERE = Path(__file__).resolve().parent
_MC_SPEC = importlib.util.spec_from_file_location(
    "measure_coverage", _HERE / "measure_coverage.py"
)
_measure_coverage = importlib.util.module_from_spec(_MC_SPEC)
sys.modules.setdefault("measure_coverage", _measure_coverage)
_MC_SPEC.loader.exec_module(_measure_coverage)
measure = _measure_coverage.measure

REPO_ROOT = _HERE.parent.parent


def _regrade_one(
    growth_path: Path,
    sut: str,
    format_: str,
    config_path: Path,
) -> dict:
    """Load `growth_path`, regrade each tick against the fairness
    recipe, rewrite in place. Returns a summary dict for logging."""
    data = json.loads(growth_path.read_text(encoding="utf-8"))
    run_idx = data.get("run_index")
    run_dir = growth_path.parent / f"run_{run_idx}" / "jacoco_exec"
    if not run_dir.exists():
        raise FileNotFoundError(
            f"expected jacoco_exec dir at {run_dir} for {growth_path.name}"
        )

    old_ticks = data.get("coverage_growth", [])
    new_ticks: list[dict] = []
    diffs: list[tuple[int, float, float, float, float]] = []
    for entry in old_ticks:
        t = int(entry["t_s"])
        xml = run_dir / f"tick_{t}.xml"
        if not xml.exists():
            logger.warning(
                "  t=%ds: %s missing — keeping prior numbers",
                t, xml.name,
            )
            new_ticks.append(entry)
            continue
        line_r = measure(xml, sut=sut, format_=format_,
                         config_path=config_path, metric="LINE")
        branch_r = measure(xml, sut=sut, format_=format_,
                           config_path=config_path, metric="BRANCH")
        new_line = round(line_r.weighted_pct, 3)
        new_branch = round(branch_r.weighted_pct, 3)
        diffs.append((t, entry.get("line_pct", 0.0), new_line,
                      entry.get("branch_pct", 0.0), new_branch))
        new_ticks.append({
            "t_s": t,
            "line_pct": new_line,
            "branch_pct": new_branch,
        })

    # Record provenance — helps anyone reading the JSON later see that
    # the coverage % is the fairness-recipe number, not whatever the
    # sampler's on-disk code happened to compute.
    extra = dict(data.get("extra", {}))
    regrade = extra.get("regrade", {})
    regrade["by"] = "compares/scripts/recompute_growth.py"
    regrade["recipe"] = "compares/scripts/measure_coverage.py"
    regrade["config"] = str(config_path)
    regrade["sut"] = sut
    regrade["format"] = format_
    regrade["ticks_regraded"] = len(diffs)
    extra["regrade"] = regrade

    data["coverage_growth"] = new_ticks
    data["extra"] = extra
    growth_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    return {
        "path": str(growth_path),
        "ticks_regraded": len(diffs),
        "sample": diffs[-3:],  # last few ticks for quick-scan stdout
    }


def _rebuild_aggregate(growth_dir: Path, per_rep_files: list[Path]) -> Path | None:
    """Regenerate `growth_aggregate.json` from the (just-regraded)
    per-rep growth_<idx>.json files.

    Schema mirrors what the sampler writes at end-of-cell (line_pct_mean
    / _ci_lo / _ci_hi / _n + branch equivalents per tick). A 95% CI with
    N=1 collapses to ±0; with N≥2 we use the Student-t half-width as the
    sampler does. If no aggregate is needed (single rep, no sibling
    file), returns None.
    """
    if not per_rep_files:
        return None
    import statistics

    # Gather per-tick lists across reps.
    per_t_line: dict[int, list[float]] = {}
    per_t_branch: dict[int, list[float]] = {}
    meta: dict = {}
    for gp in per_rep_files:
        d = json.loads(gp.read_text(encoding="utf-8"))
        if not meta:
            meta = {k: d.get(k) for k in ("tool", "sut", "format", "phase",
                                           "time_budget_s", "seed_corpus_hash")}
        for tick in d.get("coverage_growth", []):
            per_t_line.setdefault(int(tick["t_s"]), []).append(float(tick["line_pct"]))
            per_t_branch.setdefault(int(tick["t_s"]), []).append(float(tick["branch_pct"]))

    if not per_t_line:
        return None

    def _ci95_halfwidth(xs: list[float]) -> float:
        """Student-t 95% CI half-width; 0 for N<=1."""
        if len(xs) <= 1:
            return 0.0
        # Use stdev (sample) / sqrt(n) * t_{0.025, n-1}. For small n use
        # a lookup for t_{0.025} so we don't pull scipy.
        t_crit = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571,
                  7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262}.get(len(xs), 2.0)
        s = statistics.stdev(xs)
        return t_crit * s / (len(xs) ** 0.5)

    agg_rows = []
    for t in sorted(per_t_line):
        xs_l = per_t_line[t]
        xs_b = per_t_branch.get(t, [])
        mean_l = statistics.mean(xs_l)
        mean_b = statistics.mean(xs_b) if xs_b else 0.0
        hw_l = _ci95_halfwidth(xs_l)
        hw_b = _ci95_halfwidth(xs_b) if xs_b else 0.0
        agg_rows.append({
            "t_s": t,
            "line_pct_mean": round(mean_l, 3),
            "line_pct_ci_lo": round(mean_l - hw_l, 3),
            "line_pct_ci_hi": round(mean_l + hw_l, 3),
            "line_pct_n": len(xs_l),
            "branch_pct_mean": round(mean_b, 3),
            "branch_pct_ci_lo": round(mean_b - hw_b, 3),
            "branch_pct_ci_hi": round(mean_b + hw_b, 3),
            "branch_pct_n": len(xs_b),
        })

    out = {
        **meta,
        "reps": len(per_rep_files),
        "ticks": [r["t_s"] for r in agg_rows],
        "coverage_growth_aggregate": agg_rows,
    }
    out_path = growth_dir / "growth_aggregate.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out_path


def _cli() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--growth-dir", type=Path, required=True,
                    help="directory holding growth_<idx>.json + run_<idx>/")
    ap.add_argument("--sut", required=True)
    ap.add_argument("--format", dest="format_", required=True,
                    choices=["VCF", "SAM", "vcf", "sam"])
    ap.add_argument("--config", default=str(REPO_ROOT / "biotest_config.yaml"),
                    help="Path to biotest_config.yaml (the fairness-recipe "
                         "source of truth).")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s %(message)s",
    )

    # Match growth_<int>.json per-rep files only — skip aggregates
    # (growth_aggregate.json) and other sampler-side derived files that
    # don't carry a run_index / jacoco_exec sibling dir.
    import re as _re
    _per_rep = _re.compile(r"^growth_\d+\.json$")
    growth_files = sorted(
        p for p in args.growth_dir.glob("growth_*.json")
        if _per_rep.match(p.name)
    )
    if not growth_files:
        logger.error("no growth_<idx>.json per-rep files under %s", args.growth_dir)
        return 2

    fmt = args.format_.upper()
    total_ticks = 0
    for gf in growth_files:
        summary = _regrade_one(
            growth_path=gf, sut=args.sut, format_=fmt,
            config_path=Path(args.config),
        )
        total_ticks += summary["ticks_regraded"]
        print(f"[regrade] {gf.name}: regraded {summary['ticks_regraded']} ticks")
        for t, old_l, new_l, old_b, new_b in summary["sample"]:
            # ASCII arrow so Windows cp1252 consoles don't UnicodeEncodeError.
            print(
                f"  t={t:>4}s  line {old_l:>6.2f} -> {new_l:>6.2f}  "
                f"branch {old_b:>6.2f} -> {new_b:>6.2f}"
            )
    print(f"[regrade] total: {len(growth_files)} file(s), {total_ticks} tick(s) regraded")

    agg_path = _rebuild_aggregate(args.growth_dir, growth_files)
    if agg_path:
        print(f"[regrade] rebuilt aggregate: {agg_path.name} "
              f"(reps={len(growth_files)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
