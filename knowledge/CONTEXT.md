# Knowledge - Agent Context

## Purpose
Repository of scraped and curated documentation. This is the **source material** that feeds into the RAG pipeline.

## Contents
| Folder | Description |
|--------|-------------|
| `anthropic-docs/` | Official Claude Code and Anthropic documentation |
| `rugs-events/` | Rugs.fun WebSocket protocol and CDP connection docs |

## Planned Content
- Claude Code documentation (complete)
- Claude API documentation
- Agent SDK documentation
- Best practices and tutorials

## Integration Points
- Indexed by `rag-pipeline/ingestion/`
- Searchable via `rag-pipeline/retrieval/`
- Updated via scraping scripts

## Development Status
- [x] Initial structure
- [ ] Anthropic docs scraped
- [ ] Index created
- [ ] Update automation
- [ ] Production ready

## For Future Agents
When adding knowledge:
1. Organize by source (e.g., `anthropic-docs/`, `community/`)
2. Preserve original structure where possible
3. Include metadata (source URL, date scraped)
4. Re-run ingestion after adding content
5. Verify search retrieves new content
