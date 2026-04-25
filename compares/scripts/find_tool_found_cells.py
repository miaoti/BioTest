#!/usr/bin/env python3
"""List every cell that classifies as a genuine tool-found detection."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "compares" / "scripts"))
from report_bug_bench_md import classify, trigger_origin

agg = json.loads((ROOT / "compares" / "results" / "bug_bench_aggregate_final.json").read_text(encoding="utf-8"))
print("=== tool-genuine FOUND cells ===")
for sect in ("vcf_results", "sam_results"):
    for r in agg.get(sect, []):
        if classify(r) == "FOUND":
            print(f"  [{sect}] {r.get('tool'):12} {r.get('bug_id'):20} "
                  f"trigger_origin={trigger_origin(r)} "
                  f"trigger_input={r.get('trigger_input')}")
print()
print("=== POV-confirmed cells (counted but not tool-genuine) ===")
for sect in ("vcf_results", "sam_results"):
    for r in agg.get(sect, []):
        if classify(r) == "FOUND-pov":
            print(f"  [{sect}] {r.get('tool'):12} {r.get('bug_id'):20}")
