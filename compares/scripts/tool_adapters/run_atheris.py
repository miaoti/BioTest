"""Atheris adapter — invokes the pysam / biopython harnesses.

Not Windows-compatible; runs on WSL2 / Linux / macOS only (Atheris
limitation).
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
import argparse

from _base import (
    AdapterResult,
    prepare_out_dir,
    run_subprocess_with_timeout,
    count_files,
    seed_copy,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
HARNESS_DIR = REPO_ROOT / "compares" / "harnesses" / "atheris"


def _harness_for(sut: str) -> Path:
    if sut == "pysam":
        return HARNESS_DIR / "fuzz_pysam.py"
    if sut == "biopython":
        return HARNESS_DIR / "fuzz_biopython.py"
    raise ValueError(f"Atheris adapter does not support SUT {sut!r}")


def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    format_hint: str = "VCF",
    python_bin: str = "/opt/atheris-venv/bin/python",
    **_kwargs,
) -> AdapterResult:
    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    seed_copy(seed_corpus, corpus_dir)
    harness = _harness_for(sut)

    started = time.time()
    cmd = [
        python_bin,
        str(harness),
        f"--format={format_hint.upper()}",
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        "-atheris_runs=0",
        str(corpus_dir),
    ]
    exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
    ended = time.time()

    return AdapterResult(
        tool="atheris",
        sut=sut,
        time_budget_s=time_budget_s,
        started_at=started,
        ended_at=ended,
        corpus_dir=corpus_dir,
        crashes_dir=crashes_dir,
        log_file=log_file,
        generated_count=count_files(corpus_dir),
        crash_count=count_files(crashes_dir),
        exit_code=exit_code,
        extra={"harness": str(harness), "format": format_hint.upper()},
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", required=True, choices=["pysam", "biopython"])
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--format", default="VCF")
    p.add_argument("--python-bin", default="/opt/atheris-venv/bin/python",
                   help="Python interpreter with atheris installed. Inside "
                        "the benchmark image this is /opt/atheris-venv/bin/python "
                        "(a 3.11 venv because atheris 2.3.0 has no Python "
                        "3.12 support).")
    args = p.parse_args()

    res = run(args.sut, args.seed_corpus, args.out_dir, args.time_budget_s,
              format_hint=args.format, python_bin=args.python_bin)
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[atheris/{args.sut}] exit={res.exit_code} "
          f"corpus={res.generated_count} crashes={res.crash_count} "
          f"t={res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
