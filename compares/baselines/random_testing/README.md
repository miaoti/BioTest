# Pure Random Testing baseline

Byte-level random VCF / SAM file generator. Language-agnostic — works against all four SUTs (htsjdk, biopython, seqan3, pysam) because its output is a file, not a Java in-memory object.

This is the **floor baseline**: the expectation is that Validity Ratio hovers near zero (the probability of random bytes forming a parseable VCF header plus at least one valid record is vanishingly small) and Structural Coverage saturates far below BioTest because the SUT's parsers reject inputs on the first malformed token.

## Two generation modes (to be implemented)

### Mode A — Uniform random bytes

`generate_uniform.py` emits files of length drawn uniformly from [256, 8192] bytes, contents from `os.urandom`. Saves to `output/uniform/{vcf,sam}/`.

### Mode B — Structure-aware random

`generate_structural.py` starts from a required minimal skeleton (`##fileformat=VCFv4.5` or `@HD\tVN:1.6`) then appends random bytes. This is a slightly stronger random baseline — it passes the trivial first-line check but fails on any deeper constraint. Included because "pure random" vs "random with minimal header" is a useful contrast in the validity-ratio plot.

Both generators accept `--count N` and `--seed S` for reproducibility.

## Why this is in-house rather than downloaded

There is no canonical "pure random VCF/SAM fuzzer" project to cite; we implement a minimal one here so the semantics of the baseline are explicit and reviewable rather than "whatever tool X happens to do."

## Integration

`compares/scripts/coverage_sampler.py` treats this generator like any other tool: runs it for 300 s, passes the output files to the SUT-specific coverage-instrumented runners, samples coverage at 60 s intervals.

No mutation scoring against this baseline's suite is expected to produce meaningful kills — we still run it so the zero baseline is documented.
