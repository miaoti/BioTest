"""Inflate the 3-record seed into a 10 000-record SAM for perf timing.

Usage:
    python generate_large_sam.py [--count N] [--out OUT]
"""

from __future__ import annotations

import argparse
from pathlib import Path


HEADER = "@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:chr1\tLN:10000000\n"
SEQ = "ACGT" * 12 + "AC"  # 50 bp
QUAL = "I" * 50
TEMPLATE = "r{i}\t0\tchr1\t{pos}\t60\t50M\t*\t0\t0\t{seq}\t{qual}\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=10_000)
    p.add_argument("--out", type=Path,
                   default=Path(__file__).resolve().parent / "large.sam")
    args = p.parse_args()

    with args.out.open("w", encoding="ascii", newline="\n") as fh:
        fh.write(HEADER)
        for i in range(args.count):
            fh.write(TEMPLATE.format(i=i, pos=1 + 60 * (i % 100_000),
                                     seq=SEQ, qual=QUAL))

    print(f"[large-sam] wrote {args.count} records to {args.out}")


if __name__ == "__main__":
    main()
