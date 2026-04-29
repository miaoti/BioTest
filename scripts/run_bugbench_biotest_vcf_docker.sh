#!/usr/bin/env bash
# Real-Bug Benchmark driver (VCF phase) — run BioTest against every
# verified VCF bug (25 bugs across htsjdk / vcfpy / noodles).
#
# DESIGN.md §5 protocol: per bug, install pre-fix SUT, run BioTest for
# --time-budget-s seconds, install post-fix, replay trigger to confirm
# silence. Bounded 300 s per cell for an initial demo-run; the production
# sweep would use 7200 s per cell (§5.5).
#
# Invoke from Windows host:
#   docker run -d --name biotest-bugbench-vcf \
#       -v "$(pwd):/work" -w /work biotest-bench:latest \
#       bash scripts/run_bugbench_biotest_vcf_docker.sh
set -euxo pipefail

export PATH="/root/.cargo/bin:${PATH}"
cd /work

LOG_FILE="compares/results/bug_bench_vcf.log"
mkdir -p "$(dirname "${LOG_FILE}")"
exec > >(tee -a "${LOG_FILE}") 2>&1

# 2026-04-24: adapter now wipes bug_reports/ per cell (see
# run_biotest.py ENOMEM fix). Don't attempt a session-level rm here —
# 9p is flaky and `rm -rf bug_reports/` was aborting the whole
# script via `set -e` when the dir had 50k+ leftover entries from
# prior runs. Let the adapter do cleanup incrementally.
mkdir -p bug_reports

python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.vcf_only.json \
    --out compares/results/bug_bench \
    --only-tool biotest \
    --time-budget-s 300

# 2026-04-24: force 9p sync back to host. Writes to the bind mount
# during the run are sometimes visible only after an explicit sync;
# without this, `docker rm` orphans files that the driver did write.
sync
ls -la compares/results/bug_bench/ | head -5
ls compares/results/bug_bench/biotest/ 2>/dev/null | wc -l
echo "[done] VCF phase of BioTest bug_bench complete"
