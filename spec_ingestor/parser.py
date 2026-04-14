"""
Step 2 & 3: Document Parsing, Table Reconstruction, Hierarchical Chunking & Tagging

Parses downloaded .tex files to extract:
  - Tabular environments as structured JSON (CIGAR tables, INFO/FORMAT semantics, etc.)
  - Normative keywords (MUST, SHALL, SHOULD, MAY, etc.)
  - Hierarchical section structure for semantic chunking

Each chunk receives rich metadata for downstream filtering.
"""

import json
import logging
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

from pylatexenc.latex2text import LatexNodes2Text

from .config import NORMATIVE_KEYWORDS, SPEC_META, PARSED_DIR

logger = logging.getLogger(__name__)

# Pre-compile patterns
_SECTION_RE = re.compile(
    r"\\(section|subsection|subsubsection)\{([^}]+)\}", re.MULTILINE
)
_TABULAR_RE = re.compile(
    r"\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}", re.DOTALL
)
_NORMATIVE_RE = re.compile(
    r"\b(" + "|".join(
        re.escape(kw)
        for kwlist in NORMATIVE_KEYWORDS.values()
        for kw in kwlist
    ) + r")\b"
)

_latex2text = LatexNodes2Text()


def _safe_latex_to_text(tex: str) -> str:
    """Convert LaTeX to plain text, falling back to regex stripping on failure."""
    try:
        return _latex2text.latex_to_text(tex)
    except Exception:
        # Fallback: strip common LaTeX commands via regex
        text = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", tex)
        text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
        text = re.sub(r"[{}]", "", text)
        return text.strip()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ParsedTable:
    """A single extracted tabular environment."""
    section_id: str
    column_spec: str
    headers: list[str]
    rows: list[list[str]]
    raw_latex: str


@dataclass
class Chunk:
    """A semantically-tagged text chunk ready for embedding."""
    chunk_id: str
    text: str
    format: str
    spec_version: str
    commit_sha: str
    section_id: str
    rule_severity: str
    chunk_type: str = "text"  # "text" or "table"
    tables: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Table extraction
# ---------------------------------------------------------------------------

def _parse_tabular(raw: str, column_spec: str, section_id: str) -> ParsedTable:
    """Convert a raw LaTeX tabular body into a structured ParsedTable."""
    # Strip \hline, \toprule, etc.
    body = re.sub(r"\\(hline|toprule|midrule|bottomrule|cline\{[^}]*\})", "", raw)
    # Split rows by \\
    raw_rows = [r.strip() for r in re.split(r"\\\\", body) if r.strip()]

    parsed_rows: list[list[str]] = []
    for row in raw_rows:
        cells = [_safe_latex_to_text(c.strip()) for c in row.split("&")]
        parsed_rows.append(cells)

    headers = parsed_rows[0] if parsed_rows else []
    data_rows = parsed_rows[1:] if len(parsed_rows) > 1 else []

    return ParsedTable(
        section_id=section_id,
        column_spec=column_spec,
        headers=headers,
        rows=data_rows,
        raw_latex=raw,
    )


def extract_tables(tex_content: str) -> list[ParsedTable]:
    """Extract all tabular environments from a TeX source string."""
    # Build a section map so each table knows which section it belongs to
    section_positions: list[tuple[int, str]] = []
    for m in _SECTION_RE.finditer(tex_content):
        section_positions.append((m.start(), m.group(2)))

    def _section_at(pos: int) -> str:
        current = "preamble"
        for spos, sname in section_positions:
            if spos > pos:
                break
            current = sname
        return current

    tables: list[ParsedTable] = []
    for m in _TABULAR_RE.finditer(tex_content):
        col_spec = m.group(1)
        body = m.group(2)
        section = _section_at(m.start())
        tables.append(_parse_tabular(body, col_spec, section))

    logger.info("Extracted %d tables", len(tables))
    return tables


def normalize_tables(tables: list[ParsedTable]) -> list[dict]:
    """
    Post-process extracted tables into clean structured JSON.

    Handles:
    - Multirow/multicolumn headers (e.g., CIGAR 'Consumes query'/'Consumes reference')
    - Rows with mismatched column counts (sub-headers, merged cells)
    - Known table schemas for CIGAR ops and INFO/FORMAT Number semantics
    """
    normalized: list[dict] = []

    for table in tables:
        # Detect CIGAR operations table by signature
        if table.headers[:3] == ["Op", "BAM", "Description"]:
            normalized.append(_normalize_cigar_table(table))
            continue

        # Detect FLAG bits table
        if any("Bit" in h or "bit" in h for h in table.headers):
            if any("FLAG" in str(r) or "flag" in str(r) or len(table.rows) > 5
                   for r in table.rows):
                normalized.append(_normalize_flag_table(table))
                continue

        # Generic normalization: filter out sub-header rows, align columns
        clean_rows = []
        n_cols = len(table.headers)
        for row in table.rows:
            if len(row) == n_cols:
                clean_rows.append(dict(zip(table.headers, row)))
            # Rows with different col counts are likely sub-headers — skip

        normalized.append({
            "type": "generic",
            "section": table.section_id,
            "headers": table.headers,
            "records": clean_rows,
        })

    return normalized


def _normalize_cigar_table(table: ParsedTable) -> dict:
    """Normalize the CIGAR operations table into structured records."""
    records = []
    for row in table.rows:
        if len(row) == 5:
            records.append({
                "op": row[0].strip(),
                "bam_code": int(row[1].strip()) if row[1].strip().isdigit() else row[1].strip(),
                "description": row[2].strip(),
                "consumes_query": row[3].strip().lower() == "yes",
                "consumes_reference": row[4].strip().lower() == "yes",
            })
    return {
        "type": "cigar_operations",
        "section": table.section_id,
        "headers": ["op", "bam_code", "description", "consumes_query", "consumes_reference"],
        "records": records,
    }


def _normalize_flag_table(table: ParsedTable) -> dict:
    """Normalize the SAM FLAG bits table."""
    records = []
    n_cols = len(table.headers)
    for row in table.rows:
        if len(row) == n_cols:
            records.append(dict(zip(table.headers, [c.strip() for c in row])))
    return {
        "type": "flag_bits",
        "section": table.section_id,
        "headers": table.headers,
        "records": records,
    }


# ---------------------------------------------------------------------------
# Normative keyword detection
# ---------------------------------------------------------------------------

def classify_severity(text: str) -> str:
    """
    Return 'CRITICAL' if any MUST/SHALL keyword is present,
    'ADVISORY' if any SHOULD/MAY keyword is present, else 'INFORMATIONAL'.
    """
    upper = text.upper()
    for kw in NORMATIVE_KEYWORDS["CRITICAL"]:
        if re.search(r"\b" + re.escape(kw) + r"\b", upper):
            return "CRITICAL"
    for kw in NORMATIVE_KEYWORDS["ADVISORY"]:
        if re.search(r"\b" + re.escape(kw) + r"\b", upper):
            return "ADVISORY"
    return "INFORMATIONAL"


def highlight_normative(text: str) -> str:
    """Wrap normative keywords with «» markers for visibility."""
    def _replace(m: re.Match) -> str:
        return f"«{m.group(0)}»"
    return _NORMATIVE_RE.sub(_replace, text)


# ---------------------------------------------------------------------------
# Hierarchical chunking
# ---------------------------------------------------------------------------

@dataclass
class _SectionNode:
    level: int  # 1=section, 2=subsection, 3=subsubsection
    title: str
    content_start: int
    content_end: int = -1

_LEVEL_MAP = {"section": 1, "subsection": 2, "subsubsection": 3}


def _build_section_tree(tex_content: str) -> list[_SectionNode]:
    """Identify section boundaries in the TeX source."""
    nodes: list[_SectionNode] = []
    for m in _SECTION_RE.finditer(tex_content):
        level = _LEVEL_MAP[m.group(1)]
        title = m.group(2)
        start = m.end()
        nodes.append(_SectionNode(level=level, title=title, content_start=start))

    # Close each section at the start of the next same-or-higher-level section
    for i, node in enumerate(nodes):
        node.content_end = len(tex_content)
        for j in range(i + 1, len(nodes)):
            if nodes[j].level <= node.level:
                node.content_end = nodes[j].content_start
                break

    return nodes


def _split_paragraphs(text: str) -> list[str]:
    """Split text on blank lines (paragraph boundaries in TeX)."""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def chunk_document(
    tex_content: str,
    filename: str,
    commit_sha: str,
) -> list[Chunk]:
    """
    Produce semantic chunks from a TeX document.

    Strategy: Section -> Paragraph level splitting. Each paragraph becomes its
    own chunk, tagged with the enclosing section hierarchy. Tables within a
    section are attached to the section's first chunk or emitted standalone.
    """
    meta = SPEC_META.get(filename, {"format": "UNKNOWN", "spec_version": "UNKNOWN"})
    tables = extract_tables(tex_content)
    sections = _build_section_tree(tex_content)
    chunks: list[Chunk] = []
    chunk_counter = 0

    # Index tables by their section
    table_by_section: dict[str, list[ParsedTable]] = {}
    for t in tables:
        table_by_section.setdefault(t.section_id, []).append(t)

    if not sections:
        # Fallback: treat entire document as one section
        sections = [_SectionNode(level=1, title="document", content_start=0,
                                 content_end=len(tex_content))]

    for sec in sections:
        raw_section = tex_content[sec.content_start : sec.content_end]
        plain_text = _safe_latex_to_text(raw_section)
        paragraphs = _split_paragraphs(plain_text)

        if not paragraphs:
            continue

        section_tables = table_by_section.get(sec.title, [])

        for i, para in enumerate(paragraphs):
            if len(para.split()) < 5:
                continue  # skip trivially short fragments

            chunk_counter += 1
            severity = classify_severity(para)
            highlighted = highlight_normative(para)

            attached_tables = []
            if i == 0 and section_tables:
                norm = normalize_tables(section_tables)
                attached_tables = norm

            # Prefix with section context to improve embedding relevance
            prefix = f"[{meta['format']} {meta['spec_version']} — {sec.title}] "

            chunks.append(
                Chunk(
                    chunk_id=f"{filename}::{sec.title}::p{chunk_counter}",
                    text=prefix + highlighted,
                    format=meta["format"],
                    spec_version=meta["spec_version"],
                    commit_sha=commit_sha,
                    section_id=sec.title,
                    rule_severity=severity,
                    chunk_type="table" if attached_tables else "text",
                    tables=attached_tables,
                )
            )

    # Emit standalone table chunks for tables whose section had no text
    for sec_title, sec_tables in table_by_section.items():
        already_attached = any(
            c.section_id == sec_title and c.tables for c in chunks
        )
        if not already_attached:
            norm = normalize_tables(sec_tables)
            for nt in norm:
                chunk_counter += 1
                # Build readable text from normalized records
                prefix = f"[{meta['format']} {meta['spec_version']} — {sec_title}] "
                if nt.get("records"):
                    table_text = prefix + json.dumps(nt["records"], indent=2)
                else:
                    table_text = prefix + " | ".join(nt.get("headers", [])) + "\n"
                chunks.append(
                    Chunk(
                        chunk_id=f"{filename}::{sec_title}::table{chunk_counter}",
                        text=table_text,
                        format=meta["format"],
                        spec_version=meta["spec_version"],
                        commit_sha=commit_sha,
                        section_id=sec_title,
                        rule_severity=classify_severity(table_text),
                        chunk_type="table",
                        tables=[nt],
                    )
                )

    logger.info("Chunked %s into %d chunks", filename, len(chunks))
    return chunks


def parse_and_chunk_all(
    files: dict[str, str], commit_sha: str
) -> list[Chunk]:
    """
    Parse and chunk all fetched files.

    Args:
        files: dict mapping filename -> TeX content.
        commit_sha: the commit SHA used during ingestion.

    Returns:
        Flat list of all Chunk objects across all files.
    """
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    all_chunks: list[Chunk] = []

    for filename, content in files.items():
        if not filename.endswith(".tex"):
            logger.warning("Skipping non-TeX file: %s", filename)
            continue

        chunks = chunk_document(content, filename, commit_sha)
        all_chunks.extend(chunks)

        # Persist parsed output as JSON for inspection
        out_path = PARSED_DIR / filename.replace(".tex", "_chunks.json")
        out_path.write_text(
            json.dumps([c.to_dict() for c in chunks], indent=2),
            encoding="utf-8",
        )

        # Also persist extracted tables — both raw and normalized
        tables = extract_tables(content)
        tables_path = PARSED_DIR / filename.replace(".tex", "_tables.json")
        tables_path.write_text(
            json.dumps(
                [
                    {
                        "section": t.section_id,
                        "headers": t.headers,
                        "rows": t.rows,
                        "column_spec": t.column_spec,
                    }
                    for t in tables
                ],
                indent=2,
            ),
            encoding="utf-8",
        )

        # Normalized (structured) tables
        norm_tables = normalize_tables(tables)
        norm_path = PARSED_DIR / filename.replace(".tex", "_tables_normalized.json")
        norm_path.write_text(json.dumps(norm_tables, indent=2), encoding="utf-8")

    logger.info("Total chunks across all files: %d", len(all_chunks))
    return all_chunks
