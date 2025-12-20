# Event Documentation System Design

**Created**: December 19, 2025
**Status**: Approved - Ready for Implementation
**Author**: Brainstorming session with user

---

## Goal

Create a comprehensive event documentation system for the rugs.fun WebSocket protocol that:
1. Defines every unique event with data types, examples, and relationships
2. Enables the `rugs-expert` agent to serve as sole arbiter of protocol knowledge
3. Guarantees 100% field coverage with verification provenance
4. Supports predictive modeling and RL training data extraction

---

## Current State

| Metric | Value |
|--------|-------|
| Raw WebSocket Recordings | 20 files, 19,207 events |
| Unique Event Types | 29 |
| Total Field Paths | 290 indexed |
| Fields Needing Docs | 262 (OBSERVED status) |
| Fields Validated | 28 (match canonical spec) |
| Fields Stale | 17 (in spec but not in recordings) |

---

## Architecture

### Four-Tier Verification System

| Status | Meaning | Authority | Can Modify Spec |
|--------|---------|-----------|-----------------|
| `THEORETICAL` | Documented externally, never observed in captures | Auto | NO |
| `OBSERVED` | Seen in raw WebSocket captures | Auto | NO |
| `VERIFIED` | Confirmed in multiple captures, structure validated | Auto | NO |
| `CANONICAL` | User-authorized, added to spec | **Human only** | YES |

### Promotion Flow

```
THEORETICAL → OBSERVED → VERIFIED → CANONICAL
     ↓            ↓           ↓           ↓
  (capture)   (validated)  (reviewed)  (USER APPROVES)
    auto         auto        auto       HUMAN GATE
```

### CANONICAL Promotion Laws

**These are LAWS, not guidelines. Violation = session failure.**

1. **Law 1: Single Source of Truth**
   - ONLY `/home/nomad/Desktop/claude-flow/knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md`
   - No other document may contain CANONICAL-status field definitions

2. **Law 2: Human Authorization Gate**
   - NO agent may promote to CANONICAL without explicit user approval
   - Workflow: Agent proposes → User reviews → User approves → Agent commits

3. **Law 3: Physical Validation**
   - Raw capture evidence (file:line)
   - Type verification (matches observed data)
   - Example values (real, not fabricated)
   - Phase context (when does field appear)

4. **Law 4: Audit Trail**
   - Date of approval
   - Evidence used
   - User authorization reference

---

## File Locations

| Purpose | Location |
|---------|----------|
| **Canonical Spec (TRUTH)** | `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md` |
| **Laws Definition** | `knowledge/rugs-events/CONTEXT.md` |
| **Raw Recordings** | `rag-pipeline/RAW SOCKETS/rugs_recordings/raw_captures/` |
| **Discovered Fields** | `knowledge/rugs-events/generated/discovered_fields.json` |
| **Discovered Schemas** | `knowledge/rugs-events/generated/discovered_schemas.json` |
| **Coverage Report** | `knowledge/rugs-events/generated/coverage_report.md` |
| **Diff Report** | `knowledge/rugs-events/generated/diff_report.md` |

---

## Documentation Format

### Hybrid Approach

**1. Tables for Field Overview** (all 290 fields)
```markdown
| Field | Type | Status | Phases | Meaning |
|-------|------|--------|--------|---------|
| `data.price` | number | CANONICAL | ACTIVE | Current multiplier |
| `data.rugpool.threshold` | number | OBSERVED | ALL | Instarug trigger |
```

**2. Rich Structured Blocks for High-Value Fields** (top 30 RL fields)
```markdown
### `data.price`
- **Type**: number
- **Status**: CANONICAL
- **Source**: WEBSOCKET_EVENTS_SPEC.md:219
- **Capture Proof**: 2025-12-14_23-04-44_cdp.jsonl:4523
- **Range**: 0.01 - 1000+ (observed)
- **Phases**: ACTIVE, RUGGED
- **Related**: `data.tickCount` (price changes each tick)
- **RL Use**: Primary reward signal, normalize by entry price
- **Examples**: `1.234`, `45.67`, `0.02`
```

---

## Priority Events for Rich Documentation

| Rank | Event | % Traffic | RL Value | Current Status |
|------|-------|-----------|----------|----------------|
| 1 | `gameStateUpdate` | 64.4% | Critical | Partially documented |
| 2 | `gameStatePlayerUpdate` | 25.0% | Critical | Minimal |
| 3 | `playerUpdate` | 0.3% | Critical | Partial (auth-required) |
| 4 | `standard/newTrade` | 4.7% | High | Minimal |
| 5 | `sidebetEventUpdate` | 0.3% | High | Undocumented |

---

## Multi-Layer Law Distribution

Laws are codified in three locations to ensure redundancy:

| Location | Scope | Purpose |
|----------|-------|---------|
| `knowledge/rugs-events/CONTEXT.md` | Primary | Full law text (authoritative) |
| `agents/rugs-expert.md` | Agent | References laws, enforces them |
| `CLAUDE.md` | Global | Brief mention, points to laws |

---

## Implementation Workflow

### For Promoting OBSERVED → VERIFIED → CANONICAL

```
1. Agent scans discovered_fields.json for OBSERVED fields
2. Agent validates against raw capture (file:line evidence)
3. Agent presents field for promotion:
   - Field path
   - Type
   - Evidence (capture:line)
   - Proposed documentation text
4. User reviews and says "approved" or requests changes
5. Only after approval: Agent adds to WEBSOCKET_EVENTS_SPEC.md
6. Field status becomes CANONICAL
7. Audit entry logged
```

### For Running Ingestion Pipeline

```bash
cd ~/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m ingestion.jsonl_ingest \
  --recordings "RAW SOCKETS/rugs_recordings/raw_captures" \
  --output ../knowledge/rugs-events/generated
```

---

## Consumer

**Sole Consumer**: `rugs-expert` agent

The rugs-expert agent:
- Acts as sole arbiter of rugs.fun protocol knowledge
- MUST read `CONTEXT.md` before any operation
- MUST follow CANONICAL PROMOTION LAWS
- CANNOT modify spec without user approval

---

## Success Criteria

- [ ] All 262 OBSERVED fields reviewed for promotion
- [ ] Top 5 events have rich structured documentation
- [ ] rugs-expert agent enforces laws correctly
- [ ] Coverage report shows 100% of fields catalogued
- [ ] Audit trail exists for all CANONICAL promotions

---

## Files Modified in This Session

| File | Change |
|------|--------|
| `knowledge/rugs-events/CONTEXT.md` | Added CANONICAL PROMOTION LAWS |
| `agents/rugs-expert.md` | Added MANDATORY LAWS section |
| `CLAUDE.md` | Added Rugs.fun Knowledge Base Laws reference |
| `docs/plans/2025-12-19-event-documentation-system-design.md` | This document |

---

*Design approved and ready for implementation.*
