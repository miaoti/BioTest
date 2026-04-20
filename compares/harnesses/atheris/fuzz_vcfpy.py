"""Atheris harness for vcfpy VCF parsing (added 2026-04-20).

vcfpy is the pure-Python bihealth/vcfpy parser. Unlike pysam, its
entire VCF surface is implemented in Python, so coverage.py traces it
cleanly and Atheris can drive it in-process without libFuzzer hooking
into Cython.

Run (Linux / WSL2 / macOS):

    /opt/atheris-venv/bin/python compares/harnesses/atheris/fuzz_vcfpy.py \\
        -atheris_runs=0 \\
        -max_total_time=7200 \\
        -artifact_prefix=compares/results/atheris/vcfpy_vcf/ \\
        seeds/vcf/

vcfpy only parses VCF; the `--format=SAM` escape hatch is preserved
from the pysam harness but errors fast with a clear message.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import atheris

with atheris.instrument_imports():
    import vcfpy


FORMAT = "VCF"


def _with_temp_input(data: bytes, suffix: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=suffix, prefix="atheris-vcfpy-"
    )
    try:
        tmp.write(data)
        tmp.flush()
        return Path(tmp.name)
    finally:
        tmp.close()


def fuzz_vcf(data: bytes) -> None:
    if not data:
        return
    path = _with_temp_input(data, ".vcf")
    try:
        reader = vcfpy.Reader.from_path(str(path))
        try:
            _ = reader.header
            for rec in reader:
                # Exercise INFO / FORMAT / sample paths — mirrors the
                # pysam harness's lazy-field walk.
                _ = rec.CHROM, rec.POS, rec.ID, rec.REF, rec.ALT
                _ = rec.QUAL, rec.FILTER
                _ = dict(rec.INFO)
                for call in rec.calls:
                    _ = call.sample, dict(call.data)
        finally:
            reader.close()
    except (OSError, vcfpy.exceptions.VCFPyException) as expected:
        # vcfpy raises VCFPyException + subclasses on malformed input;
        # OSError for bgzf/path issues. Both expected on adversarial bytes.
        del expected
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def fuzz_sam(_data: bytes) -> None:
    raise RuntimeError(
        "vcfpy is VCF-only; run the biopython or pysam harness for SAM."
    )


def _dispatch(data: bytes) -> None:
    if FORMAT == "SAM":
        fuzz_sam(data)
    else:
        fuzz_vcf(data)


def main() -> None:
    global FORMAT
    argv = list(sys.argv)
    cleaned = []
    for tok in argv:
        if tok.startswith("--format="):
            FORMAT = tok.split("=", 1)[1].upper()
        else:
            cleaned.append(tok)
    atheris.Setup(cleaned, _dispatch)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
