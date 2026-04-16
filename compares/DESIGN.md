# Comparative Evaluation Design — BioTest vs Baseline Test Generators

## 1. Purpose

This document specifies how BioTest will be benchmarked against established test-input-generation baselines on the four SUTs already in use (`htsjdk`, `biopython`, `seqan3`, `pysam`). The comparison is **deferred** — it runs only after the main BioTest evaluation is complete. This file exists now so the protocol, source-code locations, mutation tooling, and scoping decisions are recorded precisely and can be reviewed/adjusted before execution.

## 2. Tools Under Comparison

| Tool | Class | Language support | Role in this study |
| :--- | :--- | :--- | :--- |
| **BioTest** (this repo) | Spec-grounded metamorphic + differential fuzzing | Multi-lang via adapters | Tool under evaluation |
| **EvoSuite** | Search-based unit-test generation | Java only (JUnit) | Baseline |
| **Randoop** | Feedback-directed random unit-test generation | Java only (JUnit) | Baseline |
| **Pure Random** | Byte-level random file generation | Language-agnostic (input-as-file) | Floor baseline — we implement this in `baselines/random_testing/` |

### 2.1 Language-coverage caveat

EvoSuite and Randoop are **Java-only unit-test generators**; they cannot be pointed at biopython (Python), seqan3 (C++), or pysam (Python) directly. This asymmetry shapes the protocol:

- **Java axis (htsjdk)**: full 4-way comparison — BioTest vs EvoSuite vs Randoop vs Pure Random.
- **Python / C++ axes (biopython / seqan3 / pysam)**: 2-way comparison — BioTest vs Pure Random.
- Optionally, if time permits we add **Pynguin** (Python) and **libFuzzer** (C++) as per-language near-equivalents and list them as "secondary baselines."

The report will make the scope clear so the comparison is apples-to-apples per SUT.

## 3. Metrics

Three metrics, all reported per SUT per tool over a fixed time budget (default **300 s**, matching the growth-curve plot in the proposal). All three are plotted as growth curves at {0, 60, 120, 180, 240, 300} s sample points.

### 3.1 Validity Ratio (Compliant-Input Rate)

**Definition**: fraction of generated test inputs that the SUT's parser accepts as syntactically / structurally valid VCF or SAM files (no parse error, no crash on load).

**Why it matters**: pure random file generation typically has near-zero validity (missing `##fileformat`, malformed CIGAR, wrong column count, etc.). Establishes that BioTest produces *compliant* inputs, not garbage.

**Measurement**: each tool emits N candidate files; we run them through a *reference parser* (pysam + htsjdk in lenient mode) and count `parse_success / N`. Pure crashes and reject-with-diagnostic both count as "invalid."

**Instrumentation**: `compares/scripts/validity_probe.py` (to be written) — reads a directory of candidate inputs, calls each SUT's runner once per file, emits `validity.json`.

### 3.2 Structural Coverage (Branch + Line)

**Definition**: percentage of branches and lines reached inside the SUT's VCF/SAM-handling code region, as a function of elapsed wall time.

**Why it matters**: tests the tool's ability to drive the SUT's internal logic deep. This is the metric plotted in the user's proposal figure (branch coverage growth curve).

**Per-SUT tooling**:

| SUT | Language | Tool | Output |
| :--- | :--- | :--- | :--- |
| htsjdk | Java | JaCoCo (already integrated — see `coverage_artifacts/jacoco/`) | `.exec` → XML → per-line / per-branch counts |
| biopython | Python | coverage.py (already integrated) | `.coverage` SQLite → branch rates via `coverage report --format=json` |
| pysam | Python | coverage.py in Docker (already integrated) | `summary.*.json` in `coverage_artifacts/pysam/` |
| seqan3 | C++ | gcovr + `--coverage` compile flag | `gcovr.json` |

**Scoping**: coverage is restricted to the VCF/SAM-relevant paths already defined in `biotest_config.yaml: coverage.target_filters`:

```yaml
VCF: [htsjdk/variant/vcf, pysam]
SAM: [htsjdk/samtools, Bio/Align/sam, seqan3/io/sam_file, pysam]
```

This is the same whitelist BioTest's Phase D uses; reusing it keeps the comparison aligned.

**Sampling strategy**: sample coverage every 60 s during the 300 s budget to produce the growth curve. Between sample points, each tool runs its own generation loop; we pause, query coverage, resume.

### 3.3 Mutation Score

**Definition**: `killed_mutants / total_reachable_mutants`, where a mutant is *killed* if the test suite produced by the tool causes the mutated SUT to fail (parse error, crash, or different canonical JSON from the unmutated SUT's output).

**Why it matters**: measures actual defect-detection power, not coverage. High coverage with low mutation score = tool runs the code but doesn't distinguish correct from buggy behavior.

**Per-SUT mutation tooling**:

| SUT | Language | Mutation tool | Notes |
| :--- | :--- | :--- | :--- |
| htsjdk | Java | **PIT** (`pitest`, 1.15+) | Gradle plugin; mutators = DEFAULT_GROUP (Conditionals, Math, Void-method, Return-values, Negate-conditionals, Increments) |
| biopython | Python | **mutmut** (3.x) | File-based, works on package subtree |
| pysam | Python | **mutmut** | Same as biopython; run inside the Docker image to match runtime |
| seqan3 | C++ | **mull** (0.18+) | LLVM-IR-based; needs Clang build with `-fexperimental-new-pass-manager` |

**Scoping (critical)**: mutation is expensive and meaningless outside the VCF/SAM code. For each SUT, we restrict the mutation target to the same path whitelist used for coverage (§3.2). Concretely:

| SUT | Mutation target path (inside SUT source tree) |
| :--- | :--- |
| htsjdk | `src/main/java/htsjdk/variant/vcf/**`, `src/main/java/htsjdk/samtools/**` |
| biopython | `Bio/Align/sam.py`, `Bio/SeqIO/...` (if VCF path exists) |
| pysam | the VCF and SAM reader/writer modules inside the installed `pysam` package |
| seqan3 | `include/seqan3/io/sam_file/**` |

**Test-kill protocol**: for each tool's output test suite `T`, for each mutant `m`:
1. Apply `m` to the SUT.
2. Run `T` against the mutated SUT.
3. If any test in `T` produces a *different* observable outcome (parse-success flip, canonical-JSON diff, or crash flip) vs the unmutated baseline, `m` is killed.
4. Score = `|killed| / |total_reachable_mutants|`, where `reachable` = mutants in code the test suite actually executed (to avoid penalizing coverage gaps twice).

**Run time**: mutation testing is O(|T| × |M|). We cap per-SUT budget at **2 hours** and report only reachable mutants within the budget.

## 4. Comparison Protocol

### 4.1 Matrix

```
           htsjdk     biopython    pysam      seqan3
BioTest       Y          Y          Y          Y
EvoSuite      Y          —          —          —
Randoop       Y          —          —          —
Pure Random   Y          Y          Y          Y
Pynguin       —        (optional) (optional)    —
libFuzzer     —          —          —        (optional)
```

### 4.2 Fixed conditions

- **Time budget**: 300 s per tool per SUT per run (matches the proposal figure).
- **Repetitions**: 5 independent runs per (tool, SUT) cell; report mean + 95% CI for each metric.
- **Seed corpus**: for BioTest and pure random, use the Tier-1 + Tier-2 seeds from `seeds/`. EvoSuite/Randoop don't accept file-input seeds — they operate on Java classes directly; we document the class-list input separately.
- **Hardware**: fixed single machine (the current dev box); document CPU / RAM in the final report.
- **Environment**: Ollama must NOT be active during mutation runs (eats RAM). BioTest's test-generation phase runs ahead of time; mutation scoring only re-executes the **generated test suite**, not the LLM-driven mining.

### 4.3 Output

Per run, emit a JSON record:

```json
{
  "tool": "BioTest",
  "sut": "htsjdk",
  "run_index": 3,
  "time_budget_s": 300,
  "validity_ratio": 0.98,
  "coverage_growth": [
    {"t_s": 60,  "line_pct": 45.1, "branch_pct": 32.0},
    {"t_s": 120, "line_pct": 72.0, "branch_pct": 55.4},
    ...
  ],
  "mutation_score": {"killed": 187, "reachable": 231, "score": 0.809}
}
```

These records feed `compares/scripts/build_report.py` → `compares/results/comparison_report.md` + the three growth-curve figures.

## 5. Source Code Fetching

Baselines are large; cloning them into the repo would bloat git history. Instead, `compares/scripts/fetch_sources.sh` pulls them into `compares/baselines/*/source/` which is **gitignored**.

| Baseline | Source | Pinned version |
| :--- | :--- | :--- |
| EvoSuite | https://github.com/EvoSuite/evosuite (release JAR sufficient, no build needed) | v1.2.0 (2023) |
| Randoop | https://github.com/randoop/randoop (release JAR) | v4.3.3 |
| Pure Random | Hand-written in `compares/baselines/random_testing/` | N/A |
| Pynguin (optional) | `pip install pynguin==0.35.0` | via pip |
| libFuzzer (optional) | Part of Clang toolchain | Clang 18+ |
| PIT | Gradle plugin, no source fetch needed | 1.15.3 |
| mutmut | `pip install mutmut==3.0.0` | via pip |
| mull | https://github.com/mull-project/mull (release binary) | 0.18.0 |

`compares/scripts/fetch_sources.sh` is a thin wrapper: curl each release artifact, verify SHA, place under the matching `baselines/<tool>/source/` subfolder. It's a one-shot script — we run it once before the comparison phase.

## 6. Folder Layout

```
compares/
├── DESIGN.md                  # this file
├── README.md                  # quick-start pointer to DESIGN.md
├── .gitignore                 # excludes source/ subfolders and any large artifacts
├── baselines/
│   ├── evosuite/
│   │   ├── README.md          # version, fetch command, invocation example
│   │   └── source/            # (gitignored) downloaded release JAR
│   ├── randoop/
│   │   ├── README.md
│   │   └── source/            # (gitignored)
│   └── random_testing/
│       ├── README.md
│       ├── generate_vcf.py    # (placeholder) byte-level random VCF generator
│       └── generate_sam.py    # (placeholder) byte-level random SAM generator
├── mutation/
│   ├── pit/
│   │   └── README.md          # PIT Gradle config snippet + targetClasses filter
│   ├── mutmut/
│   │   └── README.md          # mutmut config + paths_to_mutate
│   └── mull/
│       └── README.md          # mull CLI flags + ir-tests filter
├── scripts/
│   ├── fetch_sources.sh       # (placeholder) one-shot download
│   ├── validity_probe.py      # (placeholder) §3.1 implementation
│   ├── coverage_sampler.py    # (placeholder) §3.2 sampling loop
│   ├── mutation_driver.py     # (placeholder) §3.3 orchestrator
│   └── build_report.py        # (placeholder) aggregate JSON → markdown + plots
└── results/                   # populated at run time; gitignored raw outputs
```

## 7. Open Decisions (to resolve before executing)

1. **Pynguin and libFuzzer as secondary Python/C++ baselines?** Adds ~50% more setup but makes the non-Java SUT comparison stronger than "vs pure random alone."
2. **5 or 10 repetitions?** 10 doubles runtime; 5 gives usable CIs for a demo.
3. **Mutation budget**: 2 hours per SUT may be insufficient for htsjdk (large codebase). Option: run overnight with no cap; accept the wall time.
4. **EvoSuite/Randoop class-list**: which Java classes inside htsjdk do we target? Logical choice: `htsjdk.variant.vcf.VCFCodec`, `VCFFileReader`, `htsjdk.samtools.SamReader`, `SAMRecord` — the I/O entry points. Needs a final confirmed list.
5. **Does "Validity Ratio" count syntactically-valid-but-semantically-wrong inputs as valid?** Proposed answer: yes — the metric is about parser acceptance, not correctness. Semantic correctness is what Mutation Score measures.

These stay open until we're ready to execute, then we lock them in a short addendum to this doc.

## 8. Non-goals

- This comparison does **not** re-evaluate BioTest's correctness or bug-finding quality against ground truth — that's measured in the main Phase A–D evaluation.
- We do not compare against neural / LLM-only fuzzers (e.g., TitanFuzz). Scope is limited to classical test-generation baselines for reproducibility.
- No real-world in-the-wild bug hunt during comparison — controlled benchmark only.

## 9. Provenance & Change Log

| Date | Change | Author |
| :--- | :--- | :--- |
| 2026-04-16 | Initial design drafted while Phase D was running live. Source/ subfolders gitignored; scripts are placeholders. | Automated assistant session |
