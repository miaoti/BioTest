#!/usr/bin/env bash
# Post-process every vcfpy mutmut cell to rewrite its summary.json from
# the authoritative spinner-line + .py.meta exit-code source. Idempotent.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"
for d in compares/results/m2_mut/vcfpy_biotest/rep_*/{kf,of}; do
  if [[ -f "${d}/mutmut_run.log" ]]; then
    echo "=== finalize ${d} ==="
    PYTHONIOENCODING=utf-8 /c/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe \
      compares/scripts/finalize_mutation_summary.py "${d}" 2>&1 | tail -2
  fi
done
