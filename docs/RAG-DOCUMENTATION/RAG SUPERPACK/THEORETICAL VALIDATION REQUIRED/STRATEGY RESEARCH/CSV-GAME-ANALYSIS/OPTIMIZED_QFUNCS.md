# Optimized Q-Learning Functions: Side Bet Chain Integration

## Executive Summary

This document outlines the corrected reward function framework and Q-learning system architecture that properly integrates the side bet chain mechanics, 5-tick cooldown system, and progressive PnL calculations for Rugs.fun side bet optimization. The system is designed to win in as few chain links as possible while avoiding maximum exposure.

---

## Core Side Bet Mechanics Integration

### **Side Bet Game Rules**
- **Payout Ratio**: 5:1 (not 2:1 like standard martingale)
- **Cooldown Period**: 5 ticks between consecutive side bets
- **Chaining Capability**: Multiple side bets per game allowed
- **Breakeven Point**: 4 consecutive losses (not 1 like standard martingale)
- **Game End Win**: If game ends during active side bet, player wins 5:1 payout
- **Chain Risk**: Each additional bet in chain increases total exposure exponentially

### **Progressive Betting Systems**

#### **Martingale Progression**
```
Bet 1: 0.001 SOL    PnL: -0.001 / +0.004
Bet 2: 0.002 SOL    PnL: -0.003 / +0.007
Bet 3: 0.004 SOL    PnL: -0.007 / +0.013
Bet 4: 0.008 SOL    PnL: -0.015 / +0.025 (Breakeven Point)
Bet 5: 0.016 SOL    PnL: -0.031 / +0.049
Bet 6: 0.032 SOL    PnL: -0.063 / +0.097
Bet 7: 0.064 SOL    PnL: -0.127 / +0.193
```

#### **Fibonacci Progression**
```
Bet 1: 0.001 SOL    PnL: -0.001 / +0.004
Bet 2: 0.002 SOL    PnL: -0.003 / +0.007
Bet 3: 0.003 SOL    PnL: -0.006 / +0.009
Bet 4: 0.005 SOL    PnL: -0.009 / +0.016 (Breakeven Point)
Bet 5: 0.008 SOL    PnL: -0.017 / +0.040
Bet 6: 0.013 SOL    PnL: -0.030 / +0.035
Bet 7: 0.021 SOL    PnL: -0.051 / +0.054
```

---

## Revised Reward Function Framework

### **Chain Length Rewards (Inverse to Chain Length - Fewer Links = Higher Reward)**
```
Chain Length 1: +10.0 reward (optimal - win immediately)
Chain Length 2: +8.0 reward (excellent - win in 2 bets)
Chain Length 3: +6.0 reward (good - win in 3 bets)
Chain Length 4: +4.0 reward (breakeven point - neutral)
Chain Length 5: +2.0 reward (poor - win in 5 bets)
Chain Length 6: +1.0 reward (very poor - win in 6 bets)
Chain Length 7: +0.5 reward (terrible - win in 7 bets)
```

### **Progressive Loss Penalties (Increasing with Chain Length)**
```
Chain Length 1 Loss: -2.0 (lost 0.001)
Chain Length 2 Loss: -4.0 (lost 0.003)
Chain Length 3 Loss: -6.0 (lost 0.007)
Chain Length 4 Loss: -8.0 (lost 0.015)
Chain Length 5 Loss: -12.0 (lost 0.031)
Chain Length 6 Loss: -16.0 (lost 0.063)
Chain Length 7+ Loss: -20.0 (lost 0.127+) - WORST OUTCOME
```

### **Cooldown Penalty (Increasing with Chain Length)**
```
Chain Length 1: -0.5 penalty (minimal cooldown impact)
Chain Length 2: -1.0 penalty
Chain Length 3: -1.5 penalty
Chain Length 4: -2.0 penalty
Chain Length 5: -2.5 penalty
Chain Length 6: -3.0 penalty
Chain Length 7+: -4.0 penalty (cooldown becomes critical)
```

### **Breakeven Point (Chain Length 4)**
```
Breakeven Reward: +0.0 (neutral - not good, not bad)
- Martingale: -0.015 loss potential, +0.025 profit potential
- Fibonacci: -0.009 loss potential, +0.016 profit potential
```

---

## Enhanced Q-Learning State Space

### **Updated State Dimensions:**
```
State = (Duration_Bucket, Treasury_Pressure, Sweet_Spot_State, Chain_Length, Progression_Type, Cooldown_Status)
```

#### **Duration Buckets (15 states) - Non-Overlapping:**
```
Bucket 0: 0-40 ticks (0-10s) - Side bet window 1
Bucket 1: 41-80 ticks (10-20s) - Side bet window 2  
Bucket 2: 81-120 ticks (20-30s) - Side bet window 3
Bucket 3: 121-160 ticks (30-40s) - Side bet window 4
Bucket 4: 161-200 ticks (40-50s) - Side bet window 5
Bucket 5: 201-240 ticks (50-60s) - Side bet window 6
Bucket 6: 241-280 ticks (60-70s) - Side bet window 7
Bucket 7: 281-320 ticks (70-80s) - Side bet window 8
Bucket 8: 321-360 ticks (80-90s) - Side bet window 9
Bucket 9: 361-400 ticks (90-100s) - Side bet window 10
Bucket 10: 401-500 ticks (100-125s) - Extended games
Bucket 11: 501-600 ticks (125-150s) - Long games
Bucket 12: 601-800 ticks (150-200s) - Very long games
Bucket 13: 801-1000 ticks (200-250s) - Ultra long games
Bucket 14: 1000+ ticks (250s+) - Extreme duration games
```

#### **Treasury Pressure (5 states):**
```
Level 0: Normal (no recent max payouts)
Level 1: Low Pressure (1-2 recent max payouts)
Level 2: Medium Pressure (3-4 recent max payouts)
Level 3: High Pressure (5+ recent max payouts)
Level 4: Recovery Protocol Active (post-max-payout game)
```

#### **Sweet Spot State (5 states):**
```
None: No sweet spot activated
Conservative: 4.0x-8.0x thresholds activated
Moderate: 9.0x-18.0x thresholds activated
Aggressive: 25.0x-60.0x thresholds activated
Ultra: 80.0x+ thresholds activated
```

#### **Chain Length (7 states):**
```
0: No active chain
1: First bet in chain
2: Second bet in chain
3: Third bet in chain
4: Fourth bet in chain (breakeven point)
5: Fifth bet in chain
6+: Extended chain (high risk)
```

#### **Progression Type (2 states):**
```
Martingale: 0.001 → 0.002 → 0.004 → 0.008 → 0.016 → 0.032 → 0.064
Fibonacci: 0.001 → 0.002 → 0.003 → 0.005 → 0.008 → 0.013 → 0.021
```

#### **Cooldown Status (2 states):**
```
Ready: Can place side bet immediately
Cooldown: Must wait 5 ticks before next bet
```

### **Updated State Space Calculation:**
```
Duration Buckets: 15 states
Treasury Pressure: 5 states
Sweet Spot State: 5 states
Chain Length: 7 states
Progression Type: 2 states
Cooldown Status: 2 states
Total: 15 × 5 × 5 × 7 × 2 × 2 = 10,500 states
```

---

## Action Space (Simplified to 2 Progression Types)

### **Martingale Actions:**
```
BET_MARTINGALE_001: 0.001 SOL (start/reset chain)
BET_MARTINGALE_002: 0.002 SOL (chain length 2)
BET_MARTINGALE_004: 0.004 SOL (chain length 3)
BET_MARTINGALE_008: 0.008 SOL (chain length 4 - breakeven)
BET_MARTINGALE_016: 0.016 SOL (chain length 5)
BET_MARTINGALE_032: 0.032 SOL (chain length 6)
BET_MARTINGALE_064: 0.064 SOL (chain length 7+)
SKIP_MARTINGALE: No bet (exit chain)
```

### **Fibonacci Actions:**
```
BET_FIBONACCI_001: 0.001 SOL (start/reset chain)
BET_FIBONACCI_002: 0.002 SOL (chain length 2)
BET_FIBONACCI_003: 0.003 SOL (chain length 3)
BET_FIBONACCI_005: 0.005 SOL (chain length 4 - breakeven)
BET_FIBONACCI_008: 0.008 SOL (chain length 5)
BET_FIBONACCI_013: 0.013 SOL (chain length 6)
BET_FIBONACCI_021: 0.021 SOL (chain length 7+)
SKIP_FIBONACCI: No bet (exit chain)
```

---

## Example Q-Table Entries (Revised)

### **Optimal Scenario (Chain Length 1 Win):**
```
State: (Bucket_0, High_Pressure, Ultra_Sweet_Spot, Chain_Length_1, Martingale, Ready)
- BET_MARTINGALE_001: Q-value = 15.0 (high confidence, optimal outcome potential)
- BET_FIBONACCI_001: Q-value = 14.5 (slightly lower due to slower progression)
- SKIP_MARTINGALE: Q-value = 2.0 (missing optimal opportunity)
- SKIP_FIBONACCI: Q-value = 2.0 (missing optimal opportunity)
```

### **Breakeven Decision Point:**
```
State: (Bucket_3, Medium_Pressure, Moderate_Sweet_Spot, Chain_Length_4, Martingale, Ready)
- BET_MARTINGALE_008: Q-value = 4.0 (breakeven - neutral)
- BET_FIBONACCI_005: Q-value = 4.5 (slightly better due to lower risk)
- SKIP_MARTINGALE: Q-value = 6.0 (avoiding risk might be better)
- SKIP_FIBONACCI: Q-value = 6.0 (avoiding risk might be better)
```

### **Maximum Risk Scenario:**
```
State: (Bucket_14, Normal_Pressure, None, Chain_Length_6, Martingale, Cooldown)
- BET_MARTINGALE_032: Q-value = -25.0 (high risk, cooldown penalty, near maximum loss)
- BET_FIBONACCI_013: Q-value = -23.0 (lower risk, still cooldown penalty)
- SKIP_MARTINGALE: Q-value = 8.0 (avoiding maximum risk)
- SKIP_FIBONACCI: Q-value = 8.0 (avoiding maximum risk)
```

### **Worst Case Scenario (Chain Length 7 Loss):**
```
State: (Bucket_14, Normal_Pressure, None, Chain_Length_7, Martingale, Cooldown)
- BET_MARTINGALE_064: Q-value = -30.0 (maximum loss potential)
- BET_FIBONACCI_021: Q-value = -28.0 (still maximum loss potential)
- SKIP_MARTINGALE: Q-value = 10.0 (avoiding maximum loss)
- SKIP_FIBONACCI: Q-value = 10.0 (avoiding maximum loss)
```

---

## Original Reasoning for Side Bet Chain Entry

### **Pattern-Based Entry Conditions**
1. **Ultra-Short Detection**: Previous games with extreme payouts (15.0x+) create conditions for insta-rug games (≤10 ticks)
2. **Duration-Treasury Correlation**: Longer games systematically reduce house profitability (r = -0.3618)
3. **Sweet Spot Activation**: High-confidence probability thresholds (12.0x → 91.8% → 15.0x+)
4. **Max Payout Recovery**: Post-max-payout games are 29.6% longer
5. **Treasury Pressure**: High pressure indicates increased insta-rug probability

### **Entry Decision Framework**
```
IF (Ultra_Short_Detected OR Sweet_Spot_Activated OR High_Treasury_Pressure)
AND (Cooldown_Status == Ready)
AND (Chain_Length < Max_Chain_Length)
THEN Enter_Side_Bet_Chain
ELSE Skip_Chain
```

### **Chain Continuation Logic**
```
IF (Previous_Bet_Lost)
AND (Game_Still_Active)
AND (Cooldown_Status == Ready)
AND (Chain_Length < Max_Chain_Length)
AND (Confidence_Still_High)
THEN Continue_Chain
ELSE Exit_Chain
```

---

## Key Learning Objectives (Revised)

### **Primary Goal: Win in Fewer Chain Links**
- **Chain Length 1 Win**: +10.0 (optimal outcome)
- **Chain Length 2 Win**: +8.0 (excellent outcome)
- **Chain Length 3 Win**: +6.0 (good outcome)
- **Chain Length 4 Win**: +4.0 (acceptable outcome)
- **Chain Length 5+ Win**: +2.0 or less (poor outcome)

### **Secondary Goal: Avoid Maximum Loss**
- **Chain Length 7+ Loss**: -20.0 (worst possible outcome)
- **Early Exit**: Better to exit early than reach maximum chain
- **Risk Management**: Prioritize avoiding maximum exposure

### **Tertiary Goal: Optimal Progression Selection**
- **Martingale**: Faster progression, higher risk
- **Fibonacci**: Slower progression, lower risk
- **System learns**: Which progression type works best for different scenarios

### **1. Chain Length Management**
- Learn optimal chain length based on confidence and risk tolerance
- Understand when to reset vs. continue chains
- Balance potential profit vs. total loss exposure

### **2. Progression Type Selection**
- Martingale vs Fibonacci based on risk tolerance and game conditions
- Understand trade-offs between faster progression (Martingale) vs. lower risk (Fibonacci)

### **3. Cooldown Timing Optimization**
- Optimize timing within 5-tick windows
- Understand impact of cooldown on chain continuation decisions
- Balance urgency vs. optimal timing

### **4. Breakeven Decisions**
- Smart decisions at chain length 4 (breakeven point)
- Understand neutral nature of breakeven (not good, not bad)
- Consider progression type differences at breakeven

### **5. Risk Assessment**
- Balance potential profit vs. total loss exposure
- Understand exponential risk increase with chain length
- Consider game end probability vs. chain continuation

---

## Implementation Architecture

### **System Components**
1. **State Manager**: Converts game state to module-specific representations
2. **Chain Manager**: Tracks side bet chains, progression types, and cooldown status
3. **Q-Table Manager**: Manages 4 separate Q-tables with independent learning
4. **Ensemble Engine**: Weighted voting and decision making
5. **Reward Calculator**: Computes rewards based on game outcomes and chain performance
6. **Performance Tracker**: Monitors individual module and ensemble performance

### **Data Flow**
```
Game State → State Manager → Chain Manager → Module Q-Tables → Ensemble Engine → Action Decision
     ↓
Game Outcome → Reward Calculator → Chain Update → Q-Table Updates → Performance Tracker → Weight Adjustment
```

### **Learning Parameters**
- **Learning Rate**: 0.1 (standard Q-learning)
- **Discount Factor**: 0.95 (future reward importance)
- **Exploration Rate**: 10% (epsilon-greedy)
- **Update Frequency**: Every game completion
- **Weight Adjustment**: Every 100 games

---

## Performance Expectations (Revised)

### **Accuracy Targets**
- **Chain Length 1-2 Wins**: 60-70% of successful bets (optimal performance)
- **Chain Length 3-4 Wins**: 25-35% of successful bets (acceptable performance)
- **Chain Length 5+ Wins**: 5-10% of successful bets (poor performance)
- **Maximum Chain Losses**: <5% of all bets (risk management success)
- **Overall System**: 80-90% accuracy for side bet profitability

### **Financial Performance**
- **Side Bet Success Rate**: 25-35% (vs 16.67% breakeven)
- **Expected Value**: 5-15% positive EV per side bet
- **Risk-Adjusted Returns**: Sharpe ratio >2.0
- **Maximum Drawdown**: <20% of bankroll

### **System Performance**
- **Decision Latency**: <50ms for real-time betting
- **Learning Convergence**: 30-50 episodes for new patterns
- **Memory Usage**: ~8MB for 10,500-state Q-tables
- **Uptime**: 99.9% during active trading hours

---

## Risk Management Considerations

### **Chain Risk Management**
- **Maximum Chain Length**: Limit to 7 bets maximum
- **Breakeven Exit**: Consider exiting at chain length 4 if confidence is low
- **Cooldown Risk**: Factor in 5-tick timing pressure
- **Game End Risk**: Longer chains = higher exposure to sudden game end

### **Pattern Decay Protection**
- **Continuous Validation**: Monitor pattern effectiveness in real-time
- **Adaptive Learning**: Adjust learning rates based on pattern performance
- **Fallback Mechanisms**: Revert to baseline strategies if patterns decay

### **Overfitting Prevention**
- **Cross-Validation**: Validate patterns across different time periods
- **Out-of-Sample Testing**: Test on unseen data before deployment
- **Regularization**: Implement regularization techniques to prevent overfitting

---

## Learning Strategy Implications

### **System Will Learn:**
1. **Prioritize Early Wins**: Chain length 1-2 wins are heavily rewarded
2. **Avoid Maximum Exposure**: Chain length 7+ losses are heavily penalized
3. **Smart Exit Strategies**: Exit before reaching maximum chain length
4. **Optimal Entry Timing**: Enter only when high confidence of early win
5. **Progression Optimization**: Choose progression type based on win probability

---

## Conclusion

This optimized Q-learning framework properly integrates the side bet chain mechanics with:

1. **Revised Reward Functions**: Inverse relationship between chain length and reward, maximum penalty for worst outcomes
2. **5-Tick Cooldown System**: Increasing penalties for longer chains
3. **Progressive PnL Integration**: Martingale and Fibonacci progression systems
4. **Original Pattern Reasoning**: Ultra-short detection, duration-treasury correlation, sweet spots
5. **Risk Management**: Proper chain length management and breakeven decisions

The system is designed to achieve 80-90% accuracy and 5-15% positive expected value per side bet while maintaining appropriate risk management through proper chain length optimization and progression type selection. The primary goal is to win in as few chain links as possible while avoiding maximum exposure.

---

*Document Status: Complete Side Bet Integration with Revised Reward Functions*
*Next: Full Q-Learning System Specification*
*Version: 2.0* 