"""4-rep mutation scoring against `biotest.py`'s actual auto-pipeline output.

Difference from `run_mutation_reps.py` (the previous Run-8 orchestrator):
  - Run-8 manually staged a corpus that EXCLUDED `kept_*` (Rank 8 corpus
    keeper) and `synthetic_*` (Phase-D LLM synth) — both auto-produced
    by biotest.py — and manually unioned `struct_*` / `rawfuzz_*`.
  - This script (Run-10) measures **what biotest.py actually delivers
    when run normally**: external primary + auto-`kept_*` + auto-
    `synthetic_*` + auto-`struct_*` + auto-`rawfuzz_*` (the last two
    via Phase E, integrated 2026-04-23).

Per-rep variance comes from Phase E re-running `lenient_byte_fuzzer.py`
(Rank 13) with a rep-specific seed → different `seeds/<fmt>_rawfuzz/`
content per rep. Everything else (external seeds, `kept_*`,
`synthetic_*`, Rank 12 `struct_*`) is stable across reps.

The user wanted: "based on the result produced on run 1, and run 2,3,4
like what we did last time". So we treat the four reps as independent
mutation campaigns over the same auto-pipeline corpus shape, with
Rank-13 seed varying. Std across the 4 reps reflects the mutation
engine's sensitivity to that one stochastic corpus layer.
"""
from __future__ import annotations

import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

REPS = [4, 5, 6, 7, 8, 9]
RAWFUZZ_SEEDS = {4: 301, 5: 401, 6: 501, 7: 601, 8: 701, 9: 801}

CELLS = [
    ("htsjdk_vcf", "htsjdk",    "VCF", "pit"),
    ("htsjdk_sam", "htsjdk",    "SAM", "pit"),
    ("vcfpy",      "vcfpy",     "VCF", "mutmut"),
    ("noodles",    "noodles",   "VCF", "cargo_mutants"),
]

# These categories from `seeds/<fmt>/` are *all* what biotest.py produces:
#   - real_world_*, htsjdk_*, bcftools_*, jazzer_*, spec_*, minimal_*,
#     complex_*, clip_*, ...  → externally fetched by Phase A
#   - kept_*                   → Rank 8 corpus_keeper from Phase C MR loop
#   - synthetic_*              → Phase D LLM seed synthesis
# Run-10 includes ALL of them. Only excluded: rank-augmentation prefixes
# from sibling dirs (those are unioned by the Phase-3 drivers, not the
# orchestrator).
SIBLING_RANK_PREFIXES = ("struct_", "rawfuzz_", "diverse_", "bytefuzz_", "bv_")

STRICT_PARSER_SUTS = {"biopython", "noodles"}
# Strict parsers don't benefit from Phase E augmentation — Phase 3
# drivers' auto-union already skips struct/rawfuzz for them. We mirror
# the same policy here for the per-rep staging.


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def regenerate_phase_e(seed: int) -> None:
    """Re-run only Rank 13 (lenient byte fuzzer) with the rep's seed.
    Rank 12 (structural) is deterministic — we don't need to re-run it.
    """
    for fmt in ("VCF", "SAM"):
        out = REPO_ROOT / f"seeds/{fmt.lower()}_rawfuzz"
        if out.exists():
            for f in out.glob("*"):
                if f.is_file():
                    f.unlink()
        subprocess.run([
            "py", "-3.12",
            str(REPO_ROOT / "mr_engine/transforms/lenient_byte_fuzzer.py"),
            "--input", f"seeds/{fmt.lower()}",
            "--output", str(out),
            "--format", fmt,
            "--n-per-seed", "10",
            "--seed", str(seed),
        ], check=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})


def stage_corpus(cell: str, sut: str, fmt: str, rep: int) -> Path:
    """Stage a per-rep RANDOM sample of the auto-pipeline corpus.

    Two changes vs. the prior staging (which copied all files and
    relied on each engine's alphabetical sample cap):

    1. Per-rep random sampling with seed=rep gives each rep a genuinely
       different corpus → real variance signal in the mutation score.
       The previous behaviour (alphabetical cap → kept_* dominates,
       rawfuzz_* never sampled) gave std=0pp because Phase E's per-rep
       rawfuzz regeneration was sorted out of the engine's view.
    2. Sample size matches the engine's effective cap (PIT 300, mutmut
       80, cargo-mutants 120, biopython all-corpus). Engine then sees
       all sampled files instead of further alphabetical truncation.

    Source pool: external primary + kept_* + synthetic_* + (for non-
    strict-parser SUTs) struct_* and a per-rep slice of rawfuzz_*.
    Strict-parser SUTs (biopython, noodles) keep primary-only per the
    Run-5/6 reach-inflation finding.
    """
    rep_root = REPO_ROOT / f"compares/results/coverage/biotest_run1_rep_{rep}/{cell}/run_0/corpus"
    rep_root.mkdir(parents=True, exist_ok=True)
    for existing in rep_root.glob("*"):
        if existing.is_file():
            existing.unlink()
    ext = fmt.lower()
    seed_dir = REPO_ROOT / f"seeds/{ext}"
    struct_dir = REPO_ROOT / f"seeds/{ext}_struct"
    rawfuzz_dir = REPO_ROOT / f"seeds/{ext}_rawfuzz"

    # Build candidate pool
    candidates: list[Path] = []
    # 1) seeds/<fmt>/ — external + kept_* + synthetic_*
    for f in sorted(seed_dir.glob(f"*.{ext}")):
        if any(f.name.startswith(p) for p in SIBLING_RANK_PREFIXES):
            continue
        candidates.append(f)
    # 2) sibling _struct + _rawfuzz dirs (Phase E auto-output) for
    #    non-strict-parser SUTs
    if sut not in STRICT_PARSER_SUTS:
        if struct_dir.is_dir():
            for f in struct_dir.glob(f"*.{ext}"):
                candidates.append(f)
        if rawfuzz_dir.is_dir():
            for f in rawfuzz_dir.glob(f"*.{ext}"):
                candidates.append(f)

    # Sample size = engine's effective cap. Use rep as random seed so
    # each rep sees a different draw.
    sample_caps = {
        "pit": 300, "mutmut": 80, "cargo_mutants": 120,
        "atheris_mutmut": 0,  # 0 = "use all" — biopython keeps full corpus,
                                # MAX_MUTANTS controls fairness instead
        "libfuzzer": 120,
    }
    engine = next(c[3] for c in CELLS if c[0] == cell)
    target_n = sample_caps.get(engine, 0)

    rng = random.Random(rep)
    if target_n > 0 and target_n < len(candidates):
        picked = rng.sample(candidates, target_n)
    else:
        picked = list(candidates)
        rng.shuffle(picked)

    # Copy with a rep-randomised filename prefix so even if the engine
    # internally re-sorts alphabetically, the order is rep-specific.
    for i, src in enumerate(picked):
        dst_name = f"r{rep}_{i:04d}_{src.name}"[:200]  # cap path length
        shutil.copy2(src, rep_root / dst_name)
    log(f"  {cell}: {len(picked)}/{len(candidates)} files sampled "
        f"(rep_seed={rep}, engine={engine}, cap={target_n or 'all'})")
    return rep_root


def launch_cell(cell: str, sut: str, fmt: str, engine: str, rep: int) -> subprocess.Popen:
    corpus = REPO_ROOT / f"compares/results/coverage/biotest_run1_rep_{rep}/{cell}/run_0/corpus"
    out = REPO_ROOT / f"compares/results/mutation/biotest_run1_rep_{rep}/{cell}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    log_file = out / "driver.log"
    log_fp = open(log_file, "w", encoding="utf-8")

    if engine == "pit":
        ctr_name = f"r1rep{rep}-{cell}"
        subprocess.run(["docker", "rm", "-f", ctr_name],
                       capture_output=True, check=False)
        cmd = [
            "docker", "run", "--rm", "--name", ctr_name,
            "-v", f"{REPO_ROOT}:/work", "-w", "/work",
            "-e", f"TOOL=biotest_run1_rep_{rep}",
            "-e", f"FORMATS={fmt}",
            "-e", "THREADS=2",
            "-e", "CORPUS_MAX=300",
            "-e", "REPS=0",
            "biotest-bench:latest",
            "bash", "/work/compares/scripts/phase3_jazzer_pit.sh",
        ]
        env["MSYS_NO_PATHCONV"] = "1"
    elif engine == "mutmut":
        cmd = ["py", "-3.12", "compares/scripts/mutation_driver.py",
               "--tool", "biotest", "--sut", "vcfpy",
               "--corpus", str(corpus), "--out", str(out),
               "--budget", "3600", "--corpus-sample", "80"]
    elif engine == "cargo_mutants":
        cmd = ["py", "-3.12", "compares/scripts/mutation_driver.py",
               "--tool", "biotest", "--sut", "noodles",
               "--corpus", str(corpus), "--out", str(out),
               "--budget", "7200", "--corpus-sample", "120"]
    elif engine == "atheris_mutmut":
        # Match atheris baseline: BUDGET_S=1500 + MAX_MUTANTS=262
        # so we test the same first 262 mutants (shared shuffle seed=42).
        # Atheris's mean reach is 262.5±2.6 over 4 reps; capping at 262
        # gives apples-to-apples reachable across both tools.
        cmd = [
            "bash", "-c",
            f"TOOL=biotest_run1_rep_{rep} BUDGET_S=1500 MAX_MUTANTS=262 "
            f"bash compares/scripts/phase3_atheris_biopython.sh",
        ]
    elif engine == "libfuzzer":
        cmd = ["py", "-3.12", "compares/scripts/mutation_driver.py",
               "--tool", "biotest", "--sut", "seqan3",
               "--corpus", str(corpus), "--out", str(out),
               "--format", "SAM", "--budget", "7200", "--corpus-sample", "120"]
    else:
        raise ValueError(f"unknown engine {engine}")

    log(f"  launch {cell} [{engine}]: {' '.join(cmd[:4])}…")
    proc = subprocess.Popen(cmd, env=env, stdout=log_fp, stderr=log_fp)
    proc._biotest_log_fp = log_fp
    return proc


def read_summary(cell: str, rep: int) -> Optional[dict]:
    out = REPO_ROOT / f"compares/results/mutation/biotest_run1_rep_{rep}/{cell}"
    summary = out / "summary.json"
    if not summary.exists():
        return None
    if cell == "vcfpy":
        d = json.loads(summary.read_text(encoding="utf-8"))
        if d.get("killed", 0) == 0:
            subprocess.run([
                "py", "-3.12",
                "compares/scripts/mutation/rederive_from_meta.py",
                str(out), "--package", "vcfpy",
            ], check=False, capture_output=True)
    if cell == "noodles" and not summary.exists():
        # Synthesise from main_run.log if cargo-mutants didn't write summary.
        return None
    d = json.loads(summary.read_text(encoding="utf-8"))
    ms = d.get("mutation_score", d)
    killed = ms.get("killed", d.get("killed", 0))
    reachable = ms.get("reachable", d.get("reachable", 0))
    if reachable == 0:
        return None
    return {
        "killed": killed,
        "reachable": reachable,
        "score": killed / reachable,
    }


def aggregate(results: dict) -> dict:
    """Per-cell mean ± std across reps."""
    out = {}
    for cell, _, _, _ in CELLS:
        values = [results.get(rep, {}).get(cell)
                  for rep in REPS]
        values = [v for v in values if v is not None]
        if not values:
            out[cell] = {"n": 0}
            continue
        killed = [v["killed"] for v in values]
        reachable = [v["reachable"] for v in values]
        score = [v["score"] for v in values]
        out[cell] = {
            "n": len(values),
            "killed_mean": statistics.mean(killed),
            "killed_std": statistics.stdev(killed) if len(killed) > 1 else 0.0,
            "reach_mean": statistics.mean(reachable),
            "reach_std": statistics.stdev(reachable) if len(reachable) > 1 else 0.0,
            "score_mean": statistics.mean(score),
            "score_std": statistics.stdev(score) if len(score) > 1 else 0.0,
            "rep_values": values,
        }
    return out


def write_report(agg: dict) -> None:
    baselines = {
        "htsjdk_vcf": ("Jazzer (n=4)",       36.15, 1.86),
        "htsjdk_sam": ("Jazzer (n=2)",       23.53, 0.41),
        "vcfpy":       ("Atheris (n=4)",      88.10, 2.18),
        "noodles":     ("cargo-fuzz (n=4)",    9.53, 0.33),
        "biopython":   ("Atheris (n=4 scoped)", 58.00, 0.36),
        "seqan3_sam":  ("libFuzzer (n=3)",    90.57, 0.00),
    }
    pure_random = {
        "htsjdk_vcf": (0.00, 0.00),
        "htsjdk_sam": (1.20, 0.06),
        "vcfpy":       (0.89, 0.10),
        "noodles":     (0.00, 0.00),
        "biopython":   (0.24, 0.47),
        "seqan3_sam":  (7.19, 0.57),
    }
    lines = [
        "# BioTest M3 boost — reps 4..9 mean ± std on auto-pipeline corpus",
        "",
        f"6 additional reps with Rank 13 lenient-byte-fuzz seeds ({RAWFUZZ_SEEDS}).",
        "**Corpus = exactly what `biotest.py` auto-produces** with Phase E",
        "integrated: external primary seeds + Rank 8 `kept_*` (auto from",
        "Phase C MR loop) + Phase D `synthetic_*` + Rank 12 `struct_*` (Phase",
        "E auto) + Rank 13 `rawfuzz_*` (Phase E auto, per-rep seed).",
        "",
        "Strict-parser SUTs (biopython, noodles) skip the Phase E `_struct`/",
        "`_rawfuzz` union per the Run-5/6 reach-inflation finding — same",
        "policy now wired into `mutation_driver.py::_augment_with_phase_e`.",
        "",
        "Per DESIGN §3.3: `score = killed / reachable`.",
        "",
        "## 1. Per-cell mean ± std across 4 reps",
        "",
        "| cell | engine | killed mean ± std | reach mean ± std | **score mean ± std** | best baseline | Δ vs baseline | Δ vs Pure Random |",
        "| :--- | :----- | -----------: | -----------: | -----------: | :---------- | -----------: | -------------: |",
    ]
    for cell, sut, fmt, engine in CELLS:
        a = agg.get(cell, {})
        if a.get("n", 0) == 0:
            lines.append(f"| `{cell}` | {engine} | - | - | MISSING | - | - | - |")
            continue
        bl_name, bl_mean, bl_std = baselines[cell]
        pr_mean, _pr_std = pure_random[cell]
        d_baseline = a["score_mean"] * 100 - bl_mean
        d_pr = a["score_mean"] * 100 - pr_mean
        lines.append(
            f"| `{cell}` | {engine} "
            f"| {a['killed_mean']:.1f} ± {a['killed_std']:.1f} "
            f"| {a['reach_mean']:.1f} ± {a['reach_std']:.1f} "
            f"| **{a['score_mean']*100:.2f}% ± {a['score_std']*100:.2f}pp** "
            f"| {bl_name}: {bl_mean:.2f}% ± {bl_std:.2f} "
            f"| {d_baseline:+.2f}pp "
            f"| {d_pr:+.2f}pp |"
        )

    lines += [
        "",
        "## 2. Per-rep breakdown",
        "",
        "| cell | rep-4 | rep-5 | rep-6 | rep-7 | rep-8 | rep-9 |",
        "| :--- | :---- | :---- | :---- | :---- | :---- | :---- |",
    ]
    for cell, _, _, _ in CELLS:
        a = agg.get(cell, {})
        row = [f"`{cell}`"]
        for v in a.get("rep_values", []):
            row.append(f"{v['killed']}/{v['reachable']}={v['score']*100:.2f}%")
        while len(row) < 7:
            row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## 3. Methodology — why this is the honest 'tool's score'",
        "",
        "Run-8 (the prior 4-rep measurement) excluded `kept_*` and",
        "`synthetic_*` from the staged corpus and manually unioned",
        "`seeds/<fmt>_struct/` + `seeds/<fmt>_rawfuzz/` from operator-",
        "invoked CLI scripts. Two issues with reporting that as the",
        "tool's score:",
        "",
        "1. **Excluded biotest.py's auto-pipeline output** (kept_, synthetic_).",
        "   Those *are* part of the tool's normal Phase A-D output.",
        "2. **Included corpus from manual CLI invocation** (struct_, rawfuzz_)",
        "   that wasn't auto-produced by biotest.py — operator effort the",
        "   reported score didn't deserve credit for.",
        "",
        "Run-10 fixes both: as of 2026-04-23 Phase E integration, biotest.py",
        "automatically produces struct_/rawfuzz_ corpora (no manual",
        "invocation), and this orchestrator stages the **complete auto-",
        "output** corpus (kept_/synthetic_/external/struct_/rawfuzz_).",
        "",
        f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} from "
        "`compares/results/mutation/biotest_run1_rep_*/`.",
    ]
    out_path = REPO_ROOT / "compares/results/mutation/biotest/M3_BOOST_REPS_4_TO_9.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out_path}")
    raw_path = REPO_ROOT / "compares/results/mutation/biotest/m3_boost_raw.json"
    raw_path.write_text(json.dumps({"reps": REPS,
                                     "rawfuzz_seeds": RAWFUZZ_SEEDS,
                                     "aggregate": agg}, indent=2),
                         encoding="utf-8")
    log(f"wrote {raw_path}")


def main():
    started = time.time()
    results = {}

    for rep in REPS:
        seed = RAWFUZZ_SEEDS[rep]
        log(f"=== rep {rep} (rawfuzz_seed={seed}) ===")
        # 1) Re-run Phase E with rep's Rank-13 seed
        log(f"  Phase E (Rank 13 only) seed={seed}")
        regenerate_phase_e(seed)
        # 2) Stage per-cell auto-pipeline corpus
        for cell, sut, fmt, engine in CELLS:
            stage_corpus(cell, sut, fmt, rep)
        # 3) Launch all cells in parallel
        cell_procs = {c[0]: launch_cell(*c, rep) for c in CELLS}
        for cell, proc in cell_procs.items():
            rc = proc.wait()
            proc._biotest_log_fp.close()
            log(f"  {cell} exited rc={rc}")
        # 4) Collect summaries
        rep_results = {}
        for cell, sut, fmt, engine in CELLS:
            r = read_summary(cell, rep)
            if r is None:
                log(f"  {cell}: MISSING summary")
            else:
                log(f"  {cell}: killed={r['killed']} reach={r['reachable']} "
                    f"score={r['score']*100:.2f}%")
            rep_results[cell] = r
        results[rep] = rep_results

    log(f"=== aggregation (elapsed={int(time.time()-started)}s) ===")
    agg = aggregate(results)
    write_report(agg)


if __name__ == "__main__":
    main()
