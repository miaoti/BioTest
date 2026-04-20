"""Render a markdown catalogue of every bug in manifest.verified.json.

Produces `compares/bug_bench/CATALOGUE.md` with one section per SUT,
one subsection per bug, enough detail that a paper reader can
understand what each bug is, how to reproduce it, and which signal
the bench driver listens for. Useful as the authoritative per-bug
reference and as source material for DESIGN.md §13.4.7.
"""

from __future__ import annotations

import json
import pathlib

BENCH = pathlib.Path(__file__).resolve().parent
MANIFEST = BENCH / "manifest.verified.json"
CATALOGUE = BENCH / "CATALOGUE.md"


def main() -> int:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lines: list[str] = []
    lines.append("# Verified Bug Catalogue")
    lines.append("")
    lines.append(f"**Generated from**: `{MANIFEST.name}`")
    lines.append(f"**Total bugs**: {len(m['bugs'])}")
    lines.append(f"**By SUT**: " +
                 "  ·  ".join(f"{k} {v}" for k, v in
                               m["bench_counts_by_sut"].items()))
    lines.append("")
    lines.append("Single-source-of-truth reference for every bug the "
                 "Phase-4 bench driver will run. Edit `manifest.verified.json` "
                 "and regenerate this file via "
                 "`python compares/bug_bench/render_catalogue.py`.")
    lines.append("")

    for sut in ("htsjdk", "pysam", "biopython", "seqan3"):
        bugs = [b for b in m["bugs"] if b["sut"] == sut]
        if not bugs:
            continue
        lines.append(f"## {sut} ({len(bugs)} bugs)")
        lines.append("")
        for b in bugs:
            lines.extend(_render_bug(b))
            lines.append("")
    CATALOGUE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[catalogue] wrote {CATALOGUE.name} ({len(m['bugs'])} bugs)")
    return 0


def _render_bug(bug: dict) -> list[str]:
    a = bug["anchor"]
    t = bug["trigger"]
    s = bug["expected_signal"]
    lines: list[str] = []
    lines.append(f"### `{bug['id']}` — {bug['format']}")
    lines.append("")
    lines.append(f"- **Issue / PR**: {bug['issue_url']}")
    lines.append(f"- **Anchor**: `{a.get('type')}` — "
                 f"pre-fix `{a.get('pre_fix')}` → post-fix `{a.get('post_fix')}`")
    lines.append(f"- **Confidence**: {a.get('confidence', 'unknown')}")
    lines.append(f"- **Category**: `{t.get('category')}` "
                 f"{'(logic bug)' if t.get('logic_bug') else '(crash / rejection)'}")
    lines.append(f"- **Expected signal**: `{s.get('type')}` "
                 f"against {', '.join(s.get('against', [])) or 'pre-fix SUT'}")
    also = s.get("also_detectable_via")
    if also:
        lines.append(f"- **Also detectable via**: {', '.join(also)}")
    lines.append(f"- **Trigger folder**: `{t.get('evidence_dir', '')}`")
    lines.append("")
    lines.append(f"{t.get('description', '')}")
    lines.append("")
    lines.append(f"*Verification rule*: {a.get('verification_rule', '—')}")
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
