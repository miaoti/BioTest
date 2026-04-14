<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Java-21-orange?logo=openjdk&logoColor=white" />
  <img src="https://img.shields.io/badge/Tests-191%20passing-brightgreen?logo=pytest" />
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
                  biotest.py (Grand Orchestrator)
                  biotest_config.yaml
                           |
          +----------------+----------------+
          |                |                |
      Phase A          Phase B          Phase C
    Spec Ingest       MR Mining      Cross-Execution
          |                |                |
   VCFv4.5.tex      LLM Agent +       Metamorphic +
   SAMv1.tex        RAG Query        Differential
          |                |            Oracles
     ChromaDB        MR Registry          |
   (1,425 chunks)   (3 enforced)    Bug Reports
                                    DET Report
```

| Phase | Module | What it does |
|:-----:|--------|-------------|
| **A** | `spec_ingestor/` | Fetches VCF/SAM LaTeX specs from GitHub, parses them into semantic chunks, tags normative rules (MUST/SHALL/SHOULD), and indexes into ChromaDB |
| **B** | `mr_engine/` | LLM agent autonomously queries the knowledge base, extracts Metamorphic Relations, validates them against a 13-transform whitelist, hydrates evidence from ChromaDB, and triages into Enforced/Quarantine tiers |
| **C** | `test_engine/` | Applies transforms to seed files, runs them through real parsers, compares outputs with dual oracles (metamorphic + differential), classifies failures, and generates reproducible bug reports |
| **D** | `biotest.py` | Grand Orchestrator that sequences A->B->C from a single YAML config and prints a rich terminal dashboard |

---

## Quick Start

### Prerequisites

```bash
# Python 3.12 (required for binary wheel compatibility)
py -3.12 --version

# Java 21 (for HTSJDK harness)
java -version

# Install dependencies
py -3.12 -m pip install -r requirements.txt
py -3.12 -m pip install rich pyyaml hypothesis z3-solver biopython numpy
```

### Run the Pipeline

```bash
# Full pipeline (A -> B -> C)
py -3.12 biotest.py

# Phase C only (uses existing MR registry, fastest)
py -3.12 biotest.py --phase C

# Dry run (validate config without executing)
py -3.12 biotest.py --dry-run

# Custom config
py -3.12 biotest.py --config my_config.yaml

# Verbose logging
py -3.12 biotest.py --phase C --verbose
```

### Run Tests

```bash
# All 191 tests (< 0.4 seconds)
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
|-- biotest.py                    # Grand Orchestrator (Phase D)
|-- biotest_config.yaml           # Pipeline configuration
|
|-- spec_ingestor/                # Phase A: Spec Ingestion
|   |-- config.py                 #   Constants (GitHub repo, ChromaDB settings)
|   |-- ingestor.py               #   GitHub API spec fetcher
|   |-- parser.py                 #   LaTeX parser + semantic chunker
|   |-- indexer.py                #   ChromaDB SpecIndex (query + index)
|   +-- main.py                   #   CLI: step_ingest / step_parse / step_index
|
|-- mr_engine/                    # Phase B: MR Mining
|   |-- llm_factory.py            #   Multi-model routing (Groq/OpenAI/Gemini/Anthropic)
|   |-- behavior.py               #   6 BehaviorTarget enums + descriptions
|   |-- transforms/               #   13 atomic transform functions
|   |   |-- __init__.py           #     TRANSFORM_REGISTRY + decorator
|   |   |-- vcf.py                #     9 VCF transforms
|   |   +-- sam.py                #     4 SAM transforms
|   |-- agent/                    #   LangChain ReAct Agent
|   |   |-- tools.py              #     query_spec_database tool
|   |   |-- prompts.py            #     System prompt builder
|   |   |-- transforms_menu.py    #     Transform menu for LLM
|   |   +-- engine.py             #     mine_mrs() with retry loop
|   |-- dsl/                      #   Pydantic DSL Compiler
|   |   |-- models.py             #     MetamorphicRelation, Evidence, compute_mr_id
|   |   +-- compiler.py           #     JSON extraction + validation + hydration
|   +-- registry.py               #   Enforced/Quarantine triage + export
|
|-- test_engine/                  # Phase C: Cross-Execution
|   |-- config.py                 #   Paths, timeouts, parser matrix
|   |-- orchestrator.py           #   Main test loop
|   |-- __main__.py               #   CLI: python -m test_engine run
|   |-- canonical/                #   Canonical JSON normalization
|   |   |-- schema.py             #     Pydantic models (CanonicalVcf, CanonicalSam)
|   |   |-- vcf_normalizer.py     #     Raw VCF text -> canonical JSON
|   |   +-- sam_normalizer.py     #     Raw SAM text -> canonical JSON
|   |-- runners/                  #   Multi-language parser runners
|   |   |-- base.py               #     ParserRunner ABC + RunnerResult
|   |   |-- htsjdk_runner.py      #     Java subprocess (fat JAR)
|   |   |-- biopython_runner.py   #     Python in-process (SAM)
|   |   |-- pysam_runner.py       #     Python in-process (VCF+SAM)
|   |   |-- seqan3_runner.py      #     C++ subprocess (SAM)
|   |   +-- reference_runner.py   #     Built-in Python parser
|   |-- generators/               #   Test generation engine
|   |   |-- dispatch.py           #     Transform dispatcher (13 wrappers)
|   |   |-- seeds.py              #     Seed corpus loader
|   |   |-- vcf_strategies.py     #     Hypothesis strategies for VCF
|   |   |-- sam_strategies.py     #     Hypothesis strategies for SAM
|   |   |-- z3_constraints.py     #     Z3 constraint guards
|   |   +-- shrink.py             #     Custom shrink hooks
|   |-- oracles/                  #   Dual oracle system
|   |   |-- deep_equal.py         #     Semantic comparison
|   |   |-- metamorphic.py        #     Oracle 1: parse(x) == parse(T(x))
|   |   |-- differential.py       #     Oracle 2: HTSJDK(x) == Biopython(x)
|   |   +-- det_tracker.py        #     DET rate tracking
|   +-- triage/                   #   Bug report generation
|       |-- classifier.py         #     4 failure types
|       |-- report_builder.py     #     Auto-generates BUG-{timestamp}/ bundles
|       +-- evidence_formatter.py #     Spec evidence -> Markdown
|
|-- harnesses/                    # External parser harnesses
|   +-- java/
|       |-- BioTestHarness.java   #   HTSJDK -> canonical JSON to stdout
|       +-- build/libs/
|           +-- biotest-harness-all.jar  # Fat JAR (HTSJDK bundled)
|
|-- seeds/                        # Test seed corpus
|   |-- vcf/                      #   3 VCF seeds (spec example, multi-sample, minimal)
|   +-- sam/                      #   3 SAM seeds (spec example, tags, complex CIGAR)
|
|-- data/                         # Persistent data
|   |-- chroma_db/                #   ChromaDB vector store (1,425 chunks)
|   |-- parsed/                   #   VCF/SAM parsed chunks JSON
|   |-- mr_registry.json          #   Mined MR registry (3 enforced)
|   +-- det_report.json           #   DET rate report
|
|-- bug_reports/                  # Auto-generated bug report bundles
|   +-- BUG-{timestamp}/
|       |-- x.vcf                 #   Original seed
|       |-- T_x.vcf               #   Transformed variant
|       |-- canonical_outputs/    #   Parser JSON comparison
|       |-- logs/                 #   Diffs + stderr
|       |-- evidence.md           #   Spec citations
|       +-- summary.json          #   Classification metadata
|
|-- tests/                        # 191 tests (12 test files)
|   |-- test_transforms.py        #   42 tests: atomic transform correctness
|   |-- test_dsl.py               #   17 tests: Pydantic validation + hashing
|   |-- test_registry.py          #   11 tests: triage + dedup + export
|   |-- test_deep_equal.py        #   22 tests: semantic comparison
|   |-- test_canonical.py         #   16 tests: VCF/SAM normalizers
|   |-- test_dispatch.py          #   11 tests: transform dispatch wrappers
|   |-- test_runner_defense.py    #   13 tests: timeout/crash/availability guards
|   |-- test_generator_boundary.py#   25 tests: Z3 constraints + shrink hooks
|   |-- test_triage_defense.py    #   18 tests: concurrent reports + evidence formatting
|   |-- test_orchestrator_mocked.py#   8 tests: full E2E with DummyRunners
|   |-- test_integration.py       #   Integration tests (needs ChromaDB)
|   +-- test_golden_retrieval.py  #   Phase A retrieval tests
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
    - file: VCFv4.5.tex
      format: VCF
      version: "4.5"
    - file: SAMv1.tex
      format: SAM
      version: "1.6"

phase_b:
  formats: [VCF]
  themes: [ordering_invariance]
  llm:
    model: moonshotai/kimi-k2-instruct

phase_c:
  format_filter: VCF
  suts:
    - name: htsjdk
      enabled: true
      adapter: harnesses/java/build/libs/biotest-harness-all.jar
    - name: biopython
      enabled: true
    - name: reference
      enabled: true
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

| Runner | VCF | SAM | Status | Notes |
|--------|:---:|:---:|:------:|-------|
| **HTSJDK** | Yes | Yes | Available | Java 21 + fat JAR |
| **Biopython** | - | Yes | Available | pip install biopython |
| **pysam** | Yes | Yes | Windows N/A | Needs Linux/macOS (HTSlib) |
| **SeqAn3** | - | Yes | Needs build | cmake + C++20 |
| **Reference** | Yes | Yes | Always | Built-in Python parser |

---

## Test Suite

**191 tests in 12 files, executing in < 0.4 seconds**

| Category | Tests | Coverage |
|----------|:-----:|----------|
| **Phase B: Transforms** | 42 | All 13 atomic transforms (determinism, correctness, invariants) |
| **Phase B: DSL Models** | 17 | Pydantic validation, hashing, compound-step rules |
| **Phase B: Registry** | 11 | Triage, dedup, JSON export |
| **Phase C: Deep Equal** | 22 | Dict/set/float/nested/multiset comparison |
| **Phase C: Canonical** | 16 | VCF + SAM normalizers, schema validation |
| **Phase C: Dispatch** | 11 | All transform granularity levels + compound group |
| **Hardening: Runners** | 13 | Timeout interception, crash stderr, availability guards |
| **Hardening: Generators** | 25 | Z3 CIGAR constraints, INFO/FLAG validation, shrink hooks |
| **Hardening: Triage** | 18 | Concurrent report builder, evidence Markdown, classifier |
| **Hardening: E2E Mocked** | 8 | Full pipeline with DummyRunners, exact DET rate verification |

---

## Code Metrics

| Module | Files | Lines | Purpose |
|--------|:-----:|------:|---------|
| `spec_ingestor/` | 8 | 976 | Phase A: Spec Ingestion |
| `mr_engine/` | 16 | 2,479 | Phase B: MR Mining |
| `test_engine/` | 21 | 3,482 | Phase C: Cross-Execution |
| `tests/` | 12 | 2,976 | Test suite (191 tests) |
| `biotest.py` | 1 | 664 | Phase D: Grand Orchestrator |
| `BioTestHarness.java` | 1 | 425 | Java HTSJDK harness |
| **Total** | **59** | **11,002** | |

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
rich, pyyaml
```

### System

```
Java 21          # HTSJDK harness
CMake 4.3+       # SeqAn3 build (optional)
g++ 15+ (C++20)  # SeqAn3 compilation (optional)
```

---

## License

MIT
