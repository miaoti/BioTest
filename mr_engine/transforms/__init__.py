"""
B2: Atomic Transforms Library

Decorator-based registry of all legal atomic transform operations.
The TRANSFORM_REGISTRY dict is the single source of truth for the
whitelist enforced by the DSL compiler (B5).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

@dataclass
class TransformMeta:
    fn: Callable
    format: str          # "VCF", "SAM", or "VCF/SAM"
    description: str     # one-line explanation for the LLM prompt
    group: str           # logical group — used to show compound-step relationships


TRANSFORM_REGISTRY: dict[str, TransformMeta] = {}


def register_transform(name: str, *, format: str, description: str, group: str = ""):
    """Decorator to register an atomic transform function with metadata."""
    def decorator(fn: Callable) -> Callable:
        if name in TRANSFORM_REGISTRY:
            raise ValueError(f"Duplicate transform registration: '{name}'")
        TRANSFORM_REGISTRY[name] = TransformMeta(
            fn=fn,
            format=format,
            description=description,
            group=group or name,
        )
        return fn
    return decorator


# Import submodules to trigger registration
from . import vcf, sam  # noqa: E402, F401


def get_whitelist() -> list[str]:
    """Return sorted list of all registered transform names."""
    return sorted(TRANSFORM_REGISTRY.keys())


def get_compound_groups() -> dict[str, frozenset[str]]:
    """
    Return all compound-step groups discovered from the registry.

    A compound group is any group with more than one member.  The returned
    dict maps group_id -> frozenset of transform names that must appear
    together in an MR's transform_steps.

    Example
    -------
    >>> get_compound_groups()
    {'alt_permutation': frozenset({'choose_permutation', 'permute_ALT',
                                   'remap_GT', 'permute_Number_A_R_fields'})}
    """
    groups: dict[str, set[str]] = {}
    for name, meta in TRANSFORM_REGISTRY.items():
        if meta.group:
            groups.setdefault(meta.group, set()).add(name)
    # Only groups with 2+ members are compound steps
    return {gid: frozenset(members) for gid, members in groups.items()
            if len(members) > 1}


def get_transform_menu() -> str:
    """
    Return the formatted transform menu for inclusion in the LLM system prompt.

    Transforms are grouped by logical compound steps (e.g. ALT permutation
    requires three coordinated functions). Within each group, members are
    listed in the order they must be applied.
    """
    # Collect entries, preserving group order via first-seen group ordering
    seen_groups: list[str] = []
    groups: dict[str, list[tuple[str, TransformMeta]]] = {}
    for name in sorted(TRANSFORM_REGISTRY.keys()):
        meta = TRANSFORM_REGISTRY[name]
        if meta.group not in groups:
            seen_groups.append(meta.group)
            groups[meta.group] = []
        groups[meta.group].append((name, meta))

    lines: list[str] = []
    for group in seen_groups:
        members = groups[group]
        if len(members) == 1:
            name, meta = members[0]
            lines.append(f"  [{meta.format}] {name}")
            lines.append(f"      {meta.description}")
        else:
            # Compound group — show header then each step
            first_meta = members[0][1]
            lines.append(f"  [{first_meta.format}] *** Compound step — apply all three together ***")
            for name, meta in members:
                lines.append(f"    {name}")
                lines.append(f"        {meta.description}")
        lines.append("")

    return "\n".join(lines)
