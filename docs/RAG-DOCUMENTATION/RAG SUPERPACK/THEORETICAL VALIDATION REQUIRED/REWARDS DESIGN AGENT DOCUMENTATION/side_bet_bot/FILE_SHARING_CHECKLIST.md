# File Sharing Checklist: Reward Design Session Guide

**Purpose**: Step-by-step guide for conducting reward function design session with external LLM

**Last Updated**: November 7, 2025

---

## 📋 Pre-Session Checklist

### ✅ Files Prepared (5 core documents)
- [ ] `REWARD_DESIGN_PROMPT.md` - Master prompt with full context
- [ ] `REWARD_DESIGN_BUNDLE.md` - File reference guide
- [ ] `REWARD_DESIGN_KEY_INSIGHTS.md` - Critical findings summary
- [ ] `REWARD_DESIGN_QUESTIONS.md` - Structured questionnaire
- [ ] `FILE_SHARING_CHECKLIST.md` - This guide

### ✅ Supporting Files Available (17 reference files)
See `REWARD_DESIGN_BUNDLE.md` for complete list and priorities

### ✅ Session Goals Defined
- [ ] Primary goal: Redesign reward function to prevent bankruptcy
- [ ] Secondary goals: Optimize pattern exploitation, improve win rate
- [ ] Success criteria: >90% survival, >60% win rate, >0.010 SOL profit

---

## 🚀 Session Flow: Recommended Approach

### **Phase 1: Initial Context (15-20 minutes)**

**Step 1: Start with Master Prompt**
- Share: `REWARD_DESIGN_PROMPT.md`
- Why: Establishes complete context in single message
- Expected response: LLM confirms understanding, asks clarifying questions

**Step 2: Provide Key Insights**
- Share: `REWARD_DESIGN_KEY_INSIGHTS.md`
- Why: Ensures LLM has distilled critical findings
- Expected response: LLM identifies priority areas (likely risk management, pattern bonuses)

**Step 3: Present Questionnaire**
- Share: `REWARD_DESIGN_QUESTIONS.md`
- Why: Structures the design conversation systematically
- Expected response: LLM begins working through questions or asks for supporting files

### **Phase 2: Deep Dive (30-60 minutes)**

**Step 4: Share Tier 1 Critical Files (as requested)**
When LLM asks for implementation details or game mechanics:

**4A. Current Reward Implementation**
- File: `rugs_bot/training/reward_calculator.py`
- Lines: 187-456 (RewardCalculator class)
- Why: Shows exact current implementation
- How: Share code block or entire file

**4B. Game Mechanics Knowledge Base**
- File: `docs/game_mechanics/RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md`
- Why: Comprehensive game rules and constraints
- How: Share full document (it's already written for external consumption)

**4C. Current Configuration**
- File: `rugs_bot/training/reward_config.yaml`
- Why: Shows current weights and thresholds
- How: Share full YAML file

### **Phase 3: Analysis and Recommendations (45-90 minutes)**

**Step 5: Work Through Questionnaire**
Let LLM systematically answer each section of `REWARD_DESIGN_QUESTIONS.md`:
- Section 1: Component weights
- Section 2: Missing components
- Section 3: Penalty structure
- ... (all 11 sections)

**Step 6: Share Supporting Files (as needed)**
When LLM requests specific context:

**For statistical validation:**
- `docs/research/PATTERN_EXPLOITATION_RESEARCH.md`
- `docs/research/VOLATILITY_ANALYSIS_FINDINGS.md`

**For implementation details:**
- `rugs_bot/analysis/pattern_detector.py`
- `rugs_bot/analysis/volatility_tracker.py`

**For failure analysis:**
- `docs/training/PHASE_1_TRAINING_FAILURE_ANALYSIS.md`

**Step 7: Iterative Refinement**
- LLM proposes reward function design
- You ask clarifying questions
- LLM refines based on feedback
- Repeat until consensus

### **Phase 4: Deliverables (30-45 minutes)**

**Step 8: Request Final Design**
Ask LLM to provide:
1. Complete reward function pseudocode
2. Specific weight recommendations
3. Implementation priorities
4. Expected outcomes and validation criteria
5. Contingency plans if design fails

**Step 9: Implementation Guidance**
Ask LLM to outline:
- Phased rollout strategy
- Testing approach
- Metrics to monitor
- Red flags to watch for

---

## 💬 Conversation Templates

### Opening Message (Copy/Paste Template)

```
I need your help redesigning a reward function for a reinforcement learning trading bot that's currently experiencing a 94.6% bankruptcy rate.

I'm going to share several documents with you:

1. First, the master prompt with complete context (REWARD_DESIGN_PROMPT.md)
2. Then, a summary of key insights (REWARD_DESIGN_KEY_INSIGHTS.md)
3. Finally, a structured questionnaire to guide our design (REWARD_DESIGN_QUESTIONS.md)

Additional reference files are available if you need them - just ask.

**Primary Goal**: Redesign the reward function to achieve >90% survival rate while maintaining >60% win rate and >0.010 SOL profit per episode.

**Key Constraints**:
- Training uses actual game engine (REPLAYER) - no simulation
- Multi-game episodes (15 consecutive games)
- Instant liquidation on rug (no gradual stops)
- Strong statistical signals available (94.7% volatility accuracy, validated patterns)

Ready to begin?

[Paste REWARD_DESIGN_PROMPT.md content here]
```

### Follow-up Message Template

```
Here are the key insights distilled from our research:

[Paste REWARD_DESIGN_KEY_INSIGHTS.md content here]

And here's the structured questionnaire to guide our design:

[Paste REWARD_DESIGN_QUESTIONS.md content here]

Please work through the questionnaire systematically. Feel free to request any of the 17 reference files listed in the master prompt if you need more context.
```

### File Request Template

```
You asked for [filename]. Here it is:

[Paste file content]

This file shows [brief explanation of what it contains and why it's relevant].
```

---

## 📁 File Sharing Order (Recommended)

### Tier 1: Always Share First (Core Context)
Share these in your opening messages:
1. `REWARD_DESIGN_PROMPT.md` - Master context
2. `REWARD_DESIGN_KEY_INSIGHTS.md` - Critical findings
3. `REWARD_DESIGN_QUESTIONS.md` - Structured questions

### Tier 2: Share When Requested (Implementation)
Share these when LLM asks for implementation details:
4. `rugs_bot/training/reward_calculator.py:187-456` - Current implementation
5. `rugs_bot/training/reward_config.yaml` - Current weights
6. `docs/game_mechanics/RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` - Game rules

### Tier 3: Share If Needed (Research)
Share these if LLM asks for statistical validation:
7. `docs/research/PATTERN_EXPLOITATION_RESEARCH.md`
8. `docs/research/VOLATILITY_ANALYSIS_FINDINGS.md`
9. `rugs_bot/analysis/pattern_detector.py`
10. `rugs_bot/analysis/volatility_tracker.py`

### Tier 4: Share On Demand (Supporting)
Share these only if specifically requested:
11. `rugs_bot/environment/replayer_gym_env.py` - Environment wrapper
12. `docs/training/PHASE_1_TRAINING_FAILURE_ANALYSIS.md` - Failure analysis
13. Other files from REWARD_DESIGN_BUNDLE.md

---

## 🎯 Expected Outputs

### What You Should Receive

**1. Revised Weight Recommendations**
```yaml
# Expected format
pnl_weight: [specific value with rationale]
pattern_bonus_weight: [specific value with rationale]
risk_management_weight: [specific value with rationale]
# ... etc for all 13 components
```

**2. New Components to Add**
```python
# Expected format
class PatienceReward:
    """[Description of new component]"""
    weight = [recommended value]

    def calculate(self, state, action, info):
        # [Pseudocode or actual implementation]
        return reward
```

**3. Penalty Structure Updates**
- Entry without edge penalty: [value and logic]
- Over-trading penalty: [value and logic]
- Risk exposure penalty: [value and logic]

**4. Implementation Strategy**
- Phase 1: [specific changes]
- Phase 2: [specific changes]
- Phase 3: [specific changes]
- Testing approach: [specific tests]

**5. Success Metrics Validation**
- Expected survival rate: [X]%
- Expected win rate: [Y]%
- Expected profit: [Z] SOL/episode
- Time to convergence: [N] episodes

**6. Contingency Plans**
- If survival still low: [backup plan]
- If not learning: [backup plan]
- If overfitting: [backup plan]

---

## ✅ Validation Checklist

### After Receiving Recommendations

**Sanity Check Questions:**
- [ ] Do recommended weights sum to reasonable total? (Not all 1.0+)
- [ ] Are risk components weighted heavily enough to prevent bankruptcy?
- [ ] Are pattern bonuses proportional to statistical significance?
- [ ] Are all 8 design questions (Q1-Q8) addressed?
- [ ] Is implementation strategy phased and testable?
- [ ] Are success metrics specific and measurable?

**Red Flags to Watch For:**
- ❌ PnL weight still dominates (>0.7) without risk normalization
- ❌ Risk management weight still low (<0.5)
- ❌ No explicit patience or survival components
- ❌ Pattern bonuses don't reflect p-value strength
- ❌ No contingency plans for failure scenarios
- ❌ Vague recommendations ("increase slightly", "adjust as needed")

**Green Flags to Look For:**
- ✅ Specific numerical recommendations with rationale
- ✅ Risk management is multiplicative or heavily weighted
- ✅ New components added (patience, survival, setup quality)
- ✅ Pattern weights proportional to statistical evidence
- ✅ Phased implementation with testing at each stage
- ✅ Clear success criteria and validation approach

---

## 🔄 Iteration Strategy

### If First Design Isn't Satisfactory

**Round 2: Clarify Constraints**
Share additional context:
- Game phase dynamics
- Episode progression effects
- Balance-dependent risk scaling

Ask LLM to reconsider specific sections:
- "Can you revisit Section 6 (Risk Management) with these constraints?"
- "How would you adjust pattern bonuses given X?"

**Round 3: Challenge Assumptions**
Play devil's advocate:
- "What if this approach leads to excessive WAIT actions?"
- "How does this prevent [specific failure mode]?"
- "What's the worst-case outcome with these weights?"

**Round 4: Request Alternatives**
Ask for multiple options:
- "Provide 3 different approaches: conservative, balanced, aggressive"
- "Compare additive vs multiplicative risk management"
- "Show trade-offs between survival and profit optimization"

---

## 📊 Post-Session Checklist

### After Design Session Complete

**Documentation:**
- [ ] Save complete LLM conversation transcript
- [ ] Extract key recommendations to new file: `REWARD_REDESIGN_RECOMMENDATIONS.md`
- [ ] Create implementation task list from phased approach
- [ ] Update reward_config.yaml with new weights (don't deploy yet!)

**Validation:**
- [ ] Review recommendations with original project context
- [ ] Identify any contradictions or gaps
- [ ] Prepare test cases for new components
- [ ] Create rollback plan if design fails

**Implementation Prep:**
- [ ] Create feature branch: `reward-redesign-v2`
- [ ] Write unit tests for new components
- [ ] Update RewardCalculator class incrementally
- [ ] Prepare 100-episode smoke test

**Follow-up Questions:**
Document any unresolved questions:
- [ ] Edge cases not covered
- [ ] Hyperparameters needing tuning
- [ ] Alternative approaches to explore
- [ ] Research gaps to fill

---

## 🎓 Tips for Effective Session

### Maximizing LLM Performance

**1. Be Specific in Questions**
- ❌ "What do you think about the weights?"
- ✅ "Given 94.7% volatility accuracy (p<0.001), should volatility_weight increase from 0.2 to 0.8-1.0, or be made multiplicative?"

**2. Provide Numerical Context**
- ❌ "The bot goes bankrupt a lot"
- ✅ "94.6% bankruptcy rate (151/160 episodes), 5.4% survival rate"

**3. Request Concrete Outputs**
- ❌ "How should we improve risk management?"
- ✅ "Provide exact weight value for risk_management_weight and pseudocode for calculation"

**4. Challenge Vague Answers**
If LLM says "increase moderately":
- ❌ Accept and move on
- ✅ "Please specify exact numerical value (e.g., 0.6, 0.8, 1.0) with rationale"

**5. Ask for Trade-offs**
- "If we increase pattern bonuses to 1.0, what should we decrease?"
- "What's the cost of prioritizing survival over profit?"
- "Which components can we remove if 13 is too many?"

**6. Request Validation Logic**
- "How would we test if this component is working?"
- "What metric would prove this change was successful?"
- "What would failure look like?"

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**Issue 1: LLM Overwhelmed by Context**
- Solution: Start with just master prompt, add files incrementally
- Alternative: Use REWARD_DESIGN_KEY_INSIGHTS.md as primary context

**Issue 2: LLM Gives Generic Advice**
- Solution: Point to specific numbers ("p=0.0038", "94.6% bankruptcy")
- Alternative: Ask "How does your recommendation address this specific failure?"

**Issue 3: LLM Doesn't Understand Game Mechanics**
- Solution: Share RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md immediately
- Alternative: Explain instant liquidation constraint explicitly

**Issue 4: Recommendations Contradict Each Other**
- Solution: Point out contradiction, ask for resolution
- Alternative: Request priority ranking of conflicting recommendations

**Issue 5: LLM Suggests Infeasible Implementation**
- Solution: Share actual code (reward_calculator.py), show constraints
- Alternative: Ask "How would this work given [specific technical constraint]?"

---

## 📞 Quick Reference

### Essential Files (Must Share)
1. REWARD_DESIGN_PROMPT.md
2. REWARD_DESIGN_KEY_INSIGHTS.md
3. REWARD_DESIGN_QUESTIONS.md

### Critical Numbers to Emphasize
- 94.6% bankruptcy rate
- 94.7% volatility accuracy
- Pattern p-values: 0.0038, 0.0092, 0.0156
- Target: >90% survival, >60% win rate

### Key Questions to Answer
1. How to prevent bankruptcy?
2. How to weight pattern bonuses?
3. Should risk be multiplicative or additive?
4. Should we add patience/survival components?
5. What's the implementation priority?

### Success Indicators
- ✅ Specific numerical recommendations
- ✅ Clear rationale tied to statistics
- ✅ Phased implementation plan
- ✅ Testable predictions
- ✅ Contingency plans

---

## 🎯 Final Pre-Session Check

**Before starting session, confirm:**
- [ ] You understand the bankruptcy problem (94.6% rate)
- [ ] You know the statistical findings (volatility, patterns)
- [ ] You have all 5 core documents ready
- [ ] You have supporting files accessible
- [ ] You have 2-3 hours for thorough session
- [ ] You're prepared to iterate if needed
- [ ] You have validation checklist ready

**Ready to proceed!** 🚀

---

**Status**: This checklist provides complete guidance for conducting effective reward design session with external LLM. Follow the recommended flow for best results.
