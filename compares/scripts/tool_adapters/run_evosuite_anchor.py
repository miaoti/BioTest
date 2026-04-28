"""EvoSuite bug-bench anchor adapter.

Implements Magma-style detection: generate a JUnit test suite with
EvoSuite against the POST-fix htsjdk version, then run those tests
against PRE-fix and POST-fix in turn. Tests that fail pre-fix AND
pass post-fix are saved under `failing-tests/` — they empirically
detected the target bug.

Why this replaces the legacy shell adapter: `compares/scripts/run_evosuite.sh`
is a Windows-only coverage-parity sweep (hard-codes `C:/Users/.../java`,
rc=127s on Linux) that never writes `failing-tests/`. Every cell in the
previous run scored miss because of that, not because the budget was too
short. See `PHASE4_BASELINE_FIXES.md §1.1`.

Contract matches the driver's `_invoke_evosuite_anchor` dict result:
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
EVOSUITE_ROOT = REPO_ROOT / "compares" / "baselines" / "evosuite"
EVOSUITE_JAR = EVOSUITE_ROOT / "source" / "evosuite-1.2.0.jar"
FATJAR_DIR = EVOSUITE_ROOT / "fatjar"
JUNIT_JAR = EVOSUITE_ROOT / "test-deps" / "junit-4.13.2.jar"
HAMCREST_JAR = EVOSUITE_ROOT / "test-deps" / "hamcrest-core-1.3.jar"

JAVA = os.environ.get("EVOSUITE_JAVA", "/usr/bin/java")
JAVAC = os.environ.get("EVOSUITE_JAVAC", "/usr/bin/javac")

JAVA_OPENS = [
    "--add-opens=java.base/java.lang=ALL-UNNAMED",
    "--add-opens=java.base/java.util=ALL-UNNAMED",
    "--add-opens=java.base/java.io=ALL-UNNAMED",
    "--add-opens=java.base/java.net=ALL-UNNAMED",
    "--add-opens=java.base/java.text=ALL-UNNAMED",
    "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
    "--add-opens=java.desktop/java.awt=ALL-UNNAMED",
]

# Bug → EvoSuite target class. Chosen to match the area each fix touches
# per manifest.verified.json::trigger.description. If a bug isn't in this
# map the default AbstractVCFCodec is used.
BUG_TO_TARGET: dict[str, str] = {
    # VCF bugs (Chat 1)
    "htsjdk-1554": "htsjdk.variant.variantcontext.VariantContext",
    "htsjdk-1637": "htsjdk.variant.variantcontext.VariantContextComparator",
    "htsjdk-1364": "htsjdk.variant.vcf.AbstractVCFCodec",
    "htsjdk-1389": "htsjdk.variant.vcf.VCFEncoder",
    "htsjdk-1372": "htsjdk.variant.vcf.AbstractVCFCodec",
    "htsjdk-1401": "htsjdk.variant.vcf.VCFHeader",
    "htsjdk-1403": "htsjdk.variant.variantcontext.VariantContextBuilder",
    "htsjdk-1418": "htsjdk.variant.vcf.VCFContigHeaderLine",
    "htsjdk-1544": "htsjdk.variant.variantcontext.VariantContext",
    # SAM bugs (Chat 2 — manifest revision 2026-04-21)
    # 1238: comma in @SQ SN: violates RNAME regex; SAMSequenceRecord ctor throws.
    "htsjdk-1238": "htsjdk.samtools.SAMSequenceRecord",
    # 1360: zero-length read with SEQ=*,QUAL=* — STRICT EMPTY_READ on SAMRecord parse.
    "htsjdk-1360": "htsjdk.samtools.SAMRecord",
    # 1410: |TLEN| > 2^29 — STRICT MAX_INSERT_SIZE check on SAMRecord.
    "htsjdk-1410": "htsjdk.samtools.SAMRecord",
}
# Default chosen heuristically by format if available; both classes are
# top-level parser entry points within their respective subsystems.
DEFAULT_TARGET_VCF = "htsjdk.variant.vcf.AbstractVCFCodec"
DEFAULT_TARGET_SAM = "htsjdk.samtools.SAMRecord"
# Backward-compat alias used by callers; format-aware lookup happens below.
DEFAULT_TARGET = DEFAULT_TARGET_VCF


def _project_cp(primary_jar: Path) -> str:
    """Build EvoSuite -projectCP with the primary htsjdk jar + transitive deps.

    EvoSuite's instrumenting classloader walks class hierarchies during
    `ComputeClassWriter.getCommonSuperClass`. If a parent class isn't
    resolvable on the classpath it throws an opaque "Class not found"
    NPE (see htsjdk-1372 / htsjdk-1364 failure mode, 2026-04-21). Include
    every supporting jar from the EvoSuite deps directory to make
    type resolution robust across htsjdk versions.
    """
    parts = [str(primary_jar)]
    deps_dir = EVOSUITE_ROOT / "deps"
    if deps_dir.is_dir():
        parts.extend(str(p) for p in sorted(deps_dir.glob("*.jar")))
    return os.pathsep.join(parts)


def _generate_tests(
    target_class: str, post_jar: Path, work_dir: Path, search_budget_s: int,
    log_fh,
) -> Path | None:
    """Run EvoSuite on POST-fix; return the per-class ESTest dir or None."""
    work_dir.mkdir(parents=True, exist_ok=True)
    project_cp = _project_cp(post_jar)
    evosuite_cmd = [
        JAVA, *JAVA_OPENS,
        "-jar", str(EVOSUITE_JAR),
        "-class", target_class,
        "-projectCP", project_cp,
        f"-Dsearch_budget={search_budget_s}",
        "-Dstopping_condition=MaxTime",
        "-Dclient_on_thread=true",
        "-Dsandbox=false",
        "-Dminimize=true",
        "-Dassertions=true",
        "-Dshow_progress=false",
        "-Dprint_to_system=true",
        "-Dminimization_timeout=60",
        "-Dassertion_timeout=60",
        "-Dextra_timeout=60",
        "-Dinitialization_timeout=120",
        "-generateMOSuite",
        "-criterion", "BRANCH:LINE",
    ]
    log_fh.write(f"[evosuite-anchor] generate: {' '.join(evosuite_cmd)}\n")
    log_fh.flush()
    try:
        subprocess.run(
            evosuite_cmd, cwd=work_dir,
            stdout=log_fh, stderr=subprocess.STDOUT,
            timeout=search_budget_s + 600,
        )
    except subprocess.TimeoutExpired:
        log_fh.write("[evosuite-anchor] generation TIMEOUT\n")
        log_fh.flush()
    tests_root = work_dir / "evosuite-tests"
    if not tests_root.exists():
        log_fh.write("[evosuite-anchor] no evosuite-tests/ produced\n")
        return None
    # Each class produces <class>_ESTest.java + <class>_ESTest_scaffolding.java
    rel_parts = target_class.split(".")
    target_dir = tests_root.joinpath(*rel_parts[:-1])
    estest = target_dir / f"{rel_parts[-1]}_ESTest.java"
    scaffold = target_dir / f"{rel_parts[-1]}_ESTest_scaffolding.java"
    if not estest.is_file() or not scaffold.is_file():
        log_fh.write(f"[evosuite-anchor] expected {estest} + scaffolding missing\n")
        return None
    return tests_root


def _compile_tests(
    tests_root: Path, classes_out: Path, classpath: list[Path], log_fh,
) -> bool:
    classes_out.mkdir(parents=True, exist_ok=True)
    srcs = [str(p) for p in tests_root.rglob("*.java")]
    if not srcs:
        return False
    cp_str = os.pathsep.join(str(p) for p in classpath)
    cmd = [JAVAC, "-cp", cp_str, "-d", str(classes_out), *srcs]
    log_fh.write(f"[evosuite-anchor] compile ({len(srcs)} srcs) -> {classes_out}\n")
    log_fh.flush()
    proc = subprocess.run(cmd, stdout=log_fh, stderr=subprocess.STDOUT, timeout=300)
    if proc.returncode != 0:
        log_fh.write(f"[evosuite-anchor] javac rc={proc.returncode}\n")
        return False
    return True


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
            # Log only a short summary line per test
            last = proc.stdout.strip().splitlines()[-3:] if proc.stdout else []
            log_fh.write(
                f"[evosuite-anchor] junit {fqn} rc={proc.returncode} "
                f"pass={passed} | {' // '.join(last)[:200]}\n"
            )
            result[fqn] = passed
        except subprocess.TimeoutExpired:
            log_fh.write(f"[evosuite-anchor] junit {fqn} TIMEOUT\n")
            result[fqn] = False
        log_fh.flush()
    return result


def _collect_test_fqns(tests_root: Path) -> list[str]:
    """Return FQNs of *_ESTest.java under tests_root, skipping scaffolding."""
    out: list[str] = []
    for p in tests_root.rglob("*_ESTest.java"):
        rel = p.relative_to(tests_root).with_suffix("")
        fqn = ".".join(rel.parts)
        out.append(fqn)
    return out


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
    tests_copy = out_dir / "evosuite-tests"
    failing_dir = out_dir / "failing-tests"
    failing_dir.mkdir(exist_ok=True)
    log_file = out_dir / "tool.log"

    pre_jar = FATJAR_DIR / f"htsjdk-{pre_ver}.jar"
    post_jar = FATJAR_DIR / f"htsjdk-{post_ver}.jar"
    fmt = (bug.get("format") or "VCF").upper()
    fmt_default = DEFAULT_TARGET_SAM if fmt == "SAM" else DEFAULT_TARGET_VCF
    target_class = BUG_TO_TARGET.get(bug_id, fmt_default)

    result: dict[str, Any] = {
        "tool": "evosuite_anchor",
        "sut": bug.get("sut"),
        "bug_id": bug_id,
        "target_class": target_class,
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
            f"[evosuite-anchor] bug={bug_id} target={target_class} "
            f"pre={pre_ver} post={post_ver} budget={time_budget_s}s\n"
        )
        if not pre_jar.is_file() or not post_jar.is_file():
            result["exit_code"] = 2
            result["error"] = f"missing jar(s): pre={pre_jar.exists()} post={post_jar.exists()}"
            result["notes"] = result["error"]
            result["ended_at"] = time.time()
            log_fh.write(f"[evosuite-anchor] {result['notes']}\n")
            return result

        # Budget split: 70% generation, 10% compile, 20% junit runs (pre+post)
        search_budget = max(60, int(time_budget_s * 0.70))

        tests_root = _generate_tests(
            target_class, post_jar, work_dir, search_budget, log_fh,
        )
        if tests_root is None:
            result["exit_code"] = 3
            result["error"] = "EvoSuite generation produced no tests (see tool.log for ASM/instrumentation errors)"
            result["notes"] = result["error"]
            result["ended_at"] = time.time()
            return result

        # Snapshot tests so the cell is self-describing even after work_dir cleanup
        try:
            if tests_copy.exists():
                shutil.rmtree(tests_copy)
            shutil.copytree(tests_root, tests_copy)
        except Exception as e:
            log_fh.write(f"[evosuite-anchor] tests snapshot skipped: {e}\n")

        # Compile once per jar because the compiled classes reference the
        # concrete htsjdk API of that jar. Include EvoSuite deps so junit
        # runs don't NoClassDefFoundError when the generated tests walk
        # into htsjdk methods that transit through commons-logging etc.
        cp_base = [EVOSUITE_JAR, JUNIT_JAR, HAMCREST_JAR]
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
        log_fh.write(f"[evosuite-anchor] {len(test_fqns)} test class(es) generated\n")

        # Run against post-fix first (sanity — expect most passes)
        post_pass = _run_junit(test_fqns, classes_post, cp_base + [post_jar], log_fh)
        if pre_compile_ok:
            pre_pass = _run_junit(
                test_fqns, classes_pre, cp_base + [pre_jar], log_fh,
            )
        else:
            # Tests couldn't compile against pre-fix API — that itself is a
            # strong signal of a detection-worthy API change. Treat every
            # test as pre-failing.
            pre_pass = {fqn: False for fqn in test_fqns}
            result["notes"] += " pre-fix compile failed (API drift); "

        # Tests detected a pre→post behavioural change iff pre_pass[fqn]
        # is False AND post_pass[fqn] is True.
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
                    log_fh.write(f"[evosuite-anchor] copy fail {fqn}: {e}\n")
        result["trigger_input"] = first_trigger
        log_fh.write(
            f"[evosuite-anchor] detected={len(detected)}/{len(test_fqns)} "
            f"(pre_pass={result['pre_pass_count']} post_pass={result['post_pass_count']})\n"
        )

    result["ended_at"] = time.time()
    # Persist the full adapter dict alongside tool.log so a post-run
    # sweep can recover pre/post pass counts even if the driver
    # overwrites the main result.json (see PHASE4_BASELINE_FIXES.md §1.1
    # driver-replay override for evosuite_anchor).
    try:
        (out_dir / "adapter_result.json").write_text(
            json.dumps(result, indent=2, default=str), encoding="utf-8",
        )
    except Exception:
        pass
    return result
