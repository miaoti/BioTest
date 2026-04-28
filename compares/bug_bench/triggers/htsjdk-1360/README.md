# htsjdk-1360 — Pre-fix rejects valid zero-length read under STRICT

**SUT**: htsjdk
**Format**: SAM
**Severity**: logic bug (over-strict spec rejection of valid input)
**Anchor**: install_version `2.19.0` → `2.20.0`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1360 (closes #1174)

## What the bug does

Pre-fix `SAMRecord.isValid()` adds an `EMPTY_READ` validation error
when `SEQ=*`, `QUAL=*`, the read is primary, and no `FZ` / `CS` /
`CQ` tag is present. Under default STRICT stringency this becomes
`SAMFormatException` at parse time. The SAM spec does not require
zero-length reads to carry these tags; htslib and pysam accept them
silently. So pre-fix htsjdk is the outlier rejecting valid input.

Post-fix (2.20.0) deletes the entire EMPTY_READ validation block
(commit text references PR #1360 explicitly).

## Trigger

`original.sam` — single record with `CIGAR=*`, `SEQ=*`, `QUAL=*`,
`FLAG=0` (primary), no special tags. 2.19.0 STRICT throws; 2.20.0
STRICT accepts.

## Detection criterion

- **Direction**: forward §5.3.1 — pre-fix STRICT fails; post-fix
  STRICT succeeds.
- **Stringency**: requires `_replay_trigger_silenced` to invoke
  `run_strict_parse` (in addition to default SILENT) so the
  pre/post difference is observable.
- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib (htslib silently accepts).
