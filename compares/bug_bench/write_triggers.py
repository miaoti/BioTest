"""Generate trigger folders for newly-verified bugs.

Reads the manifest, finds bugs whose trigger folder is missing or
empty, and writes a stub consisting of README.md + issue_source.txt.
Existing trigger folders are preserved untouched.

For bugs where a text-format minimal reproducer is obvious (VCF / SAM
text), this script also writes an `original.vcf` / `original.sam`
seed file. Complex bugs (SAM binary cache, multithread issues) get a
descriptive README only and rely on the fuzzer-synthesis fallback
documented in DESIGN.md §4.3.
"""

from __future__ import annotations

import json
import pathlib
import textwrap

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
TRIGGERS = REPO_ROOT / "compares" / "bug_bench" / "triggers"
MANIFEST = REPO_ROOT / "compares" / "bug_bench" / "manifest.verified.json"


# Minimal VCF / SAM reproducers for bugs where the format is obvious
# from the fix-commit description. Where None, the README + issue_source
# suffice and the fuzzer handles synthesis.
TRIGGER_FILES: dict[str, dict[str, str]] = {
    "htsjdk-1364": {
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tA\tT\tNaN\t.\tAF=Inf
            1\t200\t.\tC\tG\t1e308\t.\tAF=Infinity
            1\t300\t.\tG\tA\t.\t.\tAF=nan
            """),
    },
    "htsjdk-1389": {
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##INFO=<ID=AC,Number=A,Type=Integer,Description="AC">
            ##INFO=<ID=AF,Number=A,Type=Float,Description="AF">
            ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
            ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="AD">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
            1\t100\t.\tA\tT\t.\t.\tAC=.;AF=.\tGT:AD\t./.:.
            """),
    },
    "htsjdk-1372": {
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
            ##FORMAT=<ID=GL,Number=G,Type=Float,Description="Genotype likelihoods">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\ts2
            1\t100\t.\tA\tT\t.\t.\t.\tGT:GL\t0/1:.,.,.\t./.:.,.,.
            """),
    },
    "htsjdk-1418": {
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=chr1>
            ##contig=<ID=chr2,length=2000>
            ##INFO=<ID=.,Number=0,Type=Flag,Description="no-op">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            chr1\t100\t.\tA\tT\t.\t.\t.
            """),
    },
    "htsjdk-1561": {
        "original.sam": textwrap.dedent("""\
            @HD\tVN:1.6\tSO:coordinate\tTOOLONG:bad
            @SQ\tSN:chr1\tLN:1000\tX:single
            r1\t0\tchr1\t1\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII
            """),
    },
    "htsjdk-1544": {
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##ALT=<ID=NON_REF,Description="Any non-reference allele">
            ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
            1\t100\t.\tA\t<NON_REF>\t.\t.\t.\tGT\t0/0
            1\t200\t.\tC\tT,<NON_REF>\t.\t.\t.\tGT\t0/1
            """),
    },
    "htsjdk-1538": {
        # SAM with a record whose CIGAR will be mutated at runtime.
        "original.sam": textwrap.dedent("""\
            @HD\tVN:1.6\tSO:coordinate
            @SQ\tSN:chr1\tLN:1000
            r1\t0\tchr1\t1\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII
            """),
    },
    # ----- 2026-04-20 vcfpy additions (DESIGN §A.2) -----
    "vcfpy-146": {
        # INFO flag 'STR_AS_FLAG' declared as String but appears without
        # a value → pre-fix raises TypeError.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##INFO=<ID=STR_AS_FLAG,Number=1,Type=String,Description="Mis-typed flag">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tA\tT\t.\t.\tSTR_AS_FLAG
            """),
    },
    "vcfpy-171": {
        # INFO value with %3D-escaped equals sign — pre-fix strips it on
        # re-write, so round-trip diverges.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##INFO=<ID=HGVS,Number=1,Type=String,Description="HGVS">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tA\tT\t.\t.\tHGVS=p.Lys%3DVal
            """),
    },
    "vcfpy-176": {
        # Sample GT '0|0' with GT not declared in header — pre-fix
        # crashes with ValueError on list-artefact leak.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
            1\t100\t.\tA\tT\t.\t.\t.\tGT\t0|0
            """),
    },
    "vcfpy-127": {
        # Truncated FORMAT fields (GATK 3.8 output shape) — pre-fix
        # raises KeyError: 'GQ'.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##FORMAT=<ID=GT,Number=1,Type=String,Description="GT">
            ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="AD">
            ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="DP">
            ##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="GQ">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
            1\t100\t.\tA\tT\t.\t.\t.\tGT:AD:DP:GQ\t0/1:10,5:15
            """),
    },
    "vcfpy-gtone-0.13": {
        # Haploid GT describing a single allele — pre-fix mis-parses.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=MT,length=16569>
            ##FORMAT=<ID=GT,Number=1,Type=String,Description="GT">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
            MT\t100\t.\tA\tT\t.\t.\t.\tGT\t1
            """),
    },
    # ----- 2026-04-20 noodles-vcf additions (DESIGN §A.3) -----
    "noodles-241": {
        # VCF 4.2 header with raw <-prefixed value but no ID= — pre-fix
        # (noodles-vcf 0.58) raises MissingId.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            ##META=<Description="Other record starting with '<'">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tA\tT\t.\t.\t.
            """),
    },
    "noodles-300": {
        # INFO String field containing ';' — pre-fix (noodles-vcf 0.63)
        # writer produced unreadable output.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.3
            ##contig=<ID=1,length=1000>
            ##INFO=<ID=NOTE,Number=1,Type=String,Description="Free-form note">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tA\tT\t.\t.\tNOTE=val1%3Bval2
            """),
    },
    "noodles-268": {
        # IUPAC ambiguity codes in REF — pre-fix (noodles-vcf 0.57)
        # writer corrupted output lines.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.2
            ##contig=<ID=1,length=1000>
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tR\tA\t.\t.\t.
            1\t200\t.\tY\tC\t.\t.\t.
            1\t300\t.\tN\tG\t.\t.\t.
            """),
    },
    "noodles-259": {
        # Multiple ##-prefixed header records that pre-fix 0.55
        # concatenated without newline separators on write.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.3
            ##contig=<ID=1,length=1000>
            ##META=<ID=A,Description="first">
            ##META=<ID=B,Description="second">
            ##META=<ID=C,Description="third">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
            1\t100\t.\tA\tT\t.\t.\t.
            """),
    },
    "noodles-339": {
        # INFO value containing ':' and sample value containing ';' —
        # pre-fix 0.81 writer over-encoded them.
        "original.vcf": textwrap.dedent("""\
            ##fileformat=VCFv4.3
            ##contig=<ID=1,length=1000>
            ##INFO=<ID=URL,Number=1,Type=String,Description="URL">
            ##FORMAT=<ID=GT,Number=1,Type=String,Description="GT">
            ##FORMAT=<ID=NOTE,Number=1,Type=String,Description="note">
            #CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1
            1\t100\t.\tA\tT\t.\t.\tURL=http://x:80\tGT:NOTE\t0/1:a%3Bb
            """),
    },
}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for bug in manifest["bugs"]:
        bug_id = bug["id"]
        folder = TRIGGERS / bug_id
        folder.mkdir(parents=True, exist_ok=True)

        readme = folder / "README.md"
        if not readme.exists():
            _write_readme(readme, bug)
            print(f"[readme] {bug_id}")

        issue = folder / "issue_source.txt"
        if not issue.exists():
            issue.write_text(
                f"Issue / PR: {bug['issue_url']}\n\n"
                f"Verification rule: {bug['anchor'].get('verification_rule','')}\n\n"
                f"Description (from manifest):\n"
                f"  {bug['trigger']['description']}\n",
                encoding="utf-8",
            )

        # Inline text-format triggers for bugs where the input is simple.
        for fname, content in TRIGGER_FILES.get(bug_id, {}).items():
            p = folder / fname
            if not p.exists():
                p.write_text(content, encoding="utf-8")
                print(f"[trigger] {bug_id}/{fname}")

    return 0


def _write_readme(readme: pathlib.Path, bug: dict) -> None:
    anchor = bug["anchor"]
    trig = bug["trigger"]
    signal = bug["expected_signal"]
    body = f"""# {bug['id']} — {trig['description'].split('.')[0]}.

**SUT**: {bug['sut']}
**Format**: {bug['format']}
**Severity**: {'logic bug' if trig.get('logic_bug') else 'crash / incorrect rejection'}
**Anchor**: {anchor['type']} `{anchor['pre_fix']}` → `{anchor['post_fix']}`
**Confidence**: {anchor.get('confidence', 'unknown')}
**Issue / PR**: {bug['issue_url']}

## What the bug does

{trig['description']}

## Trigger

See sibling files in this folder (if present):

- `original.{bug['format'].lower()}` — minimal text-format input seed when applicable.
- `issue_source.txt` — raw issue / PR reference for traceability.

If no `original.*` file is present, the bench driver falls back to
fuzzer-synthesised triggers per DESIGN.md §4.3.

## Detection criterion

- **Expected signal**: `{signal['type']}`
- **Compared against**: {', '.join(signal.get('against', [])) or 'pre-fix SUT'}
"""
    also = signal.get("also_detectable_via")
    if also:
        body += f"- **Also detectable via**: {', '.join(also)}\n"
    readme.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
