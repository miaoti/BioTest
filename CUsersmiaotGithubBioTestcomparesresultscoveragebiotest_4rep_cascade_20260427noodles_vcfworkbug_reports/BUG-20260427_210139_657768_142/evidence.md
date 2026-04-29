# Evidence Report: INFO field key=value pairs in data lines can be shuffled
**MR ID**: `31e4b85ca55b`
**Scope**: VCF.record
**Oracle**: After shuffling the semicolon-separated key=value entries in the INFO column of data records, the SUT must produce identical canonical output. The spec does not impose ordering constraints on INFO sub-fields; duplicate keys are forbidden but order is not semantically significant.

## Transform Steps
- `shuffle_info_field_kv`

## Preconditions
- has_info_field
- info_has_multiple_keys

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::Data lines::p221`
- **Section**: Data lines
- **Severity**: CRITICAL
- **Quote**:
  > Duplicate keys are not allowed. Arbitrary keys are permitted, although those listed in Table <ref> and described below are reserved (albeit optional).

## Ambiguity Flags

- The spec does not explicitly state that INFO key=value order is insignificant, but it only forbids duplicate keys and does not mandate any ordering. This is an implicit ordering invariance.