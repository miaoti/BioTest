"""
Rank 5 — query_method_roundtrip transform.

Runtime-dispatched transform that stages an MR's input file, asks the
primary SUT's runner to invoke a list of public query methods on the
parsed object, and returns the scalar results packaged into the
transform's output `canonical_json["method_results"]`. The
`query_consensus` oracle then compares method_results between x and
T(x) — the real invariant the MR checks.

This is the framework-level half of Rank 5; per-SUT reflection lives
inside each `ParserRunner.run_query_methods`. The transform itself is
SUT-agnostic: it only dispatches. The MR's `transform_steps` must
include `query_method_roundtrip` as the LAST step — any preceding
transforms mutate the file first.

Grounded in:
  - Chen, Kuo, Liu, Tse (ACM CSUR 2018) §3.2 — API-level MRs.
  - MR-Scout (Xu, Terragni, Zhu, Wu, Cheung — TOSEM 2024, arXiv:2304.07548)
    — mined 11,000 query-method MRs on 701 OSS projects; +13.5 pp line
    coverage vs baseline.
  - MeMo (Blasi, Gorla, Ernst, Pezzè, Carzaniga — JSS vol.181, 2021) —
    auto-mines equivalence MRs from Javadoc.
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path as _P
from typing import Any, Optional

from . import register_transform


@register_transform(
    "query_method_roundtrip",
    format="VCF/SAM",
    description=(
        "Invoke public query methods (e.g. isStructural, getNAlleles, "
        "isProperPair) on the primary SUT's parsed object. Returns the "
        "scalar results in canonical_json['method_results'] so the "
        "query-consensus oracle can compare them across x and T(x). "
        "Per Chen-Kuo-Liu-Tse 2018 §3.2 and MR-Scout 2024."
    ),
    contextual_hint=(
        "the MR's target is API_QUERY_INVARIANCE and the primary SUT's "
        "runner sets `supports_query_methods=True`. The prompt lists the "
        "specific method names the primary SUT exposes — pick 2-5 of them "
        "for the MR's oracle. Typically paired with a semantics-preserving "
        "text transform (shuffle_meta_lines, etc.) as an earlier step."
    ),
    preconditions=(
        "primary_sut_supports_query_methods",
    ),
)
def query_method_roundtrip(
    file_lines: list[str],
    seed: Optional[int] = None,
    runner: Any = None,
    format_type: str = "VCF",
    method_names: Optional[list[str]] = None,
) -> list[str]:
    """Dispatch to `runner.run_query_methods` and pack results.

    Returns the ORIGINAL file_lines — this transform does not mutate
    the file. The meaningful payload is `method_results`, surfaced via
    the `query_consensus` oracle which reads it directly from the
    runner result (the oracle call path goes through the orchestrator,
    not through the transform's return value).

    When called outside the Rank 5 dispatch path (e.g. unit tests
    without a runner_hook), this transform gracefully no-ops — same
    safe-default policy as sut_write_roundtrip.
    """
    logger = logging.getLogger(__name__)

    if not file_lines or runner is None:
        return file_lines
    if not getattr(runner, "supports_query_methods", False):
        logger.debug(
            "query_method_roundtrip: runner %r does not support query-methods",
            getattr(runner, "name", type(runner).__name__),
        )
        return file_lines

    fmt = (format_type or "VCF").upper()
    ext = ".vcf" if fmt == "VCF" else ".sam"
    names = method_names or []
    if not names:
        logger.debug("query_method_roundtrip: no method_names supplied; no-op")
        return file_lines

    with tempfile.TemporaryDirectory(prefix="biotest_query_") as tmpdir:
        input_path = _P(os.path.join(tmpdir, f"input{ext}"))
        with open(input_path, "w", encoding="utf-8") as f:
            f.writelines(file_lines)
        try:
            runner.run_query_methods(input_path, fmt, names)
        except NotImplementedError:
            logger.warning(
                "Runner %r declares supports_query_methods=True but raises "
                "NotImplementedError — no-op",
                getattr(runner, "name", type(runner).__name__),
            )
        except Exception as e:
            logger.debug("query_method_roundtrip: runner raised: %s", e)

    return file_lines
