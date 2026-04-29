# Evidence Report: Permute structured KV order in header then BCF round-trip preserves query method results
**MR ID**: `283f6ab86e27`
**Scope**: VCF.header
**Oracle**: After reordering key=value pairs inside structured ##INFO/##FORMAT/##FILTER meta-lines and round-tripping through BCF, all public query methods on parsed records must return identical values. The BCF2 spec requires all INFO and GENOTYPE fields to be fully typed in the header (p1297), and the dictionary of strings depends on the order of header lines (p1304). A spec-compliant parser must resolve field types by ID, not by key order within a structured line.

## Transform Steps
- `permute_structured_kv_order`
- `vcf_bcf_round_trip`

## Preconditions
- bcf_codec_available
- pysam_runtime_reachable
- header_has_structured_meta_lines

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1297`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] * All INFO and GENOTYPE fields must be fully typed in the BCF2 header to enable type-specific encoding of the fields in records.
  An error must be thrown when converting a VCF to BCF2 when an unknown or not fully specified field is encountered in the records.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::BCF specification::p1292`
- **Section**: BCF specification
- **Severity**: CRITICAL
- **Quote**:
  > [VCF v4.5 — BCF specification] Overall, the idea behind is BCF2 is simple.
BCF2 is a binary, compressed equivalent of VCF that can be indexed with tabix and can be efficiently decoded from disk or streams.
For efficiency reasons BCF2 only supports a subset of VCF, in that all info and genotype fields must have their full types specified.
That is, BCF2 requires that if e.g. an info field AC is present then it must contain an equivalent VCF header line noting that AC is an allele indexed array of type integer.

## Ambiguity Flags

- The spec does not explicitly state that key=value order within a structured meta-line is semantically irrelevant, though the ID field is the authoritative identifier.