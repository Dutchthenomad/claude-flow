"""Query interface for RAG pipeline."""
import os
import sys
from pathlib import Path
from typing import Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DEFAULT_TOP_K
from embeddings.embedder import embed_text
from storage.store import query, count


def search(
    query_text: str,
    top_k: int = DEFAULT_TOP_K,
    *,
    backend: str | None = None,
) -> list[dict[str, Any]]:
    """Search for relevant documents.
    
    Args:
        query_text: Natural language query
        top_k: Number of results to return
        backend: Optional backend override ("native" or "langchain_hybrid")
        
    Returns:
        List of result dicts with text, source, line, headers, score
    """
    if count() == 0:
        print("Warning: Index is empty. Run ingestion first.")
        return []

    selected_backend = (backend or os.getenv("CLAUDE_FLOW_RAG_BACKEND", "native")).strip()
    if selected_backend in {"langchain_hybrid", "hybrid", "langchain"}:
        from retrieval import langchain_hybrid

        return langchain_hybrid.search(query_text, top_k=top_k)
    
    # Embed query
    query_embedding = embed_text(query_text)
    
    # Search
    results = query(query_embedding, top_k=top_k)
    
    return results


def search_with_filter(
    query_text: str,
    source_filter: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    *,
    backend: str | None = None,
) -> list[dict[str, Any]]:
    """Search with source path filter.
    
    Args:
        query_text: Natural language query
        source_filter: Filter to sources containing this string
        top_k: Number of results to return
        backend: Optional backend override ("native" or "langchain_hybrid")
        
    Returns:
        List of result dicts
    """
    results = search(query_text, top_k=top_k * 2, backend=backend)  # Get more, then filter
    
    if source_filter:
        results = [r for r in results if source_filter in r["source"]]
    
    return results[:top_k]


def format_results(results: list[dict[str, Any]]) -> str:
    """Format results for display.
    
    Args:
        results: Search results
        
    Returns:
        Formatted string
    """
    if not results:
        return "No results found."
    
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"\n{'='*60}")
        lines.append(f"Result {i} (score: {r['score']:.3f})")
        lines.append(f"Source: {r['source']}:{r['line_start']}-{r['line_end']}")
        if r["headers"]:
            lines.append(f"Context: {' > '.join(r['headers'])}")
        lines.append("-" * 60)
        # Truncate long texts
        text = r["text"]
        if len(text) > 500:
            text = text[:500] + "..."
        lines.append(text)
    
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG Pipeline Search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("-f", "--filter", help="Source path filter")
    args = parser.parse_args()
    
    if not args.query:
        print("Usage: python -m retrieval.retrieve 'your query here'")
        print(f"\nIndex contains {count()} documents")
        sys.exit(0)
    
    if args.filter:
        results = search_with_filter(args.query, args.filter, args.top_k)
    else:
        results = search(args.query, args.top_k)
    
    print(format_results(results))
