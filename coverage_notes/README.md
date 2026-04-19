# Coverage Notes — Index

Per-SUT, per-format, per-tool coverage measurements. One file per
`<sut>/<format>/<tool>` so a glance at the tree shows exactly which
combinations have been measured.

## Tree

```
coverage_notes/
  htsjdk/
    vcf/
      biotest.md     # all BioTest runs on htsjdk/VCF (Runs 1-6)
      evosuite.md    # EvoSuite 1.2.0 baseline on htsjdk/VCF
    sam/             # (empty — no SAM runs yet)
  biopython/
    sam/
      biotest.md     # BioTest runs on biopython/SAM (Run 1)
  pysam/             # (empty — future)
  seqan3/            # (empty — future)
```

## Guidelines for adding a measurement

1. File path mirrors the combination: `<sut>/<format>/<tool>.md`.
2. Always report against the exact filter rules in
   `biotest_config.yaml: coverage.target_filters[<sut>][<format>]`.
   Copy those rules verbatim into the doc so the denominator is
   reproducible.
3. Include a timeline table if the same tool is re-run; never overwrite
   a prior run's numbers in place.
4. Name JaCoCo / coverage-data snapshots as
   `jacoco_post_<tool>_run{N}.xml` or equivalent and reference them by
   path; the per-run XMLs are the source of truth if a number is
   disputed later.
5. Keep bug-finding, feature-coverage, and SCC discussion separate from
   line-coverage — mix only when the same run produced both signals.
