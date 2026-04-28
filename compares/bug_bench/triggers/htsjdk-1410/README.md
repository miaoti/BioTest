# htsjdk-1410 — Pre-fix rejects |TLEN| > 2^29 under STRICT

**SUT**: htsjdk
**Format**: SAM
**Severity**: logic bug (over-strict spec rejection of valid input)
**Anchor**: install_version `2.20.2` → `2.20.3`
**Confidence**: high
**Issue / PR**: https://github.com/samtools/htsjdk/pull/1410

## What the bug does

Pre-fix `SAMRecord.MAX_INSERT_SIZE = 1 << 29 = 536_870_912`. Under
default STRICT stringency, `isValid()` raises `INVALID_INSERT_SIZE`
("Insert size out of range") whenever `|TLEN| > 2^29`. SAM spec
defines TLEN as a signed 32-bit integer, so values up to
`Integer.MAX_VALUE = 2_147_483_647` are spec-compliant. Pre-fix
htsjdk is the outlier; htslib / pysam accept any int32 TLEN.

Post-fix (2.20.3) raises `MAX_INSERT_SIZE` to `Integer.MAX_VALUE`.

## Trigger

`original.sam` — single paired record with `TLEN=600000000`
(> 2^29 but well within int32). 2.20.2 STRICT throws; 2.20.3 STRICT
accepts.

## Detection criterion

- **Direction**: forward §5.3.1 — pre-fix STRICT fails; post-fix
  STRICT succeeds.
- **Stringency**: requires `_replay_trigger_silenced` to invoke
  `run_strict_parse` (in addition to default SILENT).
- **Expected signal**: `differential_disagreement`
- **Compared against**: htslib (htslib accepts any int32 TLEN).
