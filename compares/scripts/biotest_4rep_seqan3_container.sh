#!/usr/bin/env bash
# Container-side 4-rep full-pipeline sweep for the seqan3/SAM cell.
#
# Runs inside biotest-bench (Linux, Clang 18 + patched seqan3 3.3.0 +
# gcovr 8.6 + Python 3.12). The host harness can't be measured under
# the DESIGN seqan3 filter because it doesn't link seqan3; this script
# rebuilds biotest_harness.cpp with `-DUSE_SEQAN3` so the seqan3
# pre-pass actually executes seqan3::sam_file_input + format_sam paths,
# then runs biotest.py 4 times inside the container.
#
# Usage (from host):
#   docker exec biotest-bench-setup bash /work/compares/scripts/biotest_4rep_seqan3_container.sh
set -euo pipefail

WORK=/work
OUT_ROOT="${OUT_ROOT:-${WORK}/compares/results/coverage/biotest_4rep_fullD_20260423/seqan3_sam_container}"
mkdir -p "${OUT_ROOT}"
LOG="${OUT_ROOT}/run.log"
: > "${LOG}"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S)] $*" | tee -a "${LOG}"; }

log "===== biotest-bench seqan3/SAM 4-rep sweep (full Phase A,B,C,D) ====="

# Step 1 — Python deps (idempotent)
log "Step 1: pip install -r requirements.txt + gcovr"
if ! python3.12 -c "import yaml, rich, hypothesis, chromadb, gcovr" >/dev/null 2>&1; then
  python3.12 -m pip install --quiet --no-warn-script-location -r "${WORK}/requirements.txt" gcovr lxml >>"${LOG}" 2>&1 \
    || { log "pip install failed"; exit 1; }
fi
python3.12 -c "import yaml, rich, hypothesis, chromadb; import gcovr; print('deps OK')" | tee -a "${LOG}"

# Step 2 — build seqan3-instrumented harness ONCE
HARNESS_SRC="${WORK}/harnesses/cpp/biotest_harness.cpp"
HARNESS_BIN="${WORK}/harnesses/cpp/build/biotest_harness_cov_seqan3"
log "Step 2: clang++-18 -fprofile-arcs -ftest-coverage -DUSE_SEQAN3 build"
if [[ ! -x "${HARNESS_BIN}" ]] || [[ "${HARNESS_SRC}" -nt "${HARNESS_BIN}" ]]; then
  rm -f "${WORK}/harnesses/cpp/build/"*.gcda "${WORK}/harnesses/cpp/build/"*.gcno
  clang++-18 -std=c++23 -O0 -g \
    -DNDEBUG -DUSE_SEQAN3 -DSEQAN3_DISABLE_COMPILER_CHECK \
    -isystem /opt/seqan3/include \
    -fprofile-arcs -ftest-coverage \
    "${HARNESS_SRC}" \
    -o "${HARNESS_BIN}" >>"${LOG}" 2>&1 \
    || { log "clang++-18 build failed"; exit 1; }
fi
ls -la "${HARNESS_BIN}" | tee -a "${LOG}"

# Step 3 — small seed dir
SEEDS_SMALL="${OUT_ROOT}/seeds_small"
mkdir -p "${SEEDS_SMALL}/vcf" "${SEEDS_SMALL}/sam"
# 2026-04-26: "normal running" — use ALL seeds (don't filter kept_*
# / synthetic_*). Other tools' seqan3 coverage cells (aflpp, libfuzzer,
# pure_random in compares/results/coverage/ALL_SUT_COVERAGE.md) feed
# tens of thousands of fuzzer-generated inputs through the cov harness;
# biotest needs comparable corpus volume to be apples-to-apples. The
# 586 SAM seeds in seeds/sam/ (curated + jazzer + kept_* + synthetic_*)
# are still bounded but give biotest a fair starting corpus.
python3.12 - <<'PY' "${WORK}" "${SEEDS_SMALL}"
import os, pathlib, shutil, sys
repo, out_root = sys.argv[1], pathlib.Path(sys.argv[2])
for fmt in ("vcf", "sam"):
    src = pathlib.Path(repo) / "seeds" / fmt
    dst = out_root / fmt
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob(f"*.{fmt}"))
    for s in files:
        link = dst / s.name
        if link.exists(): continue
        try: os.symlink(s.resolve(), link)
        except OSError: shutil.copy2(s, link)
    print(f"  {fmt}: staged {len(files)} seeds at {dst}")
ref = pathlib.Path(repo) / "seeds" / "ref"
if ref.exists() and not (out_root / "ref").exists():
    shutil.copytree(ref, out_root / "ref")
PY

STATE_FILES=(
  "${WORK}/data/mr_registry.json"
  "${WORK}/data/feedback_state.json"
  "${WORK}/data/rule_attempts.json"
  "${WORK}/data/coverage_report.json"
  "${WORK}/data/det_report.json"
  "${WORK}/data/scc_report.json"
)

# Step 4 — 4 reps of biotest A,D with primary=seqan3, format=SAM
for rep in 0 1 2 3; do
  log ""
  log "### seqan3/SAM -- rep ${rep} --"
  for f in "${STATE_FILES[@]}"; do [[ -f "${f}" ]] && rm -f "${f}"; done
  rm -f "${WORK}/coverage_artifacts/gcovr.json"
  rm -f "${WORK}/harnesses/cpp/build/"*.gcda

  REP_DIR="${OUT_ROOT}/run_${rep}"
  mkdir -p "${REP_DIR}"
  CFG="${REP_DIR}/biotest_config.rep${rep}.yaml"

  # Per-rep config: pin seqan3 cell, point adapter at the seqan3-linked
  # cov binary (Linux ELF), max_iterations=2, seed_synthesis off,
  # timeout_minutes=80.
  python3.12 - <<PY "${WORK}" "${CFG}" "${SEEDS_SMALL}" "${rep}" "${HARNESS_BIN}"
import yaml, sys, pathlib
repo, cfg_path, seeds, rep, hbin = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
cfg = yaml.safe_load(pathlib.Path(repo, "biotest_config.yaml").read_text("utf-8"))
cfg.setdefault("phase_c", {})["format_filter"] = "SAM"
cfg["phase_c"]["seeds_dir"] = seeds
cfg["phase_c"]["corpus_keeper"] = {"enabled": False, "max_files_per_format": 2000}

# Override the seqan3 SUT entry to point at the seqan3-linked cov binary.
for sut in cfg["phase_c"]["suts"]:
    if sut.get("name") == "seqan3":
        sut["adapter"] = hbin
        sut["coverage_binary"] = hbin

fb = cfg.setdefault("feedback_control", {})
fb["enabled"] = True
fb["primary_target"] = "seqan3"
fb["max_iterations"] = 2
fb["plateau_patience"] = 4
fb["coverage_plateau_patience"] = 4
fb["timeout_minutes"] = 110
fb.setdefault("seed_synthesis", {})["enabled"] = False
cfg["phase_e"] = {
    "enabled": True,
    "structural_max_per_seed": 10,
    "rawfuzz_n_per_seed": 2,
    "rawfuzz_seed": 42 + rep,
}
cfg.setdefault("global", {})["seed_rng"] = 42 + rep
pathlib.Path(cfg_path).write_text(yaml.safe_dump(cfg, sort_keys=False), "utf-8")
print(f"wrote {cfg_path}")
PY

  BIOTEST_LOG="${REP_DIR}/biotest.log"
  log "  cmd: python3.12 biotest.py --config ${CFG} --phase A,D,E"
  cd "${WORK}"
  t0=$(date +%s)
  # --phase A,D,E: see biotest_4rep_noodles_container.sh comment.
  # DESIGN §3 compute parity: 7200 s per rep.
  timeout --kill-after=60 7200 python3.12 "${WORK}/biotest.py" \
    --config "${CFG}" --phase A,D,E --verbose \
    > "${BIOTEST_LOG}" 2>&1 || true
  t1=$(date +%s)
  elapsed=$((t1 - t0))
  log "  elapsed=${elapsed}s"

  # Run gcovr against the seqan3 build dir, then measure under DESIGN scope.
  python3.12 -m gcovr --json -o "${WORK}/coverage_artifacts/gcovr.json" \
    --root /opt/seqan3/include \
    --filter '.*seqan3.*' \
    --gcov-executable 'llvm-cov-18 gcov' \
    "${WORK}/harnesses/cpp/build" >>"${LOG}" 2>&1 || true

  MEASURE_OUT="${REP_DIR}/measurement.json"
  if [[ -f "${WORK}/coverage_artifacts/gcovr.json" ]]; then
    python3.12 - <<PY "${WORK}" "${rep}" "${elapsed}" "${MEASURE_OUT}"
import json, pathlib, subprocess, sys
repo, rep, elapsed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
proc = subprocess.run([
    "python3.12", f"{repo}/compares/scripts/measure_coverage.py",
    "--report", f"{repo}/coverage_artifacts/gcovr.json",
    "--sut", "seqan3", "--format", "SAM",
], capture_output=True, text=True, cwd=repo)
stdout = proc.stdout
line_pct = covered = total = 0.0
for ln in stdout.splitlines():
    if "OVERALL" in ln and "weighted" in ln:
        tail = ln.split(")", 1)[1].strip()
        frac, pct = tail.split("(")
        c, t = frac.strip().split("/")
        pct = pct.replace("%", "").replace(")", "").strip()
        line_pct, covered, total = float(pct), int(c), int(t)
        break
payload = {
  "cell": "seqan3_sam", "sut": "seqan3", "format": "SAM",
  "rep": rep, "elapsed_s": elapsed, "line_pct": line_pct,
  "covered": covered, "total": total, "phases": "A,D",
  "max_iterations": 2, "status": "ok" if total else "missing",
  "source": "coverage_artifacts/gcovr.json",
}
pathlib.Path(out).write_text(json.dumps(payload, indent=2), "utf-8")
print(json.dumps(payload, indent=2))
PY
  else
    echo "{\"cell\":\"seqan3_sam\",\"sut\":\"seqan3\",\"format\":\"SAM\",\"rep\":${rep},\"elapsed_s\":${elapsed},\"line_pct\":0.0,\"covered\":0,\"total\":0,\"status\":\"missing\"}" > "${MEASURE_OUT}"
  fi

  line=$(python3.12 -c "import json; d=json.load(open('${MEASURE_OUT}')); print(f\"line={d['line_pct']:.2f}%% covered={d['covered']}/{d['total']} status={d['status']}\")")
  log "  -> ${line}"
done

log ""
log "===== seqan3/SAM container sweep complete ====="
