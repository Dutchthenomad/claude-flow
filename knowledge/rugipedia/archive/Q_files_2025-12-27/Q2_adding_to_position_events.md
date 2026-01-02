# Question 2: Adding to Position (Positive → More Positive)

**Date**: 2025-12-28
**Session**: WebSocket Documentation Enhancement
**Status**: OBSERVED (pending canonical review)

---

## Question Context

The agent identified 4 position transition cases that must be handled:

2. **Adding to position (positive → more positive)**: Keep original entry_tick

This document captures the exact WebSocket events that fire when a player adds to an existing position during active gameplay.

---

## Scenario Description

Player "N0m4D" executed the following sequence:
1. Opened presale position: 0.002 SOL
2. Game started (tick 0)
3. At approximately tick 11-16, added another 0.002 SOL to position
4. Sold a few ticks later

---

## Event Sequence Timeline

| Time | Event | Length | Description |
|------|-------|--------|-------------|
| 21:02:55.825 | `gameStatePlayerUpdate` | 2350 | Initial position state |
| 21:02:56.038 | `buyOrder` | 122 | Client → Server buy request |
| 21:02:56.081 | `standard/newTrade` | - | Another player's trade (Vmoney) |
| 21:02:56.107 | `standard/newTrade` | - | Our trade confirmation |
| 21:02:56.236 | `playerUpdate` | 902 | Balance/position sync |
| 21:02:56.251 | `gameStatePlayerUpdate` | 421 | Updated position state |
| 21:02:56.257 | `success` | 22 | Server acknowledgment |
| 21:02:58.054 | `gameStateUpdate` | 165280 | Full state with gameHistory |

**Key Observation**: Full add-to-position cycle completes in ~432ms (from buyOrder to success)

---

## Raw Event Examples

### Event 1: gameStatePlayerUpdate (BEFORE adding - 21:02:55.825)

```json
42["gameStatePlayerUpdate", {
  "gameId": "20251228-242b2d81e73e4f27",
  "leaderboardEntry": {
    "id": "did:privy:cma094vht019il80np6aidhqd",
    "username": "N0m4D",
    "level": 14,
    "pnl": 0.000745529,
    "pnlPercent": 37.27645,
    "avgCost": 1,
    "hasActiveTrades": true,
    "position": 39,
    "positionQty": 0.002,
    "regularPnl": 0.000745529,
    "selectedCoin": null,
    "shortPnl": 0,
    "shortPosition": null,
    "sideBet": null,
    "sidebetActive": null,
    "sidebetPnl": 0,
    "totalInvested": 0.002,
    "username": "N0m4D"
  }
}]
```

### Event 2: buyOrder (CLIENT → SERVER - 21:02:56.038)

**Direction**: Outgoing (client to server)

```json
4229["buyOrder", {
  "__trace": true,
  "traceparent": "00-55110064298fdee6dc04d093c003b5c9-2870159c41eb0cab-01"
}, {
  "amount": 0.002
}]
```

**Note**: Message prefix `4229` vs typical `42` - the `29` may indicate message acknowledgment ID.

### Event 3: standard/newTrade (SERVER → CLIENT - 21:02:56.107)

**Direction**: Incoming (server broadcast to all clients)

```json
42["standard/newTrade", {
  "__trace": true,
  "traceparent": "00-55110064298fdee6dc04d093c003b5c9-65b220dcba23a3a0-01"
}, {
  "id": "9111d2c8-efcc-449e-b081-0c8c59e0bc45",
  "gameId": "20251228-242b2d81e73e4f27",
  "playerId": "did:privy:cma094vht019il80np6aidhqd",
  "username": "N0m4D",
  "level": 14,
  "amount": 0.002,
  "qty": 0.001384584,
  "price": 1.4444769765026393,
  "tickIndex": 16,
  "type": "buy",
  "leverage": 1,
  "coin": "solana",
  "bonusPortion": 0,
  "realPortion": 0.002
}]
```

### Event 4: playerUpdate (21:02:56.236)

```json
42["playerUpdate", {
  "id": "did:privy:cma094vht019il80np6aidhqd",
  "role": null,
  "cash": 0.09503525,
  "bonusBalance": 0,
  "authenticated": true,
  "autobuysEnabled": false,
  "autosellPrice": null,
  "avgCost": 1.181828845,
  "bonusWagerReq": 0,
  "bonusWagered": 0,
  "crateKeys": {
    "gold": 0,
    "diamond": 0,
    "coal": 0,
    "iron": 0,
    "tier1": 0,
    "tier0": 0
  },
  "cumulativePnL": 0.000888953,
  "hasInteracted": true,
  "hitMaxWin": false,
  "levelInfo": {
    "level": 14,
    "xp": 1956,
    "xpForNextLevel": 5000,
    "totalXP": 31956
  },
  "leveragedPositions": [],
  "pnlPercent": 44.44765,
  "positionQty": 0.003384584,
  "recentCrateRewards": [],
  "role": null,
  "selectedCoin": null,
  "shitcoinBalances": {
    "0xPractice": 100
  },
  "shortPosition": null,
  "sideBet": null,
  "sidebetPnl": 0,
  "sidebets": [],
  "totalInvested": 0.004,
  "xpBoost": {
    "active": false,
    "activeUntil": 0,
    "available": 0
  }
}]
```

### Event 5: gameStatePlayerUpdate (AFTER adding - 21:02:56.251)

```json
42["gameStatePlayerUpdate", {
  "gameId": "20251228-242b2d81e73e4f27",
  "leaderboardEntry": {
    "id": "did:privy:cma094vht019il80np6aidhqd",
    "username": "N0m4D",
    "level": 14,
    "pnl": 0.000888953,
    "pnlPercent": 44.44765,
    "avgCost": 1,
    "hasActiveTrades": true,
    "position": 39,
    "positionQty": 0.002,
    "regularPnl": 0.000888953,
    "selectedCoin": null,
    "shortPnl": 0,
    "shortPosition": null,
    "sideBet": null,
    "sidebetActive": null,
    "sidebetPnl": 0,
    "totalInvested": 0.002,
    "username": "N0m4D"
  }
}]
```

### Event 6: success (21:02:56.257)

**Direction**: Server acknowledgment (ACK)

```json
4329[{
  "success": true
}]
```

**Note**: Message prefix `4329` corresponds to the `4229` from buyOrder - this is the ACK.

### Event 7: gameStateUpdate (partial - 21:02:58.054)

**Length**: 165,280 bytes (contains gameHistory)

**GodCandle Fields** (for tracking extreme price movements):
```json
{
  "godCandle2x": null,
  "godCandle2xMassiveJump": null,
  "godCandle2xPrices": [],
  "godCandle2xTimestamp": null,
  "godCandle10x": null,
  "godCandle10xMassiveJump": null,
  "godCandle10xPrices": [],
  "godCandle10xTimestamp": null,
  "godCandle50x": null,
  "godCandle50xMassiveJump": null,
  "godCandle50xPrices": [],
  "godCandle50xTimestamp": null
}
```

**Daily High Tracking**:
```json
{
  "highestToday": 1329.9752646165282,
  "highestTodayTimestamp": 1766855639499
}
```

---

## Complete Findings Summary

### NEW EVENT TYPES DISCOVERED

#### 1. buyOrder (Client → Server)

**Direction**: Outgoing
**Purpose**: Request to open/add to position
**Category**: TRADING_ACTION

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `__trace` | bool | `true` | OpenTelemetry tracing enabled |
| `traceparent` | string | `"00-55110..."` | Distributed trace ID |
| `amount` | number | `0.002` | Buy amount in SOL |

**Message Format**: `4229["buyOrder", {trace}, {amount}]`
- Prefix `42` = Socket.IO message
- Suffix `29` = ACK request ID

#### 2. standard/newTrade (Server → Client)

**Direction**: Incoming (broadcast)
**Purpose**: Trade confirmation for all players
**Category**: TRADING_EVENT

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"9111d2c8-..."` | Trade UUID |
| `gameId` | string | `"20251228-..."` | Game identifier |
| `playerId` | string | `"did:privy:..."` | Player DID |
| `username` | string | `"N0m4D"` | Player display name |
| `level` | int | `14` | Player level |
| `amount` | number | `0.002` | SOL amount |
| `qty` | number | `0.001384584` | Token quantity received |
| `price` | number | `1.4444769765` | Execution price |
| `tickIndex` | int | `16` | Tick when executed |
| `type` | string | `"buy"` | Trade type (buy/sell) |
| `leverage` | int | `1` | Position leverage (1 = spot) |
| `coin` | string | `"solana"` | Token identifier |
| `bonusPortion` | number | `0` | Bonus SOL portion |
| `realPortion` | number | `0.002` | Real SOL portion |
| `__trace` | bool | `true` | Tracing enabled |
| `traceparent` | string | `"00-..."` | Trace ID |

#### 3. success (Server → Client ACK)

**Direction**: Incoming (ACK response)
**Purpose**: Acknowledge successful action
**Category**: SYSTEM_ACK

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `success` | bool | `true` | Action succeeded |

**Message Format**: `4329[{success: true}]`
- The `29` matches the buyOrder's `29` - this is the ACK

---

### NEW FIELDS IN EXISTING EVENTS

#### gameStatePlayerUpdate - New Fields

| Field Path | Type | Example | Priority | Description |
|------------|------|---------|:--------:|-------------|
| `leaderboardEntry.regularPnl` | number | `0.000745529` | P1 | PnL from main trades only |
| `leaderboardEntry.shortPnl` | number | `0` | P1 | PnL from short positions |
| `leaderboardEntry.sidebetPnl` | number | `0` | P1 | PnL from sidebets |

**Note**: `pnl = regularPnl + shortPnl + sidebetPnl` (hypothesis)

#### gameStateUpdate - GodCandle Fields (NEW)

| Field | Type | Description | Priority |
|-------|------|-------------|:--------:|
| `godCandle2x` | null/object | 2x godcandle data | P2 |
| `godCandle2xMassiveJump` | null/bool | Massive jump flag at 2x | P2 |
| `godCandle2xPrices` | array | Price history for 2x candle | P2 |
| `godCandle2xTimestamp` | null/int | When 2x godcandle occurred | P2 |
| `godCandle10x` | null/object | 10x godcandle data | P2 |
| `godCandle10xMassiveJump` | null/bool | Massive jump flag at 10x | P2 |
| `godCandle10xPrices` | array | Price history for 10x candle | P2 |
| `godCandle10xTimestamp` | null/int | When 10x godcandle occurred | P2 |
| `godCandle50x` | null/object | 50x godcandle data | P2 |
| `godCandle50xMassiveJump` | null/bool | Massive jump flag at 50x | P2 |
| `godCandle50xPrices` | array | Price history for 50x candle | P2 |
| `godCandle50xTimestamp` | null/int | When 50x godcandle occurred | P2 |

**Use Case**: Track extreme price movements for aggregate analysis across games.

#### gameStateUpdate - Daily High Tracking

| Field | Type | Example | Priority | Description |
|-------|------|---------|:--------:|-------------|
| `highestToday` | number | `1329.975...` | P1 | Highest peak price today |
| `highestTodayTimestamp` | int | `1766855639499` | P1 | Unix ms when peak occurred |

---

### KEY INSIGHTS

#### 1. avgCost is Weighted Average Entry Price

**Before add-to-position**:
- `positionQty`: 0.002 SOL
- `avgCost`: 1.0 (entered at price 1.0)

**After add-to-position**:
- `positionQty`: 0.003384584 SOL
- `avgCost`: 1.181828845 (weighted average)

**Calculation**:
```
New avgCost = (old_qty * old_price + new_qty * new_price) / total_qty
            = (0.002 * 1.0 + 0.001384584 * 1.4444769765) / 0.003384584
            = (0.002 + 0.002) / 0.003384584
            ≈ 1.1818
```

**Conclusion**: `avgCost` is NOT lifetime profitability - it's the weighted average entry price for the current position.

#### 2. Socket.IO ACK Pattern

**Request**: `4229["buyOrder", ...]` - The `29` is the ACK ID
**Response**: `4329[{success: true}]` - The `29` matches, prefixed with `43`

This allows matching requests to responses for async operations.

#### 3. Trade Execution Flow

```
Client                          Server
  |                               |
  |-- buyOrder (4229) ----------->|
  |                               |
  |<-- standard/newTrade ---------|  (broadcast to all)
  |                               |
  |<-- playerUpdate --------------|  (personal balance)
  |                               |
  |<-- gameStatePlayerUpdate -----|  (personal position)
  |                               |
  |<-- success (4329) ------------|  (ACK)
  |                               |
```

**Total Latency**: ~219ms (buyOrder → success)

#### 4. Event Ordering for Add-to-Position

1. `buyOrder` - Client sends buy request
2. `standard/newTrade` - Server broadcasts trade
3. `playerUpdate` - Server syncs balance/position
4. `gameStatePlayerUpdate` - Server updates leaderboard entry
5. `success` - Server acknowledges

---

## Categorization Note

**ACTION**: When reviewing for canonical verification, create categorical sort:

| Category | Events | Direction |
|----------|--------|-----------|
| TRADING_ACTION | `buyOrder`, `sellOrder` | Client → Server |
| TRADING_EVENT | `standard/newTrade` | Server → Client (broadcast) |
| PLAYER_STATE | `playerUpdate`, `gameStatePlayerUpdate` | Server → Client (personal) |
| GAME_STATE | `gameStateUpdate` | Server → Client (broadcast) |
| SYSTEM_ACK | `success` | Server → Client (ACK) |

---

## Summary of Undocumented Elements

### New Event Types: 3

| Event | Direction | Priority |
|-------|-----------|:--------:|
| `buyOrder` | Client → Server | P0 |
| `standard/newTrade` | Server → Client | P0 |
| `success` | Server → Client (ACK) | P1 |

### New Fields: 18

| Category | Field Count | Priority |
|----------|:-----------:|:--------:|
| gameStatePlayerUpdate PnL breakdown | 3 | P1 |
| GodCandle tracking | 12 | P2 |
| Daily high tracking | 2 | P1 |
| Trade tracing | 2 | P3 |

### Behavioral Patterns: 2

1. **Trade execution flow** (5-event sequence)
2. **Socket.IO ACK pattern** (42XX → 43XX)

---

## Open Questions for Investigation

1. **avgCost lifetime tracking**: Is there a separate field for lifetime average profitability?
2. **GodCandle definition**: What triggers a "godCandle" vs regular price movement?
3. **MassiveJump threshold**: What constitutes a "massive jump"?
4. **Leverage > 1**: When is leverage used? Future/margin trading?

---

## Next Steps

- [ ] Capture Question 3 events (Closing position)
- [ ] Capture Question 4 events (Partial close)
- [ ] Prepare staging plan for canonical review
- [ ] Categorize all events by direction (Client→Server vs Server→Client)
