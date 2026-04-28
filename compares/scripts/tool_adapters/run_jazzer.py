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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _base import (  # noqa: E402
    AdapterResult,
    prepare_out_dir,
    run_subprocess_with_timeout,
    count_files,
    seed_copy,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
JAZZER_JAR = REPO_ROOT / "compares" / "harnesses" / "jazzer" / "build" / "libs" / "biotest-jazzer.jar"


def _target_class(format_hint: str) -> tuple[str, list[str]]:
    """(target-class, [glob]) per format. Jazzer rejects CSV in
    --instrumentation_includes and expects the flag repeated per glob."""
    fmt = format_hint.upper()
    if fmt == "SAM":
        return ("SAMCodecFuzzer", ["htsjdk.samtools.**"])
    return (
        "VCFCodecFuzzer",
        ["htsjdk.variant.vcf.**", "htsjdk.variant.variantcontext.**"],
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
    target_class, instrument_globs = _target_class(format_hint)
    reproducers_dir = out_dir / "reproducers"
    reproducers_dir.mkdir(exist_ok=True)

    started = time.time()
    cmd = [
        "jazzer",
        f"--cp={JAZZER_JAR}",
        f"--target_class={target_class}",
    ]
    # Jazzer's --instrumentation_includes accepts a single glob per flag;
    # repeat the flag for each glob we need.
    for glob in instrument_globs:
        cmd.append(f"--instrumentation_includes={glob}")
    # --keep_going=1000 (Jazzer ≥0.17) keeps the fuzzer running until
    # 1000 distinct findings; -fork=1 + -ignore_crashes=1 passthrough to
    # the libFuzzer runtime do the same at the runtime level. Belt-and-
    # braces so one crash doesn't burn the rest of the budget (Klees
    # CCS'18 §3.1; PHASE4_BASELINE_FIXES.md §0.2).
    # --reproducer_path pins Java `Crash_<hash>.java` stubs into the run
    # output; without it Jazzer dumps them into cwd (the repo root).
    cmd.extend([
        "--keep_going=1000",
        f"--reproducer_path={reproducers_dir}",
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        "-fork=1",
        "-ignore_crashes=1",
        "-print_final_stats=1",
        str(corpus_dir),
    ])
    # Jazzer auto-parses every JAZZER_* env var as a CLI option. Scrub
    # any that might be lingering (e.g. a build-time JAZZER_VERSION
    # pin) so Jazzer doesn't misinterpret them as fuzzer flags.
    child_env = {k: v for k, v in os.environ.items() if not k.startswith("JAZZER_")}
    exit_code = run_subprocess_with_timeout(
        cmd, log_file, time_budget_s, env=child_env,
    )
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
        extra={
            "target_class": target_class,
            "format": format_hint.upper(),
            "instrumentation_includes": instrument_globs,
        },
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
