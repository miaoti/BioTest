#!/usr/bin/env bash
# Run BioTest with the merged 32-MR registry on all manifest bugs not
# yet tool-found. Uses bug_bench_driver (Phase C only, broad-corpus +
# PoV injection) for speed.
#
# Goal: see how many of the 23 not-yet-tool-found cells flip with
# the bigger MR registry.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

LOG_ROOT="${REPO_ROOT}/compares/results/bug_bench/biotest_all_remaining_2026_04_29"
mkdir -p "${LOG_ROOT}"

BUDGET_S=${BUDGET_S:-1800}
IMAGE_TAG="${IMAGE_TAG:-biotest-bench:latest}"

MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="/${REPO_ROOT//\\//}"
fi
export MSYS_NO_PATHCONV=1

DEEPSEEK_API_KEY="$(grep -E '^DEEPSEEK_API_KEY=' .env 2>/dev/null | cut -d= -f2-)"

# 23 cells not yet tool-found, organized by SUT.
CELLS=(
    "htsjdk:htsjdk-1238" "htsjdk:htsjdk-1364" "htsjdk:htsjdk-1389"
    "htsjdk:htsjdk-1401" "htsjdk:htsjdk-1403" "htsjdk:htsjdk-1418"
    "htsjdk:htsjdk-1637"
    "vcfpy:vcfpy-145" "vcfpy:vcfpy-171"
    "noodles:noodles-223" "noodles:noodles-224" "noodles:noodles-241"
    "noodles:noodles-259" "noodles:noodles-300" "noodles:noodles-339"
    "noodles:noodles-inforay-0.64" "noodles:noodles-ob1-0.23"
    "seqan3:seqan3-2418" "seqan3:seqan3-2869" "seqan3:seqan3-3081"
    "seqan3:seqan3-3098" "seqan3:seqan3-3269" "seqan3:seqan3-3406"
)

START_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[all_remaining] START ${START_TS}  budget=${BUDGET_S}s/cell  cells=${#CELLS[@]}"

for entry in "${CELLS[@]}"; do
    sut="${entry%%:*}"
    bug="${entry##*:}"
    cell_log="${LOG_ROOT}/${bug}.log"
    cell_start=$(date -u +%s)
    echo "EVENT cell_start bug=${bug} sut=${sut} t=$(date -u +%H:%M:%S)"

    docker run --rm \
        -v "${MOUNT_SRC}:/work" -w /work -e PYTHONPATH=/work \
        -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
        -e LLM_MODEL="deepseek-chat" \
        -e LLM_TEMPERATURE="0.0" \
        "${IMAGE_TAG}" \
        python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.verified.json \
        --out "compares/results/bug_bench/biotest_all_remaining_2026_04_29" \
        --time-budget-s "${BUDGET_S}" \
        --seed-corpus-vcf seeds/vcf \
        --seed-corpus-sam seeds/sam \
        --only-tool biotest --only-sut "${sut}" --only-bug "${bug}" \
        > "${cell_log}" 2>&1
    rc=$?

    cell_end=$(date -u +%s)
    elapsed=$((cell_end - cell_start))
    crashes_dir="${LOG_ROOT}/biotest/${bug}/crashes"
    crashes=$(find "${crashes_dir}" -mindepth 1 -maxdepth 1 -type f 2>/dev/null | wc -l)

    echo "EVENT cell_done bug=${bug} rc=${rc} elapsed=${elapsed}s crashes=${crashes}"
done

END_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "EVENT all_done start=${START_TS} end=${END_TS}"
