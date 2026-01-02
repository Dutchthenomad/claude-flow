# Instructions: Reward Function Redesign Session

## Your Role
You are an expert in reinforcement learning reward design. Your task is to redesign a reward function for a trading bot that currently has a **94.6% bankruptcy rate** (151/160 episodes failed).

## Critical Context
- **Problem**: Trading bot goes bankrupt in 94.6% of training episodes
- **Cause**: Reward function encourages aggressive trading without proper risk management
- **Goal**: Redesign reward function to achieve >90% survival rate, >60% win rate, >0.010 SOL profit per episode
- **Constraint**: Training uses actual game engine (no simulation) with instant liquidation mechanics

## Session Workflow

### Phase 1: Understand the Problem (15-20 min)
1. **Read**: `REWARD_DESIGN_PROMPT.md` (master context document)
2. **Read**: `REWARD_DESIGN_KEY_INSIGHTS.md` (critical findings summary)
3. **Confirm**: You understand the bankruptcy problem and statistical findings
4. **Ask**: For any clarifying questions before proceeding

### Phase 2: Analyze Current System (20-30 min)
5. **Request**: Supporting files as needed from `REWARD_DESIGN_BUNDLE.md`
   - Priority 1: `reward_calculator.py` (lines 187-456) - current implementation
   - Priority 2: `reward_config.yaml` - current weights
   - Priority 3: `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` - game rules
6. **Identify**: Specific issues with current reward components and weights
7. **Prioritize**: Which changes will have biggest impact on survival rate

### Phase 3: Systematic Redesign (60-90 min)
8. **Work through**: `REWARD_DESIGN_QUESTIONS.md` systematically (11 sections, 40+ questions)
9. **Provide**: Specific numerical answers (not "increase slightly" - give exact values like "0.8")
10. **Justify**: Every recommendation with statistical evidence or game mechanics reasoning
11. **Request**: Additional files from bundle as needed for context

### Phase 4: Deliver Final Design (30-45 min)
12. **Provide complete deliverables** (see below)

## Required Deliverables

### 1. Revised Component Weights (REQUIRED)
Provide exact values for all 13 components with rationale:
```yaml
# Format:
pnl_weight: [exact value]  # Rationale: [why this value]
pattern_bonus_weight: [exact value]  # Rationale: [reference to p-values]
risk_management_weight: [exact value]  # Rationale: [bankruptcy prevention]
volatility_weight: [exact value]  # Rationale: [94.7% accuracy]
entry_timing_weight: [exact value]
exit_timing_weight: [exact value]
sidebet_ev_weight: [exact value]
balance_preservation: [exact value]
liquidity_weight: [exact value]
sweet_spot_weight: [exact value]
win_rate_weight: [exact value]
consistency_weight: [exact value]
drawdown_penalty: [exact value]
```

### 2. New Components to Add (REQUIRED)
Specify new reward components needed:
```python
# Format for each new component:
class ComponentName:
    """What it does and why needed"""
    weight = [exact value]

    def calculate(self, state, action, info):
        # Pseudocode or actual implementation
        return reward_value
```

**Minimum required new components:**
- Patience reward (for WAIT actions when no edge)
- Survival milestone bonuses (for completing games)
- Setup quality scoring (multi-factor entry quality)

### 3. Penalty Structure Updates (REQUIRED)
Specify exact penalties for:
- Entry without pattern signal: `[value]` (e.g., -0.05)
- Trading during high volatility without edge: `[value]`
- Over-trading (frequency penalty): `[formula]`
- Any other penalties needed

### 4. Risk Management Architecture (REQUIRED)
Choose and specify:
- **Additive** (current): `reward = pnl + risk_bonus + patterns + ...`
- **Multiplicative**: `reward = (pnl + patterns) * risk_multiplier`
- **Hybrid**: `reward = (pnl * risk_multiplier) + patterns + ...`

Provide exact formula and explain why chosen.

### 5. Implementation Priority (REQUIRED)
Rank changes in implementation order:
```
Phase 1 (Must have - bankruptcy fix):
1. [Specific change with exact values]
2. [Specific change with exact values]
3. ...

Phase 2 (Should have - performance optimization):
1. ...

Phase 3 (Nice to have - refinements):
1. ...
```

### 6. Expected Outcomes (REQUIRED)
Provide specific predictions:
- **Survival rate**: [X]% (target: >90%)
- **Win rate**: [Y]% (target: >60%)
- **Profit per episode**: [Z] SOL (target: >0.010)
- **Training episodes to convergence**: [N] episodes
- **Key behavioral changes**: [specific changes expected]

### 7. Validation Strategy (REQUIRED)
Specify:
- **Unit tests**: What to test for each new component
- **Smoke test**: 100-episode initial validation criteria
- **Success metrics**: What metrics prove it's working
- **Failure indicators**: Red flags that design isn't working

### 8. Contingency Plans (REQUIRED)
If new design fails, what to try next:
- If survival rate < 50%: [specific backup plan]
- If not learning: [specific backup plan]
- If still going bankrupt: [specific backup plan]

## Output Requirements

### ✅ MUST PROVIDE (Non-negotiable)
- Exact numerical values for all weights (not ranges, not "moderate increase")
- Concrete pseudocode for new components (not conceptual descriptions)
- Specific formulas for risk calculations
- Measurable success criteria
- Implementation order with dependencies

### ❌ AVOID (These are not helpful)
- Vague recommendations ("adjust as needed", "tune during training")
- Relative changes without specifics ("increase slightly", "reduce a bit")
- Generic advice ("improve risk management", "optimize patterns")
- Ungrounded suggestions (must reference statistics or game mechanics)
- Theory without implementation (must provide code/formulas)

## Key Numbers to Reference

**Statistical Findings** (use these to justify weights):
- Volatility prediction: 94.7% accuracy, 664.7% mean spike, p < 0.001
- Post-Max-Payout pattern: +31.9% win rate, p = 0.0038 (very strong)
- Ultra-Short pattern: +24.4% win rate, p = 0.0092 (strong)
- Moonshot pattern: +18.7% win rate, p = 0.0156 (moderate)

**Current Failure Metrics** (problem to solve):
- Bankruptcy rate: 94.6% (151/160 episodes)
- Survival rate: 5.4% (9/160 episodes)
- Average games per episode: 2.3 (of 15 possible)

**Current Weights** (baseline to improve):
```yaml
pnl_weight: 1.0              # TOO HIGH - dominates
pattern_bonus_weight: 0.4    # TOO LOW - underweights p=0.0038 signal
risk_management_weight: 0.2  # WAY TOO LOW - causes bankruptcy
volatility_weight: 0.2       # TOO LOW - underweights 94.7% accuracy
```

**Success Targets** (design goals):
- Survival rate: >90% (currently 5.4%)
- Win rate: >60% (currently unknown)
- Profit per episode: >0.010 SOL (10% ROI)
- Pattern usage: >80% of entries have pattern signal
- Games per episode: >8 average (of 15 possible)

## Design Principles (Follow These)

1. **Survival First**: Capital preservation > short-term profit
   - Risk management must be multiplicative OR weighted ≥1.0
   - Add explicit survival bonuses for completing games

2. **Edge-Based Entry**: Only trade when statistical advantage exists
   - Heavy penalty for entry without pattern signal (-0.05 or more)
   - Pattern bonuses proportional to p-value strength

3. **Volatility-Informed**: Use 94.7% accurate volatility signals
   - Volatility weight should reflect prediction power (0.8-1.0)
   - Block/penalize trades during high volatility without edge

4. **Pattern-Driven**: Exploit validated statistical patterns
   - Post-Max-Payout (p=0.0038) should have highest weight
   - Pattern bonuses should match or exceed PnL weight

5. **Risk-Adjusted**: Normalize rewards by risk taken
   - Consider Sharpe-style risk adjustment
   - Penalize high-risk actions disproportionately

6. **Long-Term Thinking**: Incentivize episode completion
   - Add milestone bonuses (games 5, 10, 15)
   - Progressive risk reduction as episode continues

7. **Behavioral Shaping**: Explicitly reward desired behaviors
   - Patience reward for WAIT when no edge
   - Setup quality bonus for ideal entry conditions

8. **Statistical Grounding**: All weights justified by data
   - Reference p-values, effect sizes, accuracy metrics
   - No arbitrary "feels right" recommendations

## Quality Standards

Your recommendations will be evaluated on:

**Specificity**: ✅ "pnl_weight: 0.6" vs ❌ "reduce PnL weight somewhat"

**Justification**: ✅ "Pattern weight 0.8 because p=0.0038 has very strong significance" vs ❌ "patterns are important"

**Implementability**: ✅ Pseudocode with formulas vs ❌ Conceptual description

**Completeness**: ✅ All 8 deliverables provided vs ❌ Partial recommendations

**Groundedness**: ✅ References statistics (94.7%, p-values) vs ❌ Generic best practices

## Success Criteria for This Session

You've succeeded if your recommendations:
- [ ] Include exact values for all 13 component weights
- [ ] Add at least 3 new components (patience, survival, setup quality)
- [ ] Specify concrete penalty values and formulas
- [ ] Provide clear implementation priority (Phase 1, 2, 3)
- [ ] Predict specific outcomes (survival %, win %, profit)
- [ ] Reference statistical findings (p-values, accuracy) in justifications
- [ ] Include validation strategy and contingency plans
- [ ] Can be directly translated to code without further clarification

## Additional Context Available

If you need more information, request any of these 17 files from `REWARD_DESIGN_BUNDLE.md`:

**Tier 1 (Critical)**:
- `reward_calculator.py:187-456` - Current implementation
- `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` - Game rules
- `reward_config.yaml` - Current weights

**Tier 2 (Core Context)**:
- `volatility_tracker.py` - How 94.7% accuracy is calculated
- `PATTERN_EXPLOITATION_RESEARCH.md` - Pattern discovery research
- `pattern_detector.py` - Pattern detection implementation
- `environment.py` - Training environment details

**Tier 3 (Supporting)**:
- `sweet_spot_detector.py`, `sidebet_ev_calculator.py`, etc.

**Tier 4 (Reference)**:
- Technical specs, tests, failure analysis

## Final Checklist

Before submitting your final design, verify:
- [ ] All 8 required deliverables provided
- [ ] All weights are exact numerical values (not ranges)
- [ ] All new components have pseudocode/formulas
- [ ] All recommendations reference statistics or game mechanics
- [ ] Implementation is phased (Phase 1, 2, 3)
- [ ] Success metrics are specific and measurable
- [ ] Contingency plans are concrete (not "try different approach")
- [ ] Design would realistically achieve >90% survival based on changes

---

**Ready to begin?** Start by reading `REWARD_DESIGN_PROMPT.md` and `REWARD_DESIGN_KEY_INSIGHTS.md`, then work through `REWARD_DESIGN_QUESTIONS.md` systematically.
