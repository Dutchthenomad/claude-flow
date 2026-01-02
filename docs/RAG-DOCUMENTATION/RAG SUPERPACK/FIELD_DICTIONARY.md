# WebSocket Event Field Dictionary

**Source**: Reviewed from VECTRA-PLAYER data dictionaries + canonical spec
**Created**: December 18, 2025
**Status**: Active - rugs-expert validated

---

## gameStateUpdate Fields

### Core State (P0)

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.gameId` | string | - | Unique identifier for current game session (format: YYYYMMDD-uuid) |
| `$.data.active` | boolean | - | Whether game is currently in progress (trading enabled) |
| `$.data.rugged` | boolean | - | Whether game has ended via rug pull event |
| `$.data.price` | number | multiplier | Current token multiplier (entry price = 1.0) |
| `$.data.tickCount` | number | ticks | Number of ticks elapsed since game start (~4 ticks/sec) |
| `$.data.gameVersion` | string | - | Game protocol version (currently "v3") |

### Phase Indicators

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.cooldownTimer` | number | milliseconds | Milliseconds remaining until next game starts (0 = active/presale) |
| `$.data.allowPreRoundBuys` | boolean | - | Whether presale phase is active (pre-game trading) |
| `$.data.cooldownPaused` | boolean | - | Whether cooldown timer is paused by admin |
| `$.data.pauseMessage` | string | - | Admin message explaining why cooldown is paused |

### Leaderboard (Server-Authoritative)

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.leaderboard[*].id` | string | - | Player's unique Privy DID identifier |
| `$.data.leaderboard[*].username` | string | - | Player's display name |
| `$.data.leaderboard[*].pnl` | number | SOL | Server-authoritative profit/loss for current game |
| `$.data.leaderboard[*].regularPnl` | number | SOL | PnL from regular trading (excludes sidebets/shorts) |
| `$.data.leaderboard[*].positionQty` | number | units | Current position size in token units |
| `$.data.leaderboard[*].avgCost` | number | multiplier | Average entry price (weighted by position size) |
| `$.data.leaderboard[*].hasActiveTrades` | boolean | - | Whether player has open position |
| `$.data.leaderboard[*].totalInvested` | number | SOL | Total SOL committed to current position |
| `$.data.leaderboard[*].position` | number | rank | Leaderboard rank (1 = highest PnL) |
| `$.data.leaderboard[*].pnlPercent` | number | percent | PnL as percentage of total invested |
| `$.data.leaderboard[*].sidebetPnl` | number | SOL | PnL from sidebet lottery system |
| `$.data.leaderboard[*].sidebetActive` | boolean | - | Whether player has active sidebet |
| `$.data.leaderboard[*].level` | number | level | Player's account level (experience points) |

### Partial Prices (Rolling Window)

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.partialPrices.startTick` | number | ticks | First tick in rolling price history window |
| `$.data.partialPrices.endTick` | number | ticks | Last tick in rolling price history window |
| `$.data.partialPrices.values.{key}` | number | multiplier | Price at specific tick (key = tick number) |

### Statistics

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.connectedPlayers` | number | count | Number of active WebSocket connections |
| `$.data.averageMultiplier` | number | multiplier | Mean rug point across recent games (session average) |
| `$.data.count2x` | number | count | Number of games reaching 2x multiplier this session |
| `$.data.count10x` | number | count | Number of games reaching 10x multiplier this session |
| `$.data.count50x` | number | count | Number of games reaching 50x multiplier this session |
| `$.data.count100x` | number | count | Number of games reaching 100x multiplier this session |
| `$.data.highestToday` | number | multiplier | Highest multiplier achieved today (daily record) |
| `$.data.highestTodayTimestamp` | number | unix_ms | When the daily high was achieved |

### Game History (ML Gold Mine)

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.gameHistory[*].id` | string | - | Game ID of completed game in rolling history |
| `$.data.gameHistory[*].timestamp` | number | unix_ms | When game ended (rug event timestamp) |
| `$.data.gameHistory[*].rugged` | boolean | - | Always true (history only contains completed games) |
| `$.data.gameHistory[*].peakMultiplier` | number | multiplier | Highest price reached before rug |
| `$.data.gameHistory[*].prices[*]` | number | multiplier | Tick-by-tick price history for completed game |
| `$.data.gameHistory[*].gameVersion` | string | - | Protocol version for historical game |
| `$.data.gameHistory[*].globalTrades[*]` | object | - | All player trades from that game |
| `$.data.gameHistory[*].globalSidebets[*]` | object | - | All sidebets from that game |
| `$.data.gameHistory[*].provablyFair` | object | - | Server seed + hash for verification |

### Provably Fair

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.provablyFair.serverSeedHash` | string | hex | SHA-256 hash of server seed (pre-reveal) |
| `$.data.provablyFair.version` | string | - | Provably fair protocol version |

---

## playerUpdate Fields

Server-authoritative state for authenticated player.

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `cash` | number | SOL | TRUE wallet balance |
| `cumulativePnL` | number | SOL | Total PnL this game |
| `positionQty` | number | units | Current position size |
| `avgCost` | number | multiplier | Average entry price |
| `totalInvested` | number | SOL | Total SOL invested this game |

---

## gameStatePlayerUpdate Fields

Our entry from the leaderboard (authenticated player only).

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `id` | string | - | Our Privy DID |
| `username` | string | - | Our display name |
| `pnl` | number | SOL | Our profit/loss this game |
| `position` | number | rank | Our leaderboard position |
| `positionQty` | number | units | Our current position size |
| `avgCost` | number | multiplier | Our average entry price |
| `hasActiveTrades` | boolean | - | Whether we have open position |

---

## Scope Legend

| Scope | Meaning |
|-------|---------|
| **IN_SCOPE** | Actively used in REPLAYER/bot |
| **OUT_OF_SCOPE** | Exists but not currently used |
| **FUTURE** | Planned for future integration |

---

## Group Categories

| Group | Purpose |
|-------|---------|
| `core_state` | Essential game state tracking |
| `phase_indicator` | Game phase detection |
| `leaderboard` | Player rankings and verification |
| `trading` | Price and position data |
| `statistics` | Session/daily aggregates |
| `game_history` | Completed game archives (ML training) |

---

*Generated by rugs-expert agent from VECTRA-PLAYER data dictionaries*
