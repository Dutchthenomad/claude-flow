# WebSocket Events Specification
**rugs.fun Socket.IO Protocol** | **Version**: 2.1 | **Date**: December 24, 2025

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
| `currentSidebet` | **YES** | After YOUR sidebet placement |
| `currentSidebetResult` | **YES** | When YOUR sidebet resolves (win/loss) |
| `newSideBet` | No | When ANY player places a sidebet |

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
| `currentSidebet` | ❌ | ✅ | ✅ | ❌ | After YOUR sidebet placement |
| `currentSidebetResult` | ❌ | ❌ | ✅ | ❌ | After 40 ticks from placement |
| `newSideBet` | ❌ | ✅ | ✅ | ❌ | Any player sidebet |
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
**Purpose**: Real-time trade feed
**Auth Required**: No
**Scope**: IN_SCOPE
**Priority**: P1
**Phases**: PRESALE, ACTIVE
**Validated**: December 24, 2025 (empirical capture)

```json
{
  "id": "trade-uuid-here",
  "gameId": "20251224-71c79a83d9074b04",
  "playerId": "did:privy:cm3xxxxxxxxxxxxxx",
  "username": "TraderName",
  "level": 15,
  "type": "buy",
  "qty": 0.001,
  "amount": 0.001,
  "price": 1.234,
  "tickIndex": 42,
  "coin": "solana",
  "leverage": 1,
  "bonusPortion": 0,
  "realPortion": 0.001,
  "timestamp": 1765069123456
}
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"trade-uuid"` | Unique trade identifier |
| `gameId` | string | `"20251224-..."` | Game identifier |
| `playerId` | string | `"did:privy:..."` | Trader's player ID |
| `username` | string | `"TraderName"` | Trader's display name |
| `level` | int | `15` | Trader's level |
| `type` | string | `"buy"` / `"sell"` | Trade direction (lowercase) |
| `qty` | float | `0.001` | Position size (units) |
| `amount` | float | `0.001` | Trade amount (SOL) |
| `price` | float | `1.234` | Execution price |
| `tickIndex` | int | `42` | Tick when executed |
| `coin` | string | `"solana"` | Token type |
| `leverage` | int | `1` | Leverage multiplier (1 = no leverage) |
| `bonusPortion` | float | `0` | Bonus SOL used in trade |
| `realPortion` | float | `0.001` | Real SOL used in trade |
| `timestamp` | int | `1765069123456` | Server timestamp (ms) |

**Use Case**:
- Track all market activity
- Whale trade alerts
- Volume analysis
- ML training data (other players' behavior)
- Leverage position tracking

---

### 4. `playerUpdate` (Personal State Sync) ✅ VERIFIED

**Frequency**: After each of our trades
**Purpose**: Sync local state with server truth
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P0
**Phases**: PRESALE, ACTIVE, RUGGED
**Validated**: December 24, 2025 (empirical capture - 27 fields confirmed)

```json
{
  "id": "did:privy:cmaibr7rt0094jp0mc2mbpfu4",
  "cash": 3.967072345,
  "cumulativePnL": 0.264879755,
  "positionQty": 0.2222919,
  "avgCost": 1.259605046,
  "totalInvested": 0.251352892,
  "pnlPercent": 48.9,
  "authenticated": true,
  "sidebets": [...],
  "sideBet": {...},
  "sidebetPnl": -0.002,
  "shortPosition": null,
  "levelInfo": {...},
  "bonusBalance": 0.05,
  "bonusWagerReq": 0.10,
  "bonusWagered": 0.03,
  "hasInteracted": true,
  "selectedCoin": "solana",
  "autobuysEnabled": false,
  "autosellPrice": null,
  "hitMaxWin": false,
  "leveragedPositions": [],
  "shitcoinBalances": {},
  "role": null,
  "xpBoost": 1.0,
  "crateKeys": 3,
  "recentCrateRewards": []
}
```

#### P0 Fields - Core Trading (Critical)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `cash` | float | `3.967` | **TRUE wallet balance** (SOL) |
| `cumulativePnL` | float | `0.265` | Total PnL this game |
| `positionQty` | float | `0.222` | Current position size |
| `avgCost` | float | `1.26` | Average entry price (VWAP) |
| `totalInvested` | float | `0.251` | Total invested this game |

#### P0 Fields - Sidebet State (Critical)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"did:privy:..."` | Player's DID identity |
| `sidebets` | array | `[{...}]` | **ALL active sidebets** |
| `sideBet` | object/null | `{...}` | Current/most recent sidebet |
| `sidebetPnl` | float | `-0.002` | Cumulative sidebet P&L |

**`sidebets` array structure**:
```json
[
  {
    "gameId": "20251224-71c79a83d9074b04",
    "betAmount": 0.001,
    "xPayout": 5,
    "startTick": 0,
    "endTick": 40
  }
]
```

#### P1 Fields - Trading & Account State (High Priority)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `shortPosition` | object/null | `{qty, avgCost, ...}` | Active short position *(new feature - needs UI integration)* |
| `pnlPercent` | float | `48.9` | Current PnL as percentage |
| `authenticated` | bool | `true` | Wallet connection status |
| `levelInfo` | object | `{...}` | Player level/XP progression |

**`levelInfo` structure**:
```json
{
  "level": 7,
  "xp": 683,
  "xpForNextLevel": 1500,
  "totalXP": 4183
}
```

#### P2 Fields - Medium Priority

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `bonusBalance` | float | `0.05` | Promotional bonus balance (player retention, not used by bots) |
| `bonusWagerReq` | float | `0.10` | Wagering requirement to unlock bonus |
| `bonusWagered` | float | `0.03` | Progress toward bonus unlock |
| `hasInteracted` | bool | `true` | Has placed any trades this session |
| `selectedCoin` | string/null | `"solana"` | Practice token selection (for learning + Rug Royale tournaments) |
| `autobuysEnabled` | bool | `false` | Auto-pilot buy feature (casual players, not used by bots) |
| `autosellPrice` | float/null | `2.5` | Auto-pilot sell trigger (casual players, not used by bots) |
| `hitMaxWin` | bool | `false` | Whether player hit per-game max win cap |
| `leveragedPositions` | array | `[...]` | Active leveraged positions |
| `shitcoinBalances` | object | `{...}` | Practice token balances (for learning + tournaments) |

#### P3 Fields - Gamification (Low Priority)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `role` | string/null | `null` | Admin role (null for regular players) |
| `xpBoost` | float | `1.5` | XP multiplier (promotional) |
| `crateKeys` | int | `3` | Loot crate keys owned |
| `recentCrateRewards` | array | `[...]` | Recent loot crate rewards |

**Use Case**:
- **Critical for verification layer**
- Compare local `balance` calculation vs server `cash`
- Compare local position vs server `positionQty`
- Track sidebet state via `sidebets` array and `sidebetPnl`
- Detect calculation drift

---

### 5. `gameStatePlayerUpdate` (Personal Leaderboard Entry) ✅ VERIFIED

**Frequency**: After each of our trades
**Purpose**: Our leaderboard entry, same structure as `leaderboard[]` items
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Phases**: PRESALE, ACTIVE, RUGGED

Same fields as leaderboard entry above, but specifically for the authenticated player.

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

### 8. `currentSidebet` (Sidebet Placement Confirmation) ✅ VERIFIED

**Frequency**: After YOUR sidebet placement
**Purpose**: Server confirms sidebet was accepted
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Phases**: PRESALE, ACTIVE
**Validated**: December 24, 2025 (19 occurrences in empirical capture)

```json
{
  "playerId": "did:privy:cmaibr7rt0094jp0mc2mbpfu4",
  "gameId": "20251224-71c79a83d9074b04",
  "username": "Dutch",
  "level": 7,
  "price": 1,
  "betAmount": 0.001,
  "xPayout": 5,
  "coinAddress": "So11111111111111111111111111111111111111112",
  "endTick": 40,
  "startTick": 0,
  "tickIndex": 0,
  "timestamp": 1766591720857,
  "type": "placed"
}
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `playerId` | string | `"did:privy:..."` | Your player DID |
| `gameId` | string | `"20251224-..."` | Current game |
| `username` | string | `"Dutch"` | Your username |
| `level` | int | `7` | Your level |
| `betAmount` | float | `0.001` | SOL wagered |
| `xPayout` | int | `5` | Always 5x multiplier |
| `price` | float | `1.0` | Price when placed |
| `coinAddress` | string | `"So111..."` | Token address |
| `startTick` | int | `0` | Sidebet window start |
| `endTick` | int | `40` | Sidebet window end (startTick + 40) |
| `tickIndex` | int | `0` | Current tick when placed |
| `timestamp` | int | `1766591720857` | Server timestamp (ms) |
| `type` | string | `"placed"` | Always "placed" for confirmations |

**Use Case**:
- Confirm sidebet placement was accepted by server
- Track sidebet window (startTick → endTick)
- Bot action confirmation loop
- Latency measurement

---

### 9. `currentSidebetResult` (Sidebet Resolution) ✅ VERIFIED

**Frequency**: ~13-14 seconds after placement (40 ticks)
**Purpose**: Server reports sidebet win/loss and payout
**Auth Required**: Yes
**Scope**: IN_SCOPE
**Priority**: P1
**Phases**: ACTIVE
**Validated**: December 24, 2025 (19 occurrences in empirical capture)

```json
{
  "playerId": "did:privy:cmaibr7rt0094jp0mc2mbpfu4",
  "gameId": "20251224-71c79a83d9074b04",
  "username": "Dutch",
  "level": 7,
  "betAmount": 0.001,
  "payout": 0.005,
  "profit": 0.004,
  "xPayout": 5,
  "coinAddress": "So11111111111111111111111111111111111111112",
  "endTick": 40,
  "startTick": 0,
  "tickIndex": 28,
  "price": 0.0196566440891481,
  "timestamp": 1766591734291,
  "type": "payout"
}
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `payout` | float | `0.005` | Total returned (5x bet on win, 0 on loss) |
| `profit` | float | `0.004` | Net profit (payout - betAmount) |
| `tickIndex` | int | `28` | Tick when resolved |
| `price` | float | `0.0196...` | Price at resolution tick |
| `type` | string | `"payout"` | Always "payout" for results |
| *(+ all fields from `currentSidebet`)* | | | |

**Latency Observed**:
- Placement → Result: ~13-14 seconds (40 ticks × ~250ms + processing)

**Use Case**:
- Accurate sidebet P&L tracking
- Win/loss determination
- Reward calculation for RL training

---

### 10. `newSideBet` (Other Players' Sidebets) ✅ VERIFIED

**Frequency**: When ANY player places a sidebet
**Purpose**: Broadcast sidebet activity to all clients
**Auth Required**: No
**Scope**: IN_SCOPE
**Priority**: P2
**Phases**: PRESALE, ACTIVE
**Validated**: December 24, 2025 (34 occurrences in empirical capture)

```json
{
  "playerId": "did:privy:cmfoi1a3m007ol80b8hts2atu",
  "gameId": "20251224-d1e99a53500244e1",
  "username": "B31",
  "level": 35,
  "price": 0.06206866697682252,
  "betAmount": 0.01,
  "xPayout": 5,
  "coinAddress": "So11111111111111111111111111111111111111112",
  "endTick": 326,
  "startTick": 286,
  "tickIndex": 286,
  "timestamp": 1766591654448,
  "type": "placed"
}
```

Same fields as `currentSidebet` but for other players.

**Use Case**:
- Track sidebet volume/sentiment in real-time
- Potential signal: high sidebet activity = market confidence
- Analytics for strategy development

---

### 11. Other Events

Events documented but currently lower priority for implementation:

| Event | Auth | Scope | Priority | Phases | Description |
|-------|:----:|-------|:--------:|--------|-------------|
| `rugRoyaleUpdate` | No | OUT_OF_SCOPE | P3 | All | Tournament mode updates |
| `battleEventUpdate` | No | OUT_OF_SCOPE | P3 | All | Battle mode updates |
| `newChatMessage` | No | OUT_OF_SCOPE | P3 | All | Chat messages |
| `godCandle50xUpdate` | No | FUTURE | P2 | ACTIVE | 50x candle celebration |
| `globalSidebets` | No | FUTURE | P2 | ACTIVE | All active sidebets |
| `goldenHourUpdate` | No | OUT_OF_SCOPE | P3 | All | Lottery event updates |
| `goldenHourDrawing` | No | OUT_OF_SCOPE | P3 | All | Lottery drawing results |
| `sidebetEventUpdate` | No | OUT_OF_SCOPE | P3 | All | Sidebet tournament scheduling 🔬 |
| `pinpointPartyEventUpdate` | No | OUT_OF_SCOPE | P3 | All | Unknown game mode (investigate) 🔬 |
| `diddyPartyUpdate` | No | OUT_OF_SCOPE | P3 | All | Unknown game mode (investigate) 🔬 |
| `getLeaderboard` | No | OUT_OF_SCOPE | P3 | All | Client→Server leaderboard request 🔬 |
| `getPlayerLeaderboardPosition` | No | OUT_OF_SCOPE | P3 | All | Client→Server rank request 🔬 |
| `leaderboardData` | No | OUT_OF_SCOPE | P3 | All | Server→Client leaderboard response 🔬 |
| `rugpassQuestCompleted` | Yes | OUT_OF_SCOPE | P3 | All | Quest completion notification |

**🔬 = Flagged for future research** (post-core-bot deployment):
- **Game mode events**: Potential expanded profit opportunities (sidebet tournaments, parties)
- **Leaderboard events**: Higher-order ML/RL features from player behavior analytics

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
| Dec 24, 2025 | `currentSidebet`, `currentSidebetResult`, `newSideBet` | Sidebet events CANONICAL (23,194 events, 11 games) |
| Dec 24, 2025 | `playerUpdate` (22 new fields) | Expanded from 5→27 fields |
| Dec 24, 2025 | `standard/newTrade` (14 fields) | Complete field enumeration |
| Dec 24, 2025 | 7 OUT_OF_SCOPE events | Game modes + leaderboard queries |

---

*Last updated: December 24, 2025 | Version 2.1*

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
