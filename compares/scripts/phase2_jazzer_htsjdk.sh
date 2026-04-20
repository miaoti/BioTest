#!/usr/bin/env bash
# Phase 2 driver: Jazzer × htsjdk, both formats, primary regime (2h×3 reps).
#
# DESIGN.md §13.5 Phase 2. Produces:
#   compares/results/coverage/jazzer/htsjdk_vcf/growth_{0,1,2}.json
#   compares/results/coverage/jazzer/htsjdk_sam/growth_{0,1,2}.json
# and a run-log at compares/results/coverage/jazzer/phase2_jazzer_htsjdk.log.
#
# Invoke inside biotest-bench:
#   bash compares/scripts/phase2_jazzer_htsjdk.sh
# …or from the Windows host:
#   bash compares/docker/run.sh bash compares/scripts/phase2_jazzer_htsjdk.sh
#
# Env overrides:
#   BUDGET_S   — per-rep wall-clock (default 7200 = DESIGN primary regime)
#   REPS       — independent reps (default 3)
#   FORMATS    — space-separated list (default "VCF SAM")
#   PORT_BASE  — TCP port base for jacocoagent; VCF uses this, SAM += 100
set -euo pipefail

BUDGET_S="${BUDGET_S:-7200}"
REPS="${REPS:-3}"
FORMATS="${FORMATS:-VCF SAM}"
PORT_BASE="${PORT_BASE:-6300}"
TICKS="${TICKS:-1,10,60,300,1800,7200}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_ROOT="${REPO_ROOT}/compares/results/coverage/jazzer"
LOG_FILE="${OUT_ROOT}/phase2_jazzer_htsjdk.log"
mkdir -p "${OUT_ROOT}"

{
  echo "[$(date -Is)] phase2 start — budget=${BUDGET_S}s reps=${REPS} formats='${FORMATS}'"
  echo "[$(date -Is)] repo=${REPO_ROOT}"
  echo "[$(date -Is)] log=${LOG_FILE}"
} | tee -a "${LOG_FILE}"

for FMT in ${FORMATS}; do
  case "${FMT}" in
    VCF) SEED_DIR="${REPO_ROOT}/compares/results/bench_seeds/vcf"; OUT_DIR="${OUT_ROOT}/htsjdk_vcf"; PORT=${PORT_BASE} ;;
    SAM) SEED_DIR="${REPO_ROOT}/compares/results/bench_seeds/sam"; OUT_DIR="${OUT_ROOT}/htsjdk_sam"; PORT=$((PORT_BASE + 100)) ;;
    *) echo "unknown format ${FMT}" >&2; exit 1 ;;
  esac
  mkdir -p "${OUT_DIR}"
  echo "[$(date -Is)] -- cell jazzer x htsjdk ${FMT} — out=${OUT_DIR}" | tee -a "${LOG_FILE}"
  python3.12 "${REPO_ROOT}/compares/scripts/coverage_sampler.py" \
      --tool jazzer --sut htsjdk --format "${FMT}" \
      --seed-corpus "${SEED_DIR}" \
      --budget "${BUDGET_S}" --reps "${REPS}" \
      --ticks "${TICKS}" \
      --jacoco-port-start "${PORT}" \
      --out "${OUT_DIR}" \
      2>&1 | tee -a "${LOG_FILE}"
  echo "[$(date -Is)] cell ${FMT} done." | tee -a "${LOG_FILE}"
done

echo "[$(date -Is)] phase2 complete." | tee -a "${LOG_FILE}"
