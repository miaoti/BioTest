# Citation Audit -- biotest.bib (2026-04-27)

This audit re-verifies every entry in `biotest.bib` against authoritative
sources (DOI resolution, dblp records, publisher pages, project repositories).
A prior audit (`BIB_AUDIT.md`) flagged two `MAJOR` issues
(`metzman2021fuzzbench`, `vikram2023guiding`) and two `MINOR` BibTeX
type/field observations (`hazimeh2020magma`, `pham2021smartgreybox`).

The two prior `MAJOR` issues have been fixed in the current `biotest.bib`:
both author lists now match dblp exactly.

## Summary

- Total entries: **42**
- VERIFIED: **40**
- MINOR: **2** (`hazimeh2020magma`, `pham2021smartgreybox` -- BibTeX entry-type/field
  mismatch, but bibliographic facts are correct)
- MAJOR: **0**
- NOT FOUND: **0**
- AMBIGUOUS: **1** (`tian2023mrscout` -- intentional citekey/author mismatch
  documented in the `note` field; counted under VERIFIED for total)

Net: **clean, ready for submission, with 2 cosmetic BibTeX type fixes
recommended.**

## Per-entry findings

### just2014mutants
- Status: VERIFIED
- Bib: Just, Jalali, Inozemtseva, Ernst, Holmes, Fraser / 2014 / FSE 2014
  / "Are Mutants a Valid Substitute for Real Faults in Software Testing?"
- Verified against: DOI 10.1145/2635868.2635929 (ACM DL).
- Notes: pages 654--665 confirmed.

### andrews2005mutation
- Status: VERIFIED
- Bib: Andrews, Briand, Labiche / 2005 / ICSE 2005 / "Is Mutation an
  Appropriate Tool for Testing Experiments?"
- Verified against: DOI 10.1109/ICSE.2005.1553583, dblp AndrewsBL05.
- Notes: pages 402--411 confirmed.

### klees2018fuzz
- Status: VERIFIED
- Bib: Klees, Ruef, Cooper, Wei, Hicks / 2018 / CCS 2018 / "Evaluating
  Fuzz Testing"
- Verified against: DOI 10.1145/3243734.3243804.
- Notes: pages 2123--2138 confirmed.

### padhye2019zest
- Status: VERIFIED
- Bib: Padhye, Lemieux, Sen, Papadakis, Le Traon / 2019 / ISSTA 2019 /
  "Semantic Fuzzing with Zest"
- Verified against: DOI 10.1145/3293882.3330576, arXiv 1812.00078.
- Notes: pages 329--340 confirmed.

### barr2015oracle
- Status: VERIFIED
- Bib: Barr, Harman, McMinn, Shahbaz, Yoo / 2015 / IEEE TSE 41(5):507-525
  / "The Oracle Problem in Software Testing: A Survey"
- Verified against: DOI 10.1109/TSE.2014.2372785.

### papadakis2019mutation
- Status: VERIFIED
- Bib: Papadakis, Kintis, Zhang, Jia, Le Traon, Harman / 2019 / Advances
  in Computers 112:275-378 / "Mutation Testing Advances: An Analysis and Survey"
- Verified against: DOI 10.1016/bs.adcom.2018.03.015, dblp PapadakisK00TH19.

### coles2016pit
- Status: VERIFIED
- Bib: Coles, Laurent, Henard, Papadakis, Ventresque / 2016 / ISSTA 2016
  / "PIT: A Practical Mutation Testing Tool for Java (Tool Demo)"
- Verified against: DOI 10.1145/2931037.2948707.
- Notes: pages 449--452 confirmed.

### aschermann2019nautilus
- Status: VERIFIED
- Bib: Aschermann, Frassetto, Holz, Jauernig, Sadeghi, Teuchert / 2019 /
  NDSS 2019 / "NAUTILUS: Fishing for Deep Bugs with Grammars"
- Verified against: NDSS-symposium paper page.

### wang2019superion
- Status: VERIFIED
- Bib: Wang, Chen, Wei, Liu / 2019 / ICSE 2019 / "Superion: Grammar-Aware
  Greybox Fuzzing"
- Verified against: DOI 10.1109/ICSE.2019.00081.
- Notes: pages 724--735 confirmed.

### boehme2020boosting
- Status: VERIFIED
- Bib: Boehme, Manes, Cha / 2020 / ESEC/FSE 2020 / "Boosting Fuzzer
  Efficiency: An Information Theoretic Perspective"
- Verified against: DOI 10.1145/3368089.3409748 (also CACM reprint
  10.1145/3611019).
- Notes: pages 678--689 confirmed.

### arcuri2014statistical
- Status: VERIFIED
- Bib: Arcuri, Briand / 2014 / STVR 24(3):219-250 / "A Hitchhiker's
  Guide to Statistical Tests..."
- Verified against: DOI 10.1002/stvr.1486.

### jazzer2024
- Status: VERIFIED (tool reference)
- Bib: Code Intelligence GmbH / 2024 / GitHub project URL.
- Verified against: https://github.com/CodeIntelligenceTesting/jazzer.

### atheris2023
- Status: VERIFIED (tool reference)
- Bib: Google LLC / 2023 / GitHub project URL.
- Verified against: https://github.com/google/atheris.

### libfuzzer2024
- Status: VERIFIED (tool reference)
- Bib: LLVM Project / 2024 / LLVM docs URL.
- Verified against: https://llvm.org/docs/LibFuzzer.html.

### cargofuzz2024
- Status: VERIFIED (tool reference)
- Bib: The Rust Fuzzing Authority / 2024 / GitHub URL.
- Verified against: https://github.com/rust-fuzz/cargo-fuzz.
- Notes: "The Rust Fuzzing Authority" is the rust-fuzz GitHub org's
  self-styled handle; acceptable as institutional author.

### cargomutants2024
- Status: VERIFIED (tool reference)
- Bib: Pool, Martin / 2024 / GitHub URL.
- Verified against: https://github.com/sourcefrog/cargo-mutants.

### mutmut2024
- Status: VERIFIED (tool reference)
- Bib: Hovmoller, Anders / 2024 / GitHub URL.
- Verified against: https://github.com/boxed/mutmut.

### denisov2018mull
- Status: VERIFIED
- Bib: Denisov, Pankevich / 2018 / ICSTW 2018 / "Mull It Over: Mutation
  Testing Based on LLVM"
- Verified against: DOI 10.1109/ICSTW.2018.00024.
- Notes: pages 25--31 confirmed.

### fioraldi2020aflpp
- Status: VERIFIED
- Bib: Fioraldi, Maier, Eissfeldt, Heuse / 2020 / WOOT 2020 / "AFL++:
  Combining Incremental Steps of Fuzzing Research"
- Verified against: USENIX WOOT 2020 page.

### chen2018metamorphic
- Status: VERIFIED
- Bib: Chen, Kuo, Liu, Poon, Towey, Tse, Zhou / 2018 / ACM Comput. Surv.
  51(1) Article 4 / "Metamorphic Testing: A Review of Challenges and Opportunities"
- Verified against: DOI 10.1145/3143561.

### segura2016survey
- Status: VERIFIED
- Bib: Segura, Fraser, Sanchez, Ruiz-Cortes / 2016 / IEEE TSE
  42(9):805-824 / "A Survey on Metamorphic Testing"
- Verified against: DOI 10.1109/TSE.2016.2532875.

### chen1998metamorphic
- Status: VERIFIED
- Bib: Chen, Cheung, Yiu / 1998 / HKUST CS tech report HKUST-CS98-01
- Verified against: HKUST CS website tech-report PDF.
- Notes: bib correctly notes arXiv:2002.12543 republication.

### myers1979art
- Status: VERIFIED
- Bib: Myers / 1979 / Wiley / "The Art of Software Testing"
- Verified against: ISBN 0471043281 (Open Library, Wiley listing).

### mckeeman1998differential
- Status: VERIFIED
- Bib: McKeeman / 1998 / Digital Technical Journal 10(1):100-107 /
  "Differential Testing for Software"
- Verified against: dblp McKeeman98.

### lewis2020rag
- Status: VERIFIED
- Bib: Lewis et al. (12 authors) / 2020 / NeurIPS 33:9459-9474 /
  "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- Verified against: NeurIPS 2020 proceedings.

### tian2023mrscout
- Status: AMBIGUOUS (intentional, documented)
- Bib: Xu, Terragni, Zhu, Wu, Cheung / 2024 / ACM TOSEM 33(6) / "MR-Scout:
  Automated Synthesis of Metamorphic Relations from Existing Test Cases"
- Verified against: DOI 10.1145/3656340; preprint arXiv:2304.07548 (2023).
- Notes: citekey deliberately preserves the 2023 preprint year. The bib's
  `note` field documents this. Lead author of the journal version is Xu,
  not Tian -- this is correctly recorded in the bib.

### blasi2021memo
- Status: VERIFIED
- Bib: Blasi, Gorla, Ernst, Pezze, Carzaniga / 2021 / Journal of Systems
  and Software 181:111041 / "MeMo: Automatically identifying metamorphic
  relations in Javadoc comments for test automation"
- Verified against: DOI 10.1016/j.jss.2021.111041.

### danecek2011vcf
- Status: VERIFIED
- Bib: Danecek, Auton, Abecasis et al. / 2011 / Bioinformatics
  27(15):2156-2158 / "The Variant Call Format and VCFtools"
- Verified against: DOI 10.1093/bioinformatics/btr330, PubMed 21653522.

### li2009sam
- Status: VERIFIED
- Bib: Li, Handsaker, Wysoker et al. / 2009 / Bioinformatics
  25(16):2078-2079 / "The Sequence Alignment/Map Format and SAMtools"
- Verified against: DOI 10.1093/bioinformatics/btp352, PubMed 19505943.

### yang2011csmith
- Status: VERIFIED
- Bib: Yang, Chen, Eide, Regehr / 2011 / PLDI 2011:283-294 / "Finding and
  Understanding Bugs in C Compilers"
- Verified against: DOI 10.1145/1993498.1993532.

### krusche2019benchmarking
- Status: VERIFIED
- Bib: Krusche, Trigg, Boutros et al. (GA4GH Benchmarking Team) / 2019 /
  Nature Biotechnology 37(5):555-560 / "Best practices for benchmarking
  germline small-variant calls in human genomes"
- Verified against: DOI 10.1038/s41587-019-0054-x.

### zook2019giab
- Status: VERIFIED
- Bib: Zook, McDaniel, Olson et al. / 2019 / Nature Biotechnology
  37(5):561-566 / "An open resource for accurately benchmarking small
  variant and reference calls"
- Verified against: DOI 10.1038/s41587-019-0074-6.

### orawe2013concordance
- Status: VERIFIED
- Bib: O'Rawe et al. / 2013 / Genome Medicine 5(3):28 / "Low concordance
  of multiple variant-calling pipelines: practical implications for exome
  and genome sequencing"
- Verified against: DOI 10.1186/gm432, PMC 3706896.

### hazimeh2020magma
- Status: MINOR (BibTeX type/field cosmetic; bibliographic facts correct)
- Bib (current state): `@article` / Hazimeh, Herrera, Payer / 2020 /
  POMACS 4(3):49:1-49:29 / "Magma: A Ground-Truth Fuzzing Benchmark"
- Verified against: DOI 10.1145/3428334, dblp HazimehHP20.
- Notes: The current `biotest.bib` already uses `@article` with the
  POMACS journal name, volume 4, issue 3, pages 49:1-49:29. This is fully
  correct. The prior audit's MINOR observation has been resolved.
  (Re-verified 2026-04-27: the bib entry is `@article{hazimeh2020magma}`
  with `journal = {Proceedings of the ACM on Measurement and Analysis of
  Computing Systems (POMACS)}` and `pages = {49:1--49:29}`.)
  **Status downgraded to VERIFIED.** No fix needed.

### metzman2021fuzzbench
- Status: VERIFIED (was MAJOR in prior audit; now fixed)
- Bib (current state): Metzman, Szekeres, Simon, Sprabery, Arya / 2021 /
  ESEC/FSE 2021:1393-1403 / "FuzzBench: An Open Fuzzer Benchmarking
  Platform and Service"
- Verified against: DOI 10.1145/3468264.3473932, dblp MetzmanSSSA21.
- Notes: re-fetched dblp -- author list matches exactly. Prior audit's
  flagged authors ("Maximilien", "Stepanov", "Serebryany") are gone;
  "Simon, Laurent" and "Sprabery, Read" are present. **Fix applied. No
  further action needed.**

### pacheco2007randoop
- Status: VERIFIED
- Bib: Pacheco, Lahiri, Ernst, Ball / 2007 / ICSE 2007:75-84 /
  "Feedback-Directed Random Test Generation"
- Verified against: DOI 10.1109/ICSE.2007.37.

### vargha2000critique
- Status: VERIFIED
- Bib: Vargha, Delaney / 2000 / J. Educational and Behavioral Statistics
  25(2):101-132 / "A Critique and Improvement of the CL Common Language
  Effect Size Statistics of McGraw and Wong"
- Verified against: DOI 10.3102/10769986025002101.

### vikram2023guiding
- Status: VERIFIED (was MAJOR in prior audit; now fixed)
- Bib (current state): Vikram, Laybourn, Li, Nair, O'Brien, Sanna,
  Padhye / 2023 / ISSTA 2023:929-941 / "Guiding Greybox Fuzzing with
  Mutation Testing"
- Verified against: DOI 10.1145/3597926.3598107, dblp VikramLLNOSP23.
- Notes: re-fetched dblp -- author list matches exactly (7 authors,
  correct order). **Fix applied. No further action needed.**

### boehme2021estimating
- Status: VERIFIED
- Bib: Boehme, Liyanage, Wustholz / 2021 / ESEC/FSE 2021:230-241 /
  "Estimating Residual Risk in Greybox Fuzzing"
- Verified against: DOI 10.1145/3468264.3468570.

### gopinath2020mining
- Status: VERIFIED
- Bib: Gopinath, Mathis, Zeller / 2020 / ESEC/FSE 2020:172-183 /
  "Mining Input Grammars from Dynamic Control Flow"
- Verified against: DOI 10.1145/3368089.3409679.

### pham2021smartgreybox
- Status: MINOR (BibTeX type cosmetic; bibliographic facts correct)
- Bib (current state): `@article` / Pham, Boehme, Santosa, Caciulescu,
  Roychoudhury / 2021 / IEEE TSE 47(9):1980-1997 / "Smart Greybox Fuzzing"
- Verified against: DOI 10.1109/TSE.2019.2941681 (IEEE Xplore),
  arXiv 1811.09447, mboehme.github.io PDF.
- Notes: The current `biotest.bib` already uses `@article` with `journal
  = {IEEE Transactions on Software Engineering}`. This is fully correct.
  The prior audit's MINOR observation (an `@inproceedings` type) has been
  resolved. **Status downgraded to VERIFIED.** No fix needed.

### xia2024fuzz4all
- Status: VERIFIED
- Bib: Xia, Paltenghi, Tian, Pradel, Zhang / 2024 / ICSE 2024 /
  "Fuzz4All: Universal Fuzzing with Large Language Models"
- Verified against: DOI 10.1145/3597503.3639121, arXiv 2308.04748,
  software-lab.org PDF.

## Recommended fixes

**No mandatory fixes are required.** The two `MAJOR` errors flagged in
the prior audit (`metzman2021fuzzbench`, `vikram2023guiding`) have already
been corrected, and the two prior `MINOR` cosmetic issues
(`hazimeh2020magma`, `pham2021smartgreybox`) have also been resolved
(both are now `@article` entries with the correct journal fields).

**Optional polish (low-priority, no semantic impact):**

1. `cargofuzz2024` -- the institutional author "The Rust Fuzzing Authority"
   is the rust-fuzz GitHub org's self-styled handle and renders as
   "The Rust Fuzzing Authority"; this is acceptable but a more standard
   form would be "{Rust Fuzz Working Group}" or "{rust-fuzz Project}".
   Not a correctness issue.

2. The `lewis2020rag` entry is missing a DOI/URL field. The NeurIPS 2020
   paper has no DOI (NeurIPS proceedings traditionally don't), but adding
   `url = {https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html}`
   would help reviewers locate the paper. Optional.

3. `chen1998metamorphic` -- the existing `note` correctly mentions the
   arXiv republication. Optional: add `url =
   {https://arxiv.org/abs/2002.12543}` for direct accessibility.

None of the above are required for submission.
