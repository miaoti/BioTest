"""Backfill detected_via_{tool_output,pov_verification} into existing
result.json files for any tool's bug-bench cells.

The schema split landed 2026-04-28 (see DETECTION_RATIONALE.md); this
script rewrites every existing result.json with the two new boolean
fields derived from `trigger_input` so historical runs become
comparable to fresh ones without requiring a re-run.

Classification:
  - trigger_input under `compares/bug_bench/triggers/`  → PoV verification
  - trigger_input under `<tool_out>/crashes/`           → tool output
  - trigger_input == None or `detected=False`           → both False
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = ROOT / "compares" / "results" / "bug_bench"


def classify(detected: bool, trig: str | None) -> tuple[bool, bool]:
    if not detected or not trig:
        return False, False
    norm = trig.replace("\\", "/")
    if "compares/bug_bench/triggers/" in norm:
        return False, True
    if "/crashes/" in norm:
        return True, False
    return True, False


def main() -> None:
    changed = 0
    seen = 0
    for tool_dir in BENCH_DIR.iterdir():
        if not tool_dir.is_dir() or tool_dir.name in {"sweep_logs"}:
            continue
        for bug_dir in tool_dir.iterdir():
            rj = bug_dir / "result.json"
            if not rj.is_file():
                continue
            seen += 1
            data = json.loads(rj.read_text(encoding="utf-8"))
            via_tool, via_pov = classify(
                data.get("detected", False),
                data.get("trigger_input"),
            )
            if (
                data.get("detected_via_tool_output") == via_tool
                and data.get("detected_via_pov_verification") == via_pov
            ):
                continue
            data["detected_via_tool_output"] = via_tool
            data["detected_via_pov_verification"] = via_pov
            rj.write_text(json.dumps(data, indent=2), encoding="utf-8")
            changed += 1
    print(f"reclassified {changed} of {seen} per-cell result.json files")


if __name__ == "__main__":
    main()
