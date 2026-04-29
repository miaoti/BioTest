# Evidence Report: Missing-value round-trip via equivalent FORMAT extension
**MR ID**: `6cd9bfb18f53`
**Scope**: VCF.record
**Oracle**: Appending a FORMAT field filled with '.' (missing) to all samples is semantically a no-op; parsing and re-serializing must produce the same canonical content as the original.

## Transform Steps
- `inject_equivalent_missing_values`

## Preconditions
- format_has_gt

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::The VCF specification::p64`
- **Section**: The VCF specification
- **Severity**: CRITICAL
- **Quote**:
  > If any of the fields is missing, it is replaced with the MISSING value. For example if the FORMAT is GT:GQ:DP:HQ then 0|0:.:23:23,34 indicates that GQ is missing.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::Data lines::p250`
- **Section**: Data lines
- **Severity**: CRITICAL
- **Quote**:
  > If a field contains a list of missing values, it can be represented either as a single MISSING value (`.') or as a list of missing values (e.g. `.,.,.' if the field was Number=3).
