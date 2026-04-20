"""Aggregate every validity.json under compares/results/validity/ into
a single summary.csv for the Phase-6 report consumer.

Scans `compares/results/validity/<tool>/<cell>/validity.json`, pulls
the canonical fields, and writes `compares/results/validity/summary.csv`
with one row per cell. Smoke-test rows under `validity/smoke/` are
excluded (they live beside real cells and would duplicate the per-cell
row for each tool).

Run (idempotent):

    py -3.12 compares/scripts/validity_rollup.py
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "compares" / "results" / "validity"
OUT = ROOT / "summary.csv"

FIELDS = [
    "tool", "sut", "format", "validity_ratio",
    "parse_success", "generated_total",
    "timeout_count", "crash_count", "parse_error_count", "ineligible_count",
    "duration_s", "runner", "corpus_dir",
]


def _is_smoke(p: pathlib.Path) -> bool:
    return "smoke" in p.parts


def main() -> int:
    rows: list[dict] = []
    for j in sorted(ROOT.rglob("validity.json")):
        if _is_smoke(j):
            continue
        try:
            d = json.loads(j.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"SKIP {j}: {e}", file=sys.stderr)
            continue
        row = {k: d.get(k) for k in FIELDS}
        # Derive "cell" tag from path:
        # compares/results/validity/<tool>/<cell>/validity.json
        rel = j.relative_to(ROOT)
        parts = rel.parts
        if len(parts) >= 3:
            row["tool"] = parts[0]          # trust path over JSON 'tool'
            row["cell"] = parts[1]
        rows.append(row)

    if not rows:
        print("[rollup] no validity.json found under", ROOT, file=sys.stderr)
        return 1

    # Ensure `cell` is in the header even though it's injected here.
    header = ["tool", "cell"] + [f for f in FIELDS if f != "tool"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[rollup] wrote {len(rows)} cells to {OUT}")
    for r in rows:
        print(f"  {r['tool']:<12} {r['cell']:<14} {r['sut']:<10} "
              f"{r['format']}: "
              f"{r['parse_success']}/{r['generated_total']} = "
              f"{(r['validity_ratio'] or 0):.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
