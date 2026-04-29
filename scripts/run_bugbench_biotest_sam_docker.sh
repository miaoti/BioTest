#!/usr/bin/env bash
# Real-Bug Benchmark driver (SAM phase) — run BioTest against every
# verified SAM bug (10 bugs: 3 htsjdk/SAM + 1 biopython + 6 seqan3).
#
# Precondition: SAM MR registry must be populated. We mine it here via
# Phase B before running bug_bench.
#
# Invoke from Windows host:
#   docker run -d --name biotest-bugbench-sam \
#       -v "$(pwd):/work" -w /work biotest-bench:latest \
#       bash scripts/run_bugbench_biotest_sam_docker.sh
set -euxo pipefail

export PATH="/root/.cargo/bin:${PATH}"
cd /work

LOG_FILE="compares/results/bug_bench_sam.log"
mkdir -p "$(dirname "${LOG_FILE}")"
exec > >(tee -a "${LOG_FILE}") 2>&1

# 1) Snapshot the VCF MR registry so we can restore it afterwards.
if [ -f data/mr_registry.json ]; then
    cp data/mr_registry.json data/mr_registry.json.vcf_run12
fi
if [ -f data/feedback_state.json ]; then
    cp data/feedback_state.json data/feedback_state.json.vcf_run12
fi

# 2) Flip format_filter AND primary_target for SAM. noodles is
# VCF-only — leaving primary_target=noodles makes Phase C skip
# every SAM MR ("0 tests"). htsjdk is the only multi-format SUT
# in the matrix, so we use it as the primary for SAM.
python3.12 -c "
import yaml, pathlib
p = pathlib.Path('biotest_config.yaml')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('  format_filter: VCF', '  format_filter: SAM', 1)
txt = txt.replace('  primary_target: noodles', '  primary_target: htsjdk', 1)
p.write_text(txt, encoding='utf-8')
print('flipped format_filter to SAM + primary_target to htsjdk')
"

# 3) Mine SAM MRs (Phase B only — we don't need Phase C/D coverage here).
rm -f data/mr_registry.json
rm -f data/feedback_state.json data/rule_attempts.json
python3.12 biotest.py --phase B --verbose

# 2026-04-25: pin the freshly-mined SAM registry to a stable
# "fixture" path that the adapter reads from. /work/data/mr_registry.json
# was being mutated/contaminated mid-run (hybrid SAM+VCF state observed
# in v6 ELT cell, despite Phase B only writing SAM); pinning to the
# fixture path eliminates that race. The adapter (run_biotest.py) sees
# the BIOTEST_SAM_REGISTRY env var and uses it for `phase_b.registry_path`
# in the per-cell temp config.
sync
SAM_FIXTURE="$(pwd)/data/mr_registry.sam_pristine.json"
cp data/mr_registry.json "${SAM_FIXTURE}"
python3.12 -c "
import json
m = json.load(open('${SAM_FIXTURE}'))
print(f'PINNED SAM registry @ ${SAM_FIXTURE}: enforced={len(m.get(\"enforced\",[]))} quarantine={len(m.get(\"quarantine\",[]))}')
from collections import Counter
scopes = Counter(mr.get('scope','?') for mr in m.get('enforced',[]))
print('  scopes:', dict(scopes))
"
export BIOTEST_SAM_REGISTRY="${SAM_FIXTURE}"

# 4) Don't try to wipe bug_reports/ here — adapter handles per-cell
# cleanup, and `set -e` would abort the whole script if 9p mount
# refused the rm (Windows-Docker pathology — see run_biotest.py).
mkdir -p bug_reports

# 5) Run bug_bench SAM phase.
python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.sam_only.json \
    --out compares/results/bug_bench \
    --only-tool biotest \
    --time-budget-s 300

# 6) Restore format_filter to VCF + restore registry so follow-up runs
#    aren't surprised.
python3.12 -c "
import pathlib
p = pathlib.Path('biotest_config.yaml')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('  format_filter: SAM', '  format_filter: VCF', 1)
txt = txt.replace('  primary_target: htsjdk', '  primary_target: noodles', 1)
p.write_text(txt, encoding='utf-8')
print('restored format_filter to VCF + primary_target to noodles')
"
cp data/mr_registry.json data/mr_registry.json.sam_run13
if [ -f data/mr_registry.json.vcf_run12 ]; then
    cp data/mr_registry.json.vcf_run12 data/mr_registry.json
fi

echo "[done] SAM phase of BioTest bug_bench complete"
