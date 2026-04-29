# BioTest — noodles-vcf / VCF line coverage

Source-of-truth for every BioTest coverage measurement against the
**noodles-vcf** SUT (zaeleus/noodles, pure-Rust VCF parser). All numbers
honour the filter in
`biotest_config.yaml: coverage.target_filters.VCF.noodles`:

```
noodles-vcf/src/io/reader
noodles-vcf/src/io/writer
noodles-vcf/src/header
noodles-vcf/src/record
noodles-vcf/src/variant
noodles-vcf/src/lib.rs
```

The filter matches against the Cargo-normalized path (registry prefix +
`<crate>-<version>/` suffix stripped; see
`compares/scripts/measure_coverage.py::_normalize_cargo_path`). Total
denominator at noodles-vcf 0.57.0 (Linux ELF build from
`biotest-bench:latest`) is **6 920 lines** across the six subpaths.

Run-by-run snapshots under
`coverage_artifacts/noodles/llvm-cov_post_run{N}.json`.

---

## Timeline

| Run | Date | Wall | Iters | **Weighted VCF** | Covered / Total | Enforced MRs | Notes |
|:-:|:--|:-:|:-:|:-:|:-:|:-:|:--|
| **12** | **2026-04-21** | **64 m** | **2** (budget_exhausted) | **39.6 %** | **2 741 / 6 920** | **11 / 30** | First BioTest × noodles × VCF cell. `max_iter=2` bounded-budget run inside `biotest-bench:latest` (cargo-llvm-cov unavailable on Windows host). 105 seeds, 2 013 tests, 520 DETs. |

---

## Head-to-head against other tools (cargo-fuzz, Pure Random)

Both external baselines were measured by `compares/scripts/coverage_sampler.py`
with a broader filter — any file whose path contains the substring
`noodles-vcf` — so its denominator includes `async/`, `indexed_reader/`,
`fs/`, etc. that the BioTest filter excludes. To make the comparison
apples-to-apples, Run 12's `llvm-cov.json` was also regraded under
that broader scope via `scripts/measure_noodles_broad_scope.py`.

### 1. Under the cargo-fuzz / Phase-2-sampler scope (any path contains `noodles-vcf`)

| Tool | Wall (mean) | Reps | Scope files | **Line % (mean [95 % CI])** |
|:--|:-:|:-:|:-:|:-:|
| **BioTest Run 12** | 64 min | 1 | 168 | **38.94 %** (2 741 / 7 039) |
| cargo-fuzz | 30 min / rep | 3 | 168 † | 22.72 % [22.42, 23.01] |
| Pure Random | 2 h / rep | 3 | 168 † | 0.00 % [0.00, 0.00] |

**Δ BioTest − cargo-fuzz = +16.22 pp** at ~2× wall time (single rep).

† cargo-fuzz + Pure Random numbers lifted from
`compares/results/coverage/{cargo_fuzz,pure_random}/noodles/growth_aggregate.json`;
the file count is the same build's crate surface.

### 2. Under the BioTest filter (narrower: the 6 subpaths above)

| Bucket | Covered / Total | % |
|:--|:-:|:-:|
| `noodles-vcf/src/io/reader` | 128 / 937 | 13.7 % |
| `noodles-vcf/src/io/writer` | 803 / 925 | **86.8 %** |
| `noodles-vcf/src/header` | 1 209 / 2 999 | 40.3 % |
| `noodles-vcf/src/record` | 486 / 751 | 64.7 % |
| `noodles-vcf/src/variant` | 115 / 1 308 | 8.8 % |
| `noodles-vcf/src/lib.rs` | 0 / 0 | — |
| **OVERALL (weighted)** | **2 741 / 6 920** | **39.6 %** |

cargo-fuzz + Pure Random don't have a preserved raw JSON under this
narrower scope (only per-tick summaries survive), so we can't regrade
them here. The 22.72 % / 0.00 % numbers quoted above are the only
cross-tool points we have, and only at the broader scope.

---

## Run 12 detailed breakdown (2026-04-21)

First BioTest measurement against a Rust SUT. Launched in
`biotest-bench:latest` via
`scripts/run_biotest_noodles_docker.sh`:

```bash
docker run -d --name biotest-run12-noodles \
    -v "<repo>:/work" -w /work \
    biotest-bench:latest bash scripts/run_biotest_noodles_docker.sh
```

Config flip:
- `feedback_control.primary_target: vcfpy → noodles`
- `feedback_control.max_iterations: <unset> → 2` (override; VCF default is 4)
- All other defaults preserved (Rank 5 on by default; Rank 6 off;
  Tier-2 prompt enrichment off).

### Phase progression

| Phase | Status | Wall | Detail |
|:--|:-:|:-:|:--|
| A: Ingest | PASS | 0 ms | Spec index cached from prior run. |
| B: Mine MRs | PASS | 7 m 31 s | 6 enforced, 7 quarantine (13 mined). |
| C: Execute | PASS | 9 m 18 s | 2 013 tests, 520 bugs. |
| D: Feedback | PASS | 47 m 11 s | 2 iter, SCC 3.2 % → 4.4 %, stop: budget_exhausted. |
| **Total** | | **64 m** | |

### Phase-D iterations

| Iter | End SCC | Enforced MRs | Quarantined | Notes |
|:-:|:-:|:-:|:-:|:--|
| 1 | 3.2 % | 9 / 25 | 16 | +3 new MRs synthesised via Rank-6-equivalent blindspot feedback (auto). |
| 2 | 4.4 % | **11 / 30** | 19 | +1 more MR rescued. Stop on `iteration=2 >= 2` (budget_exhausted). |

### Test metrics

| Metric | Value |
|:--|:-:|
| Seeds used | 105 |
| Variants generated | 2 013 |
| Metamorphic failures | 535 |
| Differential failures | 297 |
| Crashes | 0 |
| DET rate | 41.3 % |
| Bug reports written | 520 |
| Runners (VCF voters) | htsjdk, vcfpy, pysam, reference, noodles |

### Honest reading

**Strengths (why BioTest beats cargo-fuzz by +16 pp):**

- **Writer path: 86.8 %.** BioTest's `sut_write_roundtrip` transform
  exercises the entire serialization path on every record mutation.
  cargo-fuzz has no writer oracle — it only fuzzes the parser, so any
  writer coverage is incidental and bounded by whatever parse outputs
  happen to feed back through `println!`. This is a paradigm-level
  advantage, not a knob we can tune.
- **Record + header: 64.7 % / 40.3 %.** Real-world seeds plus
  permutation / ordering MRs hit many structural shapes of the record
  surface. MRs like *ALT permutation with dependent field remapping*,
  *Trim Common Affixes*, *Split Multi-Allelic*, *BCF binary round-trip*
  drive these numbers.

**Remaining gaps (noodles-specific data-model bucket):**

- **`variant`: 8.8 %.** Same paradigm pattern we see on htsjdk/SAM:
  the data-model subtree is API-only, reachable by calling methods on
  parsed records, which `parse(x) → canonical_JSON` paths never do.
  The zero-user-cost lever for this bucket is Tier-2 Rank-5 (already
  on) + Rank-6 LLM-synth MRs (currently off). The same 25-pp-bucket
  gap documented in `coverage_notes/htsjdk/sam/biotest.md` Run 10
  writeup.
- **`io/reader`: 13.7 %.** Low, but the reader is one file
  (`src/io/reader.rs`) that sits behind noodles-vcf's async + sync +
  indexed + tabix sub-trees. Many branches are guarded by features
  BioTest doesn't use (async tokio, BGZF, tabix index lookups).
- **`lib.rs`: 0 / 0.** Empty — the crate's top-level `lib.rs` is
  pure re-exports with no instrumented lines.

**Why wall time (64 min) landed where it did:**

- Max iterations capped at 2; iteration 1 + 2 took 47 min of Phase D
  plus 9 min Phase C + 7 min Phase B mining = 63 min. Consistent with
  the SAM Run 11 pattern (`max_iter=2` for bounded budgets).
- Termination was `budget_exhausted` (iteration=2 >= 2), not
  coverage-plateau / timeout. Raising to `max_iter=4` would likely
  add +2-4 pp via the variant bucket at 2× wall time.

### Next levers (not applied)

1. **Raise `max_iterations` to 4** (the VCF default). Expected +2-4 pp
   mainly in `variant` + `header`. Wall time ~2 h.
2. **Flip `mr_synthesis.enabled: true`** (Rank 6). Would feed the
   uncovered `variant`-file class-gap ticket directly to the LLM; same
   lever that drove +3 pp on htsjdk/VCF Runs 7-8. Zero per-SUT code
   because the LLM consumes the runtime-discovered mutator catalog
   from `NoodlesRunner.discover_mutator_methods`.
3. **Regrade cargo-fuzz under the BioTest filter** for a proper
   apples-to-apples at the narrower scope. Requires re-running cargo-
   fuzz Phase 2 with profdata preserved (currently only summary JSON
   survives). Would also let us compare at branch-coverage level.

---

## Reproducing Run 12

Prereqs: `biotest-bench:latest` Docker image (has Rust toolchain +
cargo-llvm-cov + llvm-tools-preview baked in).

```bash
# 1. Flip config (already committed):
#    feedback_control.primary_target: noodles
#    feedback_control.max_iterations: 2 (override)
#    phase_c.format_filter: VCF

# 2. Launch
docker run --rm --name biotest-run-noodles \
    -v "$(pwd):/work" -w /work \
    biotest-bench:latest \
    bash scripts/run_biotest_noodles_docker.sh

# 3. If the in-script `cargo llvm-cov report` step failed (it did on
#    Run 12 — cargo-llvm-cov's default workspace scope doesn't include
#    external deps like noodles-vcf), regenerate the JSON via direct
#    llvm-cov export:
docker run --rm -v "$(pwd):/work" -w /work biotest-bench:latest bash -c '
    export PATH=/root/.cargo/bin:$PATH
    LLVM_BIN=$(rustc --print sysroot)/lib/rustlib/x86_64-unknown-linux-gnu/bin
    $LLVM_BIN/llvm-profdata merge -sparse \
        -o /tmp/noodles.profdata coverage_artifacts/noodles/*.profraw
    $LLVM_BIN/llvm-cov export -format=text \
        -instr-profile=/tmp/noodles.profdata \
        harnesses/rust/noodles_harness/target/llvm-cov-target/release/noodles_harness \
        > coverage_artifacts/noodles/llvm-cov.json'

# 4. Measure — BioTest filter (narrow, biotest_config.yaml scope):
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/noodles/llvm-cov.json \
    --sut noodles --format VCF --label "BioTest Run N"

# 5. Cross-tool (broader noodles-vcf substring):
py -3.12 scripts/measure_noodles_broad_scope.py
```

---

## Methodology note — why Run 12 needed direct `llvm-cov export`

`NoodlesCoverageCollector._ensure_report` calls
`cargo llvm-cov report --json --manifest-path <harness>/Cargo.toml`
without `--package` flags. On cargo-llvm-cov 0.8.5 that produces a
workspace-only report — external dependencies like `noodles-vcf` get
dropped. The `--package noodles-vcf` flag from the harness README
raises "not found package 'noodles-vcf' in workspace" because noodles-
vcf is a registry crate, not a workspace member.

The reliable path is the one `coverage_sampler.py::_llvm_cov_export_json`
already uses for cargo-fuzz: merge `.profraw` via `llvm-profdata merge`,
then `llvm-cov export -format=text -instr-profile=<profdata> <binary>`
against the release binary. That disassembles every instrumented source
file the binary touched, including transitive deps. Measurement then
runs through `measure_coverage.py` unchanged (it detects the
`data[*].files[*]` cargo-llvm-cov shape and normalizes Cargo registry
paths via `_normalize_cargo_path`).

The framework bug (NoodlesCoverageCollector generating an incomplete
report that measures 0.0 %) is documented as a follow-up — Phase D's
runtime coverage signal is therefore effectively blind on noodles
today. Run 12 ran to `max_iter=2` (budget_exhausted) rather than
plateau-stop because the feedback loop never saw real coverage
deltas; this doesn't affect the end-state measurement but does mean
Phase D couldn't adapt its blindspots to the actual noodles-vcf gap
shape. Fixing the collector is a separate ticket.
