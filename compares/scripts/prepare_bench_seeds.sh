#!/usr/bin/env bash
# Materialise a synthetic-free seed corpus for the comparison bench.
#
# Why: seeds/vcf/ currently mixes hand-curated Tier-1 + fetched Tier-2
# real-world files with LLM-synthesised Phase-D seeds (prefix
# `synthetic_iter*`). Including synthetics in the bench would bias the
# comparison toward BioTest because they were produced by its own
# feedback loop. Per compares/DESIGN.md §4.2 "Seed corpus", the bench
# uses Tier-1 + Tier-2 only.
#
# This script hardlinks the non-synthetic seeds into
# compares/results/bench_seeds/{vcf,sam}/ so every adapter can point
# --seed-corpus at a deterministic, gitignored location.
#
# Usage (from repo root, either on host or inside biotest-bench):
#     bash compares/scripts/prepare_bench_seeds.sh
#
# The target directory is recreated on every run so removed synthetics
# don't linger. Hardlinks (not copies) keep the operation fast and
# inode-cheap; fallback to copy if the source and target live on
# different filesystems.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SRC_VCF="${REPO_ROOT}/seeds/vcf"
SRC_SAM="${REPO_ROOT}/seeds/sam"
DST_ROOT="${REPO_ROOT}/compares/results/bench_seeds"
DST_VCF="${DST_ROOT}/vcf"
DST_SAM="${DST_ROOT}/sam"

rm -rf "${DST_ROOT}"
mkdir -p "${DST_VCF}" "${DST_SAM}"

copy_non_synthetic() {
    local src="$1"
    local dst="$2"
    local ext="$3"
    local n=0
    shopt -s nullglob
    for f in "${src}"/*."${ext}" "${src}"/*.bam; do
        local base
        base="$(basename "${f}")"
        case "${base}" in
            synthetic_iter*) continue ;;
        esac
        if ln "${f}" "${dst}/${base}" 2>/dev/null; then
            :
        else
            cp "${f}" "${dst}/${base}"
        fi
        n=$((n+1))
    done
    shopt -u nullglob
    echo "${n}"
}

vcf_count="$(copy_non_synthetic "${SRC_VCF}" "${DST_VCF}" vcf)"
sam_count="$(copy_non_synthetic "${SRC_SAM}" "${DST_SAM}" sam)"

echo "[bench-seeds] VCF: ${vcf_count} files  →  ${DST_VCF}"
echo "[bench-seeds] SAM: ${sam_count} files  →  ${DST_SAM}"

# Sanity-check the minimums from DESIGN.md §5.1.
if (( vcf_count < 15 )); then
    echo "[bench-seeds] WARNING: VCF seed count ${vcf_count} < 15 (DESIGN.md threshold)" >&2
fi
if (( sam_count < 6 )); then
    echo "[bench-seeds] WARNING: SAM seed count ${sam_count} < 6 (DESIGN.md threshold)" >&2
fi
