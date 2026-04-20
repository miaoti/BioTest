"""Validate every growth_<idx>.json under compares/results/coverage/
against the DESIGN.md §4.5 schema.

Usage:

    py -3.12 compares/scripts/validate_growth_schema.py \\
        [--cell compares/results/coverage/<tool>/<sut>[_<fmt>]] \\
        [--ticks 1,10,60,300,1800,7200]

Checks per file:

  * required keys: tool, sut, format, phase="coverage", run_index,
    time_budget_s, seed_corpus_hash (string), coverage_growth (list),
    mutation_score, bug_bench
  * coverage_growth entries: t_s (int), line_pct (float), branch_pct (float)
  * requested tick set is a subset of the t_s values actually present
    (this is the DESIGN §13.5 "Monitor: confirm log ticks" one-liner).
  * line_pct monotonically non-decreasing (coverage never shrinks within
    a single rep) — this is a soft check: a decrease ≥ 0.5 pp triggers
    a warning rather than a failure, because the post-hoc tick can
    sometimes round slightly below the prior live snapshot.

Returns exit 0 if every file passes, exit 1 if any hard check fails.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

REQUIRED_KEYS = {
    "tool", "sut", "format", "phase", "run_index", "time_budget_s",
    "seed_corpus_hash", "coverage_growth", "mutation_score", "bug_bench",
}


def _validate_one(p: pathlib.Path, required_ticks: set[int]) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"JSON parse: {exc}"]

    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        errors.append(f"missing required keys: {sorted(missing)}")

    if data.get("phase") != "coverage":
        errors.append(f"phase != 'coverage' ({data.get('phase')!r})")

    growth = data.get("coverage_growth") or []
    if not isinstance(growth, list):
        errors.append("coverage_growth is not a list")
        growth = []

    ticks_present: set[int] = set()
    prev_line = None
    for snap in growth:
        if not isinstance(snap, dict):
            errors.append(f"coverage_growth entry is not a dict: {snap!r}")
            continue
        t_s = snap.get("t_s")
        lp = snap.get("line_pct")
        bp = snap.get("branch_pct")
        if not isinstance(t_s, int):
            errors.append(f"coverage_growth.t_s not an int: {snap!r}")
            continue
        ticks_present.add(t_s)
        if not isinstance(lp, (int, float)):
            errors.append(f"coverage_growth[t={t_s}].line_pct not numeric: {lp!r}")
        if not isinstance(bp, (int, float)):
            errors.append(f"coverage_growth[t={t_s}].branch_pct not numeric: {bp!r}")
        if prev_line is not None and isinstance(lp, (int, float)) and lp < prev_line - 0.5:
            warnings.append(
                f"line_pct dropped at t={t_s}: {prev_line} → {lp} "
                "(Δ > 0.5 pp — check instrumentation consistency)"
            )
        if isinstance(lp, (int, float)):
            prev_line = lp

    missing_ticks = required_ticks - ticks_present
    if missing_ticks:
        errors.append(
            f"missing required ticks {sorted(missing_ticks)}; "
            f"present={sorted(ticks_present)}"
        )

    if errors:
        return [f"FAIL {p}", *[f"  - {e}" for e in errors]] + \
               [f"  WARN {w}" for w in warnings]
    if warnings:
        return [f"WARN {p}", *[f"  - {w}" for w in warnings]]
    return [f"OK   {p}"]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--cell", type=pathlib.Path, default=None,
                   help="Single cell dir to validate. If omitted, scans "
                        "compares/results/coverage/**/growth_*.json.")
    p.add_argument("--ticks", default="1,10,60,300,1800,7200",
                   help="Required tick set. Comma-separated, matches DESIGN §3.2.")
    args = p.parse_args()

    required = {int(x) for x in args.ticks.split(",") if x.strip()}

    if args.cell is not None:
        paths = sorted(args.cell.glob("growth_*.json"))
    else:
        root = REPO_ROOT / "compares" / "results" / "coverage"
        paths = sorted(root.rglob("growth_*.json"))

    # Drop aggregate + smoke paths
    paths = [q for q in paths
             if not q.name.startswith("growth_aggregate")
             and "smoke" not in q.parts]

    if not paths:
        print(f"[validate] no growth_*.json files found under "
              f"{args.cell or 'compares/results/coverage'}")
        return 0

    any_fail = False
    for q in paths:
        results = _validate_one(q, required)
        for line in results:
            print(line)
        if any(line.startswith("FAIL") for line in results):
            any_fail = True

    print(f"\n[validate] {len(paths)} file(s) checked; {'FAIL' if any_fail else 'ALL PASS'}")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
