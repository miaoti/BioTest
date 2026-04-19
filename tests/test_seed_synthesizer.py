"""
Tests for mr_engine/agent/seed_synthesizer.py (Rank 1 coverage lever).

Uses a fake LLM stand-in (duck-typed `.invoke()` → object with `.content`) so
tests never touch the real network / LLM provider. The validation pipeline
runs against the real framework normalizers — any future breakage of
`normalize_vcf_text` / `normalize_sam_text` assumptions will surface here.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from mr_engine.agent.seed_synthesizer import (
    synthesize_seeds,
    _extract_fenced_blocks,
    _validate_candidate,
    _atomic_write,
)
from mr_engine.agent.seed_synth_prompts import (
    build_vcf_prompt,
    build_sam_prompt,
    build_prompt,
)


# ---------------------------------------------------------------------------
# Minimal valid seed bodies used across several tests. Kept tiny but
# structurally correct so the normalizer accepts them.
# ---------------------------------------------------------------------------

VALID_VCF_BODY = (
    "##fileformat=VCFv4.3\n"
    "##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\">\n"
    "##contig=<ID=chr1,length=248956422>\n"
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
    "chr1\t100\t.\tA\tT\t30\tPASS\tDP=15\n"
)

VALID_VCF_BODY_2 = (
    "##fileformat=VCFv4.3\n"
    "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele count\">\n"
    "##contig=<ID=chr2,length=242193529>\n"
    "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
    "chr2\t200\t.\tG\tC\t40\tPASS\tAC=1\n"
)

VALID_SAM_BODY = (
    "@HD\tVN:1.6\tSO:unsorted\n"
    "@SQ\tSN:chr1\tLN:248956422\n"
    "r1\t0\tchr1\t100\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n"
)


class FakeLLMResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    """Minimal stand-in matching langchain BaseChatModel.invoke() contract."""
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


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------


class TestPromptTemplates:
    def test_vcf_prompt_embeds_blindspot_context(self):
        ctx = "UNCOVERED CODE: line 123 of VCFCodec.java"
        prompt = build_vcf_prompt(ctx, n=3, max_bytes=1024)
        assert ctx in prompt
        assert "VCFv4.3" in prompt
        assert "```vcf" in prompt or "vcf\\n" in prompt  # fence hint present
        # The {n} placeholder must have been substituted
        assert "exactly 3" in prompt
        assert "1,024 bytes" in prompt or "1024 bytes" in prompt

    def test_sam_prompt_embeds_blindspot_context(self):
        ctx = "UNCOVERED CODE: SAMTextReader line 45"
        prompt = build_sam_prompt(ctx, n=2, max_bytes=2048)
        assert ctx in prompt
        assert "@HD" in prompt
        assert "exactly 2" in prompt

    def test_dispatch_rejects_unknown_format(self):
        with pytest.raises(ValueError):
            build_prompt("ctx", fmt="BCF")

    def test_blindspot_context_with_braces_is_safe(self):
        """Regression: a blindspot_context containing `{` (Java/C++ source
        slices) must NOT crash the prompt builder via str.format()
        mis-parsing. Observed in Phase D iter 2 of the 2026-04-17 run:
        `Synth failed (non-fatal): unexpected '{' in field name`."""
        ctx_with_braces = (
            "UNCOVERED CODE in htsjdk:\n"
            "VCFCodec.java:43-57\n"
            "    43 |     public boolean canDecodeURI(final IOPath ioPath) {\n"
            "    44 |         ValidationUtils.nonNull(ioPath, \"ioPath\");\n"
            "    45 |         return extensionMap.stream().anyMatch(ext ->\n"
            "    46 |             ioPath.hasExtension(ext));\n"
            "    47 |     }\n"
        )
        # Must not raise.
        vp = build_vcf_prompt(ctx_with_braces, n=3, max_bytes=1024)
        sp = build_sam_prompt(ctx_with_braces, n=3, max_bytes=1024)
        # Both prompts must still carry the verbatim braces through.
        assert "canDecodeURI(final IOPath ioPath) {" in vp
        assert "canDecodeURI(final IOPath ioPath) {" in sp
        # And the output-contract substitutions still happened.
        assert "exactly 3" in vp
        assert "1,024 bytes" in vp


# ---------------------------------------------------------------------------
# Response parser
# ---------------------------------------------------------------------------


class TestFencedBlockExtraction:
    def test_single_block(self):
        text = f"```vcf\n{VALID_VCF_BODY}```\n"
        blocks = _extract_fenced_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].startswith("##fileformat=VCFv4.3")

    def test_multiple_blocks(self):
        text = (
            f"```vcf\n{VALID_VCF_BODY}```\n\n"
            f"```vcf\n{VALID_VCF_BODY_2}```\n"
        )
        blocks = _extract_fenced_blocks(text)
        assert len(blocks) == 2

    def test_blocks_with_different_language_tags(self):
        # Language tag is ignored; any fenced block counts.
        text = f"```\n{VALID_VCF_BODY}```\n"
        blocks = _extract_fenced_blocks(text)
        assert len(blocks) == 1

    def test_empty_block_dropped(self):
        text = "```vcf\n\n```\n"
        blocks = _extract_fenced_blocks(text)
        assert blocks == []

    def test_no_blocks(self):
        assert _extract_fenced_blocks("just prose, no fences") == []


# ---------------------------------------------------------------------------
# Validation gates
# ---------------------------------------------------------------------------


class TestValidation:
    def test_accept_valid_vcf(self):
        result = _validate_candidate(VALID_VCF_BODY, "VCF", 100_000)
        assert result is not None
        assert result.endswith("\n")

    def test_accept_valid_sam(self):
        result = _validate_candidate(VALID_SAM_BODY, "SAM", 100_000)
        assert result is not None

    def test_reject_vcf_missing_fileformat(self):
        broken = VALID_VCF_BODY.replace("##fileformat=VCFv4.3\n", "")
        assert _validate_candidate(broken, "VCF", 100_000) is None

    def test_reject_sam_missing_header(self):
        broken = "\n".join(VALID_SAM_BODY.splitlines()[2:])  # drop @HD + @SQ
        assert _validate_candidate(broken, "SAM", 100_000) is None

    def test_reject_oversized(self):
        huge = VALID_VCF_BODY + ("chr1\t200\t.\tA\tC\t.\tPASS\tDP=1\n" * 20_000)
        # ~600 KB
        assert _validate_candidate(huge, "VCF", 500 * 1024) is None

    def test_reject_unparsable(self):
        # Well-formatted header but data row with wrong column count.
        broken = (
            "##fileformat=VCFv4.3\n"
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
            "chr1\tnot-a-number\n"  # missing columns
        )
        # Whether this passes depends on normalizer strictness — the test
        # guards the contract: if normalize_vcf_text raises, the candidate
        # is rejected. If it doesn't raise, this test is informational.
        from test_engine.canonical.vcf_normalizer import normalize_vcf_text
        try:
            normalize_vcf_text(broken.splitlines(keepends=True))
            normalizer_raises = False
        except Exception:
            normalizer_raises = True

        result = _validate_candidate(broken, "VCF", 100_000)
        if normalizer_raises:
            assert result is None
        # else: normalizer is too permissive to reject this; informational.


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------


class TestAtomicWrite:
    def test_write_creates_final_file(self, tmp_path):
        target = tmp_path / "out.vcf"
        _atomic_write(target, VALID_VCF_BODY)
        assert target.exists()
        assert not (tmp_path / "out.vcf.tmp").exists()
        assert target.read_text(encoding="utf-8") == VALID_VCF_BODY

    def test_write_failure_leaves_no_final_file(self, tmp_path):
        target = tmp_path / "out.vcf"
        # Simulate rename crash: patch os.replace to raise.
        with patch("mr_engine.agent.seed_synthesizer.os.replace",
                   side_effect=OSError("simulated disk full")):
            with pytest.raises(OSError):
                _atomic_write(target, VALID_VCF_BODY)
        # .tmp may linger on a real crash — we only assert the FINAL file
        # was never visible mid-write, which is what matters for the
        # SeedCorpus glob.
        assert not target.exists()


# ---------------------------------------------------------------------------
# End-to-end with FakeLLM
# ---------------------------------------------------------------------------


class TestSynthesizeSeedsEndToEnd:
    def test_all_valid_candidates_written(self, tmp_path):
        llm_text = (
            f"```vcf\n{VALID_VCF_BODY}```\n\n"
            f"```vcf\n{VALID_VCF_BODY_2}```\n"
        )
        fake = FakeLLM(llm_text)
        result = synthesize_seeds(
            blindspot_context="uncovered code slice here",
            fmt="VCF",
            primary_target="test",
            n_seeds=2,
            out_dir=tmp_path,
            iteration=1,
            llm=fake,
        )
        assert len(result) == 2
        for p in result:
            assert p.exists()
            assert p.parent.name == "vcf"
            assert p.name.startswith("synthetic_iter1_")
            assert p.name.endswith(".vcf")

    def test_mix_of_valid_and_invalid_only_valid_land(self, tmp_path):
        # 3 blocks: 1 valid VCF, 1 missing fileformat, 1 empty
        llm_text = (
            f"```vcf\n{VALID_VCF_BODY}```\n\n"
            "```vcf\nnot a VCF at all\njust garbage\n```\n\n"
            f"```vcf\n{VALID_VCF_BODY_2}```\n"
        )
        result = synthesize_seeds(
            blindspot_context="ctx",
            fmt="VCF",
            n_seeds=3,
            out_dir=tmp_path,
            iteration=1,
            llm=FakeLLM(llm_text),
        )
        # Valid ones kept, invalid one dropped.
        assert len(result) == 2

    def test_hash_dedup_across_iterations(self, tmp_path):
        text1 = f"```vcf\n{VALID_VCF_BODY}```\n"
        text2 = f"```vcf\n{VALID_VCF_BODY}```\n"  # same body

        r1 = synthesize_seeds(
            "ctx", "VCF", n_seeds=1, out_dir=tmp_path, iteration=1,
            llm=FakeLLM(text1),
        )
        assert len(r1) == 1

        r2 = synthesize_seeds(
            "ctx", "VCF", n_seeds=1, out_dir=tmp_path, iteration=2,
            llm=FakeLLM(text2),
        )
        # Same content → same hash → skip, no second file written.
        assert len(r2) == 0
        # Only one synthetic VCF on disk.
        synth = list((tmp_path / "vcf").glob("synthetic_iter*_*.vcf"))
        assert len(synth) == 1

    def test_empty_blindspot_returns_empty(self, tmp_path):
        # Empty ticket → skip. Don't waste an LLM call.
        class NotCalledLLM:
            def invoke(self, messages):  # pragma: no cover
                raise AssertionError("LLM should not be invoked on empty ctx")
        result = synthesize_seeds(
            blindspot_context="",
            fmt="VCF",
            out_dir=tmp_path,
            llm=NotCalledLLM(),
        )
        assert result == []

    def test_llm_exception_is_non_fatal(self, tmp_path):
        result = synthesize_seeds(
            blindspot_context="ctx",
            fmt="VCF",
            out_dir=tmp_path,
            llm=RaisingLLM(),
        )
        assert result == []
        # No partial state on disk.
        assert not (tmp_path / "vcf").exists() or not list(
            (tmp_path / "vcf").glob("*.vcf")
        )

    def test_sam_format_dispatch(self, tmp_path):
        llm_text = f"```sam\n{VALID_SAM_BODY}```\n"
        result = synthesize_seeds(
            blindspot_context="ctx",
            fmt="SAM",
            out_dir=tmp_path,
            llm=FakeLLM(llm_text),
        )
        assert len(result) == 1
        assert result[0].parent.name == "sam"
        assert result[0].name.endswith(".sam")

    def test_unsupported_format_returns_empty(self, tmp_path):
        result = synthesize_seeds(
            blindspot_context="ctx",
            fmt="BCF",
            out_dir=tmp_path,
            llm=FakeLLM("anything"),
        )
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
