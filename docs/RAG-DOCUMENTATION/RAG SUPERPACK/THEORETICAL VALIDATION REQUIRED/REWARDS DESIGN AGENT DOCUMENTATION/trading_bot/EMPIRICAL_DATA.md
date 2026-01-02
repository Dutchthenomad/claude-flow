# Empirical Game Pattern Analysis
## 899-Game Dataset Analysis for RL Reward Design

**Generated**: 2025-11-08
**Dataset**: 899 games from `/home/nomad/rugs_recordings`
**Source Script**: `/home/nomad/Desktop/REPLAYER/analyze_trading_patterns.py`
**Priority**: **T1 - CRITICAL** (Read First - Empirical Foundation)

---

## Executive Summary

Analysis of 899 recorded Rugs.fun games reveals **critical insights that contradict common assumptions** and provide empirical foundation for RL reward function design.

### Key Discoveries

1. **Rug Rate Reality**: 96-100% of all entries eventually rug (not 50-60% assumed)
2. **Profit Opportunity Windows**: Entry at 1-50x offers 72-427% median max returns
3. **Volatility Reality**: Average drawdowns are 8-25%, not 10% (stop losses too tight)
4. **Survival Curves**: 98-99% survival for 20-200 ticks (games last longer than expected)
5. **Sweet Spot Zones**: Entry at 25-50x offers **best risk/reward** (75%+ profit achievement)
6. **NEW: Temporal Risk Model**: **50% of games rug by tick 138**, 79.3% by tick 300 (finite game lifespan)
7. **NEW: Position Duration**: Sweet spot entries (25-50x) exit in 48-60 ticks with 75% success
8. **NEW: Survivor Bias Warning**: "Hold for 300 ticks" strategies ignore that 79% of games already rugged

### Impact on Reward Design

**CRITICAL**: Current RL bot assumptions are fundamentally wrong. Empirical data shows:
- Entry timing matters more than assumed (25-50x sweet spot)
- Stop losses should be 30-50%, not 10%
- Profit targets must be dynamic based on entry point
- 100% of entries rug eventually - **exit timing is EVERYTHING**

---

## Phase 1: Entry Opportunity Analysis

### Methodology

For each entry multiplier (1x, 2x, 5x, 10x, 25x, 50x, 100x, 250x, 500x, 1000x, 2000x):
- Find all possible entries within 5% of target multiplier
- Calculate forward-looking returns from each entry
- Measure: max return achieved, eventual return (at rug), rug rate
- Calculate profit target achievement rates (10%, 25%, 50%, 100%, 200%)

### Results: Entry Opportunity Table

| Entry Multiplier | N Samples | Avg Max Return | Median Max Return | Rug Rate | 10% Target | 25% Target | 50% Target | 100% Target |
|-----------------|-----------|----------------|-------------------|----------|------------|------------|------------|-------------|
| **1x** | 140,384 | **373.4%** | **73.4%** | 96.4% | 82.1% | 72.5% | 59.7% | 43.8% |
| **2x** | 5,459 | 297.9% | 72.6% | 98.1% | 79.9% | 69.5% | 57.6% | 42.2% |
| **5x** | 1,847 | 329.8% | 48.4% | 96.6% | 79.9% | 65.5% | 48.3% | 30.8% |
| **10x** | 527 | 166.4% | 29.0% | 98.5% | 77.4% | 53.1% | 39.8% | 30.0% |
| **25x** | 271 | **814.5%** | **427.2%** | 100.0% | 83.4% | 76.8% | **74.5%** | **68.6%** |
| **50x** | 125 | 205.8% | 186.3% | 100.0% | 90.4% | 86.4% | **75.2%** | **75.2%** |
| **100x** | 77 | 94.5% | 32.5% | 100.0% | 93.5% | 59.7% | 36.4% | 9.1% |
| **500x** | 32 | 67.0% | 67.7% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |

### Key Insights

#### 🎯 Sweet Spot: 25-50x Entry Zone

**Entry at 25x**:
- **271 samples** (statistically significant)
- Median max return: **427.2%** (best in dataset)
- Average max return: **814.5%** (exceptional)
- 74.5% achieve 50% profit target
- 68.6% achieve 100% profit target
- **Interpretation**: Games that reach 25x often continue to 100-200x+ before rugging

**Entry at 50x**:
- **125 samples**
- Median max return: **186.3%**
- **75.2% achieve both 50% AND 100% profit targets** (highest success rate)
- **Interpretation**: Still excellent opportunity, more conservative than 25x

#### ⚠️ Rug Rate Reality Check

**100% of entries at 25x+ eventually rug** (not 50-60% assumed).

**Why this matters**:
- Cannot hold forever waiting for mega returns
- **Exit timing is EVERYTHING** - must exit before rug
- Sidebet model (38% win rate) is critical for detecting rug window
- Reward function must SEVERELY penalize holding past high rug probability

#### 💰 Profit Target Achievement by Entry Point

**Early Entry (1-10x)**:
- 82% achieve 10% profit
- 43-73% achieve 50% profit
- 30-44% achieve 100% profit
- **Strategy**: Conservative targets (25-50%) with high success rate

**Sweet Spot Entry (25-50x)**:
- 83-90% achieve 10% profit
- 75-86% achieve 50% profit
- **69-75% achieve 100% profit** (extraordinary)
- **Strategy**: Aggressive targets (50-100%) with high success rate

**Late Entry (100x+)**:
- 94-100% achieve 10% profit
- 36-60% achieve 50% profit
- Only 0-9% achieve 100% profit
- **Strategy**: Quick scalp targets (10-25%), exit fast

#### 📊 Entry Score Implications for RL Rewards

The **eventual return** column shows **-93.8% to -100%** (all entries rug):

| Entry | Eventual Return | Rug Rate |
|-------|----------------|----------|
| 1x | -93.8% | 96.4% |
| 2x | -97.4% | 98.1% |
| 5x | -96.1% | 96.6% |
| 10x | -98.9% | 98.5% |
| 25x | **-99.9%** | 100.0% |
| 50x | **-100.0%** | 100.0% |
| 100x | **-100.0%** | 100.0% |
| 500x | **-100.0%** | 100.0% |

**Interpretation**:
- If agent holds to rug, **100% loss** at all entry points
- "Eventual return" measures outcome if agent never exits
- **RL agent MUST learn to exit before rug** - no other path to profit

### Recommended Entry Strategy (For Reward Design)

```python
# Pseudocode for entry scoring in rewards

def calculate_entry_score(multiplier, tick, rug_probability):
    """
    Entry scoring based on empirical data
    """
    # Base score from empirical profit achievement rates
    if multiplier < 10:
        base_score = 0.5  # 50% achieve 50% profit
        target_profit = 0.25  # Conservative 25% target

    elif 10 <= multiplier < 25:
        base_score = 0.4  # 40% achieve 50% profit
        target_profit = 0.25

    elif 25 <= multiplier < 50:
        base_score = 0.75  # 75% achieve 50% profit (SWEET SPOT)
        target_profit = 0.50  # Aggressive 50% target

    elif 50 <= multiplier < 100:
        base_score = 0.75  # 75% achieve 50% profit
        target_profit = 0.50

    elif 100 <= multiplier < 500:
        base_score = 0.36  # 36% achieve 50% profit
        target_profit = 0.10  # Quick scalp

    else:  # 500x+
        base_score = 0.10  # High risk
        target_profit = 0.10

    # Penalty for high rug probability (sidebet model)
    if rug_probability >= 0.50:
        return 0.0  # NO ENTRY if critical rug risk
    elif rug_probability >= 0.40:
        base_score *= 0.3  # 70% penalty
    elif rug_probability >= 0.30:
        base_score *= 0.6  # 40% penalty

    return base_score, target_profit
```

---

## Phase 2: Volatility Analysis

### Methodology

For each multiplier zone (1-10x, 10-50x, 50-200x, 200-1000x, 1000x+):
- Measure tick-to-tick % price changes
- Track drawdowns from local peaks
- Classify drawdowns as: recovered (reached 95% of peak again) or rugged (game ended)

### Results: Tick-to-Tick Volatility by Zone

| Zone | Avg % Change | Median % Change | 90th Percentile | Max % Change |
|------|--------------|-----------------|-----------------|--------------|
| **1-10x** | 1.54% | 0.00% | 2.41% | 25.00% |
| **10-50x** | 3.85% | 1.67% | 16.61% | 24.96% |
| **50-200x** | 4.31% | 2.54% | 15.46% | 24.98% |
| **200-1000x** | 3.94% | 2.68% | 6.14% | 24.49% |

### Results: Drawdown Analysis

| Zone | Avg Drawdown | Max Drawdown | Recovery Rate | Rug Rate |
|------|--------------|--------------|---------------|----------|
| **1-10x** | 7.99% | 87.37% | **91.1%** | 8.6% |
| **10-50x** | 17.58% | 81.88% | **85.2%** | 14.5% |
| **50-200x** | 25.51% | 64.13% | **87.2%** | 12.8% |
| **200-1000x** | 13.85% | 45.13% | **100.0%** | 0.0% |

### Key Insights

#### 💡 Stop Loss Reality: 30-50%, NOT 10%

**Current assumption**: 10% stop loss protects capital.

**Empirical data**:
- Average drawdowns: **8-25%** depending on zone
- Max drawdowns: **45-87%** (!)
- **91.1% of drawdowns in 1-10x zone recover** (false alarm rate)

**Implications**:
- 10% stop loss triggers on **normal volatility**, not rug signals
- **30-50% stop loss** is more realistic for this game
- Better strategy: Use **sidebet model rug probability** as exit trigger, not fixed stop loss

#### 📉 Drawdown Recovery Rates

**High recovery rates across all zones** (85-100%):
- 91.1% recovery at 1-10x
- 85.2% recovery at 10-50x
- 87.2% recovery at 50-200x
- 100% recovery at 200-1000x (but 0% sample size issue)

**Interpretation**:
- Price volatility and temporary drawdowns are **normal game behavior**
- Do NOT exit on drawdown alone - wait for rug signal
- Sidebet model differentiates "normal volatility" from "rug imminent"

#### 🎯 Volatility-Adjusted Stop Losses (Recommendation)

```python
# Pseudocode for stop loss in rewards

def calculate_stop_loss(multiplier, baseline_volatility):
    """
    Dynamic stop loss based on zone volatility
    """
    if multiplier < 10:
        # Zone: 1-10x
        # Avg drawdown: 7.99%, Max: 87%
        # 91.1% recovery rate
        stop_loss = 0.40  # 40% (conservative, above avg)

    elif 10 <= multiplier < 50:
        # Zone: 10-50x
        # Avg drawdown: 17.58%, Max: 82%
        # 85.2% recovery rate
        stop_loss = 0.50  # 50% (wider for higher volatility)

    elif 50 <= multiplier < 200:
        # Zone: 50-200x
        # Avg drawdown: 25.51%, Max: 64%
        # 87.2% recovery rate
        stop_loss = 0.50  # 50%

    else:  # 200x+
        # Zone: 200-1000x
        # Avg drawdown: 13.85%, Max: 45%
        stop_loss = 0.35  # 35% (tighter for extreme zones)

    # Adjust for current volatility spike
    if baseline_volatility > 0.15:  # 15% baseline
        stop_loss *= 1.2  # Widen stops in volatile conditions

    return stop_loss


# HOWEVER: Prefer sidebet rug probability as primary exit signal
def should_exit(current_pnl, stop_loss, rug_probability, confidence):
    """
    Combine stop loss with rug prediction
    """
    # Exit if rug probability critical
    if rug_probability >= 0.50:
        return True, "CRITICAL_RUG_RISK"

    # Exit if high rug probability + drawdown approaching stop
    if rug_probability >= 0.40 and current_pnl < -stop_loss * 0.7:
        return True, "HIGH_RUG_RISK_WITH_DRAWDOWN"

    # Exit if stop loss breached (safety net)
    if current_pnl < -stop_loss:
        return True, "STOP_LOSS"

    return False, None
```

---

## Phase 3: Survival Curve Analysis

### Methodology

For each (multiplier zone, tick) combination:
- Measure survival probability at horizons: 20, 50, 100, 200 ticks
- Survival = game does not rug within N ticks from current tick
- Build probability matrix

### Results: Survival Probability Matrix

| Zone | 20 Ticks | 50 Ticks | 100 Ticks | 200 Ticks |
|------|----------|----------|-----------|-----------|
| **1-10x** | 99.5% | 99.4% | 99.2% | 98.9% |
| **10-50x** | 98.7% | 98.7% | 98.9% | 98.8% |
| **50-200x** | 99.3% | 99.0% | 99.2% | 98.4% |
| **200-1000x** | 99.0% | 98.8% | 98.2% | 100.0% |

### Key Insights

#### 🕐 Games Last Longer Than Expected

**Assumption**: Most games rug within 50-100 ticks.

**Empirical data**:
- **98.9% survival at 200 ticks** (1-10x zone)
- **98.4% survival at 200 ticks** (50-200x zone)
- Games routinely last 300-500+ ticks

**Implications**:
- Agent has MORE time to make decisions than assumed
- Holding for 50-100 ticks is NOT inherently risky
- **Rug timing is NOT tick-based** - it's **price/volatility-based** (hence sidebet model)

#### 📊 Survival Curves Are Flat (High Survival)

**Surprise finding**: Survival probability barely decreases with time.
- 20 ticks: 98.7-99.5%
- 200 ticks: 98.4-100%
- **Only ~1-2% decrease over 180 ticks**

**Interpretation**:
1. Rugs are **not time-dependent** (no "expiration timer")
2. Rugs are **event-dependent** (price spikes, volatility, smart money exit)
3. **Holding duration alone is not a strong predictor** of rug
4. **Sidebet model features (z-score, volatility) are better predictors**

#### 🎯 Implications for RL Hold Duration Rewards

```python
# WRONG approach (time-based penalty):
hold_duration_penalty = -0.01 * ticks_held  # Penalize holding longer

# RIGHT approach (state-based penalty):
def calculate_hold_risk(ticks_held, rug_probability, multiplier):
    """
    Hold risk based on rug probability, NOT duration
    """
    # Base risk from sidebet model
    base_risk = rug_probability

    # Slight increase for extreme multipliers (>500x)
    if multiplier > 500:
        base_risk *= 1.2

    # Duration is NOT a primary factor (survival curves are flat)
    # Only penalize extreme hold times (>300 ticks) slightly
    if ticks_held > 300:
        duration_penalty = 0.1  # Small 10% increase
    else:
        duration_penalty = 0.0

    return base_risk * (1 + duration_penalty)
```

**Key takeaway**: Do NOT penalize hold duration directly. Penalize holding **when rug probability is high**.

---

## Phase 4: Profit Distribution Analysis

### Methodology

For each entry point (1x, 5x, 10x, 25x, 50x, 100x, 250x, 500x):
- Calculate maximum forward return achieved from entry
- Measure profit target achievement rates: 10%, 25%, 50%, 100%, 200%
- Calculate average returns

### Results: Profit Achievement Rates (%)

| Entry | N Samples | 10% | 25% | 50% | 100% | 200% | Avg Return |
|-------|-----------|-----|-----|-----|------|------|------------|
| **1x** | 140,384 | 82.1 | 72.5 | 59.7 | 43.8 | 26.8 | 373.4% |
| **5x** | 1,847 | 79.9 | 65.5 | 48.3 | 30.8 | 16.1 | 329.8% |
| **10x** | 527 | 77.4 | 53.1 | 39.8 | 30.0 | 19.5 | 166.4% |
| **25x** | 271 | 83.4 | 76.8 | **74.5** | **68.6** | **58.3** | **814.5%** |
| **50x** | 125 | 90.4 | 86.4 | **75.2** | **75.2** | 29.6 | 205.8% |
| **100x** | 77 | 93.5 | 59.7 | 36.4 | 9.1 | 9.1 | 94.5% |
| **500x** | 32 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 67.0% |

### Key Insights

#### 🎯 Dynamic Profit Targets by Entry Point

**Entry at 1-10x** (Early Entry):
- Conservative: **25% target** (72.5% achievement at 1x)
- Moderate: **50% target** (59.7% achievement at 1x)
- Aggressive: **100% target** (43.8% achievement at 1x)

**Entry at 25-50x** (SWEET SPOT):
- Conservative: **50% target** (74.5% achievement at 25x)
- Moderate: **100% target** (68.6% achievement at 25x)
- Aggressive: **200% target** (58.3% achievement at 25x)
- **This is THE opportunity zone**

**Entry at 100x+** (Late Entry):
- Conservative: **10% target** (93.5% achievement at 100x)
- Moderate: **25% target** (59.7% achievement at 100x)
- Aggressive: **50% target** (36.4% achievement at 100x)
- **Quick scalp only**

#### 📊 Recommended Profit Targets (For Reward Design)

Based on **50%+ achievement rate** threshold:

| Entry Multiplier | Recommended Target | Conservative | Aggressive | Achievement Rate |
|-----------------|-------------------|--------------|------------|------------------|
| 1x | 50% | 35% | 65% | 59.7% |
| 5x | 25% | 18% | 32% | 65.5% |
| 10x | 25% | 18% | 32% | 53.1% |
| **25x** | **200%** | **140%** | **260%** | **58.3%** |
| **50x** | **100%** | **70%** | **130%** | **75.2%** |
| 100x | 25% | 18% | 32% | 59.7% |
| 500x | 50% | 35% | 65% | 100.0%* |

*Small sample size (N=32)

#### 🎯 Profit Target Reward Function (Pseudocode)

```python
def calculate_profit_target_reward(entry_price, current_price, multiplier):
    """
    Dynamic profit target based on entry multiplier
    """
    current_return = (current_price - entry_price) / entry_price

    # Determine target based on entry multiplier
    if multiplier < 10:
        target = 0.50  # 50%
    elif 10 <= multiplier < 25:
        target = 0.25  # 25%
    elif 25 <= multiplier < 50:
        target = 2.00  # 200% (SWEET SPOT)
    elif 50 <= multiplier < 100:
        target = 1.00  # 100%
    elif 100 <= multiplier < 500:
        target = 0.25  # 25%
    else:
        target = 0.50  # 50%

    # Reward for reaching target
    if current_return >= target:
        return +100.0  # Major reward - TARGET ACHIEVED

    # Partial reward for progress toward target
    elif current_return >= target * 0.7:
        return +20.0 * (current_return / target)  # Scaled reward

    # Small reward for positive progress
    elif current_return > 0:
        return +5.0 * (current_return / target)

    # No penalty for not reaching target (yet)
    else:
        return 0.0


def calculate_exit_timing_reward(current_return, rug_probability, confidence):
    """
    Reward for exiting at right time (before rug)
    """
    # CRITICAL: Reward early exit if rug probability high
    if rug_probability >= 0.50 and current_return > 0:
        # Exited with profit before critical rug - EXCELLENT
        return +200.0

    elif rug_probability >= 0.40 and current_return > 0:
        # Exited with profit before high rug - GOOD
        return +100.0

    elif rug_probability >= 0.30 and current_return > 0:
        # Exited with profit before medium rug - OK
        return +50.0

    # Penalize holding past critical rug probability
    elif rug_probability >= 0.50 and current_return < 0:
        # Still holding despite critical rug risk - BAD
        return -100.0

    else:
        return 0.0
```

---

## Bayesian Model Parameters (Generated from Data)

### Entry Score Table

Based on empirical success rates and rug rates:

| Entry Multiplier | Score | Base Return | Rug Risk |
|-----------------|-------|-------------|----------|
| 1x | 0.000 | -93.8% | 96.4% |
| 2x | 0.000 | -97.4% | 98.1% |
| 5x | 0.000 | -96.1% | 96.6% |
| 10x | 0.000 | -98.9% | 98.5% |
| **25x** | **0.000** | **-99.9%** | **100.0%** |
| **50x** | **0.000** | **-100.0%** | **100.0%** |
| 100x | 0.000 | -100.0% | 100.0% |
| 500x | 0.000 | -100.0% | 100.0% |

**NOTE**: All scores are 0.000 because **eventual return** (if held to rug) is negative 93-100%.

**Critical interpretation**:
- **No entry point is profitable if held to rug**
- Entry timing alone is insufficient
- **Exit timing is EVERYTHING** - must use sidebet model

### Risk Zones

Classify multiplier ranges by risk:

```python
risk_zones = {
    'green': (1.0, 10.0),        # Low risk, moderate returns (25-50% targets)
    'yellow': (10.0, 50.0),      # Medium risk, high returns (50-100% targets)
    'orange': (50.0, 200.0),     # High risk, very high returns (100-200% targets)
    'red': (200.0, float('inf')) # Extreme risk, quick scalp only (10-25% targets)
}
```

---

## Critical Recommendations for RL Reward Design

### 1. Abandon Fixed Stop Losses (10%)

**Empirical data shows**:
- Average drawdowns: 8-25%
- Recovery rates: 85-91%
- 10% stop loss triggers on normal volatility (false alarms)

**Recommendation**:
```python
# INSTEAD OF:
if pnl < -0.10:
    reward = -100  # Stop loss penalty

# USE:
if rug_probability >= 0.50:
    reward = -100  # Exit on rug signal, not fixed stop
elif rug_probability >= 0.40 and pnl < -0.30:
    reward = -50  # Combine rug signal + drawdown
```

### 2. Use Dynamic Profit Targets

**Empirical data shows** entry point determines achievable profit:

```python
profit_targets = {
    (1, 10): 0.25,      # 25% target (53-73% achievable)
    (10, 25): 0.25,     # 25% target
    (25, 50): 2.00,     # 200% target (58% achievable) - SWEET SPOT
    (50, 100): 1.00,    # 100% target (75% achievable)
    (100, 500): 0.25,   # 25% target (quick scalp)
    (500, inf): 0.50    # 50% target (extreme risk)
}

def get_target(entry_multiplier):
    for (low, high), target in profit_targets.items():
        if low <= entry_multiplier < high:
            return target
    return 0.10  # Default
```

### 3. Prioritize 25-50x Entry Zone

**Empirical data shows** 25-50x offers **best risk/reward**:
- 74.5% achieve 50% profit (25x entry)
- 75.2% achieve 100% profit (50x entry)
- Median returns: 186-427%

**Recommendation**:
```python
def calculate_entry_bonus(multiplier):
    """Bonus reward for entering sweet spot zone"""
    if 25 <= multiplier < 50:
        return +50.0  # Major bonus
    elif 10 <= multiplier < 25 or 50 <= multiplier < 100:
        return +20.0  # Moderate bonus
    elif multiplier < 10:
        return +5.0   # Small bonus (early entry OK)
    else:
        return 0.0    # No bonus (risky late entry)
```

### 4. Severe Penalties for Ignoring Rug Signals

**Empirical data shows** 100% of entries rug eventually - **must exit before rug**:

```python
def calculate_rug_penalty(position_active, rug_probability, ticks_held_at_high_prob):
    """
    Penalize holding when rug probability critical
    """
    if not position_active:
        return 0.0

    if rug_probability >= 0.50:
        # Critical rug probability - MUST EXIT
        penalty = -50.0 * (1 + ticks_held_at_high_prob * 0.1)
        return penalty

    elif rug_probability >= 0.40:
        # High rug probability - should exit
        penalty = -20.0 * (1 + ticks_held_at_high_prob * 0.05)
        return penalty

    elif rug_probability >= 0.30:
        # Medium rug probability - warning
        penalty = -5.0
        return penalty

    return 0.0
```

### 5. Reward Exit Timing, Not Hold Duration

**Empirical data shows** survival curves are flat (98-99% across 20-200 ticks):
- Hold duration is NOT predictive of rug
- Rug is event-driven (volatility, price action)
- Sidebet model captures this

**Recommendation**:
```python
# WRONG:
hold_penalty = -0.01 * ticks_held  # Penalize holding longer

# RIGHT:
def calculate_exit_timing_reward(exited, rug_occurred_within_N_ticks, profit):
    """
    Reward for exiting BEFORE rug (not exiting early)
    """
    if exited and rug_occurred_within_N_ticks <= 20 and profit > 0:
        # Exited just before rug with profit - PERFECT TIMING
        return +200.0

    elif exited and rug_occurred_within_N_ticks <= 50 and profit > 0:
        # Exited before rug with profit - GOOD TIMING
        return +100.0

    elif not exited and rug_occurred_within_N_ticks <= 20:
        # Failed to exit before rug - BAD
        return -200.0

    return 0.0
```

---

## Phase 5: Position Duration & Temporal Risk Analysis

### Methodology

**NEW ANALYSIS** (2025-11-08 update): Additional analysis of 899 games to determine:
1. **Survival curve by absolute tick** (P(game survives past tick N))
2. **Average position hold durations** (from entry to profitable exit or rug)
3. **Hold time vs success rate** (optimal hold durations by zone)
4. **Bayesian temporal risk parameters**

**Source**: `/home/nomad/Desktop/REPLAYER/analyze_position_duration.py`

### Results: Survival Curve by Absolute Tick

**CRITICAL FINDING**: This is fundamentally different from earlier "survival from current position" analysis.

| Tick Checkpoint | Survived | Rugged | P(Survive) |
|----------------|----------|--------|------------|
| 50 | 689 | 210 | **76.6%** |
| 100 | 552 | 347 | **61.4%** |
| 150 | 418 | 481 | **46.5%** |
| 200 | 320 | 579 | **35.6%** |
| 250 | 248 | 651 | **27.6%** |
| 300 | 186 | 713 | **20.7%** |
| 400 | 117 | 782 | **13.0%** |
| 500 | 61 | 838 | **6.8%** |
| 1000 | 7 | 892 | **0.8%** |

#### Rug Timing Statistics

- **Mean rug tick**: 194.7
- **Median rug tick**: **138.0** (50% of games rug by tick 138)
- **Std dev**: 196.1
- **Min rug tick**: 0
- **Max rug tick**: 1,308

#### Rug Tick Percentiles

| Percentile | Rug Tick | Interpretation |
|------------|----------|----------------|
| P10 | 19.0 | 10% of games rug by tick 19 |
| P25 | 55.0 | 25% of games rug by tick 55 (relatively safe before this) |
| **P50** | **138.0** | **50% of games rug by tick 138** |
| P75 | 267.5 | 75% of games rug by tick 268 |
| P90 | 441.2 | 90% of games rug by tick 441 |
| P95 | 540.0 | 95% of games rug by tick 540 |
| P99 | 916.3 | 99% of games rug by tick 916 |

#### Hazard Rate (Rug Probability Density)

| Tick Range | Games Rugged | Percentage |
|------------|--------------|------------|
| 0-100 | 344 | **38.3%** (highest density) |
| 100-200 | 235 | **26.1%** |
| 200-300 | 132 | 14.7% |
| 300-400 | 71 | 7.9% |
| 400-500 | 56 | 6.2% |
| 500-600 | 22 | 2.4% |
| 600+ | 39 | 4.3% |

### Key Insights

#### 🎯 Temporal Risk Model

**Cumulative rug probability by tick**:

```python
temporal_risk = {
    50: 0.234,   # 23.4% of games have rugged by tick 50
    100: 0.386,  # 38.6% by tick 100
    150: 0.535,  # 53.5% by tick 150
    200: 0.644,  # 64.4% by tick 200
    250: 0.724,  # 72.4% by tick 250
    300: 0.793,  # 79.3% by tick 300
    400: 0.870,  # 87.0% by tick 400
    500: 0.932,  # 93.2% by tick 500
    1000: 0.992  # 99.2% by tick 1000
}
```

**Interpretation**:
- Games have a **finite lifespan** - median is 138 ticks
- **38.3% of rugs happen in first 100 ticks** (early rugs are common)
- By tick 300, **79.3% of games have rugged**
- Very few games (0.8%) survive past tick 1000

**Compare to earlier finding** (Phase 3):
- Earlier: "98-99% survival for 20-200 ticks *from current position*"
- Now: "Only 35.6% survival *to absolute tick 200*"

**Resolution**: Earlier analysis measured "survive N more ticks from now", which is condition on still being alive. This analysis measures "survive to absolute tick N from game start", which accounts for all games including early rugs.

#### ⏰ Exit Urgency Model (Bayesian Parameters)

Based on empirical rug timing:

| Risk Window | Tick Range | Description |
|-------------|------------|-------------|
| **Safe** | < 69 ticks | Low time-based risk (before 50% of median) |
| **Caution** | 69-104 ticks | Moderate time-based risk (50-75% of median) |
| **Danger** | 104-138 ticks | High time-based risk (75-100% of median) |
| **Critical** | > 268 ticks | Extreme time-based risk (past P75, 75% already rugged) |

**Pseudocode for temporal risk factor**:

```python
def calculate_temporal_risk_factor(current_tick):
    """
    Returns temporal risk multiplier based on absolute tick number
    """
    if current_tick < 69:
        return 1.0  # Baseline risk
    elif current_tick < 104:
        return 1.3  # +30% risk from time alone
    elif current_tick < 138:
        return 1.6  # +60% risk (approaching median rug)
    elif current_tick < 268:
        return 2.0  # 2x risk (past median)
    else:
        return 3.0  # 3x risk (extreme danger zone)

# Integrate with sidebet model:
def combined_rug_risk(rug_probability, confidence, current_tick):
    """
    Combine sidebet prediction with temporal risk
    """
    # Base risk from sidebet model
    base_risk = rug_probability * confidence

    # Temporal adjustment
    temporal_factor = calculate_temporal_risk_factor(current_tick)

    # Combined risk (capped at 1.0)
    combined = min(1.0, base_risk * temporal_factor)

    return combined
```

### Results: Position Hold Duration

**Analysis**: Simulated entering at various multipliers and measured how long positions were held until:
- Reaching profit target (win), or
- Game rugged (loss)

#### Position Hold Times by Entry Point (50% Profit Target)

| Entry Multiplier | N Samples | Success Rate | Avg Hold (All) | Avg Hold (Win) | Avg Hold (Loss) |
|-----------------|-----------|--------------|----------------|----------------|-----------------|
| **1x** | 137,426 | **61.0%** | 83.9 ticks | 65.1 ticks | 113.4 ticks |
| **5x** | 1,810 | 49.3% | 85.5 ticks | 63.4 ticks | 107.0 ticks |
| **10x** | 519 | 40.5% | 60.1 ticks | 37.1 ticks | 75.8 ticks |
| **25x** | 271 | **74.5%** 🔥 | 54.9 ticks | **60.0 ticks** | 39.9 ticks |
| **50x** | 125 | **75.2%** 🔥 | 45.3 ticks | **48.0 ticks** | 37.0 ticks |
| **100x** | 77 | 36.4% | 94.4 ticks | 71.1 ticks | 107.7 ticks |
| **500x** | 32 | 100.0% * | 50.6 ticks | 50.6 ticks | N/A |

*Small sample size (N=32)

#### Key Insights from Position Duration

**1. Sweet Spot Entries (25-50x) Have FASTER Exits**:
- Entry at 25x: **60.0 ticks** avg hold (74.5% success)
- Entry at 50x: **48.0 ticks** avg hold (75.2% success)
- **Interpretation**: These entries hit profit targets quickly (within 45-60 ticks)

**2. Late Entries (100x+) Take LONGER**:
- Entry at 100x: **71.1 ticks** avg hold for wins
- **Problem**: By this time, temporal risk is already high (past safe window)

**3. Losing Positions Hold Longer**:
- Entry at 1x: 65.1 ticks (win) vs 113.4 ticks (loss) - **74% longer**
- Entry at 25x: 60.0 ticks (win) vs 39.9 ticks (loss) - loss happens FASTER
- **Interpretation**: At 25-50x, when it rugs, it rugs fast (no time to exit)

**4. Optimal Hold Times (for 50% target)**:

```python
optimal_hold_times = {
    1: 65.1,    # 61% success rate
    5: 63.4,    # 49% success rate
    10: 37.1,   # 40% success rate
    25: 60.0,   # 75% success rate  ← BEST
    50: 48.0,   # 75% success rate  ← BEST
    100: 71.1,  # 36% success rate
    500: 50.6   # 100% success rate (but N=32, unreliable)
}
```

### Results: Hold Time vs Success Rate

**Analysis**: For fixed hold durations (10, 20, 50, 100, 150, 200, 300 ticks), what's the success rate by zone?

#### Success Rate by Hold Duration and Zone

| Zone | Hold (Ticks) | N Samples | Success Rate | Avg PnL | Median PnL |
|------|--------------|-----------|--------------|---------|------------|
| **1-10x** | 10 | 217,957 | 26.1% | 1.4% | 0.0% |
| **1-10x** | 50 | 194,990 | 31.7% | 10.4% | 0.0% |
| **1-10x** | 100 | 164,237 | 42.6% | 26.0% | 0.0% |
| **1-10x** | 150 | 131,057 | 57.6% | 49.4% | 9.6% |
| **1-10x** | 200 | 99,679 | 59.9% | 81.3% | 23.8% |
| **1-10x** | **300** | 56,224 | **63.5%** | **159.1%** | 47.3% |
|  |  |  |  |  |  |
| **10-50x** | 10 | 4,354 | 60.0% | 4.2% | 4.2% |
| **10-50x** | 50 | 3,377 | 60.5% | 29.5% | 13.6% |
| **10-50x** | 100 | 2,545 | 68.0% | 72.2% | 40.6% |
| **10-50x** | 150 | 1,850 | 72.8% | 125.9% | 69.8% |
| **10-50x** | 200 | 1,324 | 80.6% | 228.7% | 148.8% |
| **10-50x** | **300** | 672 | **95.7%** 🔥 | **688.1%** 🔥 | 427.2% |
|  |  |  |  |  |  |
| **50-200x** | 10 | 954 | 53.9% | 2.4% | 1.8% |
| **50-200x** | 50 | 797 | 55.6% | 16.6% | 5.3% |
| **50-200x** | 100 | 606 | 50.0% | 39.0% | -0.3% |
| **50-200x** | **200** | 371 | 50.1% | 130.5% | 0.1% |
|  |  |  |  |  |  |
| **200-1000x** | 50 | 163 | 70.6% | 30.9% | 36.3% |
| **200-1000x** | 100 | 113 | 90.3% | 74.2% | 46.1% |
| **200-1000x** | **150** | 63 | **96.8%** | 94.6% | 108.2% |

#### CRITICAL Insight: Survivor Bias

**WARNING**: The "optimal hold times" above suffer from **survivor bias**:
- 10-50x zone, 300 ticks hold: 95.7% success, 688% avg PnL
- **BUT**: Only 672 samples (out of 3,377 at 50 ticks)
- **Interpretation**: By tick 300, most games have already rugged (79.3% cumulative rug probability)
- The 672 samples are **only the games that survived to tick 300**
- This does NOT mean "hold for 300 ticks" is optimal

**Correct Interpretation**:
- **IF the game survives to tick 300**, AND you entered at 10-50x, you have 95.7% chance of profit
- **BUT**: 79.3% of games don't survive to tick 300
- **Therefore**: Cannot plan to hold for 300 ticks - must use sidebet model to detect rug before it happens

### Bayesian Model Parameters (Temporal)

Based on position duration and survival analysis:

```python
class TemporalBayesianParameters:
    """
    Empirically-derived temporal risk parameters
    """

    # 1. Cumulative rug probability by tick
    TEMPORAL_RUG_PROB = {
        50: 0.234,
        100: 0.386,
        150: 0.535,
        200: 0.644,
        250: 0.724,
        300: 0.793,
        400: 0.870,
        500: 0.932,
        1000: 0.992
    }

    # 2. Optimal hold times by entry (50% target)
    OPTIMAL_HOLD = {
        1: 65,    # ticks
        5: 63,
        10: 37,
        25: 60,   # Sweet spot
        50: 48,   # Sweet spot
        100: 71
    }

    # 3. Exit urgency thresholds
    EXIT_URGENCY = {
        'safe': 69,        # < 69 ticks (low risk)
        'caution': 104,    # 69-104 ticks (moderate)
        'danger': 138,     # 104-138 ticks (high risk, median rug)
        'critical': 268    # > 268 ticks (extreme risk, P75)
    }

    # 4. Zone-based survival multipliers
    ZONE_SURVIVAL_ADJUSTMENT = {
        (1, 10): 1.0,      # Baseline
        (10, 50): 0.9,     # Slightly lower survival
        (50, 200): 0.85,   # Lower survival
        (200, 1000): 0.95  # Small sample, uncertain
    }

    @staticmethod
    def get_temporal_risk(current_tick):
        """Get interpolated temporal rug probability"""
        if current_tick <= 50:
            return 0.234 * (current_tick / 50)
        elif current_tick <= 100:
            return 0.234 + (0.386 - 0.234) * ((current_tick - 50) / 50)
        elif current_tick <= 150:
            return 0.386 + (0.535 - 0.386) * ((current_tick - 100) / 50)
        elif current_tick <= 200:
            return 0.535 + (0.644 - 0.535) * ((current_tick - 150) / 50)
        elif current_tick <= 300:
            return 0.644 + (0.793 - 0.644) * ((current_tick - 200) / 100)
        elif current_tick <= 500:
            return 0.793 + (0.932 - 0.793) * ((current_tick - 300) / 200)
        else:
            return min(0.99, 0.932 + (current_tick - 500) * 0.0001)

    @staticmethod
    def get_exit_urgency_level(current_tick):
        """Get urgency level (0-3) based on tick"""
        if current_tick < 69:
            return 0  # Safe
        elif current_tick < 104:
            return 1  # Caution
        elif current_tick < 138:
            return 2  # Danger
        else:
            return 3  # Critical
```

### Reward Function Integration (Temporal + Sidebet)

```python
def calculate_rug_avoidance_reward(state, action, info):
    """
    Combine sidebet prediction with temporal risk
    """
    # Extract features
    rug_probability = state['rug_probability']  # From sidebet model
    confidence = state['confidence']
    current_tick = state['tick']
    position_active = info.get('position_active', False)
    pnl = info.get('pnl', 0.0)

    # 1. Get temporal risk factor
    temporal_risk = TemporalBayesianParameters.get_temporal_risk(current_tick)
    urgency_level = TemporalBayesianParameters.get_exit_urgency_level(current_tick)

    # 2. Combine sidebet + temporal
    # Sidebet model is primary (trained signal)
    # Temporal risk is secondary (statistical prior)
    combined_risk = max(rug_probability, temporal_risk * 0.5)  # Sidebet dominates

    # 3. Urgency penalty if holding too long
    if position_active and urgency_level >= 2:  # Danger or Critical
        hold_penalty = -10.0 * urgency_level  # -20 for Danger, -30 for Critical
    else:
        hold_penalty = 0.0

    # 4. Exit timing reward
    if action == 'EXIT' and position_active and pnl > 0:
        # Reward exiting with profit before rug
        if combined_risk >= 0.50:
            exit_reward = +200.0  # Exited at critical risk
        elif combined_risk >= 0.40:
            exit_reward = +100.0  # Exited at high risk
        elif combined_risk >= 0.30:
            exit_reward = +50.0   # Exited at medium risk
        else:
            exit_reward = +10.0   # Exited with profit (always good)

        # Bonus if exiting in danger/critical temporal window
        if urgency_level >= 2:
            exit_reward *= 1.5  # 50% bonus for late-game exit

    else:
        exit_reward = 0.0

    # 5. Hold penalty if ignoring signals
    if position_active and action != 'EXIT':
        if combined_risk >= 0.50:
            ignore_penalty = -100.0  # Critical risk, MUST exit
        elif combined_risk >= 0.40:
            ignore_penalty = -50.0   # High risk, should exit
        elif combined_risk >= 0.30 and urgency_level >= 2:
            ignore_penalty = -20.0   # Medium risk + late game = bad
        else:
            ignore_penalty = 0.0
    else:
        ignore_penalty = 0.0

    # Total reward
    total = hold_penalty + exit_reward + ignore_penalty

    return total
```

---

## Integration with Sidebet Model

### Sidebet Model Performance (Recap)

- **Win rate**: 38.1% (vs 16.7% random)
- **ROI**: 754% on 200-game backtest
- **Martingale success**: 100% (never bankrupted)
- **Features**: 5 prediction values every tick
  - `rug_probability`: 0.0-1.0
  - `confidence`: 0.0-1.0
  - `ticks_to_rug_norm`: 0.0-1.0
  - `is_critical`: 0.0 or 1.0 (prob ≥ 0.50)
  - `should_exit`: 0.0 or 1.0 (prob ≥ 0.40)

### Combined Strategy: Empirical Data + Sidebet Predictions

```python
class EmpiricalBayesianRewardFunction:
    """
    Reward function combining empirical game patterns with sidebet predictions
    """

    def __init__(self):
        # Load empirical profit targets
        self.profit_targets = {
            (1, 10): 0.25,
            (10, 25): 0.25,
            (25, 50): 2.00,  # SWEET SPOT
            (50, 100): 1.00,
            (100, 500): 0.25,
            (500, float('inf')): 0.50
        }

        # Load empirical stop losses (zone-based)
        self.stop_losses = {
            (1, 10): 0.40,
            (10, 50): 0.50,
            (50, 200): 0.50,
            (200, float('inf')): 0.35
        }

    def calculate_reward(self, state, action, next_state, info):
        """
        Calculate reward using empirical data + sidebet predictions
        """
        reward = 0.0

        # Extract state info
        multiplier = state['current_price']
        pnl = info.get('pnl', 0.0)
        position_active = info.get('position_active', False)
        rug_probability = state['rug_probability']
        confidence = state['confidence']
        is_critical = state['is_critical']
        should_exit = state['should_exit']

        # 1. Entry Reward (based on empirical sweet spot)
        if action == 'ENTER' and not position_active:
            if 25 <= multiplier < 50:
                reward += 50.0  # Sweet spot entry
            elif 10 <= multiplier < 25 or 50 <= multiplier < 100:
                reward += 20.0  # Good entry
            elif multiplier < 10:
                reward += 5.0   # Early entry OK
            # Late entry (>100x) gets no bonus

        # 2. Profit Target Reward (dynamic based on entry)
        if position_active:
            entry_mult = info.get('entry_multiplier', multiplier)
            target = self._get_profit_target(entry_mult)

            if pnl >= target:
                reward += 100.0  # Target achieved!
            elif pnl >= target * 0.7:
                reward += 20.0 * (pnl / target)  # Partial progress

        # 3. Rug Avoidance Penalty (PRIMARY FACTOR)
        if position_active:
            if is_critical:  # rug_prob ≥ 0.50
                # CRITICAL: Must exit immediately
                if action != 'EXIT':
                    reward -= 100.0  # Severe penalty for ignoring critical signal

            elif should_exit:  # rug_prob ≥ 0.40
                # HIGH: Should exit
                if action != 'EXIT':
                    reward -= 50.0  # Penalty for ignoring exit signal

            elif rug_probability >= 0.30:
                # MEDIUM: Warning signal
                if action != 'EXIT':
                    reward -= 10.0  # Small penalty

        # 4. Exit Timing Reward (reward exiting before rug)
        if action == 'EXIT' and position_active and pnl > 0:
            if is_critical:
                reward += 200.0  # Perfect timing - exited at critical rug signal
            elif should_exit:
                reward += 100.0  # Good timing - exited at high rug signal
            elif rug_probability >= 0.30:
                reward += 50.0   # OK timing - exited at medium signal

        # 5. Stop Loss (zone-based, but secondary to rug signals)
        if position_active:
            stop_loss = self._get_stop_loss(multiplier)
            if pnl < -stop_loss:
                reward -= 100.0  # Emergency stop loss

        # 6. Rug Event Penalty (if agent failed to exit)
        if info.get('rugged', False) and position_active:
            reward -= 200.0  # Catastrophic failure - held through rug

        return reward

    def _get_profit_target(self, entry_multiplier):
        """Get empirical profit target for entry point"""
        for (low, high), target in self.profit_targets.items():
            if low <= entry_multiplier < high:
                return target
        return 0.10  # Default

    def _get_stop_loss(self, multiplier):
        """Get empirical stop loss for multiplier zone"""
        for (low, high), stop in self.stop_losses.items():
            if low <= multiplier < high:
                return stop
        return 0.40  # Default
```

---

## Summary: Empirical Findings for Agent

### Top 5 Critical Insights

1. **100% of entries rug eventually** → Exit timing is EVERYTHING (sidebet model is critical)

2. **25-50x is the sweet spot** → 75% achieve 50-100% profit targets (prioritize this zone)

3. **Stop losses should be 30-50%, not 10%** → Average drawdowns are 8-25%, recovery rate is 85-91%

4. **Survival curves are flat** → Don't penalize hold duration, penalize ignoring rug signals

5. **Dynamic profit targets** → 1-10x target 25%, 25-50x target 100-200%, 100x+ target 10-25%

### Reward Function Design Priorities

**Primary** (weight 5.0x+):
1. Rug avoidance (use sidebet `is_critical` and `should_exit` flags)
2. Exit timing (reward exiting BEFORE rug, not early exit)

**Secondary** (weight 1.0-2.0x):
3. Profit target achievement (dynamic based on entry point)
4. Entry zone selection (bonus for 25-50x sweet spot)

**Tertiary** (weight 0.1-0.5x):
5. Risk management (zone-based stop losses, 30-50%)
6. Position sizing (scale by entry score and rug probability)

### Integration Checklist for Agent

When designing rewards, ensure:

- [ ] Sidebet predictions (`rug_probability`, `is_critical`, `should_exit`) are **primary factors**
- [ ] Profit targets are **dynamic** based on `entry_multiplier`
- [ ] Stop losses are **zone-based** (30-50%), not fixed 10%
- [ ] Entry bonuses prioritize **25-50x zone** (sweet spot)
- [ ] Hold duration is **not penalized** (survival curves are flat)
- [ ] Rug event has **catastrophic penalty** (-200) if position held
- [ ] Exit timing is **rewarded** when `rug_probability ≥ 0.40` and `pnl > 0`

---

## Files and References

### Generated Files

- **Analysis Script**: `/home/nomad/Desktop/REPLAYER/analyze_trading_patterns.py` (870 lines)
- **Results JSON**: `/home/nomad/Desktop/REPLAYER/trading_pattern_analysis.json` (12KB)
- **Analysis Output**: `/home/nomad/Desktop/REPLAYER/analysis_output.txt` (full console output)

### Dataset

- **Location**: `/home/nomad/rugs_recordings/`
- **Games Analyzed**: 899 (out of 926 files)
- **Corrupted Files**: 27 (JSON parsing errors)
- **Total Ticks**: ~600,000-800,000 (estimated)
- **Date Range**: 2025-10-29 to 2025-11-08

### Sidebet Model

- **Model File**: `/home/nomad/Desktop/rugs-rl-bot/models/sidebet_v3_gb_*.pkl`
- **Training Report**: `/home/nomad/Desktop/rugs-rl-bot/REWARDS DESIGN AGENT DOCUMENTATION/sidebet_training/REPORT.md`
- **Performance**: 38.1% win rate, 754% ROI
- **Features**: 14 input features → 5 output values

---

**END OF EMPIRICAL DATA ANALYSIS**

**Next Steps**:
1. Agent uses this data to design reward function
2. Integrate sidebet predictions as primary reward factors
3. Validate empirically-informed design with backtest
4. Compare to baseline (current RL bot: 30% win rate)
5. Target: 60%+ win rate, 90%+ rug avoidance, <5% bankruptcy

---
