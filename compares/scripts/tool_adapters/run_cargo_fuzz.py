"""cargo-fuzz adapter — Rust fair-E2E baseline for the noodles-vcf row.

cargo-fuzz is the rust-fuzz WG's canonical binding over libFuzzer; the
binary it produces has the same `-artifact_prefix`, `-max_total_time`
and positional-corpus CLI as §13.2.4's libFuzzer seqan3 harness, so
this adapter is a thin specialisation of `run_libfuzzer.py`.

Binary layout (cargo-fuzz default, `cargo fuzz build --release`):
    compares/harnesses/cargo_fuzz/fuzz/target/<triple>/release/<target>

If the harness isn't built yet, this adapter raises FileNotFoundError
with a one-liner build command. The driver catches adapter-raise
exceptions and records a clean error record per (tool, bug) cell, so
the rest of the bench still runs.

Added 2026-04-20 as part of the pysam → vcfpy+noodles refactor
(DESIGN §2.1, §13.2.7).
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _base import (  # noqa: E402
    AdapterResult,
    count_files,
    prepare_out_dir,
    run_subprocess_with_timeout,
    seed_copy,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
HARNESS_DIR = REPO_ROOT / "compares" / "harnesses" / "cargo_fuzz"
FUZZ_TARGET_DEFAULT = "noodles_vcf_target"


def _find_binary(target: str) -> Path | None:
    """Search the cargo-fuzz default layout for the built target binary."""
    candidates = [
        HARNESS_DIR / "fuzz" / "target" / "x86_64-unknown-linux-gnu"
        / "release" / target,
        HARNESS_DIR / "target" / "release" / target,
        HARNESS_DIR / "fuzz" / "target" / "release" / target,
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    binary: Path | None = None,
    format_hint: str = "VCF",
    fuzz_target: str = FUZZ_TARGET_DEFAULT,
    **_kwargs,
) -> AdapterResult:
    if sut != "noodles":
        raise ValueError("cargo-fuzz adapter only targets noodles-vcf.")
    if format_hint.upper() != "VCF":
        raise ValueError("noodles-vcf is VCF-only.")

    bin_path = binary or _find_binary(fuzz_target)
    if bin_path is None:
        raise FileNotFoundError(
            f"cargo-fuzz target {fuzz_target!r} not built under "
            f"{HARNESS_DIR}. Build once with: "
            f"cd {HARNESS_DIR} && cargo fuzz build {fuzz_target} --release"
        )

    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    seed_copy(seed_corpus, corpus_dir)

    started = time.time()
    # cargo-fuzz binaries accept libFuzzer's standard CLI because they
    # link libFuzzer's runtime. Same flags as run_libfuzzer.py.
    # -fork=1 + -ignore_crashes=1 per PHASE4_BASELINE_FIXES.md §0.2 so
    # one crash doesn't halt the trial.
    cmd = [
        str(bin_path),
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        "-fork=1",
        "-ignore_crashes=1",
        "-print_final_stats=1",
        str(corpus_dir),
    ]
    exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
    ended = time.time()

    return AdapterResult(
        tool="cargo_fuzz",
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
        extra={"binary": str(bin_path), "fuzz_target": fuzz_target},
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", required=True)
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--format", default="VCF")
    p.add_argument("--binary", type=Path, default=None)
    p.add_argument("--fuzz-target", default=FUZZ_TARGET_DEFAULT)
    args = p.parse_args()

    res = run(
        args.sut, args.seed_corpus, args.out_dir, args.time_budget_s,
        binary=args.binary, format_hint=args.format,
        fuzz_target=args.fuzz_target,
    )
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[cargo_fuzz] exit={res.exit_code} corpus={res.generated_count} "
          f"crashes={res.crash_count}")


if __name__ == "__main__":
    _cli()
