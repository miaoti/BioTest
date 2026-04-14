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
