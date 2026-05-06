#!/bin/bash
# Strand-based rerun orchestrator. Three parallel strands (E0/E1S/E2)
# spawn run_4rep.py per (config, run_id) group, serializing within strand.
# seqan3 cells share /work/harnesses/cpp/build/*.gcda inside the docker
# container, so seqan3-containing groups across strands serialize via
# `flock` on a shared lock file.
#
# Why bash not Python: the previous Python orchestrator was killed by a
# stray PowerShell Stop-Process and lost state. Bash strands handle
# subprocess lifetimes via wait/exec naturally and are robust to
# intermediate kills (each strand is independent).

set -u
cd "$(dirname "$0")/../.."  # repo root

CHAIN_LOG=compares/ApplicationStudy/chain.log
# Git Bash on Windows lacks `flock`. Use mkdir atomicity instead — only
# one `mkdir DIR` succeeds when multiple processes race; the loser polls
# until the winner releases via rmdir.
SEQAN3_LOCK_DIR=compares/ApplicationStudy/.seqan3.lockdir
STRAND_DIR=compares/ApplicationStudy/strands
mkdir -p "$STRAND_DIR"
rmdir "$SEQAN3_LOCK_DIR" 2>/dev/null || true  # cleanup stale lock

PY=C:/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe
RUN_4REP=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_4rep.py

log() {
  printf '[%s] [chain v4] %s\n' "$(date +%H:%M:%S)" "$1" >> "$CHAIN_LOG"
}

# acquire_seqan3_lock <strand>: blocks until $SEQAN3_LOCK_DIR can be
# created. mkdir is atomic — only one of N racing processes succeeds.
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

# run_group <strand> <config> <run_id> <cumulative> <reps> <out_root> <cell1> [cell2 ...]
# Calls run_4rep.py with --only flags. Locks seqan3 across strands when
# seqan3_sam is in the cells list.
run_group() {
  local strand=$1 config=$2 run_id=$3 cum=$4 reps=$5 out_root=$6
  shift 6
  local cells=("$@")
  local has_seqan3=0
  for c in "${cells[@]}"; do
    [ "$c" = "seqan3_sam" ] && has_seqan3=1
  done

  # Nuke each cell dir on host
  for c in "${cells[@]}"; do
    if [ -d "$out_root/$c" ]; then
      log "[$strand] nuking $out_root/$c"
      rm -rf "$out_root/$c"
    fi
  done

  # Build --only flags
  local only_args=()
  for c in "${cells[@]}"; do
    only_args+=("--only" "$c")
  done

  log "[$strand] launching $config/$run_id cells=${cells[*]} (has_seqan3=$has_seqan3)"
  local t0
  t0=$(date +%s)
  if [ $has_seqan3 -eq 1 ]; then
    acquire_seqan3_lock "$strand"
    "$PY" "$RUN_4REP" \
      --mode "$config" --reps "$reps" --cumulative "$cum" \
      --max-workers 3 --out-root "$out_root" "${only_args[@]}"
    local rc=$?
    release_seqan3_lock "$strand"
  else
    "$PY" "$RUN_4REP" \
      --mode "$config" --reps "$reps" --cumulative "$cum" \
      --max-workers 3 --out-root "$out_root" "${only_args[@]}"
    local rc=$?
  fi
  local elapsed=$(( ($(date +%s) - t0) / 60 ))
  log "[$strand] $config/$run_id done rc=$rc elapsed=${elapsed}min"
}

# ------------- E0 strand -------------
strand_e0() {
  log "[E0] strand start"
  local OUT_ROOT_BASE=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E0_baseline/results_4big_runs
  run_group E0 E0 a true 3 "$OUT_ROOT_BASE/run_a" seqan3_sam
  run_group E0 E0 b true 3 "$OUT_ROOT_BASE/run_b" biopython_sam vcfpy_vcf
  run_group E0 E0 c true 3 "$OUT_ROOT_BASE/run_c" biopython_sam vcfpy_vcf
  run_group E0 E0 d true 3 "$OUT_ROOT_BASE/run_d" biopython_sam vcfpy_vcf
  log "[E0] strand complete"
}

# ------------- E1S strand -------------
strand_e1s() {
  log "[E1S] strand start"
  local OUT_ROOT_BASE=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E1S_strict/results_4big_runs
  run_group E1S E1S b true 3 "$OUT_ROOT_BASE/run_b" htsjdk_sam
  run_group E1S E1S d true 3 "$OUT_ROOT_BASE/run_d" htsjdk_sam htsjdk_vcf
  log "[E1S] strand complete"
}

# ------------- E2 strand -------------
strand_e2() {
  log "[E2] strand start"
  local OUT_ROOT=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E2_no_phase_d/results_4rep
  # E2 layout=reps: all 4 reps live under the same out_root. detect_failures
  # reports each failed cell × 4 (one per rep id), but in run_4rep.py terms
  # it's ONE cascade with --reps 4. So a single invocation suffices.
  run_group E2 E2 reps false 4 "$OUT_ROOT" biopython_sam seqan3_sam vcfpy_vcf
  log "[E2] strand complete"
}

# Launch strands in parallel
log "===== chain v4 launch ====="
strand_e0 > >(tee -a "$STRAND_DIR/e0.log") 2>&1 &
PID_E0=$!
strand_e1s > >(tee -a "$STRAND_DIR/e1s.log") 2>&1 &
PID_E1S=$!
strand_e2 > >(tee -a "$STRAND_DIR/e2.log") 2>&1 &
PID_E2=$!

log "[main] strands launched: E0=$PID_E0 E1S=$PID_E1S E2=$PID_E2"

wait $PID_E0; RC_E0=$?
log "[main] E0 strand exited rc=$RC_E0"
wait $PID_E1S; RC_E1S=$?
log "[main] E1S strand exited rc=$RC_E1S"
wait $PID_E2; RC_E2=$?
log "[main] E2 strand exited rc=$RC_E2"

log "===== all strands done; starting metrics chain ====="

# Mutation + bug_bench + aggregate
log "[main] === MUTATION step ==="
PYTHONIOENCODING=utf-8 "$PY" compares/ApplicationStudy/run_metrics_4rep.py \
  --config ALL --step mutation --mutation-budget-s 1800 \
  >> "$CHAIN_LOG" 2>&1
log "[main] mutation done rc=$?"

log "[main] === BUG_BENCH step ==="
PYTHONIOENCODING=utf-8 "$PY" compares/ApplicationStudy/run_metrics_4rep.py \
  --config ALL --step bug_bench --bug-bench-budget-s 600 \
  >> "$CHAIN_LOG" 2>&1
log "[main] bug_bench done rc=$?"

log "[main] === AGGREGATE step ==="
PYTHONIOENCODING=utf-8 "$PY" compares/ApplicationStudy/aggregate_4rep.py \
  >> "$CHAIN_LOG" 2>&1
log "[main] aggregate done rc=$?"

log "===== chain v4 ALL DONE ====="
echo "===CHAIN V4 DONE===" >> "$CHAIN_LOG"
