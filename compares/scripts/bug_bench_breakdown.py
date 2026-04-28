#!/usr/bin/env python3
"""Compute per-(tool, sut) breakdown into FOUND / false+ / crash? / miss / skip.

Reads aggregate.json and prints a semantic breakdown that distinguishes
"adapter reported any crash" (the existing `detected` boolean) from
"FOUND the target bug" (detected AND confirmed_fix_silences_signal is True).
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregate", type=Path, required=True)
    args = ap.parse_args()

    agg = json.loads(args.aggregate.read_text(encoding="utf-8"))
    records = agg["results"]

    counts = defaultdict(lambda: {
        "total": 0, "detected_any_crash": 0,
        "FOUND": 0, "false_plus": 0, "crash_qmark": 0, "miss": 0, "skip": 0,
    })
    found_cells = defaultdict(list)
    fp_cells = defaultdict(list)
    skip_cells = defaultdict(list)
    for r in records:
        key = (r.get("tool", ""), r.get("sut", ""))
        c = counts[key]
        c["total"] += 1
        bug = r.get("bug_id", "?")
        if r.get("install_error") or r.get("error"):
            c["skip"] += 1
            skip_cells[key].append(bug)
            continue
        det = r.get("detected")
        conf = r.get("confirmed_fix_silences_signal")
        if det:
            c["detected_any_crash"] += 1
            if conf is True:
                c["FOUND"] += 1
                found_cells[key].append(bug)
            elif conf is False:
                c["false_plus"] += 1
                fp_cells[key].append(bug)
            else:
                c["crash_qmark"] += 1
        else:
            c["miss"] += 1

    for key, c in sorted(counts.items()):
        tool, sut = key
        line = (
            f"{tool}/{sut}:"
            f" total={c['total']}"
            f" detected_any={c['detected_any_crash']}"
            f" FOUND={c['FOUND']}"
            f" false+={c['false_plus']}"
            f" crash?={c['crash_qmark']}"
            f" miss={c['miss']}"
            f" skip={c['skip']}"
        )
        print(line)
        if found_cells[key]:
            print(f"  FOUND bugs: {sorted(found_cells[key])}")
        if fp_cells[key]:
            print(f"  false+ bugs: {sorted(fp_cells[key])}")
        if skip_cells[key]:
            print(f"  skip bugs: {sorted(skip_cells[key])}")


if __name__ == "__main__":
    main()
