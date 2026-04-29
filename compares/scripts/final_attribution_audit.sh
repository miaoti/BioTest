#!/usr/bin/env bash
# Run after rerun_biotest_solewitness.sh finishes. Verifies each cell's
# tool-output triggers against the silence-on-fix predicate inside the
# Docker image, then aggregates the deployed-bench data + new-rerun
# data into a final tool-found tally.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

MOUNT_SRC="${REPO_ROOT}"
if [[ "$(uname -s)" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    MOUNT_SRC="/${REPO_ROOT//\\//}"
fi
export MSYS_NO_PATHCONV=1

DEEPSEEK_API_KEY="$(grep -E '^DEEPSEEK_API_KEY=' .env 2>/dev/null | cut -d= -f2-)"

RERUN_ROOT="compares/results/bug_bench/biotest_rerun_2026_04_28"
ORIG_ROOT="compares/results/bug_bench"

echo "=== Step 1: verify_tool_found on rerun (8 sole-witness cells) ==="
docker run --rm \
    -v "${MOUNT_SRC}:/work" -w /work -e PYTHONPATH=/work \
    -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
    biotest-bench:latest \
    python3.12 compares/scripts/verify_tool_found.py \
    "${RERUN_ROOT}" \
    htsjdk-1364 htsjdk-1372 htsjdk-1544 htsjdk-1554 \
    vcfpy-127 vcfpy-146 vcfpy-176 noodles-268 \
    2>&1 | tee "${RERUN_ROOT}/verify_summary.log"

echo
echo "=== Step 2: verify_tool_found on original biotest data (already-confirmed 5) ==="
# htsjdk-1238/-1360/-1410 are SAM cells where adapter fired in the
# original bench; htsjdk-1389/-1418 are VCF cells multi-witnessed with
# evosuite — still worth checking adapter triggers.
docker run --rm \
    -v "${MOUNT_SRC}:/work" -w /work -e PYTHONPATH=/work \
    -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
    biotest-bench:latest \
    python3.12 compares/scripts/verify_tool_found.py \
    "${ORIG_ROOT}" \
    htsjdk-1238 htsjdk-1360 htsjdk-1389 htsjdk-1410 htsjdk-1418 \
    2>&1 | tee "${ORIG_ROOT}/verify_summary_2026_04_29.log"

echo
echo "=== Step 3: Tally across all 13 BioTest FOUND cells ==="
py -3.12 -c "
import json
from pathlib import Path

rerun_audit = json.loads(Path('${RERUN_ROOT}/tool_found_audit.json').read_text())
orig_audit  = json.loads(Path('${ORIG_ROOT}/tool_found_audit.json').read_text())

all_results = {r['bug_id']: r for r in rerun_audit['results']}
for r in orig_audit['results']:
    all_results[r['bug_id']] = r

tool_found_bugs = sorted(b for b, r in all_results.items() if r.get('tool_found'))
print(f'BioTest TRUE tool-found = {len(tool_found_bugs)}')
print(f'Bugs: {tool_found_bugs}')

summary_path = Path('compares/results/bug_bench/FINAL_TOOL_FOUND.json')
summary_path.write_text(json.dumps({
    'total_tool_found': len(tool_found_bugs),
    'bugs': tool_found_bugs,
    'all_audit_results': [all_results[b] for b in sorted(all_results)],
}, indent=2), encoding='utf-8')
print(f'wrote {summary_path}')
"
