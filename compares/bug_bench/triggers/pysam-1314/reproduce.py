"""Minimal reproducer for pysam-1314.

Run under pysam 0.22.1 (pre-fix) to see the contig rename; run under
pysam 0.23.0 (post-fix) to see that the contig is preserved.

Usage (inside the biotest-bench image):

    /work/compares/results/sut-envs/pysam/bin/pip install --force-reinstall pysam==0.22.1
    /work/compares/results/sut-envs/pysam/bin/python reproduce.py

Expected (buggy 0.22.1):
    written record chrom:  mychr           <-- WRONG: silent remap
Expected (fixed 0.23.0):
    written record chrom:  Horvu_VADA_Un01G000200.1
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pysam

HERE = Path(__file__).resolve().parent
SRC = HERE / "original.vcf"


def main() -> None:
    # Build a header from scratch with a contig that is NOT present in
    # the input file, registered before the input file's real contig.
    hand_built = pysam.VariantHeader()
    hand_built.contigs.add("mychr", length=1000)
    hand_built.contigs.add("Horvu_VADA_Un01G000200.1", length=2673)
    hand_built.add_line(
        '##INFO=<ID=.,Number=0,Type=Flag,Description="no-op">')

    out_path = Path(tempfile.mkstemp(suffix=".vcf")[1])
    src = pysam.VariantFile(str(SRC))
    dst = pysam.VariantFile(str(out_path), "w", header=hand_built)
    for rec in src:
        print("source chrom :", rec.chrom)
        dst.write(rec)
    dst.close()
    src.close()

    # Re-read the output and see what chrom was actually written.
    with pysam.VariantFile(str(out_path)) as back:
        for rec in back:
            print("written chrom:", rec.chrom,
                  "  <-- expected Horvu_VADA_Un01G000200.1")


if __name__ == "__main__":
    main()
