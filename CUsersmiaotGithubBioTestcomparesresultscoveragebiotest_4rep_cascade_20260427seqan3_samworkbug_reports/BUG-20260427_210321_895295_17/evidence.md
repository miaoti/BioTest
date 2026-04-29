# Evidence Report: Reordering @RG header lines preserves SAM semantics
**MR ID**: `a6d5fda42b2b`
**Scope**: SAM.header
**Oracle**: After reordering @RG header lines, the output must be semantically equivalent to the original. The SAM spec explicitly states that unordered multiple @RG lines are allowed.

## Transform Steps
- `reorder_header_records`

## Preconditions
- has_rg_line

## Specification Evidence

### Evidence 1
- **Chunk ID**: `SAMv1.tex::The SAM Format Specification::p29`
- **Section**: The SAM Format Specification
- **Severity**: CRITICAL
- **Quote**:
  > @HD & File-level metadata. Optional. If present, there must be only one @HD line and it must be the first line of the file.
