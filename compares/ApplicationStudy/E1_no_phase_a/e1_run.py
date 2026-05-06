"""Thin entry-point: apply E1 patches, then biotest.run_pipeline(cfg).

Used by the 4-rep harness to launch each cell in its own subprocess
with the E1 (no-Phase-A) patches in effect. Replaces the direct
`python biotest.py --config X --phase D` invocation that the cascade
script does for E0.

Usage (matches the surface biotest.py exposes — required to swap into
the existing cascade subprocess command):

    py -3.12 compares/ApplicationStudy/E1_no_phase_a/e1_run.py
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

E1_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = E1_ROOT.parents[2]
SHARED_DIR = E1_ROOT.parent / "shared"
SPEC_DUMP_PATH = SHARED_DIR / "raw_spec_dump.txt"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(E1_ROOT))


def main() -> int:
    p = argparse.ArgumentParser(description="E1 thin runner — applies patches, runs biotest")
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

    if not SPEC_DUMP_PATH.exists():
        print(f"ERROR: missing {SPEC_DUMP_PATH}", file=sys.stderr)
        return 1

    spec_text = SPEC_DUMP_PATH.read_text(encoding="utf-8")
    print(f"[e1_run] spec dump: {len(spec_text):,} chars", flush=True)

    # Pre-import patches (tools / engine / compiler).
    from run_e1 import apply_e1_patches, apply_phase_e_patch
    patches = apply_e1_patches(spec_text)
    for k, v in patches.items():
        print(f"[e1_run] pre-import patch: {k}: {v}", flush=True)

    # Now import biotest and apply the post-import Phase E patch.
    import biotest
    pe = apply_phase_e_patch(biotest)
    print(f"[e1_run] post-import patch: {pe}", flush=True)

    cfg_path = Path(args.config)
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    print(f"[e1_run] config: {cfg_path}", flush=True)
    print(f"[e1_run] phase_filter: {args.phase}", flush=True)

    return biotest.run_pipeline(cfg, phase_filter=args.phase)


if __name__ == "__main__":
    sys.exit(main())
