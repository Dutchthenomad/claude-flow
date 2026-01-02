# Trading Bot RL Rewards Design - File Sharing Checklist

**Purpose**: Step-by-step guide for conducting the LLM rewards design session
**Target LLM**: Claude Sonnet 4.5 or equivalent
**Session Duration**: 3-5 hours (can be split across multiple sessions)
**Expected Outcome**: Comprehensive reward function redesign with 8 specific deliverables

---

## Pre-Session Checklist

### ✅ Files to Prepare

**Core Bundle** (share immediately):
- [ ] `LLM_INSTRUCTIONS.md` - Role definition & deliverables
- [ ] `REWARD_DESIGN_PROMPT.md` - Complete context document
- [ ] `KEY_INSIGHTS.md` - Executive summary
- [ ] `QUESTIONS.md` - Structured questionnaire

**Supporting Files** (share on request):
- [ ] `BUNDLE.md` - File reference guide
- [ ] Current reward calculator code
- [ ] Environment observation space documentation
- [ ] Sidebet model success report (v3, 38% win rate)
- [ ] Game mechanics specifications
- [ ] Statistical analysis documents

**Optional Reference** (have ready):
- [ ] Pattern analysis research
- [ ] Volatility tracker documentation
- [ ] Sweet spot detector documentation
- [ ] Previous training failure analysis

---

## Session Flow (4 Phases)

### Phase 1: Context Loading (15-20 minutes)

**Goal**: Load LLM with essential context

**Steps**:
1. **Open with role assignment**
   Copy-paste from `LLM_INSTRUCTIONS.md` (first 50 lines)

2. **Share core bundle** in this order:
   - `REWARD_DESIGN_PROMPT.md` (complete context)
   - `KEY_INSIGHTS.md` (distilled findings)
   - `QUESTIONS.md` (structured exploration framework)

3. **Confirm understanding**
   Ask: "Do you understand the problem, objectives, and your role?"

4. **Check for immediate questions**
   LLM may request clarifications or specific files

**Success Indicators** (green flags):
- ✅ LLM summarizes the critical problem accurately
- ✅ LLM identifies the key constraint (sidebet model = primary exit signal)
- ✅ LLM asks for specific files/data (shows engagement)
- ✅ LLM proposes initial approach (shows understanding)

**Red Flags** (warning signs):
- ❌ LLM gives generic advice (not specific to Rugs.fun)
- ❌ LLM doesn't acknowledge the 79-feature observation space
- ❌ LLM ignores the sidebet model (38% win rate opportunity)
- ❌ LLM proposes solutions without asking for data

**Template Message**:
```
I need you to redesign the reward function for an RL trading bot that plays Rugs.fun.

The critical problem: [INSERT QUANTIFIED METRIC - e.g., "30% win rate, high bankruptcy"]

I'm providing 3 documents to start:
1. REWARD_DESIGN_PROMPT.md - Complete context
2. KEY_INSIGHTS.md - Key findings and constraints
3. QUESTIONS.md - Design questions to explore

Please read all three, then confirm your understanding of:
- The critical problem
- The opportunity (sidebet model with 38% win rate)
- Your role (redesign rewards to leverage this signal)
- Expected deliverables (8 specific outputs)

[Paste files here]
```

---

### Phase 2: Deep Dive (30-60 minutes)

**Goal**: LLM requests specific files and explores implementation details

**Expected Behavior**:
- LLM asks for Tier 1 files (implementation code)
- LLM explores current reward calculator
- LLM examines observation space structure (79 features)
- LLM reviews sidebet model capabilities

**Steps**:
1. **Wait for file requests**
   LLM should ask for specific files from `BUNDLE.md`

2. **Share Tier 1 files** (implementation details):
   - Reward calculator code (`reward_calculator.py`)
   - Environment observation space (`environment.py` relevant sections)
   - Sidebet model documentation (v3 success report)
   - Current reward config (YAML if exists)

3. **Answer clarifying questions**
   - How are observations structured?
   - What are action constraints?
   - How does sidebet model output look?
   - What are current reward component weights?

4. **Share Tier 2 files** if requested:
   - Pattern detector documentation
   - Volatility tracker implementation
   - Sweet spot detector logic
   - Game mechanics deep dive

**Success Indicators**:
- ✅ LLM asks about specific observation features (which of the 79 to use?)
- ✅ LLM inquires about sidebet prediction format (5 features)
- ✅ LLM explores current reward weights (wants to see baseline)
- ✅ LLM asks about constraints (what can/cannot change?)

**Red Flags**:
- ❌ LLM doesn't ask for implementation files
- ❌ LLM proposes rewards without seeing current structure
- ❌ LLM ignores available observations (doesn't ask what's available)
- ❌ LLM makes assumptions without verification

**Template Response**:
```
Great question! Here's the [requested file]:

[Paste file or relevant sections]

Key sections to note:
- [Line X-Y]: Current reward component
- [Line A-B]: How sidebet predictions are structured
- [Line M-N]: Observation space definition

Let me know if you need clarification on any part.
```

---

### Phase 3: Systematic Analysis (45-90 minutes)

**Goal**: LLM works through QUESTIONS.md systematically, providing specific answers

**Expected Process**:
1. LLM tackles questions section by section
2. For each question, LLM provides:
   - Specific numerical recommendation (weights, thresholds)
   - Justification citing data/statistics
   - Pseudocode or formula
   - Expected impact

**Steps**:
1. **Monitor progress through QUESTIONS.md**
   LLM should work through all 11 sections:
   - Component Weight Rebalancing
   - Sidebet Prediction Integration
   - Exit Signal Hierarchy
   - Position Sizing Optimization
   - Penalty Structure Redesign
   - Risk Management Architecture
   - Temporal Dynamics
   - Implementation Strategy
   - Success Metrics Validation
   - Contingency Planning
   - Final Recommendations

2. **Challenge vague answers**
   If LLM says "increase moderately", push for exact numbers:
   ```
   Can you provide a specific numerical value?
   Current weight is 1.0, what should it be? (e.g., 2.5, 5.0, 10.0?)
   ```

3. **Request statistical justification**
   If LLM proposes a change, ask:
   ```
   What data supports this recommendation?
   Can you cite the specific finding from KEY_INSIGHTS.md?
   ```

4. **Share Tier 3 files** if LLM requests deeper analysis:
   - Statistical analysis (p-values, effect sizes)
   - Backtest results from previous training
   - Failure analysis documentation
   - Pattern validation research

**Success Indicators**:
- ✅ LLM provides exact numerical values (not ranges)
- ✅ LLM cites specific statistics (p-values, win rates)
- ✅ LLM provides pseudocode for new components
- ✅ LLM explores trade-offs (acknowledges costs of decisions)
- ✅ LLM asks clarifying questions when stuck

**Red Flags**:
- ❌ Answers like "increase significantly" (not specific)
- ❌ Recommendations without justification (no data cited)
- ❌ Generic advice (applies to any RL problem)
- ❌ Ignoring constraints (proposes infeasible changes)
- ❌ Skipping sections (incomplete analysis)

**Template Challenge**:
```
Thanks for the analysis. Can you be more specific?

Instead of "increase the exit penalty significantly", can you provide:
1. Exact penalty value (e.g., -50.0, -100.0, -200.0?)
2. What threshold triggers it? (rug_prob >= 0.50? 0.40?)
3. Why this specific value? (cite data if possible)
4. What's the expected impact? (% improvement in rug avoidance?)
```

---

### Phase 4: Deliverables (30-45 minutes)

**Goal**: Receive 8 specific, implementable outputs

**Required Deliverables**:

1. **Component Weight Recommendations**
   Format: Table with current → proposed weights + justification
   ```
   | Component | Current | Proposed | Justification |
   |-----------|---------|----------|---------------|
   | pnl_reward | 1.0 | 0.5 | Reduce financial focus... |
   | rug_avoidance | 0.0 | 10.0 | NEW: Primary objective... |
   ```

2. **New Reward Components**
   Format: Component name, formula, weight, when to apply
   ```python
   def rug_avoidance_reward(state, action, next_state):
       """Reward for exiting before rug"""
       if exited_before_rug(state, next_state):
           rug_prob = state['rug_prediction'][0]
           if rug_prob >= 0.50:
               return 50.0  # Emergency exit bonus
           elif rug_prob >= 0.40:
               return 30.0  # Proactive exit bonus
       return 0.0
   ```

3. **Penalty Structure**
   Format: List of penalties with exact values and triggers
   ```
   - Hold through critical signal: -100.0 (rug_prob >= 0.50, has_positions)
   - Early exit during sweet spot: -10.0 (in_sweet_spot, rug_prob < 0.20)
   - Bankruptcy: -1000.0 (bankroll <= threshold)
   ```

4. **Sidebet Integration Strategy**
   Format: How to use the 5 rug prediction features in rewards
   ```
   Features available:
   - probability (0-1): Use as signal strength multiplier
   - confidence (0-1): Use as reliability weight
   - ticks_to_rug_norm (0-1): Use for urgency scaling
   - is_critical (0/1): Use as emergency trigger
   - should_exit (0/1): Use as action validator

   Proposed usage:
   - Exit rewards scaled by confidence
   - Penalties scaled by probability
   - Emergency bonuses triggered by is_critical
   ```

5. **Implementation Roadmap**
   Format: Phased rollout plan (Phase 1, 2, 3)
   ```
   Phase 1 (Week 1): Core changes
   - Update component weights
   - Add rug avoidance rewards
   - Implement critical penalties

   Phase 2 (Week 2): Fine-tuning
   - Add position sizing rewards
   - Implement early exit penalties
   - Tune thresholds

   Phase 3 (Week 3): Validation
   - Backtest on 100 episodes
   - Monitor rug avoidance rate
   - Adjust if needed
   ```

6. **Success Metrics**
   Format: Primary/secondary/tertiary targets
   ```
   Primary (must achieve):
   - Rug avoidance: >90% (currently ~30%)
   - Win rate: >60% (currently ~30%)
   - Bankruptcy: <5% (currently ~20%)

   Secondary (highly desired):
   - ROI: >200% (currently variable)
   - Sharpe ratio: >1.5 (currently <1.0)

   Tertiary (nice to have):
   - Max drawdown: <20% (currently ~50%)
   - Avg position hold: 40-80 ticks (sweet spot)
   ```

7. **YAML Configuration**
   Format: Complete config file ready to use
   ```yaml
   # Reward Configuration - Sidebet-Enhanced Trading
   version: "2.0"

   components:
     rug_avoidance:
       weight: 10.0
       emergency_exit_bonus: 50.0
       proactive_exit_bonus: 30.0
       hold_through_critical_penalty: -100.0

     # ... (complete config)
   ```

8. **Validation Checklist**
   Format: How to verify the design works
   ```
   Before deployment:
   - [ ] Reward function compiles without errors
   - [ ] All weights are positive for bonuses, negative for penalties
   - [ ] Rug avoidance rewards are highest weight (>5.0)
   - [ ] YAML config matches code implementation

   After 100 training episodes:
   - [ ] Rug avoidance rate >70% (intermediate milestone)
   - [ ] Agent is exiting on critical signals (rug_prob >= 0.50)
   - [ ] Bankruptcy rate declining (<15%)

   After 1000 training episodes:
   - [ ] Rug avoidance rate >90% (target)
   - [ ] Win rate >60% (target)
   - [ ] Bankroll growing consistently
   ```

**Quality Checklist**:
- [ ] All 8 deliverables received
- [ ] Numerical values are specific (not ranges)
- [ ] Justifications cite data/statistics
- [ ] Pseudocode/formulas provided where needed
- [ ] YAML config is complete and valid
- [ ] Success metrics are quantified
- [ ] Implementation roadmap has timeline
- [ ] Validation checklist is actionable

**Template Request**:
```
Excellent analysis! Now please provide the 8 required deliverables:

1. Component Weight Recommendations (table format)
2. New Reward Components (with pseudocode)
3. Penalty Structure (exact values)
4. Sidebet Integration Strategy (how to use 5 features)
5. Implementation Roadmap (phased plan)
6. Success Metrics (primary/secondary/tertiary)
7. YAML Configuration (complete file)
8. Validation Checklist (before/after deployment)

Please be specific with numerical values and include code examples where applicable.
```

---

## Post-Session Validation

### Green Flags (Design is good):
- ✅ Rug avoidance is highest weighted component (>5.0x others)
- ✅ Sidebet predictions are used in multiple reward components
- ✅ Penalties are severe for ignoring critical signals (-50 to -100)
- ✅ Early exit penalties prevent overfitting (balance needed)
- ✅ Success metrics are ambitious but achievable (>90% rug avoidance)
- ✅ Implementation is phased (not all-at-once)
- ✅ Validation metrics are concrete and measurable

### Red Flags (Design needs iteration):
- ❌ Rug avoidance weight is <2.0 (too low priority)
- ❌ Sidebet predictions are ignored or underutilized
- ❌ Penalties are weak (<-10 for critical mistakes)
- ❌ No early exit penalties (risk of "always exit immediately")
- ❌ Success metrics are vague ("improve performance")
- ❌ Implementation lacks phases (big-bang approach)
- ❌ No validation plan (can't verify if working)

### If Design Has Red Flags:

**Iteration Strategy**:
1. **Identify the gap**
   Which deliverable(s) have issues?

2. **Challenge the assumption**
   ```
   I notice the rug avoidance weight is only 2.0. Given that:
   - Sidebet model has 38% win rate
   - Rug avoidance is our #1 objective
   - Current bankruptcy is 20%

   Shouldn't this be significantly higher? (e.g., 10.0+)
   What's your reasoning for 2.0?
   ```

3. **Request revision**
   Ask for specific deliverables to be redone

4. **Provide additional data**
   Share Tier 3-4 files if LLM needs more context

5. **Iterate**
   Repeat Phase 3-4 until green flags achieved

**Alternative Approach** (if stuck after 2 iterations):
1. Take a break (end session, return fresh)
2. Try different LLM model (GPT-4, Claude Opus)
3. Simplify scope (focus on top 3 components only)
4. Consult human expert (domain knowledge needed)

---

## Success Criteria

**Session is successful when**:
- ✅ All 8 deliverables received
- ✅ All green flags present, no red flags
- ✅ Design is specific and implementable
- ✅ Expected impact is quantified (90% rug avoidance, 60% win rate)
- ✅ You feel confident deploying this design

**Session needs iteration when**:
- ⚠️ Some deliverables missing or vague
- ⚠️ Mix of green and red flags
- ⚠️ Design is generic (not specific to Rugs.fun + sidebet model)
- ⚠️ You have doubts about feasibility

**Session has failed when**:
- ❌ Multiple red flags persist after 2 iterations
- ❌ LLM cannot provide specific values
- ❌ Design ignores key constraints (sidebet model, game mechanics)
- ❌ No clear path to 90% rug avoidance

---

## Troubleshooting

### Problem: LLM gives vague answers
**Solution**: Use template challenges (see Phase 3)

### Problem: LLM doesn't use sidebet predictions
**Solution**: Explicitly ask how each of the 5 features is used

### Problem: LLM proposes unrealistic goals
**Solution**: Ground with current baseline metrics

### Problem: LLM copies generic RL advice
**Solution**: Require citations to provided documents

### Problem: Session is taking too long (>5 hours)
**Solution**: Split across multiple sessions, save progress

---

## Time Estimates

**Fast Track** (experienced user, clear problem):
- Phase 1: 15 min
- Phase 2: 30 min
- Phase 3: 45 min
- Phase 4: 30 min
- **Total: 2 hours**

**Standard Track** (first time, complex problem):
- Phase 1: 20 min
- Phase 2: 60 min
- Phase 3: 90 min
- Phase 4: 45 min
- **Total: 3.5 hours**

**Deep Dive** (multiple iterations, research needed):
- Phase 1: 30 min
- Phase 2: 90 min
- Phase 3: 120 min
- Phase 4: 60 min
- **Total: 5 hours**

---

## Files to Have Ready

**Critical (T1)**: Share immediately on request
- Current reward calculator implementation
- Environment observation space (79 features)
- Sidebet model v3 success report
- Game mechanics specification

**Important (T2)**: Share if LLM asks
- Pattern detector code and research
- Volatility tracker implementation
- Sweet spot detector logic
- Current training config (PPO params)

**Supporting (T3)**: Share for deeper analysis
- Statistical analysis (p-values, correlations)
- Previous training failure analysis
- Backtest results (baseline performance)
- Market pattern validation

**Reference (T4)**: Share if needed
- Test suite (how components are tested)
- Alternative reward designs (what was tried)
- Research papers (if applicable)
- Edge case handling

---

**This checklist ensures a structured, efficient, and productive LLM session that produces high-quality, implementable reward function designs.**
