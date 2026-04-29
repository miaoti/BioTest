# Coverage Notes — Index

Per-SUT, per-format, per-tool coverage measurements. One file per
`<sut>/<format>/<tool>` so a glance at the tree shows exactly which
combinations have been measured.

## Tree

```
coverage_notes/
  htsjdk/
    vcf/
      biotest.md     # all BioTest runs on htsjdk/VCF (Runs 1-8)
      evosuite.md    # EvoSuite 1.2.0 baseline on htsjdk/VCF
    sam/
      biotest.md     # BioTest runs on htsjdk/SAM (Run 9)
  biopython/
    sam/
      biotest.md     # BioTest runs on biopython/SAM (Run 1)
  seqan3/
    sam/
      biotest.md     # BioTest runs on seqan3/SAM (Run 1 — harness-level 95.3 %, DESIGN-scope 0/0 pending harness link to seqan3)
  vcfpy/
    vcf/
      biotest.md     # BioTest runs on vcfpy/VCF (Run 1 — 73.4 % weighted, 863/1 176 lines; + cross-tool comparison vs Atheris)
  noodles/
    vcf/
      biotest.md     # BioTest runs on noodles-vcf/VCF (Run 12 — 39.6 % weighted, 2 741/6 920 lines; + cross-tool comparison vs cargo-fuzz / Pure Random)
  pysam/             # (empty — future)

  MUTATION_SCORE_ANALYSIS.md   # Cross-SUT mutation-score report
                               # (Run-8 4-rep mean±std, citations,
                               # per-cell gap analysis vs baselines)
```

## Cross-cutting reports (not per-SUT)

- `MUTATION_SCORE_ANALYSIS.md` — cross-SUT mutation-score analysis
  based on the Run-8 4-rep measurements. Compares BioTest against
  jazzer / atheris / cargo-fuzz / libfuzzer baselines cell-by-cell
  with referenced literature citations. Read this when you need to
  explain *why* BioTest scores what it does relative to a baseline
  on a given cell — all six cells are covered.

## Guidelines for adding a measurement

1. File path mirrors the combination: `<sut>/<format>/<tool>.md`.
2. **Always compute numbers via `compares/scripts/measure_coverage.py`**
   — never write inline filter code. The script reads filter rules from
   `biotest_config.yaml: coverage.target_filters[<format>][<sut>]` so
   every tool and every run is graded on the same scope.
   See `compares/scripts/README.md` for the full fairness recipe and
   the checklist for adding a new baseline testing tool.
3. Include a timeline table if the same tool is re-run; never overwrite
   a prior run's numbers in place.
4. Name JaCoCo / coverage-data snapshots as
   `jacoco_post_<tool>_run{N}.xml` or equivalent and reference them by
   path; the per-run XMLs are the source of truth if a number is
   disputed later.
5. Keep bug-finding, feature-coverage, and SCC discussion separate from
   line-coverage — mix only when the same run produced both signals.
