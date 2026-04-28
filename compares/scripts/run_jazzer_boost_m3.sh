#!/usr/bin/env bash
# Jazzer × htsjdk M3 boost — reps 4..9 for VCF + SAM.
# Reproducer mirrors compares/results/jazzer_4rep_baseline.md §"Reproducer"
# extended to reps 4..9. Runs sequentially to avoid the PIT 0-tests-run
# anomaly documented for parallel containers on htsjdk/SAM.
set -euo pipefail
cd "$(dirname "$0")/../.."

REPS="4 5 6 7 8 9"
FORMATS="VCF SAM"
LOG_DIR="compares/results/mutation/biotest/m3_boost_logs/jazzer"
mkdir -p "$LOG_DIR"

echo "[$(date -u +%H:%M:%S)] === Jazzer coverage (300 s × $REPS × $FORMATS) ==="
for R in $REPS; do
    for FMT in $FORMATS; do
        LCASE=$(echo "$FMT" | tr A-Z a-z)
        SEEDS="compares/results/bench_seeds/$LCASE"
        OUT="compares/results/coverage/jazzer_4rep/htsjdk_$LCASE/rep_$R"
        if [[ -f "$OUT/growth_0.json" ]]; then
            echo "[$(date -u +%H:%M:%S)]   skip $OUT (already exists)"
            continue
        fi
        echo "[$(date -u +%H:%M:%S)]   coverage rep_$R $FMT -> $OUT"
        MSYS_NO_PATHCONV=1 docker run --rm \
            -v "$(pwd):/work" -w /work -e PYTHONPATH=/work \
            biotest-bench:latest \
            python3.12 compares/scripts/coverage_sampler.py \
                --tool jazzer --sut htsjdk --format "$FMT" \
                --seed-corpus "$SEEDS" \
                --budget 300 --reps 1 \
                --out "$OUT" \
            > "$LOG_DIR/cov_rep_${R}_${LCASE}.log" 2>&1
    done
done

echo "[$(date -u +%H:%M:%S)] === Stage run_N symlinks for PIT ==="
for FMT in $FORMATS; do
    LCASE=$(echo "$FMT" | tr A-Z a-z)
    pushd "compares/results/coverage/jazzer_4rep/htsjdk_$LCASE" > /dev/null
    for N in $REPS; do
        ln -sfn "rep_$N/run_0" "run_$N"
    done
    popd > /dev/null
done

echo "[$(date -u +%H:%M:%S)] === PIT mutation (sequential) ==="
for R in $REPS; do
    for FMT in $FORMATS; do
        LCASE=$(echo "$FMT" | tr A-Z a-z)
        SUMMARY="compares/results/mutation/jazzer_4rep/rep_$R/htsjdk_$LCASE/summary.json"
        if [[ -f "$SUMMARY" ]]; then
            echo "[$(date -u +%H:%M:%S)]   skip $SUMMARY (already exists)"
            continue
        fi
        echo "[$(date -u +%H:%M:%S)]   mutation rep_$R $FMT"
        MSYS_NO_PATHCONV=1 docker run --rm \
            -v "$(pwd):/work" -w /work biotest-bench:latest \
            bash -c "TOOL=jazzer \
                COVERAGE_ROOT=/work/compares/results/coverage/jazzer_4rep \
                OUT_ROOT=/work/compares/results/mutation/jazzer_4rep/rep_$R \
                REPS='$R' FORMATS='$FMT' \
                CORPUS_MAX=100 THREADS=4 MUTATION_UNIT_SIZE=10 \
                bash compares/scripts/phase3_jazzer_pit.sh" \
            > "$LOG_DIR/mut_rep_${R}_${LCASE}.log" 2>&1 || true
    done
done

echo "[$(date -u +%H:%M:%S)] === Done ==="
