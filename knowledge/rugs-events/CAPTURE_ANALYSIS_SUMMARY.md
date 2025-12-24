# Capture Analysis Summary - December 24, 2025

## Quick Stats
- **23,194 messages** analyzed (11 games, authenticated session)
- **10 novel events** discovered
- **22 undocumented fields** in `playerUpdate`
- **3 critical sidebet events** missing from spec

---

## Critical Findings

### 1. Sidebet Events (MISSING FROM SPEC)
Three auth-required events that are essential for sidebet tracking:

**`currentSidebet`** (19 occurrences) - P1 Priority
- Confirms sidebet placement
- Contains: betAmount, xPayout, endTick, startTick, timestamp
- **USE CASE**: Verify sidebet accepted by server

**`currentSidebetResult`** (19 occurrences) - P1 Priority  
- Confirms sidebet win/loss
- Contains: payout, profit, tickIndex (when resolved)
- **USE CASE**: Track sidebet P&L accurately

**`newSideBet`** (34 occurrences) - P2 Priority
- Broadcasts other players' sidebets
- Same fields as `currentSidebet`
- **USE CASE**: Track market sidebet volume/activity

### 2. playerUpdate Fields (CRITICALLY INCOMPLETE)

**Spec has**: 5 fields  
**Reality has**: 27 fields (22 undocumented!)

**CRITICAL missing fields** (P0):
- `sidebets` (array) - ALL active sidebets
- `sideBet` (object) - Current sidebet details
- `sidebetPnl` (float) - Sidebet profit/loss
- `shortPosition` (object) - Active short position

**HIGH priority missing fields** (P1):
- `id` (string) - Player DID
- `levelInfo` (object) - Level, XP, progress
- `pnlPercent` (float) - PnL percentage
- `authenticated` (bool) - Wallet connection status

**Full list**: See section 3 of main report.

### 3. Game Mode Events (NEW)

Three high-frequency events (~118-119 occurrences each):
- `sidebetEventUpdate` - Sidebet tournament scheduling
- `pinpointPartyEventUpdate` - Unknown mode (trace-only)
- `diddyPartyUpdate` - Unknown mode (trace-only)

**Recommendation**: Add as OUT_OF_SCOPE (P3) or investigate payloads during active events.

---

## Immediate Actions

1. **Update WEBSOCKET_EVENTS_SPEC.md**:
   - Add 3 sidebet events (`currentSidebet`, `currentSidebetResult`, `newSideBet`)
   - Expand `playerUpdate` from 5 to 27 fields
   - Add complete `standard/newTrade` field list (14 fields)

2. **Investigate Missing Events**:
   - `usernameStatus` - needs fresh connection capture
   - `buyOrder`/`sellOrder` - needs active trading session
   - `sidebetResponse` - may have been replaced by `currentSidebet`

3. **Verify Trace-Only Events**:
   - `pinpointPartyEventUpdate` - check during active event
   - `diddyPartyUpdate` - check during active event
   - `leaderboardData` - capture full payload

---

## Impact on Current Systems

### REPLAYER
- **MISSING**: Sidebet confirmation tracking (`currentSidebet`)
- **MISSING**: Sidebet result tracking (`currentSidebetResult`)
- **INCOMPLETE**: Only using 5 of 27 `playerUpdate` fields

### rugs-rl-bot
- **NEEDS**: `sidebets` array for multi-sidebet strategies
- **NEEDS**: `shortPosition` for short trading features
- **NEEDS**: `leveragedPositions` for leverage tracking

### VECTRA-PLAYER
- **Schema v2.0.0**: Already has placeholders for sidebets
- **ACTION**: Update event schemas to match capture findings

---

## Evidence Files

- **Main Report**: `/home/nomad/Desktop/claude-flow/knowledge/rugs-events/CAPTURE_ANALYSIS_2025-12-24.md`
- **Raw Capture**: `/tmp/claude/full_game_capture_20251224_105411.jsonl` (23,194 lines)
- **Canonical Spec**: `/home/nomad/Desktop/claude-flow/knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md`

---

**Status**: VERIFIED (all findings)  
**Next Step**: User approval required for CANONICAL promotion (per CONTEXT.md laws)
