#!/usr/bin/env bash
# Chat 5 retry pass v3 — adaptive backoff for 5 skipped cells.
#
# Strategy: waits for container quiet (fewer than 3 concurrent bench
# drivers AND >2 GiB MemAvailable) before each attempt, then fires one
# shot. Up to 25 attempts per cell, 120 s fallback backoff.
#
# Cells to recover (the rev-parse driver patch for "edbfa956f^" has
# already landed):
#   pure_random biopython-4825  (OOM during pip install)
#   pure_random seqan3-3098     (OOM during git checkout)
#   pure_random seqan3-2869     (rev-spec + OOM)
#   pure_random seqan3-3406     (OOM during git read-object)
#   libfuzzer   seqan3-2869     (rev-spec)
set -u
export PATH=/root/.cargo/bin:$PATH
cd /work

LOG=/tmp/phase4-chat5.log
OUT=/tmp/bug_bench_chat5
BUDGET_S=${BUDGET_S:-300}
export BUDGET_S
MAX_TRIES=25

echo "[chat5] RETRY-v3 start $(date -u +%FT%TZ)" >> "$LOG"

wait_for_quiet() {
  local spins=0
  while [ $spins -lt 20 ]; do
    local nconc
    nconc=$(pgrep -c -f "bug_bench_driver.py" 2>/dev/null || echo 99)
    local memfree_mb
    memfree_mb=$(awk "/^MemAvailable/ {print int(\$2/1024); exit}" /proc/meminfo 2>/dev/null || echo 0)
    if [ "${nconc:-99}" -le 2 ] && [ "${memfree_mb:-0}" -gt 2000 ]; then
      return 0
    fi
    sleep 90
    spins=$((spins+1))
  done
  return 0
}

retry_cell() {
  local tool=$1
  local bug=$2
  local tries=0
  while [ $tries -lt $MAX_TRIES ]; do
    tries=$((tries+1))
    if [ -f "$OUT/${tool}/${bug}/result.json" ]; then
      echo "[chat5-retry-v3] SKIP (already present) tool=${tool} bug=${bug}" >> "$LOG"
      return 0
    fi
    wait_for_quiet
    echo "[chat5-retry-v3] tool=${tool} bug=${bug} attempt=${tries} $(date -u +%FT%TZ)" >> "$LOG"
    rm -rf "$OUT/${tool}/${bug}"
    if python3.12 compares/scripts/bug_bench_driver.py \
         --manifest compares/bug_bench/manifest.verified.json \
         --only-bug "$bug" --only-tool "$tool" \
         --time-budget-s ${BUDGET_S} \
         --out "$OUT" >> "$LOG" 2>&1; then
      if [ -f "$OUT/${tool}/${bug}/result.json" ]; then
        echo "[chat5-retry-v3] SUCCESS tool=${tool} bug=${bug} attempt=${tries}" >> "$LOG"
        return 0
      fi
    fi
    echo "[chat5-retry-v3] MISS tool=${tool} bug=${bug} attempt=${tries}" >> "$LOG"
    sleep 120
  done
  echo "[chat5-retry-v3] GIVE-UP tool=${tool} bug=${bug} after ${tries} attempts" >> "$LOG"
  return 1
}

# repair biopython venv
repair_tries=0
while [ $repair_tries -lt $MAX_TRIES ]; do
  repair_tries=$((repair_tries+1))
  if /work/compares/results/sut-envs/biopython/bin/python -c \
       "import Bio, numpy" 2>/dev/null; then
    echo "[chat5-retry-v3] biopython venv OK (no repair needed) attempt=${repair_tries}" >> "$LOG"
    break
  fi
  wait_for_quiet
  echo "[chat5-retry-v3] repair biopython venv attempt=${repair_tries} $(date -u +%FT%TZ)" >> "$LOG"
  if /work/compares/results/sut-envs/biopython/bin/pip install --force-reinstall \
       numpy biopython==1.85 >> "$LOG" 2>&1; then
    if /work/compares/results/sut-envs/biopython/bin/python -c \
         "import Bio, numpy" >> "$LOG" 2>&1; then
      echo "[chat5-retry-v3] biopython venv repair SUCCESS attempt=${repair_tries}" >> "$LOG"
      break
    fi
  fi
  echo "[chat5-retry-v3] biopython venv repair failed attempt=${repair_tries}" >> "$LOG"
  sleep 120
done

retry_cell pure_random biopython-4825
retry_cell pure_random seqan3-3098
retry_cell pure_random seqan3-2869
retry_cell pure_random seqan3-3406
retry_cell libfuzzer  seqan3-2869

# rebuild aggregate / manifest / report
for step in rollup manifest report; do
  tries=0
  while [ $tries -lt 15 ]; do
    tries=$((tries+1))
    wait_for_quiet
    case "$step" in
      rollup)
        python3.12 compares/scripts/rollup_bug_bench.py \
          --bench-root "$OUT" \
          --out "$OUT/aggregate.json" >> "$LOG" 2>&1 \
          && { echo "[chat5-retry-v3] rollup OK" >> "$LOG"; break; }
        ;;
      manifest)
        python3.12 - > "$OUT/run_manifest.json" 2>>"$LOG" <<'PY' && { echo "[chat5-retry-v3] manifest OK" >> "$LOG"; break; }
import json, subprocess, os, time
print(json.dumps({
    "chat": 5,
    "scope": "biopython+seqan3 SAM x {atheris|libfuzzer, pure_random} (biotest excluded by operator)",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "retry_pass": "v3",
    "git_sha": subprocess.check_output(
        ["git", "-C", "/work", "rev-parse", "HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME", ""),
}, indent=2))
PY
        ;;
      report)
        python3.12 /work/compares/scripts/_chat5_report.py \
          --bench-root "$OUT" \
          --out "$OUT/report.md" >> "$LOG" 2>&1 \
          && { echo "[chat5-retry-v3] report OK" >> "$LOG"; break; }
        ;;
    esac
    echo "[chat5-retry-v3] ${step} failed attempt=${tries}" >> "$LOG"
    sleep 90
  done
done

echo "[chat5] RETRY-v3 end=$(date -u +%FT%TZ)" >> "$LOG"
