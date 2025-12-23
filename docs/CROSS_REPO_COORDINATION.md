# Cross-Repository Coordination - claude-flow Role

**Status:** Active
**Created:** December 18, 2025
**Purpose:** Define claude-flow's role in the VECTRA-PLAYER/claude-flow/rugs-rl-bot ecosystem

---

## claude-flow's Role: Knowledge Indexer & Protocol Expert

claude-flow is responsible for:
1. **Canonical Protocol Documentation** - Single source of truth for rugs.fun WebSocket events
2. **Semantic Vector Index** - ChromaDB index built from knowledge base + VECTRA-PLAYER data
3. **rugs-expert Agent** - RAG-powered protocol specialist for answering event questions

---

## Data Flow Architecture

```
                    ┌─────────────────────────────────────────┐
                    │          VECTRA-PLAYER                   │
                    │   (WebSocket → Parquet writer)          │
                    └─────────────────┬───────────────────────┘
                                      │ writes
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │         ~/rugs_data/events_parquet/      │
                    │   (Canonical game data - Parquet)        │
                    └────────┬────────────────────┬───────────┘
                             │                    │
                reads for    │                    │ reads for
                indexing     ▼                    ▼ training
            ┌─────────────────────┐    ┌─────────────────────┐
            │    claude-flow       │    │    rugs-rl-bot      │
            │  ┌───────────────┐   │    │  ┌───────────────┐  │
            │  │ ChromaDB      │   │    │  │ DuckDB Query  │  │
            │  │ Vector Index  │   │    │  │ (features)    │  │
            │  └───────────────┘   │    │  └───────────────┘  │
            │  ┌───────────────┐   │    │                     │
            │  │ rugs-expert   │   │    │                     │
            │  │ agent         │   │    │                     │
            │  └───────────────┘   │    │                     │
            └─────────────────────┘    └─────────────────────┘
```

---

## Database Ownership (IMPORTANT)

| Repository | Vector DB | Analytical DB | Purpose |
|------------|-----------|---------------|---------|
| **claude-flow** | ChromaDB | None | Semantic search over protocol docs |
| **rugs-rl-bot** | None | DuckDB | Feature engineering for RL training |
| **VECTRA-PLAYER** | None | None | Writes Parquet only (no queries) |

**CRITICAL:** claude-flow does NOT use DuckDB. Each repository owns its database layer independently. Cross-repo validation (shown below) runs from the appropriate repository context.

---

## Knowledge Sources

### 1. Protocol Documentation (Always Indexed)

| Source | Location | Content |
|--------|----------|---------|
| WebSocket Spec | `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md` | Canonical event definitions |
| Game Cycle | `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md#game-cycle` | Phase state machine |
| Agent Definition | `agents/rugs-expert.md` | Query protocol |

### 2. Game Recording Data (Future - VECTRA-PLAYER Integration)

| Source | Location | Content |
|--------|----------|---------|
| Game Ticks | `~/rugs_data/events_parquet/doc_type=game_tick/` | Price/tick stream |
| Player Actions | `~/rugs_data/events_parquet/doc_type=player_action/` | Trading history |
| Raw Events | `~/rugs_data/events_parquet/doc_type=ws_event/` | Full WebSocket payloads |

---

## RAG Pipeline

### Technology Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Vector DB | ChromaDB | Local, serverless, persistent |
| Embeddings | all-MiniLM-L6-v2 | 384 dimensions, runs locally |
| Chunking | Markdown-aware | 512 tokens, 50 overlap |

### Commands

```bash
# Index knowledge base
cd rag-pipeline
source .venv/bin/activate
python -m ingestion.ingest

# Query from Python
from retrieval.retrieve import search
results = search("What fields are in gameStateUpdate?", top_k=5)
```

### Current Index Stats

- **Total Chunks:** 211
- **From WEBSOCKET_EVENTS_SPEC.md:** 15 chunks
- **From rugs-expert.md:** 4 chunks

---

## Integration with VECTRA-PLAYER

### Phase 1: Protocol Knowledge (CURRENT)
- claude-flow indexes static protocol documentation
- rugs-expert answers event/field questions
- No live data integration yet

### Phase 2: Game Data Indexing (FUTURE)
- VECTRA-PLAYER writes Parquet to `~/rugs_data/events_parquet/`
- claude-flow indexes selected chunks for semantic search
- Enables queries like "Show me games where price reached 100x"

### Interface Contract

```python
# VECTRA-PLAYER writes (DO NOT MODIFY from claude-flow)
~/rugs_data/events_parquet/doc_type=*/date=YYYY-MM-DD/*.parquet

# claude-flow reads and indexes
~/rugs_data/events_parquet/**/*.parquet → ChromaDB

# Schema version coordination
~/rugs_data/manifests/schema_version.json
```

---

## Shared Configuration

### Environment Variables

| Variable | Default | Used By |
|----------|---------|---------|
| `RUGS_DATA_DIR` | `~/rugs_data/` | All repos |
| `RUGS_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | claude-flow |
| `RUGS_SCHEMA_VERSION` | `1.0.0` | All repos |

### Schema Version Contract

All repos must check `~/rugs_data/manifests/schema_version.json`:

```json
{
  "version": "1.0.0",
  "embedding_model": "all-MiniLM-L6-v2",
  "vector_db": "chromadb"
}
```

**Version Bump Rules:**
1. **Patch (1.0.x):** New optional fields, backward compatible
2. **Minor (1.x.0):** New required fields, migration needed
3. **Major (x.0.0):** Breaking changes, full rebuild required

---

## rugs-expert Agent

### Capabilities

1. **Answer Event Questions** - Field definitions, types, phases
2. **Debug Event Issues** - Expected vs actual behavior
3. **Guide Implementation** - Which events for which features

### Query Protocol

```bash
# Step 1: Agent reads canonical spec
cat knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md

# Step 2: Check generated indexes (when available)
cat knowledge/rugs-events/generated/phase_matrix.json

# Step 3: Query ChromaDB for context
python -c "from retrieval.retrieve import search; print(search('...'))"
```

### Output Format

When answering event questions, include:
- Event name, purpose, frequency
- Auth requirements, scope, priority
- Phases where event fires
- Key fields with types
- Example payload
- REPLAYER code locations

---

## Development Workflow

### Adding a New Event Type

1. **claude-flow:** Update `WEBSOCKET_EVENTS_SPEC.md`
2. **claude-flow:** Re-run `python -m ingestion.ingest`
3. **VECTRA-PLAYER:** Add Pydantic model in `src/models/events/`
4. **VECTRA-PLAYER:** Update EventStore schema
5. **rugs-rl-bot:** Update feature engineering if needed

### Validating Protocol Changes

```bash
# In claude-flow (ChromaDB semantic search)
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m retrieval.retrieve "playerUpdate fields" -k 5

# Cross-repo validation: Run from rugs-rl-bot (NOT claude-flow)
# This uses DuckDB which is owned by rugs-rl-bot
cd /home/nomad/Desktop/rugs-rl-bot
duckdb -c "SELECT DISTINCT json_keys(raw_json) FROM '~/rugs_data/**/*.parquet' WHERE event_name = 'playerUpdate'"
```

---

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| VECTRA-PLAYER Coordination | `/home/nomad/Desktop/VECTRA-PLAYER/docs/CROSS_REPO_COORDINATION.md` | Full system overview |
| WebSocket Spec | `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md` | Canonical source |
| RAG Pipeline | `rag-pipeline/CONTEXT.md` | Implementation details |
| rugs-expert Agent | `agents/rugs-expert.md` | Agent definition |

---

*Last Updated: December 18, 2025*
