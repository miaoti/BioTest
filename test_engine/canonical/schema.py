"""
Pydantic v2 models for Canonical JSON output of SAM and VCF parsers.

Every parser adapter normalizes its output into these models before
comparison by the oracles. This is the single source of truth for
cross-language differential testing.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, field_validator


# ---------------------------------------------------------------------------
# SAM Canonical Schema
# ---------------------------------------------------------------------------

class CigarOp(BaseModel):
    """Single CIGAR operation: operator + length."""
    op: str    # M, I, D, N, S, H, P, =, X
    len: int

    @field_validator("op")
    @classmethod
    def _valid_op(cls, v: str) -> str:
        valid = {"M", "I", "D", "N", "S", "H", "P", "=", "X"}
        if v not in valid:
            raise ValueError(f"Invalid CIGAR op '{v}', must be one of {valid}")
        return v


class TagValue(BaseModel):
    """SAM optional tag with type and value."""
    type: str    # A, i, f, Z, H, B
    value: Any


class CanonicalSamHeader(BaseModel):
    """Normalized SAM header."""
    HD: Optional[dict[str, str]] = None
    SQ: list[dict[str, str]]             # Preserve physical order
    RG: list[dict[str, str]] = []
    PG: list[dict[str, str]] = []
    CO: list[str] = []                    # Sorted (multiset semantics)

    @field_validator("CO")
    @classmethod
    def _sort_comments(cls, v: list[str]) -> list[str]:
        return sorted(v)


class CanonicalSamRecord(BaseModel):
    """Normalized SAM alignment record."""
    QNAME: str
    FLAG: int
    RNAME: Optional[str] = None           # None if "*"
    POS: Optional[int] = None             # 1-based; None if unmapped (0)
    MAPQ: int
    CIGAR: Optional[list[CigarOp]] = None  # None if "*"
    RNEXT: Optional[str] = None
    PNEXT: Optional[int] = None           # 1-based; None if 0
    TLEN: int
    SEQ: Optional[str] = None             # None if "*"
    QUAL: Optional[str] = None            # None if "*"
    tags: dict[str, TagValue] = {}        # Sorted by key in serialization


class CanonicalSam(BaseModel):
    """Full canonical SAM document."""
    format: str = "SAM"
    header: CanonicalSamHeader
    records: list[CanonicalSamRecord]


# ---------------------------------------------------------------------------
# VCF Canonical Schema
# ---------------------------------------------------------------------------

class CanonicalVcfHeader(BaseModel):
    """Normalized VCF header."""
    fileformat: str                       # e.g. "VCFv4.5"
    meta: dict[str, Any]                  # INFO/FORMAT/FILTER/contig indexed by ID
    samples: list[str]                    # Ordered from #CHROM line


class CanonicalVcfRecord(BaseModel):
    """Normalized VCF data record."""
    CHROM: str
    POS: int                              # 1-based
    ID: Optional[str] = None              # None if "."
    REF: str
    ALT: list[str] = []                   # [] if "."
    QUAL: Optional[float] = None          # None if "."
    FILTER: list[str] = []               # Sorted set
    INFO: dict[str, Any] = {}            # Typed map, keys sorted
    FORMAT: Optional[list[str]] = None
    samples: Optional[dict[str, dict[str, Any]]] = None  # sample_name -> fields

    @field_validator("FILTER")
    @classmethod
    def _sort_filter(cls, v: list[str]) -> list[str]:
        return sorted(v)


class CanonicalVcf(BaseModel):
    """Full canonical VCF document."""
    format: str = "VCF"
    header: CanonicalVcfHeader
    records: list[CanonicalVcfRecord]
