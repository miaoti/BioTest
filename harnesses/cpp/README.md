# seqan3 Harness — Coverage Limitations

## Current state

`biotest_harness.cpp` is a **pure C++ text parser for SAM** — it does **not** link or call into seqan3. It was kept this way to sidestep two platform issues on the Windows dev box:

1. **seqan3 requires C++23.** GCC 15.2 (MinGW/MSYS2 UCRT64) supports it, but the toolchain must be told explicitly (`-std=c++23`).
2. **seqan3's BAM format struct packs to 36 bytes on Linux x86_64 ABI, but 40 bytes on MinGW.** A `static_assert` in `seqan3/io/sam_file/format_bam.hpp:160` fires immediately:

   ```
   static assertion failed: the comparison reduces to '(40 == 36)'
   ```

Consequence: any attempt to `#include <seqan3/io/sam_file/input.hpp>` on this Windows setup fails at compile time. The current harness deliberately avoids the include.

## What this means for coverage

Because the harness never executes seqan3 code, compiling it with `-fprofile-arcs -ftest-coverage` would produce `.gcda` files only for the harness's own ~250 lines — not for seqan3 itself. That metric would be meaningless.

The runtime collector in `test_engine/feedback/coverage_collector.py` therefore reports seqan3 as `available=False` when it can't find gcovr output, and the Phase D report shows "not collected" rather than fabricating a misleading number.

## Two paths forward (when seqan3 coverage is actually needed)

### Option A — WSL2 / Linux build (recommended)

1. In WSL2, install `gcovr`, `g++` ≥ 13, and clone seqan3 to `SUTfolder/cpp/seqan3/`.
2. Rewrite `biotest_harness.cpp` to use `seqan3::sam_file_input` for parsing (see `SUTfolder/cpp/seqan3/include/seqan3/io/sam_file/input.hpp` for API). The existing canonical-JSON output format stays the same.
3. Build:

   ```
   g++ -std=c++23 -O0 -g -fprofile-arcs -ftest-coverage \
       -I SUTfolder/cpp/seqan3/include \
       harnesses/cpp/biotest_harness.cpp \
       -lpthread \
       -o harnesses/cpp/build/biotest_harness_cov
   ```

4. Run seqan3 tests from WSL; `.gcda` files land next to the binary; `gcovr --json` parses them.
5. The config path `coverage_binary: harnesses/cpp/build/biotest_harness_cov.exe` would need a Linux variant without the `.exe`.

### Option B — Accept harness-level coverage only

Rewrite the harness to at least *instantiate* seqan3's parser even if we keep the current text-scanning logic side-by-side. This would trace seqan3's header-decoder and record-constructor templates but not its full state machine. Marginal value; not recommended unless WSL2 is unavailable.

## Task-list reality

C4 (original plan: "rebuild with coverage flags") is **not actionable on the current Windows toolchain** without addressing either the ABI mismatch (Option A) or rewriting the harness (Option B). The coverage plumbing (`gcovr_report_path` → `GcovrCollector` → Phase D SCC) is already in place on the Python side and will light up automatically once a real seqan3 build produces `.gcda` artifacts.

## References

- seqan3 C++23 requirement: `SUTfolder/cpp/seqan3/include/seqan3/core/platform.hpp:91`
- BAM ABI `static_assert`: `SUTfolder/cpp/seqan3/include/seqan3/io/sam_file/format_bam.hpp:160`
- Windows compile attempt: `g++ -std=c++23 -I .../seqan3/include ... -o smoke.exe` fails at the format_bam assertion.

---

## Rank 5 — query-method MR scaffolding (template only)

C++ has no portable runtime reflection. Scaffolding lives at framework
level under `harnesses/_reflect/`:

```bash
# 1. Generate a methods manifest from the SUT's public header.
py -3.12 -m harnesses._reflect.libclang_walker \
    --header /path/to/seqan3/io/sam_file/record.hpp \
    --type seqan3::sam_record \
    --sut-name seqan3 \
    --language cpp \
    --out manifest.json \
    -- -I /path/to/seqan3/include -std=c++23

# 2. Hand-port the manifest entries into a CMake-compiled adapter
#    (`biotest_harness_query.cpp` — same CLI grammar as the C harness:
#    `--mode discover_methods <FMT>` and `--mode query <FMT> <PATH>
#    --methods n1,n2`).

# 3. Add the adapter as a CMake target alongside biotest_harness:
#       add_executable(biotest_harness_query biotest_harness_query.cpp)
#       target_link_libraries(biotest_harness_query PRIVATE seqan3::seqan3)

# 4. Flip seqan3_runner.py's `supports_query_methods = True` once the
#    binary is on disk. The runner tests if the binary exists at
#    runtime and gracefully opts out otherwise.
```

### Limitations (libclang AST walk)

- **Templates / overloads / SFINAE-gated methods** are skipped — the
  walker only admits concrete, non-templated, public, `const`,
  zero-arg member functions. seqan3 is *very* template-heavy, so
  the discovered method list will be small in practice.
- **Macros** (`#define X 1`) and headers behind conditional compilation
  hide methods from the AST walker.
- **ABI stability**: the harness pins seqan3 to a specific commit so
  struct layouts don't drift mid-run.

### Reference citations for the Rank 5 lever

- Chen, T. Y., Kuo, F.-C., Liu, H., Tse, T. H. (2018). "Metamorphic
  Testing: A Review of Challenges and Opportunities." *ACM Computing
  Surveys* 51(1):4 §3.2 — API metamorphic relations.
- Xu, C., Terragni, V., Zhu, H., Wu, J., Cheung, S.-C. (2024).
  "MR-Scout: Mining Metamorphic Relations from Existing Test Cases."
  *ACM TOSEM* 33(6), arXiv:2304.07548. Reports +13.5 pp line coverage
  from query-method MRs across 701 OSS projects.
