#!/usr/bin/env python3
"""Inspect the 9-cell SAM rerun results."""
import json
from pathlib import Path

BENCH = Path("/tmp/bug_bench_sam_new")
agg = json.loads((BENCH / "aggregate.json").read_text(encoding="utf-8"))
results = agg.get("results", agg)
print(f"=== {len(results)} cells ===")
for r in sorted(results, key=lambda x: (x.get("tool", ""), x.get("bug_id", ""))):
    tool = r.get("tool")
    bug = r.get("bug_id")
    det = r.get("detected")
    conf = r.get("confirmed_fix_silences_signal")
    err = r.get("error") or ""
    notes = (r.get("notes") or "")[:60]
    ttfb = r.get("ttfb_s")
    exit_code = r.get("adapter_exit_code")
    line = (
        f"  {tool:16} {bug:14} det={str(det):5} conf={str(conf):5} "
        f"ttfb={str(ttfb):8} exit={exit_code} err={err[:40]} notes={notes}"
    )
    print(line)
