"""
Integration test for Phase B: full pipeline simulation.

This test exercises the complete compilation → hydration → hashing → triage
pipeline using realistic mock LLM output against the live ChromaDB index.
No LLM API calls are made — only ChromaDB queries and Pydantic validation.
"""

import json
import logging
import tempfile

import pytest

logging.basicConfig(level=logging.INFO)


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture(scope="module")
def spec_index():
    """Load the ephemeral SpecIndex once for all tests in this module."""
    from mr_engine.index_loader import get_ephemeral_index
    return get_ephemeral_index()


@pytest.fixture(scope="module")
def real_chunk_ids(spec_index):
    """Get real chunk_ids from ChromaDB for realistic test fixtures."""
    # Query for VCF meta-information ordering rules
    r1 = spec_index.query("VCF header meta-information line ordering", n_results=2,
                          where={"format": "VCF"})
    # Query for SAM optional tag ordering
    r2 = spec_index.query("SAM optional fields tags order", n_results=2,
                          where={"format": "SAM"})
    # Query for VCF ALT allele ordering and Number=A
    r3 = spec_index.query("ALT allele order Number=A values same order", n_results=2,
                          where={"format": "VCF"})
    return {
        "vcf_ordering": [(r1["ids"][0][i], r1["documents"][0][i][:100],
                          r1["metadatas"][0][i]) for i in range(len(r1["ids"][0]))],
        "sam_tags": [(r2["ids"][0][i], r2["documents"][0][i][:100],
                      r2["metadatas"][0][i]) for i in range(len(r2["ids"][0]))],
        "vcf_alt": [(r3["ids"][0][i], r3["documents"][0][i][:100],
                      r3["metadatas"][0][i]) for i in range(len(r3["ids"][0]))],
    }


# ===========================================================================
# Test 1: ChromaDB query tool integration
# ===========================================================================

class TestToolIntegration:
    """Test the query_spec_database LangChain tool against live ChromaDB."""

    def test_query_returns_results(self, spec_index):
        result = spec_index.query("VCF header ordering", n_results=3)
        assert len(result["ids"][0]) == 3
        assert all(d < 0.5 for d in result["distances"][0])

    def test_format_filter_works(self, spec_index):
        result = spec_index.query("CIGAR operations",
                                  n_results=3, where={"format": "SAM"})
        for meta in result["metadatas"][0]:
            assert meta["format"] == "SAM"

    def test_severity_filter_works(self, spec_index):
        result = spec_index.query("MUST", n_results=5,
                                  where={"rule_severity": "CRITICAL"})
        for meta in result["metadatas"][0]:
            assert meta["rule_severity"] == "CRITICAL"

    def test_rejection_threshold(self, spec_index):
        """Irrelevant queries should have high distances."""
        result = spec_index.query("chocolate cake recipe", n_results=3)
        assert all(d > 0.39 for d in result["distances"][0])

    def test_collection_stats(self, spec_index):
        stats = spec_index.collection_stats()
        assert stats["total_documents"] > 1000


# ===========================================================================
# Test 2: Full compilation pipeline with real chunk_ids
# ===========================================================================

class TestCompilationPipeline:
    """Test compile_mr_output with realistic mock LLM output + live ChromaDB."""

    def test_valid_vcf_ordering_mr(self, spec_index, real_chunk_ids):
        """Simulate LLM output for VCF ordering invariance MR."""
        chunks = real_chunk_ids["vcf_ordering"]
        mock_llm_output = json.dumps([{
            "mr_name": "VCF Header Meta-Info Shuffle",
            "scope": "VCF.header",
            "preconditions": ["header has at least 2 meta-information lines"],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "Shuffling meta-information lines must not change parsed semantics",
            "evidence": [{
                "chunk_id": chunks[0][0],
                "quote": chunks[0][1],
            }],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_llm_output, spec_index)

        assert result.success, f"Compilation failed: {result.error_detail}"
        assert len(result.relations) == 1

        mr = result.relations[0]
        assert mr.mr_name == "VCF Header Meta-Info Shuffle"
        assert mr.scope == "VCF.header"
        assert mr.transform_steps == ["shuffle_meta_lines"]
        assert len(mr.mr_id) == 12  # deterministic hash
        assert mr.evidence[0].rule_severity in ("CRITICAL", "ADVISORY", "INFORMATIONAL")
        assert mr.evidence[0].section_id  # hydrated from ChromaDB

    def test_valid_sam_tag_ordering_mr(self, spec_index, real_chunk_ids):
        """Simulate LLM output for SAM tag ordering invariance MR."""
        chunks = real_chunk_ids["sam_tags"]
        mock_llm_output = json.dumps([{
            "mr_name": "SAM Optional Tag Reorder",
            "scope": "SAM.record",
            "preconditions": ["record has at least 2 optional tags"],
            "transform_steps": ["permute_optional_tag_fields"],
            "oracle": "Reordering optional tags must not change alignment semantics",
            "evidence": [{
                "chunk_id": chunks[0][0],
                "quote": chunks[0][1],
            }],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_llm_output, spec_index)

        assert result.success, f"Compilation failed: {result.error_detail}"
        mr = result.relations[0]
        assert mr.scope == "SAM.record"

    def test_valid_alt_permutation_mr(self, spec_index, real_chunk_ids):
        """Simulate LLM output for VCF ALT permutation MR."""
        chunks = real_chunk_ids["vcf_alt"]
        mock_llm_output = json.dumps([{
            "mr_name": "VCF ALT Permutation with GT Remap",
            "scope": "VCF.record",
            "preconditions": [
                "record.alt_count >= 2",
                "record.has_format_key('GT')",
            ],
            "transform_steps": [
                "choose_permutation",
                "permute_ALT",
                "remap_GT",
                "permute_Number_A_R_fields",
            ],
            "oracle": "Biological semantics must be preserved after ALT reordering",
            "evidence": [{
                "chunk_id": chunks[0][0],
                "quote": chunks[0][1],
            }],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_llm_output, spec_index)

        assert result.success, f"Compilation failed: {result.error_detail}"
        mr = result.relations[0]
        assert len(mr.transform_steps) == 4
        assert "choose_permutation" in mr.transform_steps

    def test_multiple_mrs_in_batch(self, spec_index, real_chunk_ids):
        """Simulate LLM returning multiple MRs at once."""
        vcf_chunks = real_chunk_ids["vcf_ordering"]
        sam_chunks = real_chunk_ids["sam_tags"]

        mock_llm_output = json.dumps([
            {
                "mr_name": "VCF INFO Field Shuffle",
                "scope": "VCF.record",
                "preconditions": ["INFO has multiple key-value pairs"],
                "transform_steps": ["shuffle_info_field_kv"],
                "oracle": "INFO field ordering is irrelevant to semantics",
                "evidence": [{"chunk_id": vcf_chunks[0][0], "quote": "test"}],
                "ambiguity_flags": [],
            },
            {
                "mr_name": "SAM Header SQ Reorder",
                "scope": "SAM.header",
                "preconditions": ["header has multiple @SQ lines"],
                "transform_steps": ["reorder_header_records"],
                "oracle": "@SQ order must not affect downstream analysis",
                "evidence": [{"chunk_id": sam_chunks[0][0], "quote": "test"}],
                "ambiguity_flags": ["spec says SHOULD, not MUST"],
            },
        ])

        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_llm_output, spec_index)

        assert result.success
        assert len(result.relations) == 2
        # Different MRs should have different mr_ids
        assert result.relations[0].mr_id != result.relations[1].mr_id

    def test_markdown_fenced_json(self, spec_index, real_chunk_ids):
        """LLMs often wrap JSON in markdown code fences."""
        chunks = real_chunk_ids["vcf_ordering"]
        mock_output = f"""Here are the MRs I found:

```json
[{{
    "mr_name": "VCF Structured KV Reorder",
    "scope": "VCF.header",
    "preconditions": ["structured meta-info line exists"],
    "transform_steps": ["permute_structured_kv_order"],
    "oracle": "Key-value order in structured lines is irrelevant",
    "evidence": [{{"chunk_id": "{chunks[0][0]}", "quote": "test"}}],
    "ambiguity_flags": []
}}]
```

These are based on normative spec evidence.
"""
        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_output, spec_index)

        assert result.success, f"Failed: {result.error_detail}"


# ===========================================================================
# Test 3: Whitelist enforcement
# ===========================================================================

class TestWhitelistEnforcement:
    """Verify that non-whitelisted transforms are rejected."""

    def test_unknown_transform_fails(self, spec_index, real_chunk_ids):
        chunks = real_chunk_ids["vcf_ordering"]
        mock_output = json.dumps([{
            "mr_name": "Bad MR",
            "scope": "VCF.header",
            "preconditions": [],
            "transform_steps": ["hallucinated_transform_function"],
            "oracle": "test",
            "evidence": [{"chunk_id": chunks[0][0], "quote": "test"}],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_output, spec_index)

        assert not result.success
        assert "whitelist" in result.error_detail.lower()

    def test_hallucinated_chunk_id_fails(self, spec_index):
        """Fake chunk_ids must be caught during hydration."""
        mock_output = json.dumps([{
            "mr_name": "Hallucinated Evidence MR",
            "scope": "VCF.header",
            "preconditions": [],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "test",
            "evidence": [{"chunk_id": "FAKE_NONEXISTENT_CHUNK_12345", "quote": "made up"}],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        result = compile_mr_output(mock_output, spec_index)

        assert not result.success
        assert "not found" in result.error_detail.lower() or "hallucination" in result.error_detail.lower()


# ===========================================================================
# Test 4: Deterministic hashing + dedup
# ===========================================================================

class TestDedupIntegration:
    """Test that the deterministic hash and registry dedup work end-to-end."""

    def test_same_transforms_same_id(self, spec_index, real_chunk_ids):
        """Two MRs with same scope+transforms but different names get same mr_id."""
        chunks = real_chunk_ids["vcf_ordering"]

        mr1_json = json.dumps([{
            "mr_name": "Header Shuffle Version A",
            "scope": "VCF.header",
            "preconditions": [],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "test",
            "evidence": [{"chunk_id": chunks[0][0], "quote": "a"}],
            "ambiguity_flags": [],
        }])
        mr2_json = json.dumps([{
            "mr_name": "Header Shuffle Version B (different name!)",
            "scope": "VCF.header",
            "preconditions": ["different precondition"],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "different oracle",
            "evidence": [{"chunk_id": chunks[0][0], "quote": "b"}],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        r1 = compile_mr_output(mr1_json, spec_index)
        r2 = compile_mr_output(mr2_json, spec_index)

        assert r1.success and r2.success
        assert r1.relations[0].mr_id == r2.relations[0].mr_id

        # Registry dedup
        from mr_engine.registry import triage
        reg = triage(r1.relations + r2.relations)
        assert reg.total == 1  # deduped!


# ===========================================================================
# Test 5: Full triage with hydrated severity
# ===========================================================================

class TestTriageWithHydration:
    """Test that triage correctly uses ChromaDB-hydrated severity."""

    def test_critical_evidence_goes_enforced(self, spec_index, real_chunk_ids):
        chunks = real_chunk_ids["vcf_ordering"]

        mock_output = json.dumps([{
            "mr_name": "Test Enforced",
            "scope": "VCF.header",
            "preconditions": [],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "test",
            "evidence": [{"chunk_id": chunks[0][0], "quote": "test"}],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        from mr_engine.registry import triage

        result = compile_mr_output(mock_output, spec_index)
        assert result.success

        mr = result.relations[0]
        # Check that severity was hydrated from ChromaDB
        assert mr.evidence[0].rule_severity in ("CRITICAL", "ADVISORY", "INFORMATIONAL")

        reg = triage(result.relations)
        if all(ev.rule_severity == "CRITICAL" for ev in mr.evidence) and not mr.ambiguity_flags:
            assert mr.mr_id in reg.enforced
        else:
            assert mr.mr_id in reg.quarantine

    def test_ambiguity_forces_quarantine(self, spec_index, real_chunk_ids):
        chunks = real_chunk_ids["vcf_ordering"]

        mock_output = json.dumps([{
            "mr_name": "Ambiguous MR",
            "scope": "VCF.header",
            "preconditions": [],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "test",
            "evidence": [{"chunk_id": chunks[0][0], "quote": "test"}],
            "ambiguity_flags": ["spec uses MAY not MUST"],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        from mr_engine.registry import triage

        result = compile_mr_output(mock_output, spec_index)
        assert result.success

        reg = triage(result.relations)
        assert result.relations[0].mr_id in reg.quarantine


# ===========================================================================
# Test 6: Registry export
# ===========================================================================

class TestRegistryExport:
    def test_export_with_hydrated_mrs(self, spec_index, real_chunk_ids):
        """Full pipeline: compile -> triage -> export JSON."""
        import os
        chunks = real_chunk_ids["vcf_ordering"]

        mock_output = json.dumps([{
            "mr_name": "Export Test MR",
            "scope": "VCF.header",
            "preconditions": ["test"],
            "transform_steps": ["shuffle_meta_lines"],
            "oracle": "test oracle",
            "evidence": [{"chunk_id": chunks[0][0], "quote": "spec text"}],
            "ambiguity_flags": [],
        }])

        from mr_engine.dsl.compiler import compile_mr_output
        from mr_engine.registry import triage, export_registry

        result = compile_mr_output(mock_output, spec_index)
        assert result.success

        reg = triage(result.relations)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name

        try:
            export_registry(reg, path)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert "enforced" in data
            assert "quarantine" in data
            assert data["summary"]["total"] == 1
            # Verify hydrated evidence is in the export
            all_mrs = data["enforced"] + data["quarantine"]
            assert len(all_mrs) == 1
            assert "rule_severity" in all_mrs[0]["evidence"][0]
            assert "section_id" in all_mrs[0]["evidence"][0]
        finally:
            os.unlink(path)


# ===========================================================================
# Test 7: Behavior targets + prompt construction
# ===========================================================================

class TestPromptIntegration:
    def test_all_targets_produce_valid_prompts(self):
        from mr_engine.behavior import get_all_targets
        from mr_engine.agent.prompts import build_system_prompt

        for target in get_all_targets():
            for fmt in ["VCF", "SAM"]:
                prompt = build_system_prompt(target, fmt)
                # Format-appropriate whitelist entry must appear.
                if fmt == "VCF":
                    assert "shuffle_meta_lines" in prompt
                else:  # SAM
                    assert "permute_optional_tag_fields" in prompt
                # Must ask for mr_name, NOT mr_id
                assert "mr_name" in prompt
                assert "mr_id" not in prompt.split("Output")[1] if "Output" in prompt else True
                # Must contain the format
                assert fmt in prompt
                # Must contain behavior description
                assert target.value in prompt

    def test_primary_target_block_appears_when_set(self):
        # When the caller passes primary_target, the prompt gains a
        # SUT-SELECTION RULE header that the LLM uses to align
        # SUT-specific transforms (e.g. htsjdk_write_roundtrip) with
        # the actual target. Without this header the LLM would have to
        # infer the target from the menu's contextual hints alone.
        from mr_engine.behavior import BehaviorTarget
        from mr_engine.agent.prompts import build_system_prompt

        prompt = build_system_prompt(
            BehaviorTarget.ROUND_TRIP_INVARIANCE, "VCF",
            primary_target="htsjdk",
            available_suts=["htsjdk", "pysam", "reference"],
        )
        assert "PRIMARY TARGET FOR THIS RUN" in prompt
        assert "htsjdk" in prompt
        # With the Option-C collapse, the per-SUT SUT-SELECTION RULE is
        # gone; the prompt now carries a single WRITER-TRANSFORM NOTE
        # explaining that sut_write_roundtrip is SUT-agnostic.
        assert "WRITER-TRANSFORM NOTE" in prompt
        assert "sut_write_roundtrip" in prompt
        # Available SUT list must render.
        assert "Available SUTs in this runtime: htsjdk, pysam, reference" in prompt

    def test_no_primary_target_block_when_unset(self):
        # Legacy path: when no primary_target is given, the new header
        # must NOT appear (preserves old prompt shape for callers that
        # predate this wiring, e.g. standalone smoke tests).
        from mr_engine.behavior import BehaviorTarget
        from mr_engine.agent.prompts import build_system_prompt

        prompt = build_system_prompt(
            BehaviorTarget.ROUND_TRIP_INVARIANCE, "VCF",
        )
        assert "PRIMARY TARGET FOR THIS RUN" not in prompt
        assert "WRITER-TRANSFORM NOTE" not in prompt

    def test_writer_transform_hidden_when_primary_lacks_writer(self):
        # When runtime_capabilities does NOT include primary_sut_has_writer,
        # sut_write_roundtrip must be filtered out of the LLM's transform
        # menu — otherwise the LLM would pick it, the transform would
        # no-op (runner lacks a writer), and an MR slot would be wasted.
        from mr_engine.behavior import BehaviorTarget
        from mr_engine.agent.prompts import build_system_prompt

        # Runtime does NOT satisfy primary_sut_has_writer.
        prompt_hidden = build_system_prompt(
            BehaviorTarget.ROUND_TRIP_INVARIANCE, "VCF",
            primary_target="biopython",           # biopython: no writer
            available_suts=["biopython", "reference"],
            runtime_capabilities={"pysam_runtime_reachable"},  # no "primary_sut_has_writer"
        )
        # The transform name must NOT appear as a menu entry. It DOES
        # appear in the filtered-out note we render at the bottom — so
        # the test guards by requiring it's in the "hidden" list rather
        # than in the "Valid names" list.
        assert "Valid names" in prompt_hidden
        # Split out the two sections and assert the filter behaviour.
        valid_block = prompt_hidden.split("Valid names")[1].split("Note:")[0]
        assert "sut_write_roundtrip" not in valid_block
        # Sanity: the hidden-list footer names it.
        assert "sut_write_roundtrip" in prompt_hidden
        assert "hidden because the current runtime" in prompt_hidden

    def test_writer_transform_shown_when_primary_has_writer(self):
        # When runtime satisfies primary_sut_has_writer, the writer
        # transform MUST appear in the "Valid names" menu block.
        from mr_engine.behavior import BehaviorTarget
        from mr_engine.agent.prompts import build_system_prompt

        prompt_shown = build_system_prompt(
            BehaviorTarget.ROUND_TRIP_INVARIANCE, "VCF",
            primary_target="htsjdk",
            available_suts=["htsjdk", "pysam"],
            runtime_capabilities={
                "primary_sut_has_writer",
                "pysam_runtime_reachable",
                "htsjdk_runtime_reachable",
                "bcf_codec_available",
            },
        )
        valid_block = prompt_shown.split("Valid names")[1].split("Note:")[0]
        assert "sut_write_roundtrip" in valid_block

    def test_compute_runtime_capabilities_from_class_attrs(self):
        # Direct check of biotest._compute_runtime_capabilities —
        # confirms it reads the class-level supports_write_roundtrip
        # attr rather than instantiating runners (no subprocesses).
        from biotest import _compute_runtime_capabilities

        # htsjdk primary + pysam available → full capability set.
        caps = _compute_runtime_capabilities(
            primary_target="htsjdk",
            available_suts=["htsjdk", "pysam", "reference"],
        )
        assert "primary_sut_has_writer" in caps
        assert "pysam_runtime_reachable" in caps
        assert "htsjdk_runtime_reachable" in caps
        assert "bcf_codec_available" in caps

        # biopython primary (no writer) — primary_sut_has_writer absent.
        caps = _compute_runtime_capabilities(
            primary_target="biopython",
            available_suts=["biopython", "reference"],
        )
        assert "primary_sut_has_writer" not in caps
        # Also: no pysam in available list → no pysam tags.
        assert "pysam_runtime_reachable" not in caps
        assert "bcf_codec_available" not in caps

    def test_bcf_transforms_hidden_without_pysam(self):
        # vcf_bcf_round_trip and permute_bcf_header_dictionary are gated
        # on pysam_runtime_reachable + bcf_codec_available. In an env
        # without pysam, they MUST be filtered out.
        from mr_engine.behavior import BehaviorTarget
        from mr_engine.agent.prompts import build_system_prompt

        prompt = build_system_prompt(
            BehaviorTarget.ROUND_TRIP_INVARIANCE, "VCF",
            primary_target="htsjdk",
            available_suts=["htsjdk", "reference"],      # no pysam
            runtime_capabilities={
                "primary_sut_has_writer",
                "htsjdk_runtime_reachable",
            },
        )
        valid_block = prompt.split("Valid names")[1].split("Note:")[0]
        assert "vcf_bcf_round_trip" not in valid_block
        assert "permute_bcf_header_dictionary" not in valid_block
        # But sut_write_roundtrip is present (primary htsjdk has writer).
        assert "sut_write_roundtrip" in valid_block


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
