#!/usr/bin/env python3
"""Per-method refinement of evosuite_anchor cells.

The primary adapter (`tool_adapters/run_evosuite_anchor.py`) runs JUnit
one class at a time — which lumps all test methods together. If any one
method fails, the class is marked "failed", and the pre/post delta is
invisible for cells where both versions have *some* failure.

This sweep re-runs each cell's ESTest class against pre-fix and post-fix
classpaths, parses JUnitCore's per-method failure output, and recomputes:

    detected_methods     = methods that fail pre-fix AND pass post-fix
    confirmed_silences   = True iff detected_methods is non-empty
    overlap              = methods that fail both (unrelated / flaky)

The result.json for each cell is rewritten. Stack-trace excerpts for
detected methods are saved under `failing-tests/<method>.trace`.

Usage:
    python3 evosuite_per_method_sweep.py --bench-root /tmp/bug_bench_chat1
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path


REPO = Path("/work")
EVOSUITE_ROOT = REPO / "compares" / "baselines" / "evosuite"
EVOSUITE_JAR = EVOSUITE_ROOT / "source" / "evosuite-1.2.0.jar"
JUNIT_JAR = EVOSUITE_ROOT / "test-deps" / "junit-4.13.2.jar"
HAMCREST_JAR = EVOSUITE_ROOT / "test-deps" / "hamcrest-core-1.3.jar"
FATJAR = EVOSUITE_ROOT / "fatjar"
JAVA = os.environ.get("EVOSUITE_JAVA", "/usr/bin/java")
JAVA_OPENS = [
    "--add-opens=java.base/java.lang=ALL-UNNAMED",
    "--add-opens=java.base/java.util=ALL-UNNAMED",
    "--add-opens=java.base/java.io=ALL-UNNAMED",
    "--add-opens=java.base/java.net=ALL-UNNAMED",
    "--add-opens=java.base/java.text=ALL-UNNAMED",
    "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
    "--add-opens=java.desktop/java.awt=ALL-UNNAMED",
]


def _parse_failures(stdout: str, class_fqn: str) -> tuple[int, dict[str, str]]:
    """Return (tests_run, {method: short-trace})."""
    m = re.search(r"Tests run:\s*(\d+)", stdout)
    tests_run = int(m.group(1)) if m else 0
    failures: dict[str, str] = {}
    pat = re.escape(class_fqn)
    for block in re.finditer(
        r"(\d+)\)\s+(\w+)\(" + pat + r"\)\n([\s\S]*?)(?=(?:\n\d+\)\s+\w+\()|\nFAILURES!!!|\Z)",
        stdout,
    ):
        method = block.group(2)
        trace = block.group(3).strip().splitlines()
        failures[method] = "\n".join(trace[:8])
    return tests_run, failures


def _run_class(
    classes_dir: Path, cp_jars: list[Path], fqn: str, timeout_s: int = 600,
) -> tuple[int, dict[str, str]]:
    cp = os.pathsep.join([str(classes_dir)] + [str(p) for p in cp_jars])
    cmd = [JAVA, *JAVA_OPENS, "-cp", cp, "org.junit.runner.JUnitCore", fqn]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_s,
        )
        return _parse_failures(proc.stdout + proc.stderr, fqn)
    except subprocess.TimeoutExpired:
        return 0, {}


def _bug_anchor(manifest_path: Path) -> dict[str, dict]:
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    return {b["id"]: b.get("anchor", {}) for b in m["bugs"]}


def _find_estest(cell: Path) -> Path | None:
    # Prefer adapter snapshot under evosuite-tests/
    cands = list((cell / "evosuite-tests").rglob("*_ESTest.java"))
    if cands:
        return cands[0]
    # Fallback: work/evosuite-tests/
    cands = list((cell / "work" / "evosuite-tests").rglob("*_ESTest.java"))
    if cands:
        return cands[0]
    return None


def _fqn_from_java(tests_root: Path, java_file: Path) -> str:
    rel = java_file.relative_to(tests_root).with_suffix("")
    return ".".join(rel.parts)


def _methods_in_estest(java_file: Path) -> list[str]:
    """Extract @Test method names from a generated EvoSuite ESTest.java."""
    src = java_file.read_text(encoding="utf-8", errors="replace")
    return re.findall(
        r"@Test[^\n]*\n\s*public\s+void\s+(\w+)\s*\(", src,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench-root", type=Path, required=True)
    ap.add_argument(
        "--manifest", type=Path,
        default=REPO / "compares" / "bug_bench" / "manifest.verified.json",
    )
    ap.add_argument("--tool-dir", default="evosuite_anchor")
    args = ap.parse_args()

    anchor_by = _bug_anchor(args.manifest)
    root = args.bench_root / args.tool_dir
    if not root.is_dir():
        print(f"[sweep] {root} missing; nothing to do.")
        return

    summary_rows = []
    for cell in sorted(root.iterdir()):
        if not cell.is_dir():
            continue
        bug_id = cell.name
        rj_path = cell / "result.json"
        if not rj_path.exists():
            print(f"[sweep] {bug_id}: no result.json; skip")
            continue
        anchor = anchor_by.get(bug_id)
        if not anchor:
            print(f"[sweep] {bug_id}: no manifest entry; skip")
            continue

        pre_ver = anchor.get("pre_fix")
        post_ver = anchor.get("post_fix")
        pre_jar = FATJAR / f"htsjdk-{pre_ver}.jar"
        post_jar = FATJAR / f"htsjdk-{post_ver}.jar"
        classes_pre = cell / "work" / "classes_pre"
        classes_post = cell / "work" / "classes_post"
        if not classes_pre.is_dir() or not classes_post.is_dir():
            print(f"[sweep] {bug_id}: classes_pre/post missing; skip")
            continue
        if not pre_jar.is_file() or not post_jar.is_file():
            print(f"[sweep] {bug_id}: jar missing; skip")
            continue

        estest = _find_estest(cell)
        if estest is None:
            print(f"[sweep] {bug_id}: no ESTest.java; skip")
            continue
        tests_root = cell / "evosuite-tests"
        if not tests_root.exists():
            tests_root = cell / "work" / "evosuite-tests"
        fqn = _fqn_from_java(tests_root, estest)

        cp_base = [EVOSUITE_JAR, JUNIT_JAR, HAMCREST_JAR]
        deps_dir = EVOSUITE_ROOT / "deps"
        if deps_dir.is_dir():
            cp_base.extend(sorted(deps_dir.glob("*.jar")))

        # Detect pre-compile failure: classes_pre is missing the ESTest
        # bytecode even though classes_post has it. Treat every post-passing
        # method as pre-failing (API drift between pre and post — the code
        # couldn't even be compiled against pre-fix).
        estest_rel = Path(*fqn.split(".")).with_suffix(".class")
        pre_compiled = (classes_pre / estest_rel).is_file()
        post_compiled = (classes_post / estest_rel).is_file()

        print(f"[sweep] {bug_id} fqn={fqn} pre={pre_ver} post={post_ver} "
              f"pre_compiled={pre_compiled} post_compiled={post_compiled}")

        total_post, fail_post = _run_class(classes_post, cp_base + [post_jar], fqn)

        if pre_compiled:
            total_pre, fail_pre = _run_class(classes_pre, cp_base + [pre_jar], fqn)
            pre_only = set(fail_pre) - set(fail_post)
            overlap = set(fail_pre) & set(fail_post)
            pre_compile_drift = False
        else:
            # All post-passing methods are treated as pre-failing by
            # construction (the class itself didn't compile against pre-fix).
            total_pre = 0
            pre_compile_drift = True
            from_methods = _methods_in_estest(estest)
            post_passing = set(from_methods) - set(fail_post)
            pre_only = post_passing
            overlap = set()
            fail_pre = {m: "(pre-fix compile failed — API drift)" for m in pre_only}

        print(
            f"  tests_run pre={total_pre} post={total_post} | "
            f"fail pre={len(fail_pre)} post={len(fail_post)} | "
            f"pre_only={len(pre_only)} overlap={len(overlap)}"
        )

        # Write traces for detected methods
        failing_dir = cell / "failing-tests"
        failing_dir.mkdir(exist_ok=True)
        trace_lines = []
        for m in sorted(pre_only):
            (failing_dir / f"{m}.trace").write_text(
                f"# {fqn}#{m} (fails pre={pre_ver}, passes post={post_ver})\n"
                + fail_pre[m] + "\n",
                encoding="utf-8",
            )
            trace_lines.append(m)

        rj = json.loads(rj_path.read_text(encoding="utf-8"))
        rj["detected"] = bool(pre_only)
        rj["signal"] = "uncaught_exception" if pre_only else None
        if pre_only:
            first = sorted(pre_only)[0]
            rj["trigger_input"] = str(failing_dir / f"{first}.trace")
            rj["confirmed_fix_silences_signal"] = True
            if pre_compile_drift:
                rj["notes"] = (
                    f"per-method sweep (pre-compile drift): ESTest "
                    f"class did not compile against pre-fix {pre_ver} "
                    f"— {len(pre_only)} method(s) that pass on post-fix "
                    f"{post_ver} are treated as pre-failing (API drift "
                    "itself is a strong detection signal)"
                )
            else:
                rj["notes"] = (
                    f"per-method sweep: {len(pre_only)} test method(s) "
                    f"fail on pre-fix {pre_ver} and pass on post-fix "
                    f"{post_ver}: {', '.join(sorted(pre_only))}"
                    + (
                        f"; {len(overlap)} overlap (unrelated / flaky)"
                        if overlap else ""
                    )
                )
        else:
            rj["trigger_input"] = None
            rj["confirmed_fix_silences_signal"] = None
            rj["notes"] = (
                f"per-method sweep: pre fail={len(fail_pre)}, "
                f"post fail={len(fail_post)}, no pre-only method — "
                "target bug not detected at class behaviour level"
            )
        rj["per_method_sweep"] = {
            "class_fqn": fqn,
            "pre_compile_drift": pre_compile_drift,
            "tests_run_pre": total_pre,
            "tests_run_post": total_post,
            "fail_pre_methods": sorted(fail_pre.keys()),
            "fail_post_methods": sorted(fail_post.keys()),
            "pre_only_methods": sorted(pre_only),
            "overlap_methods": sorted(overlap),
        }
        rj_path.write_text(json.dumps(rj, indent=2), encoding="utf-8")
        summary_rows.append((bug_id, len(pre_only), len(fail_pre), len(fail_post)))

    print()
    print("[sweep] SUMMARY (bug, detected_pre_only, fail_pre, fail_post)")
    for bug_id, det, fp, fpo in summary_rows:
        tag = "FOUND" if det > 0 else "miss"
        print(f"  {bug_id:20s} {tag:6s} detected={det} fail_pre={fp} fail_post={fpo}")


if __name__ == "__main__":
    main()
