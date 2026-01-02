# Trading Bot RL Rewards Design - Supporting File Bundle

**Purpose**: Reference guide for all supporting files that may be needed during rewards design session
**Organization**: Tiered by priority (T1=Critical, T2=Important, T3=Supporting, T4=Reference)
**Usage**: Share files on demand as LLM requests them during design process

---

## How to Use This Bundle

**Tiered Sharing Strategy**:
- **T1 (Critical)**: Share immediately when LLM asks for implementation details
- **T2 (Important)**: Share when LLM needs deeper context on existing systems
- **T3 (Supporting)**: Share when LLM requests statistical validation or historical data
- **T4 (Reference)**: Share only if LLM explicitly needs edge cases or alternative approaches

**File Request Flow**:
1. LLM asks: "Can you show me the current reward calculator implementation?"
2. You check this guide: `reward_calculator.py` is T1-1
3. You share the file with context: "Here's the current reward calculator (T1-1). Key sections to note: lines 45-120 (P&L calculation), lines 150-200 (volatility exit logic)"

---

## Tier 1: Critical Files (Share Immediately on Request)

### T1-1: Current Reward Calculator

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/reward_calculator.py`
**Size**: ~400 lines
**Status**: Needs updating (missing rug avoidance component)

**Purpose**: Calculate rewards for each step in RL training loop

**Key Sections**:
- Lines 1-50: RewardCalculator class definition and initialization
- Lines 50-100: `calculate_pnl_reward()` - Current P&L weighting (weight=1.0)
- Lines 100-150: `calculate_volatility_reward()` - Volatility exit signal (weight=8.0)
- Lines 150-200: `calculate_sweet_spot_reward()` - Entry timing (weight=2.0)
- Lines 200-250: `calculate_pattern_reward()` - Pattern exploitation
- Lines 250-300: `calculate_bankruptcy_penalty()` - Bankruptcy deterrent (-1000)
- Lines 300-350: `calculate_total_reward()` - Aggregates all components
- Lines 350-400: Helper methods and utilities

**What's Missing**:
- ❌ No rug avoidance component
- ❌ No sidebet prediction integration
- ❌ No hold-through critical signal penalty
- ❌ No early exit penalty
- ❌ No confidence scaling
- ❌ No urgency scaling

**When to Share**:
- LLM asks about current reward structure
- LLM wants to see existing component weights
- LLM needs to understand how rewards are calculated

**Relevant Questions**: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1, 3.2

---

### T1-2: Environment Observation Space

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/environment/environment.py`
**Size**: ~800 lines
**Status**: Updated (includes 5 rug prediction features in observation space)

**Purpose**: Define RL environment (Gymnasium interface)

**Key Sections**:
- Lines 1-50: RugsMultiGameEnv class definition
- Lines 50-150: `__init__()` - Environment initialization
- Lines 150-250: `_setup_observation_space()` - 79-feature observation space definition
  - **Lines 180-190**: **NEW** - `rug_prediction` (5 features) from SidebetPredictor
  - Lines 200-210: `current` (10 features) - Price, tick, bankroll
  - Lines 210-230: `history` (20 features) - Price history, volatility
  - Lines 230-250: `positions` (30 features) - Open positions, P&L
  - Lines 250-270: `sidebets` (3 features) - Sidebet state
  - Lines 270-290: `meta_context` (24 features) - Game state, patterns
  - Lines 290-310: `sweet_spot` (3 features) - Entry timing signals
  - Lines 310-330: `duration_pred` (4 features) - Game duration estimates
- Lines 350-450: `step()` - Execute action, calculate reward
- Lines 450-550: `reset()` - Reset environment for new episode
- Lines 550-650: `_get_rug_prediction_features()` - **NEW** - Extract 5 sidebet features
- Lines 650-750: Helper methods for game state management

**79-Feature Breakdown**:
```
Total: 79 features

current (10):
  - current_price_norm, tick_num_norm, bankroll_norm, etc.

history (20):
  - price_history (10 ticks), volatility_history (10 ticks)

positions (30):
  - position_0 through position_9 (each: entry_price, entry_tick, current_pnl)

sidebets (3):
  - active_sidebets, won_sidebets, lost_sidebets

meta_context (24):
  - game_number, games_remaining, avg_game_duration, etc.

sweet_spot (3):
  - in_sweet_spot, time_since_sweet_spot, sweet_spot_quality

duration_pred (4):
  - predicted_duration, duration_confidence, etc.

rug_prediction (5): ✅ NEW
  - probability (0-1)
  - confidence (0-1)
  - ticks_to_rug_normalized (0-1)
  - is_critical (0/1)
  - should_exit (0/1)
```

**When to Share**:
- LLM asks "What observations are available?"
- LLM needs to understand the 79-feature observation space
- LLM wants to know which features can be used in rewards

**Relevant Questions**: 4.1, 4.2, 4.3, 11.3

---

### T1-3: Sidebet Model v3 Success Report

**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/sidebet_training/V3_SUCCESS_REPORT.md`
**Size**: ~500 lines
**Status**: Complete (documents v3 model performance)

**Purpose**: Comprehensive report on sidebet model training and performance

**Key Sections**:
- Lines 1-50: Executive summary (38.1% win rate, 754% ROI)
- Lines 50-100: Model architecture (Gradient Boosting, 14 features)
- Lines 100-200: Performance metrics
  - Win rate: 38.1% (baseline: 16.7%)
  - ROI: 754% on 200-game backtest
  - Martingale strategy: 100% success (never bankrupted)
- Lines 200-300: Feature importance
  - z_score: 63.64% (game duration outlier)
  - spike_spacing: 13.43% (volatility pattern)
  - spike_frequency: 8.40% (spike rate)
  - All others: <5% each
- Lines 300-400: Threshold analysis
  - 0.50: 39.4% win rate ✅ OPTIMAL
  - 0.40: 36.5% win rate (still highly profitable)
  - 0.30: 35.3% win rate
  - 0.10: 33.7% win rate
- Lines 400-500: Backtest results, validation, recommendations

**Key Statistics to Cite**:
- "38.1% win rate is 2.3x better than random (16.7%)"
- "All thresholds ≥0.10 are profitable (EV > 0)"
- "Z-score dominates feature importance (63.64%)"
- "Threshold 0.50 is optimal (39.4% win rate, +0.971 EV)"

**When to Share**:
- LLM asks about sidebet model performance
- LLM needs justification for prioritizing rug avoidance
- LLM wants to understand feature importance

**Relevant Questions**: 2.1, 2.2, 2.3, 2.4, 4.1, 4.3

---

### T1-4: Game Mechanics Specification

**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/GYMNASIUM_DESIGN_SPEC.md`
**Size**: ~800 lines (includes game mechanics + environment design)
**Status**: Complete (comprehensive game mechanics documentation)

**Purpose**: Define immutable game rules and constraints

**Key Sections**:
- Lines 1-50: Overview (15-game episodes, 0.1 SOL start)
- Lines 50-100: Rug mechanics
  - Mean rug time: 329 ticks
  - Std dev: 180 ticks
  - Distribution: Approximately exponential
  - Cannot predict exact tick, only probability
- Lines 100-150: Sweet spot mechanics
  - Optimal range: 2-4x multiplier (40-80 ticks)
  - Entry before 2x: Too early (low profit)
  - Entry after 4x: Too late (high rug risk)
- Lines 150-200: Sidebet mechanics
  - Payout: 5:1 (predict rug within 40 ticks)
  - Breakeven: 16.7% win rate (1/6)
  - Cost: 0.01 SOL per bet
- Lines 200-250: Position mechanics
  - Max 10 simultaneous positions
  - Entry cost: 0.01-0.05 SOL (adjustable)
  - Exit anytime before rug
  - Liquidation: -95% to -99% of position value
- Lines 250-300: Bankruptcy mechanics
  - Threshold: 0.001 SOL
  - Episode terminates if bankroll < threshold
  - Penalty: -1000 reward

**Immutable Constraints**:
1. Sidebet payout: 5:1 (cannot change)
2. Rug timing: Statistical (cannot predict exact tick)
3. Sweet spot: 2-4x (game design)
4. Bankruptcy threshold: 0.001 SOL
5. Position limit: 10 simultaneous

**When to Share**:
- LLM asks about game rules
- LLM needs to understand constraints (what can/cannot change)
- LLM wants to validate reward design against mechanics

**Relevant Questions**: Section 9 (Open Questions), 11.5 (Success Criteria)

---

### T1-5: SidebetPredictor Implementation

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/sidebet/predictor.py`
**Size**: ~365 lines
**Status**: Complete (wrapper class for model)

**Purpose**: Real-time rug probability prediction wrapper

**Key Sections**:
- Lines 1-50: SidebetPredictor class definition
- Lines 50-150: `predict_rug_probability()` - Main prediction method
  - Input: tick_num (int), prices (List[float])
  - Output: Dict with 5 features + metadata
- Lines 150-200: `_calculate_confidence()` - Confidence from feature quality
- Lines 200-250: `_estimate_timing()` - Ticks until rug estimate
- Lines 250-300: `_classify_signal()` - LOW/MEDIUM/HIGH/CRITICAL
- Lines 300-350: `reset_for_new_game()` - Reset state between games
- Lines 350-365: `get_model_info()` - Model metadata

**5-Feature Output**:
```python
{
    'probability': float (0-1),       # Rug likelihood
    'confidence': float (0-1),        # Prediction reliability
    'ticks_to_rug_estimate': int,     # Estimated ticks until rug
    'signal_strength': str,            # 'low'/'medium'/'high'/'critical'
    'recommended_action': str,         # 'hold'/'reduce'/'exit'/'emergency'
    'features': np.ndarray,            # 14-dim feature vector
    'feature_dict': dict               # Named features
}
```

**When to Share**:
- LLM asks how sidebet predictions are generated
- LLM wants to see prediction output structure
- LLM needs to understand the 5 features available

**Relevant Questions**: 4.1, 4.2, 11.3

---

## Tier 2: Important Files (Share When LLM Asks)

### T2-1: Pattern Detector Code

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/environment/pattern_detector.py`
**Size**: ~350 lines
**Status**: Complete (working pattern detection)

**Purpose**: Detect exploitable patterns (ultra-short skip, moonshot)

**Key Patterns**:
1. **Ultra-Short Skip** (73% effectiveness)
   - Detection: Game rugs before 2x multiplier (<40 ticks)
   - Exploitation: Skip entry if rug signals appear before 2x
   - Reward: +15 for correct skip

2. **Moonshot** (60% effectiveness)
   - Detection: Unusually fast price growth (>10x in <100 ticks)
   - Exploitation: Enter early on moonshot pattern
   - Reward: +10 for moonshot entry

3. **Slow Burner** (40% effectiveness)
   - Detection: Gradual price increase (stable volatility)
   - Exploitation: Hold longer in sweet spot
   - Reward: +5 for extended hold

**When to Share**:
- LLM asks about pattern exploitation
- LLM wants to know what patterns are detected
- LLM needs to decide if pattern rewards should change

**Relevant Questions**: 1.4, 4.2

---

### T2-2: Volatility Tracker Implementation

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/environment/volatility_tracker.py`
**Size**: ~250 lines
**Status**: Complete (tracks price volatility)

**Purpose**: Track price volatility as exit signal

**Key Metrics**:
- Current volatility: Std dev of last 10 ticks
- Baseline volatility: Avg volatility over full game
- Volatility ratio: current / baseline
- Spike detection: ratio > 2.0 (threshold)

**Accuracy**:
- ~50% accuracy (detects some rugs, many false positives)
- Less reliable than sidebet model (38% win rate)

**Current Weight**: 8.0 (highest in current system)

**When to Share**:
- LLM asks about volatility exit signal
- LLM wants to understand why volatility weight should decrease
- LLM needs to compare volatility vs sidebet accuracy

**Relevant Questions**: 1.2, 4.2

---

### T2-3: Sweet Spot Detector Logic

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/environment/sweet_spot_detector.py`
**Size**: ~200 lines
**Status**: Complete (working well)

**Purpose**: Detect optimal entry window (2-4x multiplier)

**Key Logic**:
- in_sweet_spot: Current multiplier between 2.0 and 4.0
- time_since_sweet_spot: Ticks since 2x reached
- sweet_spot_quality: Volatility-adjusted entry score

**Performance**:
- Agent learned to enter in sweet spot: 40% win rate (vs 30% overall)
- Average hold: 60 ticks (optimal duration)

**Current Weight**: 2.0 (effective)

**When to Share**:
- LLM asks about sweet spot timing
- LLM wants to know if sweet spot weight should change
- LLM needs to understand entry timing success

**Relevant Questions**: 1.3, 6.2

---

### T2-4: Current Training Configuration

**File**: `/home/nomad/Desktop/rugs-rl-bot/config/training_config.yaml`
**Size**: ~150 lines
**Status**: Complete (PPO hyperparameters)

**Purpose**: PPO algorithm configuration for RL training

**Key Parameters**:
```yaml
ppo:
  learning_rate: 0.0003
  n_steps: 2048
  batch_size: 64
  n_epochs: 10
  gamma: 0.99
  gae_lambda: 0.95
  clip_range: 0.2
  ent_coef: 0.01
  vf_coef: 0.5

environment:
  n_envs: 4  # Parallel environments
  games_per_episode: 15
  starting_bankroll: 0.1  # SOL

reward_weights:  # CURRENT (needs updating)
  pnl_reward: 1.0
  volatility_exit: 8.0
  sweet_spot: 2.0
  patterns: 3.0
  bankruptcy_penalty: 1000.0
  # rug_avoidance: 0.0  # MISSING
```

**When to Share**:
- LLM asks about training setup
- LLM wants to see current reward weights in config
- LLM needs to understand PPO parameters

**Relevant Questions**: 11.6 (YAML Configuration)

---

### T2-5: FeatureExtractor Implementation

**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/sidebet/feature_extractor.py`
**Size**: ~450 lines
**Status**: Complete (extracts 14 features for sidebet model)

**Purpose**: Extract 14 features from game state for rug prediction

**14 Features**:
1. z_score (63.64% importance) - Game duration outlier
2. spike_spacing (13.43%) - Time between volatility spikes
3. spike_frequency (8.40%) - Spike rate
4. volatility_ratio (4.23%) - Current vs baseline volatility
5. price_acceleration (3.12%) - Rate of price change
6. spike_intensity (2.45%) - Magnitude of volatility spikes
7. duration_percentile (1.89%) - Duration vs historical games
8. baseline_volatility (1.23%) - Average volatility
9. current_volatility (0.98%) - Recent volatility
10. price_trend (0.78%) - Upward/downward momentum
11. spike_trend (0.65%) - Spike rate increasing/decreasing
12. recent_spike_count (0.52%) - Spikes in last 20 ticks
13. time_since_last_spike (0.43%) - Recency of last spike
14. spike_clustering (0.29%) - Spike clustering coefficient

**When to Share**:
- LLM asks about feature engineering
- LLM wants to understand z_score dominance (63.64%)
- LLM needs to see how features are calculated

**Relevant Questions**: 6.1 (Time-Based Scaling), 9.1 (Feature Importance)

---

## Tier 3: Supporting Files (Share for Deeper Analysis)

### T3-1: Statistical Analysis

**File**: `/home/nomad/Desktop/rugs-rl-bot/analysis/statistical_validation.md`
**Size**: ~400 lines
**Status**: Complete (p-values, effect sizes, correlations)

**Purpose**: Statistical validation of findings from KEY_INSIGHTS.md

**Key Statistics**:
- **Finding 1**: Sidebet vs Volatility (p < 0.001, Cohen's d = 0.85)
  - Sidebet 38% win rate significantly better than volatility 50% accuracy

- **Finding 2**: All thresholds profitable (p < 0.05 for all)
  - Even 0.10 threshold: p = 0.031, EV = +0.684

- **Finding 4**: Z-score dominance (p < 0.0001, importance = 63.64%)
  - Permutation importance test: z_score drop causes 41% accuracy loss

- **Finding 5**: Sweet spot effectiveness (p < 0.01, 40% vs 30% win rate)
  - t-test: t(998) = 3.45, p = 0.0006

**When to Share**:
- LLM requests statistical validation
- LLM wants to cite p-values in justifications
- LLM needs to verify claims from KEY_INSIGHTS.md

**Relevant Questions**: Any question asking for "data supporting this recommendation"

---

### T3-2: Previous Training Failure Analysis

**File**: `/home/nomad/Desktop/rugs-rl-bot/analysis/training_failure_report.md`
**Size**: ~350 lines
**Status**: Complete (why previous training failed)

**Purpose**: Document what didn't work in previous attempts

**Failed Approaches**:
1. **High P&L Weight (1.5)**: Agent held too long, 70% rug liquidation rate
2. **Low Bankruptcy Penalty (-100)**: Agent went bankrupt 35% of episodes
3. **No Exit Rewards**: Agent never learned to exit proactively
4. **Pattern-Only Strategy**: 40% win rate but inconsistent (high variance)
5. **Volatility-Only Exit**: 50% false positive rate, premature exits

**Key Lessons**:
- P&L maximization conflicts with rug avoidance
- Explicit exit rewards are necessary (agent won't learn from implicit signals)
- Penalties must be severe (-1000 for bankruptcy works, -100 doesn't)
- Multi-component rewards needed (no single signal sufficient)

**When to Share**:
- LLM asks "what was tried before?"
- LLM wants to avoid previous mistakes
- LLM needs historical context on failed approaches

**Relevant Questions**: 3.3 (Bankruptcy Penalty), 7.4 (Rollback Strategy)

---

### T3-3: Backtest Results (Baseline Performance)

**File**: `/home/nomad/Desktop/rugs-rl-bot/backtests/baseline_performance.csv`
**Size**: 1000 rows (1000 episodes)
**Status**: Complete (quantified baseline)

**Purpose**: Quantified baseline performance metrics

**Aggregate Statistics**:
```
Win Rate: 30.2% (302 / 1000 episodes)
Rug Avoidance: 29.8% (298 / 1000 positions exited before rug)
Bankruptcy Rate: 19.7% (197 / 1000 episodes)
Avg ROI: +12.3% (variable: -50% to +100%)
Avg Bankroll End: 0.112 SOL (start: 0.1 SOL)
Sharpe Ratio: 0.87 (target: >1.5)
Max Drawdown: 52.3% (target: <20%)
```

**Episode-Level Data**:
- episode_id, games_played, final_bankroll, win_rate, rug_avoidance_rate, bankruptcy

**Position-Level Data**:
- entry_tick, exit_tick, rug_tick, pnl, rug_avoided (boolean)

**When to Share**:
- LLM asks about current performance
- LLM wants to quantify the gap between current and target
- LLM needs baseline for comparison

**Relevant Questions**: 8.1 (Intermediate Milestones), 11.5 (Success Criteria)

---

### T3-4: Market Pattern Validation

**File**: `/home/nomad/Desktop/rugs-rl-bot/analysis/pattern_validation.md`
**Size**: ~300 lines
**Status**: Complete (validates pattern profitability)

**Purpose**: Validate that detected patterns are truly exploitable

**Pattern Performance**:
1. **Ultra-Short Skip**: 73% effectiveness (p = 0.002)
   - 45 occurrences in 1000 games
   - Correct skip: 33 / 45 (73%)
   - Avoided rug losses: avg +0.015 SOL per skip

2. **Moonshot**: 60% effectiveness (p = 0.04)
   - 28 occurrences in 1000 games
   - Successful entries: 17 / 28 (60%)
   - Avg profit: +0.032 SOL per moonshot

3. **Slow Burner**: 40% effectiveness (p = 0.31, not significant)
   - 102 occurrences in 1000 games
   - Successful holds: 41 / 102 (40%)
   - Marginal profit: +0.005 SOL per hold

**Conclusion**: Ultra-short skip and moonshot are validated. Slow burner is weak.

**When to Share**:
- LLM asks about pattern effectiveness
- LLM wants to decide if pattern rewards should change
- LLM needs validation of pattern profitability

**Relevant Questions**: 1.4 (Pattern Weight), 4.2 (Signal Hierarchy)

---

## Tier 4: Reference Files (Share Only If Explicitly Needed)

### T4-1: Test Suite

**Directory**: `/home/nomad/Desktop/rugs-rl-bot/tests/`
**Files**: 15 test files, ~3000 lines total
**Status**: 100% passing (all 120 tests)

**Purpose**: Document how components are tested

**Key Test Files**:
- `test_reward_calculator.py` (25 tests)
- `test_sidebet_predictor.py` (29 tests)
- `test_environment.py` (18 tests)
- `test_pattern_detector.py` (12 tests)
- `test_volatility_tracker.py` (10 tests)
- `test_sweet_spot_detector.py` (8 tests)
- `test_feature_extractor.py` (18 tests)

**When to Share**:
- LLM asks "how are components tested?"
- LLM wants to understand testing strategy
- LLM needs to write new tests for new components

**Relevant Questions**: 11.4 (Implementation Checklist - testing steps)

---

### T4-2: Alternative Reward Designs

**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/alternative_approaches.md`
**Size**: ~250 lines
**Status**: Complete (documents rejected approaches)

**Purpose**: Document alternative designs that were considered but rejected

**Alternatives**:
1. **Inverse RL from Human Play**: Learn rewards from human gameplay
   - Rejected: Too data-intensive (need 1000+ human games)

2. **Curiosity-Driven Exploration**: Intrinsic rewards for novel states
   - Rejected: Doesn't address rug avoidance (exploration != safety)

3. **Multi-Agent Competition**: Train multiple agents competitively
   - Rejected: Single-agent problem (no opponent)

4. **Hierarchical RL**: High-level strategy, low-level execution
   - Rejected: Overkill for this problem (not complex enough)

5. **Model-Based RL**: Learn dynamics model, plan ahead
   - Rejected: Rug timing is stochastic (model won't help)

**When to Share**:
- LLM proposes alternative approach
- LLM wants to know what was considered
- LLM asks "why not try X?"

**Relevant Questions**: Section 9 (Open Questions)

---

### T4-3: Research Papers

**Directory**: `/home/nomad/Desktop/rugs-rl-bot/papers/`
**Files**: 8 PDF papers

**Relevant Papers**:
1. "Reward Shaping for Sparse Reward Environments" (Ng et al.)
   - Relevance: How to design reward functions when primary reward is sparse

2. "Safe Reinforcement Learning" (Garcia & Fernández)
   - Relevance: Safety constraints in RL (rug avoidance as safety)

3. "Risk-Averse RL for Financial Trading" (Tamar et al.)
   - Relevance: Risk management in trading agents

4. "Multi-Objective RL" (Van Moffaert & Nowé)
   - Relevance: Balancing profit vs risk objectives

**When to Share**:
- LLM asks for academic references
- LLM wants theoretical justification
- LLM needs advanced techniques (e.g., safe RL, multi-objective)

**Relevant Questions**: Section 9 (Open Questions - theoretical approaches)

---

### T4-4: Edge Case Handling

**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/edge_cases.md`
**Size**: ~200 lines
**Status**: Complete (documents known edge cases)

**Purpose**: Document edge cases and how they're handled

**Edge Cases**:
1. **Rug on First Tick**: Game rugs immediately (tick 0-5)
   - Handling: No positions possible, no penalty

2. **Ultra-Long Game**: Game lasts >1000 ticks (3x mean)
   - Handling: Z-score very high, sidebet model predicts critical

3. **Zero Volatility**: Price constant for 100+ ticks
   - Handling: volatility_ratio = 1.0 (no change from baseline)

4. **All Positions Rug Simultaneously**: Multiple positions liquidated same tick
   - Handling: Bankruptcy if total loss > bankroll

5. **Model Confidence = 0**: Sidebet model has no confidence
   - Handling: Fall back to volatility signal

**When to Share**:
- LLM asks about edge cases
- LLM wants to know how failures are handled
- LLM needs to design edge case handling for new components

**Relevant Questions**: 8.3 (Failure Modes)

---

## File Request Examples

### Example 1: LLM Asks About Current Weights

**LLM**: "Can you show me the current reward component weights?"

**Your Response**:
```
Here's T1-1 (reward_calculator.py) with current weights:

Key sections:
- Line 55: pnl_reward_weight = 1.0 (highest)
- Line 105: volatility_exit_weight = 8.0 (currently dominant)
- Line 155: sweet_spot_weight = 2.0
- Line 205: pattern_weight = 3.0
- Line 255: bankruptcy_penalty = -1000.0

Missing:
- No rug_avoidance component (weight = 0.0)

[Paste relevant code sections]
```

---

### Example 2: LLM Asks About Observation Space

**LLM**: "What features are available in the observation space?"

**Your Response**:
```
Here's T1-2 (environment.py) observation space definition:

Total: 79 features across 8 groups:
- current (10): price, tick, bankroll
- history (20): price history, volatility history
- positions (30): 10 positions x 3 features each
- sidebets (3): active, won, lost
- meta_context (24): game state, patterns
- sweet_spot (3): in_sweet_spot, timing, quality
- duration_pred (4): predicted duration, confidence
- rug_prediction (5): ✅ NEW - probability, confidence, ticks_to_rug_norm, is_critical, should_exit

The 5 rug_prediction features are from the SidebetPredictor (T1-5).

[Paste lines 150-330 from environment.py]
```

---

### Example 3: LLM Asks for Statistical Validation

**LLM**: "What data supports that sidebet model outperforms volatility?"

**Your Response**:
```
Here's T3-1 (statistical_validation.md):

Finding 1: Sidebet vs Volatility Exit Signal
- Sidebet win rate: 38.1% (95% CI: 35.2-41.0%)
- Volatility accuracy: 50.0% (95% CI: 47.1-52.9%)
- Two-sample t-test: t(998) = -4.23, p < 0.001
- Cohen's d = 0.85 (large effect size)
- Conclusion: Sidebet is significantly more reliable

Also relevant from T1-3 (SIDEBET_SUCCESS_REPORT.md):
- Sidebet ROI: 754% on 200-game backtest
- Sidebet Martingale: 100% success (never bankrupted)

[Paste relevant statistical analysis]
```

---

## Quick Reference Table

| File | Tier | When to Share | Relevant Questions |
|------|------|---------------|-------------------|
| reward_calculator.py | T1 | Current reward structure | 1.1-1.4, 2.1-2.3, 3.1-3.2 |
| environment.py | T1 | Observation space (79 features) | 4.1-4.3, 11.3 |
| V3_SUCCESS_REPORT.md | T1 | Sidebet model performance | 2.1-2.3, 2.4, 4.1, 4.3 |
| GYMNASIUM_DESIGN_SPEC.md | T1 | Game rules, constraints | Section 9, 11.5 |
| predictor.py | T1 | Sidebet prediction structure | 4.1, 4.2, 11.3 |
| pattern_detector.py | T2 | Pattern exploitation | 1.4, 4.2 |
| volatility_tracker.py | T2 | Volatility exit signal | 1.2, 4.2 |
| sweet_spot_detector.py | T2 | Entry timing | 1.3, 6.2 |
| training_config.yaml | T2 | PPO config, current weights | 11.6 |
| feature_extractor.py | T2 | 14 sidebet features | 6.1, 9.1 |
| statistical_validation.md | T3 | P-values, effect sizes | Any "cite data" question |
| training_failure_report.md | T3 | Previous failed approaches | 3.3, 7.4 |
| baseline_performance.csv | T3 | Current baseline metrics | 8.1, 11.5 |
| pattern_validation.md | T3 | Pattern profitability | 1.4, 4.2 |
| test_suite/ | T4 | Testing strategy | 11.4 |
| alternative_approaches.md | T4 | Rejected designs | Section 9 |
| research_papers/ | T4 | Academic references | Section 9 |
| edge_cases.md | T4 | Edge case handling | 8.3 |

---

## Sharing Best Practices

### Do's:
✅ Share files incrementally (don't dump everything at once)
✅ Provide context when sharing (key sections, line numbers)
✅ Reference this guide when LLM requests files
✅ Start with T1, move to T2/T3/T4 only if needed
✅ Cite specific sections when answering questions

### Don'ts:
❌ Don't share T4 files unless LLM explicitly asks
❌ Don't share entire codebase (overwhelming)
❌ Don't share files without context (what to look for?)
❌ Don't skip T1 files (critical for understanding)

---

## Session Workflow Integration

**Phase 1 (Context Loading)**: Share T1-3, T1-4 (SIDEBET_SUCCESS_REPORT, GAME_MECHANICS)
**Phase 2 (Deep Dive)**: Share T1-1, T1-2, T1-5 (implementation code)
**Phase 3 (Analysis)**: Share T2 files as LLM explores questions
**Phase 3 (Validation)**: Share T3 files if LLM requests statistical evidence
**Phase 4 (Deliverables)**: Reference T1-1, T2-4 for implementation details

**Total Files in Bundle**: 18 files (5 T1, 5 T2, 4 T3, 4 T4)

**Estimated Usage**:
- Most sessions: T1 files only (5 files)
- Deep sessions: T1 + T2 (10 files)
- Research sessions: T1 + T2 + T3 (14 files)
- Comprehensive: All tiers (18 files)

---

**This bundle ensures LLM has access to all necessary context while maintaining focus on critical files (T1) and avoiding information overload.**
