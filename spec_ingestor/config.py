"""Shared configuration constants for the spec ingestor pipeline."""

from pathlib import Path

# GitHub source
GITHUB_REPO = "samtools/hts-specs"
GITHUB_BRANCH = "master"
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_REPO}"

# Target spec files to download
TARGET_TEX_FILES = ["VCFv4.5.tex", "SAMv1.tex"]

# Local storage
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw_tex"
PARSED_DIR = DATA_DIR / "parsed"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Normative keywords and their severity mapping
NORMATIVE_KEYWORDS = {
    "CRITICAL": ["MUST", "SHALL", "REQUIRED", "MUST NOT", "SHALL NOT"],
    "ADVISORY": ["SHOULD", "SHOULD NOT", "MAY", "RECOMMENDED", "OPTIONAL"],
}

# Spec metadata derived from filenames
SPEC_META = {
    "VCFv4.5.tex": {"format": "VCF", "spec_version": "v4.5"},
    "SAMv1.tex": {"format": "SAM", "spec_version": "v1"},
}

# Embedding model
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# ChromaDB collection name
CHROMA_COLLECTION = "hts_specs"
