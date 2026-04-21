#!/usr/bin/env python3
"""Generate a markdown report summarising which bugs each tool found.

Reads <bench_root>/aggregate.json and emits a per-bug × per-tool matrix
plus a per-tool bug list. Written for Chat 3 of the Phase 4 real-bug
benchmark (vcfpy VCF × {atheris, pure_random}; biotest excluded by
operator). Script is chat-agnostic — pass --bench-root and --bugs and
--tools to reuse for other chats.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


CHAT3_BUGS = [
    "vcfpy-176",
    "vcfpy-171",
    "vcfpy-146",
    "vcfpy-145",
    "vcfpy-gtone-0.13",
    "vcfpy-127",
    "vcfpy-nocall-0.8",
]
CHAT3_TOOLS = ["atheris", "pure_random"]


def classify(rec: dict) -> str:
    if rec is None:
        return "-"
    err = rec.get("install_error") or rec.get("error")
    if err:
        return "skip"
    detected = bool(rec.get("detected"))
    conf = rec.get("confirmed_fix_silences_signal")
    if detected and conf is True:
        return "FOUND"
    if detected and conf is None:
        return "crash?"
    if detected and conf is False:
        return "false+"
    return "miss"


def render(bench_root: Path, bugs: list[str], tools: list[str]) -> str:
    agg = json.loads((bench_root / "aggregate.json").read_text(encoding="utf-8"))
    records = agg.get("results", [])
    by: dict[tuple[str, str], dict] = {(r["tool"], r["bug_id"]): r for r in records}

    rm_path = bench_root / "run_manifest.json"
    rm = json.loads(rm_path.read_text(encoding="utf-8")) if rm_path.exists() else {}

    lines: list[str] = []
    lines.append(f"# {bench_root.name} - bug-bench results")
    lines.append("")
    lines.append(f"- cells recorded: {len(records)}")
    lines.append(f"- tools: {', '.join(tools)} (biotest excluded by operator)")
    lines.append(f"- bugs: {len(bugs)} vcfpy")
    if rm:
        lines.append(f"- budget_s: {rm.get('budget_s')}")
        lines.append(f"- ended_at: {rm.get('ended_at')}")
        lines.append(f"- git_sha: {rm.get('git_sha')}")
    lines.append("")

    lines.append("## Legend")
    lines.append("- **FOUND**: tool produced a trigger that crashed pre-fix and is silenced by post-fix")
    lines.append("- **crash?**: tool crashed pre-fix but post-fix replay inconclusive (null)")
    lines.append("- **false+**: tool crashed pre-fix but post-fix STILL crashes (likely unrelated)")
    lines.append("- **miss**: tool ran the full budget without finding the bug")
    lines.append("- **skip**: cell skipped (install failed, harness-skew, etc.)")
    lines.append("- **-**: no record written")
    lines.append("")

    lines.append("## Per-bug x per-tool matrix")
    lines.append("")
    header = ["bug"] + tools
    sep = [":--"] + [":--:"] * len(tools)
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(sep) + " |")
    for bug in bugs:
        row = [bug] + [classify(by.get((t, bug))) for t in tools]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Per-tool bug lists")
    lines.append("")
    for tool in tools:
        cells = {bug: classify(by.get((tool, bug))) for bug in bugs}
        found = [b for b, v in cells.items() if v == "FOUND"]
        crashed = [b for b, v in cells.items() if v == "crash?"]
        missed = [b for b, v in cells.items() if v == "miss"]
        skipped = [b for b, v in cells.items() if v == "skip"]
        falsep = [b for b, v in cells.items() if v == "false+"]
        lines.append(f"### {tool}")
        lines.append(f"- FOUND ({len(found)}): {', '.join(found) if found else '(none)'}")
        if crashed:
            lines.append(f"- crash? ({len(crashed)}): {', '.join(crashed)}")
        lines.append(f"- miss ({len(missed)}): {', '.join(missed) if missed else '(none)'}")
        if skipped:
            lines.append(f"- skip ({len(skipped)}): {', '.join(skipped)}")
        if falsep:
            lines.append(f"- false+ ({len(falsep)}): {', '.join(falsep)}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--bugs", nargs="+", default=CHAT3_BUGS)
    p.add_argument("--tools", nargs="+", default=CHAT3_TOOLS)
    args = p.parse_args()
    md = render(args.bench_root, args.bugs, args.tools)
    args.out.write_text(md, encoding="utf-8")
    print(f"[report] wrote {args.out}")


if __name__ == "__main__":
    main()
