# Reward Design: Key Insights Summary

**Purpose**: Quick reference of critical findings that must inform reward function design

**Last Updated**: November 7, 2025

---

## 🚨 Critical Problem

### The Bankruptcy Crisis
- **Previous Training Result**: 94.6% bankruptcy rate (151/160 episodes)
- **Root Cause**: Reward function encouraged aggressive trading without proper risk management
- **Consequence**: Models learned to maximize short-term rewards at the cost of survival
- **Implication**: Reward function MUST prioritize capital preservation

---

## 📊 Statistical Findings (High Confidence)

### 1. Volatility Prediction Power
- **Accuracy**: 94.7% at predicting rugs
- **Signal Strength**: 664.7% mean price spike before rugs
- **Confidence**: p < 0.001 (highly significant)
- **Implication**: Volatility signals should be heavily weighted in reward function

### 2. Pattern Exploitation Opportunities
Three validated statistical patterns with proven edge:

**Pattern A: Post-Max-Payout Windows**
- **Effect Size**: +31.9% win rate improvement
- **Statistical Significance**: p = 0.0038 (very strong)
- **Mechanism**: Games are 2-3x more likely to rug after max payout reached
- **Reward Implication**: Should receive significant bonus when detected

**Pattern B: Ultra-Short Games**
- **Duration**: < 12 ticks
- **Win Rate**: +24.4% improvement
- **Statistical Significance**: p = 0.0092 (strong)
- **Mechanism**: Quick rugs are more predictable
- **Reward Implication**: Moderate bonus for early detection

**Pattern C: Moonshot Games**
- **Multiplier**: > 7.3x
- **Win Rate**: +18.7% improvement
- **Statistical Significance**: p = 0.0156 (moderate)
- **Mechanism**: Extreme price movements signal instability
- **Reward Implication**: Moderate bonus for extreme volatility

---

## ⚖️ Design Trade-offs

### 1. Selective Entry vs Aggressive Trading
**Current Issue**: Bot trades too frequently, doesn't wait for high-probability setups

**Solution Space**:
- Penalize entries without pattern signals
- Reward "patience" (WAIT actions when no edge detected)
- Require minimum volatility threshold for BUY actions
- Add "setup quality" bonus for ideal entry conditions

### 2. Position Sizing vs Fixed Bet
**Current**: Fixed 0.005 SOL per trade (hardcoded)

**Problem**: No risk adjustment based on:
- Account balance
- Pattern confidence
- Volatility level
- Game phase

**Future Consideration**: Variable position sizing based on edge strength

### 3. Risk Management vs Profit Maximization
**Current Imbalance**: Rewards focus on profit, minimal penalties for risk

**Need**:
- Survival bonus (reward not going bankrupt)
- Drawdown penalties (punish large losses)
- Risk-adjusted returns (Sharpe-style metrics)
- Capital preservation thresholds

---

## 🎮 Game Mechanics Constraints

### Instant Liquidation Reality
- **Mechanism**: Positions liquidate to $0.000 instantly when rug occurs
- **No Gradual Decline**: Can't "cut losses" once rug starts
- **Implication**: Prevention >> reaction (must predict rugs, not react)
- **Reward Impact**: Heavy penalty for holding during rug (but model can't learn from it if bankrupt)

### Sidebets as Free Lottery Tickets
- **Cost**: 0.00001 SOL (negligible)
- **Payout**: Up to 400x multiplier
- **Expected Value**: Positive if pattern detected
- **Current Issue**: Bot ignores sidebets (26.9% usage)
- **Opportunity**: Low-risk lottery tickets with statistical edge

### Multi-Game Episode Structure
- **Length**: 15 consecutive games
- **Problem**: Bankruptcy ends episode early (lost training signal)
- **Implication**: Early-game mistakes cascade
- **Reward Need**: Progressive risk reduction as episode continues

---

## 🔧 Current Reward System Analysis

### Component Weights (Existing)
```yaml
pnl_weight: 1.0              # Profit & Loss
entry_timing_weight: 0.3     # Pattern detection quality
exit_timing_weight: 0.3      # Exit decision quality
volatility_weight: 0.2       # Volatility signal usage
pattern_bonus_weight: 0.4    # Pattern exploitation
risk_management_weight: 0.2  # Risk controls
sidebet_ev_weight: 0.1       # Sidebet EV optimization
balance_preservation: 0.5    # Capital preservation
liquidity_weight: 0.1        # Liquidity management
sweet_spot_weight: 0.3       # Ideal entry zones
win_rate_weight: 0.2         # Win consistency
consistency_weight: 0.15     # Performance stability
drawdown_penalty: 0.4        # Drawdown control
```

### Identified Issues

**1. PnL Dominates** (weight = 1.0)
- Problem: Short-term profit >> long-term survival
- Solution: Reduce or normalize by risk

**2. Pattern Bonuses Too Weak** (weight = 0.4)
- Problem: 31.9% win rate improvement only gets 0.4 weight vs 1.0 for PnL
- Solution: Increase to 0.8-1.0 to match statistical significance

**3. Risk Management Underweighted** (weight = 0.2)
- Problem: Bankruptcy prevention is more important than 5x profit
- Solution: Increase to 1.0+ or make it multiplicative (not additive)

**4. No Patience Reward**
- Problem: Model never learns to WAIT for ideal setups
- Solution: Add explicit "patience bonus" for WAIT during low-edge scenarios

**5. No Survival Incentive**
- Problem: Episode ending early from bankruptcy removes future rewards
- Solution: Add "games survived" bonus or "episode completion" reward

---

## 🎯 Success Criteria for New Reward Function

### Primary Metrics
1. **Survival Rate**: > 90% (currently 5.4%)
2. **Win Rate**: > 60% (baseline ~50%)
3. **Profit per Episode**: > 0.010 SOL (10% ROI)
4. **Pattern Usage**: > 80% of entries have pattern signal
5. **Sidebet Optimization**: > 50% usage when EV+ detected

### Secondary Metrics
6. **Average Game Length**: 8-12 games per episode (of 15 possible)
7. **Risk-Adjusted Returns**: Sharpe ratio > 1.0
8. **Drawdown Control**: Max drawdown < 30% of starting balance
9. **Consistency**: Win rate variance < 15%

### Training Behavior Goals
10. Model learns to WAIT (patience)
11. Model exploits patterns (opportunistic)
12. Model uses volatility signals (predictive)
13. Model preserves capital (defensive)
14. Model optimizes sidebets (EV maximization)

---

## 💡 Hypotheses to Test

### H1: Multiplicative Risk Management
**Theory**: Make risk_management_weight multiplicative instead of additive
```python
# Instead of: reward = pnl + risk_bonus
# Try: reward = pnl * risk_multiplier (where risk_multiplier < 1 if risky)
```
**Rationale**: Forces model to care about risk even when profitable

### H2: Patience Reward
**Theory**: Reward WAIT actions when no pattern detected
```python
if action == WAIT and pattern_strength < threshold:
    reward += patience_bonus
```
**Rationale**: Teaches model that doing nothing is better than bad trades

### H3: Pattern-Conditional Entry
**Theory**: Heavy penalty for BUY without pattern signal
```python
if action == BUY and pattern_detected == False:
    reward -= no_edge_penalty  # Large penalty
```
**Rationale**: Forces model to wait for statistical edge

### H4: Survival Milestone Bonuses
**Theory**: Give bonus for completing N games without bankruptcy
```python
if games_completed % 5 == 0:
    reward += survival_bonus
```
**Rationale**: Incentivizes long-term thinking

### H5: Normalized PnL
**Theory**: Normalize PnL by balance and risk taken
```python
risk_adjusted_pnl = pnl / (balance * volatility)
```
**Rationale**: Prevents model from taking excessive risk for small gains

---

## 🚧 Known Unknowns

### Questions Without Clear Answers
1. **Optimal patience/aggression balance**: How many WAIT actions is "too many"?
2. **Pattern confidence thresholds**: What minimum p-value should trigger entry?
3. **Risk scaling**: Should penalties scale linearly or exponentially with risk?
4. **Temporal discounting**: Should early-game trades be weighted differently than late-game?
5. **Sidebet integration**: Should sidebets affect trading decisions or be independent?

### Areas Needing More Data
- Long-term model behavior beyond 15 games
- Interaction effects between reward components
- Sensitivity to hyperparameter changes
- Generalization to unseen game patterns

---

## 📚 Cross-References

**For implementation details**: See `reward_calculator.py:187-456`
**For game mechanics**: See `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md`
**For pattern research**: See `PATTERN_EXPLOITATION_RESEARCH.md`
**For statistical analysis**: See `VOLATILITY_ANALYSIS_FINDINGS.md`
**For failure modes**: See `PHASE_1_TRAINING_FAILURE_ANALYSIS.md`

---

## 🎓 Design Principles

1. **Survival First**: Capital preservation >> short-term profit
2. **Edge-Based Entry**: Only trade when statistical advantage exists
3. **Volatility-Informed**: Use 94.7% accurate volatility signals
4. **Pattern-Driven**: Exploit validated statistical patterns (p < 0.05)
5. **Risk-Adjusted**: Normalize all rewards by risk taken
6. **Long-Term Thinking**: Incentivize episode completion over quick wins
7. **EV Maximization**: Optimize expected value across all decisions
8. **Behavioral Shaping**: Explicitly reward desired behaviors (patience, pattern usage)

---

**Status**: This document captures the essential insights needed for reward function redesign. Use this as a reference when making design decisions.
