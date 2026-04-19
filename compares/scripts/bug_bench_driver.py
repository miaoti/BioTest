"""Phase-4 orchestrator for the real-bug benchmark.

Modes:
    --verify-only        pre-flight install-verification only (no fuzzing)
    (default)            full bug-bench run

For every verified bug in the manifest, for every tool eligible for the
bug's SUT row (see DESIGN.md §4.1):
    1. Install the pre-fix SUT version (pip / Maven / git checkout).
    2. Run the tool for --time-budget-s seconds against the pre-fix SUT.
    3. Record TTFB + detection outcome.
    4. Install the post-fix version; replay the detecting input;
       confirm the signal disappears.
    5. Write per-(tool, bug) JSON under --out.

The tool-adapter contract is defined in `tool_adapters/_base.py`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
ADAPTERS_DIR = REPO_ROOT / "compares" / "scripts" / "tool_adapters"

# Ensure adapter module imports resolve.
sys.path.insert(0, str(ADAPTERS_DIR))

# Row membership per DESIGN.md §4.1 slim matrix.
# seqan3 uses AFL++ (GCC + afl-g++) instead of libFuzzer (Clang) because
# Clang 18 rejects seqan3 3.x concept constraints — see §9 Risk 1.
MATRIX: dict[str, list[str]] = {
    "htsjdk":    ["biotest", "jazzer", "pure_random", "evosuite_anchor"],
    "pysam":     ["biotest", "atheris", "pure_random"],
    "biopython": ["biotest", "atheris", "pure_random"],
    "seqan3":    ["biotest", "aflpp", "pure_random"],
}


@dataclass
class BugResult:
    tool: str
    bug_id: str
    sut: str
    detected: bool
    ttfb_s: float | None
    trigger_input: str | None
    signal: str | None
    confirmed_fix_silences_signal: bool | None
    adapter_exit_code: int
    notes: str = ""


# ---------- SUT install helpers ---------------------------------------

def _install_pysam(version: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--force-reinstall",
         f"pysam=={version}"],
        check=True,
    )


def _install_biopython(version: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--force-reinstall",
         f"biopython=={version}"],
        check=True,
    )


def _install_htsjdk_jar(version: str, out_path: Path) -> None:
    """Download the versioned htsjdk JAR from Maven Central."""
    url = ("https://repo.maven.apache.org/maven2/com/github/samtools/htsjdk/"
           f"{version}/htsjdk-{version}.jar")
    subprocess.run(["curl", "-L", "-o", str(out_path), url], check=True)


def _checkout_seqan3(commit: str, seqan3_src_dir: Path) -> None:
    subprocess.run(
        ["git", "-C", str(seqan3_src_dir), "checkout", "-f", commit],
        check=True,
    )


def install_sut(sut: str, anchor: dict[str, Any], which: str) -> None:
    """Install the pre-fix or post-fix SUT version in the current env."""
    if anchor.get("type") == "feature_gap":
        raise RuntimeError("feature_gap entries should be pre-filtered out")
    version = anchor[which]
    if version in ("PENDING_VERIFICATION", "N/A") or "PENDING" in str(version):
        raise RuntimeError(
            f"anchor.{which}={version!r} is unverified; run --verify-only first")

    if sut == "pysam":
        _install_pysam(version)
    elif sut == "biopython":
        _install_biopython(version)
    elif sut == "htsjdk":
        # Drop the versioned JAR into a known path the htsjdk runner uses.
        dest = REPO_ROOT / "compares" / "baselines" / "evosuite" / "fatjar" / (
            f"htsjdk-{version}.jar")
        dest.parent.mkdir(parents=True, exist_ok=True)
        _install_htsjdk_jar(version, dest)
    elif sut == "seqan3":
        seqan3_src = REPO_ROOT / "compares" / "baselines" / "seqan3" / "source"
        if not seqan3_src.exists():
            raise RuntimeError(
                f"seqan3 source not found at {seqan3_src}; clone first")
        _checkout_seqan3(version, seqan3_src)
    else:
        raise RuntimeError(f"unknown sut: {sut}")


# ---------- Verification ----------------------------------------------

def verify_bug(bug: dict[str, Any]) -> tuple[bool, str]:
    """Confirm pre-fix and post-fix are both installable.

    Does NOT run the fuzzer; just exercises the install step.
    """
    anchor = bug["anchor"]
    if anchor.get("type") == "feature_gap":
        return False, "feature_gap: drop"
    pre = anchor.get("pre_fix", "")
    post = anchor.get("post_fix", "")
    if "PENDING" in pre or "PENDING" in post or pre in ("", "N/A") or post in ("", "N/A"):
        return False, (
            f"pending verification (pre_fix={pre!r} post_fix={post!r}); "
            f"rule: {anchor.get('verification_rule')}"
        )

    try:
        install_sut(bug["sut"], anchor, "pre_fix")
        install_sut(bug["sut"], anchor, "post_fix")
    except Exception as e:
        return False, f"install failed: {e}"
    return True, "installable"


# ---------- Adapter dispatch ------------------------------------------

def invoke_adapter(
    tool: str, bug: dict[str, Any], out_dir: Path, time_budget_s: int,
    seed_corpus: Path,
) -> dict[str, Any]:
    """Dispatch to the named adapter; return its JSON result."""
    if tool == "biotest":
        from run_biotest import run as _run  # type: ignore
    elif tool == "jazzer":
        from run_jazzer import run as _run  # type: ignore
    elif tool == "atheris":
        from run_atheris import run as _run  # type: ignore
    elif tool == "libfuzzer":
        from run_libfuzzer import run as _run  # type: ignore
    elif tool == "aflpp":
        from run_aflpp import run as _run  # type: ignore
    elif tool == "pure_random":
        from run_pure_random import run as _run  # type: ignore
    elif tool == "evosuite_anchor":
        # Delegate to the existing shell-based EvoSuite pipeline.
        return _invoke_evosuite_anchor(bug, out_dir, time_budget_s)
    else:
        raise RuntimeError(f"unknown tool {tool!r}")

    result = _run(
        sut=bug["sut"],
        seed_corpus=seed_corpus,
        out_dir=out_dir,
        time_budget_s=time_budget_s,
        format_hint=bug.get("format", "VCF"),
    )
    return result.to_json()


def _invoke_evosuite_anchor(
    bug: dict[str, Any], out_dir: Path, time_budget_s: int
) -> dict[str, Any]:
    script = REPO_ROOT / "compares" / "scripts" / "run_evosuite.sh"
    log_file = out_dir / "tool.log"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_file.touch()
    started = time.time()
    try:
        subprocess.run(
            ["bash", str(script), "--budget", str(time_budget_s),
             "--out", str(out_dir)],
            timeout=time_budget_s + 60, check=False,
            stdout=log_file.open("ab"), stderr=subprocess.STDOUT,
        )
        exit_code = 0
    except subprocess.TimeoutExpired:
        exit_code = -1
    except Exception:
        exit_code = 1
    ended = time.time()
    return {
        "tool": "evosuite_anchor",
        "sut": bug["sut"],
        "exit_code": exit_code,
        "started_at": started,
        "ended_at": ended,
        "corpus_dir": str(out_dir / "evosuite-tests"),
        "crashes_dir": str(out_dir / "failing-tests"),
        "log_file": str(log_file),
    }


# ---------- Detection predicate ---------------------------------------

def detection_from_adapter(
    adapter_json: dict[str, Any], bug: dict[str, Any],
) -> tuple[bool, float | None, str | None, str | None]:
    """Compute (detected, ttfb_s, trigger_input_path, signal) from adapter output.

    This is a minimal implementation. For a crash-finding tool we trust
    the adapter's crash count. For BioTest we would additionally parse
    its DET report — TODO hook that up during Phase-0 smoke test.
    """
    crashes = adapter_json.get("crash_count", 0)
    if crashes > 0:
        duration = float(adapter_json.get("ended_at", 0)
                         - adapter_json.get("started_at", 0))
        # TTFB estimation: without per-crash timestamps we use mid-point.
        ttfb = duration * 0.5
        crashes_dir = Path(adapter_json.get("crashes_dir", ""))
        sample = next(iter(crashes_dir.glob("*"))) if crashes_dir.exists() else None
        return (
            True,
            ttfb,
            str(sample) if sample else None,
            bug.get("expected_signal", {}).get("type", "crash"),
        )
    return False, None, None, None


# ---------- Main loop -------------------------------------------------

def run_bench(
    manifest_path: Path,
    out_root: Path,
    time_budget_s: int,
    seed_corpus_vcf: Path,
    seed_corpus_sam: Path,
    only_sut: str | None = None,
    only_tool: str | None = None,
) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out_root.mkdir(parents=True, exist_ok=True)
    aggregate: list[dict[str, Any]] = []

    for bug in manifest.get("bugs", []):
        bug_id = bug["id"]
        sut = bug["sut"]
        if only_sut and sut != only_sut:
            continue

        ok, reason = verify_bug(bug)
        if not ok:
            print(f"[skip] {bug_id}: {reason}")
            continue

        # Install post-fix baseline first so reverting after run is cheap.
        install_sut(sut, bug["anchor"], "pre_fix")
        seed_corpus = (
            seed_corpus_vcf if bug.get("format") == "VCF" else seed_corpus_sam)

        for tool in MATRIX.get(sut, []):
            if only_tool and tool != only_tool:
                continue
            tool_out = out_root / tool / bug_id
            tool_out.mkdir(parents=True, exist_ok=True)
            print(f"[run] {tool} @ {bug_id}  t={time_budget_s}s")
            try:
                adapter_json = invoke_adapter(
                    tool, bug, tool_out, time_budget_s, seed_corpus,
                )
            except Exception:
                traceback.print_exc()
                adapter_json = {"exit_code": 99, "error": "adapter_raise"}

            detected, ttfb, trig, sig = detection_from_adapter(adapter_json, bug)

            confirmed = None
            if detected and trig:
                # Replay on post-fix to confirm silencing.
                try:
                    install_sut(sut, bug["anchor"], "post_fix")
                    confirmed = _replay_trigger_silenced(
                        sut, Path(trig), bug.get("format", "VCF")
                    )
                except Exception:
                    traceback.print_exc()
                    confirmed = None
                finally:
                    install_sut(sut, bug["anchor"], "pre_fix")

            record = BugResult(
                tool=tool,
                bug_id=bug_id,
                sut=sut,
                detected=detected,
                ttfb_s=ttfb,
                trigger_input=trig,
                signal=sig,
                confirmed_fix_silences_signal=confirmed,
                adapter_exit_code=int(adapter_json.get("exit_code", 0)),
            )
            (tool_out / "result.json").write_text(
                json.dumps(asdict(record), indent=2), encoding="utf-8"
            )
            aggregate.append(asdict(record))

    (out_root / "aggregate.json").write_text(
        json.dumps({"results": aggregate}, indent=2), encoding="utf-8"
    )
    print(f"[done] wrote {len(aggregate)} records to "
          f"{out_root/'aggregate.json'}")


def _replay_trigger_silenced(sut: str, trig_path: Path, fmt: str) -> bool:
    """Re-run the triggering input against the post-fix SUT; return True
    iff the signal has vanished."""
    # Minimal: call the repo's existing ParserRunner and check success.
    sys.path.insert(0, str(REPO_ROOT))
    try:
        if sut == "pysam":
            from test_engine.runners.pysam_runner import PysamRunner  # type: ignore
            r = PysamRunner().run(trig_path, fmt)
        elif sut == "biopython":
            from test_engine.runners.biopython_runner import BiopythonRunner  # type: ignore
            r = BiopythonRunner().run(trig_path, fmt)
        elif sut == "htsjdk":
            from test_engine.runners.htsjdk_runner import HTSJDKRunner  # type: ignore
            r = HTSJDKRunner().run(trig_path, fmt)
        elif sut == "seqan3":
            from test_engine.runners.seqan3_runner import SeqAn3Runner  # type: ignore
            r = SeqAn3Runner().run(trig_path, fmt)
        else:
            return False
        # Silenced means: post-fix SUT handles the trigger cleanly.
        return bool(r.success)
    finally:
        sys.path.pop(0)


def _verify_only(manifest_path: Path, out_path: Path | None) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    verified: list[str] = []
    dropped: list[dict[str, str]] = []
    for bug in manifest.get("bugs", []):
        ok, reason = verify_bug(bug)
        if ok:
            verified.append(bug["id"])
            print(f"[ok]   {bug['id']}")
        else:
            dropped.append({"id": bug["id"], "reason": reason})
            print(f"[drop] {bug['id']}: {reason}")
    print(f"\nSummary: {len(verified)} verified, {len(dropped)} dropped "
          f"of {len(manifest.get('bugs', []))} candidates.")
    if out_path:
        out_path.write_text(
            json.dumps({"verified": verified, "dropped": dropped}, indent=2),
            encoding="utf-8",
        )


# ---------- CLI -------------------------------------------------------

def _cli() -> None:
    p = argparse.ArgumentParser(description="Phase-4 bug-bench orchestrator")
    p.add_argument("--manifest", type=Path,
                   default=REPO_ROOT/"compares"/"bug_bench"/"manifest.json")
    p.add_argument("--out", type=Path,
                   default=REPO_ROOT/"compares"/"results"/"bug_bench")
    p.add_argument("--time-budget-s", type=int, default=7200)
    p.add_argument("--seed-corpus-vcf", type=Path,
                   default=REPO_ROOT/"seeds"/"vcf")
    p.add_argument("--seed-corpus-sam", type=Path,
                   default=REPO_ROOT/"seeds"/"sam")
    p.add_argument("--only-sut", default=None)
    p.add_argument("--only-tool", default=None)
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--dropped-out", type=Path, default=None,
                   help="write a verify summary JSON to this path")
    args = p.parse_args()

    if args.verify_only:
        _verify_only(args.manifest, args.dropped_out)
        return

    run_bench(
        manifest_path=args.manifest,
        out_root=args.out,
        time_budget_s=args.time_budget_s,
        seed_corpus_vcf=args.seed_corpus_vcf,
        seed_corpus_sam=args.seed_corpus_sam,
        only_sut=args.only_sut,
        only_tool=args.only_tool,
    )


if __name__ == "__main__":
    _cli()
