"""Aggregate the 4-run atheris × vcfpy re-run campaign.

Collects:
  * Coverage: 4 reps under compares/results/coverage/atheris/vcfpy/
    (run_0/, run_1/, run_2/, run_3/) via their harness_growth.json,
    computes per-tick mean ± std across the 4 reps.
  * Mutation: 4 campaigns under compares/results/mutation/atheris/
    vcfpy_runs/run_{0..3}/ via summary.json, computes mean ± std of
    score/killed/reachable/per-file score.

Writes:
  * coverage/.../vcfpy/aggregate_4run.json  — per-run table + mean±std
  * mutation/atheris/vcfpy_runs/aggregate_4run.json — same shape
  * Prints a markdown-ready table for pasting into REPORT.md /
    MUTATION_REPORT.md.

Usage:
  py -3.12 compares/scripts/aggregate_4run.py
"""

from __future__ import annotations

import json
import math
import pathlib
import statistics

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
COV_DIR = REPO_ROOT / "compares/results/coverage/atheris/vcfpy"
MUT_DIR = REPO_ROOT / "compares/results/mutation/atheris/vcfpy_runs"
TICKS = (1, 10, 60, 300, 1800, 7200)


def _mean_std(vals: list[float]) -> tuple[float | None, float | None]:
    vals = [v for v in vals if v is not None]
    if not vals:
        return None, None
    if len(vals) == 1:
        return vals[0], 0.0
    return statistics.fmean(vals), statistics.stdev(vals)


def aggregate_coverage() -> dict:
    per_run: dict[int, dict] = {}
    for n in range(4):
        h = COV_DIR / f"run_{n}" / "harness_growth.json"
        if not h.exists():
            per_run[n] = {"status": "missing"}
            continue
        d = json.loads(h.read_text(encoding="utf-8"))
        ticks = {int(r["t_s"]): r for r in d.get("coverage_growth", [])}
        # Fill in missing (e.g. t=7200 not captured by live thread) by
        # taking the final recorded tick's value as a plateau.
        if ticks:
            last_t = max(ticks)
            last_r = ticks[last_t]
            for t in TICKS:
                if t not in ticks and t <= last_t:
                    continue
                if t not in ticks and t >= last_t:
                    ticks[t] = last_r
        per_run[n] = {
            "status": "ok",
            "ticks": {
                t: {
                    "line_pct": ticks.get(t, {}).get("line_pct"),
                    "branch_pct": ticks.get(t, {}).get("branch_pct"),
                }
                for t in TICKS
            },
        }

    # Per-tick aggregate across the 4 runs
    aggregate = {}
    for t in TICKS:
        line_vals = [
            per_run[n]["ticks"][t]["line_pct"]
            for n in range(4)
            if per_run[n].get("status") == "ok"
            and per_run[n]["ticks"].get(t, {}).get("line_pct") is not None
        ]
        br_vals = [
            per_run[n]["ticks"][t]["branch_pct"]
            for n in range(4)
            if per_run[n].get("status") == "ok"
            and per_run[n]["ticks"].get(t, {}).get("branch_pct") is not None
        ]
        lm, ls = _mean_std(line_vals)
        bm, bs = _mean_std(br_vals)
        aggregate[t] = {
            "line_pct_mean": round(lm, 2) if lm is not None else None,
            "line_pct_std": round(ls, 3) if ls is not None else None,
            "line_pct_n": len(line_vals),
            "branch_pct_mean": round(bm, 2) if bm is not None else None,
            "branch_pct_std": round(bs, 3) if bs is not None else None,
            "branch_pct_n": len(br_vals),
        }

    out = {
        "n_runs": sum(1 for v in per_run.values() if v.get("status") == "ok"),
        "ticks": list(TICKS),
        "per_run": per_run,
        "aggregate": aggregate,
    }
    (COV_DIR / "aggregate_4run.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8",
    )
    return out


def aggregate_mutation() -> dict:
    per_run: dict[int, dict] = {}
    for n in range(4):
        s = MUT_DIR / f"run_{n}" / "summary.json"
        if not s.exists():
            per_run[n] = {"status": "missing"}
            continue
        d = json.loads(s.read_text(encoding="utf-8"))
        per_run[n] = {
            "status": "ok",
            "score": d.get("score"),
            "score_display": d.get("score_display"),
            "killed": d.get("killed"),
            "survived": d.get("survived"),
            "reachable": d.get("reachable"),
            "mutant_count": d.get("mutant_count"),
            "no_tests": d.get("no_tests"),
            "mutmut_duration_s": d.get("mutmut_duration_s"),
            "corpus_size": d.get("corpus_size"),
            "per_file": d.get("per_file", {}),
        }

    oks = [p for p in per_run.values() if p.get("status") == "ok"]

    def _f(key: str) -> tuple[float | None, float | None]:
        return _mean_std([p[key] for p in oks if p.get(key) is not None])

    sm, ss = _f("score")
    km, ks = _f("killed")
    rm, rs = _f("reachable")
    mm, ms = _f("mutant_count")
    dm, ds = _f("mutmut_duration_s")

    # Per-file score aggregate
    file_names = sorted({
        fn
        for p in oks
        for fn in (p.get("per_file") or {})
    })
    per_file_agg = {}
    for fn in file_names:
        scores = []
        killed_vals = []
        reach_vals = []
        for p in oks:
            info = (p.get("per_file") or {}).get(fn, {})
            if info.get("score") is not None:
                scores.append(info["score"])
            if info.get("killed") is not None:
                killed_vals.append(info["killed"])
            if info.get("reachable") is not None:
                reach_vals.append(info["reachable"])
        s_mean, s_std = _mean_std(scores)
        k_mean, k_std = _mean_std(killed_vals)
        r_mean, r_std = _mean_std(reach_vals)
        per_file_agg[fn] = {
            "score_mean": round(s_mean, 4) if s_mean is not None else None,
            "score_std": round(s_std, 4) if s_std is not None else None,
            "score_n": len(scores),
            "killed_mean": round(k_mean, 2) if k_mean is not None else None,
            "killed_std": round(k_std, 2) if k_std is not None else None,
            "reachable_mean": round(r_mean, 2) if r_mean is not None else None,
            "reachable_std": round(r_std, 2) if r_std is not None else None,
        }

    out = {
        "n_runs": len(oks),
        "per_run": per_run,
        "aggregate": {
            "score_mean": round(sm, 4) if sm is not None else None,
            "score_std": round(ss, 4) if ss is not None else None,
            "killed_mean": round(km, 2) if km is not None else None,
            "killed_std": round(ks, 2) if ks is not None else None,
            "reachable_mean": round(rm, 2) if rm is not None else None,
            "reachable_std": round(rs, 2) if rs is not None else None,
            "mutant_count_mean": round(mm, 2) if mm is not None else None,
            "mutant_count_std": round(ms, 2) if ms is not None else None,
            "mutmut_duration_s_mean": round(dm, 2) if dm is not None else None,
            "mutmut_duration_s_std": round(ds, 2) if ds is not None else None,
        },
        "per_file": per_file_agg,
    }
    (MUT_DIR / "aggregate_4run.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8",
    )
    return out


def _fmt_pct(m, s):
    if m is None:
        return "-"
    if s is None or s == 0:
        return f"{m:.2f}"
    return f"{m:.2f} ± {s:.2f}"


def _fmt_int(m, s):
    if m is None:
        return "-"
    if s is None or s == 0:
        return f"{m:.0f}"
    return f"{m:.1f} ± {s:.1f}"


def _render_coverage_tables(cov: dict) -> str:
    # Per-run rows
    hdr = "| tick (s) | run 0 | run 1 | run 2 | run 3 | **mean ± std (line%)** |"
    sep = "|:-:|:-:|:-:|:-:|:-:|:-:|"
    lines = [hdr, sep]
    for t in TICKS:
        row = [f"**{t}**"]
        for n in range(4):
            p = cov["per_run"].get(n, {})
            v = (p.get("ticks") or {}).get(t, {}).get("line_pct") if p.get("status") == "ok" else None
            row.append(f"{v:.2f}" if v is not None else "—")
        agg = cov["aggregate"][t]
        row.append(f"**{_fmt_pct(agg['line_pct_mean'], agg['line_pct_std'])}**")
        lines.append("| " + " | ".join(str(x) for x in row) + " |")

    lines.append("")
    lines.append("### Branch %")
    hdr2 = "| tick (s) | run 0 | run 1 | run 2 | run 3 | **mean ± std (branch%)** |"
    lines += [hdr2, sep]
    for t in TICKS:
        row = [f"**{t}**"]
        for n in range(4):
            p = cov["per_run"].get(n, {})
            v = (p.get("ticks") or {}).get(t, {}).get("branch_pct") if p.get("status") == "ok" else None
            row.append(f"{v:.2f}" if v is not None else "—")
        agg = cov["aggregate"][t]
        row.append(f"**{_fmt_pct(agg['branch_pct_mean'], agg['branch_pct_std'])}**")
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def _render_mutation_tables(mut: dict) -> str:
    hdr = "| metric | run 0 | run 1 | run 2 | run 3 | **mean ± std** |"
    sep = "|:--|:-:|:-:|:-:|:-:|:-:|"
    lines = [hdr, sep]

    def row_int(label, key):
        cells = [f"**{label}**"]
        for n in range(4):
            v = mut["per_run"].get(n, {}).get(key)
            cells.append(f"{v}" if v is not None else "—")
        agg = mut["aggregate"]
        cells.append(f"**{_fmt_int(agg.get(key + '_mean'), agg.get(key + '_std'))}**")
        return "| " + " | ".join(cells) + " |"

    def row_pct(label, key):
        cells = [f"**{label}**"]
        for n in range(4):
            v = mut["per_run"].get(n, {}).get(key)
            cells.append(f"{v*100:.2f}%" if v is not None else "—")
        agg = mut["aggregate"]
        m = agg.get(key + "_mean")
        s = agg.get(key + "_std")
        if m is None:
            cells.append("—")
        else:
            disp = f"{m*100:.2f}%"
            if s:
                disp += f" ± {s*100:.2f} pp"
            cells.append(f"**{disp}**")
        return "| " + " | ".join(cells) + " |"

    lines.append(row_pct("Mutation score", "score"))
    lines.append(row_int("Killed", "killed"))
    lines.append(row_int("Reachable", "reachable"))
    lines.append(row_int("Mutant count", "mutant_count"))
    lines.append(row_int("mutmut duration (s)", "mutmut_duration_s"))

    lines.append("")
    lines.append("### Per-file mutation score (4-run mean ± std)")
    lines.append("| file | run 0 | run 1 | run 2 | run 3 | **mean ± std** |")
    lines.append(sep)
    for fn, agg in mut["per_file"].items():
        cells = [f"`{fn}.py`"]
        for n in range(4):
            p = mut["per_run"].get(n, {}).get("per_file", {}).get(fn, {})
            v = p.get("score") if p else None
            cells.append(f"{v*100:.2f}%" if v is not None else "—")
        m = agg.get("score_mean")
        s = agg.get("score_std")
        if m is None:
            cells.append("—")
        else:
            disp = f"{m*100:.2f}%"
            if s:
                disp += f" ± {s*100:.2f} pp"
            cells.append(f"**{disp}**")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> int:
    cov = aggregate_coverage()
    mut = aggregate_mutation()

    print("=" * 72)
    print(f"COVERAGE — 4-run aggregate (n_runs={cov['n_runs']})")
    print("=" * 72)
    print(_render_coverage_tables(cov))
    print()
    print("=" * 72)
    print(f"MUTATION — 4-run aggregate (n_runs={mut['n_runs']})")
    print("=" * 72)
    print(_render_mutation_tables(mut))
    print()
    print(f"JSON summaries written to:")
    print(f"  {COV_DIR / 'aggregate_4run.json'}")
    print(f"  {MUT_DIR / 'aggregate_4run.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
