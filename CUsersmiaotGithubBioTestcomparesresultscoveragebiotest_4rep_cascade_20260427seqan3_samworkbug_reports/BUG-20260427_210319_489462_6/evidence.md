# Evidence Report: Permute optional TAG:TYPE:VALUE fields on alignment lines
**MR ID**: `97a5283cec91`
**Scope**: SAM.record
**Oracle**: Parsing the transformed file must produce identical alignment data as the original; the order of optional TAG:TYPE:VALUE fields on alignment lines is not semantically significant per SAMv1 §1.5

## Transform Steps
- `permute_optional_tag_fields`

## Preconditions
- has_optional_tag

## Specification Evidence

### Evidence 1
- **Chunk ID**: `SAMv1.tex::SAM Version History::p326`
- **Section**: SAM Version History
- **Severity**: CRITICAL
- **Quote**:
  > Clarify that header field tags must be distinct within each line, and that the ordering of both header fields and alignment optional fields is not significant.
