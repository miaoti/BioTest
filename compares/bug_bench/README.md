# Real-Bug Benchmark — Authoring & Execution Guide

This folder houses the real-bug benchmark for the comparative evaluation
(`compares/DESIGN.md` §5).

## What this is

A set of historical, GitHub-documented VCF/SAM-related bugs in the four
SUTs (`htsjdk`, `pysam`, `biopython`, `seqan3`). Each bug is anchored by a
pair of installable library versions — the version *just before* the fix
("pre-fix") and the version that shipped the fix ("post-fix"). BioTest
and the baseline fuzzers are pointed at the **pre-fix** version; each
tool is scored on whether it detects the bug within a fixed time budget.

The benchmark is modelled on **Magma** (Hazimeh, Herrera, Payer,
SIGMETRICS'20) — the canonical ground-truth fuzzing benchmark for
general-purpose fuzzers — adapted to use install-version anchoring rather
than source-patch application because the SUTs here are maintained as
released packages, not embedded in Magma's target harness.

## Files

- `manifest.json` — the authoritative bug list. 32 candidates at present;
  expected verified N after Phase-0 pre-flight: **18–25**.
- `triggers/<bug_id>/` — per-bug folder for hand-curated trigger inputs,
  evidence files pulled from the issue / PR, and minimised repro scripts.
  Folder created on demand.

## Manifest schema

Each entry in `manifest.json["bugs"]`:

```json
{
  "id": "pysam-1314",
  "sut": "pysam",
  "issue_url": "https://github.com/pysam-developers/pysam/issues/1314",
  "format": "VCF",
  "anchor": {
    "type": "install_version",
    "pre_fix":  "0.20.0",
    "post_fix": "0.21.0",
    "verification_rule": "release_notes_must_reference_1314_or_contig_remap"
  },
  "trigger": {
    "category": "incorrect_field_value",
    "logic_bug": true,
    "description": "…",
    "evidence_dir": "compares/bug_bench/triggers/pysam-1314/"
  },
  "expected_signal": {
    "type": "differential_disagreement",
    "against": ["htslib"]
  }
}
```

For seqan3 entries: `anchor.type = "commit_sha"`, with `pre_fix` set to
the parent commit of the merged fix and `post_fix` set to the merge
commit.

## Anchor types

| `anchor.type` | Meaning | Applies to |
| :--- | :--- | :--- |
| `install_version` | Install pre/post-fix via `pip` / Maven / system package manager | pysam, biopython, htsjdk |
| `commit_sha` | `git checkout` at the pre-fix parent / post-fix merge | seqan3 |
| `feature_gap` | Not actually a bug — context only | (drop candidates) |

## Verification protocol (Phase-0 pre-flight)

Before Phase 4 runs, each entry is verified:

1. **Install the pre-fix version** in a clean environment.
2. **Install the post-fix version** in a second clean environment.
3. **Confirm release-notes linkage**: the post-fix release's CHANGELOG /
   NEWS / release-notes must explicitly reference the issue number OR the
   PR that merged the fix.
4. **(Optional but preferred)** Construct a minimal trigger input from
   the issue evidence and confirm: the trigger elicits the expected
   signal on pre-fix AND does NOT elicit the signal on post-fix.
5. If **any** of (1)–(3) fail, the entry is **dropped** from the
   benchmark. Drop-list discipline per Böhme et al. ICSE'22.

Pre-flight is driven by:

```bash
py -3.12 compares/scripts/bug_bench_driver.py --verify-only \
        --manifest compares/bug_bench/manifest.json \
        --dropped-out compares/bug_bench/dropped.json
```

The driver writes `dropped.json` listing every entry that failed
verification and the reason. The final verified manifest is saved as
`manifest.verified.json` alongside the original.

## Why install-version anchoring instead of `git bisect`

Most htsjdk / pysam / biopython issues do **not** have a reliable
"bad commit" SHA in their GitHub metadata. Recovering it requires
bisecting across releases with drifted build configs (Gradle version
jumps, dropped JDK support, Python wheel vs source). The cost is hours
per bug × 26 bugs; many would fail to build at all.

Install-version anchoring is a pragmatic compromise:

- **Reproducible**: `pip install pysam==0.20.0` is deterministic (modulo
  PyPI / Maven availability).
- **Honest**: when a version can't be installed, the bug is dropped.
- **Calibrated**: the release boundary *is* the fix boundary for all bugs
  fixed by a single PR that landed in one release. Release-notes linkage
  is the verification.

The one downside: for bugs fixed mid-version (e.g., a follow-up patch in
the same release), install-version anchoring collapses the pre/post
distinction. Such bugs are dropped.

## Adding a new bug

1. Find a GitHub issue / PR in one of the four SUTs that:
   - Fixes a VCF or SAM parsing / writing / round-tripping bug.
   - Landed between 2020 and 2026.
   - Has a post-fix release whose release-notes reference the issue.
   - Ideally ships an input that triggers the bug (file, byte sequence,
     or minimal Python / Java snippet).
2. Add an entry to `manifest.json["bugs"]` with the schema above. Mark
   `pre_fix` / `post_fix` as `PENDING_VERIFICATION` if you haven't yet
   confirmed the exact versions.
3. (If available) drop the trigger evidence into
   `triggers/<bug_id>/original.{vcf,sam,bam,py,java}` and reference it
   in `trigger.evidence_dir`.
4. Open a PR or merge directly; run `--verify-only` pre-flight to confirm
   the entry is installable before including it in the next benchmark
   run.

## Running the bug-bench

After pre-flight:

```bash
py -3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.verified.json \
        --tool-adapter-dir compares/scripts/tool_adapters/ \
        --time-budget-s 7200 \
        --out compares/results/bug_bench/
```

Per-bug output lands in `compares/results/bug_bench/<tool>/<bug_id>.json`.
The aggregator `build_report.py` consumes those into the final heatmap
and TTFB violin plots.

## Detection criterion

Per `compares/DESIGN.md` §4.3, a tool "detects" a bug iff:

1. At least one input the tool generates, on the pre-fix SUT, elicits the
   expected signal type (`differential_disagreement`, `crash`,
   `uncaught_exception`, etc.).
2. The same input, replayed on the post-fix SUT, does **not** elicit the
   signal. This controls for spec-ambiguity false positives.

The detecting tool, the trigger input, and the TTFB are all recorded.

## Drop candidates (pre-verification)

The following entries are already flagged for likely drop during
pre-flight and are included in the manifest only so they can be
evaluated honestly:

- `biopython-4868` — feature gap, not a bug. Include only as narrative
  context in the report.
- `pysam-1038` — resource-leak bug, unlikely to fire in a 2h budget.
- `seqan3-2869` — FASTA-adjacent, may be out of SAM scope.
- `seqan3-3406` — BGZF data race; hard to reproduce deterministically.
- `biopython-4825` — primarily a performance regression; correctness
  impact secondary.
- `htsjdk-1026` — needs a multithreaded harness to reproduce.

## Change log

| Date | Change |
| :--- | :--- |
| 2026-04-19 | Initial manifest authored from 32 candidate bugs (DESIGN.md Appendix A). All entries `pending_phase_0_verification`. |
