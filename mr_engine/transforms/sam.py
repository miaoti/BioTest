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


# ---------------------------------------------------------------------------
# Phase 4 of SAM coverage plan — record-level metamorphic transforms targeting
# Picard validation rules and SAMv1 spec invariants for unmapped/unpaired
# reads, SEQ-case normalization, CIGAR zero-op cleanup, and CIGAR M ↔ =/X
# canonicalization (with NM tag recomputation).
#
# Each transform here operates on a single SAM alignment line (or a CIGAR
# string for the pure-CIGAR case) and is wrapped in dispatch.py to iterate
# the non-header lines of the seed file. All transforms are written to be
# byte-identity safe on no-op inputs.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 12. normalize_unmapped_record_fields
# ---------------------------------------------------------------------------
@register_transform(
    "normalize_unmapped_record_fields",
    format="SAM",
    description=(
        "When FLAG bit 0x4 (unmapped) is set, normalize MAPQ to the "
        "spec-defined sentinel 255 (\"not available\"). RNAME/POS/CIGAR "
        "are left untouched — SAMv1 §1.4 says \"no assumptions can be "
        "made\" but does not mandate they be invalidated. Targets "
        "Picard's INVALID_MAPPING_QUALITY validation rule."
    ),
    preconditions=("has_unmapped_reads",),
)
def normalize_unmapped_record_fields(sam_line: str) -> str:
    """Normalize MAPQ to 255 (sentinel "not available") for unmapped reads.

    SAMv1 §1.4 p47: "Bit 0x4 is the only reliable place to tell whether
    the read is unmapped. If 0x4 is set, no assumptions can be made about
    RNAME, POS, CIGAR, MAPQ, and bits 0x2, 0x100, 0x800."
    SAMv1 §1.4.5: MAPQ=255 is the spec-defined sentinel for "not available".

    Args:
        sam_line: A single tab-separated SAM alignment line (no @ prefix).

    Returns:
        The same line with MAPQ canonicalized when applicable; byte-identical
        on no-op (mapped read, MAPQ already 0/255, malformed, or header).
    """
    if sam_line.startswith("@"):
        return sam_line
    # Preserve trailing newline
    trailing = ""
    body = sam_line
    if body.endswith("\r\n"):
        trailing = "\r\n"
        body = body[:-2]
    elif body.endswith("\n"):
        trailing = "\n"
        body = body[:-1]

    cols = body.split("\t")
    if len(cols) < 11:
        return sam_line

    try:
        flag = int(cols[1])
    except (ValueError, IndexError):
        return sam_line

    if (flag & 0x4) == 0:
        return sam_line  # mapped read, no normalization needed

    try:
        mapq = int(cols[4])
    except (ValueError, IndexError):
        return sam_line

    if mapq == 0 or mapq == 255:
        return sam_line  # already canonical

    cols[4] = "255"
    return "\t".join(cols) + trailing


# ---------------------------------------------------------------------------
# 13. strip_mate_flags_if_unpaired
# ---------------------------------------------------------------------------
@register_transform(
    "strip_mate_flags_if_unpaired",
    format="SAM",
    description=(
        "When FLAG bit 0x1 (multiple segments) is unset, clear the "
        "mate-context bits 0x2, 0x8, 0x20, 0x40, 0x80. SAMv1 §1.4 p47: "
        "these bits are only meaningful when 0x1 is set. Targets "
        "Picard's INVALID_FLAG_PROPER_PAIR / FIRST_OF_PAIR / "
        "SECOND_OF_PAIR / MATES_ARE_SAME_END validation rules."
    ),
)
def strip_mate_flags_if_unpaired(sam_line: str) -> str:
    """Clear bits 0x2/0x8/0x20/0x40/0x80 when the read is not paired (0x1 unset).

    SAMv1 §1.4 p47: "Bits 0x2, 0x8, 0x20, 0x40, 0x80 are only meaningful
    when 0x1 (multiple segments) is set."

    Args:
        sam_line: A single tab-separated SAM alignment line.

    Returns:
        The line with mate-context bits cleared when 0x1 is unset; byte-
        identical on no-op (paired read, malformed, or header).
    """
    if sam_line.startswith("@"):
        return sam_line
    trailing = ""
    body = sam_line
    if body.endswith("\r\n"):
        trailing = "\r\n"
        body = body[:-2]
    elif body.endswith("\n"):
        trailing = "\n"
        body = body[:-1]

    cols = body.split("\t")
    if len(cols) < 11:
        return sam_line

    try:
        flag = int(cols[1])
    except (ValueError, IndexError):
        return sam_line

    if (flag & 0x1) != 0:
        return sam_line  # paired — mate flags are meaningful

    keep_mask = ~(0x2 | 0x8 | 0x20 | 0x40 | 0x80)
    new_flag = flag & keep_mask
    if new_flag == flag:
        return sam_line  # already clean

    cols[1] = str(new_flag)
    return "\t".join(cols) + trailing


# ---------------------------------------------------------------------------
# 14. normalize_seq_case
# ---------------------------------------------------------------------------
@register_transform(
    "normalize_seq_case",
    format="SAM",
    description=(
        "Uppercase the SEQ field (column 9) of a SAM alignment line. "
        "SAMv1 §1.4.10 (SEQ): \"No assumptions can be made on the letter "
        "cases\" — the regex permits both upper and lower case. No-op when "
        "SEQ is the missing-value sentinel '*'."
    ),
)
def normalize_seq_case(sam_line: str) -> str:
    """Uppercase the SEQ column of a SAM alignment line.

    SAMv1 §1.4.10: SEQ regex permits both cases; uppercasing is a
    semantics-preserving canonicalization.

    Args:
        sam_line: A single tab-separated SAM alignment line.

    Returns:
        The line with SEQ uppercased when applicable; byte-identical on
        no-op (SEQ='*', too few columns, or header).
    """
    if sam_line.startswith("@"):
        return sam_line
    trailing = ""
    body = sam_line
    if body.endswith("\r\n"):
        trailing = "\r\n"
        body = body[:-2]
    elif body.endswith("\n"):
        trailing = "\n"
        body = body[:-1]

    cols = body.split("\t")
    if len(cols) < 10:
        return sam_line

    seq = cols[9]
    if seq == "*":
        return sam_line  # missing value, no-op

    new_seq = seq.upper()
    if new_seq == seq:
        return sam_line

    cols[9] = new_seq
    return "\t".join(cols) + trailing


# ---------------------------------------------------------------------------
# 15. cigar_zero_length_op_removal
# ---------------------------------------------------------------------------
@register_transform(
    "cigar_zero_length_op_removal",
    format="SAM",
    description=(
        "Strip zero-length CIGAR ops and merge any newly-adjacent ops of "
        "the same type. SAMv1 §1.4.6 doesn't forbid 0-length ops but the "
        "SAM Recommended Practice (p134) says \"adjacent CIGAR operations "
        "should be different\". htsjdk normalizes 0-length ops away "
        "internally — this transform makes that canonicalization explicit."
    ),
    preconditions=("has_cigar",),
)
def cigar_zero_length_op_removal(cigar: str) -> str:
    """Remove zero-length CIGAR ops then merge any newly-adjacent same ops.

    Pure CIGAR-string transform; doesn't touch SEQ/QUAL. Total
    query-consumed length is preserved (zero-length ops consume nothing).

    Args:
        cigar: CIGAR string like "5M0D5M" or "0H10M2I0M3S".

    Returns:
        Cleaned + merged CIGAR string. "*" passes through unchanged.

    Raises:
        AssertionError: If query-consumed length changes (should never
            happen — zero-length ops consume zero bases by definition).
    """
    if cigar == "*" or not cigar:
        return cigar

    ops = _parse_cigar(cigar)
    original_consumed = _query_consumed(ops)

    # Strip zeros
    nonzero = [(length, op) for length, op in ops if length > 0]

    # Merge adjacent same ops (lifted from split_or_merge_adjacent_cigar_ops
    # mode="merge")
    merged: list[tuple[int, str]] = []
    for length, op in nonzero:
        if merged and merged[-1][1] == op:
            merged[-1] = (merged[-1][0] + length, op)
        else:
            merged.append((length, op))

    assert _query_consumed(merged) == original_consumed, (
        f"CIGAR invariant violated: consumed {_query_consumed(merged)} "
        f"!= original {original_consumed}"
    )

    return _unparse_cigar(merged)


# ---------------------------------------------------------------------------
# 16. canonicalize_cigar_match_operators
# ---------------------------------------------------------------------------
def _parse_md_tokens(md: str) -> Optional[list[tuple[str, object]]]:
    """Parse an MD-tag value into a list of tokens.

    Tokens are:
      ("match", int)     -- N matched bases
      ("mismatch", str)  -- one ref base that mismatches the read
      ("delete", str)    -- deletion-from-reference; the str is the deleted bases

    Returns None on parse error (caller must no-op).
    """
    # MD spec regex: [0-9]+(([A-Z]|\^[A-Z]+)[0-9]+)*
    # We accept zero-length numeric runs because tools commonly emit "0A0"
    # to denote two adjacent mismatches.
    pos = 0
    tokens: list[tuple[str, object]] = []
    n = len(md)
    while pos < n:
        c = md[pos]
        if c.isdigit():
            j = pos
            while j < n and md[j].isdigit():
                j += 1
            try:
                tokens.append(("match", int(md[pos:j])))
            except ValueError:
                return None
            pos = j
        elif c == "^":
            j = pos + 1
            if j >= n or not md[j].isalpha():
                return None
            while j < n and md[j].isalpha():
                j += 1
            tokens.append(("delete", md[pos + 1:j]))
            pos = j
        elif c.isalpha():
            tokens.append(("mismatch", c))
            pos += 1
        else:
            return None
    return tokens


@register_transform(
    "canonicalize_cigar_match_operators",
    format="SAM",
    description=(
        "Rewrite each M (match-or-mismatch) op as a sequence of '=' "
        "(match) and 'X' (mismatch) ops by walking the MD tag. After "
        "rewriting CIGAR, recompute the NM tag (mismatch bases + indel "
        "bases per SAMv1 §1.4.6 / SAMtags). No-op when CIGAR has no M "
        "ops, MD tag is absent, or MD parsing fails."
    ),
    preconditions=("has_md_tag", "has_cigar_m_ops"),
)
def canonicalize_cigar_match_operators(sam_line: str) -> str:
    """Replace CIGAR M ops with '=' / 'X' runs driven by the MD tag.

    Walks MD tokens in lockstep with each CIGAR M op, emitting a run of
    '=' for matched bases and 'X' for mismatched ones. D ops consume one
    ^XXX MD deletion token whose letter count must equal the D-op length.
    All other ops pass through unchanged.

    After rewriting, if an NM tag is present, recompute its value as
    (sum of X-op lengths) + (sum of I-op + D-op lengths) per SAMv1.

    Args:
        sam_line: A single tab-separated SAM alignment line.

    Returns:
        Line with M ops canonicalized to '='/'X' and NM updated; byte-
        identical on any precondition failure (no MD tag, no M ops,
        malformed MD, MD coverage mismatch, header line, < 11 cols).
    """
    if sam_line.startswith("@"):
        return sam_line

    trailing = ""
    body = sam_line
    if body.endswith("\r\n"):
        trailing = "\r\n"
        body = body[:-2]
    elif body.endswith("\n"):
        trailing = "\n"
        body = body[:-1]

    cols = body.split("\t")
    if len(cols) < 11:
        return sam_line

    cigar = cols[5]
    if cigar == "*":
        return sam_line

    # Find MD tag among optional tags (cols 11+).
    md_value: Optional[str] = None
    md_col_idx: Optional[int] = None
    for i in range(11, len(cols)):
        field = cols[i]
        if field.startswith("MD:Z:"):
            md_value = field[5:]
            md_col_idx = i
            break
    if md_value is None:
        return sam_line

    # Parse CIGAR; bail on any malformed input.
    try:
        ops = _parse_cigar(cigar)
    except Exception:
        return sam_line
    # Verify the parse round-trips — catches stray characters that the
    # regex finditer silently skipped.
    if _unparse_cigar(ops) != cigar:
        return sam_line

    # No-op if there are no M ops to canonicalize.
    if not any(op == "M" for _, op in ops):
        return sam_line

    md_tokens = _parse_md_tokens(md_value)
    if md_tokens is None:
        return sam_line

    # Walk CIGAR; for each M op consume `length` reference-aligned positions
    # from MD; for each D op consume one ^XXX deletion token.
    new_ops: list[tuple[int, str]] = []
    md_idx = 0
    md_match_remaining = 0  # cursor into a numeric "match" token

    def _take_one_md_position() -> Optional[str]:
        """Advance MD by one reference-aligned position; return '=' or 'X'.
        Returns None on coverage exhaustion or malformed sequence."""
        nonlocal md_idx, md_match_remaining
        # Advance over consumed match tokens / mismatch tokens.
        while md_idx < len(md_tokens):
            kind, val = md_tokens[md_idx]
            if kind == "match":
                if md_match_remaining == 0:
                    md_match_remaining = int(val)  # type: ignore[arg-type]
                if md_match_remaining > 0:
                    md_match_remaining -= 1
                    if md_match_remaining == 0:
                        md_idx += 1
                    return "="
                # Zero-length match: skip token.
                md_idx += 1
                continue
            if kind == "mismatch":
                md_idx += 1
                return "X"
            # Hitting a delete token mid-M op is a coverage mismatch.
            return None
        return None

    for length, op in ops:
        if op == "M":
            run: list[str] = []
            for _ in range(length):
                eq_or_x = _take_one_md_position()
                if eq_or_x is None:
                    return sam_line  # MD exhausted / malformed -> no-op
                run.append(eq_or_x)
            # Compress consecutive identical chars into runs.
            cur_char = run[0]
            cur_len = 1
            for ch in run[1:]:
                if ch == cur_char:
                    cur_len += 1
                else:
                    new_ops.append((cur_len, cur_char))
                    cur_char = ch
                    cur_len = 1
            new_ops.append((cur_len, cur_char))
        elif op == "D":
            # Flush any pending zero-length match token.
            if md_idx < len(md_tokens) and md_tokens[md_idx][0] == "match" and md_match_remaining == 0:
                if md_tokens[md_idx][1] == 0:
                    md_idx += 1
            if md_match_remaining != 0:
                return sam_line  # in-progress match shouldn't cross a D
            if md_idx >= len(md_tokens):
                return sam_line
            kind, val = md_tokens[md_idx]
            if kind != "delete" or len(val) != length:  # type: ignore[arg-type]
                return sam_line
            md_idx += 1
            new_ops.append((length, op))
        else:
            new_ops.append((length, op))

    # Trailing zero-length match token is acceptable.
    if md_idx < len(md_tokens):
        if md_tokens[md_idx][0] == "match" and md_match_remaining == 0 and md_tokens[md_idx][1] == 0:
            md_idx += 1
    if md_match_remaining != 0 or md_idx != len(md_tokens):
        return sam_line  # MD content didn't sum to op coverage

    new_cigar = _unparse_cigar(new_ops)

    # Recompute NM if present: NM = X-bases + indel-bases.
    new_nm_value: Optional[int] = None
    nm_col_idx: Optional[int] = None
    for i in range(11, len(cols)):
        if cols[i].startswith("NM:i:"):
            nm_col_idx = i
            break
    if nm_col_idx is not None:
        new_nm_value = sum(l for l, op in new_ops if op == "X") + sum(
            l for l, op in new_ops if op in ("I", "D")
        )

    cols[5] = new_cigar
    if nm_col_idx is not None and new_nm_value is not None:
        cols[nm_col_idx] = f"NM:i:{new_nm_value}"

    return "\t".join(cols) + trailing


# ---------------------------------------------------------------------------
# Round 2 — additional SAM record/header-level transforms.
#
# These three were identified in the prior MT/MR research dossier (Sec 5
# "Recommended additions beyond the 8") + Tier 2 (deferred); each carries
# direct SAM v1 spec backing.
#
# Goal: close the residual gap between BioTest's MR-driven coverage and
# the SOTA coverage-guided baselines (jazzer, atheris, libfuzzer) on SAM.
# ---------------------------------------------------------------------------

# Ops that consume reference (ref_consume_length) — used by the bound check
# in pos_shift_with_sq_ln_bound_check.
_REF_CONSUMING = {"M", "D", "N", "=", "X"}


def _ref_consumed_from_cigar_str(cigar: str) -> int:
    """Total reference bases consumed by a CIGAR string. '*' returns 0.

    Per SAM v1 §1.4.6, ops M/D/N/=/X consume reference bases. Used for
    POS+CIGAR vs LN bound checking.
    """
    if cigar == "*" or not cigar:
        return 0
    total = 0
    for m in re.finditer(r"(\d+)([MIDNSHP=X])", cigar):
        if m.group(2) in _REF_CONSUMING:
            total += int(m.group(1))
    return total


# ---------------------------------------------------------------------------
# 16. pos_shift_with_sq_ln_bound_check
# ---------------------------------------------------------------------------
@register_transform(
    "pos_shift_with_sq_ln_bound_check",
    format="SAM",
    description=(
        "Shift every alignment record's POS by +shift AND increase the "
        "matching @SQ LN by +shift. Bound-check: if any record's "
        "POS + CIGAR_ref_consume would exceed the new LN, no-op. "
        "POS=0 (unmapped per SAMv1 §1.4) and RNAME='*' records are "
        "skipped. Spec backing: SAMv1 §1.4.4 (POS) + §1.3 (@SQ LN range "
        "[1, 2^31-1]) + Picard `SAMValidationError.CIGAR_MAPS_OFF_REFERENCE` "
        "validates POS+ref_consume <= LN. Exercises the POS-against-LN "
        "validation path that other text-only MRs do not reach."
    ),
    preconditions=("has_sq_with_ln",),
)
def pos_shift_with_sq_ln_bound_check(
    file_lines: list[str],
    shift: int = 1000,
) -> list[str]:
    """Shift all alignment POS by +shift; widen @SQ LN by +shift.

    Args:
        file_lines: list of SAM file lines (header + alignments).
        shift: positive integer shift in bp. Default 1000.

    Returns:
        List of lines with shifted POS / widened LN, OR a copy of
        the input unchanged if any record's new POS would push the
        alignment past the widened LN. Always returns a fresh list
        (never mutates input).

    Edge handling:
        - Records with POS=0 OR RNAME='*' are skipped (unmapped).
        - Records whose RNAME is not in the @SQ table are left alone
          (the bound check has nothing to compare against).
        - LN values that exceed SAMv1's [1, 2^31-1] range cap the no-op
          gate.
        - shift=0 returns a fresh copy of the input.
    """
    if shift == 0:
        return list(file_lines)
    if shift < 0:
        raise ValueError(f"shift must be non-negative, got {shift}")

    sq_lns: dict[str, int] = {}
    sq_line_indices: list[int] = []
    for i, line in enumerate(file_lines):
        stripped = line.rstrip("\r\n")
        if not stripped.startswith("@SQ\t"):
            continue
        sq_line_indices.append(i)
        sn = ln = None
        for f in stripped.split("\t")[1:]:
            if f.startswith("SN:"):
                sn = f[3:]
            elif f.startswith("LN:"):
                try:
                    ln = int(f[3:])
                except ValueError:
                    ln = None
        if sn is not None and ln is not None and ln > 0:
            sq_lns[sn] = ln

    if not sq_lns:
        return list(file_lines)

    # Bound check every mapped record. If any would overflow new LN, no-op.
    record_indices: list[tuple[int, list[str]]] = []
    for i, line in enumerate(file_lines):
        stripped = line.rstrip("\r\n")
        if stripped.startswith("@") or "\t" not in stripped:
            continue
        cols = stripped.split("\t")
        if len(cols) < 11:
            continue
        rname = cols[2]
        try:
            pos = int(cols[3])
        except ValueError:
            continue
        if pos == 0 or rname == "*":
            continue  # unmapped — POS is irrelevant per SAMv1 §1.4
        if rname not in sq_lns:
            continue  # unknown ref — leave alone, no bound to check
        ref_consume = _ref_consumed_from_cigar_str(cols[5])
        new_ln = sq_lns[rname] + shift
        if new_ln > (2**31 - 1):
            return list(file_lines)  # would exceed SAMv1 LN range
        new_pos = pos + shift
        # SAMv1 spec implication: alignment occupies [POS, POS+ref_consume-1]
        # (1-based inclusive). Must be <= LN.
        if ref_consume > 0 and new_pos + ref_consume - 1 > new_ln:
            return list(file_lines)
        record_indices.append((i, cols))

    # All checks passed — widen @SQ LN unconditionally (LN is independent of
    # records; widening it just states "the reference is at least this long").
    # Then shift POS only on the mapped records that survived the bound check.
    # If `record_indices` is empty (e.g. only unmapped or unknown-RNAME records),
    # we still widen LN — the file remains spec-conformant.
    result = list(file_lines)
    for sq_idx in sq_line_indices:
        line = result[sq_idx]
        stripped = line.rstrip("\r\n")
        trailing = line[len(stripped):]  # preserve trailing \r\n if any
        new_fields: list[str] = []
        for f in stripped.split("\t"):
            if f.startswith("LN:"):
                try:
                    ln = int(f[3:])
                    f = f"LN:{ln + shift}"
                except ValueError:
                    pass
            new_fields.append(f)
        result[sq_idx] = "\t".join(new_fields) + trailing
    for idx, cols in record_indices:
        line = result[idx]
        stripped = line.rstrip("\r\n")
        trailing = line[len(stripped):]
        cols[3] = str(int(cols[3]) + shift)
        result[idx] = "\t".join(cols) + trailing
    return result


# ---------------------------------------------------------------------------
# 17. canonicalize_rnext_equals_alias
# ---------------------------------------------------------------------------
@register_transform(
    "canonicalize_rnext_equals_alias",
    format="SAM",
    description=(
        "Toggle RNEXT between explicit RNAME and the '=' alias. "
        "mode='alias' (default): when RNEXT==RNAME and RNEXT != '*', "
        "replace RNEXT with '='. mode='explicit': when RNEXT=='=' and "
        "RNAME != '*', replace RNEXT with the literal RNAME. SAMv1 §1.4.7 "
        "explicitly allows '=' as a synonym for 'same as RNAME'. The "
        "Run-10 sam_normalizer fix already canonicalizes the explicit "
        "side (sam_normalizer.py:166-168); this transform produces text-"
        "level variations on the OTHER side so all parsers' dual-form "
        "handling is exercised."
    ),
    preconditions=(),
)
def canonicalize_rnext_equals_alias(
    sam_line: str,
    mode: str = "alias",
) -> str:
    """Toggle RNEXT '=' alias.

    Args:
        sam_line: a single SAM alignment line (no @ prefix).
        mode: "alias" → RNAME→'=' when RNEXT==RNAME; "explicit" → '='→RNAME.

    Returns:
        Modified line, or input unchanged if precondition not met. Always
        preserves the trailing newline state of the input.
    """
    if mode not in ("alias", "explicit"):
        raise ValueError(f"Invalid mode: {mode!r}. Must be 'alias' or 'explicit'.")
    stripped = sam_line.rstrip("\n")
    trailing = sam_line[len(stripped):]
    fields = stripped.split("\t")
    if len(fields) < 11:
        return sam_line
    rname = fields[2]
    rnext = fields[6]
    if mode == "alias":
        # RNEXT=RNAME (and not '*') → RNEXT='='
        if rnext != "*" and rnext == rname and rname != "*":
            fields[6] = "="
            return "\t".join(fields) + trailing
    else:  # mode == "explicit"
        # RNEXT='=' (and RNAME not '*') → RNEXT=RNAME
        if rnext == "=" and rname != "*":
            fields[6] = rname
            return "\t".join(fields) + trailing
    return sam_line


# ---------------------------------------------------------------------------
# 18. bump_hd_vn_minor
# ---------------------------------------------------------------------------
@register_transform(
    "bump_hd_vn_minor",
    format="SAM",
    description=(
        "Toggle the @HD VN field between SAM versions 1.5 and 1.6. "
        "Per the SAM v1 spec history, 1.5 -> 1.6 added clarifications "
        "but kept backwards-compatibility for files that don't use "
        "1.6-only features (none in our test corpus). Toggling exposes "
        "version-gated parser branches in SUTs that switch behavior on "
        "VN. Files without @HD or without VN are returned unchanged "
        "(no @HD added — SAMv1 only requires @HD if header is present "
        "and the file is sorted)."
    ),
    preconditions=("has_hd_vn",),
)
def bump_hd_vn_minor(header_lines: list[str]) -> list[str]:
    """Toggle @HD VN between '1.5' and '1.6'.

    Args:
        header_lines: list of header lines (each starts with '@').

    Returns:
        Fresh list with @HD VN toggled (1.5 ↔ 1.6) where applicable;
        non-@HD lines and @HD lines without VN are unchanged.
    """
    out: list[str] = []
    for line in header_lines:
        stripped = line.rstrip("\r\n")
        trailing = line[len(stripped):]
        if not stripped.startswith("@HD"):
            out.append(line)
            continue
        new_fields: list[str] = []
        toggled = False
        for f in stripped.split("\t"):
            if f.startswith("VN:"):
                v = f[3:].strip()
                if v == "1.6":
                    f = "VN:1.5"
                    toggled = True
                elif v == "1.5":
                    f = "VN:1.6"
                    toggled = True
            new_fields.append(f)
        if toggled:
            out.append("\t".join(new_fields) + trailing)
        else:
            out.append(line)
    return out
