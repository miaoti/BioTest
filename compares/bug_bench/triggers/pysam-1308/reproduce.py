"""Minimal reproducer for pysam-1308.

Two successive VariantHeader.new_record(...) calls with identical
payload. On pysam 0.22.1 the second raises KeyError.

Usage (inside the biotest-bench image):

    /work/compares/results/sut-envs/pysam/bin/pip install --force-reinstall pysam==0.22.1
    /work/compares/results/sut-envs/pysam/bin/python reproduce.py
"""

from __future__ import annotations

import pysam


def main() -> None:
    vcfh = pysam.VariantHeader()
    vcfh.contigs.add("chr1")
    vcfh.add_sample("sample1")
    vcfh.formats.add("GT", "1", "String", "Genotype")

    payload = {
        "contig": "chr1",
        "start": 10,
        "stop": 15,
        "alleles": ["A", "TCGA"],
        "samples": [{"GT": (0, 0)}],
    }

    first = vcfh.new_record(**payload)
    print("first  call OK:", first)

    try:
        second = vcfh.new_record(**payload)
        print("second call OK (post-fix):", second)
    except KeyError as e:
        print("second call raised KeyError (PRE-FIX BUG):", e)


if __name__ == "__main__":
    main()
