# HTSlib harness — Gold-Standard reference SUT

`samtools` and `bcftools` are the upstream reference CLIs maintained by
the same working group that owns the SAM/VCF specifications
([github.com/samtools](https://github.com/samtools)). In our consensus
oracle they serve as the **tie-breaker** when other SUTs disagree —
their output is the closest thing we have to ground truth without a
formal grammar checker.

Unlike the Python / Java / C++ harnesses, this directory contains *no*
bespoke wrapper code. `test_engine/runners/htslib_runner.py` calls the
standard CLIs directly, then pipes their output through our own
canonical normalizers. The rest of this document is just the install +
coordinate-system contract.

## Install

### Linux / macOS
```bash
# Debian / Ubuntu
sudo apt-get install -y samtools bcftools

# macOS (Homebrew)
brew install samtools bcftools
```

### Windows
samtools / bcftools are not natively supported on Windows. Use WSL2 or
a Docker image (e.g. `biocontainers/samtools:v1.20` and
`biocontainers/bcftools:v1.20`). The runner honours `bcftools_path` /
`samtools_path` constructor args so you can point at a Docker-wrapper
shell script if you prefer.

## Role vs the other SUTs

| SUT         | Language | Underlying lib | Role in consensus           |
| :---------- | :------- | :------------- | :-------------------------- |
| htsjdk      | Java     | (own)          | Regular voter               |
| pysam       | Python   | libhts (C)     | Regular voter               |
| biopython   | Python   | (own)          | Regular voter (SAM only)    |
| seqan3      | C++      | (own)          | Regular voter (SAM only)    |
| **htslib**  | CLI      | **libhts (C)** | **Tie-breaker (Gold Std.)** |
| reference   | Python   | our own        | Not a voter (framework)     |

Tie-breaker semantics: htslib's vote only activates when no parser
bucket has a strict majority (`>N/2`). A majority without htslib still
wins outright. See `test_engine/oracles/consensus.py` for the decision
rules.

> **Note on pysam vs htslib**: pysam shares the same underlying C
> library as samtools/bcftools, but bugs do occur independently — in
> the Cython bindings, in Python object construction, or in how pysam
> exposes fields that the CLI formats textually. Their agreement is
> therefore a *stronger* signal than either alone, but their
> disagreement still happens and is informative.

## Canonical-form contract

Both CLIs are invoked with flags that produce a full round-trip text:

- VCF: `bcftools view <file>` — prints header + records.
- SAM: `samtools view -h <file>` — prints header + records.

The stdout text is then fed through `normalize_vcf_text` /
`normalize_sam_text` — the same normalizers used by `ReferenceRunner`.
This means HTSlib's vote reflects **what it thinks the file *is*** after
parsing and re-emitting, not the on-disk bytes.

### Coordinate-system alignment

- **VCF**: 1-based, inclusive. Both `bcftools view` output and our
  canonical schema use 1-based coordinates — no conversion needed.
- **SAM**: 1-based, inclusive. Same story — `samtools view -h` emits
  SAM text with 1-based POS exactly as it appears on disk. Only the
  binary BAM parsing path (which we don't use here) stores POS
  0-based; text SAM is 1-based on both sides.

## Invalid-input guard

If the CLI exits non-zero AND stderr contains any of
`invalid`, `malformed`, `parse error`, `truncated`, `could not parse`,
the runner tags the result with `error_type="parse_error"`. The
consensus oracle then sets `htslib_rejected_as_invalid=True`, which
the quarantine manager uses as strong evidence that the MR generated a
semantically invalid file and should be demoted — see
`test_engine/feedback/quarantine_manager.py`.
