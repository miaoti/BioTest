# Evidence Report: Write round-trip invariance via SUT serializer
**MR ID**: `9e3642fe5315`
**Scope**: VCF.record
**Oracle**: After parsing the VCF with the primary SUT and re-serializing via its public writer API, the re-parsed output must deep-equal the original parse result. Per Chen et al. 2018 §3.2, parse(write(parse(x))) must be invariant.

## Transform Steps
- `sut_write_roundtrip`

## Preconditions
- primary_sut_has_writer

## Specification Evidence

### Evidence 1
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p122`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > Other than |##fileformat|, they may appear in any order.

### Evidence 2
- **Chunk ID**: `VCFv4.5.tex::Meta-information lines::p121`
- **Section**: Meta-information lines
- **Severity**: CRITICAL
- **Quote**:
  > Implementations must not rely on the order of the fields within structured lines and are not required to preserve field ordering.

## Ambiguity Flags

- The SUT writer may reorder meta-lines or structured field key-value pairs; the oracle must compare semantic equivalence, not byte-level equality.