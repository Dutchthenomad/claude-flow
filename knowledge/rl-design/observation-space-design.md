# Observation Space Design

**Date:** 2025-12-25 (Created) | 2025-12-28 (Pipeline C Complete)
**Status:** PHASE C COMPLETE - All Player Action Features Validated
**Validated By:** rugs-expert agent (Sessions 1-2)

---

## Validation Status

| Category | Status | Session |
|----------|--------|---------|
| Server State Features | ✅ VALIDATED | Session 1 |
| Derived Features | ✅ VALIDATED | Session 1 |
| Player Action Features | ✅ **ALL VALIDATED** | Session 2 (2025-12-28) |
| Execution Tracking Features | ✅ **NEW - VALIDATED** | Session 2 (2025-12-28) |
| Market Aggregation Features | ⏳ PENDING Implementation | Session 3 |

**Pipeline B Gate Passed:** 2025-12-27 - ButtonEvents capture tick=712, price=3.69, game_id=real
**Pipeline C Gate Passed:** 2025-12-28 - All player action features implemented and validated

**See:** `docs/plans/GLOBAL-DEVELOPMENT-PLAN.md` for current development status.

---

## Revision History

| Date | Change | By |
|------|--------|-----|
| 2025-12-25 | Initial draft | Human |
| 2025-12-26 | Validated server state fields against WebSocket spec | rugs-expert |
| 2025-12-26 | Removed whale_activity_flag, god_candle_*, gameHistory[] | Decision Points 2-4 |
| 2025-12-26 | Split into feature categories with dependency tracking | Session 1 revision |
| 2025-12-27 | Pipeline B verified, Player Action features 2/3 validated | Session 2 |
| 2025-12-28 | **Pipeline C COMPLETE** - All player action features validated | Session 2 |
| 2025-12-28 | Added execution tracking fields (execution_tick, trade_id, latency_ms) | rugs-expert RAG |
| 2025-12-28 | Implemented time_in_position in LiveStateProvider | TDD (1149 tests) |

---

## Overview

This document defines the canonical Observation Space for RL training in the VECTRA-PLAYER bot system.

**Design Principle:** Features are categorized by their data source to ensure proper implementation sequencing.

---

## Feature Categories

### Category 1: Server State Features (✅ VALIDATED)

These fields come directly from WebSocket events and have been validated against the protocol spec.

#### Game State (from `gameStateUpdate`)

| Field | JSON Path | Type | Status |
|-------|-----------|------|--------|
| `tick` | `.tickCount` | int | ✅ VALIDATED |
| `price` | `.price` | float | ✅ VALIDATED |
| `game_phase` | **DERIVED** | int | ✅ VALIDATED (see note) |
| `cooldown_timer_ms` | `.cooldownTimer` | int | ✅ VALIDATED |
| `allow_pre_round_buys` | `.allowPreRoundBuys` | bool | ✅ VALIDATED |
| `active` | `.active` | bool | ✅ VALIDATED |
| `rugged` | `.rugged` | bool | ✅ VALIDATED |
| `connected_players` | `.connectedPlayers` | int | ✅ VALIDATED (renamed from players_in_game) |
| `gameId` | `.gameId` | string | 🆕 ADDED - detect new game |

**Game Phase Derivation (4 phases - Decision Point 1):**
```python
def detect_phase(event: dict) -> int:
    if event.get('cooldownTimer', 0) > 0:
        return 0  # COOLDOWN
    elif event.get('rugged', False) and not event.get('active', False):
        return 3  # RUGGED (brief, 1-2 ticks)
    elif event.get('allowPreRoundBuys', False) and not event.get('active', False):
        return 1  # PRESALE
    elif event.get('active', False):
        return 2  # ACTIVE
    return 0  # COOLDOWN (default)
```

#### Player State (from `playerUpdate` - AUTH REQUIRED)

| Field | JSON Path | Type | Status |
|-------|-----------|------|--------|
| `balance` | `.cash` | float | ✅ VALIDATED (server-authoritative) |
| `position_qty` | `.positionQty` | float | ✅ VALIDATED |
| `avg_entry_price` | `.avgCost` | float | ✅ VALIDATED |
| `cumulative_pnl` | `.cumulativePnL` | float | ✅ VALIDATED |
| `total_invested` | `.totalInvested` | float | ✅ VALIDATED |

#### Rugpool (from `gameStateUpdate.rugpool`)

| Field | JSON Path | Type | Status |
|-------|-----------|------|--------|
| `rugpool_amount` | `.rugpool.rugpoolAmount` | float | ✅ VALIDATED |
| `rugpool_threshold` | `.rugpool.threshold` | float | ✅ VALIDATED |
| `instarug_count` | `.rugpool.instarugCount` | int | 🆕 ADDED |

#### Session Statistics (from `gameStateUpdate`)

| Field | JSON Path | Type | Status |
|-------|-----------|------|--------|
| `average_multiplier` | `.averageMultiplier` | float | ✅ VALIDATED |
| `count_2x` | `.count2x` | int | ✅ VALIDATED |
| `count_10x` | `.count10x` | int | ✅ VALIDATED |
| `count_50x` | `.count50x` | int | ✅ VALIDATED |
| `count_100x` | `.count100x` | int | ✅ VALIDATED |
| `highest_today` | `.highestToday` | float | ✅ VALIDATED |

---

### Category 2: Derived Features (✅ VALIDATED)

These are calculated from server state data.

| Field | Formula | Type | Status |
|-------|---------|------|--------|
| `price_velocity` | `(price[t] - price[t-1]) / dt` | float | ✅ VALIDATED |
| `price_acceleration` | `(vel[t] - vel[t-1]) / dt` | float | ✅ VALIDATED |
| `unrealized_pnl` | `(price - avgCost) * positionQty` | float | ✅ VALIDATED |
| `position_pnl_pct` | `(price - avgCost) / avgCost` | float | ✅ VALIDATED |
| `rugpool_ratio` | `rugpoolAmount / threshold` | float | ✅ VALIDATED |
| `balance_at_risk_pct` | `positionQty / (balance + value)` | float | ✅ VALIDATED |

---

### Category 3: Player Action Features (✅ ALL VALIDATED)

**Phase B GATE PASSED (2025-12-27):** ButtonEvents now capture real game context.
**Phase C GATE PASSED (2025-12-28):** All player action features implemented.

| Field | Source | Type | Status |
|-------|--------|------|--------|
| `time_in_position` | `LiveStateProvider.time_in_position` | int | ✅ **IMPLEMENTED** (2025-12-28) |
| `ticks_since_last_action` | ButtonEvent tracking | int | ✅ VALIDATED (range 1-517) |
| `bet_amount` | UI state from ButtonEvent | Decimal | ✅ VALIDATED (17/20 nonzero) |

**Implementation Details (2025-12-28):**
- `entry_tick` tracked in `LiveStateProvider` when `positionQty` changes from 0 → non-zero
- `time_in_position = current_tick - entry_tick`
- Resets on: game_id change (new game), position close (qty → 0)
- **Tests:** 6 new tests added (1149 total passing)

**Validation Evidence (2025-12-27):**
- `ticks_since_last_action`: 20/20 valid int values, range 1-517
- `bet_amount`: 17/20 nonzero (3 with 0.0 are SELL actions as expected)
- Action sequences properly grouped with unique sequence_id

---

### Category 3b: Execution Tracking Features (✅ NEW - VALIDATED)

**Added (2025-12-28):** Based on rugs-expert RAG validation against WebSocket protocol spec.

| Field | Source | Type | Status |
|-------|--------|------|--------|
| `execution_tick` | `standard/newTrade.tickIndex` | int | ✅ IMPLEMENTED |
| `execution_price` | `standard/newTrade.price` | float | ✅ IMPLEMENTED |
| `trade_id` | `standard/newTrade.id` | str | ✅ IMPLEMENTED |
| `client_timestamp` | Local timestamp (ms since epoch) | int | ✅ IMPLEMENTED |
| `latency_ms` | `server_ts - client_timestamp` | int | ✅ IMPLEMENTED |

**Why These Matter for RL:**
- `execution_tick` vs `tick`: 20-50ms latency means actual execution may differ from request
- `latency_ms`: Bot learns realistic timing expectations
- `trade_id`: Links ButtonEvent to broadcast trade for outcome tracking

**Protocol Sources (from rugs-expert RAG):**
- `standard/newTrade.tickIndex`: Line 585
- `success.timestamp`: Lines 810, 838
- `standard/newTrade.id`: Line 577

---

### Category 4: Market Aggregation Features (⏳ PENDING Implementation)

**BLOCKED:** These require aggregation logic implementation.

| Field | Source | Type | Status |
|-------|--------|------|--------|
| `players_with_positions` | Count from leaderboard where hasActiveTrades | int | ⏳ PENDING |
| `total_market_capital` | Sum from leaderboard totalInvested | float | ⏳ PENDING |
| `recent_buy_volume` | Rolling window from standard/newTrade | float | ⏳ PENDING |
| `recent_sell_volume` | Rolling window from standard/newTrade | float | ⏳ PENDING |
| `trade_flow_ratio` | buy_volume / sell_volume | float | ⏳ PENDING |

**Note:** `standard/newTrade` structure validated:
```json
{
  "playerId": "did:privy:...",
  "type": "BUY" | "SELL",
  "amount": 0.001,
  "price": 1.234,
  "timestamp": 1765069123456
}
```

---

### Category 5: Historical Features (⏳ PENDING Implementation)

| Field | Source | Type | Status |
|-------|--------|------|--------|
| `price_history` | Local rolling buffer (20 prices) | list[float] | ⏳ PENDING |
| `volume_history` | Aggregated from standard/newTrade | list[float] | ⏳ PENDING |

**Note:** `.partialPrices.values` is a dict `{tick: price}` for backfill, not a rolling window. Maintain local array.

---

## Removed Features (v1.0)

| Feature | Reason | Decision |
|---------|--------|----------|
| `whale_activity_flag` | No empirical threshold | Decision Point 2 |
| `god_candle_2x` | Focus on core | Decision Point 3 |
| `god_candle_2x_timestamp` | Focus on core | Decision Point 3 |
| `god_candle_2x_massive_jump` | Focus on core | Decision Point 3 |
| `god_candle_10x` | Focus on core | Decision Point 3 |
| `god_candle_10x_timestamp` | Focus on core | Decision Point 3 |
| `god_candle_10x_massive_jump` | Focus on core | Decision Point 3 |
| `god_candle_50x` | Focus on core | Decision Point 3 |
| `god_candle_50x_timestamp` | Focus on core | Decision Point 3 |
| `god_candle_50x_massive_jump` | Focus on core | Decision Point 3 |
| `game_history` | Requires ButtonEvent | Decision Point 4 |
| `last_game_peak` | Requires ButtonEvent | Decision Point 4 |
| `last_game_ticks` | Requires ButtonEvent | Decision Point 4 |

---

## Canonical Event Capture List

| Event | Priority | Auth | Key Fields | Status |
|-------|:--------:|:----:|------------|--------|
| `gameStateUpdate` | P0 | No | tick, price, active, rugged, leaderboard | ✅ VALIDATED |
| `playerUpdate` | P0 | **YES** | cash, positionQty, avgCost, cumulativePnL | ✅ VALIDATED |
| `standard/newTrade` | P1 | No | playerId, type, amount, price | ✅ VALIDATED |
| `buyOrder` | P0 | **YES** | Request/response via ID matching | ✅ VALIDATED |
| `sellOrder` | P0 | **YES** | Request/response via ID matching | ✅ VALIDATED |
| `sidebet` | P1 | **YES** | Request/response via ID matching | ✅ VALIDATED |
| `gameStatePlayerUpdate` | P1 | **YES** | Your leaderboard entry | ✅ VALIDATED |
| `usernameStatus` | **P1** | **YES** | id, username | ✅ VALIDATED (upgraded) |
| `playerLeaderboardPosition` | P2 | **YES** | 7-day leaderboard rank | 🆕 ADDED |

---

## Feature Count Summary

| Category | Count | Status |
|----------|:-----:|--------|
| Server State | 22 | ✅ VALIDATED |
| Derived | 6 | ✅ VALIDATED |
| Player Action | 3 | ✅ **ALL VALIDATED** |
| Execution Tracking | 5 | ✅ **NEW - VALIDATED** |
| Market Aggregation | 5 | ⏳ PENDING |
| Historical | 2 | ⏳ PENDING |
| **TOTAL** | **43** | **36 validated, 7 pending** |

---

## Python Dataclass Definition (v1.1 - Pipeline C Complete)

```python
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class Observation:
    """
    Standard observation for RL training.
    v1.1: 36 validated features (server state + derived + player action + execution)

    Updated: 2025-12-28 - Pipeline C Complete
    """

    # === GAME STATE (9 features) ===
    tick: int
    price: float
    game_phase: int  # 0=cooldown, 1=presale, 2=active, 3=rugged
    cooldown_timer_ms: int
    allow_pre_round_buys: bool
    active: bool
    rugged: bool
    connected_players: int
    game_id: str  # Detect game boundaries

    # === PLAYER STATE (5 features, AUTH REQUIRED) ===
    balance: float  # Server-authoritative
    position_qty: float
    avg_entry_price: float
    cumulative_pnl: float
    total_invested: float

    # === RUGPOOL (3 features) ===
    rugpool_amount: float
    rugpool_threshold: float
    instarug_count: int

    # === SESSION STATS (6 features) ===
    average_multiplier: float
    count_2x: int
    count_10x: int
    count_50x: int
    count_100x: int
    highest_today: float

    # === DERIVED (6 features) ===
    price_velocity: float
    price_acceleration: float
    unrealized_pnl: float
    position_pnl_pct: float
    rugpool_ratio: float
    balance_at_risk_pct: float

    # === PLAYER ACTION (3 features) - NEW in v1.1 ===
    time_in_position: int  # current_tick - entry_tick
    ticks_since_last_action: int  # Time since last button press
    bet_amount: Decimal  # Current bet amount in entry field

    # === EXECUTION TRACKING (5 features, Optional) - NEW in v1.1 ===
    execution_tick: Optional[int] = None  # Actual tick when trade executed
    execution_price: Optional[float] = None  # Actual price at execution
    trade_id: Optional[str] = None  # Links to newTrade broadcast
    client_timestamp: Optional[int] = None  # When we sent request
    latency_ms: Optional[int] = None  # server_ts - client_timestamp

    # === PENDING (Session 3) ===
    # players_with_positions: int
    # total_market_capital: float
    # recent_buy_volume: float
    # recent_sell_volume: float
    # trade_flow_ratio: float
    # price_history: List[float]
    # volume_history: List[float]
```

---

## Next Steps

1. ~~**Phase B:** Implement ButtonEvent logging~~ ✅ COMPLETE (2025-12-27)
2. ~~**Session 2:** Validate Player Action features~~ ✅ **ALL VALIDATED** (2025-12-28)
3. ~~**Implement `time_in_position` tracking**~~ ✅ COMPLETE (2025-12-28)
4. ~~**Add execution tracking fields**~~ ✅ COMPLETE (2025-12-28)
5. **Pipeline D:** Implement training data pipeline with validated schema
6. **Session 3:** Market aggregation features (players_with_positions, trade_flow_ratio, etc.)

---

## References

- **Validation Report:** `docs/plans/observation-space-field-validation-report.md`
- **Revised Pipeline:** `docs/plans/2025-12-26-revised-bot-training-pipeline.md`
- **WebSocket Spec:** `/home/nomad/Desktop/claude-flow/knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md`
- **Action Space Design:** `action-space-design.md`
- **Implementation Plan:** `implementation-plan.md`

---

*Validated: 2025-12-26*
*Session: Observation Space Field Validation Review (Session 1 of 3)*
*Agent: rugs-expert (Claude Opus 4.5)*
