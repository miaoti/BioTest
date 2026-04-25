#!/usr/bin/env python3
"""Inspect per-cell coverage for the 3 new SAM htsjdk bugs across all tools."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH = ROOT / "compares" / "results" / "bug_bench"
NEW_BUGS = ["htsjdk-1238", "htsjdk-1360", "htsjdk-1410"]
HTSJDK_TOOLS = ["biotest", "jazzer", "pure_random", "evosuite_anchor"]

print("=== per-cell coverage for new SAM htsjdk bugs ===")
print(f"{'tool':12} {'bug':14} {'has_result':10} det conf  notes")
for tool in HTSJDK_TOOLS:
    for bug in NEW_BUGS:
        f = BENCH / tool / bug / "result.json"
        if f.exists():
            try:
                r = json.loads(f.read_text(encoding="utf-8"))
                det = r.get("detected")
                conf = r.get("confirmed_fix_silences_signal")
                notes = r.get("notes") or ""
                err = r.get("error") or ""
                line = (f"{tool:12} {bug:14} present    "
                        f"{str(det):5} {str(conf):5}  "
                        f"{(notes or err)[:60]}")
                print(line)
            except Exception as e:
                print(f"{tool:12} {bug:14} BROKEN     {e}")
        else:
            print(f"{tool:12} {bug:14} MISSING    -     -      no result.json on disk")
