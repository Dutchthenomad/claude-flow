"""Sentence-transformers embedding wrapper."""
from typing import Union
import sys

# Lazy load to avoid slow imports
_embedder = None


def get_embedder():
    """Get or create singleton embedder.
    
    Returns:
        SentenceTransformer model instance
    """
    global _embedder
    if _embedder is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            print("Error: sentence-transformers not installed.")
            print("Run: pip install sentence-transformers")
            sys.exit(1)
        
        # Import config here to avoid circular imports
        sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
        from config import EMBEDDING_MODEL
        
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
        print("Model loaded.")
    
    return _embedder


def embed_text(text: str) -> list[float]:
    """Embed a single text string.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats (embedding vector)
    """
    embedder = get_embedder()
    embedding = embedder.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def embed_batch(texts: list[str], show_progress: bool = False) -> list[list[float]]:
    """Embed multiple texts efficiently.
    
    Args:
        texts: List of texts to embed
        show_progress: Show progress bar
        
    Returns:
        List of embedding vectors
    """
    if not texts:
        return []
    
    embedder = get_embedder()
    embeddings = embedder.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=show_progress,
    )
    return embeddings.tolist()


if __name__ == "__main__":
    # Test embeddings
    print("Testing embedder...")
    
    vec = embed_text("How do slash commands work?")
    print(f"Single embedding: {len(vec)} dimensions")
    print(f"First 5 values: {vec[:5]}")
    
    vecs = embed_batch(["Hello world", "Goodbye world"])
    print(f"Batch embedding: {len(vecs)} vectors")
