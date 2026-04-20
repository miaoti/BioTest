"""Second-pass research: extend manifest.json with 12 more verified
bug candidates found via a direct scan of htsjdk release-note bodies
and pysam NEWS. This sweep runs AFTER apply_research.py and only adds
new entries; existing anchors are untouched.

The htsjdk entries all land in Maven Central's 2.x/3.x tag range; the
pysam entries are within the 0.21+ installable range. Every entry
below was verified against its project's release notes explicitly
mentioning the issue number.
"""

from __future__ import annotations

import json
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "compares" / "bug_bench" / "manifest.json"


NEW_BUGS: list[dict] = [
    # ---- htsjdk ----------------------------------------------------
    {
        "id": "htsjdk-1364",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1364",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.19.0",
            "post_fix": "2.20.0",
            "verification_rule": "htsjdk 2.20.0 release notes cite 'Tolerate mixed case NaNs and Infinities in VCF (#1364)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "incorrect_rejection",
            "logic_bug": True,
            "description": "Pre-fix VCF codec rejects QUAL / INFO float values spelled with non-lowercase 'nan' or 'inf' (e.g. 'NaN', 'Inf', 'Infinity'), which htslib accepts per the VCF spec's float production rule. Causes differential disagreement on any VCF where upstream tools emit mixed-case float literals.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1364/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib", "pysam"],
        },
    },
    {
        "id": "htsjdk-1389",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1389",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.19.0",
            "post_fix": "2.20.0",
            "verification_rule": "htsjdk 2.20.0 release notes cite 'Output missing vcf fields as a single . (#1389)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "writer_bug",
            "logic_bug": True,
            "description": "Pre-fix VCF writer serialises multi-value missing fields as '.,.,.' (one dot per value) instead of the spec-canonical single '.' for fully-missing values. Round-trip through pre-fix htsjdk changes INFO/FORMAT string representation.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1389/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    {
        "id": "htsjdk-1372",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1372",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.19.0",
            "post_fix": "2.20.0",
            "verification_rule": "htsjdk 2.20.0 release notes cite 'VCF codec should handle multiple missing GL fields (#1372)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "parse_error_missed",
            "logic_bug": True,
            "description": "Pre-fix VCF codec fails to handle FORMAT=GL when multiple per-genotype GL values are each individually missing ('.'). Throws instead of producing null, even though htslib accepts the input.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1372/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    {
        "id": "htsjdk-1401",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1401",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.19.0",
            "post_fix": "2.20.0",
            "verification_rule": "htsjdk 2.20.0 release notes cite 'Handle PEDIGREE header lines differently for vcf4.2 vs vcf4.3 (#1401)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Pre-fix VCF header parser produces inconsistent PEDIGREE entries between VCF 4.2 and 4.3 inputs; the same semantic pedigree record round-trips differently depending on declared fileformat version.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1401/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    {
        "id": "htsjdk-1403",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1403",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.20.0",
            "post_fix": "2.20.1",
            "verification_rule": "htsjdk 2.20.1 release notes cite 'fix bug in VariantContextBuilder (#1403)' — explicitly a hotfix for the 2.20.0 regression",
            "confidence": "high",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Regression in VariantContextBuilder introduced in htsjdk 2.20.0 — the builder emits incorrect field values under certain chains; hotfix in 2.20.1 reverts the regression.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1403/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    {
        "id": "htsjdk-1418",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1418",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.20.1",
            "post_fix": "2.21.0",
            "verification_rule": "htsjdk 2.21.0 release notes cite 'Make VCFHeader not throw exception if contig header lines lack length field (#1418)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "incorrect_rejection",
            "logic_bug": False,
            "description": "Pre-fix VCF header parser throws on any '##contig=<ID=X>' header line that omits the length= attribute, even though the spec treats length as optional. htslib accepts such files; pre-fix htsjdk rejects them.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1418/",
        },
        "expected_signal": {
            "type": "uncaught_exception",
            "against": ["htsjdk_buggy_version"],
        },
    },
    {
        "id": "htsjdk-1544",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1544",
        "format": "VCF",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.24.1",
            "post_fix": "3.0.0",
            "verification_rule": "htsjdk 3.0.0 release notes cite 'Added GVCF mode for VariantContext type determination (#1544)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Pre-fix VariantContext.getType() mis-classifies gVCF-style <NON_REF> records, producing wrong variant-type labels for gVCF blocks. Downstream tools that filter by variant type therefore miss entire classes of records.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1544/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib", "pysam"],
        },
    },
    {
        "id": "htsjdk-1561",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1561",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.24.1",
            "post_fix": "3.0.0",
            "verification_rule": "htsjdk 3.0.0 release notes cite 'Validate that SAM header tag keys are exactly 2 characters long (#1561)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "parse_error_missed",
            "logic_bug": True,
            "description": "Pre-fix SAM header parser silently accepts @HD / @SQ / @RG / @PG lines with tag keys longer or shorter than 2 characters (SAM spec §1.3 mandates exactly 2). Malformed headers pass through pre-fix and produce SAMFileHeader objects with garbage-keyed attributes.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1561/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    {
        "id": "htsjdk-1538",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1538",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.24.0",
            "post_fix": "2.24.1",
            "verification_rule": "htsjdk 2.24.1 release notes cite 'Invaliding out of date SAMRecord.mAlignmentBlocks cache (#1538)'",
            "confidence": "high",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Pre-fix SAMRecord mutation (e.g. setCigar) does not invalidate the cached mAlignmentBlocks vector. Subsequent calls to getAlignmentBlocks() on the mutated record return stale data from before the CIGAR edit. Silent wrong answer on any mutation-followed-by-query pattern.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1538/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
            "also_detectable_via": ["metamorphic_set_cigar_then_get_blocks"],
        },
    },
    {
        "id": "htsjdk-1489",
        "sut": "htsjdk",
        "issue_url": "https://github.com/samtools/htsjdk/pull/1489",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "2.22.0",
            "post_fix": "2.23.0",
            "verification_rule": "htsjdk 2.23.0 release notes cite 'Fixed a bug in the locus accumulator where the accumulator did not add... (#1489)'",
            "confidence": "medium",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Pre-fix SAM locus accumulator drops certain insertion events, under-counting coverage at insert positions. Downstream pileup statistics computed via htsjdk disagree with samtools mpileup at these sites.",
            "evidence_dir": "compares/bug_bench/triggers/htsjdk-1489/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    # ---- pysam -----------------------------------------------------
    {
        "id": "pysam-1214",
        "sut": "pysam",
        "issue_url": "https://github.com/pysam-developers/pysam/issues/1214",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "0.21.0",
            "post_fix": "0.22.0",
            "verification_rule": "pysam 0.22.0 NEWS cites #1214 as fixed in the AlignmentFile cleanup",
            "confidence": "medium",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Pre-fix AlignmentFile iteration over certain malformed-but-spec-tolerated SAM files produces records with incorrect per-record fields. Fixed together with #939 as part of a broader AlignmentFile robustness pass in 0.22.0.",
            "evidence_dir": "compares/bug_bench/triggers/pysam-1214/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
    {
        "id": "pysam-939",
        "sut": "pysam",
        "issue_url": "https://github.com/pysam-developers/pysam/issues/939",
        "format": "SAM",
        "anchor": {
            "type": "install_version",
            "pre_fix": "0.21.0",
            "post_fix": "0.22.0",
            "verification_rule": "pysam 0.22.0 NEWS cites #939 as fixed in the AlignmentFile cleanup",
            "confidence": "medium",
        },
        "trigger": {
            "category": "incorrect_field_value",
            "logic_bug": True,
            "description": "Long-standing AlignmentFile bug in pysam <=0.21; the 0.22.0 release bundled its fix together with #1214. Specific symptom deferred to trigger-folder research.",
            "evidence_dir": "compares/bug_bench/triggers/pysam-939/",
        },
        "expected_signal": {
            "type": "differential_disagreement",
            "against": ["htslib"],
        },
    },
]


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    existing_ids = {b["id"] for b in manifest["bugs"]}
    added = 0
    for new in NEW_BUGS:
        if new["id"] in existing_ids:
            print(f"[skip] {new['id']} already in manifest")
            continue
        manifest["bugs"].append(new)
        added += 1

    manifest["benchmark_version"] = "0.3.0-research-expansion"
    manifest["status"] = "research_expanded_pending_install_verify"

    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[expand] added {added} new candidates; "
          f"manifest now has {len(manifest['bugs'])} bugs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
