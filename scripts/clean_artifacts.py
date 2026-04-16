#!/usr/bin/env python3
"""
Clean stale Phase D artifacts before a fresh run.

Actions:
  - Archive bug_reports/BUG-* -> bug_reports/.archive/run_{timestamp}/
  - Clear coverage_artifacts/jacoco/jacoco.exec (accumulation file)
  - Clear coverage_artifacts/.coverage (biopython coverage.py data)
  - Clear coverage_artifacts/pysam/.coverage.* and summary.*.json (Docker fragments)
  - Remove data/feedback_state.json (fresh start, not resume)

Preserved:
  - data/mr_registry.json (we want to build on existing MRs)
  - coverage_artifacts/pysam/source/ (extracted pysam source for slice extraction)
  - coverage_artifacts/jacoco/jacocoagent.jar + jacococli.jar (tooling)
  - coverage_artifacts/gcovr.json (seqan3 coverage, if exists)

Usage:
    py -3.12 scripts/clean_artifacts.py           # interactive (asks before archiving)
    py -3.12 scripts/clean_artifacts.py --force   # no prompt
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def archive_bug_reports(force: bool) -> int:
    bug_dir = ROOT / "bug_reports"
    if not bug_dir.exists():
        return 0

    bugs = [p for p in bug_dir.iterdir() if p.is_dir() and p.name.startswith("BUG-")]
    if not bugs:
        print("  No old bug reports to archive.")
        return 0

    archive_root = bug_dir / ".archive"
    archive_root.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_target = archive_root / f"run_{ts}"

    if not force:
        ans = input(f"  Archive {len(bugs)} bug reports to {archive_target.name}? [y/N]: ")
        if ans.strip().lower() != "y":
            print("  Skipped.")
            return 0

    archive_target.mkdir(exist_ok=True)
    for b in bugs:
        shutil.move(str(b), str(archive_target / b.name))
    print(f"  Archived {len(bugs)} reports -> bug_reports/.archive/run_{ts}/")
    return len(bugs)


def clear_coverage_artifacts() -> int:
    cleared = 0
    cov_dir = ROOT / "coverage_artifacts"
    if not cov_dir.exists():
        return 0

    # JaCoCo exec file (htsjdk)
    jacoco_exec = cov_dir / "jacoco" / "jacoco.exec"
    if jacoco_exec.exists():
        jacoco_exec.unlink()
        print(f"  Cleared: jacoco/jacoco.exec")
        cleared += 1

    # coverage.py top-level data (biopython)
    coverage_py = cov_dir / ".coverage"
    if coverage_py.exists():
        coverage_py.unlink()
        print(f"  Cleared: .coverage")
        cleared += 1

    # pysam Docker fragments
    pysam_dir = cov_dir / "pysam"
    if pysam_dir.exists():
        for frag in pysam_dir.glob(".coverage.*"):
            frag.unlink()
            cleared += 1
        for summary in pysam_dir.glob("summary.*.json"):
            summary.unlink()
            cleared += 1
        if cleared > 0:
            print(f"  Cleared: pysam/.coverage.* + summary.*.json fragments")

    # seqan3 gcovr output (if exists)
    gcovr_json = cov_dir / "gcovr.json"
    if gcovr_json.exists():
        gcovr_json.unlink()
        print(f"  Cleared: gcovr.json")
        cleared += 1

    return cleared


def clear_feedback_state() -> bool:
    state_file = ROOT / "data" / "feedback_state.json"
    if state_file.exists():
        state_file.unlink()
        print(f"  Cleared: data/feedback_state.json (fresh start, no resume)")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Clean Phase D artifacts")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")
    args = parser.parse_args()

    print("Workspace cleanup:\n")

    print("[1/3] Archiving bug reports...")
    archive_bug_reports(args.force)
    print()

    print("[2/3] Clearing coverage artifacts...")
    n_cov = clear_coverage_artifacts()
    if n_cov == 0:
        print("  Nothing to clear.")
    print()

    print("[3/3] Clearing feedback state...")
    if not clear_feedback_state():
        print("  No stale state file.")
    print()

    print("Cleanup complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
