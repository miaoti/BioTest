"""
SAM format atomic transform functions.

Each function operates on plain Python types and uses `random.Random(seed)`
for reproducibility.
"""

from __future__ import annotations

import logging
import re
import random
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from . import register_transform

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper: parse and unparse CIGAR strings
# ---------------------------------------------------------------------------
def _parse_cigar(cigar: str) -> list[tuple[int, str]]:
    """Parse CIGAR string into [(length, op), ...]."""
    return [(int(m.group(1)), m.group(2)) for m in re.finditer(r"(\d+)([MIDNSHP=X])", cigar)]


def _unparse_cigar(ops: list[tuple[int, str]]) -> str:
    """Reconstruct CIGAR string from [(length, op), ...]."""
    return "".join(f"{length}{op}" for length, op in ops)


# Ops that consume query (SEQ) — used for length invariant assertions
_QUERY_CONSUMING = {"M", "I", "S", "=", "X"}


def _query_consumed(ops: list[tuple[int, str]]) -> int:
    """Total bases consumed from SEQ by the given CIGAR ops."""
    return sum(length for length, op in ops if op in _QUERY_CONSUMING)


# ---------------------------------------------------------------------------
# 1. permute_optional_tag_fields
# ---------------------------------------------------------------------------
@register_transform(
    "permute_optional_tag_fields",
    format="SAM",
    description="Shuffle the optional TAG:TYPE:VALUE fields (columns 12+) of a SAM alignment line while keeping the 11 mandatory fields fixed.",
)
def permute_optional_tag_fields(
    sam_line: str,
    seed: Optional[int] = None,
) -> str:
    """
    Shuffle the optional TAG:TYPE:VALUE fields (columns 12+) in a SAM
    alignment line while preserving the 11 mandatory fields.

    Args:
        sam_line: A single SAM alignment line (tab-separated).
        seed: RNG seed.

    Returns:
        The SAM line with optional tags in shuffled order.
    """
    rng = random.Random(seed)
    fields = sam_line.rstrip("\n").split("\t")
    if len(fields) <= 11:
        return sam_line  # no optional tags

    mandatory = fields[:11]
    optional = fields[11:]

    # Verify TAG uniqueness
    tags = [f.split(":", 1)[0] for f in optional]
    if len(tags) != len(set(tags)):
        raise ValueError(f"Duplicate optional tags detected: {tags}")

    rng.shuffle(optional)
    return "\t".join(mandatory + optional)


# ---------------------------------------------------------------------------
# 2. split_or_merge_adjacent_cigar_ops
# ---------------------------------------------------------------------------
@register_transform(
    "split_or_merge_adjacent_cigar_ops",
    format="SAM",
    description="Split one CIGAR op into two identical ops (10M -> 4M6M) or merge adjacent identical ops (4M6M -> 10M); total query-consumed length is always preserved.",
)
def split_or_merge_adjacent_cigar_ops(
    cigar: str,
    mode: str = "split",
    seed: Optional[int] = None,
) -> str:
    """
    Split or merge adjacent identical CIGAR operations.

    Split mode:  10M -> randomly split into (x)M + (10-x)M where 1 <= x < 10
    Merge mode:  4M6M -> 10M

    The total query-consumed length is always preserved (asserted).

    Args:
        cigar: CIGAR string, e.g. "10M5I3M".
        mode: "split" to split one random op, "merge" to merge adjacent same ops.
        seed: RNG seed.

    Returns:
        Transformed CIGAR string.

    Raises:
        ValueError: If mode is invalid or invariant is violated.
    """
    rng = random.Random(seed)
    ops = _parse_cigar(cigar)
    original_consumed = _query_consumed(ops)

    if mode == "merge":
        merged: list[tuple[int, str]] = []
        for length, op in ops:
            if merged and merged[-1][1] == op:
                merged[-1] = (merged[-1][0] + length, op)
            else:
                merged.append((length, op))
        result_ops = merged

    elif mode == "split":
        # Pick a random op with length > 1 to split
        splittable = [i for i, (length, _) in enumerate(ops) if length > 1]
        if not splittable:
            return cigar  # nothing to split

        idx = rng.choice(splittable)
        length, op = ops[idx]
        split_at = rng.randint(1, length - 1)
        new_ops = list(ops)
        new_ops[idx:idx + 1] = [(split_at, op), (length - split_at, op)]
        result_ops = new_ops

    else:
        raise ValueError(f"Invalid mode: {mode!r}. Must be 'split' or 'merge'.")

    # Invariant: query-consumed length must not change
    assert _query_consumed(result_ops) == original_consumed, (
        f"CIGAR invariant violated: consumed {_query_consumed(result_ops)} "
        f"!= original {original_consumed}"
    )

    return _unparse_cigar(result_ops)


# ---------------------------------------------------------------------------
# 3. reorder_header_records
# ---------------------------------------------------------------------------
@register_transform(
    "reorder_header_records",
    format="SAM",
    description="Shuffle SAM header lines of one type (e.g. all @SQ or all @RG lines) while keeping @HD mandatory as the first line.",
)
def reorder_header_records(
    header_lines: list[str],
    record_type: str = "@SQ",
    seed: Optional[int] = None,
) -> list[str]:
    """
    Shuffle SAM header records of a given type while keeping @HD as the
    first line (if present).

    Args:
        header_lines: List of SAM header lines (starting with @).
        record_type: The record type to shuffle, e.g. "@SQ" or "@RG".
        seed: RNG seed.

    Returns:
        Header lines with the specified record type shuffled.
    """
    rng = random.Random(seed)

    # Separate records by type, preserving order of non-target types
    target_lines: list[str] = []
    other_with_positions: list[tuple[int, str]] = []

    for i, line in enumerate(header_lines):
        tag = line.split("\t", 1)[0]
        if tag == record_type:
            target_lines.append(line)
        else:
            other_with_positions.append((i, line))

    rng.shuffle(target_lines)

    # Rebuild: @HD must be first
    result: list[str] = []
    hd_line: str | None = None
    non_hd_others: list[str] = []

    for _, line in other_with_positions:
        if line.startswith("@HD"):
            hd_line = line
        else:
            non_hd_others.append(line)

    if hd_line is not None:
        result.append(hd_line)

    # Interleave: place shuffled target records where they originally appeared
    # For simplicity, put all target records together after @HD, then the rest
    result.extend(target_lines)
    result.extend(non_hd_others)

    return result


# ---------------------------------------------------------------------------
# 4. toggle_cigar_hard_soft_clipping
# ---------------------------------------------------------------------------
@register_transform(
    "toggle_cigar_hard_soft_clipping",
    format="SAM",
    description="Convert H<->S clipping in CIGAR and synchronize SEQ/QUAL (H->S: pad dummy bases; S->H: trim those bases); used to test clipping-representation equivalence.",
)
def toggle_cigar_hard_soft_clipping(
    cigar: str,
    seq: str,
    qual: str,
    dummy_base: str = "N",
    dummy_qual: str = "!",
) -> tuple[str, str, str]:
    """
    Convert between Hard (H) and Soft (S) clipping in a CIGAR string,
    synchronizing SEQ and QUAL fields.

    H -> S: Prepend/append dummy bases and quality values.
    S -> H: Truncate the corresponding bases from SEQ and QUAL.

    Args:
        cigar: CIGAR string.
        seq: SEQ field.
        qual: QUAL field.
        dummy_base: Base character to insert for H->S conversion.
        dummy_qual: Quality character to insert for H->S conversion.

    Returns:
        Tuple of (new_cigar, new_seq, new_qual).
    """
    ops = _parse_cigar(cigar)
    new_ops: list[tuple[int, str]] = []
    prepend_bases = 0
    append_bases = 0
    trim_front = 0
    trim_back = 0

    for i, (length, op) in enumerate(ops):
        is_leading = i == 0
        is_trailing = i == len(ops) - 1

        if op == "H":
            # H -> S: mark how many dummy bases to add
            new_ops.append((length, "S"))
            if is_leading:
                prepend_bases += length
            elif is_trailing:
                append_bases += length
        elif op == "S":
            # S -> H: mark how many bases to trim
            new_ops.append((length, "H"))
            if is_leading:
                trim_front += length
            elif is_trailing:
                trim_back += length
        else:
            new_ops.append((length, op))

    # Apply SEQ/QUAL modifications
    new_seq = seq
    new_qual = qual

    if prepend_bases > 0:
        new_seq = dummy_base * prepend_bases + new_seq
        new_qual = dummy_qual * prepend_bases + new_qual
    if append_bases > 0:
        new_seq = new_seq + dummy_base * append_bases
        new_qual = new_qual + dummy_qual * append_bases
    if trim_front > 0:
        new_seq = new_seq[trim_front:]
        new_qual = new_qual[trim_front:]
    if trim_back > 0:
        new_seq = new_seq[:-trim_back]
        new_qual = new_qual[:-trim_back]

    return _unparse_cigar(new_ops), new_seq, new_qual


# ---------------------------------------------------------------------------
# Phase 2 of SAM coverage plan — 5 new semantics-preserving header transforms.
#
# Each shuffles TAG:VALUE pairs WITHIN a header line of a given type. The
# SAMv1 spec §1.3 does not impose an order on the TAG:VALUE pairs inside
# @HD/@SQ/@RG/@PG, so permutation preserves semantics. The canonicalizer
# in test_engine/canonical/sam_normalizer.py now sorts header-subtag dicts
# (see _parse_tag_fields), so these MRs produce byte-identical canonical
# JSON on any conformant parser — the metamorphic oracle passes.
# ---------------------------------------------------------------------------


def _split_hd_line(line: str) -> tuple[str, list[str]]:
    """Return (record_tag, [tag:value, ...]) for a single header line."""
    parts = line.rstrip("\r\n").split("\t")
    return parts[0], parts[1:]


def _rebuild_header_line(tag: str, kv_fields: list[str]) -> str:
    """Reconstruct a header line preserving trailing-newline absence."""
    return "\t".join([tag, *kv_fields])


def _shuffle_subtags_of_record_type(
    header_lines: list[str],
    record_type: str,
    seed: Optional[int],
) -> list[str]:
    """Return a copy of `header_lines` with TAG:VALUE pairs shuffled
    within every line whose record tag matches `record_type`.

    Lines of other types (including @HD ordering and @CO text) are left
    byte-identical. Line-level order is preserved; only intra-line field
    ordering changes. Callers use this helper to implement the five
    Phase 2 subtag-shuffle transforms.
    """
    rng = random.Random(seed)
    out: list[str] = []
    for line in header_lines:
        tag, kv = _split_hd_line(line)
        if tag != record_type or len(kv) <= 1:
            out.append(line)
            continue
        shuffled = list(kv)
        rng.shuffle(shuffled)
        out.append(_rebuild_header_line(tag, shuffled))
    return out


# ---------------------------------------------------------------------------
# 5. shuffle_hd_subtags
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_hd_subtags",
    format="SAM",
    description=(
        "Shuffle the TAG:VALUE pairs INSIDE the @HD header line "
        "(e.g. `VN:1.6\\tSO:coordinate\\tGO:none` -> `GO:none\\tVN:1.6\\tSO:coordinate`). "
        "SAMv1 §1.3 does not order these pairs, so this is semantics-"
        "preserving; the canonical normalizer sorts them so the oracle "
        "passes for conformant parsers."
    ),
    preconditions=("has_hd_line",),
)
def shuffle_hd_subtags(
    header_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Permute TAG:VALUE pairs within the @HD header line."""
    return _shuffle_subtags_of_record_type(header_lines, "@HD", seed)


# ---------------------------------------------------------------------------
# 6. shuffle_sq_record_subtags
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_sq_record_subtags",
    format="SAM",
    description=(
        "Independently shuffle the TAG:VALUE pairs INSIDE each @SQ "
        "reference-sequence record (e.g. `SN:chr1\\tLN:248956422\\tM5:abc` "
        "-> `M5:abc\\tLN:248956422\\tSN:chr1`). Preserves @SQ line order — "
        "only intra-line field order changes. SAMv1 §1.3 leaves this "
        "unconstrained."
    ),
    preconditions=("has_sq_line",),
)
def shuffle_sq_record_subtags(
    header_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Permute TAG:VALUE pairs within every @SQ header record."""
    return _shuffle_subtags_of_record_type(header_lines, "@SQ", seed)


# ---------------------------------------------------------------------------
# 7. shuffle_rg_record_subtags
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_rg_record_subtags",
    format="SAM",
    description=(
        "Independently shuffle the TAG:VALUE pairs INSIDE each @RG "
        "read-group record (e.g. `ID:sample1\\tLB:libA\\tSM:subject1` -> "
        "`SM:subject1\\tID:sample1\\tLB:libA`). Preserves @RG line order; "
        "only intra-line field order changes."
    ),
    preconditions=("has_rg_line",),
)
def shuffle_rg_record_subtags(
    header_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Permute TAG:VALUE pairs within every @RG header record."""
    return _shuffle_subtags_of_record_type(header_lines, "@RG", seed)


# ---------------------------------------------------------------------------
# 8. shuffle_pg_record_subtags
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_pg_record_subtags",
    format="SAM",
    description=(
        "Independently shuffle the TAG:VALUE pairs INSIDE each @PG "
        "program record (e.g. `ID:bwa\\tPN:bwa\\tVN:0.7.17\\tPP:samtools` "
        "-> `PP:samtools\\tID:bwa\\tVN:0.7.17\\tPN:bwa`). Preserves @PG "
        "line order so PP parent-program pointers remain valid; only "
        "intra-line field order changes."
    ),
    preconditions=("has_pg_line",),
)
def shuffle_pg_record_subtags(
    header_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Permute TAG:VALUE pairs within every @PG header record."""
    return _shuffle_subtags_of_record_type(header_lines, "@PG", seed)


# ---------------------------------------------------------------------------
# 9. shuffle_co_comments
# ---------------------------------------------------------------------------
@register_transform(
    "shuffle_co_comments",
    format="SAM",
    description=(
        "Shuffle the order of @CO comment lines within the header. "
        "SAMv1 §1.3 declares @CO to be free-text comments with no "
        "ordering semantics; the canonical normalizer sorts them, so "
        "this MR passes deterministically on conformant parsers."
    ),
    preconditions=("has_co_lines",),
)
def shuffle_co_comments(
    header_lines: list[str],
    seed: Optional[int] = None,
) -> list[str]:
    """Shuffle @CO lines while leaving every other header line's order
    (and every non-@CO line) byte-identical."""
    rng = random.Random(seed)
    co_indices = [i for i, ln in enumerate(header_lines) if ln.startswith("@CO")]
    if len(co_indices) < 2:
        return list(header_lines)
    co_lines = [header_lines[i] for i in co_indices]
    rng.shuffle(co_lines)
    out = list(header_lines)
    for pos, new_line in zip(co_indices, co_lines):
        out[pos] = new_line
    return out


# ---------------------------------------------------------------------------
# Phase 3 of SAM coverage plan — cross-format round-trip MRs via htslib.
#
# The samtools CLI is the canonical SAM↔BAM↔CRAM reference implementation.
# These transforms pipe the SAM seed through a binary codec (BAM or CRAM)
# and back to text SAM, exercising binary code paths that the text-SAM
# oracle never reaches. Gated at runtime: if `samtools` is not on PATH,
# the transforms_menu filter hides the MRs from the LLM prompt so no
# wasted mining.
#
# Analogue of the existing `vcf_bcf_round_trip` VCF transform; zero
# per-SUT code changes required.
# ---------------------------------------------------------------------------


def _samtools_binary() -> Optional[str]:
    """Return the samtools CLI path, or None if not installed."""
    return shutil.which("samtools")


def _run_samtools(
    args: list[str],
    stdin: Optional[bytes] = None,
    timeout_s: float = 30.0,
) -> tuple[int, bytes, str]:
    """Invoke `samtools <args>`, return (returncode, stdout, stderr).

    Dedicated helper so the round-trip transforms share cmd-line
    handling (-@ thread count, timeout policy, stderr capture).
    """
    binary = _samtools_binary()
    if not binary:
        raise RuntimeError("samtools CLI not on PATH — runtime precondition should have gated this")
    proc = subprocess.run(
        [binary, *args],
        input=stdin,
        capture_output=True,
        timeout=timeout_s,
    )
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", errors="replace")


@register_transform(
    "sam_bam_round_trip",
    format="SAM",
    description=(
        "Pipe the SAM seed through `samtools view -b | samtools view -h` "
        "so it transits the BAM binary codec and comes back to text SAM. "
        "Exercises the BAM writer + BAM reader code paths in every SUT's "
        "full `parse` flow (pysam/htsjdk that support BAM natively; "
        "text-only parsers like biopython still observe whatever samtools "
        "canonicalizes on the return trip). Analogue of VCF's "
        "`vcf_bcf_round_trip`."
    ),
    preconditions=("samtools_available",),
)
def sam_bam_round_trip(
    file_lines: list[str],
    seed: Optional[int] = None,
    timeout_s: float = 30.0,
) -> list[str]:
    """Round-trip the SAM seed through BAM via samtools.

    Writes input to a temp .sam, encodes to .bam, decodes back to SAM
    text, and returns the result as `list[str]` (with trailing newlines,
    matching the other line-level transforms' output shape).
    """
    if not _samtools_binary():
        # Runtime-precondition filter should have prevented the MR from
        # being mined, but fall back gracefully to a no-op if somehow we
        # reached here without samtools.
        logger.debug("sam_bam_round_trip: samtools unavailable — no-op")
        return list(file_lines)

    with tempfile.TemporaryDirectory(prefix="biotest_sam_bam_") as tmp:
        tmp_path = Path(tmp)
        in_sam = tmp_path / "input.sam"
        bam_path = tmp_path / "roundtrip.bam"
        out_sam = tmp_path / "output.sam"

        in_sam.write_text("".join(file_lines), encoding="utf-8")

        # SAM → BAM (--no-PG so samtools doesn't add its own @PG record
        # and thereby change canonical output byte-for-byte).
        rc1, _, err1 = _run_samtools(
            ["view", "-b", "--no-PG", "-o", str(bam_path), str(in_sam)],
            timeout_s=timeout_s,
        )
        if rc1 != 0:
            logger.debug("sam_bam_round_trip: SAM->BAM failed (rc=%s): %s", rc1, err1.strip())
            return list(file_lines)

        # BAM → SAM text, preserving @HD/@SQ/@RG/@PG via -h.
        rc2, sam_bytes, err2 = _run_samtools(
            ["view", "-h", "--no-PG", str(bam_path)],
            timeout_s=timeout_s,
        )
        if rc2 != 0:
            logger.debug("sam_bam_round_trip: BAM->SAM failed (rc=%s): %s", rc2, err2.strip())
            return list(file_lines)

        text = sam_bytes.decode("utf-8", errors="replace")
        # Splitlines with keepends so downstream writers don't double-\n
        return text.splitlines(keepends=True)


@register_transform(
    "sam_cram_round_trip",
    format="SAM",
    description=(
        "Pipe the SAM seed through `samtools view -C -T ref.fa` and back "
        "so it transits the CRAM binary codec. Requires a committed toy "
        "reference (seeds/ref/toy.fa) whose @SQ SN names match the seed's. "
        "Bonfield CRAM 3.1 2022 documents lossy edges (=/X collapsed to M, "
        "NM/MD recompute) — the oracle accounts for those via the canonical "
        "normalizer's `cram_safe` mode."
    ),
    preconditions=(
        "samtools_available",
        "cram_reference_available",
    ),
)
def sam_cram_round_trip(
    file_lines: list[str],
    seed: Optional[int] = None,
    timeout_s: float = 30.0,
) -> list[str]:
    """Round-trip the SAM seed through CRAM via samtools + toy reference.

    If the seed's @SQ SN names are not covered by the toy reference
    (seeds/ref/toy.fa), the transform is a no-op — the framework's
    quarantine logic auto-demotes MRs that always no-op, so bad seed/ref
    pairings correct themselves.
    """
    if not _samtools_binary():
        logger.debug("sam_cram_round_trip: samtools unavailable — no-op")
        return list(file_lines)

    # Resolve the toy reference relative to project root (the runner
    # can't pass absolute paths through dispatch; hard-code the committed
    # fixture path).
    repo_root = Path(__file__).resolve().parent.parent.parent
    ref_fa = repo_root / "seeds" / "ref" / "toy.fa"
    if not ref_fa.exists():
        logger.debug("sam_cram_round_trip: toy reference missing — no-op")
        return list(file_lines)

    # Collect seed's @SQ SN names so we can short-circuit if none of
    # them live in the reference (avoids a guaranteed-failure samtools
    # invocation).
    ref_names = _parse_fasta_names(ref_fa)
    sq_names_in_seed: list[str] = []
    for ln in file_lines:
        stripped = ln.rstrip("\r\n")
        if not stripped.startswith("@SQ"):
            continue
        for field in stripped.split("\t"):
            if field.startswith("SN:"):
                sq_names_in_seed.append(field[3:])
                break
    if sq_names_in_seed and not any(n in ref_names for n in sq_names_in_seed):
        logger.debug(
            "sam_cram_round_trip: seed @SQ names %r not in toy reference — no-op",
            sq_names_in_seed,
        )
        return list(file_lines)

    with tempfile.TemporaryDirectory(prefix="biotest_sam_cram_") as tmp:
        tmp_path = Path(tmp)
        in_sam = tmp_path / "input.sam"
        cram_path = tmp_path / "roundtrip.cram"
        in_sam.write_text("".join(file_lines), encoding="utf-8")

        rc1, _, err1 = _run_samtools(
            [
                "view", "-C", "--no-PG",
                "-T", str(ref_fa),
                "-o", str(cram_path),
                str(in_sam),
            ],
            timeout_s=timeout_s,
        )
        if rc1 != 0:
            logger.debug("sam_cram_round_trip: SAM->CRAM failed (rc=%s): %s", rc1, err1.strip())
            return list(file_lines)

        rc2, sam_bytes, err2 = _run_samtools(
            [
                "view", "-h", "--no-PG",
                "-T", str(ref_fa),
                str(cram_path),
            ],
            timeout_s=timeout_s,
        )
        if rc2 != 0:
            logger.debug("sam_cram_round_trip: CRAM->SAM failed (rc=%s): %s", rc2, err2.strip())
            return list(file_lines)

        text = sam_bytes.decode("utf-8", errors="replace")
        return text.splitlines(keepends=True)


def _parse_fasta_names(fa_path: Path) -> set[str]:
    """Return the set of sequence names (header text after '>') in a
    FASTA file. Parses the header line only — does not load sequences."""
    names: set[str] = set()
    try:
        with fa_path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith(">"):
                    name = line[1:].split()[0].strip()
                    if name:
                        names.add(name)
    except OSError:
        pass
    return names
