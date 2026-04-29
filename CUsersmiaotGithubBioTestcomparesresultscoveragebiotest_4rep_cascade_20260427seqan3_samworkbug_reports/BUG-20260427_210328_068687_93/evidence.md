# Evidence Report: Shuffle TAG:VALUE pairs within @PG header lines
**MR ID**: `e9f5e0fe0e71`
**Scope**: SAM.header
**Oracle**: Parsing the transformed file must produce identical alignment data and header metadata as the original; the order of TAG:VALUE pairs within each @PG line is not semantically significant per SAMv1 §1.3

## Transform Steps
- `shuffle_pg_record_subtags`

## Preconditions
- has_pg_line

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
