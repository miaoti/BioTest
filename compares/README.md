# compares/ — Comparative Evaluation

Design and (eventually) execution artefacts for benchmarking **BioTest**
against fair end-to-end, input-level test-generation baselines on the
four SUTs (`htsjdk`, `pysam`, `biopython`, `seqan3`), plus a real-bug
detection benchmark drawn from historical GitHub issues.

**Nothing here executes yet.** The structure and methodology are locked
*before* the main BioTest Phase A–D evaluation finishes so the protocol
is fixed at run time.

See [`DESIGN.md`](./DESIGN.md) for the full specification and
[`bug_bench/README.md`](./bug_bench/README.md) for the bug-benchmark
authoring / execution guide.

## Slim matrix (13 primary cells + 1 anchor)

| SUT            | BioTest | Jazzer | Atheris | libFuzzer | Pure Random | EvoSuite (anchor) |
| :---           | :---:   | :---:  | :---:   | :---:     | :---:       | :---:             |
| htsjdk         | P       | P      | —       | —         | P           | A                 |
| pysam          | P       | —      | P       | —         | P           | —                 |
| biopython (SAM) | P      | —      | P       | —         | P           | —                 |
| seqan3 (SAM)   | P       | —      | —       | P         | P           | —                 |

P = primary (2h × 3 reps + 2h × 1 bug-bench). A = white-box anchor
(labelled "different paradigm — unit-level" throughout the report).

## Metrics

1. **Validity Ratio** — `parse_OK / generated_total`.
2. **Coverage Growth** — branch + line coverage vs. log wall time.
3. **Mutation Score** — `killed / reachable` via PIT / mutmut / mull.
4. **Real-Bug Detection Rate** *(new)* — fraction of 32-candidate
   benchmark bugs (see `bug_bench/`) detected by each tool.
5. **Time-to-First-Bug (TTFB)** *(new)* — median wall-clock seconds
   per bug per tool.

## Layout

- `baselines/` — EvoSuite + Jazzer JARs, Atheris pip install, libFuzzer
  via Clang, pure-random generator. Source subfolders gitignored.
- `bug_bench/` — real-bug benchmark manifest + triggers.
- `harnesses/` — fuzzer harnesses (Jazzer Java, Atheris Python, libFuzzer C++).
- `mutation/` — PIT / mutmut / mull scope notes.
- `scripts/` — fetch, build, probe, driver, report scripts + per-tool
  uniform adapters under `scripts/tool_adapters/`.
- `results/` — populated at run time, gitignored.

The `source/` subfolders under `baselines/` and everything under
`results/` are gitignored — we pull upstream release artefacts on demand
and don't vendor them into this repo.

## Baselines, rationale in one line each

- **BioTest** — tool under evaluation.
- **Jazzer** — fair E2E baseline for Java (htsjdk). In-process,
  coverage-guided, OSS-Fuzz-integrated.
- **Atheris** — fair E2E baseline for Python (pysam, biopython).
  libFuzzer-style, supports C extensions.
- **libFuzzer** — fair E2E baseline for C++ (seqan3). Gold standard.
- **Pure Random** — floor baseline; byte-level `os.urandom`.
- **EvoSuite** — *white-box anchor only* on htsjdk; preserves the
  "semantic metamorphic vs. white-box unit-level" comparison claim with
  actual numbers rather than hand-wave.

Other fuzzers (JQF+Zest, AFL++, Nautilus, Fuzz4All, Randoop) are
documented in DESIGN.md §2.3 as optional secondary baselines — run only
if time permits after the primary matrix.
