#!/usr/bin/env bash
# M2 fix — run the mutation engine against each (cell, rep, strategy) cmin'd
# corpus produced by m2_run_cmin.sh. Outputs land at:
#
#   compares/results/m2_mut/<cell>/rep_<r>/<strategy>/summary.json
#
# Cells:
#   vcfpy_biotest      — mutmut on vcfpy. Engine = atheris/vcfpy backend
#   biopython_biotest  — atheris-mutmut on biopython
#   biopython_atheris  — atheris-mutmut on biopython (symmetry)
#
# Same shuffle-seed / budget across reps and strategies — only the corpus
# input changes. Designed to be invoked sequentially after m2_run_cmin.sh.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

DOCKER_IMAGE="${DOCKER_IMAGE:-biotest-bench:latest}"

run_biopython_mutation() {
  local cell="$1"; local rep="$2"; local strat="$3"
  local short
  if [[ "${strat}" == "kill_aware" ]]; then short=kf; else short=of; fi
  local corpus="compares/results/m2_cmin/${cell}/rep_${rep}/${short}"
  local out="compares/results/m2_mut/${cell}/rep_${rep}/${short}"
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
print(f\"  -> killed={ms.get('killed')} reach={ms.get('reachable')} score={ms.get('score'):.4f}\")"
  fi
}

run_vcfpy_mutation() {
  local rep="$1"; local strat="$2"
  local short
  if [[ "${strat}" == "kill_aware" ]]; then short=kf; else short=of; fi
  local corpus="compares/results/m2_cmin/vcfpy_biotest/rep_${rep}/${short}"
  local out="compares/results/m2_mut/vcfpy_biotest/rep_${rep}/${short}"
  mkdir -p "${out}"
  echo "[m2-mut] cell=vcfpy_biotest rep=${rep} strat=${strat}  corpus=${corpus}  out=${out}"
  PYTHONIOENCODING=utf-8 \
  /c/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe \
    compares/scripts/mutation_driver.py \
      --tool biotest --sut vcfpy \
      --corpus "${corpus}" \
      --out "${out}" \
      --budget 1800 \
      --corpus-sample 200 \
      --per-file-timeout-s 2.0 \
      --max-children 1 \
      --no-augment-corpus --no-coverage-select 2>&1 | tail -15
  # mutation_driver.py's inline summariser is incomplete for mutmut 3.x;
  # finalize_mutation_summary.py rewrites summary.json from the spinner
  # line + per-file .py.meta exit codes (the authoritative source).
  PYTHONIOENCODING=utf-8 /c/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe \
    compares/scripts/finalize_mutation_summary.py "${out}" 2>&1 | tail -3
  if [[ -f "${out}/summary.json" ]]; then
    PYTHONIOENCODING=utf-8 /c/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe -c "
import json
d = json.load(open('${out}/summary.json'))
print(f\"  -> killed={d.get('killed')} reach={d.get('reachable')} score={d.get('score', 0):.4f}\")"
  fi
}

CELLS_BP=("biopython_biotest" "biopython_atheris")
STRATS=("kill_aware" "outcome_fingerprint")

# 1. vcfpy_biotest cells (mutmut on host)
for rep in 0 1 2 3; do
  for strat in "${STRATS[@]}"; do
    run_vcfpy_mutation "${rep}" "${strat}"
  done
done

# 2. biopython cells (atheris-mutmut in docker)
for cell in "${CELLS_BP[@]}"; do
  for rep in 0 1 2 3; do
    for strat in "${STRATS[@]}"; do
      run_biopython_mutation "${cell}" "${rep}" "${strat}"
    done
  done
done

echo "[m2-mut] all 24 mutation campaigns complete"
