# cargo-fuzz harness for noodles-vcf

Rust fair-E2E baseline for the noodles-vcf row of the comparative
matrix (DESIGN.md §4.1, §13.2.7). Added 2026-04-20 when pysam was
demoted and noodles-vcf became a primary VCF SUT.

## One-time build

```bash
cd compares/harnesses/cargo_fuzz
cargo fuzz build noodles_vcf_target --release
```

Produces
`compares/harnesses/cargo_fuzz/fuzz/target/x86_64-unknown-linux-gnu/release/noodles_vcf_target`
(~4 MB, libFuzzer-instrumented). The `bug_bench_driver.py` adapter
`run_cargo_fuzz.py` finds this binary automatically.

## Per-bug version swap (no manual step during bench)

`bug_bench_driver._install_noodles(<version>)` rewrites the
`noodles-vcf = "X.Y"` pin in both this harness's `fuzz/Cargo.toml`
and the primary `harnesses/rust/noodles_harness/Cargo.toml` before
each anchor group's pre-fix / post-fix swap. The incremental rebuild
is ~30 s after the first full build.

## Layout

```
compares/harnesses/cargo_fuzz/
├── README.md                          # this file
└── fuzz/
    ├── Cargo.toml                     # pins noodles-vcf version; driver rewrites
    └── fuzz_targets/
        └── noodles_vcf_target.rs      # fuzz target entry point
```

The `fuzz/` subdirectory structure is the cargo-fuzz default, so
`cargo fuzz build` finds everything without extra flags.
