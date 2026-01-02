# BotActionInterface Documentation Plan

**Created:** 2025-12-25
**Status:** PLANNING
**Related:** VECTRA-PLAYER Phase 6 Implementation

---

## Overview

The BotActionInterface (Player Piano Architecture) was implemented in VECTRA-PLAYER on 2025-12-25. This document outlines the documentation work needed to integrate this knowledge into the rugipedia system.

**Implementation Location:** `/home/nomad/Desktop/VECTRA-PLAYER/src/bot/action_interface/`
**Plan File:** `/home/nomad/.claude/plans/wise-jinkling-acorn.md`
**Tests:** 166 new tests, 1092 total passing

---

## What Was Built

### Player Piano Architecture

A unified action execution layer supporting 4 modes:

```
RECORDING   → Human plays, system records inputs with full context
TRAINING    → RL model trains with fast SimulatedExecutor
VALIDATION  → Model replays pre-recorded games with UI animation
LIVE        → Real browser automation (v1.0 stub, v2.0 PuppeteerExecutor)
```

### Files Created

```
src/bot/action_interface/
├── __init__.py
├── types.py                    # ActionParams, ActionResult, ExecutionMode, GameContext
├── interface.py                # BotActionInterface orchestrator
├── factory.py                  # create_for_training/recording/validation/live
├── executors/
│   ├── base.py                 # ActionExecutor ABC
│   ├── simulated.py            # SimulatedExecutor (TradeManager)
│   └── tkinter.py              # TkinterExecutor (UI layer)
├── confirmation/
│   ├── monitor.py              # ConfirmationMonitor (latency via EventBus)
│   └── mock.py                 # MockConfirmationMonitor
├── state/
│   └── tracker.py              # StateTracker (HYBRID: LiveStateProvider + GameState)
└── recording/
    └── human_interceptor.py    # HumanActionInterceptor (async recording)
```

### Key Concepts

1. **HYBRID StateTracker** - Uses LiveStateProvider in live mode, GameState fallback in replay
2. **Latency Chain** - client_ts → server_ts → confirmed_ts for timing analysis
3. **Schema v2.0.0 Reuse** - Extends existing PlayerState, ActionType from models/events
4. **Factory Pattern** - Simple functions for each execution mode

---

## Documentation Tasks

### Priority 1: L4-vectra-codebase (CRITICAL)

**Location:** `/home/nomad/Desktop/claude-flow/knowledge/rugs-strategy/L4-vectra-codebase/`

| Document | Purpose | Est. Time |
|----------|---------|-----------|
| `bot-action-interface-architecture.md` | Comprehensive architecture overview | 3 hours |
| `state-tracker-hybrid-design.md` | HYBRID live/replay state approach | 2 hours |
| `bot-action-interface-factory-patterns.md` | Factory usage and mode selection | 2 hours |

**Total: ~7 hours**

#### Architecture Doc Sections
- Overview (Player Piano concept)
- Core Components (Interface, Executor, Monitor, Tracker)
- Execution Modes Deep Dive
- Data Flow Diagrams
- Integration Points (EventBus, EventStore, LiveStateProvider)

#### State Design Doc Sections
- The Hybrid Problem (live vs replay)
- StateTracker Solution
- PlayerState Schema
- Cross-references to Schema v2.0.0

#### Factory Patterns Doc Sections
- Factory Functions (all 4)
- Mode Selection Decision Tree
- Configuration Examples

### Priority 2: Cross-Reference Updates (HIGH)

**Location:** `/home/nomad/Desktop/claude-flow/knowledge/rugs-events/`

| Document | Update | Est. Time |
|----------|--------|-----------|
| `WEBSOCKET_EVENTS_SPEC.md` | Add BotActionInterface integration section | 1 hour |
| `CONTEXT.md` | Add VECTRA-PLAYER integration section | 30 min |

**Total: ~1.5 hours**

**Content to Add:**
- How ConfirmationMonitor uses playerUpdate events
- Confirmation flow diagram
- Links to L4 codebase docs

### Priority 3: RAG Ingestion (MEDIUM)

| Task | Description | Est. Time |
|------|-------------|-----------|
| Create ChromaDB collection | `vectra_player_codebase` | 30 min |
| Run ingestion pipeline | Chunk and embed new docs | 30 min |
| Validate queries | Test retrieval accuracy | 30 min |

**Total: ~1.5 hours**

**Metadata Schema:**
```python
{
    "doc_type": "architecture" | "factory_pattern" | "state_design",
    "layer": "L4-vectra-codebase",
    "component": "BotActionInterface" | "StateTracker" | "ConfirmationMonitor",
    "related_schema": "player_action" | "server_state",
}
```

### Priority 4: Conceptual Docs (LOW/OPTIONAL)

**Location:** `/home/nomad/Desktop/claude-flow/knowledge/rugs-strategy/L5-strategy-tactics/`

| Document | Purpose | Est. Time |
|----------|---------|-----------|
| `player-piano-architecture.md` | High-level concept explanation | 2 hours |

---

## Cross-Reference Map

```
player_action (Schema v2.0.0)
    ↓
BotActionInterface (L4)
    ↓
├─ ActionExecutor (SimulatedExecutor, TkinterExecutor)
├─ ConfirmationMonitor (playerUpdate subscription)
└─ StateTracker (LiveStateProvider + GameState)
    ↓
EventStore (Parquet persistence)
    ↓
ChromaDB (Vector search)
```

---

## Questions Docs Should Answer

### Architecture Questions
1. What is the Player Piano Architecture?
2. How does BotActionInterface work?
3. What are the 4 execution modes?
4. How is latency tracked?

### Implementation Questions
5. How do I create a BotActionInterface for training?
6. How do I switch execution modes?
7. How does StateTracker handle live vs replay?
8. What events does ConfirmationMonitor subscribe to?

### Integration Questions
9. How does this integrate with Schema v2.0.0?
10. Which WebSocket events are used?
11. How does this integrate with EventStore?
12. Can I use this with rugs-rl-bot?

---

## Estimated Total Effort

| Phase | Hours |
|-------|-------|
| L4 Core Docs | 7 |
| Cross-Reference Updates | 1.5 |
| RAG Ingestion | 1.5 |
| Optional L5 Concept Doc | 2 |
| **Total** | **10-12 hours** |

---

## Session Checklist

When starting the documentation session:

- [ ] Read this plan
- [ ] Read `/home/nomad/.claude/plans/wise-jinkling-acorn.md` (implementation plan)
- [ ] Review key source files in VECTRA-PLAYER:
  - [ ] `src/bot/action_interface/interface.py`
  - [ ] `src/bot/action_interface/state/tracker.py`
  - [ ] `src/bot/action_interface/factory.py`
- [ ] Create L4-vectra-codebase directory if not exists
- [ ] Write docs in priority order
- [ ] Run RAG ingestion after docs complete
- [ ] Validate with test queries

---

## Related Work (After Documentation)

### VECTRA-PLAYER Integration Tasks
1. Wire HumanActionInterceptor into main_window.py button handlers
2. Add optional action_interface parameter to BotController
3. Implement PuppeteerExecutor for v2.0 live trading

### GitHub Issues to Create
- [ ] BotController integration with BotActionInterface
- [ ] UI recording wiring for human gameplay capture
- [ ] PuppeteerExecutor implementation (v2.0)

---

*Created by rugs-expert agent analysis, 2025-12-25*
