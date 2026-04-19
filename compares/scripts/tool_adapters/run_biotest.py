"""BioTest adapter — invokes the main BioTest pipeline's Phase C with
overridden seed + output directories so its corpus lands under the
comparison results tree.

The adapter does not re-run Phase A/B; it expects a prebuilt MR registry
at data/mr_registry.json. Pass --phase-c-only to skip the full pipeline.
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
)


REPO_ROOT = Path(__file__).resolve().parents[3]  # compares/scripts/tool_adapters -> repo root


def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    format_hint: str = "VCF",
    config_path: Path | None = None,
    **_kwargs,
) -> AdapterResult:
    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    started = time.time()

    cmd = [
        sys.executable,
        str(REPO_ROOT / "biotest.py"),
        "--phase", "C",
        "--seed-dir", str(seed_corpus),
        "--bug-output-dir", str(crashes_dir),
        "--corpus-output-dir", str(corpus_dir),
        "--time-budget-s", str(time_budget_s),
        "--format", format_hint,
        "--primary-sut", sut,
    ]
    if config_path:
        cmd.extend(["--config", str(config_path)])

    exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
    ended = time.time()

    return AdapterResult(
        tool="biotest",
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
        notes=("biotest.py CLI flags --seed-dir/--bug-output-dir/"
               "--corpus-output-dir/--time-budget-s/--primary-sut "
               "are assumed; adjust if the top-level orchestrator "
               "exposes them under different names."),
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", required=True)
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--format", default="VCF")
    p.add_argument("--config", type=Path, default=None)
    args = p.parse_args()

    res = run(
        args.sut, args.seed_corpus, args.out_dir,
        args.time_budget_s, format_hint=args.format, config_path=args.config,
    )
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[biotest] exit={res.exit_code} corpus={res.generated_count} "
          f"crashes={res.crash_count} t={res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
