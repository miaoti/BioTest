#!/usr/bin/env bash
# Compile EvoSuite-generated tests, execute against OFFLINE-INSTRUMENTED
# htsjdk, and emit a jacoco.xml report scoped identically to BioTest
# Run 6's 3-path weighted VCF filter.
#
# Why offline instrumentation: EvoSuite tests load htsjdk via its own
# EvoClassLoader which bypasses JaCoCo's -javaagent path. Offline-
# instrumented htsjdk classes record coverage from ANY classloader.

set -u
set -o pipefail

ROOT_UNIX="/c/Users/miaot/Github/BioTest"
ROOT_WIN="C:/Users/miaot/Github/BioTest"
JDK17="$ROOT_WIN/compares/baselines/evosuite/jdk17/jdk-17.0.13+11"
JAVAC="$JDK17/bin/javac"
JAVA="$JDK17/bin/java"

EVO="$ROOT_WIN/compares/baselines/evosuite/source/evosuite-1.2.0.jar"
HTSJDK_FAT="$ROOT_WIN/compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar"
HTSJDK_FAT_INSTR="$ROOT_WIN/compares/baselines/evosuite/fatjar/instrumented/htsjdk-with-deps.jar"
HTSJDK_CLASSDIR="$ROOT_WIN/compares/baselines/evosuite/fatjar/extract"

JACOCO_AGENT="$ROOT_WIN/coverage_artifacts/jacoco/jacocoagent.jar"
JACOCO_CLI="$ROOT_WIN/coverage_artifacts/jacoco/jacococli.jar"

WORK_UNIX="$ROOT_UNIX/compares/baselines/evosuite/results/work"
WORK_WIN="$ROOT_WIN/compares/baselines/evosuite/results/work"
TESTS_SRC="$WORK_UNIX/evosuite-tests"
TESTS_BIN_UNIX="$WORK_UNIX/test-classes"
TESTS_BIN="$WORK_WIN/test-classes"
EXEC_FILE="$WORK_WIN/jacoco.exec"
REPORT_XML="$WORK_WIN/jacoco.xml"

# JUnit 4 + Hamcrest
DEPS_DIR_UNIX="$ROOT_UNIX/compares/baselines/evosuite/test-deps"
DEPS_DIR="$ROOT_WIN/compares/baselines/evosuite/test-deps"
mkdir -p "$DEPS_DIR_UNIX"
[ -f "$DEPS_DIR_UNIX/junit-4.13.2.jar" ] || curl -sSL --fail \
  -o "$DEPS_DIR_UNIX/junit-4.13.2.jar" \
  https://repo1.maven.org/maven2/junit/junit/4.13.2/junit-4.13.2.jar
[ -f "$DEPS_DIR_UNIX/hamcrest-core-1.3.jar" ] || curl -sSL --fail \
  -o "$DEPS_DIR_UNIX/hamcrest-core-1.3.jar" \
  https://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar

# COMPILE classpath: ORIGINAL (uninstrumented) fat jar for resolution
CP_COMPILE="$HTSJDK_FAT;$EVO;$DEPS_DIR/junit-4.13.2.jar;$DEPS_DIR/hamcrest-core-1.3.jar"
# RUN classpath: INSTRUMENTED fat jar + jacocoagent runtime classes
CP_RUN="$HTSJDK_FAT_INSTR;$JACOCO_AGENT;$EVO;$DEPS_DIR/junit-4.13.2.jar;$DEPS_DIR/hamcrest-core-1.3.jar;$TESTS_BIN"

JAVA_OPENS=(
  --add-opens java.base/java.lang=ALL-UNNAMED
  --add-opens java.base/java.util=ALL-UNNAMED
  --add-opens java.base/java.io=ALL-UNNAMED
  --add-opens java.base/java.net=ALL-UNNAMED
  --add-opens java.base/java.lang.reflect=ALL-UNNAMED
  --add-opens java.base/java.time=ALL-UNNAMED
  --add-opens java.base/java.math=ALL-UNNAMED
  --add-opens java.base/sun.net=ALL-UNNAMED
  --add-opens java.base/jdk.internal.loader=ALL-UNNAMED
  --add-opens java.desktop/java.awt=ALL-UNNAMED
  --add-opens java.desktop/sun.awt=ALL-UNNAMED
)

echo "=== Step 1: Compile generated EvoSuite tests ==="
N_SRC=$(find "$TESTS_SRC" -name "*.java" 2>/dev/null | wc -l)
echo "  Found $N_SRC .java files under $TESTS_SRC"
if [[ "$N_SRC" -eq 0 ]]; then
  echo "  No tests to compile — aborting."; exit 1
fi
rm -rf "$TESTS_BIN_UNIX"
mkdir -p "$TESTS_BIN_UNIX"
TEST_FQNS_FILE="$WORK_UNIX/test_fqns.txt"
> "$TEST_FQNS_FILE"
COMPILE_OK=0
COMPILE_FAIL=0
for est in $(find "$TESTS_SRC" -name "*_ESTest.java"); do
  scaf="${est%_ESTest.java}_ESTest_scaffolding.java"
  if "$JAVAC" -cp "$CP_COMPILE;$TESTS_BIN" -d "$TESTS_BIN_UNIX" \
       "$est" "$scaf" 2> "$WORK_UNIX/javac_errors.tmp"; then
    COMPILE_OK=$((COMPILE_OK + 1))
    rel="${est#$TESTS_SRC/}"
    fqn="${rel%.java}"
    fqn="${fqn//\//.}"
    echo "$fqn" >> "$TEST_FQNS_FILE"
  else
    COMPILE_FAIL=$((COMPILE_FAIL + 1))
    head -3 "$WORK_UNIX/javac_errors.tmp" >&2
  fi
done
rm -f "$WORK_UNIX/javac_errors.tmp"
echo "  Compile: ok=$COMPILE_OK, fail=$COMPILE_FAIL"
[[ "$COMPILE_OK" -eq 0 ]] && { echo "  Nothing compiled — aborting."; exit 1; }

echo
echo "=== Step 2: Offline-instrument htsjdk fat jar with JaCoCo ==="
if [[ ! -f "$HTSJDK_FAT_INSTR" ]]; then
  mkdir -p "$(dirname "$HTSJDK_FAT_INSTR")"
  "$JAVA" -jar "$JACOCO_CLI" instrument "$HTSJDK_FAT" \
    --dest "$(dirname "$HTSJDK_FAT_INSTR")" 2>&1 | tail -3
fi
echo "  Instrumented jar: $(du -h "$HTSJDK_FAT_INSTR" | awk '{print $1}')"

echo
echo "=== Step 3: Run the JUnit suite against instrumented classes ==="
rm -f "$EXEC_FILE"
# Run each test class one at a time so a single hang doesn't kill the batch.
# JaCoCo's runtime accumulates into the exec file when dumponexit=true.
N_FQNS=$(wc -l < "$TEST_FQNS_FILE")
RUN_OK=0
RUN_FAIL=0
# Run all classes in a single JUnit invocation — faster & single exec dump
# on exit. If any scaffolding hangs, we rely on the external wall cap.
(
  "$JAVA" "${JAVA_OPENS[@]}" \
    -Djava.awt.headless=true \
    -Djacoco-agent.destfile="$EXEC_FILE" \
    -Djacoco-agent.output=file \
    -Djacoco-agent.dumponexit=true \
    -cp "$CP_RUN" \
    org.junit.runner.JUnitCore $(tr '\n' ' ' < "$TEST_FQNS_FILE") \
    > "$WORK_UNIX/junit_run.log" 2>&1
) &
JP=$!
SECS=0
while kill -0 $JP 2>/dev/null; do
  if [[ $SECS -ge 1800 ]]; then
    echo "  Wall cap hit, killing JUnit"
    kill -9 $JP 2>/dev/null
    break
  fi
  sleep 5
  SECS=$((SECS + 5))
done
wait $JP 2>/dev/null
echo "  JUnit done (ran ${SECS}s). Last 3 lines:"
tail -3 "$WORK_UNIX/junit_run.log"

if [[ ! -f "$EXEC_FILE" ]]; then
  echo "  No exec file produced — aborting."
  exit 1
fi
echo "  jacoco.exec size: $(du -h "$EXEC_FILE" | awk '{print $1}')"

echo
echo "=== Step 4: Generate jacoco.xml ==="
"$JAVA" -jar "$JACOCO_CLI" report "$EXEC_FILE" \
  --classfiles "$HTSJDK_CLASSDIR/htsjdk" \
  --xml "$REPORT_XML" 2>&1 | tail -3
echo "  Wrote $REPORT_XML"

echo
echo "=== Step 5: Apply BioTest filter via measure_coverage.py (single source of truth) ==="
cd "$ROOT_UNIX"
BIOTEST_REF="coverage_artifacts/jacoco/jacoco_post_run6.xml"
if [[ -f "$BIOTEST_REF" ]]; then
  py -3.12 compares/scripts/measure_coverage.py \
    --report "$REPORT_XML"   --label "EvoSuite (this run)" \
    --report "$BIOTEST_REF"  --label "BioTest Run 6 (baseline)" \
    --sut htsjdk --format VCF
else
  py -3.12 compares/scripts/measure_coverage.py \
    --report "$REPORT_XML" --label "EvoSuite (this run)" \
    --sut htsjdk --format VCF
fi
