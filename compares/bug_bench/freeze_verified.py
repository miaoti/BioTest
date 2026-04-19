"""Freeze the verified subset of manifest.json into manifest.verified.json.

Reads `dropped.json` (produced by `bug_bench_driver.py --verify-only`),
picks the `verified` ids out of `manifest.json`, and writes them to
`manifest.verified.json`. The Phase-4 bench driver should run against
the verified file, not the candidate manifest.

The verified file is committed to the repo alongside `manifest.json` so
the exact bench set is reproducible.
"""

from __future__ import annotations

import json
import pathlib

BENCH = pathlib.Path(__file__).resolve().parent
MANIFEST = BENCH / "manifest.json"
DROPPED = BENCH / "dropped.json"
VERIFIED = BENCH / "manifest.verified.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    dropped = json.loads(DROPPED.read_text(encoding="utf-8"))

    verified_ids = set(dropped["verified"])
    verified_bugs = [b for b in manifest["bugs"] if b["id"] in verified_ids]

    assert len(verified_bugs) == len(verified_ids), (
        f"mismatch: {len(verified_bugs)} verified bugs, "
        f"{len(verified_ids)} verified ids — some ids not in manifest?")

    out = {
        "$schema": manifest.get("$schema", "./schema.json"),
        "benchmark_version": "1.0.0-verified",
        "status": "frozen_for_phase_4",
        "frozen_on": "2026-04-19",
        "description": (
            f"Verified subset of manifest.json. "
            f"{len(verified_bugs)} bugs of {len(manifest['bugs'])} candidates "
            f"({len(verified_bugs)/len(manifest['bugs']):.0%}) survived "
            f"Phase-0 install-verification per DESIGN.md §13.4. Drops follow "
            f"Bohme et al. ICSE'22 discipline — see dropped.json for per-bug "
            f"reasons."
        ),
        "bench_counts_by_sut": _bucket_by_sut(verified_bugs),
        "bugs": verified_bugs,
    }
    VERIFIED.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[freeze] wrote {len(verified_bugs)} bugs to {VERIFIED.name}")
    for sut, n in out["bench_counts_by_sut"].items():
        print(f"  {sut:10} {n}")
    return 0


def _bucket_by_sut(bugs: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for b in bugs:
        out[b["sut"]] = out.get(b["sut"], 0) + 1
    return dict(sorted(out.items()))


if __name__ == "__main__":
    raise SystemExit(main())
