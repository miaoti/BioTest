# Evidence Report: Split or merge adjacent identical CIGAR operations preserves semantics
**MR ID**: `7690cdb23c3e`
**Scope**: SAM.record
**Oracle**: The total query-consuming length (sum of M, I, S, =, X operations) must remain unchanged; the alignment position and reference-consuming length must remain unchanged.

## Transform Steps
- `split_or_merge_adjacent_cigar_ops`

## Preconditions
- has_cigar

## Specification Evidence

### Evidence 1
- **Chunk ID**: `SAMv1.tex::Recommended Practice for the SAM Format::p134`
- **Section**: Recommended Practice for the SAM Format
- **Severity**: ADVISORY
- **Quote**:
  > Adjacent CIGAR operations should be different.

## Ambiguity Flags

- The spec says 'should' (advisory), not 'must' — adjacent identical CIGAR ops are not strictly prohibited, so splitting/merging them is semantics-preserving for conformant parsers.