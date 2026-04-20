"""Append the 2026-04-20 vcfpy + noodles-vcf bug candidates to manifest.json.

Idempotent: if an entry with the same `id` already exists, the script
updates it in place rather than appending a duplicate.

Research source: see DESIGN.md §A.2 (vcfpy, 7 candidates) + §A.3
(noodles-vcf, 9 candidates). Version pins come from the upstream
CHANGELOGs and are quoted verbatim in `anchor.verification_rule`.
"""

from __future__ import annotations

import json
import pathlib

BENCH = pathlib.Path(__file__).resolve().parent
MANIFEST = BENCH / "manifest.json"


def _bug(
    bug_id: str,
    sut: str,
    issue_url: str,
    pre_fix: str,
    post_fix: str,
    category: str,
    logic_bug: bool,
    description: str,
    signal_type: str,
    signal_against: list[str],
    verification_rule: str,
    confidence: str,
    anchor_type: str = "install_version",
) -> dict:
    return {
        "id": bug_id,
        "sut": sut,
        "issue_url": issue_url,
        "format": "VCF",
        "anchor": {
            "type": anchor_type,
            "pre_fix": pre_fix,
            "post_fix": post_fix,
            "verification_rule": verification_rule,
            "confidence": confidence,
        },
        "trigger": {
            "category": category,
            "logic_bug": logic_bug,
            "description": description,
            "evidence_dir": f"compares/bug_bench/triggers/{bug_id}/",
        },
        "expected_signal": {
            "type": signal_type,
            "against": signal_against,
        },
    }


VCFPY_BUGS = [
    _bug(
        "vcfpy-176",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/issues/176",
        "0.13.8", "0.14.0",
        "incorrect_field_value", True,
        "Sample GT value '0|0' with GT undeclared in header causes a list "
        "artefact to leak into _genotype_updated, raising ValueError: "
        "invalid literal for int() with base 10: \"['0\".",
        "uncaught_exception", ["vcfpy"],
        "Changelog 0.14.0 Bug Fixes: \"A sample column value of 0|0 is not "
        "being parsed correctly (#176) (#187)\"",
        "high",
    ),
    _bug(
        "vcfpy-171",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/issues/171",
        "0.13.8", "0.14.0",
        "round_trip_asymmetry", True,
        "Escaped '=' in INFO (e.g., p.Lys%3D) is lost on re-write; comma is "
        "escaped but '=' is not, breaking round-trip.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.14.0 Bug Fixes: \"escaped equal sign in INFO fields "
        "(#171) (#172)\"",
        "high",
    ),
    _bug(
        "vcfpy-146",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/issues/146",
        "0.13.3", "0.13.4",
        "parse_error_missed", False,
        "INFO flag present but header declares it as String type; raises "
        "TypeError: argument of type 'bool' is not iterable.",
        "uncaught_exception", ["vcfpy"],
        "Changelog 0.13.4: \"Fix INFO flag raises TypeError (#146)\"",
        "high",
    ),
    _bug(
        "vcfpy-145",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/issues/145",
        "0.13.4", "0.13.5",
        "parse_error_missed", False,
        "'.bgz'-suffixed bgzipped VCF not recognized by reader; open fails.",
        "uncaught_exception", ["vcfpy"],
        "Changelog 0.13.5: \"Treat .bgz files the same as .gz (#145, #149)\"",
        "medium",
    ),
    _bug(
        "vcfpy-gtone-0.13",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/blob/main/CHANGELOG.md",
        "0.12.1", "0.12.2",
        "edge_case_missed", True,
        "Haploid / partial-haploid GT describing only one allele parsed "
        "incorrectly.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.12.2: \"Fixing bug in case GT describes only one "
        "allele.\"",
        "medium",
    ),
    _bug(
        "vcfpy-127",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/issues/127",
        "0.11.0", "0.11.1",
        "parse_error_missed", False,
        "Incomplete trailing FORMAT fields (e.g. GATK 3.8 truncated output) "
        "raises KeyError: 'GQ'.",
        "uncaught_exception", ["vcfpy"],
        "Changelog 0.11.1: \"Working around problem in HTSJDK output with "
        "incomplete FORMAT fields (#127)\"",
        "medium",
    ),
    _bug(
        "vcfpy-nocall-0.8",
        "vcfpy",
        "https://github.com/bihealth/vcfpy/blob/main/CHANGELOG.md",
        "0.8.1", "0.9.0",
        "incorrect_field_value", True,
        "No-call GT (./.) parsed incorrectly in very early vcfpy. Install-rot "
        "risk on 0.8.1 under modern Python.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.9.0: \"Fixing parsing of no-call GT fields\"",
        "low",
    ),
]


NOODLES_BUGS = [
    _bug(
        "noodles-300",
        "noodles",
        "https://github.com/zaeleus/noodles/issues/300",
        "0.63", "0.64",
        "round_trip_asymmetry", True,
        "Writing an INFO String containing ';' produced unreadable VCF; "
        "round-trip broke. Fix: percent-decoding of string/char values.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.64: \"vcf/record/info/field/value: Percent-decode "
        "character and string values ([#300])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-339",
        "noodles",
        "https://github.com/zaeleus/noodles/issues/339",
        "0.81", "0.82",
        "writer_bug", True,
        "Writer over-encoded ':' in INFO values and ';'/'=' in sample values, "
        "producing non-round-trippable output.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.82: \"vcf/io/writer/record/info/field/value: Remove "
        "colon (:) from encode set ([#339])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-268",
        "noodles",
        "https://github.com/zaeleus/noodles/issues/268",
        "0.57", "0.58",
        "writer_bug", True,
        "IUPAC ambiguity codes in REF caused writer to emit corrupted / "
        "truncated lines (e.g. two records merged).",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.58: \"vcf/io/writer/record/reference_bases: Resolve "
        "IUPAC ambiguity codes ([#268])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-223",
        "noodles",
        "https://github.com/zaeleus/noodles/pull/223",
        "0.48", "0.49",
        "incorrect_field_value", True,
        "lazy::Record::info_range returned the FILTER byte range instead of "
        "INFO; callers reading INFO saw FILTER bytes.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.49: \"vcf/lazy/record/bounds: Fix range for info field "
        "([#223])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-224",
        "noodles",
        "https://github.com/zaeleus/noodles/pull/224",
        "0.48", "0.49",
        "parse_error_missed", True,
        "Lazy reader read past end-of-record into next line when optional "
        "trailing fields were missing, corrupting the buffer.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.49: \"vcf/reader/lazy_record: Disallow newlines to "
        "appear in fields ([#224])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-259",
        "noodles",
        "https://github.com/zaeleus/noodles/issues/259",
        "0.55", "0.56",
        "writer_bug", True,
        "Writer emitted multiple '##'-prefixed header records without "
        "separator newlines, producing a malformed header.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.56: \"vcf/io/writer/header/record: Write newlines for "
        "records in other collections ([#259])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-241",
        "noodles",
        "https://github.com/zaeleus/noodles/issues/241",
        "0.58", "0.59",
        "incorrect_rejection", False,
        "VCF 4.2 header with raw value starting with '<' but no ID= (e.g., "
        "##ID=<Description=\"...\">) raised MissingId parse error.",
        "uncaught_exception", ["noodles"],
        "Changelog 0.59: \"Parse other header record values that start with "
        "a map prefix (<) as a string if there is no map identifier "
        "([#241])\"",
        "high",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-inforay-0.64",
        "noodles",
        "https://github.com/zaeleus/noodles/blob/master/noodles-vcf/CHANGELOG.md",
        "0.63", "0.64",
        "incorrect_field_value", True,
        "array::values iterator mis-counted entries and didn't terminate on "
        "empty lists; wrong length / infinite loop for INFO/FORMAT arrays.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.64 Fixed: \"Fix counting number of values\" / \"Fix "
        "iterating over empty lists\"",
        "medium",
        anchor_type="cargo_version",
    ),
    _bug(
        "noodles-ob1-0.23",
        "noodles",
        "https://github.com/zaeleus/noodles/blob/master/noodles-vcf/CHANGELOG.md",
        "0.23", "0.24",
        "edge_case_missed", True,
        "Genotype parser silently dropped sample values after the last "
        "FORMAT key; header without trailing newline triggered an infinite "
        "loop.",
        "differential_disagreement", ["htslib", "htsjdk"],
        "Changelog 0.24: \"vcf/record/genotypes/genotype: Fail parsing when "
        "there are more values than keys.\"",
        "medium",
        anchor_type="cargo_version",
    ),
]


NEW_BUGS = VCFPY_BUGS + NOODLES_BUGS


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {b["id"]: i for i, b in enumerate(manifest["bugs"])}
    added = 0
    updated = 0
    for bug in NEW_BUGS:
        if bug["id"] in by_id:
            manifest["bugs"][by_id[bug["id"]]] = bug
            updated += 1
        else:
            manifest["bugs"].append(bug)
            added += 1

    # Bump the benchmark_version string to mark the refactor.
    manifest["benchmark_version"] = "0.4.0-vcfpy-noodles"
    manifest["status"] = "vcfpy_noodles_appended_pending_install_verify"
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[append] vcfpy+noodles: added={added} updated={updated} "
          f"total_bugs={len(manifest['bugs'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
