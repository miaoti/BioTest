"""
Custom Hypothesis shrink hooks for minimizing VCF and SAM test cases.

When a failure is found, these functions reduce the input to the
smallest reproduction case possible.
"""

from __future__ import annotations


def shrink_vcf_lines(lines: list[str]) -> list[str]:
    """
    Minimize a VCF file for bug reproduction.

    Strategy:
    1. Keep ##fileformat as first line (required)
    2. Keep at most 2 ##meta lines (one INFO, one FORMAT)
    3. Keep #CHROM header line
    4. Keep only 1 data record
    5. Reduce to 1 sample if possible
    """
    fileformat = None
    meta_lines = []
    header_line = None
    data_lines = []

    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("##fileformat"):
            fileformat = stripped
        elif stripped.startswith("##"):
            meta_lines.append(stripped)
        elif stripped.startswith("#CHROM"):
            header_line = stripped
        elif stripped and not stripped.startswith("#"):
            data_lines.append(stripped)

    result = []
    if fileformat:
        result.append(fileformat)

    # Keep at most 2 essential meta lines
    essential = [m for m in meta_lines if "##INFO=" in m or "##FORMAT=" in m]
    result.extend(essential[:2])

    if header_line:
        result.append(header_line)

    # Keep only the first data record
    if data_lines:
        result.append(data_lines[0])

    return [l + "\n" for l in result]


def shrink_sam_lines(lines: list[str]) -> list[str]:
    """
    Minimize a SAM file for bug reproduction.

    Strategy:
    1. Keep @HD as first line
    2. Keep only 1 @SQ line
    3. Drop @RG, @PG, @CO
    4. Keep only 1 alignment record
    5. Strip optional tags down to at most 2
    """
    hd_line = None
    sq_lines = []
    alignment_lines = []

    for line in lines:
        stripped = line.rstrip("\n\r")
        if stripped.startswith("@HD"):
            hd_line = stripped
        elif stripped.startswith("@SQ"):
            sq_lines.append(stripped)
        elif not stripped.startswith("@") and "\t" in stripped:
            alignment_lines.append(stripped)

    result = []
    if hd_line:
        result.append(hd_line)
    if sq_lines:
        result.append(sq_lines[0])

    if alignment_lines:
        cols = alignment_lines[0].split("\t")
        # Keep only 2 optional tags
        if len(cols) > 13:
            cols = cols[:13]
        result.append("\t".join(cols))

    return [l + "\n" for l in result]
