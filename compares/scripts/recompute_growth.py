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

    growth_files = sorted(args.growth_dir.glob("growth_*.json"))
    if not growth_files:
        logger.error("no growth_*.json files under %s", args.growth_dir)
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
            print(
                f"  t={t:>4}s  line {old_l:>6.2f} → {new_l:>6.2f}  "
                f"branch {old_b:>6.2f} → {new_b:>6.2f}"
            )
    print(f"[regrade] total: {len(growth_files)} file(s), {total_ticks} tick(s) regraded")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
