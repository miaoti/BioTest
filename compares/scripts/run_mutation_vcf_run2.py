"""Standalone Run-2 VCF-only n=10 mutation grading (Option A).

Re-grades the three VCF cells (htsjdk/VCF, vcfpy, noodles) over n=10
fresh, independent reps. Reuses the Phase A--D corpora produced by
the Run-1 BioTest pipeline (input at
`compares/results/coverage/biotest_run1_rep_{N}/{cell}/run_0/corpus/`)
so the experiment is "fresh mutation grading on existing BioTest
output," not a fresh end-to-end pipeline.

Independence from Run-1 grading:
  - Disjoint Phase-E Rank-13 (lenient byte fuzzer) seeds
    (RUN2_RAWFUZZ_SEEDS = 1000 + rep), so the per-rep rawfuzz_*
    files differ from Run-1.
  - Disjoint per-rep corpus-sampling RNG (random.Random(rep + 5000)),
    so the engine's effective input slice differs.
  - Output directory `compares/results/mutation/biotest_run2_vcf_rep_{N}/{cell}`,
    so Run-1 mutation results are untouched.

Same protocol per DESIGN.md sec.3.3 and sec.4 in every other respect:
identical mutation engine per cell (PIT for htsjdk/VCF, mutmut for
vcfpy, cargo-mutants for noodles), identical target-class scope,
identical kill semantics (parse-success flip / canonical-JSON
divergence / crash-class flip), score = killed / reachable.
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

REPS = list(range(10))                         # 0..9 = 10 reps
RUN2_RAWFUZZ_SEEDS = {r: 1000 + r for r in REPS}
SAMPLE_RNG_OFFSET = 5000                       # disjoint from Run-1's rng

CELLS = [
    ("htsjdk_vcf", "htsjdk",  "VCF", "pit"),
    ("vcfpy",      "vcfpy",   "VCF", "mutmut"),
    ("noodles",    "noodles", "VCF", "cargo_mutants"),
]

SIBLING_RANK_PREFIXES = ("struct_", "rawfuzz_", "diverse_", "bytefuzz_", "bv_")
STRICT_PARSER_SUTS = {"biopython", "noodles"}


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def regenerate_phase_e(seed: int) -> None:
    """Re-run Rank 13 (lenient byte fuzzer) with this rep's seed."""
    for fmt in ("VCF",):                       # VCF-only
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

    Source pool: external primary + kept_* + synthetic_* + (for
    non-strict-parser SUTs) struct_* + a per-rep slice of rawfuzz_*.
    Strict-parser SUTs (noodles) keep primary-only.
    """
    rep_root = REPO_ROOT / (
        f"compares/results/coverage/biotest_run1_rep_{rep}/{cell}/run_0/corpus_run2"
    )
    rep_root.mkdir(parents=True, exist_ok=True)
    for existing in rep_root.glob("*"):
        if existing.is_file():
            existing.unlink()
    ext = fmt.lower()
    seed_dir = REPO_ROOT / f"seeds/{ext}"
    struct_dir = REPO_ROOT / f"seeds/{ext}_struct"
    rawfuzz_dir = REPO_ROOT / f"seeds/{ext}_rawfuzz"

    candidates: list[Path] = []
    for f in sorted(seed_dir.glob(f"*.{ext}")):
        if any(f.name.startswith(p) for p in SIBLING_RANK_PREFIXES):
            continue
        candidates.append(f)
    if sut not in STRICT_PARSER_SUTS:
        if struct_dir.is_dir():
            for f in struct_dir.glob(f"*.{ext}"):
                candidates.append(f)
        if rawfuzz_dir.is_dir():
            for f in rawfuzz_dir.glob(f"*.{ext}"):
                candidates.append(f)

    sample_caps = {"pit": 300, "mutmut": 80, "cargo_mutants": 120}
    engine = next(c[3] for c in CELLS if c[0] == cell)
    target_n = sample_caps.get(engine, 0)

    rng = random.Random(rep + SAMPLE_RNG_OFFSET)
    if target_n > 0 and target_n < len(candidates):
        picked = rng.sample(candidates, target_n)
    else:
        picked = list(candidates)
        rng.shuffle(picked)

    for i, src in enumerate(picked):
        dst_name = f"r2{rep}_{i:04d}_{src.name}"[:200]
        shutil.copy2(src, rep_root / dst_name)
    log(f"  {cell}: {len(picked)}/{len(candidates)} files sampled "
        f"(rep_seed={rep+SAMPLE_RNG_OFFSET}, engine={engine}, "
        f"cap={target_n or 'all'})")
    return rep_root


def launch_cell(cell: str, sut: str, fmt: str, engine: str,
                rep: int) -> subprocess.Popen:
    corpus = REPO_ROOT / (
        f"compares/results/coverage/biotest_run1_rep_{rep}/{cell}/run_0/corpus_run2"
    )
    out = REPO_ROOT / f"compares/results/mutation/biotest_run2_vcf_rep_{rep}/{cell}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    log_file = out / "driver.log"
    log_fp = open(log_file, "w", encoding="utf-8")

    if engine == "pit":
        ctr_name = f"r2vcf-rep{rep}-{cell}"
        subprocess.run(["docker", "rm", "-f", ctr_name],
                       capture_output=True, check=False)
        # phase3_jazzer_pit.sh discovers the corpus from
        # compares/results/coverage/<TOOL>_rep_{REP}/<cell>/run_0/corpus,
        # so we point TOOL at biotest_run2_vcf and stage the same dir.
        # We use a parallel "corpus_run2" subdir, so we need the script
        # to read from there. The existing script reads .../corpus/, so
        # we instead point TOOL at a freshly-prepared sibling directory.
        run2_corpus_dir = REPO_ROOT / (
            f"compares/results/coverage/biotest_run2_vcf_rep_{rep}/{cell}/run_0/corpus"
        )
        run2_corpus_dir.parent.mkdir(parents=True, exist_ok=True)
        if run2_corpus_dir.exists():
            shutil.rmtree(run2_corpus_dir)
        shutil.copytree(corpus, run2_corpus_dir)
        cmd = [
            "docker", "run", "--rm", "--name", ctr_name,
            "-v", f"{REPO_ROOT}:/work", "-w", "/work",
            "-e", f"TOOL=biotest_run2_vcf_rep_{rep}",
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
    else:
        raise ValueError(f"unknown engine {engine}")

    log(f"  launch {cell} [{engine}]: {' '.join(cmd[:4])}…")
    proc = subprocess.Popen(cmd, env=env, stdout=log_fp, stderr=log_fp)
    proc._biotest_log_fp = log_fp
    return proc


def read_summary(cell: str, rep: int) -> Optional[dict]:
    if cell == "htsjdk_vcf":
        # phase3_jazzer_pit.sh writes its summary under TOOL=biotest_run2_vcf,
        # which lands in biotest_run2_vcf_rep_{rep}/{cell}.
        out = REPO_ROOT / (
            f"compares/results/mutation/biotest_run2_vcf_rep_{rep}/{cell}"
        )
    else:
        out = REPO_ROOT / (
            f"compares/results/mutation/biotest_run2_vcf_rep_{rep}/{cell}"
        )
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
    d = json.loads(summary.read_text(encoding="utf-8"))
    ms = d.get("mutation_score", d)
    killed = ms.get("killed", d.get("killed", 0))
    reachable = ms.get("reachable", d.get("reachable", 0))
    if reachable == 0:
        return None
    return {"killed": killed, "reachable": reachable,
            "score": killed / reachable}


def aggregate(results: dict) -> dict:
    out = {}
    for cell, _, _, _ in CELLS:
        values = [results.get(rep, {}).get(cell) for rep in REPS]
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
    paper_run1 = {
        "htsjdk_vcf": (32.40, 0.71),
        "vcfpy":      (85.66, 0.14),
        "noodles":    ( 8.10, 0.27),
    }
    baselines = {
        "htsjdk_vcf": ("Jazzer (n=10)",     36.59, 1.34),
        "vcfpy":      ("Atheris (n=6)",     87.37, 1.83),
        "noodles":    ("cargo-fuzz (n=9)",   8.74, 1.91),
    }
    pure_random = {
        "htsjdk_vcf": (0.00, 0.00),
        "vcfpy":      (0.89, 0.10),
        "noodles":    (0.00, 0.00),
    }
    lines = [
        "# Run-2 VCF-only n=10 mutation grading (standalone replication)",
        "",
        "Independent replication of the Run-1 mutation grading on the",
        "three VCF cells. Reuses Run-1 BioTest pipeline corpora as input",
        "(Option A); fresh per-rep Rank-13 lenient-byte-fuzz seeds (1000+rep)",
        "and disjoint corpus-sampling RNG (rep + 5000) so the slice fed",
        "to the engine is a fresh draw.",
        "",
        "## 1. Per-cell mean ± std across 10 reps",
        "",
        "| cell | engine | killed | reach | **Run-2 score** | Run-1 (paper) | Δ vs Run-1 | Best baseline | Δ vs baseline | Δ vs Pure-Random |",
        "| :--- | :----- | -----: | ----: | ----: | ----: | ----: | :----- | ----: | ----: |",
    ]
    for cell, sut, fmt, engine in CELLS:
        a = agg.get(cell, {})
        if a.get("n", 0) == 0:
            lines.append(f"| `{cell}` | {engine} | - | - | MISSING | - | - | - | - | - |")
            continue
        run1_mean, run1_std = paper_run1[cell]
        bl_name, bl_mean, bl_std = baselines[cell]
        pr_mean, _pr_std = pure_random[cell]
        run2_pct = a["score_mean"] * 100
        run2_std_pp = a["score_std"] * 100
        lines.append(
            f"| `{cell}` | {engine} "
            f"| {a['killed_mean']:.1f}±{a['killed_std']:.1f} "
            f"| {a['reach_mean']:.1f}±{a['reach_std']:.1f} "
            f"| **{run2_pct:.2f}±{run2_std_pp:.2f}pp** "
            f"| {run1_mean:.2f}±{run1_std:.2f}pp "
            f"| {run2_pct - run1_mean:+.2f}pp "
            f"| {bl_name}: {bl_mean:.2f}±{bl_std:.2f} "
            f"| {run2_pct - bl_mean:+.2f}pp "
            f"| {run2_pct - pr_mean:+.2f}pp |"
        )

    lines += ["", "## 2. Per-rep breakdown", "",
              "| cell | rep-0 | rep-1 | rep-2 | rep-3 | rep-4 | rep-5 | rep-6 | rep-7 | rep-8 | rep-9 |",
              "| :--- | " + " | ".join([":--"] * 10) + " |"]
    for cell, _, _, _ in CELLS:
        a = agg.get(cell, {})
        row = [f"`{cell}`"]
        for v in a.get("rep_values", []):
            row.append(f"{v['killed']}/{v['reachable']}={v['score']*100:.2f}%")
        while len(row) < 11:
            row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    lines += ["", "## 3. Methodology",
              "",
              "Same DESIGN sec 3.3 / sec 4 protocol as Run-1: identical mutation",
              "engine per cell (PIT for htsjdk, mutmut for vcfpy, cargo-mutants",
              "for noodles), identical target-class scope, identical kill",
              "semantics. score = killed / reachable.",
              "",
              "Independence from Run-1: per-rep RAWFUZZ seed = 1000+rep,",
              "per-rep corpus-sampling RNG = rep+5000. Run-1 used 100+rep",
              "and rep respectively, so the two runs are disjoint draws.",
              "",
              f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} from "
              "`compares/results/mutation/biotest_run2_vcf_rep_*/`."]

    out_dir = REPO_ROOT / "compares/results/mutation/biotest_run2_vcf"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "RUN2_VCF.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out_path}")
    raw_path = out_dir / "run2_vcf_raw.json"
    raw_path.write_text(json.dumps({
        "reps": REPS,
        "rawfuzz_seeds": RUN2_RAWFUZZ_SEEDS,
        "sample_rng_offset": SAMPLE_RNG_OFFSET,
        "aggregate": agg,
    }, indent=2), encoding="utf-8")
    log(f"wrote {raw_path}")


def regenerate_phase_e_struct() -> None:
    """One-time Rank-12 (structural diversifier) regen for VCF.

    Rank 12 is deterministic, so it's done once before the rep loop
    rather than per-rep like Rank 13.
    """
    out = REPO_ROOT / "seeds/vcf_struct"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*"):
        if f.is_file():
            f.unlink()
    subprocess.run([
        "py", "-3.12",
        str(REPO_ROOT / "mr_engine/transforms/structural_diversifier.py"),
        "--input", "seeds/vcf",
        "--output", str(out),
        "--format", "VCF",
    ], check=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})


def main():
    started = time.time()
    results = {}

    # CLI override: --reps 0,1,2 runs that subset; --reps 0 runs only rep 0.
    reps = REPS
    if len(sys.argv) > 1 and sys.argv[1] == "--reps":
        reps = [int(r) for r in sys.argv[2].split(",")]
    log(f"reps to run: {reps}")

    log("=== one-time Rank-12 structural diversifier regen ===")
    regenerate_phase_e_struct()

    for rep in reps:
        seed = RUN2_RAWFUZZ_SEEDS[rep]
        log(f"=== rep {rep} (rawfuzz_seed={seed}) ===")
        log(f"  Phase E (Rank 13, VCF only) seed={seed}")
        regenerate_phase_e(seed)
        for cell, sut, fmt, engine in CELLS:
            stage_corpus(cell, sut, fmt, rep)
        cell_procs = {c[0]: launch_cell(*c, rep) for c in CELLS}
        for cell, proc in cell_procs.items():
            rc = proc.wait()
            proc._biotest_log_fp.close()
            log(f"  {cell} exited rc={rc}")
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
