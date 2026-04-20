#!/usr/bin/env bash
# Phase 2 driver: Atheris × biopython, SAM only, primary regime (2h×3 reps).
#
# DESIGN.md §13.5 Phase 2. Produces:
#   compares/results/coverage/atheris/biopython/growth_{0,1,2}.json
#   compares/results/coverage/atheris/biopython/run_{0,1,2}/harness_growth.json
# and a run-log at
#   compares/results/coverage/atheris/phase2_atheris_biopython.log
#
# Invoke from the Windows host (docker in-loop handled by the sampler):
#   bash compares/scripts/phase2_atheris_biopython.sh
#
# Env overrides:
#   BUDGET_S — per-rep wall-clock (default 7200 = DESIGN primary regime)
#   REPS     — independent reps (default 3)
#   TICKS    — comma-separated sample points (default DESIGN §3.2 log ticks)
set -euo pipefail

BUDGET_S="${BUDGET_S:-7200}"
REPS="${REPS:-3}"
TICKS="${TICKS:-1,10,60,300,1800,7200}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="${REPO_ROOT}/compares/results/coverage/atheris/biopython"
SEED_DIR="${REPO_ROOT}/compares/results/bench_seeds/sam"
LOG_FILE="${REPO_ROOT}/compares/results/coverage/atheris/phase2_atheris_biopython.log"
mkdir -p "${OUT_DIR}"

{
  echo "[$(date -Is)] phase2 atheris x biopython — budget=${BUDGET_S}s reps=${REPS} ticks=${TICKS}"
  echo "[$(date -Is)] repo=${REPO_ROOT}"
  echo "[$(date -Is)] out=${OUT_DIR}"
} | tee -a "${LOG_FILE}"

PYTHONIOENCODING=utf-8 python3.12 "${REPO_ROOT}/compares/scripts/coverage_sampler.py" \
    --tool atheris --sut biopython --format SAM \
    --seed-corpus "${SEED_DIR}" \
    --budget "${BUDGET_S}" --reps "${REPS}" \
    --ticks "${TICKS}" \
    --out "${OUT_DIR}" \
    2>&1 | tee -a "${LOG_FILE}"

echo "[$(date -Is)] phase2 atheris x biopython complete." | tee -a "${LOG_FILE}"
