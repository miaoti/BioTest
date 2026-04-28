"""M3 boost aggregator — compute n=10 (or partial-n) statistics on the
four close-margin cells once the boost runs land.

Reads per-rep summary.json from:
  - BioTest:    compares/results/mutation/biotest_run1_rep_{0..9}/<cell>/summary.json
  - Jazzer:     compares/results/mutation/jazzer_4rep/rep_{0..9}/htsjdk_<fmt>/summary.json
  - Atheris:    compares/results/mutation/atheris/vcfpy_runs/run_{0..9}/summary.json
  - cargo-fuzz: compares/results/mutation/cargo_fuzz/noodles/run_{01..10}/summary.json

Computes (per cell):
  - per-rep score, mean ± std at the achieved n
  - exact two-sided Mann–Whitney U p-value (full enumeration)
  - Vargha–Delaney Â₁₂ with magnitude label
  - Holm–Bonferroni correction across the four close-margin cells

Outputs:
  - compares/results/mutation/biotest/M3_N10_AGGREGATE.json (raw)
  - compares/results/mutation/biotest/M3_N10_AGGREGATE.md   (markdown table)
"""

from __future__ import annotations

import collections
import glob
import json
import os
import statistics
from itertools import combinations
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)


def _load_summary(path: Path) -> tuple[int, int, float] | None:
    if not path.exists():
        return None
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    killed = d.get("killed", 0)
    reachable = d.get("reachable", 0)
    if reachable == 0:
        return None
    return killed, reachable, killed / reachable


def collect(globs: list[str]) -> list[tuple[str, int, int, float]]:
    out = []
    for pattern in globs:
        for p in sorted(REPO_ROOT.glob(pattern)):
            triple = _load_summary(p)
            if triple is None:
                continue
            killed, reachable, score = triple
            label = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            out.append((label, killed, reachable, score))
    return out


def vargha_a12(s_a: list[float], s_b: list[float]) -> float:
    gt = sum(1 for x in s_a for y in s_b if x > y)
    eq = sum(1 for x in s_a for y in s_b if x == y)
    return (gt + 0.5 * eq) / (len(s_a) * len(s_b))


def magnitude_label(a12: float) -> str:
    diff = abs(a12 - 0.5)
    if diff < 0.06:
        return "negligible"
    if diff < 0.14:
        return "small"
    if diff < 0.21:
        return "medium"
    return "large"


def mwu_two_sided_exact_p(s_a: list[float], s_b: list[float]) -> float:
    n_a, n_b = len(s_a), len(s_b)
    if n_a == 0 or n_b == 0:
        return float("nan")
    pooled = sorted(s_a + s_b)
    rank = {}
    i = 0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1] == pooled[i]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rank[(pooled[k], k)] = avg
        i = j + 1
    used = [False] * len(pooled)
    R_a = 0.0
    for x in s_a:
        for k in range(len(pooled)):
            if not used[k] and pooled[k] == x:
                R_a += rank[(pooled[k], k)]
                used[k] = True
                break
    obs_U_a = R_a - n_a * (n_a + 1) / 2
    obs_U_b = n_a * n_b - obs_U_a
    obs_U = min(obs_U_a, obs_U_b)
    total = comb(n_a + n_b, n_a)
    extreme = 0
    for combo in combinations(range(n_a + n_b), n_a):
        R = sum(rank[(pooled[k], k)] for k in combo)
        U_a = R - n_a * (n_a + 1) / 2
        U_b = n_a * n_b - U_a
        U = min(U_a, U_b)
        if U <= obs_U:
            extreme += 1
    return extreme / total


CLOSE_MARGIN_CELLS = [
    {
        "name": "htsjdk_vcf",
        "biotest": ["compares/results/mutation/biotest_run1_rep_*/htsjdk_vcf/summary.json"],
        "baseline": ["compares/results/mutation/jazzer_4rep/rep_*/htsjdk_vcf/summary.json"],
        "baseline_name": "Jazzer",
    },
    {
        "name": "htsjdk_sam",
        "biotest": ["compares/results/mutation/biotest_run1_rep_*/htsjdk_sam/summary.json"],
        "baseline": ["compares/results/mutation/jazzer_4rep/rep_*/htsjdk_sam/summary.json"],
        "baseline_name": "Jazzer",
    },
    {
        "name": "vcfpy",
        "biotest": ["compares/results/mutation/biotest_run1_rep_*/vcfpy/summary.json"],
        "baseline": ["compares/results/mutation/atheris/vcfpy_runs/run_*/summary.json"],
        "baseline_name": "Atheris",
    },
    {
        "name": "noodles",
        "biotest": ["compares/results/mutation/biotest_run1_rep_*/noodles/summary.json"],
        "baseline": ["compares/results/mutation/cargo_fuzz/noodles/run_*/summary.json"],
        "baseline_name": "cargo-fuzz",
    },
]


def main() -> None:
    raw = {}
    rows = []
    for cell in CLOSE_MARGIN_CELLS:
        bt = collect(cell["biotest"])
        bl = collect(cell["baseline"])
        bt_scores = [t[3] for t in bt]
        bl_scores = [t[3] for t in bl]
        if not bt_scores or not bl_scores:
            print(f"{cell['name']}: insufficient data — bt={len(bt_scores)} bl={len(bl_scores)}")
            raw[cell["name"]] = {
                "bt_n": len(bt_scores), "bl_n": len(bl_scores),
                "bt_per_rep": bt, "bl_per_rep": bl,
            }
            continue
        a12 = vargha_a12(bt_scores, bl_scores)
        mag = magnitude_label(a12)
        if len(bt_scores) >= 2 and len(bl_scores) >= 2:
            p = mwu_two_sided_exact_p(bt_scores, bl_scores)
        else:
            p = float("nan")
        bt_mu = statistics.fmean(bt_scores)
        bl_mu = statistics.fmean(bl_scores)
        bt_sd = statistics.stdev(bt_scores) if len(bt_scores) > 1 else 0.0
        bl_sd = statistics.stdev(bl_scores) if len(bl_scores) > 1 else 0.0
        rows.append({
            "cell": cell["name"],
            "baseline_name": cell["baseline_name"],
            "bt_n": len(bt_scores), "bl_n": len(bl_scores),
            "bt_mean": 100 * bt_mu, "bt_std": 100 * bt_sd,
            "bl_mean": 100 * bl_mu, "bl_std": 100 * bl_sd,
            "a12": a12, "mag": mag, "raw_p": p,
        })
        raw[cell["name"]] = {
            "bt_n": len(bt_scores), "bl_n": len(bl_scores),
            "bt_mean": bt_mu, "bt_std": bt_sd,
            "bl_mean": bl_mu, "bl_std": bl_sd,
            "a12": a12, "magnitude": mag, "raw_p": p,
            "bt_per_rep": bt, "bl_per_rep": bl,
        }

    rows.sort(key=lambda r: r["raw_p"])
    m = len(rows)
    for rank_i, r in enumerate(rows, start=1):
        factor = m - rank_i + 1
        r["holm_factor"] = factor
        r["holm_p"] = min(1.0, r["raw_p"] * factor)
        raw[r["cell"]]["holm_factor"] = factor
        raw[r["cell"]]["holm_p"] = r["holm_p"]

    md_lines = [
        "# M3 boost aggregate — n=10 close-margin cells",
        "",
        "Per-cell mean ± std, Â₁₂, exact two-sided Mann–Whitney p, and",
        "Holm–Bonferroni correction across the four close-margin cells.",
        "Sorted by raw p (smallest first → highest Holm correction factor).",
        "",
        f"| cell | n_BT / n_base | mean_BT ± σ | mean_base ± σ ({rows[0]['baseline_name'] if rows else ''}, etc.) | Â₁₂ | mag | exact p | Holm × {m} factors | Holm p |",
        "|:-----|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|",
    ]
    for r in rows:
        md_lines.append(
            f"| `{r['cell']}` | {r['bt_n']} / {r['bl_n']} "
            f"| {r['bt_mean']:.2f} ± {r['bt_std']:.2f} "
            f"| {r['bl_mean']:.2f} ± {r['bl_std']:.2f} ({r['baseline_name']}) "
            f"| {r['a12']:.4f} | {r['mag']} "
            f"| {r['raw_p']:.5f} | rank-{rows.index(r)+1} ×{r['holm_factor']} | {r['holm_p']:.5f} |"
        )

    out_md = REPO_ROOT / "compares/results/mutation/biotest/M3_N10_AGGREGATE.md"
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    out_json = REPO_ROOT / "compares/results/mutation/biotest/M3_N10_AGGREGATE.json"
    out_json.write_text(json.dumps(raw, indent=2, default=float), encoding="utf-8")
    print(f"wrote {out_md}")
    print(f"wrote {out_json}")
    for r in rows:
        print(f"  {r['cell']}: n_BT={r['bt_n']}/n_base={r['bl_n']} "
              f"Â12={r['a12']:.4f} raw_p={r['raw_p']:.5f} Holm_p={r['holm_p']:.5f}")


if __name__ == "__main__":
    main()
