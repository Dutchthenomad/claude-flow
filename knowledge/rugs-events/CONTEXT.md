# Rugs-Events Knowledge Base - Agent Context

## Purpose

This folder contains the **canonical source of truth** for rugs.fun WebSocket protocol documentation. All downstream formats (JSONL, JSON indexes, vector embeddings) are derived from the spec file.

## Canonical Source

**`WEBSOCKET_EVENTS_SPEC.md`** - Edit this file to update protocol documentation.

All other documentation in this folder is either:
- **Auto-generated** (in `generated/`) - Do not edit directly
- **Legacy** - Kept for reference, will be removed after migration

## Contents

| File | Type | Purpose |
|------|------|---------|
| `WEBSOCKET_EVENTS_SPEC.md` | **Canonical** | Single source of truth - EDIT THIS |
| `generated/` | Auto-generated | Derived formats for RAG/queries |
| `CONTEXT.md` | Documentation | This file |
| `EVENTS_INDEX.md` | Legacy | Will be removed (merged into spec) |
| `BROWSER_CONNECTION_PROTOCOL.md` | Reference | CDP connection guide |
| `QUICK_REFERENCE.md` | Reference | Fast lookup patterns |
| `CONNECTION_DIAGRAM.md` | Reference | Visual diagrams |

## Architecture

```
WEBSOCKET_EVENTS_SPEC.md (you edit this)
           │
           ▼
    ┌─────────────┐
    │   Parser    │  python -m rag_pipeline.ingest --source rugs-spec
    └─────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
generated/    ChromaDB
├── events.jsonl     (vector search)
├── phase_matrix.json
└── field_index.json
```

## Key Concepts

### Game Cycle Phases

| Phase | Indicators | What Happens |
|-------|------------|--------------|
| COOLDOWN | `cooldownTimer > 0` | Between games, no trading |
| PRESALE | `allowPreRoundBuys = true` | Pre-round buys only |
| ACTIVE | `active = true` | Full trading |
| RUGGED | `rugged = true` | Game ended, positions liquidated |

### Event Categories

| Category | Auth | Examples |
|----------|------|----------|
| Broadcast | No | `gameStateUpdate`, `standard/newTrade` |
| Auth-Required | Yes | `playerUpdate`, `usernameStatus` |
| Request/Response | Yes | `buyOrder`, `sellOrder`, `sidebet` |

### Scope Markers

| Scope | Meaning |
|-------|---------|
| IN_SCOPE | Actively implemented |
| OUT_OF_SCOPE | Documented but not used (tournaments, etc.) |
| FUTURE | Planned for later |

## Usage

### For Humans
Edit `WEBSOCKET_EVENTS_SPEC.md` directly. Use any text editor.

### For Agents
1. Read `WEBSOCKET_EVENTS_SPEC.md` first
2. Check `generated/phase_matrix.json` for event-phase relationships
3. Check `generated/field_index.json` for field lookups

### Regenerating Derived Files
```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m ingestion.ingest --source rugs-spec
```

## Integration Points

| Project | Location | How It Uses This |
|---------|----------|------------------|
| **REPLAYER** | `/home/nomad/Desktop/REPLAYER/` | Event handling implementation |
| **rugs-rl-bot** | `/home/nomad/Desktop/rugs-rl-bot/` | RL environment design |
| **VECTRA-PLAYER** | `/home/nomad/Desktop/VECTRA-PLAYER/` | References (source deleted) |
| **rugs-expert agent** | `agents/rugs-expert.md` | Answers protocol questions |

## Data Sources

| Source | Location | Purpose |
|--------|----------|---------|
| Raw Captures | `~/rugs_recordings/raw_captures/` | Protocol validation |
| Game Recordings | `~/rugs_recordings/*.jsonl` | Historical data (929 games) |

## Quality Standards

When editing `WEBSOCKET_EVENTS_SPEC.md`:

1. **Completeness**: Document ALL fields, not just important ones
2. **Metadata**: Every event needs Scope, Priority, Phases
3. **Examples**: Include real payload examples
4. **Types**: Specify data types (string, number, bool, object, array)
5. **Phase Context**: Note phase-specific behaviors

## Development Status

- [x] Canonical spec established (`WEBSOCKET_EVENTS_SPEC.md`)
- [x] Game Cycle State Machine documented
- [x] Event-Phase Matrix complete
- [x] All events have Scope/Priority/Phases markers
- [x] rugs-expert agent updated
- [ ] Parser implementation (pending)
- [ ] Generated files populated (pending)
- [ ] Legacy files removed (after validation)

---

*This knowledge base is the authoritative source for rugs.fun protocol documentation.*
*Last updated: December 18, 2025*
