"""
Semantic deep-equality comparison for canonical JSON objects.

Handles:
- dict: key order ignored
- set/frozenset: mathematical set equality
- list: element-wise ordered comparison
- float: math.isclose with configurable tolerance
- int vs float: promote both to float
- None: equal only to None

Returns (is_equal, list_of_difference_path_descriptions) for debugging.
"""

from __future__ import annotations

import math
from typing import Any


DEFAULT_FLOAT_TOL = 1e-6
QUAL_FLOAT_TOL = 0.01


def deep_equal(
    a: Any,
    b: Any,
    float_tol: float = DEFAULT_FLOAT_TOL,
    path: str = "$",
) -> tuple[bool, list[str]]:
    """
    Recursively compare two values with semantic tolerance.

    Args:
        a: Left value.
        b: Right value.
        float_tol: Absolute tolerance for float comparison.
        path: JSON-path prefix for difference descriptions.

    Returns:
        (is_equal, differences) where differences is a list of
        human-readable path descriptions of every mismatch.
    """
    diffs: list[str] = []

    # Both None
    if a is None and b is None:
        return True, []

    # One None
    if a is None or b is None:
        diffs.append(f"{path}: {_repr(a)} vs {_repr(b)}")
        return False, diffs

    # Cross-type: int vs float
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if not math.isclose(float(a), float(b), abs_tol=float_tol):
            diffs.append(f"{path}: {a} != {b} (tol={float_tol})")
            return False, diffs
        return True, []

    # Type mismatch
    if type(a) is not type(b):
        # Allow Pydantic model vs dict comparison
        if hasattr(a, "model_dump") and isinstance(b, dict):
            return deep_equal(a.model_dump(), b, float_tol, path)
        if isinstance(a, dict) and hasattr(b, "model_dump"):
            return deep_equal(a, b.model_dump(), float_tol, path)
        diffs.append(f"{path}: type {type(a).__name__} vs {type(b).__name__}")
        return False, diffs

    # dict — key order ignored
    if isinstance(a, dict):
        all_keys = set(a.keys()) | set(b.keys())
        for key in sorted(all_keys, key=str):
            child_path = f"{path}.{key}"
            if key not in a:
                diffs.append(f"{child_path}: missing in left")
            elif key not in b:
                diffs.append(f"{child_path}: missing in right")
            else:
                # Use QUAL tolerance for quality-related fields
                tol = QUAL_FLOAT_TOL if key in ("QUAL", "qual") else float_tol
                _, sub_diffs = deep_equal(a[key], b[key], tol, child_path)
                diffs.extend(sub_diffs)
        return len(diffs) == 0, diffs

    # set / frozenset — mathematical set equality
    if isinstance(a, (set, frozenset)):
        if a != b:
            only_a = a - b
            only_b = b - a
            if only_a:
                diffs.append(f"{path}: only in left: {only_a}")
            if only_b:
                diffs.append(f"{path}: only in right: {only_b}")
        return len(diffs) == 0, diffs

    # list — element-wise ordered
    if isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"{path}: length {len(a)} vs {len(b)}")
            # Compare up to the shorter length for detail
            min_len = min(len(a), len(b))
            for i in range(min_len):
                _, sub_diffs = deep_equal(a[i], b[i], float_tol, f"{path}[{i}]")
                diffs.extend(sub_diffs)
            return False, diffs
        for i in range(len(a)):
            _, sub_diffs = deep_equal(a[i], b[i], float_tol, f"{path}[{i}]")
            diffs.extend(sub_diffs)
        return len(diffs) == 0, diffs

    # float
    if isinstance(a, float):
        if not math.isclose(a, b, abs_tol=float_tol):
            diffs.append(f"{path}: {a} != {b} (tol={float_tol})")
            return False, diffs
        return True, []

    # str, int, bool — exact equality
    if a != b:
        diffs.append(f"{path}: {_repr(a)} != {_repr(b)}")
        return False, diffs

    return True, []


def deep_equal_multiset(
    a: list,
    b: list,
    float_tol: float = DEFAULT_FLOAT_TOL,
    path: str = "$",
) -> tuple[bool, list[str]]:
    """
    Compare two lists as multisets (sorted by string representation).

    Use this for collections where order is not significant
    (e.g., SAM @CO comments, VCF FILTER entries).
    """
    if len(a) != len(b):
        return False, [f"{path}: multiset length {len(a)} vs {len(b)}"]
    sa = sorted(a, key=str)
    sb = sorted(b, key=str)
    return deep_equal(sa, sb, float_tol, path)


def all_equal(
    results: dict[str, Any],
    float_tol: float = DEFAULT_FLOAT_TOL,
) -> tuple[bool, dict[tuple[str, str], list[str]]]:
    """
    Compare all parser outputs pairwise.

    Args:
        results: {parser_name: canonical_json_dict}

    Returns:
        (all_agree, pairwise_diffs) where pairwise_diffs maps
        (parser_a, parser_b) -> list of differences.
    """
    pairwise: dict[tuple[str, str], list[str]] = {}
    names = sorted(results.keys())
    all_agree = True

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a_name, b_name = names[i], names[j]
            eq, diffs = deep_equal(results[a_name], results[b_name], float_tol)
            pairwise[(a_name, b_name)] = diffs
            if not eq:
                all_agree = False

    return all_agree, pairwise


def _repr(val: Any) -> str:
    """Short repr for diff messages."""
    s = repr(val)
    return s if len(s) <= 80 else s[:77] + "..."
