# 4-Module Q-Learning System: 10,772-State Architecture Proposal

## Executive Summary

This document proposes a comprehensive 4-module Q-learning system for Rugs.fun side bet optimization, designed to capture the statistically validated patterns discovered in the CSV analysis. The system uses 10,772 total states across specialized modules to predict insta-rug events, duration patterns, treasury states, and compound interactions, with a primary focus on winning side bets in as few chain links as possible.

---

## System Overview

### **Total Architecture**
- **4 Specialized Modules**: Each targeting specific pattern types
- **10,772 Total States**: Comprehensive coverage of game mechanics and side bet chains
- **Ensemble Decision Engine**: Weighted voting across all modules
- **Real-Time Learning**: Continuous adaptation to pattern evolution
- **Side Bet Chain Integration**: Complete progressive betting system with 5-tick cooldown

### **Key Innovation**
- **Modular Design**: Independent learning for different pattern types
- **Empirical Foundation**: Based on statistically validated CSV analysis
- **Side Bet Optimization**: Primary focus on insta-rug prediction during presale
- **Risk-Adjusted Actions**: Martingale and Fibonacci progression with proper reward functions
- **Chain Length Optimization**: Win in fewer chain links while avoiding maximum exposure

---

## Module 1: Duration-Treasury Q-Table (Primary Module)

### **Purpose**
Primary side bet timing optimization using duration-based predictions, treasury state management, and side bet chain optimization.

### **State Space: 10,500 States**
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

### **Action Space (16 actions)**
```
Martingale Actions (8):
BET_MARTINGALE_001: 0.001 SOL (start/reset chain)
BET_MARTINGALE_002: 0.002 SOL (chain length 2)
BET_MARTINGALE_004: 0.004 SOL (chain length 3)
BET_MARTINGALE_008: 0.008 SOL (chain length 4 - breakeven)
BET_MARTINGALE_016: 0.016 SOL (chain length 5)
BET_MARTINGALE_032: 0.032 SOL (chain length 6)
BET_MARTINGALE_064: 0.064 SOL (chain length 7+)
SKIP_MARTINGALE: No bet (exit chain)

Fibonacci Actions (8):
BET_FIBONACCI_001: 0.001 SOL (start/reset chain)
BET_FIBONACCI_002: 0.002 SOL (chain length 2)
BET_FIBONACCI_003: 0.003 SOL (chain length 3)
BET_FIBONACCI_005: 0.005 SOL (chain length 4 - breakeven)
BET_FIBONACCI_008: 0.008 SOL (chain length 5)
BET_FIBONACCI_013: 0.013 SOL (chain length 6)
BET_FIBONACCI_021: 0.021 SOL (chain length 7+)
SKIP_FIBONACCI: No bet (exit chain)
```

### **Reward Function (Revised)**
```
Chain Length Rewards (Inverse to Chain Length):
Chain Length 1: +10.0 reward (optimal - win immediately)
Chain Length 2: +8.0 reward (excellent - win in 2 bets)
Chain Length 3: +6.0 reward (good - win in 3 bets)
Chain Length 4: +4.0 reward (breakeven point - neutral)
Chain Length 5: +2.0 reward (poor - win in 5 bets)
Chain Length 6: +1.0 reward (very poor - win in 6 bets)
Chain Length 7: +0.5 reward (terrible - win in 7 bets)

Progressive Loss Penalties:
Chain Length 1 Loss: -2.0 (lost 0.001)
Chain Length 2 Loss: -4.0 (lost 0.003)
Chain Length 3 Loss: -6.0 (lost 0.007)
Chain Length 4 Loss: -8.0 (lost 0.015)
Chain Length 5 Loss: -12.0 (lost 0.031)
Chain Length 6 Loss: -16.0 (lost 0.063)
Chain Length 7+ Loss: -20.0 (lost 0.127+) - WORST OUTCOME

Cooldown Penalty (Increasing with Chain Length):
Chain Length 1: -0.5 penalty
Chain Length 2: -1.0 penalty
Chain Length 3: -1.5 penalty
Chain Length 4: -2.0 penalty
Chain Length 5: -2.5 penalty
Chain Length 6: -3.0 penalty
Chain Length 7+: -4.0 penalty
```

### **Example Q-Table Entries**
```
State: (Bucket_0, High_Pressure, Ultra_Sweet_Spot, Chain_Length_1, Martingale, Ready)
- BET_MARTINGALE_001: Q-value = 15.0 (high confidence, optimal outcome potential)
- BET_FIBONACCI_001: Q-value = 14.5 (slightly lower due to slower progression)
- SKIP_MARTINGALE: Q-value = 2.0 (missing optimal opportunity)
- SKIP_FIBONACCI: Q-value = 2.0 (missing optimal opportunity)

State: (Bucket_14, Normal_Pressure, None, Chain_Length_7, Martingale, Cooldown)
- BET_MARTINGALE_064: Q-value = -30.0 (maximum loss potential)
- BET_FIBONACCI_021: Q-value = -28.0 (still maximum loss potential)
- SKIP_MARTINGALE: Q-value = 10.0 (avoiding maximum loss)
- SKIP_FIBONACCI: Q-value = 10.0 (avoiding maximum loss)
```

---

## Module 2: Ultra-Short Detection Q-Table (Specialized Module)

### **Purpose**
Predict insta-rug events (≤10 ticks) during presale window based on previous game patterns.

### **State Space: 240 States**
```
State = (Previous_Game_Payout, Previous_Game_Duration, Treasury_Pressure, Time_Since_High_Payout)
```

#### **Previous Game Payout Level (5 states)**
- **None**: No previous game data
- **Low**: 1.0x - 2.0x (normal payout)
- **Medium**: 2.0x - 5.0x (moderate payout)
- **High**: 5.0x - 15.0x (high payout)
- **Extreme**: 15.0x+ (extreme payout - triggers insta-rug)

#### **Previous Game Duration (4 states)**
- **Ultra-Short**: ≤10 ticks (insta-rug)
- **Short**: 11-50 ticks
- **Medium**: 51-200 ticks
- **Long**: 200+ ticks

#### **Treasury Pressure (4 states)**
- **Normal**: No recent high payouts
- **Low**: 1-2 recent high payouts
- **Medium**: 3-4 recent high payouts
- **High**: 5+ recent high payouts (high insta-rug probability)

#### **Time Since High Payout (3 states)**
- **Immediate**: 0-1 games since extreme payout
- **Recent**: 2-3 games since extreme payout
- **Distant**: 4+ games since extreme payout

### **Action Space (16 actions)**
```
Martingale Actions (8):
BET_MARTINGALE_001: 0.001 SOL (start/reset chain)
BET_MARTINGALE_002: 0.002 SOL (chain length 2)
BET_MARTINGALE_004: 0.004 SOL (chain length 3)
BET_MARTINGALE_008: 0.008 SOL (chain length 4 - breakeven)
BET_MARTINGALE_016: 0.016 SOL (chain length 5)
BET_MARTINGALE_032: 0.032 SOL (chain length 6)
BET_MARTINGALE_064: 0.064 SOL (chain length 7+)
SKIP_MARTINGALE: No bet (exit chain)

Fibonacci Actions (8):
BET_FIBONACCI_001: 0.001 SOL (start/reset chain)
BET_FIBONACCI_002: 0.002 SOL (chain length 2)
BET_FIBONACCI_003: 0.003 SOL (chain length 3)
BET_FIBONACCI_005: 0.005 SOL (chain length 4 - breakeven)
BET_FIBONACCI_008: 0.008 SOL (chain length 5)
BET_FIBONACCI_013: 0.013 SOL (chain length 6)
BET_FIBONACCI_021: 0.021 SOL (chain length 7+)
SKIP_FIBONACCI: No bet (exit chain)
```

### **Reward Function**
```
If insta-rug occurs (≤10 ticks):
- Chain Length 1: +10.0 reward (optimal outcome)
- Chain Length 2: +8.0 reward (excellent outcome)
- Chain Length 3: +6.0 reward (good outcome)
- Chain Length 4: +4.0 reward (acceptable outcome)
- Chain Length 5+: +2.0 or less (poor outcome)

If normal game occurs (>10 ticks):
- Chain Length 1 Loss: -2.0 (lost 0.001)
- Chain Length 2 Loss: -4.0 (lost 0.003)
- Chain Length 3 Loss: -6.0 (lost 0.007)
- Chain Length 4 Loss: -8.0 (lost 0.015)
- Chain Length 5 Loss: -12.0 (lost 0.031)
- Chain Length 6 Loss: -16.0 (lost 0.063)
- Chain Length 7+ Loss: -20.0 (lost 0.127+) - WORST OUTCOME
```

### **Example Q-Table Entries**
```
State: (Extreme_Payout, Medium_Duration, High_Pressure, Immediate)
- BET_MARTINGALE_001: Q-value = 12.5 (high confidence, optimal outcome potential)
- BET_FIBONACCI_001: Q-value = 12.0 (slightly lower due to slower progression)
- SKIP_MARTINGALE: Q-value = 2.0 (missing optimal opportunity)
- SKIP_FIBONACCI: Q-value = 2.0 (missing optimal opportunity)
```

---

## Module 3: Max Payout Recovery Q-Table (Specialized Module)

### **Purpose**
Predict longer duration games after max payout events (0.020 treasury remainder).

### **State Space: 12 States**
```
State = (Max_Payout_Context, Recovery_Position)
```

#### **Max Payout Context (3 states)**
- **None**: No recent max payout
- **Just_Occurred**: Max payout in previous game
- **Recent**: Max payout in last 2-3 games

#### **Recovery Position (4 states)**
- **None**: Not in recovery period
- **1st_Game**: First game after max payout
- **2nd_Game**: Second game after max payout
- **3rd_Game**: Third game after max payout

### **Action Space (16 actions)**
```
Martingale Actions (8):
BET_MARTINGALE_001: 0.001 SOL (start/reset chain)
BET_MARTINGALE_002: 0.002 SOL (chain length 2)
BET_MARTINGALE_004: 0.004 SOL (chain length 3)
BET_MARTINGALE_008: 0.008 SOL (chain length 4 - breakeven)
BET_MARTINGALE_016: 0.016 SOL (chain length 5)
BET_MARTINGALE_032: 0.032 SOL (chain length 6)
BET_MARTINGALE_064: 0.064 SOL (chain length 7+)
SKIP_MARTINGALE: No bet (exit chain)

Fibonacci Actions (8):
BET_FIBONACCI_001: 0.001 SOL (start/reset chain)
BET_FIBONACCI_002: 0.002 SOL (chain length 2)
BET_FIBONACCI_003: 0.003 SOL (chain length 3)
BET_FIBONACCI_005: 0.005 SOL (chain length 4 - breakeven)
BET_FIBONACCI_008: 0.008 SOL (chain length 5)
BET_FIBONACCI_013: 0.013 SOL (chain length 6)
BET_FIBONACCI_021: 0.021 SOL (chain length 7+)
SKIP_FIBONACCI: No bet (exit chain)
```

### **Reward Function**
```
If long game occurs (>200 ticks):
- Chain Length 1: +10.0 reward (optimal outcome)
- Chain Length 2: +8.0 reward (excellent outcome)
- Chain Length 3: +6.0 reward (good outcome)
- Chain Length 4: +4.0 reward (acceptable outcome)
- Chain Length 5+: +2.0 or less (poor outcome)

If short game occurs (≤200 ticks):
- Chain Length 1 Loss: -2.0 (lost 0.001)
- Chain Length 2 Loss: -4.0 (lost 0.003)
- Chain Length 3 Loss: -6.0 (lost 0.007)
- Chain Length 4 Loss: -8.0 (lost 0.015)
- Chain Length 5 Loss: -12.0 (lost 0.031)
- Chain Length 6 Loss: -16.0 (lost 0.063)
- Chain Length 7+ Loss: -20.0 (lost 0.127+) - WORST OUTCOME
```

### **Example Q-Table Entries**
```
State: (Just_Occurred, 1st_Game)
- BET_MARTINGALE_001: Q-value = 8.5 (high confidence, optimal outcome potential)
- BET_FIBONACCI_001: Q-value = 8.2 (slightly lower due to slower progression)
- SKIP_MARTINGALE: Q-value = 2.0 (missing optimal opportunity)
- SKIP_FIBONACCI: Q-value = 2.0 (missing optimal opportunity)
```

---

## Module 4: Compound Pattern Q-Table (Advanced Module)

### **Purpose**
Recognize and exploit interactions between multiple patterns occurring simultaneously.

### **State Space: 20 States**
```
State = (Active_Pattern_Count, Pattern_Combination)
```

#### **Active Pattern Count (5 states)**
- **0**: No active patterns
- **1**: One active pattern
- **2**: Two active patterns
- **3**: Three active patterns
- **4+**: Four or more active patterns

#### **Pattern Combination (4 states)**
- **Duration**: Duration-based patterns active
- **Treasury**: Treasury pressure patterns active
- **Ultra-Short**: Ultra-short detection patterns active
- **Max-Payout**: Max payout recovery patterns active

### **Action Space (16 actions)**
```
Martingale Actions (8):
BET_MARTINGALE_001: 0.001 SOL (start/reset chain)
BET_MARTINGALE_002: 0.002 SOL (chain length 2)
BET_MARTINGALE_004: 0.004 SOL (chain length 3)
BET_MARTINGALE_008: 0.008 SOL (chain length 4 - breakeven)
BET_MARTINGALE_016: 0.016 SOL (chain length 5)
BET_MARTINGALE_032: 0.032 SOL (chain length 6)
BET_MARTINGALE_064: 0.064 SOL (chain length 7+)
SKIP_MARTINGALE: No bet (exit chain)

Fibonacci Actions (8):
BET_FIBONACCI_001: 0.001 SOL (start/reset chain)
BET_FIBONACCI_002: 0.002 SOL (chain length 2)
BET_FIBONACCI_003: 0.003 SOL (chain length 3)
BET_FIBONACCI_005: 0.005 SOL (chain length 4 - breakeven)
BET_FIBONACCI_008: 0.008 SOL (chain length 5)
BET_FIBONACCI_013: 0.013 SOL (chain length 6)
BET_FIBONACCI_021: 0.021 SOL (chain length 7+)
SKIP_FIBONACCI: No bet (exit chain)
```

### **Reward Function**
```
Base reward for correct prediction: +3.0

Pattern multiplier:
- 1 pattern: ×1.0
- 2 patterns: ×1.5
- 3 patterns: ×2.0
- 4+ patterns: ×2.5

Combination bonus:
- Duration + Treasury: +2.0
- Ultra-Short + Max-Payout: +3.0
- All patterns: +5.0

Chain Length Rewards (Inverse to Chain Length):
Chain Length 1: +10.0 reward (optimal - win immediately)
Chain Length 2: +8.0 reward (excellent - win in 2 bets)
Chain Length 3: +6.0 reward (good - win in 3 bets)
Chain Length 4: +4.0 reward (breakeven point - neutral)
Chain Length 5: +2.0 reward (poor - win in 5 bets)
Chain Length 6: +1.0 reward (very poor - win in 6 bets)
Chain Length 7: +0.5 reward (terrible - win in 7 bets)
```

### **Example Q-Table Entries**
```
State: (3_Patterns, Duration_Treasury_UltraShort)
- BET_MARTINGALE_001: Q-value = 12.0 (high confidence, optimal outcome potential)
- BET_FIBONACCI_001: Q-value = 11.5 (slightly lower due to slower progression)
- SKIP_MARTINGALE: Q-value = 2.0 (missing optimal opportunity)
- SKIP_FIBONACCI: Q-value = 2.0 (missing optimal opportunity)
```

---

## Ensemble Decision Engine

### **Weighted Voting System**
```javascript
Module Weights (Initial):
- Module 1 (Duration-Treasury): 35% (primary focus)
- Module 2 (Ultra-Short): 30% (insta-rug prediction)
- Module 3 (Max Payout): 20% (recovery patterns)
- Module 4 (Compound): 15% (pattern interactions)
```

### **Decision Process**
1. **State Conversion**: Convert current game state to each module's format
2. **Q-Value Lookup**: Get Q-values for all actions in each module
3. **Weighted Combination**: Combine Q-values using module weights
4. **Action Selection**: Choose action with highest weighted Q-value
5. **Confidence Calculation**: Calculate confidence based on Q-value differences

### **Adaptive Weighting**
```javascript
Weight Adjustment Formula:
new_weight = old_weight + learning_rate * (module_accuracy - ensemble_accuracy)

Learning Rate: 0.01
Update Frequency: Every 100 games
```

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

## Performance Expectations

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
- **Memory Usage**: ~8MB for 10,772-state Q-tables
- **Uptime**: 99.9% during active trading hours

---

## Implementation Roadmap

### **Phase 1: Core System (Weeks 1-2)**
- Implement Module 1 (Duration-Treasury Q-Table)
- Basic ensemble engine with fixed weights
- Real-time state conversion and action selection
- Expected Impact: 70-80% of system performance

### **Phase 2: Specialized Modules (Weeks 3-4)**
- Implement Module 2 (Ultra-Short Detection)
- Implement Module 3 (Max Payout Recovery)
- Enhanced ensemble voting system
- Expected Impact: 15-20% performance improvement

### **Phase 3: Advanced Features (Weeks 5-6)**
- Implement Module 4 (Compound Patterns)
- Adaptive weight adjustment system
- Performance monitoring and optimization
- Expected Impact: 5-10% performance improvement

### **Phase 4: Production Deployment (Weeks 7-8)**
- Real-time WebSocket integration
- Risk management and position sizing
- Monitoring and alerting systems
- Expected Impact: Production readiness

---

## Risk Management

### **Pattern Decay Protection**
- **Continuous Validation**: Monitor pattern effectiveness in real-time
- **Adaptive Learning**: Adjust learning rates based on pattern performance
- **Fallback Mechanisms**: Revert to baseline strategies if patterns decay

### **Overfitting Prevention**
- **Cross-Validation**: Validate patterns across different time periods
- **Out-of-Sample Testing**: Test on unseen data before deployment
- **Regularization**: Implement regularization techniques to prevent overfitting

### **Market Adaptation**
- **Real-Time Monitoring**: Track pattern performance continuously
- **Adaptive Thresholds**: Adjust sweet spot thresholds based on market conditions
- **Dynamic Weighting**: Adjust module weights based on recent performance

---

## Learning Strategy Implications

### **System Will Learn:**
1. **Prioritize Early Wins**: Chain length 1-2 wins are heavily rewarded
2. **Avoid Maximum Exposure**: Chain length 7+ losses are heavily penalized
3. **Smart Exit Strategies**: Exit before reaching maximum chain length
4. **Optimal Entry Timing**: Enter only when high confidence of early win
5. **Progression Optimization**: Choose progression type based on win probability

---

## Questions and Considerations

### **Design Questions**
1. **State Granularity**: Are the current state divisions optimal for each module?
2. **Action Space Size**: Is 16 actions sufficient or do we need more granularity?
3. **Module Independence**: How much should modules influence each other?
4. **Learning Rate**: Should different modules have different learning rates?

### **Implementation Questions**
1. **Real-Time Processing**: Can we maintain <50ms decision latency with 10,772 states?
2. **Memory Management**: How do we handle the memory requirements for 4 Q-tables?
3. **State Synchronization**: How do we ensure consistent state across modules?
4. **Weight Convergence**: How quickly will the ensemble weights converge?

### **Risk Questions**
1. **Pattern Evolution**: How do we detect when patterns change fundamentally?
2. **Competition**: How do we maintain edge as others discover similar patterns?
3. **Regulatory Risk**: What are the implications of systematic pattern exploitation?
4. **Technical Risk**: What happens if one or more modules fail?

### **Performance Questions**
1. **Accuracy Validation**: How do we validate the expected 80-90% accuracy?
2. **Financial Validation**: How do we measure the 5-15% positive EV?
3. **Scalability**: Can the system handle multiple concurrent games?
4. **Reliability**: How do we ensure 99.9% uptime?

---

## Conclusion

This 4-module Q-learning system with 10,772 total states represents a comprehensive approach to systematic side bet optimization based on empirically validated patterns. The modular design allows for specialized learning of different pattern types while the ensemble engine provides robust decision making.

The key strengths of this architecture are:
1. **Empirical Foundation**: Based on statistically validated CSV analysis
2. **Modular Design**: Independent learning for different pattern types
3. **Ensemble Decision Making**: Robust combination of multiple predictions
4. **Real-Time Adaptation**: Continuous learning and weight adjustment
5. **Risk Management**: Comprehensive protection against pattern decay
6. **Side Bet Chain Integration**: Complete progressive betting system with proper reward functions

The system is designed to achieve 80-90% accuracy and 5-15% positive expected value per side bet, providing a robust foundation for systematic pattern exploitation while maintaining appropriate risk management. The primary goal is to win in as few chain links as possible while avoiding maximum exposure.

---

*Document Status: Complete System Specification with Side Bet Integration*
*Next: Implementation Planning and Development*
*Version: 2.0* 