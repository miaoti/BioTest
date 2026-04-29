#!/usr/bin/env bash
# Driver to run BioTest on noodles-vcf × VCF inside biotest-bench:latest.
# Produces coverage_artifacts/noodles/llvm-cov.json scoped to the same
# filter BioTest uses at Phase D (biotest_config.yaml:
# coverage.target_filters.VCF.noodles). Invoke from the Windows host via:
#   bash compares/docker/run.sh -- bash scripts/run_biotest_noodles_docker.sh
# or let the parent script docker-run it directly.
set -euxo pipefail

export PATH="/root/.cargo/bin:${PATH}"
cd /work

LOG_FILE="coverage_artifacts/noodles/run12.log"

# Clean prior state.
rm -f data/feedback_state.json data/rule_attempts.json data/mr_registry.json
rm -f seeds/vcf/synthetic_*.vcf
rm -rf coverage_artifacts/noodles
mkdir -p coverage_artifacts/noodles

# Mirror every subsequent command's output to a mounted log file so we
# can still see progress if `docker logs` doesn't capture stdout.
exec > >(tee -a "${LOG_FILE}") 2>&1

# Build coverage-instrumented release binary.
# --release puts it where biotest_config.yaml expects (.../release/).
cargo llvm-cov --no-report --release \
    --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
    run -- VCF seeds/vcf/minimal_single.vcf >/dev/null

INST_BIN=harnesses/rust/noodles_harness/target/llvm-cov-target/release/noodles_harness
test -x "${INST_BIN}"

# Move the initial profraws into coverage_artifacts/noodles so downstream
# runner calls (LLVM_PROFILE_FILE pattern noodles-%p-%m.profraw) append
# alongside them.
find harnesses/rust/noodles_harness/target/llvm-cov-target -name "*.profraw" \
    -exec mv {} coverage_artifacts/noodles/ \; 2>/dev/null || true

python3.12 biotest.py --phase B,C,D --verbose

# Generate llvm-cov.json from all accumulated profraws so
# measure_coverage.py can read it. NoodlesCoverageCollector would do
# this on-the-fly during Phase D, but we regenerate here post-hoc with
# explicit --package flags so noodles-vcf (external dep) is included.
cargo llvm-cov report --json \
    --manifest-path harnesses/rust/noodles_harness/Cargo.toml \
    --package noodles-vcf --package noodles_harness \
    > coverage_artifacts/noodles/llvm-cov.json

echo "=== llvm-cov.json size: ==="
ls -la coverage_artifacts/noodles/llvm-cov.json

python3.12 compares/scripts/measure_coverage.py \
    --report coverage_artifacts/noodles/llvm-cov.json \
    --label "BioTest Run 12 (noodles)" \
    --sut noodles --format VCF
