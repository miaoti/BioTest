#!/usr/bin/env bash
# Re-run BioTest on the 8 sole-witness cells inside biotest-bench Docker
# image, using DeepSeek as the LLM. After the run, verify_tool_found.py
# computes harvested-only attribution per cell.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

LOG_ROOT="${REPO_ROOT}/compares/results/bug_bench/biotest_rerun_2026_04_28"
mkdir -p "${LOG_ROOT}"

BUDGET_S=${BUDGET_S:-3600}
IMAGE_TAG="${IMAGE_TAG:-biotest-bench:latest}"

# Path translation matching compares/docker/run.sh exactly.
MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="/${REPO_ROOT//\\//}"
fi
export MSYS_NO_PATHCONV=1

DEEPSEEK_API_KEY="$(grep -E '^DEEPSEEK_API_KEY=' .env 2>/dev/null | cut -d= -f2-)"
if [ -z "${DEEPSEEK_API_KEY}" ]; then
    echo "FATAL: DEEPSEEK_API_KEY not found in .env" >&2
    exit 2
fi

CELLS=(
    "htsjdk:htsjdk-1364"
    "htsjdk:htsjdk-1372"
    "htsjdk:htsjdk-1544"
    "htsjdk:htsjdk-1554"
    "vcfpy:vcfpy-127"
    "vcfpy:vcfpy-146"
    "vcfpy:vcfpy-176"
    "noodles:noodles-268"
)

START_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[rerun] START ${START_TS}  budget=${BUDGET_S}s  cells=${#CELLS[@]}"
echo "[rerun] log_root=${LOG_ROOT}"
echo "[rerun] image=${IMAGE_TAG}  mount=${MOUNT_SRC}"

for entry in "${CELLS[@]}"; do
    sut="${entry%%:*}"
    bug="${entry##*:}"
    cell_log="${LOG_ROOT}/${bug}.log"
    cell_status="${LOG_ROOT}/${bug}.status"

    cell_start=$(date -u +%s)
    echo "EVENT cell_start bug=${bug} sut=${sut} t=$(date -u +%H:%M:%S)"

    docker run --rm \
        -v "${MOUNT_SRC}:/work" \
        -w /work \
        -e PYTHONPATH=/work \
        -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
        -e LLM_MODEL="deepseek-chat" \
        -e LLM_TEMPERATURE="0.0" \
        -e LLM_MAX_TOKENS="4096" \
        "${IMAGE_TAG}" \
        python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.verified.json \
        --out compares/results/bug_bench/biotest_rerun_2026_04_28 \
        --time-budget-s "${BUDGET_S}" \
        --seed-corpus-vcf seeds/vcf \
        --seed-corpus-sam seeds/sam \
        --only-tool biotest \
        --only-sut "${sut}" \
        --only-bug "${bug}" \
        > "${cell_log}" 2>&1
    rc=$?

    cell_end=$(date -u +%s)
    elapsed=$((cell_end - cell_start))

    crashes_dir="${LOG_ROOT}/biotest/${bug}/crashes"
    crashes_count=0
    if [ -d "${crashes_dir}" ]; then
        crashes_count=$(find "${crashes_dir}" -mindepth 1 -maxdepth 1 -type f 2>/dev/null | wc -l)
    fi

    rj="${LOG_ROOT}/biotest/${bug}/result.json"
    if [ -f "${rj}" ]; then
        verdict=$(py -3.12 -c "
import json, sys
r = json.loads(open(sys.argv[1]).read())
print(f\"detected={r.get('detected')} confirmed={r.get('confirmed_fix_silences_signal')} via_tool={r.get('detected_via_tool_output')} via_pov={r.get('detected_via_pov_verification')}\")
" "${rj}" 2>&1)
    else
        verdict="(no result.json)"
    fi

    echo "rc=${rc} elapsed=${elapsed}s crashes=${crashes_count} verdict=${verdict}" > "${cell_status}"
    echo "EVENT cell_done bug=${bug} rc=${rc} elapsed=${elapsed}s crashes=${crashes_count} verdict=${verdict}"
done

END_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "EVENT all_done start=${START_TS} end=${END_TS}"
