"""
B2: Atomic Transforms Library

Decorator-based registry of all legal atomic transform operations.
The TRANSFORM_REGISTRY dict is the single source of truth for the
whitelist enforced by the DSL compiler (B5).
"""

from __future__ import annotations

from typing import Callable

TRANSFORM_REGISTRY: dict[str, Callable] = {}


def register_transform(name: str):
    """Decorator to register an atomic transform function by name."""
    def decorator(fn: Callable) -> Callable:
        if name in TRANSFORM_REGISTRY:
            raise ValueError(f"Duplicate transform registration: '{name}'")
        TRANSFORM_REGISTRY[name] = fn
        return fn
    return decorator


# Import submodules to trigger registration
from . import vcf, sam  # noqa: E402, F401


def get_whitelist() -> list[str]:
    """Return sorted list of all registered transform names."""
    return sorted(TRANSFORM_REGISTRY.keys())
