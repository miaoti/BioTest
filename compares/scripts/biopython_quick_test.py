"""Biopython-only quick test: include Rank 12 + 13 augmentation under
matched-budget (MAX_MUTANTS=262, BUDGET_S=1500) to see if it helps
close the −32pp gap to atheris baseline.

Compares against Run-10v2 biopython baseline (67/262 = 25.57% with
strict-parser policy that EXCLUDED struct/rawfuzz).
"""
from __future__ import annotations

import json
import os
import random
import shutil
import statistics
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def stage_corpus_with_augmentation(rep: int) -> Path:
    """Stage biopython corpus WITH Rank 12 struct + Rank 13 rawfuzz
    augmentation (the 'strict parser' exclusion temporarily lifted).
    Per-rep random sample to expose variance."""
    rep_root = REPO_ROOT / f"compares/results/coverage/bp_quick_test_rep_{rep}/biopython/run_0/corpus"
    rep_root.mkdir(parents=True, exist_ok=True)
    for f in rep_root.glob("*"):
        if f.is_file():
            f.unlink()

    seed_dir = REPO_ROOT / "seeds/sam"
    struct_dir = REPO_ROOT / "seeds/sam_struct"
    rawfuzz_dir = REPO_ROOT / "seeds/sam_rawfuzz"

    rank_prefixes = ("kept_", "synthetic_", "struct_", "rawfuzz_",
                      "diverse_", "bytefuzz_", "bv_")
    candidates: list[Path] = []
    # Primary: external + kept_* + synthetic_* (everything in seeds/sam/
    # that isn't from a sibling rank dir).
    for f in sorted(seed_dir.glob("*.sam")):
        if any(f.name.startswith(p) for p in rank_prefixes):
            # ...except kept_/synthetic_ which ARE seeds/sam/ direct
            # children, not from sibling dirs. Recheck:
            if f.name.startswith(("kept_", "synthetic_")):
                candidates.append(f)
            continue
        candidates.append(f)
    # +Rank 12 struct
    if struct_dir.is_dir():
        for f in struct_dir.glob("*.sam"):
            candidates.append(f)
    # +Rank 13 rawfuzz
    if rawfuzz_dir.is_dir():
        for f in rawfuzz_dir.glob("*.sam"):
            candidates.append(f)

    # Per-rep random subset — biopython phase3_mutation_loop reads ALL
    # corpus files for baseline computation, so the size affects per-
    # mutant time. Cap at ~250 to keep replay fast (similar to atheris's
    # 390-file regime).
    rng = random.Random(rep)
    target = 250
    if len(candidates) > target:
        picked = rng.sample(candidates, target)
    else:
        picked = list(candidates)
        rng.shuffle(picked)

    for i, src in enumerate(picked):
        dst_name = f"r{rep}_{i:04d}_{src.name}"[:200]
        shutil.copy2(src, rep_root / dst_name)
    log(f"  rep {rep}: {len(picked)}/{len(candidates)} files staged "
        f"(includes struct + rawfuzz)")
    return rep_root


def launch_biopython(rep: int) -> subprocess.Popen:
    out = REPO_ROOT / f"compares/results/mutation/bp_quick_test_rep_{rep}/biopython"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    log_fp = open(out / "driver.log", "w", encoding="utf-8")

    cmd = [
        "bash", "-c",
        f"TOOL=bp_quick_test_rep_{rep} BUDGET_S=1500 MAX_MUTANTS=262 "
        f"bash compares/scripts/phase3_atheris_biopython.sh",
    ]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    log(f"  launch biopython rep {rep}")
    proc = subprocess.Popen(cmd, env=env, stdout=log_fp, stderr=log_fp)
    proc._biotest_log_fp = log_fp
    return proc


def read_summary(rep: int) -> dict | None:
    p = REPO_ROOT / f"compares/results/mutation/bp_quick_test_rep_{rep}/biopython/summary.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    ms = d.get("mutation_score", d)
    k = ms.get("killed", d.get("killed", 0))
    r = ms.get("reachable", d.get("reachable", 0))
    if not r:
        return None
    return {"killed": k, "reachable": r, "score": k / r}


def main():
    REPS = [0, 1, 2, 3]
    started = time.time()
    log("=== biopython quick test: Rank 12+13 enabled, matched budget ===")
    log("    BUDGET_S=1500, MAX_MUTANTS=262 (same first 262 mutants as atheris baseline)")

    # Stage all 4 reps' corpora
    for rep in REPS:
        stage_corpus_with_augmentation(rep)

    # Run reps serially — parallel docker invocations from WSL race on
    # the docker.exe broker handshake.
    for rep in REPS:
        proc = launch_biopython(rep)
        rc = proc.wait()
        proc._biotest_log_fp.close()
        log(f"  rep {rep} exited rc={rc}")

    # Collect results
    results = {}
    for rep in REPS:
        r = read_summary(rep)
        if r is None:
            log(f"  rep {rep}: MISSING")
        else:
            log(f"  rep {rep}: killed={r['killed']}/{r['reachable']} score={r['score']*100:.2f}%")
        results[rep] = r

    # Aggregate
    valid = [v for v in results.values() if v is not None]
    if valid:
        kills = [v["killed"] for v in valid]
        reach = [v["reachable"] for v in valid]
        scores = [v["score"] for v in valid]
        log("")
        log(f"=== summary (elapsed={int(time.time()-started)}s) ===")
        log(f"  killed: mean={statistics.mean(kills):.1f} std={statistics.stdev(kills) if len(kills)>1 else 0:.1f}  per_rep={kills}")
        log(f"  reach:  mean={statistics.mean(reach):.1f} std={statistics.stdev(reach) if len(reach)>1 else 0:.1f}  per_rep={reach}")
        log(f"  score:  mean={statistics.mean(scores)*100:.2f}% std={(statistics.stdev(scores) if len(scores)>1 else 0)*100:.2f}pp")
        log("")
        log(f"  Run-10v2 baseline (no augmentation, same matched budget): 67/262 = 25.57%")
        log(f"  Atheris baseline (n=4, scoped):                            152.2/262.5 = 58.00% ± 0.36pp")


if __name__ == "__main__":
    main()
