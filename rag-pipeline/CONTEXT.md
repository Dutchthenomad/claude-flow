# RAG Pipeline - Agent Context

## Purpose
This folder contains the **Retrieval-Augmented Generation pipeline** - a system for ingesting, embedding, storing, and retrieving documentation to enhance agent capabilities.

## Architecture Overview
```
Documents → Ingestion → Chunking → Embeddings → Vector DB → Semantic Search → LLM
```

## Contents
| Folder | Description |
|--------|-------------|
| `ingestion/` | Document processing (PDF, MD, HTML, etc.) |
| `embeddings/` | Vector generation using embedding models |
| `storage/` | Vector database (PGVector/ChromaDB) |
| `retrieval/` | Semantic search and query processing |

## Reference Implementation
Based on: [ottomator-agents/docling-rag-agent](https://github.com/coleam00/ottomator-agents/tree/main/docling-rag-agent)

## Technology Stack (Planned)
- **Ingestion**: Docling for multi-format conversion
- **Embeddings**: OpenAI text-embedding-3-small (or local alternatives)
- **Storage**: PostgreSQL + PGVector extension
- **Retrieval**: Cosine similarity search

## Integration Points
- Feeds knowledge to agents via tool calls
- Indexes `knowledge/` folder documentation
- Provides semantic search for codebase questions

## Development Status
- [x] Initial structure
- [ ] Ingestion pipeline
- [ ] Embedding generation
- [ ] Vector storage
- [ ] Retrieval API
- [ ] Integration with agents

## For Future Agents
When developing the RAG pipeline:
1. Start with simple document types (Markdown)
2. Use chunking strategies that preserve context
3. Implement caching for embeddings
4. Add metadata filtering for precise retrieval
5. Monitor and tune retrieval quality
6. Consider local embedding models for privacy
