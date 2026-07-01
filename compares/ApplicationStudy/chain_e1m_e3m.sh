#!/bin/bash
# E1M + E3M chain — TRUE-PARALLEL variant.
#
# Each strand splits its run into two concurrent groups per cascade:
#   * NON-SEQAN3 group (5 cells, no lock): htsjdk_vcf, vcfpy_vcf, noodles_vcf,
#     htsjdk_sam, biopython_sam — run with --max-workers 5.
#   * SEQAN3 group (1 cell, lock-protected): seqan3_sam — runs under
#     SEQAN3_LOCK because all seqan3 runs share /work/harnesses/cpp/build/*.gcda
#     inside the docker container.
#
# Result: E1M's 5 non-seqan3 cells AND E3M's 5 non-seqan3 cells run in parallel
# (10 concurrent biotest cells), while E1M's seqan3 + E3M's seqan3 serialize via
# the shared lock. Wall time roughly halved versus the serial-strand variant.
#
# Output dirs disjoint: E1M_medium/ and E3M_medium/. Same SEQAN3_LOCK as
# postfix/v4/e3 chains for cross-chain seqan3 isolation.

set -u
cd "$(dirname "$0")/../.."  # repo root

CHAIN_LOG=compares/ApplicationStudy/chain_e1m_e3m.log
SEQAN3_LOCK_DIR=compares/ApplicationStudy/.seqan3.lockdir
STRAND_DIR=compares/ApplicationStudy/strands_e1m_e3m
mkdir -p "$STRAND_DIR"
rmdir "$SEQAN3_LOCK_DIR" 2>/dev/null || true  # cleanup any stale lock from prior aborts

PY=C:/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe
RUN_4REP=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_4rep.py
RUN_METRICS=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_metrics_4rep.py
AGG=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/aggregate_4rep.py

E1M_OUT_BASE=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E1M_medium/results_4big_runs
E3M_OUT=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E3M_medium/results_4rep

NON_SEQAN3_FLAGS="--only htsjdk_vcf --only vcfpy_vcf --only noodles_vcf --only htsjdk_sam --only biopython_sam"
SEQAN3_FLAGS="--only seqan3_sam"

log() {
  printf '[%s] [chain e1m+e3m] %s\n' "$(date +%H:%M:%S)" "$1" >> "$CHAIN_LOG"
}

acquire_seqan3_lock() {
  local strand=$1
  local waited=0
  until mkdir "$SEQAN3_LOCK_DIR" 2>/dev/null; do
    sleep 5
    waited=$((waited + 5))
    if [ $((waited % 60)) -eq 0 ]; then
      log "[$strand] still waiting for SEQAN3_LOCK (${waited}s)"
    fi
  done
  log "[$strand] acquired SEQAN3_LOCK"
}

release_seqan3_lock() {
  local strand=$1
  rmdir "$SEQAN3_LOCK_DIR" 2>/dev/null
  log "[$strand] released SEQAN3_LOCK"
}

# ------------- E1M strand -------------
# 4 sequential big runs (a, b, c, d). Each big run launches non-seqan3 (5 cells)
# and seqan3_sam concurrently inside the same out_root. The seqan3 invocation
# holds the lock; non-seqan3 does not. Both run_4rep.py invocations write to
# disjoint per-cell sub-dirs of $out, so no host-side race; container .gcda
# race is prevented by the lock.
strand_e1m() {
  log "[E1M] strand start"
  for run_id in a b c d; do
    local out="$E1M_OUT_BASE/run_$run_id"
    if [ -d "$out" ]; then
      log "[E1M] nuking $out"
      rm -rf "$out"
    fi
    mkdir -p "$out"

    log "[E1M/run_$run_id] launching non-seqan3 (5 cells, no lock) + seqan3 (locked) in parallel"
    local t0=$(date +%s)

    # Non-seqan3 group (no lock, 5 cells parallel)
    "$PY" "$RUN_4REP" \
      --mode E1M --reps 3 --cumulative true \
      --max-workers 5 --out-root "$out" \
      $NON_SEQAN3_FLAGS \
      > "$STRAND_DIR/e1m_run_${run_id}_nonseqan3.log" 2>&1 &
    local PID_NS=$!

    # seqan3_sam group (locked)
    (
      acquire_seqan3_lock "E1M/run_$run_id/seqan3"
      "$PY" "$RUN_4REP" \
        --mode E1M --reps 3 --cumulative true \
        --max-workers 1 --out-root "$out" \
        $SEQAN3_FLAGS \
        > "$STRAND_DIR/e1m_run_${run_id}_seqan3.log" 2>&1
      release_seqan3_lock "E1M/run_$run_id/seqan3"
    ) &
    local PID_S=$!

    wait $PID_NS; local rc_ns=$?
    wait $PID_S;  local rc_s=$?
    local elapsed=$(( ($(date +%s) - t0) / 60 ))
    log "[E1M/run_$run_id] done — non-seqan3 rc=$rc_ns seqan3 rc=$rc_s elapsed=${elapsed}min"
  done
  log "[E1M] strand complete"
}

# ------------- E3M strand -------------
# Single run_4rep call covers all 4 reps (cumulative=false). Same split:
# non-seqan3 5 cells parallel without lock, seqan3 1 cell under lock.
strand_e3m() {
  log "[E3M] strand start"
  if [ -d "$E3M_OUT" ]; then
    log "[E3M] nuking $E3M_OUT"
    rm -rf "$E3M_OUT"
  fi
  mkdir -p "$E3M_OUT"

  log "[E3M] launching non-seqan3 (5 cells, no lock) + seqan3 (locked) in parallel"
  local t0=$(date +%s)

  # Non-seqan3 group
  "$PY" "$RUN_4REP" \
    --mode E3M --reps 4 --cumulative false \
    --max-workers 5 --out-root "$E3M_OUT" \
    $NON_SEQAN3_FLAGS \
    > "$STRAND_DIR/e3m_nonseqan3.log" 2>&1 &
  local PID_NS=$!

  # seqan3 group
  (
    acquire_seqan3_lock "E3M/seqan3"
    "$PY" "$RUN_4REP" \
      --mode E3M --reps 4 --cumulative false \
      --max-workers 1 --out-root "$E3M_OUT" \
      $SEQAN3_FLAGS \
      > "$STRAND_DIR/e3m_seqan3.log" 2>&1
    release_seqan3_lock "E3M/seqan3"
  ) &
  local PID_S=$!

  wait $PID_NS; local rc_ns=$?
  wait $PID_S;  local rc_s=$?
  local elapsed=$(( ($(date +%s) - t0) / 60 ))
  log "[E3M] done — non-seqan3 rc=$rc_ns seqan3 rc=$rc_s elapsed=${elapsed}min"

  # Type-3 zero rerun pass (E3M only)
  log "[E3M] failure detection + 1 rerun pass for type-3 zeros"
  local failures_count
  failures_count=$("$PY" -c "
import sys, os
sys.path.insert(0, r'C:\Users\miaot\Github\BioTest\compares\ApplicationStudy')
from rerun_failed_parallel import CONFIGS
PROJECT_ROOT = r'C:\Users\miaot\Github\BioTest'
cfg = CONFIGS['E3M']
n_failed = 0
failed_cells = set()
for cell in ['htsjdk_vcf','vcfpy_vcf','noodles_vcf','htsjdk_sam','biopython_sam','seqan3_sam']:
    base = os.path.join(PROJECT_ROOT, 'compares', 'ApplicationStudy', cfg['sub'], 'results_4rep', cell)
    n_missing_file = 0
    for r in range(cfg['reps']):
        p = os.path.join(base, f'run_{r}', 'measurement.json')
        if not os.path.exists(p):
            n_missing_file += 1
    if n_missing_file > 0:
        n_failed += 1
        failed_cells.add(cell)
print(n_failed)
print(' '.join(sorted(failed_cells)))
")
  local n_fail=$(echo "$failures_count" | head -1)
  local cells=$(echo "$failures_count" | tail -1)
  log "[E3M] type-3 detected: $n_fail cells: $cells"
  if [ "$n_fail" != "0" ]; then
    local non_seqan3_only=()
    local has_seqan3=0
    for c in $cells; do
      if [ "$c" = "seqan3_sam" ]; then
        has_seqan3=1
      else
        non_seqan3_only+=("--only" "$c")
      fi
      if [ -d "$E3M_OUT/$c" ]; then
        log "[E3M-rerun] nuking $E3M_OUT/$c"
        rm -rf "$E3M_OUT/$c"
      fi
    done

    local rerun_pids=()
    if [ ${#non_seqan3_only[@]} -gt 0 ]; then
      "$PY" "$RUN_4REP" \
        --mode E3M --reps 4 --cumulative false \
        --max-workers 5 --out-root "$E3M_OUT" \
        "${non_seqan3_only[@]}" \
        >> "$STRAND_DIR/e3m_nonseqan3.log" 2>&1 &
      rerun_pids+=($!)
    fi
    if [ $has_seqan3 -eq 1 ]; then
      (
        acquire_seqan3_lock "E3M-rerun/seqan3"
        "$PY" "$RUN_4REP" \
          --mode E3M --reps 4 --cumulative false \
          --max-workers 1 --out-root "$E3M_OUT" \
          --only seqan3_sam \
          >> "$STRAND_DIR/e3m_seqan3.log" 2>&1
        release_seqan3_lock "E3M-rerun/seqan3"
      ) &
      rerun_pids+=($!)
    fi
    for pid in "${rerun_pids[@]}"; do wait $pid; done
    log "[E3M] type-3 rerun done"
  fi
  log "[E3M] strand complete"
}

# ------------- Launch -------------
log "===== chain e1m+e3m TRUE-PARALLEL launch ====="
strand_e1m > >(tee -a "$STRAND_DIR/e1m.log") 2>&1 &
PID_E1M=$!
strand_e3m > >(tee -a "$STRAND_DIR/e3m.log") 2>&1 &
PID_E3M=$!

log "[main] strands launched: E1M=$PID_E1M E3M=$PID_E3M"

wait $PID_E1M; RC_E1M=$?
log "[main] E1M strand exited rc=$RC_E1M"
wait $PID_E3M; RC_E3M=$?
log "[main] E3M strand exited rc=$RC_E3M"

log "===== both strands done; starting metrics chain ====="

# E1M type-3 failure detection + 1 rerun pass (big_runs layout)
log "[main] E1M failure detection + 1 rerun pass for type-3 zeros"
e1m_failures=$("$PY" -c "
import sys, os
sys.path.insert(0, r'C:\Users\miaot\Github\BioTest\compares\ApplicationStudy')
from rerun_failed_parallel import CONFIGS
PROJECT_ROOT = r'C:\Users\miaot\Github\BioTest'
cfg = CONFIGS['E1M']
groups = []
for run_id in cfg['ids']:
    failed_cells = set()
    for cell in ['htsjdk_vcf','vcfpy_vcf','noodles_vcf','htsjdk_sam','biopython_sam','seqan3_sam']:
        base = os.path.join(PROJECT_ROOT, 'compares', 'ApplicationStudy', cfg['sub'], 'results_4big_runs', f'run_{run_id}', cell)
        n_missing_file = 0
        for r in range(cfg['reps']):
            p = os.path.join(base, f'run_{r}', 'measurement.json')
            if not os.path.exists(p):
                n_missing_file += 1
        if n_missing_file > 0:
            failed_cells.add(cell)
    if failed_cells:
        groups.append((run_id, sorted(failed_cells)))
for run_id, cells in groups:
    print(run_id + '|' + ','.join(cells))
")
if [ -n "$e1m_failures" ]; then
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    run_id="${line%|*}"
    cells_csv="${line#*|}"
    IFS=',' read -ra cells_arr <<< "$cells_csv"
    non_seqan3_only=()
    has_seqan3=0
    for c in "${cells_arr[@]}"; do
      if [ "$c" = "seqan3_sam" ]; then
        has_seqan3=1
      else
        non_seqan3_only+=("--only" "$c")
      fi
      if [ -d "$E1M_OUT_BASE/run_$run_id/$c" ]; then
        log "[E1M-rerun] nuking $E1M_OUT_BASE/run_$run_id/$c"
        rm -rf "$E1M_OUT_BASE/run_$run_id/$c"
      fi
    done
    log "[E1M-rerun] run_$run_id cells=${cells_arr[*]} (has_seqan3=$has_seqan3)"

    rerun_pids=()
    if [ ${#non_seqan3_only[@]} -gt 0 ]; then
      "$PY" "$RUN_4REP" \
        --mode E1M --reps 3 --cumulative true \
        --max-workers 5 --out-root "$E1M_OUT_BASE/run_$run_id" \
        "${non_seqan3_only[@]}" \
        >> "$STRAND_DIR/e1m_run_${run_id}_nonseqan3.log" 2>&1 &
      rerun_pids+=($!)
    fi
    if [ $has_seqan3 -eq 1 ]; then
      (
        acquire_seqan3_lock "E1M-rerun/run_$run_id/seqan3"
        "$PY" "$RUN_4REP" \
          --mode E1M --reps 3 --cumulative true \
          --max-workers 1 --out-root "$E1M_OUT_BASE/run_$run_id" \
          --only seqan3_sam \
          >> "$STRAND_DIR/e1m_run_${run_id}_seqan3.log" 2>&1
        release_seqan3_lock "E1M-rerun/run_$run_id/seqan3"
      ) &
      rerun_pids+=($!)
    fi
    for pid in "${rerun_pids[@]}"; do wait $pid; done
    log "[E1M-rerun] run_$run_id done"
  done <<< "$e1m_failures"
fi

log "[main] === MUTATION step (idempotent — only E1M+E3M will run) ==="
PYTHONIOENCODING=utf-8 "$PY" "$RUN_METRICS" \
  --config ALL --step mutation --mutation-budget-s 1800 \
  >> "$CHAIN_LOG" 2>&1
log "[main] mutation rc=$?"

log "[main] === BUG_BENCH step ==="
PYTHONIOENCODING=utf-8 "$PY" "$RUN_METRICS" \
  --config ALL --step bug_bench --bug-bench-budget-s 600 \
  >> "$CHAIN_LOG" 2>&1
log "[main] bug_bench rc=$?"

log "[main] === AGGREGATE step (now includes E1M + E3M) ==="
PYTHONIOENCODING=utf-8 "$PY" "$AGG" \
  >> "$CHAIN_LOG" 2>&1
log "[main] aggregate rc=$?"

log "===== chain e1m+e3m ALL DONE ====="
echo "===CHAIN E1M+E3M DONE===" >> "$CHAIN_LOG"
