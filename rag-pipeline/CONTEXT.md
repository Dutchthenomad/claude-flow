# RAG Pipeline - Agent Context

## Purpose
Local RAG (Retrieval-Augmented Generation) system for the claude-flow knowledge base. Provides semantic search over project documentation, code, and scraped Anthropic docs.

## Architecture

```
rag-pipeline/
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
├── ingestion/         # Document processing
│   ├── ingest.py      # Main ingestion script
│   └── chunker.py     # Text chunking logic
├── embeddings/        # Vector embedding
│   └── embedder.py    # Sentence-transformers wrapper
├── storage/           # ChromaDB persistence
│   ├── chroma/        # Database files
│   └── store.py       # Storage abstraction
└── retrieval/         # Query interface
    └── retrieve.py    # Search functions
```

## Technology Stack
- **Vector DB**: ChromaDB (local, serverless, no external dependencies)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2, runs locally)
- **Chunking**: Markdown-aware text splitting with overlap

## Data Flow
```
Documents → Chunking → Embeddings → ChromaDB → Semantic Search
```

1. **Ingest**: Read markdown/code files from knowledge/, docs/, commands/
2. **Chunk**: Split into semantic chunks (512 tokens max, 50 token overlap)
3. **Embed**: Generate 384-dim vectors with sentence-transformers
4. **Store**: Persist to ChromaDB (./storage/chroma/)
5. **Retrieve**: Cosine similarity search returns top-k chunks

## Usage

### Initial Setup
```bash
cd rag-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Index Knowledge Base
```bash
python -m ingestion.ingest
```

### Query from Python
```python
from retrieval.retrieve import search
results = search("How do slash commands work?", top_k=5)
for r in results:
    print(f"{r['source']}:{r['line']} - {r['text'][:100]}...")
```

## Integration Points
- `knowledge/anthropic-docs/` - Scraped official documentation (12 files)
- `integrations/anthropic/` - Cloned reference repos
- `commands/`, `agents/`, `skills/` - Project components
- `docs/` - Project documentation

## Development Status
- [x] Initial structure
- [x] Architecture design
- [ ] Ingestion pipeline (ingest.py, chunker.py)
- [ ] Embedding generation (embedder.py)
- [ ] Vector storage (store.py)
- [ ] Retrieval API (retrieve.py)
- [ ] Integration with flow-keeper agent
- [ ] CLI query interface

## For Future Agents
When modifying this pipeline:
1. Test with small dataset first (2-3 files)
2. Verify embedding dimensions match (384 for MiniLM)
3. Clear ChromaDB if schema changes: `rm -rf storage/chroma/`
4. Update CONTEXT.md after any structural changes
5. Keep chunk size reasonable (512 tokens prevents truncation)
