"""
Rank 5 — query-method consensus oracle.

For an MR with `behavior_target == API_QUERY_INVARIANCE`, voters return
scalar `method_results: {method_name: scalar_value}` maps for both x
and T(x) (instead of canonical-JSON parses). The oracle's task is:

  - For each method requested by the MR, compare its result on x and
    T(x) under deep_equal across every eligible voter.
  - Aggregate per-voter pass/fail into a consensus verdict.

Failure modes surfaced (mirrors `error_consensus`):

  - `query_changed`        — same SUT got different scalar results
                             on x and T(x). The MR claims the query is
                             invariant under T; this SUT contradicts it.
  - `cross_sut_disagreement` — SUTs disagreed about the result on x
                             (or on T(x)) — a differential bug.
  - `method_unavailable`   — runner reported `__error__` for a method.
                             Excluded from consensus voting.

Reference: Chen-Kuo-Liu-Tse (ACM CSUR 2018) §3.2 — API metamorphic
relations; MR-Scout (Xu et al., TOSEM 2024, arXiv:2304.07548) — the
canonical reference for query-method MR oracles.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Optional

from ..runners.base import RunnerResult
from .deep_equal import deep_equal


@dataclass
class QueryConsensusResult:
    """Outcome of a query-method consensus across voters."""
    # per-voter, per-method outcomes:
    #   value: True if x & T(x) agreed, False if they disagreed,
    #          None if method was unavailable on this runner.
    per_voter: dict[str, dict[str, Optional[bool]]] = field(default_factory=dict)
    # methods whose verdict was unanimous-agree across all voters
    methods_invariant: list[str] = field(default_factory=list)
    # methods where ≥1 voter said "value changed" (T broke the invariant)
    methods_changed: list[str] = field(default_factory=list)
    # methods where voters disagreed about the value on x (cross-SUT bug)
    methods_cross_sut_disagreement: list[str] = field(default_factory=list)
    # voters that contributed to a `methods_changed` flag — bug owners
    dissenting_voters: list[str] = field(default_factory=list)
    # overall pass: True if methods_changed and methods_cross_sut_disagreement
    # are both empty.
    passed: bool = True
    reason: str = ""


def _is_error(scalar: Any) -> bool:
    return isinstance(scalar, dict) and "__error__" in scalar


def _compare_scalar(a: Any, b: Any) -> bool:
    """True when two scalars are deep-equal under the framework's semantic
    comparison (handles bool/int/float/str/None and lists/dicts of same)."""
    eq, _ = deep_equal(a, b)
    return eq


def get_query_consensus(
    voter_results_x: dict[str, RunnerResult],
    voter_results_tx: dict[str, RunnerResult],
    method_names: list[str],
) -> QueryConsensusResult:
    """Build a query-consensus verdict from per-voter RunnerResults.

    Each voter's RunnerResult must contain
    `canonical_json["method_results"]` mapping method_name → scalar.
    Voters whose canonical_json is missing/None or that returned an
    error are silently excluded from voting on that method.
    """
    per_voter: dict[str, dict[str, Optional[bool]]] = {}

    # --- Step 1: per-voter, per-method "did x and T(x) agree?" ---
    for vname in voter_results_x.keys() | voter_results_tx.keys():
        rx = voter_results_x.get(vname)
        rt = voter_results_tx.get(vname)
        per_voter[vname] = {}
        if (
            rx is None or not rx.success or not rx.canonical_json
            or rt is None or not rt.success or not rt.canonical_json
        ):
            for m in method_names:
                per_voter[vname][m] = None
            continue
        mr_x = rx.canonical_json.get("method_results") or {}
        mr_tx = rt.canonical_json.get("method_results") or {}
        for m in method_names:
            vx = mr_x.get(m)
            vtx = mr_tx.get(m)
            if vx is None or vtx is None or _is_error(vx) or _is_error(vtx):
                per_voter[vname][m] = None
                continue
            per_voter[vname][m] = _compare_scalar(vx, vtx)

    # --- Step 2: aggregate per-method outcomes across voters ---
    methods_invariant: list[str] = []
    methods_changed: list[str] = []
    methods_cross_sut_disagreement: list[str] = []
    dissenters: set[str] = set()

    for m in method_names:
        votes = [per_voter[v][m] for v in per_voter]
        eligible = [v for v in votes if v is not None]
        if not eligible:
            continue
        n_true = sum(1 for v in eligible if v)
        n_false = len(eligible) - n_true
        if n_false == 0:
            methods_invariant.append(m)
        elif n_true == 0:
            # Every eligible voter says T broke this query's invariant —
            # the MR is wrong (T is not actually preserving this).
            methods_changed.append(m)
        else:
            # Voters disagree — cross-SUT bug. Record voters that voted
            # False (they're claiming the invariant holds for them when
            # the majority says it doesn't, or vice versa).
            methods_cross_sut_disagreement.append(m)
            for v, vote in per_voter.items():
                if vote.get(m) is False:
                    dissenters.add(v)

    passed = not methods_changed and not methods_cross_sut_disagreement
    if passed:
        reason = (
            f"All {len(methods_invariant)} probed methods returned identical "
            f"scalar values across voters on x and T(x)."
        )
    else:
        parts = []
        if methods_changed:
            parts.append(
                f"{len(methods_changed)} methods changed across T: "
                f"{methods_changed}"
            )
        if methods_cross_sut_disagreement:
            parts.append(
                f"{len(methods_cross_sut_disagreement)} methods saw cross-"
                f"SUT disagreement: {methods_cross_sut_disagreement}"
            )
        reason = "; ".join(parts)

    return QueryConsensusResult(
        per_voter=per_voter,
        methods_invariant=methods_invariant,
        methods_changed=methods_changed,
        methods_cross_sut_disagreement=methods_cross_sut_disagreement,
        dissenting_voters=sorted(dissenters),
        passed=passed,
        reason=reason,
    )
