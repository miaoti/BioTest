#!/usr/bin/env bash
# Fast re-run for the 3 htsjdk SAM cells only — reuses the SAM MR
# registry mined by run_bugbench_biotest_sam_docker.sh's prior run
# (skip Phase B mining → ~5 min instead of ~60 min).
#
# Use ONLY for verification of bug_bench_driver changes; the full
# canonical run still goes through run_bugbench_biotest_sam_docker.sh.
set -euxo pipefail

export PATH="/root/.cargo/bin:${PATH}"
cd /work

LOG_FILE="compares/results/bug_bench_sam_htsjdk_rerun.log"
mkdir -p "$(dirname "${LOG_FILE}")"
exec > >(tee -a "${LOG_FILE}") 2>&1

# 1) Make sure we're on SAM/htsjdk config (the prior SAM run already
#    flipped these but the post-run restore reverted to VCF/noodles).
python3.12 -c "
import pathlib
p = pathlib.Path('biotest_config.yaml')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('  format_filter: VCF', '  format_filter: SAM', 1)
txt = txt.replace('  primary_target: noodles', '  primary_target: htsjdk', 1)
p.write_text(txt, encoding='utf-8')
print('flipped to SAM + htsjdk')
"

# 2) Reinstate the pristine SAM registry mined by the previous run.
SAM_FIXTURE="$(pwd)/data/mr_registry.sam_pristine.json"
if [ ! -f "${SAM_FIXTURE}" ]; then
    echo "ERROR: ${SAM_FIXTURE} missing — run the full SAM script first."
    exit 1
fi
cp "${SAM_FIXTURE}" data/mr_registry.json
export BIOTEST_SAM_REGISTRY="${SAM_FIXTURE}"

mkdir -p bug_reports

# 3) Run bug_bench_driver against ONLY the 3 htsjdk SAM cells.
for bug in htsjdk-1238 htsjdk-1360 htsjdk-1410; do
    python3.12 compares/scripts/bug_bench_driver.py \
        --manifest compares/bug_bench/manifest.sam_only.json \
        --out compares/results/bug_bench \
        --only-tool biotest \
        --only-bug "${bug}" \
        --time-budget-s 300
done

# 4) Restore VCF/noodles config so follow-up runs aren't surprised.
python3.12 -c "
import pathlib
p = pathlib.Path('biotest_config.yaml')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('  format_filter: SAM', '  format_filter: VCF', 1)
txt = txt.replace('  primary_target: htsjdk', '  primary_target: noodles', 1)
p.write_text(txt, encoding='utf-8')
print('restored to VCF + noodles')
"

echo '[done] htsjdk SAM rerun complete'
