"""
DSL Compiler: validation + metadata hydration + deterministic hashing.

Pipeline:
  1. Extract JSON from agent output (handles markdown fences)
  2. Validate against RawMRFromAgent schema (whitelist enforcement)
  3. Hydrate evidence: look up each chunk_id in ChromaDB for ground-truth severity
  4. Compute deterministic mr_id via hash
  5. Assemble final MetamorphicRelation
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field

from pydantic import ValidationError

from spec_ingestor.indexer import SpecIndex
from .models import (
    HydratedEvidence,
    MetamorphicRelation,
    RawEvidence,
    RawMRFromAgent,
    compute_mr_id,
)

logger = logging.getLogger(__name__)


@dataclass
class CompilationResult:
    """Result of compiling agent output into validated MRs."""
    success: bool
    relations: list[MetamorphicRelation] = field(default_factory=list)
    error_detail: str | None = None
    raw_json: str | None = None


def compile_mr_output(
    raw_text: str,
    spec_index: SpecIndex,
) -> CompilationResult:
    """
    Full compilation pipeline: parse -> validate -> hydrate -> hash -> assemble.

    Args:
        raw_text: Raw text output from the LLM agent.
        spec_index: SpecIndex instance for evidence hydration.

    Returns:
        CompilationResult with validated MRs or error details for agent feedback.
    """
    # Step 1: Extract JSON
    json_str = _extract_json(raw_text)
    if json_str is None:
        return CompilationResult(
            success=False,
            error_detail=(
                "Could not find valid JSON in your output. "
                "Return a JSON array of MR objects, optionally inside ```json fences."
            ),
            raw_json=raw_text,
        )

    # Step 2: Parse JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return CompilationResult(
            success=False,
            error_detail=f"JSON parse error at position {e.pos}: {e.msg}",
            raw_json=json_str,
        )

    # Normalize: accept array or {"relations": [...]}
    if isinstance(data, list):
        raw_items = data
    elif isinstance(data, dict) and "relations" in data:
        raw_items = data["relations"]
    else:
        return CompilationResult(
            success=False,
            error_detail=(
                "Expected a JSON array of MR objects, or an object with a "
                "'relations' key. Got neither."
            ),
            raw_json=json_str,
        )

    # Step 3: Validate each item as RawMRFromAgent
    validated_raws: list[RawMRFromAgent] = []
    errors: list[str] = []

    for i, item in enumerate(raw_items):
        try:
            raw_mr = RawMRFromAgent.model_validate(item)
            validated_raws.append(raw_mr)
        except ValidationError as e:
            for err in e.errors():
                loc = " -> ".join(str(x) for x in err["loc"])
                errors.append(f"  MR[{i}].{loc}: {err['msg']}")

    if errors:
        return CompilationResult(
            success=False,
            error_detail="Pydantic validation errors:\n" + "\n".join(errors),
            raw_json=json_str,
        )

    # Step 4 & 5: Hydrate evidence + compute mr_id + assemble
    compiled: list[MetamorphicRelation] = []

    for i, raw_mr in enumerate(validated_raws):
        hydrated_evidence, hydration_errors = _hydrate_evidence(
            raw_mr.evidence, spec_index
        )

        if hydration_errors:
            errors.extend(
                f"  MR[{i}] ({raw_mr.mr_name}): {err}" for err in hydration_errors
            )
            continue

        mr_id = compute_mr_id(raw_mr.scope, raw_mr.transform_steps)

        compiled.append(MetamorphicRelation(
            mr_id=mr_id,
            mr_name=raw_mr.mr_name,
            scope=raw_mr.scope,
            preconditions=raw_mr.preconditions,
            transform_steps=raw_mr.transform_steps,
            oracle=raw_mr.oracle,
            evidence=hydrated_evidence,
            ambiguity_flags=raw_mr.ambiguity_flags,
        ))

    if errors:
        return CompilationResult(
            success=False,
            error_detail="Evidence hydration errors:\n" + "\n".join(errors),
            raw_json=json_str,
        )

    if not compiled:
        return CompilationResult(
            success=False,
            error_detail="No MRs were produced after compilation.",
            raw_json=json_str,
        )

    logger.info("Compiled %d MRs successfully", len(compiled))
    return CompilationResult(
        success=True,
        relations=compiled,
        raw_json=json_str,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hydrate_evidence(
    raw_evidences: list[RawEvidence],
    spec_index: SpecIndex,
) -> tuple[list[HydratedEvidence], list[str]]:
    """
    Look up each chunk_id in ChromaDB to retrieve ground-truth metadata.

    Returns:
        Tuple of (hydrated_evidences, error_messages).
        If error_messages is non-empty, hydration failed.
    """
    hydrated: list[HydratedEvidence] = []
    errors: list[str] = []

    # Batch lookup: collect all chunk_ids
    chunk_ids = [e.chunk_id for e in raw_evidences]
    try:
        result = spec_index._collection.get(
            ids=chunk_ids,
            include=["metadatas"],
        )
    except Exception as e:
        return [], [f"ChromaDB lookup failed: {e}"]

    # Build a map of chunk_id -> metadata
    found: dict[str, dict] = {}
    if result and result["ids"]:
        for cid, meta in zip(result["ids"], result["metadatas"]):
            found[cid] = meta

    for raw_ev in raw_evidences:
        meta = found.get(raw_ev.chunk_id)
        if meta is None:
            errors.append(
                f"chunk_id '{raw_ev.chunk_id}' not found in ChromaDB — "
                f"possible LLM hallucination. Reject this evidence."
            )
            continue

        hydrated.append(HydratedEvidence(
            chunk_id=raw_ev.chunk_id,
            quote=raw_ev.quote,
            rule_severity=meta.get("rule_severity", "INFORMATIONAL"),
            section_id=meta.get("section_id", "unknown"),
        ))

    return hydrated, errors


def _extract_json(text: str) -> str | None:
    """
    Extract JSON from agent output, handling:
    - ```json ... ``` markdown fences
    - Raw JSON starting with [ or {
    """
    # Try markdown fenced code blocks first
    match = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Try raw JSON
    stripped = text.strip()
    if stripped.startswith(("[", "{")):
        return stripped

    return None
