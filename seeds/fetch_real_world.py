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

# Per-file cap: skip any source > 500 KB to keep Phase C fast
# and the corpus manageable.
MAX_FILE_BYTES = 500 * 1024

# Curated real-world seeds from public GitHub repos. All sources are
# Apache 2.0 or permissive-license test data — safe to redistribute
# via a fetch script into this repo (source files NOT committed; see
# seeds/SOURCES.md for the full provenance manifest).
#
# Format: (output_subdir, output_filename, source_url, description)
#
# File-naming convention: real_world_*.vcf / *.sam so the .gitignore
# pattern keeps the downloaded files out of the tracked tree while
# leaving hand-crafted Tier-1 seeds (minimal_*, spec_example) tracked.
SEED_SOURCES: list[tuple[str, str, str, str]] = [
    # ---------------------------------------------------------------
    # htsjdk test resources
    # (github.com/samtools/htsjdk/src/test/resources/htsjdk/variant/)
    # Characteristic: multi-sample, structural variants, NaN QUAL,
    # dbSNP-style INFO flags. Apache 2.0.
    # ---------------------------------------------------------------
    ("vcf", "real_world_htsjdk_ex2.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/ex2.vcf",
     "htsjdk ex2.vcf — 3-sample multi-ALT example"),
    ("vcf", "real_world_htsjdk_HiSeq.10000.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/HiSeq.10000.vcf",
     "htsjdk HiSeq subset (2 MB — skipped by default under cap)"),
    ("vcf", "real_world_htsjdk_dbsnp_135.b37.1000.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/dbsnp_135.b37.1000.vcf",
     "htsjdk dbSNP 135 subset (1000 rows, rich INFO flags CLN/G5/GENEINFO)"),
    ("vcf", "real_world_htsjdk_structuralvariants.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/structuralvariants.vcf",
     "htsjdk structural variants (<DEL>, <INS>, <INV>, <DUP>, <BND>)"),
    ("vcf", "real_world_htsjdk_test_withNanQual.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/test_withNanQual.vcf",
     "htsjdk NaN QUAL edge case"),
    ("vcf", "real_world_htsjdk_test_withGLandPL.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/test_withGLandPL.vcf",
     "htsjdk deep FORMAT: GT:GQ:DP:AD:PL"),
    ("vcf", "real_world_htsjdk_breakpointExample.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/breakpointExample.vcf",
     "htsjdk BND breakpoint notation"),
    ("vcf", "real_world_htsjdk_diploid.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/diploid-gvcfs/test.diploid-gvcfs.raw.gvcf.vcf",
     "htsjdk diploid gVCF (phased)"),
    ("vcf", "real_world_htsjdk_reblocked.gvcf.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/reblocked.gvcf.vcf",
     "htsjdk reblocked gVCF with <NON_REF>"),
    ("vcf", "real_world_htsjdk_clinvar.vcf",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/variant/clinvar_20140902.vcf",
     "htsjdk ClinVar variants with clinical significance INFO"),

    # ---------------------------------------------------------------
    # bcftools test suite (github.com/samtools/bcftools/test/)
    # Characteristic: small focused edge cases, normalization tests,
    # annotation tests, split/join tests. MIT-equivalent.
    # ---------------------------------------------------------------
    ("vcf", "real_world_bcftools_view.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/view.vcf",
     "bcftools canonical test — `bcftools view` input"),
    ("vcf", "real_world_bcftools_norm_merge.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/norm.merge.vcf",
     "bcftools norm merge test — multi-allelic join inputs"),
    ("vcf", "real_world_bcftools_norm_split.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/norm.split.vcf",
     "bcftools norm split test — multi-allelic split inputs"),
    ("vcf", "real_world_bcftools_norm_left_align.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/norm.left-align.vcf",
     "bcftools norm left-alignment test"),
    ("vcf", "real_world_bcftools_annotate.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/annotate.vcf",
     "bcftools annotate test"),
    ("vcf", "real_world_bcftools_csq.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/csq.vcf",
     "bcftools +csq test with CSQ annotation"),
    ("vcf", "real_world_bcftools_csq_in.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/csq/test.vcf",
     "bcftools csq full gene model input"),
    ("vcf", "real_world_bcftools_missing.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/missing.vcf",
     "bcftools missing-value handling test"),
    ("vcf", "real_world_bcftools_ad_bias.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/ad-bias.vcf",
     "bcftools allelic-depth bias test"),
    ("vcf", "real_world_bcftools_af_dist.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/af-dist.vcf",
     "bcftools allele-frequency distribution test"),
    ("vcf", "real_world_bcftools_concat_1.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/concat.1.vcf",
     "bcftools concat input 1"),
    ("vcf", "real_world_bcftools_concat_2.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/concat.2.vcf",
     "bcftools concat input 2"),
    ("vcf", "real_world_bcftools_concat_3.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/concat.3.vcf",
     "bcftools concat input 3"),
    ("vcf", "real_world_bcftools_plugin_fill_tags.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/fill-tags.vcf",
     "bcftools +fill-tags input"),
    ("vcf", "real_world_bcftools_plugin_setGT.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/setGT.vcf",
     "bcftools +setGT input"),
    ("vcf", "real_world_bcftools_query.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/query.vcf",
     "bcftools query input"),
    ("vcf", "real_world_bcftools_check.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/check.vcf",
     "bcftools check input"),
    ("vcf", "real_world_bcftools_filter.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/filter.vcf",
     "bcftools filter input — FILTER column edge cases"),
    ("vcf", "real_world_bcftools_isec_1.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/isec.a.vcf",
     "bcftools isec input A"),
    ("vcf", "real_world_bcftools_isec_2.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/isec.b.vcf",
     "bcftools isec input B"),
    ("vcf", "real_world_bcftools_merge_1.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/merge.a.vcf",
     "bcftools merge input A"),
    ("vcf", "real_world_bcftools_merge_2.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/merge.b.vcf",
     "bcftools merge input B"),
    ("vcf", "real_world_bcftools_mpileup.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/mpileup.vcf",
     "bcftools mpileup sample output"),
    ("vcf", "real_world_bcftools_norm_check_ref.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/check-ref.vcf",
     "bcftools norm check-ref edge case"),
    ("vcf", "real_world_bcftools_polysomy.vcf",
     "https://raw.githubusercontent.com/samtools/bcftools/develop/test/polysomy.vcf",
     "bcftools polysomy (aneuploid) test"),

    # ---------------------------------------------------------------
    # hts-specs test corpus (github.com/samtools/hts-specs/test/vcf/)
    # Characteristic: spec-compliance edge cases split by VCF version.
    # MIT-equivalent.
    # ---------------------------------------------------------------
    ("vcf", "real_world_hts_specs_v4.1_passed_all_fields.vcf",
     "https://raw.githubusercontent.com/samtools/hts-specs/master/test/vcf/4.1/passed/passed_body_fileformat_v4.1.vcf",
     "hts-specs v4.1 passed fileformat"),
    ("vcf", "real_world_hts_specs_v4.2_passed_fileformat.vcf",
     "https://raw.githubusercontent.com/samtools/hts-specs/master/test/vcf/4.2/passed/passed_body_fileformat_v4.2.vcf",
     "hts-specs v4.2 passed fileformat"),
    ("vcf", "real_world_hts_specs_v4.3_passed_fileformat.vcf",
     "https://raw.githubusercontent.com/samtools/hts-specs/master/test/vcf/4.3/passed/passed_body_fileformat_v4.3.vcf",
     "hts-specs v4.3 passed fileformat"),
    ("vcf", "real_world_hts_specs_v4.5_passed_fileformat.vcf",
     "https://raw.githubusercontent.com/samtools/hts-specs/master/test/vcf/4.5/passed/passed_body_fileformat_v4.5.vcf",
     "hts-specs v4.5 passed fileformat"),

    # ---------------------------------------------------------------
    # Broad Institute GATK test resources
    # (github.com/broadinstitute/gatk/src/test/resources/)
    # Apache 2.0. Curated small files only (<500 KB cap).
    # ---------------------------------------------------------------
    ("vcf", "real_world_gatk_feature_data_source_test.vcf",
     "https://raw.githubusercontent.com/broadinstitute/gatk/master/src/test/resources/org/broadinstitute/hellbender/engine/feature_data_source_test.vcf",
     "GATK feature data source test"),
    ("vcf", "real_world_gatk_feature_data_source_test_gvcf.vcf",
     "https://raw.githubusercontent.com/broadinstitute/gatk/master/src/test/resources/org/broadinstitute/hellbender/engine/feature_data_source_test_gvcf.vcf",
     "GATK gVCF with <NON_REF>"),
    ("vcf", "real_world_gatk_count_variants.vcf",
     "https://raw.githubusercontent.com/broadinstitute/gatk/master/src/test/resources/org/broadinstitute/hellbender/tools/CountVariants/count_variants.vcf",
     "GATK CountVariants tool test"),
    ("vcf", "real_world_gatk_select_variants.vcf",
     "https://raw.githubusercontent.com/broadinstitute/gatk/master/src/test/resources/org/broadinstitute/hellbender/tools/walkers/variantutils/SelectVariants/expected.testVariantIDSelection.vcf",
     "GATK SelectVariants test"),
    ("vcf", "real_world_gatk_funcotator_snpeff_sample.vcf",
     "https://raw.githubusercontent.com/broadinstitute/gatk/master/src/test/resources/org/broadinstitute/hellbender/tools/funcotator/SnpEffSamples/SnpEffSamples.vcf",
     "GATK Funcotator with SnpEff ANN annotation"),

    # ---------------------------------------------------------------
    # SAM corpus (unchanged; these work for the SAM-focused runs)
    # ---------------------------------------------------------------
    ("sam", "real_world_htsjdk_example.sam",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/samtools/example.sam",
     "htsjdk canonical SAM example"),
    ("sam", "real_world_htsjdk_unmapped_reads.sam",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/samtools/unmapped_reads.sam",
     "htsjdk unmapped reads (edge case)"),
    ("sam", "real_world_htsjdk_coordinate_sorted.sam",
     "https://raw.githubusercontent.com/samtools/htsjdk/master/src/test/resources/htsjdk/samtools/coordinate_sorted.sam",
     "htsjdk coordinate-sorted SAM"),
    ("sam", "real_world_samtools_ce.sam",
     "https://raw.githubusercontent.com/samtools/samtools/develop/test/ce.sam",
     "samtools C. elegans genome test"),
]


def download_one(url: str, dest: Path, timeout: int = 30) -> int:
    """Download a single file. Returns size in bytes (0 if failed/skipped).

    Enforces MAX_FILE_BYTES cap. Files larger than that are skipped with
    a note — keeps Phase C fast and the repo footprint manageable.
    """
    try:
        resp = requests.get(url, timeout=timeout, stream=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"    FAIL: {e}", file=sys.stderr)
        return 0

    # Honor Content-Length if the server reports one — avoids downloading
    # the whole blob just to discover it's too big.
    claimed = resp.headers.get("content-length")
    if claimed:
        try:
            if int(claimed) > MAX_FILE_BYTES:
                print(
                    f"    SKIP: {int(claimed):,} bytes > cap {MAX_FILE_BYTES:,}",
                    file=sys.stderr,
                )
                return 0
        except ValueError:
            pass

    # Read body with a hard byte ceiling.
    chunks: list[bytes] = []
    total = 0
    for chunk in resp.iter_content(chunk_size=8192):
        if not chunk:
            continue
        chunks.append(chunk)
        total += len(chunk)
        if total > MAX_FILE_BYTES:
            print(
                f"    SKIP: body exceeded cap {MAX_FILE_BYTES:,} bytes mid-stream",
                file=sys.stderr,
            )
            return 0
    content = b"".join(chunks)

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
