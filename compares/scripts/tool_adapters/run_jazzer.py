"""Jazzer adapter — drives the htsjdk VCF / SAM harness classes built by
`compares/harnesses/jazzer/build.gradle`.

Jazzer must be on PATH. The harness JAR is expected at
`compares/harnesses/jazzer/build/libs/biotest-jazzer.jar` (produced by
`./gradlew :jazzer:jazzerHarness`).
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
JAZZER_JAR = REPO_ROOT / "compares" / "harnesses" / "jazzer" / "build" / "libs" / "biotest-jazzer.jar"


def _target_class(format_hint: str) -> tuple[str, str]:
    """(target-class, instrumentation-includes) per format."""
    fmt = format_hint.upper()
    if fmt == "SAM":
        return (
            "SAMCodecFuzzer",
            "htsjdk.samtools.*",
        )
    return (
        "VCFCodecFuzzer",
        "htsjdk.variant.vcf.*,htsjdk.variant.variantcontext.*",
    )


def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    format_hint: str = "VCF",
    **_kwargs,
) -> AdapterResult:
    if sut != "htsjdk":
        raise ValueError("Jazzer only fuzzes Java SUTs; expected 'htsjdk'.")

    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    seed_copy(seed_corpus, corpus_dir)
    target_class, instrument_includes = _target_class(format_hint)

    started = time.time()
    cmd = [
        "jazzer",
        f"--cp={JAZZER_JAR}",
        f"--target_class={target_class}",
        f"--instrumentation_includes={instrument_includes}",
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        str(corpus_dir),
    ]
    exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
    ended = time.time()

    return AdapterResult(
        tool="jazzer",
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
        extra={"target_class": target_class, "format": format_hint.upper()},
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", default="htsjdk")
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--format", default="VCF")
    args = p.parse_args()

    res = run(args.sut, args.seed_corpus, args.out_dir, args.time_budget_s,
              format_hint=args.format)
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[jazzer] exit={res.exit_code} corpus={res.generated_count} "
          f"crashes={res.crash_count} t={res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
