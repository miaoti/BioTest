"""Parse a PIT run's `mutations.xml` into a DESIGN.md §4.5-compatible
`summary.json`:

    {
      "tool": "jazzer",
      "sut": "htsjdk",
      "format": "VCF" | "SAM",
      "phase": "mutation",
      "target_classes_n": int,   # classes in scope (fairness-recipe)
      "classes_with_mutations": int,
      "total_mutations": int,
      "killed": int,
      "survived": int,
      "no_coverage": int,
      "timed_out": int,
      "non_viable": int,
      "memory_error": int,
      "run_error": int,
      "reachable": int,          # killed + survived + timed_out + no_coverage
      "score": float,             # killed / reachable
      "by_class_top5": [{"class": ..., "killed": k, "reachable": r, "score": ...}],
      "corpus_dir": str,
      "baseline_json": str,
      "mutations_xml": str
    }

PIT's mutations.xml lines:

    <mutation detected='true' status='KILLED' numberOfTestsRun='1'>
      <sourceFile>VCFCodec.java</sourceFile>
      <mutatedClass>htsjdk.variant.vcf.VCFCodec</mutatedClass>
      <mutatedMethod>parseSingleAltAllele</mutatedMethod>
      ...
      <mutator>org.pitest.mutationtest.engine.gregor.mutators.NegateConditionalsMutator</mutator>
      ...
    </mutation>

Statuses observed: KILLED, SURVIVED, NO_COVERAGE, TIMED_OUT, NON_VIABLE,
MEMORY_ERROR, RUN_ERROR.
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


def summarise(report_dir: Path) -> dict:
    xml_path = report_dir / "mutations.xml"
    if not xml_path.exists():
        raise FileNotFoundError(f"no mutations.xml under {report_dir}")
    tree = ET.parse(xml_path)
    root = tree.getroot()

    status_counter: Counter[str] = Counter()
    by_class_killed: dict[str, int] = defaultdict(int)
    by_class_reachable: dict[str, int] = defaultdict(int)
    classes_with_mutations: set[str] = set()

    for m in root.findall("mutation"):
        status = m.attrib.get("status", "UNKNOWN").upper()
        status_counter[status] += 1
        mc = m.findtext("mutatedClass") or ""
        classes_with_mutations.add(mc)
        # Reachable = KILLED + SURVIVED + TIMED_OUT (TIMED_OUT counts as
        # killed in some PIT variants, but we keep it as its own bucket
        # and follow the conservative DESIGN.md §3.3 definition:
        # reachable = mutants in code the corpus EXECUTED. NO_COVERAGE
        # is excluded because the test suite didn't reach them.)
        if status in {"KILLED", "SURVIVED", "TIMED_OUT"}:
            by_class_reachable[mc] += 1
            if status == "KILLED":
                by_class_killed[mc] += 1

    killed = status_counter["KILLED"]
    survived = status_counter["SURVIVED"]
    timed_out = status_counter["TIMED_OUT"]
    no_coverage = status_counter["NO_COVERAGE"]
    non_viable = status_counter["NON_VIABLE"]
    memory_error = status_counter["MEMORY_ERROR"]
    run_error = status_counter["RUN_ERROR"]
    reachable = killed + survived + timed_out
    score = (killed / reachable) if reachable else 0.0

    # Top-5 classes by reachable-mutant count — useful signal for the
    # MD report, highlights where the test suite actually drives test
    # coverage.
    top5 = sorted(
        (
            {
                "class": c,
                "killed": by_class_killed.get(c, 0),
                "reachable": r,
                "score": round(by_class_killed.get(c, 0) / r, 4) if r else 0.0,
            }
            for c, r in by_class_reachable.items()
        ),
        key=lambda d: (-d["reachable"], -d["killed"], d["class"]),
    )[:5]

    return {
        "classes_with_mutations": len(classes_with_mutations),
        "total_mutations": sum(status_counter.values()),
        "killed": killed,
        "survived": survived,
        "no_coverage": no_coverage,
        "timed_out": timed_out,
        "non_viable": non_viable,
        "memory_error": memory_error,
        "run_error": run_error,
        "reachable": reachable,
        "score": round(score, 6),
        "by_class_top5": top5,
    }


def _cli() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--report-dir", type=Path, required=True)
    ap.add_argument("--corpus-dir", type=Path, required=True)
    ap.add_argument("--baseline-json", type=Path, required=True)
    ap.add_argument("--target-classes-n", type=int, required=True)
    ap.add_argument("--fmt", required=True, choices=["VCF", "SAM"])
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    summary = summarise(args.report_dir)
    out = {
        "tool": "jazzer",
        "sut": "htsjdk",
        "format": args.fmt,
        "phase": "mutation",
        "target_classes_n": args.target_classes_n,
        **summary,
        "corpus_dir": str(args.corpus_dir.resolve()),
        "baseline_json": str(args.baseline_json.resolve()),
        "mutations_xml": str((args.report_dir / "mutations.xml").resolve()),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[summarise] {args.fmt}/htsjdk "
        f"killed={out['killed']}/{out['reachable']} "
        f"score={out['score']*100:.2f}%  "
        f"(survived={out['survived']} no_coverage={out['no_coverage']} "
        f"timed_out={out['timed_out']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
