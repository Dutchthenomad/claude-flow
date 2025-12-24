---
layer: 6
domain: statistical-baselines/volatility
priority: P1
bot_relevant: true
validation_tier: reviewed
source_file: "RAG SUPERPACK/review data/volatility-reference.md"
cross_refs:
  - L1-game-mechanics/provably-fair.md
  - L5-strategy-tactics/probability-framework.md
last_validated: 2025-12-24
---

# Volatility Reference Guide (Logarithmic Scale)

## Understanding the Logarithmic Volatility Curve

The relationship between price and volatility follows a square root function:
`volatility = 0.005 * min(10, sqrt(price))`

When viewed on a logarithmic scale, this relationship becomes more intuitive:
- Equal distances on the chart represent equal percentage changes (e.g., 1→2 has same visual distance as 10→20)
- The square root curve appears more linear and easier to understand
- The volatility cap at 100x is clearly visible

## Quick Reference Table

| Price | Volatility | Min Change | Max Change | Notes |
|-------|------------|------------|------------|-------|
| 1x    | 0.50%      | 0.00%*     | 3.50%      | Starting price |
| 2x    | 0.71%      | 0.00%*     | 3.71%      | × √2 increase from 1x |
| 4x    | 1.00%      | 0.00%*     | 4.00%      | × √2 increase from 2x |
| 9x    | 1.50%      | 0.00%*     | 4.50%      | × √2.25 increase from 4x |
| 16x   | 2.00%      | 0.00%*     | 5.00%      | × √1.78 increase from 9x |
| 25x   | 2.50%      | 0.50%      | 5.50%      | One-quarter to max volatility |
| 36x   | 3.00%      | 1.00%      | 6.00%      | × √1.44 increase from 25x |
| 49x   | 3.50%      | 1.50%      | 6.50%      | × √1.36 increase from 36x |
| 64x   | 4.00%      | 2.00%      | 7.00%      | × √1.31 increase from 49x |
| 81x   | 4.50%      | 2.50%      | 7.50%      | × √1.27 increase from 64x |
| 100x  | 5.00%      | 3.00%      | 8.00%      | Volatility cap reached |
| >100x | 5.00%      | 3.00%      | 8.00%      | No further increase |

*Min change is capped at 0% (cannot be negative)

## Logarithmic Pattern Insights

On a logarithmic scale, you can see that:

1. **Early Volatility Growth**: The steepest growth in volatility happens in the very early price range (1x to 4x)

2. **Perfect Squares**: Volatility values at perfect square prices (1, 4, 9, 16, 25...) show clear patterns:
   - 1x → 0.5%
   - 4x → 1.0%
   - 9x → 1.5%
   - 16x → 2.0%
   - 25x → 2.5%
   - ...and so on

3. **Doubling Pattern**: Each time the price multiplier quadruples (2²), the volatility doubles:
   - 1x → 0.5%
   - 4x → 1.0%
   - 16x → 2.0%
   - 64x → 4.0%

4. **Rule of Thumb**: You can approximate volatility as `0.5% × √price` up to 100x

## Game Strategy Implications

- **1x to 4x**: Relatively predictable with low volatility (0.5% to 1.0%)
- **4x to 25x**: Medium volatility zone (1.0% to 2.5%)
- **25x to 100x**: High volatility zone (2.5% to 5.0%)
- **Above 100x**: Maximum volatility zone (capped at 5.0%)

Remember that these volatility values are separate from the random 15-25% "big moves" that have a 12.5% chance of occurring each tick, and from the 0.5% chance of a rug pull each tick.

---

## For Bot Development

**Key Parameters**:
- `volatilityFunction`: `0.005 * Math.min(10, Math.sqrt(price))`
- `volatilityCap`: 100x price (5% max volatility)
- `bigMoveChance`: 12.5% per tick
- `bigMoveRange`: 15-25%

**Integration Points**:
- Calculate expected volatility based on current price
- Adjust position sizing inversely to volatility
- Use volatility zones for risk management

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
