# Bug-Bench Review Packet — ready for sign-off

**Purpose**: one-page summary you (the user) use to decide whether
`compares/bug_bench/manifest.verified.json` is fit to drive Phase 4.
Once you're satisfied, no further edits until Phase 4 completes, per
DESIGN.md §13.4.5.

**Generated**: 2026-04-19, post second research pass + CRAM-scope drop.

---

## Headline numbers

| | Count |
| :--- | :---: |
| Candidate bugs in `manifest.json` | **44** (after two research passes) |
| Verified (versions install + format in scope + signal plausible) | **23** |
| Dropped | **21** |
| Yield | 52% |

Inside the 18–25 forecast in DESIGN.md §5.2 → bench runs at the full
2 h × 1 rep budget per (tool, bug).

## The 23 verified bugs

Full per-bug reference with categories, signals, and descriptions is
in `compares/bug_bench/CATALOGUE.md` (regenerable via
`render_catalogue.py`) and mirrored compactly in DESIGN.md §13.4.7.

Per-SUT bench shape:

| SUT | Verified | VCF | SAM (or SAM-adjacent) |
| :--- | :---: | :---: | :---: |
| htsjdk | **12** (was 2 after the CRAM drop) | 9 — `1554`, `1637`, `1364`, `1389`, `1372`, `1401`, `1403`, `1418`, `1544` | 3 — `1561`, `1538`, `1489` |
| pysam | **4** (was 2) | 2 — `1314`, `1308` | 2 — `1214`, `939` |
| biopython | 1 | 0 | 1 — `4825` |
| seqan3 | 6 | 0 | 5 SAM (`2418`, `3081`, `3269`, `3098`, `3406`) + 1 FASTA-adjacent (`2869`) |
| **total** | **23** | **11** | **12** |

See `CATALOGUE.md` (regenerable via `render_catalogue.py`) for the
authoritative per-bug format, category, and detection signal. Mirrored
compactly in DESIGN.md §13.4.7.

## The 21 drops — reason breakdown

| Category | Count | IDs |
| :--- | :---: | :--- |
| **UNRESOLVABLE — no PR linkage** | 11 | htsjdk-1117, htsjdk-1686, htsjdk-1026, htsjdk-761, htsjdk-423, pysam-1225, pysam-771, biopython-4731, biopython-1913, biopython-1699, biopython-4769 |
| **Feature gap (not a bug)** | 1 | biopython-4868 |
| **Pre-fix pysam build-rot on modern Python** | 6 | pysam-450 (0.11.0), pysam-641 (0.16.0), pysam-904 (0.15.0), pysam-966 (0.16.0), pysam-1038 (0.16.0), pysam-1175 (0.20.0) |
| **Out of scope — CRAM not VCF/SAM** | 3 | htsjdk-1708, htsjdk-1590, htsjdk-1592 |

Details: `compares/bug_bench/dropped.json`.

### Why CRAM is out of scope

Every runner in the repo declares `supported_formats = {"VCF", "SAM"}`
or narrower. `BioTestHarness.java` contains zero CRAM code paths. The
three CRAM bugs would require a CRAM-aware harness + coverage wiring
that doesn't exist — adding them is a research extension, not a
bench-readiness gap. Their trigger folders and research remain under
`triggers/htsjdk-{1708,1590,1592}/` for the day CRAM support lands.

## Flagged concerns for the user

Things that might warrant a second look before you green-light:

1. **htsjdk cohort is now 12 bugs** (was 2 after CRAM drop). Much
   healthier, but most new entries sit in the 2.19–3.0 release range.
   If you want to include a 4.x cohort, a third research pass on
   htsjdk 4.x release notes can be added; current scan covered
   releases through 3.0.1 exhaustively and pulled 4.1.1 (1708) but
   that was CRAM.
2. **pysam-939** description is thin — "long-standing AlignmentFile
   bug" per the 0.22.0 NEWS one-liner; specific input shape wasn't
   called out. Install-verified but detection may need bench-time
   discovery. Consider flagging as low-confidence.
3. **htsjdk-1489** ("locus accumulator") confidence was rated medium
   because the release-notes sentence was truncated in the scan;
   verify against the PR body before sign-off if you want it at
   high confidence.
4. **seqan3-3406 is a BGZF data race**: non-deterministic, won't
   reliably fire under single-threaded fuzzing. Flag as
   "stress-only" in the report.
5. **seqan3-2869 is FASTA-adjacent**: fix handles FASTA IDs
   containing `>`, not strictly SAM. Keep as a seqan3 I/O regression
   and label the format accordingly in the final report.
6. **biopython-4825 is a perf regression**: detection is "pre-fix
   SUT doesn't finish in budget" vs "post-fix does". Valid per
   DESIGN.md §4.3 but softer than crash/diff signals.

## Sign-off checklist

When you're satisfied, either:

- [ ] Accept: the 23-bug frozen manifest is fit to drive Phase 4.
      Commit `manifest.verified.json`, `CATALOGUE.md`, and this file.
- [ ] Push back: raise any of the flagged concerns above, and we
      adjust the manifest (add, drop, re-confidence) before freezing.

A no-action sign-off is an implicit accept of all 23 entries as they
currently stand.
