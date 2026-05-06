"""Unified per-cell biotest launcher for the 4-rep E0/E1 study.

Replaces the cascade script's `python biotest.py --config X --phase D`
invocation. Both E0 and E1 need the Phase E isolation patch (so Rank
12 + 13 augmentation lands in the per-cell working dir, not global
seeds/_struct paths). E1 additionally applies the three spec-blind
patches (no RAG retrieval, naive prompt-stuffing, no chunk_id check).

Usage:
    py -3.12 compares/ApplicationStudy/harness_run.py
        --mode E0|E1
        --config <cfg.yaml>
        [--phase B,C,D,E]
        [--verbose]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

HARNESS_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = HARNESS_ROOT.parents[1]
E1_DIR = HARNESS_ROOT / "E1_no_phase_a"
SHARED_DIR = HARNESS_ROOT / "shared"
SPEC_DUMP_PATH = SHARED_DIR / "raw_spec_dump.txt"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(E1_DIR))


def main() -> int:
    p = argparse.ArgumentParser(description="E0/E1/E1S/E2/E3 thin runner — patches + biotest.run_pipeline")
    p.add_argument(
        "--mode", required=True, choices=("E0", "E1", "E1S", "E2", "E3"),
        help=(
            "E0: full BioTest with RAG (Phase E patch only); "
            "E1: spec in prompt via naive stuffing (E1's 4 patches); "
            "E1S: STRICT — no spec text, bare transform names, no spec rules in blindspot; "
            "E2: full RAG + Phase D loop disabled (single-shot B+C+E); "
            "E3: NO Phase A (E1S patches) + NO Phase D (E2 Phase C bound) — fully ablated"
        ),
    )
    p.add_argument("--config", required=True)
    p.add_argument("--phase", default="B,C,D,E")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("chromadb").setLevel(logging.WARNING)

    print(f"[harness_run/{args.mode}] mode = {args.mode}", flush=True)

    # Pre-import patches differ per mode.
    if args.mode == "E1":
        if not SPEC_DUMP_PATH.exists():
            print(f"ERROR: missing {SPEC_DUMP_PATH}", file=sys.stderr)
            return 1
        spec_text = SPEC_DUMP_PATH.read_text(encoding="utf-8")
        print(f"[harness_run/E1] spec dump: {len(spec_text):,} chars", flush=True)
        from run_e1 import apply_e1_patches
        for k, v in apply_e1_patches(spec_text).items():
            print(f"[harness_run/E1] pre-import patch: {k}: {v}", flush=True)
    elif args.mode == "E1S":
        # E1-strict: no naive spec stuffing + bare transform menu +
        # bare behavior fragment + stripped blindspot rules.
        from run_e1 import apply_e1_strict_patches
        for k, v in apply_e1_strict_patches().items():
            print(f"[harness_run/E1S] pre-import patch: {k}: {v}", flush=True)
    elif args.mode == "E3":
        # E3 = E1S patches (no Phase A, strict spec-blind) + E2 Phase C
        # bound (applied post-import below).
        from run_e1 import apply_e1_strict_patches
        for k, v in apply_e1_strict_patches().items():
            print(f"[harness_run/E3] pre-import patch: {k}: {v}", flush=True)

    # Import biotest and apply post-import Phase E patch (BOTH modes —
    # Phase E in upstream biotest.py:1552 hardcodes seeds_root, so even
    # E0 needs cfg-driven redirect to keep per-cell isolation).
    import biotest
    from run_e1 import apply_phase_e_patch
    pe = apply_phase_e_patch(biotest)
    print(f"[harness_run/{args.mode}] post-import patch: {pe}", flush=True)

    # E2/E3 (no Phase D): bound Phase C runtime so coverage collection runs.
    # Without Phase D's natural timeout, Hypothesis shrink storms can
    # consume the whole wall budget and the post-Phase-C measurement
    # never executes — host cells (biopython, vcfpy) end with
    # status="missing".
    if args.mode in ("E2", "E3"):
        from run_e1 import apply_e2_phase_c_patch
        for k, v in apply_e2_phase_c_patch(per_test_deadline_ms=5000).items():
            print(f"[harness_run/{args.mode}] phase_c patch: {k}: {v}", flush=True)

    cfg_path = Path(args.config)
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    print(f"[harness_run/{args.mode}] config: {cfg_path}", flush=True)
    print(f"[harness_run/{args.mode}] phase_filter: {args.phase}", flush=True)

    return biotest.run_pipeline(cfg, phase_filter=args.phase)


if __name__ == "__main__":
    sys.exit(main())
