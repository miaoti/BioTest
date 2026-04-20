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

# Include noodles-vcf (an external crate) explicitly — by default
# cargo-llvm-cov's report step shows only workspace packages. The
# --package flags below pull noodles-vcf + harness into the JSON.
cargo llvm-cov report --json \
    --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
    --package noodles-vcf --package noodles_harness \
    > coverage_artifacts/noodles/llvm-cov.json
```

## Usage contract

```bash
# Parse mode (default) — prints canonical JSON:
noodles_harness VCF <input.vcf>

# Write-roundtrip mode — re-serializes via noodles-vcf's Writer:
noodles_harness --mode write_roundtrip VCF <input.vcf> <output.vcf>
```

`NoodlesCoverageCollector` reads the JSON at
`coverage_artifacts/noodles/llvm-cov.json` and filters it to files under
the `noodles-vcf` crate (see `coverage.target_filters.VCF.noodles` in the
config). The framework calls `cargo llvm-cov report --json` automatically
if `.profraw` files exist under `coverage_artifacts/noodles/` but no
JSON report is found yet.

The canonical-JSON shape matches `test_engine/canonical/schema.py`
(`CanonicalVcf`). POS is emitted 1-based (noodles-vcf is 1-based
natively — no +1 shim). Capability parity with `BioTestHarness.java`
is covered in `SUTfolder/rust/noodles-vcf/README.md`.

## Graceful degradation

When the binary isn't built, `NoodlesRunner.is_available()` returns
False and Phase C silently skips this voter. Phase B's runtime-
capability resolver hides any noodles-specific MR from the LLM menu
under that condition, so nothing downstream breaks.
