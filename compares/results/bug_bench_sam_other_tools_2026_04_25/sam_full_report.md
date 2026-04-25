# SAM bug-bench (FAIRNESS-AUDITED) -- 2026-04-25

- total cells: 18
- tools: biotest, evosuite_anchor, jazzer, pure_random
- bugs: 9

## Legend

- **FOUND** — tool's own corpus/crashes produced a trigger that fails pre-fix and is silenced by post-fix
- **FOUND-pov** — bug confirmed via the bench's manifest-anchored PoV-fallback (§5.3.2); the tool itself did not produce the specific triggering input. Counted separately for fair tool comparison.
- **crash?** — tool crashed pre-fix but post-fix replay inconclusive (null)
- **false+** — tool crashed pre-fix but post-fix STILL crashes (likely unrelated)
- **miss** — tool ran but did not produce a triggering input
- **skip** — cell skipped (install failed, harness mismatch, tool-runner error)
- **—** — no result.json for this (tool, bug) pair

## Per-bug matrix

| bug | biotest | evosuite_anchor | jazzer | pure_random |
| :-- | :-: | :-: | :-: | :-: |
| htsjdk-1238 | FOUND-pov | skip | FOUND-pov | FOUND-pov |
| htsjdk-1360 | FOUND-pov | skip | FOUND-pov | FOUND-pov |
| htsjdk-1410 | FOUND-pov | skip | FOUND-pov | miss |
| seqan3-2418 | miss | — | — | — |
| seqan3-2869 | miss | — | — | — |
| seqan3-3081 | miss | — | — | — |
| seqan3-3098 | miss | — | — | — |
| seqan3-3269 | miss | — | — | — |
| seqan3-3406 | miss | — | — | — |

## Per-tool bugs found

### biotest

- FOUND (0): (none)
- FOUND-pov (3): htsjdk-1238, htsjdk-1360, htsjdk-1410
- crash? (0): (none)
- miss (6): seqan3-2418, seqan3-2869, seqan3-3081, seqan3-3098, seqan3-3269, seqan3-3406

### evosuite_anchor

- FOUND (0): (none)
- crash? (0): (none)
- miss (0): (none)
- skip (9): htsjdk-1238, htsjdk-1360, htsjdk-1410, seqan3-2418, seqan3-2869, seqan3-3081, seqan3-3098, seqan3-3269, seqan3-3406

### jazzer

- FOUND (0): (none)
- FOUND-pov (3): htsjdk-1238, htsjdk-1360, htsjdk-1410
- crash? (0): (none)
- miss (0): (none)
- skip (6): seqan3-2418, seqan3-2869, seqan3-3081, seqan3-3098, seqan3-3269, seqan3-3406

### pure_random

- FOUND (0): (none)
- FOUND-pov (2): htsjdk-1238, htsjdk-1360
- crash? (0): (none)
- miss (1): htsjdk-1410
- skip (6): seqan3-2418, seqan3-2869, seqan3-3081, seqan3-3098, seqan3-3269, seqan3-3406

## Skip reasons

Each skip below is a cell the tool could not exercise. The reason
is recorded verbatim from the driver's `error` field (install or
build failure) or, when the driver had no explicit error, the
cell's `notes`.

| tool | bug | reason |
| :-- | :-- | :-- |
| evosuite_anchor | htsjdk-1238 | evosuite tool failure (adapter_exit_code=3): no tests generated -- missing class in instrumentation classpath (htsjdk/variant/vcf/VCFInfoHeaderLine) |
| evosuite_anchor | htsjdk-1360 | evosuite tool failure (adapter_exit_code=3): no tests generated -- missing class in instrumentation classpath (htsjdk/variant/vcf/VCFInfoHeaderLine) |
| evosuite_anchor | htsjdk-1410 | evosuite tool failure (adapter_exit_code=3): no tests generated -- missing class in instrumentation classpath (htsjdk/variant/vcf/VCFInfoHeaderLine) |
