#!/bin/bash
# E3 (no Phase A + no Phase D) chain — runs in parallel with v4b.
#
# Isolation guarantees vs running v4b (chain_v4b):
#   * Output dir: compares/ApplicationStudy/E3_no_a_no_d/results_4rep/
#     — completely disjoint from E0/E1S/E2 output dirs.
#   * Log file: chain_e3.log (NOT chain.log).
#   * SEQAN3_LOCK: SAME .seqan3.lockdir as v4b. E3's seqan3 cell will
#     serialize with v4b's E0/E2 seqan3 cells via mkdir-based mutex.
#     No .gcda contamination inside the docker container.
#   * Mutation/bug_bench: idempotent — run_metrics_4rep.py skips cells
#     whose summary.json already exists, so re-running with --config ALL
#     after E3 done only fills in E3 entries.
#   * No edits to v4b processes' loaded code: my run_4rep.py / harness_run.py
#     edits are additive only (E3 mode in choices, MODE in ("E2","E3"));
#     v4b's E0/E1S/E2 modes hit the same branches as before.

set -u
cd "$(dirname "$0")/../.."  # repo root

CHAIN_LOG=compares/ApplicationStudy/chain_e3.log
SEQAN3_LOCK_DIR=compares/ApplicationStudy/.seqan3.lockdir
PY=C:/Users/miaot/AppData/Local/Programs/Python/Python312/python.exe
RUN_4REP=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_4rep.py
RERUN_PARALLEL=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/rerun_failed_parallel.py
RUN_METRICS=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/run_metrics_4rep.py
AGG=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/aggregate_4rep.py

E3_OUT=C:/Users/miaot/Github/BioTest/compares/ApplicationStudy/E3_no_a_no_d/results_4rep

log() {
  printf '[%s] [chain e3] %s\n' "$(date +%H:%M:%S)" "$1" >> "$CHAIN_LOG"
}

acquire_seqan3_lock() {
  local waited=0
  until mkdir "$SEQAN3_LOCK_DIR" 2>/dev/null; do
    sleep 5
    waited=$((waited + 5))
    if [ $((waited % 60)) -eq 0 ]; then
      log "still waiting for SEQAN3_LOCK (${waited}s) — v4b's E0/E2 may be holding"
    fi
  done
  log "acquired SEQAN3_LOCK"
}

release_seqan3_lock() {
  rmdir "$SEQAN3_LOCK_DIR" 2>/dev/null
  log "released SEQAN3_LOCK"
}

# --- Phase 1: E3 main run (1 group, 3 cells × 4 reps, layout=reps) ---
log "===== chain E3 launch ====="
log "Phase 1: E3 main run for biopython_sam + seqan3_sam + vcfpy_vcf"

# Nuke any prior E3 cell dirs
for cell in biopython_sam seqan3_sam vcfpy_vcf; do
  if [ -d "$E3_OUT/$cell" ]; then
    log "nuking $E3_OUT/$cell"
    rm -rf "$E3_OUT/$cell"
  fi
done

# E3 has seqan3_sam → must hold SEQAN3_LOCK for the duration of the cascade.
# The lock is shared with v4b's E0/E2 strands — this E3 strand will wait
# in line behind them.
acquire_seqan3_lock
t0=$(date +%s)
"$PY" "$RUN_4REP" \
  --mode E3 --reps 4 --cumulative false \
  --max-workers 3 --out-root "$E3_OUT" \
  --only biopython_sam --only seqan3_sam --only vcfpy_vcf \
  >> "$CHAIN_LOG" 2>&1
RC_MAIN=$?
elapsed=$(( ($(date +%s) - t0) / 60 ))
log "Phase 1 main run done rc=$RC_MAIN elapsed=${elapsed}min"
release_seqan3_lock

# --- Phase 2: failure detection + reruns (max 2 passes) ---
# Use rerun_failed_parallel.py but invoke it once per pass with config=E3
# only. Since rerun_failed_parallel.py runs all configs in parallel by
# default, we'd accidentally rerun E0/E1S/E2 too. Instead we do detection
# manually and rerun only E3 groups in this script.
log "Phase 2: E3-only failure detection + reruns (max 2 passes)"
for pass in 1 2; do
  # Detect E3 failures
  failures_count=$("$PY" -c "
import sys, os, json
sys.path.insert(0, r'C:\Users\miaot\Github\BioTest\compares\ApplicationStudy')
from rerun_failed_parallel import CONFIGS
PROJECT_ROOT = r'C:\Users\miaot\Github\BioTest'
cfg = CONFIGS['E3']
n_failed = 0
failed_cells = set()
for cell in ['htsjdk_vcf','vcfpy_vcf','noodles_vcf','htsjdk_sam','biopython_sam','seqan3_sam']:
    base = os.path.join(PROJECT_ROOT, 'compares', 'ApplicationStudy', cfg['sub'], 'results_4rep', cell)
    n_ok = 0
    for r in range(cfg['reps']):
        p = os.path.join(base, f'run_{r}', 'measurement.json')
        if os.path.exists(p):
            try:
                d = json.loads(open(p).read())
                if d.get('status') == 'ok' and d.get('total', 0) > 0:
                    n_ok += 1
            except Exception:
                pass
    if n_ok < cfg['reps']:
        n_failed += 1
        failed_cells.add(cell)
print(n_failed)
print(' '.join(sorted(failed_cells)))
")
  n_fail=$(echo "$failures_count" | head -1)
  cells=$(echo "$failures_count" | tail -1)
  log "pass $pass: detected $n_fail failed cells: $cells"
  if [ "$n_fail" = "0" ]; then
    log "E3 all cells full — done"
    break
  fi

  # Build --only flags
  only_args=()
  for c in $cells; do
    only_args+=("--only" "$c")
    if [ -d "$E3_OUT/$c" ]; then
      log "nuking $E3_OUT/$c"
      rm -rf "$E3_OUT/$c"
    fi
  done

  # Need lock if seqan3_sam is in the failed set
  has_seqan3=0
  for c in $cells; do
    [ "$c" = "seqan3_sam" ] && has_seqan3=1
  done

  if [ $has_seqan3 -eq 1 ]; then
    acquire_seqan3_lock
  fi
  t0=$(date +%s)
  "$PY" "$RUN_4REP" \
    --mode E3 --reps 4 --cumulative false \
    --max-workers 3 --out-root "$E3_OUT" \
    "${only_args[@]}" \
    >> "$CHAIN_LOG" 2>&1
  RC_PASS=$?
  elapsed=$(( ($(date +%s) - t0) / 60 ))
  log "pass $pass rerun done rc=$RC_PASS elapsed=${elapsed}min"
  if [ $has_seqan3 -eq 1 ]; then
    release_seqan3_lock
  fi
done

# --- Phase 3: wait for v4b to finish (===CHAIN V4 DONE=== marker) ---
log "Phase 3: waiting for v4b chain to finish (===CHAIN V4 DONE===)"
DEADLINE=$(($(date +%s) + 86400))  # 24 h hard cap
while true; do
  if grep -q "===CHAIN V4 DONE===" compares/ApplicationStudy/chain.log 2>/dev/null; then
    log "v4b done — proceeding to metrics"
    break
  fi
  if [ "$(date +%s)" -gt "$DEADLINE" ]; then
    log "WARNING: v4b deadline hit (24h) — proceeding anyway with available data"
    break
  fi
  sleep 300
done

# --- Phase 4: mutation + bug_bench + aggregate (idempotent skips) ---
# Run with --config ALL. run_metrics_4rep.py:127 skips cells whose
# summary.json already exists, so v4b's E0/E1S/E2 entries are NOT
# redone. Only E3 (and any v4b stragglers) get run here.
log "Phase 4: mutation step (idempotent — only E3 will run)"
PYTHONIOENCODING=utf-8 "$PY" "$RUN_METRICS" \
  --config ALL --step mutation --mutation-budget-s 1800 \
  >> "$CHAIN_LOG" 2>&1
log "mutation rc=$?"

log "Phase 4: bug_bench step (idempotent)"
PYTHONIOENCODING=utf-8 "$PY" "$RUN_METRICS" \
  --config ALL --step bug_bench --bug-bench-budget-s 600 \
  >> "$CHAIN_LOG" 2>&1
log "bug_bench rc=$?"

log "Phase 4: aggregate (now includes E3)"
PYTHONIOENCODING=utf-8 "$PY" "$AGG" \
  >> "$CHAIN_LOG" 2>&1
log "aggregate rc=$?"

log "===== chain E3 ALL DONE ====="
echo "===CHAIN E3 DONE===" >> "$CHAIN_LOG"
