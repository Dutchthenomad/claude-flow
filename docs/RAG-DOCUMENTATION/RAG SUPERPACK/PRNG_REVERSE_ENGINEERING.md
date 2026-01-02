# Rugs.fun Knowledge Base

> Complete protocol documentation for the `rugs-expert` agent
> Version: 1.0.0 | Last updated: 2025-12-15

---

## What's Inside

This knowledge base contains everything you need to understand and work with the rugs.fun WebSocket protocol and browser connection methods.

### Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| **QUICK_REFERENCE.md** | Fast lookup, common patterns | Start here for quick answers |
| **BROWSER_CONNECTION_PROTOCOL.md** | Complete CDP setup guide | Setting up browser connection |
| **EVENTS_INDEX.md** | Full event catalog | Understanding event data structures |
| **CONNECTION_DIAGRAM.md** | Visual architecture diagrams | Understanding system architecture |
| **CONTEXT.md** | Knowledge base overview | Contributing to documentation |

### Total Content
- **5 documentation files**
- **1,812 lines** of comprehensive documentation
- **80KB** of curated knowledge

---

## Quick Start

### I want to...

**...connect to rugs.fun via CDP**
→ Read: `BROWSER_CONNECTION_PROTOCOL.md` → "Starting Chrome with CDP"

**...understand what events are available**
→ Read: `EVENTS_INDEX.md` → "Event Summary"

**...parse Socket.IO frames**
→ Read: `QUICK_REFERENCE.md` → "Socket.IO Frame Format"

**...see the connection architecture**
→ Read: `CONNECTION_DIAGRAM.md` → "Connection Method Comparison"

**...know which events require authentication**
→ Read: `EVENTS_INDEX.md` → "Auth-Required Events"

**...troubleshoot connection issues**
→ Read: `BROWSER_CONNECTION_PROTOCOL.md` → "Troubleshooting"

**...understand the data flow**
→ Read: `CONNECTION_DIAGRAM.md` → "Data Flow: From Browser to GameState"

---

## Key Concepts

### Two Connection Methods

1. **Direct WebSocket** - Public events only (no auth)
2. **CDP WebSocket Interception** - ALL events (authenticated via browser)

**Recommendation**: Use CDP for complete event coverage.

### Event Categories

| Category | Auth Required | Frequency | Examples |
|----------|---------------|-----------|----------|
| **Broadcast** | No | ~4/sec | gameStateUpdate |
| **Auth-Required** | Yes | Sporadic | playerUpdate, usernameStatus |
| **Protocol** | No | 25sec | PING/PONG |

### Critical Parameters

```bash
CDP Port:      9222
Profile Path:  /home/nomad/.gamebot/chrome_profiles/rugs_bot
Target URL:    https://rugs.fun
Player:        Dutch (did:privy:cmaibr7rt0094jp0mc2mbpfu4)
```

---

## Documentation Structure

```
rugs-events/
├── README.md                           ← You are here
├── QUICK_REFERENCE.md                  ← Fast lookup (286 lines)
├── BROWSER_CONNECTION_PROTOCOL.md      ← CDP guide (465 lines)
├── EVENTS_INDEX.md                     ← Event catalog (422 lines)
├── CONNECTION_DIAGRAM.md               ← Visual diagrams (406 lines)
└── CONTEXT.md                          ← Meta documentation (233 lines)
```

---

## Learning Path

### Beginner (Never used rugs.fun protocol)

1. **QUICK_REFERENCE.md**
   - Overview section
   - Connection Quick Start
   - Event Categories

2. **CONNECTION_DIAGRAM.md**
   - Connection Method Comparison
   - REPLAYER Integration Architecture

3. **BROWSER_CONNECTION_PROTOCOL.md**
   - Starting Chrome with CDP
   - Verifying CDP Connection

### Intermediate (Need to implement connection)

1. **BROWSER_CONNECTION_PROTOCOL.md**
   - Complete read (all sections)
   - Focus: Connection Architecture, CDP Configuration

2. **EVENTS_INDEX.md**
   - Event Summary table
   - gameStateUpdate (most important event)
   - Auth-Required Events section

3. **QUICK_REFERENCE.md**
   - Socket.IO Frame Format
   - CDP Python Example

### Advanced (Building production system)

1. **EVENTS_INDEX.md**
   - Complete read (all event types)
   - Event Detection Patterns
   - Usage in REPLAYER

2. **CONNECTION_DIAGRAM.md**
   - Complete Data Flow
   - Event Flow Timeline
   - Troubleshooting Decision Tree

3. **BROWSER_CONNECTION_PROTOCOL.md**
   - Security Considerations
   - Implementation References

---

## Common Queries

### "How do I start Chrome with CDP?"

**Answer**: `BROWSER_CONNECTION_PROTOCOL.md` → Starting Chrome with CDP

```bash
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/nomad/.gamebot/chrome_profiles/rugs_bot \
  --no-first-run \
  "https://rugs.fun"
```

### "What events require authentication?"

**Answer**: `EVENTS_INDEX.md` → Auth-Required Events

- `usernameStatus` - Player identity
- `playerUpdate` - Balance/position sync
- Trade responses (buy/sell/sidebet)

### "How do I parse Socket.IO frames?"

**Answer**: `QUICK_REFERENCE.md` → Socket.IO Frame Format

```python
# Strip "42" prefix, parse JSON array
json_str = payload[2:]
event_name, data = json.loads(json_str)
```

### "Why can't I receive playerUpdate events?"

**Answer**: `BROWSER_CONNECTION_PROTOCOL.md` → Why CDP?

Server only sends auth events to authenticated clients. You must use CDP to intercept the browser's authenticated WebSocket connection.

### "What's in a gameStateUpdate event?"

**Answer**: `EVENTS_INDEX.md` → gameStateUpdate section

36+ root fields including:
- `gameId`, `active`, `rugged`
- `price`, `tickCount`
- `leaderboard[]` (nested)
- `partialPrices`, `gameHistory[]`

---

## Integration with REPLAYER

This knowledge base documents the protocol implemented in the **REPLAYER** project.

**Location**: `/home/nomad/Desktop/REPLAYER/`

**Key Implementation Files**:
- `src/sources/cdp_websocket_interceptor.py` (205 lines)
- `src/sources/socketio_parser.py` (151 lines)
- `browser_automation/cdp_browser_manager.py` (270 lines)

**Test Coverage**: 796 tests passing (as of Phase 11 completion)

**Documentation Reference**: `/home/nomad/Desktop/REPLAYER/CLAUDE.md`

---

## RAG Pipeline Integration

### Indexing the Knowledge Base

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate

# Index knowledge base
python -m ingestion.ingest --force-reindex
```

### Querying the Knowledge Base

```bash
# Query for specific information
python -m retrieval.retrieve "How do I connect to rugs.fun with CDP?" --top_k=5
```

### rugs-expert Agent

The `rugs-expert` agent uses this knowledge base via the RAG pipeline to answer questions about the rugs.fun protocol.

**Agent Location**: `/home/nomad/Desktop/claude-flow/agents/rugs-expert.yaml`

---

## Contributing

When adding new documentation to this knowledge base:

1. **Update the appropriate file**:
   - New events → `EVENTS_INDEX.md`
   - Connection changes → `BROWSER_CONNECTION_PROTOCOL.md`
   - Quick tips → `QUICK_REFERENCE.md`
   - Architecture changes → `CONNECTION_DIAGRAM.md`

2. **Update CONTEXT.md**:
   - Add file to Contents table if new
   - Update last-updated dates

3. **Re-run ingestion**:
   ```bash
   cd /home/nomad/Desktop/claude-flow/rag-pipeline
   source .venv/bin/activate
   python -m ingestion.ingest --force-reindex
   ```

4. **Verify retrieval**:
   ```bash
   python -m retrieval.retrieve "your new content" --top_k=3
   ```

**See**: `CONTEXT.md` → For Future Agents section for detailed guidelines.

---

## Data Sources

| Source | Location | Description |
|--------|----------|-------------|
| **Raw Captures** | `/home/nomad/rugs_recordings/raw_captures/` | Raw WebSocket frames |
| **RAG Catalog** | `/home/nomad/rugs_recordings/rag_events/` | Parsed events (JSONL) |
| **Game Recordings** | `/home/nomad/rugs_recordings/*.jsonl` | Historical games (929 sessions) |
| **REPLAYER Docs** | `/home/nomad/Desktop/REPLAYER/docs/` | Implementation specs |

---

## Quality Standards

All documentation in this knowledge base follows these standards:

- **Completeness**: Document ALL fields, not just important ones
- **Examples**: Include real data examples (sanitized)
- **Types**: Specify data types (string, number, boolean, object, array)
- **Frequency**: Note how often events occur
- **Authentication**: Clearly mark auth vs public events
- **Source**: Reference capture files or analysis
- **Dates**: Include last-updated in frontmatter
- **Code**: Provide working code examples

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-15 | Initial knowledge base creation |
| | | - EVENTS_INDEX.md (existing, updated metadata) |
| | | - BROWSER_CONNECTION_PROTOCOL.md (new) |
| | | - QUICK_REFERENCE.md (new) |
| | | - CONNECTION_DIAGRAM.md (new) |
| | | - CONTEXT.md (new) |
| | | - README.md (new) |

---

## Related Projects

| Project | Location | Relationship |
|---------|----------|--------------|
| **REPLAYER** | `/home/nomad/Desktop/REPLAYER/` | Implements this protocol |
| **rugs-rl-bot** | `/home/nomad/Desktop/rugs-rl-bot/` | Uses events for RL training |
| **CV-BOILER-PLATE-FORK** | `/home/nomad/Desktop/CV-BOILER-PLATE-FORK/` | Provides profile manager |
| **claude-flow** | `/home/nomad/Desktop/claude-flow/` | Hosts this knowledge base |

---

## Support

For questions about the rugs.fun protocol:

1. **Search this knowledge base** using the RAG pipeline
2. **Ask the rugs-expert agent** (uses this knowledge via RAG)
3. **Reference REPLAYER implementation** for working code examples
4. **Analyze raw captures** in `/home/nomad/rugs_recordings/raw_captures/`

---

*This knowledge base is the authoritative source for rugs.fun WebSocket protocol documentation.*

**Total Documentation**: 1,812 lines | **Size**: 80KB | **Files**: 5

**Start reading**: `QUICK_REFERENCE.md`
