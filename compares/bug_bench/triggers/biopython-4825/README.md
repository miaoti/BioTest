# biopython-4825 — SAM parser excessive `copy.deepcopy`

**Severity**: performance regression with correctness-at-scale impact
  (timeouts on benchmark runs; risk of truncation in bounded
  harness time).
**Format**: SAM (plain text).
**Anchor**: pre_fix = Biopython 1.85, post_fix = Biopython 1.86
  (PR #4837 merged 2024-09-23).
**Issue / PR**: https://github.com/biopython/biopython/issues/4825

## What the bug does

`Bio.Align.sam.AlignmentIterator.__next__` around line 702 does
`copy.deepcopy(self.targets[index])` for every record. For each
`SeqRecord` target this recursively copies every attribute, but only
two (`_seq` and `annotations`) actually need a per-alignment copy —
everything else is safe to share. On a 200 000-alignment benchmark
the deepcopy cost is >50 % of parser runtime.

The bench-relevant impact: at the bench's 2 h budget, on large inputs
the parser may exhaust time before finishing, silently producing a
truncated alignment list that downstream code treats as complete.
That makes it a *correctness* bug in the presence of a wall-clock
limit, not just a "slow".

## Trigger

Any SAM with ≥ ~10 000 alignments against one or more long targets
will show it. For a smoke-test scale trigger we replicate one
alignment ~5 000 times (small enough to load in seconds post-fix,
noticeably slow pre-fix).

## Files

- `original.sam` — a 3-alignment seed SAM (enough for correctness
  check; for a perf-demo use `generate_large_sam.py`).
- `generate_large_sam.py` — inflates the seed to 10 000 alignments;
  useful for the timed-parse comparison.
- `reproduce.py` — times parse of the large SAM under pre-fix vs
  post-fix Biopython.
- `issue_source.txt` — excerpt of issue #4825.

## Detection criterion

- **Expected signal**: `timeout_or_differential_disagreement` against
  `htsjdk` / `pysam`. Quantitatively: parse(10k reads) > 5 s on pre-
  fix 1.85 vs < 1 s on post-fix 1.86 on a modern laptop, with the
  same output shape. The bug-bench driver can also treat
  timeout-on-pre-fix / success-on-post-fix as a detection.
