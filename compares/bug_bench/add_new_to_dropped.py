"""Mark the 2026-04-20 vcfpy + noodles bugs as verified in dropped.json,
and push the pysam primary-dropped bugs out of `verified` (DESIGN §A.6).

The optimistic-verified status is consistent with DESIGN.md §A.2/§A.3:
every vcfpy / noodles candidate carries a concrete version pin from the
upstream CHANGELOG, so install-verification is expected to pass. If a
version does fail at run time, the driver records the error and moves
on — the pipeline is still safe.

Idempotent: re-running won't create duplicates.
"""

from __future__ import annotations

import json
import pathlib

BENCH = pathlib.Path(__file__).resolve().parent
DROPPED = BENCH / "dropped.json"

NEW_VERIFIED_IDS = [
    # vcfpy (7)
    "vcfpy-176", "vcfpy-171", "vcfpy-146", "vcfpy-145",
    "vcfpy-gtone-0.13", "vcfpy-127", "vcfpy-nocall-0.8",
    # noodles-vcf (9)
    "noodles-300", "noodles-339", "noodles-268", "noodles-223",
    "noodles-224", "noodles-259", "noodles-241",
    "noodles-inforay-0.64", "noodles-ob1-0.23",
]

# pysam was demoted to voter (DESIGN §2.6 / §9 Risk 4). The 4 bugs that
# used to be in `verified` move to `dropped` with a `primary_drop` reason.
PYSAM_PRIMARY_DROP = [
    "pysam-1314", "pysam-1308", "pysam-1214", "pysam-939",
]


def main() -> int:
    data = json.loads(DROPPED.read_text(encoding="utf-8"))
    verified: list[str] = list(data.get("verified", []))
    dropped = list(data.get("dropped", []))

    # Remove pysam primary-dropped IDs from verified; record them under
    # dropped with a clear reason so §A.6 is auditable from the file.
    dropped_ids = {d["id"] for d in dropped if isinstance(d, dict) and "id" in d}
    for pid in PYSAM_PRIMARY_DROP:
        if pid in verified:
            verified.remove(pid)
        if pid not in dropped_ids:
            dropped.append({
                "id": pid,
                "reason": "primary_drop_2026-04-20",
                "note": (
                    "pysam removed from primary SUT set; retained as "
                    "voter in the differential oracle (DESIGN §2.6, "
                    "§9 Risk 4). Trigger folder kept on disk for "
                    "historical reference."
                ),
            })

    # Append the new vcfpy + noodles IDs to verified (optimistic; real
    # install-verify happens at Phase-0 run time).
    for vid in NEW_VERIFIED_IDS:
        if vid not in verified:
            verified.append(vid)

    data["verified"] = verified
    data["dropped"] = dropped
    DROPPED.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[dropped.json] verified={len(verified)} dropped={len(dropped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
