# BioTest — Phase 4 VCF Rerun after Oracle Fix (v4, 2026-04-22)

Follow-up to `oracle_and_detection_audit.md`. After landing the
oracle fix-pack (per-voter post-normalizer + strict bucketing on
variant-identity + driver-side pre-fix-failure check) the real-bug
benchmark was re-run for the VCF half of the manifest and the
numbers now match what the independent audit script said was
*actually* real.

## Headline

| Metric | Original run (v2) | Audit-corrected | **v4 re-run (in-driver)** |
|:--|:-:|:-:|:-:|
| htsjdk confirmed | 9 / 9 | 0 / 9 | **0 / 9** ✓ |
| vcfpy confirmed | 2 / 7 | 2 / 7 | **2 / 7** ✓ |
| noodles confirmed | 6 / 9 | 0 / 6 scored (3 install-fail) | **0 / 6 scored** ✓ |
| **Total confirmed** | **17 / 25 (68 %)** | **2 / 25 (8 %)** | **2 / 25 (8 %)** ✓ |
| False positives | 15 | — | **0** |

The v4 run reproduces the audit-corrected numbers directly — no
post-hoc re-scoring needed. The driver now enforces both halves of
DESIGN.md §5.3.1's detection predicate.

## What changed since v2

1. **Post-normalization layer** (`test_engine/canonical/post_normalize.py`)
   — folds per-voter canonicalisation quirks before the consensus
   oracle buckets. Handles:
   - fileformat coercion (htsjdk `VCF4_3`, noodles Rust `Debug` form,
     dict form → `VCFv4.3`)
   - header-meta quoting / `IDX` pruning / `Number` str coercion /
     implicit-PASS + simple-scalar normalisation
   - INFO/FORMAT schema-aware typing (htsjdk's always-string numeric
     fields → int/float per header declaration)
   - ALT bracket strip + harness `getBaseString` → `getDisplayString`
     fix (see below) so every voter represents `<NON_REF>`, `<DEL>`,
     `<*>` as the same token
   - RNEXT `=` resolution, SEQ case-normalize, POS/FLAG/MAPQ int
     coercion, GT phase recovery from pysam's `phased` flag
2. **Strict bucket scope** (`test_engine/oracles/tolerance.py`) —
   the bucket key drops `header` entirely and keeps only variant-
   identity fields per record (`CHROM`, `POS`, `REF`, `ALT`).
   Per-voter header variance on free-form ## keys was the dominant
   cause of the `1 / 47` consensus floor.
3. **Java harness rebuild** (`harnesses/java/BioTestHarness.java`)
   — `Allele.getBaseString()` returns `""` on symbolic alleles;
   switched to `getDisplayString()` and strip `<>` so `<*>` /
   `<NON_REF>` / `<DEL>` agree with vcfpy / pysam / reference.
   This single harness fix eliminated 621 ALT diffs on
   `real_world_htslib_index.vcf` alone.
4. **pysam POS off-by-one** (`test_engine/runners/pysam_runner.py`)
   — removed the stale `+1` that was written against 0-based
   `rec.pos` semantics; pysam ≥ 0.22 already returns 1-based.
5. **Driver pre-fix-failure check** (`compares/scripts/bug_bench_driver.py`)
   — before scoring a cell as `detected=True`, re-runs the picked
   trigger against the already-installed pre-fix SUT. If pre-fix
   parses cleanly, demotes `detected → False` with a note. The old
   implementation only checked `signal(I, V_post) = false`, which
   let 15 of 17 v2 "confirmed" cells through as vacuously silenced.
6. **Driver `UnboundLocalError` fix** — removed a shadowing local
   `import subprocess` in the noodles branch of
   `_replay_trigger_silenced` that broke every vcfpy replay.
7. **Driver noodles replay CLI** — pass `fmt.upper()` as argv[1]
   (the harness signature is `noodles_harness <FORMAT> <path>`).

## Oracle-consensus validation before rerun

Running `scripts/validate_oracle_on_correct_vcfs.py` and
`scripts/validate_oracle_on_correct_sams.py` on the repo's seed
corpora:

| Format | Correct seeds | Consensus ≥ 2 voters | Oracle-blind (all disagree) |
|:--|:-:|:-:|:-:|
| VCF | 47 | **46 (98 %)** — only 1 file where most voters crash | **0** |
| SAM | 72 | **58 (81 %)** — the 14 with no-consensus are single-voter cases where most crash | **0** |

Before the fix-pack this was **VCF 1 / 47 (2 %)** and **SAM 39 / 72
(54 %)** with 14 / 72 oracle-blind on SAM.

## Per-cell V4 detail

### htsjdk — 9 bugs, 0 confirmed (all correctly demoted)

All 9 cells show `detected=False` with note *"pre_fix SUT parses
the picked trigger cleanly — detection demoted to False (no
pre-fix signal to silence); likely cross-voter canonical-JSON
variance."* Crash counts range from 344 – 769 (BioTest generated
lots of bug reports), but every picked trigger parses cleanly on
the pre-fix htsjdk jar → not a real detection per §5.3.1.

### vcfpy — 7 bugs, 2 confirmed, 4 unconfirmed, 1 null

| bug_id | anchor | det | conf | meaning |
|:--|:--|:-:|:-:|:--|
| **vcfpy-171** | 0.13.8 → 0.14.0 | ✓ | ✓ | **real detection** |
| **vcfpy-176** | 0.13.8 → 0.14.0 | ✓ | ✓ | **real detection** |
| vcfpy-127 | 0.11.0 → 0.11.1 | ✓ | ✗ | trigger fails both pre- and post-fix (spec-ambiguous; not the target bug) |
| vcfpy-145 | 0.13.4 → 0.13.5 | ✓ | ✗ | same |
| vcfpy-146 | 0.13.3 → 0.13.4 | ✓ | ✗ | same |
| vcfpy-gtone-0.13 | 0.12.1 → 0.12.2 | ✓ | ✗ | same |
| vcfpy-nocall-0.8 | 0.8.1 → 0.9.0 | ✓ | — | post_fix=0.9.0 install fails (pip sdist build error) → replay impossible |

The 4 `conf=False` cells are under DESIGN.md §5.3.1's
`null_silences` category: BioTest's first-picked trigger hits a
real vcfpy parse bug that *every* 0.x release also rejects
— not the specific bug the manifest anchors on. Fixing this
requires either (a) iterating all triggers until one silences on
post-fix (Magma §III.B), or (b) PoV-seed ordering in Phase C so
the first harvested trigger IS the targeted PoV.

### noodles — 9 bugs, 0 confirmed, 6 demoted, 3 install-fail

Same demotion pattern as htsjdk for the 6 that built: pre-fix
noodles parses the picked trigger cleanly, detection demoted. 3
cells (noodles-223/224 at 0.48, noodles-ob1-0.23 at 0.23) fail
`cargo build --release` against the harness's current API
dependencies — documented as environmental gaps in
`biotest_bugbench_summary.md`.

## Retraction status

`biotest_bugbench_summary.md` already carries a retraction notice
pointing at this file. The old headline ("24 / 35 confirmed,
69 %") was a measurement artifact of a broken oracle; the
corrected number across the full 35-bug manifest matches the audit
at **2 real detections** (both in vcfpy; both pre-fix-fail +
post-fix-silence).

## Next

- SAM phase rerun: launch after VCF phase. Preconditions: SAM MR
  registry populated (mine via `--phase B` with
  `format_filter=SAM`), config flipped. Expected outcome: driver
  will correctly demote every currently-"confirmed" cell that
  hasn't genuinely triggered the target bug.
- Longer per-cell budget (7200 s per DESIGN.md §5.5) would let the
  trigger-iteration path find more of the target vcfpy bugs in the
  4 spec-ambiguous cells. Cost: ~70 wall-hours total for the full
  SAM + VCF matrix.

## Reproduce

```bash
# Validate oracle on correct inputs (should show ≥ 80 % consensus).
py -3.12 scripts/validate_oracle_on_correct_vcfs.py --primary reference --strict
py -3.12 scripts/validate_oracle_on_correct_sams.py --primary htsjdk --strict

# Rebuild Java harness with the getDisplayString fix.
bash harnesses/java/build.sh

# Clear stale .pyc so the driver picks up the import-subprocess fix.
find compares/scripts -name __pycache__ -type d | xargs rm -rf

# Run the VCF phase of the bug_bench inside the bench image.
docker run --rm --name biotest-bugbench-vcf \
  -v "$(pwd):/work" -w /work biotest-bench:latest \
  bash scripts/run_bugbench_biotest_vcf_docker.sh
```
