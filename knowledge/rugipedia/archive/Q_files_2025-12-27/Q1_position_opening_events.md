# Question 1: Position Opening Events (0 → Positive)

**Date**: 2025-12-27
**Session**: WebSocket Documentation Enhancement
**Status**: OBSERVED (pending canonical review)

---

## Question Context

The agent identified 4 position transition cases that must be handled:

1. **Opening position (0 → positive)**: Record entry_tick = current_tick

This document captures the exact WebSocket events that fire when a player opens a position during presale, including a main trade and sidebet.

---

## Event Sequence Discovered

**Trigger**: After `coolDownTimer` transitions from 200 → 100 → 0

**Order**:
1. `gameStatePlayerUpdate` - Personal state with new position
2. `playerUpdate` - Server-authoritative balance sync
3. `gameStateUpdate` - Global state (tick 0)

---

## Raw Event Examples

### Event 1: gameStatePlayerUpdate (between coolDownTimer:200 and coolDownTimer:100)

```json
42["gameStatePlayerUpdate", {
  "gameId": "20251227-65bd74ba1bc54708",
  "leaderboardEntry": {
    "id": "did:privy:cma094vht019il80np6aidhqd",
    "username": "N0m4D",
    "level": 14,
    "pnl": 0,
    "pnlPercent": 0,
    "avgCost": 1,
    "hasActiveTrades": true,
    "position": 39,
    "positionQty": 0.001,
    "selectedCoin": null,
    "shortPosition": null,
    "sideBet": {
      "startedAtTick": 0,
      "gameId": "20251227-65bd74ba1bc54708",
      "end": 40,
      "betAmount": 0.001,
      "xPayout": 5,
      "bonusPortion": 0,
      "coinAddress": "So11111111111111111111111111111111111111112",
      "realPortion": 0.001
    },
    "sidebetActive": true,
    "totalInvested": 0.002,
    "username": "N0m4D"
  },
  "rugpool": {
    "instarugCount": 3,
    "rugpoolAmount": 2.1897343695,
    "totalEntries": 8270,
    "threshold": 10
  }
}]
```

### Event 2: playerUpdate

```json
42["playerUpdate", {
  "id": "did:privy:cma094vht019il80np6aidhqd",
  "role": null,
  "cash": 0.097595869,
  "bonusBalance": 0,
  "authenticated": true,
  "autobuysEnabled": false,
  "autosellPrice": null,
  "avgCost": 1,
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
  "cumulativePnL": 0,
  "hasInteracted": true,
  "hitMaxWin": false,
  "levelInfo": {
    "level": 14,
    "xp": 1953,
    "xpForNextLevel": 5000,
    "totalXP": 31953
  },
  "leveragedPositions": [],
  "pnlPercent": -99.3217,
  "positionQty": 0.001,
  "recentCrateRewards": [],
  "selectedCoin": null,
  "shitcoinBalances": {
    "0xPractice": 100
  },
  "shortPosition": null,
  "sideBet": {
    "startedAtTick": 0,
    "gameId": "20251227-65bd74ba1bc54708",
    "end": 40,
    "betAmount": 0.001,
    "xPayout": 5,
    "bonusPortion": 0,
    "coinAddress": "So11111111111111111111111111111111111111112",
    "realPortion": 0.001
  },
  "sidebetPnl": 0,
  "sidebets": [],
  "totalInvested": 0.002,
  "xpBoost": {
    "active": false,
    "activeUntil": 0,
    "available": 0
  }
}]
```

### Event 3: gameStateUpdate (tick 0)

```json
42["gameStateUpdate", {
  "active": true,
  "price": 1,
  "rugged": false,
  "tickCount": 0,
  "cooldownTimer": 0,
  "cooldownPaused": false,
  "allowPreRoundBuys": false,
  "connectedPlayers": 244,
  "gameId": "20251227-65bd74ba1bc54708",
  "gameVersion": "v3",
  "leaderboard": [],
  "partialPrices": {
    "startTick": 0,
    "endTick": 0,
    "values": {
      "0": 1
    }
  },
  "pauseMessage": "",
  "provablyFair": {
    "serverSeedHash": "d74b42aabdce7c6d8aaea9d23aa3453a55ed7b1b19d8ebd0e1380178b7dc12ae",
    "version": "v3"
  }
}]
```

---

## Complete Findings Summary

### Total Undocumented Elements

| Category | Count |
|----------|:-----:|
| New Fields | 37 |
| Structure Corrections | 1 |
| Behavioral Patterns | 1 |

---

### 1. gameStatePlayerUpdate Findings

#### Structure Correction Required

**Current Spec (Line 605)**: "Same fields as leaderboard entry above"

**Actual Structure**: Container object with:
- `gameId` (string) - Current game identifier
- `leaderboardEntry` (object) - Player's leaderboard entry
- `rugpool` (object) - Rugpool lottery state

#### New Fields Discovered

| Field Path | Type | Example | Priority |
|------------|------|---------|:--------:|
| `gameId` | string | `"20251227-65bd74ba1bc54708"` | P1 |
| `rugpool.totalEntries` | int | `8270` | P3 |
| `leaderboardEntry.sideBet.bonusPortion` | number | `0` | P1 |
| `leaderboardEntry.sideBet.coinAddress` | string | `"So11...112"` | P1 |
| `leaderboardEntry.sideBet.realPortion` | number | `0.001` | P1 |

**Count**: 5 new fields

---

### 2. playerUpdate Findings

**Documentation Gap**: 84% undocumented (5 fields documented, 37 total)

#### Category 1: Identity & Authentication (P0)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `id` | string | `"did:privy:cma094vht019il80np6aidhqd"` | Player's Privy DID |
| `role` | null/string | `null` | Admin/moderator role |
| `authenticated` | bool | `true` | Wallet auth status |

#### Category 2: Account Balances & Bonus System (P2)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `bonusBalance` | number | `0` | Promotional balance (SOL) |
| `bonusWagerReq` | number | `0` | Wagering requirement remaining |
| `bonusWagered` | number | `0` | Bonus amount wagered |
| `shitcoinBalances` | object | `{"0xPractice": 100}` | Alt token balances |

#### Category 3: Gamification & Rewards (P3 - OUT_OF_SCOPE)

| Field | Type | Description |
|-------|------|-------------|
| `levelInfo` | object | Player progression system |
| `levelInfo.level` | int | Current player level |
| `levelInfo.xp` | int | XP toward next level |
| `levelInfo.xpForNextLevel` | int | XP required for next level |
| `levelInfo.totalXP` | int | Lifetime XP earned |
| `xpBoost` | object | XP multiplier system |
| `xpBoost.active` | bool | Boost currently active |
| `xpBoost.activeUntil` | int | Unix timestamp expiry |
| `xpBoost.available` | int | Available boosts |
| `crateKeys` | object | Loot box key inventory |
| `crateKeys.gold` | int | Gold crate keys |
| `crateKeys.diamond` | int | Diamond crate keys |
| `crateKeys.coal` | int | Coal crate keys |
| `crateKeys.iron` | int | Iron crate keys |
| `crateKeys.tier1` | int | Tier 1 crate keys |
| `crateKeys.tier0` | int | Tier 0 crate keys |
| `recentCrateRewards` | array | Recent loot box drops |

#### Category 4: Trading Configuration & Automation (P1)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `autobuysEnabled` | bool | `false` | Auto-buy bot enabled |
| `autosellPrice` | null/number | `null` | Auto-sell trigger price |
| `hasInteracted` | bool | `true` | Has placed at least one trade |
| `hitMaxWin` | bool | `false` | Hit max win limit |
| `selectedCoin` | null/string | `null` | Selected shitcoin (null = SOL) |

#### Category 5: Position & Risk Management (P1)

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `pnlPercent` | number | `-99.3217` | PnL as percentage |
| `sidebetPnl` | number | `0` | PnL from sidebets only |
| `shortPosition` | null/object | `null` | Short position details |
| `leveragedPositions` | array | `[]` | Leveraged positions |
| `sidebets` | array | `[]` | Array of active sidebets |

#### Category 6: SideBet (confirms gameStatePlayerUpdate)

| Field | Type | Description |
|-------|------|-------------|
| `sideBet.bonusPortion` | number | Bonus SOL portion |
| `sideBet.coinAddress` | string | Token address |
| `sideBet.realPortion` | number | Real SOL portion |

**Count**: 32 new fields

---

### 3. gameStateUpdate Findings

#### Phase-Dependent Field Presence (NEW DISCOVERY)

| Field | Tick 0 | Mid-Game | Notes |
|-------|:------:|:--------:|-------|
| `active` | ✅ | ✅ | Always present |
| `price` | ✅ | ✅ | Always present |
| `tickCount` | ✅ | ✅ | Always present |
| `leaderboard` | ✅ (empty) | ✅ | Always present |
| `partialPrices` | ✅ | ✅ | Always present |
| `provablyFair` | ✅ | ✅ | Always present |
| `averageMultiplier` | ❌ | ✅ | Only after session data |
| `count2x/10x/50x/100x` | ❌ | ✅ | Only after session data |
| `highestToday*` | ❌ | ✅ | Only after daily high |
| `gameHistory[]` | ❌ | ✅ | Only after games complete |

**Finding**: Field presence varies by game phase - need to document optionality

---

### 4. Event Ordering Pattern (NEW)

**Pattern**: Position opening triggers 3-event sequence after `coolDownTimer:100`:

```
1. gameStatePlayerUpdate  (personal state)
2. playerUpdate           (balance sync)
3. gameStateUpdate        (global state tick 0)
```

**Use Case**: Bot should wait for all 3 events before confirming position opened.

---

## Priority Classification

| Priority | Category | Field Count | Action |
|----------|----------|:-----------:|--------|
| **P0** | Identity & Core Trading | 3 | Immediate |
| **P1** | Trading Features & Position | 15 | High |
| **P2** | Bonus System | 4 | Medium |
| **P3** | Gamification (OUT_OF_SCOPE) | 15 | Low/Document only |

---

## Hypotheses to Validate

1. **Bonus Split**: `betAmount = realPortion + bonusPortion`
2. **Auto-Trading Conflict**: `autobuysEnabled` may conflict with external bots
3. **Multi-Sidebet**: `sidebets[]` array suggests multiple simultaneous sidebets possible

---

## Next Steps

- [ ] Capture Question 2 events
- [ ] Capture Question 3 events
- [ ] Capture Question 4 events
- [ ] Prepare staging plan for canonical review
- [ ] Promote P0-P1 fields to CANONICAL status
