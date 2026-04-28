#!/usr/bin/env bash
# Re-run Phase-2 rep_3 + Phase-3 mutation rep_3 in an isolated host slot
# (no concurrent Docker containers) so host-load contention doesn't
# degrade the 4th data point for the atheris × biopython cell.
# Produces:
#   compares/results/coverage/atheris/biopython/run_3/             (fresh)
#   compares/results/coverage/atheris/biopython/growth_3.json      (overwritten)
#   compares/results/mutation/atheris/biopython/rep_3_run/         (fresh)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}"

echo "[$(date -Is)] rerun_rep3_clean: Phase 2 rep_3 (isolated)..."
rm -rf compares/results/coverage/atheris/biopython/run_3 \
       compares/results/coverage/atheris/biopython/growth_3.json
PYTHONIOENCODING=utf-8 py -3.12 -c "
import sys, argparse, logging, json, time
from pathlib import Path
sys.path.insert(0, 'compares/scripts')
import coverage_sampler as m
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

out_dir = Path('compares/results/coverage/atheris/biopython')
rep_dir = out_dir / 'run_3'
rep_dir.mkdir(parents=True, exist_ok=True)
rep_start = time.time()
snapshots = m._run_atheris_rep(
    sut='biopython', format_hint='SAM',
    seed_corpus=Path('compares/results/bench_seeds/sam'),
    out_rep=rep_dir, time_budget_s=300,
    ticks=(1, 10, 60, 300),
    opts=argparse.Namespace(
        atheris_image='biotest-bench:latest',
        atheris_python='/opt/atheris-venv/bin/python',
        atheris_harness=None,
    ),
)
rep_end = time.time()
record = m.GrowthRecord(
    tool='atheris', sut='biopython', format='SAM', phase='coverage',
    run_index=3, time_budget_s=300,
    seed_corpus_hash=m._hash_corpus(Path('compares/results/bench_seeds/sam')),
    coverage_growth=snapshots,
    extra={'duration_s': round(rep_end - rep_start, 2),
           'seed_corpus_dir': 'compares/results/bench_seeds/sam',
           'out_dir': str(rep_dir), 'ticks_requested': [1,10,60,300],
           'reason': 'clean re-run in isolated host slot'},
)
(out_dir / 'growth_3.json').write_text(json.dumps(record.to_json(), indent=2), encoding='utf-8')
print('rep 3 ticks:', [(t.t_s, round(t.line_pct,2)) for t in snapshots])
"

echo "[$(date -Is)] rerun_rep3_clean: Phase 3 mutation on rep_3 corpus..."
rm -rf compares/results/mutation/atheris/biopython/rep_3_run
CORPUS_DIR="${REPO_ROOT}/compares/results/coverage/atheris/biopython/run_3/corpus" \
  OUT_DIR="${REPO_ROOT}/compares/results/mutation/atheris/biopython/rep_3_run" \
  BUDGET_S=1500 MAX_MUTANTS=0 \
  bash compares/scripts/phase3_atheris_biopython.sh

echo "[$(date -Is)] rerun_rep3_clean: done."
