"""Run BioTest mutation scoring across 4 independent reps and aggregate.

Mechanism:
- For each rep in {0..3}, regenerate the stochastic corpus-layer (Rank 13
  lenient byte fuzzer with a rep-specific seed + rep-specific random
  sampling of the rawfuzz subset).
- Stage a fresh per-rep corpus per cell under
  `compares/results/coverage/biotest_rep_<N>/<cell>/run_0/corpus/`.
- Launch each cell's mutation engine in parallel (Docker per cell).
- Collect per-rep summaries once all cells complete.
- After all 4 reps, compute mean ± std per cell and write RUN8_FINAL.md.

Design-level: the only randomness we *have* to vary is Rank 13 (byte-
level fuzz) and random sampling. Everything else (Ranks 9/11/12, primary
seeds, mutation operators) is deterministic. If a cell happens to
include no stochastic corpus content (e.g. biopython is primary-only
by policy), its 4 reps will land identical — std == 0 is the honest
answer, not a bug.
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

REPS = [0, 1, 2, 3]
RAWFUZZ_SEEDS = [0, 42, 100, 200]  # per-rep Rank 13 seed

CELLS = [
    # (cell_name, sut, format, engine)
    ("htsjdk_vcf", "htsjdk",    "VCF", "pit"),
    ("htsjdk_sam", "htsjdk",    "SAM", "pit"),
    ("vcfpy",      "vcfpy",     "VCF", "mutmut"),
    ("noodles",    "noodles",   "VCF", "cargo_mutants"),
    ("biopython",  "biopython", "SAM", "atheris_mutmut"),
    ("seqan3_sam", "seqan3",    "SAM", "libfuzzer"),
]

STRICT_PARSER_SUTS = {"biopython", "noodles"}
# biopython stays on primary-only (struct/rawfuzz inflate reach without
# adding kills, per Run-5/6 post-mortem). Other cells get the full stack.


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def regenerate_rawfuzz(seed: int) -> None:
    """Regenerate seeds/<fmt>_rawfuzz/ with the given seed."""
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


def stage_corpus(
    cell: str, sut: str, fmt: str, rep: int, sample_seed: int,
) -> Path:
    """Stage primary + struct + (optional) rawfuzz into rep-specific dir."""
    rep_root = REPO_ROOT / f"compares/results/coverage/biotest_rep_{rep}/{cell}/run_0/corpus"
    rep_root.mkdir(parents=True, exist_ok=True)
    for existing in rep_root.glob("*"):
        if existing.is_file():
            existing.unlink()
    ext = fmt.lower()
    seed_dir = REPO_ROOT / f"seeds/{ext}"
    struct_dir = REPO_ROOT / f"seeds/{ext}_struct"
    rawfuzz_dir = REPO_ROOT / f"seeds/{ext}_rawfuzz"
    rank_prefixes = ("kept_", "diverse_", "bytefuzz_", "bv_", "struct_", "rawfuzz_")

    # Primary seeds (always included)
    for f in sorted(seed_dir.glob(f"*.{ext}")):
        if not f.name.startswith(rank_prefixes):
            shutil.copy2(f, rep_root / f.name)

    if sut not in STRICT_PARSER_SUTS:
        # Struct (deterministic — same set every rep)
        if struct_dir.is_dir():
            for f in sorted(struct_dir.glob(f"*.{ext}")):
                shutil.copy2(f, rep_root / f.name)
        # Rawfuzz (per-rep sample)
        if rawfuzz_dir.is_dir():
            rng = random.Random(sample_seed)
            all_rawfuzz = sorted(rawfuzz_dir.glob(f"*.{ext}"))
            picked = rng.sample(all_rawfuzz, min(50, len(all_rawfuzz)))
            for f in picked:
                shutil.copy2(f, rep_root / f.name)

    return rep_root


def launch_cell(cell: str, sut: str, fmt: str, engine: str, rep: int) -> subprocess.Popen:
    """Launch mutation run for one cell as a background subprocess.
    Returns the Popen so caller can wait on it later."""
    corpus = REPO_ROOT / f"compares/results/coverage/biotest_rep_{rep}/{cell}/run_0/corpus"
    out = REPO_ROOT / f"compares/results/mutation/biotest_rep_{rep}/{cell}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    log_file = out / "driver.log"
    log_fp = open(log_file, "w", encoding="utf-8")

    if engine == "pit":
        # phase3_jazzer_pit.sh uses javac/java/python3.12 which live in
        # biotest-bench; run the whole script inside the container.
        ctr_name = f"rep{rep}-{cell}"
        # Remove any stale container with same name
        subprocess.run(["docker", "rm", "-f", ctr_name],
                       capture_output=True, check=False)
        cmd = [
            "docker", "run", "--rm", "--name", ctr_name,
            "-v", f"{REPO_ROOT}:/work", "-w", "/work",
            "-e", f"TOOL=biotest_rep_{rep}",
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
        # env= on subprocess.Popen doesn't propagate reliably to bash
        # subprocesses spawned through docker bind mounts on Windows
        # (observed rep-0 2026-04-23: TOOL/BUDGET_S defaulted despite
        # env.update). Put the vars inline via `bash -c VAR=val ...`
        # so they are definitely exported before the script runs.
        cmd = [
            "bash", "-c",
            f"TOOL=biotest_rep_{rep} BUDGET_S=1800 "
            f"bash compares/scripts/phase3_atheris_biopython.sh",
        ]
    elif engine == "libfuzzer":
        cmd = ["py", "-3.12", "compares/scripts/mutation_driver.py",
               "--tool", "biotest", "--sut", "seqan3",
               "--corpus", str(corpus), "--out", str(out),
               "--format", "SAM", "--budget", "7200", "--corpus-sample", "120"]
    else:
        raise ValueError(f"unknown engine {engine}")

    log(f"  launch {cell} [{engine}]: {' '.join(cmd[:4])}...")
    proc = subprocess.Popen(cmd, env=env, stdout=log_fp, stderr=log_fp)
    proc._biotest_log_fp = log_fp  # keep fp alive
    return proc


def read_summary(cell: str, rep: int) -> Optional[dict]:
    """Read {cell}/summary.json and normalise to {killed, reachable, score}.
    For mutmut cells, rederive from .meta if summary is the broken text
    parse."""
    out = REPO_ROOT / f"compares/results/mutation/biotest_rep_{rep}/{cell}"
    summary = out / "summary.json"
    if not summary.exists():
        return None
    # For vcfpy we may need to rederive
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
    score = killed / reachable if reachable > 0 else 0.0
    return {"killed": killed, "reachable": reachable, "score": score}


def wait_for_cells(cell_procs: dict) -> dict:
    """Wait for all cell processes to exit. Returns {cell: returncode}."""
    results = {}
    for cell, proc in cell_procs.items():
        rc = proc.wait()
        proc._biotest_log_fp.close()
        results[cell] = rc
        log(f"  {cell} exited rc={rc}")
    return results


def aggregate(results: dict) -> dict:
    """Given {rep_id: {cell: {killed, reachable, score}}}, compute per-cell
    mean ± std across reps."""
    out = {}
    for cell, _, _, _ in CELLS:
        values = []
        for rep in REPS:
            r = results.get(rep, {}).get(cell)
            if r is not None:
                values.append(r)
        if not values:
            out[cell] = {"n": 0, "mean_killed": 0, "mean_reachable": 0,
                         "mean_score": 0, "std_killed": 0,
                         "std_reachable": 0, "std_score": 0,
                         "rep_values": []}
            continue
        killed = [v["killed"] for v in values]
        reachable = [v["reachable"] for v in values]
        score = [v["score"] for v in values]
        out[cell] = {
            "n": len(values),
            "mean_killed": statistics.mean(killed),
            "mean_reachable": statistics.mean(reachable),
            "mean_score": statistics.mean(score),
            "std_killed": statistics.stdev(killed) if len(killed) > 1 else 0.0,
            "std_reachable": statistics.stdev(reachable) if len(reachable) > 1 else 0.0,
            "std_score": statistics.stdev(score) if len(score) > 1 else 0.0,
            "rep_values": values,
        }
    return out


def write_report(agg: dict, out_path: Path) -> None:
    """Write the mean ± std comparison table."""
    baselines = {
        "htsjdk_vcf": ("jazzer",       233, 628, 0.3710),
        "htsjdk_sam": ("jazzer",       161, 630, 0.2556),
        "vcfpy":       ("atheris",      852, 951, 0.8959),
        "noodles":     ("cargo_fuzz",    28, 299, 0.0936),
        "biopython":   ("atheris",      155, 265, 0.5849),
        "seqan3_sam":  ("libfuzzer",     48,  53, 0.9057),
    }
    lines = [
        "# BioTest Run-8 — 4-rep mean ± std mutation score",
        "",
        "4 independent reps with different Rank 13 lenient-fuzz seeds + random",
        f"corpus samples ({RAWFUZZ_SEEDS}).  Score per DESIGN §3.3 (killed / reachable).",
        "",
        "## Per-cell mean ± std across 4 reps",
        "",
        "| cell | engine | k mean±std | reach mean±std | score mean±std | baseline | Δ vs baseline |",
        "| :--- | :----- | ---------: | -------------: | -------------: | :------- | ------------: |",
    ]
    for cell, sut, fmt, engine in CELLS:
        a = agg.get(cell, {})
        if not a or a.get("n", 0) == 0:
            lines.append(f"| `{cell}` | {engine} | - | - | MISSING | - | - |")
            continue
        base_tool, base_k, base_r, base_s = baselines[cell]
        score_delta = a["mean_score"] - base_s
        lines.append(
            f"| `{cell}` | {engine} "
            f"| {a['mean_killed']:.1f} ± {a['std_killed']:.1f} "
            f"| {a['mean_reachable']:.1f} ± {a['std_reachable']:.1f} "
            f"| **{a['mean_score']*100:.2f}% ± {a['std_score']*100:.2f}pp** "
            f"| {base_tool} {base_s*100:.2f}% ({base_k}/{base_r}) "
            f"| {score_delta*100:+.2f}pp |"
        )

    lines += [
        "",
        "## Per-rep breakdown",
        "",
        "| cell | rep-0 | rep-1 | rep-2 | rep-3 |",
        "| :--- | :---- | :---- | :---- | :---- |",
    ]
    for cell, sut, fmt, engine in CELLS:
        a = agg.get(cell, {})
        row = [f"`{cell}`"]
        for i, v in enumerate(a.get("rep_values", [])):
            row.append(f"{v['killed']}/{v['reachable']}={v['score']*100:.2f}%")
        while len(row) < 5:
            row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} from "
        f"`compares/results/mutation/biotest_rep_*/`.",
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out_path}")


def main():
    results = {}  # rep -> {cell: {killed, reachable, score}}
    started = time.time()

    for rep in REPS:
        rep_seed_rawfuzz = RAWFUZZ_SEEDS[rep]
        log(f"=== rep {rep} (rawfuzz_seed={rep_seed_rawfuzz}) ===")

        # 1. Regenerate rawfuzz with rep-specific seed
        log(f"  regenerating Rank 13 rawfuzz seed={rep_seed_rawfuzz}")
        regenerate_rawfuzz(rep_seed_rawfuzz)

        # 2. Stage per-cell corpora
        for cell, sut, fmt, engine in CELLS:
            stage_corpus(cell, sut, fmt, rep, sample_seed=rep)

        # 3. Launch all cells in parallel
        cell_procs = {}
        for cell, sut, fmt, engine in CELLS:
            cell_procs[cell] = launch_cell(cell, sut, fmt, engine, rep)

        # 4. Wait for all
        wait_for_cells(cell_procs)

        # 5. Collect results
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

    # Aggregate + write
    log(f"=== aggregation (elapsed={int(time.time()-started)}s) ===")
    agg = aggregate(results)
    report_path = REPO_ROOT / "compares/results/mutation/biotest/RUN8_MEAN_STD.md"
    write_report(agg, report_path)
    # Also dump raw JSON
    raw_path = REPO_ROOT / "compares/results/mutation/biotest/run8_raw.json"
    raw_path.write_text(json.dumps({
        "reps": REPS,
        "rawfuzz_seeds": RAWFUZZ_SEEDS,
        "per_rep": results,
        "aggregate": agg,
    }, indent=2), encoding="utf-8")
    log(f"wrote {raw_path}")


if __name__ == "__main__":
    main()
