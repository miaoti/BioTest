# Evidence Report: Structured meta-line key=value pairs can be reordered
**MR ID**: `bc124d1e4573`
**Scope**: VCF.header
**Oracle**: After reordering key=value pairs inside ##INFO, ##FORMAT, or ##FILTER structured meta-lines (e.g., Number=1,Type=Integer -> Type=Integer,Number=1), the SUT must produce identical canonical output. Per VCF v4.5 §1.2, implementations must not rely on the order of fields within structured lines.

## Transform Steps
- `permute_structured_kv_order`

## Preconditions
- has_structured_meta_lines

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p121`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > Implementations must not rely on the order of the fields within structured lines and are not required to preserve field ordering.
