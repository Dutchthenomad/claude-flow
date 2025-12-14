"""Embeddings module for RAG pipeline."""
from .embedder import get_embedder, embed_text, embed_batch

__all__ = ["get_embedder", "embed_text", "embed_batch"]
