"""
Tests for mr_engine/agent/mr_synthesizer.py (Rank 6 coverage lever).

Uses a fake LLM + fake SpecIndex so the tests never touch the real network
or ChromaDB. The compile pipeline runs end-to-end through
``compile_mr_output``, so whitelist + query-methods validators are
exercised here — any future regression in those will surface here first.
"""

from __future__ import annotations

import json

import pytest

from mr_engine.agent.mr_synth_prompts import build_prompt
from mr_engine.agent.mr_synthesizer import synthesize_mrs


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------

class FakeLLMResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    """Stand-in matching langchain BaseChatModel.invoke() contract."""
    def __init__(self, response_text: str):
        self._text = response_text
        self.last_prompt = None

    def invoke(self, messages):
        assert isinstance(messages, list) and messages
        self.last_prompt = messages[0].content
        return FakeLLMResponse(self._text)


class RaisingLLM:
    def invoke(self, messages):
        raise RuntimeError("LLM network error")


class _FakeCollection:
    """Mimics the ChromaDB collection surface used by ``_hydrate_evidence``.
    Returns a single metadata blob per id with deterministic severity so
    compiled MRs get non-empty hydrated evidence."""
    def __init__(self, known_chunks: set[str]):
        self._known = known_chunks

    def get(self, ids, include=None):
        ids = list(ids or [])
        matched = [cid for cid in ids if cid in self._known]
        metas = [
            {"rule_severity": "CRITICAL", "section_id": "test.section"}
            for _ in matched
        ]
        return {"ids": matched, "metadatas": metas}


class FakeSpecIndex:
    def __init__(self, known_chunks: set[str]):
        self._collection = _FakeCollection(known_chunks)


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------


class TestPromptBuilder:
    def test_embeds_blindspot_and_whitelist(self):
        prompt = build_prompt(
            blindspot_context="UNCOVERED CODE: isStructural() at line 42",
            fmt="VCF",
            whitelist=["shuffle_meta_lines", "query_method_roundtrip"],
            n=3,
        )
        assert "UNCOVERED CODE: isStructural() at line 42" in prompt
        assert "shuffle_meta_lines" in prompt
        assert "query_method_roundtrip" in prompt
        # Output contract rendered
        assert "at most 3" in prompt
        assert "RawMRFromAgent" not in prompt  # implementation detail hidden

    def test_query_methods_block_appears_when_present(self):
        prompt = build_prompt(
            blindspot_context="ctx",
            fmt="VCF",
            whitelist=["shuffle_meta_lines"],
            n=2,
            query_methods=[
                {"name": "isStructural", "returns": "bool", "args": []},
                {"name": "getNAlleles", "returns": "int", "args": []},
            ],
        )
        assert "AVAILABLE QUERY METHODS" in prompt
        assert "isStructural()" in prompt
        assert "getNAlleles()" in prompt

    def test_no_query_methods_block_when_empty(self):
        prompt = build_prompt(
            blindspot_context="ctx",
            fmt="VCF",
            whitelist=["shuffle_meta_lines"],
            n=1,
            query_methods=[],
        )
        # The catalog header only appears when methods were supplied. The
        # unqualified phrase "AVAILABLE QUERY METHODS" shows up in the
        # output-contract reminder regardless, so key on the catalog
        # block's distinct "on the primary SUT (Rank 5 catalog)" marker.
        assert "on the primary SUT (Rank 5 catalog)" not in prompt

    def test_exemplars_block_when_supplied(self):
        prompt = build_prompt(
            blindspot_context="ctx",
            fmt="VCF",
            whitelist=["shuffle_meta_lines"],
            exemplars=[{"mr_name": "demo", "scope": "VCF.header",
                        "transform_steps": ["shuffle_meta_lines"]}],
        )
        assert "EXAMPLES" in prompt
        assert "demo" in prompt

    def test_rejects_unknown_format(self):
        with pytest.raises(ValueError):
            build_prompt(
                blindspot_context="ctx",
                fmt="BCF",
                whitelist=["shuffle_meta_lines"],
            )

    def test_braces_in_context_are_safe(self):
        """Regression with Java / C++ source slices containing `{` — the
        prompt must not be built via str.format() and must preserve them."""
        ctx = "isStructural(final IOPath p) { return extensionMap.stream(); }"
        prompt = build_prompt(
            blindspot_context=ctx,
            fmt="VCF",
            whitelist=["shuffle_meta_lines"],
        )
        assert ctx in prompt


# ---------------------------------------------------------------------------
# End-to-end with FakeLLM + FakeSpecIndex
# ---------------------------------------------------------------------------


def _make_mr_json(
    transform_steps: list[str],
    scope: str = "VCF.header",
    chunk_id: str = "chunk-1",
    query_methods: list[str] | None = None,
) -> dict:
    mr = {
        "mr_name": "synth-" + "-".join(transform_steps)[:20],
        "scope": scope,
        "preconditions": [],
        "transform_steps": transform_steps,
        "oracle": "parse(x) == parse(T(x))",
        "evidence": [{"chunk_id": chunk_id, "quote": "spec says so"}],
        "ambiguity_flags": [],
    }
    if query_methods is not None:
        mr["query_methods"] = query_methods
    return mr


class TestSynthesizeMrsEndToEnd:
    def test_single_valid_mr_compiled(self):
        # MR uses a transform that is definitely on the whitelist.
        mr = _make_mr_json(["shuffle_meta_lines"], scope="VCF.header")
        llm_text = "```json\n" + json.dumps([mr]) + "\n```"
        spec = FakeSpecIndex({"chunk-1"})

        out = synthesize_mrs(
            blindspot_context="uncovered header logic",
            fmt="VCF",
            spec_index=spec,
            n_mrs=3,
            llm=FakeLLM(llm_text),
        )
        assert len(out) == 1
        assert out[0].transform_steps == ["shuffle_meta_lines"]
        # mr_id must be 12 lowercase hex chars (compute_mr_id contract).
        assert len(out[0].mr_id) == 12

    def test_query_mr_with_populated_query_methods_accepted(self):
        mr = _make_mr_json(
            ["shuffle_meta_lines", "query_method_roundtrip"],
            scope="VCF.record",
            chunk_id="chunk-qm",
            query_methods=["isBiallelic", "getNAlleles"],
        )
        llm_text = "```json\n" + json.dumps([mr]) + "\n```"
        spec = FakeSpecIndex({"chunk-qm"})

        out = synthesize_mrs(
            blindspot_context="uncovered SV logic",
            fmt="VCF",
            spec_index=spec,
            llm=FakeLLM(llm_text),
        )
        assert len(out) == 1
        assert out[0].query_methods == ["isBiallelic", "getNAlleles"]

    def test_query_mr_with_empty_query_methods_rejected(self):
        """The Pydantic validator added after Phase D run 5 must still
        reject an MR that includes query_method_roundtrip but leaves
        query_methods empty — even through the synthesizer path."""
        mr = _make_mr_json(
            ["shuffle_meta_lines", "query_method_roundtrip"],
            scope="VCF.record",
            chunk_id="chunk-qm",
            # query_methods omitted -> defaults to []
        )
        llm_text = "```json\n" + json.dumps([mr]) + "\n```"
        spec = FakeSpecIndex({"chunk-qm"})
        out = synthesize_mrs(
            blindspot_context="uncovered SV logic",
            fmt="VCF",
            spec_index=spec,
            llm=FakeLLM(llm_text),
        )
        # Whole batch rejected -> empty list, non-fatal.
        assert out == []

    def test_hallucinated_chunk_id_rejected(self):
        """Evidence hydration must drop MRs referencing unknown chunk_ids."""
        mr = _make_mr_json(["shuffle_meta_lines"], chunk_id="not-in-index")
        llm_text = "```json\n" + json.dumps([mr]) + "\n```"
        spec = FakeSpecIndex(set())  # empty index
        out = synthesize_mrs(
            blindspot_context="ctx",
            fmt="VCF",
            spec_index=spec,
            llm=FakeLLM(llm_text),
        )
        assert out == []

    def test_unknown_transform_rejected(self):
        mr = _make_mr_json(["does_not_exist_transform"])
        llm_text = "```json\n" + json.dumps([mr]) + "\n```"
        spec = FakeSpecIndex({"chunk-1"})
        out = synthesize_mrs(
            blindspot_context="ctx",
            fmt="VCF",
            spec_index=spec,
            llm=FakeLLM(llm_text),
        )
        assert out == []

    def test_empty_blindspot_returns_empty(self):
        class NotCalledLLM:
            def invoke(self, messages):  # pragma: no cover
                raise AssertionError("LLM should not be invoked on empty ctx")
        out = synthesize_mrs(
            blindspot_context="",
            fmt="VCF",
            spec_index=FakeSpecIndex(set()),
            llm=NotCalledLLM(),
        )
        assert out == []

    def test_unsupported_format_returns_empty(self):
        out = synthesize_mrs(
            blindspot_context="ctx",
            fmt="BCF",
            spec_index=FakeSpecIndex(set()),
            llm=FakeLLM("whatever"),
        )
        assert out == []

    def test_llm_exception_is_non_fatal(self):
        out = synthesize_mrs(
            blindspot_context="ctx",
            fmt="VCF",
            spec_index=FakeSpecIndex({"chunk-1"}),
            llm=RaisingLLM(),
        )
        assert out == []

    def test_malformed_json_returns_empty(self):
        out = synthesize_mrs(
            blindspot_context="ctx",
            fmt="VCF",
            spec_index=FakeSpecIndex({"chunk-1"}),
            llm=FakeLLM("not even a code fence"),
        )
        assert out == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
