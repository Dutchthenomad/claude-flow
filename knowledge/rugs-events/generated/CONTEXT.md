# Generated Files - Do Not Edit

This directory contains auto-generated files derived from `WEBSOCKET_EVENTS_SPEC.md`.

**DO NOT EDIT THESE FILES DIRECTLY.**

Edit the canonical source instead:
- `../WEBSOCKET_EVENTS_SPEC.md`

## Contents

| File | Purpose | Regenerate Command |
|------|---------|-------------------|
| `events.jsonl` | RAG-queryable event documentation | `python -m rag_pipeline.ingest --source rugs-spec` |
| `phase_matrix.json` | Event-phase relationship lookup | (same command) |
| `field_index.json` | Field name quick lookup | (same command) |

## Regeneration

These files are regenerated when:
1. Manual run of ingestion pipeline
2. Git hook on commit to `WEBSOCKET_EVENTS_SPEC.md`
3. Session start hook (optional)

## Schema

### events.jsonl
```json
{
  "event_name": "gameStateUpdate",
  "scope": "IN_SCOPE",
  "priority": "P0",
  "phases": ["COOLDOWN", "PRESALE", "ACTIVE", "RUGGED"],
  "auth_required": false,
  "frequency": "~4x/second",
  "fields": [...],
  "text": "Full searchable text for RAG"
}
```

### phase_matrix.json
```json
{
  "COOLDOWN": ["gameStateUpdate", "usernameStatus", ...],
  "PRESALE": ["gameStateUpdate", "standard/newTrade", ...],
  "ACTIVE": ["gameStateUpdate", "sidebetResponse", ...],
  "RUGGED": ["gameStateUpdate", "playerUpdate", ...]
}
```

### field_index.json
```json
{
  "price": {"event": "gameStateUpdate", "type": "float", "description": "..."},
  "cash": {"event": "playerUpdate", "type": "float", "description": "..."},
  ...
}
```

---

*Auto-generated directory. Last structure update: December 18, 2025*
