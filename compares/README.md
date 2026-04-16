# compares/ — Comparative Evaluation

This folder holds the design and (eventually) execution artifacts for benchmarking **BioTest** against classical test-input-generation baselines (EvoSuite, Randoop, pure random testing) plus mutation-score measurement across the four SUTs (htsjdk, biopython, seqan3, pysam).

**Nothing here executes yet.** We are creating the structure and locking the methodology *before* the main BioTest Phase A–D evaluation finishes so that when it's time to run the comparison, the protocol is already fixed.

Read [`DESIGN.md`](./DESIGN.md) for the complete specification: baseline tools, metrics (Validity Ratio / Structural Coverage / Mutation Score), per-language mutation tooling, the SUT × tool applicability matrix, and open decisions.

Quick map:

- `baselines/` — EvoSuite, Randoop, random-testing (source fetched via `scripts/fetch_sources.sh`, gitignored)
- `mutation/` — PIT (Java), mutmut (Python), mull (C++) config notes
- `scripts/` — placeholder fetch/probe/driver/report scripts (to be implemented pre-run)
- `results/` — populated at run time (gitignored)

The `source/` subfolders under `baselines/` are **gitignored** — we pull upstream release artifacts on demand rather than vendoring them into this repo.
