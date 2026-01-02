# RAG Pipeline - Agent Context

## Purpose
Local RAG (Retrieval-Augmented Generation) system for the claude-flow knowledge base. Provides semantic search over project documentation, code, and scraped Anthropic docs.

## Architecture

```
rag-pipeline/
├── config.py                     # Configuration settings
├── requirements.txt              # Core Python dependencies
├── requirements-langchain.txt    # Optional LangChain hybrid deps
├── ingestion/                    # Document processing
│   ├── ingest.py                 # Main ingestion script
│   ├── jsonl_ingest.py           # JSONL event ingestion
│   └── chunker.py                # Text chunking logic
├── embeddings/                   # Vector embedding
│   └── embedder.py               # Sentence-transformers wrapper
├── storage/                      # ChromaDB persistence
│   ├── chroma/                   # Database files (~23MB, 1169 chunks)
│   ├── hf_cache/                 # Cached HuggingFace models
│   └── store.py                  # Storage abstraction
└── retrieval/                    # Query interface
    ├── retrieve.py               # Main search API (backend toggle)
    ├── langchain_hybrid.py       # Hybrid backend (dense+BM25+rerank)
    └── CONTEXT.md                # Retrieval module docs
```

## Technology Stack
- **Vector DB**: ChromaDB (local, serverless, no external dependencies)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2, runs locally)
- **Chunking**: Markdown-aware text splitting with overlap
- **Hybrid Retrieval** (optional): LangChain ensemble retriever + cross-encoder rerank

## Retrieval Backends

### Native Backend (default)
- Dense vector similarity (cosine)
- Scores: 0.0-1.0 (higher = more similar)
- Best for semantic similarity queries

### Hybrid Backend (optional)
- Dense Chroma + BM25 lexical + cross-encoder rerank
- Enable: `CLAUDE_FLOW_RAG_BACKEND=langchain_hybrid`
- Best for field-specific lookups and exact term matching
- Requires: `pip install -r requirements-langchain.txt`

## Data Flow
```
Documents → Chunking → Embeddings → ChromaDB → Semantic Search
                                                      ↓
                                    Native (dense) OR Hybrid (dense+BM25+rerank)
```

1. **Ingest**: Read markdown/code files from knowledge/, docs/, commands/
2. **Chunk**: Split into semantic chunks (512 tokens max, 50 token overlap)
3. **Embed**: Generate 384-dim vectors with sentence-transformers
4. **Store**: Persist to ChromaDB (./storage/chroma/)
5. **Retrieve**: Native or hybrid search returns top-k chunks

## Usage

### Initial Setup
```bash
cd rag-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: Enable hybrid retrieval
pip install -r requirements-langchain.txt
```

### Index Knowledge Base
```bash
python -m ingestion.ingest
```

### Query from Python
```python
from retrieval.retrieve import search

# Native backend (default)
results = search("How do slash commands work?", top_k=5)

# Hybrid backend (better for field lookups)
results = search("data.price", top_k=5, backend="langchain_hybrid")

for r in results:
    print(f"{r['source']}:{r['line_start']} - {r['text'][:100]}...")
```

### CLI Query
```bash
# Native
python -m retrieval.retrieve "playerUpdate fields" -k 5

# Hybrid
CLAUDE_FLOW_RAG_BACKEND=langchain_hybrid python -m retrieval.retrieve "data.price" -k 5
```

## Integration Points
- `knowledge/anthropic-docs/` - Scraped official documentation
- `knowledge/rugs-events/` - WebSocket protocol documentation
- `integrations/anthropic/` - Cloned reference repos
- `commands/`, `agents/`, `skills/` - Project components
- `docs/` - Project documentation
- `mcp-server/` - MCP server uses search via `search_knowledge()` tool

## Development Status
- [x] Initial structure
- [x] Architecture design
- [x] Ingestion pipeline (ingest.py, chunker.py)
- [x] Embedding generation (embedder.py)
- [x] Vector storage (store.py)
- [x] Retrieval API (retrieve.py)
- [x] CLI query interface
- [x] **LangChain hybrid backend** (langchain_hybrid.py)
- [x] **Cross-encoder reranking** (optional)
- [x] **Integration with rugs-expert agent**
- [ ] Integration with flow-keeper agent
- [ ] MCP tool backend parameter exposed

## Current Index Stats
- **Documents**: 1169 chunks indexed
- **Database size**: ~23MB (storage/chroma/chroma.sqlite3)
- **Embedding model**: all-MiniLM-L6-v2 (384 dimensions)
- **Cross-encoder**: cross-encoder/ms-marco-MiniLM-L-6-v2 (optional)

## For Future Agents
When modifying this pipeline:
1. Test with small dataset first (2-3 files)
2. Verify embedding dimensions match (384 for MiniLM)
3. Clear ChromaDB if schema changes: `rm -rf storage/chroma/`
4. Update CONTEXT.md after any structural changes
5. Keep chunk size reasonable (512 tokens prevents truncation)
6. Run tests: `.venv/bin/python -m pytest -q` (43 tests)
