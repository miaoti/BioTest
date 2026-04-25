#!/usr/bin/env python3
"""Audit jazzer's three new htsjdk SAM cells.

Each cell's verdict is supposed to come from a tool-generated trigger.
The 2026-04-21 driver revision added a PoV-fallback path that can
confirm a cell even when jazzer's own corpus did not produce the
triggering bytes — this script makes that explicit per-cell so we can
distinguish a real find from a fallback confirmation.
"""
import json
from pathlib import Path

BENCH = Path("/tmp/bug_bench_sam_new")
print(f"=== jazzer cells in {BENCH} ===")
for bug in ("htsjdk-1238", "htsjdk-1360", "htsjdk-1410"):
    cell = BENCH / "jazzer" / bug
    if not cell.exists():
        print(f"\n--- {bug}: no cell dir")
        continue
    print(f"\n--- {bug} ---")
    rj_path = cell / "result.json"
    if rj_path.exists():
        rj = json.loads(rj_path.read_text(encoding="utf-8"))
        for k in (
            "detected", "ttfb_s", "trigger_input", "signal",
            "confirmed_fix_silences_signal", "adapter_exit_code", "notes",
        ):
            print(f"  {k}: {rj.get(k)}")
    crashes = cell / "crashes"
    if crashes.exists():
        items = sorted(crashes.iterdir())
        print(f"  crashes/: {len(items)} entries")
        for c in items[:5]:
            try:
                size = c.stat().st_size
            except Exception:
                size = "?"
            print(f"    {c.name} ({size}B)")
    else:
        print(f"  crashes/: <missing>")
    corpus = cell / "corpus"
    if corpus.exists():
        n = sum(1 for _ in corpus.iterdir())
        print(f"  corpus/: {n} entries")
    log = cell / "tool.log"
    if log.exists():
        size = log.stat().st_size
        print(f"  tool.log: {size} bytes")
        # Look for libFuzzer terminal lines that signal a real crash
        lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
        for tag in ("crash-", "==ERROR", "ERROR: AddressSanitizer",
                    "Java Exception", "WARNING: ", "INFO: Found",
                    "==FATAL", "stat::number_of_executed_units"):
            hits = [ln for ln in lines if tag in ln]
            if hits:
                print(f"    log[{tag!r}]: {hits[-1][:150]}")
