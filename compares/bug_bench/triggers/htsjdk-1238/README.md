# htsjdk-1238 — `@SQ SN:` accepts characters disallowed by SAM 1.6 RNAME regex

**SUT**: htsjdk
**Format**: SAM
**Severity**: logic bug (parse-time spec rejection silently accepted)
**Anchor**: install_version `2.18.1` → `2.18.2`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1238 (closes #1471)

## What the bug does

Pre-fix htsjdk `SAMSequenceRecord` constructor only checks for whitespace
in `SN:` values. Spec §1.3 mandates the RNAME regex
`[0-9A-Za-z!#$%&+./:;?@^_|~-][0-9A-Za-z!#$%&*+./:;=?@^_|~-]*`. Comma,
parentheses, brackets, quotes, etc. are all spec-disallowed but parse
silently in 2.18.1.

Post-fix (2.18.2) adds `validateSequenceName()` which throws
`SAMException: Sequence name '...' doesn't match regex` from inside the
constructor — so opening the file fails immediately.

## Trigger

`original.sam` — minimal SAM with `@SQ SN:gi|123|chr,1` (the comma is
the spec violation). 2.18.1 parses cleanly; 2.18.2 throws.

## Detection criterion

- **Direction**: reverse §5.3.1 — pre-fix accepts; post-fix rejects.
  Bidirectional logic in `bug_bench_driver.run_bench` fires when
  `pre_fix_succeeds=True AND post_silenced=False`.
- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib (htslib also accepts the comma; the bug
  is htsjdk-specific over-permissiveness in pre-fix).
