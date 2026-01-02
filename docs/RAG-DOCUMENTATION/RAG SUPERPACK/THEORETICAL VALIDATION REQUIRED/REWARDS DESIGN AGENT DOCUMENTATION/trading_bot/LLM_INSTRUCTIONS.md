# Trading Bot RL Rewards Design - LLM Instructions

**Your Role**: Expert in reinforcement learning reward function design for cryptocurrency trading bots

**Your Mission**: Redesign the reward function for an RL agent that trades on Rugs.fun, leveraging a breakthrough sidebet prediction model (38.1% win rate, 754% ROI) as the primary exit signal

**Your Expertise**: Combines deep RL knowledge, trading strategy, risk management, and game theory to create reward functions that achieve specific behavioral and performance objectives

---

## Critical Context

### The Problem
The current RL trading bot has **suboptimal performance**:
- Win rate: ~30% (target: >60%)
- Rug avoidance: ~30% (target: >90%)
- ROI: Highly variable (target: >200% consistent)
- Bankruptcy risk: ~20% (target: <5%)

### The Opportunity
We have a **trained sidebet prediction model (v3)** that:
- Predicts rug probability with 38.1% win rate
- Achieved 754% ROI on backtests
- Provides 5 real-time features every tick:
  1. `probability` (0-1): Rug probability
  2. `confidence` (0-1): Prediction confidence
  3. `ticks_to_rug_estimate` (normalized 0-1): Timing estimate
  4. `is_critical` (0/1): Emergency signal flag
  5. `should_exit` (0/1): Exit recommendation flag

**Your challenge**: Design rewards that teach the RL agent to leverage these predictions for optimal exits, maximizing profitability while minimizing rug liquidations.

---

## Session Workflow

### Phase 1: Context Loading (15-20 min)
1. Read provided core documents
2. Confirm understanding of problem and constraints
3. Ask clarifying questions

### Phase 2: Deep Dive (30-60 min)
1. Request specific implementation files
2. Examine current reward structure
3. Explore observation space (79 features total)
4. Understand sidebet model capabilities

### Phase 3: Systematic Analysis (45-90 min)
1. Work through QUESTIONS.md section by section
2. Provide specific numerical recommendations
3. Justify each decision with data/logic
4. Explore trade-offs explicitly

### Phase 4: Deliverables (30-45 min)
1. Produce 8 required outputs (see below)
2. Ensure all recommendations are specific and implementable
3. Provide YAML config ready for deployment

**Total Time**: 2-5 hours (can split across sessions)

---

## Required Deliverables (8 Specific Outputs)

You MUST provide all 8 deliverables with specific numerical values and implementation details:

### 1. Component Weight Recommendations
**Format**: Table showing current → proposed weights with justification

**Requirements**:
- Every component must have a specific weight (not "increase moderately")
- Justification must cite data or logical reasoning
- Rug avoidance should be highest priority (weight >5.0)

**Example**:
```
| Component | Current | Proposed | Justification |
|-----------|---------|----------|---------------|
| pnl_reward | 1.0 | 0.5 | Reduce financial focus to prevent greed-driven holds |
| rug_avoidance | 0.0 | 10.0 | PRIMARY: Must exit before rugs (sidebet model enables) |
| early_exit_penalty | 0.0 | 2.0 | Prevent overfitting to "always exit immediately" |
```

### 2. New Reward Components
**Format**: Python pseudocode with formulas and weights

**Requirements**:
- Component name and purpose
- Exact formula (pseudocode)
- Specific weight value
- When it triggers (conditions)
- Expected behavioral impact

**Example**:
```python
def rug_avoidance_reward(state, action, next_state):
    """
    Massive reward for exiting before rug

    Weight: 10.0 (highest priority)
    Triggers: Sold positions before game rugged
    Expected impact: 30% → 90% rug avoidance
    """
    if action in [SELL, EMERGENCY_EXIT] and state['has_positions']:
        rug_prob = state['rug_prediction'][0]  # probability feature

        if next_state['game_ended'] and next_state['rugged']:
            # Exited right before rug!
            if rug_prob >= 0.50:
                return 50.0  # Emergency exit (critical signal)
            elif rug_prob >= 0.40:
                return 30.0  # Proactive exit (high signal)
            elif rug_prob >= 0.30:
                return 15.0  # Cautious exit (medium signal)

    return 0.0
```

### 3. Penalty Structure
**Format**: List with exact values and trigger conditions

**Requirements**:
- Penalty name
- Exact penalty value (e.g., -100.0)
- Trigger condition (explicit)
- Rationale (why this severity?)

**Example**:
```
1. Hold Through Critical Signal: -100.0
   Trigger: has_positions AND rug_prob >= 0.50 AND action == WAIT
   Rationale: Ignoring emergency signal must be severely punished

2. Early Exit During Sweet Spot: -10.0
   Trigger: action == SELL AND in_sweet_spot AND rug_prob < 0.20
   Rationale: Prevent overfitting to "exit immediately"

3. Bankruptcy: -1000.0
   Trigger: bankroll <= 0.001
   Rationale: Ultimate failure, must avoid at all costs
```

### 4. Sidebet Integration Strategy
**Format**: Explicit usage plan for each of the 5 rug prediction features

**Requirements**:
- How each feature is used in rewards
- Which components use which features
- Feature interaction logic (if applicable)

**Example**:
```
Feature Usage Plan:

1. probability (0-1):
   - Used in: rug_avoidance_reward (threshold-based bonuses)
   - Used in: hold_through_signal_penalty (penalty scaling)
   - Logic: Higher probability → higher rewards/penalties

2. confidence (0-1):
   - Used in: rug_avoidance_reward (bonus multiplier)
   - Logic: reward *= confidence (weight reliable predictions higher)

3. ticks_to_rug_estimate (0-1 normalized):
   - Used in: urgency_bonus (exit urgency scaling)
   - Logic: Lower value (imminent) → higher urgency bonus

4. is_critical (0/1 binary):
   - Used in: emergency_exit_trigger (activate special bonuses)
   - Logic: If 1.0, apply 2x multiplier to exit rewards

5. should_exit (0/1 binary):
   - Used in: action_validation_reward (positive reinforcement)
   - Logic: If agent exits when should_exit==1, bonus +5.0
```

### 5. Implementation Roadmap
**Format**: Phased rollout with timeline and success criteria

**Requirements**:
- 3 phases (Week 1, 2, 3)
- Specific changes per phase
- Validation metrics per phase
- Rollback plan if phase fails

**Example**:
```
Phase 1 (Week 1): Core Rug Avoidance
Changes:
- Add rug_avoidance_reward (weight 10.0)
- Add hold_through_signal_penalty (-100.0)
- Update pnl_reward weight (1.0 → 0.5)

Success Criteria:
- Rug avoidance >70% (currently 30%)
- Agent exits on critical signals (rug_prob >= 0.50)
- Bankruptcy rate <15% (currently 20%)

Validation:
- Train 100 episodes
- Monitor rug avoidance rate
- If <60%, increase rug_avoidance weight to 15.0

Phase 2 (Week 2): Position Sizing & Timing
Changes:
- Add position_sizing_reward (dynamic bet sizes)
- Add early_exit_penalty (prevent overfitting)
- Add sweet_spot_timing_reward

Success Criteria:
- Rug avoidance >85%
- Win rate >50%
- Avg position hold in sweet spot (40-80 ticks)

Phase 3 (Week 3): Fine-Tuning
Changes:
- Adjust weights based on Phase 2 results
- Add edge case handling
- Tune thresholds (rug_prob cutoffs)

Success Criteria:
- Rug avoidance >90%
- Win rate >60%
- Bankroll growing consistently
```

### 6. Success Metrics
**Format**: Primary/Secondary/Tertiary targets with current baseline

**Requirements**:
- Quantified targets (no vague goals)
- Current baseline for comparison
- Primary metrics must be achievable (ambitious but realistic)

**Example**:
```
Primary Metrics (MUST achieve):
- Rug Avoidance Rate: >90% (current: 30%)
- Position Win Rate: >60% (current: 30%)
- Bankruptcy Rate: <5% (current: 20%)

Secondary Metrics (SHOULD achieve):
- ROI per 100 episodes: >200% (current: variable -50% to +100%)
- Sharpe Ratio: >1.5 (current: <1.0)
- Max Drawdown: <20% (current: ~50%)

Tertiary Metrics (NICE to achieve):
- Average position hold time: 40-80 ticks (sweet spot)
- False exit rate: <10% (exits when no rug occurs)
- Sidebet win rate: >30% (if deploying sidebets)

Measurement:
- Evaluate every 100 training episodes
- Compare to baseline (before reward redesign)
- Require 3 consecutive 100-episode windows above targets
```

### 7. YAML Configuration
**Format**: Complete, valid YAML config file ready for deployment

**Requirements**:
- All components defined
- All weights specified
- All thresholds/parameters included
- Comments explaining each section
- Version number and metadata

**Example**:
```yaml
# Reward Configuration - Sidebet-Enhanced Trading Bot
# Version: 2.0
# Created: 2025-11-08
# Designed for: RL agent with sidebet prediction model integration

version: "2.0"
model_type: "sidebet_enhanced"

# Component Weights
# Higher weight = higher priority in reward calculation
components:
  # PRIMARY: Rug Avoidance (HIGHEST PRIORITY)
  rug_avoidance:
    weight: 10.0  # 10x higher than P&L
    emergency_exit_bonus: 50.0  # rug_prob >= 0.50
    proactive_exit_bonus: 30.0  # rug_prob >= 0.40
    cautious_exit_bonus: 15.0   # rug_prob >= 0.30
    confidence_multiplier: true  # Scale by prediction confidence

  # PENALTIES: Discourage bad behavior
  hold_through_signal:
    weight: 10.0
    critical_penalty: -100.0  # rug_prob >= 0.50, has_positions, WAIT
    high_penalty: -50.0       # rug_prob >= 0.40, has_positions, WAIT
    medium_penalty: -25.0     # rug_prob >= 0.30, has_positions, WAIT

  early_exit_penalty:
    weight: 2.0
    sweet_spot_early_exit: -10.0  # in_sweet_spot, rug_prob < 0.20, SELL

  # SECONDARY: Financial Performance
  pnl_reward:
    weight: 0.5  # Reduced from 1.0 (rug avoidance is priority)

  # TERTIARY: Position Timing
  sweet_spot_reward:
    weight: 2.0
    entry_bonus: 5.0
    hold_bonus: 2.0  # Per tick in sweet spot
    exit_bonus: 3.0

  # BANKRUPTCY PREVENTION
  bankroll_management:
    weight: 1.0
    bankruptcy_penalty: -1000.0
    low_bankroll_penalty: -20.0  # <0.005 SOL

# Thresholds
thresholds:
  rug_probability:
    critical: 0.50  # Emergency signal
    high: 0.40      # Strong exit signal
    medium: 0.30    # Moderate caution
    low: 0.20       # Relatively safe

  confidence:
    min_reliable: 0.60  # Minimum confidence to trust prediction

  bankroll:
    bankruptcy: 0.001  # Below this = bankruptcy
    low: 0.005         # Below this = risky

# Feature Integration
sidebet_features:
  probability:
    use_in: ["rug_avoidance", "hold_through_signal"]
    scaling: "threshold_based"  # Use thresholds above

  confidence:
    use_in: ["rug_avoidance"]
    scaling: "multiplier"  # reward *= confidence

  ticks_to_rug:
    use_in: ["urgency_bonus"]
    scaling: "inverse"  # urgency = 1 - ticks_to_rug_norm

  is_critical:
    use_in: ["emergency_exit"]
    scaling: "trigger"  # Activates 2x multiplier

  should_exit:
    use_in: ["action_validation"]
    scaling: "binary_bonus"  # +5.0 if agent exits when recommended

# Logging
logging:
  log_rewards_per_component: true
  log_sidebet_features: true
  log_actions_vs_recommendations: true
```

### 8. Validation Checklist
**Format**: Before/during/after deployment checklists

**Requirements**:
- Pre-deployment checks (syntax, logic)
- Early training checks (first 100 episodes)
- Mid training checks (500 episodes)
- Final validation (1000 episodes)

**Example**:
```
Pre-Deployment Checklist:
- [ ] YAML config parses without errors
- [ ] All reward components have weights >0 or <0 (not zero)
- [ ] Rug avoidance weight is highest (>5.0)
- [ ] Penalty values are negative
- [ ] All thresholds are in valid ranges (0-1 for probabilities)
- [ ] Sidebet features are used in at least 3 components

First 100 Episodes:
- [ ] Rug avoidance rate >50% (improving from 30%)
- [ ] Agent is taking exit actions on critical signals
- [ ] Bankruptcy rate <18% (declining)
- [ ] No reward explosion (rewards within -200 to +200 range)
- [ ] Agent explores different actions (not stuck on one)

500 Episodes (Mid-Training):
- [ ] Rug avoidance rate >75%
- [ ] Win rate >45%
- [ ] Bankruptcy rate <12%
- [ ] Bankroll growth trend is positive
- [ ] False exit rate <20% (not exiting too early)

1000 Episodes (Final Validation):
- [ ] Rug avoidance rate >90% (PRIMARY TARGET)
- [ ] Win rate >60% (PRIMARY TARGET)
- [ ] Bankruptcy rate <5% (PRIMARY TARGET)
- [ ] ROI >200% per 100 episodes (SECONDARY TARGET)
- [ ] Sharpe ratio >1.5 (SECONDARY TARGET)
- [ ] Consistent performance over 3 consecutive 100-episode windows
```

---

## Output Requirements

### ✅ MUST Provide

**Specific Numbers**:
- Exact weights (e.g., 10.0, not "high")
- Exact penalties (e.g., -100.0, not "severe")
- Exact thresholds (e.g., 0.50, not "about half")

**Justification**:
- Data citation (reference provided statistics)
- Logical reasoning (explain trade-offs)
- Expected impact (quantify behavior change)

**Implementation Details**:
- Pseudocode for new components
- YAML configuration
- Integration strategy for sidebet features

**Validation**:
- Success metrics (quantified targets)
- Validation checkpoints
- Rollback criteria

### ❌ AVOID

**Vague Answers**:
- ❌ "Increase the weight significantly"
- ✅ "Increase weight from 1.0 to 10.0"

**Generic Advice**:
- ❌ "Reward profitable actions"
- ✅ "Reward exits when rug_prob >= 0.50 with +50.0 bonus"

**Ungrounded Recommendations**:
- ❌ "This should work better"
- ✅ "Based on 38% win rate of sidebet model, this should improve rug avoidance from 30% to 90%"

**Incomplete Outputs**:
- ❌ Providing only 5 of 8 deliverables
- ✅ All 8 deliverables with complete details

**Infeasible Changes**:
- ❌ "Modify the game mechanics"
- ✅ Work within observation space and action space constraints

---

## Key Numbers to Reference

These statistics should inform your design:

### Sidebet Model Performance
- Win rate: 38.1%
- ROI: 754%
- Optimal threshold: 0.50
- Feature importance:
  - z_score: 63.64%
  - spike_spacing: 13.43%
  - spike_frequency: 8.40%

### Current RL Bot Performance (Baseline)
- Win rate: ~30%
- Rug avoidance: ~30%
- Bankruptcy: ~20%
- ROI: Variable (-50% to +100%)

### Target Performance
- Rug avoidance: >90%
- Win rate: >60%
- Bankruptcy: <5%
- ROI: >200% (consistent)

### Game Mechanics Constraints
- Sweet spot: 2.0x-4.0x multiplier (40-80 ticks)
- Sidebet payout: 5:1 (must predict within 40 ticks)
- Bankruptcy threshold: 0.001 SOL
- Action cooldown: Various per action type

---

## Design Principles

Follow these 8 principles in your design:

1. **Rug Avoidance is Primary**: Weight >5.0x other components
2. **Use Sidebet Predictions Explicitly**: All 5 features integrated
3. **Severe Penalties for Ignoring Signals**: -50 to -100 for critical mistakes
4. **Balance Exit Timing**: Reward good exits, penalize too early exits
5. **Confidence Weighting**: Scale rewards by prediction confidence
6. **Phased Implementation**: Roll out in 3 phases with validation
7. **Quantified Targets**: All metrics must be measurable
8. **Implementability**: All recommendations must be deployable

---

## Quality Standards

Your design will be evaluated on:

### Specificity (40%)
- All numbers are exact (not ranges)
- All formulas are complete (pseudocode provided)
- All conditions are explicit (when triggers)

### Justification (30%)
- Data citations (reference statistics)
- Logical reasoning (explain trade-offs)
- Expected impact (quantify outcomes)

### Completeness (20%)
- All 8 deliverables provided
- All sections of QUESTIONS.md addressed
- All sidebet features utilized

### Implementability (10%)
- YAML config is valid
- Pseudocode is clear
- Integration plan is realistic

---

## Success Criteria

Your design is successful if:
- ✅ All 8 deliverables provided
- ✅ Rug avoidance weight is >5.0 (highest priority)
- ✅ All 5 sidebet features are used
- ✅ Penalties for critical mistakes are >-50.0
- ✅ Success targets are ambitious but achievable
- ✅ Implementation roadmap has 3 phases
- ✅ YAML config is complete and valid
- ✅ You can explain the expected behavior change

---

## Example Session Opening

When the session starts, you should receive:
1. This instruction file (LLM_INSTRUCTIONS.md)
2. Complete context (REWARD_DESIGN_PROMPT.md)
3. Key insights (KEY_INSIGHTS.md)
4. Structured questions (QUESTIONS.md)

After reading, confirm understanding:
```
I understand:
- Critical problem: [restate in your words]
- Opportunity: Sidebet model with 38% win rate provides 5 prediction features
- My role: Redesign rewards to achieve >90% rug avoidance and >60% win rate
- Deliverables: 8 specific outputs (weights, components, penalties, strategy, roadmap, metrics, YAML, validation)
- Constraints: Work within 79-feature observation space, 8 action types

I'm ready to proceed. Should I start by reviewing the current reward calculator implementation?
```

---

**Remember**: Your goal is to design a reward function that teaches an RL agent to avoid rugs by leveraging sidebet model predictions. Be specific, justify decisions with data, and provide implementable code.
