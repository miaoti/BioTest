# Seed Corpus — Sources & Provenance

BioTest's seed corpus is split into two tiers. This file is the provenance manifest for every file we ship or fetch, so a reviewer can audit diversity coverage and license compliance end-to-end.

## Tier-1 — Hand-crafted (committed to git)

| File | Purpose | Diversity axes exercised |
| :--- | :--- | :--- |
| `seeds/vcf/minimal_single.vcf` | Smallest parseable single-sample VCF v4.3 | fileformat, minimal header, 1 sample |
| `seeds/vcf/minimal_multisample.vcf` | Two-sample VCF v4.3 | multi-sample, multi-ALT, Number=A fields |
| `seeds/vcf/spec_example.vcf` | Canonical example from VCF v4.3 spec | phased GT, rich INFO, multi-ALT |
| `seeds/sam/minimal_tags.sam` | Minimal SAM with optional tags | @HD, optional TAG:TYPE:VALUE |
| `seeds/sam/spec_example.sam` | SAM v1 spec example | multi-record, CIGAR ops |
| `seeds/sam/complex_cigar.sam` | SAM with hard/soft clipping | CIGAR H/S, padding |

## Tier-2 — Real-world public test suites (fetched on demand, gitignored)

Run `py -3.12 seeds/fetch_real_world.py` to populate. All sources are under permissive licenses (Apache 2.0 / MIT / BSD) and are official test data from the upstream format's reference implementations.

**Per-file size cap: 500 KB.** Files over the cap are skipped at download time so the corpus stays fast to iterate on.

### htsjdk test resources (Apache 2.0)
Source: `github.com/samtools/htsjdk/src/test/resources/htsjdk/variant/`

| File | Diversity axis |
| :--- | :--- |
| `real_world_htsjdk_ex2.vcf` | 3-sample multi-ALT; phased + unphased GT mix |
| `real_world_htsjdk_dbsnp_135.b37.1000.vcf` | 1000 dbSNP rows; rich INFO flags (CLN, G5, GENEINFO, GMAF, NSM/NSN/NSF) |
| `real_world_htsjdk_structuralvariants.vcf` | Structural variants: `<DEL>`, `<INS>`, `<INV>`, `<DUP>`, `<BND>` |
| `real_world_htsjdk_test_withNanQual.vcf` | NaN QUAL — edge case for float parsers |
| `real_world_htsjdk_test_withGLandPL.vcf` | Deep FORMAT: `GT:GQ:DP:AD:PL` + GL array |
| `real_world_htsjdk_breakpointExample.vcf` | BND breakpoint notation |
| `real_world_htsjdk_diploid.vcf` | Diploid gVCF (phased) |
| `real_world_htsjdk_reblocked.gvcf.vcf` | Reblocked gVCF with `<NON_REF>` |
| `real_world_htsjdk_clinvar.vcf` | ClinVar clinical-significance INFO |
| `real_world_htsjdk_example.sam` | Canonical SAM example |
| `real_world_htsjdk_unmapped_reads.sam` | Unmapped reads (edge case) |
| `real_world_htsjdk_coordinate_sorted.sam` | Coordinate-sorted SAM |

### bcftools test suite (MIT-equivalent)
Source: `github.com/samtools/bcftools/test/`

| File | Diversity axis |
| :--- | :--- |
| `real_world_bcftools_view.vcf` | Canonical view input |
| `real_world_bcftools_norm_merge.vcf` | Multi-allelic join corpus |
| `real_world_bcftools_norm_split.vcf` | Multi-allelic split corpus |
| `real_world_bcftools_norm_left_align.vcf` | Left-alignment test |
| `real_world_bcftools_norm_check_ref.vcf` | check-ref edge case |
| `real_world_bcftools_annotate.vcf` | Annotation field handling |
| `real_world_bcftools_csq.vcf` | CSQ (VEP) annotation test |
| `real_world_bcftools_csq_in.vcf` | Gene-model CSQ input |
| `real_world_bcftools_missing.vcf` | Missing-value handling |
| `real_world_bcftools_ad_bias.vcf` | Allelic-depth bias |
| `real_world_bcftools_af_dist.vcf` | AF distribution |
| `real_world_bcftools_concat_1/2/3.vcf` | Concat across chromosomes |
| `real_world_bcftools_plugin_fill_tags.vcf` | +fill-tags plugin input |
| `real_world_bcftools_plugin_setGT.vcf` | +setGT plugin input |
| `real_world_bcftools_query.vcf` | Query language input |
| `real_world_bcftools_check.vcf` | `bcftools check` input |
| `real_world_bcftools_filter.vcf` | FILTER column edge cases |
| `real_world_bcftools_isec_1/2.vcf` | Intersection inputs |
| `real_world_bcftools_merge_1/2.vcf` | Merge inputs |
| `real_world_bcftools_mpileup.vcf` | mpileup output |
| `real_world_bcftools_polysomy.vcf` | Aneuploid (polysomy) records |
| `real_world_samtools_ce.sam` | C. elegans SAM test |

### htslib SAM / BAM corpus (MIT-equivalent)
Source: `github.com/samtools/htslib/test/`. Phase 1 of the SAM-coverage plan triples the SAM Tier-2 corpus (7 → ~30+ files) by pulling every htslib-curated SAM edge case under the 500 KB cap. Each `#` in the upstream filename is URL-encoded as `%23` in the fetch URL; the committed filename strips it.

| File | Diversity axis |
| :--- | :--- |
| `real_world_htslib_ce_1/2/5/5b/supp.sam` | C. elegans alignment variety (ce series) |
| `real_world_htslib_ce_tag_padded/depadded.sam` | Padded vs depadded CIGAR with MD tag |
| `real_world_htslib_ce_unmap/unmap1/unmap2.sam` | Unmapped-read flag + pair variants |
| `real_world_htslib_c1_clip.sam` | Hard/soft clipping corner cases |
| `real_world_htslib_c1_bounds.sam` | CIGAR length-boundary conditions |
| `real_world_htslib_c1_noseq.sam` | SEQ='*' alignments (no sequence) |
| `real_world_htslib_c1_pad1/pad2/pad3.sam`, `c2_pad.sam` | CIGAR `P` (pad) op variants — triggers padding-specific branches |
| `real_world_htslib_c1_unknown.sam` | CIGAR `B` (back) op — rare/optional spec op |
| `real_world_htslib_auxf_values.sam` | Optional auxiliary tag type-B (array) values |
| `real_world_htslib_md_1.sam`, `embed_md.sam` | MD tag parsing + embedded-MD records |
| `real_world_htslib_xx_tlen.sam` | TLEN (template length) edge cases |
| `real_world_htslib_index2/index3/index3_exp/index_dos.sam` | Index-selection + CRLF line endings |
| `real_world_htslib_fieldarith.sam` | Field arithmetic on POS/MAPQ/TLEN |
| `real_world_htslib_realn01/01_exp/01_exp-a/01_exp-e.sam` | Realign test inputs + expected outputs, variant A/E |
| `real_world_htslib_realn02/02-r/02_exp/02_exp-a/02_exp-e.sam` | Realign 02 with reverse-strand variant |
| `real_world_htslib_realn03/03_exp.sam` | Tiny realign edge case (138 / 172 bytes) |
| `real_world_htslib_colons.bam` | BAM with colons in read names — binary |
| `real_world_htslib_no_hdr_sq.bam` | BAM without @SQ header — binary |
| `real_world_htslib_range.bam` | BAM for range-query tests — binary |

**BAM files note.** Downloaded into `seeds/sam/` (alongside text SAM) so a single glob discovers both once the corpus is extended in Phase 3 (SAM↔BAM↔CRAM round-trip). Until then they are inert baggage — no SUT is run against them. The `fetch_real_world.py` format validator accepts BGZF magic (`\x1f\x8b\x08\x04`) on BAM-named files.

### hts-specs test corpus (MIT-equivalent)
Source: `github.com/samtools/hts-specs/test/vcf/`

| File | Diversity axis |
| :--- | :--- |
| `real_world_hts_specs_v4.1_passed_all_fields.vcf` | VCF v4.1 compliance |
| `real_world_hts_specs_v4.2_passed_fileformat.vcf` | VCF v4.2 compliance |
| `real_world_hts_specs_v4.3_passed_fileformat.vcf` | VCF v4.3 compliance |
| `real_world_hts_specs_v4.5_passed_fileformat.vcf` | VCF v4.5 compliance |

### Broad Institute GATK test resources (Apache 2.0)
Source: `github.com/broadinstitute/gatk/src/test/resources/`

| File | Diversity axis |
| :--- | :--- |
| `real_world_gatk_feature_data_source_test.vcf` | Feature-source test |
| `real_world_gatk_feature_data_source_test_gvcf.vcf` | gVCF with `<NON_REF>` |
| `real_world_gatk_count_variants.vcf` | CountVariants input |
| `real_world_gatk_select_variants.vcf` | SelectVariants input |
| `real_world_gatk_funcotator_snpeff_sample.vcf` | SnpEff ANN annotation |

## Diversity-axis coverage matrix

Every axis below is covered by at least one seed across the corpus. Relevant transforms and literature are listed so a reviewer can trace an axis → seed → transform → MR claim.

| Axis | Seed examples | Related transforms | Literature |
| :--- | :--- | :--- | :--- |
| VCF spec version coverage (v4.1, v4.2, v4.3, v4.5) | `hts_specs_v4.{1,2,3,5}_*.vcf` | shuffle_meta_lines, permute_structured_kv_order | VCF v4.x spec |
| Structural variants (`<DEL>`, `<INV>`, `<BND>`) | `htsjdk_structuralvariants.vcf`, `htsjdk_breakpointExample.vcf` | choose_permutation + permute_ALT compound | VCF v4.5 §5.4 |
| gVCF with `<NON_REF>` | `gatk_feature_data_source_test_gvcf.vcf`, `htsjdk_reblocked.gvcf.vcf` | inject_equivalent_missing_values | GATK gVCF spec |
| CSQ annotations (VEP) | `bcftools_csq.vcf`, `bcftools_csq_in.vcf` | permute_csq_annotations | Ensembl VEP docs |
| ANN annotations (SnpEff) | `gatk_funcotator_snpeff_sample.vcf` | permute_csq_annotations (key="ANN") | Cingolani et al. 2012 |
| Phased genotypes | `spec_example.vcf`, `htsjdk_diploid.vcf` | permute_sample_columns | VCF v4.5 §1.6.2 |
| Deep FORMAT fields | `htsjdk_test_withGLandPL.vcf` | inject_equivalent_missing_values | VCF v4.5 §1.4.2 |
| NaN QUAL / missing values | `htsjdk_test_withNanQual.vcf`, `bcftools_missing.vcf` | inject_equivalent_missing_values | VCF v4.5 §1.6.2 |
| Multi-allelic records | `minimal_multisample.vcf`, `bcftools_norm_split.vcf`, `bcftools_norm_merge.vcf` | split_multi_allelic, alt_permutation compound | Danecek & McCarthy 2017 |
| Left-alignable indels | `bcftools_norm_left_align.vcf` | left_align_indel, trim_common_affixes | Tan et al. 2015 |
| BCF codec exercises | Any valid VCF | vcf_bcf_round_trip, permute_bcf_header_dictionary | VCF v4.5 §6 |
| Rich dbSNP INFO flags | `htsjdk_dbsnp_135.b37.1000.vcf`, `htsjdk_clinvar.vcf` | shuffle_info_field_kv | dbSNP submission guide |
| Aneuploid (polysomy) GT | `bcftools_polysomy.vcf` | permute_sample_columns | VCF v4.5 §1.6.2 |

## Literature references

1. **Tan A, Abecasis GR, Kang HM. (2015).** *Unified representation of genetic variants.* Bioinformatics 31(13):2202–2204. doi:10.1093/bioinformatics/btv112. — Canonical variant normalization algorithm (left alignment, common-affix trimming).
2. **Danecek P, McCarthy SA. (2017).** *BCFtools/csq: haplotype-aware variant consequences.* Bioinformatics 33(13):2037–2039. doi:10.1093/bioinformatics/btx100. — Multi-allelic split/join semantics and CSQ handling.
3. **Cingolani P, Platts A, Wang L, et al. (2012).** *A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff.* Fly 6(2):80–92. — SnpEff ANN format specification.
4. **GA4GH VCF v4.5 specification.** `github.com/samtools/hts-specs` §1.2 (meta lines), §1.6.2 (structured headers), §5.4 (structural variants), §6 (BCF), §6.2.1 (dictionaries).
5. **Ensembl VEP output format documentation.** `ensembl.org/info/docs/tools/vep/vep_formats.html` — CSQ field format and multi-record semantics.
6. **Giannoulatou E, et al. (2014).** *Metamorphic testing of next-generation sequencing software.* Bioinformatics 30(11):1583–1590. — General framework for bioinformatics MR testing.

## License notes

- **htsjdk** (Apache 2.0) — permissive, test data redistributable.
- **bcftools / samtools / hts-specs** — MIT / MIT-equivalent, redistributable.
- **GATK** (Apache 2.0) — permissive, test data redistributable.
- **BioTest** (MIT) — inherits compatible upstream licenses.

No seed file is generated by a proprietary pipeline or subject to a patient-data consent restriction. Every upstream source is a public open-source test suite intended for downstream redistribution.

## Regenerating this manifest

If seed sources change, update `seeds/fetch_real_world.py` first (the single source of truth for URLs + descriptions), then regenerate this table by hand or via a helper script. The diversity-axis matrix above should be kept current when a new axis is introduced.
