"""
Tests for the Tier-2b mutator catalog reflection helper
(``test_engine.runners.introspection.get_mutator_methods``) and the
opt-in contract on ``test_engine.runners.base.ParserRunner``.

All fixtures are plain Python classes — no SUT dependency.
"""

from __future__ import annotations

from typing import Optional

import pytest

from test_engine.runners.introspection import get_mutator_methods


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

class _PlainMutators:
    """A vanilla Python class with a mix of getters, mutators, and dunders."""

    def get_alleles(self) -> list:  # pragma: no cover — reflection only
        return []

    # Mutators — should be discovered.
    def set_alleles(self, alleles: list) -> None: ...
    def add_filter(self, flag: str) -> None: ...
    def remove_filter(self, flag: str) -> None: ...
    def clear_filters(self) -> None: ...
    def put_attribute(self, k: str, v: int) -> None: ...
    def reset(self) -> None: ...
    def replace_quality(self, q: float) -> None: ...

    # Private / dunder / non-mutator — should be skipped.
    def _private_set(self) -> None: ...
    def __init__(self) -> None: ...
    def compute(self) -> int:  # pragma: no cover
        return 0


class _FluentBuilder:
    """A fluent builder whose mutators return self — still mutators."""

    def add_read(self, read: str) -> "_FluentBuilder":
        return self

    def set_tag(self, k: str, v: str) -> "_FluentBuilder":
        return self

    def build(self) -> object:  # pragma: no cover — not a mutator prefix
        return object()


# ---------------------------------------------------------------------------
# Reflection on plain classes
# ---------------------------------------------------------------------------

class TestGetMutatorMethodsOnPlainClass:
    def test_discovers_all_standard_prefixes(self):
        ms = get_mutator_methods(_PlainMutators)
        names = {m["name"] for m in ms}
        # Every standard mutator verb present → discovered.
        assert "set_alleles" in names
        assert "add_filter" in names
        assert "remove_filter" in names
        assert "clear_filters" in names
        assert "put_attribute" in names
        assert "reset" in names
        assert "replace_quality" in names

    def test_skips_private_and_dunder(self):
        ms = get_mutator_methods(_PlainMutators)
        names = {m["name"] for m in ms}
        assert "_private_set" not in names
        assert "__init__" not in names

    def test_skips_non_mutator_prefix_methods(self):
        ms = get_mutator_methods(_PlainMutators)
        names = {m["name"] for m in ms}
        assert "compute" not in names  # starts with 'c' but not 'clear'
        assert "get_alleles" not in names  # getter, not mutator

    def test_descriptor_shape(self):
        ms = get_mutator_methods(_PlainMutators)
        setter = next(m for m in ms if m["name"] == "set_alleles")
        assert isinstance(setter["name"], str)
        assert isinstance(setter["returns"], str)
        assert isinstance(setter["args"], list)
        # set_alleles(self, alleles: list) → one arg (alleles) rendered.
        assert len(setter["args"]) == 1

    def test_limit_cap(self):
        ms = get_mutator_methods(_PlainMutators, limit=3)
        assert len(ms) == 3


class TestGetMutatorMethodsOnFluentBuilder:
    def test_fluent_returning_self_is_accepted(self):
        ms = get_mutator_methods(_FluentBuilder)
        names = {m["name"] for m in ms}
        assert "add_read" in names
        assert "set_tag" in names
        # 'build' is not a mutator prefix — excluded.
        assert "build" not in names


# ---------------------------------------------------------------------------
# Pydantic fast path
# ---------------------------------------------------------------------------

class TestGetMutatorMethodsOnPydanticModel:
    def test_pydantic_model_fields_enumerated(self):
        from pydantic import BaseModel

        class _Model(BaseModel):
            x: int
            y: Optional[str] = None

        ms = get_mutator_methods(_Model)
        names = {m["name"] for m in ms}
        assert "x" in names
        assert "y" in names

    def test_pydantic_frozen_field_excluded(self):
        from pydantic import BaseModel, Field

        class _FrozenModel(BaseModel):
            name: str = Field(frozen=True)
            score: int = 0

        ms = get_mutator_methods(_FrozenModel)
        names = {m["name"] for m in ms}
        assert "name" not in names  # frozen → excluded
        assert "score" in names


# ---------------------------------------------------------------------------
# Prompt block rendering
# ---------------------------------------------------------------------------

class TestPromptMutatorBlock:
    def test_build_prompt_with_mutator_catalog(self):
        from mr_engine.agent.mr_synth_prompts import build_prompt
        out = build_prompt(
            blindspot_context="ctx",
            fmt="VCF",
            whitelist=["shuffle_meta_lines"],
            mutator_catalog=[
                {"name": "add_filter", "returns": "None", "args": ["str"]},
                {"name": "set_alleles", "returns": "None", "args": ["list"]},
            ],
        )
        assert "AVAILABLE MUTATOR METHODS" in out
        assert "add_filter" in out
        assert "set_alleles" in out

    def test_build_prompt_without_mutator_catalog_skips_block(self):
        from mr_engine.agent.mr_synth_prompts import build_prompt
        out = build_prompt(
            blindspot_context="ctx",
            fmt="VCF",
            whitelist=["shuffle_meta_lines"],
            mutator_catalog=[],
        )
        # Header only appears when the catalog is populated.
        assert "AVAILABLE MUTATOR METHODS" not in out


# ---------------------------------------------------------------------------
# Runner base opt-in contract
# ---------------------------------------------------------------------------

class TestRunnerBaseMutatorContract:
    def test_base_defaults(self):
        from test_engine.runners.base import ParserRunner
        # Base class advertises False; an empty list is returned.
        assert ParserRunner.supports_mutator_methods is False

    def test_reference_runner_opts_in(self):
        from test_engine.runners.reference_runner import ReferenceRunner
        assert ReferenceRunner.supports_mutator_methods is True

    def test_biopython_runner_opts_in(self):
        from test_engine.runners.biopython_runner import BiopythonRunner
        assert BiopythonRunner.supports_mutator_methods is True

    def test_pysam_runner_opts_in(self):
        from test_engine.runners.pysam_runner import PysamRunner
        assert PysamRunner.supports_mutator_methods is True

    def test_reference_runner_discovers_for_vcf(self):
        from test_engine.runners.reference_runner import ReferenceRunner
        r = ReferenceRunner()
        ms = r.discover_mutator_methods("VCF")
        assert isinstance(ms, list)
        # CanonicalVcfRecord has at least one non-frozen field → non-empty.
        assert len(ms) > 0
        # Descriptor shape is {name, returns, args}.
        for m in ms:
            assert {"name", "returns", "args"} <= set(m.keys())

    def test_reference_runner_discovers_for_sam(self):
        from test_engine.runners.reference_runner import ReferenceRunner
        r = ReferenceRunner()
        ms = r.discover_mutator_methods("SAM")
        assert isinstance(ms, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
