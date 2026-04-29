#!/usr/bin/env bash
set -euxo pipefail
cd /work
python3.12 -c "
import pathlib
p = pathlib.Path('biotest_config.yaml')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('  format_filter: VCF', '  format_filter: SAM', 1)
txt = txt.replace('  primary_target: noodles', '  primary_target: htsjdk', 1)
p.write_text(txt, encoding='utf-8')
print('flipped to SAM + htsjdk')
"
SAM_FIXTURE="$(pwd)/data/mr_registry.sam_pristine.json"
cp "${SAM_FIXTURE}" data/mr_registry.json
export BIOTEST_SAM_REGISTRY="${SAM_FIXTURE}"
mkdir -p bug_reports
python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.sam_only.json \
    --out compares/results/bug_bench \
    --only-tool biotest \
    --only-bug htsjdk-1238 \
    --time-budget-s 300
python3.12 -c "
import pathlib
p = pathlib.Path('biotest_config.yaml')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('  format_filter: SAM', '  format_filter: VCF', 1)
txt = txt.replace('  primary_target: htsjdk', '  primary_target: noodles', 1)
p.write_text(txt, encoding='utf-8')
"
echo '[done]'
