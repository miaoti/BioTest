#!/bin/bash
# Parallel-with-mutation reruns. Three rerun strands fire IMMEDIATELY in
# parallel with each other AND with v4b's mutation step. After all three
# strands finish AND v4b emits ===CHAIN V4 DONE===, invalidate stale
# results_metrics summaries for the rerun cells and re-run mutation +
# bug_bench + aggregate to refresh.
#
# Why no resource conflict with v4b mutation:
#   - Reruns and mutation use disjoint working dirs (results_4*/run_*/
#     vs results_metrics/*/cell/).
#   - No seqan3 cells in the rerun list → SEQAN3_LOCK never contested.
#   - htsjdk/noodles run via `docker exec` — multiple parallel exec
#     against same container is fine; each spawns a separate process.
#   - host cells (biopython, vcfpy) use coverage.py per-cell .coverage
#     paths — no shared file.
# Risk: Windows host RAM. 5-7 parallel pythons should fit on a typical
# dev machine. Watch chain_postfix.log for OOM.

set -u
cd "$(dirname "$0")/../.."

CHAIN_LOG=compares/ApplicationStudy/chain_postfix.log
SEQAN3_LOCK_DIR=compares/ApplicationStudy/.seqan3.lockdir
PY=C:/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe
RUN_4REP=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_4rep.py
RUN_METRICS=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_metrics_4rep.py
AGG=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/aggregate_4rep.py

E0_OUT_BASE=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E0_baseline/results_4big_runs
E1S_OUT_BASE=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E1S_strict/results_4big_runs
E3_OUT=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E3_no_a_no_d/results_4rep
E0_METRICS=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E0_baseline/results_metrics
E1S_METRICS=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E1S_strict/results_metrics
E3_METRICS=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E3_no_a_no_d/results_metrics

mkdir -p compares/ApplicationStudy/postfix_strands

log() {
  printf '[%s] [postfix] %s\n' "$(date +%H:%M:%S)" "$1" >> "$CHAIN_LOG"
}

# Strand 1: E0/run_b biopython (3 reps cumulative=True, ~4.5h)
strand_e0() {
  local strand_log=compares/ApplicationStudy/postfix_strands/e0.log
  log "[E0] strand start"
  rm -rf "$E0_OUT_BASE/run_b/biopython_sam"
  "$PY" "$RUN_4REP" \
    --mode E0 --reps 3 --cumulative true \
    --max-workers 1 --out-root "$E0_OUT_BASE/run_b" \
    --only biopython_sam \
    > "$strand_log" 2>&1
  log "[E0] strand done rc=$?"
}

# Strand 2: E1S/run_b/htsjdk_sam THEN E1S/run_d/htsjdk_{vcf,sam}
strand_e1s() {
  local strand_log=compares/ApplicationStudy/postfix_strands/e1s.log
  log "[E1S] strand start"
  rm -rf "$E1S_OUT_BASE/run_b/htsjdk_sam"
  "$PY" "$RUN_4REP" \
    --mode E1S --reps 3 --cumulative true \
    --max-workers 1 --out-root "$E1S_OUT_BASE/run_b" \
    --only htsjdk_sam \
    >> "$strand_log" 2>&1
  log "[E1S] run_b/htsjdk_sam rc=$?"

  rm -rf "$E1S_OUT_BASE/run_d/htsjdk_vcf"
  rm -rf "$E1S_OUT_BASE/run_d/htsjdk_sam"
  "$PY" "$RUN_4REP" \
    --mode E1S --reps 3 --cumulative true \
    --max-workers 2 --out-root "$E1S_OUT_BASE/run_d" \
    --only htsjdk_vcf --only htsjdk_sam \
    >> "$strand_log" 2>&1
  log "[E1S] run_d/htsjdk_{vcf,sam} rc=$?"
  log "[E1S] strand done"
}

# Strand 3: E3 htsjdk_vcf + noodles_vcf + htsjdk_sam (4 reps cumulative=False)
strand_e3() {
  local strand_log=compares/ApplicationStudy/postfix_strands/e3.log
  log "[E3] strand start"
  rm -rf "$E3_OUT/htsjdk_vcf"
  rm -rf "$E3_OUT/noodles_vcf"
  rm -rf "$E3_OUT/htsjdk_sam"
  "$PY" "$RUN_4REP" \
    --mode E3 --reps 4 --cumulative false \
    --max-workers 3 --out-root "$E3_OUT" \
    --only htsjdk_vcf --only noodles_vcf --only htsjdk_sam \
    > "$strand_log" 2>&1
  log "[E3] strand done rc=$?"
}

log "===== chain_postfix start (parallel with v4b mutation) ====="

strand_e0 &
PID_E0=$!
strand_e1s &
PID_E1S=$!
strand_e3 &
PID_E3=$!
log "strands launched: E0=$PID_E0 E1S=$PID_E1S E3=$PID_E3"

wait $PID_E0; log "E0 strand wait done rc=$?"
wait $PID_E1S; log "E1S strand wait done rc=$?"
wait $PID_E3; log "E3 strand wait done rc=$?"

log "all rerun strands done; waiting for ===CHAIN V4 DONE=== before re-mutation"
DEADLINE=$(($(date +%s) + 86400))
while true; do
  v4_done=0
  e3_done=0
  grep -q "===CHAIN V4 DONE===" compares/ApplicationStudy/chain.log 2>/dev/null && v4_done=1
  grep -q "===CHAIN E3 DONE===" compares/ApplicationStudy/chain_e3.log 2>/dev/null && e3_done=1
  if [ $v4_done -eq 1 ] && [ $e3_done -eq 1 ]; then
    log "both chains done — proceeding to refresh metrics"
    break
  fi
  if [ "$(date +%s)" -gt "$DEADLINE" ]; then
    log "WARNING: 24h cap hit — proceeding anyway"
    break
  fi
  sleep 300
done

# Invalidate stale results_metrics for cells that were rerun (mutation +
# bug_bench need rebuild from new corpus).
log "invalidating stale results_metrics for rerun cells"
rm -rf "$E0_METRICS/b/biopython_sam"
rm -rf "$E1S_METRICS/b/htsjdk_sam"
rm -rf "$E1S_METRICS/d/htsjdk_vcf"
rm -rf "$E1S_METRICS/d/htsjdk_sam"
for run_id in 0 1 2 3; do
  rm -rf "$E3_METRICS/$run_id/htsjdk_vcf"
  rm -rf "$E3_METRICS/$run_id/noodles_vcf"
  rm -rf "$E3_METRICS/$run_id/htsjdk_sam"
done
# bug_bench depends on htsjdk corpora — invalidate where applicable
rm -rf "$E1S_METRICS/b/bug_bench"
rm -rf "$E1S_METRICS/d/bug_bench"
for run_id in 0 1 2 3; do
  rm -rf "$E3_METRICS/$run_id/bug_bench"
done

log "re-running mutation step (idempotent — fills only invalidated cells)"
PYTHONIOENCODING=utf-8 "$PY" "$RUN_METRICS" \
  --config ALL --step mutation --mutation-budget-s 1800 \
  >> "$CHAIN_LOG" 2>&1
log "mutation rc=$?"

log "re-running bug_bench step"
PYTHONIOENCODING=utf-8 "$PY" "$RUN_METRICS" \
  --config ALL --step bug_bench --bug-bench-budget-s 600 \
  >> "$CHAIN_LOG" 2>&1
log "bug_bench rc=$?"

log "re-running aggregate"
PYTHONIOENCODING=utf-8 "$PY" "$AGG" >> "$CHAIN_LOG" 2>&1
log "aggregate rc=$?"

log "===== chain_postfix DONE ====="
echo "===CHAIN POSTFIX DONE===" >> "$CHAIN_LOG"
