#!/usr/bin/env bash
# Phase 2 driver: cargo-fuzz × noodles-vcf (VCF only), primary regime.
#
# DESIGN.md §13.5 Phase 2. Produces:
#   compares/results/coverage/cargo_fuzz/noodles/growth_{0,1,2}.json
# and a run-log at compares/results/coverage/cargo_fuzz/phase2_cargo_fuzz_noodles.log.
#
# Invoke inside biotest-bench:
#   bash compares/scripts/phase2_cargo_fuzz_noodles.sh
# …or from the Windows host:
#   bash compares/docker/run.sh bash compares/scripts/phase2_cargo_fuzz_noodles.sh
#
# Env overrides:
#   BUDGET_S   — per-rep wall-clock seconds (default 7200 = DESIGN primary)
#   REPS       — independent reps (default 3)
#   TICKS      — comma-separated tick seconds
#                (default 1,10,60,300,1800,7200 per DESIGN §3.2)
#
# Tooling prerequisites (already baked into biotest-bench:latest by §13.1):
#   * rustup stable + llvm-tools-preview + cargo-fuzz 0.13+ + cargo-llvm-cov
#   * The cargo-fuzz target must be built once:
#       cd compares/harnesses/cargo_fuzz && \
#         cargo fuzz build --sanitizer none noodles_vcf_target --release
#   * harnesses/rust/noodles_harness/ — coverage sampler auto-rebuilds this
#     with RUSTFLAGS=-C instrument-coverage at run start.
set -euo pipefail

BUDGET_S="${BUDGET_S:-7200}"
REPS="${REPS:-3}"
TICKS="${TICKS:-1,10,60,300,1800,7200}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SEED_DIR="${REPO_ROOT}/compares/results/bench_seeds/vcf"
OUT_DIR="${REPO_ROOT}/compares/results/coverage/cargo_fuzz/noodles"
LOG_FILE="${OUT_DIR}/phase2_cargo_fuzz_noodles.log"
mkdir -p "${OUT_DIR}"

export PATH="/root/.cargo/bin:${PATH}"

{
  echo "[$(date -Is)] phase2 start — budget=${BUDGET_S}s reps=${REPS} ticks=${TICKS}"
  echo "[$(date -Is)] repo=${REPO_ROOT}"
  echo "[$(date -Is)] seed=${SEED_DIR}  out=${OUT_DIR}  log=${LOG_FILE}"
} | tee -a "${LOG_FILE}"

python3.12 "${REPO_ROOT}/compares/scripts/coverage_sampler.py" \
    --tool cargo_fuzz --sut noodles --format VCF \
    --seed-corpus "${SEED_DIR}" \
    --budget "${BUDGET_S}" --reps "${REPS}" \
    --ticks "${TICKS}" \
    --out "${OUT_DIR}" \
    2>&1 | tee -a "${LOG_FILE}"

echo "[$(date -Is)] phase2 complete." | tee -a "${LOG_FILE}"
