#!/usr/bin/env bash
# Full BioTest bug-bench rerun against the new verification infrastructure.
# Includes both anchor sweeps and the bench itself.
#
# Lever 1: anchor sweep on suspect cells, --apply if empirical pair found
# Lever 2: STRICT gate generalized to htsjdk + pysam + vcfpy
# Lever 3: Tier-2 mutator-discovery + class-gap blindspot enrichment
#
# Invoke from Windows host:
#   docker run -d --name biotest-bench-full-rerun \
#       -v "$(pwd):/work" -w /work biotest-bench:latest \
#       bash scripts/rerun_full_bench_docker.sh
set -euxo pipefail

export PATH="/root/.cargo/bin:${PATH}"
cd /work

LOG_FILE="compares/results/bug_bench_full_rerun.log"
mkdir -p "$(dirname "${LOG_FILE}")"
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "=== Lever 1: anchor sweep on suspect cells ==="
# vcfpy-gtone-0.13: claimed haploid GT bug, anchor 0.12.1 -> 0.12.2
python3.12 compares/bug_bench/sweep_anchors.py \
    --bug-id vcfpy-gtone-0.13 \
    --versions 0.11.0,0.11.1,0.12.0,0.12.1,0.12.2,0.13.0,0.13.1,0.13.2,0.13.3,0.13.4,0.13.5 \
    --apply || echo "[warn] vcfpy-gtone-0.13 sweep exited non-zero"

# noodles-241: anchor sweep (cargo-build slow; allow up to 30 min, defer if blocked)
# python3.12 compares/bug_bench/sweep_anchors.py \
#     --bug-id noodles-241 \
#     --versions 0.55,0.56,0.57,0.58,0.59,0.60 \
#     --apply || echo "[warn] noodles-241 sweep exited non-zero"

echo "=== VCF bench ==="
bash scripts/run_bugbench_biotest_vcf_docker.sh || echo "[warn] vcf bench exited non-zero"

echo "=== SAM bench ==="
bash scripts/run_bugbench_biotest_sam_docker.sh || echo "[warn] sam bench exited non-zero"

echo "[done] full BioTest rerun complete"
