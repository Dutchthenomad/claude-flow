---
layer: 1
domain: game-mechanics/phases
priority: P1
bot_relevant: true
validation_tier: theoretical
status: DEPRECATED-NEEDS-REVALIDATION
source_file: "RAG SUPERPACK/CORE ARCHITECTURE/rugs-game-phases-unified.md"
cross_refs:
  - L2-protocol/websocket-spec.md
  - L1-game-mechanics/WHAT-IT-IS-NOT.md
last_validated: 2025-12-24
warning: "DEPRECATED SCHEMA - Needs revalidation against current WebSocket events"
---

# Rugs.fun Game Phases - Unified Specification

> **WARNING: DEPRECATED SCHEMA**
>
> This document is from an earlier version of the rugs.fun WebSocket system. Events, fields, and features may have changed.
> **Do NOT consider this information canonical** - it provides historical context and guides development of the current validated game phase loop architecture.
>
> **Validation Required**: Compare against current `gameStateUpdate` events before using.

---

## Overview

The Rugs.fun game operates in a **perpetual 4-phase loop** that repeats continuously:

```
ACTIVE GAMEPLAY → RUG EVENT → COOLDOWN PHASE → GAME ACTIVATION → [repeat]
```

---

## Phase Architecture

### Core Loop Structure

The game consists of four distinct phases that cycle perpetually:

1. **ACTIVE GAMEPLAY** - Live gameplay with price movements and trading
2. **RUG EVENT** - Game termination with provably fair seed revelation
3. **COOLDOWN PHASE** - Settlement period with embedded presale window
4. **GAME ACTIVATION** - Fresh game start at 1.00x price

### Phase Timing Overview

- **ACTIVE GAMEPLAY Phase**: Variable duration (1-5000 ticks, 250ms per tick)
- **RUG EVENT Phase**: Instantaneous dual-event pattern
- **COOLDOWN PHASE**: 15 seconds total, split into:
  - **Settlement Buffer**: 15000ms → 10000ms (5 seconds)
  - **PRESALE Window**: 10000ms → 0ms (exactly 10 seconds, `allowPreRoundBuys: true`)
- **GAME ACTIVATION Phase**: Instantaneous transition to active gameplay

---

## Phase 1: ACTIVE GAMEPLAY

The main gameplay phase where live trading occurs with real-time price movements.

### Primary Detection Logic

```javascript
// DEFINITIVE ACTIVE GAMEPLAY IDENTIFIER
if (data.active === true && data.tickCount > 0 && data.tradeCount > 0) {
  return "ACTIVE_GAMEPLAY";
}
```

### Key Characteristics

| Field | Value | Description |
|-------|-------|-------------|
| `active` | `true` | Game is actively running |
| `rugged` | `false` | Game has not ended |
| `allowPreRoundBuys` | `false` | Presale disabled during active phase |
| `cooldownTimer` | `0` | No cooldown during active gameplay |
| `tickCount` | `0` → `5000` max | Current game tick (increments every 250ms) |
| `price` | `1.0` at tick 0, then variable | ALWAYS starts at exactly 1.00x |
| `tradeCount` | `> 0` | Total trades executed in current game |

---

## Phase 2: RUG EVENT

The game termination phase featuring a dual-event pattern for provably fair seed revelation.

### Definitive Detection Logic

```javascript
// ONLY DEFINITIVE RUG EVENT IDENTIFIER
if (data.gameHistory && Array.isArray(data.gameHistory)) {
  // gameHistory ONLY appears during rug events - NEVER any other time

  if (data.active === true && data.rugged === true) {
    return "RUG_EVENT_1_SEED_REVEAL";
  } else if (data.active === false && data.rugged === true) {
    return "RUG_EVENT_2_NEW_GAME_SETUP";
  }
}
```

**CRITICAL**: The presence of `gameHistory` array is the **ONLY** definitive indicator of a rug event.

### Dual Event Pattern

The rug phase consists of two distinct back-to-back `gameStateUpdate` events:

#### Event 1: Seed Reveal
*Occurs milliseconds after PRNG triggers rug*

```json
{
  "active": true,                    // Still true in first event
  "rugged": true,                    // Rug state confirmed
  "gameHistory": [/* 10 games */],   // ONLY TIME this appears
  "gameId": "20250618-7117...",     // Current game ID (that just rugged)
  "tickCount": 291,                  // Final tick count
  "provablyFair": {
    "serverSeedHash": "9d3c862e..."  // Hash for game that just rugged
  }
}
```

#### Event 2: New Game Setup
*Immediate follow-up event*

```json
{
  "active": false,                   // Now false - cooldown begins
  "rugged": true,                    // Still shows rugged state
  "gameHistory": [/* same array */], // Same gameHistory data
  "gameId": "20250618-4370...",     // NEW game ID generated
  "cooldownTimer": 14900,            // Cooldown timer activated
  "provablyFair": {
    "serverSeedHash": "e17c39a6..."  // NEW hash for next game
  }
}
```

---

## Phase 3: COOLDOWN PHASE

### Cooldown Structure

Total cooldown after rug: **15 seconds** (15000ms total)

#### Part 1: Settlement Buffer (15000ms → 10000ms)
- **Duration**: 5 seconds
- **State**: `rugged: true`, `active: false`, `allowPreRoundBuys: false`
- **Purpose**: Backend settlement and balancing of previous game results
- **Actions**: No trading allowed

#### Part 2: Presale Window (10000ms → 0ms)
- **Duration**: Exactly 10 seconds (always, no exceptions)
- **State**: `allowPreRoundBuys: true`
- **Purpose**: Optional pre-game buy-in and SideBet placement
- **Actions**: Buy orders and SideBet placement only (no selling)

### Detection Logic

```javascript
// PRESALE WINDOW DETECTION (within cooldown)
if (data.cooldownTimer > 0 &&
    data.cooldownTimer <= 10000 &&
    data.allowPreRoundBuys === true) {
  return "PRESALE_PHASE";
}

// SETTLEMENT BUFFER DETECTION
if (data.cooldownTimer > 10000 &&
    data.rugged === true &&
    data.active === false) {
  return "COOLDOWN_PHASE";
}
```

---

## Phase 4: GAME ACTIVATION

The instantaneous transition from cooldown to active gameplay.

### Detection Logic

```javascript
// GAME ACTIVATION DETECTION
if (data.active === true && data.tickCount === 0) {
  return "GAME_ACTIVATION";
}
```

### Activation Characteristics

When `cooldownTimer` reaches 0:
- `active` becomes `true`
- `tickCount` starts at 0
- `price` begins at exactly 1.00x
- `allowPreRoundBuys` becomes `false`
- Trading (buy/sell) fully enabled
- SideBets become locked in for the game duration

---

## Summary

**4 phases** in the complete cycle:
1. ACTIVE GAMEPLAY
2. RUG EVENT
3. COOLDOWN PHASE
4. GAME ACTIVATION

**Key Detection Points**:
- `gameHistory` presence = definitive rug indicator
- `cooldownTimer` value determines presale vs cooldown
- `active` + `tickCount` confirms game state

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
*STATUS: Needs revalidation against current protocol*
