# Trading Bot RL Rewards Design - Complete Context

**Project**: Rugs.fun RL Trading Bot Reward Function Redesign
**Date**: November 8, 2025
**Status**: Reward Design Phase
**Goal**: Leverage sidebet prediction model (38% win rate) to achieve >90% rug avoidance and >60% win rate

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Critical Game Mechanics](#critical-game-mechanics)
3. [Current Reward System](#current-reward-system)
4. [Current Performance Baseline](#current-performance-baseline)
5. [The Breakthrough: Sidebet Prediction Model](#the-breakthrough-sidebet-prediction-model)
6. [Key Statistical Findings](#key-statistical-findings)
7. [What Failed in Previous Training](#what-failed-in-previous-training)
8. [Design Objectives](#design-objectives)
9. [Available Observations](#available-observations)
10. [Available Actions](#available-actions)
11. [Design Questions to Address](#design-questions-to-address)
12. [Design Constraints](#design-constraints)
13. [Expected Outputs](#expected-outputs)
14. [Reference Materials](#reference-materials)
15. [Success Criteria](#success-criteria)

---

## 1. Project Overview

### What is Rugs.fun?

Rugs.fun is a decentralized casino game on Solana where:
- **Players trade a token** with a continuously rising multiplier
- **The token will "rug"** (crash to near-zero) at a random time
- **Players must exit before the rug** to profit
- **Sidebets available**: Predict the rug within a 40-tick window for 5:1 payout

**Game Flow**:
```
Start (1.0x) → Rising multiplier (1.5x, 2.0x, 3.0x...) → RUG (0.01x) → Cooldown → Repeat
```

**Key Insight**: Games last ~300 ticks on average, with high variance (σ=180 ticks). The rug timing is unpredictable but has statistical patterns.

### What We're Building

An **RL trading bot** that:
1. **Enters positions** at optimal times (buy tokens)
2. **Exits before rugs** (sell before crash)
3. **Sizes bets dynamically** based on risk
4. **Deploys sidebets** when rug prediction confidence is high
5. **Manages bankroll** to avoid bankruptcy

**Architecture**:
- **Environment**: Gymnasium-compatible with 79 observation features
- **Algorithm**: PPO (Proximal Policy Optimization)
- **Action Space**: 8 discrete actions (wait, buy, sell, sidebet, etc.)
- **Episode**: 15 consecutive games with persistent bankroll

### The Critical Challenge

Current bot has **suboptimal performance** across all metrics:
- Win rate: ~30% (need >60%)
- Rug avoidance: ~30% (need >90%)
- Bankruptcy risk: ~20% (need <5%)
- ROI: Highly variable (need consistent >200%)

**Root Cause**: Reward function doesn't prioritize rug avoidance highly enough. Bot learns to maximize P&L but gets liquidated by rugs.

---

## 2. Critical Game Mechanics

### 2.1 Trading Mechanics

**Buy (Open Position)**:
- Costs: `bet_size` SOL deducted from bankroll
- Creates position at current multiplier
- Max 10 positions simultaneously
- Position tracks: entry_price, size, current_pnl

**Sell (Close Position)**:
- Returns: `position_value = bet_size * (current_price / entry_price)`
- Can sell all positions or partial (10%, 20%, ..., 100%)
- Immediately adds proceeds to bankroll
- Clears position tracking

**Position P&L**:
```python
pnl = bet_size * (current_price / entry_price - 1.0)
pnl_percent = ((current_price / entry_price) - 1.0) * 100
```

### 2.2 Rug Mechanics

**Rug Event**:
- Occurs at unpredictable tick (statistical distribution available)
- Multiplier crashes to near-zero (typically 0.01x-0.05x)
- All positions liquidated at rug price
- Typical loss: 95-99% of position value

**Rug Statistics**:
- Mean game duration: 329 ticks
- Median: 281 ticks
- Std dev: 180 ticks
- Range: 50-800+ ticks

**Predictability**: Historically unpredictable, but our sidebet model achieves 38% prediction accuracy.

### 2.3 Sidebet Mechanics

**Sidebet Placement**:
- Must place within first 40 ticks of game
- Costs: `bet_size` SOL (separate from main position)
- Predicts: "Game will rug within next 40 ticks"
- Payout: 5:1 if correct, 0 if wrong
- Cooldown: 5 ticks between sidebets

**Sidebet Window**:
```
Tick 0 ────────────────────► Tick 40 ───────────────────► Rug
         Can place sidebet         Prediction window (40 ticks)
```

**Example**:
- Place sidebet at tick 150 with 0.001 SOL
- If game rugs between tick 150-190: Win 0.005 SOL (5x payout)
- If game rugs at tick 191+: Lose 0.001 SOL

### 2.4 Bankroll & Bankruptcy

**Initial Bankroll**: 0.01 SOL (typical)

**Bankruptcy**:
- Occurs when bankroll ≤ 0.001 SOL
- Episode terminates immediately
- Massive penalty in reward function (-1000.0 currently)

**Bankroll Management**:
- Must preserve capital for 15-game episode
- Each position/sidebet reduces available capital
- Early bankruptcy prevents learning from remaining games

### 2.5 Sweet Spot

**Definition**: Multiplier range where risk/reward is optimal
- **Range**: 2.0x - 4.0x
- **Typical ticks**: 40-80 ticks into game
- **Characteristics**: Profitable but not overextended

**Why Important**:
- Entry before sweet spot: Slow gains, wasted time
- Entry in sweet spot: Optimal risk/reward
- Entry after sweet spot: High risk, race against rug

---

## 3. Current Reward System

### 3.1 Reward Components (13 total)

Current reward function has 13 components with various weights:

**Financial (Primary)**:
1. **pnl_reward** (weight: 1.0)
   - Raw P&L from closed positions
   - `reward = position_pnl`

**Pattern Exploitation (Secondary)**:
2. **ultra_short_skip_reward** (weight: 1.0)
   - Skip games predicted to be ultra-short
   - Bonus for avoiding likely early rugs

3. **moonshot_exit_reward** (weight: 1.0)
   - Exit games predicted to be moonshoots
   - Bonus for riding long games

**Sidebet (Separate)**:
4. **sidebet_payout** (weight: 1.0)
   - 5:1 payout on successful sidebets
   - Separate from main position P&L

**Volatility (Exit Signal)**:
5. **volatility_exit_reward** (weight: 3.0)
   - Bonus for exiting during high volatility spikes
   - Based on 10x baseline volatility threshold

6. **volatility_emergency_exit** (weight: 5.0)
   - Larger bonus for emergency exits at extreme volatility
   - Currently the highest-weighted exit signal

**Sweet Spot Timing**:
7. **sweet_spot_entry** (weight: 2.0)
   - Bonus for entering in 2-4x range

8. **sweet_spot_hold** (weight: 1.0)
   - Bonus for holding through sweet spot

9. **sweet_spot_exit** (weight: 2.0)
   - Bonus for exiting within sweet spot

**Bankroll Management**:
10. **bankruptcy_penalty** (weight: 1.0, value: -1000.0)
    - Massive penalty for running out of money

11. **low_bankroll_penalty** (weight: 1.0, value: -20.0)
    - Penalty when bankroll < 0.005 SOL

**Meta**:
12. **action_invalid_penalty** (weight: 1.0, value: -10.0)
    - Penalty for attempting invalid actions

13. **wait_penalty** (weight: 0.1, value: -0.1)
    - Small penalty for waiting (encourage action)

### 3.2 Current Component Weights (Summary)

```python
weights = {
    'pnl_reward': 1.0,
    'ultra_short_skip': 1.0,
    'moonshot_exit': 1.0,
    'sidebet_payout': 1.0,
    'volatility_exit': 3.0,           # Highest exit signal currently
    'volatility_emergency': 5.0,      # CURRENT PRIMARY EXIT SIGNAL
    'sweet_spot_entry': 2.0,
    'sweet_spot_hold': 1.0,
    'sweet_spot_exit': 2.0,
    'bankruptcy_penalty': 1.0,        # -1000.0 value
    'low_bankroll_penalty': 1.0,      # -20.0 value
    'action_invalid': 1.0,            # -10.0 value
    'wait_penalty': 0.1,              # -0.1 value
}
```

**Total Weight**: ~20.1 (sum of absolute values)

**Primary Focus**: Volatility (weight 8.0 combined) and P&L (weight 1.0)

### 3.3 Problems with Current System

**Issue 1: No Rug Avoidance Component**
- No reward for exiting before rug
- No penalty for holding through high rug probability
- Agent learns to maximize P&L but ignores rug risk

**Issue 2: Volatility as Primary Signal**
- Volatility exit weight: 8.0 (highest)
- But volatility spikes don't always precede rugs
- Can exit too early or miss rugs without spikes

**Issue 3: Sidebet Model Unused**
- Trained sidebet model (38% win rate) available
- 5 prediction features in observation space
- But no reward components use these predictions!

**Issue 4: P&L Weight Too High Relative to Risk**
- P&L weight: 1.0 (significant)
- Encourages holding for profits
- Conflicts with exiting early (rug avoidance)

---

## 4. Current Performance Baseline

### 4.1 Training Metrics (Last 1000 Episodes)

**Position Performance**:
- Win rate: ~30% (positions profitable)
- Loss rate: ~70% (positions liquidated by rugs)
- Average position hold: ~120 ticks
- Average win: +0.015 SOL
- Average loss: -0.008 SOL (rug liquidation)

**Episode Performance**:
- Average bankroll end: 0.008 SOL (loss from 0.01 start)
- Bankruptcy rate: ~20% (1 in 5 episodes)
- ROI: Variable (-50% to +100%)
- Sharpe ratio: <1.0 (high volatility)

**Behavioral Patterns**:
- Enters positions: 60% of games
- Avg entry time: Tick 80 (often post-sweet spot)
- Holds too long: Average 120 ticks (past optimal)
- Rug avoidance: ~30% (exits before rug only 30% of time)

**Key Observation**: Agent learns to enter and profit, but fails to exit before rugs. This causes 70% loss rate and frequent bankruptcies.

### 4.2 Rug Avoidance Analysis

**Exits Before Rug**: 30%
- **With volatility signal**: 20% (detects some rugs)
- **Without signal**: 10% (luck or P&L target)

**Liquidated by Rug**: 70%
- **High volatility present**: 30% (signal present but ignored)
- **Low volatility present**: 40% (no signal, agent unaware)

**Missed Exit Opportunities**:
- Agent often has high rug probability predictions (>0.50) but doesn't exit
- Volatility signal sometimes triggers but agent waits for more profit
- Sweet spot timing conflicts with exit timing

### 4.3 What Works Currently

**✅ Successful Behaviors**:
1. **Sweet spot entry**: Agent learned to enter at 2-4x (good timing)
2. **Position sizing**: Reasonable bet sizes (~0.002-0.005 SOL)
3. **Bankruptcy avoidance when careful**: Some episodes preserve capital well
4. **Pattern exploitation**: Ultra-short skip and moonshot patterns show learning

**❌ Failed Behaviors**:
1. **Rug avoidance**: Only 30% success rate (need >90%)
2. **Exit timing**: Holds too long chasing profits
3. **Sidebet deployment**: Rarely uses sidebets despite having predictions
4. **Risk management**: Takes positions in late game (high rug risk)

---

## 5. The Breakthrough: Sidebet Prediction Model

### 5.1 Model Overview

**Sidebet Model v3** (Production-Ready):
- **Win Rate**: 38.1% (target was >25%)
- **ROI**: 754% on 200-game backtest
- **Martingale Success**: 100% (never bankrupted with 4-attempt strategy)
- **Model Type**: Gradient Boosting Classifier
- **Training Data**: 644 games
- **Validation**: 200 held-out games

**Key Achievement**: This is **the most reliable exit signal** we have. Better than volatility, better than patterns.

### 5.2 How the Model Works

**Input**: 14 features extracted from game state
- Statistical position (tick_percentile, z_score, iqr_position)
- Volatility evolution (ratio, momentum, intensity, acceleration)
- Spike patterns (frequency, spacing, death_spike_score)
- Strategic context (theta_factor, sequence_feasibility, cooldown)

**Output**: Rug probability (0.0 - 1.0)
- **≥0.50**: Critical (emergency exit) - 39.4% win rate
- **≥0.40**: High (exit recommended) - ~36% win rate
- **≥0.30**: Medium (reduce positions) - ~35% win rate
- **<0.30**: Low (safe to hold) - <30% win rate

**Dominant Feature**: `z_score` (63.64% importance)
- Measures how long game has lasted vs historical average
- Games lasting abnormally long → high rug probability
- More reliable than individual spike detection

### 5.3 Integration into Environment

The sidebet model is wrapped in `SidebetPredictor` class and provides **5 features every tick**:

```python
rug_prediction = {
    'probability': float,        # 0.0-1.0 (rug probability)
    'confidence': float,         # 0.0-1.0 (prediction reliability)
    'ticks_to_rug_estimate': int,  # ~10-80 ticks until predicted rug
    'signal_strength': str,      # 'low' | 'medium' | 'high' | 'critical'
    'recommended_action': str,   # 'hold' | 'reduce' | 'exit' | 'emergency'
}
```

**In Observation Space** (5 features):
```python
'rug_prediction': [
    probability,          # 0.0-1.0
    confidence,           # 0.0-1.0
    ticks_to_rug_norm,   # 0.0-1.0 (normalized)
    is_critical,          # 0.0 or 1.0 (binary flag)
    should_exit,          # 0.0 or 1.0 (binary flag)
]
```

**These 5 features are AVAILABLE but UNUSED** in current rewards!

### 5.4 Prediction Examples

**Example 1: Early Game (Tick 50)**
```python
probability: 0.12
confidence: 0.45
signal_strength: 'low'
recommended_action: 'hold'
```
→ Safe to enter/hold positions

**Example 2: Mid Game (Tick 200)**
```python
probability: 0.35
confidence: 0.72
signal_strength: 'medium'
recommended_action: 'reduce'
```
→ Consider partial exit, reduce exposure

**Example 3: Late Game (Tick 300)**
```python
probability: 0.58
confidence: 0.85
signal_strength: 'critical'
recommended_action: 'emergency'
```
→ EXIT IMMEDIATELY! Very high rug risk

### 5.5 Why This is Transformative

**Before Sidebet Model**:
- Relied on volatility spikes (unreliable)
- Relied on patterns (noisy)
- Rug avoidance: 30%

**With Sidebet Model**:
- Direct rug probability prediction
- 38% win rate = 2x better than random (16.7%)
- Confidence scoring allows selective action
- **Expected rug avoidance: >90%**

**The Opportunity**:
Design rewards that teach the agent to:
1. Trust high-confidence predictions (probability + confidence)
2. Exit when probability ≥ 0.40 (proactive)
3. Emergency exit when probability ≥ 0.50 (critical)
4. Continue holding when probability < 0.30 (safe)
5. Deploy sidebets when confidence is high

---

## 6. Key Statistical Findings

### 6.1 Game Duration Patterns

**Distribution**:
- Mean: 329 ticks
- Median: 281 ticks
- Std Dev: 180 ticks
- Q1: 186 ticks
- Q3: 424 ticks

**Insight**: High variance makes duration unpredictable. Z-score (deviation from mean) is dominant predictor.

### 6.2 Volatility Spike Analysis

**Findings**:
- 67.4% of rugs have multiple volatility spikes
- Average 4.04 spikes per game
- 10x baseline volatility = strong signal
- But not all rugs have spikes (32.6%)

**Limitation**: Volatility alone insufficient for 90% rug avoidance.

### 6.3 Sweet Spot Performance

**Entry in Sweet Spot (2-4x)**:
- Average hold time: 60 ticks
- Win rate: ~40% (better than overall 30%)
- ROI: +15% per position

**Entry Outside Sweet Spot**:
- Too early (<2x): Slow gains, opportunity cost
- Too late (>4x): High rug risk, race against time

**Insight**: Sweet spot timing helps but doesn't guarantee exits before rugs.

### 6.4 Pattern Detection

**Ultra-Short Games** (<100 ticks):
- Frequency: ~15% of games
- Skip rate when detected: 73%
- Avoids early losses

**Moonshot Games** (>500 ticks):
- Frequency: ~8% of games
- Early exit prevents rug capture
- Mixed results (some moonshoots still rug)

**Insight**: Patterns help but are secondary to rug prediction.

### 6.5 Sidebet Model Validation

**Threshold Analysis** (All Profitable!):
```
Threshold | Win Rate | EV per Bet | Status
----------|----------|------------|--------
0.100     | 33.7%    | +0.684     | ✅
0.200     | 34.4%    | +0.722     | ✅
0.300     | 35.3%    | +0.765     | ✅
0.400     | 36.5%    | +0.827     | ✅✅
0.500     | 39.4%    | +0.971     | ✅✅✅ OPTIMAL
```

**Insight**: Model is robust across all thresholds. Even conservative (0.10) is profitable. Optimal at 0.50 threshold.

---

## 7. What Failed in Previous Training

### 7.1 Attempt 1: Pure P&L Maximization

**Approach**: Reward only position P&L
```python
reward = position_pnl
```

**Result**: ❌ FAILED
- Win rate: 20%
- Rug avoidance: 15%
- Bankruptcy: 35%
- Agent learned to hold indefinitely for max profit

**Lesson**: Greed kills. Need exit incentives.

### 7.2 Attempt 2: Volatility-Based Exits

**Approach**: Add volatility exit rewards
```python
if volatility_ratio >= 10.0:
    reward += 30.0  # Exit bonus
```

**Result**: ⚠️ PARTIAL SUCCESS
- Win rate: 25% → 30% (improvement)
- Rug avoidance: 20% → 30% (improvement)
- Bankruptcy: 25%
- Agent exits on some spikes but misses many rugs

**Lesson**: Volatility helps but insufficient. Need better signal.

### 7.3 Attempt 3: Pattern Exploitation

**Approach**: Add ultra-short skip and moonshot exit
```python
if ultra_short_predicted:
    reward += 10.0  # Skip game
if moonshot_detected:
    reward += 15.0  # Early exit
```

**Result**: ⚠️ PARTIAL SUCCESS
- Win rate: 30% (stable)
- Rug avoidance: 30% (stable)
- Bankruptcy: 20%
- Agent skips some bad games but overall limited impact

**Lesson**: Patterns are noisy. Need direct rug prediction.

### 7.4 Common Failure Modes

**Failure Mode 1: Late Exit**
- Agent waits for higher profits
- Rug occurs before agent exits
- Most common failure (50% of losses)

**Failure Mode 2: No Exit Signal**
- Low volatility rugs (no spike warning)
- Agent has no indication to exit
- 30% of losses

**Failure Mode 3: Signal Ignored**
- Volatility spike occurs
- Agent doesn't exit (chasing profits)
- 20% of losses

**Root Cause**: **Insufficient incentive to exit early**. P&L reward dominates, exit signals weak.

---

## 8. Design Objectives

### 8.1 Primary Objectives (MUST Achieve)

**1. Rug Avoidance: >90%**
- Currently: 30%
- Target: >90%
- Impact: 3x improvement
- Measurement: % of positions exited before rug

**2. Position Win Rate: >60%**
- Currently: 30%
- Target: >60%
- Impact: 2x improvement
- Measurement: % of closed positions with positive P&L

**3. Bankruptcy Rate: <5%**
- Currently: 20%
- Target: <5%
- Impact: 4x reduction
- Measurement: % of episodes ending in bankruptcy

### 8.2 Secondary Objectives (SHOULD Achieve)

**4. ROI: >200%**
- Currently: Variable (-50% to +100%)
- Target: >200% consistent
- Impact: Stable profitability
- Measurement: (end_bankroll - start_bankroll) / start_bankroll

**5. Sharpe Ratio: >1.5**
- Currently: <1.0
- Target: >1.5
- Impact: Better risk-adjusted returns
- Measurement: (mean_return - risk_free_rate) / std_dev_return

**6. Max Drawdown: <20%**
- Currently: ~50%
- Target: <20%
- Impact: Capital preservation
- Measurement: Worst peak-to-trough decline

### 8.3 Tertiary Objectives (NICE to Achieve)

**7. Average Position Hold: 40-80 ticks**
- Sweet spot duration
- Not too short (missed profits), not too long (rug risk)

**8. False Exit Rate: <10%**
- Exits when no rug occurs shortly after
- Balance needed: exit on signals but not too early

**9. Sidebet Win Rate: >30%**
- If agent deploys sidebets
- Should match or exceed model performance

### 8.4 Behavioral Objectives

**Agent Should Learn To**:
1. ✅ Enter in sweet spot (2-4x) - ALREADY LEARNED
2. ✅ Exit when rug_probability ≥ 0.50 (critical) - **NEEDS LEARNING**
3. ✅ Exit when rug_probability ≥ 0.40 (high) - **NEEDS LEARNING**
4. ✅ Reduce positions when rug_probability ≥ 0.30 (medium) - **NEEDS LEARNING**
5. ✅ Hold when rug_probability < 0.30 (safe) - **NEEDS LEARNING**
6. ⚠️ Deploy sidebets when confidence > 0.70 - **OPTIONAL**
7. ⚠️ Scale bet sizes based on rug risk - **OPTIONAL**

**Agent Should NOT**:
1. ❌ Exit immediately (wait penalty + early exit penalty)
2. ❌ Hold indefinitely (rug avoidance penalty)
3. ❌ Ignore high-confidence predictions (severe penalty)
4. ❌ Bankrupt (massive penalty)

---

## 9. Available Observations

The RL agent receives **79 features** every tick, organized in 8 groups:

### 9.1 Current State (10 features)
```python
'current': [
    price,               # Current multiplier (e.g., 2.5x)
    tick,                # Current tick number (0-800+)
    phase,               # Game phase (early/mid/late)
    has_positions,       # 1.0 if positions open, 0.0 otherwise
    bankroll,            # Current bankroll (SOL)
    rugged,              # 1.0 if game rugged, 0.0 otherwise
    position_count,      # Number of open positions (0-10)
    volatility_baseline, # Baseline volatility (first 40 ticks)
    volatility_current,  # Current volatility (last 10 ticks)
    volatility_ratio,    # Current / baseline (THE #1 EXIT SIGNAL pre-sidebet)
]
```

### 9.2 History (20 features)
Last 5 games × 4 features:
```python
'history': [
    # Game -5
    end_price, duration, peak, ultra_short_flag,
    # Game -4
    end_price, duration, peak, ultra_short_flag,
    # ... (repeat for -3, -2, -1)
]
```

### 9.3 Positions (30 features)
Up to 10 positions × 3 features:
```python
'positions': [
    # Position 1
    entry_price, bet_size, current_pnl_percent,
    # Position 2
    entry_price, bet_size, current_pnl_percent,
    # ... (repeat for positions 3-10)
]
```

### 9.4 Sidebets (3 features)
```python
'sidebets': [
    active,         # 1.0 if sidebet placed, 0.0 otherwise
    amount,         # Sidebet size (SOL)
    ticks_left,     # Ticks remaining in 40-tick window
]
```

### 9.5 Meta Context (24 features)
Data-driven scalping signals:
```python
'meta_context': [
    # Position timing
    position_entry_tick, ticks_in_position, position_age_percentile,
    # Price evolution
    price_velocity, price_acceleration, price_above_entry,
    # Risk indicators
    drawdown_from_peak, time_since_peak, drawdown_velocity,
    # Sweet spot proximity
    distance_to_sweet_spot_start, distance_to_sweet_spot_end,
    # Historical context
    recent_game_avg_duration, game_length_percentile,
    # Pattern signals
    ultra_short_pattern_score, moonshot_pattern_score,
    # Volatility evolution
    volatility_trend, volatility_acceleration,
    # Opportunity indicators
    missed_exit_count, optimal_exit_window_open,
    # Risk exposure
    total_exposure_ratio, risk_adjusted_pnl,
    # Bankroll health
    bankroll_percentile, capital_at_risk,
]
```

### 9.6 Sweet Spot (3 features)
```python
'sweet_spot': [
    in_sweet_spot,        # 1.0 if in 2-4x range, 0.0 otherwise
    ticks_in_sweet_spot,  # How long we've been in range
    sweet_spot_available, # 1.0 if not yet passed, 0.0 if passed
]
```

### 9.7 Duration Prediction (4 features)
```python
'duration_pred': [
    predicted_duration,    # Rolling average of last 5 games
    confidence,            # Prediction confidence
    cooldown_active,       # 1.0 if sidebet cooldown, 0.0 otherwise
    ticks_until_available, # Ticks until can place sidebet
]
```

### 9.8 Rug Prediction (5 features) **← THE BREAKTHROUGH**
```python
'rug_prediction': [
    probability,           # 0.0-1.0 (rug probability from model)
    confidence,            # 0.0-1.0 (prediction reliability)
    ticks_to_rug_norm,    # 0.0-1.0 (normalized ticks until rug)
    is_critical,           # 0.0 or 1.0 (emergency flag, prob ≥ 0.50)
    should_exit,           # 0.0 or 1.0 (exit recommendation, prob ≥ 0.40)
]
```

**Total**: 10 + 20 + 30 + 3 + 24 + 3 + 4 + 5 = **79 features**

---

## 10. Available Actions

The agent can take **8 discrete actions** per tick:

### 10.1 Action Space
```python
ACTION_WAIT = 0           # Do nothing this tick
ACTION_BUY_MAIN = 1       # Open main position
ACTION_SELL_MAIN = 2      # Close all positions
ACTION_BUY_SIDE = 3       # Place sidebet
ACTION_BUY_BOTH = 4       # Open position + place sidebet
ACTION_EMERGENCY_EXIT = 5 # Force close all positions
ACTION_PARTIAL_SELL = 6   # Close partial positions (10-100%)
ACTION_SKIP = 7           # Skip this game (no entry)
```

### 10.2 Action Parameters

**Bet Size** (9 options):
```python
BET_SIZES = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
```

**Sell Percent** (11 options):
```python
SELL_PERCENT = [0%, 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%]
```

**Action Space Structure**:
```python
MultiDiscrete([8, 9, 11])  # [action_type, bet_size_idx, sell_percent_idx]
```

### 10.3 Action Constraints

**Buy Actions** (BUY_MAIN, BUY_SIDE, BUY_BOTH):
- Require: `bankroll >= bet_size`
- Require: `position_count < 10` (for main position)
- Sidebet: Must be within first 40 ticks

**Sell Actions** (SELL_MAIN, EMERGENCY_EXIT, PARTIAL_SELL):
- Require: `has_positions == True`
- Execute immediately at current price
- Clear position tracking

**Skip Action**:
- Only effective at tick 0 (game start)
- Prevents entry for entire game
- Used for ultra-short pattern avoidance

---

## 11. Design Questions to Address

You should provide specific, numerical answers to these core questions:

### Q1: Component Weighting
**Current**: Volatility exit (8.0) is highest weighted
**Question**: Should rug_avoidance_reward be higher? By how much?
- Proposed weight: ___ (e.g., 10.0, 15.0, 20.0?)
- Justification: ___

### Q2: Sidebet Feature Integration
**Current**: 5 rug prediction features available but unused
**Question**: How should each feature be used?
- `probability`: ___
- `confidence`: ___
- `ticks_to_rug_norm`: ___
- `is_critical`: ___
- `should_exit`: ___

### Q3: Exit Reward Structure
**Question**: What bonuses for exiting at different rug probabilities?
- rug_prob ≥ 0.50: Bonus = ___ (e.g., +50.0?)
- rug_prob ≥ 0.40: Bonus = ___ (e.g., +30.0?)
- rug_prob ≥ 0.30: Bonus = ___ (e.g., +15.0?)

### Q4: Hold-Through Penalties
**Question**: What penalties for ignoring signals?
- Hold through critical (≥0.50): Penalty = ___ (e.g., -100.0?)
- Hold through high (≥0.40): Penalty = ___ (e.g., -50.0?)
- Hold through medium (≥0.30): Penalty = ___ (e.g., -25.0?)

### Q5: Early Exit Prevention
**Question**: How to prevent "always exit immediately"?
- Early exit during sweet spot (<0.20 rug_prob): Penalty = ___
- Conditions: ___

### Q6: Confidence Weighting
**Question**: Should rewards scale with prediction confidence?
- Formula: reward *= confidence? Or reward *= (confidence)^2?
- Minimum confidence to apply rewards: ___ (e.g., 0.60?)

### Q7: P&L Weight Reduction
**Current**: P&L weight = 1.0
**Question**: Should this be reduced to deprioritize greed?
- Proposed weight: ___ (e.g., 0.5, 0.3, 0.1?)
- Justification: ___

### Q8: Implementation Phasing
**Question**: Should changes roll out in phases or all at once?
- Phase 1 (Week 1): ___
- Phase 2 (Week 2): ___
- Phase 3 (Week 3): ___

---

## 12. Design Constraints

### 12.1 Hard Constraints (CANNOT Change)

**Observation Space**:
- ✅ Cannot add new observations (79 features fixed)
- ✅ Can use any/all of the 79 features
- ✅ 5 rug prediction features available

**Action Space**:
- ✅ Cannot add new actions (8 actions fixed)
- ✅ Can adjust action selection logic via rewards

**Game Mechanics**:
- ✅ Cannot change rug timing, payout ratios, cooldowns
- ✅ Must work within Rugs.fun rules

**Training Setup**:
- ✅ PPO algorithm (cannot change to SAC, DQN, etc.)
- ✅ 15-game episodes
- ✅ Initial bankroll 0.01 SOL

### 12.2 Soft Constraints (Can Change with Justification)

**Component Weights**:
- Can increase/decrease any component weight
- Must justify with data or logic

**Reward Component Addition**:
- Can add new reward components
- Must provide formula and weight

**Penalty Structure**:
- Can adjust penalty values
- Must ensure penalties are negative

**Thresholds**:
- Can adjust rug probability thresholds (0.30, 0.40, 0.50)
- Must justify based on sidebet model performance

### 12.3 Design Principles to Follow

1. **Rug Avoidance is Primary**: Weight must be >5.0x other components
2. **Use Sidebet Predictions Explicitly**: All 5 features should be used
3. **Severe Penalties for Ignoring Signals**: -50 to -100 for critical mistakes
4. **Balance Exit Timing**: Reward good exits, penalize premature exits
5. **Confidence Weighting**: Scale rewards by prediction confidence
6. **Phased Implementation**: Roll out in 3 phases with validation
7. **Quantified Targets**: All metrics must be measurable
8. **Implementability**: All recommendations must be deployable

---

## 13. Expected Outputs

You must provide these 8 deliverables:

1. **Component Weight Recommendations** (table format)
2. **New Reward Components** (pseudocode with formulas)
3. **Penalty Structure** (exact values and triggers)
4. **Sidebet Integration Strategy** (how to use 5 features)
5. **Implementation Roadmap** (3 phases with timeline)
6. **Success Metrics** (primary/secondary/tertiary targets)
7. **YAML Configuration** (complete config file)
8. **Validation Checklist** (before/during/after deployment)

See `LLM_INSTRUCTIONS.md` for detailed format requirements.

---

## 14. Reference Materials

### 14.1 Critical Files (Tier 1)
- Current reward calculator code
- Environment observation space code
- Sidebet model v3 success report (38% win rate)
- Game mechanics specification

### 14.2 Important Files (Tier 2)
- Pattern detector implementation
- Volatility tracker code
- Sweet spot detector logic
- Training configuration (PPO hyperparameters)

### 14.3 Supporting Files (Tier 3)
- Statistical analysis (p-values, correlations)
- Previous training failure logs
- Backtest results (baseline performance)
- Market pattern validation

### 14.4 Reference Files (Tier 4)
- Test suite (component testing)
- Alternative reward designs attempted
- Research papers (if applicable)

Request specific files from `BUNDLE.md` as needed.

---

## 15. Success Criteria

### Your Design is Successful If:

**Deliverables**:
- ✅ All 8 deliverables provided
- ✅ All numerical values are specific (not ranges)
- ✅ All recommendations have justification

**Design Quality**:
- ✅ Rug avoidance weight is >5.0 (highest priority)
- ✅ All 5 sidebet features are used in rewards
- ✅ Penalties for critical mistakes are >-50.0
- ✅ Early exit penalties prevent overfitting

**Expected Impact**:
- ✅ Expected rug avoidance: >90% (from 30%)
- ✅ Expected win rate: >60% (from 30%)
- ✅ Expected bankruptcy: <5% (from 20%)

**Implementability**:
- ✅ YAML config is complete and valid
- ✅ Pseudocode is clear and implementable
- ✅ Implementation roadmap has 3 phases
- ✅ Validation plan is concrete

### Your Design Needs Iteration If:

- ⚠️ Rug avoidance weight <2.0 (too low priority)
- ⚠️ Sidebet predictions underutilized (not in multiple components)
- ⚠️ Penalties are weak (<-10 for critical mistakes)
- ⚠️ No early exit penalties (risk of always-exit behavior)
- ⚠️ Success targets are vague or missing

---

## Summary

**The Challenge**: Current RL bot has 30% win rate and 30% rug avoidance. Too low.

**The Opportunity**: We have a sidebet model with 38% win rate that predicts rugs. It's available but unused.

**Your Mission**: Design rewards that teach the agent to use these predictions for >90% rug avoidance and >60% win rate.

**Key Insight**: Make rug avoidance the PRIMARY objective (weight >10.0), use all 5 prediction features, implement severe penalties for ignoring signals, and balance with early-exit penalties.

**Expected Outcome**: 3x improvement in rug avoidance, 2x improvement in win rate, 4x reduction in bankruptcy.

**Ready? Let's design the reward function that will transform this bot.**
