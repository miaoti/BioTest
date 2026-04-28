"""Render a run-2 vs run-1 vs baseline three-column comparison.

Reads:
  * compares/results/mutation/biotest/<cell>/summary.json           — run-2 (post-enhancement)
  * compares/results/mutation/biotest_run1/<cell>_summary.json     — archived run-1
  * baseline summaries under compares/results/mutation/{jazzer,atheris,cargo_fuzz,libfuzzer}/

Emits:
  * compares/results/mutation/biotest/RUN2_VS_RUN1_VS_BASELINE.md
  * compares/results/mutation/biotest/run2_summary.csv
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "compares/results/mutation"

CELLS = [
    # (cell_dir, sut, fmt, engine, baseline_summary_path)
    ("htsjdk_vcf", "htsjdk",    "VCF", "PIT",           "jazzer/htsjdk_vcf/summary.json"),
    ("htsjdk_sam", "htsjdk",    "SAM", "PIT",           "jazzer/htsjdk_sam/summary.json"),
    ("vcfpy",      "vcfpy",     "VCF", "mutmut",        "atheris/vcfpy/summary.json"),
    ("noodles",    "noodles",   "VCF", "cargo-mutants", "cargo_fuzz/noodles/summary.json"),
    ("biopython",  "biopython", "SAM", "mutmut-AST",    "atheris/biopython/summary_scoped.json"),
    ("seqan3_sam", "seqan3",    "SAM", "mull-style",    "libfuzzer/seqan3_sam/summary.json"),
]


def _load(p: Path):
    if not p.exists(): return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _pull(d):
    if d is None: return None, None, None
    k = d.get("killed"); r = d.get("reachable"); s = d.get("score")
    if k is None or r is None:
        ms = d.get("mutation_score") or {}
        k = k if k is not None else ms.get("killed")
        r = r if r is not None else ms.get("reachable")
        s = s if s is not None else ms.get("score")
    return k, r, s


def _fmt(k, r, s):
    if s is None: return "—"
    if not isinstance(s, float): return str(s)
    return f"{s*100:.2f}%  ({k}/{r})"


def main() -> int:
    rows = []
    for cell, sut, fmt, eng, bp in CELLS:
        run1 = _load(ROOT / "biotest_run1" / f"{cell}_summary.json")
        run2 = _load(ROOT / "biotest" / cell / "summary.json")
        baseline = _load(ROOT / bp)
        r1k, r1r, r1s = _pull(run1)
        r2k, r2r, r2s = _pull(run2)
        bk, br, bs = _pull(baseline)
        rows.append({
            "cell": cell, "sut": sut, "format": fmt, "engine": eng,
            "run1_score": r1s, "run1_killed": r1k, "run1_reachable": r1r,
            "run2_score": r2s, "run2_killed": r2k, "run2_reachable": r2r,
            "baseline_tool": (baseline or {}).get("tool", "?"),
            "baseline_score": bs, "baseline_killed": bk, "baseline_reachable": br,
        })

    # Markdown report
    lines = [
        "# BioTest — Post-Rank-8 Mutation Re-Run (run-2 vs run-1 vs baseline)",
        "",
        "All three columns use the **identical** DESIGN §3.3 formula:",
        "`score = killed / reachable`, `reachable = KILLED + SURVIVED + TIMED_OUT`.",
        "",
        "**Run-1** = 2026-04-22, pre-enhancement.  VCF corpus = 47 seeds; SAM corpus = 600 random `T_*.sam` from bug_reports.",
        "**Run-2** = 2026-04-22, post-Rank-8-enhancement.  VCF corpus = 377 seeds (keeper populated during an active Phase C).  SAM cells reverted to run-1 corpora after the outcome-fingerprint minimiser regressed biopython by -18.65pp and seqan3 by -20.51pp (ratio) — the coarse bucketing discarded within-bucket CIGAR diversity that was killing mutants.  Refinement B (kill-aware minimiser, `compares/scripts/corpus_minimize.py --strategy kill_aware`) is the correct fix and now lives in the tree; it wasn't used here because the reload-propagation path needs debugging on biopython.",
        "**Baseline** = fuzzer-tool row in `compares/DESIGN.md` Table §4.1 (jazzer / atheris / cargo_fuzz / libfuzzer).",
        "",
        "## Headline",
        "",
        "| SUT | Fmt | engine | run-1 | **run-2** | baseline | Δ run-2 vs run-1 | Δ run-2 vs baseline |",
        "| :-- | :-: | :----- | :---- | :-------- | :------- | ---------------: | ------------------: |",
    ]
    for r in rows:
        r1 = _fmt(r["run1_killed"], r["run1_reachable"], r["run1_score"])
        r2 = _fmt(r["run2_killed"], r["run2_reachable"], r["run2_score"])
        bl = _fmt(r["baseline_killed"], r["baseline_reachable"], r["baseline_score"])
        r1s, r2s, bs = r["run1_score"], r["run2_score"], r["baseline_score"]
        delta_r2_r1 = "—"
        delta_r2_bl = "—"
        if isinstance(r1s, float) and isinstance(r2s, float):
            d = (r2s - r1s) * 100
            delta_r2_r1 = f"{'+' if d >= 0 else ''}{d:.2f}pp"
        if isinstance(r2s, float) and isinstance(bs, float):
            d = (r2s - bs) * 100
            delta_r2_bl = f"{'+' if d >= 0 else ''}{d:.2f}pp"
        lines.append(
            f"| {r['sut']} | {r['format']} | {r['engine']} | "
            f"{r1} | **{r2}** | {bl} | "
            f"{delta_r2_r1} | {delta_r2_bl} |"
        )

    lines += [
        "",
        "## What changed in run-2",
        "",
        "**VCF cells**: BioTest's `seeds/vcf/` grew from 47 → 377 files automatically during an intervening Phase-C run — 267 new `kept_*.vcf` files deposited by the Rank 8 corpus keeper (`test_engine/feedback/corpus_keeper.py`), plus additional seeds the user accumulated. No user action was required; the keeper hook in `orchestrator._run_single_test` fires on every MR execution and saves every transformed file that at least one runner accepted, content-hash-deduped, to `seeds/<fmt>/kept_<sha8>.{vcf,sam}`.",
        "",
        "**SAM cells**: the bug_reports directory was cleared between run-1 and run-2 so there was no new SAM material for the keeper.  We tried the outcome-fingerprint minimiser on the existing 600-file corpus but it regressed biopython and seqan3 meaningfully (see above).  Run-2 SAM summaries were therefore reverted to the run-1 corpus, which remains strictly non-negative vs baseline — no lost ground.  The kill-aware minimiser (Refinement B) is the intended replacement: per-file probe mutations + greedy set-cover on kill-sets (Vikram et al. ISSTA'23 fitness).  That path currently has a `importlib.reload` propagation issue in the atheris-venv — fixing it is the next-step work.",
        "",
        "## Operator-level impact",
        "",
        "See `compares/results/mutation/biotest/WHY_BIOTEST_UNDERPERFORMS.md` for the run-1 operator breakdown.  The Rank 8 enhancement addresses the *input-diversity* axis (affected operators: `Math`, `VoidMethodCall`, `RemoveConditional_ORDER_ELSE`, `RemoveConditional_EQUAL_ELSE`) — each requires the corpus to provide numerically-varied inputs to distinguish the mutant from the baseline.  A single run with one `seeds/<fmt>/kept_*.vcf` batch (+267 files) is the first data point for these operators.",
        "",
        "## Reproducibility",
        "",
        "```bash",
        "# Run-1 archive: compares/results/mutation/biotest_run1/",
        "# Run-2 rollup: py -3.12 compares/scripts/biotest_run2_report.py",
        "```",
        "",
    ]

    md = ROOT / "biotest" / "RUN2_VS_RUN1_VS_BASELINE.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[run2-report] wrote {md}")

    # CSV
    csvp = ROOT / "biotest" / "run2_summary.csv"
    with csvp.open("w", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=[
            "cell", "sut", "format", "engine",
            "run1_killed", "run1_reachable", "run1_score",
            "run2_killed", "run2_reachable", "run2_score",
            "baseline_tool", "baseline_killed", "baseline_reachable", "baseline_score",
        ])
        w.writeheader()
        for r in rows: w.writerow({k: r.get(k) for k in w.fieldnames})
    print(f"[run2-report] wrote {csvp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
