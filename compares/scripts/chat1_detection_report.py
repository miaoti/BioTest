#!/usr/bin/env python3
"""Chat 1 detection report — emits a Markdown summary of per-tool findings."""
import argparse
import json
from pathlib import Path


BUGS = [
    "htsjdk-1554", "htsjdk-1637", "htsjdk-1364", "htsjdk-1389",
    "htsjdk-1372", "htsjdk-1401", "htsjdk-1403", "htsjdk-1418",
    "htsjdk-1544",
]
TOOLS = ["jazzer", "pure_random", "evosuite_anchor"]


def classify(r: dict) -> str:
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
    args = p.parse_args()

    agg = json.loads((args.bench_root / "aggregate.json").read_text())
    manifest = {}
    rm = args.bench_root / "run_manifest.json"
    if rm.exists():
        manifest = json.loads(rm.read_text())
    records = agg["results"]
    by = {(r.get("tool"), r.get("bug_id")): r for r in records}

    def cell(tool: str, bug: str) -> str:
        r = by.get((tool, bug))
        if r is None:
            return "—"
        return classify(r)

    L = []
    L.append("# Chat 1 — htsjdk VCF bug-bench detections")
    L.append("")
    L.append(f"- git_sha: `{manifest.get('git_sha', '?')}`")
    L.append(f"- budget_s: {manifest.get('budget_s', '?')}")
    L.append(f"- ended_at: {manifest.get('ended_at', '?')}")
    L.append(f"- scope: {manifest.get('scope', '?')}")
    L.append(f"- total cells: {len(records)} (9 bugs × {len(TOOLS)} tools = {9*len(TOOLS)})")
    L.append("")
    L.append("## Legend")
    L.append("")
    L.append("- **FOUND** — tool produced a trigger that crashes pre-fix and is silenced by post-fix (real detection)")
    L.append("- **crash?** — tool crashed pre-fix but post-fix replay was inconclusive (null)")
    L.append("- **false+** — tool crashed pre-fix but post-fix STILL crashes (likely unrelated bug)")
    L.append("- **miss** — tool ran to budget without finding the bug")
    L.append("- **skip** — cell skipped (install failure, etc.)")
    L.append("")

    L.append("## Per-bug matrix")
    L.append("")
    L.append("| bug | " + " | ".join(TOOLS) + " |")
    L.append("| :-- | " + " | ".join([":--"] * len(TOOLS)) + " |")
    for bug in BUGS:
        L.append(f"| {bug} | " + " | ".join(cell(t, bug) for t in TOOLS) + " |")
    L.append("")

    L.append("## Per-tool bugs found")
    L.append("")
    for tool in TOOLS:
        buckets = {"FOUND": [], "crash?": [], "false+": [], "miss": [], "skip": []}
        for bug in BUGS:
            c = cell(tool, bug)
            if c in buckets:
                buckets[c].append(bug)
        L.append(f"### {tool}")
        L.append("")
        L.append(f"- **FOUND** ({len(buckets['FOUND'])}): {', '.join(buckets['FOUND']) or '_(none)_'}")
        if buckets["crash?"]:
            L.append(f"- crash? ({len(buckets['crash?'])}): {', '.join(buckets['crash?'])}")
        if buckets["false+"]:
            L.append(f"- false+ ({len(buckets['false+'])}): {', '.join(buckets['false+'])}")
        L.append(f"- miss ({len(buckets['miss'])}): {', '.join(buckets['miss']) or '_(none)_'}")
        if buckets["skip"]:
            L.append(f"- skip ({len(buckets['skip'])}): {', '.join(buckets['skip'])}")
        L.append("")

    detected_counts = {
        t: sum(1 for b in BUGS if cell(t, b) == "FOUND") for t in TOOLS
    }
    L.append("## Summary")
    L.append("")
    L.append("| tool | FOUND / total |")
    L.append("| :-- | :-- |")
    for t in TOOLS:
        L.append(f"| {t} | {detected_counts[t]} / {len(BUGS)} |")
    L.append("")

    args.out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"[report] wrote {args.out} — FOUND counts: {detected_counts}")


if __name__ == "__main__":
    main()
