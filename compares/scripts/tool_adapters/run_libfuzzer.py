"""libFuzzer adapter — drives the seqan3 SAM harness built by the
CMake shim at `compares/harnesses/libfuzzer/`.

GATED on the WSL2 seqan3 rewrite (see DESIGN.md §9 Risk 1). Windows
builds are not supported.
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
BINARY_DEFAULT = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
                  / "build" / "seqan3_sam_fuzzer")


def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    binary: Path | None = None,
    format_hint: str = "SAM",
    **_kwargs,
) -> AdapterResult:
    if sut != "seqan3":
        raise ValueError("libFuzzer adapter only targets seqan3.")
    if format_hint.upper() != "SAM":
        raise ValueError("seqan3 has no VCF support — SAM only.")

    bin_path = binary or BINARY_DEFAULT
    if not bin_path.exists():
        raise FileNotFoundError(
            f"libFuzzer binary not found at {bin_path}. "
            f"Build it first: cd {bin_path.parent.parent} && "
            "mkdir -p build && cd build && "
            "cmake -DCMAKE_CXX_COMPILER=clang++-18 .. && make")

    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    seed_copy(seed_corpus, corpus_dir)

    started = time.time()
    cmd = [
        str(bin_path),
        f"-artifact_prefix={crashes_dir}{os.sep}",
        f"-max_total_time={time_budget_s}",
        str(corpus_dir),
    ]
    exit_code = run_subprocess_with_timeout(cmd, log_file, time_budget_s)
    ended = time.time()

    return AdapterResult(
        tool="libfuzzer",
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
        extra={"binary": str(bin_path)},
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", default="seqan3")
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--binary", type=Path, default=None)
    p.add_argument("--format", default="SAM")
    args = p.parse_args()

    res = run(args.sut, args.seed_corpus, args.out_dir, args.time_budget_s,
              binary=args.binary, format_hint=args.format)
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[libfuzzer] exit={res.exit_code} corpus={res.generated_count} "
          f"crashes={res.crash_count} t={res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
