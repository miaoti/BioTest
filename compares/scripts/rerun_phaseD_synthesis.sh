#!/usr/bin/env bash
# Run BioTest with seed_synthesis enabled (Phase D) on htsjdk-1364
# specifically — the only sole-witness cell where broad-corpus + focused-PoV
# regimes both failed to produce a §5.3.1-satisfying trigger.
#
# Hypothesis: enabling seed_synthesis lets the LLM propose new file shapes
# (NaN/Inf/Infinity literal variants) beyond what MR transforms can reach
# from the canonical PoV alone. The bug-shape (NaN/Inf rejection) is a
# narrow byte pattern — synthesis can target it directly.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

LOG_ROOT="${REPO_ROOT}/compares/results/bug_bench/biotest_phaseD_synth_2026_04_29"
mkdir -p "${LOG_ROOT}"

BUDGET_S=${BUDGET_S:-3600}
IMAGE_TAG="${IMAGE_TAG:-biotest-bench:latest}"
BUG_ID="${BUG_ID:-htsjdk-1364}"
SUT="htsjdk"

MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="/${REPO_ROOT//\\//}"
fi
export MSYS_NO_PATHCONV=1

DEEPSEEK_API_KEY="$(grep -E '^DEEPSEEK_API_KEY=' .env 2>/dev/null | cut -d= -f2-)"

CELL_DIR="${LOG_ROOT}/biotest/${BUG_ID}"
mkdir -p "${CELL_DIR}"

# Stage a config that enables seed_synthesis and points outputs at the
# cell dir. The bench's run_biotest.py adapter already wires temp-config
# generation, but it hardcodes --phase C and doesn't enable synthesis;
# we side-step by writing our own config + running biotest.py directly.
CFG_REL="${CELL_DIR#${REPO_ROOT}/}/biotest_config_synth.yaml"
CFG_PATH="${REPO_ROOT}/${CFG_REL}"
echo "[phaseD] writing config to /work/${CFG_REL}"
docker run --rm \
    -v "${MOUNT_SRC}:/work" -w /work \
    "${IMAGE_TAG}" \
    python3.12 /work/compares/scripts/_make_phaseD_config.py \
    "${BUG_ID}" "/work/${CFG_REL}"
ls -la "${CFG_PATH}" 2>/dev/null && echo "[phaseD] config OK" || echo "[phaseD] config WRITE FAILED"

# Stage a single-PoV seed dir (focused regime)
SEEDS_IN="${CELL_DIR}/seeds_in"
mkdir -p "${SEEDS_IN}/vcf" "${SEEDS_IN}/sam"
cp "${REPO_ROOT}/compares/bug_bench/triggers/${BUG_ID}/original.vcf" \
   "${SEEDS_IN}/vcf/_aa_pov_${BUG_ID}_original.vcf"

mkdir -p "${CELL_DIR}/bug_reports"
mkdir -p "${CELL_DIR}/crashes"

START_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[phaseD] START ${START_TS} bug=${BUG_ID} budget=${BUDGET_S}s"

# Step 1: install pre-fix htsjdk 2.19.0 into the harness fatjar.
echo "[phaseD] install htsjdk 2.19.0 (pre-fix) into harness"
docker run --rm \
    -v "${MOUNT_SRC}:/work" -w /work -e PYTHONPATH=/work \
    "${IMAGE_TAG}" \
    python3.12 -c "
import sys
sys.path.insert(0, '/work')
from compares.scripts.bug_bench_driver import install_sut
install_sut('htsjdk', {'type':'install_version','pre_fix':'2.19.0','post_fix':'2.20.0'}, 'pre_fix')
print('install pre_fix done')
" 2>&1 | tail -3

# Step 2: run biotest.py with --phase B,C,D inside Docker
echo "[phaseD] run biotest --phase B,C,D"
CELL_LOG="${CELL_DIR}/tool.log"
docker run --rm \
    -v "${MOUNT_SRC}:/work" -w /work -e PYTHONPATH=/work \
    -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
    -e LLM_MODEL=deepseek-chat \
    "${IMAGE_TAG}" \
    timeout "${BUDGET_S}" python3.12 /work/biotest.py \
    --config "/work/${CFG_REL}" \
    --phase B,C \
    > "${CELL_LOG}" 2>&1
biotest_rc=$?
echo "[phaseD] biotest exited rc=${biotest_rc}"

# Step 3: harvest T_*.vcf trigger files into crashes/ for verify_tool_found
echo "[phaseD] harvest triggers from bug_reports/"
find "${CELL_DIR}/bug_reports" -mindepth 2 -maxdepth 2 -type f -name "T_*" 2>/dev/null | \
    while read -r f; do
        bug_id=$(basename "$(dirname "$f")")
        cp "$f" "${CELL_DIR}/crashes/${bug_id}__$(basename "$f")"
    done
crash_count=$(find "${CELL_DIR}/crashes" -mindepth 1 -maxdepth 1 -type f 2>/dev/null | wc -l)
echo "[phaseD] crashes harvested: ${crash_count}"

# Step 4: verify
echo "[phaseD] verify_tool_found"
docker run --rm \
    -v "${MOUNT_SRC}:/work" -w /work -e PYTHONPATH=/work \
    "${IMAGE_TAG}" \
    python3.12 compares/scripts/verify_tool_found.py \
    "${LOG_ROOT}" "${BUG_ID}" 2>&1 | grep -E "tool_found|reason|Summary"

END_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[phaseD] END ${END_TS}"
echo "EVENT phaseD_done bug=${BUG_ID} crashes=${crash_count}"
