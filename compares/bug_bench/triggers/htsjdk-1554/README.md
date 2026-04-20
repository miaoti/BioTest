# htsjdk-1554 — AC / AN / AF include filtered genotypes

**Severity**: logic bug (incorrect field values affect every downstream
  filter / recomputation).
**Format**: VCF.
**Anchor**: pre_fix = htsjdk 2.24.1, post_fix = htsjdk 3.0.0.
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1554

## What the bug does

The VCF spec treats per-sample `FT` (genotype filter) as indicating
that the genotype itself should be **excluded** from cohort-level
allele-count statistics (AC, AN, AF). htsjdk 2.x's
`VariantContext.getCalledChrCount()` was enumerating all genotypes
regardless of FT, inflating AC/AN/AF for any cohort where any sample
had a genotype-level filter applied.

## Trigger

A VCF with at least two samples, where at least one sample has a
non-`PASS` FT value on a genotype that contains a non-reference
allele. `original.vcf` below is the minimal case.

## Files

- `original.vcf` — 2-sample VCF, sample1 hom-ref passing, sample2
  het-variant but FT-filtered. On the pre-fix SUT, recomputed AC = 1
  (wrong, because the FT-filtered allele is included); on the post-
  fix SUT, AC = 0 (correct).
- `reproduce.java` — minimal main() calling `VariantContext.
  getCalledChrCount()` before and after applying
  `GenotypeBuilder.filter(...)`.
- `issue_source.txt` — excerpted from the PR description + the test
  method added by the fix.

## Detection criterion

- **Expected signal**: `differential_disagreement` against `htslib`
  (`bcftools view` respects FT) and `pysam`.
- **Metamorphic variant**: BioTest's
  `metamorphic_filter_then_recompute_AC` transform — filter one
  genotype on post-fix SUT and recompute; on buggy SUT the AC stays
  the same (wrong) where it should drop by one.
