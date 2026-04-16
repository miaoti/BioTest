"""
B6: MR Quality Triage Registry

Two-tier classification based on hydrated evidence severity from ChromaDB:
  - Enforced: ALL evidence is CRITICAL and no ambiguity flags -> block CI on failure
  - Quarantine: any ADVISORY/INFORMATIONAL evidence or ambiguity -> warn only

Deduplication is handled naturally by using mr_id (deterministic hash) as dict key.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from mr_engine.dsl.models import MetamorphicRelation

logger = logging.getLogger(__name__)


@dataclass
class MRRegistry:
    """Registry of triaged MRs, keyed by mr_id for natural deduplication."""
    enforced: dict[str, MetamorphicRelation] = field(default_factory=dict)
    quarantine: dict[str, MetamorphicRelation] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return len(self.enforced) + len(self.quarantine)


def triage(relations: list[MetamorphicRelation]) -> MRRegistry:
    """
    Classify compiled MRs into Enforced or Quarantine tiers.

    Dedup: if an mr_id already exists in the registry, it is skipped
    (deterministic hash guarantees same transform logic = same key).

    Enforced criteria:
      - ALL evidence has rule_severity == "CRITICAL" (MUST/SHALL backed)
      - No ambiguity_flags

    Everything else goes to Quarantine.

    Args:
        relations: List of compiled MetamorphicRelation objects.

    Returns:
        MRRegistry with enforced and quarantine dicts.
    """
    registry = MRRegistry()
    skipped = 0

    for mr in relations:
        # Dedup check
        if mr.mr_id in registry.enforced or mr.mr_id in registry.quarantine:
            skipped += 1
            logger.debug("Skipping duplicate mr_id=%s (%s)", mr.mr_id, mr.mr_name)
            continue

        if _is_enforced(mr):
            registry.enforced[mr.mr_id] = mr
        else:
            registry.quarantine[mr.mr_id] = mr

    if skipped:
        logger.info("Dedup: skipped %d duplicate MR(s)", skipped)

    logger.info(
        "Triage result: %d enforced, %d quarantine",
        len(registry.enforced), len(registry.quarantine),
    )
    return registry


def _is_enforced(mr: MetamorphicRelation) -> bool:
    """Check if an MR qualifies for the enforced tier."""
    if mr.ambiguity_flags:
        return False
    return all(e.rule_severity == "CRITICAL" for e in mr.evidence)


def export_registry(registry: MRRegistry, path: str) -> None:
    """
    Serialize the registry to a JSON file for CI consumption.

    Args:
        registry: The triaged MRRegistry.
        path: Output file path.
    """
    data = {
        "enforced": [mr.model_dump() for mr in registry.enforced.values()],
        "quarantine": [mr.model_dump() for mr in registry.quarantine.values()],
        "summary": {
            "enforced_count": len(registry.enforced),
            "quarantine_count": len(registry.quarantine),
            "total": registry.total,
        },
    }
    _atomic_write_json(path, data)

    logger.info("Registry exported to %s (%d MRs)", path, registry.total)


def load_registry_from_file(path: str) -> dict:
    """Load a registry from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def merge_registries(existing_path: str, new_registry: MRRegistry) -> None:
    """
    Merge new MRs into an existing registry file, deduplicating by mr_id.

    New MRs are appended to the existing file. Existing mr_ids are preserved.
    """
    try:
        with open(existing_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"enforced": [], "quarantine": [], "summary": {}}

    existing_ids = {mr["mr_id"] for mr in data.get("enforced", [])}
    existing_ids |= {mr["mr_id"] for mr in data.get("quarantine", [])}

    added = 0
    for mr in new_registry.enforced.values():
        if mr.mr_id not in existing_ids:
            data["enforced"].append(mr.model_dump())
            existing_ids.add(mr.mr_id)
            added += 1

    for mr in new_registry.quarantine.values():
        if mr.mr_id not in existing_ids:
            data["quarantine"].append(mr.model_dump())
            existing_ids.add(mr.mr_id)
            added += 1

    data["summary"] = {
        "enforced_count": len(data["enforced"]),
        "quarantine_count": len(data["quarantine"]),
        "total": len(data["enforced"]) + len(data["quarantine"]),
    }

    _atomic_write_json(existing_path, data)

    logger.info("Merged %d new MRs into %s", added, existing_path)


def _atomic_write_json(path: str, data: dict) -> None:
    """Write JSON atomically: write to tmp file then os.replace."""
    import os
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)
