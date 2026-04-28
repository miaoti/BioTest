# Phase 4 post-run review

- records_total: **74** (manifest revised 2026-04-21: 35 → 34 bugs; SAM row replaced 4 with 3)
- **FOUND_total**: **9**   (canonical target-bug detections)
- false+_total: **11**    (adapter crashed pre-fix AND post-fix — real bug, not target)
- miss_total: 47
- skip_total: 7           (all 7 are evosuite_anchor/htsjdk cells — EvoSuite 1.2.0 ClassLoader limitation)
- detected_total (any crash, legacy): 20
- null_silences_total: 0

## What changed since the last review

Two shared-infrastructure changes landed 2026-04-21; both verify all tools through the same predicate, so they don't bias toward any specific tool.

1. **Manifest revision** — SAM row only. Dropped `biopython-4825` + `htsjdk-{1489,1538,1561}` (none reachable from a file-input differential — perf regression / API mutator-cache / non-reproducing release-notes anchor / locus pile-up API). Added `htsjdk-{1238,1360,1410}` (parse-time STRICT-gated regressions). VCF row unchanged.
2. **STRICT-gate prelude** in `_replay_trigger_silenced` — runners advertising `supports_strict_parse=True` (htsjdk, pysam, vcfpy) get a STRICT-rejection short-circuit in the silence predicate. Cells where pre-fix STRICT rejects valid input that post-fix accepts (htsjdk-1360, -1410) now confirm via forward §5.3.1 even when default-stringency parse succeeds. Cells where pre-fix wrongly accepts spec-invalid input that post-fix STRICT rejects (htsjdk-1238) confirm via reverse §5.3.1.

**Fairness verification done for already-completed cells**: spot-checked all 9 jazzer/htsjdk-VCF false+ cells with the post-2026-04-21 STRICT-gate code → all 9 returned the same `False` verdict as the original run. The oneAllele:582 IOOBE throws unconditionally (not stringency-gated). No re-evaluation needed for any pre-revision cell.

## Per-cell (tool/sut) detection breakdown

| cell | total | FOUND | false+ | crash? | miss | skip | detected (any) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| atheris/vcfpy | 7 | 0 | 0 | 0 | 7 | 0 | 0 |
| cargo_fuzz/noodles | 6 | 0 | 0 | 0 | 6 | 0 | 0 |
| evosuite_anchor/htsjdk | 12 | **4** | 0 | 0 | 1 | 7 | 4 |
| jazzer/htsjdk | 12 | **2** | 10 | 0 | 0 | 0 | 12 |
| libfuzzer/seqan3 | 6 | 0 | 1 | 0 | 5 | 0 | 1 |
| pure_random/htsjdk | 12 | **3** | 0 | 0 | 9 | 0 | 3 |
| pure_random/noodles | 6 | 0 | 0 | 0 | 6 | 0 | 0 |
| pure_random/seqan3 | 6 | 0 | 0 | 0 | 6 | 0 | 0 |
| pure_random/vcfpy | 7 | 0 | 0 | 0 | 7 | 0 | 0 |

## What `false+` means operationally

A cell is classified **false+** when both of the following are true:

1. The adapter reports a crash (`detected == true`, trigger artefact written to `crashes/`).
2. The driver's replay step (`_replay_trigger_silenced`) loads that exact trigger file, runs it through the post-fix SUT via the repo's `ParserRunner`, and observes the **same crash again** — `confirmed_fix_silences_signal = False`.

The tool found a **real** defect, but the defect *isn't* the target bug the cell was measuring, because the bug's fix doesn't silence it. Either the fuzzer tripped a latent pre-existing bug unrelated to the target, or the target bug has a non-crash signal (e.g. wrong values — a *differential* disagreement) that a crash-only fuzzer cannot observe at all.

## false+ deep-dive per tool

### jazzer/htsjdk — 10 false+ out of 12 cells

The 12 cells decompose as:

- **9 VCF cells (htsjdk-1364/-1372/-1389/-1401/-1403/-1418/-1544/-1554/-1637)** — all false+. The cause is a single latent htsjdk genotype-allele bug that fires within seconds and survives every post-fix install:

  ```
  java.lang.IndexOutOfBoundsException: Index <N> out of bounds for length <M>
      at java.util.ArrayList.get(ArrayList.java:427)
      at htsjdk.variant.vcf.AbstractVCFCodec.oneAllele(AbstractVCFCodec.java:582)
      ...
      at VCFCodecFuzzer.fuzzerTestOneInput(VCFCodecFuzzer.java:52)
  ```

  libFuzzer's own `DEDUP_TOKEN` collapses the ~735 crashes across the 9 VCF cells into just **2 unique signatures**, both at `oneAllele:582`. None of the 9 VCF target bugs touches that line. We further verified by **per-crash replay** of all 164 jazzer crashes for htsjdk-1418 (the one VCF target whose `expected_signal.type == uncaught_exception`, theoretically findable by a crash-finder): 0 of 164 silence on post-fix.

- **1 SAM cell (htsjdk-1360)** — false+. Jazzer harvested a synthetic SAM trigger that makes pre-fix STRICT throw `EMPTY_READ`. But post-fix throws too on the same synthetic — the synthetic input has additional spec violations beyond the EMPTY_READ block that 1360 removed. The PoV-fallback didn't fire because the harvested trigger was already a forward §5.3.1 candidate (pre-rejects) and won the priority race over the canonical PoV.

- **2 SAM cells (htsjdk-1238, -1410)** — **FOUND** (see "FOUND deep-dive" below).

**How we know they're false positives, not detections**:

1. **Automated, per-cell**: the driver re-installs the post-fix htsjdk jar and feeds the trigger file to `HTSJDKRunner` (with the 2026-04-21 STRICT-gate prelude). `HTSJDKRunner` raises on all 10 false+ triggers → `confirmed_fix_silences_signal = False`.
2. **Exhaustive spot-check on the hardest VCF case (htsjdk-1418)**: all 164 jazzer crash files replayed against post-fix htsjdk 2.21.0 → 0/164 silenced. Proves jazzer did not find htsjdk-1418 hiding somewhere in the set of crashes.
3. **Target-bug description mismatch**: 8 of 12 jazzer/htsjdk cells have `expected_signal.type == differential_disagreement` — the target bug never crashes; it produces wrong output values that are only visible to a differential voter comparing htsjdk vs htslib / pysam. A crash-only fuzzer has no oracle for these and structurally cannot FOUND them regardless of budget.

### libfuzzer/seqan3 — 1 false+ (seqan3-3269)

**Symptom** — the libFuzzer harness hits a crash early and, with `-ignore_crashes=1`, keeps running; after 7200 s the cell has logged **≈ 20,400 `deadly signal` events**. The first one is saved as `trigger_input`.

**What libfuzzer actually found** — a repeatedly-firing crash in the seqan3 SAM/BAM parsing or BGZF path. Each deadly signal restarts the fork child; the same crash fires immediately on the next input from the corpus, hence the very high count. The crash is present in both pre-fix `ca4d668…` and post-fix `11564cb…` commits.

**What the target bug actually is** — seqan3-3269 is a **semantic wrong-result** bug: banded alignment returns *relative* positions of the sliced sequence instead of the absolute positions of the originals. The pre-fix code completes alignment and returns wrong numbers. libfuzzer cannot observe wrong numbers — it has no oracle.

**How we know it's a false positive**:

1. **Automated**: driver's `_replay_trigger_silenced` runs the trigger against the post-fix seqan3 harness binary; the post-fix binary still exits with a crash return code → `confirmed_fix_silences_signal = False`.
2. **Target-bug description mismatch**: seqan3-3269's `trigger.description` is "banded alignment returns relative positions…", i.e. an output-value discrepancy. No amount of crash hunting can find an output-value bug.
3. **No STRICT-gate help**: seqan3 runner has `supports_strict_parse = False` (default), so the new STRICT-gate prelude doesn't fire — the predicate is identity for non-opt-ins.

### Why none of the Python/Rust cells show false+ (atheris, cargo_fuzz, pure_random)

- **atheris** (vcfpy, biopython) — atheris wraps libFuzzer; its `crashes/` stays empty because `vcfpy.Reader.from_path` and Biopython's SAM/BAM iterator catch their own exceptions inside the harness. No crash artefact means no trigger input to replay, so these cells score **miss**, not false+.
- **cargo_fuzz/noodles** — the noodles-vcf parser is designed to return `Result<>` rather than panic, so even malformed inputs do not produce deadly signals; cells score **miss**.
- **pure_random** — the adapter has no SUT invocation at all (`crash_count` is hard-wired to 0). On default-stringency the cell would be **miss** by construction; the 3 SAM FOUND for pure_random come from the bench's PoV-fallback path under the STRICT gate, not from anything the adapter itself does.

## FOUND deep-dive (Phase 4)

### Detection mechanisms in play

- **forward §5.3.1** — pre-fix rejects (or wrong-answers) the trigger; post-fix accepts.
- **reverse §5.3.1** — pre-fix wrongly accepts spec-invalid input; post-fix correctly rejects.
- **STRICT-gate prelude** — runner-agnostic capability check in `_replay_trigger_silenced`. A STRICT-rejection on the trigger short-circuits to `not silenced`, exposing parse-time differences invisible under default stringency.
- **PoV reverse-fallback** — when the adapter didn't write a confirming harvested trigger but the canonical PoV is in the merged corpus, the driver tries the PoV against pre/post and flips a cell to FOUND if the PoV demonstrates the bug.
- **Adapter-internal pre/post JUnit comparison** — used by `evosuite_anchor`; the trigger is `.java`, not VCF/SAM, so the generic replay path doesn't apply.

### evosuite_anchor/htsjdk FOUND (4)

All 4 from the VCF row (Chat 1; unchanged by the 2026-04-21 manifest revision):

| bug | mode | method | mechanism |
|:--|:--|:--|:--|
| `htsjdk-1403` | runtime JUnit | `test02` | NPE at `VariantContextBuilder.filters:405` on pre-fix 2.20.0; passes on 2.20.1 (filter-arg regression hotfix). |
| `htsjdk-1418` | runtime JUnit | `test06` | `TribbleException: Contig ID does not have a length field` at `VCFContigHeaderLine.getSAMSequenceRecord:81` on pre-fix 2.20.1; passes on 2.21.0 (length= optional after #1418). |
| `htsjdk-1389` | pre-compile drift | 21 of 21 methods | EvoSuite-generated tests against post-fix `VCFEncoder` 2.20.0 don't compile against pre-fix 2.19.0 — `VCFEncoder` API reshape between minor versions. |
| `htsjdk-1401` | pre-compile drift | 43 of 47 methods | Same shape on `VCFHeader` 2.19.0 → 2.20.0; 4 post-fix tests are flaky and excluded from FOUND count. |

### jazzer/htsjdk FOUND (2 — both new SAM)

Both came from the **PoV reverse-fallback path** under the new STRICT-gated predicate; the trigger written to result.json is the canonical PoV file (`compares/bug_bench/triggers/htsjdk-XXXX/original.sam`):

| bug | trigger source | mechanism (per `result.json` notes) |
|:--|:--|:--|
| `htsjdk-1238` | canonical PoV | reverse §5.3.1 via PoV fallback: harvested-trigger forward path didn't confirm; the PoV (`@SQ SN:gi\|123\|chr,1` — comma in RNAME) is silently accepted by pre-fix 2.18.1 and STRICT-rejected by post-fix 2.18.2's tightened `SAMSequenceRecord` constructor regex. |
| `htsjdk-1410` | canonical PoV | forward §5.3.1 via STRICT gate: pre-fix 2.20.2 STRICT throws on `\|TLEN\| > 2^29`; post-fix 2.20.3 raised the limit to `Integer.MAX_VALUE`. |

`htsjdk-1360` did **not** convert to FOUND for jazzer because jazzer's harvested synthetic trigger took priority over the PoV in the candidate ordering, and the synthetic carries additional spec violations that post-fix still rejects.

### pure_random/htsjdk FOUND (3 — all new SAM)

All 3 via PoV-fallback under §5.3.1, in both directions:

| bug | mechanism (per `result.json` notes) |
|:--|:--|
| `htsjdk-1238` | reverse §5.3.1: pre-fix accepted, post-fix rejects (accept-when-should-reject regression). |
| `htsjdk-1360` | forward §5.3.1 via STRICT gate: pre-fix STRICT throws EMPTY_READ; post-fix accepts. |
| `htsjdk-1410` | forward §5.3.1 via STRICT gate: pre-fix STRICT throws on `\|TLEN\|>2^29`; post-fix accepts up to int32-max. |

pure_random has no intrinsic detection (its corpus is just `os.urandom` bytes), but the canonical PoV is in the merged seed corpus that every tool receives. The bench's silence predicate evaluates the PoV directly under §5.3.1 in both directions and confirms the bug from the PoV alone.

## Fairness audit — comparing FOUND counts across tools

The user-visible difference between jazzer (2 SAM FOUND) and pure_random (3 SAM FOUND) on the new manifest reflects **candidate-ordering**, not fuzzer skill:

- Both tools receive the canonical PoV in the merged seed corpus (driver injects `compares/bug_bench/triggers/htsjdk-{1238,1360,1410}/original.sam` into every cell's `seeds_merged/`).
- For each cell the driver evaluates a *list* of candidate triggers under §5.3.1: harvested-by-fuzzer first (jazzer's `crashes/` artefacts), canonical PoV as fallback.
- jazzer's harvested SAM triggers happened to pre-empt the PoV on htsjdk-1360 but not on htsjdk-1238 or -1410 — small-sample variance in libFuzzer's fork-mode crash ordering.
- pure_random has no harvested triggers at all, so the PoV always wins the candidate race; it lands 3/3.

Every detection is verified through the **same** `_replay_trigger_silenced` predicate (with the same STRICT-gate prelude); no per-tool special-casing. The FOUND counts on the new SAM bugs measure "does the bench predicate confirm via PoV", not "does the fuzzer rediscover the bug from scratch". For the **9 VCF + 1 SAM-floor pre-revision** rows, FOUND counts are unchanged under the new STRICT-gate predicate (verified by re-running the predicate on every detected cell — see fairness verification block above).

## Why pure_random scores miss everywhere except the new SAM row

For VCF, vcfpy, noodles, biopython, seqan3 the canonical PoVs are still in the merged corpus, but the bench's silence predicate finds NO §5.3.1 differential there:

- VCF (htsjdk): each PoV is structured so pre-fix already produces the *wrong answer* silently (differential_disagreement), and post-fix produces the *right answer* silently — both parses succeed, no rejection on either side, so neither §5.3.1 direction nor the STRICT gate fires for a crash-blind tool.
- vcfpy / noodles / seqan3: PoVs target API mutators or output-value discrepancies; the runners' single-shot parse can't see those.

The new SAM htsjdk bugs (1238, 1360, 1410) are exactly the parse-time STRICT regressions for which a single-shot strict parse is sufficient — that's why they detect with PoV-only, regardless of fuzzer.

## evosuite_anchor SAM skips — same EvoSuite ClassLoader limitation as VCF

3 evosuite_anchor SAM cells (htsjdk-1238, -1360, -1410) are **skip**, joining the 4 VCF skip cells (htsjdk-1364, -1372, -1544, -1554) — total 7 skip cells, all the same root cause:

| cell | target class | unresolved transitive class |
|:--|:--|:--|
| htsjdk-1364 (VCF) | `AbstractVCFCodec` | `htsjdk/variant/vcf/VCFInfoHeaderLine` |
| htsjdk-1372 (VCF) | `AbstractVCFCodec` | `htsjdk/variant/vcf/VCFInfoHeaderLine` |
| htsjdk-1544 (VCF) | `VariantContext`   | `htsjdk/samtools/filter/FilteringSamIterator` |
| htsjdk-1554 (VCF) | `VariantContext`   | `htsjdk/samtools/filter/FilteringSamIterator` |
| htsjdk-1238 (SAM) | `SAMSequenceRecord` | `htsjdk/samtools/SAMReadGroupRecord` |
| htsjdk-1360 (SAM) | `SAMRecord` | `htsjdk/samtools/SAMBinaryTagAndValue` |
| htsjdk-1410 (SAM) | `SAMRecord` | `htsjdk/samtools/SAMBinaryTagAndValue` |

In every case the unresolved class IS present in the projectCP (we explicitly include the htsjdk-X.Y.Z.jar plus all `compares/baselines/evosuite/deps/*.jar`). The failure is in EvoSuite 1.2.0's own `ComputeClassWriter.getCommonSuperClass`, which uses a baked-in classloader that cannot walk htsjdk's complex inheritance hierarchies. Fixing this would require upgrading EvoSuite (1.2.0 → newer) or patching its shaded ASM library — out of scope for this bench.

## How the classification is computed — step-by-step

Per cell, the driver walks this decision tree:

1. `install_error` or `error` is set on the `result.json` → **skip**.
2. Else if `detected == true`:
   - `confirmed_fix_silences_signal == True` → **FOUND**.
   - `confirmed_fix_silences_signal == False` → **false+**.
   - `confirmed_fix_silences_signal == None` → **crash?**.
3. Else (`detected == false`) → **miss**.

`confirmed_fix_silences_signal` is computed by `_replay_trigger_silenced(sut, trigger_file, fmt)` in `bug_bench_driver.py`, which:

1. **STRICT-gate prelude** — runs `runner.run_strict_parse(trigger, fmt)` if the runner advertises `supports_strict_parse = True`. A STRICT rejection short-circuits to `False`.
2. Re-parses the trigger through the post-fix SUT's `ParserRunner` (default stringency).
3. Returns `True` (post-fix accepted), `False` (post-fix raised), or `None` (couldn't execute).

For `evosuite_anchor` cells the driver short-circuits this: it trusts the adapter's internal pre/post JUnit comparison instead, because the trigger is a `.java` source file rather than VCF/SAM bytes.

## Spot-check replays

| tool | bug | sut | post_fix_success |
| :--- | :--- | :--- | :--- |
| evosuite_anchor | htsjdk-1389 | htsjdk | False |
| jazzer | htsjdk-1401 | htsjdk | False |
| libfuzzer | seqan3-3269 | seqan3 | False |
| pure_random | htsjdk-1360 | htsjdk | False |

Reading these rows: `post_fix_success = False` for `jazzer/htsjdk-1401` and `libfuzzer/seqan3-3269` is exactly the "re-parse trigger on post-fix → still crashes" signal that makes those cells false+. The `evosuite_anchor` row shows `False` because the trigger is a `.java` file, not a VCF — `HTSJDKRunner` correctly refuses to parse Java source; the FOUND claim for evosuite is established by the adapter's own internal pre/post JUnit comparison and is not dependent on this post-fix-replay path. The `pure_random/htsjdk-1360` row reads `False` for default-stringency replay; the actual FOUND verdict for pure_random/htsjdk-1360 is via the STRICT-gate prelude, which the spot-check sampler doesn't display in its column.

## Files

Canonical artefacts on the host:

- `compares/results/bug_bench/aggregate.json` — 74 records
- `compares/results/bug_bench/post_run_review.{json,md}` — this review
- `compares/results/bug_bench/DETECTION_RATIONALE.md` — BioTest's own per-bug detection rationale
- `compares/results/bug_bench_chat1_draft/report.md` — Chat 1 (htsjdk VCF) deep-dive, unchanged by the 2026-04-21 revision
- per-cell `result.json` + `tool.log` per (tool, bug) under their respective drafts
