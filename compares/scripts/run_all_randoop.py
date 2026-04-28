"""Run the Randoop adapter across every htsjdk bug in the verified
manifest, then print and persist a one-line-per-bug summary.

Usage:
    python compares/scripts/run_all_randoop.py [--time-budget-s 600] [--out-root <dir>]

Sequential by design: each invocation forks several JVMs (Randoop main,
javac×2, JUnit×N), and Windows javac contends for the same lock under
parallel runs. 12 htsjdk bugs × 600 s budget caps wall time at 2 h, but
Randoop hits its `--output-limit` long before that on small classes
(~5–30 s per bug in practice).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTER = REPO_ROOT / "compares" / "scripts" / "tool_adapters" / "run_randoop.py"
MANIFEST = REPO_ROOT / "compares" / "bug_bench" / "manifest.verified.json"
OUT_ROOT = REPO_ROOT / "compares" / "baselines" / "randoop" / "results"
SUMMARY_JSON = OUT_ROOT / "summary.json"
SUMMARY_MD = OUT_ROOT / "summary.md"


def _bug_ids(manifest_path: Path, sut: str) -> list[str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [b["id"] for b in manifest["bugs"] if b["sut"] == sut]


def _run_one(bug_id: str, out_dir: Path, time_budget_s: int) -> dict:
    cmd = [
        sys.executable, str(ADAPTER),
        "--bug-id", bug_id,
        "--out-dir", str(out_dir),
        "--time-budget-s", str(time_budget_s),
    ]
    print(f"[run-all] {bug_id} -> {out_dir}", flush=True)
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - started
    rc = proc.returncode
    # Adapter's CLI prints adapter_result.json to stdout. Prefer reading
    # the on-disk artefact since it survives even if stdout was truncated.
    art = out_dir / "adapter_result.json"
    if art.is_file():
        try:
            adapter_json = json.loads(art.read_text(encoding="utf-8"))
        except Exception as e:
            adapter_json = {"error": f"adapter_result.json unreadable: {e}"}
    else:
        adapter_json = {"error": "adapter_result.json missing", "stderr": proc.stderr[-1000:]}
    adapter_json["_runner_rc"] = rc
    adapter_json["_runner_wall_s"] = duration
    return adapter_json


def _summary_row(r: dict) -> str:
    bug = r.get("bug_id", "?")
    pre = r.get("pre_fix", "?")
    post = r.get("post_fix", "?")
    gen = r.get("tests_generated", "?")
    pre_p = r.get("pre_pass_count", "?")
    post_p = r.get("post_pass_count", "?")
    crashes = r.get("crash_count", "?")
    notes = (r.get("notes") or "").strip().rstrip(";").strip() or "-"
    detected = "DETECT" if isinstance(crashes, int) and crashes > 0 else "miss"
    wall = r.get("_runner_wall_s")
    wall_s = f"{wall:.1f}s" if isinstance(wall, (int, float)) else "?"
    return (
        f"| {bug} | {pre} → {post} | {gen} | {pre_p}/{gen if gen != '?' else '?'} | "
        f"{post_p}/{gen if gen != '?' else '?'} | {crashes} | {wall_s} | {detected} | {notes} |"
    )


def _write_summary(rows: list[dict]) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(
        json.dumps(rows, indent=2, default=str), encoding="utf-8",
    )
    md = ["# Randoop bug-bench summary",
          "",
          f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}.",
          "",
          ("| bug | pre→post | tests | pre pass | post pass | crashes | wall | "
           "verdict | notes |"),
          "|:----|:---------|------:|---------:|----------:|--------:|-----:|:--|:--|"]
    md.extend(_summary_row(r) for r in rows)
    md.append("")
    detected_n = sum(1 for r in rows
                     if isinstance(r.get("crash_count"), int)
                     and r.get("crash_count", 0) > 0)
    md.append(f"**Detection rate**: {detected_n} / {len(rows)}")
    SUMMARY_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--out-root", type=Path, default=OUT_ROOT)
    p.add_argument("--time-budget-s", type=int, default=600)
    p.add_argument("--sut", default="htsjdk",
                   help="Only run bugs for this SUT (default htsjdk; "
                        "Randoop is Java-only)")
    args = p.parse_args()

    bug_ids = _bug_ids(args.manifest, args.sut)
    print(f"[run-all] {len(bug_ids)} {args.sut} bug(s): "
          f"{', '.join(bug_ids)}", flush=True)
    args.out_root.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    for bid in bug_ids:
        out_dir = args.out_root / bid
        out_dir.mkdir(parents=True, exist_ok=True)
        results.append(_run_one(bid, out_dir, args.time_budget_s))
        # Persist incrementally so progress survives a Ctrl-C.
        _write_summary(results)

    print("\n[run-all] DONE")
    print(f"\nSummary: {SUMMARY_MD}")
    detected_n = sum(1 for r in results
                     if isinstance(r.get("crash_count"), int)
                     and r.get("crash_count", 0) > 0)
    print(f"Detection rate: {detected_n} / {len(results)}")


if __name__ == "__main__":
    main()
