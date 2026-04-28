"""Apply the 2026-04-21 C2/C3/C4 audit findings.

Two drops + three seqan3 verification_rule corrections. Drops follow
the same precedent as the htsjdk-1561 drop (manifest revision
2026-04-21 SAM): when an anchor empirically fails C2 or C4, the entry
is removed rather than retained as a forever-zero.

Drops:
  - vcfpy-gtone-0.13 — C2 violation. Sweep log
    `compares/bug_bench/sweep_logs/vcfpy-gtone-0.13.json` proves all
    versions 0.11.0 → 0.13.5 silence the captured PoV; pre-fix and
    post-fix produce identical output.
  - vcfpy-nocall-0.8 — C4 violation. PyPI's simple index
    (`https://pypi.org/simple/vcfpy/`) shows the published versions
    jump 0.7.0 → 0.9.0. vcfpy 0.8.1 was never released; pre_fix
    anchor pins a non-existent version.

seqan3 verification_rule corrections (2026-04-21 audit found the
pre-fix SHAs cite merge commits of unrelated PRs):
  - seqan3-3098: pre `4961904fb` = merge of PR #3097 ([TEST] API),
    NOT PR #3098. Post-fix `4fe54891` references issue #3043.
  - seqan3-3269: pre `ca4d66839` = merge of PR #3263 (dependabot),
    NOT PR #3269. Post-fix `11564cb3` references issue #3266.
  - seqan3-3406: pre `745c645fe` = merge of PR #3404 (clang22),
    NOT PR #3406. Real PR #3406 merge is `d0f13f32`.

These are paradigm-out anyway (alignment-internal / concurrency) so
detection isn't affected, but the verification_rule strings must not
falsely cite the right PR.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
VERIFIED = ROOT / "manifest.verified.json"
VCF_ONLY = ROOT / "manifest.vcf_only.json"
SAM_ONLY = ROOT / "manifest.sam_only.json"
DROPPED = ROOT / "dropped.json"

DROP_IDS = {
    "vcfpy-gtone-0.13": (
        "C2_empirically_violated_2026-04-21: sweep_logs/vcfpy-gtone-0.13.json "
        "proves versions 0.11.0–0.13.5 ALL silence the captured PoV "
        "(silenced=true uniformly; new_anchor=null). Same failure mode as "
        "htsjdk-1561 — manifest's pre/post pair does not produce different "
        "observable output on the captured PoV. Either the haploid-GT bug "
        "doesn't manifest in vcfpy 0.12.x at all, or the PoV doesn't "
        "exercise the bug-specific code path."
    ),
    "vcfpy-nocall-0.8": (
        "C4_empirically_violated_2026-04-21: PyPI simple index "
        "(https://pypi.org/simple/vcfpy/) shows the released versions "
        "jump 0.7.0 → 0.9.0; vcfpy 0.8.1 was never published. The "
        "manifest's pre_fix anchor pins a non-existent version. "
        "Recovery would require a git-checkout fallback against a "
        "0.8.x source SHA, which we don't have."
    ),
}

SEQAN3_RULE_FIXES = {
    "seqan3-3098": {
        "verification_rule": (
            "ANCHOR DEFECT 2026-04-21: pre-fix SHA 4961904fb is the "
            "merge commit of PR #3097 ([TEST] API), NOT PR #3098. "
            "Post-fix commit 4fe54891 message says \"[FIX] Alignment "
            "Wrong alignment score #3043\" — i.e. the actual fix is "
            "for issue #3043, not PR #3098. Manifest entry retained "
            "since the bug is paradigm-out anyway (alignment-internal "
            "score field), but the SHA citation is misleading and "
            "should be repaired in a follow-up."
        ),
    },
    "seqan3-3269": {
        "verification_rule": (
            "ANCHOR DEFECT 2026-04-21: pre-fix SHA ca4d66839 is the "
            "merge commit of PR #3263 (dependabot bump), NOT PR "
            "#3269. Post-fix commit 11564cb3 message says \"Fixes "
            "#3266: Incorrect begin/end of alignment for banded "
            "alignment\" — i.e. the actual fix is for issue #3266, "
            "not PR #3269. Paradigm-out anyway (alignment-internal); "
            "SHA citation retained pending follow-up."
        ),
    },
    "seqan3-3406": {
        "verification_rule": (
            "ANCHOR DEFECT 2026-04-21: pre-fix SHA 745c645fe is the "
            "merge commit of PR #3404 (clang22 fix), NOT PR #3406. "
            "Real PR #3406 merge commit is d0f13f32 (BGZF data race "
            "port from seqan2). Paradigm-out anyway (concurrency, "
            "non-deterministic); SHA citation retained pending "
            "follow-up."
        ),
    },
}


def apply():
    # ---- 1. Update manifest.verified.json ----
    verified = json.loads(VERIFIED.read_text(encoding="utf-8"))
    bugs = verified["bugs"]

    # Apply seqan3 verification_rule fixes in place.
    for bug in bugs:
        if bug["id"] in SEQAN3_RULE_FIXES:
            bug["anchor"]["verification_rule"] = (
                SEQAN3_RULE_FIXES[bug["id"]]["verification_rule"]
            )

    kept = [b for b in bugs if b["id"] not in DROP_IDS]
    actually_dropped = [b for b in bugs if b["id"] in DROP_IDS]
    if len(actually_dropped) != len(DROP_IDS):
        missing = set(DROP_IDS) - {b["id"] for b in actually_dropped}
        raise SystemExit(f"verified manifest missing entries to drop: {missing}")

    counts: dict[str, int] = {}
    for b in kept:
        counts[b["sut"]] = counts.get(b["sut"], 0) + 1

    verified["bugs"] = kept
    verified["bench_counts_by_sut"] = counts
    verified["frozen_on"] = "2026-04-21"
    verified["description"] = (
        "Verified subset of manifest.json (2026-04-21 audit-finalized: "
        "dropped 4 unreachable SAM bugs + added 3 file-level htsjdk SAM "
        "regressions on the morning patch; the C2/C3/C4 audit later that "
        "day dropped 2 further entries that empirically failed criterion "
        "2 or 4 — vcfpy-gtone-0.13 and vcfpy-nocall-0.8). 32 bugs total; "
        "see dropped.json for per-bug rationale and "
        "compares/results/bug_bench/DETECTION_RATIONALE.md §\"2026-04-21 "
        "audit\" for the per-bug verdict table with citations."
    )
    VERIFIED.write_text(
        json.dumps(verified, indent=2) + "\n", encoding="utf-8"
    )
    print(f"verified: {len(bugs)} -> {len(kept)} (dropped {len(DROP_IDS)})")
    print(f"  new counts_by_sut: {counts}")

    # ---- 2. Mirror to manifest.vcf_only.json ----
    vcf = json.loads(VCF_ONLY.read_text(encoding="utf-8"))
    vcf_bugs = vcf["bugs"]
    vcf_kept = [b for b in vcf_bugs if b["id"] not in DROP_IDS]
    vcf_counts: dict[str, int] = {}
    for b in vcf_kept:
        vcf_counts[b["sut"]] = vcf_counts.get(b["sut"], 0) + 1
    vcf["bugs"] = vcf_kept
    vcf["bench_counts_by_sut"] = vcf_counts
    vcf["frozen_on"] = "2026-04-21"
    vcf["description"] = (
        "VCF-only subset of manifest.verified.json. 2026-04-21 audit "
        "drops vcfpy-gtone-0.13 (C2 ✗) and vcfpy-nocall-0.8 (C4 ✗)."
    )
    VCF_ONLY.write_text(
        json.dumps(vcf, indent=2) + "\n", encoding="utf-8"
    )
    print(f"vcf_only: {len(vcf_bugs)} -> {len(vcf_kept)}")

    # ---- 3. Mirror seqan3 verification_rule fixes to sam_only ----
    sam = json.loads(SAM_ONLY.read_text(encoding="utf-8"))
    for bug in sam["bugs"]:
        if bug["id"] in SEQAN3_RULE_FIXES:
            bug["anchor"]["verification_rule"] = (
                SEQAN3_RULE_FIXES[bug["id"]]["verification_rule"]
            )
    SAM_ONLY.write_text(
        json.dumps(sam, indent=2) + "\n", encoding="utf-8"
    )
    print("sam_only: seqan3 verification_rule strings updated")

    # ---- 4. Update dropped.json ----
    dropped = json.loads(DROPPED.read_text(encoding="utf-8"))
    verified_ids = dropped["verified"]
    dropped["verified"] = [bid for bid in verified_ids if bid not in DROP_IDS]
    existing_dropped = {
        entry["id"] for entry in dropped["dropped"] if isinstance(entry, dict)
    }
    for bid, reason in DROP_IDS.items():
        if bid in existing_dropped:
            continue
        dropped["dropped"].append(
            {"id": bid, "reason": reason, "dropped_on": "2026-04-21"}
        )
    DROPPED.write_text(
        json.dumps(dropped, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"dropped.json: verified={len(dropped['verified'])} "
        f"dropped={len(dropped['dropped'])}"
    )


if __name__ == "__main__":
    apply()
