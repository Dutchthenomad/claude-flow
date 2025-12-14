"""Main ingestion script for RAG pipeline."""
import sys
from pathlib import Path
from typing import Iterator

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import KNOWLEDGE_PATHS, INCLUDE_PATTERNS, CHUNK_SIZE, CHUNK_OVERLAP
from ingestion.chunker import chunk_markdown, chunk_text, Chunk
from embeddings.embedder import embed_batch
from storage.store import add_documents, clear, count


def find_files() -> Iterator[Path]:
    """Find all files to index based on config."""
    for knowledge_path in KNOWLEDGE_PATHS:
        if not knowledge_path.exists():
            print(f"  Skipping (not found): {knowledge_path}")
            continue
        
        for pattern in INCLUDE_PATTERNS:
            for file_path in knowledge_path.rglob(pattern):
                if file_path.is_file():
                    yield file_path


def ingest_file(file_path: Path) -> list[dict]:
    """Ingest a single file into chunks.
    
    Args:
        file_path: Path to file
        
    Returns:
        List of chunk dicts
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  Error reading {file_path}: {e}")
        return []
    
    # Make source path relative to project root
    try:
        from config import PROJECT_ROOT
        source = str(file_path.relative_to(PROJECT_ROOT))
    except ValueError:
        source = str(file_path)
    
    # Choose chunker based on file type
    if file_path.suffix == ".md":
        chunks = list(chunk_markdown(text, source, CHUNK_SIZE, CHUNK_OVERLAP))
    else:
        chunks = list(chunk_text(text, source, CHUNK_SIZE, CHUNK_OVERLAP))
    
    # Convert Chunk objects to dicts
    return [
        {
            "text": c.text,
            "source": c.source,
            "line_start": c.line_start,
            "line_end": c.line_end,
            "headers": c.headers,
        }
        for c in chunks
    ]


def ingest_all(clear_first: bool = True) -> int:
    """Ingest all knowledge sources.
    
    Args:
        clear_first: Clear existing index before ingesting
        
    Returns:
        Total number of chunks indexed
    """
    if clear_first:
        print("Clearing existing index...")
        clear()
    
    print("Finding files to index...")
    files = list(find_files())
    print(f"Found {len(files)} files")
    
    all_chunks = []
    for file_path in files:
        chunks = ingest_file(file_path)
        if chunks:
            all_chunks.extend(chunks)
            print(f"  {file_path.name}: {len(chunks)} chunks")
    
    if not all_chunks:
        print("No chunks to index!")
        return 0
    
    print(f"\nGenerating embeddings for {len(all_chunks)} chunks...")
    texts = [c["text"] for c in all_chunks]
    embeddings = embed_batch(texts, show_progress=True)
    
    print("Storing in ChromaDB...")
    added = add_documents(all_chunks, embeddings)
    
    total = count()
    print(f"\nDone! Total documents in index: {total}")
    
    return added


def clear_index():
    """Clear the entire index."""
    print("Clearing index...")
    clear()
    print("Done!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG Pipeline Ingestion")
    parser.add_argument("--clear", action="store_true", help="Clear index only")
    parser.add_argument("--no-clear", action="store_true", help="Don't clear before indexing")
    args = parser.parse_args()
    
    if args.clear:
        clear_index()
    else:
        ingest_all(clear_first=not args.no_clear)
