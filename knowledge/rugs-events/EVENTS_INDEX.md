# Rugs.fun WebSocket Events Index

> Master index of all Socket.IO events in the rugs.fun protocol.
> Last updated: 2025-12-14 from raw capture analysis.

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
| `count2x` | number | Games reaching 2x today |
| `count10x` | number | Games reaching 10x today |
| `count50x` | number | Games reaching 50x today |
| `count100x` | number | Games reaching 100x today |
| `highestToday` | number | Highest multiplier today |

#### Nested Objects

##### leaderboard[]
Top 10 players in current game.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Player's privy DID |
| `username` | string | Display name |
| `level` | number | Player level |
| `pnl` | number | Total profit/loss (SOL) |
| `regularPnl` | number | P&L from regular trades |
| `sidebetPnl` | number | P&L from sidebets |
| `shortPnl` | number | P&L from shorts |
| `pnlPercent` | number | P&L as percentage |
| `hasActiveTrades` | boolean | Has open position |
| `positionQty` | number | Position size |
| `avgCost` | number | Average entry price |
| `totalInvested` | number | Total SOL invested |
| `sidebetActive` | boolean | Has active sidebet |
| `sideBet` | object | Sidebet details (if active) |
| `shortPosition` | object | Short position (if any) |
| `position` | number | Leaderboard rank (1-10) |

##### sideBet (nested in leaderboard entry)
| Field | Type | Description |
|-------|------|-------------|
| `startedAtTick` | number | Tick when sidebet placed |
| `gameId` | string | Game ID |
| `end` | number | Tick when sidebet resolves |
| `betAmount` | number | Amount wagered |
| `xPayout` | number | Multiplier on win (typically 5x) |
| `coinAddress` | string | Token address |
| `bonusPortion` | number | Bonus portion of bet |
| `realPortion` | number | Real SOL portion |

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
| `globalTrades` | array | All trades in game |
| `globalSidebets` | array | All sidebets in game |
| `provablyFair` | object | Server seed reveal |

##### rugpool
Instarug lottery pool.

| Field | Type | Description |
|-------|------|-------------|
| `instarugCount` | number | Current instarug count |
| `threshold` | number | Threshold for payout |
| `rugpoolAmount` | number | Current pool size (SOL) |

##### provablyFair
Cryptographic fairness proof.

| Field | Type | Description |
|-------|------|-------------|
| `serverSeedHash` | string | Hash of server seed (pre-reveal) |
| `serverSeed` | string | Actual seed (post-game reveal) |
| `version` | string | Provably fair version |

##### rugRoyale
Tournament mode data.

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | INACTIVE, ACTIVE, etc. |
| `activeEventId` | string | Current event ID |
| `currentEvent` | object | Event details |
| `upcomingEvents` | array | Future events |
| `events` | array | All events |

---

### standard/newTrade

Broadcasts when ANY player makes a trade.

- **Frequency**: Sporadic (depends on market activity)
- **Auth Required**: No
- **Note**: Your OWN trades appear here to other players

#### Data Structure
Array with trace header + trade object:
```json
[
  {"__trace": true, "traceparent": "..."},
  {
    "id": "uuid",
    "gameId": "20251214-xxx",
    "playerId": "did:privy:xxx",
    "type": "buy" | "sell",
    "price": 1.234,
    "tickIndex": 17,
    "coin": "solana",
    "amount": 0.123,
    "qty": 5,
    "bonusPortion": 0.1,
    "realPortion": 0.023,
    "username": "PlayerName",
    "level": 42
  }
]
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Trade UUID |
| `gameId` | string | Game identifier |
| `playerId` | string | Trader's privy DID |
| `type` | string | `buy` or `sell` |
| `price` | number | Price at trade time |
| `tickIndex` | number | Tick when trade executed |
| `coin` | string | Token type |
| `amount` | number | SOL value |
| `qty` | number | Quantity |
| `bonusPortion` | number | Bonus SOL used |
| `realPortion` | number | Real SOL used |
| `username` | string | Trader's display name |
| `level` | number | Trader's level |

---

### newChatMessage

Chat message broadcast.

- **Frequency**: Sporadic
- **Auth Required**: No

#### Data Structure
```json
[
  {"__trace": true, "traceparent": "..."},
  {
    "playerId": "did:privy:xxx",
    "username": "PlayerName",
    "level": 55,
    "message": "Hello world",
    "timestamp": 1765577835613,
    "filtered": false,
    "role": null,
    "tag": "ghoul",
    "verified": true,
    "discordUsername": "player#1234"
  }
]
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `playerId` | string | Sender's privy DID |
| `username` | string | Display name |
| `level` | number | Player level |
| `message` | string | Chat content |
| `timestamp` | number | Unix timestamp (ms) |
| `filtered` | boolean | Was content filtered |
| `role` | string | Special role (admin, mod, etc.) |
| `tag` | string | Player tag/badge |
| `verified` | boolean | Verified account |
| `discordUsername` | string | Discord link (if any) |

---

### goldenHourUpdate

Lottery/raffle event status updates.

- **Frequency**: Sporadic (during golden hour events)
- **Auth Required**: No

#### Data Structure
```json
[
  {"__trace": true, "traceparent": "..."},
  {
    "status": "ACTIVE",
    "activeEventId": "admin-xxx",
    "currentEvent": {
      "id": "admin-xxx",
      "startTime": "2025-12-14T05:05:00.000Z",
      "endTime": "2025-12-15T05:05:00.000Z",
      "levelRequired": 10,
      "status": "SCHEDULED",
      "prizeAmount": 0.05,
      "maxEntries": 50,
      "durationMinutes": 60
    },
    "upcomingEvents": [],
    "events": [...]
  }
]
```

---

### goldenHourDrawing

Lottery drawing results.

- **Frequency**: When drawing occurs
- **Auth Required**: No

#### Data Structure
```json
[
  {"__trace": true, "traceparent": "..."},
  {
    "id": "drawing-uuid",
    "timestamp": 1765731135035,
    "gameId": "20251214-xxx",
    "entries": [
      {
        "playerId": "did:privy:xxx",
        "username": "PlayerName",
        "entryCount": 50,
        "entryPercentage": 3.39
      }
    ]
  }
]
```

---

### battleEventUpdate

Battle mode tournament updates.

- **Frequency**: During battle events
- **Auth Required**: No

#### Key Fields
- `status`: INACTIVE, ACTIVE, QUEUING
- `leaderboard`: Battle rankings
- `queue`: Waiting players
- `config`: Battle settings

---

## Auth-Required Events

These events are only sent to authenticated clients (wallet connected).

### usernameStatus

Confirms player identity after authentication.

#### Data Structure
```json
{
  "id": "did:privy:xxx",
  "username": "YourName",
  "level": 42
}
```

### playerUpdate

Server-side truth for your balance and positions.

#### Key Fields
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

### Detecting Sidebet Resolution
```python
# In leaderboard entry
if player['sidebetActive'] == False and previous_sidebet_active == True:
    # Sidebet just resolved
```

---

## Data Sources

- **Raw Captures**: `/home/nomad/rugs_recordings/raw_captures/`
- **REPLAYER Spec**: `/home/nomad/Desktop/REPLAYER/docs/specs/WEBSOCKET_EVENTS_SPEC.md`
- **Capture Analyzed**: `2025-12-14_11-51-33_raw.jsonl` (1,199 events, 7 types)

---

## Usage in REPLAYER

| Event | Handler Location | Purpose |
|-------|------------------|---------|
| `gameStateUpdate` | `src/sources/websocket_feed.py:790` | Primary signal source |
| `gameStateUpdate` | `src/sources/game_state_machine.py` | Phase detection |
| All events | `src/debug/raw_capture_recorder.py` | Protocol debugging |

---

*This index is iteratively updated as new events are discovered.*
