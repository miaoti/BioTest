#!/usr/bin/env bash
# Drive EvoSuite 1.2.0 across BioTest's VCF-scope target classes.
#
# Fairness protocol vs BioTest Run 6 (170 min total wall clock):
#   - Target classes = EXACTLY the 54 classes admitted by the 3-path
#     weighted VCF coverage filter used for BioTest's 46.9% measurement.
#   - Per-class wall time capped at ~3 min; total ~160 min.
#   - EvoSuite uses a single fat JAR with htsjdk + every transitive dep
#     so its custom InstrumentingClassLoader can resolve every type it
#     encounters during ASM frame computation.
#   - Runs under Temurin JDK 17 (not the JDK 21 BioTest uses) because
#     EvoSuite 1.2.0's shaded ASM cannot read class file major version
#     65 (Java 21). htsjdk version chosen accordingly: 2.24.1, the
#     last release with Java 8 bytecode.
#
# Output: per-class log + EvoSuite's evosuite-tests/ tree (cwd-relative,
# EvoSuite ignores -base_dir for some reason).
# Successes/failures are tallied on stdout.

set -u

ROOT_UNIX="/c/Users/miaot/Github/BioTest"
ROOT_WIN="C:/Users/miaot/Github/BioTest"
JDK17="$ROOT_WIN/compares/baselines/evosuite/jdk17/jdk-17.0.13+11"
EVO="$ROOT_WIN/compares/baselines/evosuite/source/evosuite-1.2.0.jar"
HTSJDK_FAT="$ROOT_WIN/compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar"

LOG_DIR="$ROOT_UNIX/compares/baselines/evosuite/results/logs"
WORK_DIR="$ROOT_UNIX/compares/baselines/evosuite/results/work"
mkdir -p "$LOG_DIR" "$WORK_DIR"

# EvoSuite writes evosuite-tests/ under cwd, not -base_dir, so we cd
# into a stable working dir to keep all generated tests together.
cd "$WORK_DIR"

# Per-class flags. search_budget drives most of wall time.
# Pass SEARCH_BUDGET=<sec> in the env to override; default 30 s
# (matches Run 1 rapid sweep). For the 170-min parity re-run, export
# SEARCH_BUDGET=180 before calling this script.
SEARCH_BUDGET="${SEARCH_BUDGET:-30}"
MINIM_TO="${MINIM_TO:-20}"
ASSERT_TO="${ASSERT_TO:-20}"
EXTRA_TO="${EXTRA_TO:-20}"
INIT_TO="${INIT_TO:-60}"
ES_FLAGS=(
  -generateMOSuite -criterion BRANCH:LINE
  -Dclient_on_thread=true -Dsandbox=false
  "-Dsearch_budget=$SEARCH_BUDGET" -Dstopping_condition=MaxTime
  "-Dminimization_timeout=$MINIM_TO" "-Dassertion_timeout=$ASSERT_TO"
  "-Dextra_timeout=$EXTRA_TO" "-Dinitialization_timeout=$INIT_TO"
  -Dminimize=true -Dassertions=false
  -Dprint_to_system=true -Dshow_progress=false
)

JAVA_OPENS=(
  --add-opens java.base/java.lang=ALL-UNNAMED
  --add-opens java.base/java.util=ALL-UNNAMED
  --add-opens java.base/java.io=ALL-UNNAMED
  --add-opens java.base/java.net=ALL-UNNAMED
  --add-opens java.desktop/java.awt=ALL-UNNAMED
)

CLASSES=(
  htsjdk.variant.vcf.AbstractVCFCodec
  htsjdk.variant.vcf.VCF3Codec
  htsjdk.variant.vcf.VCF3Parser
  htsjdk.variant.vcf.VCF4Parser
  htsjdk.variant.vcf.VCFAltHeaderLine
  htsjdk.variant.vcf.VCFCodec
  htsjdk.variant.vcf.VCFCompoundHeaderLine
  htsjdk.variant.vcf.VCFConstants
  htsjdk.variant.vcf.VCFContigHeaderLine
  htsjdk.variant.vcf.VCFEncoder
  htsjdk.variant.vcf.VCFFileReader
  htsjdk.variant.vcf.VCFFilterHeaderLine
  htsjdk.variant.vcf.VCFFormatHeaderLine
  htsjdk.variant.vcf.VCFHeader
  htsjdk.variant.vcf.VCFHeaderLine
  htsjdk.variant.vcf.VCFHeaderLineCount
  htsjdk.variant.vcf.VCFHeaderLineTranslator
  htsjdk.variant.vcf.VCFHeaderLineType
  htsjdk.variant.vcf.VCFHeaderVersion
  htsjdk.variant.vcf.VCFIDHeaderLine
  htsjdk.variant.vcf.VCFInfoHeaderLine
  htsjdk.variant.vcf.VCFIterator
  htsjdk.variant.vcf.VCFIteratorBuilder
  htsjdk.variant.vcf.VCFLineParser
  htsjdk.variant.vcf.VCFMetaHeaderLine
  htsjdk.variant.vcf.VCFPassThruTextTransformer
  htsjdk.variant.vcf.VCFPedigreeHeaderLine
  htsjdk.variant.vcf.VCFPercentEncodedTextTransformer
  htsjdk.variant.vcf.VCFReader
  htsjdk.variant.vcf.VCFRecordCodec
  htsjdk.variant.vcf.VCFSampleHeaderLine
  htsjdk.variant.vcf.VCFSimpleHeaderLine
  htsjdk.variant.vcf.VCFStandardHeaderLines
  htsjdk.variant.vcf.VCFTextTransformer
  htsjdk.variant.vcf.VCFUtils
  htsjdk.variant.variantcontext.Allele
  htsjdk.variant.variantcontext.CommonInfo
  htsjdk.variant.variantcontext.FastGenotype
  htsjdk.variant.variantcontext.Genotype
  htsjdk.variant.variantcontext.GenotypeBuilder
  htsjdk.variant.variantcontext.GenotypeLikelihoods
  htsjdk.variant.variantcontext.GenotypeNumLikelihoodsCache
  htsjdk.variant.variantcontext.GenotypeType
  htsjdk.variant.variantcontext.GenotypesContext
  htsjdk.variant.variantcontext.LazyGenotypesContext
  htsjdk.variant.variantcontext.SimpleAllele
  htsjdk.variant.variantcontext.StructuralVariantType
  htsjdk.variant.variantcontext.VariantContext
  htsjdk.variant.variantcontext.VariantContextBuilder
  htsjdk.variant.variantcontext.VariantContextComparator
  htsjdk.variant.variantcontext.VariantContextUtils
  htsjdk.variant.variantcontext.writer.VCFWriter
  htsjdk.variant.variantcontext.writer.VariantContextWriter
  htsjdk.variant.variantcontext.writer.VariantContextWriterBuilder
)

N=${#CLASSES[@]}
echo "[driver] Launching EvoSuite on $N VCF-scope classes."
echo "[driver] JDK: $("$JDK17/bin/java" -version 2>&1 | head -1)"
echo "[driver] EvoSuite jar: $EVO"
echo "[driver] htsjdk fat jar: $HTSJDK_FAT ($(du -h "$HTSJDK_FAT" 2>/dev/null | awk '{print $1}'))"
echo "[driver] search_budget=${SEARCH_BUDGET}s  minim=${MINIM_TO}s  assert=${ASSERT_TO}s  extra=${EXTRA_TO}s  init=${INIT_TO}s"
echo "[driver] Projected wall (if 34 successes): $((34 * (SEARCH_BUDGET + 30) / 60)) min (BioTest Run 6 = 170 min)"
echo "[driver] CWD for evosuite-tests/: $WORK_DIR"

T_START=$(date +%s)
PASS=0
FAIL=0
NOGOAL=0

for i in "${!CLASSES[@]}"; do
  cls="${CLASSES[$i]}"
  log="$LOG_DIR/${cls}.log"
  n=$(( i + 1 ))
  elapsed=$(( $(date +%s) - T_START ))
  echo
  echo "[driver] ($n/$N, elapsed $(( elapsed / 60 ))m$(( elapsed % 60 ))s) === $cls ==="

  # Make sure no stray Java procs are hogging RAM between classes.
  taskkill -F -IM java.exe 2>/dev/null > /dev/null
  sleep 1

  "$JDK17/bin/java" "${JAVA_OPENS[@]}" \
    -jar "$EVO" \
    -class "$cls" \
    -projectCP "$HTSJDK_FAT" \
    "${ES_FLAGS[@]}" \
    > "$log" 2>&1
  rc=$?

  tpath="$WORK_DIR/evosuite-tests/${cls//./\/}_ESTest.java"
  if [[ -f "$tpath" ]]; then
    PASS=$(( PASS + 1 ))
    loc=$(wc -l < "$tpath")
    echo "[driver]   OK rc=$rc, test file $loc LOC"
  elif grep -q "Total number of test goals for DYNAMOSA: 0" "$log" 2>/dev/null; then
    NOGOAL=$(( NOGOAL + 1 ))
    echo "[driver]   SKIP rc=$rc, class has 0 reachable goals (trivial)"
  else
    FAIL=$(( FAIL + 1 ))
    snippet=$(grep -E "Class not found|Error|Exception" "$log" 2>/dev/null | head -1)
    echo "[driver]   FAIL rc=$rc — ${snippet:-no test file produced}"
  fi
done

TOTAL=$(( $(date +%s) - T_START ))
echo
echo "[driver] DONE — pass=$PASS  trivial=$NOGOAL  fail=$FAIL  total_wall=$(( TOTAL / 60 ))m$(( TOTAL % 60 ))s"
echo "[driver] Tests landed in: $WORK_DIR/evosuite-tests/"
n_tests=$(find "$WORK_DIR/evosuite-tests" -name "*ESTest.java" 2>/dev/null | wc -l)
echo "[driver] Total test files generated: $n_tests"
