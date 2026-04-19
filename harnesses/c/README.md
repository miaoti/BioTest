# C Harness Template (Rank 5 — Query-Method MRs)

This directory contains scaffolding for onboarding a new C-language SUT
to BioTest's API-query metamorphic testing path. C lacks runtime
reflection, so the framework uses a **code-generation pipeline**:
parse the SUT's public header with `libclang`, emit a uniform
`methods_manifest.json`, and link a generated dispatch adapter against
the SUT library at compile time.

> **Citation**: Chen, Kuo, Liu, Tse (ACM CSUR 2018) §3.2 — API
> metamorphic relations; MR-Scout (Xu et al., TOSEM 2024,
> arXiv:2304.07548) — query-method MR mining.

## Onboarding contract — what the framework requires from a C SUT

1. A **public header** (`.h`) declaring an opaque or transparent
   parsed-record `struct` plus public functions of shape:
       Scalar fn(const struct Record *r);
   where `Scalar` is `bool`, an integer type, `float/double`,
   `enum X`, or `const char *`.
2. A linkable shared library (`.so` / `.dll`) exporting those functions.
3. A **harness binary** that:
     - parses an input file into the SUT's record struct,
     - dispatches to the named query functions for `--mode query`,
     - prints `{"method_results": {…}}` on stdout.

If you ship those three things, the framework calls your harness via
the same `--mode query` / `--mode discover_methods` CLI it uses for
htsjdk and pysam — no per-SUT framework code needed.

## Onboarding workflow (one-time per SUT)

```bash
# 1. Discover the SUT's API surface from its public header.
py -3.12 -m harnesses._reflect.libclang_walker \
    --header /path/to/sut/include/parser.h \
    --type Record \
    --sut-name my_c_parser \
    --language c \
    --out manifest.json \
    -- -I/path/to/sut/include

# 2. Inspect manifest.json — it lists every public scalar getter
#    libclang found. Edit by hand if you want to drop methods.

# 3. (Hand-write or generate) the dispatch C source — see
#    biotest_harness.c for the template skeleton; fill in:
#       - parse_input(path)        → returns struct Record*
#       - dispatch_method(name, r) → switch over the manifest's names
#    The framework supplies the JSON I/O.

# 4. Compile the harness into a binary.
gcc -o biotest_harness biotest_harness.c -L/path/to/sut/lib -lparser

# 5. Add a runner subclass mirroring c_template_runner.py — it just
#    subprocess-calls your binary and parses its JSON output.

# 6. Add a coverage filter block to biotest_config.yaml under
#    coverage.target_filters.<FORMAT>.<sut_name> so the framework
#    knows which source paths count as "in scope" for your SUT.
```

## libclang limitations (documented; do not file as bugs)

- Macros (`#define X 1`), static-inline functions, and headers with
  conditional compilation that hide the parsed-record struct will not
  appear in the manifest. Move them to a regular function declaration
  in a separate compilation unit if you want them included.
- The walker only admits functions with EXACTLY one argument typed as
  `const struct StructName *` (or `struct StructName *`). Multi-arg
  helpers are skipped — they aren't pure query methods anyway.
- Struct layout / ABI must be stable across SUT versions. The harness
  pins a SUT version in its build script.

## Files in this directory

| File | Purpose |
|:-----|:--------|
| `README.md` | This file. |
| `biotest_harness.c` | Skeleton harness — fill in `parse_input` + `dispatch_method`. |
| `example_vcf_parser/` | (Optional) tiny toy C VCF parser proving the pipeline; not committed by default. |

## Reference implementation pattern

Look at `harnesses/java/BioTestHarness.java` (lines around `--mode query`
and `--mode discover_methods`) for the equivalent Java code path.
The C harness mirrors it: same CLI grammar, same JSON output shape.

## When to opt OUT

If your C SUT can't expose a clean public header (e.g., it's wrapped
behind a SWIG-generated Python module already), use that Python wrapper
as the SUT instead and rely on the Python introspection path
(`test_engine/runners/introspection.py`) — it covers C libraries
indirectly via their Python bindings.
