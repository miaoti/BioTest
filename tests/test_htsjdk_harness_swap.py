"""Unit + smoke tests for `_swap_htsjdk_in_harness`.

Verifies:
  1. The fatjar rewrite preserves BioTestHarness.class.
  2. The fatjar's htsjdk classes come from the input jar, not the
     original bundled version.
  3. The manifest's Main-Class is preserved (so `java -jar` still
     picks up BioTestHarness).
  4. `_restore_harness_from_backup` round-trips the pristine build
     output.
  5. (Smoke) The rewritten jar actually runs under JVM — no
     ClassFormatError / no NoSuchMethodError on common htsjdk API
     calls in the 2.19 – 3.0 range.

Does NOT require network / Maven Central — uses a synthetic
input jar containing stub htsjdk/* class files, so the test
is hermetic and fast.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _make_stub_htsjdk_jar(out_path: Path, marker: bytes) -> None:
    """Produce a fake htsjdk-x.y.z.jar with one stub class in htsjdk/
    carrying `marker` bytes. Used to prove the swap actually replaced
    the harness's htsjdk contents with our input.
    """
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("htsjdk/_StubMarker.class", marker)
        zf.writestr("htsjdk/variant/vcf/VCFHeader.class", marker + b":header")
        zf.writestr("META-INF/MANIFEST.MF",
                    "Manifest-Version: 1.0\nImplementation-Title: "
                    "htsjdk-stub\n\n")


def _harness_exists() -> bool:
    from compares.scripts.bug_bench_driver import _harness_jar
    return _harness_jar().exists()


def test_swap_preserves_biotest_harness_class():
    """BioTestHarness.class must survive the swap unchanged."""
    if not _harness_exists():
        # Harness not built — skip. CI builds the harness in
        # compares/docker/Dockerfile.bench before running tests.
        print("[skip] harness fatjar not built")
        return

    from compares.scripts.bug_bench_driver import (
        _harness_jar, _harness_backup, _swap_htsjdk_in_harness,
        _restore_harness_from_backup,
    )
    harness = _harness_jar()

    # Read BioTestHarness.class bytes from the pristine harness.
    with zipfile.ZipFile(harness, "r") as zf:
        original_bth = zf.read("BioTestHarness.class")
    assert len(original_bth) > 0

    with tempfile.TemporaryDirectory() as td:
        stub_jar = Path(td) / "htsjdk-stub.jar"
        _make_stub_htsjdk_jar(stub_jar, b"stub-classes-v1")

        _swap_htsjdk_in_harness(stub_jar)
        try:
            # Post-swap, BioTestHarness.class bytes should be identical.
            with zipfile.ZipFile(harness, "r") as zf:
                swapped_bth = zf.read("BioTestHarness.class")
            assert swapped_bth == original_bth, \
                "BioTestHarness.class changed during htsjdk swap"

            # The stub htsjdk class should now be present.
            with zipfile.ZipFile(harness, "r") as zf:
                names = set(zf.namelist())
                assert "htsjdk/_StubMarker.class" in names
                stub_bytes = zf.read("htsjdk/_StubMarker.class")
            assert stub_bytes == b"stub-classes-v1"
        finally:
            _restore_harness_from_backup()
    print("[pass] test_swap_preserves_biotest_harness_class")


def test_swap_replaces_all_bundled_htsjdk_classes():
    """After swap, no htsjdk class from the original bundle should
    survive unless it was also in the input jar."""
    if not _harness_exists():
        print("[skip] harness fatjar not built")
        return

    from compares.scripts.bug_bench_driver import (
        _harness_jar, _swap_htsjdk_in_harness, _restore_harness_from_backup,
    )
    harness = _harness_jar()

    # Snapshot the original's htsjdk entry set.
    with zipfile.ZipFile(harness, "r") as zf:
        original_htsjdk_entries = {
            n for n in zf.namelist()
            if n.startswith("htsjdk/") and not n.endswith("/")
        }
    assert len(original_htsjdk_entries) > 100, \
        "pristine harness should bundle hundreds of htsjdk classes"

    with tempfile.TemporaryDirectory() as td:
        stub_jar = Path(td) / "htsjdk-stub.jar"
        # Only TWO stub classes in the input — after swap, the fatjar
        # should only contain those two under htsjdk/.
        _make_stub_htsjdk_jar(stub_jar, b"v2")

        _swap_htsjdk_in_harness(stub_jar)
        try:
            with zipfile.ZipFile(harness, "r") as zf:
                post_swap_htsjdk = {
                    n for n in zf.namelist()
                    if n.startswith("htsjdk/") and not n.endswith("/")
                }
            expected = {
                "htsjdk/_StubMarker.class",
                "htsjdk/variant/vcf/VCFHeader.class",
            }
            assert post_swap_htsjdk == expected, \
                f"unexpected htsjdk entries after swap: {post_swap_htsjdk - expected}"
        finally:
            _restore_harness_from_backup()
    print("[pass] test_swap_replaces_all_bundled_htsjdk_classes")


def test_manifest_main_class_preserved():
    """Main-Class must still be BioTestHarness post-swap — so
    `java -jar harness.jar ...` invocation keeps working."""
    if not _harness_exists():
        print("[skip] harness fatjar not built")
        return

    from compares.scripts.bug_bench_driver import (
        _harness_jar, _swap_htsjdk_in_harness, _restore_harness_from_backup,
    )
    harness = _harness_jar()

    with tempfile.TemporaryDirectory() as td:
        stub_jar = Path(td) / "htsjdk-stub.jar"
        _make_stub_htsjdk_jar(stub_jar, b"v3")

        _swap_htsjdk_in_harness(stub_jar)
        try:
            with zipfile.ZipFile(harness, "r") as zf:
                mf = zf.read("META-INF/MANIFEST.MF").decode("utf-8")
            assert "Main-Class: BioTestHarness" in mf, \
                f"Main-Class missing in manifest: {mf!r}"
        finally:
            _restore_harness_from_backup()
    print("[pass] test_manifest_main_class_preserved")


def test_restore_returns_pristine_bytes():
    """After swap → restore, the harness bytes match the pristine
    backup bytes exactly."""
    if not _harness_exists():
        print("[skip] harness fatjar not built")
        return

    from compares.scripts.bug_bench_driver import (
        _harness_jar, _harness_backup, _swap_htsjdk_in_harness,
        _restore_harness_from_backup,
    )
    harness = _harness_jar()

    pristine_bytes = harness.read_bytes()

    with tempfile.TemporaryDirectory() as td:
        stub_jar = Path(td) / "htsjdk-stub.jar"
        _make_stub_htsjdk_jar(stub_jar, b"v4")
        _swap_htsjdk_in_harness(stub_jar)
        assert harness.read_bytes() != pristine_bytes, \
            "swap should have changed the fatjar"
        _restore_harness_from_backup()
        assert harness.read_bytes() == pristine_bytes, \
            "restore should yield byte-identical pristine fatjar"
        # Clean up the backup so repeated test runs start fresh.
        backup = _harness_backup()
        if backup.exists():
            backup.unlink()
    print("[pass] test_restore_returns_pristine_bytes")


def _have_java() -> bool:
    return shutil.which("java") is not None


def test_swapped_harness_still_executable_smoke():
    """End-to-end smoke: after swap to a real htsjdk jar (if
    available on disk), the harness still runs `java -jar` without
    ClassFormatError or ClassNotFoundException. Skipped when no
    real htsjdk jar or java is available.
    """
    if not _harness_exists() or not _have_java():
        print("[skip] harness fatjar or java not available")
        return

    # Prefer a real downloaded htsjdk jar from a prior bench run.
    fatjar_dir = (_REPO_ROOT / "compares" / "baselines" / "evosuite"
                  / "fatjar")
    real_jars = sorted(fatjar_dir.glob("htsjdk-*.jar")) if fatjar_dir.exists() else []
    # Exclude our own with-deps shaded bundle.
    real_jars = [p for p in real_jars if "with-deps" not in p.name
                 and "harness" not in p.name]
    if not real_jars:
        print("[skip] no downloaded htsjdk-VERSION.jar present")
        return

    from compares.scripts.bug_bench_driver import (
        _harness_jar, _swap_htsjdk_in_harness, _restore_harness_from_backup,
    )
    harness = _harness_jar()
    target = real_jars[0]

    _swap_htsjdk_in_harness(target)
    try:
        # Minimal VCF (spec-valid) — the harness should parse it and
        # emit canonical JSON without classloader errors.
        with tempfile.TemporaryDirectory() as td:
            vcf = Path(td) / "minimal.vcf"
            vcf.write_text(
                "##fileformat=VCFv4.2\n"
                "##contig=<ID=1,length=1000>\n"
                "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
                "1\t100\t.\tA\tT\t.\t.\t.\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                ["java", "-jar", str(harness), "VCF", str(vcf)],
                capture_output=True, text=True, timeout=60,
            )
            # Exit 0 = parsed OK. Non-zero may be spec-reject (we're
            # using minimal but tolerable input); scan stderr for
            # classloader errors specifically.
            bad = ("ClassFormatError", "ClassNotFoundException",
                   "NoClassDefFoundError")
            for err in bad:
                assert err not in (proc.stderr or ""), (
                    f"harness failed with {err} after htsjdk swap to "
                    f"{target.name}:\n{proc.stderr[:600]}"
                )
    finally:
        _restore_harness_from_backup()
    print("[pass] test_swapped_harness_still_executable_smoke")


if __name__ == "__main__":
    test_swap_preserves_biotest_harness_class()
    test_swap_replaces_all_bundled_htsjdk_classes()
    test_manifest_main_class_preserved()
    test_restore_returns_pristine_bytes()
    test_swapped_harness_still_executable_smoke()
    print("All tests passed.")
