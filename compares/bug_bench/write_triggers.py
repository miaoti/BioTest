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
