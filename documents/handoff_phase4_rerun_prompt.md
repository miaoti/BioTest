# Handoff prompt — re-verify your tool against the new bug-bench infrastructure

Paste this into each of the per-tool detection chats (jazzer, pure_random,
evosuite_anchor, libfuzzer, atheris, cargo_fuzz). The bench's
verification predicate has been generalized — your tool's results may
change without your tool itself changing, so you need to re-run.

---

## What changed in the shared bug-bench infrastructure (2026-04-21)

Two changes affect every tool's run. Both live in the **bench
infrastructure** (`compares/scripts/bug_bench_driver.py` and the
shared manifests) — neither is tool-specific.

### Change 1 — Manifest revision (you must re-pull and re-read the manifest)

`compares/bug_bench/manifest.verified.json`,
`compares/bug_bench/manifest.sam_only.json`, and
`compares/bug_bench/manifest.vcf_only.json` were re-frozen on
2026-04-21. Total: 35 → 32 bugs (after two patches that day).

**Removed (6 bugs — none reachable through the bench's selection criteria):**

*Morning patch (file-level reachability — see DESIGN.md §5.1.1 criterion 1):*
- `biopython-4825` (perf-only)
- `htsjdk-1538` (API mutator-cache, not parse path)
- `htsjdk-1561` (release-notes anchor doesn't reproduce empirically)
- `htsjdk-1489` (locus pile-up API, not parse path)

*Afternoon audit (criteria 2 / 4 — empirical):*
- `vcfpy-gtone-0.13` (C2 ✗: sweep at `compares/bug_bench/sweep_logs/vcfpy-gtone-0.13.json` proves all versions 0.11.0 → 0.13.5 silence the trigger; pre-fix and post-fix produce identical output)
- `vcfpy-nocall-0.8` (C4 ✗: PyPI simple index proves vcfpy 0.8.1 was never published; pre-fix anchor pins a non-existent version)

**Added (3 SAM bugs — all parse-time htsjdk regressions):**
- `htsjdk-1238` (anchor 2.18.1 → 2.18.2): RNAME regex tightening; pre
  accepts comma-in-`SN:`, post throws `SAMException` from the
  constructor unconditionally.
- `htsjdk-1360` (anchor 2.19.0 → 2.20.0): EMPTY_READ removal; pre
  STRICT throws on zero-length read, post accepts.
- `htsjdk-1410` (anchor 2.20.2 → 2.20.3): TLEN limit raise; pre
  STRICT rejects |TLEN| > 2^29, post accepts up to int32-max.

PoVs are at `compares/bug_bench/triggers/htsjdk-{1238,1360,1410}/original.sam`.

Anchor sweeps may have corrected other anchors as well — read the
sweep logs at `compares/bug_bench/sweep_logs/<bug_id>.json` and the
current `manifest.verified.json` as ground truth.

### Change 2 — STRICT-stringency gate in the silence predicate

`bug_bench_driver._replay_trigger_silenced` (the post-fix verifier
used for every tool's confirmation) now queries each runner's
`supports_strict_parse` capability and short-circuits to `not silenced`
if the strict-parse rejects the trigger. This means:

- Cells where pre-fix STRICTLY rejects valid input that post-fix
  accepts (e.g. htsjdk-1360, htsjdk-1410) now confirm via forward
  §5.3.1 even though the runner's default-stringency parse succeeds.
- Cells where pre-fix wrongly accepts spec-invalid input that post-fix
  STRICTLY rejects (e.g. htsjdk-1238) now confirm via reverse §5.3.1.

Currently opt-in: htsjdk, pysam, vcfpy. Other runners default to
`supports_strict_parse: bool = False` and behave as before.

The bidirectional §5.3.1 + PoV reverse-fallback paths are also live —
see `compares/DESIGN.md §5.3.2` for the formal predicate.

## Your action items

1. **Pull latest `main`** (or whichever branch carries the manifest
   revision and the `bug_bench_driver` changes).
2. **Wipe stale per-cell outputs** for any bug that was either removed
   or whose ID was added:
   ```bash
   rm -rf compares/results/bug_bench/<your_tool>/{biopython-4825,htsjdk-1538,htsjdk-1561,htsjdk-1489,vcfpy-gtone-0.13,vcfpy-nocall-0.8}
   ```
3. **Re-run your tool against the revised manifest.** The standard
   driver invocation is unchanged; pass `--only-tool <your_tool>`:
   ```bash
   python3.12 compares/scripts/bug_bench_driver.py \
       --manifest compares/bug_bench/manifest.verified.json \
       --out compares/results/bug_bench \
       --only-tool <your_tool> \
       --time-budget-s 300
   ```
   For a SAM-only sweep, swap in `manifest.sam_only.json`.
4. **Inspect per-cell `result.json`** for the 3 new htsjdk SAM cells
   and the 4 dropped IDs. Expect the 3 new cells to confirm via the
   STRICT gate even on tools that don't generate the exact PoV byte
   shape — the canonical PoV is in the candidate list and the
   bench's verification predicate is what fires.
5. **Update your aggregate** — if your downstream report concatenates
   per-cell results, refresh it after the rerun and drop any rows for
   the 4 removed IDs.

## Quick reference

| where to look | what's there |
|:--|:--|
| `compares/DESIGN.md §5.3.1–§5.3.4` | formal predicate + manifest-anchor sweep + STRICT-gate docs |
| `compares/bug_bench/dropped.json` | per-bug drop reasons (with dates) |
| `compares/bug_bench/apply_sam_replacement.py` | atomic patch script for the 2026-04-21 SAM revision |
| `compares/bug_bench/sweep_anchors.py` | manifest-anchor sweep |
| `compares/bug_bench/sweep_logs/` | per-bug sweep verdicts |

## Fairness statement

Both changes are bench-level — they verify all tools' detections
through the same predicate, so they don't bias toward any specific
tool. The shared manifest is the single source of truth; if you see
a discrepancy, file it against the bench, not the tool.
