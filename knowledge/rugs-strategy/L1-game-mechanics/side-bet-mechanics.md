---
layer: 1
domain: game-mechanics/side-bets
priority: P0
bot_relevant: true
validation_tier: reviewed
source_file: "RAG SUPERPACK/review data/side_bet_mechanics_v2.md"
cross_refs:
  - L1-game-mechanics/provably-fair.md
  - L5-strategy-tactics/probability-framework.md
  - L2-protocol/websocket-spec.md
last_validated: 2025-12-24
---

# Side Bet Mechanics: Complete System Rules (v2.0)

## Executive Summary
The Rugs.fun side betting system enables players to wager that the current game will end (rug) within the next 40 ticks. This document provides the definitive mechanical rules based on analysis of 100 games with 22,507 tick intervals, establishing accurate timing models and mathematical frameworks.

## Critical Timing Analysis Update (July 2025)

### Comprehensive Data Analysis
Based on analysis of 100 randomly sampled games containing 22,507 tick intervals:

**Distribution Analysis:**
- 98.14% of ticks fall between 200-300ms
- 95% of ticks occur between 237-269ms
- Only 0.39% of ticks are under 200ms
- 0.44% of ticks exceed 1000ms (outliers/spikes)

---

## Core Mechanical Rules

### 1. Betting Window and Constraints

#### 1.1 Active Bet Limitations
- **One bet limit**: Players can have exactly ONE active side bet at any time
- **No queuing**: Cannot pre-place bets during cooldown periods
- **Immediate deduction**: SOL is instantly debited from wallet upon placement
- **No cancellation**: Once placed, bets cannot be cancelled or modified

#### 1.2 Placement Window
- **Availability**: From tick 0 through the final tick of any active game
- **Presale betting**: Available during 10-second presale phase (startTick: -1)
- **Late game**: Can bet even at tick 500+ (extremely high probability zones)
- **Final tick**: Betting closes when game rugs (no warning period)

#### 1.3 Bet Amount Constraints
- **Minimum**: 0.001 SOL
- **Maximum**: 5.0 SOL (standard game limit)
- **Precision**: System accepts up to 6 decimal places
- **Currency**: SOL only (coinAddress: "So11111111111111111111111111111111111111112")

### 2. Outcome Resolution System

#### 2.1 Win Condition
- **Binary outcome**: Game must rug within exactly 40 ticks of placement
- **Tick precision**: If placed at tick N, covers ticks N through N+39 (inclusive)
- **Timing basis**: Uses tick count, not elapsed time (critical difference)

#### 2.2 Payout Structure
- **Win ratio**: 5:1 (400% profit + original bet returned)
- **Calculation**: `payout = betAmount × 5`
- **Net profit**: `profit = betAmount × 4`
- **Instant credit**: Winning payouts credited immediately upon game rug

#### 2.3 Loss Scenarios
- **Complete loss**: 100% of bet amount lost if game continues past tick window
- **No partial payouts**: Binary win/lose only
- **Cooldown trigger**: ~1 second display period showing "sidebet lost"

### 3. Event Structure Analysis

#### 3.1 newSideBet Event Schema
```javascript
{
  betAmount: 0.001,              // SOL amount wagered
  coinAddress: "So11...112",     // SOL identifier
  endTick: 108,                  // startTick + 40
  playerId: "did:privy:...",     // Unique player ID
  startTick: 68,                 // Tick when bet placed (-1 for presale)
  tickIndex: 68,                 // Current game tick (matches startTick)
  timestamp: 1753306685322,      // Unix timestamp (milliseconds)
  type: "placed",                // Event type
  username: "PlayerName",        // Display name
  xPayout: 5                     // Payout multiplier
}
```

#### 3.2 gameStateUpdate Integration
```javascript
// Side bet status within main game state
{
  sideBet: {
    startedAtTick: 384,
    gameId: '20250723-...',
    end: 424,                    // startedAtTick + 40
    betAmount: 0.005,
    xPayout: 5
  },
  sidebetActive: true,           // Boolean flag
  sidebetPnl: -0.01             // Running P&L (negative = losing)
}
```

### 4. Updated Timing Analysis and Compensation

#### 4.1 Empirical vs. Theoretical Timing
```javascript
// Theoretical specifications
const THEORETICAL = {
  tickDuration: 250,      // ms per tick
  windowDuration: 10000,  // 40 ticks × 250ms = 10 seconds
  precision: "exact"
};

// Empirical findings (July 2025 analysis)
const EMPIRICAL = {
  meanTickDuration: 271.5,     // 8.6% higher than theoretical
  medianTickDuration: 251.0,   // Very close to theoretical
  stdDev: 295.3,               // High variability
  variance: 87174.6,           // Significant instability
  reliableRange: {
    min: 237,                  // 5th percentile
    max: 269                   // 95th percentile
  },
  expectedWindowDuration: 10860,  // 40 ticks × 271.5ms ≈ 10.86 seconds
  precision: "highly_variable"
};
```

### 5. Session and Game Interaction Rules

#### 5.1 Session Limits
- **Winning cap**: 20 SOL maximum winnings per game triggers auto-stop
- **No loss limits**: Players can lose entire wallet if not managed
- **Cross-game tracking**: Winnings/losses accumulate across games
- **Reset conditions**: New wallet or manual reset only

#### 5.2 Main Game Integration
- **Independence**: Side bets do not affect PRNG within single game
- **Combined exposure**: Can maintain both main positions and side bets
- **Visibility**: All players see others' side bet positions and P&L
- **Hedging capability**: Can use side bets to hedge main game positions

#### 5.3 Game Phase Interactions
```javascript
// Phase-specific betting behavior
const PHASE_RULES = {
  presale: {
    sideBetting: true,
    startTick: -1,           // Special identifier
    window: "10_seconds",    // Fixed presale duration
    mainGame: false          // No main game activity
  },
  active: {
    sideBetting: true,
    startTick: "current_tick",
    window: "40_ticks",      // Standard window
    mainGame: true           // Full trading available
  },
  rugged: {
    sideBetting: false,      // No betting during rug events
    settlement: "immediate", // Instant payout processing
    cooldown: "~15_seconds"  // Before next game
  }
};
```

### 6. Mathematical Framework

#### 6.1 Expected Value Formula
```javascript
function calculateExpectedValue(winProbability, betAmount, timingReliability = 1.0) {
  const winOutcome = betAmount * 4;  // Net profit (400%)
  const loseOutcome = -betAmount;    // Total loss

  // Adjust probability based on timing reliability
  const adjustedProbability = winProbability * timingReliability;

  return (adjustedProbability * winOutcome) + ((1 - adjustedProbability) * loseOutcome);
}

// Breakeven probability
const BREAKEVEN_PROBABILITY = 1/6; // 16.67%
```

---

## For Bot Development

**Key Parameters**:
- `sideBetWindow`: 40 ticks
- `payoutMultiplier`: 5 (4x net profit)
- `minBet`: 0.001 SOL
- `maxBet`: 5.0 SOL
- `breakevenProbability`: 16.67%

**Integration Points**:
- Monitor `newSideBet` events for bet placement
- Track `gameStateUpdate.sideBet` for active bet status
- Calculate probability at current tick for bet timing
- Account for timing variance in probability estimates

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
