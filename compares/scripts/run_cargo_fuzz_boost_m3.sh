#!/usr/bin/env bash
# cargo-fuzz × noodles-vcf M3 boost — reps 4..9 (output dirs run_05..10).
# Existing 4-run regime: 1800 s fuzz budget + cargo-mutants ≈ 33 min.
# 6 reps × ~63 min ≈ 6.3 hours sequential.
set -euo pipefail
cd "$(dirname "$0")/../.."

REPS="${REPS:-05 06 07 08 09 10}"
LOG_DIR="compares/results/mutation/biotest/m3_boost_logs/cargo_fuzz"
mkdir -p "$LOG_DIR"

echo "[$(date -u +%H:%M:%S)] === cargo-fuzz × noodles boost (REPS=$REPS) ==="
for R in $REPS; do
    SEED=$((10#$R * 100 + 7))
    COV_OUT="compares/results/coverage/cargo_fuzz/noodles/run_$R"
    MUT_OUT="compares/results/mutation/cargo_fuzz/noodles/run_$R"
    GROWTH="$COV_OUT/growth_0.json"
    SUMMARY="$MUT_OUT/summary.json"

    if [[ -f "$GROWTH" ]]; then
        echo "[$(date -u +%H:%M:%S)]   skip rep_$R coverage ($GROWTH exists)"
    else
        echo "[$(date -u +%H:%M:%S)]   rep_$R: cargo-fuzz coverage (budget=1800, seed=$SEED)"
        MSYS_NO_PATHCONV=1 docker run --rm \
            -v "$(pwd):/work" -w /work -e PYTHONPATH=/work \
            biotest-bench:latest \
            python3.12 compares/scripts/coverage_sampler.py \
                --tool cargo_fuzz --sut noodles --format VCF \
                --seed-corpus compares/results/bench_seeds/vcf \
                --budget 1800 --reps 1 \
                --out "$COV_OUT" \
            > "$LOG_DIR/cov_rep_${R}.log" 2>&1
    fi

    if [[ -f "$SUMMARY" ]]; then
        echo "[$(date -u +%H:%M:%S)]   skip rep_$R cargo-mutants ($SUMMARY exists)"
    else
        echo "[$(date -u +%H:%M:%S)]   rep_$R: cargo-mutants"
        # coverage_sampler --reps 1 --out X writes corpus to X/run_0/corpus
        # PYTHONIOENCODING=utf-8 needed because mutation_driver.py prints
        # Unicode arrows that fail under Windows cp1252 stdout redirection.
        PYTHONIOENCODING=utf-8 py -3.12 compares/scripts/mutation_driver.py \
            --tool cargo_fuzz --sut noodles \
            --corpus "$COV_OUT/run_0/corpus" \
            --out "$MUT_OUT" \
            --budget 7200 --corpus-sample 200 \
            > "$LOG_DIR/mut_rep_${R}.log" 2>&1 || true
    fi
done

echo "[$(date -u +%H:%M:%S)] === Done ==="
