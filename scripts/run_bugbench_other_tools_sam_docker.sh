#!/usr/bin/env bash
# Multi-tool SAM bug-bench driver (everything EXCEPT BioTest, which
# already ran via run_bugbench_biotest_sam_docker.sh).
#
# 2026-04-21 manifest revision changed the SAM row from 10 → 9 bugs
# (4 dropped, 3 added). The biotest results are already in place;
# this script fills in jazzer / pure_random / evosuite_anchor /
# libfuzzer / cargo_fuzz against the new manifest.
#
# Per DESIGN.md §4.1 + bug_bench_driver MATRIX:
#   htsjdk SAM (1238, 1360, 1410):
#     biotest, jazzer, pure_random, evosuite_anchor
#   seqan3 SAM (6 bugs — manifest unchanged):
#     biotest, libfuzzer, pure_random
#   biopython SAM: 0 bugs (4825 dropped)
#
# Invoke from Windows host:
#   docker run -d --name biotest-bench-sam-other-tools \
#       -v "$(pwd):/work" -w /work biotest-bench:latest \
#       bash scripts/run_bugbench_other_tools_sam_docker.sh
set -euxo pipefail

export PATH="/root/.cargo/bin:${PATH}"
cd /work

LOG_FILE="compares/results/bug_bench_sam_other_tools.log"
mkdir -p "$(dirname "${LOG_FILE}")"
exec > >(tee -a "${LOG_FILE}") 2>&1

# Run each non-biotest tool that appears in the SAM MATRIX rows.
# We loop per-tool (rather than calling without --only-tool) so a
# single tool's adapter failure doesn't block the others.
for tool in jazzer pure_random evosuite_anchor libfuzzer; do
    echo "=== running ${tool} on SAM manifest ==="
    python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.sam_only.json \
        --out compares/results/bug_bench \
        --only-tool "${tool}" \
        --time-budget-s 300 || \
        echo "[warn] ${tool} pass exited non-zero (continuing)"
done

echo "[done] non-biotest SAM bug-bench complete"
