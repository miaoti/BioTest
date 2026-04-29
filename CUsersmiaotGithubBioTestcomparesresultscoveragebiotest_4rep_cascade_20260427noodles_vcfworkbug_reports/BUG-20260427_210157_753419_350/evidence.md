# Evidence Report: Shuffle meta-lines round-trip through SUT writer preserves content
**MR ID**: `9c145ef41bc2`
**Scope**: VCF.header
**Oracle**: After shuffling ##meta-information lines (keeping ##fileformat first), parsing with noodles, re-serializing, and re-parsing must yield identical canonical content. The order of meta-information lines is not semantically significant per VCF spec, so a compliant parser must produce identical records regardless of header line ordering.

## Transform Steps
- `shuffle_meta_lines`
- `sut_write_roundtrip`

## Preconditions
- primary_sut_has_writer

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1304`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] Defined this way, the dictionary of strings depends on the order and the presence of all preceding header lines.
If an existing tag needs to be removed from a BCF, also all consequent tags throughout the whole BCF would have to be recoded.
In order to avoid this costly operation, a new IDX field can be used to explicitly define the position which is dropped on BCF-to-VCF conversion.
If not present, the implicit relative position is assumed.
If the IDX field is present in one record, it must be present also in all other dictionary-defining records.
The IDX tag is not necessary in newly created BCF files, but if present, the numbering must match the implicit dictionary of tags.

## Ambiguity Flags

- The BCF dictionary of strings depends on header line order; a VCF-only writer round-trip (no BCF) should not be affected by this, but some parsers may internally reorder header lines on serialization.