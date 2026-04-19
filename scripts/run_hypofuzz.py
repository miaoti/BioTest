#!/usr/bin/env python3
"""
HypoFuzz CI entry — Rank 7 lever.

Drives `tests/test_hypofuzz_targets.py` under HypoFuzz's coverage-guided
fuzzer instead of plain Hypothesis. HypoFuzz plugs branch-coverage signals
into Hypothesis's strategy choices, so it explores valid-but-unusual
parser inputs more aggressively than `target()`'s scalar objective.

Usage (from repo root):
    py -3.12 scripts/run_hypofuzz.py [--minutes N]

Reference: HypoFuzz docs at https://hypofuzz.com/, Hatfield-Dodds 2024-2026.
JFuzz / Zest precedent: Padhye et al., ISSTA 2019,
  DOI 10.1145/3293882.3339002.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run HypoFuzz against tests/test_hypofuzz_targets.py",
    )
    parser.add_argument(
        "--minutes", type=float, default=10.0,
        help="Wall-clock budget in minutes (default: 10).",
    )
    parser.add_argument(
        "--target-file", default="tests/test_hypofuzz_targets.py",
        help="Path to the HypoFuzz target file.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    target = repo_root / args.target_file
    if not target.exists():
        print(f"Target file not found: {target}", file=sys.stderr)
        return 1

    try:
        import hypofuzz  # noqa: F401
    except ImportError:
        print(
            "hypofuzz not installed. Run: py -3.12 -m pip install hypofuzz",
            file=sys.stderr,
        )
        return 1

    seconds = int(args.minutes * 60)
    cmd = [
        sys.executable, "-m", "hypofuzz", "run",
        "--seconds", str(seconds),
        str(target),
    ]
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(repo_root))
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd, env=env, cwd=str(repo_root))


if __name__ == "__main__":
    sys.exit(main())
