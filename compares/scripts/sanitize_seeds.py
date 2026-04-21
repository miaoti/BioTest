"""Drop poison seeds — inputs that every in-scope SUT rejects as
validation-errors on both pre-fix and post-fix versions.

Motivation: libFuzzer/jazzer/atheris/cargo_fuzz all HALT on the first
crash. If a seed already crashes the SUT (e.g. seqan3/sam's
`real_world_htslib_colons.bam` with `@SQ chr1,chr3`), the fuzzer's
entire time budget is burned on that single seed without ever
performing a mutation. See `compares/PHASE4_DIAGNOSIS.md §2.6` and
`compares/PHASE4_BASELINE_FIXES.md §0.1`.

Sanitization rule (per §0.1):
    DROP iff ALL in-scope SUTs for the seed's format reject it
    (error_type ∈ {"crash", "parse_error"}).
    KEEP if any SUT returns success=True OR error_type == "ineligible"
    (ineligible means the SUT doesn't declare support for this format;
    not evidence the seed is bad).

Dropped seeds are MOVED (not deleted) to seeds/dropped_during_sanitization/
so the operator has an audit trail. A JSON manifest is written at
seeds/dropped_during_sanitization.json with the drop reason per seed.

Usage (host or inside biotest-bench-setup container):
    python3 compares/scripts/sanitize_seeds.py
    python3 compares/scripts/sanitize_seeds.py --dry-run
    python3 compares/scripts/sanitize_seeds.py --format VCF

The script uses the repo's ParserRunner implementations; it needs
JDK (for htsjdk), the atheris-venv (for vcfpy/biopython), and the
built noodles / seqan3 harnesses. Inside the bench image all of those
are available; on the host, expect some runners to report
`is_available() == False` — those are excluded from the "ALL SUTs
rejected" check so the sanitization is still safe to run (a seed only
drops if every *available* SUT rejects it).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

# Scope: which SUTs we feed each format through. Matches DESIGN §4.1.
# pysam retained as a voter here (not a primary SUT) because its
# htslib-bound acceptance is a useful tie-breaker when the pure
# implementations disagree.
SCOPE: dict[str, list[str]] = {
    "VCF": ["htsjdk", "vcfpy", "noodles", "pysam"],
    "SAM": ["htsjdk", "biopython", "seqan3", "pysam"],
}


def _load_runner(name: str):
    """Instantiate a ParserRunner by short name, or return None on failure."""
    try:
        if name == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner
            return HTSJDKRunner()
        if name == "vcfpy":
            from test_engine.runners.vcfpy_runner import VcfpyRunner
            return VcfpyRunner()
        if name == "noodles":
            from test_engine.runners.noodles_runner import NoodlesRunner
            return NoodlesRunner()
        if name == "pysam":
            from test_engine.runners.pysam_runner import PysamRunner
            return PysamRunner()
        if name == "biopython":
            from test_engine.runners.biopython_runner import BiopythonRunner
            return BiopythonRunner()
        if name == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner
            return SeqAn3Runner()
    except Exception as e:
        print(f"[sanitize] runner load failed for {name}: {e}", file=sys.stderr)
    return None


def _probe(runner, seed: Path, fmt: str, timeout_s: float) -> tuple[bool, str]:
    """Return (rejected, reason) where rejected=True means the SUT
    treats this seed as an error (crash/parse_error) — it's a candidate
    for dropping. rejected=False means success OR ineligible (not
    evidence the seed is bad).
    """
    try:
        r = runner.run(seed, fmt, timeout_s=timeout_s)
    except Exception as e:
        return True, f"runner_raise:{type(e).__name__}"
    if r.success:
        return False, "success"
    err = r.error_type or "unknown"
    if err == "ineligible":
        return False, "ineligible"
    return True, err


def sanitize(
    format_type: str, seeds_dir: Path, dropped_dir: Path,
    timeout_s: float, dry_run: bool,
) -> list[dict[str, Any]]:
    suts = SCOPE[format_type]
    runners = {}
    for s in suts:
        r = _load_runner(s)
        if r is not None and r.is_available():
            runners[s] = r
        else:
            print(f"[sanitize] {format_type}: skipping {s} (unavailable)")

    if not runners:
        print(f"[sanitize] {format_type}: NO runners available — skipping "
              f"(every seed would survive by vacuous truth)")
        return []

    drops: list[dict[str, Any]] = []
    for seed in sorted(seeds_dir.iterdir()):
        if not seed.is_file():
            continue
        verdicts: dict[str, str] = {}
        for name, runner in runners.items():
            _, reason = _probe(runner, seed, format_type, timeout_s)
            verdicts[name] = reason

        # DROP iff every available, non-ineligible SUT rejected.
        considered = {n: v for n, v in verdicts.items() if v != "ineligible"}
        if considered and all(v != "success" for v in considered.values()):
            drops.append({
                "seed": str(seed.relative_to(REPO)),
                "format": format_type,
                "verdicts": verdicts,
            })
            print(f"[drop] {seed.name:40s}  " + "  ".join(
                f"{n}={v}" for n, v in verdicts.items()))
            if not dry_run:
                dest = dropped_dir / seed.name
                dropped_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(seed), str(dest))
        else:
            kept = [n for n, v in verdicts.items() if v == "success"]
            print(f"[keep] {seed.name:40s}  accepted_by={kept or '[ineligible-only]'}")
    return drops


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--format", choices=["VCF", "SAM", "ALL"], default="ALL")
    p.add_argument("--timeout-s", type=float, default=10.0,
                   help="Per-seed, per-runner probe timeout.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print drop decisions without moving files.")
    args = p.parse_args()

    seeds_root = REPO / "seeds"
    dropped_root = seeds_root / "dropped_during_sanitization"
    manifest_path = seeds_root / "dropped_during_sanitization.json"

    fmts = ["VCF", "SAM"] if args.format == "ALL" else [args.format]
    all_drops: list[dict[str, Any]] = []
    started_at = time.strftime("%FT%TZ", time.gmtime())
    for fmt in fmts:
        seeds_dir = seeds_root / fmt.lower()
        if not seeds_dir.exists():
            print(f"[sanitize] {fmt}: {seeds_dir} missing; skipping")
            continue
        all_drops.extend(
            sanitize(fmt, seeds_dir, dropped_root / fmt.lower(),
                     args.timeout_s, args.dry_run))

    ended_at = time.strftime("%FT%TZ", time.gmtime())
    summary = {
        "started_at": started_at,
        "ended_at": ended_at,
        "timeout_s": args.timeout_s,
        "dry_run": args.dry_run,
        "dropped": all_drops,
    }
    if not args.dry_run:
        manifest_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n[sanitize] dropped {len(all_drops)} seeds"
          f"{' (dry-run)' if args.dry_run else ''}; "
          f"manifest -> {manifest_path}")


if __name__ == "__main__":
    main()
