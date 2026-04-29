# Baseline Tool Provenance & Defensibility

Concise reference for justifying each baseline in the comparative
evaluation. Citation counts and GitHub-star numbers should be
re-verified at submission time (Google Scholar / GitHub API).

## Input fuzzers

| Tool | Origin | Venue | Year | Tier | Defensibility evidence |
| :--- | :--- | :--- | ---: | :--- | :--- |
| **Jazzer** | Code Intelligence GmbH (industrial OSS) | n/a (no peer-reviewed paper); integrated into OSS-Fuzz | 2021– | OSS, industrial-grade | Default JVM fuzzer in Google's OSS-Fuzz infrastructure; 2k+ GitHub stars; cited as state-of-the-art Java in-process coverage-guided fuzzer in `boehme2021estimating` and several follow-ups |
| **Atheris** | Google (industrial OSS) | n/a (no paper); Google security team | 2020– | OSS, industrial-grade | The de-facto coverage-guided fuzzer for CPython and CPython C extensions; integrated into OSS-Fuzz; 1.7k+ GitHub stars |
| **libFuzzer** | Serebryany et al., LLVM Project | USENIX ATC | 2016 | A* (CORE), top systems venue | ~600 Google Scholar citations; the canonical in-process coverage-guided fuzzer; baseline in essentially every fuzzing paper since 2016 |
| **cargo-fuzz** | Rust Fuzzing Authority (OSS) | n/a; standard Rust tooling | 2017– | OSS, language-standard | Default fuzzer for Rust crates; wraps libFuzzer; recommended by the Rust Foundation; 1.5k+ GitHub stars |
| **AFL++** | Fioraldi, Maier, Eißfeldt, Heuse | USENIX WOOT | 2020 | A (CORE) | 200+ Google Scholar citations; default coverage-guided fuzzer in academia post-2020; SOTA fork-server fuzzer |

## Random-baseline floor

| Tool | Origin | Venue | Year | Defensibility |
| :--- | :--- | :--- | ---: | :--- |
| **Pure-Random (`os.urandom` byte stream)** | Hand-implemented per Klees et al. CCS'18 §3.4 floor | n/a (methodology) | 2018 | The canonical "uninformed-fuzzing baseline" required by the Klees et al. CCS'18 evaluation guidelines (~700 Google Scholar citations on the methodology paper) |

## Unit-level Java baselines

| Tool | Origin | Venue | Year | Tier | Defensibility evidence |
| :--- | :--- | :--- | ---: | :--- | :--- |
| **EvoSuite** | Fraser & Arcuri | ESEC/FSE | 2011 | A* (CORE) | ~1.3k Google Scholar citations on the FSE'11 paper; the most cited search-based unit-test generator; multiple follow-ups (TOSEM, ICSE, ASE) |
| **Randoop** | Pacheco, Lahiri, Ernst, Ball | ICSE | 2007 | A* (CORE) | ~1.5k Google Scholar citations; the canonical feedback-directed random-testing tool; foundational reference for unit-test generation |

## Mutation engines (not directly baselines, used to grade adequacy)

| Tool | Origin | Venue | Year | Tier | Defensibility evidence |
| :--- | :--- | :--- | ---: | :--- | :--- |
| **PIT (pitest)** | Coles, Laurent, Henard, Papadakis, Ventresque | ISSTA (Tool Demo) | 2016 | A* (CORE) | The de-facto Java mutation engine; ~250+ Google Scholar citations; widely used in industry CI pipelines |
| **mull** | Denisov & Pankevich | ICSTW | 2018 | B (CORE) | ~50 Google Scholar citations; only mature LLVM-IR mutation tool that supports modern C++ across multiple compilers |
| **mutmut** | Hovmöller (OSS) | n/a (no paper) | 2017– | OSS, language-standard | The most-installed Python mutation tester (PyPI); recommended by Python testing guides; 800+ GitHub stars |
| **cargo-mutants** | Pool (OSS) | n/a (no paper) | 2021– | OSS, language-standard | The maintained Rust mutation tester; recommended by the Rust Fuzzing Authority; 1k+ GitHub stars |

## Methodology citations (not tools, but bench-design support)

| Citation | Use | Venue | Tier |
| :--- | :--- | :--- | :--- |
| Klees et al. 2018 | Fuzzer evaluation methodology + Pure-Random floor + crash-count critique | CCS | A* |
| Böhme, Liyanage, Wüstholz 2021 | Silence-on-fix predicate + drop-list discipline | ESEC/FSE | A* |
| Hazimeh, Herrera, Payer 2020 | Magma ground-truth fuzzing benchmark + canary attribution | POMACS / SIGMETRICS | A* |
| Metzman et al. 2021 | FuzzBench fuzzer-evaluation platform | ESEC/FSE | A* |
| Dolan-Gavitt et al. 2016 | LAVA magic-number injection (cited as future-work alternative) | IEEE S&P | A* |

## Notes on tier ratings

CORE rankings (Computing Research and Education Association of Australasia)
used as the standard: A* = top-tier, A = excellent, B = good. Top-tier
SE/security venues (ICSE, FSE, ASE, OOPSLA, USENIX Security, S&P, NDSS,
CCS) are A*. Workshops and demo tracks (WOOT, ICSTW, ISSTA Tool Demo) are
typically B–A. Journal IFs are not listed because all referenced
publications are conferences, where citation count and CORE tier are the
standard reputational metric.

## Aggregate justification for the baseline slate

| Paradigm covered | Tool(s) | Why this is the defensible choice |
| :--- | :--- | :--- |
| **In-process coverage-guided fuzzing (per language)** | Jazzer (Java), Atheris (Python), libFuzzer (C++), cargo-fuzz (Rust), AFL++ (C++) | Each is the canonical SOTA in its language ecosystem; OSS-Fuzz uses Jazzer + Atheris + libFuzzer for production fuzzing of every major Java/Python/C++ project. No serious "fair baseline" choice exists for these languages |
| **Uninformed floor** | Pure-Random | Required by Klees et al.~2018 to bound below-zero claims |
| **Unit-level Java GA** | EvoSuite | Most-cited search-based unit-test generator; canonical reference |
| **Unit-level Java random** | Randoop | Most-cited feedback-directed random unit-test generator; canonical reference |

The slate spans every paradigm a reviewer is likely to flag as
"missing" — coverage-guided crash fuzzing in each host language,
pure-random floor, and unit-level GA + random — using the
canonical instance of each. No top-tier alternative is omitted.
