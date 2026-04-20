# htsjdk-1637 — VCF sort-order regression breaks merging

**Severity**: logic bug (false "unsorted" rejection on valid VCFs).
**Format**: VCF.
**Anchor**: pre_fix = htsjdk 3.0.3, post_fix = htsjdk 3.0.4.
**Issue / PR**: https://github.com/samtools/htsjdk/issues/1637

## What the bug does

htsjdk 3.0.3 shipped PR #1593 which changed the VCF variant sort order
to use allele strings as a tiebreaker when two variants share the same
`CHROM:POS`. The intent was to stabilise sort order across runs. The
effect: existing VCFs sorted under the previous rule now fail htsjdk's
own "is sorted" check, so any downstream operation that validates sort
order (e.g. `bcftools merge`, htsjdk's own merge utilities) raises a
false "VCF is not coordinate sorted" error.

htsjdk 3.0.4 reverted PR #1593 via commit `e2943b7` and re-introduced
a split-comparator pattern (one comparator for *sorting*, another for
*validating already-sorted*).

## Trigger

A VCF with two records at the same `CHROM:POS` whose alleles sort in
different orders under the two comparators. Minimal case: CHROM=1,
POS=100, one REF=`A` ALT=`C` record followed by one REF=`A` ALT=`T`
record. Pre-3.0.3 (or post-fix 3.0.4+) treats this as valid;
3.0.3 rejects it with "unsorted".

## Files

- `original.vcf` — 2-record minimal reproducer.
- `issue_source.txt` — excerpt of the issue + the revert commit message.

## Detection criterion

- **Expected signal**: `differential_disagreement`. The buggy htsjdk
  (3.0.3) rejects the file; htslib (bcftools) accepts it. The
  post-fix htsjdk (3.0.4) also accepts. A bench run observes the
  rejection on the pre-fix SUT and passes on the post-fix SUT.
