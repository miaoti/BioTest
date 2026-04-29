# Evidence Report: split_multi_allelic_invariance
**MR ID**: `21172f02daed`
**Scope**: VCF.record
**Oracle**: After splitting a multi-ALT record into one record per ALT allele with synchronized Number=A INFO/FORMAT arrays and remapped GT indices, the set of variants represented must be semantically identical to the original multi-ALT form.

## Transform Steps
- `split_multi_allelic`

## Preconditions
- alt_count>=2

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p126`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > A: The field has one value per alternate allele.
The values must be in the same order as listed in the ALT column (described in section data-lines).
R: The field has one value for each possible allele, including the reference.
The order of the values must be the reference allele first, then the alternate alleles as listed in the ALT column.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::Information field format::p158`
- **Section**: Information field format
- **Severity**: CRITICAL
- **Quote**:
  > R: The field has one value for each possible allele, including the reference.
The order of the values must be the reference allele first, then the alternate alleles as listed in the ALT column.

## Ambiguity Flags

- The VCF v4.5 spec does not explicitly mandate that multi-allelic records must be splittable into individual records; this MR derives from the Number=A/R semantics which define per-allele value ordering