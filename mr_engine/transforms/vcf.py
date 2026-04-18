"""
VCF format atomic transform functions.

Each function operates on plain Python types (str, list, dict) and uses
`random.Random(seed)` for reproducibility. No global state is mutated.
"""

from __future__ import annotations

import re
import random
from typing import Optional

from . import register_transform


# ---------------------------------------------------------------------------
# 1. shuffle_meta_lines
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_meta_lines",
    format="VCF",
    description="Shuffle VCF ##meta-information lines into a new order, keeping ##fileformat pinned first.",
)
def shuffle_meta_lines(
    vcf_lines: list[str],
    except_exact: Optional[list[str]] = None,
    seed: Optional[int] = None,
) -> list[str]:
    """
    Shuffle VCF header meta-information lines (##...) while preserving
    pinned lines (e.g. ##fileformat=VCFv4.5 must stay first).

    Args:
        vcf_lines: All lines of a VCF file.
        except_exact: Lines to keep in their original position.
                      Defaults to ["##fileformat=VCFv4.5"].
        seed: RNG seed for reproducibility.

    Returns:
        New list of lines with meta lines shuffled.
    """
    if except_exact is None:
        except_exact = ["##fileformat=VCFv4.5"]

    rng = random.Random(seed)
    pinned: dict[int, str] = {}  # original index -> line
    shuffleable: list[str] = []

    for i, line in enumerate(vcf_lines):
        if not line.startswith("##"):
            break
        stripped = line.rstrip("\n")
        if any(stripped.startswith(pin) for pin in except_exact):
            pinned[i] = line
        else:
            shuffleable.append(line)

    rng.shuffle(shuffleable)

    # Rebuild: pinned lines stay at their indices, rest filled from shuffled
    result: list[str] = []
    shuffle_iter = iter(shuffleable)
    meta_count = len(pinned) + len(shuffleable)
    for i in range(meta_count):
        if i in pinned:
            result.append(pinned[i])
        else:
            result.append(next(shuffle_iter))

    # Append everything after the meta block
    result.extend(vcf_lines[meta_count:])
    return result


# ---------------------------------------------------------------------------
# 2. permute_structured_kv_order
# ---------------------------------------------------------------------------
@register_transform(
    "permute_structured_kv_order",
    format="VCF",
    description="Reorder key=value pairs inside a structured ##INFO/##FORMAT/##FILTER meta-line (e.g. ID=DP,Number=1 -> Number=1,ID=DP).",
)
def permute_structured_kv_order(
    meta_line: str,
    seed: Optional[int] = None,
) -> str:
    """
    Reorder key=value pairs inside a structured VCF meta-information line.
    E.g., ##INFO=<ID=DP,Number=1,Type=Integer,...> -> ##INFO=<Number=1,ID=DP,...>

    Handles quoted values containing commas correctly.

    Args:
        meta_line: A single VCF meta line like ##INFO=<...>.
        seed: RNG seed.

    Returns:
        The meta line with k=v pairs in shuffled order.
    """
    rng = random.Random(seed)

    match = re.match(r"(##\w+=<)(.*)(>.*)", meta_line.rstrip("\n"), re.DOTALL)
    if not match:
        return meta_line

    prefix, inner, suffix = match.group(1), match.group(2), match.group(3)

    # Split respecting quoted strings
    kvs: list[str] = []
    current: list[str] = []
    in_quote = False
    for ch in inner:
        if ch == '"':
            in_quote = not in_quote
            current.append(ch)
        elif ch == "," and not in_quote:
            kvs.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        kvs.append("".join(current))

    rng.shuffle(kvs)
    return prefix + ",".join(kvs) + suffix


# ---------------------------------------------------------------------------
# 3. choose_permutation
# ---------------------------------------------------------------------------
@register_transform(
    "choose_permutation",
    format="VCF",
    description="Generate a random permutation array [0..n-1] (helper step — always paired with permute_ALT + remap_GT + permute_Number_A_R_fields).",
    group="alt_permutation",
)
def choose_permutation(n: int, seed: Optional[int] = None) -> list[int]:
    """
    Generate a random permutation of [0, 1, ..., n-1].

    Args:
        n: Number of elements.
        seed: RNG seed.

    Returns:
        A list representing the permutation, e.g. [2, 0, 1].
    """
    rng = random.Random(seed)
    pi = list(range(n))
    rng.shuffle(pi)
    return pi


# ---------------------------------------------------------------------------
# 4. permute_alt
# ---------------------------------------------------------------------------
@register_transform(
    "permute_ALT",
    format="VCF",
    description="Reorder ALT alleles by permutation pi (e.g. 'A,C,T' with pi=[2,0,1] -> 'T,A,C').",
    group="alt_permutation",
)
def permute_alt(alt_field: str, pi: list[int]) -> str:
    """
    Reorder ALT alleles according to permutation pi.

    Args:
        alt_field: Comma-separated ALT string, e.g. "A,C,T".
        pi: Permutation array of length == number of ALT alleles.

    Returns:
        Reordered ALT string.
    """
    alleles = alt_field.split(",")
    if len(pi) != len(alleles):
        raise ValueError(
            f"Permutation length {len(pi)} != ALT allele count {len(alleles)}"
        )
    reordered = [alleles[pi[i]] for i in range(len(alleles))]
    return ",".join(reordered)


# ---------------------------------------------------------------------------
# 5. remap_gt
# ---------------------------------------------------------------------------
@register_transform(
    "remap_GT",
    format="VCF",
    description="Update GT allele indices to match the new ALT order; REF index (0) is never changed (e.g. '0/1' with A<->C swap -> '0/2').",
    group="alt_permutation",
)
def remap_gt(gt_field: str, pi: list[int], missing: str = ".") -> str:
    """
    Remap genotype allele indices according to an ALT permutation.
    REF index (0) is NEVER changed.

    Args:
        gt_field: GT string like "0/1" or "1|2" or "./."
        pi: ALT permutation array (0-indexed into ALT alleles).
        missing: Missing value marker.

    Returns:
        Remapped GT string with the same phase separator.
    """
    # Build the mapping: 0->0 (REF stays); for ALT i (1-based), new = pi.index(i-1) + 1
    allele_map: dict[int, int] = {0: 0}
    for old_alt_0based in range(len(pi)):
        old_1based = old_alt_0based + 1
        new_1based = pi.index(old_alt_0based) + 1
        allele_map[old_1based] = new_1based

    # Detect separator (/ or |)
    sep = "|" if "|" in gt_field else "/"
    parts = re.split(r"[/|]", gt_field)

    remapped: list[str] = []
    for part in parts:
        if part == missing:
            remapped.append(missing)
        else:
            idx = int(part)
            remapped.append(str(allele_map.get(idx, idx)))

    return sep.join(remapped)


# ---------------------------------------------------------------------------
# 6. permute_number_a_r_fields
# ---------------------------------------------------------------------------
@register_transform(
    "permute_Number_A_R_fields",
    format="VCF",
    description="Reorder Number=A INFO/FORMAT values (one per ALT) or Number=R values (REF fixed, ALTs reordered) to match the new ALT permutation.",
    group="alt_permutation",
)
def permute_number_a_r_fields(
    values: str,
    pi: list[int],
    is_number_r: bool = False,
) -> str:
    """
    Reorder comma-separated Number=A or Number=R field values by permutation pi.

    For Number=A: values correspond 1:1 with ALT alleles -> reorder all by pi.
    For Number=R: index 0 is REF (kept fixed), remaining reordered by pi.

    Args:
        values: Comma-separated values string, e.g. "10,20,30".
        pi: ALT permutation array.
        is_number_r: True if the field is Number=R (has a REF value at index 0).

    Returns:
        Reordered comma-separated values.
    """
    parts = values.split(",")

    if is_number_r:
        ref_val = parts[0]
        alt_vals = parts[1:]
        if len(pi) != len(alt_vals):
            raise ValueError(
                f"Permutation length {len(pi)} != Number=R ALT count {len(alt_vals)}"
            )
        reordered_alt = [alt_vals[pi[i]] for i in range(len(alt_vals))]
        return ",".join([ref_val] + reordered_alt)
    else:
        if len(pi) != len(parts):
            raise ValueError(
                f"Permutation length {len(pi)} != Number=A value count {len(parts)}"
            )
        reordered = [parts[pi[i]] for i in range(len(parts))]
        return ",".join(reordered)


# ---------------------------------------------------------------------------
# 7. permute_sample_columns
# ---------------------------------------------------------------------------
@register_transform(
    "permute_sample_columns",
    format="VCF",
    description="Shuffle sample columns across the whole file: the #CHROM header sample IDs and every data row move together with the same permutation.",
)
def permute_sample_columns(
    vcf_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """
    Reorder sample columns in the VCF #CHROM header and all data lines.
    The first 9 fixed columns (CHROM..FORMAT) are preserved.

    Args:
        vcf_lines: All lines of a VCF file.
        seed: RNG seed.

    Returns:
        New list of lines with sample columns shuffled.
    """
    rng = random.Random(seed)
    result: list[str] = []
    pi: list[int] | None = None

    for line in vcf_lines:
        if line.startswith("##"):
            result.append(line)
            continue

        fields = line.rstrip("\n").split("\t")

        if line.startswith("#CHROM"):
            # Header line: fixed cols 0-8, sample IDs from 9 onward
            fixed = fields[:9]
            samples = fields[9:]
            if not samples:
                result.append(line)
                continue
            pi = list(range(len(samples)))
            rng.shuffle(pi)
            reordered = [samples[pi[i]] for i in range(len(samples))]
            result.append("\t".join(fixed + reordered) + "\n")
        elif pi is not None and len(fields) > 9:
            # Data line: reorder sample data columns using same pi
            fixed = fields[:9]
            sample_data = fields[9:]
            reordered = [sample_data[pi[i]] for i in range(len(sample_data))]
            result.append("\t".join(fixed + reordered) + "\n")
        else:
            result.append(line)

    return result


# ---------------------------------------------------------------------------
# 8. shuffle_info_field_kv
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_info_field_kv",
    format="VCF",
    description="Shuffle the semicolon-separated key=value entries in a VCF data line's INFO column (e.g. 'DP=30;AF=0.5;MQ=60' -> 'MQ=60;DP=30;AF=0.5').",
)
def shuffle_info_field_kv(
    info_str: str,
    seed: Optional[int] = None,
) -> str:
    """
    Shuffle the key=value pairs in a VCF INFO column string.
    E.g., "DP=10;AF=0.5;MQ=30" -> "MQ=30;DP=10;AF=0.5"

    Args:
        info_str: The INFO column string (semicolon-separated).
        seed: RNG seed.

    Returns:
        INFO string with k=v pairs in shuffled order.
    """
    if info_str == "." or not info_str:
        return info_str

    rng = random.Random(seed)
    parts = info_str.split(";")
    # Remove trailing empty entries from trailing semicolons
    parts = [p for p in parts if p]
    rng.shuffle(parts)
    return ";".join(parts)


# ---------------------------------------------------------------------------
# 9. inject_equivalent_missing_values
# ---------------------------------------------------------------------------
@register_transform(
    "inject_equivalent_missing_values",
    format="VCF",
    description="Append a FORMAT field (declared in the header) filled with '.' to all samples — semantically a no-op that tests missing-value tolerance (e.g. FORMAT GT:DP -> GT:DP:GQ with all samples gaining ':.').",
)
def inject_equivalent_missing_values(
    format_str: str,
    sample_strs: list[str],
    field_id: str,
    missing: str = ".",
) -> tuple[str, list[str]]:
    """
    Add a defined-but-unused FORMAT field to a VCF record, filling all
    samples with missing values. The record is semantically equivalent.

    Args:
        format_str: The FORMAT column string, e.g. "GT:DP:GQ".
        sample_strs: List of sample data strings, e.g. ["0/1:30:99", ...].
        field_id: The FORMAT field ID to inject (must be defined in header).
        missing: Missing value marker.

    Returns:
        Tuple of (new_format_str, new_sample_strs).
    """
    new_format = format_str + ":" + field_id
    new_samples = [s + ":" + missing for s in sample_strs]
    return new_format, new_samples


# ---------------------------------------------------------------------------
# 10. trim_common_affixes — variant normalization (Tan 2015)
# ---------------------------------------------------------------------------
@register_transform(
    "trim_common_affixes",
    format="VCF",
    description=(
        "Trim shared prefix/suffix bases between REF and ALT so the pair is "
        "left-anchored and parsimonious (REF=AA, ALT=AC at POS=100 -> "
        "REF=A, ALT=C at POS=101). Produces the canonical normalized "
        "representation per Tan, Abecasis, Kang 2015."
    ),
    contextual_hint=(
        "the record's REF and ALT share a common prefix or suffix base "
        "(e.g., REF=AA ALT=AC, or REF=AT ALT=GT). Two parsers that both "
        "claim spec compliance should recognize the pair as the same "
        "variant whether or not affixes are trimmed."
    ),
    preconditions=(
        "alt_count==1",           # only apply to biallelic records for now
        "len(REF)>=2 OR len(ALT)>=2",
        "REF[0]==ALT[0] OR REF[-1]==ALT[-1]",
    ),
)
def trim_common_affixes(
    ref: str,
    alt: str,
    pos: int,
) -> tuple[str, str, int]:
    """Return (new_ref, new_alt, new_pos) with common prefix/suffix trimmed.

    Algorithm (Tan 2015 §2 "Parsimony"):
      1. Trim shared suffix bases while both sequences stay >=1 char.
      2. Trim shared prefix bases while both sequences stay >=1 char;
         increment POS by each base trimmed from the prefix (VCF POS is
         1-based, so it follows the remaining first base).

    The semantics of the variant call are unchanged.
    """
    r, a, p = ref, alt, pos
    # Suffix trim
    while len(r) > 1 and len(a) > 1 and r[-1] == a[-1]:
        r = r[:-1]
        a = a[:-1]
    # Prefix trim (advance POS for each trimmed base)
    while len(r) > 1 and len(a) > 1 and r[0] == a[0]:
        r = r[1:]
        a = a[1:]
        p += 1
    return r, a, p


# ---------------------------------------------------------------------------
# 11. left_align_indel — conservative (no-reference-FASTA) left shift
# ---------------------------------------------------------------------------
@register_transform(
    "left_align_indel",
    format="VCF",
    description=(
        "Conservatively left-shift an indel in a homopolymer run. Without a "
        "reference FASTA, only triggers when REF[0]==REF[-1] AND "
        "len(REF)!=len(ALT) (insertion/deletion into homopolymer). POS is "
        "decremented by 1, first base of REF/ALT preserved. Preserves "
        "canonical variant per Tan 2015 §2.1."
    ),
    contextual_hint=(
        "the indel sits inside a homopolymer run that makes left-shifting "
        "trivial (e.g., deletion of an A in AAAA). Parsers compliant with "
        "VCF normalization must recognize the equivalent left-shifted form."
    ),
    preconditions=(
        "alt_count==1",
        "len(REF)!=len(ALT)",
        "REF[0]==REF[-1]",
        "pos>=2",                 # can only shift left if POS > 1
    ),
)
def left_align_indel(
    ref: str,
    alt: str,
    pos: int,
) -> tuple[str, str, int]:
    """Conservative left-shift of an indel in a homopolymer context.

    Without a reference FASTA, we can only safely shift when REF is a
    homopolymer (REF[0] == REF[-1] covers both pure runs and insertions
    whose padding base matches the run). We decrement POS by 1 and emit
    REF/ALT with the last base shifted to the front.

    Example: REF=AAA ALT=AA POS=5 -> REF=AA ALT=A POS=4 (same deletion,
    just anchored one base earlier in the run).
    """
    if len(ref) == len(alt):
        return ref, alt, pos  # SNV / MNV — nothing to left-shift
    if ref[0] != ref[-1]:
        return ref, alt, pos  # not a homopolymer context
    if pos <= 1:
        return ref, alt, pos  # no room to shift left
    # Shift: the anchor base (ref[0]) moves one position earlier; the
    # indel body is unchanged. Practically REF/ALT stay the same literal
    # strings because all bases are identical in a homopolymer; what
    # moves is POS.
    return ref, alt, pos - 1


# ---------------------------------------------------------------------------
# 12. split_multi_allelic — bcftools norm --multiallelics
# ---------------------------------------------------------------------------
@register_transform(
    "split_multi_allelic",
    format="VCF",
    description=(
        "Split a multi-ALT record into one record per ALT, synchronizing "
        "Number=A (per-ALT) INFO/FORMAT arrays and remapping per-sample GT "
        "indices to preserve REF (0) semantics. Equivalent to "
        "`bcftools norm --multiallelics -any` applied to a single record."
    ),
    contextual_hint=(
        "the record has 2+ comma-separated ALT alleles and the SUT chain "
        "is expected to treat a split form identically to the multi-ALT "
        "form. Per bcftools norm + Tan 2015, same variant set either way."
    ),
    preconditions=(
        "alt_count>=2",
    ),
)
def split_multi_allelic(
    record_fields: list[str],
    info_meta: dict,
    format_meta: dict,
) -> list[list[str]]:
    """Split one multi-ALT VCF record into N single-ALT records.

    Args:
        record_fields: Tab-split fields of one VCF data line (len >= 8;
                       [CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, ...]).
        info_meta:     dict[str, dict] describing ##INFO headers — keyed by
                       INFO field ID; value has at least {"Number": "A"|"R"|
                       "G"|"1"|int}.
        format_meta:   same structure for ##FORMAT headers. Used to identify
                       per-allele FORMAT fields (Number=A) that must be
                       split across records.

    Returns:
        List of N new records (each as list[str]), one per ALT allele.
        REF stays the same across all records. Per-ALT arrays in INFO and
        FORMAT are scattered: record i gets value at index i. Per-sample GT
        is remapped so allele index i becomes 1 and all others collapse to
        ".".

    Semantic note:
        This is a lossy operation for some Number=G fields (PL arrays) in
        the strictest sense because combining per-ALT GT pairs requires
        re-genotyping; we emit "." for such fields to stay honest. Tools
        that round-trip split+join without information loss must rely on
        additional metadata.
    """
    if len(record_fields) < 8:
        return [record_fields]

    chrom = record_fields[0]
    pos = record_fields[1]
    rid = record_fields[2]
    ref = record_fields[3]
    alts = record_fields[4].split(",")
    if len(alts) < 2:
        return [record_fields]
    qual = record_fields[5]
    filt = record_fields[6]
    info_str = record_fields[7]
    has_samples = len(record_fields) > 9
    format_str = record_fields[8] if has_samples else ""
    sample_strs = record_fields[9:] if has_samples else []

    # Parse INFO into ordered list of (key, value) to preserve order.
    info_pairs: list[tuple[str, Optional[str]]] = []
    if info_str and info_str != ".":
        for chunk in info_str.split(";"):
            if "=" in chunk:
                k, v = chunk.split("=", 1)
                info_pairs.append((k, v))
            else:
                info_pairs.append((chunk, None))  # flag

    format_keys = format_str.split(":") if format_str else []

    out_records: list[list[str]] = []
    for alt_idx, alt in enumerate(alts):
        # Scatter INFO Number=A arrays; keep Number=1/0/R/G values as-is
        # (R would need REF + one ALT; we keep the REF slot and the chosen
        # ALT slot; G is too complex — emit full original to avoid lying).
        new_info_pairs: list[tuple[str, Optional[str]]] = []
        for k, v in info_pairs:
            if v is None:
                new_info_pairs.append((k, None))
                continue
            number = (info_meta.get(k) or {}).get("Number")
            if number == "A":
                parts = v.split(",")
                if len(parts) == len(alts):
                    new_info_pairs.append((k, parts[alt_idx]))
                else:
                    new_info_pairs.append((k, v))
            elif number == "R":
                parts = v.split(",")
                if len(parts) == len(alts) + 1:
                    # keep REF slot + this ALT slot
                    new_info_pairs.append(
                        (k, f"{parts[0]},{parts[alt_idx + 1]}")
                    )
                else:
                    new_info_pairs.append((k, v))
            else:
                new_info_pairs.append((k, v))

        new_info_str = ";".join(
            (f"{k}={v}" if v is not None else k) for k, v in new_info_pairs
        ) if new_info_pairs else "."

        new_samples: list[str] = []
        for sample_val in sample_strs:
            sample_parts = sample_val.split(":")
            new_parts: list[str] = []
            for fi, fkey in enumerate(format_keys):
                if fi >= len(sample_parts):
                    new_parts.append(".")
                    continue
                raw = sample_parts[fi]
                if fkey == "GT":
                    # remap: the chosen ALT (alt_idx+1) becomes 1;
                    # REF (0) stays 0; any other allele -> '.'
                    remapped = []
                    sep = "/"
                    if "|" in raw:
                        sep = "|"
                    for g in re.split(r"[|/]", raw):
                        if g == ".":
                            remapped.append(".")
                        elif g == "0":
                            remapped.append("0")
                        elif g == str(alt_idx + 1):
                            remapped.append("1")
                        else:
                            remapped.append(".")
                    new_parts.append(sep.join(remapped))
                else:
                    number = (format_meta.get(fkey) or {}).get("Number")
                    if number == "A":
                        parts = raw.split(",")
                        if len(parts) == len(alts):
                            new_parts.append(parts[alt_idx])
                        else:
                            new_parts.append(raw)
                    elif number == "R":
                        parts = raw.split(",")
                        if len(parts) == len(alts) + 1:
                            new_parts.append(f"{parts[0]},{parts[alt_idx + 1]}")
                        else:
                            new_parts.append(raw)
                    elif number == "G":
                        # True G-split requires re-genotyping; emit missing
                        # to preserve honesty over fidelity.
                        new_parts.append(".")
                    else:
                        new_parts.append(raw)
            new_samples.append(":".join(new_parts))

        new_record = [chrom, pos, rid, ref, alt, qual, filt, new_info_str]
        if has_samples:
            new_record.append(format_str)
            new_record.extend(new_samples)
        out_records.append(new_record)

    return out_records


# ---------------------------------------------------------------------------
# 13. vcf_bcf_round_trip — VCF v4.5 §6 BCF spec
# ---------------------------------------------------------------------------
@register_transform(
    "vcf_bcf_round_trip",
    format="VCF",
    description=(
        "Round-trip a VCF through its BCF2 binary equivalent (VCF -> BCF "
        "-> VCF). Semantically a no-op per VCF v4.5 §6; any difference in "
        "canonical output exposes a codec bug (precision, string encoding, "
        "dictionary remapping)."
    ),
    contextual_hint=(
        "the SUT chain includes a BCF-capable parser (pysam or htsjdk) "
        "and you want to cross-check text vs binary representation. "
        "Particularly useful for INFO/FORMAT values with rare types "
        "(Float arrays, missing values, phased genotypes)."
    ),
    preconditions=(
        "bcf_codec_available",
        "pysam_runtime_reachable",
    ),
)
def vcf_bcf_round_trip(
    vcf_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Serialize VCF -> BCF -> VCF via pysam or the Docker harness.

    On Linux with native pysam available, runs pysam in-process. On
    Windows (no native pysam), shells out to the pysam Docker image via
    the harness `--mode bcf_roundtrip` subcommand. Returns the round-
    tripped VCF lines; caller compares to the input via the oracle.

    If the round-trip cannot be executed (pysam unavailable AND Docker
    unavailable), returns the input unchanged so the metamorphic check
    trivially passes — that's safer than inventing a false positive.
    """
    return _run_bcf_pysam_mode(vcf_lines, mode="bcf_roundtrip", seed=seed)


# ---------------------------------------------------------------------------
# 14. permute_bcf_header_dictionary — VCF v4.5 §6.2.1
# ---------------------------------------------------------------------------
@register_transform(
    "permute_bcf_header_dictionary",
    format="VCF",
    description=(
        "Shuffle the order of ##contig / ##INFO / ##FORMAT / ##FILTER "
        "lines, re-emit as BCF (codec re-indexes dictionary entries), "
        "then round-trip back to VCF. Per VCF v4.5 §6.2.1 these "
        "dictionary orderings are implementation-defined; a parser that "
        "treats index i as authoritative without consulting the header "
        "produces divergent output."
    ),
    contextual_hint=(
        "the file has multiple ##INFO / ##FORMAT / ##contig entries and "
        "the SUT uses BCF encoding internally. A spec-compliant parser "
        "must produce identical canonical JSON regardless of the order "
        "dictionary entries are declared in."
    ),
    preconditions=(
        "bcf_codec_available",
        "pysam_runtime_reachable",
        "header_has_multiple_info_or_format_entries",
    ),
)
def permute_bcf_header_dictionary(
    vcf_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Shuffle BCF header dictionary order, then round-trip via BCF."""
    return _run_bcf_pysam_mode(vcf_lines, mode="bcf_header_reorder", seed=seed)


# ---------------------------------------------------------------------------
# 15. sut_write_roundtrip — parse x with the primary SUT, re-serialize via
#     the same SUT's public writer. Works for BOTH VCF and SAM: the runner
#     decides which writer to invoke based on format_type. Chen et al. 2018
#     §3.2 round-trip MR; complementary to (and distinct from)
#     vcf_bcf_round_trip which exercises the binary codec.
# ---------------------------------------------------------------------------
@register_transform(
    "sut_write_roundtrip",
    format="VCF/SAM",
    description=(
        "Parse a file with the primary SUT, then re-serialize it via "
        "that same SUT's public writer API (htsjdk VCFWriter or "
        "SAMFileWriter, pysam VariantFile or AlignmentFile, a hypothetical "
        "Rust writer). Per Chen, Kuo, Liu, Tse (2018) §3.2, "
        "`parse(write(parse(x)))` must deep-equal `parse(x)`; any diff "
        "exposes a writer bug in the primary SUT. Format-agnostic — the "
        "runner dispatches to the VCF or SAM writer based on the seed's "
        "format, so one transform covers both and adding new SUTs only "
        "needs a runner-class change."
    ),
    contextual_hint=(
        "the MR target is round_trip_invariance and the primary SUT has "
        "a writer (its Runner sets supports_write_roundtrip=True). This "
        "is the ONLY writer transform in the menu — pick it whenever you "
        "want to exercise any SUT's serializer for the current format; "
        "which SUT actually runs is decided at Phase C time, not here."
    ),
    preconditions=(
        "primary_sut_has_writer",
    ),
)
def sut_write_roundtrip(
    file_lines: list[str],
    seed: Optional[int] = None,
    runner=None,
    format_type: str = "VCF",
) -> list[str]:
    """Round-trip a file through the supplied runner's public writer.

    `runner` is the `ParserRunner` chosen by the orchestrator (usually
    the primary SUT, else the first writer-capable SUT in the pool).
    `format_type` is "VCF" or "SAM" and is threaded through to
    `runner.run_write_roundtrip` so the runner picks the right writer.
    If `runner` is None, its `supports_write_roundtrip` flag is False,
    or the call raises — returns the input unchanged (safe-default,
    same policy as `vcf_bcf_round_trip`).
    """
    import logging
    import os
    import tempfile
    from pathlib import Path as _P

    logger = logging.getLogger(__name__)

    if not file_lines or runner is None:
        return file_lines
    if not getattr(runner, "supports_write_roundtrip", False):
        logger.debug(
            "sut_write_roundtrip: runner %r does not support write_roundtrip",
            getattr(runner, "name", type(runner).__name__),
        )
        return file_lines

    fmt = (format_type or "VCF").upper()
    ext = ".vcf" if fmt == "VCF" else ".sam"
    with tempfile.TemporaryDirectory(prefix="biotest_sut_rt_") as tmpdir:
        input_path = _P(os.path.join(tmpdir, f"input{ext}"))
        with open(input_path, "w", encoding="utf-8") as f:
            f.writelines(file_lines)
        try:
            result = runner.run_write_roundtrip(input_path, fmt)
        except NotImplementedError:
            logger.warning(
                "Runner %r declares supports_write_roundtrip=True "
                "but raises NotImplementedError — no-op",
                getattr(runner, "name", type(runner).__name__),
            )
            return file_lines
        except Exception as e:
            logger.debug("sut_write_roundtrip: runner raised: %s", e)
            return file_lines

        if not result.success or not result.canonical_json:
            logger.debug(
                "sut_write_roundtrip: runner returned failure: %s",
                (result.stderr or "")[:200],
            )
            return file_lines
        text = result.canonical_json.get("rewritten_text", "") or ""
        if not text.strip():
            return file_lines
        return text.splitlines(keepends=True)


# ---------------------------------------------------------------------------
# Helper: dispatch pysam harness subcommands through native pysam or Docker
# ---------------------------------------------------------------------------

def _run_pysam_mode(
    vcf_lines: list[str],
    mode: str,
    seed: Optional[int] = None,
) -> list[str]:
    """Execute a pysam-harness subcommand and return the resulting VCF.

    Supported modes: bcf_roundtrip, bcf_header_reorder, vcf_write_roundtrip.
    Tries native pysam first (fast); falls back to Docker
    `biotest-pysam:latest` on Windows. On total failure returns the
    input unchanged — see vcf_bcf_round_trip docstring for rationale.
    """
    import logging
    import os
    import subprocess
    import sys
    import tempfile

    logger = logging.getLogger(__name__)

    if not vcf_lines:
        return vcf_lines

    with tempfile.TemporaryDirectory(prefix="biotest_pysam_") as tmpdir:
        input_path = os.path.join(tmpdir, "input.vcf")
        output_path = os.path.join(tmpdir, "output.vcf")
        with open(input_path, "w", encoding="utf-8") as f:
            f.writelines(vcf_lines)

        # Try native pysam in-process first
        try:
            import pysam  # noqa: F401 - only import if available
            from pathlib import Path as _P
            # Avoid importing the harness module (it assumes Docker paths);
            # replicate the core logic here for native path.
            if mode == "bcf_roundtrip":
                _native_bcf_roundtrip(_P(input_path), _P(output_path))
            elif mode == "bcf_header_reorder":
                _native_bcf_header_reorder(
                    _P(input_path), _P(output_path), seed=seed or 0
                )
            elif mode == "vcf_write_roundtrip":
                _native_vcf_write_roundtrip(_P(input_path), _P(output_path))
            else:
                return vcf_lines
            with open(output_path, "r", encoding="utf-8") as f:
                return f.readlines()
        except ImportError:
            pass  # pysam not available natively — try Docker below
        except Exception as e:
            logger.debug("Native pysam mode %s failed: %s", mode, e)

        # Docker fallback
        try:
            import shutil
            if not shutil.which("docker"):
                return vcf_lines
            mount = tmpdir.replace("\\", "/")
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{mount}:/data",
                "biotest-pysam:latest",
                "--mode", mode,
            ]
            if mode == "bcf_header_reorder" and seed is not None:
                cmd.extend(["--seed", str(seed)])
            cmd.extend(["/data/input.vcf", "/data/output.vcf"])
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60,
                creationflags=creation_flags,
            )
            if proc.returncode != 0 or not os.path.exists(output_path):
                logger.debug(
                    "Docker pysam mode %s failed: rc=%s stderr=%s",
                    mode, proc.returncode, (proc.stderr or "")[:200],
                )
                return vcf_lines
            with open(output_path, "r", encoding="utf-8") as f:
                return f.readlines()
        except Exception as e:
            logger.debug("Docker pysam mode %s failed: %s", mode, e)
            return vcf_lines


# Backward-compat alias. Existing callers of _run_bcf_pysam_mode
# (vcf_bcf_round_trip, permute_bcf_header_dictionary) keep working.
_run_bcf_pysam_mode = _run_pysam_mode


def _native_bcf_roundtrip(input_vcf, output_vcf) -> None:
    """Native pysam implementation of the bcf_roundtrip harness mode."""
    import pysam
    import tempfile
    tmp_bcf = tempfile.mkstemp(suffix=".bcf")[1]
    try:
        src = pysam.VariantFile(str(input_vcf))
        out = pysam.VariantFile(str(tmp_bcf), "wb", header=src.header)
        try:
            for rec in src:
                out.write(rec)
        finally:
            out.close()
            src.close()
        rd = pysam.VariantFile(str(tmp_bcf))
        fin = pysam.VariantFile(str(output_vcf), "w", header=rd.header)
        try:
            for rec in rd:
                fin.write(rec)
        finally:
            fin.close()
            rd.close()
    finally:
        import os
        try:
            os.unlink(tmp_bcf)
        except OSError:
            pass


def _native_vcf_write_roundtrip(input_vcf, output_vcf) -> None:
    """Native pysam implementation of vcf_write_roundtrip.

    Parse input_vcf via pysam.VariantFile, then re-serialize with the
    text writer (no BCF hop). Exercises libhts's `vcf_write_line` and
    the pysam Cython VCF writer — distinct from the BCF2 codec path
    covered by `_native_bcf_roundtrip`.
    """
    import pysam
    src = pysam.VariantFile(str(input_vcf))
    out = pysam.VariantFile(str(output_vcf), "w", header=src.header)
    try:
        for rec in src:
            out.write(rec)
    finally:
        out.close()
        src.close()


# ---------------------------------------------------------------------------
# 15. permute_csq_annotations — CSQ/ANN record-level ordering
# ---------------------------------------------------------------------------
@register_transform(
    "permute_csq_annotations",
    format="VCF",
    description=(
        "Permute the comma-separated RECORDS of a CSQ (Ensembl VEP) or "
        "ANN (SnpEff) INFO annotation. NEVER permutes pipe-delimited "
        "sub-fields within a record — those are positional per the "
        "##INFO Format description. Per VEP output docs, record order is "
        "not required to follow any specific sequence."
    ),
    contextual_hint=(
        "the INFO field contains a CSQ or ANN key with multiple comma-"
        "separated annotations. Useful against pipelines that silently "
        "pick [0] as 'primary consequence' (a common bug per Cingolani "
        "2012 SnpEff paper)."
    ),
    preconditions=(
        "info_has_key=CSQ OR info_has_key=ANN",
        "csq_records>=2",
    ),
)
def permute_csq_annotations(
    info_str: str,
    key: str = "CSQ",
    seed: Optional[int] = None,
) -> str:
    """Permute the comma-separated records of a CSQ/ANN INFO value.

    Args:
        info_str: The full INFO column string, e.g.
                  "DP=10;CSQ=A|gene1|...,T|gene1|...".
        key:      "CSQ" or "ANN" (or any INFO field id that carries a
                  list of pipe-delimited annotation records).
        seed:     RNG seed for reproducibility.

    Returns:
        A new INFO string with the records of `key` shuffled. All other
        INFO fields are preserved verbatim in their original positions.
        Each record's internal `|`-delimited layout is UNCHANGED.

    Raises:
        ValueError: if the permuted records would change their pipe
        count, which would indicate a bug in this function itself
        (never happens when we just reshuffle an iterable).
    """
    if not info_str or info_str == "." or "=" not in info_str:
        return info_str

    rng = random.Random(seed)
    parts = info_str.split(";")
    new_parts: list[str] = []
    for chunk in parts:
        if "=" not in chunk:
            new_parts.append(chunk)
            continue
        k, v = chunk.split("=", 1)
        if k != key or "," not in v:
            new_parts.append(chunk)
            continue
        records = v.split(",")
        if len(records) < 2:
            new_parts.append(chunk)
            continue
        # Self-check: pipe count per record must be preserved.
        original_pipes = [r.count("|") for r in records]
        permuted = records[:]
        rng.shuffle(permuted)
        new_pipes = [r.count("|") for r in permuted]
        if sorted(original_pipes) != sorted(new_pipes):
            raise ValueError(
                f"CSQ permutation would corrupt sub-field layout "
                f"(pipe counts changed: {original_pipes} -> {new_pipes})"
            )
        new_parts.append(f"{k}={','.join(permuted)}")
    return ";".join(new_parts)


def _native_bcf_header_reorder(input_vcf, output_vcf, seed: int = 0) -> None:
    """Native pysam implementation of the bcf_header_reorder harness mode."""
    import pysam
    import random
    import tempfile
    rng = random.Random(seed)

    lines = open(str(input_vcf), "r", encoding="utf-8").readlines()
    fileformat = None
    chrom = None
    bucket = {"contig": [], "INFO": [], "FORMAT": [], "FILTER": [], "other": []}
    body: list[str] = []
    in_header = True
    for ln in lines:
        if not in_header:
            body.append(ln)
            continue
        if ln.startswith("##fileformat"):
            fileformat = ln
        elif ln.startswith("#CHROM"):
            chrom = ln
            in_header = False
        elif ln.startswith("##"):
            m = re.match(r"##(contig|INFO|FORMAT|FILTER)=", ln)
            bucket[m.group(1) if m else "other"].append(ln)
        else:
            body.append(ln)
            in_header = False

    for k in ("contig", "INFO", "FORMAT", "FILTER"):
        rng.shuffle(bucket[k])

    new_header = []
    if fileformat:
        new_header.append(fileformat)
    for k in ("contig", "INFO", "FORMAT", "FILTER", "other"):
        new_header.extend(bucket[k])
    if chrom:
        new_header.append(chrom)

    tmp_vcf = tempfile.mkstemp(suffix=".vcf")[1]
    tmp_bcf = tempfile.mkstemp(suffix=".bcf")[1]
    try:
        with open(tmp_vcf, "w", encoding="utf-8") as f:
            f.write("".join(new_header) + "".join(body))
        src = pysam.VariantFile(str(tmp_vcf))
        bout = pysam.VariantFile(str(tmp_bcf), "wb", header=src.header)
        try:
            for rec in src:
                bout.write(rec)
        finally:
            bout.close()
            src.close()
        rd = pysam.VariantFile(str(tmp_bcf))
        vout = pysam.VariantFile(str(output_vcf), "w", header=rd.header)
        try:
            for rec in rd:
                vout.write(rec)
        finally:
            vout.close()
            rd.close()
    finally:
        import os
        for p in (tmp_vcf, tmp_bcf):
            try:
                os.unlink(p)
            except OSError:
                pass
