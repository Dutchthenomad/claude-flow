# rugs.fun Official FAQ & Game Mechanics

**Source**: rugs.fun FAQ (verbatim) + Analysis Notes
**Date Captured**: December 25, 2025
**Status**: CANONICAL
**Priority**: P0 - Core Game Knowledge

---

## Official FAQ (Verbatim)

### How does the Game work?

rugs.fun is similar to the popular game "Crash", except you can buy and sell any amount at any time. Just don't get rugged! Hold positions for longer periods to earn industry-leading rakebacks via crates. Charts are randomized with a provably fair system and cannot be influenced by buys or sells.

### How does bonus SOL work?

Earn Bonus SOL by entering a code at the bottom of the deposit page. Bonus SOL codes have wager requirements attached to them. Earn progress towards the requirement by placing Valid Bets. Once you hit the wager requirement, your ENTIRE remaining bonus balance converts into instantly-withdrawable SOL (meaning there is no cap on the amount you can earn from a code)!

### What are crates and keys? What are "Valid Bets"?

Crates are our way of giving SOL back to you at an industry-leading RTP rate. Earn XP to level up and receive crate keys; you earn 1 XP for every Valid Bet of 0.001 SOL. A "Valid Bet" is a position held for at least 20 game ticks (5 seconds), or a position that was rugged (after any amount of time). XP automatically multiplies the longer you hold.

### Is this a skills based game?

Contrary to popular belief, there actually are strategies you can use on rugs.fun to increase your chances of winning over the long run. You can't beat the house, but you *can* trade smarter than most.

### What's the house edge?

Every game tick (250ms) has a very small house edge built in - roughly 0.05%.

### How do I know the game is fair?

We use a provably fair system that allows you to verify that game outcomes cannot be manipulated. Check out our Fairness page for details on how this works and how you can verify the fairness of any game round.

---

## Analysis Notes (User-Verified)

### House Edge Mechanics

The house edge is applied in two ways:

1. **Per-tick edge**: ~0.05% per tick (250ms), compounding over game duration
2. **Liquidation remainder**: When the game rugs, ALL active positions are liquidated

**Critical Insight**: The final game tick price is a non-zero micro remainder (e.g., `0.0097...`). This remainder represents the house's take from all liquidated positions. By studying this final price across thousands of games, we can infer the exact liquidation mechanics.

### What Happens on Rug

When `rugged = true`:
- All active trade positions are **liquidated**
- All active sidebets that haven't resolved are **won by the house**
- All player PnLs are balanced
- The house keeps the remainder

### Valid Bet Definition (Critical for RL)

| Condition | Valid Bet? |
|-----------|------------|
| Position held < 20 ticks AND sold | NO |
| Position held >= 20 ticks (5 sec) | YES |
| Position rugged (any duration) | YES |

**RL Implication**: Bot must hold positions for at least 20 ticks to earn XP and crate progress. Early exits before 20 ticks are "invalid" and don't contribute to leveling.

### XP System

- **1 XP** = 1 Valid Bet of 0.001 SOL
- XP **multiplies** the longer you hold
- XP leads to **level ups** which grant **crate keys**

---

## Game Modes (Separate Games)

| Mode | Type | Description | Priority |
|------|------|-------------|----------|
| **Standard** | Primary | Main rugs.fun game (this doc) | P0 - Active |
| **Pinpoint (BBC)** | Side game | Bull/Bear/Crab - modified coin flip | P3 - Not tracked |
| **Candleflip** | Side game | Classic coin flip with candlestick animation | P3 - Not tracked |

**Note**: Side games use separate UIs and potentially different WebSocket events. Not tracked until main bot is operational.

---

## Special Events (Deprioritized)

### Golden Hour

**Status**: OUT_OF_SCOPE (until bot is operational)

**Mechanics**:
- SOL is awarded at the end of each game during Golden Hour
- Entry: Place Valid Bets (0.001 SOL = 1 entry)
- Max entries: 250 per round (entries reset each round)
- Winner selection: Random based on entries earned via valid trades
- Typical prize: 0.1-0.5 SOL per game

**Technical Note**: Golden Hour events cause WebSocket delays due to high activity.

### Other Special Events

| Event | Description | Priority |
|-------|-------------|----------|
| Diddy Party | Unknown mechanics | OUT_OF_SCOPE |
| Rugs Royale | Tournament mode | OUT_OF_SCOPE |

These will be tracked after main bot is fully operational.

---

## Shorting Feature

**Status**: NEW FEATURE (needs capture)

**UI Behavior**:
- Enabled via toggle button
- When enabled, SHORT button appears between BUY and SELL
- Leverage available for profiles Level 10+

**Leverage Options**: 1x, 2x, 3x, 4x, 5x (slider)

**Data Gap**: We have `shortPosition: null` in all captures. Need authenticated session captures with active shorts.

---

## Deprioritized Systems

The following are lowest priority and will not be tracked until core bot is operational:

1. **Rugpass Tier System** - Progression tiers (Tier 0, 1, 2...)
2. **Level System** - XP-based leveling (🔥 badges)
3. **Badge System** - Special badges (777, Mod, verified)
4. **Crate System** - Key earning and crate opening

---

## Key Constants for RL

| Constant | Value | Use |
|----------|-------|-----|
| Tick duration | 250ms | Time per game tick |
| Ticks per second | 4 | Broadcast rate |
| Valid bet threshold | 20 ticks (5 sec) | Minimum hold time |
| House edge per tick | ~0.05% | Risk calculation |
| XP per valid bet | 1 XP / 0.001 SOL | Leveling calculation |

---

*Document created: December 25, 2025*
*Source: rugs.fun FAQ + User analysis*
