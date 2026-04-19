"""AFL++ adapter for the seqan3 SAM harness.

Unblocks the seqan3 C++ fuzzing row (DESIGN §9 Risk 1). libFuzzer
requires Clang, which doesn't compile seqan3 3.x concepts; afl-g++
delegates to GCC 12 which does. Same harness source; same detection
criteria (crash / sanitizer abort == signal).
"""

from __future__ import annotations

import os
import shutil
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
                  / "build-aflpp" / "seqan3_sam_fuzzer_aflpp")


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
        raise ValueError("AFL++ adapter only targets seqan3.")
    if format_hint.upper() != "SAM":
        raise ValueError("seqan3 has no VCF support — SAM only.")

    bin_path = binary or BINARY_DEFAULT
    if not bin_path.exists():
        raise FileNotFoundError(
            f"AFL++ binary not found at {bin_path}. "
            f"Build it first: bash compares/scripts/build_harnesses.sh aflpp")

    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    # afl-fuzz requires an input directory with at least one seed; fall
    # back to a single zero-byte file if the corpus is empty.
    if seed_copy(seed_corpus, corpus_dir) == 0:
        (corpus_dir / "stub").write_bytes(b"\n")

    # afl-fuzz writes crashes under <output>/default/crashes/, not the
    # flat crashes_dir we create in _base. Point it at the nested path
    # so crash-file counts come out right.
    afl_out = out_dir / "afl-state"
    afl_out.mkdir(parents=True, exist_ok=True)

    started = time.time()
    cmd = [
        "afl-fuzz",
        "-i", str(corpus_dir),
        "-o", str(afl_out),
        "-V", str(time_budget_s),      # wall-clock time budget
        "-D",                           # deterministic stage first
        "--",
        str(bin_path),
    ]
    # AFL++ bails if the terminal doesn't meet its expected shape. The
    # sandbox env var silences that and skips the CPU-governor check
    # that routinely trips up Docker.
    child_env = dict(os.environ)
    child_env.setdefault("AFL_SKIP_CPUFREQ", "1")
    child_env.setdefault("AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES", "1")
    child_env.setdefault("AFL_BENCH_UNTIL_CRASH", "0")
    exit_code = run_subprocess_with_timeout(
        cmd, log_file, time_budget_s + 60, env=child_env,
    )
    ended = time.time()

    # Gather AFL++-written crashes into the uniform crashes_dir so the
    # bench driver doesn't need to know the AFL++ layout.
    crashes_src = afl_out / "default" / "crashes"
    if crashes_src.exists():
        for entry in crashes_src.iterdir():
            if entry.is_file() and entry.name != "README.txt":
                shutil.copy2(entry, crashes_dir / entry.name)

    return AdapterResult(
        tool="aflpp",
        sut=sut,
        time_budget_s=time_budget_s,
        started_at=started,
        ended_at=ended,
        corpus_dir=corpus_dir,
        crashes_dir=crashes_dir,
        log_file=log_file,
        generated_count=count_files(afl_out / "default" / "queue"),
        crash_count=count_files(crashes_dir),
        exit_code=exit_code,
        extra={"binary": str(bin_path), "afl_state": str(afl_out)},
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
    print(f"[aflpp] exit={res.exit_code} queue={res.generated_count} "
          f"crashes={res.crash_count} t={res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
