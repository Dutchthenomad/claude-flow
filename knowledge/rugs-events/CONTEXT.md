# Rugs-Events Knowledge Base - Agent Context

## Purpose

This folder contains comprehensive documentation for the **Rugs.fun WebSocket protocol** and **browser connection methods**. It serves as the knowledge base for the `rugs-expert` agent.

## Contents

| File | Description | Last Updated |
|------|-------------|--------------|
| `EVENTS_INDEX.md` | Complete catalog of all Socket.IO events | 2025-12-14 |
| `BROWSER_CONNECTION_PROTOCOL.md` | CDP connection guide for authenticated event capture | 2025-12-15 |
| `QUICK_REFERENCE.md` | Fast lookup for common patterns and commands | 2025-12-15 |
| `CONNECTION_DIAGRAM.md` | Visual diagrams of connection architecture | 2025-12-15 |
| `CONTEXT.md` | This file - folder overview | 2025-12-15 |

## Integration Points

### RAG Pipeline
- Indexed by `rag-pipeline/ingestion/ingest.py`
- Searchable via `rag-pipeline/retrieval/retrieve.py`
- Used by `rugs-expert` agent for protocol questions

### REPLAYER Project
- **Location**: `/home/nomad/Desktop/REPLAYER/`
- **Implements**: CDP WebSocket interception (Phase 11)
- **Key Files**:
  - `src/sources/cdp_websocket_interceptor.py` - Event capture
  - `src/sources/socketio_parser.py` - Frame parsing
  - `browser_automation/cdp_browser_manager.py` - CDP connection

### Raw Event Captures
- **Location**: `/home/nomad/rugs_recordings/raw_captures/`
- **Format**: JSONL files with timestamped raw Socket.IO frames
- **Tool**: `src/debug/raw_capture_recorder.py` (REPLAYER)
- **Analysis**: `scripts/analyze_raw_capture.py`

### RAG Event Catalog
- **Location**: `/home/nomad/rugs_recordings/rag_events/`
- **Format**: JSONL files with parsed events
- **Ingestion**: Automatic via `src/services/rag_ingester.py`
- **Purpose**: Catalog novel events for future documentation

## Key Concepts

### Two Connection Methods

1. **Direct WebSocket** (Public Events Only)
   - Connect to `wss://api.rugs.fun/socket.io/`
   - Receives broadcast events: `gameStateUpdate`, `standard/newTrade`, etc.
   - **Limitation**: Auth-required events (`playerUpdate`, `usernameStatus`) not sent

2. **CDP WebSocket Interception** (ALL Events)
   - Connect to Chrome browser via CDP (port 9222)
   - Intercept authenticated WebSocket frames
   - Receives ALL events (public + auth-required)
   - **Requirement**: Browser with Phantom wallet connected

### Event Categories

| Category | Auth Required | Examples |
|----------|---------------|----------|
| **Broadcast** | No | `gameStateUpdate`, `standard/newTrade`, `newChatMessage` |
| **Auth-Required** | Yes | `usernameStatus`, `playerUpdate`, trade responses |
| **Protocol** | No | `connect`, `disconnect`, ping/pong |

### Player Identity

The documented setup uses player **"Dutch"**:
- **Player ID**: `did:privy:cmaibr7rt0094jp0mc2mbpfu4`
- **Username**: `Dutch`
- **Wallet**: Phantom (Solana)
- **Profile**: `/home/nomad/.gamebot/chrome_profiles/rugs_bot`

## Usage Examples

### Query the Knowledge Base

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m retrieval.retrieve "How do I connect to rugs.fun with CDP?"
```

### Common Queries

1. **"What events require authentication?"**
   - Returns: `usernameStatus`, `playerUpdate`, trade responses
   - Reference: `EVENTS_INDEX.md` → Auth-Required Events section

2. **"How do I start Chrome with CDP?"**
   - Returns: Command-line flags, profile setup
   - Reference: `BROWSER_CONNECTION_PROTOCOL.md` → Starting Chrome section

3. **"What's in a gameStateUpdate event?"**
   - Returns: 36+ root fields, nested leaderboard/history objects
   - Reference: `EVENTS_INDEX.md` → gameStateUpdate section

4. **"How do I parse Socket.IO frames?"**
   - Returns: Engine.IO protocol, message type prefixes
   - Reference: `BROWSER_CONNECTION_PROTOCOL.md` → Event Interception Flow

## For Future Agents

### When Adding New Events

1. **Document in EVENTS_INDEX.md**:
   - Add to appropriate category (Broadcast vs Auth-Required)
   - Include data structure example
   - Document all fields with types/descriptions
   - Note frequency and authentication requirements

2. **Update Event Summary Table**:
   - Add row to summary table at top of EVENTS_INDEX.md
   - Include category, frequency, auth requirement

3. **Test Detection**:
   - Add detection pattern to "Event Detection Patterns" section
   - Include code example

4. **Re-run Ingestion**:
   ```bash
   cd /home/nomad/Desktop/claude-flow/rag-pipeline
   source .venv/bin/activate
   python -m ingestion.ingest --force-reindex
   ```

5. **Verify Retrieval**:
   ```bash
   python -m retrieval.retrieve "new event name" --top_k=3
   ```

### When Updating Connection Protocol

1. **Update BROWSER_CONNECTION_PROTOCOL.md**:
   - Modify relevant section (Connection Parameters, Troubleshooting, etc.)
   - Include version/date in change
   - Add to "Related Documentation" if new external resources

2. **Test Connection**:
   - Verify instructions work on clean profile
   - Test CDP connection with `curl` commands
   - Validate event capture receives expected frames

3. **Update Implementation References**:
   - Add file paths to "Implementation References" section
   - Include line counts (use `wc -l`)
   - Link to relevant test files

4. **Re-run Ingestion** (see above)

### Adding New Documentation Files

When creating new `.md` files in this folder:

1. **Update CONTEXT.md**:
   - Add row to "Contents" table
   - Include last-updated date
   - Brief description (1-2 sentences)

2. **Add Metadata** to new file:
   ```markdown
   # Title
   > Brief description
   > Last updated: YYYY-MM-DD
   ```

3. **Link from Existing Docs**:
   - Add cross-references in EVENTS_INDEX.md or BROWSER_CONNECTION_PROTOCOL.md
   - Include in "Related Documentation" sections

4. **Run Ingestion** (see above)

## Development Status

- [x] Initial structure (rugs-events folder)
- [x] EVENTS_INDEX.md (complete event catalog)
- [x] BROWSER_CONNECTION_PROTOCOL.md (CDP connection guide)
- [x] CONTEXT.md (this file)
- [ ] RAG ingestion tested
- [ ] rugs-expert agent verified
- [ ] Production ready

## Data Sources

| Source | Location | Purpose |
|--------|----------|---------|
| Raw Captures | `/home/nomad/rugs_recordings/raw_captures/` | Protocol debugging |
| RAG Catalog | `/home/nomad/rugs_recordings/rag_events/` | Novel event detection |
| REPLAYER Docs | `/home/nomad/Desktop/REPLAYER/docs/` | Implementation specs |
| Game Recordings | `/home/nomad/rugs_recordings/*.jsonl` | Historical game data (929 games) |

## Quality Standards

When documenting events or protocols:

1. **Completeness**: Document ALL fields, not just important ones
2. **Examples**: Include real data examples (sanitize sensitive info)
3. **Types**: Specify data types (string, number, boolean, object, array)
4. **Frequency**: Note how often events occur (~4/sec, sporadic, once)
5. **Auth**: Clearly mark auth-required vs public events
6. **Source**: Reference capture files or analysis scripts
7. **Date**: Include last-updated date in frontmatter

## Testing the Knowledge Base

After adding/updating documentation:

```bash
# 1. Re-index knowledge base
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m ingestion.ingest --force-reindex

# 2. Test retrieval
python -m retrieval.retrieve "your test query" --top_k=5

# 3. Verify rugs-expert agent can access
# (Ask rugs-expert a question that requires the new documentation)
```

## Related Projects

| Project | Location | Relationship |
|---------|----------|--------------|
| **REPLAYER** | `/home/nomad/Desktop/REPLAYER/` | Implements CDP interception |
| **rugs-rl-bot** | `/home/nomad/Desktop/rugs-rl-bot/` | Uses events for RL training |
| **CV-BOILER-PLATE-FORK** | `/home/nomad/Desktop/CV-BOILER-PLATE-FORK/` | Provides persistent profile manager |
| **claude-flow** | `/home/nomad/Desktop/claude-flow/` | RAG pipeline + rugs-expert agent |

---

*This knowledge base is the authoritative source for rugs.fun protocol documentation.*
