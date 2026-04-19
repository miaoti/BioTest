#!/usr/bin/env bash
# Build the unified BioTest benchmark image.
#
# Usage (from anywhere):
#   bash compares/docker/build.sh
#
# Resolves the repo root so `requirements.txt` and the Dockerfile resolve
# correctly regardless of where the script is invoked from.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

IMAGE_TAG="${IMAGE_TAG:-biotest-bench:latest}"

echo "[build] image     = ${IMAGE_TAG}"
echo "[build] context   = ${REPO_ROOT}"
echo "[build] dockerfile= ${SCRIPT_DIR}/Dockerfile.bench"

docker build \
    --tag "${IMAGE_TAG}" \
    --file "${SCRIPT_DIR}/Dockerfile.bench" \
    "${REPO_ROOT}"

echo "[build] image built; running verify.sh inside the container..."

# Mount the repo at /work and execute verify.sh. Mirror run.sh's TTY /
# MSYS-path handling so the same invocation works from Git-Bash / CI /
# plain Linux alike.
TTY_FLAGS=("-i")
if [[ -t 0 && -t 1 ]]; then
    TTY_FLAGS+=("-t")
fi
export MSYS_NO_PATHCONV=1
MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="$(cd "${REPO_ROOT}" && pwd -W)"
fi

docker run --rm "${TTY_FLAGS[@]}" \
    -v "${MOUNT_SRC}:/work" \
    -w /work \
    "${IMAGE_TAG}" \
    bash compares/docker/verify.sh
