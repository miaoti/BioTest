#!/usr/bin/env bash
# M2 fix — produce cmin'd corpora for both selectors, every (cell, rep)
# combination. Inputs:
#
#   vcfpy_biotest   ←  compares/results/coverage/biotest_rep_<r>/vcfpy/run_0/corpus
#   biopython_biotest ← compares/results/coverage/biotest_rep_<r>/biopython/run_0/corpus
#   biopython_atheris ← compares/results/coverage/atheris/biopython/run_<r>/corpus
#
# Output: compares/results/m2_cmin/<cell>/rep_<r>/{kf,of}/  + summary.json
#
# Each invocation also installs pydantic into /opt/atheris-venv (ephemeral
# per the --rm container, so we install on every call). Runs sequentially
# to avoid the Windows-Docker 9p ENOMEM issue under concurrent installs.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

run_cmin() {
  local cell="$1"   # vcfpy_biotest | biopython_biotest | biopython_atheris
  local rep="$2"    # 0..3
  local strat="$3"  # kill_aware | outcome_fingerprint
  local sut fmt input
  case "${cell}" in
    vcfpy_biotest)
      sut=vcfpy; fmt=VCF
      input="compares/results/coverage/biotest_rep_${rep}/vcfpy/run_0/corpus" ;;
    biopython_biotest)
      sut=biopython; fmt=SAM
      input="compares/results/coverage/biotest_rep_${rep}/biopython/run_0/corpus" ;;
    biopython_atheris)
      sut=biopython; fmt=SAM
      input="compares/results/coverage/atheris/biopython/run_${rep}/corpus" ;;
    *) echo "unknown cell ${cell}" >&2; return 2 ;;
  esac
  local short
  if [[ "${strat}" == "kill_aware" ]]; then short=kf; else short=of; fi
  local out="compares/results/m2_cmin/${cell}/rep_${rep}/${short}"
  local sum="compares/results/m2_cmin/${cell}/rep_${rep}/${short}_summary.json"
  rm -rf "${out}"; mkdir -p "${out}"
  echo "[m2-cmin] cell=${cell} rep=${rep} strat=${strat}  in=${input}"
  MSYS_NO_PATHCONV=1 docker run --rm \
    -v "${REPO_ROOT}:/work" -w /work \
    biotest-bench:latest bash -c "\
      /opt/atheris-venv/bin/python -m pip install pydantic --quiet >/dev/null 2>&1 && \
      /opt/atheris-venv/bin/python compares/scripts/corpus_minimize.py \
        --input /work/${input} \
        --output /work/${out} \
        --sut ${sut} --format ${fmt} \
        --keep 200 --strategy ${strat} \
        --probe-mutants 30" 2>&1 | tail -15 | tee "${sum}.log"
  if [[ -d "${out}" ]]; then
    echo "{\"cell\":\"${cell}\",\"rep\":${rep},\"strategy\":\"${strat}\",\"kept\":$(ls "${out}" | grep -v kept.manifest.jsonl | wc -l),\"input_count\":$(ls "${input}" | wc -l)}" > "${sum}"
    echo "  → kept $(cat "${sum}" | grep -oP '"kept":\d+' | grep -oP '\d+') files"
  fi
}

CELLS=("vcfpy_biotest" "biopython_biotest" "biopython_atheris")
STRATS=("kill_aware" "outcome_fingerprint")

for cell in "${CELLS[@]}"; do
  for rep in 0 1 2 3; do
    for strat in "${STRATS[@]}"; do
      run_cmin "${cell}" "${rep}" "${strat}"
    done
  done
done
echo "[m2-cmin] all 24 cmin runs complete"
