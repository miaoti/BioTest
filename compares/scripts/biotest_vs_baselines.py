"""Side-by-side BioTest vs baselines mutation-score comparison.

Reads each baseline's summary.json + biotest's summary.json and emits
a per-cell comparison table. "Same calculation" is enforced by reading
killed/reachable/score keys that every backend writes using the identical
DESIGN §3.3 formula.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "compares/results/mutation"

# (sut, fmt, engine, baseline_path, biotest_path)
CELLS = [
    ("htsjdk",    "VCF", "PIT",           "jazzer/htsjdk_vcf/summary.json",  "biotest/htsjdk_vcf/summary.json"),
    ("htsjdk",    "SAM", "PIT",           "jazzer/htsjdk_sam/summary.json",  "biotest/htsjdk_sam/summary.json"),
    ("vcfpy",     "VCF", "mutmut",        "atheris/vcfpy/summary.json",      "biotest/vcfpy/summary.json"),
    ("noodles",   "VCF", "cargo-mutants", "cargo_fuzz/noodles/summary.json", "biotest/noodles/summary.json"),
    ("biopython", "SAM", "mutmut",        "atheris/biopython/rep_0_run/summary_scoped.json", "biotest/biopython/summary.json"),
    ("seqan3",    "SAM", "mull",          "libfuzzer/seqan3_sam/summary.json", "biotest/seqan3_sam/summary.json"),
]


def _load(p: Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _pull(d):
    if d is None:
        return None, None, None
    # Canonical fields first, then fall back to nested mutation_score block
    # (phase3_mutation_loop writes the latter shape).
    k = d.get("killed")
    r = d.get("reachable")
    s = d.get("score")
    if k is None or r is None:
        ms = d.get("mutation_score") or {}
        k = k if k is not None else ms.get("killed")
        r = r if r is not None else ms.get("reachable")
        s = s if s is not None else ms.get("score")
    return k, r, s


def main() -> int:
    lines = [
        "# BioTest vs Baselines — Phase 3 Mutation Score",
        "",
        "Same calculation every row (DESIGN §3.3): `score = killed / reachable`.",
        "For biopython, the reached-lines-only rescope is used on both sides so they're apples-to-apples.",
        "",
        "| SUT | Fmt | engine | baseline tool | baseline k/r | baseline score | biotest k/r | biotest score | Δ (pp) |",
        "| :-- | :-: | :----- | :------------ | -----------: | :------------: | ----------: | :-----------: | -----: |",
    ]
    rows = []
    for sut, fmt, eng, bp, tp in CELLS:
        baseline_path = ROOT / bp
        biotest_path = ROOT / tp
        baseline = _load(baseline_path)
        biotest = _load(biotest_path)
        bk, br, bs = _pull(baseline)
        tk, tr, ts = _pull(biotest)
        baseline_tool = baseline.get("tool", "?") if baseline else "?"
        bscore_str = f"{bs*100:.2f}%" if isinstance(bs, float) else "n/a"
        tscore_str = f"{ts*100:.2f}%" if isinstance(ts, float) else "n/a"
        if isinstance(bs, float) and isinstance(ts, float):
            delta_pp = f"{(ts - bs)*100:+.2f}"
        else:
            delta_pp = "—"
        bkr = f"{bk}/{br}" if bk is not None else "—"
        tkr = f"{tk}/{tr}" if tk is not None else "—"
        lines.append(f"| {sut} | {fmt} | {eng} | {baseline_tool} | {bkr} | {bscore_str} | {tkr} | {tscore_str} | {delta_pp} |")
        rows.append((sut, fmt, eng, baseline_tool, bk, br, bs, tk, tr, ts))

    # Narrative sidebar
    lines += [
        "",
        "### What's comparable and what's not",
        "",
        "- **Same engine per row**: PIT, mutmut, cargo-mutants, mull — the BioTest cell uses the identical tool the baseline cell used. Only the corpus differs.",
        "- **Same target scope**: `biotest_config.yaml:coverage.target_filters` is the single source for class/package scope; both sides see the same denominator definition.",
        "- **Corpus sizes differ by tool paradigm**:",
        "    - BioTest VCF: 47 real-world seed files (BioTest's Phase-D corpus lives in `seeds/vcf/`).",
        "    - BioTest SAM: 600 `T_*.sam` transformed files sampled from 5,723 `bug_reports/*/T_*.sam`.",
        "    - Jazzer VCF: 200 files unioned from 3 reps (4,184 total deduped).",
        "    - Jazzer SAM: 150 files unioned from 3 reps.",
        "    - Atheris vcfpy: 1,025 files unioned from 3 reps.",
        "    - Atheris biopython: rep-0 fuzz corpus.",
        "    - cargo-fuzz noodles: rep-0 corpus.",
        "    - libfuzzer seqan3: rep-0 corpus (120 sampled).",
        "- **Reachable is what matters**: a smaller corpus that happens to hit more lines produces a larger `reachable` denominator, which drives the score calculus — not the raw file count.",
        "",
        "### Observations",
        "",
    ]

    # Per-row one-liners
    for sut, fmt, eng, btool, bk, br, bs, tk, tr, ts in rows:
        if isinstance(bs, float) and isinstance(ts, float):
            delta = (ts - bs) * 100
            sign = "+" if delta >= 0 else ""
            lines.append(f"- **{sut} ({fmt})**: biotest {tk}/{tr} = {ts*100:.2f}% vs {btool} {bk}/{br} = {bs*100:.2f}%  ({sign}{delta:.2f}pp)")
        else:
            lines.append(f"- **{sut} ({fmt})**: biotest or baseline data missing ({eng})")

    out = REPO / "compares/results/mutation/biotest/BIOTEST_VS_BASELINES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[vs-baselines] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
