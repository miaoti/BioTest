# Evidence Report: Meta-information lines can be reordered (except ##fileformat first)
**MR ID**: `ffbe4a62d130`
**Scope**: VCF.header
**Oracle**: After shuffling all ##meta-information lines (keeping ##fileformat pinned first), the SUT must produce identical canonical output (e.g., parsed JSON) as before the transform. Per VCF v4.5 §1.2, meta-information lines other than ##fileformat may appear in any order.

## Transform Steps
- `shuffle_meta_lines`

## Preconditions
- has_two_meta_lines

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p122`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > Other than |##fileformat|, they may appear in any order.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::Changes between VCFv4.2 and VCFv4.3::p1691`
- **Section**: Changes between VCFv4.2 and VCFv4.3
- **Severity**: CRITICAL
- **Quote**:
  > Meta-information lines can be in any order, with the exception of ##fileformat which must come first.
