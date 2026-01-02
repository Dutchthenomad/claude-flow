# 02 - Probability Framework: Adaptive Statistical Models

## Executive Summary
This document establishes the mathematical foundation for side bet probability calculations, incorporating the critical timing variance discovery and providing adaptive models that reflect real-world server behavior rather than theoretical specifications.

## Key Finding Integration
Based on analysis of 100 games (22,507 tick intervals), the empirical timing data shows:
- **Mean tick duration**: 271.5ms (8.6% above theoretical 250ms)
- **Median tick duration**: 251.0ms (very close to theoretical)
- **Standard deviation**: 295.3ms (high variability)
- **95% of ticks**: Between 237-269ms

This timing variance requires adaptive models while maintaining mathematical precision for strategic decision-making.

---

## Base Probability Model

### 1. Empirical Probability Curves

#### 1.1 Historical Data Foundation
Based on analysis of 2000+ games, probability that game ends within next 40 ticks:

```javascript
const BASE_PROBABILITIES = {
  // Early Game (0-50 ticks)
  tick_0_10:   0.15,   // 15% - Very early, low rug chance
  tick_10_20:  0.18,   // 18% - Still building momentum
  tick_20_30:  0.22,   // 22% - Early momentum phase
  tick_30_40:  0.25,   // 25% - Late early game
  tick_40_50:  0.28,   // 28% - Transitioning to mid
  
  // Early-Mid Game (50-100 ticks)  
  tick_50_60:  0.32,   // 32% - Early-mid phase
  tick_60_70:  0.35,   // 35% - Building pressure
  tick_70_80:  0.38,   // 38% - Increasing risk
  tick_80_90:  0.42,   // 42% - Mid-game tension
  tick_90_100: 0.45,   // 45% - Late early-mid
  
  // Mid Game (100-200 ticks)
  tick_100_120: 0.50,  // 50% - True mid-game
  tick_120_140: 0.55,  // 55% - Pressure building
  tick_140_160: 0.60,  // 60% - High tension zone
  tick_160_180: 0.65,  // 65% - Late mid-game
  tick_180_200: 0.70,  // 70% - Approaching danger
  
  // Late-Mid Game (200-300 ticks)
  tick_200_220: 0.74,  // 74% - Early danger zone
  tick_220_240: 0.77,  // 77% - Significant risk
  tick_240_260: 0.80,  // 80% - High danger
  tick_260_280: 0.83,  // 83% - Very high risk
  tick_280_300: 0.86,  // 86% - Extreme tension
  
  // Late Game (300-500 ticks)
  tick_300_350: 0.88,  // 88% - Late game territory
  tick_350_400: 0.91,  // 91% - Very dangerous
  tick_400_450: 0.93,  // 93% - Extremely high risk
  tick_450_500: 0.95,  // 95% - Near-certain zone
  
  // Extreme Late (500+ ticks)
  tick_500_plus: 0.96  // 96% - Mathematical certainty
};
```

#### 1.2 Interpolation Function
```javascript
function getBaseProbability(tickCount) {
  // Handle extreme cases
  if (tickCount < 0) return 0.10;      // Presale
  if (tickCount > 500) return 0.96;    // Extreme late
  
  // Find surrounding probability points
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
  
  return 0.96; // Default to highest probability
}
```

### 2. Adaptive Timing Model

#### 2.1 Timing Adjustment Framework
```javascript
class AdaptiveProbabilityEngine {
  constructor() {
    this.tickHistory = [];
    this.reliabilityScore = 1.0;
    this.adaptationFactors = new Map();
  }
  
  updateTimingData(tickInterval, tickNumber) {
    this.tickHistory.push({ interval: tickInterval, tick: tickNumber, timestamp: Date.now() });
    
    // Maintain rolling window
    if (this.tickHistory.length > 100) {
      this.tickHistory.shift();
    }
    
    this.recalculateAdaptation();
  }
  
  recalculateAdaptation() {
    const recentIntervals = this.tickHistory.slice(-20).map(t => t.interval);
    const avgInterval = recentIntervals.reduce((sum, i) => sum + i, 0) / recentIntervals.length;
    const variance = this.calculateVariance(recentIntervals);
    
    // Adaptation factors
    this.timeExtensionFactor = avgInterval / 251; // How much longer than empirical median
    this.volatilityPenalty = Math.sqrt(variance) / avgInterval; // Coefficient of variation
    this.reliabilityScore = Math.max(0.3, 1 - this.volatilityPenalty);
  }
  
  getAdaptedProbability(tickCount) {
    const baseProb = getBaseProbability(tickCount);
    
    // Longer ticks = more time for rug to occur within window
    const timeBonus = (this.timeExtensionFactor - 1) * 0.3; // 30% weight to timing
    
    // High volatility reduces confidence
    const volatilityPenalty = this.volatilityPenalty * 0.1;
    
    // Apply adaptations
    let adaptedProb = baseProb + timeBonus - volatilityPenalty;
    
    // Ensure bounds
    return Math.max(0.05, Math.min(0.98, adaptedProb));
  }
}
```

#### 2.2 Confidence Intervals
```javascript
function calculateConfidenceInterval(probability, sampleSize = 100) {
  const standardError = Math.sqrt((probability * (1 - probability)) / sampleSize);
  const z95 = 1.96; // 95% confidence
  
  return {
    lower: Math.max(0, probability - (z95 * standardError)),
    upper: Math.min(1, probability + (z95 * standardError)),
    margin: z95 * standardError
  };
}
```

### 3. Expected Value Calculations

#### 3.1 Standard EV Formula
```javascript
function calculateExpectedValue(winProbability, betAmount) {
  const winOutcome = betAmount * 4;      // Net profit (400%)
  const loseOutcome = -betAmount;        // Total loss
  
  const ev = (winProbability * winOutcome) + ((1 - winProbability) * loseOutcome);
  
  return {
    expectedValue: ev,
    winScenario: winOutcome,
    loseScenario: loseOutcome,
    breakeven: ev >= 0,
    confidence: calculateConfidenceInterval(winProbability)
  };
}
```

#### 3.2 Risk-Adjusted EV
```javascript
function calculateRiskAdjustedEV(winProbability, betAmount, reliabilityScore) {
  const baseEV = calculateExpectedValue(winProbability, betAmount);
  
  // Penalize EV based on timing reliability
  const reliabilityPenalty = (1 - reliabilityScore) * 0.2; // 20% max penalty
  const adjustedEV = baseEV.expectedValue * (1 - reliabilityPenalty);
  
  return {
    ...baseEV,
    adjustedEV: adjustedEV,
    reliabilityScore: reliabilityScore,
    penalty: reliabilityPenalty
  };
}
```

### 4. Multi-Bet Probability Models

#### 4.1 Consecutive Bet Success Probability
```javascript
function calculateConsecutiveSuccess(probabilities) {
  // Probability of winning ALL bets in sequence
  return probabilities.reduce((product, prob) => product * prob, 1);
}

function calculateAtLeastOneSuccess(probabilities) {
  // Probability of winning at least one bet
  const allFail = probabilities.reduce((product, prob) => product * (1 - prob), 1);
  return 1 - allFail;
}
```

#### 4.2 Martingale Sequence Analysis
```javascript
function analyzeMartingaleSequence(baseBet, maxBets, probability) {
  let totalRisk = 0;
  let currentBet = baseBet;
  const sequence = [];
  
  for (let i = 0; i < maxBets; i++) {
    totalRisk += currentBet;
    
    const ev = calculateExpectedValue(probability, currentBet);
    const cumulativeRisk = totalRisk;
    const successProb = Math.pow(1 - (1 - probability), i + 1); // At least one success
    
    sequence.push({
      betNumber: i + 1,
      betAmount: currentBet,
      cumulativeRisk: cumulativeRisk,
      expectedValue: ev.expectedValue,
      successProbability: successProb,
      failureProbability: Math.pow(1 - probability, i + 1)
    });
    
    currentBet *= 2; // Double for next bet
  }
  
  return sequence;
}
```

### 5. Zone-Based Probability System

#### 5.1 Strategic Zone Definitions
```javascript
const PROBABILITY_ZONES = {
  VERY_LOW: {
    range: [0, 0.167],
    label: "Avoid Zone",
    description: "Negative EV, high risk",
    recommendation: "Do not bet",
    color: "#DC2626" // Red
  },
  
  LOW: {
    range: [0.167, 0.25],
    label: "Caution Zone", 
    description: "Marginal EV, proceed carefully",
    recommendation: "Small bets only",
    color: "#F59E0B" // Amber
  },
  
  MODERATE: {
    range: [0.25, 0.50],
    label: "Opportunity Zone",
    description: "Positive EV, reasonable risk",
    recommendation: "Standard betting",
    color: "#10B981" // Green
  },
  
  HIGH: {
    range: [0.50, 0.75],
    label: "Strong Zone",
    description: "Good EV, favorable odds",
    recommendation: "Increased bet size",
    color: "#059669" // Dark Green
  },
  
  VERY_HIGH: {
    range: [0.75, 0.90],
    label: "Excellent Zone",
    description: "High EV, low risk",
    recommendation: "Aggressive betting",
    color: "#047857" // Very Dark Green
  },
  
  CERTAINTY: {
    range: [0.90, 1.0],
    label: "Mathematical Certainty",
    description: "Near-guaranteed success",
    recommendation: "Maximum bet size",
    color: "#064E3B" // Darkest Green
  }
};

function getZoneForProbability(probability) {
  for (const [zoneName, zone] of Object.entries(PROBABILITY_ZONES)) {
    if (probability >= zone.range[0] && probability < zone.range[1]) {
      return { name: zoneName, ...zone };
    }
  }
  return PROBABILITY_ZONES.CERTAINTY; // Default to highest
}
```

#### 5.2 Dynamic Zone Boundaries
```javascript
function getDynamicZoneBoundaries(reliabilityScore) {
  // Adjust zone boundaries based on timing reliability
  const adjustment = (1 - reliabilityScore) * 0.05; // Max 5% adjustment
  
  const adjustedZones = {};
  for (const [name, zone] of Object.entries(PROBABILITY_ZONES)) {
    adjustedZones[name] = {
      ...zone,
      range: [
        Math.max(0, zone.range[0] + adjustment),
        Math.min(1, zone.range[1] + adjustment)
      ]
    };
  }
  
  return adjustedZones;
}
```

### 6. Historical Performance Tracking

#### 6.1 Accuracy Measurement
```javascript
class ProbabilityTracker {
  constructor() {
    this.predictions = [];
    this.outcomes = [];
  }
  
  recordPrediction(tickCount, predictedProbability, adaptationFactors) {
    this.predictions.push({
      tick: tickCount,
      predicted: predictedProbability,
      timestamp: Date.now(),
      adaptations: adaptationFactors
    });
  }
  
  recordOutcome(gameEndTick, betStartTick) {
    const actualOutcome = (gameEndTick - betStartTick) <= 40 ? 1 : 0;
    this.outcomes.push({
      outcome: actualOutcome,
      duration: gameEndTick - betStartTick,
      timestamp: Date.now()
    });
    
    this.calculateAccuracy();
  }
  
  calculateAccuracy() {
    if (this.predictions.length !== this.outcomes.length) return;
    
    let totalError = 0;
    let correctPredictions = 0;
    
    for (let i = 0; i < this.predictions.length; i++) {
      const predicted = this.predictions[i].predicted;
      const actual = this.outcomes[i].outcome;
      
      // Brier Score (lower is better)
      totalError += Math.pow(predicted - actual, 2);
      
      // Binary accuracy (predicted >0.5 and actual = 1, or predicted <=0.5 and actual = 0)
      if ((predicted > 0.5 && actual === 1) || (predicted <= 0.5 && actual === 0)) {
        correctPredictions++;
      }
    }
    
    this.brierScore = totalError / this.predictions.length;
    this.accuracy = correctPredictions / this.predictions.length;
    
    return {
      brierScore: this.brierScore,     // 0 = perfect, 1 = worst
      accuracy: this.accuracy,          // 0-1, higher is better
      calibration: this.calculateCalibration()
    };
  }
  
  calculateCalibration() {
    // Group predictions by probability ranges and check if they match outcomes
    const bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
    const calibrationData = [];
    
    for (let i = 0; i < bins.length - 1; i++) {
      const lower = bins[i];
      const upper = bins[i + 1];
      
      const inBin = this.predictions
        .map((pred, idx) => ({ pred: pred.predicted, outcome: this.outcomes[idx].outcome }))
        .filter(item => item.pred >= lower && item.pred < upper);
      
      if (inBin.length > 0) {
        const avgPrediction = inBin.reduce((sum, item) => sum + item.pred, 0) / inBin.length;
        const avgOutcome = inBin.reduce((sum, item) => sum + item.outcome, 0) / inBin.length;
        
        calibrationData.push({
          range: [lower, upper],
          predicted: avgPrediction,
          actual: avgOutcome,
          count: inBin.length,
          calibrated: Math.abs(avgPrediction - avgOutcome) < 0.1
        });
      }
    }
    
    return calibrationData;
  }
}
```

### 7. Real-Time Probability Updates

#### 7.1 Streaming Calculation Engine
```javascript
class RealTimeProbabilityEngine {
  constructor() {
    this.adaptiveEngine = new AdaptiveProbabilityEngine();
    this.tracker = new ProbabilityTracker();
    this.currentProbabilities = new Map();
  }
  
  onTickUpdate(tickData) {
    const { tickNumber, interval, timestamp } = tickData;
    
    // Update timing models
    this.adaptiveEngine.updateTimingData(interval, tickNumber);
    
    // Recalculate probability for current tick
    const probability = this.adaptiveEngine.getAdaptedProbability(tickNumber);
    const zone = getZoneForProbability(probability);
    const ev = calculateRiskAdjustedEV(probability, 0.001, this.adaptiveEngine.reliabilityScore);
    
    // Store current calculation
    this.currentProbabilities.set(tickNumber, {
      probability,
      zone,
      expectedValue: ev,
      reliability: this.adaptiveEngine.reliabilityScore,
      timestamp
    });
    
    return {
      tick: tickNumber,
      probability: probability,
      zone: zone.name,
      expectedValue: ev.adjustedEV,
      confidence: ev.confidence,
      reliability: this.adaptiveEngine.reliabilityScore
    };
  }
  
  getProbabilityTrend(lookback = 10) {
    const recentTicks = Array.from(this.currentProbabilities.entries())
      .slice(-lookback)
      .map(([tick, data]) => ({ tick, ...data }));
    
    if (recentTicks.length < 2) return { trend: "insufficient_data" };
    
    const first = recentTicks[0].probability;
    const last = recentTicks[recentTicks.length - 1].probability;
    const change = last - first;
    const rate = change / recentTicks.length;
    
    return {
      trend: change > 0.05 ? "increasing" : change < -0.05 ? "decreasing" : "stable",
      change: change,
      rate: rate,
      acceleration: this.calculateAcceleration(recentTicks)
    };
  }
  
  calculateAcceleration(ticks) {
    if (ticks.length < 3) return 0;
    
    const rates = [];
    for (let i = 1; i < ticks.length; i++) {
      rates.push(ticks[i].probability - ticks[i-1].probability);
    }
    
    let acceleration = 0;
    for (let i = 1; i < rates.length; i++) {
      acceleration += rates[i] - rates[i-1];
    }
    
    return acceleration / (rates.length - 1);
  }
}
```

### 8. Advanced Probability Models

#### 8.1 Volatility-Adjusted Probabilities
```javascript
function calculateVolatilityAdjustment(gameVolatility, playerCount, whaleConcentration) {
  // Higher volatility often correlates with earlier rugs
  const volatilityFactor = Math.min(gameVolatility / 0.1, 2.0); // Cap at 2x
  
  // More players = more stability = later rugs
  const playerFactor = Math.max(0.5, 1 - (playerCount - 10) / 100);
  
  // High whale concentration = potential for sudden exits
  const whaleFactor = 1 + (whaleConcentration * 0.3);
  
  return volatilityFactor * playerFactor * whaleFactor;
}
```

#### 8.2 Meta-Algorithm Detection
```javascript
function detectMetaAlgorithmInfluence(recentGames, currentTick) {
  // Analyze recent game patterns for meta-algorithm intervention
  const shortGames = recentGames.filter(g => g.duration < 30).length;
  const longGames = recentGames.filter(g => g.duration > 300).length;
  const extremePayouts = recentGames.filter(g => g.peakMultiplier > 50).length;
  
  // High concentration of short games suggests treasury protection
  const shortGameRatio = shortGames / recentGames.length;
  const treasuryProtectionSignal = shortGameRatio > 0.6 ? 1.5 : 1.0;
  
  // Recent extreme payouts increase probability of correction
  const extremePayoutPenalty = extremePayouts > 0 ? 1.2 : 1.0;
  
  return {
    adjustment: treasuryProtectionSignal * extremePayoutPenalty,
    confidence: Math.min(shortGameRatio + (extremePayouts * 0.1), 1.0),
    signals: {
      shortGameRatio,
      treasuryProtection: treasuryProtectionSignal > 1,
      extremePayouts: extremePayouts
    }
  };
}
```

---

## Probability Lookup Tables

### Quick Reference Table
| Tick Range | Base Probability | Zone | Minimum Bankroll (10x) | 
|------------|------------------|------|-------------------------|
| 0-50       | 15-28%          | Avoid/Caution | - |
| 50-100     | 32-45%          | Opportunity | 0.063 SOL |
| 100-200    | 50-70%          | Strong | 0.031 SOL |
| 200-300    | 74-86%          | Excellent | 0.016 SOL |
| 300-500    | 88-95%          | Certainty | 0.008 SOL |
| 500+       | 96%+            | Mathematical | 0.004 SOL |

### Implementation Priority Checklist
- [ ] Basic probability interpolation function
- [ ] Adaptive timing adjustment system
- [ ] Expected value calculations with confidence intervals
- [ ] Zone-based classification system
- [ ] Real-time probability updates
- [ ] Historical accuracy tracking
- [ ] Advanced volatility adjustments
- [ ] Meta-algorithm detection algorithms

---

*Next: [03-websocket-integration.md](./03-websocket-integration.md) - Technical event handling and real-time data processing*