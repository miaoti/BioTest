"""
Tests for the `target_filters` matcher in coverage_collector.

Guards against the specific filter-mis-scoping bug observed on 2026-04-18:
the `::VCF,Variant` prefix whitelist was over-narrow — it correctly excluded
BCF2 + JEXL classes but also silently dropped legitimate VCF data-model
classes (Allele, Genotype, CommonInfo, …) because their names don't start
with "VCF" or "Variant". The new exclusion-prefix syntax (`-BCF2,-JEXL`)
lets us include everything that isn't explicitly disallowed.
"""

from __future__ import annotations

import pytest

from test_engine.feedback.coverage_collector import (
    parse_filter_rules,
    filter_file_matches,
)


class TestParseFilterRules:
    def test_package_only(self):
        rules = parse_filter_rules(["htsjdk/variant/vcf"])
        assert rules == [("htsjdk/variant/vcf", (), ())]

    def test_include_prefixes(self):
        rules = parse_filter_rules(["htsjdk/variant/variantcontext::VCF,Variant"])
        pkg, inc, exc = rules[0]
        assert pkg == "htsjdk/variant/variantcontext"
        assert inc == ("VCF", "Variant")
        assert exc == ()

    def test_exclude_prefixes(self):
        rules = parse_filter_rules(["htsjdk/variant/variantcontext::-JEXL,-Jexl"])
        pkg, inc, exc = rules[0]
        assert pkg == "htsjdk/variant/variantcontext"
        assert inc == ()
        assert exc == ("JEXL", "Jexl")

    def test_mixed_include_and_exclude(self):
        rules = parse_filter_rules(["pkg::VCF,-BCF2,Variant"])
        pkg, inc, exc = rules[0]
        assert pkg == "pkg"
        assert inc == ("VCF", "Variant")
        assert exc == ("BCF2",)

    def test_whitespace_tolerated(self):
        rules = parse_filter_rules(["pkg :: VCF , -BCF2"])
        pkg, inc, exc = rules[0]
        assert pkg == "pkg"
        assert inc == ("VCF",)
        assert exc == ("BCF2",)


class TestFilterFileMatches:
    def test_no_rules_matches_everything(self):
        assert filter_file_matches("Anything.java", (), ()) is True

    def test_include_only_matches_prefix(self):
        assert filter_file_matches("VCFCodec.java", ("VCF", "Variant"), ()) is True
        assert filter_file_matches("VariantContext.java", ("VCF", "Variant"), ()) is True
        assert filter_file_matches("BCF2Writer.java", ("VCF", "Variant"), ()) is False

    def test_exclude_only_drops_prefix(self):
        # With no include list, default is admit; excludes remove matches.
        assert filter_file_matches("Genotype.java", (), ("JEXL", "Jexl")) is True
        assert filter_file_matches("VariantContext.java", (), ("JEXL",)) is True
        assert filter_file_matches("JEXLMap.java", (), ("JEXL",)) is False
        assert filter_file_matches("JexlMissingValueTreatment.java", (), ("Jexl",)) is False

    def test_mixed_include_plus_exclude(self):
        # include VCF*/Variant*, also exclude anything starting with BCF2 even if it
        # happened to start with Variant (defensive — Variant name wins both rules).
        rules_inc = ("VCF", "Variant")
        rules_exc = ("BCF2",)
        assert filter_file_matches("VCFWriter.java", rules_inc, rules_exc) is True
        assert filter_file_matches("VariantContextWriter.java", rules_inc, rules_exc) is True
        assert filter_file_matches("BCF2Writer.java", rules_inc, rules_exc) is False
        # Exclude takes precedence over include if both match.
        assert filter_file_matches("VariantBCF2Foo.java", rules_inc, rules_exc) is True
        # ^ doesn't start with BCF2, so exclude doesn't fire — include wins. Correct.

    def test_regression_wrongly_excluded_vcf_data_model(self):
        """Under the old `::VCF,Variant` prefix, these were wrongly filtered out.
        The new `-JEXL,-Jexl` syntax keeps them in."""
        correct_excl = ("JEXL", "Jexl")
        for legit_vcf in [
            "Allele.java",
            "SimpleAllele.java",
            "Genotype.java",
            "GenotypeBuilder.java",
            "GenotypeLikelihoods.java",
            "GenotypesContext.java",
            "CommonInfo.java",
            "FastGenotype.java",
            "LazyGenotypesContext.java",
            "StructuralVariantType.java",
        ]:
            assert filter_file_matches(legit_vcf, (), correct_excl) is True, (
                f"{legit_vcf} is a VCF data-model class and must stay in scope"
            )

    def test_regression_still_excludes_jexl(self):
        correct_excl = ("JEXL", "Jexl")
        for jexl_class in [
            "JEXLMap.java",
            "JexlMissingValueTreatment.java",
            "GenotypeJEXLContext.java",  # Jexl appears mid-string, not at start → NOT excluded
        ]:
            matched = filter_file_matches(jexl_class, (), correct_excl)
            # JEXL/Jexl as a PREFIX → excluded. Mid-string Jexl stays in scope.
            # That's by design; we filter by name prefix only.
            expected = not (
                jexl_class.startswith("JEXL") or jexl_class.startswith("Jexl")
            )
            assert matched is expected

    def test_wildcard_contains_match(self):
        # `*Jexl*` catches JEXL residuals regardless of prefix.
        excludes = ("*JEXL*", "*Jexl*")
        for jexl_hidden in [
            "VariantJEXLContext.java",              # starts with Variant, has JEXL mid-name
            "GenotypeJEXLContext.java",
            "VariantContextUtils$JexlVCMatchExp.java",
            "JEXLMap.java",
            "JexlMissingValueTreatment.java",
        ]:
            assert filter_file_matches(jexl_hidden, (), excludes) is False, (
                f"{jexl_hidden} should be caught by substring wildcard"
            )
        # Non-JEXL classes unaffected
        for legit in ["VariantContext.java", "Genotype.java", "VCFCodec.java"]:
            assert filter_file_matches(legit, (), excludes) is True

    def test_wildcard_prefix_match(self):
        excludes = ("BCF2*",)
        assert filter_file_matches("BCF2Writer.java", (), excludes) is False
        assert filter_file_matches("BCF2Encoder.java", (), excludes) is False
        assert filter_file_matches("VariantContext.java", (), excludes) is True

    def test_wildcard_suffix_match(self):
        excludes = ("*Impl.java",)
        assert filter_file_matches("GenotypeImpl.java", (), excludes) is False
        assert filter_file_matches("VariantContext.java", (), excludes) is True

    def test_bare_prefix_still_works_backward_compat(self):
        # Previously shipping `VCF,Variant` (no wildcards) must still behave
        # as prefix match. Regression guard.
        includes = ("VCF", "Variant")
        assert filter_file_matches("VCFCodec.java", includes, ()) is True
        assert filter_file_matches("VariantContext.java", includes, ()) is True
        assert filter_file_matches("BCF2Writer.java", includes, ()) is False

    def test_writer_prefix_still_excludes_bcf2(self):
        """The `::VCF,Variant` filter for the writer subpackage must still
        keep BCF2Writer / BCF2Encoder / BCF2FieldWriter out of scope."""
        includes = ("VCF", "Variant")
        excludes = ()
        for bcf in [
            "BCF2Writer.java",
            "BCF2Encoder.java",
            "BCF2FieldWriter.java",
            "BCF2FieldWriterManager.java",
        ]:
            assert filter_file_matches(bcf, includes, excludes) is False
        for vcf in [
            "VCFWriter.java",
            "VariantContextWriter.java",
            "VariantContextWriterBuilder.java",
        ]:
            assert filter_file_matches(vcf, includes, excludes) is True


class TestPerSutFilterResolution:
    """Guards the `MultiCoverageCollector._resolve_sut_filter` shim that picks
    the right per-SUT filter list from the nested YAML shape (while staying
    backward-compatible with the legacy flat-list shape)."""

    def _make_collector(self, target_filters_yaml):
        # Minimal MultiCoverageCollector build without real collectors
        from test_engine.feedback.coverage_collector import MultiCoverageCollector
        return MultiCoverageCollector(cfg={"target_filters": target_filters_yaml})

    def test_nested_shape_picks_per_sut(self):
        c = self._make_collector({
            "VCF": {
                "htsjdk": ["htsjdk/variant/vcf"],
                "pysam": ["pysam"],
            },
            "SAM": {
                "htsjdk": ["htsjdk/samtools::SAM,Sam"],
                "biopython": ["Bio/Align/sam"],
            },
        })
        assert c._resolve_sut_filter("VCF", "htsjdk") == ["htsjdk/variant/vcf"]
        assert c._resolve_sut_filter("VCF", "pysam") == ["pysam"]
        assert c._resolve_sut_filter("SAM", "biopython") == ["Bio/Align/sam"]
        # SUT without an entry → None (no filter, collector decides default)
        assert c._resolve_sut_filter("VCF", "biopython") is None

    def test_legacy_flat_shape_applies_to_all_suts(self):
        c = self._make_collector({
            "VCF": ["htsjdk/variant/vcf", "pysam"],
        })
        # Same list returned for every SUT — legacy fan-out semantics.
        flat = ["htsjdk/variant/vcf", "pysam"]
        assert c._resolve_sut_filter("VCF", "htsjdk") == flat
        assert c._resolve_sut_filter("VCF", "pysam") == flat
        assert c._resolve_sut_filter("VCF", "anything") == flat

    def test_missing_format_returns_none(self):
        c = self._make_collector({"VCF": {"htsjdk": ["x"]}})
        assert c._resolve_sut_filter("SAM", "htsjdk") is None
        assert c._resolve_sut_filter("", "htsjdk") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
