"""Build shared/raw_spec_dump.txt for naive prompt-stuffing.

Converts data/raw_tex/VCFv4.5.tex + SAMv1.tex via pylatexenc to plain
text, concatenates with section separators, writes to
shared/raw_spec_dump.txt.

Used by E1 (no Phase A) and E3 (no Phase A, no Phase D) to inject the
full spec into the LLM system prompt as a substitute for RAG retrieval.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_TEX_DIR = PROJECT_ROOT / "data" / "raw_tex"
OUT_PATH = Path(__file__).resolve().parent / "raw_spec_dump.txt"

# Hard char cap for the combined dump. ~130k chars ≈ ~32k tokens for
# DeepSeek/OpenAI BPE — fits comfortably under DeepSeek-V3's 128k context
# window with room for the existing system prompt + blindspot ticket.
CHAR_CAP = 130_000

# Reuse the project's hardened LaTeX->text converter (handles malformed
# macros via regex fallback). See spec_ingestor/parser.py:42.
sys.path.insert(0, str(PROJECT_ROOT))
from spec_ingestor.parser import _safe_latex_to_text  # noqa: E402


def latex_to_text(tex_path: Path) -> str:
    """Convert a .tex file to plain text via the project's safe converter."""
    raw = tex_path.read_text(encoding="utf-8", errors="replace")
    return _safe_latex_to_text(raw)


def main() -> int:
    vcf_tex = RAW_TEX_DIR / "VCFv4.5.tex"
    sam_tex = RAW_TEX_DIR / "SAMv1.tex"

    for p in (vcf_tex, sam_tex):
        if not p.exists():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 1

    print(f"Converting {vcf_tex.name} ...")
    vcf_text = latex_to_text(vcf_tex)
    print(f"  {len(vcf_text):,} chars")

    print(f"Converting {sam_tex.name} ...")
    sam_text = latex_to_text(sam_tex)
    print(f"  {len(sam_text):,} chars")

    sep = "\n\n" + "=" * 70 + "\n"
    body = (
        sep
        + "VCF v4.5 SPECIFICATION (full text)\n"
        + sep
        + vcf_text
        + sep
        + "SAM v1 SPECIFICATION (full text)\n"
        + sep
        + sam_text
    )

    if len(body) > CHAR_CAP:
        # Truncate evenly across both halves to keep both formats
        # represented. We aim for header(~200) + half(VCF) + sep(~80) +
        # half(SAM) ≈ CHAR_CAP.
        half = (CHAR_CAP - 400) // 2
        body = (
            sep + "VCF v4.5 SPECIFICATION (truncated)\n" + sep
            + vcf_text[:half]
            + sep + "SAM v1 SPECIFICATION (truncated)\n" + sep
            + sam_text[:half]
        )
        print(f"  truncated to {len(body):,} chars (cap {CHAR_CAP:,})")

    OUT_PATH.write_text(body, encoding="utf-8")
    print(f"\nWrote {OUT_PATH} ({len(body):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
