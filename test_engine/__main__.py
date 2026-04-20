"""
Phase C CLI: python -m test_engine

Usage:
    python -m test_engine run --format VCF
    python -m test_engine run --format SAM --seeds seeds/
    python -m test_engine list-parsers
    python -m test_engine report --output data/det_report.json
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import MR_REGISTRY_PATH, BUG_REPORTS_DIR, SEEDS_DIR, DET_REPORT_PATH
from .runners.base import ParserRunner
from .runners.htsjdk_runner import HTSJDKRunner
from .runners.pysam_runner import PysamRunner
from .runners.biopython_runner import BiopythonRunner
from .runners.seqan3_runner import SeqAn3Runner
from .runners.vcfpy_runner import VcfpyRunner
from .runners.noodles_runner import NoodlesRunner
from .runners.reference_runner import ReferenceRunner


def get_all_runners() -> list[ParserRunner]:
    """Instantiate all known parser runners (reference always last)."""
    return [
        HTSJDKRunner(),
        PysamRunner(),
        BiopythonRunner(),
        SeqAn3Runner(),
        VcfpyRunner(),
        NoodlesRunner(),
        ReferenceRunner(),
    ]


def cmd_run(args: argparse.Namespace) -> None:
    """Run the full test suite."""
    from .orchestrator import run_test_suite

    runners = get_all_runners()
    available = [r for r in runners if r.is_available()]

    if not available:
        print("ERROR: No parser runners available. Install pysam, build HTSJDK harness, etc.")
        sys.exit(1)

    print(f"Available runners: {[r.name for r in available]}")
    print(f"Format filter: {args.format or 'all'}")
    print(f"Registry: {Path(args.registry).name}")
    print(f"Seeds: {Path(args.seeds).name}")
    print()

    result = run_test_suite(
        runners=available,
        registry_path=Path(args.registry),
        seeds_dir=Path(args.seeds) if args.seeds else None,
        output_dir=Path(args.output),
        format_filter=args.format,
    )

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUITE RESULTS")
    print("=" * 60)
    print(f"  Total tests:            {result.total_tests}")
    print(f"  Metamorphic failures:   {result.metamorphic_failures}")
    print(f"  Differential failures:  {result.differential_failures}")
    print(f"  Crashes:                {result.crashes}")
    print(f"  DET rate:               {result.det_tracker.det_rate:.4f}")
    print(f"  Bug reports generated:  {len(result.bug_reports)}")

    if result.bug_reports:
        print("\nBug reports:")
        for bp in result.bug_reports:
            print(f"  {bp.name}")

    # Export DET report
    det_path = Path(args.det_report) if args.det_report else DET_REPORT_PATH
    det_path.parent.mkdir(parents=True, exist_ok=True)
    result.det_tracker.export(str(det_path))
    print(f"\nDET report exported to: {det_path.name}")

    # Exit code: non-zero if any failures
    if result.metamorphic_failures or result.differential_failures:
        sys.exit(1)


def cmd_list_parsers(args: argparse.Namespace) -> None:
    """List available parser runners."""
    runners = get_all_runners()
    print("Parser Runners:")
    print("-" * 50)
    for runner in runners:
        status = "AVAILABLE" if runner.is_available() else "NOT AVAILABLE"
        fmts = ", ".join(sorted(runner.supported_formats))
        print(f"  {runner.name:12s}  [{fmts:10s}]  {status}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="test_engine",
        description="BioTest Phase C: Cross-Execution & Differential Testing",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="command")

    # run
    run_parser = subparsers.add_parser("run", help="Run metamorphic + differential test suite")
    run_parser.add_argument("--registry", default=str(MR_REGISTRY_PATH))
    run_parser.add_argument("--seeds", default=str(SEEDS_DIR))
    run_parser.add_argument("--format", choices=["VCF", "SAM"], default=None)
    run_parser.add_argument("--output", default=str(BUG_REPORTS_DIR))
    run_parser.add_argument("--det-report", default=None)

    # list-parsers
    subparsers.add_parser("list-parsers", help="List available parser runners")

    args = parser.parse_args()

    # Logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.command == "run":
        cmd_run(args)
    elif args.command == "list-parsers":
        cmd_list_parsers(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
