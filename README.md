<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Java-21-orange?logo=openjdk&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-29.1-blue?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-201%20passing-brightgreen?logo=pytest" />
  <img src="https://img.shields.io/badge/SUTs-4%20parsers-purple" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

```
  ____  _       _____         _
 | __ )(_) ___ |_   _|__  ___| |_
 |  _ \| |/ _ \  | |/ _ \/ __| __|
 | |_) | | (_) | | |  __/\__ \ |_
 |____/|_|\___/  |_|\___||___/\__|
```

# BioTest

**Automated Metamorphic & Differential Testing for Bioinformatics File Format Parsers**

BioTest is a fully automated pipeline that mines test rules from genomics specifications (VCF v4.5, SAM v1), then cross-examines real-world parsers (HTSJDK, Biopython, pysam, SeqAn3) to find conformance bugs — backed by spec evidence.

---

## Architecture Overview

```
          biotest.py (Grand Orchestrator)  +  biotest_config.yaml
                           |
          +----------------+----------------+----------------+
          |                |                |                |
      Phase A          Phase B          Phase C          Phase D
    Spec Ingest       MR Mining      Cross-Execution   Feedback Loop
          |                |                |                |
   VCFv4.5.tex      LLM Agent +       4 SUTs +         SCC Tracker +
   SAMv1.tex        RAG Query        Dual Oracles      Code Coverage
          |                |                |                |
     ChromaDB        MR Registry      Bug Reports      Blindspot
   (2,048 chunks)   (Enforced/       DET Report       Ticket with
                    Quarantine)                       Code Slices
                         ^                                  |
                         |                                  |
                         +---- Coverage-Steered Feedback ---+
```

| Phase | Module | What it does |
|:-----:|--------|-------------|
| **A** | `spec_ingestor/` | Fetches VCF/SAM LaTeX specs from GitHub, parses them into semantic chunks, tags normative rules (MUST/SHALL/SHOULD), and indexes into ChromaDB |
| **B** | `mr_engine/` | LLM agent autonomously queries the knowledge base, extracts Metamorphic Relations, validates against a 13-transform whitelist, hydrates evidence from ChromaDB, triages into Enforced/Quarantine tiers |
| **C** | `test_engine/` | Applies transforms to seed files, runs through 4 real parsers (HTSJDK, Biopython, pysam, SeqAn3), compares outputs with dual oracles (metamorphic + differential), generates bug reports |
| **D** | `test_engine/feedback/` | Iterative feedback loop: computes SCC (Semantic Constraint Coverage), collects multi-language code coverage (JaCoCo/coverage.py/gcovr), extracts uncovered source code slices, builds blindspot tickets to steer next-iteration MR mining, auto-quarantines failing MRs, enforces 5 termination conditions |

---

## Quick Start

### Prerequisites

```bash
# Python 3.12 (required for binary wheel compatibility)
py -3.12 --version

# Java 21 (for HTSJDK harness)
java -version

# Docker (for pysam runner on Windows)
docker --version

# Install dependencies
py -3.12 -m pip install -r requirements.txt
py -3.12 -m pip install rich pyyaml hypothesis z3-solver biopython numpy coverage
```

### Build pysam Docker Image (Windows)

```bash
# Build the Docker container for pysam (HTSlib cannot compile on Windows natively)
docker build -t biotest-pysam:latest harnesses/pysam/

# Verify all parsers are available
py -3.12 -m test_engine list-parsers
# Expected: htsjdk AVAILABLE, pysam AVAILABLE, biopython AVAILABLE, seqan3 AVAILABLE, reference AVAILABLE
```

### Set Up Local LLM (Optional)

```bash
# Install Ollama and pull qwen3-coder:30b for local Phase B mining
ollama pull qwen3-coder:30b
# Verify: curl http://localhost:11434/v1/models
```

### Run the Pipeline

```bash
# Full pipeline (A -> B -> C)
py -3.12 biotest.py

# Phase C only (uses existing MR registry, fastest)
py -3.12 biotest.py --phase C

# Phase D: Feedback-driven loop (iterates B->C with coverage steering)
py -3.12 biotest.py --phase D

# Full pipeline with feedback loop
py -3.12 biotest.py --phase A,B,C,D

# Dry run (validate config without executing)
py -3.12 biotest.py --dry-run

# Custom config + verbose logging
py -3.12 biotest.py --config my_config.yaml --verbose
```

### Run Tests

```bash
# All 201 tests
py -3.12 -m pytest tests/ -v --ignore=tests/test_integration.py --ignore=tests/test_golden_retrieval.py

# Specific module
py -3.12 -m pytest tests/test_dispatch.py -v
py -3.12 -m pytest tests/test_orchestrator_mocked.py -v
```

---

## Adding a New Parser (SUT)

> **If you want to test a parser that is not already included, you must write a
> Harness (Canonical Adapter) for it and register it in `biotest_config.yaml`.**

BioTest compares parsers by converting their outputs into a common **Canonical
JSON** format. Each parser speaks a different language and exposes a different
API, so a thin wrapper — called a **Harness** — is required to bridge the gap.

### What a Harness Does

```
Input:  file path (VCF or SAM)
          |
          v
  [ Call the SUT's native API to parse the file ]
          |
          v
  [ Convert the SUT's in-memory objects to Canonical JSON ]
          |
          v
Output: JSON to stdout  (exit 0 = success, non-zero = error)
```

Without a Harness, there is no way to compare a Java `VariantContext` object
against a Python `AlignmentIterator` object — the Harness normalizes both
into the same JSON schema so `deep_equal` can do the comparison.

### Step-by-step

**1. Write the Harness**

| SUT Language | What to write | Example |
|:------------:|---------------|---------|
| Java | A `.java` file compiled into a fat JAR | `harnesses/java/BioTestHarness.java` |
| C / C++ | A `.cpp` file compiled into an executable | `harnesses/cpp/biotest_harness.cpp` |
| Python (pip) | A runner class extending `ParserRunner` | `test_engine/runners/biopython_runner.py` |
| Python (Docker) | A harness script + Dockerfile | `harnesses/pysam/` (for libs needing Linux) |
| Rust / Go / other | A binary that reads a file and prints JSON to stdout | (same pattern as C++) |

The Harness must output JSON conforming to the canonical schema defined in
`test_engine/canonical/schema.py` (`CanonicalVcf` / `CanonicalSam`).

**2. Register it in `biotest_config.yaml`**

```yaml
phase_c:
  suts:
    # ... existing SUTs ...

    - name: my_new_parser          # unique name
      language: Rust               # for display only
      enabled: true
      sut_path: SUTfolder/rust/my_parser   # where the source lives
      adapter: harnesses/rust/my_parser    # path to compiled binary
      timeout_s: 60
```

**3. (If subprocess-based) Add a runner class**

For Java/C++/Rust SUTs that run as external processes, create a new runner in
`test_engine/runners/` following the pattern of `htsjdk_runner.py` or
`seqan3_runner.py`. For Python libraries, follow `biopython_runner.py`.

**4. Run the pipeline**

```bash
py -3.12 biotest.py --phase C
```

The orchestrator will automatically include your new SUT in both the
metamorphic and differential oracles.

### Coordinate Trap

Be aware of the **0-based vs 1-based coordinate trap**. The canonical JSON
uses 1-based positions (matching the VCF/SAM spec text). If your SUT converts
to 0-based internally (like pysam and SeqAn3 do), your Harness **must add +1**
before outputting POS and PNEXT. See the
[Coordinate Normalization](#coordinate-normalization) table below.

---

## Project Structure

```
BioTest/
|
|-- biotest.py                    # Grand Orchestrator (960 lines, Rich UI, A->B->C->D)
|-- biotest_config.yaml           # Pipeline configuration (198 lines)
|
|-- spec_ingestor/                # Phase A: Spec Ingestion
|   |-- config.py                 #   Constants (GitHub repo, ChromaDB settings)
|   |-- ingestor.py               #   GitHub API spec fetcher
|   |-- parser.py                 #   LaTeX parser + semantic chunker
|   |-- indexer.py                #   ChromaDB SpecIndex (query + index)
|   +-- main.py                   #   CLI: step_ingest / step_parse / step_index
|
|-- mr_engine/                    # Phase B: MR Mining
|   |-- llm_factory.py            #   Multi-model routing (Ollama/Groq/OpenAI/Gemini/Anthropic)
|   |-- behavior.py               #   6 BehaviorTarget enums + descriptions
|   |-- transforms/               #   13 atomic transform functions
|   |   |-- __init__.py           #     TRANSFORM_REGISTRY + decorator
|   |   |-- vcf.py                #     9 VCF transforms
|   |   +-- sam.py                #     4 SAM transforms
|   |-- agent/                    #   LangChain ReAct Agent
|   |   |-- tools.py              #     query_spec_database tool
|   |   |-- prompts.py            #     System prompt builder (+ blindspot injection)
|   |   |-- transforms_menu.py    #     Transform menu for LLM
|   |   +-- engine.py             #     mine_mrs() with retry loop + blindspot_context
|   |-- dsl/                      #   Pydantic DSL Compiler
|   |   |-- models.py             #     MetamorphicRelation, Evidence, compute_mr_id
|   |   +-- compiler.py           #     JSON extraction + validation + hydration
|   +-- registry.py               #   Enforced/Quarantine triage + merge + export
|
|-- test_engine/                  # Phase C: Cross-Execution
|   |-- config.py                 #   Paths, timeouts, parser matrix
|   |-- orchestrator.py           #   Main test loop (Hypothesis + Static dual-mode)
|   |-- __main__.py               #   CLI: python -m test_engine run / list-parsers
|   |-- canonical/                #   Canonical JSON normalization
|   |   |-- schema.py             #     Pydantic models (CanonicalVcf, CanonicalSam)
|   |   |-- vcf_normalizer.py     #     Raw VCF text -> canonical JSON
|   |   +-- sam_normalizer.py     #     Raw SAM text -> canonical JSON
|   |-- runners/                  #   Multi-language parser runners (5 SUTs)
|   |   |-- base.py               #     ParserRunner ABC + RunnerResult
|   |   |-- htsjdk_runner.py      #     Java subprocess (fat JAR + JaCoCo coverage)
|   |   |-- biopython_runner.py   #     Python in-process (SAM, hybrid approach)
|   |   |-- pysam_runner.py       #     Facade: native pysam -> Docker fallback
|   |   |-- pysam_docker_runner.py#     Docker subprocess (VCF+SAM, with coverage)
|   |   |-- seqan3_runner.py      #     C++ subprocess (SAM, optional coverage binary)
|   |   +-- reference_runner.py   #     Built-in Python parser (always available)
|   |-- generators/               #   Test generation engine
|   |   |-- dispatch.py           #     Transform dispatcher (13 wrappers + Z3 guards)
|   |   |-- strategy_router.py    #     Transform name -> Hypothesis strategy
|   |   |-- seeds.py              #     Seed corpus loader
|   |   |-- vcf_strategies.py     #     Hypothesis strategies for VCF
|   |   |-- sam_strategies.py     #     Hypothesis strategies for SAM
|   |   |-- z3_constraints.py     #     Z3 constraint guards
|   |   +-- shrink.py             #     Custom shrink hooks
|   |-- oracles/                  #   Dual oracle system
|   |   |-- deep_equal.py         #     Semantic comparison (float tolerance, QUAL)
|   |   |-- metamorphic.py        #     Oracle 1: parse(x) == parse(T(x))
|   |   |-- differential.py       #     Oracle 2: HTSJDK(x) == pysam(x) == ...
|   |   +-- det_tracker.py        #     DET rate tracking (+ failure_type field)
|   |-- triage/                   #   Bug report generation
|   |   |-- classifier.py         #     4 failure types
|   |   |-- report_builder.py     #     Auto-generates BUG-{timestamp}/ (with shrink)
|   |   +-- evidence_formatter.py #     Spec evidence -> Markdown
|   +-- feedback/                 #   Phase D: Feedback Loop (6 files)
|       |-- scc_tracker.py        #     Semantic Constraint Coverage computation
|       |-- loop_controller.py    #     5 termination conditions + state persistence
|       |-- quarantine_manager.py #     Dynamic MR demotion (Enforced -> Quarantine)
|       |-- coverage_collector.py #     Multi-language coverage (JaCoCo/coverage.py/gcovr)
|       +-- blindspot_builder.py  #     Blindspot ticket + source code slice extraction
|
|-- harnesses/                    # External parser harnesses
|   |-- java/
|   |   |-- BioTestHarness.java   #   HTSJDK -> canonical JSON (425 lines)
|   |   +-- build/libs/
|   |       +-- biotest-harness-all.jar  # Fat JAR (HTSJDK bundled)
|   |-- cpp/
|   |   +-- biotest_harness.cpp   #   SeqAn3 -> canonical JSON (248 lines)
|   +-- pysam/                    #   pysam Docker harness
|       |-- pysam_harness.py      #     Standalone CLI (VCF+SAM, --coverage mode)
|       |-- Dockerfile            #     python:3.12-slim + pysam + coverage
|       +-- build_docker.py       #     Build + smoke test script
|
|-- seeds/                        # Test seed corpus (6 files)
|   |-- vcf/                      #   3 VCF seeds (spec example, multi-sample, minimal)
|   +-- sam/                      #   3 SAM seeds (spec example, tags, complex CIGAR)
|
|-- data/                         # Persistent data
|   |-- chroma_db/                #   ChromaDB vector store (2,048 chunks)
|   |-- parsed/                   #   VCF/SAM parsed chunks JSON (453 testable rules)
|   |-- mr_registry.json          #   Mined MR registry (Enforced + Quarantine)
|   |-- det_report.json           #   DET rate report
|   |-- scc_report.json           #   Semantic Constraint Coverage report
|   +-- feedback_state.json       #   Phase D iteration state (crash recovery)
|
|-- coverage_artifacts/           # Phase D: Coverage data (gitignored)
|   |-- jacoco/                   #   JaCoCo agent JAR + exec data + XML reports
|   |-- pysam/                    #   Docker coverage fragments + extracted source
|   +-- .coverage                 #   coverage.py data (biopython)
|
|-- bug_reports/                  # Auto-generated bug report bundles
|   +-- BUG-{timestamp}/
|       |-- x.vcf                 #   Shrunk minimal reproduction seed
|       |-- T_x.vcf               #   Shrunk minimal reproduction variant
|       |-- canonical_outputs/    #   Parser JSON comparison
|       |-- logs/                 #   Diffs + stderr
|       |-- evidence.md           #   Spec citations from Phase B
|       +-- summary.json          #   Classification metadata
|
|-- tests/                        # 201 tests (12 test files)
|
+-- SUTfolder/                    # Systems Under Test (gitignored)
    |-- java/htsjdk/              #   HTSJDK (Java, VCF+SAM)
    |-- python/biopython/         #   Biopython (Python, SAM)
    +-- cpp/seqan3/               #   SeqAn3 (C++, SAM)
```

---

## The 13 Atomic Transforms

These are the building blocks for metamorphic test generation. Each transform preserves biological semantics while changing textual representation.

### VCF Transforms (9)

| # | Transform | Scope | Description |
|:-:|-----------|:-----:|-------------|
| 1 | `shuffle_meta_lines` | Header | Shuffle `##` meta-information lines (keep `##fileformat` first) |
| 2 | `permute_structured_kv_order` | Header | Reorder key=value pairs inside `##INFO=<...>` structured lines |
| 3 | `choose_permutation` | Record | Generate random permutation array `[0..n-1]` |
| 4 | `permute_ALT` | Record | Reorder ALT alleles by permutation |
| 5 | `remap_GT` | Record | Update GT indices to match new ALT order (REF=0 never changes) |
| 6 | `permute_Number_A_R_fields` | Record | Reorder Number=A/R INFO values to match ALT permutation |
| 7 | `permute_sample_columns` | File | Shuffle sample columns across header + all data rows |
| 8 | `shuffle_info_field_kv` | Record | Shuffle semicolon-separated INFO key=value pairs |
| 9 | `inject_equivalent_missing_values` | Record | Append declared-but-missing FORMAT field (semantic no-op) |

> Transforms 3-6 form a **compound group** (`alt_permutation`) and must always appear together.

### SAM Transforms (4)

| # | Transform | Scope | Description |
|:-:|-----------|:-----:|-------------|
| 10 | `permute_optional_tag_fields` | Record | Shuffle optional TAG:TYPE:VALUE fields (cols 12+) |
| 11 | `split_or_merge_adjacent_cigar_ops` | Record | Split `10M` -> `4M6M` or merge `4M6M` -> `10M` |
| 12 | `reorder_header_records` | Header | Shuffle `@SQ`/`@RG` lines (keep `@HD` first) |
| 13 | `toggle_cigar_hard_soft_clipping` | Record | Convert H<->S clipping with SEQ/QUAL sync |

---

## Configuration (`biotest_config.yaml`)

```yaml
phase_a:
  specs:
    - { file: VCFv4.5.tex, format: VCF, version: "4.5" }
    - { file: SAMv1.tex, format: SAM, version: "1.6" }

phase_b:
  formats: [VCF]
  themes: [ordering_invariance]
  llm:
    model: ollama/qwen3-coder:30b    # Local Ollama (also supports Groq, OpenAI, Gemini, Anthropic)

phase_c:
  format_filter: VCF
  suts:
    - { name: htsjdk, adapter: harnesses/java/build/libs/biotest-harness-all.jar }
    - { name: biopython }
    - { name: seqan3, adapter: harnesses/cpp/build/biotest_harness.exe }
    - { name: pysam, coverage_dir: coverage_artifacts/pysam }  # Docker on Windows

# Phase D: Feedback-driven loop
feedback_control:
  enabled: true
  max_iterations: 5
  plateau_patience: 2
  target_scc_percent: 95.0
  timeout_minutes: 120
  primary_target: htsjdk            # This SUT drives feedback evolution
  source_roots:                     # For source code slice extraction
    htsjdk: SUTfolder/java/htsjdk/src/main/java
    seqan3: SUTfolder/cpp/seqan3/include
    pysam: coverage_artifacts/pysam/source

coverage:
  enabled: true
  target_filters:                   # Format-aware whitelist filtering
    VCF: [htsjdk/variant/vcf, pysam]
    SAM: [htsjdk/samtools, Bio/Align/sam, seqan3/io/sam_file, pysam]
```

---

## Dual Oracle System

BioTest uses two complementary oracles to detect bugs:

### Oracle 1: Metamorphic

```
semantic( parse(x) )  ==  semantic( parse(T(x)) )
```

For a **single parser**, the original seed and a semantics-preserving transform must produce equivalent output. If they differ, the parser has a conformance bug.

### Oracle 2: Differential

```
HTSJDK(x)  ==  Biopython(x)  ==  pysam(x)  ==  SeqAn3(x)
```

For the **same input**, all parsers must agree. Any disagreement is a Difference-Exposing Test (DET).

### DET Rate

```
DET Rate = (tests with disagreement) / (total tests)
```

Tracked per MR and per parser pair. Exported to `data/det_report.json`.

---

## Phase D: Feedback-Driven Loop

Phase D wraps B and C into an iterative loop steered by coverage signals:

```
for each iteration (up to max_iterations):
    Phase B: mine MRs (with blindspot context from previous iteration)
    Phase C: execute tests (with coverage instrumentation)
    |
    +-> Compute SCC (Semantic Constraint Coverage)
    +-> Collect code coverage (JaCoCo / coverage.py / gcovr)
    +-> Extract uncovered source code slices from primary target
    +-> Auto-quarantine MRs with >50% crash rate
    +-> Build blindspot ticket for next iteration
    |
    Check 5 termination conditions:
      1. Timeout          2. SCC target reached
      3. Budget exhausted  4. Catastrophic demotion
      5. SCC plateau (no improvement for N rounds)
```

### Primary Target vs Auxiliary Oracles

The feedback loop is driven by a single **primary target** SUT (configurable). Other SUTs participate in differential testing but do not steer MR evolution. If the primary target fails an MR, that spec rule stays as a "blind spot" regardless of whether other parsers passed it.

### Blindspot Tickets with Source Code Slices

The blindspot builder doesn't just report "line 105-110 uncovered" -- it extracts the **actual source code** at those lines so the LLM can see the concrete `if/else` branches:

```
UNCOVERED CODE in the primary target parser:
  VCFCodec.java:43-57
      43 |     public boolean canDecodeURI(final IOPath ioPath) {
      44 |         ValidationUtils.nonNull(ioPath, "ioPath");
      45 |         return extensionMap.stream().anyMatch(ext-> ioPath.hasExtension(ext));
      46 |     }
```

### Coverage Matrix

| SUT | Tool | Instrumentation | Format Filters |
|-----|------|-----------------|---------------|
| **htsjdk** | JaCoCo | `-javaagent` runtime injection | VCF: `htsjdk/variant/vcf` |
| **biopython** | coverage.py | `cov.start()/stop()` wrapping Phase C | SAM: `Bio/Align/sam` |
| **pysam** | coverage.py (Docker) | `--coverage` flag, writes to mounted volume | VCF+SAM: `pysam` |
| **seqan3** | gcovr/gcov | Compile with `--coverage` | SAM: `seqan3/io/sam_file` |

---

## Real Bug Found

BioTest discovered that **HTSJDK rejects VCF files where structured meta-line fields appear in non-standard order**:

```
##INFO=<Type=Integer,Number=1,ID=DP,Description="Total Depth">
         ^^^^^^^^^^^^^^^^^^^^^^^^^
         HTSJDK expects ID first, but spec says order doesn't matter
```

**Spec citation** (VCF v4.5, Section "Meta-information lines"):

> *"Implementations must not rely on the order of the fields within structured lines and are not required to preserve field ordering."*

The bug report was auto-generated with: original seed, transformed variant, parser stack trace, canonical JSON diff, and spec evidence.

---

## Coordinate Normalization

Different parsers use different coordinate conventions internally. The canonical normalizers handle this:

| Parser | SAM POS | VCF POS | Adapter Action |
|--------|:-------:|:-------:|---------------|
| **HTSJDK** (Java) | 1-based | 1-based | No adjustment |
| **Biopython** (Python) | 0-based | N/A | **+1** |
| **pysam** (Python) | 0-based | **0-based** | **+1 for both** |
| **SeqAn3** (C++) | 0-based | N/A | **+1** |

---

## Parser Availability

| Runner | VCF | SAM | Status | Execution Method |
|--------|:---:|:---:|:------:|-----------------|
| **HTSJDK** | Yes | Yes | Available | Java subprocess (fat JAR + JaCoCo agent) |
| **pysam** | Yes | Yes | Available | Docker container (`biotest-pysam:latest`) or native pip |
| **Biopython** | - | Yes | Available | Python in-process (hybrid: Biopython objects + raw text) |
| **SeqAn3** | - | Yes | Available | C++ subprocess (compiled binary) |
| **Reference** | Yes | Yes | Always | Built-in Python normalizer (not a SUT) |

---

## Test Suite

**201 tests in 12 files, executing in < 1 second**

| Category | Tests | Coverage |
|----------|:-----:|----------|
| **Phase B: Transforms** | 42 | All 13 atomic transforms (determinism, correctness, invariants) |
| **Phase B: DSL Models** | 17 | Pydantic validation, hashing, compound-step rules |
| **Phase B: Registry** | 11 | Triage, dedup, JSON export |
| **Phase C: Deep Equal** | 22 | Dict/set/float/nested/multiset comparison |
| **Phase C: Canonical** | 16 | VCF + SAM normalizers, schema validation |
| **Phase C: Dispatch** | 11 | All transform granularity levels + compound group |
| **Hardening: Runners** | 13 | Timeout, crash stderr, availability guards, Docker facade |
| **Hardening: Generators** | 25 | Z3 CIGAR constraints, INFO/FLAG validation, shrink hooks |
| **Hardening: Triage** | 18 | Concurrent report builder, evidence Markdown, classifier |
| **Hardening: E2E Mocked** | 8 | Full pipeline with DummyRunners, exact DET rate verification |
| **Phase D: Feedback** | 18+ | SCC tracker, loop controller, coverage aggregation (smoke-tested) |

---

## Code Metrics

| Module | Files | Lines | Purpose |
|--------|:-----:|------:|---------|
| `spec_ingestor/` | 8 | 976 | Phase A: Spec Ingestion |
| `mr_engine/` | 16 | 2,479 | Phase B: MR Mining (+ Ollama LLM route) |
| `test_engine/` (Phase C) | 23 | 3,900+ | Cross-Execution, Runners, Oracles, Triage |
| `test_engine/feedback/` | 6 | 1,682 | Phase D: SCC, Coverage, Blindspot, Quarantine |
| `biotest.py` | 1 | 960 | Grand Orchestrator (A->B->C->D + Rich UI) |
| `harnesses/` | 5 | 952 | Java (425) + C++ (248) + pysam Docker (279) |
| `tests/` | 12 | 3,000+ | Test suite (201 tests) |
| **Total** | **71+** | **14,000+** | |

---

## Dependencies

### Python (3.12)

```
# Phase A
requests, pylatexenc, chromadb, openai, tiktoken

# Phase B
pydantic, pydantic-settings, langchain-core, langgraph
langchain-openai, langchain-google-genai, langchain-anthropic

# Phase C
hypothesis, z3-solver, numpy, biopython, jsonschema

# Phase D
rich, pyyaml, coverage
```

### System

```
Java 21            # HTSJDK harness
Docker 29+         # pysam runner (required on Windows)
Ollama 0.20+       # Local LLM for Phase B mining (optional, alternative to cloud APIs)
CMake 4.3+         # SeqAn3 build (optional)
g++ 15+ (C++20)    # SeqAn3 compilation (optional)
```

---

## License

MIT
