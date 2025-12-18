# Rugs Knowledge Base Design

**Date:** December 18, 2025
**Status:** Approved
**Purpose:** Single source of truth for rugs.fun WebSocket protocol documentation

---

## Executive Summary

Establish `WEBSOCKET_EVENTS_SPEC.md` as the canonical, human-editable source of truth for all rugs.fun protocol documentation. All downstream formats (JSONL, JSON indexes, vector embeddings) are derived and auto-generated.

**Core Principle:** Edit one file, everything else regenerates.

---

## Section 1: Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CANONICAL SOURCE                          │
│  knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md              │
│  (human-editable, version-controlled)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Parse & Index  │  (automated on change)
                    │    Pipeline     │
                    └─────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  JSONL   │   │   JSON   │   │  Vector  │
        │ (RAG KB) │   │ (indexes)│   │ (search) │
        └──────────┘   └──────────┘   └──────────┘
```

### Directory Structure

```
claude-flow/knowledge/rugs-events/
├── WEBSOCKET_EVENTS_SPEC.md     # Canonical (you edit this)
├── CONTEXT.md                    # Folder documentation
├── generated/                    # Auto-generated (don't edit)
│   ├── events.jsonl             # RAG-queryable format
│   ├── phase_matrix.json        # Event-phase relationships
│   └── field_index.json         # Quick field lookup
```

### Benefits

- Single file to maintain
- Markdown is readable, diffable, git-friendly
- Downstream formats are disposable/rebuildable
- Version history shows exactly what changed

---

## Section 2: Game Cycle State Machine

Events and fields have different meanings depending on the game phase.

### Phases

| Phase | Trigger | Duration | Key Indicators |
|-------|---------|----------|----------------|
| `COOLDOWN` | Previous game rugged | ~10-30 sec | `cooldownTimer > 0`, `active = false` |
| `PRESALE` | Cooldown ends | Until first tick | `allowPreRoundBuys = true`, `active = false` |
| `ACTIVE` | Game starts | Variable | `active = true`, `rugged = false` |
| `RUGGED` | Rug event | Instant | `rugged = true` |

### Phase Transitions

```
COOLDOWN ──(timer=0)──▶ PRESALE ──(game starts)──▶ ACTIVE ──(rug)──▶ RUGGED ──▶ COOLDOWN
```

### Event-Phase Matrix

| Event | COOLDOWN | PRESALE | ACTIVE | RUGGED |
|-------|----------|---------|--------|--------|
| `gameStateUpdate` | Y | Y | Y | Y |
| `standard/newTrade` | - | Y | Y | - |
| `playerUpdate` | - | Y | Y | Y |
| `sidebetResponse` | - | - | Y | - |
| `usernameStatus` | Y | Y | Y | Y |

---

## Section 3: Spec Document Structure

### Event Section Template

```markdown
### eventName [STATUS]

**Frequency**: ~4x/second | Once on connection | On action
**Auth Required**: Yes | No
**Scope**: IN_SCOPE | OUT_OF_SCOPE | FUTURE
**Priority**: P0 | P1 | P2
**Phases**: COOLDOWN, PRESALE, ACTIVE, RUGGED

**Phase-Specific Notes**:
- PRESALE: [behavior during presale]
- ACTIVE: [behavior during active gameplay]

#### Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `fieldName` | string | `"example"` | What this field represents |

#### Example Payload

\`\`\`json
{
  "fieldName": "example"
}
\`\`\`
```

### Metadata Markers

| Marker | Values | Purpose |
|--------|--------|---------|
| Status | `VERIFIED`, `NEEDS_REVIEW`, `DEPRECATED` | Review state |
| Scope | `IN_SCOPE`, `OUT_OF_SCOPE`, `FUTURE` | Implementation filter |
| Priority | `P0`, `P1`, `P2` | Implementation order |
| Phases | Comma-separated phase names | When event fires |

---

## Section 4: Pipeline Implementation

### Location

`claude-flow/rag-pipeline/ingestion/rugs_spec_parser.py`

### Parser Logic

```python
def parse_spec(spec_path: Path) -> dict:
    """Parse WEBSOCKET_EVENTS_SPEC.md into structured data."""
    events = []
    phases = []

    for section in parse_markdown_sections(spec_path):
        if section.is_phase_definition():
            phases.append(parse_phase(section))
        elif section.is_event():
            event = {
                'name': section.header,
                'status': extract_status(section),
                'scope': extract_metadata('Scope', section),
                'priority': extract_metadata('Priority', section),
                'phases': extract_metadata('Phases', section),
                'auth_required': extract_metadata('Auth Required', section),
                'frequency': extract_metadata('Frequency', section),
                'fields': parse_field_tables(section),
                'examples': extract_code_blocks(section),
                'phase_notes': extract_phase_notes(section),
            }
            events.append(event)

    return {
        'phases': phases,
        'events': events,
        'phase_matrix': build_phase_matrix(events),
    }
```

### Outputs

| Output | Format | Purpose |
|--------|--------|---------|
| `events.jsonl` | JSON Lines | RAG semantic search |
| `phase_matrix.json` | JSON | Event-phase lookups |
| `field_index.json` | JSON | Field name lookups |

### Triggers

1. **Manual:** `python -m rag_pipeline.ingest --source rugs-spec`
2. **Git hook:** Auto-run on commit to `WEBSOCKET_EVENTS_SPEC.md`
3. **Watch mode:** File watcher during editing sessions

### Validation

Parser warns on:
- Missing required metadata (Scope, Phases)
- Inconsistent field table columns
- Undefined phase references
- Duplicate event definitions

---

## Section 5: Agent Query Interface

### Query Patterns

| Query Type | Example | Method |
|------------|---------|--------|
| Event lookup | "What fields are in gameStateUpdate?" | Direct file read |
| Phase query | "What events fire during PRESALE?" | phase_matrix.json |
| Field search | "What field tracks player balance?" | field_index.json |
| Semantic search | "How do I detect a rug event?" | ChromaDB/RAG |

### Query Priority

1. **Exact match** - Check field_index.json first (fast)
2. **Phase lookup** - Check phase_matrix.json for relationships
3. **Semantic search** - Fall back to RAG for fuzzy questions
4. **Direct read** - Read spec section for full context

### Agent Configuration

```markdown
# In agents/rugs-expert.md

## Knowledge Sources (Priority Order)

1. knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md (canonical)
2. knowledge/rugs-events/generated/phase_matrix.json (relationships)
3. knowledge/rugs-events/generated/field_index.json (field lookup)
4. ChromaDB collection: rugs-events (semantic search)
```

---

## Section 6: Consolidation Plan

### Sources to Merge

| Source | Location | Action |
|--------|----------|--------|
| VECTRA-PLAYER spec | `docs/Web Socket Events/WEBSOCKET_EVENTS_SPEC.md` | **Primary source** |
| claude-flow EVENTS_INDEX | `knowledge/rugs-events/EVENTS_INDEX.md` | Merge unique content |
| Auto-generated JSONL | `docs/rag/socket_kb.jsonl` | Extract examples |

### Migration Steps

1. **Copy** VECTRA-PLAYER spec to claude-flow canonical location
2. **Enhance** with Game Cycle State Machine section
3. **Add** Event-Phase Matrix
4. **Add** Scope/Priority/Phase markers to each event
5. **Merge** any unique content from EVENTS_INDEX.md
6. **Review** each event for accuracy
7. **Build** pipeline to generate downstream formats
8. **Delete** redundant source files from other projects

### Post-Migration

- VECTRA-PLAYER references `claude-flow/knowledge/rugs-events/`
- REPLAYER references `claude-flow/knowledge/rugs-events/`
- rugs-rl-bot references `claude-flow/knowledge/rugs-events/`
- All redundant copies deleted

---

## Section 7: Success Criteria

### Knowledge Base Complete When:

- [ ] All events documented with required metadata
- [ ] Game Cycle State Machine defined
- [ ] Event-Phase Matrix complete
- [ ] Each field has verified description
- [ ] Pipeline generates all downstream formats
- [ ] rugs-expert agent can query successfully
- [ ] Redundant sources deleted

### Validation Checklist:

- [ ] Every event has Scope marker
- [ ] Every event has Phase(s) listed
- [ ] Every field has Type and Description
- [ ] Examples match actual payloads
- [ ] Phase transitions documented
- [ ] Auth requirements verified

---

## References

- **Current VECTRA-PLAYER spec:** `/home/nomad/Desktop/VECTRA-PLAYER/docs/Web Socket Events/WEBSOCKET_EVENTS_SPEC.md`
- **Current claude-flow events:** `/home/nomad/Desktop/claude-flow/knowledge/rugs-events/`
- **Raw captures:** `/home/nomad/rugs_recordings/raw_captures/`
- **rugs-expert agent:** `/home/nomad/Desktop/claude-flow/agents/rugs-expert.md`

---

*Approved: December 18, 2025*
