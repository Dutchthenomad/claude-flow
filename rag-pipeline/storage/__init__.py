"""Storage module for RAG pipeline."""
from .store import get_collection, add_documents, query, clear, count

__all__ = ["get_collection", "add_documents", "query", "clear", "count"]
