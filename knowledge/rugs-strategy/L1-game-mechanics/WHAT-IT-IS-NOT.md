---
layer: 1
domain: game-mechanics/misconceptions
priority: P0-CRITICAL
bot_relevant: true
validation_tier: canonical
retrieval_boost: 2.0
trigger_phrases:
  - technical analysis
  - whale
  - liquidity
  - support level
  - resistance
  - order book
  - market maker
  - bid ask spread
  - volume analysis
  - chart pattern
last_validated: 2025-12-24
---

# What Rugs.fun IS NOT

> **LLM MISCONCEPTION GUARD** - Read this BEFORE applying any financial market reasoning to Rugs.fun gameplay.

---

## Core Truth

Rugs.fun is a **PRNG-based game that simulates meme coin trading**. It is NOT a real market. The price curve is **deterministic from the moment the game starts**.

---

## Concepts That DO NOT APPLY

### No Whales

There are no large holders manipulating price. The "price" is a PRNG-generated curve, not supply/demand dynamics. Other players' trades **do not move the price**.

**Wrong thinking:** "A whale just bought, price will pump"
**Correct thinking:** "Price follows predetermined PRNG curve regardless of player actions"

### No Liquidity Pools

There is no AMM, no bonding curve based on actual liquidity. The game simulates this visually but the mechanics are pure RNG.

**Wrong thinking:** "Low liquidity means high slippage"
**Correct thinking:** "Execution is fixed, there is no slippage from trade size"

### No Technical Analysis

- **No support/resistance levels** - price is predetermined, not emergent
- **No volume analysis** - volume doesn't affect price trajectory
- **No chart patterns** - curves are PRNG output, not market psychology
- **No trend analysis** - the "trend" is a predetermined curve
- **No momentum indicators** - RSI, MACD, etc. are meaningless here

**Wrong thinking:** "Price bounced off support at 25x"
**Correct thinking:** "PRNG happened to reverse at 25x, this was predetermined"

### No Market Microstructure

- **No bid-ask spread** - single price, instant execution
- **No slippage from size** - fixed execution regardless of amount
- **No front-running or MEV** - no mempool, no transaction ordering
- **No actual blockchain settlement during gameplay** - it's a game simulation
- **No order book depth** - there is no order book

### No Market Participants

- **No market makers** - no one providing liquidity
- **No arbitrageurs** - no price discovery mechanism
- **No institutional players** - just individual game participants
- **No smart money flow** - money flow doesn't affect price

---

## What It ACTUALLY Is

A game where:

1. **Server generates a price curve** via seeded PRNG at game start
2. **Curve includes predetermined rug point** - when the game ends
3. **Players bet on timing** - enter/exit this predetermined curve
4. **"Rug" is predetermined** - not triggered by player behavior
5. **Other players' trades are cosmetic** - they don't change the curve

---

## Where Edge ACTUALLY Comes From

### Valid Edge Sources

| Source | Why It Works |
|--------|--------------|
| **Timing optimization** | Statistical patterns in PRNG output |
| **Bankroll management** | Kelly criterion, position sizing |
| **Phase awareness** | COOLDOWN → PRESALE → ACTIVE → RUGGED |
| **Latency management** | Execution timing relative to rug |
| **Statistical baselines** | Empirical tick/price distributions |

### Invalid "Edge" (Don't Pursue)

| Approach | Why It Fails |
|----------|--------------|
| Technical analysis | Price is predetermined |
| Whale tracking | No whales, no price impact |
| Volume analysis | Volume doesn't affect curve |
| Order flow | No order book |
| Sentiment analysis | Player behavior doesn't affect outcome |

---

## For Bot Development

When designing features, rewards, or strategies:

**Ask:** "Does this assume price responds to market forces?"
- If YES → Invalid assumption, redesign
- If NO → May be valid, validate empirically

**Valid bot features:**
- Tick count since game start
- Current price vs historical PRNG distributions
- Time since last player action (for timing, not price prediction)
- Own position P&L
- Latency statistics

**Invalid bot features:**
- "Whale activity" indicators
- Volume-weighted anything
- Order book imbalance
- Bid-ask spread
- Any TA indicator (RSI, MACD, Bollinger, etc.)

---

## Common LLM Hallucinations

When the agent says... | Correct response
-----------------------|------------------
"The whale activity suggests..." | There are no whales. Price is PRNG.
"Based on the volume..." | Volume doesn't affect price.
"The support level at..." | There are no support levels. Price is predetermined.
"Order flow indicates..." | There is no order book.
"Market makers are..." | There are no market makers.
"Liquidity is..." | There is no liquidity pool.

---

## Summary

**Rugs.fun is a PRNG timing game, not a market.**

All market-based reasoning is invalid. Edge comes from:
1. Understanding PRNG statistical properties
2. Optimal bankroll management
3. Latency-aware execution timing
4. Empirical pattern recognition in game outcomes

---

*Last validated: 2025-12-24*
