"""
Pydantic v2 models for MR-DSL schema.

Two-tier evidence model:
  - RawEvidence: what the LLM outputs (chunk_id + quote only, no severity)
  - HydratedEvidence: enriched by compiler via ChromaDB lookup (adds rule_severity)

Deterministic mr_id is computed from (format + scope + sorted transform_steps)
via MD5 hash, ensuring deduplication regardless of LLM naming.
"""

from __future__ import annotations

import hashlib
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from mr_engine.transforms import get_whitelist, get_compound_groups


# ---------------------------------------------------------------------------
# Evidence models
# ---------------------------------------------------------------------------

class RawEvidence(BaseModel):
    """Evidence as output by the LLM — no severity (prevents hallucination)."""
    chunk_id: str
    quote: str


class HydratedEvidence(BaseModel):
    """Evidence enriched with ground-truth metadata from ChromaDB."""
    chunk_id: str
    quote: str
    rule_severity: str   # "CRITICAL", "ADVISORY", or "INFORMATIONAL"
    section_id: str

    @field_validator("rule_severity")
    @classmethod
    def _severity_valid(cls, v: str) -> str:
        valid = {"CRITICAL", "ADVISORY", "INFORMATIONAL"}
        if v not in valid:
            raise ValueError(f"rule_severity must be one of {valid}, got '{v}'")
        return v


# ---------------------------------------------------------------------------
# Raw MR from Agent (before compilation)
# ---------------------------------------------------------------------------

class RawMRFromAgent(BaseModel):
    """
    Schema matching the LLM's JSON output.
    transform_steps are validated against the atomic transforms whitelist.
    """
    mr_name: str
    scope: str   # "VCF.header" | "VCF.record" | "SAM.header" | "SAM.record"
    preconditions: list[str]
    transform_steps: list[str]
    oracle: str
    evidence: list[RawEvidence]
    ambiguity_flags: list[str] = []

    @field_validator("scope")
    @classmethod
    def _scope_valid(cls, v: str) -> str:
        valid = {"VCF.header", "VCF.record", "SAM.header", "SAM.record"}
        if v not in valid:
            raise ValueError(f"scope must be one of {valid}, got '{v}'")
        return v

    @field_validator("transform_steps")
    @classmethod
    def _transforms_whitelisted(cls, v: list[str]) -> list[str]:
        whitelist = set(get_whitelist())
        for step in v:
            if step not in whitelist:
                raise ValueError(
                    f"Transform '{step}' is not in the whitelist. "
                    f"Valid transforms: {sorted(whitelist)}"
                )
        return v

    @model_validator(mode="after")
    def _must_have_content(self) -> "RawMRFromAgent":
        if not self.transform_steps:
            raise ValueError("MR must have at least one transform step")
        if not self.evidence:
            raise ValueError("MR must have at least one evidence citation")
        return self

    @model_validator(mode="after")
    def _compound_steps_all_or_nothing(self) -> "RawMRFromAgent":
        """
        Enforce the all-or-nothing rule for compound-step groups.

        If ANY transform from a compound group appears in transform_steps,
        then ALL members of that group must be present.  This prevents the
        LLM from listing e.g. permute_ALT without the matching remap_GT,
        which would produce a semantically broken MR.

        The compound groups are derived dynamically from the TRANSFORM_REGISTRY
        (any group with 2+ members is a compound group), so adding a new
        compound group in the future requires zero changes here.
        """
        steps = set(self.transform_steps)
        for group_id, required_members in get_compound_groups().items():
            present = steps & required_members
            if present and present != required_members:
                missing = sorted(required_members - present)
                present_list = sorted(present)
                raise ValueError(
                    f"Compound-step violation for group '{group_id}': "
                    f"found {present_list} but missing {missing}. "
                    f"These transforms are biologically co-dependent and MUST "
                    f"ALL appear together in transform_steps: "
                    f"{sorted(required_members)}"
                )
        return self


# ---------------------------------------------------------------------------
# Final compiled MetamorphicRelation
# ---------------------------------------------------------------------------

class MetamorphicRelation(BaseModel):
    """
    The fully compiled MR with system-generated mr_id and hydrated evidence.
    This is not instantiated directly from LLM output — the compiler builds it.
    """
    mr_id: str              # deterministic hash (system-generated)
    mr_name: str            # human-readable name (from LLM)
    scope: str
    preconditions: list[str]
    transform_steps: list[str]
    oracle: str
    evidence: list[HydratedEvidence]
    ambiguity_flags: list[str] = []


class MRBatch(BaseModel):
    """Top-level container for a batch of compiled MRs."""
    relations: list[MetamorphicRelation]


# ---------------------------------------------------------------------------
# Deterministic hash generation
# ---------------------------------------------------------------------------

def compute_mr_id(scope: str, transform_steps: list[str]) -> str:
    """
    Compute a deterministic mr_id from scope and transform steps.

    The hash is based on: format (extracted from scope) + scope + sorted transform_steps.
    This ensures the same logical MR always gets the same ID regardless of LLM naming.

    Returns:
        First 12 characters of the MD5 hex digest.
    """
    fmt = scope.split(".")[0]  # "VCF" from "VCF.record"
    stable_key = fmt + "|" + scope + "|" + "|".join(sorted(transform_steps))
    return hashlib.md5(stable_key.encode("utf-8")).hexdigest()[:12]
