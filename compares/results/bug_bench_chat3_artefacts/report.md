# Chat 3 -- vcfpy VCF bug-bench (biotest excluded)

- total cells: 14
- tools: atheris, pure_random
- bugs: 7

## Legend

- **FOUND** — tool produced a trigger that fails pre-fix and is silenced by post-fix
- **crash?** — tool crashed pre-fix but post-fix replay inconclusive (null)
- **false+** — tool crashed pre-fix but post-fix STILL crashes (likely unrelated)
- **miss** — tool ran but did not produce a triggering input
- **—** — no result.json (cell was skipped: install failed, harness mismatch, etc.)

## Per-bug matrix

| bug | atheris | pure_random |
| :-- | :-: | :-: |
| vcfpy-127 | skip | skip |
| vcfpy-145 | miss | miss |
| vcfpy-146 | miss | miss |
| vcfpy-171 | miss | miss |
| vcfpy-176 | miss | miss |
| vcfpy-gtone-0.13 | miss | miss |
| vcfpy-nocall-0.8 | skip | skip |

## Per-tool bugs found

### atheris

- FOUND (0): (none)
- crash? (0): (none)
- miss (5): vcfpy-145, vcfpy-146, vcfpy-171, vcfpy-176, vcfpy-gtone-0.13
- skip (2): vcfpy-127, vcfpy-nocall-0.8

### pure_random

- FOUND (0): (none)
- crash? (0): (none)
- miss (5): vcfpy-145, vcfpy-146, vcfpy-171, vcfpy-176, vcfpy-gtone-0.13
- skip (2): vcfpy-127, vcfpy-nocall-0.8
