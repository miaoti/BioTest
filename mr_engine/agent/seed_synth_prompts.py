"""
Prompt templates for LLM-driven seed synthesis (Rank 1 coverage lever).

The synthesizer feeds the same blindspot ticket that drives MR mining (uncovered
source-code slices + top-K spec-rule chunks) to a second LLM call and asks for
raw VCF/SAM files that exercise those uncovered code paths. Output is parsed as
N triple-fenced code blocks per the template contract below.

Grounded in:
  - SeedMind (arXiv:2411.18143) — LLM feedback-driven seed generator
  - SeedAIchemy (arXiv:2511.12448) — LLM-authored corpus curation
  - TitanFuzz (ISSTA 2023), Fuzz4All (ICSE 2024) — LLM-driven fuzzer seeds
"""

from __future__ import annotations


# Shared tail for both formats — explains the output contract identically.
# Build via plain f-strings at call time so `{` characters in the
# blindspot_context (Java/C++ code slices with `{`) are never interpreted
# as format placeholders.


def _render_output_contract(n: int, fmt: str, lang: str, max_bytes: int) -> str:
    return (
        "OUTPUT CONTRACT:\n"
        f"- Produce exactly {n} complete {fmt} files, nothing else.\n"
        f"- Each file in its own triple-fenced block: ```{lang}\\n<file>\\n```\n"
        f"- NO prose between blocks. NO commentary before the first block or "
        f"after the last. If you cannot produce {n} useful files, produce fewer "
        "— but every file you emit must be complete and non-trivial.\n"
        f"- Each file MUST be ≤ {max_bytes:,} bytes. Do NOT pad with filler "
        "records or large genotype matrices unless essential.\n"
        "- Each file MUST structurally parse (valid header, tab-separated columns, "
        "correct column counts). Our framework will discard any file that fails "
        "the structural-parse gate.\n"
        "- Prefer realism: use chromosomes that look biological (chr1, chr2, "
        "chrX) and PHRED-plausible QUAL/MAPQ values. But correctness first, "
        "realism second.\n"
    )


def build_vcf_prompt(
    blindspot_context: str,
    n: int = 5,
    max_bytes: int = 500 * 1024,
) -> str:
    """Build the VCF seed-synthesis prompt.

    `blindspot_context` is the same text produced by
    `BlindspotTicket.to_prompt_fragment()` and passed to MR mining —
    contains the Top-K uncovered spec rules and the "UNCOVERED CODE"
    block with source-code slices. The slices may contain `{` (Java/C++
    source), so we avoid `str.format()` entirely and concatenate.

    The prompt leans HARD on feature diversity (symbolic alleles,
    structural variants, multi-allelic + Number=A/R/G, gVCF blocks, CSQ,
    edge missing values, …) because empirical run-2 showed the default
    LLM output gravitates toward standard biallelic SNVs on chr1, which
    hit already-covered code paths. The under-covered branches live in
    the less-common features the prompt now explicitly enumerates.
    """
    return (
        "You are a senior test engineer generating VCF 4.3-compliant test "
        "inputs for a metamorphic + differential testing framework. Your "
        "goal: produce minimal VCF files that exercise SPECIFIC uncovered "
        "code paths in a bioinformatics parser — NOT typical happy-path "
        "VCFs.\n\n"
        "IMPORTANT — avoid the default. The corpus already has dozens of "
        "standard biallelic SNV records on chr1–chrX. Producing another "
        "`chr1\\t100\\t.\\tA\\tT\\t30\\tPASS\\t…` file will add ZERO new "
        "coverage. Your seeds MUST target UNDERUSED VCF features.\n\n"
        "UNDER-COVERED FEATURE PALETTE (pick 1–2 per file, mix and "
        "match across the batch):\n"
        "  a. **Symbolic alleles**: `ALT=<DEL>`, `<DUP>`, `<INS>`, `<INV>`, "
        "`<CNV>`, `<NON_REF>` (gVCF), spanning deletion `*`, or "
        "`<*>` symbolic reference block.\n"
        "  b. **Structural-variant INFO**: `SVTYPE=`, `SVLEN=`, `END=`, "
        "`CIPOS=`, `CIEND=`, `IMPRECISE`, `MATEID=`.\n"
        "  c. **Breakpoint notation (BND)**: `ALT=N[chr2:12345[` or "
        "`]chr2:12345]N` or `[chr2:12345[N` or `N]chr2:12345]` paired "
        "with `MATEID=` to the mate record.\n"
        "  d. **Multi-allelic with Number=A/R/G arrays**: `ALT=A,C,G` with "
        "3 comma-values for each `Number=A` INFO field, 4 for Number=R "
        "(REF + 3 ALTs), and properly-sized Number=G arrays.\n"
        "  e. **gVCF reference blocks**: `<NON_REF>` as the only ALT, with "
        "`END=` marking block size; GVCFBlock bands in FORMAT.\n"
        "  f. **Complex FORMAT**: phased `0|1` GT with `PS:PGT:PID` fields, "
        "triploid/polyploid (`0/1/2`), haploid (`1`), missing allele "
        "`./.` or `.|.`.\n"
        "  g. **Edge INFO types**: Flag types without `=value`, Character "
        "type (`Type=Character`), quoted-string values containing commas "
        "and semicolons, trailing-colon FORMAT.\n"
        "  h. **Coordinate edges**: POS=1, very large POS (> 2³¹), large "
        "multi-base REF/ALT indels (>100 bp each).\n"
        "  i. **Missing-value corners**: QUAL=`.`, FILTER=`.`, INFO=`.`, "
        "INFO containing `KEY=.` for explicit missing.\n"
        "  j. **CSQ/ANN multi-transcript**: multiple comma-separated "
        "transcript records, each with pipe-delimited sub-fields.\n"
        "  k. **Large header**: many `##contig=<ID=…>` lines, `##ALT=<ID=…,"
        "Description=…>` declarations, `##META=`, `##SAMPLE=` pedigree.\n\n"
        "=== BLINDSPOT REPORT (source lines not yet hit) ===\n"
        + blindspot_context
        + "\n=== END BLINDSPOT REPORT ===\n\n"
        "REQUIREMENTS FOR EACH VCF FILE:\n"
        "- Start with `##fileformat=VCFv4.3` (or v4.2/v4.5 only if the "
        "uncovered code specifically targets that version).\n"
        "- Declare every INFO / FORMAT / FILTER / ALT / contig key you "
        "reference in a proper `##…=<…>` meta-line.\n"
        "- Include the `#CHROM POS ID REF ALT QUAL FILTER INFO [FORMAT "
        "SAMPLE1 …]` header row.\n"
        "- Each file should focus on ONE feature from the palette above. "
        "If you pick `<DEL>`, don't mix it with gVCF blocks — do the "
        "gVCF block in a DIFFERENT file.\n"
        "- Include at least 1 data record that actually exercises the "
        "chosen feature. No filler records.\n"
        "- Use TAB characters as column separators, NOT multiple spaces.\n\n"
        + _render_output_contract(n=n, fmt="VCF", lang="vcf", max_bytes=max_bytes)
    )


def build_sam_prompt(
    blindspot_context: str,
    n: int = 5,
    max_bytes: int = 500 * 1024,
) -> str:
    """Build the SAM seed-synthesis prompt.

    Same structure as `build_vcf_prompt` — lean on underused SAM features
    rather than produce another typical `10M` aligned read."""
    return (
        "You are a senior test engineer generating SAM 1.6-compliant test "
        "inputs for a metamorphic + differential testing framework. Your "
        "goal: produce minimal SAM files that exercise SPECIFIC uncovered "
        "code paths in a bioinformatics parser — NOT typical aligned "
        "reads.\n\n"
        "IMPORTANT — avoid the default. The corpus already has dozens of "
        "standard `10M` / `50M` alignments with PASS QUAL. Your seeds MUST "
        "target UNDERUSED SAM features.\n\n"
        "UNDER-COVERED FEATURE PALETTE (pick 1–2 per file, mix and match):\n"
        "  a. **Complex CIGAR**: `5H10S30M5I20M3D10M2P5M5N5M2H` (hard clip, "
        "soft clip, insertion, deletion, padding, skipped ref, more hard "
        "clip); `=` and `X` instead of `M`.\n"
        "  b. **Unmapped pairs**: FLAG with unmap/mate-unmap bits set, "
        "SEQ=`*`, QUAL=`*`, CIGAR=`*`, POS=0 (written as `0` meaning "
        "unmapped).\n"
        "  c. **Supplementary / secondary**: FLAG bits 0x100 (secondary), "
        "0x800 (supplementary), `SA:Z:…` chimeric-alignment tag.\n"
        "  d. **Duplicate / QC-fail**: FLAG bits 0x400 (duplicate), 0x200 "
        "(QC fail).\n"
        "  e. **Long reads**: CIGAR with ≥ 30 operators, SEQ ≥ 500 bp.\n"
        "  f. **Cross-chromosome mate**: RNEXT is a different contig, "
        "PNEXT non-zero.\n"
        "  g. **Rich optional tags**: every type code represented — "
        "`AS:i:`, `XS:i:`, `MD:Z:` with complex insert/deletion string, "
        "`NM:i:`, `NH:i:`, `RG:Z:`, `PG:Z:`, `MC:Z:`, `MQ:i:`, `B` arrays "
        "(`XA:B:c,-1,2,-3`), hex `H:Z:` values, per-base `OQ:Z:` of "
        "len(SEQ).\n"
        "  h. **Edge QUAL**: very low (`!`), very high, SEQ=`*` with "
        "QUAL=`*`.\n"
        "  i. **Header corners**: multi-`@SQ` with M5 / UR / SP / AS "
        "fields, `@RG` with PL:ILLUMINA / ONT / PACBIO, `@PG` chain with "
        "`PP:` pointers, `@CO` freetext comments, duplicate @SQ names "
        "(should be rejected — Rank 3 MR), out-of-order HD line.\n"
        "  j. **Padding / splice**: CIGAR with `P` and `N` ops; `=`/`X` "
        "ops paired with REF differences.\n\n"
        "=== BLINDSPOT REPORT (source lines not yet hit) ===\n"
        + blindspot_context
        + "\n=== END BLINDSPOT REPORT ===\n\n"
        "REQUIREMENTS FOR EACH SAM FILE:\n"
        "- Start with `@HD\tVN:1.6` header line.\n"
        "- Include at least one `@SQ\tSN:…\tLN:…` for each reference "
        "sequence used in data rows.\n"
        "- If your records reference a read group, include the matching "
        "`@RG\tID:…` header.\n"
        "- Each file should focus on ONE feature from the palette above.\n"
        "- The 11 mandatory columns (QNAME FLAG RNAME POS MAPQ CIGAR "
        "RNEXT PNEXT TLEN SEQ QUAL) are TAB-separated.\n"
        "- CIGAR query-consuming ops (M, I, S, =, X) must sum to len(SEQ) "
        "unless CIGAR is `*`. SEQ and QUAL must be equal length if both "
        "non-`*`.\n\n"
        + _render_output_contract(n=n, fmt="SAM", lang="sam", max_bytes=max_bytes)
    )


def build_prompt(
    blindspot_context: str,
    fmt: str,
    n: int = 5,
    max_bytes: int = 500 * 1024,
) -> str:
    """Dispatch to the format-specific builder."""
    fmt_u = fmt.upper()
    if fmt_u == "VCF":
        return build_vcf_prompt(blindspot_context, n=n, max_bytes=max_bytes)
    if fmt_u == "SAM":
        return build_sam_prompt(blindspot_context, n=n, max_bytes=max_bytes)
    raise ValueError(f"Unsupported format for seed synthesis: {fmt}")


# ---------------------------------------------------------------------------
# SeedMind-style generator prompt (Phase 5 of SAM coverage plan).
#
# Instead of asking the LLM to produce raw SAM/VCF files, ask it for a
# Python generator program. The synthesizer runs that program K times
# with different seeds, validates each output, and keeps the survivors.
#
# Why generators beat raw files:
#   - A generator can parameterize edge-case axes (read length, CIGAR
#     complexity, tag count) — one prompt yields K distinct outputs.
#   - Invariants (SEQ/CIGAR-length coupling, FLAG/RNAME consistency) are
#     easier to encode once than to satisfy K times.
#   - SeedMind (arXiv:2411.18143) reports +29 % coverage vs prior LLM
#     fuzzers using this pattern.
# ---------------------------------------------------------------------------


_GENERATOR_OUTPUT_CONTRACT = """\
OUTPUT CONTRACT:
- Produce a SINGLE Python 3 module wrapped in a triple-fenced block: ```python\\n<code>\\n```.
- The module MUST define exactly one function with this signature:
      def generate(seed: int) -> str:
- `generate(seed)` must be deterministic given `seed`: calling it twice
  with the same seed returns the same string.
- The return value MUST be a complete {fmt} file as a single string
  (include trailing newlines).
- Allowed standard-library imports ONLY: random, string, itertools,
  struct, math, textwrap. NO network, NO file I/O, NO os / sys / subprocess,
  NO multiprocessing, NO importlib. No third-party packages.
- The generator must handle `seed` values 0..10^9 without raising.
- Each returned file MUST be <= {max_bytes:,} bytes.
- NO prose before or after the fenced block.
"""


def build_generator_prompt(
    blindspot_context: str,
    fmt: str,
    n: int = 5,
    max_bytes: int = 500 * 1024,
) -> str:
    """Build the SeedMind-style generator-program prompt for a format.

    The resulting prompt asks the LLM for a self-contained Python
    generator module. The synthesizer then executes it K times with
    distinct seeds to get K distinct outputs.
    """
    fmt_u = fmt.upper()
    if fmt_u not in ("VCF", "SAM"):
        raise ValueError(f"Unsupported format for seed synthesis: {fmt}")

    format_brief = (
        "VCFv4.3 / v4.2 / v4.5 text format, with ##fileformat header, "
        "##INFO/##FORMAT/##FILTER meta lines, a `#CHROM POS ID REF ALT "
        "QUAL FILTER INFO [FORMAT SAMPLES]` line, and tab-separated "
        "data records."
        if fmt_u == "VCF"
        else
        "SAM 1.6 text format: @HD (VN:1.6), at least one @SQ (SN/LN), "
        "optional @RG/@PG/@CO, then tab-separated alignment records "
        "with 11 mandatory columns (QNAME FLAG RNAME POS MAPQ CIGAR "
        "RNEXT PNEXT TLEN SEQ QUAL)."
    )
    header_brief = (
        "Return a string starting with `##fileformat=VCFv4.3`."
        if fmt_u == "VCF"
        else
        "Return a string starting with `@HD\\tVN:1.6`."
    )

    return (
        "You are writing a Python generator program for a metamorphic "
        "+ differential fuzz-test framework for bioinformatics parsers. "
        "The framework will invoke your generator multiple times with "
        "different integer seeds; each call must return a parseable "
        f"{fmt_u} file as a string.\n\n"
        f"Format brief: {format_brief}\n\n"
        "TASK. Author ONE Python module with a `generate(seed: int) -> "
        "str` function whose output exercises the UNDERCOVERED code "
        "paths listed below. The generator must use `random.Random(seed)` "
        "so the output is reproducible given a seed. Parameterize the "
        "following axes via `rng`:\n"
        f"  - {'number of data records' if fmt_u == 'VCF' else 'number of alignment records'} (1..20)\n"
        "  - record/alignment field values drawn from plausible ranges\n"
        "  - presence/absence of under-covered features (see blindspot "
        "report below)\n"
        "  - CIGAR complexity (SAM) or ALT complexity (VCF)\n\n"
        f"{header_brief}\n\n"
        "=== BLINDSPOT REPORT (source lines not yet hit) ===\n"
        + blindspot_context
        + "\n=== END BLINDSPOT REPORT ===\n\n"
        "INVARIANTS TO RESPECT (enforce programmatically):\n"
        + (
            "- REF and ALT are non-empty, ALT may be comma-separated.\n"
            "- #CHROM is a string matching declared ##contig IDs (if you declare any).\n"
            "- POS is a positive integer.\n"
            "- QUAL is either `.` or a non-negative float.\n"
            if fmt_u == "VCF"
            else
            "- sum(query-consuming CIGAR ops in {M,I,S,=,X}) == len(SEQ) unless CIGAR=='*'.\n"
            "- len(SEQ) == len(QUAL) unless either is '*'.\n"
            "- FLAG 0x4 (unmapped) iff RNAME=='*' and POS==0 (or vice versa).\n"
            "- Optional tag TYPE is one of AifZHB.\n"
        )
        + "\n"
        + _GENERATOR_OUTPUT_CONTRACT.format(fmt=fmt_u, max_bytes=max_bytes)
    )
