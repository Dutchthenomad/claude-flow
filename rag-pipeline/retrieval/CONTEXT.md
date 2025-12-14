# Retrieval - Agent Context

## Purpose
Semantic search and query processing. Retrieves relevant document chunks based on query similarity.

## Responsibilities
- Query embedding generation
- Cosine similarity search
- Result ranking and filtering
- Context assembly for LLM

## Planned Components
| File | Description |
|------|-------------|
| `search.py` | Main search interface |
| `ranking.py` | Result ranking algorithms |
| `filters.py` | Metadata filtering |

## Search API (Planned)
```python
def search_knowledge_base(
    query: str,
    top_k: int = 5,
    filters: dict = None
) -> list[Chunk]:
    """
    Search for relevant chunks using semantic similarity.
    """
```

## Development Status
- [x] Initial structure
- [ ] Basic search
- [ ] Metadata filtering
- [ ] Ranking optimization
- [ ] Integration tests
