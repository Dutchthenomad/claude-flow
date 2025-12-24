---
layer: 2
domain: protocol/websocket
priority: P0
bot_relevant: true
validation_tier: canonical
source_file: "RAG SUPERPACK/CORE ARCHITECTURE/WEBSOCKET_EVENTS_SPEC.md"
cross_refs:
  - L2-protocol/events-index.md
  - L2-protocol/field-dictionary.md
  - L2-protocol/browser-connection.md
last_validated: 2025-12-24
---

# WebSocket Events Specification
**rugs.fun Socket.IO Protocol** | **Version**: 1.2 | **Date**: December 14, 2025

---

## Overview

This document provides a formal specification of all WebSocket events broadcast by the rugs.fun backend via Socket.IO. It serves as empirical reference data for building the verification layer and expanding our data capture.

### Connection Details
- **Server URL**: `https://backend.rugs.fun?frontend-version=1.0`
- **Protocol**: Socket.IO (WebSocket with polling fallback)
- **Broadcast Rate**: ~4 messages/second (~250ms intervals)

### Message Prefix Convention
| Prefix | Meaning |
|--------|---------|
| `42` | Standard broadcast event |
| `43XXXX` | Response to request with ID `XXXX` |

### Authentication Requirements

**IMPORTANT**: Some events require wallet authentication:

| Event | Auth Required | When Sent |
|-------|---------------|-----------|
| `gameStateUpdate` | No | Every tick (~4/sec) |
| `usernameStatus` | **YES** | Once on connection (if logged in) |
| `playerUpdate` | **YES** | After **server-side** trades only |
| `playerLeaderboardPosition` | **YES** | Once on connection (if logged in) |

**Key Insight**: If the user is not logged in with their Phantom wallet, `usernameStatus`, `playerUpdate`, and `playerLeaderboardPosition` will NOT be sent.

---

## Event Taxonomy

### 1. `gameStateUpdate` (Primary Tick Event)

**Frequency**: ~4x/second (~250ms intervals)
**Purpose**: Complete game state broadcast to all connected clients
**Auth Required**: NO - Broadcast to all connections

```json
42["gameStateUpdate", {
  "gameId": "20251210-80d2ade6a0db4338",
  "gameVersion": "v3",
  "active": true,
  "rugged": true,
  "price": 0.01978688651688796,
  "tickCount": 17,
  "cooldownTimer": 0,
  "cooldownPaused": false,
  "pauseMessage": "",
  "allowPreRoundBuys": false,
  "averageMultiplier": 6.286986541653673,
  "connectedPlayers": 190,
  "count2x": 46,
  "count10x": 8,
  "count50x": 3,
  "count100x": 1,
  "highestToday": 1026.429049568061,
  "highestTodayTimestamp": 1765260384895,
  "leaderboard": [...],
  "partialPrices": {...},
  "gameHistory": [...],
  "provablyFair": {...},
  "rugRoyale": {...},
  "availableShitcoins": [...]
}]
```

#### Root Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `gameId` | string | `"20251210-80d2ade6a0db4338"` | Unique game identifier |
| `gameVersion` | string | `"v3"` | Game version |
| `active` | bool | `true` | Game in progress |
| `rugged` | bool | `true` | Game has rugged |
| `price` | float | `0.01978688651688796` | Current multiplier |
| `tickCount` | int | `17` | Current tick number |
| `cooldownTimer` | int | `0` | Countdown to next game (0 = game active) |
| `cooldownPaused` | bool | `false` | Countdown paused |
| `pauseMessage` | string | `""` | Pause reason |
| `allowPreRoundBuys` | bool | `false` | Pre-round buying enabled |

#### Statistics Fields

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `averageMultiplier` | float | `6.287` | Session average rug point |
| `count2x` | int | `46` | Games reaching 2x |
| `count10x` | int | `8` | Games reaching 10x |
| `count50x` | int | `3` | Games reaching 50x |
| `count100x` | int | `1` | Games reaching 100x |
| `connectedPlayers` | int | `190` | Current player count |
| `highestToday` | float | `1026.43` | Daily high multiplier |
| `highestTodayTimestamp` | int | `1765260384895` | Timestamp of daily high |

#### Leaderboard (`leaderboard[]`)

Each entry represents a player with active position or recent activity:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique player ID (`did:privy:*`) |
| `username` | string | Display name (null if not set) |
| `level` | int | Player level |
| `pnl` | float | **SERVER-SIDE PnL** (SOL) |
| `regularPnl` | float | PnL from regular trades |
| `sidebetPnl` | float | PnL from sidebets |
| `shortPnl` | float | PnL from shorts |
| `pnlPercent` | float | PnL as percentage |
| `hasActiveTrades` | bool | Has open position |
| `positionQty` | float | Position size (units) |
| `avgCost` | float | Average entry price |
| `totalInvested` | float | Total SOL invested |
| `sidebetActive` | bool/null | Has active sidebet |
| `sideBet` | object/null | Sidebet details |
| `shortPosition` | object/null | Short position details |
| `position` | int | Leaderboard rank |

**Use Case**: PnL verification, position sync, multi-player activity tracking.

---

### 2. `usernameStatus` (Identity Event)

**Frequency**: Once on connection (requires wallet auth)
**Purpose**: Player identity confirmation
**Auth Required**: YES - Must be logged in with Phantom wallet

```json
42["usernameStatus",
  {"__trace": true, "traceparent": "00-92cc45541ea050caeb7518ce83e610ec-5d4369ed14c75a17-01"},
  {"id": "did:privy:cmaibr7rt0094jp0mc2mbpfu4", "hasUsername": true, "username": "Dutch"}
]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"did:privy:cmaibr7rt0094jp0mc2mbpfu4"` | Unique player ID (Privy DID) |
| `username` | string | `"Dutch"` | Display name |
| `hasUsername` | bool | `true` | Whether username is set |

**Use Case**:
- Identify "our" player in leaderboard array
- Filter `playerUpdate` events for our player
- **Validate connection is authenticated**

---

### 3. `playerUpdate` (Personal State Sync)

**Frequency**: After each of our trades
**Purpose**: Sync local state with server truth

```json
{
  "cash": 3.967072345,
  "cumulativePnL": 0.264879755,
  "positionQty": 0.2222919,
  "avgCost": 1.259605046,
  "totalInvested": 0.251352892
}
```

| Field | Type | Description |
|-------|------|-------------|
| `cash` | float | **TRUE wallet balance** |
| `cumulativePnL` | float | Total PnL this game |
| `positionQty` | float | Current position size |
| `avgCost` | float | Average entry price |
| `totalInvested` | float | Total invested this game |

**Use Case**:
- **Critical for verification layer**
- Compare local `balance` calculation vs server `cash`
- Compare local position vs server `positionQty`
- Detect calculation drift

---

### 4. `gameStatePlayerUpdate` (Rugpool & Player Trades)

**Frequency**: ~4x/second (same as `gameStateUpdate`)
**Purpose**: Broadcast containing rugpool lottery state and player trades
**Auth Required**: YES - Only sent to authenticated clients
**Traffic Share**: **46.7%** of all WebSocket traffic!

Contains rugpool lottery state including:
- `rugpoolAmount` - Total SOL in lottery pool
- `totalEntries` - Total lottery entries across all players
- `playerEntries` - Top 10 players by entries
- `lastDrawing` - Previous drawing results

---

### 5. Trade Events

#### `buyOrder` / `sellOrder` (Trade Requests)

**Protocol**: Request/response pattern

```
42425["buyOrder", {"amount": 0.001}]
42426["sellOrder", {"percentage": 100}]
```

#### Response
```
43425[{"success": true, "executedPrice": 1.234, "timestamp": 1765069123456}]
```

---

## Integration Priority

### Priority 1: Verification Layer (Immediate)

| Data Point | Source | Local Equivalent |
|------------|--------|------------------|
| `playerUpdate.cash` | Server | `GameState.balance` |
| `playerUpdate.positionQty` | Server | `Position.amount` |
| `playerUpdate.avgCost` | Server | `Position.entry_price` |
| `leaderboard[me].pnl` | Server | Calculated PnL |

### Priority 2: Latency Tracking (High)

| Data Point | Source | Use |
|------------|--------|-----|
| `sidebet.timestamp` | Server | Request-to-confirm latency |
| `buyOrder.timestamp` | Server | Trade execution latency |

**Implementation**: `latency = local_receipt_time - server_timestamp`

---

## Verification History

| Date | Events Verified | Notes |
|------|-----------------|-------|
| Dec 6, 2025 | `gameStateUpdate` | Initial discovery, 200 samples |
| Dec 9, 2025 | `usernameStatus`, `playerLeaderboardPosition` | Auth requirements confirmed |
| Dec 14, 2025 | 16 new events via CDP capture | CDP WebSocket interception |

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
