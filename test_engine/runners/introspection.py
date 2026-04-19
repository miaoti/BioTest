"""
Python-side reflection helpers for Rank 5 query-method MRs.

Framework-level utilities used by Python runners (pysam, biopython,
reference). The helpers introspect any Python object and return
descriptors for the public, scalar-returning, effectively-nullary
methods the LLM can reference in API-query MRs.

Citation: Chen, Kuo, Liu, Tse (ACM CSUR 2018) §3.2 — API-level
metamorphic relations; MR-Scout (Xu et al., TOSEM 2024,
arXiv:2304.07548) — query-method MR mining.
"""

from __future__ import annotations

import inspect
import logging
from typing import Any

logger = logging.getLogger(__name__)


# Scalar return types the oracle can compare deterministically.
# `deep_equal` handles bool/int/float/str/None directly; tuples of
# scalars are treated as fixed-arity lists.
_SCALAR_TYPE_HINTS: frozenset[str] = frozenset({
    "bool", "int", "float", "str", "bytes", "NoneType",
    "Integer", "Long", "Boolean", "String", "Enum",
})


def _describe_return(annotation: Any) -> str:
    """Best-effort string rendering of a return-type annotation."""
    if annotation is inspect.Signature.empty:
        return "Any"
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation)


def _is_scalar_returning(
    sig: inspect.Signature,
) -> bool:
    """Heuristic: a method is scalar-returning if its annotation is a
    primitive or the annotation is missing (we accept, but downstream
    deep_equal catches non-scalar values at compare time)."""
    ann = sig.return_annotation
    if ann is inspect.Signature.empty:
        return True  # unannotated — let the oracle decide at call time
    name = getattr(ann, "__name__", None) or str(ann)
    return any(t == name or t in name for t in _SCALAR_TYPE_HINTS)


def _has_only_self(sig: inspect.Signature) -> bool:
    """Method is effectively nullary — `self` plus no other required params."""
    params = list(sig.parameters.values())
    # skip `self` / `cls`
    params = [p for p in params if p.name not in ("self", "cls")]
    # All remaining params must have defaults
    return all(p.default is not inspect.Parameter.empty for p in params)


# Pydantic v2 framework methods to exclude from introspection — they're
# parser-internal noise, not VCF/SAM query methods. Same idea as filtering
# out `dir()`'s dunder methods.
_PYDANTIC_NOISE: frozenset[str] = frozenset({
    "construct", "copy", "dict", "from_orm", "json", "parse_file",
    "parse_obj", "parse_raw", "schema", "schema_json", "update_forward_refs",
    "validate", "model_construct", "model_copy", "model_dump",
    "model_dump_json", "model_json_schema", "model_parametrized_name",
    "model_post_init", "model_rebuild", "model_validate",
    "model_validate_json", "model_validate_strings", "model_computed_fields",
    "model_config", "model_extra", "model_fields", "model_fields_set",
})


def get_scalar_query_methods(obj: Any, limit: int = 50) -> list[dict[str, Any]]:
    """Introspect `obj` and return up to `limit` descriptors for public,
    effectively-nullary, scalar-returning methods and properties.

    Output shape matches `ParserRunner.discover_query_methods`:
        [{"name": str, "returns": str, "args": list[str]}, ...]

    Private (underscore-prefixed) names, dunders, and Pydantic v2
    framework methods (`model_dump`, `model_validate`, …) are skipped —
    those are parser plumbing, not query methods on the parsed record.

    For a Pydantic v2 BaseModel CLASS (not instance), the helper takes
    a fast path that returns its declared `model_fields` — those are
    exactly the parser's typed scalar fields and represent the real
    "query API" the LLM should reference.
    """
    # Fast path: Pydantic BaseModel CLASS. Its `model_fields` IS the
    # field list; bypass dir() noise entirely.
    try:
        from pydantic import BaseModel as _BM
        if isinstance(obj, type) and issubclass(obj, _BM):
            results: list[dict[str, Any]] = []
            for name, field in obj.model_fields.items():
                if name.startswith("_"):
                    continue
                ann = getattr(field, "annotation", None)
                results.append({
                    "name": name,
                    "returns": _describe_return(ann) if ann is not None else "Any",
                    "args": [],
                })
                if len(results) >= limit:
                    break
            return results
    except ImportError:
        pass

    results = []
    for name in sorted(dir(obj)):
        if name.startswith("_") or name in _PYDANTIC_NOISE:
            continue
        try:
            attr = getattr(obj, name)
        except Exception:
            continue

        # Case A: property or plain attribute access.
        if not callable(attr):
            results.append({
                "name": name,
                "returns": type(attr).__name__,
                "args": [],
            })
            if len(results) >= limit:
                break
            continue

        # Case B: method. Require nullary-ish signature.
        try:
            sig = inspect.signature(attr)
        except (TypeError, ValueError):
            continue
        if not _has_only_self(sig):
            continue
        if not _is_scalar_returning(sig):
            continue
        results.append({
            "name": name,
            "returns": _describe_return(sig.return_annotation),
            "args": [],
        })
        if len(results) >= limit:
            break
    return results


def invoke_query_method(
    obj: Any, method_name: str, args: list[Any] | None = None,
) -> Any:
    """Call `method_name` on `obj` and return its scalar result.

    Properties and plain attributes are returned directly (no call).
    Raises AttributeError if the method is absent, RuntimeError on
    invocation failure. Callers catch and classify.
    """
    if not hasattr(obj, method_name):
        raise AttributeError(
            f"{type(obj).__name__} has no attribute {method_name!r}"
        )
    attr = getattr(obj, method_name)
    if not callable(attr):
        return attr
    try:
        return attr(*(args or []))
    except Exception as e:
        raise RuntimeError(
            f"Invocation {method_name}() raised: {type(e).__name__}: {e}"
        ) from e


def _coerce_scalar(value: Any) -> Any:
    """Downgrade return values to oracle-compatible scalars.

    - Enums → their .name or .value string.
    - Exceptions caught mid-invocation are already surfaced as strings
      by the caller.
    - Lists/tuples of scalars are preserved (deep_equal handles them).
    - Objects with no natural scalar are rendered via repr().
    """
    if value is None or isinstance(value, (bool, int, float, str, bytes)):
        return value
    import enum as _enum
    if isinstance(value, _enum.Enum):
        return value.name
    if isinstance(value, (list, tuple, set)):
        return [_coerce_scalar(v) for v in value]
    if isinstance(value, dict):
        return {k: _coerce_scalar(v) for k, v in value.items()}
    return repr(value)


def run_methods_on_record(
    record: Any, method_names: list[str],
) -> dict[str, Any]:
    """Helper used by each Python runner's `run_query_methods`.

    For each requested method, invoke it (or read the property) on
    `record`, coerce the result to a JSON-serializable scalar, and pack
    into a name→value map. Failures become `{"__error__": str(e)}` in
    the map so the oracle can detect them without dropping the test.
    """
    out: dict[str, Any] = {}
    for name in method_names:
        try:
            raw = invoke_query_method(record, name)
            out[name] = _coerce_scalar(raw)
        except Exception as e:
            out[name] = {"__error__": f"{type(e).__name__}: {e}"}
    return out
