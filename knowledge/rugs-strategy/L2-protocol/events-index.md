---
layer: 2
domain: protocol/events
priority: P0
bot_relevant: true
validation_tier: canonical
source_file: "RAG SUPERPACK/EVENTS_INDEX.md"
cross_refs:
  - L2-protocol/websocket-spec.md
  - L2-protocol/field-dictionary.md
last_validated: 2025-12-24
---

# Rugs.fun WebSocket Events Index

> Master index of all Socket.IO events in the rugs.fun protocol.
> Last updated: 2025-12-24 from raw capture analysis.

## Overview

Rugs.fun uses Socket.IO for real-time game communication. Events fall into two categories:
1. **Server Broadcast** - Sent to all connected clients (no auth required)
2. **Auth-Required** - Sent only to authenticated clients with wallet connection

## Event Summary

| Event | Category | Frequency | Auth | Description |
|-------|----------|-----------|------|-------------|
| `gameStateUpdate` | Broadcast | ~4/sec | No | Core game state (price, leaderboard, phase) |
| `standard/newTrade` | Broadcast | Sporadic | No | Other players' trade broadcasts |
| `newChatMessage` | Broadcast | Sporadic | No | Chat messages with player metadata |
| `goldenHourUpdate` | Broadcast | Sporadic | No | Lottery event status updates |
| `goldenHourDrawing` | Broadcast | Sporadic | No | Lottery drawing results |
| `battleEventUpdate` | Broadcast | Sporadic | No | Battle mode status |
| `connect` | Protocol | Once | No | Connection established |
| `disconnect` | Protocol | Once | No | Connection lost |
| `usernameStatus` | Auth | Once | Yes | Player identity confirmation |
| `playerUpdate` | Auth | Sporadic | Yes | Server-side balance/position sync |
| `playerLeaderboardPosition` | Auth | Sporadic | Yes | Your 7-day leaderboard rank |
| `gameStatePlayerUpdate` | Auth | ~4/sec | Yes | Your entry in leaderboard |
| `buyOrderResponse` | Auth | On action | Yes | Buy trade confirmation |
| `sellOrderResponse` | Auth | On action | Yes | Sell trade confirmation |
| `sidebetResponse` | Auth | On action | Yes | Sidebet confirmation |

---

## Server Broadcast Events

### gameStateUpdate

**The most important event** - contains ALL game state data.

- **Frequency**: ~4 per second (every 250ms)
- **Size**: Large (contains leaderboard, history, nested objects)
- **Auth Required**: No

#### Root Fields (36+)

| Field | Type | Description |
|-------|------|-------------|
| `gameId` | string | Unique game identifier (format: `YYYYMMDD-uuid`) |
| `gameVersion` | string | Protocol version (currently `v3`) |
| `active` | boolean | `true` if game is in progress |
| `rugged` | boolean | `true` if game has ended (rug pull) |
| `price` | number | Current multiplier (1.0 = entry price) |
| `tickCount` | number | Ticks since game start (0-based) |
| `cooldownTimer` | number | Milliseconds until next game (0 during active) |
| `cooldownPaused` | boolean | Whether cooldown is paused |
| `pauseMessage` | string | Message during pause |
| `allowPreRoundBuys` | boolean | Can place bets before game starts |
| `tradeCount` | number | Total trades this game |
| `connectedPlayers` | number | Players currently connected |
| `averageMultiplier` | number | Historical average peak multiplier |

#### Nested Objects

##### leaderboard[]
Top 10 players in current game.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Player's privy DID |
| `username` | string | Display name |
| `level` | number | Player level |
| `pnl` | number | Total profit/loss (SOL) |
| `hasActiveTrades` | boolean | Has open position |
| `positionQty` | number | Position size |
| `avgCost` | number | Average entry price |
| `totalInvested` | number | Total SOL invested |
| `sidebetActive` | boolean | Has active sidebet |
| `position` | number | Leaderboard rank (1-10) |

##### partialPrices
Backfill data for missed ticks.

| Field | Type | Description |
|-------|------|-------------|
| `startTick` | number | First tick in range |
| `endTick` | number | Last tick in range |
| `values` | object | Map of tick -> price |

##### gameHistory[]
Recent completed games (array of game summaries).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Game ID |
| `timestamp` | number | Unix timestamp (ms) |
| `prices` | number[] | All prices from game |
| `peakMultiplier` | number | Highest price reached |
| `rugged` | boolean | Always true (completed) |
| `provablyFair` | object | Server seed reveal |

---

### standard/newTrade

Broadcasts when ANY player makes a trade.

- **Frequency**: Sporadic (depends on market activity)
- **Auth Required**: No
- **Note**: Your OWN trades appear here to other players

#### Data Structure
```json
{
  "id": "uuid",
  "gameId": "20251214-xxx",
  "playerId": "did:privy:xxx",
  "type": "buy" | "sell",
  "price": 1.234,
  "tickIndex": 17,
  "amount": 0.123,
  "username": "PlayerName",
  "level": 42
}
```

---

## Auth-Required Events

These events are only sent to authenticated clients (wallet connected).

### usernameStatus

Confirms player identity after authentication.

```json
{
  "id": "did:privy:xxx",
  "username": "YourName",
  "level": 42
}
```

### playerUpdate

Server-side truth for your balance and positions.

| Field | Type | Description |
|-------|------|-------------|
| `cash` | number | Available balance (SOL) |
| `positionQty` | number | Current position size |
| `avgCost` | number | Average entry price |
| `totalInvested` | number | Total invested |
| `cumulativePnl` | number | All-time P&L |

### Trade Responses

- `buyOrderResponse` - Confirmation of buy order
- `sellOrderResponse` - Confirmation of sell order
- `sidebetResponse` - Confirmation of sidebet placement

Each includes:
- `success`: boolean
- `timestamp`: number (for latency calculation)
- `orderId`: string
- Error details if failed

---

## Event Detection Patterns

### Detecting Game Start
```python
if event['active'] == True and previous_active == False:
    # Game just started
```

### Detecting Rug Event
```python
if event['rugged'] == True and previous_rugged == False:
    # Rug just happened
```

### Detecting Phase Transitions
```python
if event['cooldownTimer'] > 0:
    phase = 'COOLDOWN'
elif event['active']:
    phase = 'ACTIVE_GAMEPLAY'
elif event['rugged']:
    phase = 'RUG_EVENT'
```

---

## Data Sources

- **Raw Captures**: `/home/nomad/rugs_recordings/raw_captures/`
- **REPLAYER Spec**: `/home/nomad/Desktop/REPLAYER/docs/specs/WEBSOCKET_EVENTS_SPEC.md`
- **Capture Analyzed**: `2025-12-14_11-51-33_raw.jsonl` (1,199 events, 7 types)

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
