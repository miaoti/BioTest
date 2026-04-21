#!/usr/bin/env bash
# Chat 5 runner — biotest excluded by operator.
# biopython x {atheris, pure_random}, seqan3 x {libfuzzer, pure_random}.
# 14 cells total. Emits aggregate.json + run_manifest.json + report.md.
set -u
export PATH=/root/.cargo/bin:$PATH
cd /work

LOG=/tmp/phase4-chat5.log
OUT=/tmp/bug_bench_chat5

rm -rf "$OUT"
mkdir -p "$OUT"

BUDGET_S=${BUDGET_S:-300}
export BUDGET_S
echo "[chat5] RESTART (biotest excluded) budget=${BUDGET_S}s start=$(date -u +%FT%TZ)" >> "$LOG"

# biopython × {atheris, pure_random}
for TOOL in atheris pure_random; do
  echo "[chat5] biopython tool=${TOOL} $(date -u +%FT%TZ)" >> "$LOG"
  python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.verified.json \
    --only-sut biopython --only-tool ${TOOL} \
    --time-budget-s ${BUDGET_S} \
    --out "$OUT" \
    >> "$LOG" 2>&1
done

# seqan3 × {libfuzzer, pure_random}
for TOOL in libfuzzer pure_random; do
  echo "[chat5] seqan3 tool=${TOOL} $(date -u +%FT%TZ)" >> "$LOG"
  python3.12 compares/scripts/bug_bench_driver.py \
    --manifest compares/bug_bench/manifest.verified.json \
    --only-sut seqan3 --only-tool ${TOOL} \
    --time-budget-s ${BUDGET_S} \
    --out "$OUT" \
    >> "$LOG" 2>&1
done

echo "[chat5] all tool loops done $(date -u +%FT%TZ)" >> "$LOG"

python3.12 compares/scripts/rollup_bug_bench.py \
  --bench-root "$OUT" \
  --out "$OUT/aggregate.json" >> "$LOG" 2>&1

python3.12 - > "$OUT/run_manifest.json" <<'PY'
import json, subprocess, os, time
print(json.dumps({
    "chat": 5,
    "scope": "biopython+seqan3 SAM x {atheris|libfuzzer, pure_random} (biotest excluded by operator)",
    "budget_s": int(os.environ["BUDGET_S"]),
    "ended_at": time.strftime("%FT%TZ", time.gmtime()),
    "git_sha": subprocess.check_output(
        ["git", "-C", "/work", "rev-parse", "HEAD"]).decode().strip(),
    "image_id": os.environ.get("HOSTNAME", ""),
}, indent=2))
PY

python3.12 /work/compares/scripts/_chat5_report.py \
  --bench-root "$OUT" \
  --out "$OUT/report.md" >> "$LOG" 2>&1

echo "[chat5] end=$(date -u +%FT%TZ)" >> "$LOG"
