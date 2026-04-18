#!/usr/bin/env python3
"""
pysam canonical JSON harness — runs inside Docker container.

Usage:
    python pysam_harness.py VCF /data/input.vcf
    python pysam_harness.py SAM /data/input.sam
    python pysam_harness.py --coverage /cov/dir VCF /data/input.vcf

Outputs canonical JSON to stdout. Errors go to stderr with exit code 1.

CRITICAL: pysam uses 0-based coordinates for ALL formats (including VCF).
This harness adds +1 to POS for both VCF and SAM, and +1 to PNEXT for SAM.

CRITICAL: When --coverage is used, coverage.py MUST start before any pysam
import so it can instrument the module. The coverage setup is done at the
very top of main() before the lazy pysam import in parse_vcf/parse_sam.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def parse_vcf(path: Path) -> dict[str, Any]:
    """Parse VCF via pysam into canonical dict."""
    import pysam

    vcf = pysam.VariantFile(str(path))
    header = vcf.header

    # Header
    meta: dict[str, Any] = {}
    for rec in header.records:
        if rec.type == "GENERIC":
            continue
        key = rec.key
        if hasattr(rec, "items") and callable(rec.items):
            fields = dict(rec.items())
            entry_id = fields.get("ID", "")
            if key not in meta:
                meta[key] = {}
            if isinstance(meta[key], dict):
                meta[key][entry_id] = fields

    samples = list(header.samples)

    # Records
    records = []
    for rec in vcf:
        # CRITICAL: pysam rec.pos is 0-based! Add +1 for 1-based canonical.
        pos = rec.pos + 1

        rec_id = None if rec.id is None else rec.id
        alt = list(rec.alts) if rec.alts else []
        qual = None if rec.qual is None else float(rec.qual)

        # FILTER
        filt = sorted(list(rec.filter.keys())) if rec.filter else []

        # INFO
        info: dict[str, Any] = {}
        for key in rec.info:
            val = rec.info[key]
            if isinstance(val, tuple):
                val = list(val)
            info[key] = val
        info = dict(sorted(info.items()))

        # Samples
        sample_data: dict[str, dict] = {}
        for sample_name in samples:
            sample = rec.samples[sample_name]
            fields: dict[str, Any] = {}
            for key in sample.keys():
                val = sample[key]
                if isinstance(val, tuple):
                    val = list(val)
                fields[key] = val
            sample_data[sample_name] = fields

        fmt = list(rec.format.keys()) if rec.format else None

        records.append({
            "CHROM": rec.chrom,
            "POS": pos,
            "ID": rec_id,
            "REF": rec.ref,
            "ALT": alt,
            "QUAL": qual,
            "FILTER": filt,
            "INFO": info,
            "FORMAT": fmt,
            "samples": sample_data if sample_data else None,
        })

    vcf.close()

    return {
        "format": "VCF",
        "header": {
            "fileformat": str(header.version) if hasattr(header, "version") else "",
            "meta": meta,
            "samples": samples,
        },
        "records": records,
    }


def parse_sam(path: Path) -> dict[str, Any]:
    """Parse SAM via pysam into canonical dict."""
    import pysam

    sam = pysam.AlignmentFile(str(path), "r")
    header = sam.header

    # Header
    hd = dict(header.get("HD", {})) if "HD" in header else None
    sq = [dict(s) for s in header.get("SQ", [])]
    rg = [dict(r) for r in header.get("RG", [])]
    pg = [dict(p) for p in header.get("PG", [])]
    co = sorted(header.get("CO", []))

    # Records
    records = []
    for read in sam:
        # CRITICAL: pysam reference_start is 0-based! Add +1.
        pos = None if read.is_unmapped else read.reference_start + 1
        pnext = None
        if read.next_reference_start is not None and read.next_reference_start >= 0:
            pnext = read.next_reference_start + 1

        # CIGAR
        cigar = None
        if read.cigartuples:
            op_map = {0: "M", 1: "I", 2: "D", 3: "N", 4: "S", 5: "H", 6: "P", 7: "=", 8: "X"}
            cigar = [{"op": op_map.get(op, "?"), "len": length}
                     for op, length in read.cigartuples]

        # Tags
        tags = {}
        for tag_name, tag_val in read.get_tags(with_value_type=True):
            tag_type = tag_val[0] if isinstance(tag_val, tuple) else "Z"
            val = tag_val[1] if isinstance(tag_val, tuple) else tag_val
            tags[tag_name] = {"type": tag_type, "value": val}
        tags = dict(sorted(tags.items()))

        records.append({
            "QNAME": read.query_name,
            "FLAG": read.flag,
            "RNAME": None if read.reference_name is None else read.reference_name,
            "POS": pos,
            "MAPQ": read.mapping_quality,
            "CIGAR": cigar,
            "RNEXT": None if read.next_reference_name is None else read.next_reference_name,
            "PNEXT": pnext,
            "TLEN": read.template_length,
            "SEQ": None if read.query_sequence is None else read.query_sequence,
            "QUAL": None if read.query_qualities is None else "".join(
                chr(q + 33) for q in read.query_qualities
            ),
            "tags": tags,
        })

    sam.close()

    return {
        "format": "SAM",
        "header": {"HD": hd, "SQ": sq, "RG": rg, "PG": pg, "CO": co},
        "records": records,
    }


def _run_parse(fmt: str, input_path: Path) -> None:
    """Core parse-and-emit logic."""
    if fmt == "VCF":
        result = parse_vcf(input_path)
    elif fmt == "SAM":
        result = parse_sam(input_path)
    else:
        print(f"Unsupported format: {fmt}", file=sys.stderr)
        sys.exit(1)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# BCF round-trip modes (for the vcf_bcf_round_trip and
# permute_bcf_header_dictionary transforms in mr_engine/transforms/vcf.py)
# ---------------------------------------------------------------------------

def bcf_roundtrip(input_vcf: Path, output_vcf: Path) -> None:
    """Serialize input_vcf -> BCF -> read back -> emit VCF to output_vcf.

    Tests the BCF2 binary codec round-trip invariance per VCF v4.5 §6.
    The output VCF must be semantically identical to the input; any
    difference beyond float precision implies a codec bug in pysam/HTSlib.
    """
    import pysam
    import tempfile

    tmp_bcf = Path(tempfile.mkstemp(suffix=".bcf")[1])
    try:
        # Read VCF
        src = pysam.VariantFile(str(input_vcf))
        # Write as BCF, carrying the same header
        bcf_out = pysam.VariantFile(str(tmp_bcf), "wb", header=src.header)
        try:
            for rec in src:
                bcf_out.write(rec)
        finally:
            bcf_out.close()
            src.close()

        # Read BCF back, re-emit as VCF text
        bcf_in = pysam.VariantFile(str(tmp_bcf))
        vcf_out = pysam.VariantFile(str(output_vcf), "w", header=bcf_in.header)
        try:
            for rec in bcf_in:
                vcf_out.write(rec)
        finally:
            vcf_out.close()
            bcf_in.close()
    finally:
        try:
            tmp_bcf.unlink()
        except OSError:
            pass


def vcf_write_roundtrip(input_vcf: Path, output_vcf: Path) -> None:
    """Parse input_vcf with pysam, re-serialize via pysam's VCF writer.

    Chen et al. 2018 §3.2 canonical MR: parse(write(parse(x))) must
    deep-equal parse(x). Complements bcf_roundtrip by skipping the
    binary hop — this exercises pysam's VCF text-format writer directly
    (libhts's vcf_write_line / variantfile.pyx Cython bindings),
    distinct from the BCF2 codec path.
    """
    import pysam

    src = pysam.VariantFile(str(input_vcf))
    out = pysam.VariantFile(str(output_vcf), "w", header=src.header)
    try:
        for rec in src:
            out.write(rec)
    finally:
        out.close()
        src.close()


def sam_write_roundtrip(input_sam: Path, output_sam: Path) -> None:
    """Parse input_sam with pysam, re-serialize via AlignmentFile writer.

    SAM analogue of vcf_write_roundtrip. Mode "wh" = write with header
    to text SAM output. Exercises pysam's SAM text writer bindings
    (libhts's sam_format1 + samfile.pyx Cython bindings), distinct
    from the BAM binary codec and distinct from VCF.
    """
    import pysam

    # "r" = read text SAM. pysam auto-detects BAM by file magic bytes,
    # so `check_sq=False` keeps it permissive for minimal test inputs.
    src = pysam.AlignmentFile(str(input_sam), "r", check_sq=False)
    # "wh" = write with @-prefixed header lines included (text SAM).
    out = pysam.AlignmentFile(str(output_sam), "wh", template=src)
    try:
        for rec in src:
            out.write(rec)
    finally:
        out.close()
        src.close()


def bcf_header_reorder(
    input_vcf: Path, output_vcf: Path, seed: int = 0
) -> None:
    """Shuffle the BCF header dictionary order, then round-trip back to VCF.

    The reorder is performed on the *text* header before the BCF write so
    pysam's codec re-assigns dictionary indices. The body is re-serialized
    via pysam so indices in the binary match the reordered header. The
    final VCF must still be semantically identical to the input — if a
    downstream consumer treats the new dictionary index as authoritative
    without consulting the header, a difference surfaces.
    """
    import pysam
    import random
    import re
    import tempfile

    rng = random.Random(seed)

    # Extract header lines from the input VCF, shuffle contigs / INFO /
    # FORMAT / FILTER entries, keep ##fileformat first and the #CHROM line
    # last.
    raw = input_vcf.read_text(encoding="utf-8").splitlines(keepends=True)
    fileformat_line = None
    chrom_line = None
    other_meta: list[str] = []
    body: list[str] = []
    in_header = True
    for line in raw:
        if not in_header:
            body.append(line)
            continue
        if line.startswith("##fileformat"):
            fileformat_line = line
        elif line.startswith("#CHROM"):
            chrom_line = line
            in_header = False
        elif line.startswith("##"):
            other_meta.append(line)
        else:
            # no #CHROM line yet but past ## — shouldn't happen in valid VCF
            body.append(line)
            in_header = False

    # Bucket and shuffle per dictionary class, then recombine
    bucket = {"contig": [], "INFO": [], "FORMAT": [], "FILTER": [], "other": []}
    for line in other_meta:
        m = re.match(r"##(contig|INFO|FORMAT|FILTER)=", line)
        if m:
            bucket[m.group(1)].append(line)
        else:
            bucket["other"].append(line)
    for key in ("contig", "INFO", "FORMAT", "FILTER"):
        rng.shuffle(bucket[key])

    reordered_header = []
    if fileformat_line:
        reordered_header.append(fileformat_line)
    # Interleave: contigs first, then INFO, FORMAT, FILTER, other
    for key in ("contig", "INFO", "FORMAT", "FILTER", "other"):
        reordered_header.extend(bucket[key])
    if chrom_line:
        reordered_header.append(chrom_line)

    tmp_vcf = Path(tempfile.mkstemp(suffix=".vcf")[1])
    tmp_bcf = Path(tempfile.mkstemp(suffix=".bcf")[1])
    try:
        tmp_vcf.write_text("".join(reordered_header + body), encoding="utf-8")
        # Write reordered VCF -> BCF (codec re-indexes dictionaries)
        src = pysam.VariantFile(str(tmp_vcf))
        bcf_out = pysam.VariantFile(str(tmp_bcf), "wb", header=src.header)
        try:
            for rec in src:
                bcf_out.write(rec)
        finally:
            bcf_out.close()
            src.close()
        # Read BCF back -> final VCF
        bcf_in = pysam.VariantFile(str(tmp_bcf))
        vcf_out = pysam.VariantFile(str(output_vcf), "w", header=bcf_in.header)
        try:
            for rec in bcf_in:
                vcf_out.write(rec)
        finally:
            vcf_out.close()
            bcf_in.close()
    finally:
        for p in (tmp_vcf, tmp_bcf):
            try:
                p.unlink()
            except OSError:
                pass


def main():
    # Argument grammar supported:
    #   [--coverage /cov/dir] VCF|SAM <input_file>
    #       -> parse to canonical JSON on stdout (existing path)
    #   --mode bcf_roundtrip <input_vcf> <output_vcf>
    #       -> VCF -> BCF -> VCF, emits round-tripped VCF to output_vcf
    #   --mode bcf_header_reorder [--seed N] <input_vcf> <output_vcf>
    #       -> shuffle BCF dictionary order then round-trip
    args = sys.argv[1:]
    coverage_dir = None

    if args and args[0] == "--coverage":
        if len(args) < 2:
            print("--coverage requires a directory argument", file=sys.stderr)
            sys.exit(1)
        coverage_dir = Path(args[1])
        args = args[2:]

    # BCF subcommands bypass the canonical-JSON path entirely. They write
    # a VCF file to disk; the caller reads that file back to compare with
    # the original via its normal oracle pipeline.
    if args and args[0] == "--mode":
        if len(args) < 2:
            print("--mode requires a mode name", file=sys.stderr)
            sys.exit(1)
        mode = args[1]
        rest = args[2:]
        try:
            if mode == "bcf_roundtrip":
                if len(rest) != 2:
                    print(
                        "bcf_roundtrip usage: --mode bcf_roundtrip "
                        "<input_vcf> <output_vcf>",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                bcf_roundtrip(Path(rest[0]), Path(rest[1]))
            elif mode == "vcf_write_roundtrip":
                if len(rest) != 2:
                    print(
                        "vcf_write_roundtrip usage: --mode vcf_write_roundtrip "
                        "<input_vcf> <output_vcf>",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                vcf_write_roundtrip(Path(rest[0]), Path(rest[1]))
            elif mode == "sam_write_roundtrip":
                if len(rest) != 2:
                    print(
                        "sam_write_roundtrip usage: --mode sam_write_roundtrip "
                        "<input_sam> <output_sam>",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                sam_write_roundtrip(Path(rest[0]), Path(rest[1]))
            elif mode == "bcf_header_reorder":
                seed = 0
                if rest and rest[0] == "--seed":
                    if len(rest) < 2:
                        print("--seed requires an integer", file=sys.stderr)
                        sys.exit(1)
                    try:
                        seed = int(rest[1])
                    except ValueError:
                        print(f"--seed expected int, got {rest[1]!r}", file=sys.stderr)
                        sys.exit(1)
                    rest = rest[2:]
                if len(rest) != 2:
                    print(
                        "bcf_header_reorder usage: --mode bcf_header_reorder "
                        "[--seed N] <input_vcf> <output_vcf>",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                bcf_header_reorder(Path(rest[0]), Path(rest[1]), seed=seed)
            else:
                print(f"Unknown --mode: {mode}", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"BCF mode error ({mode}): {e}", file=sys.stderr)
            sys.exit(1)
        return

    if len(args) != 2:
        print(
            f"Usage: {sys.argv[0]} [--coverage /cov/dir] <VCF|SAM> <input_file>\n"
            f"   OR  {sys.argv[0]} --mode bcf_roundtrip <input_vcf> <output_vcf>\n"
            f"   OR  {sys.argv[0]} --mode vcf_write_roundtrip <input_vcf> <output_vcf>\n"
            f"   OR  {sys.argv[0]} --mode sam_write_roundtrip <input_sam> <output_sam>\n"
            f"   OR  {sys.argv[0]} --mode bcf_header_reorder [--seed N] "
            f"<input_vcf> <output_vcf>",
            file=sys.stderr,
        )
        sys.exit(1)

    fmt = args[0].upper()
    input_path = Path(args[1])

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Coverage must start BEFORE pysam is imported (parse_vcf/parse_sam
    # import pysam at function call time). We instrument the pysam
    # site-packages directory so coverage.py traces into it.
    _cov_instance = None
    if coverage_dir:
        try:
            import coverage as _cov
            import os

            # Point source= at the pysam package dir so coverage.py
            # instruments site-packages (normally excluded).
            import importlib.util
            pysam_spec = importlib.util.find_spec("pysam")
            pysam_dir = str(Path(pysam_spec.origin).parent) if pysam_spec and pysam_spec.origin else None

            cov_file = str(coverage_dir / f".coverage.{os.getpid()}")
            _cov_instance = _cov.Coverage(
                data_file=cov_file,
                source=[pysam_dir] if pysam_dir else None,
            )
            _cov_instance.start()
        except Exception as e:
            # Coverage was explicitly requested; failing silently would
            # produce a harness result with no .coverage.* file and the
            # host-side collector would record zero coverage, poisoning
            # Phase D's SCC signal. Fail loudly instead.
            print(f"Coverage setup FAILED (requested via --coverage): {e}", file=sys.stderr)
            try:
                (coverage_dir / f"coverage_setup_failed.{os.getpid()}.log").write_text(
                    f"{type(e).__name__}: {e}\n", encoding="utf-8"
                )
            except Exception:
                pass
            sys.exit(2)

    try:
        _run_parse(fmt, input_path)
    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if _cov_instance:
            _cov_instance.stop()
            _cov_instance.save()
            # Write a coverage summary JSON for the host-side collector.
            # This includes total lines per file (which the host can't compute
            # because the source files are inside the container).
            try:
                import os
                summary = {}
                data = _cov_instance.get_data()
                for filepath in data.measured_files():
                    executed = data.lines(filepath) or []
                    # Read source to count total lines
                    total_lines = 0
                    try:
                        with open(filepath, "r") as src:
                            total_lines = sum(1 for _ in src)
                    except OSError:
                        total_lines = len(executed)
                    fname = Path(filepath).name
                    summary[fname] = {
                        "executed": len(executed),
                        "total": total_lines,
                        "missing": sorted(set(range(1, total_lines + 1)) - set(executed)),
                    }
                summary_path = coverage_dir / f"summary.{os.getpid()}.json"
                import json as _json
                with open(summary_path, "w") as f:
                    _json.dump(summary, f, indent=2)
            except Exception:
                pass  # Best-effort


if __name__ == "__main__":
    main()
