#!/usr/bin/env python3
"""Audit trigger origins for biotest in the canonical bug_bench tree."""
import json
from pathlib import Path

BENCH = Path("/work/compares/results/bug_bench")
TRIGGERS_DIR = "/work/compares/bug_bench/triggers/"


def origin(rec: dict) -> str:
    trig = rec.get("trigger_input") or ""
    notes = rec.get("notes") or ""
    if "PoV fallback" in notes or "canonical PoV" in notes:
        return "PoV-fallback"
    if trig.startswith(TRIGGERS_DIR):
        return "manifest-PoV"
    if "/crashes/" in trig:
        return "tool-crash"
    if "/corpus/" in trig:
        return "tool-corpus"
    if "/bug_reports/" in trig:
        return "biotest-report"
    if not trig:
        return "no-trigger"
    return f"other:{trig[:60]}"


print(f"{'tool':12} {'bug':14} {'detected':9} {'conf':6} {'origin':18} notes")
for tool in ("biotest",):
    for bug in ("htsjdk-1238", "htsjdk-1360", "htsjdk-1410"):
        rj = BENCH / tool / bug / "result.json"
        if not rj.exists():
            print(f"{tool:12} {bug:14} -         -      -                  (no result.json)")
            continue
        rec = json.loads(rj.read_text(encoding="utf-8"))
        det = rec.get("detected")
        conf = rec.get("confirmed_fix_silences_signal")
        note = (rec.get("notes") or "")[:90]
        print(f"{tool:12} {bug:14} {str(det):9} {str(conf):6} {origin(rec):18} {note}")
        # Also peek at trigger_input
        ti = rec.get("trigger_input") or ""
        print(f"{'':12} {'':14} trigger_input: {ti}")
