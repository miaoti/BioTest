# seqan3-3406 — BGZF stream data race condition in concurrent reads; non-deterministic corruption.

**SUT**: seqan3
**Format**: SAM
**Severity**: crash / incorrect rejection
**Anchor**: commit_sha `745c645fe26272791464cd67180775d28c00bf28` → `5e5c05a471269703d7afc38bdc4348cef60be63b`
**Confidence**: high
**Issue / PR**: https://github.com/seqan/seqan3/pull/3406

## What the bug does

BGZF stream data race condition in concurrent reads; non-deterministic corruption.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `intermittent_differential_disagreement`
- **Compared against**: htslib
