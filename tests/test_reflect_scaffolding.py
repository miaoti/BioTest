"""
Tests for the shared reflection scaffolding (`harnesses/_reflect/`).

Covers:
- The Pydantic manifest schema (round-trip + validation).
- rustdoc_parser on a small synthetic rustdoc-JSON fixture.
- libclang_walker is exercised IF libclang is installed; skipped
  otherwise (it's not a hard runtime dep — the C / C++ template
  harnesses bring it in only when those SUTs are onboarded).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from harnesses._reflect.manifest_schema import (
    MethodDescriptor,
    MethodsManifest,
)
from harnesses._reflect.rustdoc_parser import parse_rustdoc


class TestManifestSchema:
    def test_round_trip(self):
        m = MethodsManifest(
            sut_name="my_parser",
            record_type="my_parser::Record",
            methods=[
                MethodDescriptor(
                    name="is_structural", returns="bool",
                    args=[], language="rust",
                ),
                MethodDescriptor(
                    name="get_n_alleles", returns="i32",
                    args=[], language="rust",
                ),
            ],
        )
        blob = m.model_dump_json()
        m2 = MethodsManifest.model_validate_json(blob)
        assert m2.sut_name == "my_parser"
        assert len(m2.methods) == 2
        assert m2.methods[0].name == "is_structural"

    def test_default_args_empty(self):
        d = MethodDescriptor(name="foo", returns="bool")
        assert d.args == []

    def test_unknown_language_rejected(self):
        with pytest.raises(Exception):
            MethodDescriptor(
                name="foo", returns="bool", language="cobol",
            )


# ---------------------------------------------------------------------------
# Synthetic rustdoc JSON fixture — minimal shape rustdoc emits.
# ---------------------------------------------------------------------------


def _make_rustdoc_blob() -> dict:
    """Hand-rolled mini rustdoc JSON with one struct + one impl."""
    return {
        "format_version": 28,
        "index": {
            "0:1": {
                "name": "Record",
                "kind": "struct",
                "visibility": "public",
                "inner": {
                    "struct": {"impls": ["0:2"]},
                },
            },
            "0:2": {
                "name": None,
                "kind": "impl",
                "visibility": "default",
                "inner": {
                    "impl": {
                        "trait": None,
                        "items": ["0:3", "0:4", "0:5", "0:6"],
                    },
                },
            },
            # bool getter — admitted
            "0:3": {
                "name": "is_structural",
                "kind": "function",
                "visibility": "public",
                "inner": {
                    "function": {
                        "decl": {
                            "inputs": [["self", {"borrowed_ref": {"mutable": False, "type": {"resolved_path": {"name": "Record"}}}}]],
                            "output": {"primitive": "bool"},
                        },
                    },
                },
            },
            # i32 getter — admitted
            "0:4": {
                "name": "n_alleles",
                "kind": "function",
                "visibility": "public",
                "inner": {
                    "function": {
                        "decl": {
                            "inputs": [["self", {"borrowed_ref": {"mutable": False, "type": {"resolved_path": {"name": "Record"}}}}]],
                            "output": {"primitive": "i32"},
                        },
                    },
                },
            },
            # &mut self — REJECTED
            "0:5": {
                "name": "set_chrom",
                "kind": "function",
                "visibility": "public",
                "inner": {
                    "function": {
                        "decl": {
                            "inputs": [["self", {"borrowed_ref": {"mutable": True, "type": {"resolved_path": {"name": "Record"}}}}]],
                            "output": {"primitive": "i32"},
                        },
                    },
                },
            },
            # Vec<u8> output — REJECTED (not in scalar set)
            "0:6": {
                "name": "raw_bytes",
                "kind": "function",
                "visibility": "public",
                "inner": {
                    "function": {
                        "decl": {
                            "inputs": [["self", {"borrowed_ref": {"mutable": False, "type": {"resolved_path": {"name": "Record"}}}}]],
                            "output": {"resolved_path": {"name": "Vec", "args": {"angle_bracketed": {"args": [{"type": {"primitive": "u8"}}]}}}},
                        },
                    },
                },
            },
        },
        "paths": {},
        "external_crates": {},
    }


class TestRustdocParser:
    def test_admits_scalar_self_getters(self):
        blob = _make_rustdoc_blob()
        manifest = parse_rustdoc(blob, "Record", "test_sut")
        names = {m.name for m in manifest.methods}
        assert "is_structural" in names
        assert "n_alleles" in names

    def test_rejects_mut_self(self):
        blob = _make_rustdoc_blob()
        manifest = parse_rustdoc(blob, "Record", "test_sut")
        names = {m.name for m in manifest.methods}
        assert "set_chrom" not in names, (
            "rustdoc parser must skip &mut self methods (mutators)"
        )

    def test_rejects_non_scalar_return(self):
        blob = _make_rustdoc_blob()
        manifest = parse_rustdoc(blob, "Record", "test_sut")
        names = {m.name for m in manifest.methods}
        assert "raw_bytes" not in names, (
            "Vec<u8> is not a scalar return — must not appear in manifest"
        )

    def test_unknown_type_yields_empty(self):
        blob = _make_rustdoc_blob()
        manifest = parse_rustdoc(blob, "NoSuchType", "test_sut")
        assert manifest.methods == []
        assert manifest.sut_name == "test_sut"

    def test_returns_strings_are_renderable(self):
        blob = _make_rustdoc_blob()
        manifest = parse_rustdoc(blob, "Record", "test_sut")
        for m in manifest.methods:
            assert m.returns  # non-empty
            assert isinstance(m.returns, str)


# ---------------------------------------------------------------------------
# libclang walker — skipped unless libclang is installed
# ---------------------------------------------------------------------------


def _has_libclang() -> bool:
    try:
        import clang.cindex  # noqa: F401
        return True
    except ImportError:
        return False


@pytest.mark.skipif(not _has_libclang(), reason="libclang not installed")
class TestLibclangWalkerC:
    def test_admits_scalar_getter(self, tmp_path):
        from harnesses._reflect.libclang_walker import walk_c_header
        header = tmp_path / "rec.h"
        header.write_text(
            "#ifndef REC_H\n#define REC_H\n"
            "struct Record { int dummy; };\n"
            "int rec_n_alleles(const struct Record *r);\n"
            "_Bool rec_is_structural(const struct Record *r);\n"
            "void rec_set_chrom(struct Record *r);\n"  # mutator — skipped
            "#endif\n",
        )
        manifest = walk_c_header(header, "Record", "demo_c")
        names = {m.name for m in manifest.methods}
        assert "rec_n_alleles" in names
        assert "rec_is_structural" in names
