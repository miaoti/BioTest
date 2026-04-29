# Evidence Report: Sample column permutation across header and data lines
**MR ID**: `aae1913889e7`
**Scope**: VCF.header
**Oracle**: After permuting sample columns consistently across the header and all data lines, the resulting VCF must be semantically equivalent to the original. The mapping between sample IDs and their genotype/format data is preserved; only the column ordering changes.

## Transform Steps
- `permute_sample_columns`

## Preconditions
- sample_count >= 2

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::The VCF specification::p63`
- **Section**: The VCF specification
- **Severity**: CRITICAL
- **Quote**:
  > If genotype information is present, then the same types of data must be present for all samples. First a FORMAT field is given specifying the data types and order (colon-separated FORMAT keys matching the regular expression \^[A-Za-z\_][0-9A-Za-z\_.]*\$, duplicate keys are not allowed). This is followed by one data block per sample, with the colon-separated data corresponding to the types specified in the format.

## Ambiguity Flags

- The spec does not mandate any particular ordering of sample columns; column order is an implementation choice. Permuting them preserves all sample-to-data mappings.