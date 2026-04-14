"""
Z3 constraint models for VCF and SAM format invariants.

Used as:
1. Post-transform validation guards (reject invalid transforms)
2. Corner-case seed generation (Tier 3 seeds)
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from z3 import Int, IntVector, Solver, sat, And, Sum, Or
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False
    logger.warning("z3-solver not available; Z3 constraints will be skipped")


def check_cigar_seq_constraint(
    cigar_ops: list[tuple[int, str]],
    seq_len: int,
) -> bool:
    """
    Verify: sum(query_consuming_ops) == len(SEQ).

    Query-consuming ops: M, I, S, =, X.
    This is a post-condition check after transforms that modify CIGAR.

    Returns True if the constraint is satisfied.
    """
    if not Z3_AVAILABLE:
        # Fall back to simple Python check
        query_consuming = {"M", "I", "S", "=", "X"}
        consumed = sum(length for length, op in cigar_ops if op in query_consuming)
        return consumed == seq_len

    s = Solver()
    ops = IntVector("ops", len(cigar_ops))
    for i, (length, op) in enumerate(cigar_ops):
        s.add(ops[i] == length)
    query_consuming_ops = {"M", "I", "S", "=", "X"}
    query_sum = Sum([ops[i] for i, (_, op) in enumerate(cigar_ops)
                     if op in query_consuming_ops])
    s.add(query_sum == seq_len)
    return s.check() == sat


def check_info_number_a(alt_count: int, values: list) -> bool:
    """
    Verify: Number=A field has exactly len(ALT) values.
    """
    return len(values) == alt_count


def check_info_number_r(alt_count: int, values: list) -> bool:
    """
    Verify: Number=R field has exactly len(ALT) + 1 values.
    """
    return len(values) == alt_count + 1


def check_flag_type_number(number_value: int) -> bool:
    """
    Verify: Flag type fields must have Number=0.
    """
    return number_value == 0


def generate_extreme_vcf_params(
    min_alts: int = 0,
    max_alts: int = 10,
    min_samples: int = 1,
    max_samples: int = 5,
) -> Optional[dict]:
    """
    Use Z3 to solve for valid VCF parameters at boundary conditions.

    Returns dict with alt_count, sample_count, pos if solvable.
    """
    if not Z3_AVAILABLE:
        return None

    s = Solver()
    alt_count = Int("alt_count")
    sample_count = Int("sample_count")
    pos = Int("pos")

    s.add(And(alt_count >= min_alts, alt_count <= max_alts))
    s.add(And(sample_count >= min_samples, sample_count <= max_samples))
    s.add(pos >= 1)

    if s.check() == sat:
        m = s.model()
        return {
            "alt_count": m[alt_count].as_long(),
            "sample_count": m[sample_count].as_long(),
            "pos": m[pos].as_long(),
        }
    return None


def generate_extreme_sam_params(
    max_cigar_ops: int = 20,
    max_tags: int = 50,
) -> Optional[dict]:
    """
    Use Z3 to solve for valid SAM record parameters at boundary conditions.
    """
    if not Z3_AVAILABLE:
        return None

    s = Solver()
    n_ops = Int("n_ops")
    n_tags = Int("n_tags")
    seq_len = Int("seq_len")

    s.add(And(n_ops >= 1, n_ops <= max_cigar_ops))
    s.add(And(n_tags >= 0, n_tags <= max_tags))
    s.add(seq_len >= 1)

    if s.check() == sat:
        m = s.model()
        return {
            "n_ops": m[n_ops].as_long(),
            "n_tags": m[n_tags].as_long(),
            "seq_len": m[seq_len].as_long(),
        }
    return None
