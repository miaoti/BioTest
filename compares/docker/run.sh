#!/usr/bin/env bash
# Launch an interactive shell inside the BioTest benchmark image with
# the repo mounted at /work and the user's seeds / results surviving
# across container restarts.
#
# Usage:
#   bash compares/docker/run.sh              # interactive bash
#   bash compares/docker/run.sh -- verify.sh # run a named command

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

IMAGE_TAG="${IMAGE_TAG:-biotest-bench:latest}"

# Docker-on-Windows needs POSIX-style mount paths. MSYS / Git Bash prepend
# an extra slash which breaks the mount; the trailing // variant is the
# idiomatic workaround.
MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="/${REPO_ROOT//\\//}"
fi

EXTRA_ARGS=("$@")

# Use -it only when stdin is actually a TTY; piped / scripted runs
# would otherwise hit "the input device is not a TTY".
TTY_FLAGS=("-i")
if [[ -t 0 && -t 1 ]]; then
    TTY_FLAGS+=("-t")
fi

# Prevent MSYS/Git-Bash from rewriting absolute paths ("/work" becomes
# "C:/Program Files/Git/work" otherwise).
export MSYS_NO_PATHCONV=1

docker run --rm "${TTY_FLAGS[@]}" \
    -v "${MOUNT_SRC}:/work" \
    -w /work \
    -e PYTHONPATH=/work \
    "${IMAGE_TAG}" \
    "${EXTRA_ARGS[@]:-bash}"
