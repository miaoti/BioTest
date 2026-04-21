#!/usr/bin/env bash
# Archive compares/results/bug_bench/ to off-machine storage per the
# Phase 4 final bullet (DESIGN.md §13.5). This script produces a
# tar.zst inside compares/results/backups/ so the operator can rsync /
# cp / gdrive-upload it to their chosen off-machine target.
#
# Deterministic archive layout:
#   bug_bench-<timestamp>.tar.zst   (data)
#   bug_bench-<timestamp>.sha256    (hash for integrity check)
#
# Usage:
#   bash compares/scripts/backup_bug_bench.sh
#   bash compares/scripts/backup_bug_bench.sh --out /path/to/dest
#
# Idempotent: new archive each run; nothing is deleted.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
BENCH_ROOT="${REPO_ROOT}/compares/results/bug_bench"
BACKUPS_DIR="${REPO_ROOT}/compares/results/backups"

OUT_DIR="${BACKUPS_DIR}"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --out) OUT_DIR="$2"; shift 2 ;;
        *) echo "[backup] unknown flag $1" >&2; exit 2 ;;
    esac
done

if [[ ! -d "${BENCH_ROOT}" ]]; then
    echo "[backup] ERROR: ${BENCH_ROOT} does not exist" >&2
    exit 1
fi

mkdir -p "${OUT_DIR}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE="${OUT_DIR}/bug_bench-${STAMP}.tar.zst"
HASH="${OUT_DIR}/bug_bench-${STAMP}.sha256"

echo "[backup] compressing ${BENCH_ROOT}"
if command -v zstd >/dev/null 2>&1; then
    tar -C "${REPO_ROOT}/compares/results" -cf - bug_bench \
        | zstd -19 -q -o "${ARCHIVE}"
else
    echo "[backup] zstd not available; falling back to gzip" >&2
    ARCHIVE="${OUT_DIR}/bug_bench-${STAMP}.tar.gz"
    HASH="${OUT_DIR}/bug_bench-${STAMP}.sha256"
    tar -C "${REPO_ROOT}/compares/results" -czf "${ARCHIVE}" bug_bench
fi

sha256sum "${ARCHIVE}" > "${HASH}"
SIZE="$(du -h "${ARCHIVE}" | cut -f1)"
echo "[backup] wrote ${ARCHIVE} (${SIZE})"
echo "[backup] hash file ${HASH}"
echo
echo "Move this archive off-machine (rsync / gdrive / s3). The hash"
echo "file next to it lets you verify integrity after transfer."
