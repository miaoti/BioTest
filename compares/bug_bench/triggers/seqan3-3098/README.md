# seqan3-3098 — Alignment score calculation wrong in traceback; incorrect carry bit tracking on up/left open directions causes wrong score.

**SUT**: seqan3
**Format**: SAM
**Severity**: logic bug
**Anchor**: commit_sha `4961904fbc3b254f7a611b5b467c2e33ae5b1042` → `4fe548913e96d3f908dd524bd3dc13b48f87bfa4`
**Confidence**: high
**Issue / PR**: https://github.com/seqan/seqan3/pull/3098

## What the bug does

Alignment score calculation wrong in traceback; incorrect carry bit tracking on up/left open directions causes wrong score.

## Trigger

See sibling files in this folder (if present):

- `original.sam` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib
