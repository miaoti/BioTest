#!/usr/bin/env python3
"""Render a per-tool bugs-found markdown report from a bug-bench tree.

Usage:
    python3 bug_bench_markdown_report.py \
        --bench-root /tmp/bug_bench_chat4 \
        --out /tmp/bug_bench_chat4/report.md \
        [--only-sut noodles]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _cell(by: dict, tool: str, bug: str) -> str:
    r = by.get((tool, bug))
    if r is None:
        return "—"
    err = r.get("install_error") or r.get("error")
    if err:
        return "skip"
    det = r.get("detected")
    conf = r.get("confirmed_fix_silences_signal")
    if det and conf is True:
        return "FOUND"
    if det and conf is None:
        return "crash?"
    if det and conf is False:
        return "false+"
    return "miss"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--only-sut", default=None,
                   help="Filter to this SUT (e.g. noodles)")
    p.add_argument("--title", default=None,
                   help="Report title; default derived from bench-root")
    args = p.parse_args()

    agg_path = args.bench_root / "aggregate.json"
    agg = json.loads(agg_path.read_text(encoding="utf-8"))
    records = agg["results"]

    if args.only_sut:
        records = [r for r in records if r.get("sut") == args.only_sut]

    bugs: list[str] = []
    tools: list[str] = []
    for r in records:
        b = r.get("bug_id")
        t = r.get("tool")
        if b and b not in bugs:
            bugs.append(b)
        if t and t not in tools:
            tools.append(t)
    bugs.sort()
    tools.sort()

    by = {(r["tool"], r["bug_id"]): r for r in records}

    title = args.title or f"Bug-bench report — {args.bench_root.name}"
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- cells: {len(records)}")
    if args.only_sut:
        lines.append(f"- sut: {args.only_sut}")
    lines.append(f"- tools: {', '.join(tools)}")
    lines.append(f"- bugs: {len(bugs)}")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("- **FOUND**: tool produced a trigger that crashed pre-fix "
                 "and is silenced by post-fix (the canonical detection).")
    lines.append("- **crash?**: tool crashed pre-fix but post-fix replay "
                 "was inconclusive (confirmed_fix_silences_signal == null).")
    lines.append("- **false+**: tool crashed pre-fix but post-fix still "
                 "crashes — likely an unrelated bug, not the target.")
    lines.append("- **miss**: tool ran to completion without finding the bug.")
    lines.append("- **skip**: cell skipped (install failure, harness-skew, "
                 "etc.). See `install_error` in result.json.")
    lines.append("- **—**: (tool, bug) pair was not in the matrix.")
    lines.append("")

    lines.append("## Per-bug matrix")
    lines.append("")
    header = "| bug | " + " | ".join(tools) + " |"
    sep = "| :-- | " + " | ".join([":--"] * len(tools)) + " |"
    lines.append(header)
    lines.append(sep)
    for bug in bugs:
        row = f"| {bug} | " + " | ".join(_cell(by, t, bug) for t in tools) + " |"
        lines.append(row)
    lines.append("")

    lines.append("## Per-tool bugs found")
    lines.append("")
    for tool in tools:
        found = [b for b in bugs if _cell(by, tool, b) == "FOUND"]
        crashed = [b for b in bugs if _cell(by, tool, b) == "crash?"]
        missed = [b for b in bugs if _cell(by, tool, b) == "miss"]
        skipped = [b for b in bugs if _cell(by, tool, b) == "skip"]
        falsep = [b for b in bugs if _cell(by, tool, b) == "false+"]
        lines.append(f"### {tool}")
        lines.append("")
        lines.append(f"- **FOUND ({len(found)})**: "
                     f"{', '.join(found) if found else '(none)'}")
        if crashed:
            lines.append(f"- crash? ({len(crashed)}): {', '.join(crashed)}")
        if falsep:
            lines.append(f"- false+ ({len(falsep)}): {', '.join(falsep)}")
        lines.append(f"- miss ({len(missed)}): "
                     f"{', '.join(missed) if missed else '(none)'}")
        lines.append(f"- skip ({len(skipped)}): "
                     f"{', '.join(skipped) if skipped else '(none)'}")
        lines.append("")

    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[report] wrote {args.out}")


if __name__ == "__main__":
    main()
