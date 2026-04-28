"""Randoop bug-bench adapter.

Magma-style detection mirroring `run_evosuite_anchor.py`: generate a
JUnit regression suite with Randoop against the POST-fix htsjdk
version, then run those tests against PRE-fix and POST-fix in turn.
Tests that pass post-fix AND fail pre-fix are saved under
`failing-tests/` — they empirically detected the target bug.

Randoop is the feedback-directed random unit-test generator (Pacheco
et al., OOPSLA'07). It is a white-box, unit-level analogue of EvoSuite
and serves the same role here: a contextual anchor for "what white-box
unit-level Java fuzzing finds" against the same bug-bench. Listed in
DESIGN.md §2.3 as a secondary/optional baseline (kept documented even
though §4.1 doesn't include it in the slim matrix).

Contract matches the driver's dict result the same way EvoSuite's does:
    tool, sut, exit_code, started_at, ended_at,
    corpus_dir, crashes_dir, log_file, crash_count, trigger_input
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
RANDOOP_ROOT = REPO_ROOT / "compares" / "baselines" / "randoop"
RANDOOP_JAR = RANDOOP_ROOT / "source" / "randoop-all-4.3.3.jar"
# Reuse the EvoSuite anchor's pinned htsjdk fat-jars (per-version) and
# JUnit/Hamcrest deps. They were curated by the same Phase-0 setup —
# Randoop and EvoSuite operate on the same binaries.
EVOSUITE_ROOT = REPO_ROOT / "compares" / "baselines" / "evosuite"
FATJAR_DIR = EVOSUITE_ROOT / "fatjar"
JUNIT_JAR = EVOSUITE_ROOT / "test-deps" / "junit-4.13.2.jar"
HAMCREST_JAR = EVOSUITE_ROOT / "test-deps" / "hamcrest-core-1.3.jar"

JAVA = os.environ.get("RANDOOP_JAVA", os.environ.get("EVOSUITE_JAVA", "java"))
JAVAC = os.environ.get("RANDOOP_JAVAC", os.environ.get("EVOSUITE_JAVAC", "javac"))

# Reuse the same module-opens block EvoSuite needs. JDK 17+ closes
# reflection on java.base subpackages by default; Randoop's component
# manager + JUnit's assertion runner both need them open.
JAVA_OPENS = [
    "--add-opens=java.base/java.lang=ALL-UNNAMED",
    "--add-opens=java.base/java.util=ALL-UNNAMED",
    "--add-opens=java.base/java.io=ALL-UNNAMED",
    "--add-opens=java.base/java.net=ALL-UNNAMED",
    "--add-opens=java.base/java.text=ALL-UNNAMED",
    "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
    "--add-opens=java.desktop/java.awt=ALL-UNNAMED",
]

# Bug → Randoop --testclass list. Mirrors EvoSuite's BUG_TO_TARGET.
# Randoop accepts multiple --testclass flags; we use one focused class
# per bug (the area each fix touches per
# manifest.verified.json::trigger.description). Fall back to a
# format-aware default when a bug isn't mapped.
BUG_TO_TARGETS: dict[str, list[str]] = {
    # VCF bugs
    "htsjdk-1554": ["htsjdk.variant.variantcontext.VariantContext"],
    "htsjdk-1637": ["htsjdk.variant.variantcontext.VariantContextComparator"],
    "htsjdk-1364": ["htsjdk.variant.vcf.AbstractVCFCodec"],
    "htsjdk-1389": ["htsjdk.variant.vcf.VCFEncoder"],
    "htsjdk-1372": ["htsjdk.variant.vcf.AbstractVCFCodec"],
    "htsjdk-1401": ["htsjdk.variant.vcf.VCFHeader"],
    "htsjdk-1403": ["htsjdk.variant.variantcontext.VariantContextBuilder"],
    "htsjdk-1418": ["htsjdk.variant.vcf.VCFContigHeaderLine"],
    "htsjdk-1544": ["htsjdk.variant.variantcontext.VariantContext"],
    # SAM bugs (manifest revision 2026-04-21)
    "htsjdk-1238": ["htsjdk.samtools.SAMSequenceRecord"],
    "htsjdk-1360": ["htsjdk.samtools.SAMRecord"],
    "htsjdk-1410": ["htsjdk.samtools.SAMRecord"],
}
DEFAULT_TARGET_VCF = "htsjdk.variant.vcf.AbstractVCFCodec"
DEFAULT_TARGET_SAM = "htsjdk.samtools.SAMRecord"

# Randoop's default package for emitted JUnit classes. Keeps generated
# files inside a known subdir so the FQN/path mapping is unambiguous on
# both compile and JUnit-invocation sides.
JUNIT_PACKAGE = "randoop.bench"


def _project_cp(primary_jar: Path) -> list[Path]:
    """htsjdk fat jar + transitive deps from the EvoSuite deps dir.

    Same rationale as the EvoSuite anchor: type resolution needs every
    transitive jar on the classpath, otherwise Randoop's class-loading
    aborts with `ClassNotFoundException` mid-generation.
    """
    parts: list[Path] = [primary_jar]
    deps_dir = EVOSUITE_ROOT / "deps"
    if deps_dir.is_dir():
        parts.extend(sorted(deps_dir.glob("*.jar")))
    return parts


def _generate_tests(
    targets: list[str], post_jar: Path, work_dir: Path,
    time_limit_s: int, output_limit: int, log_fh,
) -> Path | None:
    """Run Randoop on POST-fix; return the per-suite tests dir or None."""
    work_dir.mkdir(parents=True, exist_ok=True)
    junit_out = work_dir / "randoop-tests"
    junit_out.mkdir(exist_ok=True)
    cp = [RANDOOP_JAR] + _project_cp(post_jar)
    cp_str = os.pathsep.join(str(p) for p in cp)

    cmd = [
        JAVA, *JAVA_OPENS,
        "-classpath", cp_str,
        "randoop.main.Main", "gentests",
        f"--time-limit={time_limit_s}",
        f"--output-limit={output_limit}",
        f"--junit-output-dir={junit_out}",
        f"--junit-package-name={JUNIT_PACKAGE}",
        # Randoop's default flaky-test policy aborts the whole run if it
        # detects nondeterminism. SUT parsers are usually deterministic
        # but htsjdk's caching codepaths occasionally read system clock /
        # tmpdir, which Randoop flags as flaky. OUTPUT keeps the rest of
        # the suite — flaky tests are tagged in the file but don't kill
        # the run.
        "--flaky-test-behavior=OUTPUT",
        # Bound suite size so compile + run stays cheap. 100 is plenty
        # for anchor-style detection.
        "--no-error-revealing-tests=false",
        "--no-regression-tests=false",
    ]
    for t in targets:
        cmd.append(f"--testclass={t}")

    log_fh.write(f"[randoop] generate: {' '.join(cmd)}\n")
    log_fh.flush()
    try:
        subprocess.run(
            cmd, cwd=work_dir,
            stdout=log_fh, stderr=subprocess.STDOUT,
            timeout=time_limit_s + 600,
        )
    except subprocess.TimeoutExpired:
        log_fh.write("[randoop] generation TIMEOUT\n")
        log_fh.flush()

    # Randoop emits *.java directly under junit_out/<package-as-dirs>/.
    pkg_dir = junit_out / Path(*JUNIT_PACKAGE.split("."))
    if not pkg_dir.is_dir():
        log_fh.write(f"[randoop] expected package dir {pkg_dir} missing\n")
        return None
    java_srcs = list(pkg_dir.glob("*.java"))
    if not java_srcs:
        log_fh.write(f"[randoop] no .java in {pkg_dir}\n")
        return None
    log_fh.write(f"[randoop] generated {len(java_srcs)} java source(s)\n")
    return junit_out


def _compile_tests(
    tests_root: Path, classes_out: Path, classpath: list[Path], log_fh,
) -> bool:
    classes_out.mkdir(parents=True, exist_ok=True)
    srcs = [str(p) for p in tests_root.rglob("*.java")]
    if not srcs:
        return False
    cp_str = os.pathsep.join(str(p) for p in classpath)
    cmd = [JAVAC, "-cp", cp_str, "-d", str(classes_out), *srcs]
    log_fh.write(f"[randoop] compile ({len(srcs)} srcs) -> {classes_out}\n")
    log_fh.flush()
    proc = subprocess.run(cmd, stdout=log_fh, stderr=subprocess.STDOUT, timeout=300)
    if proc.returncode != 0:
        log_fh.write(f"[randoop] javac rc={proc.returncode}\n")
        return False
    return True


def _collect_test_fqns(tests_root: Path) -> list[str]:
    """Return FQNs of compiled test classes (skipping inner classes).

    Randoop emits at minimum:
      RegressionTest.java     (suite that aggregates RegressionTest{0..N})
      RegressionTest0.java    (executable test class)
      ...
    and optionally ErrorTest.java + ErrorTest{0..N}.java when error-
    revealing tests are produced. We exclude the umbrella suites
    (RegressionTest / ErrorTest) — JUnit invocation runs each numbered
    leaf directly so we get a per-class pass/fail vector.
    """
    out: list[str] = []
    for p in tests_root.rglob("*.java"):
        rel = p.relative_to(tests_root).with_suffix("")
        fqn = ".".join(rel.parts)
        # Drop bare suite aggregators
        leaf = fqn.split(".")[-1]
        if leaf in {"RegressionTest", "ErrorTest"}:
            continue
        out.append(fqn)
    return out


def _run_junit(
    test_fqns: list[str], classes_dir: Path, classpath: list[Path], log_fh,
    timeout_s: int = 180,
) -> dict[str, bool]:
    """Run each JUnit test class; return {fqn: passed}."""
    result: dict[str, bool] = {}
    cp_str = os.pathsep.join([str(classes_dir)] + [str(p) for p in classpath])
    for fqn in test_fqns:
        cmd = [
            JAVA, *JAVA_OPENS,
            "-cp", cp_str,
            "org.junit.runner.JUnitCore", fqn,
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout_s,
            )
            passed = proc.returncode == 0
            last = proc.stdout.strip().splitlines()[-3:] if proc.stdout else []
            log_fh.write(
                f"[randoop] junit {fqn} rc={proc.returncode} "
                f"pass={passed} | {' // '.join(last)[:200]}\n"
            )
            result[fqn] = passed
        except subprocess.TimeoutExpired:
            log_fh.write(f"[randoop] junit {fqn} TIMEOUT\n")
            result[fqn] = False
        log_fh.flush()
    return result


def run_anchor(
    bug: dict[str, Any], out_dir: Path, time_budget_s: int,
) -> dict[str, Any]:
    started = time.time()
    bug_id = bug["id"]
    anchor = bug.get("anchor", {})
    pre_ver = anchor.get("pre_fix")
    post_ver = anchor.get("post_fix")

    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = out_dir / "work"
    tests_copy = out_dir / "randoop-tests"
    failing_dir = out_dir / "failing-tests"
    failing_dir.mkdir(exist_ok=True)
    log_file = out_dir / "tool.log"

    pre_jar = FATJAR_DIR / f"htsjdk-{pre_ver}.jar"
    post_jar = FATJAR_DIR / f"htsjdk-{post_ver}.jar"
    fmt = (bug.get("format") or "VCF").upper()
    fmt_default = DEFAULT_TARGET_SAM if fmt == "SAM" else DEFAULT_TARGET_VCF
    targets = BUG_TO_TARGETS.get(bug_id, [fmt_default])

    result: dict[str, Any] = {
        "tool": "randoop",
        "sut": bug.get("sut"),
        "bug_id": bug_id,
        "target_classes": targets,
        "pre_fix": pre_ver,
        "post_fix": post_ver,
        "corpus_dir": str(tests_copy),
        "crashes_dir": str(failing_dir),
        "log_file": str(log_file),
        "started_at": started,
        "exit_code": 0,
        "crash_count": 0,
        "trigger_input": None,
        "notes": "",
    }

    with log_file.open("a", encoding="utf-8") as log_fh:
        log_fh.write(
            f"[randoop] bug={bug_id} targets={targets} "
            f"pre={pre_ver} post={post_ver} budget={time_budget_s}s\n"
        )
        if not RANDOOP_JAR.is_file():
            result["exit_code"] = 2
            result["error"] = f"randoop jar missing: {RANDOOP_JAR}"
            result["notes"] = result["error"]
            result["ended_at"] = time.time()
            log_fh.write(f"[randoop] {result['notes']}\n")
            return result
        if not pre_jar.is_file() or not post_jar.is_file():
            result["exit_code"] = 2
            result["error"] = (
                f"missing jar(s): pre={pre_jar.exists()} "
                f"post={post_jar.exists()} (looked under {FATJAR_DIR})"
            )
            result["notes"] = result["error"]
            result["ended_at"] = time.time()
            log_fh.write(f"[randoop] {result['notes']}\n")
            return result

        # Budget split: 70 % generation, 30 % compile + JUnit pre/post
        gen_budget = max(60, int(time_budget_s * 0.70))
        # Cap suite size — Randoop will happily emit thousands. Compile
        # + JUnit-per-class scales linearly with this. 500 sequences is
        # the sweet spot: large enough to give longer time budgets
        # somewhere to land (Randoop hits output-limit=100 in ~3 s on
        # SAMSequenceRecord), small enough that JUnit replay across
        # ~5 RegressionTest{0..N} classes stays under a minute.
        output_limit = 500

        tests_root = _generate_tests(
            targets, post_jar, work_dir, gen_budget, output_limit, log_fh,
        )
        if tests_root is None:
            result["exit_code"] = 3
            result["error"] = "Randoop generation produced no tests (see tool.log)"
            result["notes"] = result["error"]
            result["ended_at"] = time.time()
            return result

        # Snapshot tests so the cell is self-describing even after work_dir cleanup
        try:
            if tests_copy.exists():
                shutil.rmtree(tests_copy)
            shutil.copytree(tests_root, tests_copy)
        except Exception as e:
            log_fh.write(f"[randoop] tests snapshot skipped: {e}\n")

        # Compile against post-fix (always) and pre-fix (best-effort —
        # API drift between versions can fail compilation against pre-
        # fix, which itself is a strong signal).
        cp_base = [JUNIT_JAR, HAMCREST_JAR]
        deps_dir = EVOSUITE_ROOT / "deps"
        if deps_dir.is_dir():
            cp_base.extend(sorted(deps_dir.glob("*.jar")))
        classes_post = work_dir / "classes_post"
        classes_pre = work_dir / "classes_pre"

        if not _compile_tests(tests_root, classes_post, cp_base + [post_jar], log_fh):
            result["exit_code"] = 4
            result["error"] = "javac failed against post-fix classpath"
            result["notes"] = result["error"]
            result["ended_at"] = time.time()
            return result

        pre_compile_ok = _compile_tests(
            tests_root, classes_pre, cp_base + [pre_jar], log_fh,
        )

        test_fqns = _collect_test_fqns(tests_root)
        result["tests_generated"] = len(test_fqns)
        log_fh.write(f"[randoop] {len(test_fqns)} test class(es) generated\n")

        # Run against post-fix first (sanity — expect most pass)
        post_pass = _run_junit(test_fqns, classes_post, cp_base + [post_jar], log_fh)
        if pre_compile_ok:
            pre_pass = _run_junit(
                test_fqns, classes_pre, cp_base + [pre_jar], log_fh,
            )
        else:
            # Pre-fix compile failure is itself a strong API-drift signal
            # — mirror EvoSuite's treatment by counting every test as
            # pre-failing.
            pre_pass = {fqn: False for fqn in test_fqns}
            result["notes"] += " pre-fix compile failed (API drift); "

        # Pre→post behavioural change iff pre fails AND post passes.
        detected: list[str] = []
        for fqn in test_fqns:
            if post_pass.get(fqn, False) and not pre_pass.get(fqn, False):
                detected.append(fqn)

        result["pre_pass_count"] = sum(1 for v in pre_pass.values() if v)
        result["post_pass_count"] = sum(1 for v in post_pass.values() if v)
        result["detected_test_fqns"] = detected
        result["crash_count"] = len(detected)

        # Copy each detected test under failing-tests/ so the driver's
        # detection predicate picks them up via crashes_dir scan.
        first_trigger = None
        for fqn in detected:
            rel = Path(*fqn.split(".")).with_suffix(".java")
            src = tests_root / rel
            if src.is_file():
                dst = failing_dir / rel.name
                try:
                    shutil.copy2(src, dst)
                    if first_trigger is None:
                        first_trigger = str(dst)
                except Exception as e:
                    log_fh.write(f"[randoop] copy fail {fqn}: {e}\n")
        result["trigger_input"] = first_trigger
        log_fh.write(
            f"[randoop] detected={len(detected)}/{len(test_fqns)} "
            f"(pre_pass={result['pre_pass_count']} "
            f"post_pass={result['post_pass_count']})\n"
        )

    result["ended_at"] = time.time()
    try:
        (out_dir / "adapter_result.json").write_text(
            json.dumps(result, indent=2, default=str), encoding="utf-8",
        )
    except Exception:
        pass
    return result


# Convenience CLI for ad-hoc runs (matches the cargo_fuzz adapter shape).
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Randoop bug-bench adapter")
    p.add_argument("--bug-id", required=True,
                   help="bug id from manifest.verified.json (e.g. htsjdk-1238)")
    p.add_argument("--manifest", type=Path,
                   default=REPO_ROOT/"compares"/"bug_bench"/"manifest.verified.json")
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--time-budget-s", type=int, default=600)
    args = p.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    bug = next((b for b in manifest["bugs"] if b["id"] == args.bug_id), None)
    if bug is None:
        raise SystemExit(f"bug {args.bug_id} not in {args.manifest}")
    res = run_anchor(bug, args.out_dir, args.time_budget_s)
    print(json.dumps(res, indent=2, default=str))
