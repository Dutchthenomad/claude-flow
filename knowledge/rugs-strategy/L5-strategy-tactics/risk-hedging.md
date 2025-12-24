---
layer: 5
domain: strategy-tactics/hedging
priority: P1
bot_relevant: true
validation_tier: reviewed
source_file: "RAG SUPERPACK/review data/risk_hedging_systems.md"
cross_refs:
  - L5-strategy-tactics/bankroll-management.md
  - L5-strategy-tactics/probability-framework.md
  - L1-game-mechanics/WHAT-IT-IS-NOT.md
last_validated: 2025-12-24
---

# Risk Hedging Systems: Combined Position Optimization

## Executive Summary

This document presents advanced risk hedging strategies that combine main game positions with side bets to create superior risk-adjusted returns. By leveraging the mathematical relationship between main game volatility and side bet probabilities, sophisticated hedging systems can dramatically reduce overall portfolio risk while maintaining profit potential.

## Hedging Theory Foundation

**Core Principle**: Main game positions and side bets have inverse correlation patterns that can be exploited for risk reduction.

- **Main Game Risk**: Price volatility and timing risk
- **Side Bet Risk**: Probability estimation and gap risk
- **Combined Opportunity**: Offsetting risk profiles create hedging potential

---

## Mathematical Hedging Framework

### Risk Profile Correlations

| Correlation | Value | Description |
|-------------|-------|-------------|
| Price volatility vs rug probability | -0.65 | Higher volatility = higher rug chance |
| Position size vs hedge ratio | 0.80 | Larger positions need more hedging |
| Hold time vs gap risk | 0.45 | Longer holds = more gap exposure |
| Game phase vs hedge effectiveness | 0.90 | Later phases = better hedging |

### Optimal Hedge Ratio Calculation

```javascript
function calculateOptimalHedgeRatio(mainPosition, currentTick, volatility) {
  const rugProbability = getBaseProbability(currentTick);
  const volatilityAdjustment = Math.min(volatility / 0.1, 2.0);
  const positionRisk = calculatePositionRisk(mainPosition);
  const timeDecay = calculateTimeDecay(currentTick);

  const baseHedgeRatio = rugProbability * 0.3; // 30% of rug probability
  const adjustedRatio = baseHedgeRatio * volatilityAdjustment * positionRisk * timeDecay;

  return Math.min(0.95, Math.max(0.05, adjustedRatio)); // Constrain to 5-95%
}
```

---

## Hedge Allocation Strategies

| Strategy | Main Allocation | Side Allocation | Hedge Ratio | Rebalance Threshold |
|----------|-----------------|-----------------|-------------|---------------------|
| Conservative | 40% | 20% | 50% | 10% |
| Balanced | 50% | 25% | 40% | 15% |
| Aggressive | 60% | 30% | 30% | 20% |
| Opportunistic | 70% | 20% | 25% | 25% |

---

## Hedging Techniques

### Perfect Hedge

Eliminates main game timing risk through precise side bet sizing.

```javascript
function calculatePerfectHedge(mainPosition, rugProbability) {
  const potentialLoss = mainPosition.currentValue;
  const sideBetPayout = 4; // 400% return
  const requiredSideBetSize = potentialLoss / sideBetPayout;
  return requiredSideBetSize / rugProbability;
}
```

### Partial Hedge

Reduces risk while maintaining upside potential. Use ratios: 25%, 50%, 75%.

### Volatility-Based Hedging

| Volatility Level | Threshold | Hedge Multiplier |
|------------------|-----------|------------------|
| Low | ≤5% | 0.50x |
| Medium | ≤10% | 1.00x |
| High | ≤20% | 1.50x |
| Extreme | >20% | 2.50x |

### Time-Decay Hedging

| Time Phase | Tick Range | Hedge Multiplier |
|------------|------------|------------------|
| Early | 0-50 | 0.30x |
| Early-Mid | 50-100 | 0.60x |
| Mid | 100-200 | 1.00x |
| Late-Mid | 200-300 | 1.40x |
| Late | 300-500 | 2.00x |
| Extreme | 500+ | 3.00x |

---

## Hedge Strategy Selection Matrix

| Market Condition | Position Size | Recommended Strategy | Hedge Ratio |
|------------------|---------------|---------------------|-------------|
| Low Vol + Early | Small (<0.1 SOL) | No Hedge | 0% |
| Low Vol + Late | Small (<0.1 SOL) | Partial Hedge | 25% |
| Medium Vol + Any | Medium (0.1-0.5 SOL) | Partial Hedge | 50% |
| High Vol + Any | Large (>0.5 SOL) | Perfect Hedge | 75-100% |
| Extreme Vol | Any | Perfect Hedge + Exit | 100% |

---

## Performance Tracking

### Key Metrics

- **Hedge Effectiveness**: How much loss was offset (0-100%)
- **Cost Efficiency**: Net benefit vs hedge cost (ROI)
- **Success Rate**: Percentage of hedges that provided value
- **Net Benefit**: Total savings minus total costs

### Performance Thresholds

| Metric | Excellent | Good | Needs Improvement |
|--------|-----------|------|-------------------|
| Success Rate | >80% | >60% | <60% |
| Net Benefit | Positive | Positive | Negative |
| Avg Effectiveness | >70% | >50% | <50% |

---

## Implementation Checklist

### Core Features
- [ ] Perfect hedge calculation system
- [ ] Partial hedge ratio optimization
- [ ] Dynamic rebalancing triggers
- [ ] Volatility-based adjustments
- [ ] Time decay compensation

### Advanced Features
- [ ] Multi-position correlation analysis
- [ ] Performance tracking and optimization
- [ ] Adaptive hedge ratio adjustment
- [ ] Emergency hedge protocols
- [ ] Real-time hedge monitoring

---

## For Bot Development

**Key Parameters**:
- `hedgeThreshold`: Minimum probability for hedging (default: 0.30)
- `maxHedgeRatio`: Maximum hedge allocation (default: 0.95)
- `rebalanceThreshold`: Deviation trigger for rebalancing

**Integration Points**:
- Calculate hedge ratio on each tick update
- Track main position value and side bet exposure
- Trigger rebalancing when deviation exceeds threshold
- Log hedge performance for optimization

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
