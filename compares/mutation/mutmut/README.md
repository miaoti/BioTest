# mutmut — Python mutation testing for biopython and pysam

mutmut is a source-to-source Python mutation tester. Used here to score test suites against **biopython** (`Bio.Align.sam`) and **pysam** (VCF/SAM reader/writer modules).

## Version

`mutmut==3.0.0` (or the latest 3.x at run time). Installed via pip.

## Scope restriction

Per `DESIGN.md` §3.3, mutate only VCF/SAM-relevant Python modules.

### biopython

```
paths_to_mutate = [
  "SUTfolder/python/biopython/Bio/Align/sam.py"
]
```

biopython does not officially support VCF, so the scope is SAM-only. If any `Bio.bgzf` or similar helper is reachable from `sam.py`, mutmut follows imports automatically — we document final reachable set in the results report.

### pysam

pysam is installed in the Docker image `biotest-pysam:latest`. To mutate it we need the package source on disk — already extracted to `coverage_artifacts/pysam/source/` by the existing Phase D pipeline. We point mutmut at that tree:

```
paths_to_mutate = [
  "coverage_artifacts/pysam/source/libcvcf.pyx",   # or whatever VCF source file exists
  "coverage_artifacts/pysam/source/libcsam.pyx",
  "coverage_artifacts/pysam/source/VariantFile.py",
  "coverage_artifacts/pysam/source/AlignmentFile.py"
]
```

The exact filenames will be confirmed once we inspect the extracted tree. `.pyx` Cython files are mutable as text — mutmut treats them as Python source even though they compile via Cython. We may need to skip files that don't compile under mutation; the pre-run smoke test will tell.

## Invocation (planned)

```
mutmut run \
  --paths-to-mutate="<path list above>" \
  --runner="<adapter script that runs the generated test suite>" \
  --tests-dir=compares/results/<tool_name>/tests
```

mutmut stores state in `.mutmut-cache/`; we namespace per (tool, sut) to avoid cross-contamination.

## Notes

- mutmut is slow for large modules; expect 30–60 min per SUT per tool within the 2-hour budget.
- Unlike PIT, mutmut does not natively report "reachable" vs "unreachable" mutants — we approximate reachability by intersecting with coverage.py's covered lines before starting mutation.
- For pysam we must run the test suite *inside* the Docker container to load the mutated module in the matching environment. The mutation driver script will handle that indirection.
