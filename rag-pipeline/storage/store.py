"""ChromaDB vector storage."""
import hashlib
import sys
from typing import Any

# Lazy load
_client = None
_collection = None


def _get_client():
    """Get or create ChromaDB client."""
    global _client
    if _client is None:
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            print("Error: chromadb not installed.")
            print("Run: pip install chromadb")
            sys.exit(1)
        
        # Import config
        sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
        from config import CHROMA_PATH
        
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        
        _client = chromadb.PersistentClient(
            path=str(CHROMA_PATH),
            settings=Settings(anonymized_telemetry=False),
        )
    
    return _client


def get_collection():
    """Get or create the knowledge collection.
    
    Returns:
        ChromaDB collection
    """
    global _collection
    if _collection is None:
        sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
        from config import COLLECTION_NAME
        
        client = _get_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    
    return _collection


def _make_id(text: str, source: str) -> str:
    """Generate unique ID for a chunk."""
    content = f"{source}:{text}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def add_documents(
    chunks: list[dict[str, Any]],
    embeddings: list[list[float]],
) -> int:
    """Add documents to the collection.
    
    Args:
        chunks: List of chunk dicts with text, source, line_start, line_end, headers
        embeddings: Corresponding embedding vectors
        
    Returns:
        Number of documents added
    """
    if not chunks:
        return 0
    
    collection = get_collection()
    
    ids = [_make_id(c["text"], c["source"]) for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "source": c["source"],
            "line_start": c["line_start"],
            "line_end": c["line_end"],
            "headers": "|".join(c.get("headers", [])),
        }
        for c in chunks
    ]
    
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    
    return len(chunks)


def query(
    embedding: list[float],
    top_k: int = 5,
    where: dict | None = None,
) -> list[dict[str, Any]]:
    """Query similar documents.
    
    Args:
        embedding: Query embedding vector
        top_k: Number of results to return
        where: Optional filter dict
        
    Returns:
        List of result dicts with text, source, line, headers, score
    """
    collection = get_collection()
    
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            doc_id = results["ids"][0][i] if results.get("ids") else None
            # Convert distance to similarity score (cosine)
            score = 1 - distance
            
            output.append({
                "id": doc_id,
                "text": doc,
                "source": meta["source"],
                "line_start": meta["line_start"],
                "line_end": meta["line_end"],
                "headers": meta["headers"].split("|") if meta["headers"] else [],
                "score": score,
            })
    
    return output


def get_all_documents() -> list[dict[str, Any]]:
    """Fetch all documents and their metadata from the collection.

    Returns:
        List of dicts with keys: id, text, source, line_start, line_end, headers
    """
    collection = get_collection()
    results = collection.get(
        include=["documents", "metadatas"],
    )

    docs: list[dict[str, Any]] = []
    for i, text in enumerate(results.get("documents") or []):
        meta = (results.get("metadatas") or [])[i]
        doc_id = (results.get("ids") or [None])[i]
        docs.append(
            {
                "id": doc_id,
                "text": text,
                "source": meta["source"],
                "line_start": meta["line_start"],
                "line_end": meta["line_end"],
                "headers": meta["headers"].split("|") if meta.get("headers") else [],
            }
        )
    return docs


def clear():
    """Delete all documents from the collection."""
    global _collection
    
    sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
    from config import COLLECTION_NAME
    
    client = _get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # Collection might not exist
    
    _collection = None


def count() -> int:
    """Get number of documents in collection."""
    collection = get_collection()
    return collection.count()


if __name__ == "__main__":
    print("Testing store...")
    print(f"Document count: {count()}")
