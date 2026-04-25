#!/usr/bin/env python3
"""Distinguish 'tool-found' vs 'PoV-fallback-found' for every detected
SAM cell.

A FOUND verdict is honest only if the tool's own corpus produced the
triggering input. The 2026-04-21 driver added a manifest-PoV fallback
that confirms a cell when the harvested trigger doesn't but the
canonical PoV does. Fair reporting flags both classes.
"""
import json
from pathlib import Path

BENCH = Path("/tmp/bug_bench_sam_new")
TRIGGERS_DIR = "/work/compares/bug_bench/triggers/"


def origin(rec: dict) -> str:
    """Where did the verifying trigger come from?"""
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
    if not trig:
        return "no-trigger"
    return f"other:{trig}"


print(f"{'tool':16} {'bug':14} {'detected':9} {'conf':6} {'origin':14} {'notes'}")
for tool in ("biotest", "jazzer", "pure_random", "evosuite_anchor"):
    for bug in ("htsjdk-1238", "htsjdk-1360", "htsjdk-1410"):
        rj = BENCH / tool / bug / "result.json"
        if not rj.exists():
            print(f"{tool:16} {bug:14} -         -      -              (no result.json)")
            continue
        rec = json.loads(rj.read_text(encoding="utf-8"))
        det = rec.get("detected")
        conf = rec.get("confirmed_fix_silences_signal")
        note = (rec.get("notes") or "")[:80]
        print(f"{tool:16} {bug:14} {str(det):9} {str(conf):6} {origin(rec):14} {note}")
