# Evidence Report: Shuffle TAG:VALUE pairs within @HD header line
**MR ID**: `04b5bce80e00`
**Scope**: SAM.header
**Oracle**: Parsing the transformed file must produce identical alignment data and header metadata as the original; the order of TAG:VALUE pairs within @HD is not semantically significant per SAMv1 §1.3

## Transform Steps
- `shuffle_hd_subtags`

## Preconditions
- has_hd_line

## Specification Evidence

### Evidence 1
- **Chunk ID**: `SAMv1.tex::The header section::p83`
- **Section**: The header section
- **Severity**: ADVISORY
- **Quote**:
  > Within each (non-@CO) header line, no field tag may appear more than once and the order in which the fields appear is not significant.

### Evidence 2
- **Chunk ID**: `SAMv1.tex::SAM Version History::p326`
- **Section**: SAM Version History
- **Severity**: CRITICAL
- **Quote**:
  > Clarify that header field tags must be distinct within each line, and that the ordering of both header fields and alignment optional fields is not significant.
