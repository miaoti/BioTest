"""Apply the 2026-04-21 SAM-bug replacement.

Drops 4 unreachable SAM bugs (not file-level detectable) and adds 3 new
file-level htsjdk parse-time bugs sourced from htsjdk releases 2.18-2.20.

Run: py -3.12 compares/bug_bench/apply_sam_replacement.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
VERIFIED = ROOT / "manifest.verified.json"
SAM_ONLY = ROOT / "manifest.sam_only.json"
DROPPED = ROOT / "dropped.json"

DROP_IDS = {
    "biopython-4825": "not_file_level: pure copy.deepcopy() perf regression; correctness side-effect speculative. Cannot be triggered by feeding a SAM file.",
    "htsjdk-1538": "not_file_level: cached mAlignmentBlocks bug only fires after API mutation (setCigar). Differential cannot reach via parse(file).",
    "htsjdk-1561": "wrong_anchor: empirically pre-fix 2.24.1 and post-fix 3.0.0 both accept the same trigger; validation only adds to getValidationErrors() and is never thrown. See research log 2026-04-21.",
    "htsjdk-1489": "not_file_level: locus accumulator under-counts only when downstream code calls SamLocusIterator/AbstractLocusIterator after parse. Parse path is unaffected.",
}

NEW_BUGS = [
    {
        "id": "htsjdk-1238",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1238",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.18.1",
            "post_fix": "2.18.2",
            "verification_rule": "htsjdk PR #1238 added validateSequenceName regex check in SAMSequenceRecord; pre-2.18.2 only checked whitespace.",
            "confidence": "high",
        },
        "trigger": {
            "category": "parse_error_missed",
            "logic_bug": True,
            "description": "Pre-fix SAM header parser accepts @SQ SN: values containing characters disallowed by SAM 1.6 RNAME regex (e.g. comma). Post-fix rejects via SAMSequenceRecord.validateSequenceName. Spec mandates rejection.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1238/",
            "notes": "Reverse §5.3.1 detection: pre accepts (matches htslib's lenient stance), post rejects.",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": [
                "htslib"
            ],
        },
    },
    {
        "id": "htsjdk-1360",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1360",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.19.0",
            "post_fix": "2.20.0",
            "verification_rule": "htsjdk PR #1360 (closes issue #1174) removed EMPTY_READ validation block from SAMRecord.isValid(). Pre-fix throws SAMFormatException under default STRICT stringency.",
            "confidence": "high",
        },
        "trigger": {
            "category": "parse_error_missed",
            "logic_bug": True,
            "description": "Pre-fix htsjdk rejects zero-length reads (SEQ=*/QUAL=*) without FZ/CS/CQ tag with SAMFormatException; post-fix accepts. htslib/pysam accept silently. Spec does not require rejection.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1360/",
            "notes": "Forward §5.3.1 detection: pre rejects (outlier), post accepts (matches htslib).",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": [
                "htslib"
            ],
        },
    },
    {
        "id": "htsjdk-1410",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1410",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.20.2",
            "post_fix": "2.20.3",
            "verification_rule": "htsjdk PR #1410 raised SAMRecord.MAX_INSERT_SIZE from 1<<29 to Integer.MAX_VALUE. Pre-fix throws INVALID_INSERT_SIZE under STRICT.",
            "confidence": "high",
        },
        "trigger": {
            "category": "parse_error_missed",
            "logic_bug": True,
            "description": "Pre-fix htsjdk rejects records with |TLEN| > 2^29 even though SAM spec allows up to int32-max. Post-fix accepts. htslib/pysam accept any int32 TLEN.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1410/",
            "notes": "Forward §5.3.1 detection: pre rejects valid spec-compliant input; post accepts.",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": [
                "htslib"
            ],
        },
    },
]


def apply():
    # 1. Update verified manifest.
    verified = json.loads(VERIFIED.read_text(encoding="utf-8"))
    bugs = verified["bugs"]
    kept = [b for b in bugs if b["id"] not in DROP_IDS]
    dropped_entries = [b for b in bugs if b["id"] in DROP_IDS]
    if len(dropped_entries) != len(DROP_IDS):
        missing = set(DROP_IDS) - {b["id"] for b in dropped_entries}
        raise SystemExit(f"verified manifest missing bugs to drop: {missing}")
    new_bugs = list(kept) + NEW_BUGS

    # Recompute counts.
    counts = {}
    for b in new_bugs:
        counts[b["sut"]] = counts.get(b["sut"], 0) + 1

    verified["bugs"] = new_bugs
    verified["bench_counts_by_sut"] = counts
    verified["frozen_on"] = "2026-04-21"
    verified["description"] = (
        "Verified subset of manifest.json (revised 2026-04-21: dropped 4 unreachable "
        "SAM bugs, added 3 new file-level htsjdk SAM bugs from releases 2.18-2.20). "
        "See dropped.json for per-bug reasons."
    )
    VERIFIED.write_text(json.dumps(verified, indent=2) + "\n", encoding="utf-8")
    print(f"verified: {len(bugs)} -> {len(new_bugs)} bugs (dropped {len(dropped_entries)}, added {len(NEW_BUGS)})")
    print(f"  new counts_by_sut: {counts}")

    # 2. Update SAM-only manifest.
    sam_only = json.loads(SAM_ONLY.read_text(encoding="utf-8"))
    sam_bugs = sam_only["bugs"]
    sam_kept = [b for b in sam_bugs if b["id"] not in DROP_IDS]
    sam_new = list(sam_kept) + NEW_BUGS
    sam_counts = {}
    for b in sam_new:
        sam_counts[b["sut"]] = sam_counts.get(b["sut"], 0) + 1
    sam_only["bugs"] = sam_new
    sam_only["bench_counts_by_sut"] = sam_counts
    sam_only["frozen_on"] = "2026-04-21"
    sam_only["description"] = (
        "SAM-only subset of manifest.verified.json. Revised 2026-04-21: dropped "
        "biopython-4825 (perf), htsjdk-1538 (API), htsjdk-1561 (wrong anchor), "
        "htsjdk-1489 (API); added htsjdk-1238/1360/1410 (parse-time)."
    )
    SAM_ONLY.write_text(json.dumps(sam_only, indent=2) + "\n", encoding="utf-8")
    print(f"sam_only: {len(sam_bugs)} -> {len(sam_new)} bugs")

    # 3. Update dropped.json.
    dropped = json.loads(DROPPED.read_text(encoding="utf-8"))
    verified_ids = dropped["verified"]
    new_verified = [bid for bid in verified_ids if bid not in DROP_IDS]
    new_verified.extend(b["id"] for b in NEW_BUGS)
    dropped["verified"] = new_verified
    existing_dropped = {entry["id"] for entry in dropped["dropped"] if isinstance(entry, dict)}
    for bid, reason in DROP_IDS.items():
        if bid in existing_dropped:
            continue
        dropped["dropped"].append({"id": bid, "reason": reason, "dropped_on": "2026-04-21"})
    DROPPED.write_text(json.dumps(dropped, indent=2) + "\n", encoding="utf-8")
    print(f"dropped.json: verified={len(new_verified)} dropped={len(dropped['dropped'])}")


if __name__ == "__main__":
    apply()
