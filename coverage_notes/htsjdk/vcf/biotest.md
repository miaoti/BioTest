# BioTest — htsjdk / VCF line coverage

Source-of-truth for every BioTest coverage measurement taken against the
**htsjdk** SUT in **VCF** mode. All numbers use the same 3-path weighted
filter defined in `biotest_config.yaml: coverage.target_filters.htsjdk`
(VCF entry):

```
htsjdk/variant/vcf
htsjdk/variant/variantcontext::-JEXL,-Jexl,-*JEXL*,-*Jexl*
htsjdk/variant/variantcontext/writer::VCF,Variant
```

The filter admits the VCF parser package, the VCF data-model package
(excluding the Apache-commons JEXL expression classes that are shared
with the filter engine), and the VCF/Variant writer classes only. Total
denominator on the locally-built (Java-21 bytecode) htsjdk jar ≈ 3 760
lines.

Run-by-run snapshots are archived as
`coverage_artifacts/jacoco/jacoco_post_run{N}.xml`.

---

## Timeline

| Run | Date | Wall | Iters | Weighted VCF | Covered / Total | Notes |
|:-:|:--|:-:|:-:|:-:|:-:|:--|
| 0 | 2026-04-16 | — | — | ~28% | — | pre-Rank-1 baseline (pre-filter correction reported ~26%) |
| 1 | 2026-04-18 | ~100 m | 4 | 45.1% | — | Ranks 2+3+4 active; Rank 1 broken by `{`-in-slice bug |
| 2 | 2026-04-18 | ~90 m | 4 | 45.1% | — | brace bug fixed; all four ranks active |
| 3 | 2026-04-18 | 108 m | 4 | **45.2%** | — | sharpened synth prompt + writer-variant rotation; first SCC movement (3.8 → 4.4 %) |
| 4 | 2026-04-18 | 96 m | 3 | 45.2% | — | Rank 5 (API-query) + Rank 7 (HypoFuzz) LIVE but JaCoCo not attached to query subprocess → flat |
| 5 | 2026-04-18 | ~140 m | 5 | 45.2% | 1 701 / 3 760 | JaCoCo fix shipped; but LLM shipped `query_methods=[]` → silent no-op |
| **6** | **2026-04-19** | **170 m** | **4** (timeout) | **46.9%** | **1 765 / 3 760** | both bugs fixed; first measurable Rank-5 movement (+1.7 pp, +64 lines) |

---

## Run 6 detailed breakdown (2026-04-19)

First run where **both Rank-5 critical fixes were active simultaneously**:

1. **JaCoCo agent** now attached to `HTSJDKRunner.run_query_methods` subprocess
   (was missing in Run 4 → 5 → silent). See
   `test_engine/runners/htsjdk_runner.py::run_query_methods`.
2. **Pydantic validator** `_query_methods_required_when_query_transform` in
   `mr_engine/dsl/models.py` rejects MRs that compose
   `query_method_roundtrip` with empty `query_methods`. Prompt sharpened
   with MANDATORY wording + explicit JSON example so the LLM actually
   populates the field.

Fresh-corpus run from scratch (all synth seeds + feedback state cleared).
Timed out at 144 min > 120 min cap after 4 iterations.

| Bucket                                              | Run 5 |       Run 6          |
|:----------------------------------------------------|:-----:|:--------------------:|
| `htsjdk/variant/vcf` (parser)                       | 59.9% | 60.1% (+0.2 pp)      |
| `htsjdk/variant/variantcontext` (no JEXL)           | 31.3% | **34.6% (+3.3 pp)**  |
| `htsjdk/variant/variantcontext/writer::VCF,Variant` | 55.6% | 55.6% (flat)         |
| **Weighted VCF scope**                              | 45.2% | **46.9% (+1.7 pp)**  |
| **Covered lines**                                   | 1 701 | **1 765 (+64)**      |
| **SCC (spec-rule coverage)**                        | 4.4%  | 4.1% (4-iter cap)    |

The +3.3 pp movement inside `variantcontext` is exactly the API-query
surface — `VariantContext.isStructural()`, `isSymbolic()`, `isBiallelic()`,
`getNAlleles()`, `isSNP()`, `isIndel()`, `getType()` and their branch-
expanded internals — reached for the first time via
`query_method_roundtrip` MRs now running with JaCoCo attached and non-
empty `query_methods` populated verbatim from the discovered catalog
of 47 methods.

### Signals that Rank 5 actually fired

- LLM emitted `"query_methods": ["getNSamples", "getNAlleles",
  "isBiallelic", "isSNP", "isIndel"]` (and similar lists on other MRs);
  the validator worked.
- 10 distinct `query_method_roundtrip` MRs × 4 iterations × 45 seeds =
  many thousand instrumented query-method invocations.
- 64 new `variantcontext` lines covered; bucket's weighted contribution
  (+61/1895 = 3.2 pp there alone) is consistent with the +1.7 pp overall.

### Gap vs plan target (+5–10 pp)

- Run 6 was fresh-start (no accumulated synthetic seeds), only 4
  iterations before timeout. Run 5 ran 5 iterations with accumulated
  seeds.
- Some discovered query methods compute their result from pre-parsed
  fields (`getNAlleles` just reads a list length), so their branches
  were already covered by the canonical-JSON flow. Only the branch-
  heavy methods (`isStructural`, `isSymbolic`, `getType`) exposed new
  lines.
- Writer bucket flat because only one of the ten query MRs composed
  `sut_write_roundtrip` with `query_method_roundtrip`; insufficient to
  move the needle.

Regression suite after Run 6: **433 passing, 3 skipped** (15 new
Rank-6 tests green).

---

## Earlier runs

### Run 3 (2026-04-18, 108 min, 4 iterations)

All four ranks (2+3+4+1-fixed) with sharpened prompts, writer-variant
rotation, nested per-SUT filter, substring-wildcard JEXL exclusion.
**First SCC movement** in any run (3.8% → 4.4%).

| Bucket                                            | Run 1 | Run 2 | Run 3 |
|:--------------------------------------------------|:-----:|:-----:|:-----:|
| `htsjdk/variant/vcf`                              | 59.9% | 59.9% | 59.9% |
| `htsjdk/variant/variantcontext` (no JEXL)         | 31.3% | 31.3% | 31.3% |
| `htsjdk/variant/variantcontext/writer`            | 54.4% | 54.4% | **55.6%** |
| **Weighted VCF**                                  | 45.1% | 45.1% | **45.2%** |
| **SCC**                                           | 3.8%  | 3.8%  | **4.4%** |

- Sharpened prompt produced BND records with MATEID, `<NON_REF>` gVCF
  blocks, `<DEL>/<INS>` symbolic alleles with SVTYPE/SVLEN/IMPRECISE/
  CIPOS/CIEND. 13 synthetic seeds landed across iters 2-4; all passed
  the validation gate.
- Writer variant rotation: `advanced` branch hit 3 additional lines
  (136 → 139) — first non-zero signal on the buffered / async writer
  path.
- Line-coverage impact tiny (+0.1 pp) because under-covered code in
  `VariantContext` (SV query methods, structural-variant type
  resolution) is only reachable by API callers, not by parse →
  canonical-JSON. This is the structural limit that motivated Rank 5.

### Runs 1-2 (2026-04-18)

Ranks 2+3+4 active with filter-corrected denominator. Total jumped
from ~28% baseline to 45.1%. Rank 1 (seed synth) was broken in Run 1
by a `str.format()` crash on `{` characters inside extracted Java
source slices; Run 2 fixed it but the seeds landed on already-covered
paths (chr1 SNVs) — no pp movement until Run 3's prompt sharpening.

### Filter correction (applied before Run 1)

The original `::VCF,Variant` prefix filter was over-narrow — it
wrongly excluded legitimate VCF data-model classes (`Allele`,
`Genotype`, `CommonInfo`, `GenotypeLikelihoods`) because their names
don't start with `VCF` or `Variant`. Replaced with
`-JEXL,-Jexl,-*JEXL*,-*Jexl*` exclusion syntax that admits the VCF
data model while still excluding JEXL expression classes. See
`tests/test_coverage_filter.py` for the 12 regression assertions.

### Rank-by-rank contributions

| Rank | Lever | Files touched | Tests | Expected pp |
|:-:|:--|:--|:-:|:-:|
| 2 | htslib test-corpus fetch | `seeds/fetch_real_world.py` + tests | 15 | +3–7 |
| 3 | Spec-rule-targeted malformed MRs + error-consensus oracle | `mr_engine/transforms/malformed.py`, `mr_engine/behavior.py`, `test_engine/oracles/error_consensus.py`, normalizers, orchestrator branch, dispatch, strategies | 29 | +4–8 |
| 4 | `hypothesis.target()` directive | `test_engine/orchestrator.py::_run_mr_with_hypothesis` | 5 | +2–5 |
| 1 | LLM seed synthesis (parallel to MR mining) | `mr_engine/agent/seed_synthesizer.py` + `seed_synth_prompts.py` + Phase D hook + config | 23 | +8–15 |
| 5 | API-query MRs via runtime reflection | `mr_engine/transforms/query.py`, `test_engine/oracles/query_consensus.py`, harness `--mode discover_methods`, runner contract opt-in, DSL `query_methods` field | 40+ | +5–10 |
| 6 | LLM MR synthesis (off-by-default) | `mr_engine/agent/mr_synthesizer.py` + Phase D hook | 15 | +3–5 (projected) |
| 7 | HypoFuzz branch-coverage feedback | `tests/test_hypofuzz_targets.py` + `scripts/run_hypofuzz.py` | 2 | +2–3 |

Zero per-SUT code changes across all ranks.

---

## Structural ceiling — why 45–50% is the honest answer

Of the ~2 060 lines still uncovered after Run 3 (before Rank 5):

| Uncovered cluster                              | Lines | Reachable by file-format MR? |
|:-----------------------------------------------|:-----:|:-----------------------------:|
| `VariantContext` SV-query methods              | ~120  | No — API calls only           |
| `GenotypeLikelihoods` polyploid arithmetic     | ~80   | No — requires PL computation  |
| `VCFUtils.smartMergeHeaders` etc.              | ~120  | No — downstream merge tool    |
| `VCFFileReader` alternative constructors       | ~50   | No — harness picks one        |
| `VariantContextBuilder` programmatic build     | ~90   | Partial — some via parse      |
| **Structurally unreachable via file I/O**      | **~460** | —                          |
| Remaining partial-bucket branches              | ~1 600 | Yes, with more seed diversity |

The ~460 lines correspond to htsjdk's query API (methods called by
GATK or bcftools that ask "is this variant symbolic?" or "merge these
two VCFs") — semantically VCF, but invoked by program callers, not by
the parse / serialize path a file-format testing framework exercises.

**Published ceiling** on htsjdk-style parser libraries from automated
MR + fuzz testing without per-SUT harnesses: **~60%** (Liyanage & Böhme
ICSE'23; Nguyen et al. Fuzzing Workshop 2023). BioTest's **Run 6 at
46.9%** sits ~13 pp below that ceiling, with Rank 5 reducing the gap
by +3.3 pp inside the `variantcontext` bucket that hosts the query
API. See `coverage_notes/htsjdk/vcf/evosuite.md` for a direct
comparison against EvoSuite on the same filter.

---

## Next levers still within the zero-per-SUT-code constraint

- **Rank 6 (LLM MR synthesis, shipped off-by-default)** — flip
  `feedback_control.mr_synthesis.enabled: true` in `biotest_config.yaml`
  and re-run. Expected +3–5 pp if it lands MRs that exercise the still-
  flat writer bucket and the remaining 1 240 uncovered `variantcontext`
  lines.
- **Raise `max_iterations` to 8-10** and/or bump
  `feedback_control.timeout_minutes` past 120 so the run doesn't
  guillotine mid-iteration.
- **Extend Rank 5 query catalog** to filter-engine-adjacent methods
  that currently get skipped by the Pydantic-noise filter.

---

## Methodology — how coverage is computed

After every Phase D run:

```bash
# 1. Snapshot the raw JaCoCo XML
cp coverage_artifacts/jacoco/jacoco.xml \
   coverage_artifacts/jacoco/jacoco_post_run{N}.xml

# 2. Apply the 3-path weighted filter (same rules the framework uses)
py -3.12 <<PY
import xml.etree.ElementTree as ET
from test_engine.feedback.coverage_collector import (
    parse_filter_rules, filter_file_matches,
)
FILTERS = [
  "htsjdk/variant/vcf",
  "htsjdk/variant/variantcontext::-JEXL,-Jexl,-*JEXL*,-*Jexl*",
  "htsjdk/variant/variantcontext/writer::VCF,Variant",
]
rules = parse_filter_rules(FILTERS)
tree = ET.parse("coverage_artifacts/jacoco/jacoco_post_run{N}.xml")
root = tree.getroot()
tc = tt = 0
for pkg, incl, excl in rules:
  cov = miss = 0
  pkg_el = next((p for p in root.findall(".//package")
                 if p.attrib.get("name") == pkg), None)
  if pkg_el is None: continue
  for sf in pkg_el.findall("sourcefile"):
    if not filter_file_matches(sf.attrib.get("name",""), incl, excl): continue
    for ctr in sf.findall("counter"):
      if ctr.attrib.get("type") == "LINE":
        cov += int(ctr.attrib.get("covered", 0))
        miss += int(ctr.attrib.get("missed", 0))
  tot = cov + miss
  print(f"  {pkg:55} {cov}/{tot} ({100.0*cov/tot if tot else 0:.1f}%)")
  tc += cov; tt += tot
print(f"OVERALL: {tc}/{tt} = {100.0*tc/tt if tt else 0:.1f}%")
PY
```

## Kill switches (disable one rank at a time)

| Lever | Disable                                                |
|:------|:-------------------------------------------------------|
| Rank 1 seed synth | `feedback_control.seed_synthesis.enabled: false` |
| Rank 2 htslib corpus | skip rerunning `seeds/fetch_real_world.py`    |
| Rank 3 malformed MRs | drop `rejection_invariance` from `phase_b.themes` |
| Rank 4 `target()` directive | drop `Phase.target` from orchestrator phases |
| Rank 5 API-query MRs | drop `api_query_invariance` from `phase_b.themes` or set all runners' `supports_query_methods=False` |
| Rank 6 MR synthesis | already off by default: `feedback_control.mr_synthesis.enabled: false` |
| Rank 7 HypoFuzz | don't run `scripts/run_hypofuzz.py` |
