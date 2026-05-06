"""Render per-rep coverage + mutation scores into a single markdown report."""
from __future__ import annotations

import datetime
import json
import os
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[2]
APP = PROJECT_ROOT / "compares" / "ApplicationStudy"

CELLS = ["htsjdk_vcf", "vcfpy_vcf", "noodles_vcf",
         "htsjdk_sam", "biopython_sam", "seqan3_sam"]

CONFIGS = [
    ("E0",  "E0_baseline",     "results_4big_runs", ["a", "b", "c", "d"], 3, "big"),
    ("E1S", "E1S_strict",      "results_4big_runs", ["a", "b", "c", "d"], 3, "big"),
    ("E2",  "E2_no_phase_d",   "results_4rep",      [0, 1, 2, 3],         4, "rep"),
    ("E3",  "E3_no_a_no_d",    "results_4rep",      [0, 1, 2, 3],         4, "rep"),
]


def read_meas(p):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def coverage_cell(d):
    """(value, note) — value is float (0 if ablation/missing), note is short
    string for footnote when value is 0 due to a known cause."""
    if d is None:
        return None, "no measurement file"
    status = d.get("status")
    total = d.get("total", 0)
    lp = d.get("line_pct", 0.0)
    elapsed = d.get("elapsed_s", 0)
    if status == "ok" and total > 0 and lp > 0:
        return lp, None
    if status == "ok" and total > 0 and lp == 0:
        return 0.0, "tool ran but covered 0 lines (cumulative=False .gcda wipe race or harness exit before SUT exec)"
    if status == "missing":
        return 0.0, "Phase B mined 0 valid MRs under ablation → Phase C ran 0 tests → no coverage capture"
    return 0.0, f"status={status} total={total}"


def fmt_pct(v):
    return f"{v:.1f}" if v is not None else "—"


def gather_coverage():
    rows = {}  # cell → list of (config, run_id, rep, line_pct, note)
    for cfg, sub, results_root, ids, n_reps, layout in CONFIGS:
        for cell in CELLS:
            if layout == "big":
                for rid in ids:
                    for r in range(n_reps):
                        p = APP / sub / results_root / f"run_{rid}" / cell / f"run_{r}" / "measurement.json"
                        d = read_meas(p)
                        v, note = coverage_cell(d)
                        rows.setdefault((cfg, cell), []).append({
                            "run_id": rid, "rep": r, "line_pct": v, "note": note,
                        })
            else:
                # layout=rep: single base dir per cell, each rep is independent.
                # The "ids" field is decorative for the script — actual data
                # is rep_0..rep_{n_reps-1} under cell/.
                for r in range(n_reps):
                    p = APP / sub / results_root / cell / f"run_{r}" / "measurement.json"
                    d = read_meas(p)
                    v, note = coverage_cell(d)
                    rows.setdefault((cfg, cell), []).append({
                        "run_id": r, "rep": r, "line_pct": v, "note": note,
                    })
    return rows


def gather_mutation():
    """(cfg, run_id, cell) → score float, plus tool name."""
    out = {}
    for cfg, sub, _results_root, ids, _n_reps, _layout in CONFIGS:
        for rid in ids:
            for cell in CELLS:
                p = APP / sub / "results_metrics" / str(rid) / cell / "summary.json"
                if not p.exists():
                    out[(cfg, rid, cell)] = (None, None)
                    continue
                try:
                    d = json.loads(p.read_text())
                    score = d.get("score")
                    if score is None and "mutation_score" in d:
                        score = d["mutation_score"].get("score")
                    tool = d.get("tool", "?")
                    out[(cfg, rid, cell)] = (score, tool)
                except Exception:
                    out[(cfg, rid, cell)] = (None, None)
    return out


def gather_bug_bench():
    """(cfg, run_id) → (detected, attempted, rate%)."""
    out = {}
    for cfg, sub, *_ in CONFIGS:
        for rid in [0, 1, 2, 3] if cfg in ("E2", "E3") else ["a", "b", "c", "d"]:
            p = APP / sub / "results_metrics" / str(rid) / "bug_bench" / "aggregate.json"
            if not p.exists():
                continue
            try:
                d = json.loads(p.read_text())
                results = d.get("results", []) if isinstance(d, dict) else d
                if isinstance(results, list):
                    detected = sum(1 for r in results if r.get("detected"))
                    attempted = sum(1 for r in results if not (
                        r.get("install_error")
                        or "install" in (r.get("notes", "") or "").lower()
                    ))
                    rate = (detected / attempted * 100) if attempted else 0
                    out[(cfg, rid)] = (detected, attempted, rate)
            except Exception:
                pass
    return out


def main():
    cov = gather_coverage()
    mut = gather_mutation()
    bb = gather_bug_bench()

    today = datetime.date.today().strftime("%Y-%m-%d")
    out_path = ROOT / f"{today}.md"

    L = []
    L.append(f"# Application Study Results — {today}\n")
    L.append("E0 = full BioTest. E1S = no Phase A. E2 = no Phase D. "
             "E3 = no A + no D.\n")
    L.append("All values are **line coverage %** unless stated. "
             "Missing reps shown as `0` with cause-of-zero footnote.\n")

    # ============= COVERAGE: rolled-up summary =============
    L.append("## Coverage — mean ± std per cell\n")
    L.append("| Cell | E0 | E1S | E2 | E3 |")
    L.append("|---|---|---|---|---|")
    for cell in CELLS:
        row = [f"| **{cell}** |"]
        for cfg, *_ in CONFIGS:
            entries = cov.get((cfg, cell), [])
            vals = [e["line_pct"] for e in entries if e["line_pct"] is not None]
            if not vals:
                row.append(" — |")
                continue
            m = statistics.mean(vals)
            s = statistics.stdev(vals) if len(vals) > 1 else 0.0
            row.append(f" {m:.1f} ± {s:.1f} (n={len(vals)}) |")
        L.append("".join(row))
    L.append("")

    # ============= COVERAGE: per-rep tables =============
    for cfg, sub, _rr, ids, n_reps, layout in CONFIGS:
        L.append(f"## E0/E1S/E2/E3 — coverage per rep — {cfg}\n" if False else f"## Coverage per rep — {cfg}\n")
        if layout == "big":
            header = "| Cell | run_a r0 | r1 | r2 | run_b r0 | r1 | r2 | run_c r0 | r1 | r2 | run_d r0 | r1 | r2 |"
        else:
            header = "| Cell | rep_0 | rep_1 | rep_2 | rep_3 |"
        L.append(header)
        L.append("| " + " | ".join(["---"] * (header.count("|") - 1)) + " |")
        for cell in CELLS:
            entries = cov.get((cfg, cell), [])
            cells = [f"| **{cell}** |"]
            zero_notes = []
            for e in entries:
                v = e["line_pct"]
                if v is None:
                    cells.append(" — |")
                elif v == 0.0 and e["note"]:
                    cells.append(f" **0** |")
                    zero_notes.append((e['run_id'], e['rep'], e['note']))
                else:
                    cells.append(f" {v:.1f} |")
            L.append("".join(cells))
            # Footnote zero explanations directly under row
            for rid, rep, note in zero_notes:
                L.append(f"  - `{cell} run_{rid} rep_{rep} = 0`: {note}")
        L.append("")

    # ============= MUTATION: rolled-up summary =============
    L.append("## Mutation — mean score per cell (× 100)\n")
    L.append("| Cell | E0 | E1S | E2 | E3 |")
    L.append("|---|---|---|---|---|")
    for cell in CELLS:
        row = [f"| **{cell}** |"]
        for cfg, _sub, _rr, ids, *_ in CONFIGS:
            scores = []
            for rid in ids:
                s, _tool = mut.get((cfg, rid, cell), (None, None))
                if s is not None:
                    scores.append(s * 100)
            if not scores:
                row.append(" — |")
                continue
            m = statistics.mean(scores)
            sd = statistics.stdev(scores) if len(scores) > 1 else 0.0
            row.append(f" {m:.1f} ± {sd:.1f} (n={len(scores)}) |")
        L.append("".join(row))
    L.append("")

    # ============= MUTATION: per-run tables =============
    for cfg, _sub, _rr, ids, _n_reps, _layout in CONFIGS:
        L.append(f"## Mutation per run — {cfg}\n")
        if isinstance(ids[0], str):
            header = "| Cell | run_a | run_b | run_c | run_d |"
        else:
            header = "| Cell | run_0 | run_1 | run_2 | run_3 |"
        L.append(header)
        L.append("| " + " | ".join(["---"] * 5) + " |")
        for cell in CELLS:
            cells = [f"| **{cell}** |"]
            for rid in ids:
                s, _tool = mut.get((cfg, rid, cell), (None, None))
                if s is None:
                    cells.append(" — |")
                else:
                    cells.append(f" {s*100:.1f} |")
            L.append("".join(cells))
        L.append("")

    # ============= BUG BENCH =============
    if bb:
        L.append("## Real-Bug Detection Rate (per run)\n")
        L.append("| Run | E0 | E1S | E2 | E3 |")
        L.append("|---|---|---|---|---|")
        for i in range(4):
            ids_per_cfg = [["a", "b", "c", "d"], ["a", "b", "c", "d"], [0, 1, 2, 3], [0, 1, 2, 3]]
            row = [f"| run {i} |"]
            for k, (cfg, *_) in enumerate(CONFIGS):
                rid = ids_per_cfg[k][i]
                e = bb.get((cfg, rid))
                if e is None:
                    row.append(" — |")
                else:
                    d, a, r = e
                    row.append(f" {d}/{a} ({r:.1f}%) |")
            L.append("".join(row))
        # Mean
        row = ["| **mean** |"]
        for cfg, *_ in CONFIGS:
            rates = []
            for k, v in bb.items():
                if k[0] == cfg:
                    rates.append(v[2])
            if rates:
                m = statistics.mean(rates)
                sd = statistics.stdev(rates) if len(rates) > 1 else 0.0
                row.append(f" **{m:.1f}%** ± {sd:.1f} (n={len(rates)}) |")
            else:
                row.append(" — |")
        L.append("".join(row))
        L.append("")

    out_path.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
