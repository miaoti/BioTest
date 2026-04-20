# Verified Bug Catalogue

**Generated from**: `manifest.verified.json`
**Total bugs**: 23
**By SUT**: biopython 1  ·  htsjdk 12  ·  pysam 4  ·  seqan3 6

Single-source-of-truth reference for every bug the Phase-4 bench driver will run. Edit `manifest.verified.json` and regenerate this file via `python compares/bug_bench/render_catalogue.py`.

## htsjdk (12 bugs)

### `htsjdk-1554` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1554
- **Anchor**: `install_version` — pre-fix `2.24.1` → post-fix `3.0.0`
- **Confidence**: high
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib, pysam
- **Also detectable via**: metamorphic_filter_then_recompute_AC
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1554/`

AC/AN/AF allele counts include filtered genotypes marked FT; should exclude filtered variants.

*Verification rule*: PR #1554 merged 2021-06-10, first in htsjdk 3.0.0 on 2022-06-06 (AC/AN/AF filtered genotypes)

### `htsjdk-1637` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/issues/1637
- **Anchor**: `install_version` — pre-fix `3.0.3` → post-fix `3.0.4`
- **Confidence**: high
- **Category**: `round_trip_asymmetry` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1637/`

VCF sort order changed to use alleles for stability; breaks merging of existing valid VCFs causing false 'unsorted' errors.

*Verification rule*: htsjdk 3.0.4 (2022-11-23) hotfix reverted PR #1593 which had caused #1637's VCF sort-order regression

### `htsjdk-1364` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1364
- **Anchor**: `install_version` — pre-fix `2.19.0` → post-fix `2.20.0`
- **Confidence**: high
- **Category**: `incorrect_rejection` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib, pysam
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1364/`

Pre-fix VCF codec rejects QUAL / INFO float values spelled with non-lowercase 'nan' or 'inf' (e.g. 'NaN', 'Inf', 'Infinity'), which htslib accepts per the VCF spec's float production rule. Causes differential disagreement on any VCF where upstream tools emit mixed-case float literals.

*Verification rule*: htsjdk 2.20.0 release notes cite 'Tolerate mixed case NaNs and Infinities in VCF (#1364)'

### `htsjdk-1389` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1389
- **Anchor**: `install_version` — pre-fix `2.19.0` → post-fix `2.20.0`
- **Confidence**: high
- **Category**: `writer_bug` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1389/`

Pre-fix VCF writer serialises multi-value missing fields as '.,.,.' (one dot per value) instead of the spec-canonical single '.' for fully-missing values. Round-trip through pre-fix htsjdk changes INFO/FORMAT string representation.

*Verification rule*: htsjdk 2.20.0 release notes cite 'Output missing vcf fields as a single . (#1389)'

### `htsjdk-1372` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1372
- **Anchor**: `install_version` — pre-fix `2.19.0` → post-fix `2.20.0`
- **Confidence**: high
- **Category**: `parse_error_missed` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1372/`

Pre-fix VCF codec fails to handle FORMAT=GL when multiple per-genotype GL values are each individually missing ('.'). Throws instead of producing null, even though htslib accepts the input.

*Verification rule*: htsjdk 2.20.0 release notes cite 'VCF codec should handle multiple missing GL fields (#1372)'

### `htsjdk-1401` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1401
- **Anchor**: `install_version` — pre-fix `2.19.0` → post-fix `2.20.0`
- **Confidence**: high
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1401/`

Pre-fix VCF header parser produces inconsistent PEDIGREE entries between VCF 4.2 and 4.3 inputs; the same semantic pedigree record round-trips differently depending on declared fileformat version.

*Verification rule*: htsjdk 2.20.0 release notes cite 'Handle PEDIGREE header lines differently for vcf4.2 vs vcf4.3 (#1401)'

### `htsjdk-1403` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1403
- **Anchor**: `install_version` — pre-fix `2.20.0` → post-fix `2.20.1`
- **Confidence**: high
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1403/`

Regression in VariantContextBuilder introduced in htsjdk 2.20.0 — the builder emits incorrect field values under certain chains; hotfix in 2.20.1 reverts the regression.

*Verification rule*: htsjdk 2.20.1 release notes cite 'fix bug in VariantContextBuilder (#1403)' — explicitly a hotfix for the 2.20.0 regression

### `htsjdk-1418` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1418
- **Anchor**: `install_version` — pre-fix `2.20.1` → post-fix `2.21.0`
- **Confidence**: high
- **Category**: `incorrect_rejection` (crash / rejection)
- **Expected signal**: `uncaught_exception` against htsjdk_buggy_version
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1418/`

Pre-fix VCF header parser throws on any '##contig=<ID=X>' header line that omits the length= attribute, even though the spec treats length as optional. htslib accepts such files; pre-fix htsjdk rejects them.

*Verification rule*: htsjdk 2.21.0 release notes cite 'Make VCFHeader not throw exception if contig header lines lack length field (#1418)'

### `htsjdk-1544` — VCF

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1544
- **Anchor**: `install_version` — pre-fix `2.24.1` → post-fix `3.0.0`
- **Confidence**: high
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib, pysam
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1544/`

Pre-fix VariantContext.getType() mis-classifies gVCF-style <NON_REF> records, producing wrong variant-type labels for gVCF blocks. Downstream tools that filter by variant type therefore miss entire classes of records.

*Verification rule*: htsjdk 3.0.0 release notes cite 'Added GVCF mode for VariantContext type determination (#1544)'

### `htsjdk-1561` — SAM

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1561
- **Anchor**: `install_version` — pre-fix `2.24.1` → post-fix `3.0.0`
- **Confidence**: high
- **Category**: `parse_error_missed` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1561/`

Pre-fix SAM header parser silently accepts @HD / @SQ / @RG / @PG lines with tag keys longer or shorter than 2 characters (SAM spec §1.3 mandates exactly 2). Malformed headers pass through pre-fix and produce SAMFileHeader objects with garbage-keyed attributes.

*Verification rule*: htsjdk 3.0.0 release notes cite 'Validate that SAM header tag keys are exactly 2 characters long (#1561)'

### `htsjdk-1538` — SAM

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1538
- **Anchor**: `install_version` — pre-fix `2.24.0` → post-fix `2.24.1`
- **Confidence**: high
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Also detectable via**: metamorphic_set_cigar_then_get_blocks
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1538/`

Pre-fix SAMRecord mutation (e.g. setCigar) does not invalidate the cached mAlignmentBlocks vector. Subsequent calls to getAlignmentBlocks() on the mutated record return stale data from before the CIGAR edit. Silent wrong answer on any mutation-followed-by-query pattern.

*Verification rule*: htsjdk 2.24.1 release notes cite 'Invaliding out of date SAMRecord.mAlignmentBlocks cache (#1538)'

### `htsjdk-1489` — SAM

- **Issue / PR**: https://github.com/samtools/htsjdk/pull/1489
- **Anchor**: `install_version` — pre-fix `2.22.0` → post-fix `2.23.0`
- **Confidence**: medium
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/htsjdk-1489/`

Pre-fix SAM locus accumulator drops certain insertion events, under-counting coverage at insert positions. Downstream pileup statistics computed via htsjdk disagree with samtools mpileup at these sites.

*Verification rule*: htsjdk 2.23.0 release notes cite 'Fixed a bug in the locus accumulator where the accumulator did not add... (#1489)'

## pysam (4 bugs)

### `pysam-1314` — VCF

- **Issue / PR**: https://github.com/pysam-developers/pysam/issues/1314
- **Anchor**: `install_version` — pre-fix `0.22.1` → post-fix `0.23.0`
- **Confidence**: low
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/pysam-1314/`

VariantFile.write() maps records to wrong contig when header contigs manually edited.

*Verification rule*: Issue #1314 filed 2024-10-21 against 0.22.1; fix expected in 0.23.0 development stream

### `pysam-1308` — VCF

- **Issue / PR**: https://github.com/pysam-developers/pysam/issues/1308
- **Anchor**: `install_version` — pre-fix `0.22.1` → post-fix `0.23.0`
- **Confidence**: high
- **Category**: `parse_error_missed` (crash / rejection)
- **Expected signal**: `uncaught_exception` against pysam_buggy_version
- **Trigger folder**: `compares/bug_bench/triggers/pysam-1308/`

VariantHeader.new_record() fails to set GT field on second+ record creation; KeyError: 'invalid FORMAT: GT'.

*Verification rule*: pysam 0.23.0 release notes explicitly cite 'VariantHeader.new_record GT setting (#1308)'

### `pysam-1214` — SAM

- **Issue / PR**: https://github.com/pysam-developers/pysam/issues/1214
- **Anchor**: `install_version` — pre-fix `0.21.0` → post-fix `0.22.0`
- **Confidence**: medium
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/pysam-1214/`

Pre-fix AlignmentFile iteration over certain malformed-but-spec-tolerated SAM files produces records with incorrect per-record fields. Fixed together with #939 as part of a broader AlignmentFile robustness pass in 0.22.0.

*Verification rule*: pysam 0.22.0 NEWS cites #1214 as fixed in the AlignmentFile cleanup

### `pysam-939` — SAM

- **Issue / PR**: https://github.com/pysam-developers/pysam/issues/939
- **Anchor**: `install_version` — pre-fix `0.21.0` → post-fix `0.22.0`
- **Confidence**: medium
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/pysam-939/`

Long-standing AlignmentFile bug in pysam <=0.21; the 0.22.0 release bundled its fix together with #1214. Specific symptom deferred to trigger-folder research.

*Verification rule*: pysam 0.22.0 NEWS cites #939 as fixed in the AlignmentFile cleanup

## biopython (1 bugs)

### `biopython-4825` — SAM

- **Issue / PR**: https://github.com/biopython/biopython/issues/4825
- **Anchor**: `install_version` — pre-fix `1.85` → post-fix `1.86`
- **Confidence**: medium
- **Category**: `edge_case_missed` (logic bug)
- **Expected signal**: `timeout_or_differential_disagreement` against htsjdk
- **Trigger folder**: `compares/bug_bench/triggers/biopython-4825/`

Excessive copy.deepcopy() in SAM parser; perf degradation with potential correctness impact on large files.

*Verification rule*: PR #4837 merged 2024-09-23 (SAM deepcopy perf); first release after 1.85 is 1.86

## seqan3 (6 bugs)

### `seqan3-2418` — SAM

- **Issue / PR**: https://github.com/seqan/seqan3/pull/2418
- **Anchor**: `commit_sha` — pre-fix `df9fd5ff64f59fdb124c4a564a4141d1f9cff22b` → post-fix `8e374d7ce7a1ce4de0077bc3698d5ae2c8e79600`
- **Confidence**: high
- **Category**: `parse_error_missed` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib, pysam
- **Trigger folder**: `compares/bug_bench/triggers/seqan3-2418/`

BAM parsing forgets to consume sequence bytes when creating dummy alignments; stream iterator misaligned, corrupts subsequent record reads.

*Verification rule*: git rev-parse confirmed: PR #2418 merge commit + parent

### `seqan3-3081` — SAM

- **Issue / PR**: https://github.com/seqan/seqan3/pull/3081
- **Anchor**: `commit_sha` — pre-fix `fa221c1302cfe515211ea70de375a1802826d3d9` → post-fix `c84f5671665478ec1b71535201cbffbe1fdd8c82`
- **Confidence**: high
- **Category**: `writer_bug` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/seqan3-3081/`

Empty SAM/BAM output files invalid (no header written); file unusable unless records explicitly written.

*Verification rule*: git rev-parse confirmed: PR #3081 merge commit + parent

### `seqan3-3269` — SAM

- **Issue / PR**: https://github.com/seqan/seqan3/pull/3269
- **Anchor**: `commit_sha` — pre-fix `ca4d668390e35b4045ccd02d070927f8178ed2ce` → post-fix `11564cb3bcea39666d6d3979080bc5d8fdbe1d7e`
- **Confidence**: high
- **Category**: `off_by_one_coord` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/seqan3-3269/`

Banded alignment returns relative positions of sliced sequences instead of absolute positions of originals; off-by-prefix offset.

*Verification rule*: git rev-parse confirmed: PR #3269 merge commit + parent

### `seqan3-3098` — SAM

- **Issue / PR**: https://github.com/seqan/seqan3/pull/3098
- **Anchor**: `commit_sha` — pre-fix `4961904fbc3b254f7a611b5b467c2e33ae5b1042` → post-fix `4fe548913e96d3f908dd524bd3dc13b48f87bfa4`
- **Confidence**: high
- **Category**: `incorrect_field_value` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/seqan3-3098/`

Alignment score calculation wrong in traceback; incorrect carry bit tracking on up/left open directions causes wrong score.

*Verification rule*: git rev-parse confirmed: PR #3098 merge commit + parent

### `seqan3-2869` — SAM

- **Issue / PR**: https://github.com/seqan/seqan3/pull/2869
- **Anchor**: `commit_sha` — pre-fix `edbfa956f^` → post-fix `edbfa956f`
- **Confidence**: high
- **Category**: `parse_error_missed` (logic bug)
- **Expected signal**: `differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/seqan3-2869/`

FASTA parser fails on IDs containing '>' character; treats '> >MyID' as ID 'MyID' instead of '>MyID'.

*Verification rule*: git log --merges found merge commit edbfa956f for PR #2869 (correct_id_parsing_fasta)

### `seqan3-3406` — SAM

- **Issue / PR**: https://github.com/seqan/seqan3/pull/3406
- **Anchor**: `commit_sha` — pre-fix `745c645fe26272791464cd67180775d28c00bf28` → post-fix `5e5c05a471269703d7afc38bdc4348cef60be63b`
- **Confidence**: high
- **Category**: `encoding_bug` (crash / rejection)
- **Expected signal**: `intermittent_differential_disagreement` against htslib
- **Trigger folder**: `compares/bug_bench/triggers/seqan3-3406/`

BGZF stream data race condition in concurrent reads; non-deterministic corruption.

*Verification rule*: git rev-parse confirmed: PR #3406 merge commit + parent
