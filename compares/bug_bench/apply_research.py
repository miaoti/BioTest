"""Apply manifest.json version pins from the Explore agent's research
plus the six seqan3 pre_fix SHAs resolved via `git rev-parse`.

Entries the agent marked UNRESOLVABLE are left at PENDING_VERIFICATION
in the main manifest AND excluded from manifest.verified.json (they
are dropped per DESIGN.md §5.2 Bohme-style drop-list discipline).

Run once after the agent research + the seqan3 SHA resolution; the
driver's --verify-only pass then filters further based on actual
install attempts.
"""

from __future__ import annotations

import json
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "compares" / "bug_bench" / "manifest.json"

# ---- Agent research output (high + medium + low-with-version) ----------
# confidence scored by the Explore agent against GitHub release notes,
# PR merges, and CHANGELOG mentions. UNRESOLVABLE entries are omitted
# below — they stay PENDING_VERIFICATION in manifest.json and do not
# enter manifest.verified.json.

RESEARCH: dict[str, dict[str, str]] = {
    # htsjdk — 5 resolvable of 10 (5 UNRESOLVABLE)
    "htsjdk-1708": {
        "pre_fix": "4.1.0", "post_fix": "4.1.1",
        "verification_rule": "PR #1708 merged 2024-06-04, shipped in htsjdk 4.1.1 on 2024-06-29 with CRAM multi-container fix cited",
        "confidence": "high",
    },
    "htsjdk-1590": {
        "pre_fix": "2.24.1", "post_fix": "3.0.0",
        "verification_rule": "PR #1590 merged 2022-02-07, first in htsjdk 3.0.0 on 2022-06-06 (CRAM 'BB' read-feature restoration)",
        "confidence": "high",
    },
    "htsjdk-1592": {
        "pre_fix": "2.24.1", "post_fix": "3.0.0",
        "verification_rule": "PR #1592 merged 2022-04-25, first in htsjdk 3.0.0 on 2022-06-06 (CRAM 'SC' scores fix)",
        "confidence": "high",
    },
    "htsjdk-1554": {
        "pre_fix": "2.24.1", "post_fix": "3.0.0",
        "verification_rule": "PR #1554 merged 2021-06-10, first in htsjdk 3.0.0 on 2022-06-06 (AC/AN/AF filtered genotypes)",
        "confidence": "high",
    },
    "htsjdk-1637": {
        "pre_fix": "3.0.3", "post_fix": "3.0.4",
        "verification_rule": "htsjdk 3.0.4 (2022-11-23) hotfix reverted PR #1593 which had caused #1637's VCF sort-order regression",
        "confidence": "high",
    },

    # pysam — 8 resolvable of 10 (2 UNRESOLVABLE: 1225, 771)
    "pysam-1314": {
        "pre_fix": "0.22.1", "post_fix": "0.23.0",
        "verification_rule": "Issue #1314 filed 2024-10-21 against 0.22.1; fix expected in 0.23.0 development stream",
        "confidence": "low",
    },
    "pysam-1308": {
        "pre_fix": "0.22.1", "post_fix": "0.23.0",
        "verification_rule": "pysam 0.23.0 release notes explicitly cite 'VariantHeader.new_record GT setting (#1308)'",
        "confidence": "high",
    },
    "pysam-966": {
        "pre_fix": "0.16.0", "post_fix": "0.17.0",
        "verification_rule": "Issue #966 filed 2020-11-06 against 0.16.0.1; 0.17.0 (2020-09-30) is the closest fix-bearing release by timeline",
        "confidence": "low",
    },
    "pysam-1175": {
        "pre_fix": "0.20.0", "post_fix": "0.21.0",
        "verification_rule": "pysam 0.21.0 release notes explicitly cite 'VariantHeader.new_record: set start/stop before alleles (#1175)'",
        "confidence": "high",
    },
    "pysam-904": {
        "pre_fix": "0.15.0", "post_fix": "0.16.0",
        "verification_rule": "pysam 0.16.0 release notes (2019-06-07) cite 'VariantFile.fetch() threw ValueError on empty files (#904)'",
        "confidence": "high",
    },
    "pysam-1038": {
        "pre_fix": "0.16.0", "post_fix": "0.17.0",
        "verification_rule": "pysam 0.17.0 release notes (2020-09-30) cite 'Eliminated file descriptor leaks in tabix_index() (#1038)'",
        "confidence": "high",
    },
    "pysam-641": {
        "pre_fix": "0.16.0", "post_fix": "0.17.0",
        "verification_rule": "Issue #641 predates 0.17.0; fix landed with index-customisation work in the 0.17.0 release stream",
        "confidence": "medium",
    },
    "pysam-450": {
        "pre_fix": "0.11.0", "post_fix": "0.12.0",
        "verification_rule": "Issue #450 was a 0.10.0 regression; 0.12.0 shipped the fix per NEWS entry referencing header-only files",
        "confidence": "low",
    },

    # biopython — 1 resolvable of 6
    "biopython-4825": {
        "pre_fix": "1.85", "post_fix": "1.86",
        "verification_rule": "PR #4837 merged 2024-09-23 (SAM deepcopy perf); first release after 1.85 is 1.86",
        "confidence": "medium",
    },

    # seqan3 — 6 resolvable of 6 (all SHAs confirmed via git rev-parse)
    "seqan3-2418": {
        "pre_fix": "df9fd5ff64f59fdb124c4a564a4141d1f9cff22b",
        "post_fix": "8e374d7ce7a1ce4de0077bc3698d5ae2c8e79600",
        "verification_rule": "git rev-parse confirmed: PR #2418 merge commit + parent",
        "confidence": "high",
    },
    "seqan3-3081": {
        "pre_fix": "fa221c1302cfe515211ea70de375a1802826d3d9",
        "post_fix": "c84f5671665478ec1b71535201cbffbe1fdd8c82",
        "verification_rule": "git rev-parse confirmed: PR #3081 merge commit + parent",
        "confidence": "high",
    },
    "seqan3-3269": {
        "pre_fix": "ca4d668390e35b4045ccd02d070927f8178ed2ce",
        "post_fix": "11564cb3bcea39666d6d3979080bc5d8fdbe1d7e",
        "verification_rule": "git rev-parse confirmed: PR #3269 merge commit + parent",
        "confidence": "high",
    },
    "seqan3-3098": {
        "pre_fix": "4961904fbc3b254f7a611b5b467c2e33ae5b1042",
        "post_fix": "4fe548913e96d3f908dd524bd3dc13b48f87bfa4",
        "verification_rule": "git rev-parse confirmed: PR #3098 merge commit + parent",
        "confidence": "high",
    },
    "seqan3-2869": {
        # Merge commit identified via `git log --merges --grep '#2869'`.
        "pre_fix": "edbfa956f^",
        "post_fix": "edbfa956f",
        "verification_rule": "git log --merges found merge commit edbfa956f for PR #2869 (correct_id_parsing_fasta)",
        "confidence": "high",
    },
    "seqan3-3406": {
        "pre_fix": "745c645fe26272791464cd67180775d28c00bf28",
        "post_fix": "5e5c05a471269703d7afc38bdc4348cef60be63b",
        "verification_rule": "git rev-parse confirmed: PR #3406 merge commit + parent",
        "confidence": "high",
    },
}

# UNRESOLVABLE entries — left at PENDING_VERIFICATION; excluded from
# manifest.verified.json. Tracked here for transparency + change log.
UNRESOLVABLE: dict[str, str] = {
    "htsjdk-1117":  "NPE in BCF2LazyGenotypesDecoder — no linked PR in release notes",
    "htsjdk-1686":  "spanning-deletion getType — issue open, no merged fix",
    "htsjdk-1026":  "multithreaded VCFEncoder — PR #1636 remains unmerged as of 2022-11",
    "htsjdk-761":   "filename '.bcf' substring — no linked PR or resolution",
    "htsjdk-423":   "multiallelic AF/AC — feature request, no merged fix",
    "pysam-1225":   "haploid PL tuple — no PR linked, no fix version documented",
    "pysam-771":    "VariantFile.write segfault on incomplete header — no merged PR",
    "biopython-4868": "Native BAM parsing — feature request, not a bug (per manifest notes)",
    "biopython-4731": "CIGAR op details — no PR linked, no fix version documented",
    "biopython-1913": "zero-score start residue — no merged PR found",
    "biopython-1699": "soft-clip query coords — no PR linked",
    "biopython-4769": "PairwiseAligner vs pairwise2 — closed without linked PR",
}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    updated = dropped = untouched = 0
    for bug in manifest["bugs"]:
        bug_id = bug["id"]
        if bug_id in RESEARCH:
            r = RESEARCH[bug_id]
            anchor = bug["anchor"]
            anchor["pre_fix"] = r["pre_fix"]
            anchor["post_fix"] = r["post_fix"]
            anchor["verification_rule"] = r["verification_rule"]
            anchor["confidence"] = r["confidence"]
            updated += 1
        elif bug_id in UNRESOLVABLE:
            bug["anchor"]["dropped_reason"] = UNRESOLVABLE[bug_id]
            dropped += 1
        else:
            untouched += 1

    manifest["benchmark_version"] = "0.2.0-research-applied"
    manifest["status"] = "research_applied_pending_install_verify"

    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[research] updated={updated} dropped={dropped} untouched={untouched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
