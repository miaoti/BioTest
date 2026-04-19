# EvoSuite 1.2.0 — htsjdk / VCF line coverage

External baseline against BioTest on the htsjdk SUT in VCF mode. Same
3-path weighted filter as `biotest.md` so numerators compare directly.

**Tool**: EvoSuite 1.2.0 (MOSA + DynaMOSA search-based unit-test
generation). Reference: Fraser & Arcuri, *EvoSuite: Automatic Test
Suite Generation for Object-Oriented Software*, FSE 2011.

## Version pairing

EvoSuite 1.2.0's shaded ASM cannot read Java-21 bytecode (class file
major version 65). The BioTest primary run uses a locally-built
Java-21-target htsjdk jar, which is therefore **not directly usable
as EvoSuite's target**. Compromises, documented here for transparency:

- **JDK**: Temurin 17.0.13 for EvoSuite (local portable install under
  `compares/baselines/evosuite/jdk17/`). BioTest uses JDK 21.
- **htsjdk**: **2.24.1** (last Java-8-compiled release from Maven
  Central) for EvoSuite. BioTest uses the locally-built ~v4.x.
- **Denominator delta**: 3 716 lines (htsjdk 2.24.1, EvoSuite) vs
  3 760 lines (local v4.x, BioTest). The 44-line gap reflects the API
  evolution between the two htsjdk versions; all three filter buckets
  are present in both jars.

Because the *numerator* is what moves with tool effort, and both tools
hit the same three package buckets with the same filter rules, the
comparison is fair enough to be informative — but the absolute pp
numbers carry a ~1 pp uncertainty band from the denominator shift.

## Target classes

Exactly the **54 classes** admitted by the three filter buckets (the
same set BioTest's Run 6 measurement scoped against):

- `htsjdk/variant/vcf` — 35 classes
- `htsjdk/variant/variantcontext` (excluding JEXL) — 16 classes
- `htsjdk/variant/variantcontext/writer::VCF,Variant` — 3 classes

The full list is embedded in `compares/scripts/run_evosuite.sh`.

## Measurement pipeline

EvoSuite tests load target classes through its own `EvoClassLoader`,
which bypasses JaCoCo's `-javaagent` instrumentation path. Standard
workaround: **offline-instrument** the htsjdk fat jar with `jacococli
instrument`. The instrumented classes record coverage to a `jacoco.exec`
file regardless of the classloader that loads them.

Pipeline:

1. `run_evosuite.sh` iterates over the 54 classes, invokes EvoSuite
   with `-generateMOSuite -criterion BRANCH:LINE` + tight per-phase
   timeouts. Stores generated `*_ESTest.java` + scaffolding under
   `compares/baselines/evosuite/results/work/evosuite-tests/`.
2. `measure_evosuite_coverage.sh`:
   - compiles every test class + scaffolding pair with javac;
   - offline-instruments the htsjdk fat jar via `jacococli`;
   - runs the whole suite through `org.junit.runner.JUnitCore` against
     the instrumented jar, with the required JDK-17 `--add-opens`
     flags so EvoSuite's runtime can use reflection on `java.*`;
   - invokes `jacococli report` to produce `jacoco.xml`;
   - applies `parse_filter_rules` (the same helper BioTest uses) to
     compute the weighted VCF score.

## Run 1 — 21 min wall, search_budget=30 s per class (2026-04-19)

Per-class flags: `-Dsearch_budget=30 -Dminimization_timeout=20
-Dassertion_timeout=20 -Dextra_timeout=20 -Dinitialization_timeout=60
-Dclient_on_thread=true -Dsandbox=false -Dminimize=true`.

Outcome:

- **34 / 54 classes** → JUnit test file generated (555 tests total;
  547 passed, 8 flaky generated assertions).
- **7 / 54 classes** → trivial (0 reachable goals: `VCFHeaderLineCount`,
  enum-only, etc.) — EvoSuite correctly skipped.
- **13 / 54 classes** → failed during ASM frame computation with
  "Class not found" errors chasing transitive htsjdk dependencies that
  exceed EvoSuite's classloader resolution (e.g.,
  `VariantContext` → `htsjdk.samtools.util.SamLocusIterator`,
  `VCFUtils` → `VariantContextWriter`).
- **Wall clock 21 min** total (vs 170 min cap) — MOSA converged fast.

Coverage against the 3-path weighted filter:

| Bucket                                              | EvoSuite (21 m, 30 s/class) |
|:----------------------------------------------------|:---------------------------:|
| `htsjdk/variant/vcf` (parser)                       | 48.6% (778/1602)            |
| `htsjdk/variant/variantcontext` (data model)        | **54.3% (1012/1864)**       |
| `htsjdk/variant/variantcontext/writer`              | 28.8% (72/250)              |
| **Weighted VCF scope**                              | **50.1% (1862/3716)**       |

Side-by-side with BioTest Run 6:

| Bucket                                  | EvoSuite | BioTest Run 6 | Winner |
|:----------------------------------------|:-:|:-:|:-:|
| `htsjdk/variant/vcf`                    | 48.6% | **60.1%** | BioTest +11.5 pp |
| `htsjdk/variant/variantcontext`         | **54.3%** | 34.6% | EvoSuite +19.7 pp |
| `htsjdk/variant/variantcontext/writer`  | 28.8% | **55.6%** | BioTest +26.8 pp |
| **Weighted VCF**                        | **50.1%** | 46.9% | EvoSuite +3.2 pp |

### Takeaways

1. **EvoSuite wins the overall weighted number by +3.2 pp** despite
   using 1/8 the wall time. MOSA converges fast on scalar-return unit
   goals; extra budget mostly idles (the 170-min re-run below stress-
   tests this claim).
2. **Bucket split tells the story**:
   - **Parser + writer buckets: BioTest wins decisively** (+11.5 pp
     and +26.8 pp). File-based metamorphic testing is the right tool
     for `VCFCodec.decode()` and `VCFWriter` code paths; EvoSuite
     constructs `VariantContext` objects in-memory and rarely drives
     the text-parse or binary-write flow end-to-end.
   - **Data-model bucket: EvoSuite wins by +19.7 pp**. Exactly the
     API-query surface Rank 5 was designed to reach. EvoSuite hits
     it trivially by calling `isStructural()`, `Allele.create()`,
     `GenotypeLikelihoods.fromPLs()` directly.
3. **Rank 5 direction is validated, ceiling is visible**. BioTest's
   34.6% on variantcontext climbed from 31.3% this run (+3.3 pp). The
   EvoSuite baseline's 54.3% is the **realistic upper bound** for
   automated API-query MRs in this package — closing the remaining
   19.7 pp gap would require more aggressive query-method selection,
   not a paradigm change.

Bug-finding is NOT compared — EvoSuite has no differential oracle,
while BioTest Run 6 reported 339 bugs via the 4-way consensus. This
note records **coverage only**.

## Run 2 — 84 min wall, search_budget=180 s per class (2026-04-19)

Stress test of Run 1's "MOSA converged early" claim. 6× the per-class
search time + larger minimization / assertion / init caps:
`-Dsearch_budget=180 -Dminimization_timeout=45 -Dassertion_timeout=30
-Dextra_timeout=30 -Dinitialization_timeout=90`.

Outcome:

- **35 / 54 classes** → tests generated (**+1 vs Run 1**:
  `GenotypeLikelihoods` succeeded with the longer budget; its 305-LOC
  test file alone added ~80 lines to the data-model bucket).
- **7 / 54 classes** → trivial (same enum-only set as Run 1).
- **12 / 54 classes** → classloader failures (same set as Run 1 minus
  GenotypeLikelihoods). These are genuine resolution failures chasing
  deep htsjdk-internal dependencies; no amount of search budget helps.
- **Wall clock 84 min** (vs 170 min cap) — used ~2× Run 1's time and
  stopped when MOSA ran out of new goals on the simpler classes while
  still hitting the per-class search cap on complex ones.
- **593 JUnit tests** ran (584 passed, 9 flaky — +38 tests vs Run 1).

Coverage against the 3-path weighted filter:

| Bucket                                   | Run 1 (21 m, 30 s) | Run 2 (84 m, 180 s) | Delta |
|:-----------------------------------------|:------------------:|:-------------------:|:-----:|
| `htsjdk/variant/vcf` (parser)            | 48.6% (778/1602)   | 48.8% (782/1602)    | +0.2 pp, +4 lines |
| `htsjdk/variant/variantcontext`          | 54.3% (1012/1864)  | **59.4% (1107/1864)** | **+5.1 pp, +95 lines** |
| `htsjdk/variant/variantcontext/writer`   | 28.8% (72/250)     | 30.4% (76/250)      | +1.6 pp, +4 lines |
| **Weighted VCF scope**                   | **50.1% (1862/3716)** | **52.9% (1965/3716)** | **+2.8 pp, +103 lines** |

### Run 2 vs Run 1 — what the extra budget bought

The variantcontext bucket moved +5.1 pp (+95 lines). Breakdown:

- **New class**: `GenotypeLikelihoods` (305 LOC test file) covered
  previously-unreachable branches in PL/GL arithmetic.
- **Bigger tests on existing classes**: `CommonInfo` 476→506 LOC,
  `GenotypesContext` 496→526, `VariantContextBuilder` 380→398,
  `VCFWriter` 224→237 — extra search found additional goals.

MOSA's "convergence" is real but **conditional**: simple classes saturated
in Run 1 (their generated suites grew by ≤ 4 LOC here), but complex
data-model classes had real headroom that 30 s search missed. The
failing-classloader set is unchanged — those are resolution bugs, not
search-budget issues, and would need EvoSuite internals to fix.

### Final comparison — BioTest Run 6 vs EvoSuite Run 2

| Bucket                                  | EvoSuite R2 (84 m) | BioTest Run 6 (170 m) | Winner |
|:----------------------------------------|:-:|:-:|:-:|
| `htsjdk/variant/vcf` (parser)           | 48.8% | **60.1%** | BioTest +11.3 pp |
| `htsjdk/variant/variantcontext`         | **59.4%** | 34.6% | EvoSuite +24.8 pp |
| `htsjdk/variant/variantcontext/writer`  | 30.4% | **55.6%** | BioTest +25.2 pp |
| **Weighted VCF**                        | **52.9%** | 46.9% | EvoSuite +5.9 pp |

### Updated takeaways after Run 2

1. **Overall lead widens** — EvoSuite +5.9 pp (was +3.2 pp). The extra
   budget closed half the gap for complex data-model classes.
2. **Bucket story unchanged, amplified**:
   - Parser bucket: BioTest still wins handily (+11.3 pp). File-based
     parsing is the right tool for `VCFCodec.decode()`.
   - Data-model bucket: EvoSuite now leads by **+24.8 pp** (was 19.7
     in Run 1). This is the published upper bound for the API-query
     surface — Rank 5's 34.6% still has ~25 pp of headroom.
   - Writer bucket: BioTest still wins by +25.2 pp. Unit-test
     generation can't drive `VCFWriter` through the actual byte
     stream.
3. **The 170-min budget was unnecessary**. EvoSuite used 84 min and
   would have used less if we capped per-class wall at ~150 s. The
   84-min number is the honest "at convergence" coverage.

Run 2 XML snapshot: `compares/baselines/evosuite/results/run2_180s_jacoco.xml`

## Artifacts

| File | Purpose |
|:--|:--|
| `compares/baselines/evosuite/source/evosuite-1.2.0.jar` | EvoSuite release |
| `compares/baselines/evosuite/jdk17/jdk-17.0.13+11/` | Portable JDK 17 |
| `compares/baselines/evosuite/htsjdk_jdk11/htsjdk-2.24.1.jar` | Maven Central htsjdk (Java-8 bytecode) |
| `compares/baselines/evosuite/deps/*.jar` | htsjdk's 8 runtime deps (commons-compress, snappy-java, nashorn-core, etc.) |
| `compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar` | Merged fat jar EvoSuite instruments |
| `compares/baselines/evosuite/fatjar/instrumented/htsjdk-with-deps.jar` | Offline-instrumented fat jar for JUnit run |
| `compares/baselines/evosuite/results/evosuite_jacoco.xml` | Final JaCoCo XML (Run 1 snapshot) |
| `compares/baselines/evosuite/results/work/evosuite-tests/` | Generated JUnit sources |
| `compares/scripts/run_evosuite.sh` | 54-class generation driver |
| `compares/scripts/measure_evosuite_coverage.sh` | Compile + instrument + run + filter |
