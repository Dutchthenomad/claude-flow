# Ingestion - Agent Context

## Purpose
Document ingestion and chunking for the RAG pipeline. Reads files from knowledge sources and splits them into semantic chunks.

## Contents
| File | Description |
|------|-------------|
| `ingest.py` | Main ingestion script - orchestrates the pipeline |
| `chunker.py` | Text chunking with markdown awareness |
| `__init__.py` | Package exports |

## Key Functions

### `ingest.py`
- `ingest_all()` - Index all knowledge sources
- `ingest_file(path)` - Index a single file
- `clear_index()` - Remove all indexed documents

### `chunker.py`
- `chunk_text(text, metadata)` - Split text into chunks
- `chunk_markdown(text, metadata)` - Markdown-aware splitting

## Configuration
Uses settings from `../config.py`:
- `KNOWLEDGE_PATHS` - Directories to index
- `INCLUDE_PATTERNS` - File extensions to include
- `CHUNK_SIZE` - Max tokens per chunk (512)
- `CHUNK_OVERLAP` - Overlap between chunks (50)

## Usage
```bash
# From rag-pipeline/
python -m ingestion.ingest
```

## For Future Agents
- Chunker preserves markdown headers for context
- Each chunk includes source file and line number metadata
- Re-indexing is idempotent (clears and rebuilds)
