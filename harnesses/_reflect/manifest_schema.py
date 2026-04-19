"""
Pydantic model for the uniform `methods_manifest.json` shape.

This file is the single source of truth for what a discovered query
method looks like across languages. Both libclang_walker.py (C/C++)
and rustdoc_parser.py (Rust) emit instances of this schema; the
framework's `ParserRunner.discover_query_methods` returns the same
shape natively from Python and Java.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MethodDescriptor(BaseModel):
    """One public scalar-returning, effectively-nullary query method."""
    name: str = Field(..., description="Method or property name.")
    returns: str = Field(
        ..., description="Return-type hint (best-effort string).",
    )
    args: list[str] = Field(
        default_factory=list,
        description="Argument-type hints. Empty for nullary methods.",
    )
    # Source language — informational; not used by the oracle. Helps
    # downstream tooling render per-language hints to the LLM.
    language: Literal["python", "java", "c", "cpp", "rust"] | None = None


class MethodsManifest(BaseModel):
    """The full discovered API surface for one SUT's parsed-record class."""
    sut_name: str = Field(
        ..., description="SUT identifier (e.g. 'htsjdk', 'pysam', 'my_rust_parser').",
    )
    record_type: str = Field(
        ..., description="Fully-qualified parsed-record type name "
                         "(e.g. 'htsjdk.variant.variantcontext.VariantContext').",
    )
    methods: list[MethodDescriptor] = Field(default_factory=list)
