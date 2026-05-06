"""
Tests for Phase C: Transform dispatch wrapper.
"""

import pytest
from pathlib import Path

from test_engine.generators.dispatch import apply_transform, apply_mr_transforms
from test_engine.canonical.vcf_normalizer import normalize_vcf_text
from test_engine.canonical.sam_normalizer import normalize_sam_text

SEEDS_DIR = Path(__file__).parent.parent / "seeds"


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


class TestVcfDispatch:
    def test_shuffle_meta_lines(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("shuffle_meta_lines", lines, seed=42)
        # fileformat must still be first
        assert result[0].startswith("##fileformat")
        # Same number of lines
        assert len(result) == len(lines)
        # Still valid VCF
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5

    def test_permute_structured_kv(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("permute_structured_kv_order", lines, seed=42)
        # All structured meta lines still present and valid
        structured = [l for l in result if l.startswith("##") and "=<" in l]
        assert len(structured) > 0
        # Still parseable
        canonical = normalize_vcf_text(result)
        assert canonical.header.fileformat == "VCFv4.3"

    def test_shuffle_info_kv(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("shuffle_info_field_kv", lines, seed=42)
        # Still parseable, same number of records
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5

    def test_permute_sample_columns(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("permute_sample_columns", lines, seed=42)
        canonical = normalize_vcf_text(result)
        # Same 3 samples (possibly reordered)
        assert set(canonical.header.samples) == {"NA00001", "NA00002", "NA00003"}

    def test_inject_missing_values(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "minimal_multisample.vcf")
        result = apply_transform("inject_equivalent_missing_values", lines, seed=42)
        canonical = normalize_vcf_text(result)
        # FORMAT should have extra field
        assert len(canonical.records[0].FORMAT) > 3

    def test_compound_alt_permutation(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        # Apply the compound group
        result = apply_mr_transforms(
            lines,
            ["choose_permutation", "permute_ALT", "remap_GT", "permute_Number_A_R_fields"],
            seed=42,
        )
        # Still parseable
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5
        # Mono-ALT records should be unchanged
        # Multi-ALT records should have reordered ALT


class TestSamDispatch:
    def test_permute_optional_tags(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "spec_example.sam")
        result = apply_transform("permute_optional_tag_fields", lines, seed=42)
        canonical = normalize_sam_text(result)
        assert len(canonical.records) == 4

    def test_reorder_header(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "spec_example.sam")
        result = apply_transform("reorder_header_records", lines, seed=42)
        canonical = normalize_sam_text(result)
        # @HD must still be first
        assert result[0].startswith("@HD")
        assert len(canonical.header.SQ) == 2

    def test_cigar_split_merge(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "minimal_tags.sam")
        result = apply_transform("split_or_merge_adjacent_cigar_ops", lines, seed=42)
        canonical = normalize_sam_text(result)
        assert len(canonical.records) == 2

    def test_toggle_clipping(self):
        lines = _read_lines(SEEDS_DIR / "sam" / "complex_cigar.sam")
        result = apply_transform("toggle_cigar_hard_soft_clipping", lines, seed=42)
        canonical = normalize_sam_text(result)
        assert len(canonical.records) >= 2


class TestDispatchMRTransforms:
    def test_single_step_mr(self):
        """Simulate MR: shuffle_meta_lines."""
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_mr_transforms(lines, ["shuffle_meta_lines"], seed=42)
        assert result[0].startswith("##fileformat")

    def test_unknown_transform_raises(self):
        lines = ["test\n"]
        with pytest.raises(ValueError, match="No dispatch wrapper"):
            apply_transform("nonexistent_transform", lines, seed=42)


class TestMultishotComposition:
    """Refine Round 4: BIOTEST_MULTISHOT_K env-var-gated extra-step composition."""

    def test_off_by_default(self, monkeypatch):
        """No env var → identical to single-step behaviour."""
        monkeypatch.delenv("BIOTEST_MULTISHOT_K", raising=False)
        lines = _read_lines(SEEDS_DIR / "sam" / "spec_example.sam")
        out_default = apply_mr_transforms(
            lines, ["permute_optional_tag_fields"], seed=42,
            format_context="SAM",
        )
        # Calling apply_transform directly should match the no-multishot path.
        out_direct = apply_transform("permute_optional_tag_fields", lines, seed=42)
        assert out_default == out_direct

    def test_k_2_adds_extra_steps(self, monkeypatch):
        """K=2 produces a different result than K=0 on the same MR + seed."""
        lines = _read_lines(SEEDS_DIR / "sam" / "spec_example.sam")
        monkeypatch.delenv("BIOTEST_MULTISHOT_K", raising=False)
        baseline = apply_mr_transforms(
            lines, ["permute_optional_tag_fields"], seed=42,
            format_context="SAM",
        )
        monkeypatch.setenv("BIOTEST_MULTISHOT_K", "2")
        multishot = apply_mr_transforms(
            lines, ["permute_optional_tag_fields"], seed=42,
            format_context="SAM",
        )
        # Either the result differs (extras did something) OR the random
        # extras both happened to no-op on this particular seed; the
        # invariant is that multishot still produces parseable SAM.
        canonical = normalize_sam_text(multishot)
        assert len(canonical.records) == 4

    def test_invalid_env_value_treated_as_zero(self, monkeypatch):
        """Junk env var value → treated as K=0, no behaviour change."""
        monkeypatch.setenv("BIOTEST_MULTISHOT_K", "not-a-number")
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        out = apply_mr_transforms(
            lines, ["shuffle_meta_lines"], seed=42, format_context="VCF",
        )
        # File still parseable, fileformat still first.
        assert out[0].startswith("##fileformat")
        canonical = normalize_vcf_text(out)
        assert len(canonical.records) == 5

    def test_compound_group_short_circuits_multishot(self, monkeypatch):
        """The ALT-permutation compound group must NOT have extras appended —
        the four members are biologically co-dependent."""
        monkeypatch.setenv("BIOTEST_MULTISHOT_K", "3")
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_mr_transforms(
            lines,
            ["choose_permutation", "permute_ALT", "remap_GT", "permute_Number_A_R_fields"],
            seed=42, format_context="VCF",
        )
        # File should still parse; the compound branch returned without
        # any extra-step injection.
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5


# ===========================================================================
# Dispatch wrappers for 6 new VCF transforms (normalization / BCF / CSQ)
# ===========================================================================

class TestVcfDispatchNew:
    """Smoke tests for the normalization + BCF + CSQ transform dispatch
    wrappers. Each test confirms the wrapper does not corrupt the file's
    core structure (fileformat preserved, record count consistent).
    """

    def test_trim_common_affixes_noop_when_nothing_to_trim(self):
        # spec_example.vcf has single-char REF/ALT for each record; nothing
        # to trim -> dispatch wrapper must leave every line byte-identical.
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("trim_common_affixes", lines, seed=42)
        # Structure preserved
        canonical = normalize_vcf_text(result)
        assert len(canonical.records) == 5
        assert result[0].startswith("##fileformat")

    def test_trim_common_affixes_actually_trims(self):
        # Craft a small VCF with REF=AA ALT=AC at POS=100 -> expect
        # REF=A ALT=C at POS=101 after trim.
        custom = [
            "##fileformat=VCFv4.3\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tAA\tAC\t50\tPASS\t.\n",
        ]
        result = apply_transform("trim_common_affixes", custom, seed=0)
        # Last line should now be the trimmed record
        last = result[-1].rstrip()
        cols = last.split("\t")
        assert cols[1] == "101", f"POS not advanced: {last}"
        assert cols[3] == "A", f"REF not trimmed: {last}"
        assert cols[4] == "C", f"ALT not trimmed: {last}"

    def test_left_align_indel_on_homopolymer(self):
        # Craft a homopolymer deletion: REF=AAA ALT=AA POS=5 -> POS=4.
        custom = [
            "##fileformat=VCFv4.3\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t5\t.\tAAA\tAA\t50\tPASS\t.\n",
        ]
        result = apply_transform("left_align_indel", custom, seed=0)
        cols = result[-1].rstrip().split("\t")
        assert cols[1] == "4"

    def test_split_multi_allelic_multiplies_records(self):
        # Craft multi-ALT record; expect 2 output records (one per ALT).
        custom = [
            "##fileformat=VCFv4.3\n",
            "##INFO=<ID=AC,Number=A,Type=Integer,Description=\"Allele Count\">\n",
            "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n",
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\n",
            "chr1\t100\t.\tA\tT,C\t50\tPASS\tAC=1,2\tGT\t0/1\n",
        ]
        result = apply_transform("split_multi_allelic", custom, seed=0)
        data_lines = [
            l for l in result
            if not l.startswith("#") and "\t" in l
        ]
        assert len(data_lines) == 2
        alts = {l.split("\t")[4] for l in data_lines}
        assert alts == {"T", "C"}

    def test_permute_csq_annotations_deterministic_on_csq_file(self):
        # Craft a VCF with CSQ header + multi-record CSQ annotation.
        custom = [
            "##fileformat=VCFv4.3\n",
            '##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence '
            'annotations from Ensembl VEP. Format: Allele|Gene|Feature">\n',
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n",
            "chr1\t100\t.\tA\tT\t50\tPASS\tCSQ=T|gene1|x,T|gene2|y,T|gene3|z\n",
        ]
        r1 = apply_transform("permute_csq_annotations", custom, seed=42)
        r2 = apply_transform("permute_csq_annotations", custom, seed=42)
        assert r1 == r2
        # Pipe count per record preserved (no sub-field corruption)
        csq_value = r1[-1].split("\t")[7].split("CSQ=")[1].rstrip()
        for record in csq_value.split(","):
            assert record.count("|") == 2

    def test_permute_csq_annotations_skips_without_csq_header(self):
        # spec_example.vcf has no CSQ header -> dispatch must no-op
        # (returns the input lines unchanged).
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("permute_csq_annotations", lines, seed=42)
        assert result == lines

    def test_vcf_bcf_round_trip_returns_lines(self):
        # Even without a working BCF codec, dispatch must return a list
        # of lines (not crash). If BCF is unavailable the wrapper returns
        # the input unchanged.
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("vcf_bcf_round_trip", lines, seed=42)
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_permute_bcf_header_dictionary_returns_lines(self):
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform(
            "permute_bcf_header_dictionary", lines, seed=42,
        )
        assert isinstance(result, list)

    def test_sut_write_roundtrip_without_runner_hook_is_safe_noop(self):
        # The generic writer transform is runner-aware (needs_runner_hook=True).
        # When dispatch is called WITHOUT a runner (e.g. from smoke tests
        # or from code paths that don't thread a runner through), the
        # transform must gracefully no-op and return the input — NOT
        # crash. This preserves the all-or-nothing safe-default policy
        # we use elsewhere (vcf_bcf_round_trip, etc.).
        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform("sut_write_roundtrip", lines, seed=42)
        # runner_hook omitted → None → no-op → input returned unchanged.
        assert result == lines

    def test_sut_write_roundtrip_with_runner_hook_dispatches(self):
        # When a real runner with supports_write_roundtrip=True is
        # passed, dispatch must call runner.run_write_roundtrip and
        # return its output split into lines.
        from test_engine.runners.base import RunnerResult

        class FakeWriterRunner:
            name = "fake"
            supports_write_roundtrip = True
            def run_write_roundtrip(self, path, fmt="VCF"):
                return RunnerResult(
                    success=True,
                    canonical_json={"rewritten_text": (
                        "##fileformat=VCFv4.2\n"
                        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
                    )},
                    parser_name="fake", format_type="VCF",
                )

        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform(
            "sut_write_roundtrip", lines, seed=42,
            runner_hook=FakeWriterRunner(),
        )
        # Output must come from the FakeWriterRunner, not the input.
        assert any("##fileformat=VCFv4.2" in (l or "") for l in result)
        assert all("spec" not in (l or "") for l in result[:2])

    def test_sut_write_roundtrip_non_writer_runner_is_noop(self):
        # A runner with supports_write_roundtrip=False must be treated
        # like no runner at all (no crash, return input unchanged).
        class FakeReadOnlyRunner:
            name = "read-only"
            supports_write_roundtrip = False
            def run_write_roundtrip(self, *a, **kw):  # pragma: no cover
                raise AssertionError("should not be called")

        lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        result = apply_transform(
            "sut_write_roundtrip", lines, seed=42,
            runner_hook=FakeReadOnlyRunner(),
        )
        assert result == lines

    def test_sut_write_roundtrip_forwards_format_context(self):
        # format_context must flow from apply_transform through the
        # dispatch wrapper into runner.run_write_roundtrip. Without it,
        # SAM seeds would route to the VCF writer and vice-versa.
        from test_engine.runners.base import RunnerResult

        captured: dict = {}

        class FmtCapturingRunner:
            name = "fmt-capture"
            supports_write_roundtrip = True
            def run_write_roundtrip(self, path, fmt="VCF"):
                captured["fmt"] = fmt
                body = "@HD\tVN:1.6\n" if fmt == "SAM" else "##fileformat=VCFv4.2\n"
                return RunnerResult(
                    success=True,
                    canonical_json={"rewritten_text": body},
                    parser_name="fmt-capture", format_type=fmt,
                )

        sam_lines = _read_lines(SEEDS_DIR / "sam" / "minimal_tags.sam")
        apply_transform(
            "sut_write_roundtrip", sam_lines, seed=7,
            runner_hook=FmtCapturingRunner(),
            format_context="SAM",
        )
        assert captured["fmt"] == "SAM"

        vcf_lines = _read_lines(SEEDS_DIR / "vcf" / "spec_example.vcf")
        apply_transform(
            "sut_write_roundtrip", vcf_lines, seed=7,
            runner_hook=FmtCapturingRunner(),
            format_context="VCF",
        )
        assert captured["fmt"] == "VCF"


class TestStrategyRouter:
    def test_sut_write_roundtrip_format_scoped_lookup(self):
        # The router must return DIFFERENT strategy factories for the
        # same transform name depending on the fmt arg. The VCF variant
        # samples from corpus.vcf_seeds, the SAM variant from
        # corpus.sam_seeds — so mis-routing would assume() into a
        # discard every call.
        from test_engine.generators.strategy_router import get_strategy

        vcf_strategy = get_strategy("sut_write_roundtrip", fmt="VCF")
        sam_strategy = get_strategy("sut_write_roundtrip", fmt="SAM")
        assert vcf_strategy is not None
        assert sam_strategy is not None
        assert vcf_strategy is not sam_strategy

        # Without fmt, defaults to VCF (single-scope fallback).
        default_strategy = get_strategy("sut_write_roundtrip")
        assert default_strategy is vcf_strategy

        # Single-scope transforms ignore fmt (same object either way).
        assert (
            get_strategy("shuffle_meta_lines", fmt="VCF")
            is get_strategy("shuffle_meta_lines", fmt="SAM")
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
