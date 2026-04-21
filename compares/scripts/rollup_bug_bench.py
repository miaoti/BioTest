#!/usr/bin/env python3
"""Walk a bug-bench results tree and emit a unified aggregate.json.

Used both by per-chat partial rollups (under /tmp/bug_bench_chatN/)
and by Chat 6's canonical rollup (under compares/results/bug_bench/).
"""
import argparse
import json
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bench-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    records = []
    for result in args.bench_root.rglob("result.json"):
        if result.parent.parent.name == args.bench_root.name:
            continue
        try:
            records.append(json.loads(result.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"[rollup] skip {result}: {e}")
    args.out.write_text(
        json.dumps({"results": records}, indent=2), encoding="utf-8",
    )
    print(f"[rollup] {len(records)} records -> {args.out}")


if __name__ == "__main__":
    main()
