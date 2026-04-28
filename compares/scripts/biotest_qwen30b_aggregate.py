#!/usr/bin/env python3
"""Aggregate the 6-cell × 4-rep BioTest qwen3-coder:30b sweep results.

Reads `compares/results/coverage/biotest_qwen30b_4rep_<date>/`
(produced by `biotest_qwen30b_6cell_runner.py`) AND
`compares/results/mutation/biotest_qwen30b_4rep_<date>/`
(produced by `biotest_qwen30b_6cell_mutation_runner.py`), collates
per-rep `measurement.json` files into mean ± std summaries, and
writes one Markdown table per metric:

    coverage_root / SUMMARY_coverage.md   — line %, mean ± std, per cell
    mutation_root / SUMMARY_mutation.md   — score %, mean ± std, per cell

Either root is optional; pass `--coverage-root` and/or
`--mutation-root` to point at your sweep dirs.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


def load_records(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not root.exists():
        return records
    for p in sorted(root.rglob("measurement.json")):
        try:
            records.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  skip {p}: {e}")
    return records


def group_by_cell(records: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for r in records:
        key = (r.get("sut", "?"), r.get("format", "?"))
        buckets.setdefault(key, []).append(r)
    return buckets


def coverage_summary(coverage_root: Path) -> str:
    records = load_records(coverage_root)
    if not records:
        return f"# Coverage summary\n\nNo measurement.json files found under {coverage_root}\n"
    buckets = group_by_cell(records)

    lines: list[str] = []
    lines.append("# BioTest — 6-cell × 4-rep coverage summary (mean ± std)")
    lines.append("")
    lines.append(
        "Each row reports end-of-Phase-D line coverage over 4 independent "
        "BioTest runs (qwen3-coder:30b via local Ollama, fresh state per "
        "rep, Tier-1+Tier-2 seeds only — no out-tool generated corpus). "
        "Measured through `biotest_config.yaml: coverage.target_filters`."
    )
    lines.append("")
    lines.append(f"Source: `{coverage_root.relative_to(Path.cwd()) if str(coverage_root).startswith(str(Path.cwd())) else coverage_root}`")
    lines.append("")
    lines.append("## Per-SUT line coverage")
    lines.append("")
    lines.append(
        "| SUT | Format | Reps | Mean line % | Std (pp) | Min | Max | "
        "Mean covered/total | Avg wall (s) | Status |"
    )
    lines.append(
        "|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|"
    )

    rows = []
    for (sut, fmt), reps in sorted(buckets.items()):
        pcts = [float(r.get("line_pct", 0.0)) for r in reps]
        covered = [int(r.get("covered", 0)) for r in reps]
        totals = [int(r.get("total", 0)) for r in reps]
        wall = [float(r.get("elapsed_s", 0.0)) for r in reps]
        mean_p = statistics.fmean(pcts) if pcts else 0.0
        std_p = statistics.stdev(pcts) if len(pcts) >= 2 else 0.0
        min_p = min(pcts) if pcts else 0.0
        max_p = max(pcts) if pcts else 0.0
        mean_cov = round(statistics.fmean(covered)) if covered else 0
        mean_tot = round(statistics.fmean(totals)) if totals else 0
        mean_wall = round(statistics.fmean(wall)) if wall else 0
        statuses = sorted({r.get("status", "?") for r in reps})
        nonzero = [r for r in reps if r.get("exit_code", 0) != 0]
        flags: list[str] = []
        if statuses != ["ok"]:
            flags.append("status=" + ",".join(statuses))
        if nonzero:
            flags.append(f"{len(nonzero)} non-zero exits")
        rows.append((sut, fmt, len(reps), mean_p, std_p, min_p, max_p,
                     mean_cov, mean_tot, mean_wall, "; ".join(flags) or "—"))

    rows.sort(key=lambda r: (r[1], r[0]))
    for sut, fmt, n, mean_p, std_p, min_p, max_p, cov, tot, wall, note in rows:
        lines.append(
            f"| {sut} | {fmt} | {n} | {mean_p:.2f}% | ±{std_p:.2f} | "
            f"{min_p:.2f}% | {max_p:.2f}% | {cov}/{tot} | {wall} | {note} |"
        )

    lines.append("")
    lines.append("## Per-rep detail")
    lines.append("")
    lines.append(
        "| SUT | Format | Rep | Exit | Line % | Covered/Total | Wall (s) | Status |"
    )
    lines.append(
        "|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|"
    )
    for r in sorted(records, key=lambda x: (x.get("format"), x.get("sut"), x.get("rep", 0))):
        lines.append(
            f"| {r.get('sut', '?')} | {r.get('format', '?')} | "
            f"{r.get('rep', '?')} | {r.get('exit_code', '—')} | "
            f"{float(r.get('line_pct', 0)):.2f}% | "
            f"{r.get('covered', 0)}/{r.get('total', 0)} | "
            f"{r.get('elapsed_s', 0)} | {r.get('status', '?')} |"
        )
    return "\n".join(lines) + "\n"


def mutation_summary(mutation_root: Path) -> str:
    records = load_records(mutation_root)
    if not records:
        return f"# Mutation summary\n\nNo measurement.json files found under {mutation_root}\n"
    buckets = group_by_cell(records)

    lines: list[str] = []
    lines.append("# BioTest — 6-cell × 4-rep mutation score summary (mean ± std)")
    lines.append("")
    lines.append(
        "Each row reports the per-rep mutation score "
        "(killed / reachable, per DESIGN §3.3) over 4 independent BioTest "
        "runs (qwen3-coder:30b via local Ollama, fresh state per rep). "
        "Each rep's corpus consists of Tier-1+Tier-2 seeds + Phase E "
        "auxiliary outputs (struct + rawfuzz) generated by THAT rep's "
        "BioTest invocation — no cross-rep / cross-SUT contamination."
    )
    lines.append("")
    lines.append(f"Source: `{mutation_root.relative_to(Path.cwd()) if str(mutation_root).startswith(str(Path.cwd())) else mutation_root}`")
    lines.append("")
    lines.append("## Per-SUT mutation score")
    lines.append("")
    lines.append(
        "| SUT | Format | Engine | Reps | Mean score | Std (pp) | Min | Max | "
        "Mean killed/reach | Avg corpus | Avg biotest (s) | Avg mut (s) | Status |"
    )
    lines.append(
        "|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|"
    )

    rows = []
    for (sut, fmt), reps in sorted(buckets.items()):
        scores = [float(r.get("score", 0.0)) for r in reps]
        killed = [int(r.get("killed", 0)) for r in reps]
        reach = [int(r.get("reachable", 0)) for r in reps]
        corpora = [int(r.get("corpus_size", 0)) for r in reps]
        bt_wall = [float(r.get("biotest_elapsed_s", 0.0)) for r in reps]
        mut_wall = [float(r.get("mutation_elapsed_s", 0.0)) for r in reps]
        engine = reps[0].get("engine", "?")
        mean_s = statistics.fmean(scores) if scores else 0.0
        std_s = statistics.stdev(scores) if len(scores) >= 2 else 0.0
        min_s = min(scores) if scores else 0.0
        max_s = max(scores) if scores else 0.0
        mean_k = round(statistics.fmean(killed)) if killed else 0
        mean_r = round(statistics.fmean(reach)) if reach else 0
        mean_c = round(statistics.fmean(corpora)) if corpora else 0
        mean_bt = round(statistics.fmean(bt_wall)) if bt_wall else 0
        mean_mut = round(statistics.fmean(mut_wall)) if mut_wall else 0
        statuses = sorted({r.get("status", "?") for r in reps})
        flags: list[str] = []
        if statuses != ["ok"]:
            flags.append("status=" + ",".join(statuses))
        nonzero = [r for r in reps
                   if r.get("biotest_exit", 0) != 0 or r.get("mutation_exit", 0) != 0]
        if nonzero:
            flags.append(f"{len(nonzero)} non-zero exits")
        rows.append((sut, fmt, engine, len(reps), mean_s, std_s, min_s, max_s,
                     mean_k, mean_r, mean_c, mean_bt, mean_mut,
                     "; ".join(flags) or "—"))

    rows.sort(key=lambda r: (r[1], r[0]))
    for sut, fmt, engine, n, mean_s, std_s, min_s, max_s, mk, mr, mc, mbt, mmut, note in rows:
        lines.append(
            f"| {sut} | {fmt} | {engine} | {n} | {mean_s*100:.2f}% | "
            f"±{std_s*100:.2f} | {min_s*100:.2f}% | {max_s*100:.2f}% | "
            f"{mk}/{mr} | {mc} | {mbt} | {mmut} | {note} |"
        )

    lines.append("")
    lines.append("## Per-rep detail")
    lines.append("")
    lines.append(
        "| SUT | Format | Rep | BT exit | Mut exit | Killed | Reach | Score | "
        "Corpus | BT wall | Mut wall | Status |"
    )
    lines.append(
        "|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|"
    )
    for r in sorted(records, key=lambda x: (x.get("format"), x.get("sut"), x.get("rep", 0))):
        lines.append(
            f"| {r.get('sut', '?')} | {r.get('format', '?')} | "
            f"{r.get('rep', '?')} | {r.get('biotest_exit', '—')} | "
            f"{r.get('mutation_exit', '—')} | "
            f"{r.get('killed', 0)} | {r.get('reachable', 0)} | "
            f"{float(r.get('score', 0))*100:.2f}% | "
            f"{r.get('corpus_size', 0)} | "
            f"{r.get('biotest_elapsed_s', 0)} | "
            f"{r.get('mutation_elapsed_s', 0)} | {r.get('status', '?')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--coverage-root", type=Path,
                    default=Path("compares/results/coverage/biotest_qwen30b_4rep_20260427"))
    ap.add_argument("--mutation-root", type=Path,
                    default=Path("compares/results/mutation/biotest_qwen30b_4rep_20260427"))
    ap.add_argument("--coverage-only", action="store_true")
    ap.add_argument("--mutation-only", action="store_true")
    args = ap.parse_args()

    if not args.mutation_only:
        if args.coverage_root.exists():
            cov_md = coverage_summary(args.coverage_root)
            out = args.coverage_root / "SUMMARY_coverage.md"
            out.write_text(cov_md, encoding="utf-8")
            print(f"wrote {out}")
            print("=" * 60)
            print(cov_md[:1500])
            print("...")
        else:
            print(f"coverage-root not found: {args.coverage_root}")

    if not args.coverage_only:
        if args.mutation_root.exists():
            mut_md = mutation_summary(args.mutation_root)
            out = args.mutation_root / "SUMMARY_mutation.md"
            out.write_text(mut_md, encoding="utf-8")
            print(f"wrote {out}")
            print("=" * 60)
            print(mut_md[:1500])
            print("...")
        else:
            print(f"mutation-root not found: {args.mutation_root}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
