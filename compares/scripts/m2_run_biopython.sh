#!/usr/bin/env bash
# M2 fix — run biopython mutation campaigns only (vcfpy already done).
# This is split out from m2_run_mutation.sh so we can re-run just the
# biopython half after the original batch died on a script-edit race.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

DOCKER_IMAGE="${DOCKER_IMAGE:-biotest-bench:latest}"

run_bp() {
  local cell="$1"; local rep="$2"; local strat="$3"
  local short
  if [[ "${strat}" == "kill_aware" ]]; then short=kf; else short=of; fi
  local corpus="compares/results/m2_cmin/${cell}/rep_${rep}/${short}"
  local out="compares/results/m2_mut/${cell}/rep_${rep}/${short}"
  if [[ -f "${out}/summary.json" ]]; then
    echo "[m2-mut] SKIP (already exists) ${cell} rep=${rep} strat=${strat}"
    return 0
  fi
  mkdir -p "${out}"
  echo "[m2-mut] cell=${cell} rep=${rep} strat=${strat}  corpus=${corpus}  out=${out}"
  MSYS_NO_PATHCONV=1 docker run --rm \
    -v "${REPO_ROOT}:/work" -w /work \
    "${DOCKER_IMAGE}" \
    /opt/atheris-venv/bin/python /work/compares/harnesses/atheris/phase3_mutation_loop.py \
      --corpus "/work/${corpus}" \
      --out "/work/${out}" \
      --budget-s 900 \
      --per-mutant-timeout-s 60 \
      --max-mutants 0 \
      --shuffle-seed 42 2>&1 | tail -5
  if [[ -f "${out}/summary.json" ]]; then
    PYTHONIOENCODING=utf-8 /c/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe -c "
import json
d = json.load(open('${out}/summary.json'))
ms = d.get('mutation_score', {})
print(f'  -> killed={ms.get(\"killed\")} reach={ms.get(\"reachable\")} score={ms.get(\"score\", 0):.4f}')"
  fi
}

CELLS=("biopython_biotest" "biopython_atheris")
STRATS=("kill_aware" "outcome_fingerprint")

for cell in "${CELLS[@]}"; do
  for rep in 0 1 2 3; do
    for strat in "${STRATS[@]}"; do
      run_bp "${cell}" "${rep}" "${strat}"
    done
  done
done
echo "[m2-mut] biopython batch complete at $(date +%T)"
