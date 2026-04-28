#!/usr/bin/env bash
# Phase 3 driver: Atheris × biopython, mutation score via mutmut-style operators.
#
# DESIGN.md §3.3 + §13.5 Phase 3. Runs the AST-mutation + corpus-replay
# loop inside biotest-bench:latest so biopython lives in the Atheris venv
# (/opt/atheris-venv/, Python 3.11) and the mutation target is the
# container's writable site-packages copy of Bio/Align/sam.py.
#
# Produces:
#   compares/results/mutation/atheris/biopython/summary.json
#   compares/results/mutation/atheris/biopython/mutants.jsonl
#   compares/results/mutation/atheris/biopython/_worker.py
#
# Env overrides:
#   BUDGET_S             — wall budget for the mutation loop (default 900)
#   PER_MUTANT_TIMEOUT_S — per-mutant worker hard timeout (default 60)
#   MAX_MUTANTS          — cap on mutants to test (0 = budget-bounded)
#   CORPUS_DIR           — corpus path (default rep 0 Phase 2 corpus)
#   DOCKER_IMAGE         — container image (default biotest-bench:latest)
set -euo pipefail

BUDGET_S="${BUDGET_S:-900}"
PER_MUTANT_TIMEOUT_S="${PER_MUTANT_TIMEOUT_S:-60}"
MAX_MUTANTS="${MAX_MUTANTS:-0}"
DOCKER_IMAGE="${DOCKER_IMAGE:-biotest-bench:latest}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# TOOL env var lets us reuse this driver for biotest as well as atheris.
TOOL="${TOOL:-atheris}"
CORPUS_DIR="${CORPUS_DIR:-${REPO_ROOT}/compares/results/coverage/${TOOL}/biopython/run_0/corpus}"
OUT_DIR="${OUT_DIR:-${REPO_ROOT}/compares/results/mutation/${TOOL}/biopython}"
LOG_FILE="${OUT_DIR}/phase3_${TOOL}_biopython.log"
mkdir -p "${OUT_DIR}"

# Container-visible paths — REPO_ROOT is mounted as /work.
REL_OUT="${OUT_DIR#${REPO_ROOT}/}"
REL_CORPUS="${CORPUS_DIR#${REPO_ROOT}/}"

{
  echo "[$(date -Is)] phase3 atheris x biopython — budget=${BUDGET_S}s"
  echo "[$(date -Is)] image=${DOCKER_IMAGE}"
  echo "[$(date -Is)] corpus=${CORPUS_DIR}"
  echo "[$(date -Is)] out=${OUT_DIR}"
} | tee -a "${LOG_FILE}"

# NOTE: coverage-guided corpus selection was evaluated for biopython
# (r19, 2026-04-23) and measured NEUTRAL — it picks 72 curated primary
# seeds + 8 coverage-diverse struct files, but biopython's strict
# AlignmentIterator sends struct files into error-handling paths whose
# lines inflate reachable without producing kills (132/523 selected vs
# run-1's 130/202 primary-only). For biopython the optimal corpus is
# the curated primary set alone; coverage-selection does not help.
# Integration is therefore limited to vcfpy (see mutation_driver.py
# _coverage_select_if_supported for vcfpy — coverage.py signal there
# genuinely maps to kills).

MSYS_NO_PATHCONV=1 docker run --rm \
    -v "${REPO_ROOT}:/work" \
    -w /work \
    "${DOCKER_IMAGE}" \
    /opt/atheris-venv/bin/python \
    /work/compares/harnesses/atheris/phase3_mutation_loop.py \
    --corpus "/work/${REL_CORPUS}" \
    --out "/work/${REL_OUT}" \
    --budget-s "${BUDGET_S}" \
    --per-mutant-timeout-s "${PER_MUTANT_TIMEOUT_S}" \
    --max-mutants "${MAX_MUTANTS}" \
    2>&1 | tee -a "${LOG_FILE}"

echo "[$(date -Is)] phase3 atheris x biopython complete." | tee -a "${LOG_FILE}"
