#!/usr/bin/env bash
# Reproducible build for the BioTest htsjdk harness.
#
# Pins -source 17 -target 17 so a JDK 21 host produces the same class
# bytecode as a JDK 17 container. Without this pin, a host rebuild
# leaves Java-21 class files (version 65.0) that the 17-JVM
# biotest-bench image refuses to load (UnsupportedClassVersionError).
#
# Inputs  : harnesses/java/BioTestHarness.java
# Classpath source: compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar
#   (a Maven-distributed, Java-17-compatible shaded htsjdk bundle)
# Outputs : harnesses/java/build/classes/BioTestHarness.class
#           harnesses/java/build/libs/biotest-harness-all.jar
#             (fatjar; Main-Class: BioTestHarness; contains htsjdk + deps)
#
# Usage:
#   bash harnesses/java/build.sh
#
# Invariants verified by the script:
#   1. javac is available and can target Java 17
#   2. the fatjar exists (populated by prepare_sut_install_envs.sh or
#      evosuite setup)
#   3. the resulting .class has class-file version 0x3D (61) = Java 17
#   4. the packaged fatjar has a valid Main-Class manifest entry

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
FATJAR_DEPS="${ROOT}/compares/baselines/evosuite/fatjar/htsjdk-with-deps.jar"
BUILD="${SCRIPT_DIR}/build"
CLASSES="${BUILD}/classes"
LIBS="${BUILD}/libs"
UNPACK="${BUILD}/unpack"
OUT_JAR="${LIBS}/biotest-harness-all.jar"
SRC="${SCRIPT_DIR}/BioTestHarness.java"

if ! command -v javac >/dev/null 2>&1; then
    echo "[harness-java] ERROR: javac not on PATH" >&2
    exit 1
fi
if [[ ! -f "${FATJAR_DEPS}" ]]; then
    echo "[harness-java] ERROR: classpath fatjar missing at" >&2
    echo "                      ${FATJAR_DEPS}" >&2
    echo "                      Run the evosuite prep pipeline first." >&2
    exit 1
fi
if [[ ! -f "${SRC}" ]]; then
    echo "[harness-java] ERROR: source missing at ${SRC}" >&2
    exit 1
fi

mkdir -p "${CLASSES}" "${LIBS}"

# cd into the source directory and feed javac a relative filename so
# MSYS / Git-Bash on Windows doesn't rewrite `/c/Users/...` into
# `\c\Users\...` (the MSYS_NO_PATHCONV=1 guard only covers docker's
# own argv, not downstream processes). Relative paths bypass MSYS
# path conversion entirely.
echo "[harness-java] javac -source 17 -target 17"
cd "${SCRIPT_DIR}"
javac -source 17 -target 17 \
    -cp "${FATJAR_DEPS}" \
    -d "${CLASSES}" \
    BioTestHarness.java

# Sanity-check the produced class-file version. Java 17 = 61 = 0x3D.
HEADER=$(od -An -c -N 8 "${CLASSES}/BioTestHarness.class" | head -1)
if [[ "${HEADER}" != *'\0   ='* ]]; then
    echo "[harness-java] WARN: class-file header is ${HEADER}; expected trailing '\\0 ='" >&2
fi

echo "[harness-java] rebuilding fatjar (Main-Class: BioTestHarness)"
rm -rf "${UNPACK}"
mkdir -p "${UNPACK}"
cd "${UNPACK}"
# Unpack the Java-17-compatible htsjdk + deps into build/unpack,
# then drop in the freshly-compiled BioTestHarness.class, then pack.
jar xf "${FATJAR_DEPS}"
cp "${CLASSES}/BioTestHarness.class" .

# Manifest with a valid Main-Class — otherwise `java -jar …` fails
# with 'no main manifest attribute'.
mkdir -p META-INF
cat > META-INF/MANIFEST.MF <<MANIFEST
Manifest-Version: 1.0
Main-Class: BioTestHarness

MANIFEST

cd "${SCRIPT_DIR}"
rm -f "${OUT_JAR}"
jar cfm "${OUT_JAR}" "${UNPACK}/META-INF/MANIFEST.MF" -C "${UNPACK}" .

echo "[harness-java] done — wrote ${OUT_JAR}"
echo "[harness-java] size: $(du -h "${OUT_JAR}" | cut -f1)"
echo "[harness-java] class version (first 8 bytes):"
od -An -c -N 8 "${CLASSES}/BioTestHarness.class" | head -1
