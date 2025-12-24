# Knowledge - Agent Context

## Purpose
Repository of scraped and curated documentation. This is the **source material** that feeds into the RAG pipeline.

**claude-flow OWNS this knowledge base.** All protocol documentation, empirical validation, and agent knowledge lives here.

## Contents
| Folder | Description | Owner |
|--------|-------------|-------|
| `anthropic-docs/` | Official Claude Code and Anthropic documentation | claude-flow |
| `rugs-events/` | Rugs.fun WebSocket protocol, CDP connection, empirical validation | claude-flow |
| `rugs-strategy/` | Trading strategies, probability models, PRNG analysis (L1-L7 layers) | claude-flow |

## Rugs.fun Knowledge Structure

```
rugs-events/
├── WEBSOCKET_EVENTS_SPEC.md     # CANONICAL protocol documentation
├── CONTEXT.md                    # CANONICAL PROMOTION LAWS
├── staging/                      # Pre-ingestion empirical validation
│   └── YYYY-MM-DD-description/   # Capture packages awaiting review
└── captures/                     # Archived validated captures

rugs-strategy/
├── L1-game-mechanics/            # Core game rules
├── L2-protocol/                  # Event schemas, confirmation mapping
├── L5-strategy-tactics/          # Trading strategies
├── L6-statistical-baselines/     # Empirical data
└── L7-advanced-analytics/        # PRNG, Bayesian models (theoretical)
```

## Cross-Repository Coordination

| Data Source | Owner | Consumers |
|-------------|-------|-----------|
| Parquet files (`~/rugs_data/`) | VECTRA-PLAYER writes | claude-flow, rugs-rl-bot read |
| Protocol spec | **claude-flow** | VECTRA-PLAYER, rugs-rl-bot |
| ChromaDB vectors | **claude-flow** | rugs-expert agent |
| ML models | rugs-rl-bot | VECTRA-PLAYER (future) |

See VECTRA-PLAYER's `docs/CROSS_REPO_COORDINATION.md` for full integration details.

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
