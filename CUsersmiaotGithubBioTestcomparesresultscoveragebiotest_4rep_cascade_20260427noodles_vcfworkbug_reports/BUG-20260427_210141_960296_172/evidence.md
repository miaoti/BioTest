# Evidence Report: Sample column permutation invariance
**MR ID**: `f335b8c5d509`
**Scope**: VCF.record
**Oracle**: After permuting sample column order consistently across the header and all data lines, the SUT must produce identical canonical output when samples are identified by ID rather than column position. The spec defines sample columns as 'an arbitrary number of sample IDs' with no positional semantics beyond the ID mapping.

## Transform Steps
- `permute_sample_columns`

## Preconditions
- has_sample_columns
- sample_count>=2

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::The VCF specification::p45`
- **Section**: The VCF specification
- **Severity**: CRITICAL
- **Quote**:
  > If genotype data is present in the file, these are followed by a FORMAT column header, then an arbitrary number of sample IDs. Duplicate sample IDs are not allowed.

## Ambiguity Flags

- The spec says 'an arbitrary number of sample IDs' but does not explicitly state that column order is semantically insignificant. However, sample identity is by ID, not position.