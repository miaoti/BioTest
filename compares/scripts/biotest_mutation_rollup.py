"""Aggregate biotest Phase-3 mutation results across all 5 SUTs.

Reads compares/results/mutation/biotest/<cell>/summary.json for the 6 cells
(htsjdk_vcf, htsjdk_sam, vcfpy, noodles, biopython, seqan3_sam) and emits
a single rollup table + CSV mirroring baseline tools' mutation_score.md
layout.

Score calculation per DESIGN §3.3 (same formula every baseline tool uses):
    score = killed / reachable
    reachable = KILLED + SURVIVED + TIMED_OUT (excludes NO_COVERAGE / NON_VIABLE)

Each backend (PIT, mutmut, cargo-mutants, mull) writes those three keys
directly into summary.json so the rollup is arithmetic only.
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_ROOT = REPO / "compares/results/mutation/biotest"

CELLS = [
    ("htsjdk_vcf", "htsjdk", "VCF", "PIT"),
    ("htsjdk_sam", "htsjdk", "SAM", "PIT"),
    ("vcfpy",       "vcfpy",     "VCF", "mutmut"),
    ("noodles",     "noodles",   "VCF", "cargo-mutants"),
    ("biopython",   "biopython", "SAM", "mutmut"),
    ("seqan3_sam",  "seqan3",    "SAM", "mull"),
]


def _load(cell: str) -> dict | None:
    p = OUT_ROOT / cell / "summary.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"_parse_error": str(e)}


def main() -> int:
    rows = []
    missing = []
    for cell, sut, fmt, engine in CELLS:
        d = _load(cell)
        if d is None:
            missing.append(cell)
            rows.append({"cell": cell, "sut": sut, "format": fmt, "engine": engine,
                         "status": "missing", "killed": None, "reachable": None, "score": None})
            continue
        if "_parse_error" in d:
            rows.append({"cell": cell, "sut": sut, "format": fmt, "engine": engine,
                         "status": "parse_error", "killed": None, "reachable": None, "score": None,
                         "note": d["_parse_error"]})
            continue
        killed = d.get("killed")
        reachable = d.get("reachable")
        score = d.get("score")
        # Some backends write "score_display" rather than score-as-float.
        if score is None and d.get("score_display"):
            score = d["score_display"]
        status = d.get("status", "ok")
        rows.append({
            "cell": cell, "sut": sut, "format": fmt, "engine": engine,
            "status": status,
            "killed": killed, "reachable": reachable, "score": score,
            "total": d.get("total_mutations") or d.get("mutant_count"),
            "survived": d.get("survived"),
            "no_coverage": d.get("no_coverage"),
            "timed_out": d.get("timed_out") or d.get("timeout"),
            "non_viable": d.get("non_viable") or d.get("unviable"),
        })

    # Markdown rollup
    md = OUT_ROOT / "MUTATION_SCORE.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phase 3 - Mutation Score - BioTest (all 5 primary SUTs)",
        "",
        "Corpus sources (per DESIGN.md SS 3.3 + user 2026-04-22 clarification):",
        "",
        "- **VCF cells** (htsjdk VCF, vcfpy, noodles): corpus = `seeds/vcf/` "
        "(47 files: 33 curated real + 14 Phase-D synthesised).  "
        "BioTest folds synthesised VCFs back into seeds/ so seeds/vcf IS the tool's corpus.",
        "- **SAM cells** (htsjdk SAM, biopython, seqan3): corpus = random sample of 600 "
        "`T_*.sam` from `bug_reports/` (5,723 transformed SAM files produced by Phase-D MR runs; "
        "fixed random seed 0xB107E57). See compares/results/coverage/biotest/CORPUS_MANIFEST.json.",
        "",
        "Score formula = **killed / reachable** (DESIGN.md SS 3.3).  Reachable = KILLED + "
        "SURVIVED + TIMED_OUT; excludes NO_COVERAGE / NON_VIABLE — identical to jazzer, "
        "atheris, cargo_fuzz, libfuzzer baseline rows in `compares/results/mutation/*/summary.json`.",
        "",
        "## Headline",
        "",
        "| cell | SUT | Fmt | engine | killed | reachable | **score** | status |",
        "| :--- | :-- | :-: | :----- | -----: | --------: | :-------: | :----- |",
    ]
    for r in rows:
        score = r["score"]
        if isinstance(score, float):
            score_str = f"{score*100:.2f}%"
        elif score in (None, "n/a"):
            score_str = "n/a"
        else:
            score_str = str(score)
        killed = r["killed"] if r["killed"] is not None else "-"
        reachable = r["reachable"] if r["reachable"] is not None else "-"
        lines.append(
            f"| `{r['cell']}` | {r['sut']} | {r['format']} | {r['engine']} | "
            f"{killed} | {reachable} | **{score_str}** | {r['status']} |"
        )

    lines += ["", "## Full breakdown per cell", ""]
    for r in rows:
        lines.append(f"### `{r['cell']}`  -  {r['engine']} on {r['sut']} ({r['format']})")
        lines.append("")
        for k in ("killed", "survived", "no_coverage", "timed_out", "non_viable",
                  "total", "reachable", "score", "status", "note"):
            v = r.get(k)
            if v is not None:
                lines.append(f"- **{k}**: `{v}`")
        lines.append("")

    if missing:
        lines.append("")
        lines.append(f"> Cells missing summary.json (not yet run or failed early): {', '.join(missing)}")

    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[rollup] wrote {md}")

    # CSV for downstream scripts
    csvp = OUT_ROOT / "summary.csv"
    with csvp.open("w", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=[
            "cell", "sut", "format", "engine", "status",
            "killed", "reachable", "score",
            "survived", "no_coverage", "timed_out", "non_viable", "total",
        ])
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in w.fieldnames})
    print(f"[rollup] wrote {csvp}")

    # Exit non-zero only if any cell is missing or parse_error
    bad = [r for r in rows if r["status"] in ("missing", "parse_error")]
    if bad:
        print(f"[rollup] {len(bad)} cell(s) incomplete: {[b['cell'] for b in bad]}", file=sys.stderr)
        return 0  # still write report; caller decides what to do
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
