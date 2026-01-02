# Reward Function Design: Structured Questionnaire

**Purpose**: Guide systematic redesign of reward function to address 94.6% bankruptcy problem

**Instructions**: Answer each question with specific recommendations, weights, formulas, or implementation guidance. Reference statistical findings and game mechanics in your answers.

**Last Updated**: November 7, 2025

---

## Section 1: Component Weight Rebalancing

### Q1.1: PnL Weight Adjustment
**Current**: `pnl_weight = 1.0` (dominates all other components)

**Question**: Should PnL weight be:
- A) Reduced to 0.5-0.7 (still important but not dominant)
- B) Kept at 1.0 but normalized by risk
- C) Made multiplicative with risk management (pnl * risk_factor)
- D) Other approach?

**Follow-up**: If normalizing, what formula should be used?
```python
# Option 1: Risk-adjusted PnL
risk_adjusted_pnl = pnl / (balance * volatility_factor)

# Option 2: Sharpe-style
sharpe_pnl = pnl / drawdown_risk

# Option 3: Kelly-criterion scaled
kelly_pnl = pnl * (win_rate - loss_rate)

# Your recommendation:
```

### Q1.2: Pattern Bonus Weight
**Current**: `pattern_bonus_weight = 0.4`
**Statistical Finding**: Patterns provide +31.9% win rate improvement (p=0.0038)

**Question**: Given the strong statistical significance, should pattern_bonus_weight be:
- A) Increased to 0.8-1.0 (match PnL importance)
- B) Kept at 0.4 (current)
- C) Made conditional (high weight only when pattern detected)
- D) Split into separate weights per pattern type?

**Follow-up**: Should different patterns have different weights based on p-values?
```yaml
post_max_payout_bonus: ???  # p=0.0038 (strongest)
ultra_short_bonus: ???       # p=0.0092 (strong)
moonshot_bonus: ???          # p=0.0156 (moderate)
```

### Q1.3: Risk Management Weight
**Current**: `risk_management_weight = 0.2`
**Problem**: 94.6% bankruptcy rate suggests insufficient weight

**Question**: Should risk_management_weight be:
- A) Increased to 1.0+ (equal or greater than PnL)
- B) Made multiplicative (acts as penalty multiplier, not additive bonus)
- C) Split into multiple risk components (drawdown, volatility, position size)
- D) Replaced with hard constraints (terminate episode if risk threshold exceeded)

**Rationale**: Explain how your choice prevents bankruptcy while still allowing profit

### Q1.4: Volatility Weight
**Current**: `volatility_weight = 0.2`
**Statistical Finding**: 94.7% accuracy predicting rugs, 664.7% mean spike

**Question**: Given 94.7% predictive power, should this be:
- A) Increased to 0.8-1.0 (heavily weight proven signal)
- B) Made multiplicative with entry decisions (gate BUY actions on volatility)
- C) Kept low but used as hard constraint (block trades above threshold)
- D) Integrated into other components rather than standalone

**Implementation**: How should volatility signal be translated to reward?
```python
# Option 1: Linear scaling
volatility_reward = volatility_weight * volatility_signal

# Option 2: Exponential (punish high volatility severely)
volatility_reward = -exp(volatility_level) * weight

# Option 3: Threshold-based
volatility_reward = -999 if volatility > threshold else 0

# Your recommendation:
```

---

## Section 2: Missing Components

### Q2.1: Patience Reward Component
**Current**: No explicit reward for WAIT actions
**Problem**: Model never learns selective entry (trades too frequently)

**Question**: Should we add a patience component? If yes:
```python
class PatienceReward:
    def calculate(self, action, pattern_strength, volatility):
        # When should WAIT be rewarded?
        # How much reward (relative to other components)?
        # Should it scale with "missed opportunity cost"?
        pass
```

**Design parameters**:
- Weight: `patience_weight = ???`
- Trigger condition: When to reward WAIT?
- Magnitude: How much reward per WAIT action?
- Diminishing returns: Should consecutive WAITs be penalized eventually?

### Q2.2: Survival Milestone Component
**Current**: No explicit reward for staying alive
**Problem**: Early bankruptcy removes all future reward signal

**Question**: Should we add survival bonuses?
```python
# Option A: Per-game survival
if game_completed:
    reward += survival_bonus

# Option B: Milestone bonuses
if games_completed in [5, 10, 15]:
    reward += milestone_bonus

# Option C: Exponential survival
survival_bonus = base_bonus * (games_completed ** exponent)

# Your recommendation:
```

**Design parameters**:
- Base survival bonus: ???
- Milestone values: [??? at 5 games, ??? at 10 games, ??? at 15 games]
- Should survival bonus scale with difficulty/volatility?

### Q2.3: Setup Quality Component
**Current**: Entry timing is binary (pattern detected or not)
**Enhancement**: Multi-factor "setup quality" scoring

**Question**: Should we score entry setups on multiple criteria?
```python
class SetupQuality:
    def score(self, state):
        quality = 0.0

        # Factor 1: Pattern strength (p-value)
        quality += pattern_score(state.pattern_strength)

        # Factor 2: Volatility level (ideal range)
        quality += volatility_score(state.volatility)

        # Factor 3: Game phase (early/mid/late)
        quality += phase_score(state.current_tick)

        # Factor 4: Balance health
        quality += balance_score(state.balance)

        # Factor 5: Recent win rate
        quality += streak_score(state.recent_trades)

        return quality  # 0.0 to 1.0
```

**Questions**:
- Which factors should be included?
- How should they be weighted relative to each other?
- What's the minimum quality score to justify a BUY action?
- Should setup quality be multiplicative with PnL?

### Q2.4: Risk-Adjusted Return Component
**Current**: PnL is absolute, not risk-adjusted
**Enhancement**: Sharpe ratio or similar risk-adjusted metric

**Question**: Should we add risk-adjusted performance tracking?
```python
# Option 1: Sharpe ratio
sharpe = (mean_return - risk_free_rate) / std_return

# Option 2: Sortino ratio (only downside deviation)
sortino = (mean_return - target) / downside_deviation

# Option 3: Calmar ratio (return / max drawdown)
calmar = annual_return / max_drawdown

# Your recommendation:
```

**Implementation**:
- Which metric fits best for 15-game episodes?
- What time window for calculation (per game? per episode?)
- How to weight it relative to absolute PnL?

---

## Section 3: Penalty Structure Redesign

### Q3.1: Entry Without Edge Penalty
**Current**: Small penalty for failed actions (0.01)
**Problem**: Not enough to prevent speculative entries

**Question**: What penalty for BUY without pattern signal?
```python
if action == BUY and no_pattern_detected:
    penalty = ???  # How severe?

# Should it scale with:
# - Volatility level (higher vol = worse penalty)?
# - Account balance (punish more when low on funds)?
# - Recent losses (compound penalty for repeated mistakes)?
```

**Design considerations**:
- Fixed penalty vs scaled penalty
- Absolute value vs percentage of balance
- Should repeated violations compound?

### Q3.2: Holding Through Rug Penalty
**Current**: Position liquidation to $0 (inherent penalty)
**Problem**: Too late - model already bankrupt

**Question**: How to penalize rug exposure without hindsight bias?
```python
# Challenge: Can't penalize "holding through rug"
# because we don't know rug is coming

# Option A: Penalize high volatility exposure
if position_size > 0 and volatility > threshold:
    penalty = position_size * volatility * penalty_weight

# Option B: Penalize late-game positions
if position_size > 0 and tick > danger_zone:
    penalty = position_size * time_penalty

# Option C: Penalize positions without stop-loss logic
# (but we have instant liquidation, no gradual stops)

# Your recommendation:
```

### Q3.3: Over-Trading Penalty
**Current**: No penalty for high trade frequency
**Problem**: Model likely trades too often (no data on this yet)

**Question**: Should we penalize excessive trading?
```python
# Option A: Fixed penalty per trade (transaction cost simulation)
reward -= transaction_cost_penalty

# Option B: Penalty for trades below minimum time spacing
if time_since_last_trade < min_spacing:
    reward -= overtrading_penalty

# Option C: Diminishing returns on consecutive trades
reward *= (0.9 ** consecutive_trades)

# Your recommendation:
```

---

## Section 4: Pattern Exploitation Optimization

### Q4.1: Pattern-Specific Reward Structure
**Current**: Single pattern_bonus for all patterns
**Statistical Reality**: Different patterns have different effect sizes and p-values

**Question**: Should each pattern have separate reward?
```yaml
# Pattern A: Post-Max-Payout
post_max_payout:
  effect_size: +31.9%
  p_value: 0.0038
  recommended_weight: ???

# Pattern B: Ultra-Short
ultra_short:
  effect_size: +24.4%
  p_value: 0.0092
  recommended_weight: ???

# Pattern C: Moonshot
moonshot:
  effect_size: +18.7%
  p_value: 0.0156
  recommended_weight: ???
```

**Follow-up**: Should weights be proportional to effect size, inverse p-value, or both?

### Q4.2: Pattern Combination Bonuses
**Current**: Patterns detected independently
**Enhancement**: Extra bonus when multiple patterns align

**Question**: Should simultaneous patterns receive amplified reward?
```python
# Example: Post-Max-Payout + High Volatility + Ultra-Short
if post_max_payout and ultra_short and high_volatility:
    bonus = base_bonus * combination_multiplier  # ???x
```

**Design**:
- Which combinations are most predictive?
- What multiplier for 2-pattern alignment? 3-pattern?
- Does this risk overfitting?

### Q4.3: Pattern Confidence Scaling
**Current**: Pattern detection is binary (yes/no)
**Enhancement**: Scale reward by pattern confidence/strength

**Question**: Should pattern rewards scale with confidence?
```python
# Option A: Linear scaling
pattern_reward = base_reward * confidence  # 0.0 to 1.0

# Option B: Threshold + scaling
if confidence > min_threshold:
    pattern_reward = base_reward * (confidence - min_threshold)

# Option C: Exponential (reward high confidence disproportionately)
pattern_reward = base_reward * (confidence ** exponent)

# Your recommendation:
```

---

## Section 5: Sidebet Integration

### Q5.1: Sidebet Reward Weight
**Current**: `sidebet_ev_weight = 0.1`
**Usage**: Only 26.9% sidebet usage (underutilized)
**Cost**: 0.00001 SOL (negligible)

**Question**: Should sidebet weight be increased?
- A) Increase to 0.3-0.5 (encourage more usage)
- B) Keep at 0.1 (sidebets are secondary)
- C) Make conditional (high weight when EV clearly positive)
- D) Make mandatory when pattern detected (hard constraint)

**Rationale**: Sidebets are essentially free lottery tickets with statistical edge

### Q5.2: Sidebet Strategy Optimization
**Current**: Basic EV calculation
**Enhancement**: Context-aware sidebet decisions

**Question**: Should sidebet strategy integrate with trading decisions?
```python
# Option A: Independent (current)
sidebet_decision = independent_ev_calculation()

# Option B: Coupled (if trading, also sidebet)
if action == BUY and pattern_detected:
    force_sidebet = True

# Option C: Inverse (sidebet instead of trading when uncertain)
if pattern_weak and high_volatility:
    sidebet_only = True  # Bet on rug without position

# Your recommendation:
```

### Q5.3: Sidebet Outcome Reward
**Current**: Unknown (need to check implementation)

**Question**: How should sidebet wins/losses affect reward?
```python
# Option A: Full PnL integration
reward += sidebet_pnl * sidebet_weight

# Option B: Bonus only (ignore losses since cost negligible)
if sidebet_win:
    reward += sidebet_bonus

# Option C: Accuracy reward (did you predict correctly?)
if sidebet_prediction == actual_outcome:
    reward += prediction_accuracy_bonus

# Your recommendation:
```

---

## Section 6: Risk Management Architecture

### Q6.1: Multiplicative vs Additive Risk
**Current**: Risk components are additive (sum of all rewards)
**Alternative**: Multiplicative risk penalties

**Question**: Should risk act as multiplier on total reward?
```python
# Current (Additive):
total_reward = pnl + pattern_bonus + volatility_bonus + risk_bonus

# Alternative (Multiplicative):
base_reward = pnl + pattern_bonus + volatility_bonus
risk_multiplier = calculate_risk_multiplier()  # 0.0 to 1.0
total_reward = base_reward * risk_multiplier

# Hybrid:
total_reward = (pnl * risk_multiplier) + pattern_bonus + volatility_bonus
```

**Which approach best prevents bankruptcy while allowing profit?**

### Q6.2: Dynamic Risk Scaling
**Current**: Fixed risk weights throughout episode
**Enhancement**: Risk weights increase as episode progresses

**Question**: Should risk management intensify over time?
```python
# Option A: Linear escalation
risk_weight = base_weight * (1 + games_completed / max_games)

# Option B: Exponential (get very conservative near end)
risk_weight = base_weight * exp(games_completed / scale_factor)

# Option C: Threshold-based (normal until 80% through episode)
risk_weight = base_weight if progress < 0.8 else base_weight * 3

# Your recommendation:
```

**Rationale**: Should model become more conservative to preserve gains?

### Q6.3: Balance-Dependent Risk Adjustment
**Current**: Risk calculations don't consider account balance
**Problem**: Same risk tolerance at 0.010 SOL and 0.100 SOL

**Question**: Should risk penalties scale with balance?
```python
# When balance is low (danger zone):
if balance < initial_balance * 0.3:
    risk_multiplier *= high_risk_penalty  # ???x

# When balance is high (protect gains):
if balance > initial_balance * 1.5:
    risk_multiplier *= conservative_factor  # ???x

# Your recommended thresholds and multipliers:
```

---

## Section 7: Temporal Dynamics

### Q7.1: Game Phase Awareness
**Current**: No differentiation between early/mid/late game
**Enhancement**: Different strategies for different phases

**Question**: Should rewards vary by game phase?
```python
class GamePhase:
    EARLY = 0-20 ticks      # Exploration phase
    MID = 21-50 ticks       # Opportunity window
    LATE = 51+ ticks        # Danger zone (rug likely)

# Should entry timing rewards scale by phase?
# Should risk penalties increase in late game?
# Should pattern bonuses differ by phase?
```

### Q7.2: Episode Progress Awareness
**Current**: Each game treated independently
**Enhancement**: Strategy evolves across 15-game episode

**Question**: Should behavior change based on episode progress?
```python
# Early episode (games 1-5): Aggressive, learn patterns
# Mid episode (games 6-10): Balanced, exploit edge
# Late episode (games 11-15): Conservative, preserve capital

# Should this be explicit in reward function or emergent?
# If explicit, how to implement?
```

### Q7.3: Momentum and Streaks
**Current**: No consideration of recent performance
**Enhancement**: Adapt strategy based on win/loss streaks

**Question**: Should reward function respond to momentum?
```python
# After losing streak:
if consecutive_losses >= 3:
    # A) Reduce risk (play safer)
    # B) Increase pattern requirement (only trade with strong edge)
    # C) Pause trading (force WAIT actions)
    # D) No change (streaks are random)

# After winning streak:
if consecutive_wins >= 3:
    # A) Increase aggression (ride hot hand)
    # B) Protect gains (become conservative)
    # C) No change

# Your recommendations:
```

---

## Section 8: Implementation Strategy

### Q8.1: Phased Rollout
**Question**: Should new reward function be deployed all at once or incrementally?

**Option A: Big Bang**
- Implement all changes simultaneously
- Pro: Fastest to optimal design
- Con: Hard to debug if still fails

**Option B: Incremental**
- Phase 1: Fix bankruptcy (risk management only)
- Phase 2: Add pattern bonuses
- Phase 3: Add patience/setup quality
- Pro: Can identify what works
- Con: Slower to optimal

**Your recommendation and rationale:**

### Q8.2: Reward Component Priority
**Question**: If implementing incrementally, what order?

**Rank these components 1-10 by implementation priority:**
```
___ Risk management (multiplicative?)
___ Pattern bonus rebalancing
___ Patience reward
___ Survival milestones
___ PnL normalization
___ Volatility weight increase
___ Setup quality scoring
___ Sidebet optimization
___ Over-trading penalty
___ Dynamic risk scaling
```

### Q8.3: Testing and Validation
**Question**: How to validate new reward function?

**Proposed test sequence:**
1. Unit test each component in isolation
2. 100-episode smoke test (does it learn anything?)
3. 1K-episode training run (does it survive?)
4. Compare to baseline (is it better?)
5. Statistical validation (is improvement significant?)

**Additional tests needed:**
- Ablation studies (remove components to test importance)
- Hyperparameter sensitivity (how robust is design?)
- Adversarial testing (worst-case scenarios)

**Your testing recommendations:**

---

## Section 9: Success Metrics Validation

### Q9.1: Primary Metric Priority
**Question**: If you could only optimize for ONE metric, which?

**Options:**
- A) Survival rate (> 90%)
- B) Win rate (> 60%)
- C) Profit per episode (> 0.010 SOL)
- D) Risk-adjusted returns (Sharpe > 1.0)
- E) Pattern exploitation (> 80% usage)

**Your choice and why:**

### Q9.2: Metric Trade-offs
**Question**: What trade-offs are acceptable?

**Scenario 1**: High survival (95%) but low profit (0.005 SOL/episode)
- Accept or reject?

**Scenario 2**: High profit (0.030 SOL/episode) but moderate survival (70%)
- Accept or reject?

**Scenario 3**: High win rate (75%) but low pattern usage (40%)
- Accept or reject?

**Your acceptable minimum thresholds:**
```yaml
survival_rate_min: ???
win_rate_min: ???
profit_per_episode_min: ???
pattern_usage_min: ???
sidebet_usage_min: ???
```

### Q9.3: Emergent Behavior Checks
**Question**: What unintended behaviors should we monitor for?

**Potential exploits:**
- Gaming patience reward (WAIT forever)
- Gaming survival bonus (never trade)
- Gaming pattern bonus (false positives)
- Gaming sidebet reward (always bet regardless of EV)

**How to detect and prevent each:**

---

## Section 10: Open Questions

### Q10.1: Unknown Unknowns
**What aspects of reward design are we not considering?**

Potential blind spots:
- Multi-agent considerations (if training multiple models)
- Transfer learning (if deploying to different game settings)
- Exploration vs exploitation balance
- Long-term vs short-term reward horizons
- Reward shaping side effects

**Your additions:**

### Q10.2: Research Gaps
**What data or analysis would improve reward design?**

**Needed research:**
- Optimal entry timing distribution (what % of ticks should have trades?)
- Risk-reward ratio distribution (what Sharpe is achievable?)
- Pattern interaction effects (do patterns combine synergistically?)
- Balance trajectory analysis (typical capital curve shape?)

**Your priority research questions:**

### Q10.3: Alternative Approaches
**Are there completely different reward paradigms to consider?**

**Alternative frameworks:**
- Inverse RL (learn reward from human demonstrations)
- Curiosity-driven exploration (intrinsic motivation)
- Curriculum learning (progressive difficulty)
- Multi-objective optimization (Pareto front)
- Hierarchical RL (separate strategy and execution)

**Your thoughts on alternatives:**

---

## Section 11: Final Recommendations

### Q11.1: Proposed Reward Function
**Based on all analysis above, provide complete reward function design:**

```python
class OptimizedRewardCalculator:
    def __init__(self):
        # Component weights (your recommendations)
        self.weights = {
            'pnl': ???,
            'pattern_bonus': ???,
            'risk_management': ???,
            'volatility': ???,
            'patience': ???,
            'survival': ???,
            'setup_quality': ???,
            # ... etc
        }

    def calculate(self, state, action, next_state, info):
        # Step 1: Calculate base components
        pnl_reward = self._calculate_pnl(...)
        pattern_reward = self._calculate_pattern(...)
        # ... etc

        # Step 2: Apply risk multiplier (if multiplicative)
        risk_multiplier = self._calculate_risk_multiplier(...)

        # Step 3: Combine components
        total_reward = ???  # Your formula

        return total_reward
```

### Q11.2: Expected Outcomes
**What results do you expect from this reward function?**

**Predictions:**
- Survival rate: ???%
- Win rate: ???%
- Profit per episode: ??? SOL
- Training time to convergence: ??? episodes
- Key behavioral changes: ???

### Q11.3: Contingency Plans
**If new reward function still fails, what next?**

**Backup plans:**
- If survival < 50%: ???
- If profit < 0: ???
- If not learning: ???
- If overfitting to patterns: ???

---

## Appendix: Quick Reference

### Statistical Findings Summary
- Volatility: 94.7% accuracy, 664.7% mean spike, p < 0.001
- Post-Max-Payout: +31.9% win rate, p = 0.0038
- Ultra-Short: +24.4% win rate, p = 0.0092
- Moonshot: +18.7% win rate, p = 0.0156

### Current Weights
```yaml
pnl_weight: 1.0
pattern_bonus_weight: 0.4
risk_management_weight: 0.2
volatility_weight: 0.2
sidebet_ev_weight: 0.1
```

### Problem Statement
- 94.6% bankruptcy rate (151/160 episodes)
- Need: Survival-focused, pattern-driven, risk-managed reward function
- Goal: >90% survival, >60% win rate, >0.010 SOL profit/episode

---

**Instructions for LLM**: Please work through each section systematically. Provide specific, implementable recommendations with concrete values and formulas. Reference statistical findings and game mechanics to justify your choices.
