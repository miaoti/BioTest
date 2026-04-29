# BioTest — Phase 4 Real-Bug Benchmark · SAM phase

Source-of-truth for every cell of
`compares/results/bug_bench/biotest/<bug_id>/result.json` covering the
SAM half of DESIGN.md §5 (`manifest.sam_only.json` = 10 verified SAM
bugs: 3 htsjdk/SAM + 1 biopython + 6 seqan3). Ran inside
`biotest-bench:latest` via
`scripts/run_bugbench_biotest_sam_docker.sh`, 2026-04-22.

Detection predicate per DESIGN.md §5.3.1 — same as the VCF phase (see
`biotest_bugbench_vcf.md`).

## Headline

| SUT | Bugs | **Confirmed detections** | Detected pre-fix | Install-failed | Adapter-raise (rescued) |
|:--|:-:|:-:|:-:|:-:|:-:|
| htsjdk/SAM | 3 | **3 (100 %)** | 3 | 0 | 0 |
| biopython | 1 | **1 (100 %)** | 1 | 0 | 0 |
| seqan3 | 6 | **3 (50 %)** | 3 | 3 | 1 |
| **SAM total** | **10** | **7 (70 %)** | 7 | 3 | 1 |

*Per-bug budget: 300 s. Scored on the 7 cells where pre_fix install
succeeded: **100 % detection rate** (7/7).*

## Run configuration

- **Container**: `biotest-bench:latest` (Rust + Java + seqan3 source +
  vcfpy venv + biopython venv pre-installed).
- **Precondition (new vs. VCF phase)**: the SAM MR registry had to be
  mined first. The driver script (`run_bugbench_biotest_sam_docker.sh`)
  flipped `format_filter: VCF → SAM`, cleared `mr_registry.json`, and
  ran Phase B before bug_bench started.
  - Phase B wall: **9 m 8 s**
  - Mined **24 SAM MRs** across the 7 themes
    (ordering=5, semantics_permutation=3, normalization=5, rejection=3,
    coordinate_indexing=2, round_trip=3, api_query=3).
  - Config restored to `format_filter: VCF` + VCF registry snapshot at
    the end of the run so VCF follow-ups aren't surprised.
- **Manifest**: `compares/bug_bench/manifest.sam_only.json` (filtered
  subset of the full 35-bug `manifest.verified.json`).
- **Driver**: `bug_bench_driver.py --only-tool biotest --time-budget-s 300`.
- **Seed corpus**: `seeds/sam/` (67 seeds: 37 curated + 30 Jazzer-
  sampled from Run 11).
- **Wall time**: ~1 h 45 m across 10 anchor-grouped cells (install
  swaps dominate — each seqan3 cell rebuilds the libfuzzer harness
  against a different commit).

## Per-SUT breakdown

### htsjdk × SAM — **3 / 3 confirmed (100 %)**

| bug_id | anchor | crashes | confirmed? |
|:--|:--|:-:|:-:|
| htsjdk-1489 | 2.22.0 → 2.23.0 | 1 132 | ✓ |
| htsjdk-1538 | 2.24.0 → 2.24.1 | 1 148 | ✓ |
| htsjdk-1561 | 2.24.1 → 3.0.0 | 1 114 | ✓ |

Every htsjdk/SAM bug was detected and silence-confirmed within 300 s
— same clean-row pattern as htsjdk/VCF. ~1 100 bug reports per cell
reflects SAM's higher DET rate (6-voter pool; more cross-voter
variance on real-world seeds) compared to the ~650 reports/cell on
VCF.

### biopython × SAM — **1 / 1 confirmed (100 %)**

| bug_id | anchor | crashes | confirmed? |
|:--|:--|:-:|:-:|
| biopython-4825 | 1.85 → 1.86 | 1 132 | ✓ |

Single-cell row; BioTest found signal, post-fix silenced it. Only one
biopython bug is in the manifest so this doesn't establish a strong
pattern by itself, but combined with the Phase-2 coverage numbers
(BioTest lands at 50–55 % on biopython; `coverage_notes/biopython/`)
the signal-finding competence here is expected.

### seqan3 × SAM — **3 / 6 confirmed, 3 install-failed**

| bug_id | anchor (short) | crashes | confirmed? | reason |
|:--|:--|:-:|:-:|:--|
| seqan3-2418 | df9fd5ff → 8e374d7c | 1 123 | ✓ | |
| seqan3-3081 | fa221c13 → c84f5671 | 1 114 | ✓ | |
| seqan3-3269 | ca4d6683 → 11564cb3 | 528 | ✓ | rescued — see "adapter raise" below |
| seqan3-2869 | edbfa956f^ → edbfa956f | — | install-fail | pre-fix `git checkout edbfa956f^` returned non-zero (the `^` parent suffix isn't resolvable on the detached cloned source) |
| seqan3-3098 | 4961904f → 4fe54891 | — | install-fail | pre-fix commit 4961904f checkout failed (not reachable from current fetch depth on the cloned seqan3 mirror) |
| seqan3-3406 | 745c645f → 5e5c05a4 | — | install-fail | same class of git-checkout-128 |

**Rescue — seqan3-3269 (adapter raise)**: the adapter's harvest loop
caught **`OSError: [Errno 12] Cannot allocate memory: '/work/bug_reports/BUG-20260422_070732_600807_529'`**
mid-copy. That's the Windows-Docker 9p-mount ENOMEM pathology
already recorded in `memory/9p_enomem_concurrent_chats.md`. The
adapter raised (exit=99, stub record written), but 528 transformed
seeds had already been harvested into `crashes/`. Post-processed via
`compares/scripts/rescue_adapter_raise_cells.py` which:

1. re-derives `detected=True` from the on-disk count (528 > 0),
2. installs the post-fix seqan3 commit,
3. replays the first trigger via `SeqAn3Runner`,
4. writes a corrected `result.json` (original preserved under
   `result.json.pre_rescue`).

Outcome: `confirmed=True`. The bug would have registered correctly
absent the 9p fault — and on a Linux host (production bench regime
per DESIGN §13), 9p is not in the path at all.

**Install-failure root cause for seqan3-2869 / 3098 / 3406**: the
cloned `compares/baselines/seqan3/source/` tree was created with a
bounded fetch depth. Three of the six anchors reference commits
older than that depth or use the `^` parent-of-commit shortcut that
requires both commits to be reachable. Follow-up: re-clone with
`--depth 1000` or `--unshallow`, or pin the manifest anchors to
commits inside the current fetch horizon.

## Known driver bug inherited from VCF phase

The VCF-phase-discovered bugs in `_replay_trigger_silenced` + the
BioTest adapter (`run_biotest.py`) were patched *before* the SAM
launch, so every SAM cell got the correct flow end-to-end. No SAM
cell required post-processing via `postprocess_bug_bench_replay.py`.
The only intervention needed was the 9p-ENOMEM rescue above.

## Reproducing the SAM run

```bash
# 1. Launch inside Docker (flips config, mines SAM MRs, runs bench,
#    restores config):
docker run --rm --name biotest-bugbench-sam \
    -v "$(pwd):/work" -w /work \
    biotest-bench:latest \
    bash scripts/run_bugbench_biotest_sam_docker.sh

# 2. Post-process 9p-ENOMEM rescue if applicable:
docker run --rm -v "$(pwd):/work" -w /work biotest-bench:latest \
    bash -c 'export PATH=/root/.cargo/bin:$PATH &&
             python3.12 compares/scripts/rescue_adapter_raise_cells.py \
                 --manifest compares/bug_bench/manifest.verified.json \
                 --results-dir compares/results/bug_bench/biotest'

# 3. Rebuild combined aggregate (VCF + SAM):
py -3.12 -c "
import json
from pathlib import Path
agg=[json.loads((c/'result.json').read_text('utf-8'))
     for c in sorted(Path('compares/results/bug_bench/biotest').iterdir())
     if (c/'result.json').exists()]
Path('compares/results/bug_bench/aggregate.json').write_text(
    json.dumps({'results':agg}, indent=2), encoding='utf-8')
"
```

## Next steps

1. **Fix the seqan3 source-clone depth** so the 3 install-failed
   cells become scorable. `git -C compares/baselines/seqan3/source
   fetch --unshallow` inside the image.
2. **Production-budget rerun** (§5.5): 7200 s × 1 rep. Expected to
   keep 100 % on the 7 scored cells and possibly pull cross-voter
   bugs out of deeper seeds.
