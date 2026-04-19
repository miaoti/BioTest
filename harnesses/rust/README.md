# Rust Harness Template (Rank 5 — Query-Method MRs)

Scaffolding for onboarding a Rust-language SUT to BioTest's API-query
metamorphic testing path. Rust has no runtime reflection by design, so
the framework uses a code-generation pipeline based on `rustdoc`'s
JSON output.

> **Citations**:
> - Chen, Kuo, Liu, Tse (ACM CSUR 2018) §3.2 — API metamorphic relations.
> - MR-Scout (Xu et al., TOSEM 2024, arXiv:2304.07548) — query-method MR mining.
> - rustdoc-json RFC #2963: <https://rust-lang.github.io/rfcs/2963-rustdoc-json.html>
>   (nightly today, expected stable in 2026).

## Onboarding contract — what the framework requires from a Rust SUT

1. A Cargo crate that exposes a public `parse_*` function returning a
   parsed-record type (e.g. `Record`).
2. The parsed-record type has public methods of shape:
       fn name(&self) -> Scalar
   where `Scalar` is `bool`, `iN`, `uN`, `fN`, `String`, `&str`, or
   `Option<T>` where `T` is one of those.
3. A binary target (in this directory or in your crate) that:
     - parses an input file,
     - dispatches to the named methods for `--mode query`,
     - prints `{"method_results": {…}}` on stdout.

## Onboarding workflow (one-time per SUT)

```bash
# 1. Generate rustdoc JSON for your SUT crate (NIGHTLY today).
rustup toolchain install nightly
cd /path/to/your/sut/crate
cargo +nightly rustdoc -- -Zunstable-options --output-format json
# Output: target/doc/<crate_name>.json

# 2. Parse the rustdoc JSON into a uniform manifest.
py -3.12 -m harnesses._reflect.rustdoc_parser \
    --rustdoc-json target/doc/<crate_name>.json \
    --type Record \
    --sut-name my_rust_parser \
    --out manifest.json

# 3. Generate the dispatch adapter — see biotest_harness/src/main.rs
#    for the template. Each manifest entry maps to one match arm in
#    `dispatch_method`.

# 4. Build the harness binary.
cargo build --release \
    --manifest-path harnesses/rust/biotest_harness/Cargo.toml

# 5. Add a runner subclass mirroring c_template_runner.py — it just
#    subprocess-calls the binary and parses its JSON.

# 6. Add a coverage filter block to biotest_config.yaml under
#    coverage.target_filters.<FORMAT>.<sut_name>.
```

## Limitations

- **Nightly required (today)**: `rustdoc --output-format json` is
  unstable; pinned to 2025 nightlies. Once RFC #2963 stabilizes you
  can drop the `+nightly` requirement.
- **Generic methods**: `fn foo<T>(&self) -> T` cannot be dispatched
  without a concrete instantiation. Generate one wrapper per
  instantiation you care about, or skip generic methods.
- **Trait-default methods**: rustdoc emits both inherent and trait-impl
  methods. The parser admits inherent methods (the `impl Record`
  block) and rejects trait-impl methods (Debug, Clone, …).
- **`&mut self`**: rejected by design — query methods must be pure.
- **MSRV**: the harness crate targets Rust 2021 edition; MSRV 1.70+.

## Files

| File | Purpose |
|:-----|:--------|
| `README.md` | This file. |
| `biotest_harness/` | Cargo crate skeleton (Cargo.toml + src/main.rs). |
| `example_vcf_parser/` | (Optional) tiny toy Rust VCF parser proving the pipeline; not committed by default. |

## Testing

Once you've onboarded a SUT, run:

```bash
# Smoke-test the binary
target/release/biotest_harness --mode discover_methods VCF
target/release/biotest_harness --mode query VCF /path/to/seed.vcf \
    --methods is_structural,n_alleles
```

Then add the runner to `biotest_config.yaml::phase_c.suts` and run
`py -3.12 biotest.py --phase D`.
