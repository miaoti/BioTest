#!/usr/bin/env bash
# Fetch baseline sources for the comparative evaluation.
#
# Usage:
#   bash compares/scripts/fetch_sources.sh                    # fetch all
#   bash compares/scripts/fetch_sources.sh evosuite           # fetch one
#   bash compares/scripts/fetch_sources.sh evosuite randoop   # fetch listed
#
# Targets download into compares/baselines/<name>/source/ (gitignored).
# This script is a placeholder — URLs and exact artifact names pinned in
# compares/DESIGN.md §5 must be verified before the first live fetch.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASELINES_DIR="$(cd "$HERE/../baselines" && pwd)"

# Pinned versions — keep in sync with DESIGN.md §5.
EVOSUITE_VERSION="1.2.0"
RANDOOP_VERSION="4.3.3"

fetch_evosuite() {
  local dst="$BASELINES_DIR/evosuite/source"
  mkdir -p "$dst"
  local url="https://github.com/EvoSuite/evosuite/releases/download/v${EVOSUITE_VERSION}/evosuite-${EVOSUITE_VERSION}.jar"
  echo "[evosuite] fetching $url"
  curl -L --fail -o "$dst/evosuite-${EVOSUITE_VERSION}.jar" "$url"
  echo "[evosuite] OK -> $dst/evosuite-${EVOSUITE_VERSION}.jar"
}

fetch_randoop() {
  local dst="$BASELINES_DIR/randoop/source"
  mkdir -p "$dst"
  local url="https://github.com/randoop/randoop/releases/download/v${RANDOOP_VERSION}/randoop-all-${RANDOOP_VERSION}.jar"
  echo "[randoop] fetching $url"
  curl -L --fail -o "$dst/randoop-all-${RANDOOP_VERSION}.jar" "$url"
  echo "[randoop] OK -> $dst/randoop-all-${RANDOOP_VERSION}.jar"
}

fetch_random_testing() {
  # Pure-random baseline is in-tree; nothing to download.
  echo "[random_testing] implemented in baselines/random_testing/ — no fetch needed"
}

dispatch() {
  case "$1" in
    evosuite) fetch_evosuite ;;
    randoop) fetch_randoop ;;
    random_testing|random) fetch_random_testing ;;
    *) echo "unknown target: $1" >&2; exit 2 ;;
  esac
}

main() {
  if [[ $# -eq 0 ]]; then
    fetch_evosuite
    fetch_randoop
    fetch_random_testing
  else
    for t in "$@"; do dispatch "$t"; done
  fi
}

main "$@"
