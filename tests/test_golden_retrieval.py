"""
Test 4: RAG Golden Retrieval Test + Robustness Checks

Indexes all parsed chunks into ChromaDB using local embeddings (no API key)
and runs:
  - 3 golden queries (positive retrieval)
  - Test 5: Cross-format metadata isolation
  - Test 6: Math/symbol fidelity in parsed chunks
  - Test 7: Negative retrieval / noise rejection

Usage:
    py -3.14 tests/test_golden_retrieval.py
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spec_ingestor.indexer import SpecIndex
from spec_ingestor.parser import Chunk
from spec_ingestor.config import PARSED_DIR


GOLDEN_QUERIES = [
    {
        "question": "What is the ordering constraint for the ##fileformat line in VCF?",
        "expected_keywords": ["fileformat", "first line", "required"],
        "description": "VCF header ordering constraint",
    },
    {
        "question": "Are SAM optional tags order-sensitive?",
        "expected_keywords": ["optional", "tag", "order"],
        "description": "SAM tag order sensitivity",
    },
    {
        "question": "How should allele indices be mapped for fields with Number=A in VCF?",
        "expected_keywords": ["Number", "allele", "ALT"],
        "description": "VCF Number=A allele index mapping",
    },
]


def load_chunks() -> list[Chunk]:
    chunks = []
    for json_file in PARSED_DIR.glob("*_chunks.json"):
        raw = json.loads(json_file.read_text(encoding="utf-8"))
        for item in raw:
            chunks.append(Chunk(**item))
    return chunks


def ensure_index(index: SpecIndex, chunks: list[Chunk]) -> None:
    """Index chunks if the collection is empty or stale."""
    if index.collection_stats()["total_documents"] < len(chunks):
        print(f"Indexing {len(chunks)} chunks...")
        index.index_chunks(chunks)
    else:
        print(f"Index already has {index.collection_stats()['total_documents']} docs")


# ======================================================================
# Test 4: Golden Retrieval
# ======================================================================

def test_golden_retrieval(index: SpecIndex) -> bool:
    print(f"\n{'='*70}")
    print("TEST 4: Golden Retrieval — Top-3 recalled chunks per query")
    print(f"{'='*70}\n")

    all_pass = True

    for i, gq in enumerate(GOLDEN_QUERIES, 1):
        print(f"--- Query {i}: {gq['description']} ---")
        print(f'Q: "{gq["question"]}"')
        print()

        results = index.query(gq["question"], n_results=3)
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]

        query_pass = False
        for j, (doc, meta, dist) in enumerate(zip(docs, metas, dists)):
            text_lower = doc.lower()
            kw_hits = [kw for kw in gq["expected_keywords"] if kw.lower() in text_lower]

            print(f"  Top-{j+1} (distance={dist:.4f}):")
            print(f"    format={meta['format']}  spec_version={meta['spec_version']}")
            print(f"    section_id={meta['section_id']}")
            print(f"    rule_severity={meta['rule_severity']}")
            print(f"    keyword_hits={kw_hits}")
            print(f"    text: {doc[:300]}")
            print()

            if len(kw_hits) >= 2:
                query_pass = True

        status = "PASS" if query_pass else "FAIL"
        if not query_pass:
            all_pass = False
        print(f"  >>> Query {i}: {status}\n")

    return all_pass


# ======================================================================
# Test 5: Cross-Format Metadata Isolation
# ======================================================================

def test_cross_contamination(index: SpecIndex) -> bool:
    """
    Search for VCF-specific terms with filter={"format": "SAM"}.
    If the metadata filter works, no VCF content should leak through.
    """
    print(f"\n{'='*70}")
    print("TEST 5: Cross-Format Metadata Isolation")
    print(f"{'='*70}\n")

    probes = [
        {"query": "##fileformat VCF header line ordering", "filter_format": "SAM",
         "desc": "VCF-only term '##fileformat' filtered to SAM"},
        {"query": "ALT allele field Number=A in VCF", "filter_format": "SAM",
         "desc": "VCF-only term 'ALT allele Number=A' filtered to SAM"},
        {"query": "CIGAR operation consumes query reference", "filter_format": "VCF",
         "desc": "SAM-only term 'CIGAR consumes' filtered to VCF"},
    ]

    all_pass = True
    for probe in probes:
        print(f"--- {probe['desc']} ---")
        results = index.query(
            probe["query"], n_results=3,
            where={"format": probe["filter_format"]},
        )
        metas = results["metadatas"][0]
        dists = results["distances"][0]
        docs = results["documents"][0]

        leaked = [m for m in metas if m["format"] != probe["filter_format"]]
        assert len(leaked) == 0, f"Metadata filter leaked: {leaked}"

        # All returned results MUST match the requested format
        formats_returned = set(m["format"] for m in metas)
        filter_ok = formats_returned <= {probe["filter_format"]}

        # The distances should be high (poor match) since the query is
        # about the *other* format — we check they're worse than 0.3
        min_dist = min(dists) if dists else 0
        dist_ok = min_dist > 0.3

        print(f"  Formats returned: {formats_returned}  (filter={probe['filter_format']})")
        print(f"  Distances: {[f'{d:.4f}' for d in dists]}")
        print(f"  Filter isolation: {'PASS' if filter_ok else 'FAIL'}")
        print(f"  Distance sanity (min > 0.3): {'PASS' if dist_ok else 'WARN (low dist={min_dist:.4f})'}")
        print(f"  Top-1 text: {docs[0][:200] if docs else 'N/A'}")
        print()

        if not filter_ok:
            all_pass = False

    status = "PASS" if all_pass else "FAIL"
    print(f"  >>> Test 5 overall: {status}")
    return all_pass


# ======================================================================
# Test 6: Math & Symbol Fidelity
# ======================================================================

def test_math_symbol_fidelity(chunks: list[Chunk]) -> bool:
    """
    Find chunks that should contain the genotype index formula n(n+1)/2
    or inequality symbols. Check they are readable, not LaTeX escape garbage.
    """
    print(f"\n{'='*70}")
    print("TEST 6: Math & Symbol Fidelity in Parsed Chunks")
    print(f"{'='*70}\n")

    # Patterns that indicate raw LaTeX leaked through (bad)
    latex_garbage = [r"\frac{", r"\geq", r"\leq", r"\times", r"\cdot",
                     r"\left", r"\right", r"\mathrm", r"\mathit"]

    # Search for chunks that likely discuss the genotype formula or math
    math_chunks = []
    for c in chunks:
        t = c.text
        if any(kw in t for kw in ["n+1", "n(n", "genotype", "ploidy", "binomial"]):
            if any(sym in t for sym in ["(", ")", "/", "2", "+"]):
                math_chunks.append(c)

    # Also look for inequality-heavy chunks
    ineq_chunks = []
    for c in chunks:
        t = c.text
        # Should contain readable symbols, not \leq \geq
        if any(sym in t for sym in ["<=", ">=", "<", ">", "≤", "≥"]):
            ineq_chunks.append(c)

    print(f"Chunks with math formulas (n+1, genotype, etc.): {len(math_chunks)}")
    print(f"Chunks with inequality symbols: {len(ineq_chunks)}")
    print()

    all_pass = True
    garbage_found = []

    # Check math chunks for LaTeX leakage
    sample = math_chunks[:5]
    print("--- Math formula samples ---")
    for i, c in enumerate(sample):
        leaked = [g for g in latex_garbage if g in c.text]
        if leaked:
            garbage_found.append((c.chunk_id, leaked))
        print(f"  [{i+1}] {c.chunk_id}")
        print(f"       section: {c.section_id}")
        print(f"       latex_leaks: {leaked if leaked else 'NONE'}")
        # Show the math-relevant snippet
        text = c.text
        for kw in ["n+1", "n(n", "genotype index", "ploidy"]:
            idx = text.find(kw)
            if idx >= 0:
                start = max(0, idx - 40)
                end = min(len(text), idx + 80)
                print(f"       context: ...{text[start:end]}...")
                break
        print()

    # Check inequality chunks
    print("--- Inequality symbol samples ---")
    ineq_sample = ineq_chunks[:5]
    for i, c in enumerate(ineq_sample):
        leaked = [g for g in latex_garbage if g in c.text]
        if leaked:
            garbage_found.append((c.chunk_id, leaked))
        print(f"  [{i+1}] {c.chunk_id}")
        print(f"       latex_leaks: {leaked if leaked else 'NONE'}")
        # Show a snippet with the symbol
        text = c.text
        for sym in ["<=", ">=", "<", ">", "≤", "≥"]:
            idx = text.find(sym)
            if idx >= 0:
                start = max(0, idx - 30)
                end = min(len(text), idx + 50)
                print(f"       context: ...{text[start:end]}...")
                break
        print()

    if garbage_found:
        all_pass = False
        print(f"  !!! LaTeX garbage found in {len(garbage_found)} chunks:")
        for cid, leaks in garbage_found:
            print(f"      {cid}: {leaks}")
    else:
        print("  No raw LaTeX escape sequences detected in sampled chunks.")

    status = "PASS" if all_pass else "FAIL — LaTeX artifacts will break Z3 constraint generation"
    print(f"\n  >>> Test 6 overall: {status}")
    return all_pass


# ======================================================================
# Test 7: Negative Retrieval / Noise Rejection
# ======================================================================

def test_noise_rejection(index: SpecIndex) -> bool:
    """
    Query with a completely irrelevant question. The returned distances
    should be significantly higher than those from golden queries,
    establishing a threshold for Phase B hallucination prevention.
    """
    print(f"\n{'='*70}")
    print("TEST 7: Negative Retrieval & Noise Rejection")
    print(f"{'='*70}\n")

    irrelevant_queries = [
        "How to extract DNA using a laboratory kit with magnetic beads?",
        "What is the recipe for chocolate chip cookies?",
        "Explain quantum entanglement in simple terms",
    ]

    # First, get baseline distances from a known-good golden query
    baseline = index.query(GOLDEN_QUERIES[0]["question"], n_results=3)
    baseline_dists = baseline["distances"][0]
    baseline_avg = sum(baseline_dists) / len(baseline_dists)

    print(f"Baseline (golden query avg distance): {baseline_avg:.4f}")
    print()

    all_pass = True
    for q in irrelevant_queries:
        results = index.query(q, n_results=3)
        dists = results["distances"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        avg_dist = sum(dists) / len(dists)
        min_dist = min(dists)
        gap = min_dist - baseline_avg

        print(f'--- Q: "{q[:60]}..." ---')
        print(f"  Distances: {[f'{d:.4f}' for d in dists]}")
        print(f"  Avg distance: {avg_dist:.4f}  (baseline: {baseline_avg:.4f})")
        print(f"  Min distance: {min_dist:.4f}  Gap from baseline: +{gap:.4f}")
        print(f"  Top-1: [{metas[0]['format']}] {metas[0]['section_id']}")
        print(f"         {docs[0][:150]}")
        print()

        # The gap between irrelevant min_dist and baseline avg should be > 0.15
        # This ensures Phase B can set a meaningful threshold
        if gap < 0.15:
            all_pass = False
            print(f"  !!! WARNING: gap too small ({gap:.4f}), hard to threshold\n")

    print(f"  Recommended Phase B threshold: ~{baseline_avg + 0.15:.2f}")
    print(f"  (reject chunks with distance > this value)")

    status = "PASS" if all_pass else "FAIL — noise not sufficiently separated from signal"
    print(f"\n  >>> Test 7 overall: {status}")
    return all_pass


# ======================================================================
# Main
# ======================================================================

def main():
    print("Loading chunks...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    print("Initializing index (local embeddings, no API key needed)...")
    index = SpecIndex()
    ensure_index(index, chunks)

    results = {}
    results["test4_golden"] = test_golden_retrieval(index)
    results["test5_isolation"] = test_cross_contamination(index)
    results["test6_math"] = test_math_symbol_fidelity(chunks)
    results["test7_noise"] = test_noise_rejection(index)

    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    for name, passed in results.items():
        print(f"  {name}: {'PASS' if passed else 'FAIL'}")
    all_ok = all(results.values())
    print(f"\n  OVERALL: {'ALL PASS — ready for Phase B' if all_ok else 'BLOCKED — fix failures before Phase B'}")
    print(f"{'='*70}")
    return all_ok


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
