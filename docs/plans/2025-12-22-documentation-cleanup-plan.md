# Documentation Cleanup Plan

**Created:** December 22, 2025
**Status:** Planning
**Priority:** CRITICAL

---

## Executive Summary

This plan addresses 8 conflicts identified during documentation review. The goal is to:
1. Clarify separation between claude-flow (ChromaDB) and rugs-rl-bot (DuckDB)
2. Fix scope creep in rugs-expert agent
3. Generate missing knowledge base files
4. Establish token efficiency as default workflow
5. Remove outdated code from agent definitions

---

## Priority Matrix

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| P0 | Fix scope creep in rugs-expert | High | Low |
| P0 | Clarify RAG ownership in docs | High | Medium |
| P1 | Generate knowledge base files | High | Medium |
| P1 | Token efficiency as default | Medium | Low |
| P2 | Remove outdated CDP code | Medium | Low |
| P2 | Consolidate CDP docs | Low | Low |
| P3 | Remove LanceDB refs | None | None (already clean) |

---

## Task Details

### P0-1: Fix Scope Creep in rugs-expert (CONFLICT 5)

**Current Problem:**
- Agent description claims "LIVE ACCESS to authenticated WebSocket feed via CDP"
- Contains raw Python CDP interception script (lines 149-180)
- Implies real-time interception capability

**Correct Role:**
- Protocol knowledge expert
- Answers questions from indexed documentation
- Uses ChromaDB semantic search
- References canonical spec (WEBSOCKET_EVENTS_SPEC.md)

**Changes Required:**
```yaml
# agents/rugs-expert.md
Old description: "...Has LIVE ACCESS to authenticated WebSocket feed via CDP browser interception."
New description: "...Provides authoritative answers about WebSocket events, game mechanics, and protocol documentation."

Remove sections:
- "Direct CDP Access (Primary Method)" (lines 134-180)
- Live WebSocket Interception Script
- Anything implying real-time data capture capability
```

**Files:** `agents/rugs-expert.md`

---

### P0-2: Clarify RAG Pipeline Ownership (CONFLICT 4)

**Current Problem:**
- CROSS_REPO_COORDINATION.md shows DuckDB in diagram (correct - shows rugs-rl-bot)
- Line 206 has `duckdb` command for validation (confusing - implies claude-flow uses it)
- No explicit statement that DuckDB is NOT part of claude-flow

**Resolution:**

1. **Add explicit clarification to CROSS_REPO_COORDINATION.md:**
```markdown
## Database Ownership

| Repository | Vector DB | Analytical DB | Purpose |
|------------|-----------|---------------|---------|
| claude-flow | ChromaDB | None | Semantic search over docs |
| rugs-rl-bot | None | DuckDB | Feature engineering queries |
| VECTRA-PLAYER | None | None | Writes Parquet only |

**NOTE:** claude-flow does NOT use DuckDB. The validation command below
is run from rugs-rl-bot context for cross-repo verification only.
```

2. **Update validation section (line 206):**
```markdown
# Compare with actual capture (run from rugs-rl-bot, NOT claude-flow)
# This is a cross-repo validation step
cd /home/nomad/Desktop/rugs-rl-bot
duckdb -c "SELECT DISTINCT json_keys(raw_json) FROM '~/rugs_data/**/*.parquet' WHERE event_name = 'playerUpdate'"
```

**Files:** `docs/CROSS_REPO_COORDINATION.md`

---

### P1-1: Generate Knowledge Base Files (CONFLICT 3)

**Current Problem:**
- `knowledge/rugs-events/generated/` directory exists
- Files referenced by rugs-expert don't exist:
  - `events.jsonl` (missing)
  - `phase_matrix.json` (missing)
  - `field_index.json` (missing)

**Resolution:**
Run the ingestion pipeline to generate these files.

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m ingestion.ingest

# Verify generated files
ls -la ../knowledge/rugs-events/generated/
```

**Files:** `knowledge/rugs-events/generated/*`

---

### P1-2: Token Efficiency as Default (NEW)

**Current Problem:**
- Efficiency mode exists in WORKFLOW_QUICKREF.md (v1.1.0)
- It's opt-in ("User can activate efficiency mode by saying...")
- Default is verbose/high-token mode

**Resolution:**
Flip the default: efficiency mode is standard, verbose mode requires explicit request.

**Changes to WORKFLOW_QUICKREF.md:**

```markdown
## Token Efficiency (Default Mode)

**Claude-flow uses token-efficient workflow by default.**

### Default Behavior
- TodoWrite: Only for 3+ step tasks or user request
- File Reads: Batch related files in parallel
- Test Runs: Once per logical unit (end of task)
- Context: Trust recent reads (< 5 messages)
- Explanations: Concise summaries

### Verbose Mode (On Request)
User can request full verbosity:
- "Use verbose mode"
- "Full workflow please"
- "Be thorough"
- "I need detailed explanations"

Verbose mode enables:
- TodoWrite for every task
- Per-edit test runs
- Full explanations
- Re-read files before each edit
```

**Files:** `docs/WORKFLOW_QUICKREF.md`

---

### P2-1: Remove Outdated CDP Code (CONFLICT 1)

**Current Problem:**
- rugs-expert.md contains Python CDP interception script
- Uses hardcoded path to CV-BOILER-PLATE-FORK venv
- Bypasses the established ingestion pipeline
- Doesn't follow CANONICAL promotion laws

**Resolution:**
Remove the entire "Direct CDP Access (Primary Method)" section (lines 134-180).
Keep only the reference to `RUGS_BROWSER_CONNECTION.md` for connection protocol.

**Files:** `agents/rugs-expert.md`

---

### P2-2: Consolidate CDP Docs (CONFLICT 2)

**Current Problem:**
- CDP connection documented in two places:
  - `knowledge/rugs-events/RUGS_BROWSER_CONNECTION.md`
  - `agents/rugs-expert.md` (duplicated content)

**Resolution:**
- Keep `RUGS_BROWSER_CONNECTION.md` as single source
- In rugs-expert.md, add only a reference:

```markdown
## Browser Connection Protocol
**See:** `knowledge/rugs-events/RUGS_BROWSER_CONNECTION.md`
```

**Files:**
- `agents/rugs-expert.md` (reduce)
- `knowledge/rugs-events/RUGS_BROWSER_CONNECTION.md` (keep as-is)

---

### P3: Remove LanceDB References (SKIPPED)

**Status:** Already clean. No LanceDB references found in codebase.

---

## Implementation Order

```
Phase 1: Critical Fixes (Same Session)
├── P0-1: Fix scope creep in rugs-expert
├── P0-2: Clarify RAG ownership
└── P2-1: Remove outdated CDP code (part of P0-1)

Phase 2: Knowledge Generation
└── P1-1: Generate knowledge base files (requires pipeline run)

Phase 3: Methodology Update
└── P1-2: Token efficiency as default

Phase 4: Final Cleanup
└── P2-2: Consolidate CDP docs
```

---

## Verification Checklist

After all changes:
- [ ] `grep -r "DuckDB\|duckdb" .` shows only clarified references
- [ ] `grep -r "LanceDB\|lancedb" .` returns nothing
- [ ] `grep -r "LIVE ACCESS" agents/` returns nothing
- [ ] `ls knowledge/rugs-events/generated/` shows all 3 files
- [ ] rugs-expert.md has no Python code blocks
- [ ] WORKFLOW_QUICKREF.md defaults to efficiency mode

---

## Rollback Plan

If issues arise:
```bash
git checkout -- agents/rugs-expert.md
git checkout -- docs/CROSS_REPO_COORDINATION.md
git checkout -- docs/WORKFLOW_QUICKREF.md
```

---

*Plan created: December 22, 2025*
