# Evidence Report: Shuffle @CO comment line order
**MR ID**: `2967d6eb3016`
**Scope**: SAM.header
**Oracle**: Parsing the transformed file must produce identical alignment data and header metadata as the original; @CO lines are free-text comments with no ordering semantics per SAMv1 §1.3

## Transform Steps
- `shuffle_co_comments`

## Preconditions
- has_co_lines

## Specification Evidence

### Evidence 1
- **Chunk ID**: `SAMv1.tex::The header section::p83`
- **Section**: The header section
- **Severity**: ADVISORY
- **Quote**:
  > Each header line begins with the character `@' followed by one of the two-letter header record type codes defined in this section. In the header, each line is TAB-delimited and, apart from @CO lines, each data field follows a format `TAG:VALUE' where TAG is a two-character string that defines the format and content of VALUE. Thus header lines match /94@(HD|SQ|RG|PG)(92t[A-Za-z][A-Za-z0-9]:[ -126]+)+$/ or /94@CO92t.*/.
