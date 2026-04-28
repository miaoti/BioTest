#!/usr/bin/env bash
# Quick status snapshot of the M3 boost runs.
set -uo pipefail
cd "$(dirname "$0")/../.."

echo "=== BioTest reps 4..9 (per-cell summary.json count) ==="
for cell in htsjdk_vcf htsjdk_sam vcfpy noodles; do
    n=0
    for r in 0 1 2 3 4 5 6 7 8 9; do
        if [[ -f "compares/results/mutation/biotest_run1_rep_$r/$cell/summary.json" ]]; then
            n=$((n+1))
        fi
    done
    echo "  $cell: $n/10"
done

echo
echo "=== Jazzer reps 4..9 (per-format summary.json count) ==="
for fmt in vcf sam; do
    n=0
    for r in 0 1 2 3 4 5 6 7 8 9; do
        if [[ -f "compares/results/mutation/jazzer_4rep/rep_$r/htsjdk_$fmt/summary.json" ]]; then
            n=$((n+1))
        fi
    done
    echo "  htsjdk_$fmt: $n/10"
done

echo
echo "=== Atheris × vcfpy (run_*/summary.json count) ==="
n=0
for r in 0 1 2 3 4 5 6 7 8 9; do
    if [[ -f "compares/results/mutation/atheris/vcfpy_runs/run_$r/summary.json" ]]; then
        n=$((n+1))
    fi
done
echo "  vcfpy: $n/10"

echo
echo "=== cargo-fuzz × noodles (run_*/summary.json count) ==="
n=0
for r in 01 02 03 04 05 06 07 08 09 10; do
    if [[ -f "compares/results/mutation/cargo_fuzz/noodles/run_$r/summary.json" ]]; then
        n=$((n+1))
    fi
done
echo "  noodles: $n/10"
