---
layer: 5
domain: strategy-tactics/bankroll
priority: P1
bot_relevant: true
validation_tier: reviewed
source_file: "RAG SUPERPACK/review data/bankroll_management.md"
cross_refs:
  - L5-strategy-tactics/risk-hedging.md
  - L5-strategy-tactics/probability-framework.md
  - L1-game-mechanics/WHAT-IT-IS-NOT.md
last_validated: 2025-12-24
---

# Bankroll Management: Mathematical Certainty Zones

## Executive Summary

This document establishes the mathematical framework for bankroll-based certainty zones, where sufficient capital combined with proper strategy execution creates near-guaranteed profitability. The system leverages the 5:1 payout ratio and known probability distributions to eliminate risk through mathematical precision.

## Core Mathematical Principle

With adequate bankroll and disciplined execution, side betting becomes a mathematical certainty rather than gambling. The key insight: **compound probability of multiple attempts approaches 100% success**.

---

## Mathematical Foundation

### Certainty Thresholds by Bankroll

| Bankroll (SOL) | Max Sequence | Min Probability | Success Rate | Entry Tick |
|----------------|--------------|-----------------|--------------|------------|
| 0.127 | 7 steps | 50% | 99.22% | ~100 |
| 0.255 | 8 steps | 45% | 99.61% | ~80 |
| 0.511 | 9 steps | 40% | 99.80% | ~60 |
| 1.023 | 10 steps | 35% | 99.90% | ~50 |
| 2.047 | 11 steps | 30% | 99.95% | ~40 |
| 4.095 | 12 steps | 25% | 99.98% | ~30 |

### Core Formula

```javascript
// Probability of winning at least once in N attempts
function calculateSuccessProbability(singleWinProb, attempts) {
  const allFailProb = Math.pow(1 - singleWinProb, attempts);
  return 1 - allFailProb;
}

// Required bankroll for N attempts in doubling sequence
function calculateRequiredBankroll(baseBet, attempts) {
  let totalRisk = 0;
  let currentBet = baseBet;

  for (let i = 0; i < attempts; i++) {
    totalRisk += currentBet;
    currentBet *= 2;
  }

  return totalRisk;
}
```

---

## Bankroll Allocation Strategies

### Professional Allocation Framework

```javascript
const allocationRules = {
  emergency_reserve: 0.30,     // 30% never touched
  active_trading: 0.50,        // 50% for active trading
  opportunity_fund: 0.15,      // 15% for high-probability opportunities
  experiment_fund: 0.05        // 5% for testing new strategies
};
```

### Risk Levels

| Level | Max Risk Per Session | Required Success Rate | Min Probability |
|-------|---------------------|----------------------|-----------------|
| Ultra Conservative | 2% of bankroll | 99% | 90% |
| Conservative | 5% of bankroll | 95% | 75% |
| Moderate | 10% of bankroll | 90% | 60% |
| Aggressive | 20% of bankroll | 80% | 45% |

---

## Multi-Tier Bankroll System

| Tier | Bankroll Range (SOL) | Max Sequence | Available Strategies |
|------|---------------------|--------------|---------------------|
| MICRO | 0.063 - 0.127 | 6 | SafeZone, Conservative |
| SMALL | 0.127 - 0.511 | 8 | SafeZone, Conservative, ZoneBased |
| MEDIUM | 0.511 - 2.047 | 10 | Conservative, ZoneBased, Adaptive |
| LARGE | 2.047 - 8.191 | 12 | ZoneBased, Adaptive, ControlledMartingale |
| WHALE | 8.191+ | 15 | All, MathematicalCertainty, Professional |

---

## Risk Management Systems

### Dynamic Stop-Loss Levels

| Level | Trigger | Action |
|-------|---------|--------|
| Emergency | 50% loss | Stop immediately |
| Critical | 35% loss | Switch to ultra-conservative |
| Warning | 20% loss | Reduce position sizes |
| Caution | 10% loss | Monitor closely |

### Profit Protection

| Profit Level | Protection Amount |
|--------------|-------------------|
| +10% gain | Protect 10% of profits |
| +25% gain | Protect 25% of profits |
| +50% gain | Protect 50% of profits |
| +100% gain | Protect 75% of profits |

---

## Tier Progression Requirements

| Current Tier | Next Tier | Additional SOL | New Benefits |
|--------------|-----------|----------------|--------------|
| MICRO | SMALL | +0.064 | Enhanced sequence depth |
| SMALL | MEDIUM | +0.384 | Professional certainty |
| MEDIUM | LARGE | +1.536 | Advanced strategies |
| LARGE | WHALE | +6.144 | Mathematical dominance |

---

## Implementation Checklist

- [ ] Calculate maximum affordable sequence depth
- [ ] Determine entry tick for target success rate
- [ ] Set stop-loss levels based on bankroll tier
- [ ] Configure profit protection thresholds
- [ ] Track performance metrics per session
- [ ] Adjust allocation rules based on results

---

## For Bot Development

**Key Parameters**:
- `baseBet`: Minimum bet size (0.001 SOL)
- `payoutRatio`: 5:1 (400% net profit on win)
- `maxSequenceSteps`: Based on bankroll tier
- `safetyBuffer`: 1.2x (20% reserve)

**Integration Points**:
- Calculate certainty zones before each betting decision
- Track bankroll tier and available strategies
- Enforce stop-loss and profit protection rules
- Log all decisions for performance analysis

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
