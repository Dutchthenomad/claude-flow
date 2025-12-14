# Ingestion - Agent Context

## Purpose
Document ingestion and conversion layer. Transforms various document formats into a unified structure for embedding.

## Responsibilities
- Multi-format document parsing (PDF, DOCX, HTML, MD, TXT)
- Audio transcription (MP3 → text via Whisper)
- Semantic chunking with overlap
- Metadata extraction

## Planned Components
| File | Description |
|------|-------------|
| `ingest.py` | Main ingestion orchestrator |
| `chunker.py` | Semantic document splitter |
| `parsers/` | Format-specific parsers |

## Development Status
- [x] Initial structure
- [ ] Markdown parser
- [ ] PDF parser
- [ ] Chunking strategy
- [ ] Integration tests
