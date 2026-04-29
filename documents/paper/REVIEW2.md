# Second-pass review of "BioTest: Metamorphic Testing for Textual VCF and SAM Parsers"

## 1. Headline judgment update

**Weak reject.** The revision genuinely repairs five of the thirteen findings I flagged (M1, M5, M11, M12, M13), partially repairs another six (M2, M3, M6, M7, M8, M10), but fails to close M4 and M9, and the new bug-bench section (M1's repair) introduces fresh, paper-internal contradictions that I did not flag the first time. The headline "13/32" claim is now *technically defensible* but is also conspicuously fragile: 3 of 13 are PoV-fallback, the comparison set has no second differential-oracle baseline, and the only tools that "match" the paradigm are unit-level. The mutation-adequacy headline still rests on a corpus selected by kill-feedback, and the disclosure paragraph is paragraph-long but the artefact is not re-graded under outcome-fingerprint cmin to show the kill-aware variant is not the explanation. This is a meaningful improvement on a reject paper, not yet a top-tier paper.

## 2. Per-finding verdict on M1–M13

### M1. Real-bug benchmark exclusion — **Closed.**

`sections/bug_bench_section.tex` and `sections/bug_bench_table.tex` add a full subsection (`\S V.B`, `\label{sec:bug-bench}`) reporting the 32-bug, 8-tool, 4-SUT benchmark in exactly the form I demanded, with provenance pinned to `compares/results/bug_bench/PHASE4_FINAL_REPORT.md`. The 13/32 figure is split into 10 tool-found + 3 PoV-fallback, with Pure-Random's 3/3 PoV-fallback disclosed in the same column-footnote ($^\dagger$). The table's "false+" column reports the Jazzer 10-cell `oneAllele:582` IOOBE collision honestly. The abstract and introduction are updated consistently. The construct-validity gap I called out is genuinely closed: the paper now reports both the proxy and the bugs, and it is explicit that mutation kills are at $r{\approx}0.7$ (`evaluation_intro.tex` lines 10-12). What does not change is that the proxy-grade headline still leads in the abstract; that is a presentation choice I can live with given the bug-bench is now carried.

### M2. Kill-aware corpus minimisation circularity — **Partially closed.**

`design.tex` lines 372-416 now disclose the asymmetric `corpus_minimize.py` policy (kill-aware on Python SUTs, outcome-fingerprint on non-Python). The disclosure is competent and directly cites `vikram2023guiding` for the precedent. **What is still missing**: no quantification. The paper asserts that "the engine's actual scoring mutants every retained file's kill behaviour is as informative as on any other corpus member" — but this is an *assertion*, not a measurement. The minimum fix I asked for was either (i) re-run with outcome-fingerprint everywhere, or (ii) report the headline numbers under both policies and show the delta. Neither was done. The disclosure paragraph closes the *honesty* gap (a reviewer can no longer say it is hidden) but it does not close the *circularity* gap (the headline mutation score on vcfpy/biopython could still be inflated by the kill-aware selector relative to what an outcome-fingerprint selector would produce, and the paper does not show otherwise).

### M3. n=4 with $\sigma{=}0.00$ — **Partially closed.**

`mutation_score_section.tex` lines 38-55 add a "Statistical-inference posture under $n{=}4$" paragraph that admits the minimum exact $p$ is $0.029$, the Holm-Bonferroni-corrected $p$ is $\sim 0.17$, and $\hat{A}_{12}$ collapses to deterministic ordinal comparison on cells where both samples have $\sigma{=}0.00$. The paragraph also adds the small/medium/large $\hat{A}_{12}$ thresholds I asked for (`vargha2000critique` cited correctly). **What is still missing**: $n$ was not increased. The paper now correctly *frames* the statistics as descriptive on deterministic cells, but it still reports $\hat{A}_{12}{=}0.000$ and $\hat{A}_{12}{=}1.000$ in the headline prose. A reader who skims the table will read those as findings; the paragraph that contextualises them is buried two paragraphs above. This is honesty-on-paper without a methodological remedy. Acceptable for a revision; not yet what a reproducibility-strict reviewer would want.

### M4. Researcher-degree-of-freedom in MR curation — **Not closed.**

`threats.tex` lines 96-141 expand the disclosure of the curation pipeline and reference a "verbatim curation log" shipped with the artefact. **What is still missing**: this is paraphrase, not measurement. None of (a) the number of MR candidates proposed, (b) the per-candidate rejection rate, or (c) the per-MR contribution to the kill rate is reported in the paper. The threats paragraph admits the seed corpus is *not* pre-registered ("the seed corpus is part of the artefact distribution and is therefore frozen *before* mutation-adequacy or bug-bench grading; we do not blind the curation step from downstream performance, and the residual researcher degree-of-freedom is not fully quantifiable"). That is an honest disclosure, but it is not a fix — the paper *adds* an admission that the curation step is unblinded and proceeds anyway. The mitigation ("verbatim curation log shipped with the artefact") shifts the work from the paper to the artefact reviewer, which is the same evasion as the first version.

### M5. Abstract vs C2 contradiction — **Closed.**

`abstract.tex` lines 14-16 are now reworded to match C2: "no per-SUT metamorphic relation, no per-SUT oracle predicate, no per-SUT seed-corpus curation, no instrumented build, and no bytecode-rewriting agent." The phrase "no curated seed corpus" was replaced with "no per-SUT seed-corpus curation" — the qualifier is the per-SUT clause, which threads the needle correctly. The introduction (lines 79-104) and conclusion are aligned with the same language. **One residual discrepancy**: the introduction at line 95 still uses the phrase "no curated seed corpus" without the per-SUT qualifier. Strictly read, this contradicts the threats section's disclosure of the Tier-1 hand-curated seeds in `seeds/vcf/` and `seeds/sam/`. The contradiction is now a phrasing slip rather than a structural one, but it is still there and a careful reviewer will notice.

### M6 (budget parity) and M7 (seqan3 oracle reconciliation) — **Partially closed (M6) / Closed (M7).**

`design.tex` lines 352-370 explicitly disclose that "wall-clock parity is *not* iteration-cost parity" and call out the AFL++ vs libFuzzer 17pp gap on seqan3 as an iteration-cost artefact, not a corpus-quality finding. `mutation_score_section.tex` lines 145-162 mirror this disclosure on the result side. The seqan3 explanation is now reconciled with the kill semantics: lines 124-146 of `mutation_score_section.tex` explicitly state "the mutation engine's kill predicate is the *same* predicate for every tool's corpus on this cell, so a kill counted for BioTest would also count for libFuzzer if libFuzzer's corpus contained an input that triggered it. The advantage therefore lives on the corpus side." The threats section repeats the same separation. M7 is closed — the seqan3 lead is now framed as a corpus-retention discipline asymmetry, not an oracle asymmetry; the kill semantics are explicitly identical. **M6 remains partially open**: the paper *acknowledges* the iteration-cost asymmetry and explicitly disclaims iteration-count parity, but it does not run the iteration-count-parity comparison I asked for. The seqan3 +6.87pp lead is therefore still conditional on the wall-clock budget; a reviewer who wants to know whether the lead would survive iteration-count parity is told "we have not run it." That is more honest than the first version but it is not yet the falsification test I asked for.

### M8. Biopython entropy claim — **Closed.**

`mutation_score_section.tex` lines 78-86 are rewritten to the "consistent with the empirical pattern reported by Klees and Boehme on byte-content-lenient parsers" framing, with the explicit disclaimer "we do not have entropy or coverage-marginal-gain measurements for the biopython parser specifically and therefore do not claim a quantitative match to either source; the biopython deficit is consistent with their qualitative prediction, not predicted by a measurement we made." This is exactly the soften-to-qualitative I asked for. The $O(2^{8k})$ figure is no longer in the text.

### M9. Thirteen-rank ablation — **Not closed.**

`threats.tex` lines 70-94 add a paragraph admitting the only per-cell ablation reported is the biopython/SAM Ranks~12-13 toggle, that the headline kill rate on the other five cells "conflates metamorphic-MR contribution with augmentation-rank contribution," and that "a reader who wants to know what fraction of each cell's kill rate is attributable to the *metamorphic* part of the stack would need experiments beyond the present paper." This is a confession, not a fix. M9's minimum fix was *to run the ablation*. The paper now contains a paragraph admitting that the contribution claim cannot be evaluated from the data the paper reports. For a revised submission this is reject-grade on its own — the paper is asking me to accept the metamorphic-contribution headline on the basis of one cell's negative result (Ranks~12-13 don't move biopython) and verbal extrapolation to the other five. The "honest-disclosure" form on lines 90-94 — "where the deficit is small, it remains plausible that turning off Ranks~8-13 would turn that deficit into a larger one; where the lead is large, the same disclosure applies" — is an admission that the headline ranking is not falsifiable from the present data.

### M10. LLM-mined MR contribution — **Partially closed.**

`threats.tex` lines 96-125 and `implementation.tex` lines 36-48 disclose that the first targeted mining campaign returned 3 enforced MRs out of 7 candidate themes, and that the "full intent\,$\times$\,format matrix" expands the registry to "$15$-$30$ enforced MRs per the design intent." **What is still missing**: the "$15$-$30$" range is *design intent*, not a measurement. I checked `data/mr_registry.json` directly: the live primary registry has **4 enforced MRs** (`enforced_count: 4, quarantine_count: 12, total: 16`); the maximum across all snapshots in `data/` is 20 (`mr_registry.pre_fullD.backup.json`), and the SAM pristine has 2. The "$15$-$30$" range is therefore not what the headline runs use; it is what the design intent *predicts*. The paper's wording — "the full registry, expanded across all intent\,$\times$\,format combinations, sits in the $15$-$30$ enforced MR range described in the design intent" — is technically truthful (it is "described in the design intent") but a reader will read it as "the headline runs use 15-30." The paper still does not report (a) the per-MR kill contribution, (b) the kill rate when only LLM-mined MRs are active, or (c) the count of LLM-mined vs hand-coded MRs in each headline run. The conflation of LLM-mined and hand-coded contributions remains.

### M11. Pure-Random as floor reference — **Closed.**

`design.tex` lines 418-440 are rewritten to acknowledge "the across-cell variation in [Pure-Random's] score is at least as informative about *parser strictness* as it is about the recipe's discrimination of corpus quality." The paragraph explicitly states that cells where Pure-Random scores zero "do not vindicate the recipe on their own; they simply tell us the parser's header gate is strict enough that no random stream gets past it under the budget." This is exactly the reframe I demanded. The minimum-fix request — "compute, per cell, the Pure-Random pass-rate" — is not done, but the conceptual reframe absorbs the M11 critique without it.

### M12. Title/scope honesty for binary formats — **Closed.**

`main.tex` line 33 retitles the paper to **"BioTest: Metamorphic Testing for Textual VCF and SAM Parsers."** The introduction (lines 7-13) and abstract (lines 10-11) explicitly scope the paper to textual VCF/SAM and call out BCF/BAM/CRAM as out of scope. The threats section repeats. M12 is closed cleanly.

### M13. Reproducibility / public artefact — **Closed.**

`implementation.tex` lines 113-118 commit the artefact to "the venue's artefact-evaluation track at camera-ready, with a public Docker registry digest and a Zenodo-archived snapshot of the source tree at the submission commit." The Windows-path de-anonymisation slip is acknowledged: "Path strings of the form `C:\Users\anonymised`... are scrubbed in the submission artefact." This is the minimum fix I asked for. The Docker-Hub URL and Zenodo DOI are still pending camera-ready, which is conventional for double-blind submission.

## 3. New issues introduced by the revision

### N1. Bug-bench: PoV-fallback inflates BioTest's lead by exactly the same mechanism as Pure-Random's.

`bug_bench_section.tex` lines 103-117 disclose that 3 of BioTest's 13 found bugs are PoV-fallback (the canonical PoV file replayed under STRICT, not a BioTest-synthesised input). Pure-Random's 3 found are *also* PoV-fallback (`bug_bench_table.tex` $^\ddag$ footnote). The fairness audit is correctly cited. **The new issue**: the table's "any tool: 15/32 distinct" row sits *next to* "BioTest: 13" without normalising for paradigm. A reader sees BioTest at 13 and Jazzer at 2 and concludes BioTest is 6.5$\times$ stronger. The honest comparison is BioTest tool-found 10 vs Jazzer tool-found 0 (Jazzer's 2 are also PoV-fallback per `PHASE4_FINAL_REPORT.md` §3.2 sub-bullet "The 2 FOUND came... from the PoV reverse-fallback path"). The paper's footnote $^\dagger$ does the right thing for BioTest; it does not do the same accounting for Jazzer's 2. A careful reviewer will check `PHASE4_FINAL_REPORT.md` and find that **all four "FOUND" cells across BioTest and Jazzer on the new SAM bugs are PoV-fallback driven, not generation-driven**. The headline number is therefore comparing 10 BioTest tool-found bugs against 0 tool-found bugs from every other crash-only fuzzer — which is a real claim, but a smaller one than 13 vs 2.

### N2. Bug-bench mixes paradigms in the same table without explicitly weighting.

EvoSuite-anchor (4 found) and Randoop (3 found) are unit-level Java baselines that exercise method APIs, not file inputs. The paper acknowledges this (`bug_bench_section.tex` lines 117-125: "we include them because two of the 15 distinct confirmed bugs are method-level mutator regressions that no input-fuzzing paradigm reaches"). **The new issue**: the table's "any tool: 15/32 distinct" cell silently fuses two paradigms whose inputs are not even of the same type (file bytes vs Java JUnit cases). The +2 distinct bugs that EvoSuite-anchor adds to BioTest's 13 are bugs no input-fuzzing tool *can* reach by construction. Stating "the union over all eight tools is 15/32" is therefore not a fair denominator for a comparison whose primary axis is input-fuzzing. The footnote does not relabel the union; it just admits the cross-paradigm signal exists. A reviewer who wants to know "what fraction of *file-input-reachable* bugs does BioTest catch?" has to do that arithmetic themselves.

### N3. Three of BioTest's bug-bench wins are htsjdk-SAM PoV-fallback wins on bugs that *every* tool with a PoV finds.

Per `PHASE4_FINAL_REPORT.md` §4 row 13-15: htsjdk-1238, -1410 are 4-witnessed (BioTest + jazzer + pure_random + randoop); htsjdk-1360 is 2-witnessed (BioTest + pure_random). All three are STRICT-gate wins on the canonical PoV. The paper's bug-bench table credits BioTest with 13 (10 tool + 3 PoV-fallback) but does not include a "of these, how many are also confirmed by Pure-Random?" row. Cross-checking the dossier: at least 3 (the three SAM PoV-fallbacks) overlap with Pure-Random. The "BioTest is the only tool with detection coverage spanning all four parser languages" claim survives this — but it survives by exactly 1 bug (`noodles-268` on Rust), and that single bug is what underlies the four-language coverage claim.

### N4. The introduction now says "no curated seed corpus" while the threats section discloses "Tier-1 hand-curated spec-example seeds."

`introduction.tex` line 95: "no curated seed corpus." `threats.tex` lines 127-130: "the relation-curation pipeline discards candidates that fail against a seed corpus consisting of (a) the three Tier-1 hand-curated spec-example seeds shipped in `seeds/vcf/` and `seeds/sam/`." The first sentence is in the contributions paragraph; the second is in the threats section. The phrasing in the introduction was *not* updated to match the abstract's "no per-SUT seed-corpus curation" qualifier. This is a regression on M5: the abstract now matches design, but the introduction does not. (See REVIEW2.M5 above for the exact lines.)

### N5. The "$15$-$30$ enforced MR" claim is a design-intent extrapolation, not a measurement.

`threats.tex` lines 105-112 and `implementation.tex` lines 41-48 say "the full registry, expanded across all intent\,$\times$\,format combinations, sits in the $15$-$30$ enforced MR range described in the design intent." Verifying against `data/mr_registry.json` directly: enforced_count is 4 in the live primary registry, 20 in `pre_fullD.backup.json` (the maximum across all snapshots), and 2 in `sam_pristine.json`. The headline runs do not use 15-30 enforced MRs; they use somewhere between 2 and 20 depending on which run. The paper's phrasing is technically truthful — the *design intent* is in the 15-30 range — but a reviewer who reads "sits in the 15-30 enforced MR range" will read it as a measurement. This is a new contradiction the revision created by trying to address M10 without running per-rep MR-count audits.

## 4. Remaining major concerns (unrelated to M1-M13)

### R1. Bug-bench has no second differential-oracle baseline to isolate "differential" from "BioTest-specific."

The paper's structural argument for crash-only fuzzers' 0/2 score is sound: if 8/12 htsjdk-VCF target bugs are `differential_disagreement`, a crash oracle cannot win there. **What is missing**: any second tool that *also* implements a differential oracle. The natural comparator is Csmith-Yarpgen-style differential testing on the same parsers, or any of the LLM-driven differential-testing systems published since 2022. Without one, the bench is "BioTest is better than crash-only fuzzers at finding non-crash bugs." That is a tautology, not a demonstration that BioTest is the *right* differential tester. A reviewer will ask: would a hand-written 50-line Python differential script finding the same 13/32?

### R2. Bug-bench manifest construction is itself unblinded.

The 32-bug manifest was filtered by a "C2/C3/C4 audit" (`PHASE4_FINAL_REPORT.md` §2.1) that dropped four SAM entries because they "passed Stage 4 install-verification but failed reachability or anchor review on a second pass." Two further VCF entries (`vcfpy-gtone-0.13`, `vcfpy-nocall-0.8`) were dropped for failing criterion 4 ("installable as versioned artifact"). Three new htsjdk SAM regressions were *added* by a "fresh Stage 1 sweep against the 2.18 → 2.20 source diffs." The paper does not disclose that the manifest was modified post-hoc. The "12/23 VCF, 3/9 SAM" headline therefore reflects a manifest that was edited *during* the campaign — bugs that BioTest's paradigm could not reach were dropped, and bugs newly discoverable by the STRICT-gate prelude were added. This is an internal-validity issue I did not flag in REVIEW.md because the bug-bench section did not exist; now that it exists, it is a serious construct-validity concern.

### R3. The "STRICT-gate prelude" introduced 4-7 new detections after the manifest was frozen.

Per `PHASE4_FINAL_REPORT.md` §2.2: "DESIGN.md §5.3.2 documents the bidirectional read: STRICT can fire 'forward' or 'reverse'... reverse-direction bugs like htsjdk-1554/-1544/-1238 surface from the same predicate." The verification-policy change post-dates the manifest revision and unlocks the htsjdk-1360 / -1410 / -1238 SAM detections plus htsjdk-1418, vcfpy-176, vcfpy-146, vcfpy-127 on the VCF side. So between 4 and 7 of BioTest's 13 found bugs were unlocked by a verification-policy change, not by the tool's own input generation. This is not paper-disclosed.

### R4. The "consensus oracle requires N≥3 runners" claim is inconsistent with the seqan3 cell.

`design.tex` lines 270-276 say the consensus oracle uses "$N \ge 3$ SUTs drawn from the runner pool (in our benchmark: htsjdk, biopython, vcfpy, noodles-vcf, and seqan3, with format applicability gating which runners participate on a given input)." On SAM, the applicable runners are htsjdk and seqan3 (and pysam for the bug-bench). On a SAM input, seqan3's lead in the mutation table is reported under the consensus oracle — but the consensus oracle requires $N \ge 3$, and only htsjdk + seqan3 + biopython are SAM-format-applicable, with biopython being the SUT under test. When seqan3 is graded, the consensus pool drops to two runners (htsjdk, biopython). The paper does not address how the "$N\ge 3$" threshold is met when seqan3 is the SUT under grading. This is structurally important because the +6.87pp seqan3 lead is supposedly mediated by the consensus oracle's typed-exception retention; but the consensus oracle on SAM under grading-of-seqan3 has only two non-SUT voters.

### R5. The paper still does not separate "MR contribution" from "consensus-oracle contribution."

Bug-bench wins on htsjdk-VCF (`htsjdk-1554`, `-1364`, `-1389`, `-1372`, `-1418`, `-1544`) are STRICT-gate or differential-disagreement detections that come from BioTest's *runner-side STRICT pass*, not from any LLM-mined MR. Per `PHASE4_FINAL_REPORT.md` §3.2 jazzer subsection: "8 of 12 jazzer/htsjdk cells have `expected_signal.type == differential_disagreement` per the manifest — the target bug never crashes; it produces wrong output values that are only visible to a differential voter comparing htsjdk vs htslib / pysam." The bug-finding mechanism here is "differential voter" — not "metamorphic relation." The paper's headline is "metamorphic testing pipeline... confirms 13/32." A reader could reasonably infer the metamorphic relation is what catches the bugs. In practice, the differential voter is what catches them. The paper does not disclose what fraction of the 13 found bugs are caught by metamorphic relation violations vs by raw differential disagreement (no MR involved). Per the dossier's mechanism column on §4, the answer appears to be: most are differential / STRICT, very few are metamorphic. This is a contribution-attribution issue that the bug-bench section makes more visible than the original mutation-only paper did.

## 5. Verdict + score breakdown

| axis | score (was) | score (now) | one-line justification |
|------|-------------|-------------|-----------------------|
| Novelty | 2/5 | **2/5** | The revision adds the bug-bench result, which is novel as an artefact, but it surfaces R5: the bug-finding mechanism is differential voting, not metamorphic relation. The packaged contribution is the same as before. |
| Technical rigor | 1/5 | **2/5** | M3, M5, M7, M11, M12 close cleanly; M2, M6 partially close with disclosure rather than measurement. M4 and M9 remain open with the paper admitting the headline is not falsifiable from present data. M3 framing improvement is real, but n was not increased. Plus one. |
| Empirical strength | 2/5 | **3/5** | The bug-bench is a meaningful addition. R1-R3 (no second differential baseline, manifest unblinded, STRICT-gate prelude post-dates the freeze) shave the gain back. The proxy is no longer the only headline. Plus one. |
| Reproducibility | 2/5 | **3/5** | M13 closes (artefact-evaluation commitment, scrubbed paths). The artefact's `mr_registry.json` snapshot landscape (4-20 enforced MRs across snapshots) does not match the paper's "15-30" claim — small contradiction documented in N5. Plus one. |
| Presentation | 3/5 | **3/5** | Clearer scope (M12), better fairness disclosure (M2 paragraph), explicit statistical-inference posture (M3 paragraph). Bug-bench table is well-laid-out. The N1-N4 contradictions slipped in. Net flat. |

**Aggregate: 13/25 → from "reject" to "weak reject."** The bar I set in the prompt — "fixes are evidence-grounded, new claims are precisely scoped, no new contradictions" — is met for 5 of 13 findings. Three of the partial closures are honesty-on-paper rather than methodological remedy. M4 and M9 are not closed. N1-N5 are real new issues.

## 6. Final rebuttal questions

1. **Bug-bench tool-found vs PoV-fallback by paradigm.** Of the 13 BioTest "FOUND" bugs, you split 10 tool-found + 3 PoV-fallback. Of Jazzer's 2 found, `PHASE4_FINAL_REPORT.md` §3 jazzer notes both came from "the PoV reverse-fallback path." That puts BioTest tool-found at 10 vs every other input-fuzzer tool-found at 0. Why does Table 2's "any tool: 15/32 distinct" union include unit-level baselines (EvoSuite-anchor, Randoop) and PoV-fallback wins from crash-only fuzzers without footnoting that the *input-fuzzing-tool-found* union is 10/32? This single comparison is the headline of the bug-bench section.

2. **Mechanism attribution for the 13 BioTest wins.** Per `PHASE4_FINAL_REPORT.md` §4, of BioTest's 13 found bugs, the mechanism column is dominated by "forward §5.3.1 via STRICT gate" and "reverse §5.3.1" — both runner-side differential detections, not metamorphic-relation violations. How many of the 13 are actually caught by an LLM-mined metamorphic relation firing on a transformed input pair, versus by the runner-level differential voter on the canonical PoV? The paper's contribution claim is metamorphic; the dossier's evidence is differential. Reconcile.

3. **Manifest revision and STRICT-gate prelude.** Per `PHASE4_FINAL_REPORT.md` §2.1-2.2, four SAM bugs were dropped and three new htsjdk-SAM bugs were added in a manifest revision; concurrently a STRICT-gate verification-policy change unlocked detections of htsjdk-1360/1410/1238 (the three added bugs) plus htsjdk-1418, vcfpy-176, vcfpy-146, vcfpy-127. What is the BioTest detection rate on the *pre-revision* 35-bug manifest under the *pre-STRICT-gate* predicate? If the answer is materially below 13/32, the headline reflects manifest-and-predicate co-evolution with the tool, not the tool's intrinsic detection capability — which is exactly the LAVA / Magma critique you cite as your construct-validity foundation.

---

## 7. Remediation plan for issues that need additional experiments

The findings below cannot be closed by paper-side rewrites alone — they need data the artefact does not currently produce. For each, I give the minimum experiment that would close it, the protocol, the predicted disclosure language, and the reject/accept implication of the outcome.

The four partially-closed findings (M2, M3, M6, M10) are listed first; their disclosure paragraphs land cleanly but the underlying methodological gap is only closed by additional measurement. The two fully-open findings (M4, M9) are second. The five new major concerns surfaced by the revision (R1–R5) are third.

### M2 (partial) — Kill-aware corpus minimisation circularity

**What was done in revision:** `design.tex` lines 372–416 disclose the asymmetric `corpus_minimize.py` policy (kill-aware on Python SUTs, outcome-fingerprint on non-Python) and cite `vikram2023guiding` as the precedent for using kill-information as a corpus-selection signal at `cmin` time.

**What's still needed:** a dual-policy run that re-grades every Python cell (vcfpy, biopython) under both `--strategy kill_aware` and `--strategy outcome_fingerprint`, so that the marginal effect of the kill-aware selector on the headline number is measured rather than asserted.

**Protocol:**
1. *Outcome-fingerprint replicate.* For vcfpy/VCF and biopython/SAM, re-run the entire mutation-adequacy pipeline with `corpus_minimize.py --strategy outcome_fingerprint --keep 200` (the same per-mutant budget cap as the kill-aware run). Same seeds, same reps ($n{=}4$), same engine. Report mean ± std side-by-side with the existing kill-aware numbers.
2. *Δ disclosure.* Compute $\Delta_{\mathrm{cmin}} = \mathit{score}_{\mathrm{kill\_aware}} - \mathit{score}_{\mathrm{outcome\_fp}}$ per cell. Predict: $|\Delta_{\mathrm{cmin}}| \le 5$ pp on vcfpy and $\le 3$ pp on biopython, based on the run-2 post-mortem in `Flow.md` lines 1418–1429 ($-18.65$ pp regression on biopython under outcome-fingerprint, recovered with kill-aware). If the $\Delta$ is materially larger than 5 pp, kill-aware is the dominant signal and the headline must be re-stated under outcome-fingerprint as the load-bearing comparison.
3. *Symmetry stress test.* Apply both selectors to Atheris's corpus on biopython under the same budget. If Atheris's score also moves under selector choice, the asymmetry is on the *cell*, not on the *tool*; if Atheris is selector-invariant, the kill-aware advantage is BioTest-specific and the paper has a circularity problem.

**Cost:** $\approx 8$ wall-hours per cell × 2 cells × 2 selectors = $32$ wall-hours; trivial alongside the other ablations.

**Citations to invoke:** Vikram et al. ISSTA'23 §5 for the empirical baseline of kill-aware vs outcome-fingerprint cmin yield delta.

**Predicted disclosure language:** "Under outcome-fingerprint cmin, vcfpy/VCF mutation score is $X$pp ($\Delta_{\mathrm{cmin}}{=}Y$) and biopython/SAM is $Z$pp ($\Delta_{\mathrm{cmin}}{=}W$). The kill-aware selector contributes $Y$pp on vcfpy and $W$pp on biopython to the headline number. Both numbers remain within the small-deficit envelope ($1.3$–$3.6$pp) we report on those cells."

**Reject implication:** if outcome-fingerprint cmin produces materially worse scores on Python SUTs while non-Python SUTs are unaffected, the headline mutation table is artificially asymmetric across languages, and the cross-language comparison in §V.A becomes meaningless until the asymmetry is normalised.

### M3 (partial) — $n{=}4$ with $\sigma{=}0.00$

**What was done in revision:** `mutation_score_section.tex` lines 38–55 added a "Statistical-inference posture under $n{=}4$" paragraph that admits the minimum exact $p{=}0.029$, the Holm–Bonferroni-corrected $p\sim 0.17$, and that $\hat{A}_{12}$ is descriptive on $\sigma{=}0$ cells. `vargha2000critique` cited correctly.

**What's still needed:** more reps. The framing repair is appropriate, but the underlying methodological problem — $n{=}4$ is too small for the comparisons being drawn — is not fixed.

**Protocol:**
1. *Boost to $n{=}10$ on the four close-margin cells.* htsjdk/VCF, htsjdk/SAM, vcfpy/VCF, noodles/VCF are the cells where the difference between BioTest and the strongest baseline is $1.3$–$3.6$pp; at $n{=}4$ the inferential apparatus cannot distinguish a true gap from sampling noise. Run six additional reps per cell per side (BioTest and strongest baseline) under independent stochastic seeds. $4 \times 2 \times 6 = 48$ additional runs, $\approx 20$ wall-hours.
2. *Power analysis.* For an $\hat{A}_{12}$ cut-off of $0.71$ (large effect, Vargha–Delaney 2000), $n_1=n_2=10$ has minimum two-sided exact $p \approx 0.0007$, well inside Holm–Bonferroni at six cells. Report the exact $p$ and the corrected $p$ together.
3. *Drop the deterministic-cell statistics.* On seqan3/SAM and biopython/SAM full-population where both samples have $\sigma{=}0$, do not report $\hat{A}_{12}$ at all in the headline prose; only report mean differences. The current paper does this in the framing paragraph but not in §V.A's per-cell narrative.

**Citations to invoke:** Arcuri & Briand TSE'14 (already cited) for the $n{\ge}10$ recommendation; Vargha & Delaney 2000 for the effect-size thresholds.

**Predicted disclosure language:** "On the four close-margin cells, $n{=}10$ reps per side give $\hat{A}_{12}\le 0.25$ on each cell at exact $p \le 0.001$ and Holm–Bonferroni-corrected $p \le 0.006$. The descriptive ranking — BioTest below the strongest baseline on every rep-pairing — is now an inferential conclusion, not just an observation."

**Reject implication:** if $n{=}10$ reveals $\hat{A}_{12}$ in the $0.4$–$0.6$ band on any close-margin cell (which would mean the rep-distributions overlap), the "$1.3$–$3.6$pp deficit" claim must be downgraded to "no statistically detectable difference," which is actually a *better* result for BioTest's bounded-effort claim — but the paper would need to be restructured around it.

### M6 (partial) — Budget parity vs iteration-cost parity

**What was done in revision:** `design.tex` lines 352–370 disclose that "wall-clock parity is *not* iteration-cost parity" and explicitly call out the AFL++ vs libFuzzer 17pp gap on seqan3 as an iteration-cost artefact. `mutation_score_section.tex` lines 145–162 mirror the disclosure.

**What's still needed:** the iteration-count-parity falsification test for the seqan3 +6.87pp lead and the four close-margin deficits.

**Protocol:**
1. *Iteration-count cap.* For each cell, run BioTest and the strongest baseline at the *same number of corpus inputs* (rather than the same wall-clock budget). Set the cap at the median of the two tools' per-cell input counts so neither is starved. This requires a small modification to the harness drivers (`compares/scripts/phase3_*.sh`) to honour an `--input-count-cap` flag.
2. *Two-axis grid.* Report mutation score under (wall-clock budget, iteration-count cap) for all six cells. The current headline is the wall-clock column; the iteration-count column would be new.
3. *Predicted outcomes.* On seqan3, the AFL++/libFuzzer 17pp gap should compress under iteration-count parity (consistent with iteration-cost being the cause). The BioTest +6.87pp lead might compress, hold, or invert; the test is whether it survives the budget normalisation.

**Cost:** $\approx 6$ cells × $2$ tools × $4$ reps = $48$ runs at the same cell-budget as the headline; $\approx 25$ wall-hours.

**Citations to invoke:** Klees et al. CCS'18 §4.2 for the multi-budget-axis methodology; Böhme & Falk FSE'19 for the iteration-cost normalisation precedent.

**Predicted disclosure language:** "Under iteration-count parity (median of the two tools' per-cell input counts), the seqan3 lead changes from $+6.87$pp to $\Delta_{\mathrm{seqan3}}$pp; the close-margin deficits change to $\Delta_{\mathrm{htsjdk-VCF}}, \Delta_{\mathrm{vcfpy}}, \Delta_{\mathrm{noodles}}, \Delta_{\mathrm{htsjdk-SAM}}$. The pattern under both budget axes is consistent: the recipe is robust to iteration-cost normalisation."

**Reject implication:** if the seqan3 lead disappears under iteration-count parity, the lead was a budget artefact and the paper must withdraw the corpus-quality story for that cell. If the close-margin deficits *grow* under iteration-count parity (because the wall-clock budget was previously favouring BioTest's faster per-input cost on its own corpus), the bounded-effort claim weakens and must be restated.

### M10 (partial) — LLM-mined MR contribution

**What was done in revision:** `threats.tex` lines 96–125 and `implementation.tex` lines 36–48 disclose the MR cardinality of the headline runs (corrected to 5/15 for VCF, 3/32 for SAM, 20/53 upper bound across snapshots, per the per-snapshot audit added in this revision's N5 fix).

**What's still needed:** isolation of LLM-mined contribution from hand-coded transform contribution; per-MR kill-rate breakdown on the headline runs.

**Protocol:**
1. *Source-tag every transform.* Annotate each entry in `data/mr_registry.json.<run_tag>` with `origin ∈ {llm_mined, hand_coded_atomic, spec_rule_target}`. The annotation already exists implicitly (LLM-mined MRs go through Phase B's RAG validation; hand-coded atomics are listed in `mr_engine/transforms/__init__.py`). Make it explicit and serialise.
2. *Three-arm ablation per cell.* (a) Full registry. (b) Hand-coded-only (LLM-mined disabled). (c) LLM-mined-only (hand-coded disabled). Report mutation score per cell per arm. Same $n{=}4$ reps. $6 \times 3 \times 4 = 72$ additional runs, $\approx 30$ wall-hours.
3. *Marginal-MR table on the most LLM-heavy cell.* Pick the cell with the highest LLM-mined MR count (likely htsjdk/VCF under `vcf_only.backup`'s 10 enforced); leave-one-out per LLM-mined MR. ${\sim}10$ MRs × $4$ reps = $40$ additional runs.

**Cost:** $\approx 50$ wall-hours total. Author-hours: 8 for the source-tagging plus 4 for the ablation report.

**Citations to invoke:** Blasi et al. ICSE'21 (already cited as `blasi2021memo`) for per-MR ablation methodology in MR-mining work; Tian et al. (already cited as `tian2023mrscout`) for the LLM-mined MR contribution-attribution pattern.

**Predicted disclosure language:** "Of the $A_{\mathrm{cell}}$pp mutation-adequacy score on cell $c$, LLM-mined MRs contribute $L_{\mathrm{cell}}$pp and hand-coded transforms contribute $A_{\mathrm{cell}}{-}L_{\mathrm{cell}}$pp. The leave-one-out marginal contribution of the most-impactful LLM-mined MR (`mr_id=...`) is $K^\star$pp; the median LLM-mined MR contributes $\tilde{L}$pp."

**Reject implication:** if LLM-mined MRs contribute $\le 1$pp on every cell while hand-coded transforms carry the headline number, the LLM-mining pipeline is window-dressing and the paper's contribution shifts to "an SUT-agnostic differential infrastructure with a small set of hand-coded metamorphic transforms" — still a contribution but not the LLM-mining one currently advertised in the title and abstract. The paper would need a partial restructuring around that.

### M4 (open) — Researcher-degree-of-freedom in MR curation

**What's needed:** quantification of the curation pipeline's discard rate, per-MR contribution, and a blinded re-run on a held-out seed corpus.

**Protocol:**
1. *Curation log audit.* Instrument `mr_engine/registry.py` to emit `data/curation_log.jsonl`: one line per LLM-proposed MR with fields `{candidate_id, transform_steps, scope, validation_outcome, accepted}`. Already partially implemented; run the full Phase B against every intent×format pair to convergence and report (a) number of candidates proposed, (b) accepted-vs-rejected counts, (c) rejection-cause histogram (`spec_rule_index_dependency`, `seed_corpus_failure`, `dedup_collision`, `whitelist_violation`).
2. *Per-MR ablation.* For each cell in the mutation-adequacy table, run mutation grading with each individual `mr_id` disabled in turn (leave-one-out). Report Δ kill-rate per MR. ~$15$ MRs $\times\,6$ cells $\times\,4$ reps $=\,360$ additional grading runs; on the existing budget of $1500$ s/cell that is $\approx 150$ wall-hours, feasible inside one weekend on a 16-vCPU machine.
3. *Blind re-curation on held-out seeds.* Hold out `seeds/vcf/spec_example.vcf` and `seeds/sam/spec_example.sam` (the two largest Tier-1 seeds), re-run the full Phase B mining without those seeds in the validation gate, and check whether the resulting registry differs from the artefact's frozen version. Report the symmetric difference.

**Citations to invoke:** Munafò et al. (Nature Human Behaviour 2017, "A manifesto for reproducible science") for the pre-registration norm; Vikram et al. ISSTA'23 for the per-MR ablation methodology.

**What the paper would say afterwards:** "Phase B accepted $X$ of $Y$ candidate MRs; the per-cell leave-one-out ablation shows the median MR contributes $Z$ pp to kill rate, the most-impactful single MR contributes $W$ pp, and removing the bottom-$K$ MRs costs $V$ pp. On a held-out seed re-curation the registry differs from the frozen artefact in $S$ of $E$ enforced MRs, all of which trace to LLM nondeterminism rather than seed-specific gating."

**If the experiment fails:** if the held-out re-curation produces a substantially different registry, the paper must downgrade the LLM-mining contribution claim to a one-shot demonstration, not a reproducible procedure.

### M9 (open) — Thirteen-rank ablation

**What's needed:** a Ranks 1–7 vs Ranks 1–13 cross-cell ablation, plus per-rank toggles on at least one cell where the deficit is small.

**Protocol:**
1. *Two-arm ablation across all six cells.* Grade with (a) Ranks 1–7 corpus only (metamorphic outputs), (b) Ranks 1–13 corpus (deployed configuration). Report mean ± std over $n{=}4$ reps per arm per cell. $6 \times 2 \times 4 = 48$ additional mutation runs; $\approx 20$ wall-hours.
2. *Per-rank leave-one-out on the two close-margin cells with the largest $\sigma$.* Pick htsjdk/VCF and vcfpy/VCF (the cells where the std across reps is non-zero), and run $13$ leave-one-out arms per cell. $13 \times 2 \times 4 = 104$ additional runs.
3. *Marginal-contribution table.* Compute $\Delta_{\mathrm{rank}} = \mathit{score}(\text{Ranks 1–13}) - \mathit{score}(\text{Ranks 1–13} \setminus \{r\})$ per rank $r$. Order ranks by $\Delta$ and identify the smallest $K$ such that the top-$K$ ranks recover ≥95% of the headline kill rate.

**Citations to invoke:** Just et al. FSE'14 §6 for the per-operator ablation methodology that motivates per-rank ablation here.

**What the paper would say afterwards:** "Of the $32.5$pp biopython deficit, Ranks 1–7 alone account for $X$pp and Ranks 8–13 account for the remaining $32.5{-}X$pp; on htsjdk/VCF and vcfpy/VCF the metamorphic Ranks 1–7 contribute $\geq Y\%$ of the headline kill rate, with the largest single-rank contribution being Rank $r^\star$ at $W$pp."

**If the experiment fails:** if Ranks 1–7 alone produce mutation scores at or below Pure-Random on multiple cells, the metamorphic-contribution claim is not supportable and the paper's contribution must be retitled to "a thirteen-rank corpus stack" with the metamorphic-MR contribution downgraded to one component among many.

### R1 (new major) — No second differential-oracle baseline

**What's needed:** a hand-written or LLM-driven differential testing baseline that uses the same SUT pool but no metamorphic relations.

**Protocol:**
1. *Hand-rolled differential script.* ~50 lines of Python that (a) reads each seed in `seeds/vcf/` and `seeds/sam/`, (b) routes through every SUT runner, (c) compares canonical JSON, (d) flags disagreements. No MRs, no transforms, no Phase B/E. Run on the exact same seed corpus and SUT pool the headline runs use; grade under the same mutation engine and the same bug-bench predicate.
2. *Csmith-style differential.* For VCF, fork a small grammar-conformant generator (e.g. `vcfgen.py` — simple PCFG over VCF v4.3) that emits valid VCF without metamorphic transformations. Pipe through the same SUT pool and oracle. This isolates "differential testing of file-format parsers" from "metamorphic relations on file-format parsers."

**Citations to invoke:** McKeeman 1998 (already cited) for differential testing baseline; Yang et al. PLDI'11 for grammar-driven differential parser testing without MRs.

**What the paper would say afterwards:** "Of the 13 \biotest{} bug-bench wins, $X$ are also reached by a hand-written 50-line differential script using the same SUT pool; the remaining $13{-}X$ are uniquely attributable to the metamorphic-transform pipeline. On mutation adequacy the differential-only baseline achieves $Y$pp on average across cells, vs $Z$pp for \biotest{}'s full Ranks 1–13 and $W$pp for Ranks 1–7."

**If the experiment fails:** if the hand-rolled differential reaches all 13, then BioTest's metamorphic-pipeline contribution to bug-finding is zero on this manifest and the paper's contribution must be relocated entirely to the *consensus-oracle infrastructure* and the SUT-agnostic harness layer. That is still a contribution but a different one.

### R2 (new major) — Bug-bench manifest is itself unblinded

**What's needed:** disclosure of the manifest revision history with pre-revision detection numbers, and a blinded second-author manifest audit.

**Protocol:**
1. *Pre-revision re-run.* Restore the pre-2026-04-21 35-bug manifest from `compares/bug_bench/dropped.json` reconstruction (the four dropped SAM entries plus the two dropped VCF entries are documented). Re-run the full bug-bench across all eight tools. Report \biotest{} \textsc{tool-found} and \textsc{found} counts on the pre-revision manifest under the pre-STRICT-gate predicate.
2. *Independent manifest audit.* A second author (one not involved in the C2/C3/C4 audit) re-runs the dropped-entry rationale on the four dropped SAM bugs and the two dropped VCF bugs with the audit blinded to the tool's paradigm. Report agreement rate.

**Citations to invoke:** Hazimeh SIGMETRICS'20 §4.2 for blinded manifest audit; Dolan-Gavitt et al. S&P'16 (LAVA) §6 for the warning against tool-paradigm-coupled manifests.

**What the paper would say afterwards:** "On the pre-revision 35-bug manifest under the pre-STRICT-gate predicate, \biotest{}'s detection rate was $X{/}35$ \textsc{tool-found} and $Y{/}35$ \textsc{found}; the audit-driven manifest revision (3 added htsjdk-SAM regressions, 4 dropped paradigm-out SAM entries, 2 dropped install-failed VCF entries) plus the STRICT-gate predicate change moved the figure to $10{/}32$ \textsc{tool-found} and $13{/}32$ \textsc{found}. Net of the manifest revision, the tool's intrinsic detection rate ratio is $\Delta$pp."

**If the experiment fails:** if \biotest{}'s pre-revision detection rate is materially below the headline (say, $7{/}35$ \textsc{tool-found}), the headline must be re-stated as conditional on the post-audit manifest, with the pre-audit number reported alongside as the unconditional rate. The construct-validity story would survive but the headline would soften by $\sim 3$ pp.

### R3 (new major) — STRICT-gate prelude post-dates the manifest freeze

**What's needed:** disentangle "tool detection" from "predicate update" by reporting both pre- and post-STRICT-gate numbers per tool.

**Protocol:**
1. *Disable STRICT-gate, replay.* Set `_replay_trigger_silenced.supports_strict_parse=False` for every runner in `bug_bench_driver.py`, re-run the bug-bench across all eight tools and the post-revision manifest. The detection counts under the pre-STRICT predicate are the lower bound.
2. *Diff table.* For every (tool, bug) cell where the post-STRICT verdict is FOUND but the pre-STRICT verdict is miss, mark "STRICT-gate-conditional." Count these per tool.

**No new citations needed**; the predicate is documented in the artefact's `compares/DESIGN.md` §5.3.2.

**What the paper would say afterwards:** "Of \biotest{}'s 13 bug-bench \textsc{found}, $X$ are STRICT-gate-conditional (post-STRICT FOUND, pre-STRICT miss) and the remaining $13{-}X$ are STRICT-independent. The corresponding numbers for Jazzer are $Y$ and $2{-}Y$; for Pure-Random, $3$ and $0$ (every Pure-Random win is STRICT-gate-conditional by construction)."

**If the experiment fails:** if the STRICT-gate-conditional fraction is high (say, $\geq 7$ of 13 for \biotest{}), the paper must lead with the STRICT-gate-independent number as the intrinsic capability and report the STRICT-conditional number as a separate column.

### R4 (new major) — Consensus-oracle $N \ge 3$ when seqan3 is the SUT

**What's needed:** clarification of how the $N\ge 3$ threshold is met when seqan3 is the SUT under grading, since only htsjdk and biopython are SAM-format-applicable as voters once seqan3 is the SUT.

**Protocol:** *paper-side fix, no new experiment.* Audit the actual voter pool for the seqan3/SAM mutation runs. Two possible resolutions:
1. *If pysam was active as a fourth SAM-format voter*, the paper must add pysam to the consensus-runner enumeration in §IV.D ("Multi-Runner Consensus Oracle"). Per `Flow.md` §10, pysam is integrated as the fourth SUT via Docker (`compares/harnesses/pysam/`); the consensus pool when grading seqan3 is therefore htsjdk + biopython + pysam = three voters, satisfying $N\ge 3$.
2. *If only htsjdk + biopython voted (pool drops to two when seqan3 is the SUT)*, the paper must explicitly disclose that the consensus-oracle definition relaxes to $N\ge 2$ for the seqan3 cell, and the seqan3 +6.87pp lead must be re-explained under the relaxed predicate.

**Recommended disclosure language** (assuming Flow.md's pysam integration is in fact active in the seqan3 grading runs): "The consensus pool for SAM-format inputs is htsjdk, biopython, seqan3, and pysam; when seqan3 is the SUT under grading the remaining three are voters and the $N\ge 3$ threshold is met, with pysam acting as the third independent reference."

**If the audit reveals only two voters:** the paper must downgrade the consensus-oracle claim on seqan3/SAM to a differential-pair claim, and re-explain the +6.87pp lead under that weaker predicate.

### R5 (new major) — MR contribution vs consensus-oracle contribution attribution

**What's needed:** per-bug attribution of which mechanism (metamorphic-relation violation vs runner-level differential vs STRICT-gate vs PoV-fallback) silenced post-fix on each of \biotest{}'s 13 wins.

**Protocol:**
1. *Per-bug mechanism audit.* For each of the 13 found bugs, examine the `result.json` and `bug_reports/<bug_id>/` artefacts. Classify the silencing trigger as:
   - (a) MR-induced: an input $T(x)$ that violates the metamorphic relation $\mathit{out}(\mathit{parse}(x))\equiv\mathit{out}(\mathit{parse}(T(x)))$;
   - (b) Differential-only: an input that is not the output of an MR transform but on which the SUT pool disagrees;
   - (c) STRICT-gate: the bench's STRICT predicate fires on a non-MR input;
   - (d) PoV-fallback: the trigger is the manifest's canonical PoV file.
2. *Report a four-column table* with each of the 13 bugs against these four mechanisms.

**No new experiments needed**; the artefacts already exist. This is paper-side audit work.

**What the paper would say afterwards:** "Of the 13 \biotest{} bug-bench wins, $A$ are MR-induced, $B$ are differential-only, $C$ are STRICT-gate, and $D$ are PoV-fallback ($A+B+C+D=13$). The metamorphic-pipeline contribution to bug-finding is therefore $A$ confirmed bugs out of 32 manifest entries; the remaining $13{-}A$ wins are attributable to the SUT-agnostic differential infrastructure (the consensus oracle, the STRICT-gate, and the PoV replay machinery) without metamorphic-relation involvement."

**Honesty implication:** if $A$ is small (say, $\le 3$), the paper's headline contribution is the *infrastructure* (SUT-agnostic differential testing pipeline with consensus oracle and STRICT predicate), not the metamorphic-relation pipeline per se. The contribution claim would shift from "metamorphic testing for bioinformatics parsers" to "an SUT-agnostic differential-testing infrastructure with metamorphic relations as one of its input-generation strategies."

---

## 8. Cost summary for closing all open and partially-closed findings

| finding | status | wall-hours | author-hours | new authoring | reject if outcome bad |
|---|---|---|---|---|---|
| M2   | partial | ~32 | 6  | Δ-cmin column on Python cells | kill-aware is dominant signal |
| M3   | partial | ~20 | 4  | $n{=}10$ statistics block | overlapping rep-distributions on close-margin |
| M6   | partial | ~25 | 6  | iteration-count-parity column | seqan3 lead disappears |
| M10  | partial | ~50 | 12 | per-MR + LLM-only/hand-only ablation | LLM-mining is window dressing |
| M4   | open    | ~150 | 10 | curation-log paragraph | LLM-mining downgraded |
| M9   | open    | ~50 | 10 | rank-ablation table | metamorphic contribution downgraded |
| R1   | new     | ~40 | 20 | differential-baseline section | MR contribution may be zero |
| R2   | new     | ~80 | 15 | pre-revision re-run | manifest is tool-coupled |
| R3   | new     | ~30 | 5  | STRICT-conditional column | STRICT-fragile headline |
| R4   | new     | 0   | 3  | voter-pool audit | $N$-threshold must relax |
| R5   | new     | 0   | 10 | mechanism-attribution table | contribution shifts to infra |

Total: ~$477$ wall-hours, ~$101$ author-hours. None individually larger than the original Phase 4 sweep. R4 + R5 are paper-side audits the artefact already supports; M2 and M6 are the highest-leverage measurements (small wall-hour cost, large effect on whether headline survives).

**Priority order if budget is finite:**
1. **R4 + R5** (zero wall-hours, paper-side audit) — close immediately.
2. **M6 + R3** ($55$ wall-hours combined) — these two budget-and-predicate-isolation experiments most directly stress-test the headline; if they hold, the headline is robust.
3. **M2 + M3** ($52$ wall-hours combined) — closes the circularity disclosure and the small-$n$ inferential gap.
4. **M9 + M10** ($100$ wall-hours combined) — disambiguates the metamorphic-vs-augmentation and LLM-vs-hand-coded contribution attributions; without these the per-component novelty claim is not supportable.
5. **R1 + R2** ($120$ wall-hours combined) — these establish whether the contribution survives independent baselines and a blinded manifest. They are necessary for top-tier acceptance but not for weak-accept.
6. **M4** ($150$ wall-hours) — closes the unblinded-curation construct-validity threat. Largest experiment; lowest urgency relative to the others because the threats section already disclaims it.

The minimum bundle to move from weak-reject to weak-accept, in my judgement: R4, R5, M6, R3, M9. The minimum bundle to move from weak-accept to accept: add M2, M3, M10, R1. M4 and R2 can land as future work if the rest are done cleanly.
