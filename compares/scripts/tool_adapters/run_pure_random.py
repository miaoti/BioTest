"""Pure Random floor baseline. Emits `os.urandom` files for `time_budget_s`.

Uniform adapter API; see `_base.py`. The generator writes one candidate
per 4 KiB block (mean 2 KiB payload) and halts when the budget elapses.
"""

from __future__ import annotations

import os
import random
import sys
import time
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _base import AdapterResult, prepare_out_dir  # noqa: E402


def run(
    sut: str,
    seed_corpus: Path,
    out_dir: Path,
    time_budget_s: int,
    format_hint: str = "VCF",
    **_kwargs,
) -> AdapterResult:
    corpus_dir, crashes_dir, log_file = prepare_out_dir(out_dir)
    started = time.time()
    suffix = ".vcf" if format_hint.upper() == "VCF" else ".sam"

    n = 0
    rng = random.Random(0xB10)
    deadline = started + time_budget_s
    while time.time() < deadline:
        size = rng.randint(16, 4096)
        blob = os.urandom(size)
        (corpus_dir / f"rand_{n:08d}{suffix}").write_bytes(blob)
        n += 1
        if n % 1000 == 0:
            log_file.open("a", encoding="utf-8").write(f"[rand] {n} files\n")

    ended = time.time()
    return AdapterResult(
        tool="pure_random",
        sut=sut,
        time_budget_s=time_budget_s,
        started_at=started,
        ended_at=ended,
        corpus_dir=corpus_dir,
        crashes_dir=crashes_dir,
        log_file=log_file,
        generated_count=n,
        accepted_count=-1,
        crash_count=0,
        exit_code=0,
    )


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sut", required=True)
    p.add_argument("--seed-corpus", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--format", default="VCF")
    args = p.parse_args()

    res = run(args.sut, args.seed_corpus, args.out_dir, args.time_budget_s,
              format_hint=args.format)
    res.write_manifest(args.out_dir / "adapter_result.json")
    print(f"[pure_random] {res.generated_count} files in {res.duration_s():.0f}s")


if __name__ == "__main__":
    _cli()
