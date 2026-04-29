# BioTest — Phase 4 Real-Bug Benchmark · VCF phase

Source-of-truth for every cell of
`compares/results/bug_bench/biotest/<bug_id>/result.json` covering the
VCF half of DESIGN.md §5 (`manifest.vcf_only.json` = 25 verified VCF
bugs: 9 htsjdk, 7 vcfpy, 9 noodles). Ran inside
`biotest-bench:latest` via
`scripts/run_bugbench_biotest_vcf_docker.sh`, 2026-04-21 → 2026-04-22.

Detection predicate per DESIGN.md §5.3.1:
> `detects(T, B) := ∃ I produced by T on V_pre such that signal(I, V_pre) = true AND signal(I, V_post) = false`

For BioTest, `signal = bug_report written` (metamorphic-relation
violation OR cross-voter canonical-JSON disagreement, per §5.3.1).

## Headline

| SUT | Bugs | **Confirmed detections** | Detected pre-fix | Install-failed | Unconfirmed (trigger also fails post-fix) |
|:--|:-:|:-:|:-:|:-:|:-:|
| htsjdk | 9 | **9 (100 %)** | 9 | 0 | 0 |
| vcfpy | 7 | **2 (29 %)** | 7 | 0 | 4 (+ 1 replay impossible) |
| noodles | 9 | **6 (67 %)** | 6 | 3 | 0 |
| **VCF total** | **25** | **17 (68 %)** | 22 | 3 | 4 |

*Per-bug budget: 300 s (§5.5 production budget is 7200 s × 1 rep; this
is a bounded demo-run, short budgets fall back to actual Phase C
execution above the adapter's 300 s `is_smoke` threshold).*

## Run configuration

- **Container**: `biotest-bench:latest` (Rust toolchain + vcfpy venv +
  Java 21 + cargo-llvm-cov pre-installed).
- **Config**: `primary_target=noodles`, `format_filter=VCF`,
  `max_iterations=2`. MR registry preserved from Run 12 (11 enforced +
  20 quarantined VCF MRs).
- **Manifest**: `compares/bug_bench/manifest.vcf_only.json` (filtered
  subset of the full 35-bug `manifest.verified.json`).
- **Driver**: `compares/scripts/bug_bench_driver.py --only-tool biotest --time-budget-s 300`.
- **Seed corpus**: `seeds/vcf/` (33 real-world + synthetic VCF files).
- **Wall time**: ~3h 10m across 25 anchor-grouped cells.

## Per-SUT breakdown

### htsjdk × VCF — **9 / 9 confirmed (100 %)**

| bug_id | anchor | crashes (bug reports written during 300 s) | confirmed? |
|:--|:--|:-:|:-:|
| htsjdk-1364 | 2.19.0 → 2.20.0 | 711 | ✓ |
| htsjdk-1372 | 2.19.0 → 2.20.0 | 626 | ✓ |
| htsjdk-1389 | 2.19.0 → 2.20.0 | 692 | ✓ |
| htsjdk-1401 | 2.19.0 → 2.20.0 | 631 | ✓ |
| htsjdk-1403 | 2.20.0 → 2.20.1 | 589 | ✓ |
| htsjdk-1418 | 2.20.1 → 2.21.0 | 563 | ✓ |
| htsjdk-1544 | 2.24.1 → 3.0.0 | 711 | ✓ |
| htsjdk-1554 | 2.24.1 → 3.0.0 | 658 | ✓ |
| htsjdk-1637 | 3.0.3 → 3.0.4 | 698 | ✓ |

Every htsjdk bug in the manifest had sufficient differential /
metamorphic signal under the 300 s budget, and for every one, the
first-picked trigger produced a silent parse on the post-fix jar.
This is the cleanest row — htsjdk's voter is instrumented, the jar
swap is fast (Maven Central fetch + symlink), and BioTest's 7-theme
MR suite covers the surface these bugs live on.

### vcfpy × VCF — **2 / 7 confirmed (29 %)**

| bug_id | anchor | crashes | confirmed? | reason |
|:--|:--|:-:|:-:|:--|
| vcfpy-171 | 0.13.8 → 0.14.0 | 412 | ✓ | |
| vcfpy-176 | 0.13.8 → 0.14.0 | 396 | ✓ | |
| vcfpy-127 | 0.11.0 → 0.11.1 | 603 | ✗ | trigger also fails on post-fix 0.11.1 |
| vcfpy-145 | 0.13.4 → 0.13.5 | 360 | ✗ | ditto 0.13.5 |
| vcfpy-146 | 0.13.3 → 0.13.4 | 370 | ✗ | ditto 0.13.4 |
| vcfpy-gtone-0.13 | 0.12.1 → 0.12.2 | 512 | ✗ | ditto 0.12.2 |
| vcfpy-nocall-0.8 | 0.8.1 → 0.9.0 | 531 | ? | post_fix vcfpy==0.9.0 pip-install failed (sdist build error against modern setuptools) — cell listed as `null_silences` for manual triage per §5.3.1 |

**Honest reading**: BioTest detected *something* in all 7 vcfpy cells
(every cell had 300-600 bug_reports). But for 5 of them, the
arbitrarily-picked first trigger was a spec-ambiguous input (every
VCF implementation, including the post-fix version, rejects or
canonical-JSON-disagrees on it). These 5 are NOT the specific bugs
the manifest anchors on — they are independent cross-voter
variations the tolerant consensus oracle is expected to filter, but
which leak through at the trigger-harvesting step.

Fixing this requires either (a) iterating *every* trigger until one
satisfies the differential predicate (Magma §III.B), or (b) linking
each bug's canonical trigger — in `compares/bug_bench/triggers/vcfpy-*/`
— into the seed corpus for that cell so BioTest's first-picked
crash IS the targeted trigger. Option (b) is the §5.3 per-sut PoV
injection path; the driver already runs `_build_merged_seed_corpus`
per-cell — worth reviewing whether the expected PoV is actually
making it into the corpus before scoring too harshly here.

**vcfpy-171, vcfpy-176 both landed at anchor 0.13.8 → 0.14.0** and
both confirmed — evidence that when the post-fix really does silence
the trigger, BioTest's first-pick heuristic works.

### noodles × VCF — **6 / 9 confirmed (67 %)**

| bug_id | anchor | crashes | confirmed? | reason |
|:--|:--|:-:|:-:|:--|
| noodles-241 | 0.58 → 0.59 | 661 | ✓ | |
| noodles-259 | 0.55 → 0.56 | 658 | ✓ | |
| noodles-268 | 0.57 → 0.58 | 682 | ✓ | |
| noodles-300 | 0.63 → 0.64 | 378 | ✓ | |
| noodles-339 | 0.81 → 0.82 | 573 | ✓ | |
| noodles-inforay-0.64 | 0.63 → 0.64 | 490 | ✓ | |
| noodles-223 | 0.48 → 0.49 | — | **install-failed** | `cargo build --release` on harness with noodles-vcf=0.48 pinned exited 101 (API drift: 0.48 pre-dates harness's current trait usage) |
| noodles-224 | 0.48 → 0.49 | — | **install-failed** | same anchor group as 223 |
| noodles-ob1-0.23 | 0.23 → 0.24 | — | **install-failed** | same, 0.23 pre-fix doesn't build |

**Why 6 / 6 of the ones that built succeeded**: BioTest's harness
preserves the per-version pinned Cargo.toml rewrite correctly, so
the pre-fix noodles voter is the exact buggy version. The
differential oracle catches the trigger, the driver then installs
post-fix, rebuilds the harness, and the replay is against the
silenced version. Post-processing was required to fix two driver
bugs that initially hid these confirmations — see "Bugs patched
mid-run" below.

**Why 3 / 9 install-failed**: noodles-vcf versions older than ~0.50
use APIs the current canonical-JSON harness
(`harnesses/rust/noodles_harness/src/main.rs`) no longer calls
compatibly. Either the harness needs per-version `cfg` gates, or
these bugs need a version-bumped harness template. Out of scope
for this bounded demo — documented as a known bench-coverage gap.

## Bugs patched mid-run

Two defects in the adapter and the driver were discovered while
watching the first cells land. Both are pre-existing (not introduced
for this run) and were invisible until the first real BioTest
bug-bench invocation.

1. **`run_biotest.py::count_files` under-counted by copying bug_report
   dirs not files.** `_base.count_files` returns
   `sum(p.is_file() for p in dir.iterdir())`, but BioTest's
   `bug_reports/<id>/` entries are directories (each bundles the
   seed + canonical outputs + evidence.md). Every cell reported
   `crash_count=0` → `detected=false`. Fix: harvest the transformed
   seed (`T_*.vcf`) directly into `crashes/` as a parseable file and
   move the full bundle to `evidence/`. Commit in
   `compares/scripts/tool_adapters/run_biotest.py`.

2. **`bug_bench_driver.py::_replay_trigger_silenced` had an
   `UnboundLocalError` on vcfpy cells.** The `noodles` branch had a
   local `import subprocess` that shadowed the module-level
   `subprocess` into a function-local across the whole function —
   so the vcfpy branch's `subprocess.run(...)` read an uninitialized
   local and raised. Every vcfpy cell got `confirmed=None`. Fix:
   removed the shadowing local import.

3. **noodles replay CLI argument drop.** `_replay_trigger_silenced`
   invoked `noodles_harness <trig>` but the harness CLI contract is
   `noodles_harness <FMT> <trig>` — the binary always errored out
   and every noodles replay looked like "post-fix still crashes".
   Fix: prepend `fmt.upper()` as argv[1].

All three fixes applied. Cells originally run with the bugs were
post-processed by
`compares/scripts/postprocess_bug_bench_replay.py` which re-installs
each cell's post-fix SUT and replays the first trigger with the
corrected logic. Original `result.json` preserved under
`result.json.pre_postprocess`.

## Aggregate

`compares/results/bug_bench/aggregate.json` regenerated after
postprocess. 25 records. Cells needing manual review (listed under
DESIGN.md §5.3.1 `null_silences`):
- `vcfpy-nocall-0.8` — post_fix=0.9.0 pip install fails; bench harness
  needs a fallback to git-checkout-of-tag here.
- `noodles-223`, `noodles-224`, `noodles-ob1-0.23` — pre_fix cargo
  build fails; harness needs per-version conditional compilation
  or a version-range floor in the manifest.

## Reproducing the VCF run

```bash
# 1. Ensure VCF MR registry is populated (Run 12 state is fine):
#    data/mr_registry.json has 11 enforced + 20 quarantined VCF MRs.

# 2. Launch inside Docker
docker run --rm --name biotest-bugbench-vcf \
    -v "$(pwd):/work" -w /work \
    biotest-bench:latest \
    bash scripts/run_bugbench_biotest_vcf_docker.sh

# 3. Post-process (re-replay cells that hit either of the patched
#    driver bugs; no-op for cells already confirmed=True):
docker run --rm -v "$(pwd):/work" -w /work biotest-bench:latest \
    bash -c 'export PATH=/root/.cargo/bin:$PATH &&
             python3.12 compares/scripts/postprocess_bug_bench_replay.py \
                 --manifest compares/bug_bench/manifest.vcf_only.json \
                 --results-dir compares/results/bug_bench/biotest \
                 --only-sut vcfpy noodles'

# 4. Aggregate + summary
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

1. **SAM phase**: flip `format_filter: SAM` + mine SAM MRs via a short
   Phase B, then re-run `bug_bench_driver.py` against the 10 SAM bugs
   (3 htsjdk, 1 biopython, 6 seqan3). See
   `coverage_notes/phase4/biotest_bugbench_sam.md` when landed.
2. **Fix the trigger-picker** so vcfpy's 4 unconfirmed cells get a
   real chance (iterate triggers, not first-lexicographic).
3. **Harness version gates** so noodles pre-0.50 anchors build,
   closing the 3 install-failed cells.
