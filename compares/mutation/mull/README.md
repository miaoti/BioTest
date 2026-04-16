# mull — C++ mutation testing for seqan3

mull is an LLVM-IR-based mutation testing tool for C/C++. Used here to score test suites against **seqan3** (SAM I/O code only).

## Version

`mull-llvm-18` (0.18+). Matches the Clang version used to build the seqan3 harness.

## Scope restriction

Per `DESIGN.md` §3.3:

```
mull-runner --ir-tests-filter='<path-glob>' seqan3/io/sam_file/**
```

Only the seqan3 SAM I/O headers and their direct dependencies are mutated. seqan3 is header-only, so "mutating a file" means recompiling the test harness with a perturbed header and checking test outcome flip.

## Build requirement

seqan3 currently builds a release binary (`biotest_harness.exe`). For mutation, we need:

1. A **separate debug build** with `-g -O0 -fembed-bitcode -fexperimental-new-pass-manager` so mull can inject mutations at IR level.
2. A runnable test driver that executes the generated test suite (i.e., feeds each test VCF/SAM file through the mutated harness and compares output to the unmutated baseline).

The debug build artifact will live at `harnesses/cpp/build-mull/biotest_harness_mull`. Not built yet.

## Invocation (planned)

```
mull-runner-18 \
  --ld-search-path /usr/lib/x86_64-linux-gnu \
  --reporters IDEReporter \
  --reporters SQLiteReporter \
  --ir-tests-path harnesses/cpp/build-mull/biotest_harness_mull \
  --workers 4
```

Output: SQLite database with one row per mutant (`killed` / `survived` / `not_covered`).

## Notes

- Windows support in mull is limited. We'll likely run the C++ mutation pass under **WSL2 / Ubuntu 22.04** for reliability. The rest of the comparison can stay on Windows.
- mull's "surviving mutant" list is a direct input to our "remaining mutation score gap" analysis — the specific spec rules those mutants correspond to are candidates for additional MR mining in a future iteration of BioTest.
- seqan3 is template-heavy; some mutants in header-only code may trigger compile errors rather than runtime test flips. mull reports those as "compile errors" — we exclude them from the denominator (they aren't testable mutants).
