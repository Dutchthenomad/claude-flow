# Questions 3 & 4: Closing Position / Rug Sequence

**Date**: 2025-12-28
**Session**: WebSocket Documentation Enhancement
**Status**: OBSERVED (pending canonical review)

---

## Question Context

The agent identified 4 position transition cases that must be handled:

3. **Partial sell (positive → less positive)**: Keep entry_tick
4. **Closing position (positive → 0)**: Reset entry_tick = None

This document captures the complete rug sequence including:
- Active position + sidebet during rug
- Sidebet payout calculation
- Forced position liquidation
- Game state transition to cooldown

---

## Scenario Description

Player "N0m4D" had:
- Active trade position (0.002273142 SOL @ avgCost 0.879838878)
- Active sidebet (placed at tick 264, target 304x, xPayout 5)
- Game rugged at tick 273, price 0.009250309566210552

**Outcome**:
- Sidebet WON (type: "payout") - paid 0.005 SOL (5x on 0.001 bet)
- Position FORCED SOLD at rug price
- Net PnL: +0.00102 SOL (+25.5%)

---

## Complete Event Sequence Timeline

| Time | Event | Length | Description |
|------|-------|--------|-------------|
| 22:26:23.018 | `gameStateUpdate` | 4368 | Pre-rug state (tick 272, price 0.72x) |
| 22:26:23.029 | `gameStatePlayerUpdate` | - | Player position + active sidebet |
| 22:26:23.274 | `currentSidebetResult` | - | **NEW** - Sidebet payout (WON!) |
| 22:26:23.286 | `playerUpdate` | - | Balance update |
| 22:26:23.295 | `standard/newTrade` | - | **FORCED SELL** at rug price |
| 22:26:23.295 | `playerUpdate` | - | Post-sell balance |
| 22:26:23.305 | `gameStatePlayerUpdate` | - | Position update |
| 22:26:23.309 | `rugPassQuestCompleted` | - | **NEW** - Quest completion |
| 22:26:23.449 | `gameStateUpdate` | - | Still active:true! |
| 22:26:23.449 | `gameStatePlayerUpdate` | - | Position update |
| 22:26:24.456 | `4358[]` | - | Empty ACK |
| 22:26:24.605 | `playerUpdate` | - | Balance sync |
| 22:26:24.456 | `ping` | - | Client ping (latency 169ms) |
| ~22:26:24.7 | `gameStateUpdate` | - | Still active:true |
| ~22:26:24.8 | `gameStatePlayerUpdate` | - | Final closed state (positionQty: 0) |
| ~22:26:25.0 | `gameStateUpdate` | - | **FINALLY** active:false, cooldown:15000 |

**Key Insight**: ~2 seconds elapsed from rug (tick 273) to active:false emission!

---

## Raw Event Examples

### Event 1: gameStateUpdate (PRE-RUG - 22:26:23.018)

```json
42["gameStateUpdate", {
  "active": true,
  "price": 0.7205941557633537,
  "rugged": false,
  "tickCount": 272,
  "cooldownTimer": 0,
  "cooldownPaused": false,
  "allowPreRoundBuys": false,
  "connectedPlayers": 205,
  "gameId": "20251228-d8d002aba86140ad",
  "averageMultiplier": 3.378798635001477,
  "count2x": 46,
  "count10x": 5,
  "count50x": 0,
  "count100x": 0,
  "tradeCount": 428,
  "leaderboard": [...],
  "partialPrices": {
    "startTick": 268,
    "endTick": 272
  },
  "pauseMessage": "",
  "provablyFair": {
    "serverSeedHash": "6f67e582cc3f4de0f4a0670975b94772a8f81603e2191aae8615bfabd9f3cfe3",
    "version": "v3"
  },
  "rugRoyale": {
    "status": "INACTIVE",
    "activeEventId": null,
    "currentEvent": null,
    "upcomingEvents": [],
    "events": []
  },
  "rugpool": {
    "instarugCount": 0,
    "threshold": 10,
    "rugpoolAmount": 0
  }
}]
```

### Event 2: gameStatePlayerUpdate (WITH ACTIVE SIDEBET - 22:26:23.029)

```json
42["gameStatePlayerUpdate", {
  "gameId": "20251228-d8d002aba86140ad",
  "leaderboardEntry": {
    "id": "did:privy:cma094vht019il80np6aidhqd",
    "username": "N0m4D",
    "level": 14,
    "pnl": -0.001345501,
    "pnlPercent": -33.637525000000004,
    "avgCost": 0.879838878,
    "hasActiveTrades": true,
    "position": 30,
    "positionQty": 0.002273142,
    "regularPnl": -0.000345501,
    "selectedCoin": null,
    "shortPnl": 0,
    "shortPosition": null,
    "sideBet": {
      "startedAtTick": 264,
      "gameId": "20251228-d8d002aba86140ad",
      "end": 304,
      "betAmount": 0.001,
      "xPayout": 5
    },
    "sidebetActive": true,
    "sidebetPnl": -0.001,
    "totalInvested": 0.004,
    "username": "N0m4D"
  }
}]
```

**Note**: `sidebetPnl: -0.001` (shows bet as lost BEFORE payout calculated)

### Event 3: currentSidebetResult (NEW EVENT - 22:26:23.274)

**Direction**: Server → Client
**Purpose**: Sidebet payout/loss notification
**Category**: SIDEBET_EVENT

```json
42["currentSidebetResult", {
  "__trace": true,
  "traceparent": "00-f89f16bbd99069674a9a54d709743847-3781631892f7fc03-01"
}, {
  "playerId": "did:privy:cma094vht019il80np6aidhqd",
  "gameId": "20251228-d8d002aba86140ad",
  "username": "N0m4D",
  "level": 14,
  "betAmount": 0.001,
  "coinAddress": "So11111111111111111111111111111111111111112",
  "startTick": 264,
  "endTick": 304,
  "tickIndex": 273,
  "price": 0.009250309566210552,
  "payout": 0.005,
  "profit": 0.004,
  "xPayout": 5,
  "type": "payout",
  "timestamp": 1766892383152
}]
```

**Key Fields**:
- `type`: "payout" (won) or likely "loss" (lost)
- `payout`: Total received (0.005 = 5x multiplier)
- `profit`: Net profit (0.004 = payout - betAmount)
- `endTick`: Target tick (304)
- `tickIndex`: Actual end tick (273 - rug happened before target)

**Sidebet Logic Insight**: Sidebet WON because game rugged BEFORE reaching target (304x). The sidebet bets the game will survive to endTick - if it rugs before, sidebet wins!

### Event 4: gameStatePlayerUpdate (FINAL CLOSED STATE)

```json
42["gameStatePlayerUpdate", {
  "gameId": "20251228-d8d002aba86140ad",
  "leaderboardEntry": {
    "id": "did:privy:cma094vht019il80np6aidhqd",
    "username": "N0m4D",
    "level": 14,
    "pnl": 0.0010210280000000002,
    "pnlPercent": 25.525700000000008,
    "avgCost": 0,
    "hasActiveTrades": true,
    "position": 25,
    "positionQty": 0,
    "regularPnl": -0.001978972,
    "selectedCoin": null,
    "shortPnl": 0,
    "shortPosition": null,
    "sideBet": null,
    "sidebetActive": null,
    "sidebetPnl": 0.003,
    "totalInvested": 0.004,
    "username": "N0m4D"
  }
}]
```

**Position Closed Indicators**:
- `positionQty`: 0 (no position)
- `avgCost`: 0 (reset)
- `sideBet`: null (settled)
- `sidebetActive`: null (settled)

**Final PnL Breakdown**:
- `regularPnl`: -0.001978972 (lost on main trade)
- `sidebetPnl`: 0.003 (profit from sidebet = 0.004 profit, but shown as 0.003?)
- `pnl`: 0.00102 (total = regularPnl + sidebetPnl + fees?)

### Event 5: gameStateUpdate (GAME END - active:false)

```json
42["gameStateUpdate", {
  "active": false,
  "price": 1,
  "rugged": false,
  "tickCount": 0,
  "cooldownTimer": 15000,
  "cooldownPaused": false,
  "allowPreRoundBuys": false,
  "connectedPlayers": 204,
  "gameId": "20251228-d03603c83ac04266",
  "gameVersion": "v3",
  "averageMultiplier": 3.373611953517094,
  "count2x": 46,
  "count10x": 5,
  "count50x": 0,
  "count100x": 0,
  "gameHistory": [
    {
      "id": "20251228-d8d002aba86140ad",
      "timestamp": 1766892383603
    }
  ],
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
  "godCandle50xTimestamp": null,
  "highestToday": 1329.9752646165282,
  "highestTodayPrices": [1, 1.0232511670978457, 1.0084532485837796, ...],
  "highestTodayTimestamp": 1766855639499,
  "availableShitcoins": [
    {
      "address": "0xPractice",
      "ticker": "FREE",
      "name": "Practice SOL",
      "max_bet": 10000,
      "max_win": 100000
    }
  ],
  "leaderboard": [...],
  "partialPrices": {
    "startTick": 0,
    "endTick": 0,
    "values": {"0": 1}
  },
  "pauseMessage": "",
  "provablyFair": {
    "serverSeedHash": "45c89bd5f01735ffc9c91fc5808ff54ec4b7338fd91f06191c58d7b0f45904e3",
    "version": "v3"
  }
}]
```

**Cooldown Behavior**:
- Starts at `cooldownTimer: 15000` (15 seconds)
- `allowPreRoundBuys: false` until cooldown reaches 10000
- At 10000, flips to `allowPreRoundBuys: true`

---

## Complete Findings Summary

### NEW EVENT TYPES DISCOVERED

#### 1. currentSidebetResult (Server → Client)

**Direction**: Incoming
**Purpose**: Sidebet outcome notification
**Category**: SIDEBET_EVENT
**Priority**: P0 (critical for sidebet tracking)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `playerId` | string | `"did:privy:..."` | Player DID |
| `gameId` | string | `"20251228-..."` | Game identifier |
| `username` | string | `"N0m4D"` | Display name |
| `level` | int | `14` | Player level |
| `betAmount` | number | `0.001` | Original bet (SOL) |
| `coinAddress` | string | `"So11...112"` | Token address |
| `startTick` | int | `264` | Tick when bet placed |
| `endTick` | int | `304` | Target survival tick |
| `tickIndex` | int | `273` | Actual end tick |
| `price` | number | `0.00925...` | Price at settlement |
| `payout` | number | `0.005` | Total payout (SOL) |
| `profit` | number | `0.004` | Net profit (SOL) |
| `xPayout` | int | `5` | Multiplier |
| `type` | string | `"payout"` | Outcome type |
| `timestamp` | int | `1766892383152` | Unix ms |
| `__trace` | bool | `true` | Tracing enabled |
| `traceparent` | string | `"00-..."` | Trace ID |

**Sidebet Win Condition**: Game rugs BEFORE `endTick` → sidebet WINS

#### 2. rugPassQuestCompleted (Server → Client)

**Direction**: Incoming
**Purpose**: Quest/achievement completion notification
**Category**: GAMIFICATION_EVENT
**Priority**: P3 (OUT_OF_SCOPE for trading)

*Note: No field data captured - likely contains quest details*

#### 3. ping (Client → Server)

**Direction**: Outgoing
**Purpose**: Latency measurement / keepalive
**Category**: SYSTEM_HEARTBEAT

```json
4259["ping", {
  "lastPing": 169.20000000298023
}]
```

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `lastPing` | number | `169.2` | Previous ping latency (ms) |

---

### NEW FIELDS IN EXISTING EVENTS

#### gameStateUpdate - New Fields

| Field | Type | Example | Priority | Description |
|-------|------|---------|:--------:|-------------|
| `tradeCount` | int | `428` | P2 | Total trades this game |
| `rugRoyale` | object | `{...}` | P2 | Tournament event state |
| `rugRoyale.status` | string | `"INACTIVE"` | P2 | Tournament status |
| `rugRoyale.activeEventId` | null/string | `null` | P2 | Current event ID |
| `rugRoyale.currentEvent` | null/object | `null` | P2 | Current event details |
| `rugRoyale.upcomingEvents` | array | `[]` | P2 | Scheduled events |
| `rugRoyale.events` | array | `[]` | P2 | Event history |
| `availableShitcoins` | array | `[{...}]` | P1 | Available alt tokens |
| `availableShitcoins[].address` | string | `"0xPractice"` | P1 | Token address |
| `availableShitcoins[].ticker` | string | `"FREE"` | P1 | Token symbol |
| `availableShitcoins[].name` | string | `"Practice SOL"` | P1 | Token name |
| `availableShitcoins[].max_bet` | int | `10000` | P1 | Max bet limit |
| `availableShitcoins[].max_win` | int | `100000` | P1 | Max win limit |
| `highestTodayPrices` | array | `[1, 1.02, ...]` | P2 | Price history of daily high |

---

### CRITICAL BEHAVIORAL DISCOVERIES

#### 1. Rug Sequence (FORCED LIQUIDATION)

When game rugs, server FORCES all positions closed:

```
Tick 272: price = 0.72x, active = true
Tick 273: RUG DETECTED (price = 0.00925x)
   ↓
Server broadcasts:
1. currentSidebetResult (settles all sidebets)
2. standard/newTrade (FORCED SELL for each player)
3. playerUpdate (balance adjustments)
4. gameStatePlayerUpdate (position = 0)
   ↓
~2 seconds later:
5. gameStateUpdate (active = false, cooldown = 15000)
```

**Key Insight**: Players do NOT need to send sellOrder - server auto-liquidates!

#### 2. Delayed active:false Emission

**Discovery**: Multiple `gameStateUpdate` events fire with `active: true` AFTER rug before finally emitting `active: false`.

**Timeline**:
- 22:26:23.274: Rug (sidebet settled)
- 22:26:23.449: gameStateUpdate (active: true still!)
- 22:26:24.7: gameStateUpdate (active: true still!)
- 22:26:25.0: gameStateUpdate (active: false finally)

**Implication**: Cannot rely on `active: false` for rug detection. Must monitor price drops!

#### 3. Cooldown Timer Behavior

| Timer Value | State |
|:-----------:|-------|
| 15000 | Cooldown starts, `allowPreRoundBuys: false` |
| 14000-10001 | Countdown, `allowPreRoundBuys: false` |
| 10000 | Flips to `allowPreRoundBuys: true` |
| 9999-1 | Presale open |
| 0 | Game starts (tick 0) |

#### 4. Position Closed Indicators

When position is fully closed (rug or manual sell):
- `positionQty`: 0
- `avgCost`: 0 (reset)
- `sideBet`: null
- `sidebetActive`: null

Bot should check: `positionQty === 0 && avgCost === 0`

#### 5. Sidebet Win Logic CONFIRMED

**Hypothesis Confirmed**: Sidebet bets on game rugging BEFORE target tick.

```
startTick: 264 (when bet placed)
endTick: 304 (target - game must survive to here for sidebet to LOSE)
tickIndex: 273 (when rug happened)

273 < 304 → Game rugged BEFORE target → Sidebet WINS
```

**Payout**: `betAmount * xPayout = 0.001 * 5 = 0.005 SOL`

---

### PNL BREAKDOWN ANALYSIS

**Before Rug** (tick 272):
```
regularPnl: -0.000345501 (main trade losing)
sidebetPnl: -0.001 (sidebet counted as lost - not yet settled)
pnl: -0.001345501 (total loss shown)
```

**After Rug** (settled):
```
regularPnl: -0.001978972 (main trade final loss)
sidebetPnl: 0.003 (sidebet profit after settlement)
pnl: 0.00102 (net profit!)
```

**Calculation**:
```
Main trade loss: -0.001978972 (bought high, sold at rug price)
Sidebet profit:  +0.003 (payout 0.005 - bet 0.001 - house edge?)
Net PnL:         +0.00102
```

**Question**: Why is sidebetPnl 0.003 when profit was 0.004? Possible fee or rounding.

---

### EVENT CATEGORY CLASSIFICATION

| Category | Events | Direction |
|----------|--------|-----------|
| TRADING_ACTION | `buyOrder`, `sellOrder` | Client → Server |
| TRADING_EVENT | `standard/newTrade` | Server → Client (broadcast) |
| SIDEBET_EVENT | `currentSidebetResult` | Server → Client |
| PLAYER_STATE | `playerUpdate`, `gameStatePlayerUpdate` | Server → Client |
| GAME_STATE | `gameStateUpdate` | Server → Client (broadcast) |
| GAMIFICATION | `rugPassQuestCompleted` | Server → Client |
| SYSTEM_HEARTBEAT | `ping` | Client → Server |
| SYSTEM_ACK | `success`, `4358[]` | Server → Client |

---

## Summary of Undocumented Elements

### New Event Types: 3

| Event | Direction | Priority |
|-------|-----------|:--------:|
| `currentSidebetResult` | Server → Client | P0 |
| `rugPassQuestCompleted` | Server → Client | P3 |
| `ping` | Client → Server | P2 |

### New Fields: 17

| Category | Field Count | Priority |
|----------|:-----------:|:--------:|
| gameStateUpdate - tradeCount | 1 | P2 |
| gameStateUpdate - rugRoyale | 6 | P2 |
| gameStateUpdate - availableShitcoins | 5 | P1 |
| gameStateUpdate - highestTodayPrices | 1 | P2 |
| currentSidebetResult - all fields | 17 | P0 |

### Behavioral Patterns: 5

1. **Forced liquidation sequence** (rug auto-sells all positions)
2. **Delayed active:false** (~2 sec after rug)
3. **Cooldown timer states** (15000 → 10000 allowPreRound → 0 start)
4. **Position closed indicators** (qty=0, avgCost=0)
5. **Sidebet win logic** (rug before target = WIN)

---

## Open Questions

1. **sidebetPnl discrepancy**: Why 0.003 shown when profit was 0.004?
2. **rugPassQuestCompleted fields**: What data does this event contain?
3. **rugRoyale mechanics**: How do tournaments work?
4. **Rug detection**: Best way to detect rug without waiting for active:false?
5. **Forced sell price**: Is the rug price deterministic or random?

---

## Rug Detection Strategy (RECOMMENDATION)

Since `active: false` is delayed ~2 seconds after rug:

```python
def detect_rug(current_price, previous_price, threshold=0.5):
    """
    Detect rug by price drop, not by active flag.

    A >50% drop in one tick strongly indicates rug.
    """
    if previous_price > 0:
        drop_percent = (previous_price - current_price) / previous_price
        if drop_percent > threshold:
            return True
    return False
```

Or monitor for `currentSidebetResult` with `type: "payout"` - this fires immediately on rug.

---

## Next Steps

- [ ] Prepare staging plan for canonical review
- [ ] Create event category taxonomy
- [ ] Generate field inventory across all events
- [ ] Prioritize P0 fields for immediate documentation
