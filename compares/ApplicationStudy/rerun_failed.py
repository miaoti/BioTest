"""Detect cells whose 4-rep main run failed (missing or status!=ok
measurement.json) and re-run only those cells in place.

Loops up to MAX_PASSES times so a transient failure on the rerun
doesn't leave the dataset incomplete. Logs every failure + rerun to
stdout for the chain log.

Usage:
    py -3.12 compares/ApplicationStudy/rerun_failed.py
        [--max-passes 3] [--max-workers 6]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
RUN_4REP = ROOT / "run_4rep.py"

CELLS = [
    ("htsjdk_vcf",     "VCF"),
    ("vcfpy_vcf",      "VCF"),
    ("noodles_vcf",    "VCF"),
    ("htsjdk_sam",     "SAM"),
    ("biopython_sam",  "SAM"),
    ("seqan3_sam",     "SAM"),
]

CONFIGS = {
    "E0":  {"sub": "E0_baseline",     "layout": "big_runs", "ids": ["a", "b", "c", "d"], "reps": 3, "cum": "true"},
    "E1S": {"sub": "E1S_strict",      "layout": "big_runs", "ids": ["a", "b", "c", "d"], "reps": 3, "cum": "true"},
    "E2":  {"sub": "E2_no_phase_d",   "layout": "reps",     "ids": [0, 1, 2, 3],         "reps": 4, "cum": "false"},
}


def _log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] [rerun_failed] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((line + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()


def _expected_measurements(config: str):
    """Yield every (run_id, cell, measurement_path) expected for a config."""
    cfg = CONFIGS[config]
    sub = cfg["sub"]
    n_reps = cfg["reps"]
    for run_id in cfg["ids"]:
        for cell, _ in CELLS:
            if cfg["layout"] == "big_runs":
                # measurement.json under run_<id>/<cell>/run_<rep>/measurement.json
                base = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                        "results_4big_runs" / f"run_{run_id}" / cell)
                paths = [base / f"run_{r}" / "measurement.json" for r in range(n_reps)]
            else:
                base = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                        "results_4rep" / cell)
                paths = [base / f"run_{r}" / "measurement.json" for r in range(n_reps)]
            yield run_id, cell, paths


def detect_failures() -> dict:
    """Returns {(config, run_id, cell) -> reason}."""
    failures = {}
    for config in CONFIGS:
        for run_id, cell, paths in _expected_measurements(config):
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


def rerun_cell(config: str, run_id, cell: str) -> int:
    """Nuke cell's work dir and re-run cascade with --only <cell>."""
    cfg = CONFIGS[config]
    sub = cfg["sub"]
    if cfg["layout"] == "big_runs":
        out_root = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                    "results_4big_runs" / f"run_{run_id}")
    else:
        out_root = (PROJECT_ROOT / "compares" / "ApplicationStudy" / sub /
                    "results_4rep")
    cell_dir = out_root / cell
    if cell_dir.exists():
        _log(f"nuking {cell_dir}")
        shutil.rmtree(cell_dir, ignore_errors=True)

    cmd = [
        sys.executable, str(RUN_4REP),
        "--mode", config,
        "--reps", str(cfg["reps"]),
        "--cumulative", cfg["cum"],
        "--max-workers", "1",
        "--out-root", str(out_root),
        "--only", cell,
    ]
    _log(f"rerun cmd: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return proc.returncode


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-passes", type=int, default=3)
    args = p.parse_args()

    for pass_idx in range(1, args.max_passes + 1):
        failures = detect_failures()
        if not failures:
            _log(f"pass {pass_idx}: all cells have full measurement coverage — done")
            return 0
        _log(f"pass {pass_idx}: detected {len(failures)} failed (config, run_id, cell)s")
        for k, why in failures.items():
            _log(f"  FAIL {k}: {why}")

        for (config, run_id, cell), why in failures.items():
            _log(f"=== rerun {config} run_{run_id} {cell} (pass {pass_idx}) ===")
            rc = rerun_cell(config, run_id, cell)
            _log(f"=== rerun {config} run_{run_id} {cell} done (rc={rc}) ===")

    # Final check
    failures = detect_failures()
    if failures:
        _log(f"WARN: {len(failures)} cells STILL failed after {args.max_passes} passes:")
        for k, why in failures.items():
            _log(f"  PERSISTENT-FAIL {k}: {why}")
        return 1
    _log("all good after retries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
