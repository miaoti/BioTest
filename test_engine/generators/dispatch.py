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
    trim_common_affixes,
    left_align_indel,
    split_multi_allelic,
    vcf_bcf_round_trip,
    permute_bcf_header_dictionary,
    permute_csq_annotations,
    sut_write_roundtrip,
)
from mr_engine.transforms.sam import (
    permute_optional_tag_fields,
    split_or_merge_adjacent_cigar_ops,
    reorder_header_records,
    toggle_cigar_hard_soft_clipping,
    shuffle_hd_subtags,
    shuffle_sq_record_subtags,
    shuffle_rg_record_subtags,
    shuffle_pg_record_subtags,
    shuffle_co_comments,
    sam_bam_round_trip,
    sam_cram_round_trip,
)
from mr_engine.transforms.malformed import (
    violate_info_number_a_cardinality,
    violate_required_fixed_columns,
    violate_fileformat_first_line,
    violate_gt_index_bounds,
    violate_cigar_seq_length,
    violate_tlen_sign_consistency,
    violate_optional_tag_type_character,
    violate_flag_bit_exclusivity,
)


# ---------------------------------------------------------------------------
# Dispatch registry: transform_name -> wrapper function
# ---------------------------------------------------------------------------

_DISPATCH: dict[str, callable] = {}

# Transforms that need a reference to the primary SUT runner at call
# time (e.g. sut_write_roundtrip dispatches to runner.run_write_roundtrip).
# The vast majority of transforms are SUT-agnostic text operations — they
# live in _DISPATCH only. Runner-aware ones register into BOTH so
# `apply_transform` knows to pass the hook as a kwarg.
_DISPATCH_NEEDS_HOOK: set[str] = set()

# Transforms that must know the seed's format ("VCF" or "SAM") at call
# time so the same transform can serve both (currently: sut_write_roundtrip).
_DISPATCH_NEEDS_FORMAT: set[str] = set()


def _register(
    name: str,
    *,
    needs_runner_hook: bool = False,
    needs_format_context: bool = False,
):
    """Decorator to register a dispatch wrapper.

    Set `needs_runner_hook=True` for transforms that must call into a
    runner instance at invocation time. Set `needs_format_context=True`
    for transforms whose behaviour depends on the seed's format ("VCF"
    or "SAM"). These flags control the positional arguments forwarded
    to the wrapper by `apply_transform`.
    """
    def decorator(fn):
        _DISPATCH[name] = fn
        if needs_runner_hook:
            _DISPATCH_NEEDS_HOOK.add(name)
        if needs_format_context:
            _DISPATCH_NEEDS_FORMAT.add(name)
        return fn
    return decorator


def apply_transform(
    name: str,
    file_lines: list[str],
    seed: Optional[int] = None,
    *,
    runner_hook=None,
    format_context: Optional[str] = None,
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
        runner_hook: Optional ParserRunner injected by the orchestrator
                     for transforms that need a SUT to call into (see
                     `needs_runner_hook` in `_register`). Ignored by
                     transforms that don't opt in.
        format_context: "VCF" or "SAM" — passed through to transforms
                     registered with `needs_format_context=True`.

    Returns:
        New list of file lines after transformation.
    """
    if name not in _DISPATCH:
        raise ValueError(
            f"No dispatch wrapper for transform '{name}'. "
            f"Available: {sorted(_DISPATCH.keys())}"
        )
    needs_hook = name in _DISPATCH_NEEDS_HOOK
    needs_fmt = name in _DISPATCH_NEEDS_FORMAT
    if needs_hook and needs_fmt:
        return _DISPATCH[name](file_lines, seed, runner_hook, format_context)
    if needs_hook:
        return _DISPATCH[name](file_lines, seed, runner_hook)
    if needs_fmt:
        return _DISPATCH[name](file_lines, seed, format_context)
    return _DISPATCH[name](file_lines, seed)


def apply_mr_transforms(
    file_lines: list[str],
    transform_steps: list[str],
    seed: Optional[int] = None,
    *,
    runner_hook=None,
    format_context: Optional[str] = None,
) -> list[str]:
    """
    Apply a sequence of transforms (from an MR) to a file.

    Handles the compound ALT permutation group specially: when all four
    members are present, they share a single permutation array.

    Args:
        file_lines: Input file lines.
        transform_steps: List of transform names from the MR.
        seed: Base RNG seed.
        runner_hook: Passed through to `apply_transform` for runner-aware
                     transforms. The orchestrator resolves this to the
                     primary SUT (or first writer-capable SUT when no
                     primary is set) and injects it here.
        format_context: "VCF" or "SAM" — passed through to transforms
                     that opted into format awareness (currently
                     `sut_write_roundtrip`).

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
        result = apply_transform(
            step_name, result, seed,
            runner_hook=runner_hook,
            format_context=format_context,
        )
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


# ===========================================================================
# VCF variant-normalization transforms (record-level)
# ===========================================================================

@_register("trim_common_affixes")
def _dispatch_trim_common_affixes(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Record-level: trim shared REF/ALT prefix+suffix for biallelic records."""
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if not stripped.startswith("#") and "\t" in stripped:
            cols = stripped.split("\t")
            if len(cols) >= 5 and "," not in cols[4]:
                # biallelic only (MR precondition)
                try:
                    pos = int(cols[1])
                except ValueError:
                    result.append(line)
                    continue
                new_ref, new_alt, new_pos = trim_common_affixes(
                    cols[3], cols[4], pos,
                )
                cols[1] = str(new_pos)
                cols[3] = new_ref
                cols[4] = new_alt
                new_line = "\t".join(cols)
                result.append(new_line + "\n" if line.endswith("\n") else new_line)
                continue
        result.append(line)
    return result


@_register("left_align_indel")
def _dispatch_left_align_indel(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Record-level: conservative left-shift of indels in homopolymer runs."""
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if not stripped.startswith("#") and "\t" in stripped:
            cols = stripped.split("\t")
            if len(cols) >= 5 and "," not in cols[4]:
                try:
                    pos = int(cols[1])
                except ValueError:
                    result.append(line)
                    continue
                new_ref, new_alt, new_pos = left_align_indel(
                    cols[3], cols[4], pos,
                )
                cols[1] = str(new_pos)
                cols[3] = new_ref
                cols[4] = new_alt
                new_line = "\t".join(cols)
                result.append(new_line + "\n" if line.endswith("\n") else new_line)
                continue
        result.append(line)
    return result


@_register("split_multi_allelic")
def _dispatch_split_multi_allelic(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Record-level: split multi-ALT records into per-ALT records.

    Z3 guard: after split, each per-ALT record must have exactly 1 ALT
    and Number=A INFO arrays of length 1. Violations discard the sample
    inside Hypothesis @given context.
    """
    # Parse header to build info_meta / format_meta dicts
    info_meta: dict = {}
    format_meta: dict = {}
    for line in lines:
        s = line.rstrip("\n\r")
        if s.startswith("##INFO=<") or s.startswith("##FORMAT=<"):
            m = re.match(
                r"##(INFO|FORMAT)=<([^>]*)>", s,
            )
            if not m:
                continue
            bucket = info_meta if m.group(1) == "INFO" else format_meta
            fields = _parse_kv(m.group(2))
            fid = fields.get("ID", "")
            if fid:
                bucket[fid] = fields
        elif s.startswith("#CHROM"):
            break

    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if not stripped.startswith("#") and "\t" in stripped:
            cols = stripped.split("\t")
            if len(cols) >= 5 and "," in cols[4]:
                new_records = split_multi_allelic(cols, info_meta, format_meta)
                # Z3 guard: verify each produced record has alt_count == 1
                # and that Number=A INFO fields are length 1.
                for nr in new_records:
                    if len(nr) >= 8 and "," in nr[4]:
                        logger.debug("split_multi_allelic Z3: ALT still comma-joined")
                        _h_assume(False)
                    for key_val in (nr[7] or "").split(";"):
                        if "=" not in key_val:
                            continue
                        k, v = key_val.split("=", 1)
                        if (info_meta.get(k) or {}).get("Number") == "A":
                            vals = v.split(",")
                            if not check_info_number_a(1, vals):
                                logger.debug(
                                    "split_multi_allelic Z3: Number=A mismatch "
                                    "on key %s: %d vals for 1 ALT",
                                    k, len(vals),
                                )
                                _h_assume(False)
                for nr in new_records:
                    new_line = "\t".join(nr)
                    result.append(
                        new_line + "\n" if line.endswith("\n") else new_line
                    )
                continue
        result.append(line)
    return result


# ===========================================================================
# VCF BCF-codec transforms (whole-file, delegate to pysam/Docker)
# ===========================================================================

@_register("vcf_bcf_round_trip")
def _dispatch_vcf_bcf_round_trip(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """File-level: VCF -> BCF -> VCF via pysam or Docker harness."""
    return vcf_bcf_round_trip(lines, seed=seed)


@_register("permute_bcf_header_dictionary")
def _dispatch_permute_bcf_header_dictionary(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """File-level: shuffle BCF header dictionary order, then round-trip."""
    return permute_bcf_header_dictionary(lines, seed=seed)


@_register(
    "sut_write_roundtrip",
    needs_runner_hook=True,
    needs_format_context=True,
)
def _dispatch_sut_write_roundtrip(
    lines: list[str],
    seed: Optional[int],
    runner_hook,
    format_context: Optional[str],
) -> list[str]:
    """File-level: parse+serialize via the runner injected by the orchestrator.

    This is the ONLY writer transform in the menu — the per-SUT writer
    dispatch (htsjdk vs pysam vs Rust) and per-format dispatch (VCF vs
    SAM) both happen inside the runner, not here. Adding a new writer
    SUT means implementing runner.run_write_roundtrip; zero changes
    land in the transform / dispatch / strategy layers.
    """
    fmt = (format_context or "VCF").upper()
    return sut_write_roundtrip(
        lines, seed=seed, runner=runner_hook, format_type=fmt,
    )


# ===========================================================================
# VCF CSQ/ANN record-level permutation
# ===========================================================================

@_register("permute_csq_annotations")
def _dispatch_permute_csq_annotations(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    """Record-level: permute comma-separated CSQ/ANN records in INFO.

    Detects whether the header declares CSQ or ANN, then applies the
    record-level permutation to the matching key in each data line's
    INFO column. Pipe-delimited sub-fields are preserved verbatim per
    the ##INFO Format description.
    """
    has_csq = False
    has_ann = False
    for line in lines:
        s = line.rstrip("\n\r")
        if s.startswith("##INFO=<ID=CSQ"):
            has_csq = True
        elif s.startswith("##INFO=<ID=ANN"):
            has_ann = True
        elif s.startswith("#CHROM"):
            break

    if not (has_csq or has_ann):
        return list(lines)  # precondition not met — no-op

    rng = random.Random(seed)
    result = []
    for line in lines:
        stripped = line.rstrip("\n\r")
        if not stripped.startswith("#") and "\t" in stripped:
            cols = stripped.split("\t")
            if len(cols) >= 8 and cols[7] != ".":
                child_seed = rng.randint(0, 2**31)
                new_info = cols[7]
                if has_csq and "CSQ=" in new_info:
                    new_info = permute_csq_annotations(
                        new_info, key="CSQ", seed=child_seed,
                    )
                if has_ann and "ANN=" in new_info:
                    new_info = permute_csq_annotations(
                        new_info, key="ANN", seed=child_seed ^ 0xABCD,
                    )
                cols[7] = new_info
                new_line = "\t".join(cols)
                result.append(new_line + "\n" if line.endswith("\n") else new_line)
                continue
        result.append(line)
    return result


# ===========================================================================
# Rank 3 — spec-rule-targeted malformed-input mutators (VCF + SAM).
# Each delegates to the corresponding `violate_*` transform verbatim —
# they already take `(lines, seed)` shape.
# ===========================================================================


@_register("violate_info_number_a_cardinality")
def _dispatch_violate_info_number_a_cardinality(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_info_number_a_cardinality(lines, seed=seed)


@_register("violate_required_fixed_columns")
def _dispatch_violate_required_fixed_columns(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_required_fixed_columns(lines, seed=seed)


@_register("violate_fileformat_first_line")
def _dispatch_violate_fileformat_first_line(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_fileformat_first_line(lines, seed=seed)


@_register("violate_gt_index_bounds")
def _dispatch_violate_gt_index_bounds(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_gt_index_bounds(lines, seed=seed)


@_register("violate_cigar_seq_length")
def _dispatch_violate_cigar_seq_length(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_cigar_seq_length(lines, seed=seed)


@_register("violate_tlen_sign_consistency")
def _dispatch_violate_tlen_sign_consistency(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_tlen_sign_consistency(lines, seed=seed)


@_register("violate_optional_tag_type_character")
def _dispatch_violate_optional_tag_type_character(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_optional_tag_type_character(lines, seed=seed)


@_register("violate_flag_bit_exclusivity")
def _dispatch_violate_flag_bit_exclusivity(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return violate_flag_bit_exclusivity(lines, seed=seed)


# ===========================================================================
# Phase 2 SAM header-subtag / @CO shuffles.
# Each splits `lines` into (header, non_header), rewrites header via the
# transform, and re-stitches. Mirrors `_dispatch_reorder_header` above.
# ===========================================================================


def _split_header_body(lines: list[str]) -> tuple[list[str], list[str]]:
    """Return (stripped_header_lines, non_header_lines_with_newlines)."""
    header = [l.rstrip("\n\r") for l in lines if l.rstrip("\n\r").startswith("@")]
    body = [l for l in lines if not l.rstrip("\n\r").startswith("@")]
    return header, body


def _stitch_header_body(header: list[str], body: list[str]) -> list[str]:
    return [h + "\n" for h in header] + body


@_register("shuffle_hd_subtags")
def _dispatch_shuffle_hd_subtags(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    header, body = _split_header_body(lines)
    return _stitch_header_body(shuffle_hd_subtags(header, seed=seed), body)


@_register("shuffle_sq_record_subtags")
def _dispatch_shuffle_sq_record_subtags(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    header, body = _split_header_body(lines)
    return _stitch_header_body(shuffle_sq_record_subtags(header, seed=seed), body)


@_register("shuffle_rg_record_subtags")
def _dispatch_shuffle_rg_record_subtags(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    header, body = _split_header_body(lines)
    return _stitch_header_body(shuffle_rg_record_subtags(header, seed=seed), body)


@_register("shuffle_pg_record_subtags")
def _dispatch_shuffle_pg_record_subtags(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    header, body = _split_header_body(lines)
    return _stitch_header_body(shuffle_pg_record_subtags(header, seed=seed), body)


@_register("shuffle_co_comments")
def _dispatch_shuffle_co_comments(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    header, body = _split_header_body(lines)
    return _stitch_header_body(shuffle_co_comments(header, seed=seed), body)


# ===========================================================================
# Phase 3 SAM <-> BAM <-> CRAM round-trip via samtools.
# Each shells out to `samtools view` twice (encode + decode) and returns
# the post-round-trip SAM text. Gated by samtools_available /
# cram_reference_available runtime preconditions.
# ===========================================================================


@_register("sam_bam_round_trip")
def _dispatch_sam_bam_round_trip(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return sam_bam_round_trip(lines, seed=seed)


@_register("sam_cram_round_trip")
def _dispatch_sam_cram_round_trip(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return sam_cram_round_trip(lines, seed=seed)


# ===========================================================================
# Rank 5 — query_method_roundtrip
# ===========================================================================
#
# This transform has NO file-mutation effect. The actual API-query work
# happens inside the orchestrator's `_handle_query_consensus` branch
# (test_engine/orchestrator.py), which detects the transform name in
# the MR's transform_steps and routes the MR to the query-consensus
# oracle instead of the deep-equal consensus.
#
# We register a no-op dispatch wrapper so that:
#   1. The transform validates against the whitelist in the DSL compiler,
#   2. apply_mr_transforms can iterate transform_steps without crashing
#      when a non-mutating step appears in the chain.
@_register("query_method_roundtrip")
def _dispatch_query_method_roundtrip(
    lines: list[str], seed: Optional[int]
) -> list[str]:
    return list(lines)
