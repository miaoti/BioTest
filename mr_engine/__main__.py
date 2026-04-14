"""
CLI entry point: python -m mr_engine

Usage:
    python -m mr_engine --format VCF
    python -m mr_engine --format VCF --target ordering_invariance
    python -m mr_engine --format SAM --export data/mr_registry.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from mr_engine.behavior import BehaviorTarget, get_all_targets
from mr_engine.agent.engine import mine_mrs
from mr_engine.registry import triage, export_registry


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="mr_engine",
        description="Agentic RAG-driven Metamorphic Relation mining & compilation",
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=["VCF", "SAM"],
        help="Spec format to mine MRs for",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Specific behavior target (e.g. ordering_invariance). "
             "If omitted, mines all targets.",
    )
    parser.add_argument(
        "--export",
        type=str,
        default=None,
        help="Export triaged registry to JSON file path",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Determine targets to mine
    if args.target:
        try:
            targets = [BehaviorTarget(args.target)]
        except ValueError:
            valid = [t.value for t in BehaviorTarget]
            print(f"Error: unknown target '{args.target}'. Valid: {valid}")
            return 1
    else:
        targets = get_all_targets()

    # Mine MRs
    all_relations = []
    for target in targets:
        print(f"\n{'='*60}")
        print(f"Mining: {args.format} / {target.value}")
        print(f"{'='*60}")

        result = mine_mrs(target, args.format)

        if result.success:
            print(f"  Compiled {len(result.relations)} MR(s)")
            for mr in result.relations:
                print(f"    - [{mr.mr_id}] {mr.mr_name}")
            all_relations.extend(result.relations)
        else:
            print(f"  FAILED: {result.error_detail}")

    # Triage
    if all_relations:
        registry = triage(all_relations)
        print(f"\n{'='*60}")
        print(f"TRIAGE RESULTS")
        print(f"{'='*60}")
        print(f"  Enforced:   {len(registry.enforced)}")
        print(f"  Quarantine: {len(registry.quarantine)}")

        if args.export:
            export_registry(registry, args.export)
            print(f"  Exported to: {args.export}")
        else:
            # Print summary to stdout
            print("\nEnforced MRs:")
            for mr in registry.enforced.values():
                print(f"  [{mr.mr_id}] {mr.mr_name}")
            print("\nQuarantine MRs:")
            for mr in registry.quarantine.values():
                print(f"  [{mr.mr_id}] {mr.mr_name}")
    else:
        print("\nNo MRs were mined.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
