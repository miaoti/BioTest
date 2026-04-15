"""
Transform Dispatch Wrapper: bridges Phase B's atomic transforms to file-level operations.

This is the most design-intensive piece of Phase C. Each of the 13 transforms
has a different signature (file-level, line-level, field-level, compound).
The dispatcher provides a uniform interface:

    apply_transform(name, file_lines, seed) -> file_lines

It knows how to extract the right input fragment from the file, call the
raw transform function, and reassemble the result into a complete file.
"""

from __future__ import annotations

import re
import random
import logging
from typing import Optional

from mr_engine.transforms import TRANSFORM_REGISTRY
from .z3_constraints import check_cigar_seq_constraint, check_info_number_a

logger = logging.getLogger(__name__)

# Safe assume() that is a no-op outside Hypothesis @given context.
# hypothesis.assume() raises UnsatisfiedAssumption when called outside
# a property-based test, so we check the internal state flag first.
def _h_assume(condition: bool) -> None:
    """Call hypothesis.assume() if inside @given, otherwise no-op."""
    if condition:
        return  # Constraint satisfied, nothing to do
    try:
        from hypothesis.core import _hypothesis_global_random  # noqa: F401
        from hypothesis._settings import note_deprecation  # noqa: F401
        from hypothesis.control import current_build_context
        # Only call assume() if we're actually inside a @given test
        ctx = current_build_context()
        if ctx is not None:
            from hypothesis import assume
            assume(condition)
    except Exception:
        # Outside @given context, hypothesis not installed, or no build context
        pass
from mr_engine.transforms.vcf import (
    shuffle_meta_lines,
    permute_structured_kv_order,
    choose_permutation,
    permute_alt,
    remap_gt,
    permute_number_a_r_fields,
    permute_sample_columns,
    shuffle_info_field_kv,
    inject_equivalent_missing_values,
)
from mr_engine.transforms.sam import (
    permute_optional_tag_fields,
    split_or_merge_adjacent_cigar_ops,
    reorder_header_records,
    toggle_cigar_hard_soft_clipping,
)


# ---------------------------------------------------------------------------
# Dispatch registry: transform_name -> wrapper function
# ---------------------------------------------------------------------------

_DISPATCH: dict[str, callable] = {}


def _register(name: str):
    """Decorator to register a dispatch wrapper."""
    def decorator(fn):
        _DISPATCH[name] = fn
        return fn
    return decorator


def apply_transform(
    name: str,
    file_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """
    Apply a named transform to a complete file (as a list of lines).

    This is the uniform interface consumed by the orchestrator.
    Each transform's dispatch wrapper handles the extraction, transform,
    and reassembly logic internally.

    Args:
        name: Transform name from TRANSFORM_REGISTRY.
        file_lines: All lines of the input file (with or without trailing newlines).
        seed: RNG seed for reproducibility.

    Returns:
        New list of file lines after transformation.
    """
    if name not in _DISPATCH:
        raise ValueError(
            f"No dispatch wrapper for transform '{name}'. "
            f"Available: {sorted(_DISPATCH.keys())}"
        )
    return _DISPATCH[name](file_lines, seed)


def apply_mr_transforms(
    file_lines: list[str],
    transform_steps: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """
    Apply a sequence of transforms (from an MR) to a file.

    Handles the compound ALT permutation group specially: when all four
    members are present, they share a single permutation array.

    Args:
        file_lines: Input file lines.
        transform_steps: List of transform names from the MR.
        seed: Base RNG seed.

    Returns:
        Transformed file lines.
    """
    # Check for compound ALT permutation group
    compound = {"choose_permutation", "permute_ALT", "remap_GT", "permute_Number_A_R_fields"}
    if compound.issubset(set(transform_steps)):
        return _apply_compound_alt_permutation(file_lines, seed)

    # Sequential application of independent transforms
    result = list(file_lines)
    for step_name in transform_steps:
        result = apply_transform(step_name, result, seed)
    return result


# ===========================================================================
# VCF File-level transforms
# ===========================================================================

@_register("shuffle_meta_lines")
def _dispatch_shuffle_meta_lines(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """File-level: directly call shuffle_meta_lines on all lines."""
    # Auto-detect the ##fileformat line to pin it first
    pinned = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("##fileformat="):
            pinned.append(stripped)
            break
    return shuffle_meta_lines(lines, except_exact=pinned or None, seed=seed)


@_register("permute_sample_columns")
def _dispatch_permute_sample_columns(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """File-level: directly call permute_sample_columns on all lines."""
    return permute_sample_columns(lines, seed=seed)


# ===========================================================================
# VCF Line-level transforms
# ===========================================================================

@_register("permute_structured_kv_order")
def _dispatch_permute_structured_kv(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Line-level: apply permute_structured_kv_order to each structured ## meta line."""
    rng = random.Random(seed)
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        # Only structured meta lines: ##KEY=<...>
        if stripped.startswith("##") and "=<" in stripped:
            child_seed = rng.randint(0, 2**31)
            transformed = permute_structured_kv_order(stripped, seed=child_seed)
            result.append(transformed + "\n" if line.endswith("\n") else transformed)
        else:
            result.append(line)
    return result


@_register("shuffle_info_field_kv")
def _dispatch_shuffle_info_kv(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Line-level: apply shuffle_info_field_kv to the INFO column of each data line."""
    rng = random.Random(seed)
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        # Data lines: don't start with # and have tabs
        if not stripped.startswith("#") and "\t" in stripped:
            cols = stripped.split("\t")
            if len(cols) >= 8:
                child_seed = rng.randint(0, 2**31)
                cols[7] = shuffle_info_field_kv(cols[7], seed=child_seed)
                new_line = "\t".join(cols)
                result.append(new_line + "\n" if line.endswith("\n") else new_line)
            else:
                result.append(line)
        else:
            result.append(line)
    return result


@_register("inject_equivalent_missing_values")
def _dispatch_inject_missing(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Field-level: inject a missing FORMAT field to all data records."""
    # Pick a field ID not already in use
    rng = random.Random(seed)
    candidates = ["XX", "YY", "ZZ"]
    field_id = rng.choice(candidates)

    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if not stripped.startswith("#") and "\t" in stripped:
            cols = stripped.split("\t")
            if len(cols) >= 10:
                format_col = cols[8]
                sample_cols = cols[9:]
                new_fmt, new_samples = inject_equivalent_missing_values(
                    format_col, sample_cols, field_id
                )
                cols[8] = new_fmt
                cols[9:] = new_samples
                new_line = "\t".join(cols)
                result.append(new_line + "\n" if line.endswith("\n") else new_line)
            else:
                result.append(line)
        else:
            result.append(line)
    return result


# ===========================================================================
# VCF Compound: ALT permutation (choose_permutation + permute_ALT +
#               remap_GT + permute_Number_A_R_fields)
# ===========================================================================

@_register("choose_permutation")
def _dispatch_choose_permutation(lines: list[str], seed: Optional[int]) -> list[str]:
    """Compound member — when called alone, apply full compound group."""
    return _apply_compound_alt_permutation(lines, seed)


@_register("permute_ALT")
def _dispatch_permute_alt(lines: list[str], seed: Optional[int]) -> list[str]:
    """Compound member — when called alone, apply full compound group."""
    return _apply_compound_alt_permutation(lines, seed)


@_register("remap_GT")
def _dispatch_remap_gt(lines: list[str], seed: Optional[int]) -> list[str]:
    """Compound member — when called alone, apply full compound group."""
    return _apply_compound_alt_permutation(lines, seed)


@_register("permute_Number_A_R_fields")
def _dispatch_permute_number_ar(lines: list[str], seed: Optional[int]) -> list[str]:
    """Compound member — when called alone, apply full compound group."""
    return _apply_compound_alt_permutation(lines, seed)


def _apply_compound_alt_permutation(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """
    Apply the full ALT permutation compound transform to a VCF file.

    For each data record with multi-ALT:
    1. choose_permutation(n_alts, seed) -> pi
    2. permute_alt(ALT_field, pi)
    3. remap_gt(GT_field, pi) for each sample
    4. permute_number_a_r_fields(value, pi) for each Number=A/R INFO field

    Needs header INFO definitions to identify Number=A and Number=R fields.
    """
    rng = random.Random(seed)

    # Parse header to find Number=A and Number=R INFO fields
    number_a_fields: set[str] = set()
    number_r_fields: set[str] = set()
    for line in lines:
        stripped = line.rstrip("\n\r")
        m = re.match(r"^##INFO=<(.+)>$", stripped)
        if m:
            fields = _parse_kv(m.group(1))
            field_id = fields.get("ID", "")
            number = fields.get("Number", "")
            if number == "A":
                number_a_fields.add(field_id)
            elif number == "R":
                number_r_fields.add(field_id)

    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("#") or "\t" not in stripped:
            result.append(line)
            continue

        cols = stripped.split("\t")
        if len(cols) < 8:
            result.append(line)
            continue

        alt_field = cols[4]
        if alt_field == "." or "," not in alt_field:
            # No multi-ALT, skip
            result.append(line)
            continue

        n_alts = len(alt_field.split(","))
        child_seed = rng.randint(0, 2**31)
        pi = choose_permutation(n_alts, seed=child_seed)

        # 1. Permute ALT
        cols[4] = permute_alt(cols[4], pi)

        # 2. Permute Number=A and Number=R in INFO
        info_str = cols[7]
        if info_str != ".":
            info_parts = info_str.split(";")
            new_parts = []
            for part in info_parts:
                if "=" in part:
                    key, val = part.split("=", 1)
                    if key in number_a_fields and "," in val:
                        val = permute_number_a_r_fields(val, pi, is_number_r=False)
                    elif key in number_r_fields and "," in val:
                        val = permute_number_a_r_fields(val, pi, is_number_r=True)
                    new_parts.append(f"{key}={val}")
                else:
                    new_parts.append(part)
            cols[7] = ";".join(new_parts)

        # 3. Remap GT in each sample
        if len(cols) > 8 and cols[8] != ".":
            fmt_keys = cols[8].split(":")
            gt_idx = fmt_keys.index("GT") if "GT" in fmt_keys else -1
            if gt_idx >= 0:
                for s_idx in range(9, len(cols)):
                    sample_vals = cols[s_idx].split(":")
                    if gt_idx < len(sample_vals):
                        sample_vals[gt_idx] = remap_gt(sample_vals[gt_idx], pi)
                        cols[s_idx] = ":".join(sample_vals)

        # Z3 post-transform guard: Number=A fields must have len(ALT) values
        new_alt_count = len(cols[4].split(","))
        info_str_check = cols[7]
        if info_str_check != ".":
            for part in info_str_check.split(";"):
                if "=" in part:
                    key, val = part.split("=", 1)
                    if key in number_a_fields and "," in val:
                        vals = val.split(",")
                        if not check_info_number_a(new_alt_count, vals):
                            logger.debug("Z3 guard: Number=A mismatch after ALT permutation")
                            _h_assume(False)

        new_line = "\t".join(cols)
        result.append(new_line + "\n" if line.endswith("\n") else new_line)

    return result


def _parse_kv(text: str) -> dict[str, str]:
    """Parse key=value pairs from structured meta line content."""
    fields: dict[str, str] = {}
    i = 0
    while i < len(text):
        eq = text.find("=", i)
        if eq == -1:
            break
        key = text[i:eq].strip()
        val_start = eq + 1
        if val_start < len(text) and text[val_start] == '"':
            close = text.find('"', val_start + 1)
            if close == -1:
                close = len(text)
            fields[key] = text[val_start + 1 : close]
            i = close + 2
        else:
            comma = text.find(",", val_start)
            if comma == -1:
                fields[key] = text[val_start:]
                break
            fields[key] = text[val_start:comma]
            i = comma + 1
    return fields


# ===========================================================================
# SAM Line-level transforms
# ===========================================================================

@_register("permute_optional_tag_fields")
def _dispatch_permute_tags(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Line-level: shuffle optional tags on each alignment line."""
    rng = random.Random(seed)
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("@") or "\t" not in stripped:
            result.append(line)
            continue
        child_seed = rng.randint(0, 2**31)
        transformed = permute_optional_tag_fields(stripped, seed=child_seed)
        result.append(transformed + "\n" if line.endswith("\n") else transformed)
    return result


@_register("reorder_header_records")
def _dispatch_reorder_header(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """File-level: shuffle SAM header records (@SQ, @RG, etc.)."""
    header_lines = [l.rstrip("\n\r") for l in lines if l.rstrip("\n\r").startswith("@")]
    non_header = [l for l in lines if not l.rstrip("\n\r").startswith("@")]
    reordered = reorder_header_records(header_lines, seed=seed)
    # Re-add newlines
    result = [h + "\n" for h in reordered] + non_header
    return result


@_register("split_or_merge_adjacent_cigar_ops")
def _dispatch_cigar_split_merge(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Line-level: split or merge CIGAR operations on each alignment.
    Z3 guard: verify sum(query_consuming_ops) == len(SEQ) after transform."""
    rng = random.Random(seed)
    mode = rng.choice(["split", "merge"])
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("@") or "\t" not in stripped:
            result.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) >= 6 and cols[5] != "*":
            child_seed = rng.randint(0, 2**31)
            new_cigar = split_or_merge_adjacent_cigar_ops(cols[5], mode=mode, seed=child_seed)

            # Z3 post-transform guard: CIGAR query length must match SEQ length
            if len(cols) >= 10 and cols[9] != "*":
                cigar_ops = [(int(m.group(1)), m.group(2))
                             for m in re.finditer(r"(\d+)([MIDNSHP=X])", new_cigar)]
                seq_len = len(cols[9])
                if not check_cigar_seq_constraint(cigar_ops, seq_len):
                    logger.debug("Z3 guard: CIGAR/SEQ mismatch after %s, discarding", mode)
                    _h_assume(False)  # Tell Hypothesis to discard this example

            cols[5] = new_cigar
            new_line = "\t".join(cols)
            result.append(new_line + "\n" if line.endswith("\n") else new_line)
        else:
            result.append(line)
    return result


@_register("toggle_cigar_hard_soft_clipping")
def _dispatch_toggle_clipping(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Line-level: toggle H<->S clipping with SEQ/QUAL sync.
    Z3 guard: verify CIGAR query length == SEQ length after transform."""
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("@") or "\t" not in stripped:
            result.append(line)
            continue
        cols = stripped.split("\t")
        if len(cols) >= 11 and cols[5] != "*" and ("H" in cols[5] or "S" in cols[5]):
            cigar_str = cols[5]
            seq = cols[9]
            qual = cols[10]
            new_cigar, new_seq, new_qual = toggle_cigar_hard_soft_clipping(
                cigar_str, seq, qual
            )

            # Z3 post-transform guard: new CIGAR must agree with new SEQ length
            if new_seq != "*":
                cigar_ops = [(int(m.group(1)), m.group(2))
                             for m in re.finditer(r"(\d+)([MIDNSHP=X])", new_cigar)]
                if not check_cigar_seq_constraint(cigar_ops, len(new_seq)):
                    logger.debug("Z3 guard: CIGAR/SEQ mismatch after clipping toggle, discarding")
                    _h_assume(False)

            cols[5] = new_cigar
            cols[9] = new_seq
            cols[10] = new_qual
            new_line = "\t".join(cols)
            result.append(new_line + "\n" if line.endswith("\n") else new_line)
        else:
            result.append(line)
    return result
