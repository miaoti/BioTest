"""Phase-4 post-run review — walks bug_bench/ aggregate.json and:

  1. Summarises detection outcomes per (tool × SUT) cell.
  2. Flags every (tool, bug) cell where
     `confirmed_fix_silences_signal is None` so the operator can replay
     the trigger manually.
  3. Spot-checks up to N detection claims across distinct tools by
     re-running the trigger_input through the repo's ParserRunner (same
     mechanism _replay_trigger_silenced uses inside the driver).

Outputs:
  compares/results/bug_bench/post_run_review.json       (structured)
  compares/results/bug_bench/post_run_review.md         (human-readable)

Usage:
  python compares/scripts/post_run_review.py
  python compares/scripts/post_run_review.py \
      --bench-root compares/results/bug_bench --spot-check 3
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_aggregate(bench_root: Path) -> list[dict]:
    agg = bench_root / "aggregate.json"
    if not agg.exists():
        raise SystemExit(f"aggregate.json missing at {agg}")
    return json.loads(agg.read_text(encoding="utf-8")).get("results", [])


def _replay(sut: str, trig: Path, fmt: str) -> bool | None:
    """Mirror bug_bench_driver._replay_trigger_silenced; returns
    True if post-fix SUT handles cleanly, False if still raises,
    None if we can't replay (missing trigger, unknown SUT, runner err).
    """
    if not trig or not trig.exists():
        return None
    sys.path.insert(0, str(REPO_ROOT))
    try:
        if sut == "pysam":
            from test_engine.runners.pysam_runner import PysamRunner as R  # type: ignore
        elif sut == "biopython":
            from test_engine.runners.biopython_runner import BiopythonRunner as R  # type: ignore
        elif sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner as R  # type: ignore
        elif sut == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner as R  # type: ignore
        else:
            return None
        res = R().run(trig, fmt)
        return bool(getattr(res, "success", False))
    except Exception:
        return None
    finally:
        sys.path.pop(0)


def review(bench_root: Path, spot_check: int, seed: int = 0) -> dict:
    records = _load_aggregate(bench_root)
    per_cell: dict[tuple[str, str], Counter] = defaultdict(Counter)
    null_silences: list[dict] = []
    detected: list[dict] = []

    for r in records:
        tool = r.get("tool", "?")
        sut = r.get("sut", "?")
        per_cell[(tool, sut)]["total"] += 1
        if r.get("detected"):
            per_cell[(tool, sut)]["detected"] += 1
            detected.append(r)
        if r.get("detected") and r.get("confirmed_fix_silences_signal") is None:
            null_silences.append(r)

    # Spot-check: sample up to `spot_check` detections across distinct tools.
    rng = random.Random(seed)
    by_tool = defaultdict(list)
    for d in detected:
        by_tool[d["tool"]].append(d)
    sampled: list[dict] = []
    for tool in sorted(by_tool):
        if len(sampled) >= spot_check:
            break
        sampled.append(rng.choice(by_tool[tool]))
    replay_results = []
    for r in sampled:
        trig = Path(r.get("trigger_input") or "")
        fmt = "VCF" if r.get("sut") in {"pysam", "vcfpy", "noodles", "htsjdk"} else "SAM"
        replay_results.append({
            "tool": r["tool"], "bug_id": r["bug_id"], "sut": r["sut"],
            "trigger_input": str(trig),
            "post_fix_success": _replay(r["sut"], trig, fmt),
        })

    return {
        "records_total": len(records),
        "per_cell": {
            f"{tool}/{sut}": dict(counter)
            for (tool, sut), counter in sorted(per_cell.items())
        },
        "detected_total": len(detected),
        "null_silences_total": len(null_silences),
        "null_silences_sample": null_silences[:20],
        "spot_check": replay_results,
    }


def _render_md(summary: dict) -> str:
    lines = ["# Phase 4 post-run review\n"]
    lines.append(f"- records_total: {summary['records_total']}")
    lines.append(f"- detected_total: {summary['detected_total']}")
    lines.append(f"- null_silences_total: {summary['null_silences_total']}\n")
    lines.append("## Per-cell (tool/sut) detection counts\n")
    lines.append("| cell | total | detected |")
    lines.append("| :--- | ---: | ---: |")
    for cell, counts in summary["per_cell"].items():
        lines.append(f"| {cell} | {counts.get('total', 0)} | {counts.get('detected', 0)} |")
    lines.append("\n## Spot-check replays\n")
    if not summary["spot_check"]:
        lines.append("_no detected cells to spot-check_")
    else:
        lines.append("| tool | bug | sut | post_fix_success |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for s in summary["spot_check"]:
            lines.append(
                f"| {s['tool']} | {s['bug_id']} | {s['sut']} | {s['post_fix_success']} |"
            )
    return "\n".join(lines) + "\n"


def _cli() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path,
                   default=REPO_ROOT / "compares" / "results" / "bug_bench")
    p.add_argument("--spot-check", type=int, default=3)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    summary = review(args.bench_root, args.spot_check, args.seed)
    (args.bench_root / "post_run_review.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    (args.bench_root / "post_run_review.md").write_text(
        _render_md(summary), encoding="utf-8"
    )
    print(f"[post-run-review] {summary['records_total']} records, "
          f"{summary['detected_total']} detected, "
          f"{summary['null_silences_total']} null_silences.")


if __name__ == "__main__":
    _cli()
