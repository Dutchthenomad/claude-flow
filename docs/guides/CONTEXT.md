# Guides - Agent Context

## Purpose
Comprehensive guides for replicating and extending claude-flow patterns to other projects.

## Contents
| Guide | Description |
|-------|-------------|
| `RAG_PIPELINE_REPLICATION.md` | Step-by-step guide for creating RAG pipelines in any project |

## Key Topics Covered

### RAG Pipeline Replication
- Architecture pattern (Ingest → Chunk → Embed → Store → Retrieve)
- Technology stack (ChromaDB, sentence-transformers)
- Step-by-step setup instructions
- Customization points (data formats, embedding models, metadata)
- **REPLAYER WebSocket Events** - Specific guidance for the rugs.fun event pipeline
- Event type taxonomy
- Custom chunker examples
- Testing and maintenance

## For Future Agents
When adding new guides:
1. Follow the established format (Overview, Steps, Examples, Reference)
2. Include concrete code examples
3. Reference the claude-flow implementation as baseline
4. Update this CONTEXT.md with new entries
