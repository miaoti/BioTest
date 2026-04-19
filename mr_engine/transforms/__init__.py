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
    format: str                    # "VCF", "SAM", or "VCF/SAM"
    description: str               # one-line explanation for the LLM prompt
    group: str                     # logical group — shows compound-step links
    contextual_hint: str = ""      # "Use when ..." — helps the LLM pick the
                                   # right transform for a seed/target combo
    preconditions: tuple[str, ...] = ()
                                   # structured gates: "info_has_key=CSQ",
                                   # "alt_count>=2", "has_cigar", etc.
                                   # Surfaced in the prompt so the agent
                                   # avoids proposing inapplicable steps.


TRANSFORM_REGISTRY: dict[str, TransformMeta] = {}


def register_transform(
    name: str,
    *,
    format: str,
    description: str,
    group: str = "",
    contextual_hint: str = "",
    preconditions: tuple[str, ...] = (),
):
    """Decorator to register an atomic transform function with metadata.

    Args:
        name: Unique transform identifier (whitelist key).
        format: "VCF", "SAM", or "VCF/SAM".
        description: One-line purpose shown in the LLM prompt menu.
        group: Logical group id; transforms sharing a group with 2+ members
               form a compound step (must be applied together).
        contextual_hint: Optional sentence explaining when this transform is
               most applicable (rendered as "Use when:" in the prompt).
        preconditions: Optional structured list of file/record-level gates
               rendered as "Preconditions:" in the prompt (e.g.,
               ("info_has_key=CSQ",) or ("alt_count>=2",)). These help the
               agent avoid proposing transforms against seeds where they
               trivially cannot apply.
    """
    def decorator(fn: Callable) -> Callable:
        if name in TRANSFORM_REGISTRY:
            raise ValueError(f"Duplicate transform registration: '{name}'")
        TRANSFORM_REGISTRY[name] = TransformMeta(
            fn=fn,
            format=format,
            description=description,
            group=group or name,
            contextual_hint=contextual_hint,
            preconditions=tuple(preconditions),
        )
        return fn
    return decorator


# Import submodules to trigger registration
from . import vcf, sam, malformed, query  # noqa: E402, F401


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

    def _render_meta(name: str, meta: TransformMeta, indent: str = "      ") -> list[str]:
        out = [f"{indent}{meta.description}"]
        if meta.contextual_hint:
            out.append(f"{indent}Use when: {meta.contextual_hint}")
        if meta.preconditions:
            out.append(
                f"{indent}Preconditions: "
                + ", ".join(meta.preconditions)
            )
        return out

    lines: list[str] = []
    for group in seen_groups:
        members = groups[group]
        if len(members) == 1:
            name, meta = members[0]
            lines.append(f"  [{meta.format}] {name}")
            lines.extend(_render_meta(name, meta))
        else:
            # Compound group — show header then each step
            first_meta = members[0][1]
            member_count = len(members)
            lines.append(
                f"  [{first_meta.format}] *** Compound step — "
                f"all {member_count} members must be applied together ***"
            )
            for name, meta in members:
                lines.append(f"    {name}")
                lines.extend(_render_meta(name, meta, indent="        "))
        lines.append("")

    return "\n".join(lines)
