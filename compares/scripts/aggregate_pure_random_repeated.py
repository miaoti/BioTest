"""Aggregate 4-run Pure Random coverage + mutation results.

DESIGN.md §13.5 Phase 2 + Phase 3 "re-run 4 times" follow-up —
consumes the existing pure_random output directories plus the
additional runs produced by the 4-run aggregation workflow and
emits:

  1. A per-cell table of mean ± std across 4 runs for **coverage**
     (line_pct + branch_pct at tick=7200 s).
  2. A per-cell table of mean ± std across 4 runs for **mutation**
     (killed, reachable, score).
  3. Appended "Per-run" sections in both REPORT.md files showing
     each run's raw numbers.

Inputs (all produced by earlier phases):

  coverage/pure_random/<cell>/growth_{0,1,2,3}.json  (4 samples)

  mutation/pure_random_run/<cell>/summary.json              (run 1)
  mutation/pure_random_run2/<cell>/summary.json             (run 2)
  mutation/pure_random_run3/<cell>/summary.json             (run 3)
  mutation/pure_random_run4/<cell>/summary.json             (run 4)

Outputs:

  coverage/pure_random/REPORT.md          (appended 4-run section)
  coverage/pure_random/summary_4runs.csv  (new)
  mutation/pure_random_run/REPORT.md      (appended 4-run section)
  mutation/pure_random_run/summary_4runs.csv  (new)

Idempotent — re-running replaces any previous 4-run section
between the two HTML-comment markers:

  <!-- 4-RUN-AGG BEGIN -->
  ...
  <!-- 4-RUN-AGG END -->
"""

from __future__ import annotations

import csv
import json
import logging
import math
import statistics
import sys
from pathlib import Path

logger = logging.getLogger("aggregate_pure_random_repeated")

REPO_ROOT = Path(__file__).resolve().parents[2]
COV_ROOT = REPO_ROOT / "compares" / "results" / "coverage" / "pure_random"
MUT_ROOTS = [
    REPO_ROOT / "compares" / "results" / "mutation" / "pure_random_run1",
    REPO_ROOT / "compares" / "results" / "mutation" / "pure_random_run2",
    REPO_ROOT / "compares" / "results" / "mutation" / "pure_random_run3",
    REPO_ROOT / "compares" / "results" / "mutation" / "pure_random_run4",
]
# The canonical REPORT.md lives with the first run for compatibility
# with the original Phase-3 report written before the 4-run pass.
MUT_REPORT_PATH = (
    REPO_ROOT / "compares" / "results" / "mutation"
    / "pure_random_run" / "REPORT.md"
)
MATRIX = (
    "htsjdk_vcf", "htsjdk_sam", "vcfpy", "noodles", "biopython", "seqan3",
)
SECTION_BEGIN = "<!-- 4-RUN-AGG BEGIN -->"
SECTION_END = "<!-- 4-RUN-AGG END -->"


def _mean_std(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) < 2:
        return values[0], 0.0
    return statistics.fmean(values), statistics.stdev(values)


# --- Coverage aggregation ---------------------------------------------------

def _load_coverage_samples() -> dict[str, dict[int, list[dict]]]:
    """For each cell → per-tick list of per-run dicts (run_0..run_3)."""
    out: dict[str, dict[int, list[dict]]] = {}
    for cell in MATRIX:
        cell_dir = COV_ROOT / cell
        if not cell_dir.is_dir():
            continue
        run_samples: dict[int, list[dict]] = {}
        for rep_idx in range(4):
            gf = cell_dir / f"growth_{rep_idx}.json"
            if not gf.exists():
                continue
            try:
                d = json.loads(gf.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                logger.warning("skip %s: %s", gf, e)
                continue
            for snap in d.get("coverage_growth", []):
                t = int(snap["t_s"])
                run_samples.setdefault(t, []).append({
                    "run_index": rep_idx,
                    "line_pct": float(snap.get("line_pct", 0.0)),
                    "branch_pct": float(snap.get("branch_pct", 0.0)),
                })
        if run_samples:
            out[cell] = run_samples
    return out


def _coverage_summary(samples: dict[str, dict[int, list[dict]]]
                      ) -> list[dict]:
    """One row per (cell, tick) with mean ± std across reps."""
    rows: list[dict] = []
    for cell, by_tick in samples.items():
        for t in sorted(by_tick):
            entries = by_tick[t]
            l_vals = [e["line_pct"] for e in entries]
            b_vals = [e["branch_pct"] for e in entries]
            lm, ls = _mean_std(l_vals)
            bm, bs = _mean_std(b_vals)
            rows.append({
                "cell": cell,
                "t_s": t,
                "n_runs": len(entries),
                "line_pct_mean": round(lm, 3),
                "line_pct_std": round(ls, 3),
                "branch_pct_mean": round(bm, 3),
                "branch_pct_std": round(bs, 3),
                "line_pct_per_run": ", ".join(f"{v:.3f}" for v in l_vals),
                "branch_pct_per_run": ", ".join(f"{v:.3f}" for v in b_vals),
            })
    return rows


def _coverage_table_md(rows: list[dict], tick: int) -> str:
    """Render the mean ± std headline table (one cell per line at
    the given tick). Match DESIGN.md §4.5 / REPORT.md §TL;DR shape."""
    cells_order = [c for c in MATRIX]
    line = {}
    branch = {}
    nruns = {}
    for r in rows:
        if r["t_s"] != tick:
            continue
        line[r["cell"]] = (r["line_pct_mean"], r["line_pct_std"])
        branch[r["cell"]] = (r["branch_pct_mean"], r["branch_pct_std"])
        nruns[r["cell"]] = r["n_runs"]
    lines = [
        f"| cell         | n | line % (mean ± std)    | branch % (mean ± std)   |",
        f"|:-------------|--:|:-----------------------|:------------------------|",
    ]
    for cell in cells_order:
        if cell not in line:
            continue
        lm, ls = line[cell]
        bm, bs = branch[cell]
        lines.append(
            f"| {cell:<12} | {nruns[cell]} | "
            f"{lm:>7.3f} ± {ls:<5.3f}    | "
            f"{bm:>7.3f} ± {bs:<5.3f}     |"
        )
    return "\n".join(lines)


# --- Mutation aggregation ---------------------------------------------------

def _load_mutation_samples() -> dict[str, list[dict]]:
    """Per-cell list of per-run summary dicts (4 runs)."""
    out: dict[str, list[dict]] = {cell: [] for cell in MATRIX}
    for run_idx, root in enumerate(MUT_ROOTS, start=1):
        if not root.is_dir():
            logger.warning("mutation run %d dir missing: %s", run_idx, root)
            continue
        for cell in MATRIX:
            sf = root / cell / "summary.json"
            if not sf.exists():
                continue
            try:
                d = json.loads(sf.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                logger.warning("skip %s: %s", sf, e)
                continue
            d["_run_index"] = run_idx
            d["_root"] = str(root)
            out[cell].append(d)
    return out


def _mutation_summary(samples: dict[str, list[dict]]) -> list[dict]:
    """One row per cell with mean ± std across runs of killed/reachable/score."""
    rows: list[dict] = []
    for cell in MATRIX:
        runs = samples.get(cell, [])
        if not runs:
            continue
        blocked_any = any(r.get("blocked_reason") for r in runs)
        killed = [int(r.get("killed", 0)) for r in runs]
        reach = [int(r.get("reachable", 0)) for r in runs]
        score = [float(r.get("score", 0.0)) for r in runs]
        km, ks = _mean_std(killed)
        rm, rs = _mean_std(reach)
        sm, ss = _mean_std(score)
        rows.append({
            "cell": cell,
            "n_runs": len(runs),
            "engine": runs[0].get("engine", ""),
            "blocked": blocked_any,
            "killed_mean": round(km, 2),
            "killed_std": round(ks, 2),
            "reachable_mean": round(rm, 2),
            "reachable_std": round(rs, 2),
            "score_mean": round(sm, 4),
            "score_std": round(ss, 4),
            "killed_per_run": ", ".join(str(v) for v in killed),
            "reachable_per_run": ", ".join(str(v) for v in reach),
            "score_per_run": ", ".join(f"{v:.4f}" for v in score),
            "blocked_reason": next(
                (r.get("blocked_reason", "") for r in runs
                 if r.get("blocked_reason")),
                "",
            ),
        })
    return rows


def _mutation_table_md(rows: list[dict]) -> str:
    lines = [
        f"| cell         | n | engine                   | killed (mean ± std) | reachable (mean ± std) | score (mean ± std)        |",
        f"|:-------------|--:|:-------------------------|:--------------------|:-----------------------|:--------------------------|",
    ]
    for r in rows:
        if r["blocked"]:
            lines.append(
                f"| {r['cell']:<12} | {r['n_runs']} | "
                f"{r['engine']:<24} |           blocked † |             blocked † |             blocked †     |"
            )
            continue
        km, ks = r["killed_mean"], r["killed_std"]
        rm, rs = r["reachable_mean"], r["reachable_std"]
        sm, ss = r["score_mean"], r["score_std"]
        lines.append(
            f"| {r['cell']:<12} | {r['n_runs']} | "
            f"{r['engine']:<24} | "
            f"{km:>8.2f} ± {ks:<6.2f} | "
            f"{rm:>10.2f} ± {rs:<6.2f} | "
            f"{sm * 100:>7.2f} % ± {ss * 100:<5.2f} %    |"
        )
    return "\n".join(lines)


# --- Per-run detail tables (appended to REPORT.md) --------------------------

def _coverage_per_run_md(samples: dict[str, dict[int, list[dict]]]
                         ) -> str:
    lines: list[str] = []
    for cell in MATRIX:
        if cell not in samples:
            continue
        lines.append(f"\n#### {cell}\n")
        lines.append("| run | line % @ 1 s | @ 10 s | @ 60 s | @ 300 s | @ 1800 s | @ 7200 s | branch % @ 7200 s |")
        lines.append("|----:|-------------:|-------:|-------:|--------:|---------:|---------:|------------------:|")
        # Group per run (one run_idx spans all ticks)
        by_run: dict[int, dict[int, dict]] = {}
        for t, entries in samples[cell].items():
            for e in entries:
                by_run.setdefault(e["run_index"], {})[t] = e
        for run_idx in sorted(by_run):
            row = by_run[run_idx]
            def lp(t: int) -> str:
                e = row.get(t)
                return f"{e['line_pct']:.3f}" if e else "—"
            def bp(t: int) -> str:
                e = row.get(t)
                return f"{e['branch_pct']:.3f}" if e else "—"
            lines.append(
                f"| {run_idx + 1:>3} | "
                f"{lp(1):>12} | {lp(10):>6} | {lp(60):>6} | "
                f"{lp(300):>7} | {lp(1800):>8} | {lp(7200):>8} | "
                f"{bp(7200):>17} |"
            )
    return "\n".join(lines)


def _mutation_per_run_md(samples: dict[str, list[dict]]) -> str:
    lines: list[str] = []
    for cell in MATRIX:
        runs = samples.get(cell, [])
        if not runs:
            continue
        lines.append(f"\n#### {cell}\n")
        blocked = any(r.get("blocked_reason") for r in runs)
        if blocked:
            lines.append(
                f"Cell blocked across all runs: "
                f"`{runs[0].get('engine', '')}` — "
                f"{runs[0].get('blocked_reason', '')[:120]}"
            )
            continue
        lines.append("| run | killed | survived | suspicious | timeout | reachable | score   | duration_s | corpus              |")
        lines.append("|----:|-------:|---------:|-----------:|--------:|----------:|:--------|-----------:|:--------------------|")
        for r in runs:
            corpus = Path(r.get("corpus_dir", "")).name or "(union)"
            lines.append(
                f"| {r['_run_index']:>3} | "
                f"{r.get('killed', 0):>6} | "
                f"{r.get('survived', 0):>8} | "
                f"{r.get('suspicious', 0):>10} | "
                f"{r.get('timeout', 0):>7} | "
                f"{r.get('reachable', 0):>9} | "
                f"{r.get('score_display', ''):<7} | "
                f"{r.get('mutmut_duration_s', 0.0):>10.1f} | "
                f"{corpus:<19} |"
            )
    return "\n".join(lines)


# --- REPORT.md patcher ------------------------------------------------------

def _patch_report_md(
    path: Path, section_title: str, section_body: str,
) -> None:
    """Insert or replace the 4-run aggregation section between the
    HTML-comment markers. Idempotent."""
    body = (
        f"\n\n{SECTION_BEGIN}\n\n## {section_title}\n\n{section_body.strip()}\n\n{SECTION_END}\n"
    )
    if not path.exists():
        path.write_text(body.lstrip(), encoding="utf-8")
        return
    original = path.read_text(encoding="utf-8")
    if SECTION_BEGIN in original and SECTION_END in original:
        prefix, rest = original.split(SECTION_BEGIN, 1)
        _, suffix = rest.split(SECTION_END, 1)
        patched = prefix.rstrip() + body + suffix.lstrip()
    else:
        patched = original.rstrip() + body
    path.write_text(patched, encoding="utf-8")


def _write_csv(path: Path, rows: list[dict], cols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


# --- main -------------------------------------------------------------------

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s %(message)s",
    )

    # Coverage
    cov_samples = _load_coverage_samples()
    cov_rows = _coverage_summary(cov_samples)
    _write_csv(
        COV_ROOT / "summary_4runs.csv", cov_rows,
        cols=[
            "cell", "t_s", "n_runs",
            "line_pct_mean", "line_pct_std",
            "branch_pct_mean", "branch_pct_std",
            "line_pct_per_run", "branch_pct_per_run",
        ],
    )
    cov_table = _coverage_table_md(cov_rows, tick=7200)
    cov_per_run = _coverage_per_run_md(cov_samples)
    cov_body = (
        "Aggregated across **4 independent Phase-2 runs** (rep_idx 0 / 1 "
        "/ 2 / 3 under `compares/results/coverage/pure_random/<cell>/"
        "run_{0,1,2,3}/`). Each run generates a fresh pure_random "
        "corpus (seed = `0xB10 + rep_idx`; file bytes from "
        "`os.urandom`, non-deterministic) and measures coverage at "
        "the DESIGN §3.2 log ticks.\n\n"
        f"**Mean ± std at t = 7200 s**:\n\n{cov_table}\n\n"
        "Raw CSV: `summary_4runs.csv` (one row per (cell, tick) with "
        "per-run values preserved).\n\n"
        f"### Per-run raw data\n{cov_per_run}"
    )
    _patch_report_md(
        COV_ROOT / "REPORT.md",
        "4-run aggregation — mean ± std across 4 Pure Random passes",
        cov_body,
    )

    # Mutation
    mut_samples = _load_mutation_samples()
    mut_rows = _mutation_summary(mut_samples)
    _write_csv(
        MUT_REPORT_PATH.parent / "summary_4runs.csv", mut_rows,
        cols=[
            "cell", "n_runs", "engine", "blocked",
            "killed_mean", "killed_std",
            "reachable_mean", "reachable_std",
            "score_mean", "score_std",
            "killed_per_run", "reachable_per_run", "score_per_run",
            "blocked_reason",
        ],
    )
    mut_table = _mutation_table_md(mut_rows)
    mut_per_run = _mutation_per_run_md(mut_samples)
    mut_body = (
        "Aggregated across **4 independent Phase-3 runs** (mutmut "
        "invocations at `pure_random_run` / `pure_random_run2` / "
        "`pure_random_run3` / `pure_random_run4`). Each run uses a "
        "DIFFERENT corpus — runs 2/3/4 reuse rep_0 / rep_1 / rep_2's "
        "200-file Phase-2 corpora respectively, so variance across "
        "runs comes from the underlying random-byte stream.\n\n"
        f"**Mean ± std across 4 runs**:\n\n{mut_table}\n\n"
        "† PIT / mull / cargo-mutants cells stay blocked across every "
        "run on the Windows host — the matrix slot is preserved for "
        "Phase-6 CI comparability; Docker rerun promotes them to "
        "real numbers. See the original §TL;DR for promotion commands.\n\n"
        "Raw CSV: `summary_4runs.csv` (one row per cell with per-run "
        "values preserved).\n\n"
        f"### Per-run raw data\n{mut_per_run}"
    )
    _patch_report_md(
        MUT_REPORT_PATH,
        "4-run aggregation — mean ± std across 4 Pure Random passes",
        mut_body,
    )

    print("\n=== Coverage — mean ± std at t=7200 s ===")
    print(cov_table)
    print("\n=== Mutation — mean ± std ===")
    print(mut_table)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
