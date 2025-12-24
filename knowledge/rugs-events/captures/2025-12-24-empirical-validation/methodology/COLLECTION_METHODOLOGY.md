---
title: Empirical Validation Data Collection Methodology
date: 2025-12-24
collector: Claude Code (assisted by human operator "Dutch")
validation_tier: verified
---

# Empirical Validation Data Collection Methodology

## 1. Purpose

To empirically validate the BotActionInterface design by:
1. Capturing real WebSocket traffic from rugs.fun
2. Mapping which events confirm which player actions (BUY/SELL/SIDEBET)
3. Identifying novel events/fields not in the canonical spec
4. Measuring latency distributions for action confirmations

---

## 2. Collection Setup

### Environment

| Parameter | Value |
|-----------|-------|
| Date | December 24, 2025 |
| Time | 10:54 - 11:24 UTC |
| Duration | ~30 minutes |
| Platform | Ubuntu Linux |
| Chrome Version | Latest stable |
| CDP Port | 9222 |

### Chrome Profile

| Parameter | Value |
|-----------|-------|
| Profile Path | `/home/nomad/.gamebot/chrome_profiles/rugs_bot` |
| Wallet | Phantom (pre-authenticated) |
| Username | Dutch |
| Player ID | `did:privy:cmaibr7rt0094jp0mc2mbpfu4` |
| Level | 7 |

### Capture Method

**Chrome DevTools Protocol (CDP) WebSocket Interception**

```bash
# Launch Chrome with remote debugging
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/nomad/.gamebot/chrome_profiles/rugs_bot \
  --no-first-run \
  "https://rugs.fun"
```

**Capture Script**: `/tmp/claude/full_game_capture.py`
- Connects to CDP via `ws://localhost:9222`
- Enables `Network.enable` for WebSocket frame interception
- Captures both `Network.webSocketFrameReceived` (RX) and `Network.webSocketFrameSent` (TX)
- Parses Socket.IO protocol (`42[...]` frames)
- Writes JSONL format with timestamps

---

## 3. Test Protocol

### Intended Button Sequence

The human operator executed multiple trading sequences across 11 games:

**Per-Game Sequence (intended):**
1. TAP - Expand sidebet UI
2. SIDEBET - Place sidebet during presale
3. BUY - Enter position during presale
4. SELL 100% - Close position
5. X2 - Double bet amount
6. BUY - Re-enter at higher price
7. 1/2 - Halve bet amount
8. SIDEBET - Place mid-game sidebet
9. BUY - DCA into position
10. SELL 100% - Exit before rug
11. Wait for rug event

### Actual Execution

Due to game timing and UI responsiveness, the operator:
- Executed trades across 11 complete games
- Placed 19 sidebets (various bet amounts: 0.001-0.004 SOL)
- Executed multiple BUY/SELL cycles
- Observed multiple rug events
- Captured both presale and active phase trading

---

## 4. Data Captured

### Raw Capture File

| Attribute | Value |
|-----------|-------|
| Filename | `full_game_capture_20251224_105411.jsonl` |
| Size | 108 MB |
| Events | 23,194 lines |
| Format | JSON Lines (JSONL) |

### Record Schema

```json
{
  "ts": 1766591653.491963,
  "iso": "2025-12-24T10:54:13.491963",
  "dir": "RX",
  "event": "gameStateUpdate",
  "data": { ... },
  "raw": "42[\"gameStateUpdate\", {...}]"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `ts` | float | Unix timestamp (seconds) |
| `iso` | string | ISO 8601 timestamp |
| `dir` | string | "RX" (received) or "TX" (sent) |
| `event` | string | Socket.IO event name |
| `data` | object | Parsed event payload |
| `raw` | string | Raw Socket.IO frame (truncated to 1000 chars) |

---

## 5. Event Inventory

### Events Captured

| Event | Count | Priority | Auth Required |
|-------|-------|----------|---------------|
| `gameStateUpdate` | 9,523 | P0 | No |
| `gameStatePlayerUpdate` | 9,397 | P1 | Yes |
| `standard/newTrade` | 815 | P1 | No |
| `newChatMessage` | 332 | P3 | No |
| `playerUpdate` | 155 | P0 | Yes |
| `sidebetEventUpdate` | 120 | P2 | No |
| `pinpointPartyEventUpdate` | 120 | P2 | No |
| `diddyPartyUpdate` | 120 | P2 | No |
| `goldenHourUpdate` | 118 | P2 | No |
| `rugRoyaleUpdate` | 117 | P2 | No |
| `battleEventUpdate` | 27 | P2 | No |
| `currentSidebet` | 19 | P1 | Yes |
| `currentSidebetResult` | 19 | P1 | Yes |
| `newSideBet` | 14 | P2 | No |
| `getLeaderboard` (TX) | 2 | P3 | No |
| `getPlayerLeaderboardPosition` (TX) | 2 | P3 | No |
| `leaderboardData` | 2 | P3 | No |
| `playerLeaderboardPosition` | 2 | P3 | No |
| `rugpassQuestCompleted` | 1 | P3 | Yes |

### Direction Distribution

| Direction | Count | Description |
|-----------|-------|-------------|
| RX | 23,190 | Server → Client |
| TX | 4 | Client → Server (only leaderboard queries) |

---

## 6. Key Findings

### Critical Discovery #1: HTTP vs WebSocket

**Button clicks do NOT send WebSocket messages.**

- All BUY/SELL/SIDEBET actions use HTTP POST to REST API
- Confirmations arrive via WebSocket RX push events
- Only leaderboard queries use WebSocket TX

### Critical Discovery #2: Confirmation Events

| Action | Confirmation Event | Key Fields |
|--------|-------------------|------------|
| BUY | `playerUpdate` | `positionQty ↑`, `cash ↓` |
| SELL | `playerUpdate` | `positionQty ↓`, `cash ↑` |
| SIDEBET | `currentSidebet` | `type: "placed"` |
| SIDEBET_WIN | `currentSidebetResult` | `won: true`, `payout > 0` |

### Critical Discovery #3: Novel Events

10 events found NOT in canonical spec:
- `currentSidebet` - Sidebet placement confirmation
- `currentSidebetResult` - Sidebet resolution
- `newSideBet` - Other players' sidebets
- `sidebetEventUpdate` - Sidebet tournament data
- `pinpointPartyEventUpdate` - Unknown game mode
- `diddyPartyUpdate` - Unknown game mode
- `goldenHourUpdate` - Unknown bonus event
- `rugRoyaleUpdate` - Unknown game mode
- `battleEventUpdate` - Unknown game mode
- `rugpassQuestCompleted` - Quest system

### Critical Discovery #4: Undocumented Fields

`playerUpdate` has 22 fields not in spec:
- `sidebets` (array) - Active sidebets
- `sideBet` (object) - Current sidebet
- `sidebetPnl` (float) - Sidebet P&L
- `shortPosition` (object) - Short position data
- `levelInfo` (object) - Player progression
- `bonusBalance` (float) - Bonus funds
- `hasInteracted` (boolean) - Engagement flag
- And 15 more...

---

## 7. Latency Measurements

| Action | Confirmation Event | Latency |
|--------|-------------------|---------|
| BUY | `playerUpdate` | ~1-2 seconds |
| SELL | `playerUpdate` | ~1-2 seconds |
| SIDEBET | `currentSidebet` | ~1 second |
| SIDEBET_RESULT | `currentSidebetResult` | ~13-14 seconds |

Sidebet result latency = 40 ticks × ~250ms + server processing

---

## 8. Files in This Package

```
staging/2025-12-24-empirical-validation/
├── methodology/
│   └── COLLECTION_METHODOLOGY.md    (this file)
├── raw_captures/
│   └── full_game_capture_20251224_105411.jsonl  (108MB, 23K events)
└── analysis/
    ├── CAPTURE_ANALYSIS_2025-12-24.md      (detailed analysis)
    ├── CAPTURE_ANALYSIS_SUMMARY.md         (executive summary)
    └── confirmation-mapping.md              (action→event mapping)
```

---

## 9. Ingestion Instructions

### For ChromaDB RAG Pipeline

1. **Move to permanent location:**
   ```bash
   mv staging/2025-12-24-empirical-validation /path/to/knowledge/rugs-events/captures/
   ```

2. **Chunk the analysis documents:**
   ```bash
   python -m ingestion.ingest \
     --collection rugs_events \
     --source captures/2025-12-24-empirical-validation/analysis/
   ```

3. **Update canonical spec (after human review):**
   - Add novel events to `WEBSOCKET_EVENTS_SPEC.md`
   - Expand `playerUpdate` field documentation
   - Add sidebet event family

### Raw Capture Processing

The JSONL capture can be queried with DuckDB:
```sql
SELECT event, COUNT(*) as count
FROM read_json_auto('raw_captures/full_game_capture_*.jsonl')
GROUP BY event ORDER BY count DESC;
```

---

## 10. Validation Tier

All findings in this package are **VERIFIED** tier:
- Captured from live authenticated session
- Multiple games observed (n=11)
- Multiple action types executed
- Latency measurements from real data

**Promotion to CANONICAL** requires human review and approval per CANONICAL PROMOTION LAWS.

---

*Last updated: December 24, 2025*
