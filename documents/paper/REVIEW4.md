# Rank-B publication readiness — open items only

This file is the running list of open issues that **must be addressed
before a Rank B submission** (SANER, ICST, ICSME, MSR, AST, BIBM).
Closed items from the prior review passes (REVIEW.md, REVIEW2.md,
REVIEW3.md) are not repeated here. Items that the prior reviews
classified as "would-strengthen" or "top-tier-only" are also not
repeated, since they do not block acceptance at Rank B.

## Status

**No blocking items remain.** The paper is ready for Rank B
submission as written, including BIBM. The single outstanding item
is the camera-ready artefact deposit listed below.

## Camera-ready item (universal)

### B2. Camera-ready Zenodo deposit
*Universal but not blocking at submission time.*

The artefact is currently committed to a Zenodo deposit with a DOI
placeholder pending camera-ready (this is acceptable for double-blind
submission). At camera-ready, replace the placeholder in
`implementation.tex` with the real DOI of the public-facing Zenodo
record, and ensure the record contains:

- the Docker image digest with a public registry URL;
- the source-tree snapshot at the submission commit;
- the verbatim MR-curation log;
- the per-pair raw kill counts and the bug-bench result records
  used to produce the tables.

This is a reproducibility-track item, not a content fix. SANER and
ICST artefact-evaluation tracks will check it.

## Items deferred as explicit future work

The following items appeared in earlier review passes and remain
useful to do eventually, but the threats section in the current
paper discloses each as a known limitation, and the prior Rank B
review (REVIEW3, the same reviewer) accepted these disclosures as
sufficient for acceptance. They are listed here only so that no
information from earlier passes is lost; none are blocking.

| Item | Status at Rank B | Disclosure in paper |
|---|---|---|
| Per-MR ablation (LLM-mined vs hand-coded contribution) | future work | `threats.tex` Internal-validity paragraph on MR cardinality |
| Ranks 1–7 vs Ranks 1–13 ablation across configurations | future work | `threats.tex` Limited-rank-ablation paragraph |
| Kill-aware vs outcome-fingerprint cmin Δ measurement | **CLOSED** (was future work) | measured: $+1.95$pp on \biotest/vcfpy, $+0.00$pp on \biotest/biopython, $+1.19$pp on Atheris/biopython under cmin trim. Disclosed inline in `design.tex` Pre-grading-cmin paragraph. Source data: `documents/paper/fix/M2.md`. |
| $n{=}10$ on close-margin configurations | **CLOSED** (was future work) | boost ran. All four close-margin pairs now clear family-wise $\alpha{=}0.05$ under Holm-Bonferroni at $k{=}4$: htsjdk/VCF Holm $p{=}4{\times}10^{-5}$, noodles/VCF $p{=}3.1{\times}10^{-3}$, htsjdk/SAM $p{=}9.5{\times}10^{-3}$, vcfpy/VCF $p{=}0.037$. Updated `mutation_table.tex` and `mutation_score_section.tex` statistical-posture paragraph. Source data: `documents/paper/fix/M3.md` §9. |
| Iteration-count vs wall-clock parity | future work | `design.tex` identical-budget paragraph |
| Hand-rolled differential-only baseline | future work | `bug_bench_section.tex` paradigm-gap paragraph |
| Pre-revision manifest replay | future work | `bug_bench_section.tex` Methodological-caveats paragraph |
| Strict-stringency-conditional column on the bug bench | future work | `bug_bench_section.tex` Methodological-caveats paragraph |
| Per-bug mechanism attribution (MR vs differential) | future work | `bug_bench_section.tex` Witness-counts paragraph |
| Tick-aligned BioTest coverage curve | future work | `coverage_section.tex` Setup paragraph (terminates on stop-criteria, not a fixed tick) |

Each of the remaining future-work items would strengthen a
top-tier submission, and none is expected by Rank B reviewers.

## Closed since REVIEW3

### M3 — n=10 boost on close-margin configurations (now closed by boost)

REVIEW3 §2 classified M3 as B-strengthen because the framing
repair was sufficient at Rank B and a quantitative boost was not
expected. The authors ran the boost. Per
`documents/paper/fix/M3.md` §9, six additional reps per cell per
side were generated under independent stochastic seeds. Achieved
$n$ on the four close-margin pairs:

- htsjdk/VCF: \biotest{} $n{=}10$, Jazzer $n{=}10$;
- noodles/VCF: \biotest{} $n{=}10$, cargo-fuzz $n{=}9$ (one boost
  rep failed the cargo baseline test);
- htsjdk/SAM: \biotest{} $n{=}10$, Jazzer $n{=}6$ (four of ten
  reps hit a documented PIT 0/0 anomaly);
- vcfpy/VCF: \biotest{} $n{=}10$, Atheris $n{=}6$ (four boost
  reps did not complete in the session).

Achieved Holm--Bonferroni-corrected $p$-values across the four-pair
family (k=4): htsjdk/VCF $4.0\times 10^{-5}$; noodles/VCF
$3.1\times 10^{-3}$; htsjdk/SAM $9.5\times 10^{-3}$; vcfpy/VCF
$3.7\times 10^{-2}$. **All four pairs clear family-wise
$\alpha{=}0.05$** (the Case-A outcome predicted by the §3 power
analysis). The descriptive ranking is now an inferential
conclusion. Updated text lives in
`mutation_score_section.tex` Setup and Statistical-posture
paragraphs and in `mutation_table.tex` row counts and footnote.

### M2 — Kill-aware vs outcome-fingerprint cmin (now closed by measurement)

REVIEW3 §2 classified M2 as B-strengthen because disclosure was
sufficient at Rank B and a quantitative re-run was not expected.
The authors ran the dual-policy comparison anyway and the data is
in `documents/paper/fix/M2.md`. Headline measurements at
$\mathit{keep}{=}200$, $\mathit{shuffle\_seed}{=}42$, $n{=}4$ reps:

- \biotest/vcfpy: kill-aware $87.94\%$ vs outcome-fingerprint
  $85.99\%$, $\Delta_{\mathrm{cmin}}{=}+1.95$pp.
- \biotest/biopython: kill-aware $25.24\%$ vs outcome-fingerprint
  $25.24\%$, $\Delta_{\mathrm{cmin}}{=}+0.00$pp (corpus is below
  the $\mathit{keep}$ cap; cmin is the identity).
- Symmetry stress test on Atheris/biopython (corpus does cross
  the cap): kill-aware $28.15\%$ vs outcome-fingerprint $26.96\%$,
  $\Delta_{\mathrm{cmin}}{=}+1.19$pp.

The selector's effect is determined by whether cmin actively
trims, not by which tool produced the corpus, which closes the
circularity worry. The headline mutation table does not need to be
re-stated under outcome-fingerprint as the load-bearing
comparison. A short measurement-driven disclosure now lives in
`design.tex` Pre-grading-cmin paragraph in place of the prior
assertion-only disclosure.

## Verdict

**Submit.** B2 is a camera-ready task; the submission itself does
not require any further content edits. BIBM-specific bioinformatics
citations have been added in `related.tex`
\S\ref{sec:related-bioinformatics}
(Krusche et al.\ 2019, Zook et al.\ 2019, O'Rawe et al.\ 2013).
