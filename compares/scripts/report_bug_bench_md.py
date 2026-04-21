#!/usr/bin/env python3
"""Emit a per-tool markdown report from a bug-bench tree.

Walks <bench_root>/<tool>/<bug_id>/result.json (or reads aggregate.json
if present) and groups detections by tool for a human-readable scorecard.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def classify(record: dict) -> str:
    if record.get("error"):
        return "skip"
    detected = record.get("detected")
    confirmed = record.get("confirmed_fix_silences_signal")
    if detected is None:
        return "skip"
    if not detected:
        return "miss"
    if confirmed is True:
        return "FOUND"
    if confirmed is False:
        return "false+"
    return "crash?"


def load_records(bench_root: Path) -> list[dict]:
    agg = bench_root / "aggregate.json"
    if agg.exists():
        try:
            return json.loads(agg.read_text(encoding="utf-8")).get("results", [])
        except Exception:
            pass
    records: list[dict] = []
    for r in bench_root.rglob("result.json"):
        if r.parent.parent.name == bench_root.name:
            continue
        try:
            records.append(json.loads(r.read_text(encoding="utf-8")))
        except Exception:
            pass
    return records


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--title", default="bug-bench report")
    args = p.parse_args()

    records = load_records(args.bench_root)

    by_tool: dict[str, dict[str, str]] = defaultdict(dict)
    skip_reasons: dict[tuple[str, str], str] = {}
    tools: list[str] = []
    bugs: list[str] = []
    for r in records:
        t = r.get("tool") or "?"
        b = r.get("bug_id") or "?"
        if t not in tools:
            tools.append(t)
        if b not in bugs:
            bugs.append(b)
        cls = classify(r)
        by_tool[t][b] = cls
        if cls == "skip":
            reason = (
                r.get("error")
                or r.get("install_error")
                or r.get("notes")
                or "(no error recorded)"
            )
            skip_reasons[(t, b)] = str(reason)
    tools.sort()
    bugs.sort()

    lines: list[str] = []
    lines.append(f"# {args.title}")
    lines.append("")
    lines.append(f"- total cells: {len(records)}")
    lines.append(f"- tools: {', '.join(tools) or '(none)'}")
    lines.append(f"- bugs: {len(bugs)}")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("- **FOUND** — tool produced a trigger that fails pre-fix and is silenced by post-fix")
    lines.append("- **crash?** — tool crashed pre-fix but post-fix replay inconclusive (null)")
    lines.append("- **false+** — tool crashed pre-fix but post-fix STILL crashes (likely unrelated)")
    lines.append("- **miss** — tool ran but did not produce a triggering input")
    lines.append("- **—** — no result.json (cell was skipped: install failed, harness mismatch, etc.)")
    lines.append("")

    lines.append("## Per-bug matrix")
    lines.append("")
    if tools and bugs:
        lines.append("| bug | " + " | ".join(tools) + " |")
        lines.append("| :-- | " + " | ".join([":-:"] * len(tools)) + " |")
        for b in bugs:
            row = [b] + [by_tool[t].get(b, "—") for t in tools]
            lines.append("| " + " | ".join(row) + " |")
    else:
        lines.append("_(no cells recorded)_")
    lines.append("")

    lines.append("## Per-tool bugs found")
    lines.append("")
    for t in tools:
        cells = by_tool[t]
        found = [b for b in bugs if cells.get(b) == "FOUND"]
        crashed = [b for b in bugs if cells.get(b) == "crash?"]
        falsep = [b for b in bugs if cells.get(b) == "false+"]
        missed = [b for b in bugs if cells.get(b) == "miss"]
        skipped = [b for b in bugs if cells.get(b) == "skip" or b not in cells]
        lines.append(f"### {t}")
        lines.append("")
        lines.append(f"- FOUND ({len(found)}): {', '.join(found) or '(none)'}")
        lines.append(f"- crash? ({len(crashed)}): {', '.join(crashed) or '(none)'}")
        lines.append(f"- miss ({len(missed)}): {', '.join(missed) or '(none)'}")
        if falsep:
            lines.append(f"- false+ ({len(falsep)}): {', '.join(falsep)}")
        if skipped:
            lines.append(f"- skip ({len(skipped)}): {', '.join(skipped)}")
        lines.append("")

    if skip_reasons:
        lines.append("## Skip reasons")
        lines.append("")
        lines.append("Each skip below is a cell the tool could not exercise. The reason")
        lines.append("is recorded verbatim from the driver's `error` field (install or")
        lines.append("build failure) or, when the driver had no explicit error, the")
        lines.append("cell's `notes`.")
        lines.append("")
        lines.append("| tool | bug | reason |")
        lines.append("| :-- | :-- | :-- |")
        for (t, b) in sorted(skip_reasons.keys()):
            reason = skip_reasons[(t, b)].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {t} | {b} | {reason} |")
        lines.append("")

    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] {len(records)} records -> {args.out}")


if __name__ == "__main__":
    main()
