# Trading Bot RL Rewards Design - Key Insights

**Purpose**: Executive summary of critical findings without reading full documentation
**Use Case**: Fast context loading (5-10 minutes) for quick understanding
**Full Context**: See REWARD_DESIGN_PROMPT.md for complete details

---

## Critical Problem

### Current Performance (Quantified Failure)

**Win Rate**: ~30% (need >60%) - **2x gap**
**Rug Avoidance**: ~30% (need >90%) - **3x gap**
**Bankruptcy Rate**: ~20% (need <5%) - **4x gap**

**Root Cause**: Reward function prioritizes P&L over rug avoidance
- Agent learns to maximize profits
- Agent holds too long chasing gains
- Agent gets liquidated by rugs (70% of positions)
- **70% loss rate is unacceptable for production**

### Why This Matters

- Current bankruptcy rate (20%) means 1 in 5 episodes fails completely
- Variable ROI (-50% to +100%) = unreliable profitability
- Agent has exit signals (volatility, patterns) but ignores them
- **Sidebet prediction model available but UNUSED in rewards**

---

## The Breakthrough

### Sidebet Prediction Model v3 (38.1% Win Rate)

**Performance**:
- Win rate: 38.1% vs 16.7% random (2.3x better)
- ROI: 754% on 200-game backtest
- Martingale success: 100% (never bankrupted)
- **Most reliable exit signal we have**

**Integration**:
- Provides **5 prediction features every tick**
- Features in observation space but **unused in current rewards**
- Predictions available: probability, confidence, timing, flags
- **This is the game-changer**

**The Opportunity**:
If agent learns to exit when rug_prob ≥ 0.50:
- Rug avoidance: 30% → 90%+ (3x improvement)
- Win rate: 30% → 60%+ (2x improvement)
- Bankruptcy: 20% → <5% (4x reduction)

---

## Statistical Findings

### Finding 1: Sidebet Model Outperforms All Other Signals

**Evidence**:
- Volatility exit: ~50% accuracy (detects some rugs, many false positives)
- Pattern detection: ~40% accuracy (noisy, inconsistent)
- Sidebet model: **38% accuracy at threshold 0.50** (optimal)
- **At 0.40 threshold**: 36.5% accuracy (still highly profitable)

**Implication**: Sidebet predictions should be PRIMARY exit signal (highest weight)

### Finding 2: All Sidebet Thresholds Are Profitable

**Threshold Analysis**:
```
Threshold | Win Rate | EV per Bet | Status
----------|----------|------------|--------
0.100     | 33.7%    | +0.684     | ✅ Profitable
0.300     | 35.3%    | +0.765     | ✅ Strong
0.400     | 36.5%    | +0.827     | ✅ Very Strong
0.500     | 39.4%    | +0.971     | ✅✅✅ OPTIMAL
```

**Implication**: Model is robust. Even conservative use (low thresholds) is profitable. Can be aggressive with high thresholds.

### Finding 3: Current Exit Signals Miss 70% of Rugs

**Analysis of 1000 episodes**:
- Exits before rug: 30%
  - With volatility signal: 20%
  - Without signal (luck/P&L): 10%
- Liquidated by rug: 70%
  - Signal present but ignored: 30%
  - No signal available: 40%

**Implication**: Need BOTH better signal (sidebet model) AND incentive to use it (reward redesign)

### Finding 4: Z-Score is Dominant Predictor (63.64% importance)

**Sidebet Model Feature Importance**:
- z_score: 63.64% (game duration outlier)
- spike_spacing: 13.43% (volatility pattern)
- spike_frequency: 8.40% (spike rate)
- All others: <5% each

**Interpretation**: Games lasting abnormally long have high rug probability. More reliable than individual spike detection.

**Implication**: Duration-based risk assessment is key. Sidebet model captures this.

### Finding 5: Sweet Spot Timing Works But Insufficient

**Sweet Spot (2-4x) Performance**:
- Entry in sweet spot: 40% win rate (vs 30% overall)
- Average hold: 60 ticks (optimal duration)
- But still 60% loss rate (rug liquidations)

**Implication**: Good timing helps but doesn't prevent rugs. Need exit strategy on top of entry timing.

---

## Design Trade-offs

### Trade-off 1: Rug Avoidance vs Profit Maximization

**Tension**:
- Higher rug_prob threshold (0.50) = safer exits, more rugs avoided
- But early exits sacrifice potential profits from games that don't rug

**Data**:
- Exit at 0.40: Avg profit +0.02 SOL, 36% win rate
- Exit at 0.50: Avg profit +0.015 SOL, 39% win rate
- Hold until rug: Avg loss -0.008 SOL, 0% win rate

**Recommendation**: Prioritize rug avoidance (0.40-0.50 threshold). Losses from rugs far exceed missed profit opportunities.

### Trade-off 2: Early Exit Prevention vs Rug Avoidance

**Tension**:
- Strong rug avoidance rewards → agent may "always exit immediately"
- Need to balance: exit on signals BUT hold when safe (low rug_prob)

**Solution**:
- Reward exits when rug_prob ≥ 0.40 (+30 to +50)
- Penalize early exits when rug_prob < 0.20 AND in_sweet_spot (-10)
- Net effect: Agent learns to exit only on real signals

### Trade-off 3: Confidence Weighting vs Signal Availability

**Tension**:
- High-confidence predictions (>0.70) are rare but reliable
- Low-confidence predictions (<0.60) are common but noisy
- Should we ignore low-confidence predictions?

**Data**:
- Confidence >0.70: 15% of ticks, 45% win rate
- Confidence 0.60-0.70: 25% of ticks, 38% win rate
- Confidence <0.60: 60% of ticks, 28% win rate

**Recommendation**: Scale rewards by confidence (reward *= confidence) rather than hard cutoff. Preserves signal availability while weighting reliable predictions higher.

---

## Game Mechanics Constraints

### Immutable Rules (Cannot Change)

1. **Sidebet Payout**: 5:1 (predict within 40 ticks)
   - Breakeven: 16.7% win rate (1/6)
   - Current model: 38% win rate (2.3x breakeven)

2. **Rug Timing**: Unpredictable but statistical
   - Mean: 329 ticks, Std dev: 180 ticks
   - Cannot predict exact tick, only probability

3. **Sweet Spot**: 2-4x multiplier (40-80 ticks)
   - Optimal risk/reward window
   - Agent already learned this (no redesign needed)

4. **Bankruptcy Threshold**: 0.001 SOL
   - Below this = episode terminates
   - Must preserve capital across 15 games

5. **Position Limits**: Max 10 simultaneous positions
   - Prevents over-exposure
   - Encourages selective entry

---

## Current Reward System Analysis

### What's Wrong

**Issue 1: No Rug Avoidance Component**
- Current components: P&L, volatility, patterns, sweet spot
- Missing: Reward for exiting before rug based on rug_prob
- **Gap**: Agent has no incentive to use sidebet predictions

**Issue 2: P&L Weight Too High (1.0)**
- Encourages holding for max profit
- Conflicts with early exit for rug avoidance
- **Fix**: Reduce to 0.3-0.5

**Issue 3: Volatility as Primary Exit Signal (weight 8.0)**
- Volatility: 50% accuracy
- Sidebet model: 38% win rate = more reliable
- **Fix**: Reduce volatility weight to 2-3, increase rug_avoidance to 10+

**Issue 4: No Penalties for Ignoring Signals**
- Agent can hold through rug_prob ≥ 0.50 with no consequence
- Only penalty is eventual liquidation (too late)
- **Fix**: Add severe penalties (-50 to -100) for holding through critical signals

### What's Working

**✅ Sweet Spot Timing**: Agent learned to enter at 2-4x (weight 2.0 effective)
**✅ Bankruptcy Penalty**: -1000 successfully deters reckless behavior
**✅ Pattern Exploitation**: Ultra-short skip (73% effective) and moonshot detection

**Keep These**: No need to change what's working

---

## Success Criteria

### Primary (MUST Achieve)

**Rug Avoidance**: >90% (from 30%)
- Measurement: % of positions exited before rug
- Method: Track exit_tick vs rug_tick per position

**Win Rate**: >60% (from 30%)
- Measurement: % of closed positions with positive P&L
- Method: Track position P&L at close

**Bankruptcy**: <5% (from 20%)
- Measurement: % of episodes ending in bankruptcy
- Method: Track bankroll <= 0.001 SOL

### Secondary (SHOULD Achieve)

**ROI**: >200% (from variable)
- Measurement: (end_bankroll - start_bankroll) / start_bankroll
- Target: Consistent across episodes

**Sharpe Ratio**: >1.5 (from <1.0)
- Measurement: (mean_return - risk_free) / std_dev_return
- Better risk-adjusted returns

**Max Drawdown**: <20% (from ~50%)
- Measurement: Worst peak-to-trough decline
- Capital preservation

---

## Hypotheses to Test

### Hypothesis 1: Rug Avoidance Should Dominate (Weight >10.0)

**Reasoning**:
- Sidebet model provides reliable exit signal (38% win rate)
- Avoiding rugs prevents 95-99% position losses
- Bankruptcy caused by accumulating rug liquidations
- **Expected Impact**: 30% → 90% rug avoidance

**Test**:
```python
reward_rug_avoidance = {
    'weight': 10.0,  # 10x higher than P&L
    'emergency_exit_bonus': 50.0,  # rug_prob >= 0.50
    'proactive_exit_bonus': 30.0,  # rug_prob >= 0.40
}
```

### Hypothesis 2: Confidence Scaling Improves Reliability

**Reasoning**:
- High-confidence predictions (>0.70) have 45% win rate
- Low-confidence predictions (<0.60) have 28% win rate
- Scaling by confidence weights reliable signals higher

**Test**:
```python
reward = base_reward * prediction['confidence']
# High confidence → full reward
# Low confidence → reduced reward
```

### Hypothesis 3: Severe Penalties Deter Ignoring Signals

**Reasoning**:
- Agent currently holds through rug_prob >= 0.50 (30% of losses)
- Small penalties (<-10) insufficient to change behavior
- Need -50 to -100 to make ignoring signals costly

**Test**:
```python
if rug_prob >= 0.50 and action == WAIT and has_positions:
    penalty = -100.0  # SEVERE
```

### Hypothesis 4: Early Exit Penalties Prevent Overfitting

**Reasoning**:
- Strong rug avoidance rewards may cause "always exit immediately"
- Need counter-incentive: penalize exits during sweet spot with low rug_prob
- Balance: exit on signals, hold when safe

**Test**:
```python
if action == SELL and in_sweet_spot and rug_prob < 0.20:
    penalty = -10.0  # Discourage premature exit
```

### Hypothesis 5: P&L Reduction Reduces Greed

**Reasoning**:
- Current P&L weight (1.0) encourages holding for max profit
- Reducing to 0.3-0.5 deprioritizes greed
- Allows rug avoidance to dominate decision-making

**Test**:
```python
pnl_reward_weight = 0.3  # Down from 1.0
```

---

## Known Unknowns

### Question 1: Optimal Rug Avoidance Weight

**What we know**: Should be >5.0 (higher than all others)
**What we don't know**: Exactly how high? 10.0, 15.0, 20.0?
**How to find out**: Start at 10.0, increase if rug avoidance <80% after 100 episodes

### Question 2: Early Exit Penalty Magnitude

**What we know**: Need to prevent overfitting to "always exit"
**What we don't know**: -10 sufficient? Or need -20, -30?
**How to find out**: Monitor false exit rate. If >20%, increase penalty.

### Question 3: Confidence Minimum Threshold

**What we know**: Low confidence (<0.60) is noisy
**What we don't know**: Should we ignore predictions below 0.60? Or scale by confidence?
**How to find out**: Test both approaches in Phase 1 vs Phase 2

### Question 4: Multiple Simultaneous Signals

**What we know**: Rug prediction, volatility, patterns all available
**What we don't know**: How to weight when signals conflict?
**How to find out**: Establish hierarchy: rug_prediction > volatility > patterns

---

## Design Principles

### 8 Core Principles for Reward Design

1. **Rug Avoidance is Primary**
   - Weight must be >5.0x other components
   - Prevent rug liquidations is job #1

2. **Use Sidebet Predictions Explicitly**
   - All 5 prediction features must be integrated
   - Cannot design rewards ignoring this signal

3. **Severe Penalties for Critical Mistakes**
   - Holding through rug_prob >= 0.50: -50 to -100
   - Ignoring emergency signal is unacceptable

4. **Balance Exit Timing**
   - Reward good exits (+30 to +50)
   - Penalize premature exits (-10)
   - Net effect: exit only on real signals

5. **Confidence Weighting**
   - Scale rewards by prediction confidence
   - High confidence → full reward
   - Low confidence → reduced reward

6. **Phased Implementation**
   - Roll out in 3 phases with validation
   - Week 1: Core changes
   - Week 2: Fine-tuning
   - Week 3: Validation

7. **Quantified Targets**
   - All success metrics must be measurable
   - Primary: >90% rug avoidance, >60% win rate
   - Secondary: >200% ROI, >1.5 Sharpe

8. **Implementability**
   - All recommendations must be deployable
   - Provide pseudocode, YAML config
   - Clear integration strategy

---

## Quick Reference

### Current Baseline
- Win rate: 30%
- Rug avoidance: 30%
- Bankruptcy: 20%
- ROI: Variable

### Sidebet Model
- Win rate: 38.1%
- ROI: 754%
- Optimal threshold: 0.50
- Features: 5 (probability, confidence, timing, flags)

### Target Performance
- Rug avoidance: >90% (3x improvement)
- Win rate: >60% (2x improvement)
- Bankruptcy: <5% (4x reduction)
- ROI: >200% (consistent)

### Key Numbers
- Rug avoidance weight: >10.0 (recommended)
- Emergency exit bonus: +50.0 (rug_prob >= 0.50)
- Proactive exit bonus: +30.0 (rug_prob >= 0.40)
- Hold-through penalty: -100.0 (critical signal ignored)
- Early exit penalty: -10.0 (premature exit)
- P&L weight reduction: 1.0 → 0.3-0.5

---

## Next Steps

1. **Read Full Context**: REWARD_DESIGN_PROMPT.md (if time permits)
2. **Review Questions**: QUESTIONS.md (structured exploration)
3. **Request Implementation Files**: See BUNDLE.md for file list
4. **Design Rewards**: Provide 8 required deliverables
5. **Validate Design**: Check against success criteria

**Time Estimate**: 2-5 hours total (can split across sessions)

---

**Summary**: Current RL bot fails because it doesn't prioritize rug avoidance. We have a sidebet model (38% win rate) that predicts rugs, but it's unused in rewards. Design rewards that make rug avoidance the PRIMARY objective (weight >10.0), use all 5 prediction features, implement severe penalties for ignoring signals, and balance with early-exit penalties. Expected outcome: 3x rug avoidance improvement, 2x win rate improvement, 4x bankruptcy reduction.
