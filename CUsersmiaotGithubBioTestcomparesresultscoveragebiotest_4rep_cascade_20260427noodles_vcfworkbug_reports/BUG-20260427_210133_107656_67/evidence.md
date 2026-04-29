# Evidence Report: Permute sample columns round-trip through SUT writer preserves per-sample data integrity
**MR ID**: `9ae0983745bc`
**Scope**: VCF.record
**Oracle**: After permuting sample column order, parsing with noodles, re-serializing, and re-parsing must yield identical canonical content with the same sample ordering as the permuted input. Each sample's genotype and FORMAT data must remain correctly associated with its sample ID regardless of column ordering.

## Transform Steps
- `permute_sample_columns`
- `sut_write_roundtrip`

## Preconditions
- primary_sut_has_writer

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1297`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] * All INFO and GENOTYPE fields must be fully typed in the BCF2 header to enable type-specific encoding of the fields in records.
  An error must be thrown when converting a VCF to BCF2 when an unknown or not fully specified field is encountered in the records.
