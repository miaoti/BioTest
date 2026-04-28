#!/usr/bin/env bash
# Run cargo-mutants on noodles-vcf inside biotest-bench:latest.
#
# Args:
#   $1 — corpus dir on the host (absolute path)
#   $2 — output dir on the host (absolute path, will be created)
#   $3 — optional budget seconds (default 3600)
#
# The container clones zaeleus/noodles at a pinned commit, creates a
# minimal consumer crate with a corpus-replay test, and runs
# `cargo mutants --package noodles-vcf`. The script writes a
# summary.json in the host output dir matching the schema the
# phase-3 aggregator expects.

set -euo pipefail

CORPUS_HOST="${1:?usage: $0 CORPUS OUT [BUDGET_S]}"
OUT_HOST="${2:?usage: $0 CORPUS OUT [BUDGET_S]}"
BUDGET_S="${3:-3600}"

# Convert Windows paths to Docker Desktop /c/... form (unchanged on Linux).
norm() {
    local p="$1"
    p="${p//\\//}"
    if [[ "${p:1:1}" == ":" ]]; then
        local drive="${p:0:1}"
        drive="${drive,,}"
        p="/${drive}${p:2}"
    fi
    printf '%s' "$p"
}

CORPUS_DOCKER="$(norm "$CORPUS_HOST")"
OUT_DOCKER="$(norm "$OUT_HOST")"

mkdir -p "$OUT_HOST"

# Pin noodles commit — one that published noodles-vcf 0.70 so the
# source tree matches the version the harness is built against.
NOODLES_COMMIT="${NOODLES_COMMIT:-noodles-vcf-0.70.0}"

SCRIPT_HOST="$(pwd)/compares/scripts/noodles_mutation_inside_docker.sh"
SCRIPT_DOCKER="$(norm "$SCRIPT_HOST")"

# MSYS_NO_PATHCONV=1 so MSYS/Git-Bash doesn't rewrite /corpus, /out, /work.
MSYS_NO_PATHCONV=1 docker run --rm \
    -v "${CORPUS_DOCKER}:/corpus:ro" \
    -v "${OUT_DOCKER}:/out" \
    -v "${SCRIPT_DOCKER}:/run.sh:ro" \
    -e PATH=/root/.cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    -e BUDGET_S="$BUDGET_S" \
    -e NOODLES_COMMIT="$NOODLES_COMMIT" \
    -e CORPUS_SAMPLE="${CORPUS_SAMPLE:-50}" \
    -w /work \
    biotest-bench:latest \
    bash /run.sh
echo "cargo-mutants host-side copy: $OUT_HOST"
