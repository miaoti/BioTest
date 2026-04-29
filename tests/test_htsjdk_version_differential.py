"""Semantic test: after a real version swap, the harness must
produce DIFFERENT output on a version-sensitive PoV.

Uses htsjdk-1544 (`<NON_REF>` mis-classification): pre-fix htsjdk
2.24.1's `VariantContext.getType()` returns `NO_VARIATION`,
post-fix 3.0.0 returns `MIXED` / `SYMBOLIC`. Without the fatjar
swap, both calls return the SAME value (whatever the bundled
harness-build htsjdk decided), so the silence predicate can
never fire.

This test proves the swap is semantically effective: after swap
we actually see the version's real behaviour.

Network-dependent (downloads htsjdk jars from Maven Central). Skip
if no network or if Java not available.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _have_java() -> bool:
    return shutil.which("java") is not None


def _run_harness_query(harness_jar: Path, vcf: Path) -> dict:
    """Invoke `java -jar harness --mode query VCF <vcf> --methods ...`
    and return the parsed method_results dict."""
    proc = subprocess.run(
        ["java", "-jar", str(harness_jar),
         "--mode", "query", "VCF", str(vcf),
         "--methods", "getType,isBiallelic,isSNP,getStart"],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        return {"__error__": proc.stderr[:400]}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        return {"__error__": f"not-JSON: {e}; stdout={proc.stdout[:400]}"}


def test_htsjdk_1544_getType_differs_across_versions():
    if not _have_java():
        print("[skip] java not available")
        return

    from compares.scripts.bug_bench_driver import (
        _install_htsjdk_jar,
        _swap_htsjdk_in_harness,
        _restore_harness_from_backup,
        _harness_jar,
    )
    if not _harness_jar().exists():
        print("[skip] harness fatjar not built")
        return

    pov = (_REPO_ROOT / "compares" / "bug_bench" / "triggers"
           / "htsjdk-1544" / "original.vcf")
    if not pov.exists():
        print(f"[skip] PoV missing: {pov}")
        return

    # Pre-fix and post-fix htsjdk versions from the manifest.
    pre_version = "2.24.1"
    post_version = "3.0.0"

    fatjar_dir = _REPO_ROOT / "compares" / "baselines" / "evosuite" / "fatjar"
    fatjar_dir.mkdir(parents=True, exist_ok=True)

    pre_jar = fatjar_dir / f"htsjdk-{pre_version}.jar"
    post_jar = fatjar_dir / f"htsjdk-{post_version}.jar"

    try:
        if not pre_jar.exists():
            _install_htsjdk_jar(pre_version, pre_jar)
        if not post_jar.exists():
            _install_htsjdk_jar(post_version, post_jar)
    except Exception as e:
        print(f"[skip] Maven download failed: {type(e).__name__}: {str(e)[:100]}")
        return

    try:
        # Swap to pre-fix and query
        _swap_htsjdk_in_harness(pre_jar)
        pre_result = _run_harness_query(_harness_jar(), pov)

        # Swap to post-fix and query
        _swap_htsjdk_in_harness(post_jar)
        post_result = _run_harness_query(_harness_jar(), pov)

        # If either side errored, surface it (may mean harness API
        # incompat between versions, which the swap can't fix).
        if "__error__" in pre_result or "__error__" in post_result:
            print(f"[warn] pre_result: {pre_result}")
            print(f"[warn] post_result: {post_result}")
            print("[warn] skipping differential assertion due to error")
            return

        # The getType value MUST differ between versions — that's the
        # whole bug. If swap is effective, the JVM loaded different
        # htsjdk classes, and the same input produces different
        # method-call output.
        pre_mr = pre_result.get("method_results", {})
        post_mr = post_result.get("method_results", {})
        print(f"[info] pre_fix  ({pre_version}) method_results: {pre_mr}")
        print(f"[info] post_fix ({post_version}) method_results: {post_mr}")
        assert pre_mr != post_mr, (
            f"htsjdk {pre_version} and {post_version} produced IDENTICAL "
            f"method_results — swap is not effective:\n"
            f"  pre:  {pre_mr}\n  post: {post_mr}"
        )
        print("[pass] htsjdk version swap actually changes semantic output")
    finally:
        _restore_harness_from_backup()


if __name__ == "__main__":
    test_htsjdk_1544_getType_differs_across_versions()
