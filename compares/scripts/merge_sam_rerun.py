#!/usr/bin/env python3
"""Merge the 2026-04-21 SAM rerun into the canonical final aggregates.

Reads the post-rerun authoritative SAM data from
``compares/results/bug_bench_sam_aggregate_2026_04_21.json`` and writes
- ``compares/results/bug_bench_sam_final.json`` (replace)
- ``compares/results/bug_bench_aggregate_final.json`` (replace sam_results
  + recompute counters)

Idempotent: re-running with the same inputs is a no-op.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "compares" / "results"

DROPPED = {"biopython-4825", "htsjdk-1538", "htsjdk-1561", "htsjdk-1489"}
ADDED = {"htsjdk-1238", "htsjdk-1360", "htsjdk-1410"}


def main() -> None:
    rerun_path = RESULTS / "bug_bench_sam_aggregate_2026_04_21.json"
    rerun = json.loads(rerun_path.read_text(encoding="utf-8"))
    new_sam = rerun["results"] if isinstance(rerun, dict) and "results" in rerun else rerun
    ids = {r["bug_id"] for r in new_sam}

    if ids & DROPPED:
        raise SystemExit(f"rerun still has dropped bugs: {sorted(ids & DROPPED)}")
    if not ADDED <= ids:
        raise SystemExit(f"rerun missing added bugs: {sorted(ADDED - ids)}")
    print(f"[merge] rerun OK: {len(new_sam)} cells; "
          f"added={sorted(ids & ADDED)}")

    # bug_bench_sam_final.json
    sam_final_path = RESULTS / "bug_bench_sam_final.json"
    sam_final = {
        "results": new_sam,
        "manifest_revision": "2026-04-21",
        "dropped": sorted(DROPPED),
        "added": sorted(ADDED),
    }
    sam_final_path.write_text(json.dumps(sam_final, indent=2), encoding="utf-8")
    print(f"[merge] wrote {sam_final_path}: {len(new_sam)} cells")

    # bug_bench_aggregate_final.json
    agg_path = RESULTS / "bug_bench_aggregate_final.json"
    agg = json.loads(agg_path.read_text(encoding="utf-8"))
    vcf = agg.get("vcf_results", [])
    agg["sam_results"] = new_sam
    agg["total_cells"] = len(vcf) + len(new_sam)
    agg["sam_confirmed"] = sum(
        1 for r in new_sam
        if r.get("detected") and r.get("confirmed_fix_silences_signal") is True
    )
    agg["total_confirmed"] = agg.get("vcf_confirmed", 0) + agg["sam_confirmed"]
    agg["sam_manifest_revision"] = "2026-04-21"
    agg["sam_dropped"] = sorted(DROPPED)
    agg["sam_added"] = sorted(ADDED)
    agg_path.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    print(f"[merge] wrote {agg_path}: total_cells={agg['total_cells']} "
          f"vcf_confirmed={agg['vcf_confirmed']} sam_confirmed={agg['sam_confirmed']} "
          f"total_confirmed={agg['total_confirmed']}")


if __name__ == "__main__":
    main()
