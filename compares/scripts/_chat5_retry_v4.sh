#!/usr/bin/env bash
# Chat 5 retry pass v4 — drives the 5 skipped cells via a tmpfs-resident
# driver copy (/tmp/chat5_scripts/driver.py), so Python's startup sys.path
# scan stays off the 9p /work share and the 9p-ENOMEM storm that killed v2/v3
# is sidestepped at the root.
#
# Cells to recover:
#   pure_random biopython-4825
#   pure_random seqan3-3098
#   pure_random seqan3-2869
#   pure_random seqan3-3406
#   libfuzzer   seqan3-2869
set -u
export PATH=/root/.cargo/bin:$PATH
cd /tmp

LOG=/tmp/phase4-chat5.log
OUT=/tmp/bug_bench_chat5
BUDGET_S=${BUDGET_S:-300}
export BUDGET_S
DRIVER=/tmp/chat5_scripts/driver.py
MANIFEST=/work/compares/bug_bench/manifest.verified.json

echo "[chat5] RETRY-v4 start $(date -u +%FT%TZ)" >> "$LOG"

retry_cell() {
  local tool=$1
  local bug=$2
  local tries=0
  while [ $tries -lt 10 ]; do
    tries=$((tries+1))
    if [ -f "$OUT/${tool}/${bug}/result.json" ]; then
      echo "[chat5-retry-v4] SKIP tool=${tool} bug=${bug} (already present)" >> "$LOG"
      return 0
    fi
    echo "[chat5-retry-v4] tool=${tool} bug=${bug} attempt=${tries} $(date -u +%FT%TZ)" >> "$LOG"
    rm -rf "$OUT/${tool}/${bug}"
    if python3.12 "$DRIVER" \
         --manifest "$MANIFEST" \
         --only-bug "$bug" --only-tool "$tool" \
         --time-budget-s ${BUDGET_S} \
         --out "$OUT" >> "$LOG" 2>&1; then
      if [ -f "$OUT/${tool}/${bug}/result.json" ]; then
        echo "[chat5-retry-v4] SUCCESS tool=${tool} bug=${bug} attempt=${tries}" >> "$LOG"
        return 0
      fi
    fi
    echo "[chat5-retry-v4] MISS tool=${tool} bug=${bug} attempt=${tries}" >> "$LOG"
    sleep 90
  done
  echo "[chat5-retry-v4] GIVE-UP tool=${tool} bug=${bug} after ${tries} attempts" >> "$LOG"
  return 1
}

retry_cell libfuzzer  seqan3-2869
retry_cell pure_random seqan3-3098
retry_cell pure_random seqan3-2869
retry_cell pure_random seqan3-3406
retry_cell pure_random biopython-4825

# rebuild aggregate + manifest + report (tmpfs-resident scripts)
echo "[chat5-retry-v4] rollup $(date -u +%FT%TZ)" >> "$LOG"
tries=0
while [ $tries -lt 10 ]; do
  tries=$((tries+1))
  python3.12 /tmp/chat5_scripts/rollup.py \
    --bench-root "$OUT" \
    --out "$OUT/aggregate.json" >> "$LOG" 2>&1 \
    && { echo "[chat5-retry-v4] rollup OK attempt=${tries}" >> "$LOG"; break; }
  sleep 60
done

echo "[chat5-retry-v4] manifest $(date -u +%FT%TZ)" >> "$LOG"
python3.12 - > "$OUT/run_manifest.json" 2>>"$LOG" <<'PY'
import json, subprocess, os, time
print(json.dumps({
    "chat": 5,
    "scope": "biopython+seqan3 SAM x {atheris|libfuzzer, pure_random} (biotest excluded by operator)",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "retry_pass": "v4-tmpfs",
    "git_sha": subprocess.check_output(
        ["git", "-C", "/work", "rev-parse", "HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME", ""),
}, indent=2))
PY

echo "[chat5-retry-v4] report $(date -u +%FT%TZ)" >> "$LOG"
tries=0
while [ $tries -lt 10 ]; do
  tries=$((tries+1))
  python3.12 /tmp/chat5_scripts/report.py \
    --bench-root "$OUT" \
    --out "$OUT/report.md" >> "$LOG" 2>&1 \
    && { echo "[chat5-retry-v4] report OK attempt=${tries}" >> "$LOG"; break; }
  sleep 60
done

echo "[chat5] RETRY-v4 end=$(date -u +%FT%TZ)" >> "$LOG"
