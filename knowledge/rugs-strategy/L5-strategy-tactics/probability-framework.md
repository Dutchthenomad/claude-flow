---
layer: 5
domain: strategy-tactics/probability
priority: P1
bot_relevant: true
validation_tier: reviewed
source_file: "RAG SUPERPACK/review data/probability_framework.md"
cross_refs:
  - L5-strategy-tactics/bankroll-management.md
  - L1-game-mechanics/provably-fair.md
  - L1-game-mechanics/WHAT-IT-IS-NOT.md
last_validated: 2025-12-24
---

# Probability Framework: Adaptive Statistical Models

## Executive Summary

This document establishes the mathematical foundation for side bet probability calculations, incorporating empirical timing variance and providing adaptive models that reflect real-world server behavior rather than theoretical specifications.

## Key Timing Findings

Based on analysis of 100 games (22,507 tick intervals):

| Metric | Value | Notes |
|--------|-------|-------|
| Mean tick duration | 271.5ms | 8.6% above theoretical 250ms |
| Median tick duration | 251.0ms | Very close to theoretical |
| Standard deviation | 295.3ms | High variability |
| 95th percentile | 237-269ms | Normal operating range |

---

## Base Probability Model

### Empirical Probability Curves

Probability that game ends within next 40 ticks:

| Tick Range | Probability | Zone |
|------------|-------------|------|
| 0-10 | 15% | Very Early |
| 10-50 | 18-28% | Early Game |
| 50-100 | 32-45% | Early-Mid |
| 100-200 | 50-70% | Mid Game |
| 200-300 | 74-86% | Late-Mid |
| 300-500 | 88-95% | Late Game |
| 500+ | 96%+ | Extreme Late |

### Interpolation Function

```javascript
function getBaseProbability(tickCount) {
  if (tickCount < 0) return 0.10;   // Presale
  if (tickCount > 500) return 0.96; // Extreme late

  const brackets = [
    [0, 0.15], [10, 0.18], [20, 0.22], [30, 0.25], [40, 0.28],
    [50, 0.32], [60, 0.35], [70, 0.38], [80, 0.42], [90, 0.45],
    [100, 0.50], [120, 0.55], [140, 0.60], [160, 0.65], [180, 0.70],
    [200, 0.74], [220, 0.77], [240, 0.80], [260, 0.83], [280, 0.86],
    [300, 0.88], [350, 0.91], [400, 0.93], [450, 0.95], [500, 0.96]
  ];

  // Linear interpolation between closest points
  for (let i = 0; i < brackets.length - 1; i++) {
    const [tick1, prob1] = brackets[i];
    const [tick2, prob2] = brackets[i + 1];

    if (tickCount >= tick1 && tickCount <= tick2) {
      const ratio = (tickCount - tick1) / (tick2 - tick1);
      return prob1 + (prob2 - prob1) * ratio;
    }
  }

  return 0.96;
}
```

---

## Strategic Probability Zones

| Zone | Probability Range | Label | Recommendation |
|------|------------------|-------|----------------|
| VERY_LOW | 0 - 16.7% | Avoid Zone | Do not bet |
| LOW | 16.7 - 25% | Caution Zone | Small bets only |
| MODERATE | 25 - 50% | Opportunity Zone | Standard betting |
| HIGH | 50 - 75% | Strong Zone | Increased bet size |
| VERY_HIGH | 75 - 90% | Excellent Zone | Aggressive betting |
| CERTAINTY | 90 - 100% | Mathematical Certainty | Maximum bet size |

---

## Expected Value Calculations

### Standard EV Formula

```javascript
function calculateExpectedValue(winProbability, betAmount) {
  const winOutcome = betAmount * 4;   // Net profit (400%)
  const loseOutcome = -betAmount;     // Total loss

  const ev = (winProbability * winOutcome) + ((1 - winProbability) * loseOutcome);

  return {
    expectedValue: ev,
    winScenario: winOutcome,
    loseScenario: loseOutcome,
    breakeven: ev >= 0
  };
}
```

### Breakeven Probability

**16.7%** - Minimum probability for positive expected value with 5:1 payout.

---

## Adaptive Timing Model

### Timing Adjustment Factors

```javascript
// Adaptation factors
this.timeExtensionFactor = avgInterval / 251; // How much longer than median
this.volatilityPenalty = Math.sqrt(variance) / avgInterval;
this.reliabilityScore = Math.max(0.3, 1 - this.volatilityPenalty);
```

### Adapted Probability

```javascript
function getAdaptedProbability(tickCount) {
  const baseProb = getBaseProbability(tickCount);

  // Longer ticks = more time for rug within window
  const timeBonus = (this.timeExtensionFactor - 1) * 0.3;

  // High volatility reduces confidence
  const volatilityPenalty = this.volatilityPenalty * 0.1;

  let adaptedProb = baseProb + timeBonus - volatilityPenalty;
  return Math.max(0.05, Math.min(0.98, adaptedProb));
}
```

---

## Martingale Sequence Analysis

### Sequence Success Probability

```javascript
function calculateAtLeastOneSuccess(probabilities) {
  const allFail = probabilities.reduce((product, prob) => product * (1 - prob), 1);
  return 1 - allFail;
}
```

### Example Sequences

| Sequence Length | Single Win Prob | Success Rate | Total Risk (base=0.001) |
|-----------------|-----------------|--------------|-------------------------|
| 5 | 50% | 96.88% | 0.031 SOL |
| 7 | 40% | 97.20% | 0.127 SOL |
| 9 | 35% | 98.65% | 0.511 SOL |
| 11 | 30% | 98.97% | 2.047 SOL |

---

## Quick Reference Table

| Tick Range | Base Probability | Zone | Minimum Bankroll (10x) |
|------------|------------------|------|------------------------|
| 0-50 | 15-28% | Avoid/Caution | - |
| 50-100 | 32-45% | Opportunity | 0.063 SOL |
| 100-200 | 50-70% | Strong | 0.031 SOL |
| 200-300 | 74-86% | Excellent | 0.016 SOL |
| 300-500 | 88-95% | Certainty | 0.008 SOL |
| 500+ | 96%+ | Mathematical | 0.004 SOL |

---

## Performance Tracking Metrics

### Accuracy Measurement

- **Brier Score**: Lower is better (0 = perfect, 1 = worst)
- **Binary Accuracy**: Percentage of correct predictions
- **Calibration**: Predicted probability matches actual outcome rate

---

## For Bot Development

**Key Parameters**:
- `baseProbabilities`: Tick-indexed probability array
- `reliabilityScore`: Current timing reliability (0.3-1.0)
- `adaptationFactors`: Timing adjustment multipliers

**Integration Points**:
- Update timing data on each tick
- Recalculate adapted probability in real-time
- Track prediction accuracy over time
- Adjust zone boundaries based on reliability

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
