#!/usr/bin/env bash
# Focused-PoV re-run for cells where the broad 33-seed corpus left no
# tool-found triggers. We restrict the corpus to just the canonical PoV
# (no Tier-1+2 seeds) so MR transforms concentrate on the bug-shape and
# the verification has fewer co-occurring spec violations to dodge.
#
# Targets: htsjdk-1364 + htsjdk-1372 — both had crashes in the broad-corpus
# re-run but none satisfied §5.3.1 in either direction. The earlier
# 1-PoV-corpus pilot run reported 10/15 satisfied for -1364, suggesting
# focused exploration dominates broad exploration for known-target bug
# verification.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

LOG_ROOT="${REPO_ROOT}/compares/results/bug_bench/biotest_focused_pov_2026_04_29"
mkdir -p "${LOG_ROOT}"

BUDGET_S=${BUDGET_S:-3600}
IMAGE_TAG="${IMAGE_TAG:-biotest-bench:latest}"

MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="/${REPO_ROOT//\\//}"
fi
export MSYS_NO_PATHCONV=1

DEEPSEEK_API_KEY="$(grep -E '^DEEPSEEK_API_KEY=' .env 2>/dev/null | cut -d= -f2-)"

# Use a synthetic seeds dir that contains only the per-bug PoV.
SEEDS_TMP="${REPO_ROOT}/compares/results/bug_bench/biotest_focused_pov_2026_04_29/_pov_seeds"

CELLS=(
    "htsjdk:htsjdk-1418"
    "htsjdk:htsjdk-1637"
    "vcfpy:vcfpy-171"
    "noodles:noodles-241"
    "noodles:noodles-259"
    "noodles:noodles-300"
    "noodles:noodles-339"
)

for entry in "${CELLS[@]}"; do
    sut="${entry%%:*}"
    bug="${entry##*:}"
    cell_log="${LOG_ROOT}/${bug}.log"
    cell_start=$(date -u +%s)
    echo "EVENT focused_start bug=${bug}"

    # Stage an EMPTY seed dir — the bench's PoV-injection will add the
    # canonical PoV with its own `_aa_pov_` filename. We avoid pre-staging
    # to skip the FileExistsError collision.
    seeds_dir="${SEEDS_TMP}/${bug}/vcf"
    mkdir -p "${seeds_dir}"
    rm -f "${seeds_dir}"/*.vcf 2>/dev/null
    mkdir -p "${SEEDS_TMP}/${bug}/sam"

    docker run --rm \
        -v "${MOUNT_SRC}:/work" \
        -w /work \
        -e PYTHONPATH=/work \
        -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
        -e LLM_MODEL="deepseek-chat" \
        "${IMAGE_TAG}" \
        python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.verified.json \
        --out compares/results/bug_bench/biotest_focused_pov_2026_04_29 \
        --time-budget-s "${BUDGET_S}" \
        --seed-corpus-vcf "compares/results/bug_bench/biotest_focused_pov_2026_04_29/_pov_seeds/${bug}/vcf" \
        --seed-corpus-sam "compares/results/bug_bench/biotest_focused_pov_2026_04_29/_pov_seeds/${bug}/sam" \
        --only-tool biotest --only-sut "${sut}" --only-bug "${bug}" \
        > "${cell_log}" 2>&1
    rc=$?

    cell_end=$(date -u +%s)
    elapsed=$((cell_end - cell_start))
    crashes=$(find "${LOG_ROOT}/biotest/${bug}/crashes" -mindepth 1 -maxdepth 1 -type f 2>/dev/null | wc -l)
    echo "EVENT focused_done bug=${bug} rc=${rc} elapsed=${elapsed}s crashes=${crashes}"
done

echo "EVENT all_focused_done"
