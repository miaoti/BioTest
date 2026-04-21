#!/usr/bin/env python3
"""Emit a Markdown summary of which bugs each tool found in Chat 5.

Reads <bench_root>/aggregate.json (produced by rollup_bug_bench.py),
writes a human-readable per-tool bug matrix to <out>.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BUGS = [
    ("biopython-4825", "biopython"),
    ("seqan3-2418", "seqan3"),
    ("seqan3-3081", "seqan3"),
    ("seqan3-3269", "seqan3"),
    ("seqan3-3098", "seqan3"),
    ("seqan3-2869", "seqan3"),
    ("seqan3-3406", "seqan3"),
]

MATRIX = {
    "biopython": ["atheris", "pure_random"],
    "seqan3": ["libfuzzer", "pure_random"],
}
TOOLS = ["atheris", "libfuzzer", "pure_random"]


def cell(records_by_key: dict, tool: str, bug: str, sut: str) -> str:
    if tool not in MATRIX[sut]:
        return "n/a"
    r = records_by_key.get((tool, bug))
    if r is None:
        return "—"
    if r.get("install_error") or r.get("error") or r.get("skipped"):
        return "skip"
    detected = r.get("detected")
    confirmed = r.get("confirmed_fix_silences_signal")
    if detected and confirmed is True:
        return "FOUND"
    if detected and confirmed is None:
        return "crash?"
    if detected and confirmed is False:
        return "false+"
    return "miss"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    agg_path = args.bench_root / "aggregate.json"
    agg = json.loads(agg_path.read_text(encoding="utf-8"))
    records = agg.get("results", agg if isinstance(agg, list) else [])
    by = {(r.get("tool"), r.get("bug_id")): r for r in records}

    lines: list[str] = []
    lines.append("# Chat 5 — biopython + seqan3 SAM bug-bench results")
    lines.append("")
    lines.append(f"- cells recorded: {len(records)}")
    lines.append("- tools: atheris (biopython) / libfuzzer (seqan3) / pure_random (both)")
    lines.append("- biotest excluded by operator for this run")
    lines.append("")
    lines.append("## Legend")
    lines.append("- **FOUND** — tool produced a trigger that fires pre-fix and is silenced by post-fix")
    lines.append("- **crash?** — tool crashed pre-fix but post-fix replay inconclusive (null)")
    lines.append("- **false+** — tool crashed pre-fix but post-fix still crashes — likely unrelated")
    lines.append("- **miss** — tool ran but did not detect the bug")
    lines.append("- **skip** — cell was skipped (install failure, harness-skew, etc.)")
    lines.append("- **n/a** — tool is not applicable for this SUT in the driver MATRIX")
    lines.append("- **—** — no record written for this cell")
    lines.append("")
    lines.append("## Per-bug × tool matrix")
    lines.append("")
    header = "| bug | sut | " + " | ".join(TOOLS) + " |"
    sep = "| :-- | :-- | " + " | ".join([":--"] * len(TOOLS)) + " |"
    lines.append(header)
    lines.append(sep)
    for bug, sut in BUGS:
        row = [bug, sut] + [cell(by, t, bug, sut) for t in TOOLS]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    lines.append("## Per-tool bugs found")
    lines.append("")
    for tool in TOOLS:
        buckets: dict[str, list[str]] = {"FOUND": [], "crash?": [], "miss": [], "skip": [], "false+": []}
        for bug, sut in BUGS:
            v = cell(by, tool, bug, sut)
            if v in buckets:
                buckets[v].append(bug)
        lines.append(f"### {tool}")
        lines.append(f"- FOUND ({len(buckets['FOUND'])}): " + (", ".join(buckets["FOUND"]) or "(none)"))
        lines.append(f"- crash? ({len(buckets['crash?'])}): " + (", ".join(buckets["crash?"]) or "(none)"))
        lines.append(f"- miss ({len(buckets['miss'])}): " + (", ".join(buckets["miss"]) or "(none)"))
        lines.append(f"- skip ({len(buckets['skip'])}): " + (", ".join(buckets["skip"]) or "(none)"))
        if buckets["false+"]:
            lines.append(f"- false+ ({len(buckets['false+'])}): " + ", ".join(buckets["false+"]))
        lines.append("")

    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[chat5-report] wrote {args.out} ({len(records)} records)")


if __name__ == "__main__":
    main()
