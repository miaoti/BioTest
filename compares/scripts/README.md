# compares/scripts — fair coverage comparison toolkit

Two scripts; one of them is the canonical way to measure any testing
tool's coverage against BioTest's scope.

## `measure_coverage.py` — fairness recipe

**Purpose.** Given a coverage report (JaCoCo XML, coverage.py JSON, or
gcovr JSON) produced by *any* testing tool, compute the same filtered
line coverage BioTest's feedback loop uses at runtime. Filter rules are
read from `biotest_config.yaml: coverage.target_filters` — single source
of truth.

**Why it matters.** Every cross-tool comparison needs this. If BioTest
is measured under one filter and, say, EvoSuite under another, any
pp-level claim is meaningless. This script removes that degree of
freedom: both sides use the exact same filter entries for the same
`(sut, format)`.

**Usage.**

```bash
# Single report
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/jacoco/jacoco_post_run6.xml \
    --sut htsjdk --format VCF \
    --label "BioTest Run 6"

# Side-by-side (add more --report / --label pairs)
py -3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/jacoco/jacoco_post_run6.xml \
    --report compares/baselines/evosuite/results/run2_180s_jacoco.xml \
    --sut htsjdk --format VCF \
    --label "BioTest Run 6" --label "EvoSuite Run 2"
```

**Output includes**:
- Which config file the filter came from (so you can audit the rules).
- Each rule verbatim (so no "which filter did you use?" ambiguity).
- Per-bucket covered / total / % (matches BioTest's internal shape).
- Overall weighted number (sum of buckets).
- Deltas against the first report when multiple reports are passed.

**Supported report formats** (auto-detected from extension + content):

| Format | Extension | Produced by |
|:--|:--|:--|
| JaCoCo XML | `.xml` | BioTest (htsjdk), EvoSuite, Randoop, PIT — any Java tool |
| coverage.py JSON | `.json` (dict `files`) | `coverage json` export from Python tools |
| gcovr JSON | `.json` (list `files`) | gcovr export from C/C++ tools |

**When to add a new report format**: add a `_measure_<fmt>` function
and a dispatcher case. Don't invent a new filter rule — that's always
read from the config.

## Adding a new testing-tool baseline

Checklist so the comparison stays honest:

1. **Run the baseline tool on the same SUT binary** BioTest tests
   (same htsjdk JAR, same pysam version, etc.). Pin the version.
2. **Execute the tool's generated tests under a coverage agent**
   (JaCoCo for Java, coverage.py for Python, gcovr for C++).
3. **Save the raw report** to
   `compares/baselines/<tool>/results/<tool>_<sut>_<format>_<tag>.xml`
   (or `.json`).
4. **Measure with `measure_coverage.py`** passing the config so both
   sides use the same filter:
   ```bash
   py -3.12 compares/scripts/measure_coverage.py \
       --report <the report you produced> --label "<tool> <tag>" \
       --report coverage_artifacts/jacoco/jacoco_post_runN.xml --label "BioTest Run N" \
       --sut <sut> --format <VCF|SAM>
   ```
5. **Append to the per-tool note** under
   `coverage_notes/<sut>/<format>/<tool>.md`. Copy the script's
   output verbatim into the doc so the measurement is reproducible.

If you find yourself tempted to write inline filter code somewhere,
stop — add it to the config or a dispatcher in this script, never to a
one-off inline block.

## `run_evosuite.sh` + `measure_evosuite_coverage.sh`

EvoSuite-specific driver. Generates JUnit tests, compiles them,
offline-instruments htsjdk with JaCoCo, runs the suite, calls
`measure_coverage.py` to apply the shared filter. Follow this pattern
for any future Java baseline (Randoop, PIT, …): build a driver that
produces a JaCoCo XML, then call `measure_coverage.py` — do not embed
measurement logic in the driver.

## Unit tests

`tests/test_measure_coverage_cli.py` — fixture-based tests for the
three report dispatchers plus a **grounding test** that locks
`BioTest Run 6 htsjdk/VCF = 1765/3760 = 46.9 %`. If that grounding
test ever flips, a code change altered the measurement semantics and
every historical number in `coverage_notes/` needs re-verifying.
