# Retrieval - Agent Context

## Purpose
Query interface for the RAG pipeline. Provides semantic search over indexed documents.

## Contents
| File | Description |
|------|-------------|
| `retrieve.py` | Main query interface |
| `langchain_hybrid.py` | Optional hybrid backend (dense + lexical + rerank) |
| `__init__.py` | Package exports |

## Key Functions

### `retrieve.py`
- `search(query, top_k=5, backend=None)` - Main search function (`backend="langchain_hybrid"` or env `CLAUDE_FLOW_RAG_BACKEND=langchain_hybrid`)
- `search_with_filter(query, source_filter, backend=None)` - Filtered search

## Return Format
```python
[
    {
        "text": "chunk content...",
        "source": "knowledge/anthropic-docs/07-plugins.md",
        "line_start": 42,
        "line_end": 58,
        "headers": ["Plugins", "Structure"],
        "score": 0.89
    },
    ...
]
```

## Usage
```python
from retrieval.retrieve import search

# Basic search
results = search("How do I create a slash command?")

# With filter
results = search_with_filter("hooks", source_filter="knowledge/anthropic-docs")

# Iterate results
for r in results:
    print(f"{r['source']}:{r['line_start']}-{r['line_end']}")
    print(f"  {r['text'][:100]}...")
    print(f"  Score: {r['score']:.2f}")
```

## CLI Interface
```bash
# From rag-pipeline/
python -m retrieval.retrieve "your query here"
```

## For Future Agents
- Results sorted by relevance (highest first)
- Score range: 0.0 (unrelated) to 1.0 (exact match)
- Typical good results have score > 0.5

## LangChain Hybrid Backend

To enable the hybrid backend (dense + lexical + optional cross-encoder rerank):

1) Install optional deps:
   - `rag-pipeline/requirements-langchain.txt`
2) Enable backend:
   - `export CLAUDE_FLOW_RAG_BACKEND=langchain_hybrid`
