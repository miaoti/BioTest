# pysam-1308 — VariantHeader.new_record() fails on second GT set

**Severity**: logic bug (raises KeyError the second time you do the
  same thing; state-dependence bug).
**Format**: VCF (in-memory, no input file needed).
**Anchor**: pre_fix = pysam 0.22.1, post_fix = pysam 0.23.0.
**Issue / PR**: https://github.com/pysam-developers/pysam/issues/1308

## What the bug does

`VariantHeader.new_record(samples=[{"GT": (0, 0)}])` succeeds on the
first call. On any subsequent call with the same payload, pysam 0.22.1
raises `KeyError: 'invalid FORMAT: GT'` even though the header's
`formats` table still has GT registered. The problem is that pysam's
record factory caches a stale-after-first-use handle to the FORMAT
table; the second `new_record` looks up GT against the cleared cache
and can't resolve it.

## Trigger

Pure in-memory Python, no file needed. Build a header, call
`new_record` twice. First succeeds; second throws.

## Files

- `reproduce.py` — the 13-line reproducer from the issue.
- `issue_source.txt` — excerpt of issue #1308.

## Detection criterion

- **Expected signal**: `uncaught_exception` on the pre-fix SUT.
  The exception type is `KeyError`; its message contains the string
  `'invalid FORMAT: GT'`. Post-fix, both calls succeed silently.
