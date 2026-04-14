"""
Tests for Phase C: deep_equal algorithm.
"""

import pytest
from test_engine.oracles.deep_equal import deep_equal, deep_equal_multiset, all_equal


class TestDeepEqualBasic:
    def test_identical_dicts(self):
        a = {"x": 1, "y": "hello"}
        eq, diffs = deep_equal(a, a)
        assert eq is True
        assert diffs == []

    def test_dict_key_order_ignored(self):
        a = {"b": 2, "a": 1}
        b = {"a": 1, "b": 2}
        eq, diffs = deep_equal(a, b)
        assert eq is True

    def test_dict_missing_key(self):
        a = {"a": 1}
        b = {"a": 1, "b": 2}
        eq, diffs = deep_equal(a, b)
        assert eq is False
        assert any("missing" in d for d in diffs)

    def test_none_equality(self):
        eq, _ = deep_equal(None, None)
        assert eq is True

    def test_none_vs_value(self):
        eq, diffs = deep_equal(None, 42)
        assert eq is False

    def test_string_exact(self):
        eq, _ = deep_equal("abc", "abc")
        assert eq is True
        eq2, _ = deep_equal("abc", "xyz")
        assert eq2 is False

    def test_int_exact(self):
        eq, _ = deep_equal(42, 42)
        assert eq is True
        eq2, _ = deep_equal(42, 43)
        assert eq2 is False

    def test_bool_exact(self):
        eq, _ = deep_equal(True, True)
        assert eq is True


class TestDeepEqualFloat:
    def test_float_within_tolerance(self):
        eq, _ = deep_equal(0.1 + 0.2, 0.3, float_tol=1e-6)
        assert eq is True

    def test_float_outside_tolerance(self):
        eq, diffs = deep_equal(1.0, 2.0, float_tol=0.5)
        assert eq is False

    def test_int_vs_float(self):
        eq, _ = deep_equal(42, 42.0)
        assert eq is True

    def test_qual_field_tolerance(self):
        """QUAL uses wider tolerance (0.01)."""
        a = {"QUAL": 29.001}
        b = {"QUAL": 29.005}
        eq, _ = deep_equal(a, b)
        assert eq is True


class TestDeepEqualCollections:
    def test_list_ordered(self):
        eq, _ = deep_equal([1, 2, 3], [1, 2, 3])
        assert eq is True
        eq2, _ = deep_equal([1, 2, 3], [3, 2, 1])
        assert eq2 is False

    def test_list_length_mismatch(self):
        eq, diffs = deep_equal([1, 2], [1, 2, 3])
        assert eq is False
        assert any("length" in d for d in diffs)

    def test_set_order_ignored(self):
        eq, _ = deep_equal({"a", "b", "c"}, {"c", "a", "b"})
        assert eq is True

    def test_set_difference(self):
        eq, diffs = deep_equal({"a", "b"}, {"b", "c"})
        assert eq is False


class TestDeepEqualNested:
    def test_nested_dict(self):
        a = {"records": [{"CHROM": "chr1", "POS": 100}]}
        b = {"records": [{"CHROM": "chr1", "POS": 100}]}
        eq, _ = deep_equal(a, b)
        assert eq is True

    def test_nested_diff_path(self):
        a = {"records": [{"CHROM": "chr1", "POS": 100}]}
        b = {"records": [{"CHROM": "chr1", "POS": 200}]}
        eq, diffs = deep_equal(a, b)
        assert eq is False
        assert any("records" in d and "POS" in d for d in diffs)


class TestDeepEqualMultiset:
    def test_multiset_equal(self):
        eq, _ = deep_equal_multiset(["b", "a", "c"], ["c", "b", "a"])
        assert eq is True

    def test_multiset_different(self):
        eq, _ = deep_equal_multiset(["a", "b"], ["a", "c"])
        assert eq is False


class TestAllEqual:
    def test_all_agree(self):
        results = {"p1": {"x": 1}, "p2": {"x": 1}, "p3": {"x": 1}}
        agree, pairwise = all_equal(results)
        assert agree is True

    def test_one_disagrees(self):
        results = {"p1": {"x": 1}, "p2": {"x": 2}, "p3": {"x": 1}}
        agree, pairwise = all_equal(results)
        assert agree is False
        assert any(len(d) > 0 for d in pairwise.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
