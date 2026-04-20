# noodles_harness

Canonical-JSON harness that wraps [zaeleus/noodles](https://github.com/zaeleus/noodles)'
`noodles-vcf` crate, so BioTest can cross-execute a pure-Rust VCF parser
alongside htsjdk / pysam / biopython / htslib / vcfpy.

## Prerequisites

- Rust 1.78+ (install via [rustup](https://rustup.rs/); runs without
  admin on Windows — installs to `%USERPROFILE%\.cargo`).
- Optional for coverage: `cargo install cargo-llvm-cov`

## Build (standard binary)

```bash
cargo build --release --manifest-path harnesses/rust/noodles_harness/Cargo.toml
```

Produces: `harnesses/rust/noodles_harness/target/release/noodles_harness(.exe)`
— the path referenced by `phase_c.suts[name=noodles].adapter` in
`biotest_config.yaml`.

## Build (coverage-instrumented)

```bash
cargo llvm-cov --no-report \
    --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
    run -- VCF seeds/vcf/minimal_single.vcf
cargo llvm-cov report --json \
    --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
    > coverage_artifacts/noodles/llvm-cov.json
```

`NoodlesCoverageCollector` reads the JSON at
`coverage_artifacts/noodles/llvm-cov.json` and filters it to files under
the `noodles-vcf` crate (see `coverage.target_filters.VCF.noodles` in the
config). The framework calls `cargo llvm-cov report --json` automatically
if `.profraw` files exist under `coverage_artifacts/noodles/` but no
JSON report is found yet.

## Usage contract

```bash
noodles_harness VCF <input.vcf>      # prints canonical JSON; exit 0 / non-0
```

The canonical-JSON shape matches `test_engine/canonical/schema.py`
(`CanonicalVcf`). POS is emitted 1-based (noodles-vcf is 1-based
natively — no +1 shim).

## Graceful degradation

When the binary isn't built, `NoodlesRunner.is_available()` returns
False and Phase C silently skips this voter. Phase B's runtime-
capability resolver hides any noodles-specific MR from the LLM menu
under that condition, so nothing downstream breaks.
