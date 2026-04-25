#!/usr/bin/env python3
"""Recompute final-aggregate counters with the FOUND vs FOUND-pov split.

Reads the same record-classification logic the markdown report uses,
walks bug_bench_aggregate_final.json's vcf_results + sam_results, and
emits split counters so a reader can tell how many cells the tools
genuinely found vs how many were confirmed via the bench's
manifest-PoV fallback.

The original `vcf_confirmed` / `sam_confirmed` keys are preserved for
backwards compat; new keys `*_tool_found` and `*_pov_confirmed` are
added alongside.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "compares" / "results"

# Reuse the report's classify so the counters are consistent.
sys.path.insert(0, str(ROOT / "compares" / "scripts"))
from report_bug_bench_md import classify  # noqa: E402


def split_counts(records: list[dict]) -> tuple[int, int]:
    tool_found = sum(1 for r in records if classify(r) == "FOUND")
    pov_found = sum(1 for r in records if classify(r) == "FOUND-pov")
    return tool_found, pov_found


def main() -> None:
    agg_path = RESULTS / "bug_bench_aggregate_final.json"
    agg = json.loads(agg_path.read_text(encoding="utf-8"))
    vcf = agg.get("vcf_results", [])
    sam = agg.get("sam_results", [])

    vcf_tool, vcf_pov = split_counts(vcf)
    sam_tool, sam_pov = split_counts(sam)

    agg["vcf_tool_found"] = vcf_tool
    agg["vcf_pov_confirmed"] = vcf_pov
    agg["sam_tool_found"] = sam_tool
    agg["sam_pov_confirmed"] = sam_pov
    # Bench-level confirmed = tool-found + pov-confirmed (existing semantics).
    agg["vcf_confirmed"] = vcf_tool + vcf_pov
    agg["sam_confirmed"] = sam_tool + sam_pov
    agg["total_confirmed"] = agg["vcf_confirmed"] + agg["sam_confirmed"]
    agg["total_tool_found"] = vcf_tool + sam_tool
    agg["total_pov_confirmed"] = vcf_pov + sam_pov
    agg["counters_split_revision"] = "2026-04-25"

    agg_path.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    print(f"[counters] vcf: tool_found={vcf_tool} pov_confirmed={vcf_pov} "
          f"(confirmed={vcf_tool + vcf_pov} of {len(vcf)})")
    print(f"[counters] sam: tool_found={sam_tool} pov_confirmed={sam_pov} "
          f"(confirmed={sam_tool + sam_pov} of {len(sam)})")
    print(f"[counters] total: tool_found={vcf_tool + sam_tool} "
          f"pov_confirmed={vcf_pov + sam_pov} "
          f"(confirmed={agg['total_confirmed']} of {len(vcf) + len(sam)})")


if __name__ == "__main__":
    main()
