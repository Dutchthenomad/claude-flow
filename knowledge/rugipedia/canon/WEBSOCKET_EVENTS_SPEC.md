# WebSocket Events Specification
**rugs.fun Socket.IO Protocol** | **Version**: 3.0 | **Date**: December 28, 2025

> **Canonical Source**: This is the single source of truth for rugs.fun protocol documentation.
> All downstream formats (JSONL, JSON indexes, vector embeddings) are derived from this file.

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
| `42` | Standard broadcast event (Server → Client) |
| `42XXXX` | Client request with ID `XXXX` (Client → Server) |
| `43XXXX` | Response to request with ID `XXXX` (Server → Client ACK) |

### Event Category Taxonomy

| Category | Events | Direction | Description |
|----------|--------|-----------|-------------|
| **TRADING_ACTION** | `buyOrder`, `sellOrder` | Client → Server | User trade requests |
| **TRADING_EVENT** | `standard/newTrade` | Server → Client | Trade broadcasts (all players) |
| **SIDEBET_ACTION** | `requestSidebet` | Client → Server | Sidebet placement request |
| **SIDEBET_EVENT** | `currentSidebet`, `currentSidebetResult` | Server → Client | Sidebet confirmations/payouts |
| **PLAYER_STATE** | `playerUpdate`, `gameStatePlayerUpdate` | Server → Client | Personal state (auth required) |
| **GAME_STATE** | `gameStateUpdate` | Server → Client | Global game state broadcast |
| **SPECIAL_EVENT** | `goldenHourUpdate`, `rugRoyaleUpdate` | Server → Client | Tournament/event updates |
| **GAMIFICATION** | `rugPassQuestCompleted` | Server → Client | Quest/achievement events |
| **SYSTEM_HEARTBEAT** | `ping` | Client → Server | Connection keepalive |
| **SYSTEM_ACK** | `success`, empty ACK (`43XX[]`) | Server → Client | Request acknowledgments |
| **IDENTITY** | `usernameStatus`, `playerLeaderboardPosition` | Server → Client | Auth confirmation (once on connect) |

### Authentication Requirements

**IMPORTANT**: Some events require wallet authentication:

| Event | Auth Required | When Sent |
|-------|---------------|-----------|
| `gameStateUpdate` | No | Every tick (~4/sec) |
| `usernameStatus` | **YES** | Once on connection (if logged in) |
| `playerUpdate` | **YES** | After **server-side** trades only |
| `playerLeaderboardPosition` | **YES** | Once on connection (if logged in) |

**Key Insight**: If the user is not logged in with their Phantom wallet, `usernameStatus`, `playerUpdate`, and `playerLeaderboardPosition` will NOT be sent.

### Our Authentication Setup

We use a **dedicated Chrome profile** with automated authentication:

| Component | Details |
|-----------|---------|
| **Chrome Profile** | `~/.gamebot/chrome_profiles/rugs_bot` |
| **Wallet** | Phantom (Solana) - pre-installed in profile |
| **Player ID** | `did:privy:cmaibr7rt0094jp0mc2mbpfu4` |
| **Username** | `Dutch` |
| **Automation** | Puppeteer/Playwright with CDP connection |

**How It Works**:
1. Puppeteer launches Chrome with the dedicated profile (`--user-data-dir`)
2. Profile already has Phantom wallet extension installed and configured
3. Browser navigates to rugs.fun, wallet auto-connects via stored session
4. CDP WebSocket interception captures ALL events (including auth-required)

**Key Benefit**: Unlike raw WebSocket captures (unauthenticated), our CDP interception through the authenticated browser session receives:
- `usernameStatus` - Confirms our player identity
- `playerUpdate` - Server-authoritative balance/position
- `gameStatePlayerUpdate` - Our leaderboard entry
- Trade responses (`buyOrderResponse`, `sellOrderResponse`, `sidebetResponse`)

**Profile Setup Script**: `scripts/setup_phantom_profile.py` (CV-BOILER-PLATE-FORK)

**CDP Connection**: See `BROWSER_CONNECTION_PROTOCOL.md` for detailed CDP setup instructions.

---

## Current Capture Status

### Currently Captured (9 fields)
```
gameId, active, rugged, tickCount, price,
cooldownTimer, allowPreRoundBuys, tradeCount, gameHistory
```

### High-Value Ignored (303+ fields)
See Priority Integration sections below.

---

## Game Cycle State Machine

Understanding the game phases is critical for interpreting events correctly. Events and fields have different meanings depending on the current phase.

### Phases

| Phase | Trigger | Duration | Key Indicators |
|-------|---------|----------|----------------|
| `COOLDOWN` | Previous game rugged | ~10-30 sec | `cooldownTimer > 0`, `active = false`, `rugged = true` |
| `PRESALE` | Cooldown ends | Until game starts | `allowPreRoundBuys = true`, `active = false`, `cooldownTimer = 0` |
| `ACTIVE` | Game starts | Variable (until rug) | `active = true`, `rugged = false` |
| `RUGGED` | Rug event | Instant (transitions to COOLDOWN) | `rugged = true`, `active = false` |

### Phase Transitions

```
┌──────────┐    timer=0     ┌──────────┐   game starts   ┌──────────┐
│ COOLDOWN │ ─────────────▶ │ PRESALE  │ ──────────────▶ │  ACTIVE  │
└──────────┘                └──────────┘                 └──────────┘
     ▲                                                        │
     │                        rug event                       │
     └────────────────────────────────────────────────────────┘
```

### Phase Detection Logic

```python
def detect_phase(event: dict) -> str:
    """Determine current game phase from gameStateUpdate."""
    if event.get('cooldownTimer', 0) > 0:
        return 'COOLDOWN'
    elif event.get('rugged', False) and not event.get('active', False):
        return 'COOLDOWN'  # Brief moment after rug
    elif event.get('allowPreRoundBuys', False) and not event.get('active', False):
        return 'PRESALE'
    elif event.get('active', False) and not event.get('rugged', False):
        return 'ACTIVE'
    elif event.get('rugged', False):
        return 'RUGGED'
    else:
        return 'UNKNOWN'
```

### Event-Phase Matrix

Which events fire during which phases:

| Event | COOLDOWN | PRESALE | ACTIVE | RUGGED | Notes |
|-------|:--------:|:-------:|:------:|:------:|-------|
| `gameStateUpdate` | ✅ | ✅ | ✅ | ✅ | Always broadcasts |
| `usernameStatus` | ✅ | ✅ | ✅ | ✅ | Once on connection |
| `playerLeaderboardPosition` | ✅ | ✅ | ✅ | ✅ | Once on connection |
| `standard/newTrade` | ❌ | ✅ | ✅ | ❌ | Only during trading |
| `playerUpdate` | ❌ | ✅ | ✅ | ✅ | After trades settle |
| `gameStatePlayerUpdate` | ❌ | ✅ | ✅ | ✅ | After trades settle |
| `sidebetResponse` | ❌ | ❌ | ✅ | ❌ | Active phase only |
| `buyOrder/sellOrder` | ❌ | ✅ | ✅ | ❌ | Trading phases only |
| `newChatMessage` | ✅ | ✅ | ✅ | ✅ | Always |
| `goldenHourUpdate` | ✅ | ✅ | ✅ | ✅ | During events |
| `rugRoyaleUpdate` | ✅ | ✅ | ✅ | ✅ | During tournaments |

### Phase-Specific Behaviors

#### COOLDOWN Phase
- `price` field shows final rug price from previous game
- `tickCount` frozen at final tick
- `leaderboard` shows previous game's final standings
- `cooldownTimer` counts down in milliseconds

#### PRESALE Phase
- `price` resets to `1.0` (entry price)
- `tickCount` is `0`
- `allowPreRoundBuys = true`
- Players can place pre-round buy orders
- No sells allowed

#### ACTIVE Phase
- `price` fluctuates based on game mechanics
- `tickCount` increments (~4/sec)
- Full trading enabled (buy/sell)
- Sidebets can be placed
- `leaderboard` updates in real-time

#### RUGGED Phase
- `rugged = true` signals game end
- Positions auto-liquidated at rug price
- Brief phase before transitioning to COOLDOWN
- `provablyFair.serverSeed` revealed

---

## Event Taxonomy

### 1. `gameStateUpdate` (Primary Tick Event) ✅ VERIFIED

**Frequency**: ~4x/second (~250ms intervals)
**Purpose**: Complete game state broadcast to all connected clients
**Auth Required**: No
**Scope**: IN_SCOPE
**Priority**: P0
**Phases**: COOLDOWN, PRESALE, ACTIVE, RUGGED

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
| `highestTodayPrices` | array | `[1, 0.99, ...]` | Price history for daily high |

#### God Candle Fields (Celebration Events)

> **NEEDS VALIDATION**: God candles are rare "jackpot" events where the price jumps dramatically.
> We need to capture live examples to validate these field structures.
>
> **PRNG Algorithm**: The game's random number generator is documented at:
> `/home/nomad/Desktop/claude-flow/knowledge/PRNG-algorithm-source-code.txt`

| Field | Type | Description |
|-------|------|-------------|
| `godCandle2x` | float/null | 2x celebration price |
| `godCandle2xTimestamp` | int/null | When 2x was hit |
| `godCandle2xPrices` | array | Price history for 2x candle |
| `godCandle2xMassiveJump` | bool/null | Large price jump indicator |
| `godCandle10x` | float/null | 10x celebration price |
| `godCandle10xTimestamp` | int/null | When 10x was hit |
| `godCandle10xPrices` | array | Price history for 10x candle |
| `godCandle10xMassiveJump` | bool/null | Large price jump indicator |
| `godCandle50x` | float/null | 50x celebration price |
| `godCandle50xTimestamp` | int/null | When 50x was hit |
| `godCandle50xPrices` | array | Price history for 50x candle |
| `godCandle50xMassiveJump` | bool/null | Large price jump indicator |

#### Available Coins

```json
{
  "availableShitcoins": [
    {
      "address": "0xPractice",
      "ticker": "FREE",
      "name": "Practice SOL",
      "max_bet": 10000,
      "max_win": 100000
    }
  ]
}
```

#### Provably Fair

```json
{
  "provablyFair": {
    "serverSeedHash": "bce190330836fffda61bdecbed6d8a83bfb7bb3a6b2bd278002a36df773c809a",
    "version": "v3"
  }
}
```

#### Rug Royale (Tournament Mode)

```json
{
  "rugRoyale": {
    "status": "INACTIVE",
    "activeEventId": null,
    "currentEvent": null,
    "upcomingEvents": [],
    "events": []
  }
}
```

#### Price History (`partialPrices`)

```json
{
  "partialPrices": {
    "startTick": 125,
    "endTick": 129,
    "values": {
      "125": 1.2749526227232495,
      "126": 1.3019525694480605,
      "127": 1.073446660724414,
      "128": 1.0654483722620864,
      "129": 1.061531247396796
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `startTick` | int | Window start tick |
| `endTick` | int | Window end tick |
| `values` | dict | Tick-indexed price map |

**Use Case**: Backfill missed ticks, verify price continuity, latency analysis.

#### Leaderboard (`leaderboard[]`)

Each entry represents a player with active position or recent activity:

```json
{
  "id": "did:privy:cmigqkf0f00x4jm0cuxvdrunq",
  "username": "Fannyman",
  "level": 43,
  "pnl": 0.264879755,
  "regularPnl": 0.264879755,
  "sidebetPnl": 0,
  "shortPnl": 0,
  "pnlPercent": 105.38,
  "hasActiveTrades": true,
  "positionQty": 0.2222919,
  "avgCost": 1.259605046,
  "totalInvested": 0.251352892,
  "sidebetActive": null,
  "sideBet": null,
  "shortPosition": null,
  "selectedCoin": null,
  "position": 1
}
```

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

#### Rugpool (`rugpool`)

```json
{
  "rugpool": {
    "rugpoolAmount": 1.025,
    "threshold": 10,
    "instarugCount": 2
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `rugpoolAmount` | float | Current rugpool SOL |
| `threshold` | int | Instarug trigger threshold |
| `instarugCount` | int | Instarugs this session |

**Use Case**: Instarug prediction - alert when `rugpoolAmount` approaches `threshold`.

#### Game History (`gameHistory[]`)

> **HIGH VALUE - ML/RL GOLD MINE**: This rolling window of recent games could replace our passive recording system.
>
> **TODO (GitHub Issue)**: Implement server-side game history collection:
> - Rolling window of last ~10 games (verify exact count)
> - Track by `gameId` to avoid duplicates
> - Contains tick-by-tick price data (`prices` array)
> - Includes all player trades, PnL, positions
> - Drastically reduces manual data collection effort for RL/ML training
>
> **Current System**: We manually record games via CDP WebSocket interception
> **Proposed System**: Pull historical data directly from `gameHistory[]` on each tick

Array of recent game summaries:

```json
{
  "id": "20251207-1e01ac417e8043ca",
  "timestamp": 1765068982439,
  "prices": [1, 0.99, 1.01, ...],
  "rugged": true,
  "rugPoint": 45.23
}
```

**Full Game History Entry** (needs validation - may include more fields):

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Game ID (format: `YYYYMMDD-uuid`) |
| `timestamp` | int | Unix timestamp (ms) when game ended |
| `prices` | array | Tick-by-tick price history |
| `rugged` | bool | Always `true` (completed games only) |
| `rugPoint` | float | Final rug multiplier |
| `globalTrades` | array | All trades in game (TBD - needs validation) |
| `globalSidebets` | array | All sidebets in game (TBD - needs validation) |
| `provablyFair` | object | Server seed reveal (TBD - needs validation) |

---

### 2. `usernameStatus` (Identity Event) ✅ VERIFIED

**Frequency**: Once on connection (requires wallet auth)
**Purpose**: Player identity confirmation
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Phases**: COOLDOWN, PRESALE, ACTIVE, RUGGED

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
| `__trace` | bool | `true` | Tracing enabled (internal) |
| `traceparent` | string | `"00-..."` | OpenTelemetry trace ID |

**Use Case**:
- Identify "our" player in leaderboard array
- Filter `playerUpdate` events for our player
- Session identity confirmation
- **Validate connection is authenticated**

**Implementation Note**: This event will NOT fire if the user is not logged in with their wallet. Use presence of this event to confirm authenticated session.

---

### 2.5. `playerLeaderboardPosition` (Leaderboard Rank Event) ✅ VERIFIED

**Frequency**: Once on connection (requires wallet auth)
**Purpose**: Player's current leaderboard standing
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P2
**Phases**: COOLDOWN, PRESALE, ACTIVE, RUGGED

```json
42["playerLeaderboardPosition",
  {"__trace": true, "traceparent": "00-68b4bec76e0efdf689a9091e89dce4dc-bcb52d7918ef5a5b-01"},
  {
    "success": true,
    "period": "7d",
    "sortDirection": "highest",
    "playerFound": true,
    "rank": 1164,
    "total": 2595,
    "playerEntry": {
      "playerId": "did:privy:cmaibr7rt0094jp0mc2mbpfu4",
      "username": "Dutch",
      "pnl": -0.015559657000000001
    },
    "surroundingEntries": [...]
  }
]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `success` | bool | `true` | Query successful |
| `period` | string | `"7d"` | Leaderboard period (7-day) |
| `sortDirection` | string | `"highest"` | Sort order |
| `playerFound` | bool | `true` | Player on leaderboard |
| `rank` | int | `1164` | Current rank position |
| `total` | int | `2595` | Total players on leaderboard |
| `playerEntry` | object | `{...}` | Player's leaderboard entry |
| `surroundingEntries` | array | `[...]` | Nearby players |

**playerEntry Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `playerId` | string | Player's Privy DID |
| `username` | string | Display name |
| `pnl` | float | 7-day PnL (SOL) |

**Use Case**:
- Validate authenticated connection (secondary to `usernameStatus`)
- Display player's current leaderboard standing
- Track competitive position over time

---

### 3. `standard/newTrade` (Trade Broadcast) ✅ VERIFIED

**Frequency**: On every trade by any player
**Purpose**: Real-time trade feed (broadcast to all connected clients)
**Auth Required**: No
**Scope**: IN_SCOPE
**Priority**: P0
**Category**: TRADING_EVENT
**Phases**: PRESALE, ACTIVE

```json
42["standard/newTrade",
  {"__trace": true, "traceparent": "00-55110064298fdee6dc04d093c003b5c9-65b220dcba23a3a0-01"},
  {
    "id": "9111d2c8-efcc-449e-b081-0c8c59e0bc45",
    "gameId": "20251228-242b2d81e73e4f27",
    "playerId": "did:privy:cma094vht019il80np6aidhqd",
    "username": "N0m4D",
    "type": "buy",
    "amount": 0.002,
    "price": 1.4444769765026393,
    "qty": 0.001384584,
    "tickIndex": 16,
    "coin": "solana",
    "leverage": 1,
    "level": 14,
    "bonusPortion": 0,
    "realPortion": 0.002
  }
]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"9111d2c8-..."` | Unique trade ID |
| `gameId` | string | `"20251228-..."` | Game identifier |
| `playerId` | string | `"did:privy:..."` | Trader's player ID |
| `username` | string | `"N0m4D"` | Trader's display name |
| `type` | string | `"buy"` / `"sell"` | Trade type |
| `amount` | float | `0.002` | SOL amount traded |
| `price` | float | `1.4444769765` | Execution price |
| `qty` | float | `0.001384584` | Position quantity received |
| `tickIndex` | int | `16` | Tick when trade executed |
| `coin` | string | `"solana"` | Currency used |
| `leverage` | int | `1` | Leverage multiplier |
| `level` | int | `14` | Player level |
| `bonusPortion` | float | `0` | Bonus balance used |
| `realPortion` | float | `0.002` | Real SOL used |
| `__trace` | bool | `true` | Tracing enabled (internal) |
| `traceparent` | string | `"00-..."` | OpenTelemetry trace ID |

**Use Case**:
- Track all market activity
- Whale trade alerts
- Volume analysis
- ML training data (other players' behavior)
- Correlate with `buyOrder`/`sellOrder` via traceparent

---

### 4. `playerUpdate` (Personal State Sync) ✅ VERIFIED

**Frequency**: After each of our trades
**Purpose**: Sync local state with server truth
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P0
**Category**: PLAYER_STATE
**Phases**: PRESALE, ACTIVE, RUGGED

```json
42["playerUpdate",
  {
    "id": "did:privy:cma094vht019il80np6aidhqd",
    "role": null,
    "authenticated": true,
    "cash": 0.09503525,
    "bonusBalance": 0,
    "bonusWagerReq": 0,
    "bonusWagered": 0,
    "cumulativePnL": 0.000888953,
    "positionQty": 0.003384584,
    "avgCost": 1.181828845,
    "totalInvested": 0.004,
    "pnlPercent": 44.44765,
    "sidebetPnl": 0,
    "shortPosition": null,
    "leveragedPositions": [],
    "sidebets": [],
    "sideBet": null,
    "autobuysEnabled": false,
    "autosellPrice": null,
    "hasInteracted": true,
    "hitMaxWin": false,
    "selectedCoin": null,
    "shitcoinBalances": {"0xPractice": 100},
    "levelInfo": {"level": 14, "xp": 1956, "xpForNextLevel": 5000, "totalXP": 31956},
    "xpBoost": {"active": false, "activeUntil": 0, "available": 0},
    "crateKeys": {"gold": 0, "diamond": 0, "coal": 0, "iron": 0, "tier1": 0, "tier0": 0},
    "recentCrateRewards": [...]
  }
]
```

#### Identity & Auth (P0)
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"did:privy:..."` | Player ID |
| `role` | null/string | `null` | Player role |
| `authenticated` | bool | `true` | Auth status |

#### Core Trading (P0)
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `cash` | float | `0.09503525` | **TRUE wallet balance** |
| `cumulativePnL` | float | `0.000888953` | Total PnL this game |
| `positionQty` | float | `0.003384584` | Current position size |
| `avgCost` | float | `1.181828845` | **Weighted avg entry price** |
| `totalInvested` | float | `0.004` | Total invested this game |

#### Position Tracking (P1)
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `pnlPercent` | float | `44.44765` | PnL percentage |
| `sidebetPnl` | float | `0` | Sidebet PnL |
| `shortPosition` | null/object | `null` | Short position details |
| `leveragedPositions` | array | `[]` | Leveraged positions |
| `sidebets` | array | `[]` | Active sidebets |
| `sideBet` | null/object | `{...}` | Current sidebet |

#### Trading Config (P1)
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `autobuysEnabled` | bool | `false` | Auto-buy feature |
| `autosellPrice` | null/float | `null` | Auto-sell trigger |
| `hasInteracted` | bool | `true` | Has traded this session |
| `hitMaxWin` | bool | `false` | Hit max win limit |
| `selectedCoin` | null/object | `null` | Selected trading coin |

#### Bonus System (P2)
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `bonusBalance` | float | `0` | Bonus balance |
| `bonusWagerReq` | float | `0` | Wagering requirement |
| `bonusWagered` | float | `0` | Amount wagered |
| `shitcoinBalances` | object | `{0xPractice: 100}` | Alt token balances |

#### Gamification (P3 - OUT_OF_SCOPE)
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `levelInfo.level` | int | `14` | Current level |
| `levelInfo.xp` | int | `1956` | Current XP |
| `levelInfo.xpForNextLevel` | int | `5000` | XP needed |
| `levelInfo.totalXP` | int | `31956` | Lifetime XP |
| `xpBoost.active` | bool | `false` | XP boost active |
| `xpBoost.activeUntil` | int | `0` | Boost expiry |
| `xpBoost.available` | int | `0` | Available boosts |
| `crateKeys` | object | `{gold:0, ...}` | Crate keys |
| `recentCrateRewards` | array | `[...]` | Recent rewards |

**Use Case**:
- **Critical for verification layer**
- Compare local `balance` calculation vs server `cash`
- Compare local position vs server `positionQty`
- Detect calculation drift
- **avgCost Calculation**: Weighted average = (old_qty × old_price + new_qty × new_price) / total_qty

---

### 5. `gameStatePlayerUpdate` (Personal Leaderboard Entry) ✅ VERIFIED

**Frequency**: After each of our trades
**Purpose**: Our leaderboard entry wrapped with game context
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Category**: PLAYER_STATE
**Phases**: PRESALE, ACTIVE, RUGGED

> **STRUCTURE CORRECTION**: This is NOT just leaderboard fields. It's a container with `gameId`, `leaderboardEntry`, and `rugpool`.

```json
42["gameStatePlayerUpdate",
  {
    "gameId": "20251228-242b2d81e73e4f27",
    "leaderboardEntry": {
      "id": "did:privy:cma094vht019il80np6aidhqd",
      "username": "N0m4D",
      "level": 14,
      "pnl": 0.000888953,
      "pnlPercent": 44.44765,
      "regularPnl": 0.000888953,
      "shortPnl": 0,
      "sidebetPnl": 0,
      "hasActiveTrades": true,
      "positionQty": 0.002,
      "avgCost": 1,
      "totalInvested": 0.002,
      "position": 39,
      "sidebetActive": null,
      "sideBet": null,
      "shortPosition": null,
      "selectedCoin": null
    },
    "rugpool": {
      "instarugCount": 3,
      "rugpoolAmount": 2.1897343695,
      "totalEntries": 8270,
      "threshold": 10
    }
  }
]
```

#### Root Fields
| Field | Type | Description |
|-------|------|-------------|
| `gameId` | string | Current game identifier |
| `leaderboardEntry` | object | Player's leaderboard data (see below) |
| `rugpool` | object | Current rugpool state |

#### leaderboardEntry Fields
Same as `leaderboard[]` items in `gameStateUpdate`, plus:

| Field | Type | Description |
|-------|------|-------------|
| `regularPnl` | float | PnL from regular trades only |
| `shortPnl` | float | PnL from short positions |
| `sidebetPnl` | float | PnL from sidebets |
| `sideBet.bonusPortion` | float | Bonus balance used for sidebet |
| `sideBet.coinAddress` | string | Token address for sidebet |
| `sideBet.realPortion` | float | Real SOL used for sidebet |

#### rugpool Fields
| Field | Type | Description |
|-------|------|-------------|
| `totalEntries` | int | Total rugpool entries (all players) |
| `rugpoolAmount` | float | Current pool size |
| `threshold` | int | Instarug trigger threshold |
| `instarugCount` | int | Instarugs this session |

---

### 6. Sidebet Response (Request/Response) ✅ VERIFIED

**Frequency**: On sidebet action
**Purpose**: Confirm sidebet placement
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Phases**: ACTIVE

**Protocol**: Request ID matching (`43XXXX` response to request `42XXXX`)

#### Request (Client → Server)
```
42424["sidebet", {"target": 10, "betSize": 0.001}]
```

#### Response (Server → Client)
```
43424[{"success": true, "timestamp": 1765068967229}]
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Sidebet accepted |
| `timestamp` | int | **Server timestamp** |

**Use Case**:
- Confirm sidebet placement
- Calculate latency: `local_timestamp - server_timestamp`
- Track sidebet success rate

---

### 7. `buyOrder` / `sellOrder` (Trade Requests) ✅ VERIFIED

**Frequency**: On trade action
**Purpose**: Execute buy/sell trades
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P0
**Phases**: PRESALE, ACTIVE

**Protocol**: Request/response pattern

#### Request (Client → Server)
```
42425["buyOrder", {"amount": 0.001}]
42426["sellOrder", {"percentage": 100}]
```

#### Response (Server → Client)
```
43425[{"success": true, "executedPrice": 1.234, "timestamp": 1765069123456}]
```

---

### 8. `requestSidebet` (Sidebet Request) ✅ VERIFIED

**Frequency**: On sidebet button press
**Purpose**: Request sidebet placement
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P0
**Category**: SIDEBET_ACTION
**Phases**: ACTIVE

```json
42XXXX["requestSidebet",
  {"__trace": true, "traceparent": "00-7de6e8288fe05b8c02ced992bd355f31-99a9b4486091ff1b-01"},
  {"amount": 0.002, "coinAddress": "So11111111111111111111111111111111111111112", "xPayout": 5}
]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `amount` | float | `0.002` | Bet amount (SOL) |
| `coinAddress` | string | `"So111..."` | Token address |
| `xPayout` | int | `5` | Target multiplier (5x, 10x, etc.) |

---

### 9. `currentSidebet` (Sidebet Confirmation) ✅ VERIFIED

**Frequency**: After sidebet placed
**Purpose**: Confirm sidebet is active
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P0
**Category**: SIDEBET_EVENT
**Phases**: ACTIVE

```json
42["currentSidebet",
  {"__trace": true, "traceparent": "00-7de6e8288fe05b8c02ced992bd355f31-c604bdaaa7a74ea0-01"},
  {
    "playerId": "did:privy:cma094vht019il80np6aidhqd",
    "gameId": "20251228-fcb81ff2dd864862",
    "username": "N0m4D",
    "level": 14,
    "price": 0.10082764283248803,
    "betAmount": 0.002,
    "xPayout": 5,
    "coinAddress": "So11111111111111111111111111111111111111112",
    "startTick": 102,
    "endTick": 142,
    "tickIndex": 102,
    "timestamp": 1766897774669,
    "type": "placed"
  }
]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `playerId` | string | `"did:privy:..."` | Player ID |
| `gameId` | string | `"20251228-..."` | Game ID |
| `username` | string | `"N0m4D"` | Display name |
| `level` | int | `14` | Player level |
| `price` | float | `0.1008...` | Price when placed |
| `betAmount` | float | `0.002` | Bet amount (SOL) |
| `xPayout` | int | `5` | Target multiplier |
| `coinAddress` | string | `"So111..."` | Token address |
| `startTick` | int | `102` | Tick when placed |
| `endTick` | int | `142` | Target tick (startTick + 40) |
| `tickIndex` | int | `102` | Current tick |
| `timestamp` | int | `1766897774669` | Server timestamp (ms) |
| `type` | string | `"placed"` | Event type |

---

### 10. `currentSidebetResult` (Sidebet Payout) ✅ VERIFIED

**Frequency**: At rug moment for active sidebets
**Purpose**: Sidebet win/loss notification
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P0
**Category**: SIDEBET_EVENT
**Phases**: RUGGED

```json
42["currentSidebetResult",
  {"__trace": true, "traceparent": "00-f89f16bbd99069674a9a54d709743847-3781631892f7fc03-01"},
  {
    "playerId": "did:privy:cma094vht019il80np6aidhqd",
    "gameId": "20251228-d8d002aba86140ad",
    "username": "N0m4D",
    "type": "payout",
    "betAmount": 0.001,
    "payout": 0.005,
    "profit": 0.004,
    "xPayout": 5,
    "startTick": 264,
    "endTick": 304,
    "tickIndex": 273,
    "price": 0.009250309566210552,
    "coinAddress": "So11111111111111111111111111111111111111112",
    "level": 14,
    "timestamp": 1766892383152
  }
]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `playerId` | string | `"did:privy:..."` | Player ID |
| `gameId` | string | `"20251228-..."` | Game ID |
| `username` | string | `"N0m4D"` | Display name |
| `type` | string | `"payout"` | Result type |
| `betAmount` | float | `0.001` | Original bet |
| `payout` | float | `0.005` | Total payout (bet × xPayout) |
| `profit` | float | `0.004` | Net profit (payout - bet) |
| `xPayout` | int | `5` | Multiplier |
| `startTick` | int | `264` | Tick when placed |
| `endTick` | int | `304` | Target tick |
| `tickIndex` | int | `273` | Tick when rug occurred |
| `price` | float | `0.00925...` | Price at rug |
| `coinAddress` | string | `"So111..."` | Token address |
| `level` | int | `14` | Player level |
| `timestamp` | int | `1766892383152` | Server timestamp |

**Key Insight**: Sidebet WINS when `tickIndex < endTick` (rug before target = WIN)

---

### 11. `success` (ACK Response) ✅ VERIFIED

**Frequency**: After client requests
**Purpose**: Acknowledge request success
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Category**: SYSTEM_ACK
**Phases**: PRESALE, ACTIVE

#### Simple ACK (Trade)
```json
43XX[{"success": true}]
```

#### Sidebet ACK (with full object)
```json
43XXXX[{
  "success": true,
  "message": "Side bet placed",
  "sidebet": {
    "playerId": "did:privy:cma094vht019il80np6aidhqd",
    "gameId": "20251228-fcb81ff2dd864862",
    "username": "N0m4D",
    "level": 14,
    "price": 0.10082764283248803,
    "betAmount": 0.002,
    "xPayout": 5,
    "coinAddress": "So11111111111111111111111111111111111111112",
    "endTick": 142,
    "startTick": 102,
    "tickIndex": 102,
    "timestamp": 1766897774669,
    "type": "placed"
  }
}]
```

#### Empty ACK (follows sidebet ACK)
```json
43XXXY[]
```

---

### 12. `ping` (Heartbeat) ✅ VERIFIED

**Frequency**: Periodic (~30 sec)
**Purpose**: Connection keepalive
**Auth Required**: No
**Scope**: IN_SCOPE
**Priority**: P2
**Category**: SYSTEM_HEARTBEAT
**Phases**: All

```json
42XX["ping", {"lastPing": 169.20000000298023}]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `lastPing` | float | `169.2` | Last measured latency (ms) |

---

### 13. `goldenHourUpdate` (Special Event) ✅ VERIFIED

**Frequency**: During Golden Hour events
**Purpose**: Tournament/lottery state broadcast
**Auth Required**: No
**Scope**: IN_SCOPE (P2)
**Priority**: P2
**Category**: SPECIAL_EVENT
**Phases**: All

```json
42["goldenHourUpdate",
  {"__trace": true, "traceparent": "00-07eba4745daba7416ad40a613c32ea16-c718170afac1254c-01"},
  {
    "status": "ACTIVE",
    "activeEventId": "admin-6825292d-e3ec-4869-8cc9-e8fe3b972718",
    "currentGameIsGolden": true,
    "currentEvent": {...},
    "events": [...],
    "upcomingEvents": []
  }
]
```

#### Root Fields
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `status` | string | `"ACTIVE"` | Event status |
| `activeEventId` | string | `"admin-..."` | Current event ID |
| `currentGameIsGolden` | bool | `true` | Current game counts for Golden Hour |
| `currentEvent` | object | `{...}` | Active event details |
| `events` | array | `[...]` | All scheduled events |
| `upcomingEvents` | array | `[]` | Future events |

#### Event Object Fields
| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"admin-..."` | Event ID |
| `status` | string | `"SCHEDULED"` | Event status |
| `startTime` | string | `"2025-12-28T05:00:00.000Z"` | ISO timestamp |
| `endTime` | string | `"2025-12-28T06:00:00.000Z"` | ISO timestamp |
| `durationMinutes` | int | `60` | Event duration |
| `levelRequired` | int | `20` | Minimum player level |
| `maxEntries` | int | `500` | Max participants |
| `prizeAmount` | float | `0.5` | Prize pool (SOL) |

> **META-LAYER OBSERVATION**: Games during Golden Hour (`currentGameIsGolden: true`) appear to have SHORTER and MORE PREDICTABLE durations, suggesting server-side parameter changes during special events.

---

### 14. Other Events (Lower Priority)

| Event | Auth | Scope | Priority | Category | Description |
|-------|:----:|-------|:--------:|----------|-------------|
| `rugRoyaleUpdate` | No | OUT_OF_SCOPE | P3 | SPECIAL_EVENT | Tournament mode updates |
| `battleEventUpdate` | No | OUT_OF_SCOPE | P3 | SPECIAL_EVENT | Battle mode updates |
| `newChatMessage` | No | OUT_OF_SCOPE | P3 | - | Chat messages |
| `rugPassQuestCompleted` | Yes | OUT_OF_SCOPE | P3 | GAMIFICATION | Quest completion |
| `godCandle50xUpdate` | No | FUTURE | P2 | - | 50x candle celebration |
| `globalSidebets` | No | FUTURE | P2 | - | All active sidebets |
| `goldenHourDrawing` | No | OUT_OF_SCOPE | P3 | SPECIAL_EVENT | Lottery drawing results |

---

## Behavioral Patterns

### Pattern 1: Position Opening Sequence (P0)
**Trigger**: After `cooldownTimer:100`
```
1. gameStatePlayerUpdate  → Position confirmation
2. playerUpdate           → Balance/state sync
3. gameStateUpdate        → tick 0, active:true
```

### Pattern 2: Buy/Sell Flow (P0)
**Trigger**: Buy/Sell button pressed during active game
```
1. buyOrder/sellOrder (42XX)  → Client → Server
2. standard/newTrade (42)     → Server broadcast
3. playerUpdate (42)          → Personal state sync
4. success (43XX)             → ACK
```

### Pattern 3: Sidebet Flow (P0)
**Trigger**: Sidebet button pressed
```
1. requestSidebet (42XXXX)           → Client → Server
2. playerUpdate (42)                 → Balance deducted
3. currentSidebet (42)               → Placement confirmed
4. success (43XXXX) + sidebet object → Full ACK
5. empty ACK (43XXXY[])              → Follows immediately
```

### Pattern 4: Socket.IO ACK Pattern (P1)
```
Request:  42XXXX["eventName", {...}]
Response: 43XXXX[{success: true, ...}]
```
The `43` prefix with matching ID = response to that request.

### Pattern 5: Forced Rug Liquidation (P0)
**Trigger**: Game rugs with open positions
```
Server auto-generates:
1. standard/newTrade (type:"sell") → Forced liquidation
2. playerUpdate                    → positionQty:0, avgCost:0
3. gameStatePlayerUpdate           → Final PnL
```
Position is sold at rug price automatically.

### Pattern 6: Delayed `active:false` (P0)
**Critical Observation**: ~2 second delay after rug
```
Timeline:
22:26:23.274  currentSidebetResult    → Sidebet settles
22:26:23.286  playerUpdate            → Position liquidated
22:26:23.295  standard/newTrade       → Forced sell
22:26:23.449  gameStateUpdate         → STILL active:true!
22:26:25.XXX  gameStateUpdate         → Finally active:false
```
**Implication**: Don't rely on `active:false` for rug detection. Use `rugged:true` or price collapse.

### Pattern 7: Cooldown Timer States (P1)
```
cooldownTimer: 15000  → Just rugged, countdown starts
cooldownTimer: 10000  → allowPreRoundBuys: true (presale opens)
cooldownTimer: 0      → Game starts, active: true
```

### Pattern 8: Position Closed Indicators (P1)
When position fully closed:
```
positionQty: 0
avgCost: 0
hasActiveTrades: true (may still be true briefly)
```

### Pattern 9: Golden Hour Meta-Layer (P2)
**Observation**: Games are SHORTER and MORE PREDICTABLE during Golden Hour.
```
currentGameIsGolden: true → Different rug timing distribution
```
Suggests server-side parameter changes during special events.

---

## Integration Priority

### Priority 1: Verification Layer (Immediate)

| Data Point | Source | Local Equivalent |
|------------|--------|------------------|
| `playerUpdate.cash` | Server | `GameState.balance` |
| `playerUpdate.positionQty` | Server | `Position.amount` |
| `playerUpdate.avgCost` | Server | `Position.entry_price` |
| `leaderboard[me].pnl` | Server | Calculated PnL |

**Implementation**: Compare on every `playerUpdate`, log discrepancies.

### Priority 2: Price History (High)

| Data Point | Source | Use |
|------------|--------|-----|
| `partialPrices.values` | Server | Backfill missed ticks |
| `partialPrices.startTick/endTick` | Server | Continuity verification |

**Implementation**: Fill gaps in local price history.

### Priority 3: Latency Tracking (High)

| Data Point | Source | Use |
|------------|--------|-----|
| `sidebet.timestamp` | Server | Request-to-confirm latency |
| `buyOrder.timestamp` | Server | Trade execution latency |
| `godCandle50xTimestamp` | Server | Event latency |

**Implementation**: `latency = local_receipt_time - server_timestamp`

### Priority 4: Auto-Start (Medium)

| Trigger | Condition |
|---------|-----------|
| Game start | `active: false → true` transition |
| Game end | `rugged: true` or `active: true → false` |
| Player identity | `usernameStatus` received |

**Implementation**: Start recording on game start, stop on rug.

### Priority 5: Rugpool Prediction (Medium)

| Data Point | Use |
|------------|-----|
| `rugpool.rugpoolAmount` | Current pool |
| `rugpool.threshold` | Trigger point |
| Ratio | Alert when approaching |

### Priority 6: Trade Feed (Lower)

| Data Point | Use |
|------------|-----|
| `standard/newTrade` | All player trades |
| Volume analysis | Market activity |
| Whale detection | Large trade alerts |

---

## Files Generated

| File | Purpose |
|------|---------|
| `sandbox/explore_websocket_data.py` | Data collection script |
| `sandbox/websocket_raw_samples.jsonl` | 200 raw samples |
| `sandbox/field_analysis.json` | Field frequency analysis |
| `sandbox/WEBSOCKET_DISCOVERY_REPORT.md` | Initial discovery report |
| `docs/WEBSOCKET_EVENTS_SPEC.md` | This specification |

---

## Next Steps

1. **Extend `_extract_signal()`** in `websocket_feed.py` for Priority 1-3 fields
2. **Add verification hooks** comparing local state to server truth
3. **Implement auto-start** using game state transitions
4. **Add latency dashboard** displaying real-time latency metrics

---

---

## Verification History

| Date | Events Verified | Notes |
|------|-----------------|-------|
| Dec 6, 2025 | `gameStateUpdate` | Initial discovery, 200 samples |
| Dec 9, 2025 | `usernameStatus`, `playerLeaderboardPosition`, `gameStateUpdate` | Live verification, auth requirements confirmed |
| Dec 28, 2025 | `buyOrder`, `requestSidebet`, `currentSidebet`, `currentSidebetResult`, `success`, `ping`, `goldenHourUpdate` | CANONICAL REVIEW session - 10 events, 52+ fields, 9 behavioral patterns. Expanded `playerUpdate`, `gameStatePlayerUpdate`, `standard/newTrade`. Golden Hour live recording (7,000+ events captured). |

---

*Last updated: December 28, 2025 | Version 3.0*

---

## Scope Legend

| Scope | Meaning |
|-------|---------|
| `IN_SCOPE` | Actively implemented and maintained |
| `OUT_OF_SCOPE` | Documented but not implemented (game modes we don't use) |
| `FUTURE` | Planned for future implementation |

## Priority Legend

| Priority | Meaning |
|----------|---------|
| `P0` | Critical - Core trading functionality |
| `P1` | High - Important for full experience |
| `P2` | Medium - Nice to have features |
| `P3` | Low - Out of scope game modes |
