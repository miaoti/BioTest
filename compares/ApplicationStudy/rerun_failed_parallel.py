"""Rerun failed cells with parallelism across config strands.

Improves on rerun_failed.py by:
  * Grouping failures by (config, run_id) so one run_4rep.py invocation
    handles multiple cells of the same big run via --only repeated.
  * Running E0/E1S/E2 strands in parallel threads — each strand does its
    own groups serially. Per-strand serialization is required because
    multiple seqan3 cells share /work/harnesses/cpp/build/*.gcda inside
    the docker container and would contaminate each other.
  * Each run_4rep.py uses --max-workers=3 internally, so cells WITHIN a
    group run in parallel.

Why parallel-across-strand only: rerun_failed.py iterated all 25 failed
(config, run_id, cell) tuples in a single sequential loop with --max-workers
1, which would take ~125h. Parallel-across-strand cuts that to ~18h while
preserving seqan3 isolation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
RUN_4REP = ROOT / "run_4rep.py"

CELLS_BY_LABEL = {
    "htsjdk_vcf":     "VCF",
    "vcfpy_vcf":      "VCF",
    "noodles_vcf":    "VCF",
    "htsjdk_sam":     "SAM",
    "biopython_sam":  "SAM",
    "seqan3_sam":     "SAM",
}

CONFIGS = {
    "E0":  {"sub": "E0_baseline",     "layout": "big_runs", "ids": ["a", "b", "c", "d"], "reps": 3, "cum": "true"},
    "E1S": {"sub": "E1S_strict",      "layout": "big_runs", "ids": ["a", "b", "c", "d"], "reps": 3, "cum": "true"},
    "E2":  {"sub": "E2_no_phase_d",   "layout": "reps",     "ids": [0, 1, 2, 3],         "reps": 4, "cum": "false"},
    "E3":  {"sub": "E3_no_a_no_d",    "layout": "reps",     "ids": [0, 1, 2, 3],         "reps": 4, "cum": "false"},
}

LOG_LOCK = threading.Lock()

# Multiple strands can run cells in parallel EXCEPT seqan3 cells, which
# share /work/harnesses/cpp/build/*.gcda inside the docker container.
# Two parallel seqan3 cascades would mutually wipe each other's coverage
# data because run_4rep.py:790 wipes .gcda at the start of every rep.
SEQAN3_LOCK = threading.Lock()


def _log(strand: str, msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] [{strand:>4s}] {msg}"
    with LOG_LOCK:
        try:
            print(line, flush=True)
        except UnicodeEncodeError:
            sys.stdout.buffer.write((line + "\n").encode("utf-8", errors="replace"))
            sys.stdout.buffer.flush()


def _expected_paths(config: str, run_id, cell: str):
    cfg = CONFIGS[config]
    sub = cfg["sub"]
    n_reps = cfg["reps"]
    if cfg["layout"] == "big_runs":
        base = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                "results_4big_runs" / f"run_{run_id}" / cell)
    else:
        base = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                "results_4rep" / cell)
    return [base / f"run_{r}" / "measurement.json" for r in range(n_reps)]


def detect_failures() -> dict:
    """Returns {(config, run_id, cell) -> reason}."""
    failures = {}
    for config in CONFIGS:
        for run_id in CONFIGS[config]["ids"]:
            for cell in CELLS_BY_LABEL:
                paths = _expected_paths(config, run_id, cell)
                n_ok = 0
                for p in paths:
                    if not p.exists():
                        continue
                    try:
                        d = json.loads(p.read_text())
                        if d.get("status") == "ok" and d.get("total", 0) > 0:
                            n_ok += 1
                    except Exception:
                        pass
                n_expected = len(paths)
                if n_ok < n_expected:
                    failures[(config, run_id, cell)] = (
                        f"only {n_ok}/{n_expected} reps with status=ok"
                    )
    return failures


def _out_root(config: str, run_id) -> Path:
    cfg = CONFIGS[config]
    sub = cfg["sub"]
    if cfg["layout"] == "big_runs":
        return (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                "results_4big_runs" / f"run_{run_id}")
    return (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
            "results_4rep")


def rerun_group(config: str, run_id, cells: list[str], strand: str,
                max_workers: int) -> int:
    """Nuke each cell's work dir and re-run cascade with one run_4rep.py
    invocation using --only repeated and --max-workers.

    seqan3 cells share /work/harnesses/cpp/build/*.gcda inside the
    container, so we serialize them with SEQAN3_LOCK across strands.
    The initial container setup is also serialized with SETUP_LOCK.
    """
    cfg = CONFIGS[config]
    out_root = _out_root(config, run_id)

    for cell in cells:
        cell_dir = out_root / cell
        if cell_dir.exists():
            _log(strand, f"nuking {cell_dir}")
            shutil.rmtree(cell_dir, ignore_errors=True)

    cmd = [
        sys.executable, str(RUN_4REP),
        "--mode", config,
        "--reps", str(cfg["reps"]),
        "--cumulative", cfg["cum"],
        "--max-workers", str(max_workers),
        "--out-root", str(out_root),
    ]
    for cell in cells:
        cmd += ["--only", cell]

    has_seqan3 = "seqan3_sam" in cells

    if has_seqan3:
        _log(strand, f"waiting for SEQAN3_LOCK ({config}/{run_id})")
        SEQAN3_LOCK.acquire()
        _log(strand, f"acquired SEQAN3_LOCK")
    try:
        _log(strand, f"rerun cmd: {' '.join(cmd)}")
        t0 = time.time()
        proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
        elapsed = (time.time() - t0) / 60
        _log(strand, f"rerun done rc={proc.returncode} elapsed={elapsed:.1f}min")
        return proc.returncode
    finally:
        if has_seqan3:
            SEQAN3_LOCK.release()
            _log(strand, f"released SEQAN3_LOCK")


def run_strand(config: str, groups: list[tuple[object, list[str]]],
               max_workers_per_group: int) -> dict:
    """Run all (run_id, cells) groups for a config sequentially."""
    strand = config
    _log(strand, f"strand start: {len(groups)} group(s)")
    results = []
    for run_id, cells in groups:
        _log(strand, f"=== group {config}/{run_id} cells={cells} ===")
        rc = rerun_group(config, run_id, cells, strand, max_workers_per_group)
        results.append({"run_id": run_id, "cells": cells, "rc": rc})
    _log(strand, "strand complete")
    return {"config": config, "results": results}


def prewarm_container_binaries() -> None:
    """Build seqan3 cov binary + ensure container deps are present BEFORE
    spawning strands so concurrent run_4rep.py invocations skip the rebuild
    branch (idempotent: clang is invoked only when source is newer)."""
    setup_cmd = (
        "set -e; export PATH=/root/.cargo/bin:$PATH; "
        "if [ ! -x /work/harnesses/cpp/build/biotest_harness_cov_seqan3 ] "
        "   || [ /work/harnesses/cpp/biotest_harness.cpp -nt "
        "        /work/harnesses/cpp/build/biotest_harness_cov_seqan3 ]; then "
        "  cd /work/harnesses/cpp; mkdir -p build; "
        "  rm -f build/*.gcda build/*.gcno; "
        "  clang++-18 -std=c++23 -O0 -g -DNDEBUG -DUSE_SEQAN3 "
        "    -DSEQAN3_DISABLE_COMPILER_CHECK -isystem /opt/seqan3/include "
        "    -fprofile-arcs -ftest-coverage biotest_harness.cpp "
        "    -o build/biotest_harness_cov_seqan3; "
        "fi; "
        "python3.12 -c 'import yaml,rich,hypothesis,chromadb,gcovr' || "
        "  python3.12 -m pip install --quiet --no-warn-script-location "
        "    -r /work/requirements.txt gcovr lxml"
    )
    proc = subprocess.run(
        ["docker", "exec", "biotest-bench-setup", "bash", "-lc", setup_cmd],
        capture_output=True, timeout=600,
    )
    if proc.returncode != 0:
        msg = proc.stderr.decode(errors="replace")[:500]
        raise RuntimeError(f"prewarm failed: {msg}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-passes", type=int, default=2)
    p.add_argument("--max-workers-per-group", type=int, default=3)
    args = p.parse_args()

    _log("INFO", "prewarming container cov binaries (one-time)...")
    prewarm_container_binaries()
    _log("INFO", "prewarm done")

    for pass_idx in range(1, args.max_passes + 1):
        failures = detect_failures()
        if not failures:
            _log("INFO", f"pass {pass_idx}: all cells full — done")
            return 0
        _log("INFO", f"pass {pass_idx}: {len(failures)} failed (config, run_id, cell)s")
        for k, why in failures.items():
            _log("INFO", f"  FAIL {k}: {why}")

        # Group by (config, run_id)
        by_group = defaultdict(list)
        for (cfg, rid, cell), _why in failures.items():
            by_group[(cfg, rid)].append(cell)

        # Group groups by config strand
        by_config = defaultdict(list)
        for (cfg, rid), cells in sorted(by_group.items()):
            by_config[cfg].append((rid, sorted(cells)))

        # Run E0/E1S/E2 strands in parallel
        with ThreadPoolExecutor(max_workers=len(by_config)) as ex:
            futures = {
                ex.submit(run_strand, cfg, groups,
                          args.max_workers_per_group): cfg
                for cfg, groups in by_config.items()
            }
            for fut in as_completed(futures):
                cfg = futures[fut]
                try:
                    fut.result()
                    _log("INFO", f"strand {cfg}: done")
                except Exception as e:
                    _log("INFO", f"strand {cfg}: FAIL {e}")

    failures = detect_failures()
    if failures:
        _log("INFO", f"WARN: {len(failures)} cells STILL failed after {args.max_passes} passes:")
        for k, why in failures.items():
            _log("INFO", f"  PERSISTENT-FAIL {k}: {why}")
        return 1
    _log("INFO", "all good after retries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
