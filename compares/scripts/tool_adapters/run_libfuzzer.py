"""libFuzzer adapter — drives the seqan3 SAM harness built by the
CMake shim at `compares/harnesses/libfuzzer/`.

Primary C++ fuzzer for the seqan3 row (DESIGN §13.2.4). Requires the
two seqan3 Clang patches — baked into the `biotest-bench` image, or
apply by hand if running on the bare host. Windows host is not
supported (Clang + libFuzzer needs a Linux toolchain).
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
BINARY_DEFAULT = (REPO_ROOT / "compares" / "harnesses" / "libfuzzer"
                  / "build" / "seqan3_sam_fuzzer_libfuzzer")


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
    # -fork=1 + -ignore_crashes=1: keep fuzzing after the first crash so
    # one unrelated crash-on-boot doesn't burn the entire budget; each
    # crash is still saved to artifact_prefix. See Klees CCS'18 §3.1
    # and PHASE4_BASELINE_FIXES.md §0.2.
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
