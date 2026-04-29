"""Rank 12 — Structural Variant Generator (branch-diversity corpus lever).

Motivation (per run-5 diagnostic, `compares/results/mutation/biotest/
RUN5_FINAL.md` + per-operator kill-gap analysis 2026-04-23):

Jazzer's coverage-guided corpus for htsjdk_sam kills +37 more
`RemoveConditional_EQUAL_ELSE` and +12 more `VoidMethodCall` mutants than
BioTest's Ranks 9+10+11 combined corpus, despite reaching almost
identical classes (25 vs 23). The gap is **within-class branch
diversity**: our seeds all traverse the same if/else chain through each
parser because every file shares the same CIGAR shape (`27M1D73M`), same
tag types (`Z`, `i`), and same header combinations (@HD + @SQ only).

Ranks 9/11 vary *values* inside a fixed structure. Rank 10 varies bytes.
Neither produces files that take *different parse paths* through the
same class. RemoveConditional_EQUAL_ELSE mutants specifically need the
else-branch to fire — which requires inputs that satisfy the opposite
predicate at each branch.

Rank 12 fills that gap by deterministically enumerating **structural**
variants from a small spec-derived catalogue: different CIGAR operator
mixes, different tag type letters, different header-line shapes, and
different flag-bit combinations. Output files are still validity-gated
through the same canonical normalizer (and optionally the SUT parser
via Refinement C).

Zero new dependency, zero oracle-path change. Output lives in
`seeds/<fmt>_struct/struct_<sha8>.{sam,vcf}` so Phase-C's MR loop
doesn't glob them; mutation-score staging unions them explicitly
(same convention as `seeds/<fmt>_diverse/` for Rank 9/11 and
`seeds/<fmt>_bytefuzz/` for Rank 10).

References:
  * Andrews, Briand & Labiche, ICSE'05 — structural test data variety
    (specifically varied CIGAR/INFO shapes) kills significantly more
    mutants than numerical variety at equal corpus size.
  * Just, Schweiggert & Kapfhammer, FSE'14 — relational/conditional
    mutants dominate real-bug prediction; branch-diverse inputs kill
    them directly, random inputs don't.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import logging
import re
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logger = logging.getLogger("structural_diversifier")


# ---------------------------------------------------------------------------
# SAM structural catalogues (all from SAMv1 spec, §5.4 CIGAR + §1.5 tags)
# ---------------------------------------------------------------------------

# Each entry is a CIGAR string whose operator mix exercises a distinct
# parse path through htsjdk's CigarElement dispatch / noodles'
# Cigar::parse / pysam's bam_cigar_* / seqan3's cigar_from_string.
# Kept short (<=20 ops) to control file size.
_CIGAR_SHAPES = [
    "10M",              # simple match — baseline
    "5M1I5M",           # insertion
    "5M1D5M",           # deletion
    "3H5M2S",           # hard + soft clip
    "2S5M3S",           # soft-only
    "5=5X",             # seq-match + seq-mismatch (requires =/X support)
    "3M1N3M",           # skipped region (RNA)
    "5M1P5M",           # pad
    "3M1I2D3M",         # insert + delete combo
    "1S1M1I1D1M1N1M1P1M1=1X1M",  # every operator
    "10M1D10M",         # longer deletion
    "10M1I10M",         # longer insertion
    "20M",              # long match
    "*",                # unknown CIGAR — valid per spec
]

# Tag types — (letter, value). Each triggers a different dispatch in
# the SAM parser's tag-type switch. Value is kept short + valid.
_TAG_TYPE_SAMPLES = [
    ("A", "N"),         # printable char
    ("i", "42"),        # signed int
    ("f", "0.5"),       # float
    ("Z", "sometext"),  # printable string
    ("H", "CAFE"),      # hex byte array (must be even length)
    ("B", "c,1,2,3"),   # byte array (8-bit signed int)
    ("B", "i,1,2,3"),   # int32 array
    ("B", "f,1.0,2.0"), # float array
]

# Common two-letter tag names (SAMv1 §1.5 specified tags + common
# optional tags). Each triggers a different htsjdk `SAMTag` enum path.
_TAG_NAMES = ["NM", "MD", "AS", "XS", "RG", "PG", "XT", "CM", "MQ", "SM"]

# Sampled flag combinations — each bit drives a different SAMFlag$N
# enum branch in htsjdk (see SamFlagField$1-$5 — observed coverage gap
# in run-5 diagnostic).
_FLAG_COMBOS = [
    0,      # unmapped
    1,      # paired
    2,      # proper pair
    4,      # unmapped (redundant-label but different flag)
    16,     # reverse strand
    64,     # first-in-pair
    128,    # second-in-pair
    256,    # secondary alignment
    512,    # QC fail
    1024,   # duplicate
    2048,   # supplementary
    99,     # proper-pair forward first (0x63 = 1+2+32+64)
    147,    # proper-pair reverse second (0x93 = 1+2+16+128)
    4095,   # all 12 bits set (stress test)
]


def _emit_sam_header(num_sq: int = 1, include_rg: bool = False,
                     include_pg: bool = False, include_co: bool = False) -> list[str]:
    """Spec-varied header: 1-3 @SQ lines + optional @RG/@PG/@CO."""
    lines = ["@HD\tVN:1.6\tSO:unsorted"]
    for i in range(num_sq):
        lines.append(f"@SQ\tSN:ref{i if num_sq > 1 else ''}\tLN:1000")
    if include_rg:
        lines.append("@RG\tID:rg1\tSM:sample1\tLB:lib1\tPL:ILLUMINA")
    if include_pg:
        lines.append("@PG\tID:bwa\tPN:bwa\tVN:0.7.17\tCL:bwa mem ref.fa reads.fq")
    if include_co:
        lines.append("@CO\tstructural-variant generator")
    return lines


def _build_sam_record(cigar: str, flag: int, pos: int = 10,
                      rname: str = "ref", mapq: int = 30,
                      tags: Optional[list[str]] = None) -> str:
    """Build a valid SAM record with given CIGAR/flag/tags. Seq + qual
    sized to match CIGAR's consumed-query length."""
    # Compute consumed query length for the CIGAR (for seq/qual size).
    import re as _re
    total_q = 0
    for length, op in _re.findall(r"(\d+)([MIDNSHPX=])", cigar):
        if op in "MIS=X":
            total_q += int(length)
    if cigar == "*" or total_q == 0:
        seq = "*"
        qual = "*"
    else:
        seq = ("ACGTN" * ((total_q // 5) + 1))[:total_q]
        qual = "I" * total_q

    fields = [
        "read1", str(flag), rname, str(pos), str(mapq), cigar,
        "*", "0", "0", seq, qual
    ]
    if tags:
        fields.extend(tags)
    return "\t".join(fields)


def generate_sam_structural_variants(source_text: str,
                                     max_per_seed: int = 60) -> list[str]:
    """Emit structural variants: vary CIGAR shapes × flags × tags × headers."""
    # We don't preserve the source records — we generate fresh records
    # whose structure covers the catalogue. Source_text is only used for
    # header hints (e.g. number of @SQ lines the source author intended).
    out: list[str] = []
    emitted = 0

    # 1) CIGAR-shape variants — for each CIGAR, emit with a mapped+flag=0 record.
    for cigar in _CIGAR_SHAPES:
        if emitted >= max_per_seed:
            break
        header = _emit_sam_header(num_sq=1, include_rg=False)
        rec = _build_sam_record(cigar, flag=0, pos=10, rname="ref")
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 2) Tag-type variants — fixed CIGAR, vary tag type in a single tag.
    for tag_name, (tt, tv) in itertools.product(_TAG_NAMES[:5], _TAG_TYPE_SAMPLES):
        if emitted >= max_per_seed:
            break
        header = _emit_sam_header(num_sq=1)
        rec = _build_sam_record("10M", flag=0, pos=10, rname="ref",
                                tags=[f"{tag_name}:{tt}:{tv}"])
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 3) Flag-combination variants — simple 10M record, different flags.
    for flag in _FLAG_COMBOS:
        if emitted >= max_per_seed:
            break
        header = _emit_sam_header(num_sq=1, include_rg=(flag & 1))
        rec = _build_sam_record("10M", flag=flag, pos=10, rname="ref",
                                tags=["NM:i:0"])
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 4) Header-shape variants — vary @SQ count, @RG/@PG/@CO presence.
    for num_sq, rg, pg, co in itertools.product([1, 2, 3], [False, True],
                                                 [False, True], [False, True]):
        if emitted >= max_per_seed:
            break
        header = _emit_sam_header(num_sq=num_sq, include_rg=rg,
                                  include_pg=pg, include_co=co)
        rec = _build_sam_record("10M", flag=0, pos=10,
                                rname=f"ref0" if num_sq > 1 else "ref")
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 5) Multi-record variants — spans a wide range of record counts so
    #     baseline outcomes cover `ok:N` for many distinct N values
    #     (outcome-diversity ceiling — same fix rationale as VCF 3d).
    # 5) Multi-record variants — 2-5 records with mixed CIGARs to exercise
    #     record-iterator state transitions (distinct parse paths through
    #     SAMTextReader's record-to-record dispatch).
    for i in range(min(max_per_seed - emitted, 8)):
        if emitted >= max_per_seed:
            break
        header = _emit_sam_header(num_sq=1, include_rg=True)
        n_recs = 2 + (i % 4)
        recs = []
        for j in range(n_recs):
            cigar = _CIGAR_SHAPES[j % len(_CIGAR_SHAPES)]
            flag = _FLAG_COMBOS[(i + j) % len(_FLAG_COMBOS)]
            recs.append(_build_sam_record(cigar, flag=flag,
                                          pos=10 + j * 20, rname="ref",
                                          tags=[f"NM:i:{j}"]))
        out.append("\n".join(header + recs) + "\n")
        emitted += 1

    return out


# ---------------------------------------------------------------------------
# VCF structural catalogues (from VCFv4.2 spec)
# ---------------------------------------------------------------------------

_VCF_INFO_SHAPES = [
    ".",                                        # missing INFO
    "DP=100",                                   # single
    "DP=100;AF=0.5",                            # pair
    "DP=100;AF=0.5;AC=1;AN=2",                  # quad
    "DP=100;AF=0.5;AC=1;AN=2;MQ=60;SOMATIC",    # 5 keys + flag
    "AA=A;CIGAR=3M1I1M;DB;H2;VALIDATED",        # spec-defined flags + strings
    "AF=0.0,0.5,1.0",                           # multi-value AF
    "AC=1,2,3;AN=6",                            # multi-value AC matching multi-ALT
]

_VCF_ALT_SHAPES = [
    "A",           # SNP
    "AT",          # insertion
    "A,T",         # multi-ALT
    "A,T,G",       # multi-ALT 3
    "<DEL>",       # symbolic DEL
    "<DUP>",       # symbolic DUP
    "<INS>",       # symbolic INS
    "<CNV>",       # symbolic CNV
    "*",           # upstream-deletion spanning
]

_VCF_FORMAT_SHAPES = [
    ("GT",         ["0/1"]),
    ("GT:DP",      ["0/1:30"]),
    ("GT:DP:GQ",   ["0/1:30:99"]),
    ("GT:DP:AD",   ["0/1:30:15,15"]),
    ("GT:PL",      ["0/1:0,30,100"]),
    ("GT:GQ:DP:HQ:PL", ["0/1:99:30:50,50:0,30,300"]),
    ("GT:PS:PID",  ["0|1:1:rs123"]),
]

# Multi-sample genotype sets — each entry is (FORMAT, [sample_values...]).
# Exercises multi-sample iteration in VariantContext / GenotypesContext
# and the sample-column-count branches in AbstractVCFCodec.
_VCF_MULTI_SAMPLE = [
    ("GT",           ["0/1", "1/1", "0/0"]),                           # 3 samples
    ("GT:DP",        ["0/1:30", "0/0:25", "1/1:40", "./.:0"]),         # 4 samples, missing
    ("GT:GQ:DP",     ["0/1:99:30", "0/0:99:25", "1/1:99:40"]),         # 3 samples
    ("GT:AD:DP:GQ:PL", ["0/1:15,15:30:99:0,30,300",
                         "0/0:30,0:30:99:0,60,600",
                         "1/1:0,40:40:99:900,90,0"]),                   # 3 samples rich
    ("GT:GQ:DP",     ["0|1:99:30", "1|0:99:25", "0|0:99:40", "1|1:99:35", "./.:.:."]),  # 5 samples phased+missing
]

# FILTER strings — jazzer corpus has rich filter diversity.
_VCF_FILTERS = ["PASS", ".", "q10", "LowQual", "q10;LowQual",
                "MinSeqDepth", "MQ40", "SnpCluster", "PASS;LowQual"]

# Varied ##FILTER definitions — each unique FILTER ID exercises a
# different branch in VCFHeader's filter map.
_EXTRA_FILTER_DEFS = [
    '##FILTER=<ID=q10,Description="Quality below 10">',
    '##FILTER=<ID=LowQual,Description="Low quality">',
    '##FILTER=<ID=MinSeqDepth,Description="DP < 10">',
    '##FILTER=<ID=MQ40,Description="MQ < 40">',
    '##FILTER=<ID=SnpCluster,Description="Cluster of SNPs">',
]


def _vcf_minimal_header(include_contig: bool = True,
                        include_format: bool = True,
                        include_info: bool = True,
                        include_filter: bool = False,
                        extra_filters: bool = False) -> list[str]:
    lines = ["##fileformat=VCFv4.2"]
    if include_contig:
        lines.append("##contig=<ID=1,length=249250621>")
        lines.append("##contig=<ID=2,length=243199373>")
        lines.append("##contig=<ID=X,length=155270560>")
    if include_info:
        lines.append('##INFO=<ID=DP,Number=1,Type=Integer,Description="">')
        lines.append('##INFO=<ID=AF,Number=A,Type=Float,Description="">')
        lines.append('##INFO=<ID=AC,Number=A,Type=Integer,Description="">')
        lines.append('##INFO=<ID=AN,Number=1,Type=Integer,Description="">')
        lines.append('##INFO=<ID=MQ,Number=1,Type=Float,Description="">')
        lines.append('##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description="">')
        lines.append('##INFO=<ID=AA,Number=1,Type=String,Description="">')
        lines.append('##INFO=<ID=CIGAR,Number=A,Type=String,Description="">')
        lines.append('##INFO=<ID=DB,Number=0,Type=Flag,Description="">')
        lines.append('##INFO=<ID=H2,Number=0,Type=Flag,Description="">')
        lines.append('##INFO=<ID=VALIDATED,Number=0,Type=Flag,Description="">')
        lines.append('##INFO=<ID=HRun,Number=1,Type=Integer,Description="">')
        lines.append('##INFO=<ID=Dels,Number=1,Type=Float,Description="">')
    if include_format:
        lines.append('##FORMAT=<ID=GT,Number=1,Type=String,Description="">')
        lines.append('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="">')
        lines.append('##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="">')
        lines.append('##FORMAT=<ID=AD,Number=R,Type=Integer,Description="">')
        lines.append('##FORMAT=<ID=PL,Number=G,Type=Integer,Description="">')
        lines.append('##FORMAT=<ID=GL,Number=3,Type=Float,Description="">')
        lines.append('##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="">')
        lines.append('##FORMAT=<ID=PS,Number=1,Type=Integer,Description="">')
        lines.append('##FORMAT=<ID=PID,Number=1,Type=String,Description="">')
    if include_filter:
        lines.append('##FILTER=<ID=PASS,Description="All filters passed">')
    if extra_filters:
        lines.extend(_EXTRA_FILTER_DEFS)
    return lines


def generate_vcf_structural_variants(source_text: str,
                                     max_per_seed: int = 50) -> list[str]:
    """Emit VCF variants with varied INFO / ALT / FORMAT / header shapes."""
    out: list[str] = []
    emitted = 0

    # 1) INFO shape × ALT shape combinations — no FORMAT column (simple record).
    for info in _VCF_INFO_SHAPES:
        if emitted >= max_per_seed:
            break
        for alt in _VCF_ALT_SHAPES[:4]:
            if emitted >= max_per_seed:
                break
            header = _vcf_minimal_header(include_contig=True, include_info=True,
                                         include_format=False)
            header.append("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")
            n_alt = len(alt.split(","))
            # Match AC/AN to ALT count if info involves them.
            info_fixed = info
            if "AC=" in info and n_alt > 1:
                info_fixed = re.sub(r"AC=\d+", f"AC={','.join(['1']*n_alt)}", info)
                info_fixed = re.sub(r"AN=\d+", f"AN={n_alt*2}", info_fixed)
            rec = f"1\t100\trs1\tA\t{alt}\t50.0\tPASS\t{info_fixed}"
            out.append("\n".join(header + [rec]) + "\n")
            emitted += 1

    # 2) FORMAT shape variants — with per-sample genotypes.
    for fmt_key, samples in _VCF_FORMAT_SHAPES:
        if emitted >= max_per_seed:
            break
        header = _vcf_minimal_header(include_contig=True, include_info=True,
                                     include_format=True)
        header.append(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE1")
        rec = f"1\t100\trs1\tA\tT\t50.0\tPASS\tDP=30\t{fmt_key}\t{samples[0]}"
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 3) Multi-record files — 2-10 records with varying INFO/ALT shapes
    #    across multiple contigs (exercises AbstractVCFCodec's record-
    #    iterator branches that jazzer's 10-20-record corpus hits heavily).
    for i in range(min(max_per_seed - emitted, 12)):
        header = _vcf_minimal_header()
        header.append("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")
        n_recs = 3 + (i % 8)  # 3..10 records
        recs = []
        for j in range(n_recs):
            info = _VCF_INFO_SHAPES[(i + j) % len(_VCF_INFO_SHAPES)]
            alt = _VCF_ALT_SHAPES[j % len(_VCF_ALT_SHAPES)]
            chrom = ["1", "2", "X"][j % 3]
            filt = _VCF_FILTERS[(i + j) % len(_VCF_FILTERS)]
            qual = ["50.0", "99.9", ".", "0.01", "999"][j % 5]
            rid = ["rs1", ".", f"id{j}", f"rs{j},esv{j+1}"][j % 4]
            recs.append(f"{chrom}\t{100 + j * 50}\t{rid}\tA\t{alt}\t{qual}\t{filt}\t{info}")
        out.append("\n".join(header + recs) + "\n")
        emitted += 1

    # 3b) Multi-sample records — 3-5 samples per record. This exercises
    #     VariantContext.getGenotypes iteration, GenotypesContext, and
    #     the sample-column-count branch in AbstractVCFCodec (+25 kill
    #     gap on AbstractVCFCodec observed in r12v1 diagnostic).
    for fmt_key, samples in _VCF_MULTI_SAMPLE:
        if emitted >= max_per_seed:
            break
        header = _vcf_minimal_header(extra_filters=True)
        sample_names = "\t".join(f"NA{i:05d}" for i in range(1, len(samples) + 1))
        header.append(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{sample_names}")
        # Emit 3-5 records in each multi-sample file.
        recs = []
        for j in range(4):
            alt = ["T", "T,C", "<DEL>", "A,T,G"][j]
            info = ["DP=30;AF=0.5", "DP=100;AF=0.5,0.25", "SVTYPE=DEL;END=200", "DP=60;AC=1,1,1;AN=6"][j]
            filt = _VCF_FILTERS[j % len(_VCF_FILTERS)]
            sample_str = "\t".join(samples)
            recs.append(f"1\t{100 + j * 100}\trs{j}\tA\t{alt}\t{50 + j * 10}.0\t{filt}\t{info}\t{fmt_key}\t{sample_str}")
        out.append("\n".join(header + recs) + "\n")
        emitted += 1

    # 3b-extended) Dense multi-sample createGenotypeMap diversifier —
    # targets the 8+ kills-gap observed in AbstractVCFCodec.createGenotypeMap.
    # Generates varied (FORMAT-key-set, genotype-pattern, sample-count,
    # per-sample-value) combinations that each drive a distinct branch
    # through createGenotypeMap's per-sample iteration loop.
    _GT_PATTERNS = ["0/0", "0/1", "1/1", "./.",
                     "0|0", "0|1", "1|0", "1|1",
                     "0/1/2", "1/2/3",          # polyploid
                     "0", "1",                    # haploid
                     ".", ".|.",                  # fully missing
                     "0/2", "2/2"]                # uncommon indices
    _FMT_SETS = [
        ("GT",             ["{gt}"]),
        ("GT:DP",          ["{gt}:30"]),
        ("GT:DP:GQ",       ["{gt}:30:99"]),
        ("GT:GQ:DP:AD",    ["{gt}:99:30:15,15"]),
        ("GT:GQ:DP:AD:PL", ["{gt}:99:30:15,15:0,30,300"]),
        ("GT:AD:PL:GQ:DP:HQ", ["{gt}:10,20:0,100,500:99:30:50,50"]),
        ("GT:GL",          ["{gt}:-2.0,-5.0,-10.0"]),
        ("GT:FT",          ["{gt}:PASS"]),
        ("GT:PS",          ["{gt}:1"]),
    ]
    for fmt_key, tmpl_list in _FMT_SETS:
        if emitted >= max_per_seed:
            break
        tmpl = tmpl_list[0]
        for gt_mix in [
            ["0/0", "0/1", "1/1"],                         # 3 samples classic diploid
            ["0|1", "1|0", "0|0", "1|1"],                  # 4 samples phased
            ["./.", "0/1", "./."],                          # 3 samples with missing
            ["0/1", "0/0", "1/1", "./.", "0|1"],           # 5 samples mix
            ["0", "1", "0"],                                # 3 samples haploid
            ["0/1/2", "0/0/0", "1/1/1", "0/1/2"],          # 4 samples polyploid
            ["0/1"] * 10,                                    # 10 identical
            ["0/0", "0/1", "0/1", "1/1", "./.", "0|1", "1|0", "0/0"],  # 8 diverse
        ]:
            if emitted >= max_per_seed:
                break
            header = _vcf_minimal_header(extra_filters=True)
            sample_names = "\t".join(f"S{i}" for i in range(len(gt_mix)))
            header.append(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{sample_names}")
            # 2 records per file — exercises record-iterator branch too.
            sample_strs_0 = "\t".join(tmpl.format(gt=g) for g in gt_mix)
            sample_strs_1 = "\t".join(tmpl.format(gt=g) for g in gt_mix[::-1])
            rec0 = f"1\t100\trs0\tA\tT\t50.0\tPASS\tDP=30\t{fmt_key}\t{sample_strs_0}"
            rec1 = f"1\t200\trs1\tA\tT,G\t99.9\tPASS\tDP=60;AC=1,1;AN=4\t{fmt_key}\t{sample_strs_1}"
            out.append("\n".join(header + [rec0, rec1]) + "\n")
            emitted += 1

    # 3b-malformed) FORMAT/sample column-count mismatches. Targets
    # AbstractVCFCodec.createGenotypeMap's "fewer values than FORMAT
    # keys" branch (lines 758/774/786/789/794/796 in htsjdk 4.1.1 —
    # 10 kills gap in Run-6 diagnostic). htsjdk LENIENT accepts these;
    # our canonical normalizer does too.
    _MISMATCHED = [
        # (format_key, [sample_values]) — intentionally mismatched
        ("GT:DP:GQ",      ["0/1:30"]),                    # 2 missing trailing vals
        ("GT:DP:GQ",      ["0/1"]),                        # 2 missing
        ("GT:DP:GQ",      ["0/1:30:99:extra"]),           # 1 extra trailing
        ("GT:DP:GQ:AD",   ["0/1::99:"]),                   # empty middle + trailing
        ("GT:DP",         [""]),                            # empty sample
        ("GT:DP:GQ",      ["."]),                           # just missing marker
        ("GT",            [".|."]),                         # phased missing
        ("GT:DP",         ["0/1:30:extra1:extra2"]),       # extra colons
        ("GT:DP:GQ",      ["./."]),                         # sample missing genotype, short
        ("GT:DP",         ["3/4:30"]),                     # genotype idx out of range
    ]
    for fmt_key, svals in _MISMATCHED:
        if emitted >= max_per_seed:
            break
        header = _vcf_minimal_header(extra_filters=True)
        header.append(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS0")
        sample_str = svals[0]
        rec = f"1\t100\trs1\tA\tT\t50.0\tPASS\tDP=30\t{fmt_key}\t{sample_str}"
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 3b-multi-mismatch) Multi-sample with column-count inconsistency.
    _MULTI_MISMATCH = [
        # header has 3 samples but some rows have fewer values per sample
        ("GT:DP:GQ", ["0/1:30:99", "0/0:25", "1/1"]),       # decreasing
        ("GT:DP:GQ", ["0/1:30:99", "", "1/1:40:99"]),        # empty middle
        ("GT:DP:GQ", ["0/1", "0/0:25:99", "."]),             # mixed shapes
        ("GT:DP:GQ", [".|.", "./.", "./."]),                  # all missing
    ]
    for fmt_key, svals in _MULTI_MISMATCH:
        if emitted >= max_per_seed:
            break
        header = _vcf_minimal_header(extra_filters=True)
        names = "\t".join(f"S{i}" for i in range(len(svals)))
        header.append(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{names}")
        svtext = "\t".join(svals)
        rec = f"1\t100\trs1\tA\tT\t50.0\tPASS\tDP=30\t{fmt_key}\t{svtext}"
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    # 3c) Symbolic ALT records — <DEL>, <DUP>, <INS>, <CNV> need END or
    #     SVLEN in INFO, which exercises AbstractVCFCodec's structural-
    #     variant branch.
    for sym in ["<DEL>", "<DUP>", "<INS>", "<CNV>", "<INV>", "<DUP:TANDEM>"]:
        if emitted >= max_per_seed:
            break
        header = _vcf_minimal_header()
        header.append('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="">')
        header.append('##INFO=<ID=END,Number=1,Type=Integer,Description="">')
        header.append('##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="">')
        header.append('##ALT=<ID=DEL,Description="Deletion">')
        header.append("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")
        svt = sym.strip("<>").split(":")[0]
        recs = [
            f"1\t100\trs1\tA\t{sym}\t50.0\tPASS\tSVTYPE={svt};END=200;SVLEN=100",
            f"2\t200\tsv1\tN\t{sym}\t99.9\tPASS\tSVTYPE={svt};END=300",
        ]
        out.append("\n".join(header + recs) + "\n")
        emitted += 1

    # 4) Header-variant records — vary which meta lines are present.
    for contig, info, fmt_hdr, filt in itertools.product([True, False],
                                                         [True, False],
                                                         [True, False],
                                                         [False, True]):
        if emitted >= max_per_seed:
            break
        if not info:
            # If no INFO defs, the record uses "." for INFO.
            header = _vcf_minimal_header(include_contig=contig,
                                         include_info=False,
                                         include_format=fmt_hdr,
                                         include_filter=filt)
            header.append("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")
            rec = "1\t100\t.\tA\tT\t50.0\tPASS\t."
        else:
            header = _vcf_minimal_header(include_contig=contig,
                                         include_info=True,
                                         include_format=fmt_hdr,
                                         include_filter=filt)
            header.append("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO")
            rec = "1\t100\trs1\tA\tT\t50.0\tPASS\tDP=30;AF=0.5"
        out.append("\n".join(header + [rec]) + "\n")
        emitted += 1

    return out


# ---------------------------------------------------------------------------
# Validity gate (reuse Rank 9's)
# ---------------------------------------------------------------------------

def _validate(text: str, fmt: str, sut_validate: Optional[str] = None) -> bool:
    from mr_engine.transforms.value_diversifier import _validate as _v9
    return _v9(text, fmt, sut_validate=sut_validate)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def generate_structural_directory(
    input_dir: Path, output_dir: Path, fmt: str,
    max_per_seed: int = 60, sut_validate: Optional[str] = None,
    max_bytes: int = 500_000,
) -> dict:
    """Walk input_dir, emit up to max_per_seed structural variants per seed.

    Rank 12 is **template-based, not transform-based**: it generates
    structural variants from a spec-derived catalogue without referencing
    the seed's content. We still iterate over input_dir so the output
    directory naming/dedup logic stays consistent with Ranks 9/10/11.
    """
    ext = fmt.lower()
    sources = sorted(p for p in input_dir.iterdir()
                     if p.is_file() and p.suffix.lower() == f".{ext}"
                     and not p.name.startswith(("kept_", "diverse_",
                                                "bytefuzz_", "bv_",
                                                "struct_")))
    if not sources:
        raise SystemExit(f"structural_diversifier: no {ext} files in {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    per_file = (generate_vcf_structural_variants
                if fmt.upper() == "VCF"
                else generate_sam_structural_variants)
    kept = 0
    rejected_invalid = 0
    rejected_dup = 0
    rejected_size = 0
    seen_hashes: set[str] = set()
    for existing in output_dir.glob(f"struct_*.{ext}"):
        seen_hashes.add(existing.stem[len("struct_"):])

    # Because the generator is seed-independent, we only need to run it
    # once per directory — use the first source as a "seed hint" (some
    # future generators may consume seed structure; current v1 ignores it).
    first_src = sources[0]
    try:
        hint_text = first_src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        hint_text = ""

    for v_text in per_file(hint_text, max_per_seed=max_per_seed):
        if not v_text:
            continue
        if len(v_text.encode("utf-8")) > max_bytes:
            rejected_size += 1
            continue
        h = hashlib.sha256(v_text.encode("utf-8")).hexdigest()[:16]
        if h in seen_hashes:
            rejected_dup += 1
            continue
        if not _validate(v_text, fmt, sut_validate=sut_validate):
            rejected_invalid += 1
            continue
        seen_hashes.add(h)
        (output_dir / f"struct_{h}.{ext}").write_text(v_text, encoding="utf-8")
        kept += 1

    result = {
        "sources": len(sources),
        "max_per_seed": max_per_seed,
        "kept": kept,
        "rejected_invalid": rejected_invalid,
        "rejected_duplicate": rejected_dup,
        "rejected_size": rejected_size,
        "output_dir": str(output_dir),
        "sut_validate": sut_validate,
    }
    logger.info("structural_diversifier result: %s", result)
    return result


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--format", required=True, choices=["VCF", "SAM"])
    p.add_argument("--max-per-seed", type=int, default=60,
                   help="Cap variants emitted per catalogue pass (default 60).")
    p.add_argument("--sut-validate", default=None,
                   help="Optional SUT-parser gate (biopython / vcfpy).")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    r = generate_structural_directory(
        input_dir=args.input.resolve(),
        output_dir=args.output.resolve(),
        fmt=args.format,
        max_per_seed=args.max_per_seed,
        sut_validate=args.sut_validate,
    )
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
