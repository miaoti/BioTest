"""
Tests for test_engine/runners/introspection.py — the Python-side
reflection helpers that power Rank 5 query-method MRs.
"""

from __future__ import annotations

import pytest

from test_engine.runners.introspection import (
    get_scalar_query_methods,
    invoke_query_method,
    run_methods_on_record,
    _PYDANTIC_NOISE,
)


# ---------------------------------------------------------------------------
# Fixture types
# ---------------------------------------------------------------------------


class _SampleRecord:
    """Plain Python class; mirrors the shape of pysam.VariantRecord etc."""
    def __init__(self, chrom: str = "chr1", pos: int = 100):
        self.CHROM = chrom
        self.POS = pos

    def is_biallelic(self) -> bool:
        return True

    def num_alleles(self) -> int:
        return 2

    def position(self) -> int:
        return self.POS

    @property
    def is_snp(self) -> bool:
        return True

    def _private_method(self) -> int:
        return 42

    def needs_arg(self, x: int) -> int:
        return x + 1

    def crashy_method(self) -> int:
        raise RuntimeError("boom")


# ---------------------------------------------------------------------------
# Reflection (non-Pydantic class)
# ---------------------------------------------------------------------------


class TestGetScalarQueryMethods:
    def test_returns_public_nullary_scalar_methods(self):
        methods = get_scalar_query_methods(_SampleRecord())
        names = {m["name"] for m in methods}
        assert "is_biallelic" in names
        assert "num_alleles" in names
        assert "is_snp" in names      # property
        assert "CHROM" in names       # plain attribute
        assert "POS" in names

    def test_skips_private_dunder_and_args(self):
        methods = get_scalar_query_methods(_SampleRecord())
        names = {m["name"] for m in methods}
        assert "_private_method" not in names
        assert "needs_arg" not in names
        # No dunders
        assert not any(n.startswith("_") for n in names)

    def test_returns_descriptors_with_args_and_returns_keys(self):
        methods = get_scalar_query_methods(_SampleRecord())
        for m in methods:
            assert "name" in m
            assert "returns" in m
            assert "args" in m
            assert m["args"] == []  # all are nullary

    def test_pydantic_class_uses_model_fields_fast_path(self):
        """For a Pydantic v2 class, the framework methods (model_dump,
        model_validate, model_fields, …) MUST NOT appear — only the
        declared scalar fields should."""
        from test_engine.canonical.schema import CanonicalVcfRecord
        methods = get_scalar_query_methods(CanonicalVcfRecord)
        names = {m["name"] for m in methods}
        # Real fields ARE present
        assert "CHROM" in names
        assert "POS" in names
        assert "REF" in names
        # Pydantic noise is NOT
        for noisy in ("model_dump", "model_validate", "model_fields", "dict"):
            assert noisy not in names, (
                f"Pydantic-internal method {noisy!r} should be filtered out"
            )

    def test_pydantic_noise_constant_is_used(self):
        """Sanity: regression guard — the exclude set is non-empty and
        contains the most common offenders we observed leaking earlier."""
        for noisy in ("model_dump", "model_validate", "dict", "json"):
            assert noisy in _PYDANTIC_NOISE


# ---------------------------------------------------------------------------
# Invocation
# ---------------------------------------------------------------------------


class TestInvokeQueryMethod:
    def test_invokes_callable(self):
        rec = _SampleRecord()
        assert invoke_query_method(rec, "num_alleles") == 2

    def test_returns_attribute_directly(self):
        rec = _SampleRecord()
        assert invoke_query_method(rec, "CHROM") == "chr1"

    def test_returns_property_directly(self):
        rec = _SampleRecord()
        assert invoke_query_method(rec, "is_snp") is True

    def test_missing_attribute_raises(self):
        with pytest.raises(AttributeError):
            invoke_query_method(_SampleRecord(), "nonexistent")

    def test_method_failure_wraps_in_runtime_error(self):
        with pytest.raises(RuntimeError, match="boom"):
            invoke_query_method(_SampleRecord(), "crashy_method")


# ---------------------------------------------------------------------------
# run_methods_on_record (the path runners actually call)
# ---------------------------------------------------------------------------


class TestRunMethodsOnRecord:
    def test_packs_results_by_name(self):
        out = run_methods_on_record(
            _SampleRecord(), ["num_alleles", "is_biallelic", "CHROM"],
        )
        assert out == {"num_alleles": 2, "is_biallelic": True, "CHROM": "chr1"}

    def test_failure_becomes_error_dict(self):
        out = run_methods_on_record(
            _SampleRecord(), ["crashy_method", "num_alleles"],
        )
        assert "__error__" in out["crashy_method"]
        assert out["num_alleles"] == 2  # successful methods still recorded

    def test_missing_method_records_attribute_error(self):
        out = run_methods_on_record(_SampleRecord(), ["does_not_exist"])
        assert "__error__" in out["does_not_exist"]
        assert "does_not_exist" in out["does_not_exist"]["__error__"]

    def test_enum_coerced_to_name_string(self):
        import enum

        class Color(enum.Enum):
            RED = 1
            BLUE = 2

        class _Rec:
            def color(self):
                return Color.RED

        out = run_methods_on_record(_Rec(), ["color"])
        assert out["color"] == "RED"
