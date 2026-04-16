#!/usr/bin/env python3
"""
Fetch real-world VCF and SAM seed files from public GitHub test suites.

All files are small (< 100KB each) curated test data from the official
samtools/htsjdk projects. No authentication required.

Usage:
    py -3.12 seeds/fetch_real_world.py          # download only missing files
    py -3.12 seeds/fetch_real_world.py --force  # re-download all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

SEEDS_DIR = Path(__file__).resolve().parent

# Curated real-world seeds from public GitHub repos.
# Format: (output_subdir, output_filename, source_url, description)
SEED_SOURCES: list[tuple[str, str, str, str]] = [
    # --- htsjdk test resources (https://github.com/samtools/htsjdk) ---
    (
        "vcf", "htsjdk_ex2.vcf",
        "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/ex2.vcf",
        "htsjdk official VCF test file (3-sample, multi-ALT)",
    ),
    (
        "vcf", "htsjdk_HiSeq.10000.vcf",
        "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/HiSeq.10000.vcf",
        "htsjdk HiSeq subset (real Illumina variant calls)",
    ),
    (
        "vcf", "htsjdk_dbsnp_135.b37.1000.vcf",
        "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/dbsnp_135.b37.1000.vcf",
        "htsjdk dbSNP 135 subset (1000 records from real dbSNP)",
    ),
    (
        "sam", "htsjdk_example.sam",
        "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/samtools/example.sam",
        "htsjdk canonical SAM example",
    ),
    (
        "sam", "htsjdk_unmapped_reads.sam",
        "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/samtools/unmapped_reads.sam",
        "htsjdk unmapped reads (edge-case SAM)",
    ),
    (
        "sam", "htsjdk_coordinate_sorted.sam",
        "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/samtools/coordinate_sorted.sam",
        "htsjdk coordinate-sorted SAM",
    ),
    # --- samtools test data (https://github.com/samtools/samtools) ---
    (
        "sam", "samtools_ce.sam",
        "https://raw.githubusercontent.com/samtools/samtools/develop/test/ce.sam",
        "samtools C. elegans genome test",
    ),
    (
        "vcf", "bcftools_test.vcf",
        "https://raw.githubusercontent.com/samtools/bcftools/develop/test/view.vcf",
        "bcftools canonical test VCF",
    ),
]


def download_one(url: str, dest: Path, timeout: int = 30) -> int:
    """Download a single file. Returns size in bytes (0 if failed)."""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        print(f"    FAIL: {e}", file=sys.stderr)
        return 0

    content = resp.content

    # Sanity check: must look like VCF or SAM
    head = content[:200].decode("utf-8", errors="replace")
    fmt = dest.parent.name
    if fmt == "vcf" and not head.startswith("##"):
        print(f"    WARN: does not look like VCF (missing ##fileformat)", file=sys.stderr)
    elif fmt == "sam" and not head.startswith("@"):
        print(f"    WARN: does not look like SAM (missing @HD/@SQ)", file=sys.stderr)

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    return len(content)


def main():
    parser = argparse.ArgumentParser(description="Fetch real-world VCF/SAM seeds")
    parser.add_argument("--force", action="store_true",
                        help="Re-download even if file exists")
    args = parser.parse_args()

    print(f"Downloading {len(SEED_SOURCES)} seed files to {SEEDS_DIR}...\n")

    ok = 0
    skipped = 0
    failed = 0

    for fmt, name, url, description in SEED_SOURCES:
        dest = SEEDS_DIR / fmt / name
        if dest.exists() and not args.force:
            print(f"  [SKIP] {fmt}/{name} (exists, {dest.stat().st_size:,} bytes)")
            skipped += 1
            continue

        print(f"  [GET]  {fmt}/{name}")
        print(f"         {description}")
        size = download_one(url, dest)
        if size > 0:
            print(f"    OK:  {size:,} bytes")
            ok += 1
        else:
            failed += 1

    print()
    print(f"Summary: {ok} downloaded, {skipped} skipped, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
