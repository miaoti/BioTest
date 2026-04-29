# Evidence Report: Hard/soft clipping equivalence invariance
**MR ID**: `db1f4df6b38f`
**Scope**: SAM.record
**Oracle**: Converting between hard-clipping (H) and soft-clipping (S) representations preserves the underlying alignment semantics; the parser must accept both forms as equivalent. When converting H->S, dummy bases are added to SEQ/QUAL; when converting S->H, those bases are trimmed.

## Transform Steps
- `toggle_cigar_hard_soft_clipping`

## Preconditions
- has_cigar
- has_seq
- seed has at least one alignment with hard-clipping (H) or soft-clipping (S) CIGAR operations

## Specification Evidence

### Evidence 1
- **Chunk ID**: `SAMv1.tex::The SAM Format Specification::p50`
- **Section**: The SAM Format Specification
- **Severity**: CRITICAL
- **Quote**:
  > H can only be present as the first and/or last operation. S may only have H operations between them and the ends of the CIGAR string.

### Evidence 2
- **Chunk ID**: `SAMv1.tex::The SAM Format Specification::p53`
- **Section**: The SAM Format Specification
- **Severity**: CRITICAL
- **Quote**:
  > If not a `*', the length of the sequence must equal the sum of lengths of MIS=X operations in CIGAR.

## Ambiguity Flags

- The spec does not explicitly define H and S as interchangeable representations; the equivalence is a normalization convention rather than a normative rule