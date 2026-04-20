"""Aggregate every growth_<idx>.json under compares/results/coverage/
into a single summary.csv for the Phase-6 report consumer.

Scans `compares/results/coverage/<tool>/<cell>/growth_<idx>.json`,
pulls the DESIGN §4.5 canonical fields, and writes
`compares/results/coverage/summary.csv` with one row per rep plus a
`coverage_growth_aggregate.json` per cell that carries the mean + 95%
CI at every tick (matches the CI-band plotting the report expects).

Smoke-test rows under `coverage/**/smoke/` are excluded.

Run (idempotent):

    py -3.12 compares/scripts/coverage_rollup.py
"""

from __future__ import annotations

import csv
import json
import math
import pathlib
import statistics
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "compares" / "results" / "coverage"
OUT_CSV = ROOT / "summary.csv"

FIELDS = [
    "tool", "sut", "format", "phase", "run_index", "time_budget_s",
    "seed_corpus_hash", "duration_s", "ticks",
    "line_pct_max", "branch_pct_max",
]


def _is_smoke(p: pathlib.Path) -> bool:
    return any(part == "smoke" or part.endswith("_smoke") for part in p.parts)


def _ci95(vals: list[float]) -> tuple[float | None, float | None]:
    if not vals:
        return None, None
    if len(vals) < 2:
        return vals[0], vals[0]
    mean = statistics.fmean(vals)
    sd = statistics.stdev(vals)
    margin = 1.96 * sd / math.sqrt(len(vals))
    return mean - margin, mean + margin


def _aggregate_cell(cell_dir: pathlib.Path) -> dict | None:
    """Collapse growth_{0,1,...}.json into a per-tick mean + 95% CI dict.
    Returns None if no reps exist."""
    reps: list[dict] = []
    for j in sorted(cell_dir.glob("growth_*.json")):
        if j.name.startswith("growth_aggregate"):
            continue
        try:
            d = json.loads(j.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"SKIP {j}: {exc}", file=sys.stderr)
            continue
        reps.append(d)
    if not reps:
        return None

    ticks: set[int] = set()
    for rep in reps:
        for snap in rep.get("coverage_growth", []):
            ticks.add(int(snap["t_s"]))
    ticks_sorted = sorted(ticks)

    aggregate_rows = []
    for t in ticks_sorted:
        line_vals = []
        br_vals = []
        for rep in reps:
            for snap in rep.get("coverage_growth", []):
                if int(snap["t_s"]) != t:
                    continue
                lp = snap.get("line_pct")
                bp = snap.get("branch_pct")
                if lp is not None:
                    line_vals.append(float(lp))
                if bp is not None:
                    br_vals.append(float(bp))
        lmean = statistics.fmean(line_vals) if line_vals else None
        bmean = statistics.fmean(br_vals) if br_vals else None
        lo, hi = _ci95(line_vals)
        blo, bhi = _ci95(br_vals)
        aggregate_rows.append({
            "t_s": t,
            "line_pct_mean": round(lmean, 2) if lmean is not None else None,
            "line_pct_ci_lo": round(lo, 2) if lo is not None else None,
            "line_pct_ci_hi": round(hi, 2) if hi is not None else None,
            "line_pct_n": len(line_vals),
            "branch_pct_mean": round(bmean, 2) if bmean is not None else None,
            "branch_pct_ci_lo": round(blo, 2) if blo is not None else None,
            "branch_pct_ci_hi": round(bhi, 2) if bhi is not None else None,
            "branch_pct_n": len(br_vals),
        })

    # Carry the cell-level metadata from rep 0 as canonical — all reps
    # share the same tool / sut / format / budget by construction.
    first = reps[0]
    out = {
        "tool": first.get("tool"),
        "sut": first.get("sut"),
        "format": first.get("format"),
        "phase": first.get("phase", "coverage"),
        "time_budget_s": first.get("time_budget_s"),
        "reps": len(reps),
        "seed_corpus_hash": first.get("seed_corpus_hash"),
        "ticks": ticks_sorted,
        "coverage_growth_aggregate": aggregate_rows,
    }
    (cell_dir / "growth_aggregate.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8",
    )
    return out


def main() -> int:
    rows: list[dict] = []
    # Cells live at: compares/results/coverage/<tool>/<cell>/
    for tool_dir in sorted(ROOT.iterdir()):
        if not tool_dir.is_dir():
            continue
        if _is_smoke(tool_dir):
            continue
        for cell_dir in sorted(tool_dir.iterdir()):
            if not cell_dir.is_dir():
                continue
            if _is_smoke(cell_dir):
                continue
            if not any(cell_dir.glob("growth_*.json")):
                continue
            _aggregate_cell(cell_dir)
            # Emit one CSV row per rep.
            for j in sorted(cell_dir.glob("growth_*.json")):
                if j.name.startswith("growth_aggregate"):
                    continue
                try:
                    d = json.loads(j.read_text(encoding="utf-8"))
                except Exception as exc:
                    print(f"SKIP {j}: {exc}", file=sys.stderr)
                    continue
                growth = d.get("coverage_growth", [])
                line_max = max((s.get("line_pct", 0) or 0 for s in growth),
                               default=None)
                branch_max = max((s.get("branch_pct", 0) or 0 for s in growth),
                                 default=None)
                rows.append({
                    "tool": tool_dir.name,
                    "cell": cell_dir.name,
                    "sut": d.get("sut"),
                    "format": d.get("format"),
                    "phase": d.get("phase"),
                    "run_index": d.get("run_index"),
                    "time_budget_s": d.get("time_budget_s"),
                    "seed_corpus_hash": d.get("seed_corpus_hash"),
                    "duration_s": (d.get("extra") or {}).get("duration_s"),
                    "ticks": ",".join(str(s["t_s"]) for s in growth),
                    "line_pct_max": round(line_max, 2) if line_max is not None else None,
                    "branch_pct_max": round(branch_max, 2) if branch_max is not None else None,
                    "growth_json": str(j.relative_to(REPO_ROOT).as_posix()),
                })

    if not rows:
        print("[coverage-rollup] no growth_*.json found under", ROOT, file=sys.stderr)
        return 1

    header = ["tool", "cell"] + [f for f in FIELDS if f != "tool"] + ["growth_json"]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[coverage-rollup] wrote {len(rows)} reps to {OUT_CSV}")
    for r in rows:
        print(f"  {r['tool']:<12} {r['cell']:<18} rep={r['run_index']}  "
              f"line_max={r['line_pct_max']}%  branch_max={r['branch_pct_max']}%  "
              f"ticks=[{r['ticks']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
