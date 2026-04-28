"""Manifest-anchor sweep — Lever 1 of the 2026-04-21 detection lift.

For a target bug, walks a list of candidate SUT versions, installs each
in turn, and runs `_replay_trigger_silenced` on the canonical PoV. Emits
the empirical pre/post pair (last version where pre-fix-style failure
fires, first version where it silences) plus a per-version log.

Usage:
    py -3.12 compares/bug_bench/sweep_anchors.py \\
        --bug-id htsjdk-1418 \\
        --versions 2.19.0,2.19.1,2.20.0,2.20.1,2.21.0,2.22.0,2.23.0 \\
        [--apply]   # update manifest.verified.json with the new anchor

Output:
  compares/bug_bench/sweep_logs/<bug-id>.json — per-version verdicts
  manifest.verified.json updated in place when --apply is set
  stdout — human-readable summary

The script is pure manifest/install plumbing — it imports `install_sut`
and `_replay_trigger_silenced` from `bug_bench_driver` and reuses them.
No new SUT-specific code introduced; SUT dispatch goes through the
existing `install_sut` table, so adding a new SUT to the bench
automatically extends the sweep.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "compares" / "scripts"))

import bug_bench_driver as bbd  # noqa: E402


def _resolve_pov(bug: dict) -> Path | None:
    """Return the canonical PoV file for a bug, or None if absent."""
    fmt = bug.get("format", "VCF").lower()
    triggers = ROOT / "compares" / "bug_bench" / "triggers" / bug["id"]
    for name in (f"original.{fmt}", "original.vcf", "original.sam"):
        p = triggers / name
        if p.is_file():
            return p
    return None


def sweep(bug_id: str, versions: list[str]) -> dict:
    manifest = json.loads(
        (ROOT / "compares" / "bug_bench" / "manifest.verified.json").read_text(
            encoding="utf-8"
        )
    )
    bug = next((b for b in manifest["bugs"] if b["id"] == bug_id), None)
    if bug is None:
        raise SystemExit(f"bug {bug_id!r} not in manifest.verified.json")
    sut = bug["sut"]
    fmt = bug.get("format", "VCF")
    pov = _resolve_pov(bug)
    if pov is None:
        raise SystemExit(
            f"no canonical PoV for {bug_id} — author triggers/{bug_id}/original.{fmt.lower()}"
        )
    old = bug["anchor"]
    print(
        f"[sweep] bug={bug_id} sut={sut} fmt={fmt} pov={pov}\n"
        f"        current anchor: pre={old.get('pre_fix')!r} post={old.get('post_fix')!r}"
    )

    tried: list[dict] = []
    for v in versions:
        anchor = {**old, "pre_fix": v, "post_fix": v}
        verdict: bool | None = None
        err: str | None = None
        t0 = time.monotonic()
        try:
            bbd.install_sut(sut, anchor, "post_fix")
        except Exception as e:
            err = f"install: {type(e).__name__}: {str(e)[:160]}"
        else:
            try:
                verdict = bbd._replay_trigger_silenced(sut, pov, fmt)
            except Exception:
                err = "replay: " + traceback.format_exc(limit=1)
        dt = time.monotonic() - t0
        tried.append({
            "version": v,
            "silenced": verdict,
            "duration_s": round(dt, 2),
            "error": err,
        })
        sym = {True: "OK ", False: "FAIL", None: "?  "}[verdict]
        print(f"  {v:>10s}  silenced={sym}  ({dt:5.1f}s)"
              + (f"  err={err[:100]}" if err else ""))

    # Empirical anchor: last consecutive run where pre-fix-style failure
    # fires (silenced=False), first version after where it silences
    # (silenced=True). Walk the list in order — versions ARE in
    # ascending order by user contract.
    last_failing: str | None = None
    first_silencing: str | None = None
    for t in tried:
        if t["silenced"] is False:
            last_failing = t["version"]
        elif t["silenced"] is True and first_silencing is None and last_failing is not None:
            first_silencing = t["version"]
            break

    new_anchor: dict | None = None
    if last_failing is not None and first_silencing is not None:
        new_anchor = {
            **old,
            "pre_fix": last_failing,
            "post_fix": first_silencing,
            "verification_rule": (
                f"empirical sweep 2026-04-21 across {versions[0]}..{versions[-1]}: "
                f"pre={last_failing} fails, post={first_silencing} silences"
            ),
        }
        print(
            f"\n[sweep] empirical anchor: pre={last_failing} -> post={first_silencing}"
        )
    else:
        print("\n[sweep] no clean pre/post pair found in this version range")

    return {
        "bug_id": bug_id,
        "sut": sut,
        "fmt": fmt,
        "pov": str(pov),
        "tried": tried,
        "old_anchor": old,
        "new_anchor": new_anchor,
    }


def write_log(result: dict) -> Path:
    log_dir = ROOT / "compares" / "bug_bench" / "sweep_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    p = log_dir / f"{result['bug_id']}.json"
    p.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return p


def apply_anchor(result: dict) -> bool:
    """Mutate manifest.verified.json in place. Returns True if changed."""
    if result.get("new_anchor") is None:
        return False
    manifest_path = ROOT / "compares" / "bug_bench" / "manifest.verified.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    bug = next(b for b in manifest["bugs"] if b["id"] == result["bug_id"])
    bug["anchor"] = result["new_anchor"]
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    # Mirror to the per-format manifest if the bug lives there.
    fmt = result["fmt"].lower()
    sub_path = ROOT / "compares" / "bug_bench" / f"manifest.{fmt}_only.json"
    if sub_path.exists():
        sub = json.loads(sub_path.read_text(encoding="utf-8"))
        sb = next(
            (b for b in sub["bugs"] if b["id"] == result["bug_id"]), None
        )
        if sb is not None:
            sb["anchor"] = result["new_anchor"]
            sub_path.write_text(
                json.dumps(sub, indent=2) + "\n", encoding="utf-8"
            )
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bug-id", required=True)
    ap.add_argument(
        "--versions",
        required=True,
        help="comma-separated, ascending order",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="patch manifest.verified.json with the empirical anchor",
    )
    args = ap.parse_args()
    versions = [v.strip() for v in args.versions.split(",") if v.strip()]
    result = sweep(args.bug_id, versions)
    log_path = write_log(result)
    print(f"\n[sweep] log -> {log_path}")
    if args.apply:
        if apply_anchor(result):
            print(
                f"[sweep] manifest.verified.json updated for {args.bug_id}"
            )
        else:
            print("[sweep] no anchor change applied (no clean pre/post)")


if __name__ == "__main__":
    main()
