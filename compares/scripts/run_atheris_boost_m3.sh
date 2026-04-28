#!/usr/bin/env bash
# Atheris × vcfpy M3 boost — reps 4..9.
# Per existing 4-run regime (compares/results/mutation/atheris/vcfpy_runs/),
# atheris coverage uses 7200 s budget per rep; mutmut on the per-rep corpus
# typically takes ~17 min. Total per-rep wall: ~135 min. 6 reps ~13.5 hours.
#
# To match the existing 4-run methodology exactly, this script keeps
# 7200 s per rep. If the campaign does not fit a single compute envelope,
# launch reps individually (REPS env override).
set -euo pipefail
cd "$(dirname "$0")/../.."

REPS="${REPS:-4 5 6 7 8 9}"
LOG_DIR="compares/results/mutation/biotest/m3_boost_logs/atheris"
mkdir -p "$LOG_DIR"

echo "[$(date -u +%H:%M:%S)] === Atheris × vcfpy boost (REPS=$REPS) ==="
for R in $REPS; do
    SEED=$((R*1000 + 42))
    COV_OUT="compares/results/coverage/atheris/vcfpy/run_$R"
    MUT_OUT="compares/results/mutation/atheris/vcfpy_runs/run_$R"
    GROWTH="$COV_OUT/growth_0.json"
    SUMMARY="$MUT_OUT/summary.json"

    if [[ -f "$GROWTH" ]]; then
        echo "[$(date -u +%H:%M:%S)]   skip rep_$R coverage ($GROWTH exists)"
    else
        echo "[$(date -u +%H:%M:%S)]   rep_$R: atheris coverage (budget=7200)"
        # coverage_sampler.py for atheris uses docker subprocess internally
        # (biotest-bench:latest atheris-venv); must run on host, not inside Docker.
        MSYS_NO_PATHCONV=1 py -3.12 compares/scripts/coverage_sampler.py \
            --tool atheris --sut vcfpy --format VCF \
            --seed-corpus compares/results/bench_seeds/vcf \
            --budget 7200 --reps 1 \
            --out "$COV_OUT" \
            > "$LOG_DIR/cov_rep_${R}.log" 2>&1
    fi

    if [[ -f "$SUMMARY" ]]; then
        echo "[$(date -u +%H:%M:%S)]   skip rep_$R mutmut ($SUMMARY exists)"
    else
        echo "[$(date -u +%H:%M:%S)]   rep_$R: mutmut on per-rep corpus"
        # coverage_sampler --reps 1 --out X writes corpus to X/run_0/corpus.
        # PYTHONIOENCODING=utf-8 to handle mutation_driver.py's Unicode arrows.
        PYTHONIOENCODING=utf-8 py -3.12 compares/scripts/mutation_driver.py \
            --tool atheris --sut vcfpy \
            --corpus "$COV_OUT/run_0/corpus" \
            --out "$MUT_OUT" \
            --budget 1800 --corpus-sample 40 \
            > "$LOG_DIR/mut_rep_${R}.log" 2>&1 || true
    fi
done

echo "[$(date -u +%H:%M:%S)] === Done ==="
