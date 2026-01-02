# Trading Bot RL Rewards Design - Structured Questionnaire

**Purpose**: Systematic exploration of reward design space
**Target LLM**: Claude Sonnet 4.5 or equivalent
**Usage**: Work through questions sequentially, provide specific numerical answers with justifications
**Output**: Evidence-based reward function redesign with concrete implementation details

---

## Instructions for LLM

**How to Use This Document**:
1. Answer questions **in order** (don't skip sections)
2. Provide **specific numerical values** (not ranges like "increase significantly")
3. **Cite evidence** from KEY_INSIGHTS.md or REWARD_DESIGN_PROMPT.md when possible
4. Include **pseudocode** for new reward components
5. Explain **trade-offs** (acknowledge costs of your recommendations)
6. Ask **clarifying questions** if you need more data

**Answer Format Template**:
```
### Question X.Y: [Question text]

**Your Answer**: [Specific numerical value or approach]

**Justification**: [Why this value? Cite data/statistics]

**Expected Impact**: [Quantified improvement, e.g., "30% → 90% rug avoidance"]

**Pseudocode** (if applicable):
```python
# Implementation example
```

**Trade-offs**: [What are the costs of this approach?]
```

---

## Section 1: Component Weight Rebalancing

**Context**: Current reward function has multiple components (P&L, volatility, patterns, sweet spot). Need to rebalance weights to prioritize rug avoidance.

### Question 1.1: P&L Weight Reduction

**Current State**: `pnl_reward_weight = 1.0` (highest weight)
**Problem**: Encourages holding for max profit, conflicts with early exit for rug avoidance

**Options**:
- A) Keep at 1.0 (no change)
- B) Reduce to 0.5 (50% reduction)
- C) Reduce to 0.3 (70% reduction)
- D) Remove entirely (0.0)

**Your Recommendation**: ___________

**Justification**: Why this specific value?

**Expected Impact**: How will this change agent behavior?

---

### Question 1.2: Volatility Exit Signal Weight

**Current State**: `volatility_exit_weight = 8.0` (currently highest)
**Problem**: Volatility has ~50% accuracy (false positives), while sidebet model has 38% win rate (more reliable)

**Options**:
- A) Keep at 8.0 (volatility remains primary signal)
- B) Reduce to 5.0 (moderate reduction)
- C) Reduce to 2-3 (significant reduction, defer to sidebet)
- D) Remove entirely (rely only on sidebet)

**Your Recommendation**: ___________

**Justification**: What data supports this? (Cite Finding 1 from KEY_INSIGHTS.md)

**Trade-off**: What do we lose by reducing volatility weight?

---

### Question 1.3: Sweet Spot Timing Weight

**Current State**: `sweet_spot_weight = 2.0` (working well)
**Performance**: Agent learned to enter at 2-4x multiplier (40% win rate vs 30% overall)

**Question**: Should we adjust this weight?

**Options**:
- A) Keep at 2.0 (it's working)
- B) Increase to 3.0 (emphasize even more)
- C) Reduce to 1.0 (less important than rug avoidance)

**Your Recommendation**: ___________

**Justification**: Why change or keep?

---

### Question 1.4: Pattern Exploitation Weight

**Current State**: Multiple pattern detectors (ultra-short skip, moonshot) with combined weight ~3.0
**Performance**: Ultra-short skip has 73% effectiveness

**Question**: Should we adjust pattern exploitation weighting?

**Options**:
- A) Keep current weights (patterns working)
- B) Reduce weights (deprioritize in favor of rug avoidance)
- C) Increase weights (patterns are profitable)

**Your Recommendation**: ___________

**Justification**: Why?

---

## Section 2: Missing Components (Sidebet Integration)

**Context**: Sidebet model provides 5 features: probability, confidence, ticks_to_rug_norm, is_critical, should_exit. These are UNUSED in current rewards. This is the critical gap.

### Question 2.1: Rug Avoidance Component Weight

**Current State**: NO rug avoidance component exists (weight = 0.0)
**Opportunity**: Sidebet model has 38.1% win rate, 754% ROI, 100% Martingale success

**Question**: What should the rug avoidance weight be?

**Options**:
- A) 5.0 (equal to other major components)
- B) 10.0 (2x highest current component)
- C) 15.0 (3x highest current component)
- D) 20.0+ (4x+ highest current component)

**Your Recommendation**: ___________

**Justification**: Why this specific weight? (Consider: this is PRIMARY objective)

**Principle**: From KEY_INSIGHTS.md - "Rug avoidance weight must be >5.0x other components"

---

### Question 2.2: Emergency Exit Bonus (Critical Signal)

**Context**: When `rug_prob >= 0.50` (critical threshold), agent should exit IMMEDIATELY

**Current State**: No bonus for exiting on critical signal
**Expected Frequency**: ~15% of ticks will have rug_prob >= 0.50
**Win Rate at 0.50**: 39.4% (optimal threshold from Finding 2)

**Question**: What bonus should we give for exiting when rug_prob >= 0.50?

**Options**:
- A) +10.0 (small bonus)
- B) +30.0 (moderate bonus)
- C) +50.0 (large bonus)
- D) +100.0 (very large bonus)

**Your Recommendation**: ___________

**Justification**: Why this magnitude?

**Pseudocode**:
```python
def emergency_exit_bonus(state, action, next_state):
    """Reward for exiting on critical signal"""
    # TODO: Your implementation
    pass
```

---

### Question 2.3: Proactive Exit Bonus (High Signal)

**Context**: When `rug_prob >= 0.40` (high threshold), agent should consider exiting

**Current State**: No bonus for proactive exits
**Expected Frequency**: ~25% of ticks will have rug_prob >= 0.40
**Win Rate at 0.40**: 36.5% (still highly profitable from Finding 2)

**Question**: What bonus for exiting when 0.40 <= rug_prob < 0.50?

**Options**:
- A) +5.0 (small bonus)
- B) +15.0 (moderate bonus)
- C) +30.0 (large bonus)
- D) +50.0 (same as emergency)

**Your Recommendation**: ___________

**Justification**: Should this be lower than emergency exit? Why?

**Expected Impact**: What % of rugs will this prevent?

---

### Question 2.4: Confidence Scaling

**Context**: Sidebet model provides confidence (0-1) for each prediction
**Data**: High confidence (>0.70) has 45% win rate, Low confidence (<0.60) has 28% win rate

**Question**: Should we scale exit bonuses by confidence?

**Options**:
- A) No scaling (all predictions weighted equally)
- B) Linear scaling (reward *= confidence)
- C) Quadratic scaling (reward *= confidence^2, emphasize high confidence)
- D) Hard cutoff (ignore predictions with confidence < 0.60)

**Your Recommendation**: ___________

**Justification**: What's the trade-off? (Cite Trade-off 3 from KEY_INSIGHTS.md)

**Pseudocode**:
```python
def confidence_scaled_reward(base_reward, confidence):
    """Scale reward by confidence"""
    # TODO: Your implementation
    pass
```

---

### Question 2.5: Timing Urgency Scaling

**Context**: Sidebet model provides `ticks_to_rug_norm` (0-1, normalized estimate of time until rug)
**Interpretation**: 0.0 = rug imminent, 1.0 = rug distant

**Question**: Should exit bonuses increase as ticks_to_rug_norm approaches 0?

**Options**:
- A) No urgency scaling (flat bonuses)
- B) Linear urgency (bonus *= (1 - ticks_to_rug_norm))
- C) Exponential urgency (bonus *= exp(-ticks_to_rug_norm))
- D) Step function (2x bonus when ticks_to_rug_norm < 0.2)

**Your Recommendation**: ___________

**Justification**: Why this approach?

**Expected Behavior**: How will agent respond to urgent signals?

---

## Section 3: Penalty Structure Redesign

**Context**: Current penalties are insufficient. Agent holds through rug_prob >= 0.50 in 30% of losses. Need severe penalties to deter ignoring signals.

### Question 3.1: Hold-Through Critical Signal Penalty

**Context**: When agent has positions AND rug_prob >= 0.50 AND action == WAIT (not exiting)

**Current State**: No explicit penalty (only eventual liquidation)
**Problem**: Agent ignores 30% of critical signals (from Finding 3)

**Question**: What penalty for holding through critical signal?

**Options**:
- A) -10.0 (small deterrent)
- B) -30.0 (moderate deterrent)
- C) -50.0 (strong deterrent)
- D) -100.0 (severe deterrent)

**Your Recommendation**: ___________

**Justification**: Why this magnitude? (Consider: this is unacceptable behavior)

**Expected Impact**: Will this reduce the 30% ignore rate? To what %?

**Pseudocode**:
```python
def hold_through_critical_penalty(state, action):
    """Penalize holding when rug_prob >= 0.50"""
    # TODO: Your implementation
    pass
```

---

### Question 3.2: Early Exit Penalty (False Alarm Prevention)

**Context**: Strong rug avoidance rewards may cause "always exit immediately" behavior

**Question**: Should we penalize exits during sweet spot when rug_prob is LOW?

**Conditions**: action == SELL AND in_sweet_spot (2-4x) AND rug_prob < 0.20

**Options**:
- A) No penalty (allow cautious behavior)
- B) -5.0 (small penalty)
- C) -10.0 (moderate penalty)
- D) -20.0 (strong penalty)

**Your Recommendation**: ___________

**Justification**: How does this balance with rug avoidance? (Cite Trade-off 2 from KEY_INSIGHTS.md)

**Risk**: If penalty too high, agent may ignore real signals. How to mitigate?

---

### Question 3.3: Bankruptcy Penalty

**Current State**: `-1000.0` (working well, 20% bankruptcy rate)
**Target**: <5% bankruptcy rate

**Question**: Should we adjust bankruptcy penalty?

**Options**:
- A) Keep at -1000.0 (seems sufficient)
- B) Increase to -2000.0 (stronger deterrent)
- C) Reduce to -500.0 (less harsh)

**Your Recommendation**: ___________

**Justification**: Why change or keep?

---

### Question 3.4: Rug Liquidation Penalty

**Context**: When position is liquidated by rug (exit_tick > rug_tick)

**Current State**: Implicit penalty from P&L loss (-95% to -99% of position)
**Problem**: May not be explicit enough for learning

**Question**: Should we add explicit rug liquidation penalty?

**Options**:
- A) No additional penalty (P&L loss is sufficient)
- B) -50.0 (moderate explicit penalty)
- C) -100.0 (strong explicit penalty)
- D) Scale by position size (larger positions = larger penalty)

**Your Recommendation**: ___________

**Justification**: Does explicit penalty help learning?

---

## Section 4: Sidebet Integration Strategy

**Context**: 5 features available: probability, confidence, ticks_to_rug_norm, is_critical, should_exit. Need concrete implementation strategy.

### Question 4.1: Which Features to Use Where?

**Available Features**:
1. `probability` (0-1): Rug likelihood
2. `confidence` (0-1): Prediction reliability
3. `ticks_to_rug_norm` (0-1): Time until rug (normalized)
4. `is_critical` (0/1): Boolean flag for critical threshold
5. `should_exit` (0/1): Boolean recommendation

**Question**: How should EACH feature be used in reward calculation?

**Your Answer**:
- `probability`: [Usage strategy]
- `confidence`: [Usage strategy]
- `ticks_to_rug_norm`: [Usage strategy]
- `is_critical`: [Usage strategy]
- `should_exit`: [Usage strategy]

**Example Strategy**:
```python
def calculate_rug_avoidance_reward(state, action, sidebet_features):
    probability = sidebet_features['probability']
    confidence = sidebet_features['confidence']
    ticks_to_rug_norm = sidebet_features['ticks_to_rug_norm']
    is_critical = sidebet_features['is_critical']
    should_exit = sidebet_features['should_exit']

    # TODO: Your implementation
    # Use probability to determine base reward
    # Use confidence to scale reward
    # Use ticks_to_rug_norm for urgency
    # Use is_critical for emergency bonuses
    # Use should_exit for action validation

    return reward
```

---

### Question 4.2: Signal Hierarchy

**Context**: Multiple exit signals available: sidebet predictions, volatility, patterns

**Question**: What should the priority hierarchy be when signals conflict?

**Example Conflict**: Sidebet says exit (rug_prob = 0.45) but volatility is low (no spike)

**Options**:
- A) Sidebet > Volatility > Patterns (sidebet dominates)
- B) Sidebet > Patterns > Volatility (deprioritize volatility)
- C) Weighted average (no strict hierarchy)
- D) Require consensus (exit only if 2+ signals agree)

**Your Recommendation**: ___________

**Justification**: Why this hierarchy? (Cite Finding 1 from KEY_INSIGHTS.md: "Sidebet model outperforms all other signals")

**Implementation**: How to encode hierarchy in rewards?

---

### Question 4.3: Threshold Sensitivity

**Context**: Sidebet thresholds determine signal strength
- LOW: rug_prob < 0.30
- MEDIUM: 0.30 <= rug_prob < 0.40
- HIGH: 0.40 <= rug_prob < 0.50
- CRITICAL: rug_prob >= 0.50

**Question**: Should we use different reward magnitudes for each level?

**Options**:
- A) Binary (reward only at CRITICAL)
- B) Two-tier (reward at HIGH and CRITICAL only)
- C) Three-tier (reward at MEDIUM, HIGH, CRITICAL)
- D) Continuous (smooth scaling from 0 to 1.0)

**Your Recommendation**: ___________

**Justification**: Why this granularity?

**Reward Structure** (if multi-tier):
```
CRITICAL (>=0.50): +_____
HIGH (0.40-0.50): +_____
MEDIUM (0.30-0.40): +_____
LOW (<0.30): +_____ (0 or small)
```

---

## Section 5: Position Sizing & Risk Management

**Context**: Agent manages bankroll across 15 games (starting: 0.1 SOL, threshold: 0.001 SOL)

### Question 5.1: Position Sizing Rewards

**Current State**: No explicit position sizing rewards
**Problem**: Agent may over-expose on risky games

**Question**: Should we reward conservative position sizing when rug_prob is high?

**Options**:
- A) No position sizing rewards (let agent learn implicitly)
- B) Small bonus (+5) for reducing position when rug_prob >= 0.40
- C) Moderate bonus (+10-15) for defensive sizing
- D) Scale bonus by rug_prob (higher prob = larger bonus for small positions)

**Your Recommendation**: ___________

**Justification**: How does this interact with exit bonuses?

---

### Question 5.2: Capital Preservation

**Context**: 20% bankruptcy rate (1 in 5 episodes fail completely)

**Question**: Should we add explicit capital preservation rewards?

**Options**:
- A) No (bankruptcy penalty is sufficient)
- B) Small bonus (+5) each tick bankroll > 0.05 SOL (50% of start)
- C) Milestone bonuses (+50 for reaching end of episode with >0.05 SOL)
- D) Quadratic reward (reward grows with bankroll)

**Your Recommendation**: ___________

**Justification**: Does this conflict with profit maximization?

---

### Question 5.3: Multi-Game Risk Awareness

**Context**: Agent plays 15 consecutive games. Bad streak can bankrupt agent.

**Question**: Should rewards scale based on current bankroll?

**Example**: If bankroll is low (<0.02 SOL), increase rug avoidance weight

**Options**:
- A) No scaling (fixed weights throughout episode)
- B) Moderate scaling (1.5x rug avoidance when bankroll < 0.02)
- C) Strong scaling (2-3x rug avoidance when bankroll < 0.02)
- D) Adaptive (scale continuously based on bankroll / start_bankroll ratio)

**Your Recommendation**: ___________

**Justification**: Will agent learn to be more cautious when vulnerable?

**Pseudocode**:
```python
def get_risk_adjusted_weight(base_weight, current_bankroll, start_bankroll):
    """Adjust weight based on remaining capital"""
    # TODO: Your implementation
    pass
```

---

## Section 6: Temporal Dynamics

**Context**: Game duration varies (mean: 329 ticks, std dev: 180 ticks). Z-score (duration outlier) is 63.64% of sidebet model importance.

### Question 6.1: Time-Based Reward Scaling

**Question**: Should exit bonuses increase with game duration?

**Rationale**: Longer games have higher rug probability (from Finding 4: z_score dominance)

**Options**:
- A) No time scaling (flat bonuses)
- B) Linear scaling (bonus *= tick_num / mean_duration)
- C) Z-score scaling (bonus *= z_score, captures outlier risk)
- D) Exponential scaling (bonus *= exp(tick_num / mean_duration))

**Your Recommendation**: ___________

**Justification**: How does this align with sidebet model's z_score feature?

---

### Question 6.2: Hold Duration Optimization

**Context**: Sweet spot is 2-4x (40-80 ticks). Average hold time is 60 ticks.

**Question**: Should we explicitly reward hold durations in optimal range?

**Options**:
- A) No hold duration rewards (entry/exit timing is enough)
- B) Bonus for exiting in sweet spot window (+10-20)
- C) Penalty for exiting too early (<20 ticks) or too late (>100 ticks)
- D) Both bonus and penalty

**Your Recommendation**: ___________

**Justification**: Does this conflict with rug avoidance?

---

## Section 7: Implementation Strategy

**Context**: Need phased rollout to validate changes incrementally

### Question 7.1: Phase 1 (Week 1) - Core Changes

**Proposed Core Changes**:
1. Add rug avoidance component (weight >10.0)
2. Reduce P&L weight (1.0 → 0.3-0.5)
3. Reduce volatility weight (8.0 → 2-3)
4. Add emergency exit bonus (+50 for rug_prob >= 0.50)
5. Add hold-through penalty (-100 for ignoring critical signal)

**Question**: Do you agree with these as Phase 1 priorities?

**Your Answer**: [Yes/No, with modifications if needed]

**Justification**: Why this set? Should any be moved to Phase 2?

**Expected Impact**: What metrics should improve after Phase 1? (Quantify)

---

### Question 7.2: Phase 2 (Week 2) - Fine-Tuning

**Proposed Fine-Tuning**:
1. Add proactive exit bonus (+30 for rug_prob >= 0.40)
2. Add early exit penalty (-10 for premature exits)
3. Implement confidence scaling
4. Add position sizing rewards
5. Tune thresholds based on Phase 1 data

**Question**: Do you agree with Phase 2 scope?

**Your Answer**: [Yes/No, with modifications]

**Justification**: Why wait until Phase 2 for these changes?

---

### Question 7.3: Phase 3 (Week 3) - Validation

**Proposed Validation**:
1. Backtest on 100 episodes
2. Monitor rug avoidance rate (target >70% as intermediate milestone)
3. Check for overfitting (agent always exiting immediately?)
4. Adjust weights if needed
5. Final validation (target >90% rug avoidance)

**Question**: Is this validation plan sufficient?

**Your Answer**: [Yes/No, suggestions]

**Additional Metrics**: What else should we track?

---

### Question 7.4: Rollback Strategy

**Question**: If Phase 1 makes performance WORSE, what's the rollback plan?

**Options**:
- A) Revert all changes, start over
- B) Keep rug avoidance component, revert weight changes
- C) Iteratively reduce rug avoidance weight until performance stabilizes
- D) Analyze failure mode, adjust specific component

**Your Recommendation**: ___________

**Criteria**: At what point do we consider Phase 1 a failure? (e.g., bankruptcy >30%?)

---

## Section 8: Success Metrics Validation

**Context**: Primary targets are >90% rug avoidance, >60% win rate, <5% bankruptcy

### Question 8.1: Intermediate Milestones

**Question**: What intermediate milestones should we target after Phase 1?

**Current Baseline**:
- Rug avoidance: 30%
- Win rate: 30%
- Bankruptcy: 20%

**Your Phase 1 Targets**:
- Rug avoidance: _____% (suggest 50-70% as intermediate)
- Win rate: _____% (suggest 40-50% as intermediate)
- Bankruptcy: _____% (suggest 10-15% as intermediate)

**Justification**: Why these intermediate targets? Are they achievable?

---

### Question 8.2: Leading Indicators

**Question**: What early signals indicate the redesign is working?

**Options** (select all applicable):
- A) Agent exits more frequently on rug_prob >= 0.50
- B) Average position hold time decreases
- C) Rug liquidation rate decreases
- D) Bankruptcy rate decreases
- E) Win rate increases
- F) Agent uses sidebet signals (observable in action logs)

**Your Selection**: [A/B/C/D/E/F]

**Metric**: What specific metric can we track in first 10 training episodes?

---

### Question 8.3: Failure Modes

**Question**: What failure modes should we watch for?

**Potential Failures**:
1. **Always Exit Immediately**: Agent exits on game start (overfitting to rug avoidance)
2. **Ignores All Signals**: Agent continues holding despite critical signals (underfitting)
3. **Thrashing**: Agent enters/exits rapidly (reward confusion)
4. **Bankruptcy Spike**: New rewards cause risk-taking (unintended)

**For Each Failure Mode**: How would we detect it? How would we fix it?

**Your Analysis**:
1. Always Exit: [Detection method] → [Fix]
2. Ignores Signals: [Detection method] → [Fix]
3. Thrashing: [Detection method] → [Fix]
4. Bankruptcy Spike: [Detection method] → [Fix]

---

### Question 8.4: Human Validation

**Question**: How should human (you, the user) validate the redesign?

**Options**:
- A) Watch REPLAYER with sidebet predictions on recorded games
- B) Monitor training logs for signal usage
- C) Review episode summaries (win rate, rug avoidance per episode)
- D) All of the above

**Your Recommendation**: ___________

**Deliverable**: What specific report/visualization would help human validation?

---

## Section 9: Open Questions & Known Unknowns

**Context**: Some design questions can only be answered through experimentation

### Question 9.1: Optimal Rug Avoidance Weight

**Known**: Weight should be >5.0 (higher than all other components)
**Unknown**: Exact value (10.0? 15.0? 20.0?)

**Your Starting Recommendation**: ___________

**Experimental Plan**: How to find optimal value? (e.g., "Start at 10.0, increase by 2.0 if rug avoidance <70% after 100 episodes")

---

### Question 9.2: Confidence Threshold

**Known**: Low confidence (<0.60) predictions are noisy (28% win rate)
**Unknown**: Should we ignore them? Or scale down?

**Your Starting Recommendation**: [Ignore / Scale by confidence / Use all]

**Experimental Plan**: How to test this? (e.g., "Phase 1: use all, Phase 2: add threshold if too noisy")

---

### Question 9.3: Multi-Signal Consensus

**Known**: Sidebet, volatility, patterns all provide exit signals
**Unknown**: How to combine when they conflict?

**Your Starting Recommendation**: [Hierarchy / Weighted average / Consensus voting]

**Experimental Plan**: How to validate this approach?

---

## Section 10: Component Interactions

**Context**: Reward components interact in complex ways. Need to consider side effects.

### Question 10.1: Rug Avoidance vs P&L Tension

**Tension**: High rug avoidance rewards encourage early exits. Low P&L weight reduces profit motive. Net effect?

**Question**: Will agent still seek profitable entries? Or just exit immediately?

**Your Analysis**: [How do these components balance?]

**Mitigation**: What prevents "always exit" behavior? (early exit penalty sufficient?)

---

### Question 10.2: Confidence Scaling vs Signal Availability

**Tension**: Scaling by confidence reduces reward for low-confidence predictions. But low-confidence predictions are 60% of signals.

**Question**: Will agent have enough learning signal?

**Your Analysis**: [Is signal availability a concern?]

**Mitigation**: If signals too sparse, what's the fallback?

---

### Question 10.3: Penalty Severity vs Exploration

**Tension**: Severe penalties (-100) discourage exploration. Agent may avoid risky but profitable strategies.

**Question**: Will harsh penalties hurt learning?

**Your Analysis**: [How does this affect exploration/exploitation balance?]

**Mitigation**: Should penalties scale during training? (e.g., start at -30, increase to -100 over time?)

---

## Section 11: Final Recommendations

**Context**: Synthesize all answers into concrete deliverables

### Question 11.1: Component Weight Summary

**Question**: Provide final weight recommendations for ALL components

**Format**:
```
| Component | Current | Proposed | Justification |
|-----------|---------|----------|---------------|
| pnl_reward | 1.0 | _____ | [Why?] |
| rug_avoidance | 0.0 | _____ | [Why?] |
| volatility_exit | 8.0 | _____ | [Why?] |
| sweet_spot | 2.0 | _____ | [Why?] |
| patterns | ~3.0 | _____ | [Why?] |
| position_sizing | 0.0 | _____ | [Why?] |
```

---

### Question 11.2: New Component Definitions

**Question**: Define ALL new reward components with pseudocode

**Required Components**:
1. Rug avoidance reward (exit bonuses)
2. Hold-through critical signal penalty
3. Early exit penalty
4. [Any others you recommend]

**Format** (for each):
```python
def component_name(state, action, next_state):
    \"\"\"
    Description: [What this rewards/penalizes]
    Trigger: [When does this apply?]
    Magnitude: [Range of values]
    \"\"\"
    # Implementation
    pass
```

---

### Question 11.3: Sidebet Feature Usage Map

**Question**: For each of the 5 sidebet features, specify exactly where/how it's used

**Format**:
```
probability (0-1):
  - Used in: [Component names]
  - Purpose: [Why?]
  - Formula: [How?]

confidence (0-1):
  - Used in: [Component names]
  - Purpose: [Why?]
  - Formula: [How?]

ticks_to_rug_norm (0-1):
  - Used in: [Component names]
  - Purpose: [Why?]
  - Formula: [How?]

is_critical (0/1):
  - Used in: [Component names]
  - Purpose: [Why?]
  - Formula: [How?]

should_exit (0/1):
  - Used in: [Component names]
  - Purpose: [Why?]
  - Formula: [How?]
```

---

### Question 11.4: Implementation Checklist

**Question**: Provide step-by-step implementation checklist

**Format**:
```
Phase 1 (Week 1):
[ ] 1. Update reward_calculator.py: Add rug_avoidance_reward() method
[ ] 2. Update reward_calculator.py: Add hold_through_critical_penalty() method
[ ] 3. Update reward config: Set rug_avoidance weight to _____
[ ] 4. Update reward config: Reduce pnl_weight to _____
[ ] 5. Update reward config: Reduce volatility_exit weight to _____
[ ] 6. Run unit tests: test_reward_calculator.py
[ ] 7. Run integration tests: test_sidebet_integration.py
[ ] 8. Backtest 10 episodes: Verify no crashes
[ ] 9. Train 100 episodes: Monitor rug avoidance rate
[ ] 10. Validate: Check rug avoidance >= ____% (intermediate target)

Phase 2 (Week 2):
[ ] ... [Continue]

Phase 3 (Week 3):
[ ] ... [Continue]
```

---

### Question 11.5: Success Criteria

**Question**: Define EXACT success criteria for each phase

**Format**:
```
Phase 1 Success Criteria (must achieve ALL):
- Rug avoidance: >= _____% (intermediate target)
- Win rate: >= _____% (intermediate target)
- Bankruptcy: <= _____% (intermediate target)
- Agent exits on critical signals: >= _____% of the time
- No "always exit immediately" behavior: entry rate >= _____% of baseline

Phase 2 Success Criteria:
- ... [Continue]

Phase 3 Success Criteria (PRIMARY TARGETS):
- Rug avoidance: >= 90% (MUST ACHIEVE)
- Win rate: >= 60% (MUST ACHIEVE)
- Bankruptcy: <= 5% (MUST ACHIEVE)
- ROI: >= 200% (SHOULD ACHIEVE)
- Sharpe ratio: >= 1.5 (SHOULD ACHIEVE)
```

---

### Question 11.6: YAML Configuration

**Question**: Provide complete YAML config file ready to deploy

**Format**:
```yaml
# Reward Configuration - Sidebet-Enhanced Trading
version: "2.0"
description: "Rug avoidance as primary objective with sidebet model integration"

components:
  rug_avoidance:
    enabled: true
    weight: _____  # [Your recommendation]
    emergency_exit_bonus: _____  # rug_prob >= 0.50
    proactive_exit_bonus: _____  # rug_prob >= 0.40
    hold_through_critical_penalty: _____  # Negative value
    confidence_scaling: [true/false]  # [Your recommendation]
    urgency_scaling: [true/false]  # [Your recommendation]

  pnl_reward:
    enabled: true
    weight: _____  # [Your recommendation]
    # ... [Continue for all components]

  # ... [Complete config]
```

---

## Summary

**Total Questions**: ~45 across 11 sections

**Expected Outputs**:
1. Specific numerical recommendations (weights, bonuses, penalties)
2. Justifications citing data/statistics
3. Pseudocode for new components
4. Trade-off analysis
5. Implementation checklist
6. Success criteria
7. Complete YAML configuration

**Next Steps After Completing Questions**:
1. Review answers for consistency (do components work together?)
2. Generate 8 required deliverables (see LLM_INSTRUCTIONS.md)
3. Validate against success criteria (>90% rug avoidance achievable?)
4. Iterate if needed (challenge vague answers, request specifics)

**Time Estimate**: 90-120 minutes to work through all questions systematically

---

**Instructions Reminder**:
- Answer in order (don't skip)
- Provide exact values (not ranges)
- Cite evidence (reference KEY_INSIGHTS.md, REWARD_DESIGN_PROMPT.md)
- Include pseudocode (show implementation)
- Explain trade-offs (acknowledge costs)
- Ask questions (if you need more data)

**Ready to begin? Start with Section 1, Question 1.1**
