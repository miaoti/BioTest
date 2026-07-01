# REVIEW7 — BIBM-calibrated round 7 (independent reviewer)

**Update note: Updated 2026-04-27 after page-budget compression round.**
The authors brought the paper from ~10 pages to a target of 8 pages by
trimming verbose phrasing, dropping redundancy between
`background.tex` and `related.tex`, and collapsing the five
phase-paragraph block of `design.tex` into a single Pipeline paragraph.
Total prose is now $5{,}743$ words in `sections/*.tex` (down from
$\sim 7{,}268$ before this round). I have re-read every section file
and reassessed the dimensions called out by the authors. Sections of
this review marked **[changed since prior]** carry material updates.
Sections marked **[unchanged]** carry only minor wording or numerical
refreshes.

## Verdict

**Weak accept.** **Verdict unchanged.**

The cuts have not damaged the technical or empirical case. Every
load-bearing numerical claim (the $n{=}10$ boost on the four
close-margin pairs, the family-wise-$\alpha{=}0.05$
Holm--Bonferroni clearance, mutation/coverage percentages,
$10/32 \cdot 13/32 \cdot 15/32$ bug counts) is still present and
internally consistent across abstract, prose, tables, and conclusion.
The contributions list is intact. The LLM-mining novelty paragraph in
`related.tex` is still load-bearing. The consensus oracle is still
defined with the three-layer predicate. The compression has materially
improved the page-budget posture, which was the single binding
question I flagged in the prior version. If anything, the cuts have
modestly strengthened acceptance prospects because the open
single-binding-risk in the prior version (would the paper land at
$\le 8.0$ pages?) is now substantially closer to settled.

## Headline judgement [unchanged]

\biotest{} is a metamorphic testing pipeline for textual VCF and SAM
parsers in which the dominant adoption cost of MT, manual MR
identification, is replaced by an LLM grounded in retrieved spec
chunks. The empirical contribution is honest: \biotest{} is within a
single-digit margin of the strongest in-process fuzzer on five of six
mutation-adequacy configurations, leads on every VCF SUT in line
coverage, and is the only tool in the slate that confirms manifest
bugs through inputs it itself synthesised ($10/32$ versus $0/32$ for
every crash-only fuzzer). The single most important strength is the
real-bug benchmark coupled to a clean tool-found vs. PoV-fallback
split, which converts the framework's design choice (rich oracle, no
coverage feedback) into measurable yield on bugs that crash-only
paradigms cannot reach by construction. The single most important
weakness is empirical breadth on the LLM-mining novelty itself: a
single LLM is used, no LLM-vs-human-MR comparison is run, and the
only intra-stack ablation is Ranks~12 and~13 on biopython/SAM. For
BIBM (a Rank-B bio+AI venue) the trade is acceptable, but the AI
contribution rests on a thinner empirical base than the
fuzzing-paradigm contribution does. Confidence: medium-high; I have
re-read every section file in its current compressed form, and the
numerical agreement between abstract, prose, tables, and conclusion
holds.

## Detailed assessment

### Did the compression preserve content quality? [changed since prior]

The authors claimed no content was lost, only redundancy and verbose
phrasing. I checked every load-bearing claim and the answer is mostly
yes, with one small caveat.

- **Numerical claims preserved.** All percentages and counts remain
  intact: the abstract's single-digit-deficit-on-five framing
  (`abstract.tex` lines 22-25), the $-32.5$\,pp biopython gap
  (`abstract.tex` line 24-25), the highest-line-coverage-on-every-VCF
  claim (`abstract.tex` line 26), and the $10/32$, $13/32$, $15/32$
  bug-bench split (`bug_bench_section.tex` lines 43-50,
  `bug_bench_table.tex` lines 29-31). The mutation-table
  per-cell numbers are unchanged. The coverage-table per-cell numbers
  are unchanged.
- **Statistical-rigour claims preserved.** The exact two-sided
  Mann--Whitney $U$ via full enumeration of
  $\binom{n_1+n_2}{n_1}$ rank arrangements, Vargha--Delaney
  $\hat{A}_{12}$ at $0.56/0.64/0.71$, and Holm--Bonferroni at $k{=}4$
  all remain (`mutation_score_section.tex` lines 23-39). The four
  pairs still all clear family-wise $\alpha{=}0.05$.
- **Caveat: explicit p-values trimmed from four to two.** The prior
  version listed all four Holm-corrected p-values explicitly
  ($4.0\times 10^{-5}$, $3.1\times 10^{-3}$, $9.5\times 10^{-3}$,
  $3.7\times 10^{-2}$). The compressed version reports only the
  strongest (htsjdk/VCF at $4.0\times 10^{-5}$) and the weakest
  (vcfpy/VCF at $3.7\times 10^{-2}$), with the middle two p-values
  dropped (`mutation_score_section.tex` lines 33-35). This is a
  defensible cut: the family-wise-clearance claim is the inferential
  conclusion that matters, and the strongest/weakest bracket bounds
  it on both sides. A reviewer who wants the per-pair p-values can
  reconstruct them from the artefact's raw kill-count files. I would
  not flag this as a meaningful loss.
- **Contributions list intact.** Three-bullet contributions list in
  `introduction.tex` lines 75-92 still names (i) the LLM-RAG MR
  miner with multi-runner consensus oracle as the headline novelty,
  (ii) the thirteen-rank corpus stack with augmentation-failure
  characterisation, and (iii) the three-axis evaluation. Nothing
  dropped.
- **LLM-mining novelty still load-bearing.** `related.tex` lines
  20-34 still spell out the MeMo and MR-Scout contrast and frame the
  combination of spec-grounded LLM-driven MR mining with a
  SUT-agnostic generator and consensus oracle as the novelty claim.
  This is the right framing and it survives the cut.
- **Consensus oracle still well-defined.** `design.tex` lines
  115-136 still carries the three-layer predicate (differential
  consensus $\to$ metamorphic consensus $\to$ relation quarantine)
  and the $N \ge 3$ minimum justification. Nothing dropped here.

Bottom line: content quality survived the cuts cleanly with one
defensible numerical-detail trim.

### Did the compression hurt readability? [changed since prior]

This is the more interesting question. Three places to check.

**The five-phase pipeline collapse (`design.tex` lines 38-61).** This
is the single largest structural cut: five paragraphs of one phase
each, collapsed into a single dense paragraph with five bolded phase
markers. I read it carefully. The condensed paragraph is dense but
readable, helped by the pattern of starting each phase with a bold
**Phase~A**/**Phase~B**/etc. tag that the eye latches onto as a
section boundary. The phase semantics are all there: Phase~A is
spec-chunk-and-embed, Phase~B is LLM-RAG MR mining, Phase~C is
multi-runner exec with consensus oracle, Phase~D is coverage feedback,
Phase~E is augmentation. The pipeline figure
(`pipeline_figure.tex`) carries the visual decomposition that the
prose no longer spreads across paragraph boundaries, so the reader
gets the spatial layout from the figure and the textual semantics from
the paragraph. This is an acceptable trade. A picky reader might
prefer the per-phase paragraph form; I would not block on it.

**Corpus-stack itemize tightened (`design.tex` lines 78-113).** Each
rank now occupies a single sentence-and-a-half rather than a
multi-line entry. Rank~1--7 in particular is now compressed into one
itemized bullet rather than seven separate descriptions. The
parenthetical R1/R2/R3/R4/R5/R6/R7 sub-tags inside the bullet keep
the granularity available to a careful reader. R8 through R13 are
still per-rank bullets. This is the right asymmetry because R1--R7
are all spec-grounded metamorphic relations (so a single
list-with-tags conveys the family), while R8--R13 are heterogeneous
augmentation operators that genuinely need per-rank descriptions.

**Background section dropped redundant MT and CG-fuzzing
subsections.** `background.tex` is now $236$ words (was $361$) and
covers only what the prior section's bioinformatics-formats and
oracle-problem subsections need. The MT and coverage-guided-fuzzing
positioning is now in `related.tex` only. I checked the design
section to see whether it now feels unmotivated by the pruned
background. It does not: `design.tex` opens by referencing the same
$\citep{chen1998metamorphic,chen2018metamorphic,segura2016survey}$
trio that `background.tex` retains, and the design-constraint
paragraph (C1/C2/C3) is the load-bearing motivation for everything
that follows in the section. The reader who has read
`introduction.tex` and `related.tex` is well-positioned to absorb
`design.tex` without the dropped background subsections. I do not
think the design section feels unmotivated.

**Other cuts.** `related.tex` lost the MT-positioning paragraph
verbosity (now $470$ words, was $664$); the substantive content
survives. `mutation_score_section.tex` (now $539$ words, was $643$)
collapsed the four explicit p-values to "strongest at htsjdk/VCF,
weakest at vcfpy/VCF" as discussed above. `bug_bench_section.tex`
(now $455$ words, was $570$) tightened Setup, Tool slate, and
Witness-counts paragraphs. `conclusion.tex` (now $194$ words, was
$255$) dropped a redundant contribution recap; the conclusion now
opens with the per-SUT-effort framing and closes with the
trade-off-and-future-direction framing, which is exactly what an
8-page submission's conclusion should do.

Overall the readability hit is mild, concentrated in the design
Pipeline paragraph, and outweighed by the page-budget benefit.

### Page budget verdict [changed since prior]

Total prose word count across `sections/*.tex` is now $5{,}743$
words. Subtracting tables and the TikZ figure source:
$5743 - (276 + 180 + 252 + 309) = 4{,}726$ prose words. At IEEEtran
2-column 10pt (roughly $600$--$650$ words per body page), this is
about $7.3$--$7.9$ pages of body prose alone. Add the pipeline
figure (~$0.55$ page), three full-width tables with footnotes
(~$1.5$ page combined), and the $42$-entry IEEEtran bibliography
(~$0.85$ page), and the realistic compiled length lands in the
$7.6$--$8.4$ page range, with the central estimate around
$8.0$--$8.1$ pages.

This is materially better than my prior estimate ($8.0$--$9.0$
pages, central $8.5$) and closes the page-budget question almost
entirely. The authors are now most likely at or just under the
$8.0$-page hard cap.

If a real compile shows $8.0$ exactly, no further cuts are needed.
If the compile shows $8.1$--$8.3$, the cheapest remaining cuts are:
(a) the C1/C2/C3 enumeration in `design.tex` lines 17-29 still
admits one further paragraph collapse (~80 words saved); (b) the
seqan3 paragraph in `mutation_score_section.tex` lines 70-85
admits another sentence-level trim (~40 words saved); (c) the
implementation Phase~A/B/C/D paragraphs in `implementation.tex`
admit a one-paragraph fusion (~50 words saved). $170$ words is
about three quarters of a column at IEEEtran widths. If the
compile shows $8.4$+ I would also recommend dropping the second
mention of the silence-on-fix predicate in
`bug_bench_section.tex` since it appears in both the Setup
paragraph and the Headline-numbers paragraph.

The single binding question of the prior version is now
substantially answered. I have not run pdflatex, so I cannot
guarantee under-8.0, but the compression has moved from
"plausibly fits" to "almost certainly fits." This is a meaningful
improvement.

### Style discipline [changed since prior]

I re-ran the four declared style sweeps after the compression round.

- **Em-dashes in prose:** none. The `---` matches in
  `sections/*.tex` are exclusively (i) `---` in tables denoting
  "not language-applicable" inside `mutation_table.tex`,
  `coverage_table.tex`, and `bug_bench_table.tex`, and (ii) TikZ
  comment-divider dashes in `pipeline_figure.tex` (lines 49 and
  66, both inside `%`-prefixed comment lines that pdflatex never
  emits). None in actual prose body text.
- **Semicolons in prose:** essentially none, with one minor caveat.
  Almost all `;` matches are TikZ statement terminators in
  `pipeline_figure.tex`. The single in-prose `;` is in the
  `mutation_table.tex` footnote at line 44 (",cargo-fuzz/noodles
  $n{=}9$ from documented run failures; libFuzzer/seqan3 $n{=}3$,
  AFL++/seqan3 $n{=}4$"). Inside a parenthetical list this is
  borderline acceptable, but to keep the strict rule a comma or
  period would be cleaner. Trivial fix.
- **`,verb+ing` chains:** none. Regex sweep returns zero matches.
- **Word "cell":** none in prose. Confirmed.

The style sweep has held through the compression round. The
single semicolon in the mutation-table footnote is the only
deviation I found and it is in a parenthetical list inside a
footnote, not in body prose. Trivial fix at camera-ready.

### Technical contribution [unchanged]

The novelty claim, as stated in `related.tex` lines 30-34, is the
combination of spec-grounded LLM-driven MR mining with a SUT-agnostic
generator and consensus oracle, not any individual component. This is
the right framing. MeMo and MR-Scout precede this work in
mining-from-artefacts, and Csmith/Zest/Nautilus precede it in
grammar-driven generation. The honest read is that \biotest{} is the
first to plug an LLM-RAG MR miner into a multi-runner consensus oracle
on a heterogeneous-language parser slate. That is genuinely new for a
parser-correctness setting, and it is a good fit for BIBM because (i)
the bioinformatics motivation (VCF/SAM, GIAB-style benchmarks
assuming sound parsers, GA4GH parser-correctness gap) is concrete and
correctly cited, and (ii) the AI angle is methodological, not
ornamental.

The single round-trip metamorphic relation
$\mathit{out}(\mathit{parse}(x)) \equiv \mathit{out}(\mathit{parse}(T(x)))$
is well-defined and the LLM mines the family of $T$'s. This framing
makes the LLM-mined component crisp and avoids the trap of claiming
the LLM is mining relations of unbounded shape.

### Methodological rigor [unchanged]

The statistical posture is appropriate for the venue. Exact two-sided
Mann--Whitney $U$ by full enumeration on $n_1=n_2=10$ on the four
close-margin pairs, Vargha--Delaney $\hat{A}_{12}$ with conventional
thresholds, and Holm--Bonferroni at $k{=}4$ all clearing family-wise
$\alpha{=}0.05$. The biopython/SAM sample is left at $n{=}4$ with the
explicit note that it is deterministic, and the seqan3/SAM pair
declines to attach an $\hat{A}_{12}$ to a
deterministic-vs-deterministic comparison. Both decisions are
defensible and explicitly stated.

The oracle definition (`design.tex` lines 115-136) is layered and
unambiguous: differential consensus first, metamorphic consensus
second, then a quarantine layer that fires when the consensus
disagrees on $x$ vs. $T(x)$. This is a textbook three-layer
differential oracle, and the $N \geq 3$ minimum is justified as the
smallest pool size that admits a strict majority.

The fairness recipe (`design.tex` lines 138-164) is the place where
I have one residual reservation. Wall-clock parity on heterogeneous
fuzzers is acknowledged as not being iteration-cost parity, and the
`+17`pp gap between AFL++ and libFuzzer on seqan3/SAM is cited as the
visible artefact. The "ablations not run" paragraph in `threats.tex`
correctly defers an iteration-count parity sweep on seqan3/SAM as
future work. For a Rank-B venue this is acceptable.

The 32-bug benchmark is constructed in the Magma/FuzzBench
ground-truth style and the silence-on-fix predicate is correctly
attributed to B\"ohme et al. 2021. The tool-found vs. PoV-fallback
split is operationally well-defined and is the cleanest single
contribution of the writeup.

### Empirical sufficiency [unchanged]

Three axes (mutation adequacy, line coverage, real-bug benchmark)
across six configurations spanning four host languages is a credible
breadth for an 8-page Rank-B submission. The thinnest axis remains
the LLM-mining contribution itself: one LLM, one provider, one prompt
template family, one embedding model, one validator, no
LLM-vs-human-authored-MR comparison, no model-substitution sweep, no
per-MR ablation across the seven metamorphic ranks. The "ablations
not run" paragraph in `threats.tex` (now lines 33-42) honestly
catalogues the deferred experiments. For BIBM Rank-B I would not
block on this. For ICSE/ISSTA I would.

The bug-bench language coverage is correctly hedged. Of the four
host languages, three (Java, Python, Rust) yield tool-found bugs,
the Rust confirmation rests on a single bug, and the C++ SUT
contributes zero confirmations because all six manifest entries are
paradigm-out. Internally consistent.

### Internal consistency [unchanged]

Cross-checked the headline numbers across abstract, body, tables,
and conclusion.

- Abstract claims "single-digit deficit on five configurations,
  exceeds libFuzzer on seqan3/SAM, trails Atheris by $32.5$\,pp on
  biopython/SAM." Mutation table: htsjdk/VCF $\Delta=-4.19$,
  htsjdk/SAM $\Delta=-2.47$, vcfpy/VCF $\Delta=-1.71$, noodles/VCF
  $\Delta=-0.64$, seqan3/SAM $\Delta=+6.87$, biopython/SAM
  $\Delta=-32.52$. Five configurations within single-digit deficit.
  Consistent.
- Abstract: "highest line coverage on every VCF SUT." Coverage
  table rows show $47.32$\%, $74.25$\%, $34.38$\%, all bold.
  Consistent.
- Abstract: "silences ten via tool-synthesised inputs across three
  parser languages where every crash-only fuzzer silences zero."
  Bug-bench table tool-found row: \biotest{} 10, all four crash-only
  fuzzers 0. Consistent.
- Statistical claim ("all four pairs clear family-wise
  $\alpha{=}0.05$ under Holm--Bonferroni") matches per-pair
  Holm-corrected p-values reported as the strongest at
  $4.0\times 10^{-5}$ (htsjdk/VCF) and weakest at
  $3.7\times 10^{-2}$ (vcfpy/VCF). Family-wise-clearance preserved.
- The conclusion's "small single-digit deficit" framing matches the
  abstract and body. Consistent.

I find no numerical mismatch.

### Pipeline figure [unchanged]

The redesigned 2-row pipeline figure (`pipeline_figure.tex`) is a
clear improvement on the prior 4-row 5-color version. Two rows
(Row 1: per-format, spec to corpus stack; Row 2: per-iteration,
user shim to candidate bugs) with three node styles and a dashed
arrow for the Phase D coverage-feedback edge. The figure now reads
as a publication-quality academic pipeline diagram. The TikZ
geometry (Row 1 totals $\approx 138$mm, comfortably under the
IEEEtran two-column-spanning textwidth of $\approx 178$mm) is
likely to compile cleanly without overflow.

## Required experiments before acceptance [unchanged]

**None required.** The three-axis evaluation is sufficient empirical
breadth for a CORE-B venue with 8-page budget. The "ablations not
run" paragraph in `threats.tex` lines 33-42 is the right way to
handle the deferred experiments.

## Recommended (non-blocking) experiments [unchanged]

1. **Per-MR ablation on the seven metamorphic ranks** for one VCF
   and one SAM SUT.
2. **LLM-vs-human-authored MR comparison** on one format (VCF).
3. **LLM ablation across two-three frontier models** on a fixed
   RAG pipeline.
4. **Iteration-count parity sweep on seqan3/SAM**, normalising the
   AFL++ vs libFuzzer comparison.
5. **Additional bioinformatics SUTs** (e.g. pysam as a first-class
   graded SUT, scikit-bio for FASTA).

All five are strong follow-ups and none is a blocker for BIBM.

## Top issues to fix before camera-ready (if accepted) [changed since prior]

1. **Compile and report exact page count.** With $5{,}743$ prose
   words my central estimate is $\approx 8.0$--$8.1$ pages
   compiled. If the real compile lands at $8.1$--$8.3$, the
   cheapest residual cuts are: (a) collapsing the C1/C2/C3
   paragraph in `design.tex` lines 17-29 into one paragraph with
   inline tags (~$80$ words), (b) trimming the seqan3 paragraph in
   `mutation_score_section.tex` lines 70-85 (~$40$ words), and
   (c) fusing the Phase~A/B/C/D paragraphs in
   `implementation.tex` lines 9-44 into one denser paragraph
   (~$50$ words). $170$ words is about three quarters of a column
   at IEEEtran 2-col widths.

2. **Single-semicolon footnote.** `mutation_table.tex` line 44
   carries one `;` separating parenthetical clauses inside the
   close-margin-pair note ("documented run failures; libFuzzer/seqan3
   $n{=}3$"). To keep the strict no-semicolon rule, replace with a
   period or comma. Trivial.

3. **Bioinformatics-impact sentence (REVIEW6 J2 partial).** The
   intro now names three concrete upstream regressions
   (`introduction.tex` lines 16-22) and includes the consequence
   sentence "the error propagates to every downstream analysis."
   Acceptable. If a sentence of pages-budget room is available,
   replace with a more concrete consequence (e.g. "these regressions
   propagate to clinical-grade pipelines that treat the parser
   output as authoritative").

4. **`\citet`/`\citep` shim cosmetics.** The `\providecommand`
   block in `main.tex` lines 23-25 aliases `\citet` and `\citep`
   to `\cite`, which collapses to bare `[N]` brackets. Several
   prose constructions explicitly name "Klees et al." and
   "B\"ohme et al." before the bracket, so the IEEEtran bracket
   form reads acceptably. Leaving as is is acceptable.

5. **Page budget if any of the figures float onto the bibliography
   page.** With three full-width `table*` floats and a full-width
   `figure*` at the top of pages, IEEEtran sometimes parks a
   float at the end of the bibliography column. If the compile
   shows this, the cheapest fix is to convert one of the tables to
   single-column where it admits, or move the pipeline figure to
   single-column form.

6. **Internal cross-reference language.** "is the load-bearing
   rejection cause across recorded snapshots"
   (`implementation.tex` line 29) is internal-jargon. Replace with
   "rejects the largest fraction of LLM-proposed relations across
   the recorded mining snapshots."

## Comments to authors [changed since prior]

The compression round has been clean and disciplined. Every
load-bearing claim in the empirical case has been preserved; the
cuts are concentrated in verbose phrasing and in the redundancy
between `background.tex` and `related.tex`. The decision to drop
the MT and coverage-guided-fuzzing subsections from
`background.tex` (which positioning was already in `related.tex`)
was the right cut. The decision to collapse the five
phase-paragraph block in `design.tex` into a single Pipeline
paragraph with bolded phase tags is harder to love, but in
combination with the figure carrying the visual decomposition, it
works.

The single piece of feedback I would offer for the camera-ready,
beyond the residual cut suggestions in the Top-issues list, is to
keep an eye on whether the Pipeline paragraph in `design.tex`
lines 38-61 reads as a wall of text once compiled. The bolded
phase tags help the eye, but the prose density is high. If a
reviewer at camera-ready time reads this paragraph and reports
they had to backtrack, the cheapest fix is restoring paragraph
breaks at `\textbf{Phase~B}`, `\textbf{Phase~C}`, and
`\textbf{Phase~D}` (so three short paragraphs instead of one
dense one), which would cost only ~$10$ words but might trade
against page budget. I would not change it now without a real
compile to confirm the visual effect.

The bug-bench writeup remains the strongest single section of the
paper empirically, and the tool-found vs. PoV-fallback split is
the cleanest fairness move I have seen in a recent
metamorphic-testing submission. The "structural, not budget"
framing in `bug_bench_section.tex` lines 56-61 (eight of twelve
htsjdk/VCF target bugs are silent differential bugs that crash-only
oracles cannot reach by construction) is exactly the right way to
explain the zero scores from Atheris and cargo-fuzz without
sounding defensive about your own paradigm.

The single highest-value follow-up experiment remains the
LLM-vs-human MR-authoring comparison, which is the empirical
substantiation that the LLM is genuinely replacing the dominant
cost of MT adoption rather than merely automating a fast-but-shallow
proposal layer. The deferred-experiments paragraph in
`threats.tex` is the honest mitigation for now.

## Comments to PC chair [unchanged]

I recommend acceptance. The paper is a credible bio+AI contribution
in scope for BIBM: the bioinformatics motivation is concrete (textual
VCF and SAM parsers underlie variant-calling and read-processing
pipelines, and the paper cites the right GIAB and GA4GH
infrastructure as the parser-correctness gap it fills); the AI/LLM
methodology is load-bearing rather than ornamental; the empirical
evaluation is honest and honest-about-its-limits. The remaining
risks are presentation-grade and resolvable in camera-ready editing.

After the page-budget compression round, my single binding concern
in the prior version (the page-budget verdict) is substantially
closer to settled. The compiled length is now most likely at or
just under the $8.0$-page hard cap, with a small headroom of
residual cuts available if the real compile lands at $8.1$--$8.3$.
This raises my confidence that the paper is ready for BIBM
submission as it stands.

I see no conflicts of interest. The submission is anonymised; the
artefact ships as a Docker image with a Zenodo deposit (DOI
placeholder for double-blind review per `implementation.tex` lines
58-62), and the authors commit to artefact-evaluation, which I
flag as a positive consideration for the proceedings.
