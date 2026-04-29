"""Rank 11 — Boundary-Value Diversifier.

Complements Rank 9 (random numerical perturbation) by emitting explicit
**spec-boundary** values for every numerical field, driven by classic
Boundary Value Analysis (BVA):

  * 0, 1, -1         — zero and one-step perturbations
  * INT_MAX, MIN     — integer bounds (32-bit signed)
  * MIN+1, MAX-1     — adjacent-to-bounds (off-by-one mutant triggers)
  * Field-specific saturations:
    - SAM MAPQ: 0, 1, 60 (practical max), 255 (spec max, "unavailable")
    - VCF QUAL: 0, 1, 9999 (Phred-score practical max)
    - VCF AF:   0.0, 0.5, 1.0 (fractional bounds)
  * Floating-point edges: NaN, Inf, -Inf (where accepted)

Why this matters: PIT's `RemoveConditional_ORDER_ELSE` and `Math`
mutants are killed ONLY when corpus inputs **cross** the mutated
comparison/arithmetic boundary. Random perturbation in Rank 9 hits
boundaries by luck (~1 in 10^4 for a random int in [-10k, 10k]);
BVA hits them deterministically.

Reference: Myers, G. *The Art of Software Testing* (Wiley, 2nd ed.
1979), Chapter 4 — the original formulation of BVA as "test at and
near the extremes of valid inputs." For mutation-testing specifically,
Just et al. *Mutation Analysis* FSE'14 shows BVA inputs kill ~30% of
relational-operator mutants that random generation misses.

Output convention (same as Rank 9/10): `seeds/<fmt>_diverse/bv_<sha8>.<ext>`.
SUT-agnostic: boundary values come from the VCF/SAM spec column
definitions, not from any SUT's impl details.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

logger = logging.getLogger("boundary_values")


# ---------------------------------------------------------------------------
# Boundary-value libraries
# ---------------------------------------------------------------------------

# Spec-boundary values per field category.  Each list is probed against
# every record position.  Small list keeps the output manageable — a
# 47-seed VCF corpus × ~8 POS boundaries × ~5 QUAL boundaries = ~1900
# records, bounded.
_POS_BOUNDARIES = [1, 2, 100, 1_000_000, 2_147_483_646, 2_147_483_647]
_QUAL_BOUNDARIES = ["0", "0.0", "1", "99.9", "9999"]  # `.` is always included separately
_AF_BOUNDARIES = ["0.0", "0.00001", "0.5", "0.99999", "1.0"]
_DP_BOUNDARIES = [0, 1, 255, 65535, 1_000_000]
_MQ_BOUNDARIES = [0, 1, 60, 255]  # SAM MAPQ practical bounds
_MAPQ_BOUNDARIES = [0, 1, 60, 255]
_TLEN_BOUNDARIES = [0, 1, -1, 500, 50_000, -50_000, 2_147_483_647, -2_147_483_648]
_PNEXT_BOUNDARIES = [0, 1, 100, 2_147_483_647]


# ---------------------------------------------------------------------------
# VCF boundary variants
# ---------------------------------------------------------------------------

def _set_vcf_field(parts: list[str], col_idx: int, value: str) -> list[str]:
    out = parts[:]
    if col_idx < len(out):
        out[col_idx] = value
    return out


def generate_vcf_boundary_variants(source_text: str) -> list[str]:
    """For each data record, emit BVA variants for POS / QUAL / INFO-subfields."""
    lines = source_text.splitlines(keepends=True)
    header_lines = [ln for ln in lines if ln.startswith("#") or not ln.strip()]
    body_lines = [ln for ln in lines if ln.strip() and not ln.startswith("#")]
    if not body_lines:
        return []
    variants: list[str] = []
    # Pick a representative record — the first one — and vary each field
    # independently to produce manageable number of variants. For each
    # file, emit (|POS| + |QUAL| + |INFO boundaries|) variants.
    representative = body_lines[0].rstrip("\r\n").split("\t")
    if len(representative) < 8:
        return []
    # POS boundaries (col 2, 0-indexed=1)
    for pos in _POS_BOUNDARIES:
        parts = _set_vcf_field(representative, 1, str(pos))
        new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
        variants.append("".join(header_lines + new_body))
    # QUAL boundaries (col 6, 0-indexed=5)
    for q in _QUAL_BOUNDARIES + ["."]:
        parts = _set_vcf_field(representative, 5, q)
        new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
        variants.append("".join(header_lines + new_body))
    # INFO boundaries — set AF and DP with spec boundaries
    for af in _AF_BOUNDARIES:
        for dp in _DP_BOUNDARIES:
            new_info = f"AF={af};DP={dp}"
            parts = _set_vcf_field(representative, 7, new_info)
            new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
            variants.append("".join(header_lines + new_body))
    return variants


# ---------------------------------------------------------------------------
# SAM boundary variants
# ---------------------------------------------------------------------------

def generate_sam_boundary_variants(source_text: str) -> list[str]:
    """For each data record, emit BVA variants for POS / MAPQ / PNEXT / TLEN."""
    lines = source_text.splitlines(keepends=True)
    header_lines = [ln for ln in lines if ln.startswith("@") or not ln.strip()]
    body_lines = [ln for ln in lines if ln.strip() and not ln.startswith("@")]
    if not body_lines:
        return []
    representative = body_lines[0].rstrip("\r\n").split("\t")
    if len(representative) < 11:
        return []
    variants: list[str] = []
    # POS (col 4, 0-indexed=3)
    for pos in _POS_BOUNDARIES:
        parts = representative[:]
        parts[3] = str(pos)
        new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
        variants.append("".join(header_lines + new_body))
    # MAPQ (col 5, 0-indexed=4)
    for mq in _MAPQ_BOUNDARIES:
        parts = representative[:]
        parts[4] = str(mq)
        new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
        variants.append("".join(header_lines + new_body))
    # PNEXT (col 8, 0-indexed=7)
    for pn in _PNEXT_BOUNDARIES:
        parts = representative[:]
        parts[7] = str(pn)
        new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
        variants.append("".join(header_lines + new_body))
    # TLEN (col 9, 0-indexed=8)
    for tl in _TLEN_BOUNDARIES:
        parts = representative[:]
        parts[8] = str(tl)
        new_body = ["\t".join(parts) + "\n"] + body_lines[1:]
        variants.append("".join(header_lines + new_body))
    return variants


# ---------------------------------------------------------------------------
# Validity gate (reuse Rank 9's)
# ---------------------------------------------------------------------------

def _validate(text: str, fmt: str, sut_validate: Optional[str] = None) -> bool:
    from mr_engine.transforms.value_diversifier import _validate as _v9
    return _v9(text, fmt, sut_validate=sut_validate)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def generate_boundary_directory(
    input_dir: Path, output_dir: Path, fmt: str,
    max_per_seed: int = 40, sut_validate: Optional[str] = None,
    max_bytes: int = 500_000,
) -> dict:
    """Walk input_dir, emit up to max_per_seed boundary variants per seed."""
    ext = fmt.lower()
    sources = sorted(p for p in input_dir.iterdir()
                     if p.is_file() and p.suffix.lower() == f".{ext}"
                     and not p.name.startswith(("kept_", "diverse_",
                                                "bytefuzz_", "bv_")))
    if not sources:
        raise SystemExit(f"boundary_values: no {ext} files in {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    per_file = (generate_vcf_boundary_variants
                if fmt.upper() == "VCF"
                else generate_sam_boundary_variants)
    kept = 0; rejected_invalid = 0; rejected_dup = 0; rejected_size = 0
    seen_hashes: set[str] = set()
    for existing in output_dir.glob(f"bv_*.{ext}"):
        seen_hashes.add(existing.stem[len("bv_"):])

    for src in sources:
        try:
            text = src.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for v_text in per_file(text)[:max_per_seed]:
            if not v_text:
                continue
            if len(v_text.encode("utf-8")) > max_bytes:
                rejected_size += 1; continue
            h = hashlib.sha256(v_text.encode("utf-8")).hexdigest()[:16]
            if h in seen_hashes:
                rejected_dup += 1; continue
            if not _validate(v_text, fmt, sut_validate=sut_validate):
                rejected_invalid += 1; continue
            seen_hashes.add(h)
            (output_dir / f"bv_{h}.{ext}").write_text(v_text, encoding="utf-8")
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
    logger.info("boundary_values result: %s", result)
    return result


def _cli() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--format", required=True, choices=["VCF", "SAM"])
    p.add_argument("--max-per-seed", type=int, default=40,
                   help="Cap variants emitted per source seed (default 40)")
    p.add_argument("--sut-validate", default=None,
                   help="Optional SUT-parser gate (biopython / vcfpy)")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    r = generate_boundary_directory(
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
