# Storage - Agent Context

## Purpose
ChromaDB vector storage for the RAG pipeline. Persists embeddings and metadata for semantic retrieval.

## Contents
| File/Dir | Description |
|----------|-------------|
| `store.py` | ChromaDB abstraction layer |
| `chroma/` | Database files (auto-created) |
| `__init__.py` | Package exports |

## Key Functions

### `store.py`
- `get_collection()` - Get or create ChromaDB collection
- `add_documents(chunks)` - Add chunks with embeddings
- `query(embedding, top_k)` - Similarity search
- `clear()` - Delete all documents
- `count()` - Get document count

## Database Location
- Path: `./chroma/`
- Persistence: Automatic (survives restarts)
- Format: SQLite + Parquet files

## Schema
Each document has:
- `id` - Unique identifier (hash of content)
- `embedding` - 384-dim vector
- `document` - Original text chunk
- `metadata` - Source file, line number, headers

## Usage
```python
from storage.store import get_collection, add_documents, query

# Add documents
collection = get_collection()
add_documents(chunks_with_embeddings)

# Query
results = query(query_embedding, top_k=5)
```

## For Future Agents
- ChromaDB handles persistence automatically
- Clear database if embedding model changes
- Collection name: `claude_flow_knowledge`
