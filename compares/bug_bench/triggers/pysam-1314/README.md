# pysam-1314 — VariantFile.write() contig-remap corruption

**Severity**: logic bug (silent wrong-chromosome writes).
**Format**: VCF.
**Anchor**: pre_fix = pysam 0.22.1, post_fix = pysam 0.23.0.
**Issue / PR**: https://github.com/pysam-developers/pysam/issues/1314

## What the bug does

When a caller creates a `pysam.VariantHeader` from scratch (no
`contigs` block), iterates records from an input VCF, and writes them
through a `VariantFile` constructed from the hand-built header, the
first contig encountered on the input is silently re-mapped to the
first contig the caller registered on the header — even though
`rec.chrom` reports the original, correct contig name right up until
the write. Downstream readers see the wrong contig on every record
originally from the affected input contig.

Example from the original report: records from
`Horvu_VADA_Un01G000200.1` silently become records from `mychr` when
serialised, because `mychr` was registered first on the new header.

## Trigger

Three ingredients:

1. A source VCF that declares its own contigs (anything will do).
2. A hand-built `VariantHeader` with `contigs.add("mychr", ...)`
   called before `contigs.add("Horvu_VADA_Un01G000200.1", ...)`.
3. A loop that fetches records from (1) and writes them through the
   new header.

## Files

- `original.vcf` — one-record VCF on contig `Horvu_VADA_Un01G000200.1`.
- `reproduce.py` — minimal Python script that reads + writes with a
  hand-built header and observes the chrom-remap on the output.
- `issue_source.txt` — excerpt from issue #1314 with the reporter's
  own reproducer.

## Detection criterion

- **Expected signal**: `differential_disagreement` against `htslib`
  (`bcftools view` on the output file reports a different CHROM than
  the input file). Trivially detectable by a diff of
  `bcftools view -o -  input.vcf` vs `bcftools view -o -  output.vcf`
  for the CHROM column.
