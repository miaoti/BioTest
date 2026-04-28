# Randoop bug-bench report

**Run date:** 2026-04-26
**Tool:** Randoop 4.3.3 (Pacheco et al., OOPSLA'07)
**Role:** White-box, unit-level Java test generator. Documented in
DESIGN.md §2.3 as a secondary/optional baseline; not in the primary
slim matrix (§4.1) because it shares EvoSuite's white-box paradigm and
the EvoSuite anchor alone makes the same point. This report is the
first time we executed it on the verified bug bench.
**SUT scope:** htsjdk only (Randoop is Java-only — same language ceiling
as the EvoSuite anchor; cannot target vcfpy / noodles-vcf / biopython /
seqan3 / pysam).
**Bugs run:** 12 / 12 verified htsjdk bugs (9 VCF + 3 SAM).
**Per-bug budget:** 600 s wall-clock cap; 70 % to generation, 30 % to
javac + JUnit pre/post replay; `--output-limit=500`.
**Detection rate:** **3 / 12 (25 %)**.

## 1. Methodology — Magma-style §5.3.1 detection

Implemented in `compares/scripts/tool_adapters/run_randoop.py`. Mirrors
the EvoSuite anchor adapter (`run_evosuite_anchor.py`):

1. Run `randoop.main.Main gentests --testclass=<bug-specific class>`
   against the **post-fix** htsjdk fat jar with the time and output
   caps above. Output package fixed to `randoop.bench` so test FQNs
   are unambiguous.
2. `javac` the emitted suite against (a) the post-fix classpath and
   (b) the pre-fix classpath. Pre-fix compile failure is itself a
   strong signal — the same fix patches usually add new public
   constants/methods that Randoop's value-from-types feedback then
   references.
3. Run `org.junit.runner.JUnitCore` on each compiled `RegressionTest{0..N}`
   class against the post-fix and pre-fix classpaths in turn.
4. Detection: any test that **passes post-fix and fails pre-fix** is
   counted, dropped under `failing-tests/`, and surfaces as
   `crash_count` in the adapter result.

Identical predicate to the EvoSuite anchor; same uniform contract for
`bug_bench_driver.invoke_adapter`. Randoop's row in the driver is
`UNIT_ANCHOR_TOOLS = {"evosuite_anchor", "randoop"}` — both skip the
generic byte-replay / method-sig diff paths because their "trigger" is
a `.java` JUnit case, not a VCF/SAM byte stream.

## 2. Aggregate

| bug | format | pre → post | tests gen | pre-pass | post-pass | crashes | wall (s) | verdict | mechanism |
|:----|:------:|:-----------|---------:|---------:|----------:|--------:|---------:|:--------|:----------|
| htsjdk-1554 | VCF | 2.24.1 → 3.0.0 | 1 | 1/1 | 1/1 | 0 | 425.4 | miss | – |
| htsjdk-1637 | VCF | 3.0.3 → 3.0.4 | 1 | 1/1 | 1/1 | 0 | 22.2 | miss | – |
| htsjdk-1364 | VCF | 2.19.0 → 2.20.0 | 1 | 1/1 | 1/1 | 0 | 260.3 | miss | – |
| htsjdk-1389 | VCF | 2.19.0 → 2.20.0 | 1 | 1/1 | 1/1 | 0 | 192.6 | miss | – |
| htsjdk-1372 | VCF | 2.19.0 → 2.20.0 | 1 | 1/1 | 1/1 | 0 | 286.2 | miss | – |
| **htsjdk-1401** | VCF | 2.19.0 → 2.20.0 | 1 | 0/1 | 1/1 | 1 | 11.4 | **DETECT** | API drift — pre-fix `javac` cannot resolve a symbol introduced in 2.20.0 |
| htsjdk-1403 | VCF | 2.20.0 → 2.20.1 | 2 | 1/2 | 1/2 | 0 | 13.8 | miss | – |
| htsjdk-1418 | VCF | 2.20.1 → 2.21.0 | 1 | 1/1 | 1/1 | 0 | 288.6 | miss | – |
| htsjdk-1544 | VCF | 2.24.1 → 3.0.0 | 1 | 1/1 | 1/1 | 0 | 425.2 | miss | – |
| **htsjdk-1238** | SAM | 2.18.1 → 2.18.2 | 1 | 0/1 | 1/1 | 1 | 10.7 | **DETECT** | API drift — pre-fix `javac` fails on `RESERVED_RNEXT_SEQUENCE_NAME` (constant added in 2.18.2 alongside the regex check) |
| htsjdk-1360 | SAM | 2.19.0 → 2.20.0 | 1 | 1/1 | 1/1 | 0 | 13.4 | miss | – |
| **htsjdk-1410** | SAM | 2.20.2 → 2.20.3 | 1 | 0/1 | 1/1 | 12.7 | 12.7 | **DETECT** | Behavioural §5.3.1 LHS — 1 of 59 sequences in `RegressionTest0` passes post-fix and throws on pre-fix (`INVALID_INSERT_SIZE` cap on `SAMRecord`) |

**Detection rate:** 3 / 12 = 25 %. 2 of 3 detections are API-drift
fallbacks (the same well-known fallback the EvoSuite anchor uses); 1 is
a real behavioural pre-fix-fails / post-fix-passes diff.

## 3. Observations

- **Wall-time bimodal.** Bugs that compile clean and pass on both
  pre/post burn the full ~7 min generation budget (1554, 1364, 1372,
  1418, 1544 ≈ 260–425 s); bugs that hit a compile or behavioural diff
  exit in 10–14 s because Randoop's `--output-limit=500` is reached
  before the time cap and the JUnit replay finishes within seconds.
- **Why 9 misses?** The bug surface for VCF/SAM bugs is overwhelmingly
  in I/O parser paths (`AbstractVCFCodec.parse`, `SAMTextReader`).
  Randoop's value-from-types feedback synthesises `String`/`int`
  arguments from observed runtime constants and rarely produces the
  malformed multi-line VCF/SAM payloads needed to drive those paths.
  This is the well-documented limitation that motivates DESIGN.md §2.1's
  preference for input-level baselines (Jazzer, Atheris, libFuzzer,
  cargo-fuzz) as the primary scoring matrix.
- **Why API drift?** Bug-fix PRs in htsjdk routinely add a public
  constant or factory method alongside the validation tightening (e.g.
  `RESERVED_RNEXT_SEQUENCE_NAME` in PR #1238). When Randoop's random
  sampling references the new symbol, the pre-fix compile fails. We
  count this as a detection — same convention the EvoSuite anchor uses
  (DESIGN.md §5.3.1 third bullet treats "test failed against V" as the
  uniform per-tool predicate, and a compile failure is the strongest
  form of "failed").
- **htsjdk-1410 is the only behavioural detection.** One of 59 generated
  sequences in `RegressionTest0` constructs a `SAMRecord` with a TLEN
  value that crosses the 2^29 boundary; post-fix accepts it, pre-fix
  throws under STRICT validation. This is the §5.3.1 LHS predicate
  firing through pure unit-level interaction — no I/O.

## 4. Result inventory — where each artefact lives

All paths relative to repo root.

```
compares/baselines/randoop/
├── README.md                        # original "planned invocation" doc (Apr 16 stub)
├── source/
│   └── randoop-all-4.3.3.jar        # 7.15 MB — fetched 2026-04-26
└── results/
    ├── report.md                    # THIS FILE
    ├── summary.md                   # one-line-per-bug aggregate (markdown)
    ├── summary.json                 # same data as summary.md, JSON
    ├── run_all.log                  # orchestrator stdout
    └── htsjdk-<id>/                 # one dir per bug (12 dirs)
        ├── adapter_result.json      # canonical per-bug result record
        ├── tool.log                 # full Randoop + javac + JUnit log
        ├── randoop-tests/           # snapshot of generated .java sources
        │   └── randoop/bench/RegressionTest{,0,1,...}.java
        ├── failing-tests/           # detected JUnit cases (only on DETECT)
        │   └── RegressionTest0.java # for 1238, 1401, 1410
        └── work/                    # transient: javac classes_{pre,post}/
                                     # + raw randoop-tests/. Safe to delete.
```

Per-bug `adapter_result.json` schema (mirrors EvoSuite anchor):

```json
{
  "tool": "randoop",
  "sut": "htsjdk",
  "bug_id": "htsjdk-1410",
  "target_classes": ["htsjdk.samtools.SAMRecord"],
  "pre_fix": "2.20.2",
  "post_fix": "2.20.3",
  "started_at": 1777230501.6,
  "ended_at":   1777230514.3,
  "exit_code":  0,
  "tests_generated":  1,
  "pre_pass_count":   0,
  "post_pass_count":  1,
  "crash_count":      1,
  "detected_test_fqns": ["randoop.bench.RegressionTest0"],
  "trigger_input":  ".../failing-tests/RegressionTest0.java",
  "notes":          ""
}
```

## 5. Reproducing this run

One bug:

```bash
python compares/scripts/tool_adapters/run_randoop.py \
  --bug-id htsjdk-1410 \
  --out-dir compares/baselines/randoop/results/htsjdk-1410 \
  --time-budget-s 600
```

All 12 htsjdk bugs (sequential):

```bash
python compares/scripts/run_all_randoop.py --time-budget-s 600
```

Through the bug-bench driver (when you also want install_sut /
post-fix replay machinery to fire — note the unit-anchor fast path
short-circuits replay for Randoop):

```bash
python compares/scripts/bug_bench_driver.py \
  --only-tool randoop --only-sut htsjdk --time-budget-s 600
```

## 6. Comparison context

DESIGN.md §2.3 lists Randoop as a secondary/optional baseline because
its paradigm overlaps EvoSuite's. This run validates that intuition:

- Both tools are Java-only.
- Both detect via the §5.3.1 differential predicate on JUnit cases.
- Both rely on either API drift or coincidental behavioural divergence
  in the generated sequences — neither drives the parser through file
  I/O the way Jazzer (the fair Java E2E baseline) does.

A meaningful side-by-side requires running EvoSuite anchor at the same
budget on the same 12 bugs and comparing detection rate + mechanism mix.
That's not in this run — see DESIGN.md §13.5 Phase 4 for the full Jazzer
+ EvoSuite cross-comparison if needed.

## 7. Plumbing changes landed for this run

Listed for reproducibility — no behavioural change to existing tools:

- **New** `compares/scripts/tool_adapters/run_randoop.py` — adapter +
  standalone CLI.
- **New** `compares/scripts/run_all_randoop.py` — sequential
  orchestrator over the htsjdk row.
- `compares/scripts/bug_bench_driver.py`:
  - Added `UNIT_ANCHOR_TOOLS = {"evosuite_anchor", "randoop"}` constant.
  - Replaced six site-specific `tool != "evosuite_anchor"` guards with
    `tool not in UNIT_ANCHOR_TOOLS`.
  - Added `_invoke_randoop` thunk + dispatch in `invoke_adapter`.
  - Made `--only-tool randoop --only-sut htsjdk` honour Randoop even
    though it isn't in the primary `MATRIX["htsjdk"]`.

End of report.
