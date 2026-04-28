#!/usr/bin/env bash
# Phase-3 driver: Jazzer × htsjdk mutation score via PIT (pitest).
#
# DESIGN.md §13.5 Phase 3 — "for each tool's final corpus, for each
# mutant m: run corpus against mutated SUT; divergent outcome vs.
# unmutated baseline = kill." We implement that with PIT by:
#   1. Materialising a combined corpus from Phase-2's three reps
#      (run_0/corpus + run_1/corpus + run_2/corpus, deduped).
#   2. Building a baseline JSON of `{filename: outcome}` from the
#      unmutated htsjdk (BaselineBuilder.main).
#   3. Running PIT with --targetClasses restricted to
#      biotest_config.yaml:coverage.target_filters.<FMT>.htsjdk
#      (via compares/scripts/enumerate_target_classes.py) and
#      --targetTests pointing at {VCF,SAM}MutationTest — which assert
#      each corpus file's outcome matches the baseline.
#
# Output per cell:
#   compares/results/mutation/jazzer/htsjdk_<fmt>/
#     baseline.json          unmutated outcome snapshot
#     corpus_combined/       N corpus files unioned across 3 reps
#     pit_report/            PIT's HTML + mutations.xml (line/mutation summary)
#     summary.json           {killed, no_coverage, survived, reachable, score}
#
# Env overrides:
#   FORMATS  — space-separated list (default "VCF SAM")
#   THREADS  — PIT --threads (default 4)
#   MUTATORS — PIT --mutators group (default DEFAULTS; use STRONGER for
#              a richer kill signal at ~2x walltime)
#   MUTATION_UNIT_SIZE — PIT --mutationUnitSize (default 5)
#   CORPUS_MAX — cap N files per cell (default 500 — full 1000+ file
#                corpus would take ~8h per cell; 500 keeps both cells
#                inside the §13.5 Phase 3 budget of ~2 overnights)
#   MAX_MUTATIONS_PER_CLASS — PIT --maxMutationsPerClass (default 0 = no cap)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PHASE3_DIR="${REPO_ROOT}/compares/scripts/phase3_pit"
# TOOL env var lets us reuse this driver for biotest as well as jazzer.
# When TOOL=biotest, coverage_root expects a staged biotest corpus at
# compares/results/coverage/biotest/htsjdk_{vcf,sam}/run_0/corpus/ and
# results land under compares/results/mutation/biotest/htsjdk_{vcf,sam}/.
TOOL="${TOOL:-jazzer}"
OUT_ROOT="${OUT_ROOT:-${REPO_ROOT}/compares/results/mutation/${TOOL}}"
COVERAGE_ROOT="${COVERAGE_ROOT:-${REPO_ROOT}/compares/results/coverage/${TOOL}}"
REPS="${REPS:-0 1 2}"

FORMATS="${FORMATS:-VCF SAM}"
THREADS="${THREADS:-4}"
MUTATORS="${MUTATORS:-DEFAULTS}"
MUTATION_UNIT_SIZE="${MUTATION_UNIT_SIZE:-5}"
CORPUS_MAX="${CORPUS_MAX:-500}"
MAX_MUTATIONS_PER_CLASS="${MAX_MUTATIONS_PER_CLASS:-0}"

HARNESS_JAR="${REPO_ROOT}/compares/harnesses/jazzer/build/libs/biotest-jazzer.jar"
HTSJDK_CLASSES_DIR="${REPO_ROOT}/compares/harnesses/jazzer/build/htsjdk-classes"
# Use the Jazzer harness fatjar as the htsjdk classpath: it's the
# exact `htsjdk:4.1.1` shipped to the Phase-2 fuzzer that generated the
# corpus, so mutants run against the same classes whose branches the
# corpus was selected for. The EvoSuite `htsjdk-with-deps.jar` is
# pinned to 2.24.1 — a different codebase; PIT'ing it would mutate code
# that didn't produce the corpus and bias the kill signal.
HTSJDK_FATJAR="${HARNESS_JAR}"

# JUnit 4 + Hamcrest. Cached under the mounted repo so the jars
# survive between `docker run --rm` invocations (/opt is ephemeral
# outside of baked image layers).
JUNIT_DIR="${JUNIT_DIR:-${PHASE3_DIR}/lib}"
JUNIT_JAR="${JUNIT_DIR}/junit-4.13.2.jar"
HAMCREST_JAR="${JUNIT_DIR}/hamcrest-core-1.3.jar"

# PIT jars (baked into biotest-bench:latest at /opt/pit).
PIT_DIR="${PIT_DIR:-/opt/pit}"
PIT_CLI="${PIT_DIR}/pitest-command-line.jar"
PIT_ENTRY="${PIT_DIR}/pitest-entry.jar"
PIT_CORE="${PIT_DIR}/pitest.jar"

mkdir -p "${OUT_ROOT}"

log() { echo "[$(date -Is)] [phase3-${TOOL}] $*" | tee -a "${OUT_ROOT}/phase3_${TOOL}_htsjdk.log"; }

# ---------------------------------------------------------------------------
# 1. Download JUnit 4 + Hamcrest if not cached
# ---------------------------------------------------------------------------
if [[ ! -f "${JUNIT_JAR}" || ! -f "${HAMCREST_JAR}" ]]; then
  log "downloading junit4 + hamcrest to ${JUNIT_DIR} (first-run only)"
  mkdir -p "${JUNIT_DIR}"
  curl -sSL -o "${JUNIT_JAR}" \
      https://repo1.maven.org/maven2/junit/junit/4.13.2/junit-4.13.2.jar
  curl -sSL -o "${HAMCREST_JAR}" \
      https://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar
fi

# ---------------------------------------------------------------------------
# 2. Ensure htsjdk classes dir is materialised (coverage_sampler.py
#    does this during Phase 2; just re-invoke for idempotency).
# ---------------------------------------------------------------------------
if [[ ! -f "${HTSJDK_CLASSES_DIR}/htsjdk/variant/vcf/VCFCodec.class" ]]; then
  log "extracting htsjdk classes from ${HARNESS_JAR}"
  mkdir -p "${HTSJDK_CLASSES_DIR}"
  ( cd "${HTSJDK_CLASSES_DIR}" && unzip -o -q "${HARNESS_JAR}" 'htsjdk/*' )
fi

# ---------------------------------------------------------------------------
# 3. Compile the three Java tools (BaselineBuilder + two JUnit tests)
# ---------------------------------------------------------------------------
BUILD_DIR="${PHASE3_DIR}/build"
mkdir -p "${BUILD_DIR}"
log "compiling BaselineBuilder / {VCF,SAM}MutationTest / PerFileCoverageProbe"
# PerFileCoverageProbe needs jacoco-core + asm on compile classpath.
# It's a no-op dependency when the jars are absent (compile step is skipped).
JACOCO_CORE_JAR="${PHASE3_DIR}/lib/jacoco-core.jar"
JACOCO_AGENT_JAR="${REPO_ROOT}/coverage_artifacts/jacoco/jacocoagent.jar"
ASM_CP="${PHASE3_DIR}/lib/asm.jar:${PHASE3_DIR}/lib/asm-commons.jar:${PHASE3_DIR}/lib/asm-tree.jar"
javac \
    -source 17 -target 17 \
    -d "${BUILD_DIR}" \
    -cp "${HTSJDK_FATJAR}:${JUNIT_JAR}:${HAMCREST_JAR}" \
    "${PHASE3_DIR}/BaselineBuilder.java" \
    "${PHASE3_DIR}/VCFMutationTest.java" \
    "${PHASE3_DIR}/SAMMutationTest.java"
if [[ -f "${JACOCO_CORE_JAR}" && -f "${JACOCO_AGENT_JAR}" ]]; then
    javac -source 17 -target 17 -d "${BUILD_DIR}" \
        -cp "${HTSJDK_FATJAR}:${JACOCO_CORE_JAR}:${JACOCO_AGENT_JAR}:${ASM_CP}:${BUILD_DIR}" \
        "${PHASE3_DIR}/PerFileCoverageProbe.java" || true
fi

# ---------------------------------------------------------------------------
# 4. Per-format cell
# ---------------------------------------------------------------------------
run_cell() {
  local FMT="$1"            # VCF or SAM
  local LCASE
  LCASE=$(echo "${FMT}" | tr A-Z a-z)

  local CELL_DIR="${OUT_ROOT}/htsjdk_${LCASE}"
  local REPORT_DIR="${CELL_DIR}/pit_report"
  local CORPUS_DIR="${CELL_DIR}/corpus_combined"
  local BASELINE_JSON="${CELL_DIR}/baseline.json"
  local TEST_CLASS
  if [[ "${FMT}" == "VCF" ]]; then TEST_CLASS="VCFMutationTest"; else TEST_CLASS="SAMMutationTest"; fi

  mkdir -p "${CELL_DIR}" "${REPORT_DIR}" "${CORPUS_DIR}"

  # 4a. Materialise a combined corpus from the 3 reps (union by name;
  #     duplicates de-duped). Cap to CORPUS_MAX for walltime sanity.
  # If a Rank-8 corpus-keeper + corpus_minimize run already produced a
  # `corpus_min/` sibling dir (per DESIGN.md §Rank 8 companion tool),
  # prefer it — it's coverage-fingerprint-deduped and directly matches
  # the PIT walltime envelope. See
  # `compares/scripts/corpus_minimize.py` and
  # `test_engine/feedback/corpus_keeper.py`.
  log "=== cell jazzer x htsjdk ${FMT} ==="
  log "materialising combined corpus at ${CORPUS_DIR} (cap=${CORPUS_MAX})"
  rm -f "${CORPUS_DIR}"/*
  local I=0
  for R in ${REPS}; do
    local SRC="${COVERAGE_ROOT}/htsjdk_${LCASE}/run_${R}/corpus"
    local SRC_MIN="${COVERAGE_ROOT}/htsjdk_${LCASE}/run_${R}/corpus_min"
    if [[ -d "${SRC_MIN}" ]]; then
      log "  using coverage-minimised corpus ${SRC_MIN}"
      SRC="${SRC_MIN}"
    fi
    if [[ ! -d "${SRC}" ]]; then
      log "  skip: ${SRC} missing"
      continue
    fi
    while IFS= read -r -d '' F; do
      if (( I >= CORPUS_MAX )); then break; fi
      local NAME
      NAME=$(basename "${F}")
      if [[ ! -e "${CORPUS_DIR}/${NAME}" ]]; then
        cp "${F}" "${CORPUS_DIR}/${NAME}"
        I=$((I + 1))
      fi
    done < <(find "${SRC}" -maxdepth 1 -type f -print0)
    if (( I >= CORPUS_MAX )); then break; fi
  done

  # 4a-augment. Union the Phase-E augmented seeds (Rank 12 struct +
  # Rank 13 rawfuzz). These dirs are auto-populated by `biotest.py`'s
  # Phase E. Skip cleanly when running for non-biotest tools or when
  # the augmented dirs don't exist yet.
  if [[ "${TOOL}" == biotest* ]]; then
    local LCASE_FMT="${LCASE}"
    for AUG in "${REPO_ROOT}/seeds/${LCASE_FMT}_struct" \
               "${REPO_ROOT}/seeds/${LCASE_FMT}_rawfuzz"; do
      if [[ -d "${AUG}" ]]; then
        local TAG
        TAG=$(basename "${AUG}")
        local ADDED=0
        while IFS= read -r -d '' F; do
          if (( I >= CORPUS_MAX )); then break; fi
          local NAME
          NAME=$(basename "${F}")
          if [[ ! -e "${CORPUS_DIR}/${NAME}" ]]; then
            cp "${F}" "${CORPUS_DIR}/${NAME}"
            I=$((I + 1)); ADDED=$((ADDED + 1))
          fi
        done < <(find "${AUG}" -maxdepth 1 -type f -print0)
        log "  +${ADDED} from ${TAG}"
        if (( I >= CORPUS_MAX )); then break; fi
      fi
    done
  fi

  local CORPUS_COUNT
  CORPUS_COUNT=$(ls "${CORPUS_DIR}" | wc -l)
  log "combined corpus: ${CORPUS_COUNT} files"

  # 4b. Build the unmutated baseline outcomes map.
  log "building baseline outcomes"
  java -cp "${BUILD_DIR}:${HTSJDK_FATJAR}" \
      BaselineBuilder "${FMT}" "${CORPUS_DIR}" "${BASELINE_JSON}"

  # NOTE: per-file JaCoCo coverage-guided selection was evaluated here
  # (r21, 2026-04-23) on both htsjdk cells:
  #   htsjdk_sam: 132 kills selected (150 files from 271) = 132 unselected — neutral
  #   htsjdk_vcf: 186 kills selected (150 files from 260) vs 192 unselected — REGRESSED -6
  # Line-level coverage is orthogonal to mutation-kill potential: a file
  # that covers line X doesn't necessarily distinguish mutated-vs-
  # unmutated behaviour at X — it has to exercise a specific byte pattern
  # that makes the mutant's output differ. Greedy-selecting for max line
  # coverage picks files that cover more *parser paths* but not
  # necessarily more *kill-discriminating* inputs.
  #
  # PerFileCoverageProbe.java + corpus_coverage_select.py's --prebuilt-json
  # path are left in place for future experiments (different target
  # sizes, different mutation-operator sets), but the shell hook that
  # wired them into the PIT flow is disabled — the full corpus wins.

  # 4c. Enumerate the target-class list per the fairness recipe.
  local TARGET_CLASSES
  TARGET_CLASSES=$(python3.12 "${REPO_ROOT}/compares/scripts/enumerate_target_classes.py" \
      --sut htsjdk --format "${FMT}" \
      --classes-dir "${HTSJDK_CLASSES_DIR}" \
      --format-out pit)
  local TARGET_N
  TARGET_N=$(python3.12 "${REPO_ROOT}/compares/scripts/enumerate_target_classes.py" \
      --sut htsjdk --format "${FMT}" \
      --classes-dir "${HTSJDK_CLASSES_DIR}" 2>&1 | wc -l)
  log "target classes: ${TARGET_N} (fairness-recipe-filtered)"

  # 4d. Invoke PIT. Classpath notes:
  #   - Use HTSJDK_CLASSES_DIR (flat class tree) not HARNESS_JAR — the
  #     Jazzer fatjar bundles JUnit 5 transitively via jazzer-junit,
  #     which makes PIT warn "JUnit 5 is on classpath" and skip our
  #     JUnit 4 test discovery. The flat dir has only htsjdk classes.
  #   - Commons-text + commons-lang3 are required by PIT's XML report
  #     writer (not bundled in pitest-entry.jar by default).
  local COMMONS_TEXT="${JUNIT_DIR}/commons-text-1.10.0.jar"
  local COMMONS_LANG3="${JUNIT_DIR}/commons-lang3-3.12.0.jar"
  for J in "${COMMONS_TEXT}" "${COMMONS_LANG3}"; do
    if [[ ! -f "${J}" ]]; then
      log "downloading $(basename ${J})"
      case "$(basename ${J})" in
        commons-text-*) curl -sSL -o "${J}" https://repo1.maven.org/maven2/org/apache/commons/commons-text/1.10.0/commons-text-1.10.0.jar ;;
        commons-lang3-*) curl -sSL -o "${J}" https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar ;;
      esac
    fi
  done

  log "running PIT (threads=${THREADS} mutators=${MUTATORS})"
  CORPUS_DIR="${CORPUS_DIR}" BASELINE_JSON="${BASELINE_JSON}" \
  java \
      -Xmx4g \
      -cp "${PIT_CLI}:${PIT_ENTRY}:${PIT_CORE}:${COMMONS_TEXT}:${COMMONS_LANG3}:${BUILD_DIR}:${HTSJDK_CLASSES_DIR}:${JUNIT_JAR}:${HAMCREST_JAR}" \
      org.pitest.mutationtest.commandline.MutationCoverageReport \
      --reportDir "${REPORT_DIR}" \
      --targetClasses "${TARGET_CLASSES}" \
      --targetTests "${TEST_CLASS}" \
      --sourceDirs "${HTSJDK_CLASSES_DIR}" \
      --classPath "${BUILD_DIR},${HTSJDK_CLASSES_DIR},${JUNIT_JAR},${HAMCREST_JAR}" \
      --outputFormats "XML" \
      --mutators "${MUTATORS}" \
      --mutationUnitSize "${MUTATION_UNIT_SIZE}" \
      --maxMutationsPerClass "${MAX_MUTATIONS_PER_CLASS}" \
      --threads "${THREADS}" \
      --timeoutConst 30000 \
      --timeoutFactor 2.0 \
      --fullMutationMatrix=false \
      --skipFailingTests=true \
      --verbose=false \
      --jvmArgs="-Xmx2g,-XX:+UseParallelGC" \
      2>&1 | tee -a "${OUT_ROOT}/phase3_${TOOL}_htsjdk.log" | tail -30

  # 4e. Parse mutations.xml into summary.json.
  log "parsing PIT report into summary.json"
  python3.12 "${REPO_ROOT}/compares/scripts/summarise_pit.py" \
      --report-dir "${REPORT_DIR}" \
      --corpus-dir "${CORPUS_DIR}" \
      --baseline-json "${BASELINE_JSON}" \
      --target-classes-n "${TARGET_N}" \
      --fmt "${FMT}" \
      --tool "${TOOL}" \
      --out "${CELL_DIR}/summary.json"

  log "cell ${FMT} done: $(cat "${CELL_DIR}/summary.json" | python3.12 -c 'import json,sys; d=json.load(sys.stdin); print(f"killed={d[\"killed\"]}/{d[\"reachable\"]}  score={d[\"score\"]*100:.2f}%")')"
}

for FMT in ${FORMATS}; do
  run_cell "${FMT}"
done

log "phase3 complete."
