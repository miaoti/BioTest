"""Remove the three CRAM-scoped bugs from dropped.json['verified'] and
re-freeze manifest.verified.json.

Our runners (htsjdk_runner, pysam_runner, biopython_runner,
seqan3_runner) all declare `supported_formats = {"VCF"} | {"SAM"}` or
narrower. None read CRAM. The htsjdk harness JAR (BioTestHarness.java)
has zero CRAM code. Including CRAM-specific bugs in the bench is a
scope violation: the harnesses can't feed CRAM bytes to the SUT
because the SUT entry point they use is SAM-only.

The three CRAM bugs move from verified → dropped with reason
"out_of_scope_cram".
"""

from __future__ import annotations

import json
import pathlib

BENCH = pathlib.Path(__file__).resolve().parent
DROPPED = BENCH / "dropped.json"

CRAM_BUGS = {
    "htsjdk-1708": "CRAM multi-container reference-region corruption "
                   "(format=CRAM; our harnesses read SAM only)",
    "htsjdk-1590": "CRAM 'BB' read features drop bases "
                   "(format=CRAM; out of scope)",
    "htsjdk-1592": "CRAM 'SC' scores misdecoded "
                   "(format=CRAM; out of scope)",
}


def main() -> int:
    data = json.loads(DROPPED.read_text(encoding="utf-8"))

    new_verified = [v for v in data["verified"] if v not in CRAM_BUGS]
    removed = [v for v in data["verified"] if v in CRAM_BUGS]

    for bug_id in removed:
        data["dropped"].append({
            "id": bug_id,
            "reason": f"out_of_scope_cram: {CRAM_BUGS[bug_id]}",
        })

    data["verified"] = new_verified
    DROPPED.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[cram-drop] moved {len(removed)} bugs out of verified:")
    for bug_id in removed:
        print(f"  - {bug_id}")
    print(f"[cram-drop] new counts: "
          f"verified={len(new_verified)} dropped={len(data['dropped'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
