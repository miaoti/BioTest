# Chat 3 -- vcfpy VCF bug-bench (biotest excluded; FAIRNESS-AUDITED)

- total cells: 14
- tools: atheris, pure_random
- bugs: 7

## Legend

- **FOUND** — tool's own corpus/crashes produced a trigger that fails pre-fix and is silenced by post-fix
- **FOUND-pov** — bug confirmed via the bench's manifest-anchored PoV-fallback (§5.3.2); the tool itself did not produce the specific triggering input. Counted separately for fair tool comparison.
- **crash?** — tool crashed pre-fix but post-fix replay inconclusive (null)
- **false+** — tool crashed pre-fix but post-fix STILL crashes (likely unrelated)
- **miss** — tool ran but did not produce a triggering input
- **skip** — cell skipped (install failed, harness mismatch, tool-runner error)
- **—** — no result.json for this (tool, bug) pair

## Per-bug matrix

| bug | atheris | pure_random |
| :-- | :-: | :-: |
| vcfpy-127 | miss | miss |
| vcfpy-145 | miss | miss |
| vcfpy-146 | miss | miss |
| vcfpy-171 | miss | miss |
| vcfpy-176 | miss | miss |
| vcfpy-gtone-0.13 | miss | miss |
| vcfpy-nocall-0.8 | miss | miss |

## Per-tool bugs found

### atheris

- FOUND (0): (none)
- crash? (0): (none)
- miss (7): vcfpy-127, vcfpy-145, vcfpy-146, vcfpy-171, vcfpy-176, vcfpy-gtone-0.13, vcfpy-nocall-0.8

### pure_random

- FOUND (0): (none)
- crash? (0): (none)
- miss (7): vcfpy-127, vcfpy-145, vcfpy-146, vcfpy-171, vcfpy-176, vcfpy-gtone-0.13, vcfpy-nocall-0.8
