# Embeddings - Agent Context

## Purpose
Vector embedding generation. Converts text chunks into dense vector representations for semantic search.

## Responsibilities
- Generate embeddings from text chunks
- Implement embedding caching
- Support multiple embedding providers
- Batch processing for efficiency

## Planned Components
| File | Description |
|------|-------------|
| `embedder.py` | Main embedding generator |
| `cache.py` | Embedding cache management |
| `providers/` | Provider implementations (OpenAI, local) |

## Configuration
- Default model: `text-embedding-3-small` (1536 dimensions)
- Alternative: Local models via sentence-transformers

## Development Status
- [x] Initial structure
- [ ] OpenAI embedder
- [ ] Caching layer
- [ ] Local model support
- [ ] Integration tests
