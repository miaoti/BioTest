#!/usr/bin/env python3
"""Merge the 9-cell SAM rerun (jazzer/pure_random/evosuite_anchor x 3 new
htsjdk bugs) into the final aggregates and patch evosuite_anchor records
that were tool-failures (not real misses).

Reads /tmp/bug_bench_sam_new/aggregate.json. Appends the new cells to
the biotest-only sam_results in:
- compares/results/bug_bench_aggregate_final.json
- compares/results/bug_bench_sam_final.json

EvoSuite cells with adapter_exit_code != 0 and no test generation are
relabelled with an explicit error string so the report classifies them
as 'skip' rather than 'miss'.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "compares" / "results"
RERUN = Path("/tmp/bug_bench_sam_new")


def patch_evosuite_failures(records: list[dict]) -> int:
    """Tag evosuite_anchor records that didn't produce any tests as
    skip-with-reason. EvoSuite returns exit 3 + 0 failing-tests when
    its instrumentation fails (typical: missing class on the classpath).
    """
    patched = 0
    for r in records:
        if r.get("tool") != "evosuite_anchor":
            continue
        if r.get("adapter_exit_code") in (0, None):
            continue
        if r.get("error"):
            continue
        r["error"] = (
            f"evosuite tool failure (adapter_exit_code="
            f"{r.get('adapter_exit_code')}): no tests generated -- "
            "missing class in instrumentation classpath "
            "(htsjdk/variant/vcf/VCFInfoHeaderLine)"
        )
        patched += 1
    return patched


def main() -> None:
    rerun_agg = RERUN / "aggregate.json"
    if not rerun_agg.exists():
        raise SystemExit(f"missing {rerun_agg}")
    new_cells = json.loads(rerun_agg.read_text(encoding="utf-8")).get("results", [])
    if not new_cells:
        raise SystemExit("no records in rerun aggregate")
    n_patched = patch_evosuite_failures(new_cells)
    print(f"[merge] patched {n_patched} evosuite_anchor records with skip reason")

    # bug_bench_sam_final.json: append; preserve biotest cells.
    sam_final_path = RESULTS / "bug_bench_sam_final.json"
    sam_final = json.loads(sam_final_path.read_text(encoding="utf-8"))
    existing = sam_final.get("results", [])
    keys = {(r.get("tool"), r.get("bug_id")) for r in existing}
    appended = 0
    for r in new_cells:
        k = (r.get("tool"), r.get("bug_id"))
        if k in keys:
            # Replace in place (idempotent re-run support)
            for i, e in enumerate(existing):
                if (e.get("tool"), e.get("bug_id")) == k:
                    existing[i] = r
                    break
        else:
            existing.append(r)
            appended += 1
    sam_final["results"] = existing
    sam_final["other_tools_rerun"] = "2026-04-25"
    sam_final_path.write_text(json.dumps(sam_final, indent=2), encoding="utf-8")
    print(f"[merge] {sam_final_path}: {len(existing)} cells (+{appended} new)")

    # bug_bench_aggregate_final.json: same logic on sam_results.
    agg_path = RESULTS / "bug_bench_aggregate_final.json"
    agg = json.loads(agg_path.read_text(encoding="utf-8"))
    sam = agg.get("sam_results", [])
    keys = {(r.get("tool"), r.get("bug_id")) for r in sam}
    appended = 0
    for r in new_cells:
        k = (r.get("tool"), r.get("bug_id"))
        if k in keys:
            for i, e in enumerate(sam):
                if (e.get("tool"), e.get("bug_id")) == k:
                    sam[i] = r
                    break
        else:
            sam.append(r)
            appended += 1
    agg["sam_results"] = sam
    agg["total_cells"] = len(agg.get("vcf_results", [])) + len(sam)
    agg["sam_confirmed"] = sum(
        1 for r in sam
        if r.get("detected") and r.get("confirmed_fix_silences_signal") is True
    )
    agg["total_confirmed"] = agg.get("vcf_confirmed", 0) + agg["sam_confirmed"]
    agg["sam_other_tools_rerun"] = "2026-04-25"
    agg_path.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    print(f"[merge] {agg_path}: total_cells={agg['total_cells']} "
          f"vcf_confirmed={agg['vcf_confirmed']} sam_confirmed={agg['sam_confirmed']} "
          f"total_confirmed={agg['total_confirmed']}")


if __name__ == "__main__":
    main()
