# 📚 REWARD DESIGN FILE BUNDLE - Complete Reference

**Purpose**: Comprehensive list of all relevant files for reward function design
**Total Files**: 17 across 3 projects
**Reading Time**: ~3-4 hours for full comprehension

---

## 🎯 QUICK REFERENCE: Must-Read Files (Top 3)

1. **reward_calculator.py** - THE core reward function (405 lines)
2. **RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md** - Game bible + failure lessons (513 lines)
3. **reward_config.yaml** - Complete parameter configuration (320 lines)

**Time**: 30-45 minutes to read these 3 files gives you 80% of context

---

## 📋 COMPLETE FILE LIST (Organized by Priority)

---

## 🔴 TIER 1: CRITICAL - Must Read (3 files, ~1,200 lines)

### 1. Reward Calculator Implementation
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/reward_calculator.py`
**Lines**: 405
**Language**: Python

**Contents**:
- `RewardCalculator` class (lines 28-404)
- 13 reward components implementation
- Component enable/disable logic
- Reward breakdown for debugging
- Integration with game state

**Key Sections**:
```python
# Component definitions (lines 16-26)
1. financial_pnl          # Primary profit/loss
2. pattern_exploitation   # Statistical pattern bonuses
3. sidebet_timing         # Strategic sidebet rewards
4. drawdown_penalty       # Bankroll loss penalties
5. bankruptcy_penalty     # Terminal state penalty
6. invalid_action_penalty # Invalid trade penalty
7. late_zone_entry        # Scalping bonus
8. quick_exit_bonus       # 10-15 tick hold reward
9. hold_too_long_penalty  # Risk increases with time
10. progressive_rug_hold  # AUDIT FIX - escalating rug penalties
11. volatility_exit_bonus # THE #1 SIGNAL - massive exit bonuses
12. selective_entry       # SKIP 73% - patience rewards
13. enhanced_sidebet      # PRESALE +4.0 EV - strategic hedging
```

**Key Functions**:
- `calculate_reward()` (lines 185-203) - Main entry point
- `calculate_reward_with_breakdown()` (lines 205-378) - Detailed breakdown
- `_is_pattern_exploitation()` (lines 380-404) - Pattern detection

**Why Critical**: This IS the reward function. Everything else is context for designing changes to this.

---

### 2. Game Mechanics Knowledge Base
**File**: `/home/nomad/Desktop/REPLAYER/docs/game_mechanics/RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md`
**Lines**: 513
**Format**: Markdown

**Contents**:
- Complete game rules and mechanics
- Strategic patterns and validated insights
- Cross-game meta-layer patterns
- Statistical findings from 528 games
- **CRITICAL**: Bankruptcy problem analysis (lines 439-458)

**Key Sections**:
- **Instant Liquidation Rule** (lines 10-28) - THE MOST IMPORTANT RULE
- **Presale Mechanics** (lines 33-71) - Strategic entry window
- **Position & Bankroll** (lines 74-103) - Multi-position management
- **Side Bet Mechanics** (lines 106-167) - 40-tick window, 5-tick cooldown, 5:1 payout
- **Meta-Layer Treasury** (lines 172-222) - Cross-game adaptive patterns
- **Rug Event Mechanics** (lines 224-253) - Volatility spikes, prediction
- **Why Training Failed** (lines 439-447):
  ```markdown
  1. Bot holds positions through rugs (instant liquidation)
  2. No side bet hedging mechanism
  3. Doesn't recognize volatility spike warnings
  4. Ignores probability curves
  5. Position sizing too aggressive
  6. No drawdown management
  7. No presale strategy
  ```
- **What Bot MUST Learn** (lines 449-458) - Required behaviors

**Why Critical**: Without understanding game mechanics, you can't design rewards that teach correct behavior.

---

### 3. Reward Configuration
**File**: `/home/nomad/Desktop/rugs-rl-bot/configs/reward_config.yaml`
**Lines**: 320
**Format**: YAML

**Contents**:
- Complete parameter configuration for all 13 components
- Enable/disable flags
- Tunable weights and thresholds
- Pre-configured variants (baseline, aggressive, conservative)
- A/B testing configurations

**Structure**:
```yaml
# Global settings (lines 14-34)
model_type: "ensemble"  # ensemble, trading, sidebet
variant: "baseline"     # baseline, aggressive, conservative

# Component 1: Financial P&L (lines 36-43)
financial_pnl:
  enabled: true
  weight: 1.0
  scale_factor: 1.0

# Component 10: Progressive Rug Hold (AUDIT FIX) (lines 143-156)
progressive_rug_hold:
  enabled: true
  levels:
    - threshold: 0.5      # 50% volatility
      penalty: -0.1
    - threshold: 1.0      # 100% volatility
      penalty: -2.5
    - threshold: 2.0      # 200% volatility
      penalty: -5.0

# Component 11: Volatility Exit (THE #1 SIGNAL) (lines 158-170)
volatility_exit_bonus:
  enabled: true
  levels:
    - threshold: 2.0      # 2x baseline
      bonus: 0.5
    - threshold: 5.0      # 5x baseline
      bonus: 1.5
    - threshold: 10.0     # 10x baseline
      bonus: 3.0

# (... continues for all 13 components)
```

**Why Critical**: These are the actual parameter values used in training. This is what you'll be modifying.

---

## 🟠 TIER 2: CORE CONTEXT (4 files, ~2,000 lines)

### 4. Volatility Tracker (THE #1 EXIT SIGNAL)
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/analysis/volatility_tracker.py`
**Lines**: 156
**Language**: Python

**Contents**:
- Rolling baseline volatility calculation
- Current volatility tracking
- Volatility ratio computation (current / baseline)
- Exit signal thresholds

**Key Statistics** (from analysis of 528 games):
```python
# 94.7% of games show >100% volatility spike before rug
mean_spike = 664.7%     # 6.6x baseline volatility
median_spike = 551.6%
percentile_95 = 1173%
max_observed = 1690%

# Exit Signal Levels
CAUTION_THRESHOLD = 2.0    # 2x baseline - early warning
WARNING_THRESHOLD = 5.0    # 5x baseline - strong signal
EMERGENCY_THRESHOLD = 10.0 # 10x baseline - exit immediately
```

**Key Functions**:
- `update()` (lines 45-73) - Updates volatility metrics each tick
- `get_exit_signal()` (lines 75-94) - Returns signal level
- `get_ratio()` (lines 96-104) - Returns volatility ratio

**Why Important**: Volatility is THE most reliable predictor of rugs (94.7% accuracy). Reward design must heavily incentivize acting on this signal.

---

### 5. Pattern Exploitation Research
**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/PATTERN_EXPLOITATION_RESEARCH.md`
**Lines**: 627
**Format**: Markdown

**Contents**:
- Complete statistical validation of 3 patterns
- P-values, sample sizes, effect sizes
- EV calculations and breakeven analysis
- Implementation examples

**Pattern 1: Post-Max-Payout Recovery** (lines 19-68):
```markdown
Ultra-Short Rate Comparison:
- After high-peak games: 21.1%
- Baseline: 12.2%
- Improvement: +72.7%
- Statistical significance: p = 0.0038 (HIGHLY SIGNIFICANT)
- Sample size: 155 games
- Confidence: 99.62%
```

**Pattern 2: Ultra-Short Arbitrage** (lines 73-158):
```markdown
Sidebet Probability After Ultra-Short:
- After ultra-short: 8.1%
- Baseline: 12.2%
- Edge: +25-50% in optimal conditions
- Statistical significance: p ≈ 0.05 (WEAKLY SIGNIFICANT)
```

**Pattern 3: Moonshot Momentum** (lines 163-252):
```markdown
Conditional Probabilities:
- P(reach 20x | reached 8x) = 50%
- P(reach 20x | reached 12x) = 65%
- P(reach 20x | reached 16x) = 80%
```

**Sidebet EV Analysis** (lines 254-373):
```markdown
Formula: EV = (P(win) × 5.0) - (P(lose) × 1.0)
Breakeven: P(win) = 16.67%

Pattern-Adjusted:
- Baseline: 12.2% → EV = -0.39 (NEGATIVE)
- Post-max-payout: 21.1% → EV = +0.16 (POSITIVE!)
- Post-long-game: 8.1% → EV = -0.59 (NEGATIVE)
- Presale (pattern): 21%+ → EV = +4.0 (MASSIVE!)
```

**Why Important**: Statistical validation justifies pattern bonuses. P-values inform how much to reward each pattern.

---

### 6. Pattern Detector Implementation
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/pattern_detector.py`
**Lines**: 293
**Language**: Python

**Contents**:
- 3 pattern detector classes
- Pattern confidence scoring
- Integration with game history

**Key Classes**:
```python
# Pattern 1: Post-Max-Payout (lines 16-37)
class PostMaxPayoutDetector:
    def detect(self, game_history):
        # Detects if last game was high-peak (>10x)
        # Returns: (detected: bool, confidence: float)

# Pattern 2: Ultra-Short Predictor (lines 40-84)
class UltraShortPredictor:
    def predict(self, last_game_duration):
        # Predicts ultra-short probability
        # Uses exponential decay model

# Pattern 3: Moonshot Momentum (lines 87-116)
class MoonshotMomentumDetector:
    def detect(self, current_price, history):
        # Detects momentum thresholds: 8x, 12x, 20x
        # Returns: (threshold_reached, probability)
```

**Key Function**:
- `detect_patterns()` (lines 166-229) - Returns 10 pattern signals:
  ```python
  {
      'post_max_payout': bool,
      'post_max_payout_confidence': float,
      'ultra_short_next': bool,
      'ultra_short_probability': float,
      'moonshot_8x': bool,
      'moonshot_12x': bool,
      'moonshot_20x': bool,
      'moonshot_probability': float,
      'pattern_active': bool,  # Any pattern detected
      'aggregated_confidence': float  # Weighted confidence
  }
  ```

**Why Important**: Pattern bonuses in reward calculator depend on these detections. Understanding detection logic helps design appropriate rewards.

---

### 7. Environment Implementation
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/environment/environment.py`
**Lines**: 920
**Language**: Python

**Contents**:
- Complete Gymnasium environment
- Observation space definition
- Action space definition
- State dictionary passed to reward calculator

**Key Sections**:

**Observation Space** (lines 142-154):
```python
observation_space = Dict({
    'current': Box(10),       # Current state
    'history': Box(20),       # Last 5 games
    'positions': Box(30),     # Up to 10 positions
    'sidebets': Box(3),       # Sidebet status
    'meta_context': Box(24),  # Scalping signals
    'sweet_spot': Box(3),     # Selective entry
    'duration_pred': Box(4),  # Sidebet timing
})
```

**Action Space** (lines 156-160):
```python
action_space = MultiDiscrete([8, 9, 11])
# [action_type (8), bet_size_idx (9), sell_percent_idx (11)]

# Action Types:
# 0=WAIT, 1=BUY_MAIN, 2=SELL_MAIN, 3=BUY_SIDE,
# 4=BUY_BOTH, 5=EMERGENCY_EXIT, 6=PARTIAL_SELL, 7=SKIP
```

**State Dictionary for Rewards** (`_get_state_dict()`, lines 713-804):
```python
state = {
    'bankroll': float,
    'positions': int,
    'pattern_active': bool,
    'pattern_type': str,
    'pattern_confidence': float,
    'in_late_zone': bool,
    'hold_duration': int,
    'optimal_hold_exceeded': bool,
    'in_danger_zone': bool,
    'has_active_sidebet': bool,
    'game_ended': bool,
    'volatility_ratio': float,
    'in_sweet_spot': bool,
    'sweet_spot_available': bool,
    'sidebet_can_place': bool
}
```

**Why Important**: Shows what observations are available to agent and what state information reward calculator can use.

---

## 🟡 TIER 3: SUPPORTING (5 files, ~1,200 lines)

### 8. Sweet Spot Detector (SELECTIVE ENTRY)
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/analysis/sweet_spot_detector.py`
**Lines**: 150
**Language**: Python

**Audit Finding**:
```python
# Only 43.3% of games reach sweet spot (2-4x)
games_reaching_sweet_spot = 229 / 528  # 43.3%
games_profitable_overall = 27%
average_duration_in_sweet_spot = 68.7  # ticks

# Implication: Skip 73% of unprofitable games!
```

**Key Functions**:
- `is_in_sweet_spot()` - Returns True if 2x ≤ price ≤ 4x
- `should_enter()` - Returns True if game likely to reach sweet spot
- `get_skip_recommendation()` - Skip vs enter decision

**Why Important**: Selective entry (Component 12) depends on this. Only 27% of games are profitable - patience is key.

---

### 9. Sidebet EV Calculator
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/analysis/sidebet_ev_calculator.py`
**Lines**: 121
**Language**: Python

**EV Formula**:
```python
EV = (P(win) × 5.0) - (P(lose) × 1.0)
breakeven_probability = 1/6 = 16.67%
```

**Pattern-Adjusted Probabilities**:
```python
baseline_prob = 0.122          # EV = -0.39 (NEGATIVE)
post_max_payout_prob = 0.211   # EV = +0.16 (POSITIVE!)
post_long_game_prob = 0.081    # EV = -0.59 (NEGATIVE)
presale_after_pattern = 0.21+  # EV = +4.0 (MASSIVE!)
```

**Key Functions**:
- `calculate_ev()` - Returns expected value for given probability
- `get_optimal_probability()` - Returns probability given context
- `should_place_sidebet()` - Boolean recommendation

**Why Important**: Sidebet bonuses (Components 3, 13) use these calculations. Shows when sidebets are profitable vs costly.

---

### 10. Gymnasium Design Specification
**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/GYMNASIUM_DESIGN_SPEC.md`
**Lines**: 1,341
**Format**: Markdown

**Contents**:
- Complete technical specification
- Observation space detailed breakdown
- Action space design rationale
- Reward function architecture
- Episode management (15-game episodes)
- State transitions

**Key Sections**:
- Observation Space (lines 125-253) - All 70 dimensions explained
- Action Space (lines 256-390) - Action encoding and mapping
- Reward Function (lines 393-492) - Component design rationale
- Episode Management (lines 495-587) - Multi-game episodes

**Why Important**: Reference document for understanding what data is available to agent and reward calculator.

---

### 11. Position Manager
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/position_manager.py`
**Lines**: 233
**Language**: Python

**Features**:
- Tracks up to 10 open positions
- Partial sell capability
- Aggregate P&L calculation
- Hold duration tracking

**Key Statistics**:
```python
optimal_hold_duration = (10, 15)  # ticks
average_profitable_hold = 23      # ticks
hold_over_30_rug_rate = 0.68     # 68% rug rate
hold_over_50_rug_rate = 0.89     # 89% rug rate
```

**Key Functions**:
- `open_position()` - Creates new position
- `close_position()` - Realizes P&L
- `get_aggregate_pnl()` - Total unrealized P&L
- `get_hold_durations()` - Returns all hold times

**Why Important**: Hold duration penalties (Component 9) and quick exit bonuses (Component 8) depend on this tracking.

---

### 12. Sidebet Manager
**File**: `/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/sidebet_manager.py`
**Lines**: 217
**Language**: Python

**Game Rules Implementation**:
```python
SIDEBET_WINDOW = 40       # ticks
SIDEBET_PAYOUT = 5.0      # 5x profit
SIDEBET_COOLDOWN = 5      # ticks between sidebets
MAX_ACTIVE_SIDEBETS = 1   # only 1 at a time
```

**Key Functions**:
- `can_place_sidebet()` - Checks cooldown and active status
- `place_sidebet()` - Creates sidebet with 40-tick window
- `resolve_sidebet()` - Handles win/loss
- `get_ticks_remaining()` - Returns time left on active sidebet

**Why Important**: Sidebet timing bonuses (Component 3, 13) depend on proper sidebet mechanics implementation.

---

## 🟢 TIER 4: REFERENCE (5 files, ~1,400 lines)

### 13. Game Mechanics Technical Spec
**File**: `/home/nomad/Desktop/REPLAYER/docs/game_mechanics/GAME_MECHANICS.md`
**Lines**: 309
**Format**: Markdown

**Contents**:
- Technical game rules specification
- Data field definitions
- P&L calculation formulas
- Phase transitions
- Trading rules

**Key Formulas**:
```markdown
# P&L Calculation
unrealized_pnl = position_amount * (current_price - entry_price) / entry_price
realized_pnl = unrealized_pnl (at close)

# Sidebet Mechanics
sidebet_win = bet_amount * 5.0 - bet_amount = bet_amount * 4.0
sidebet_lose = -bet_amount

# Bankroll Updates
new_bankroll = old_bankroll + realized_pnl  # Instant update
```

**Why Important**: Technical reference for implementing reward calculations correctly.

---

### 14. Side Bet Mechanics v2
**File**: `/home/nomad/Desktop/REPLAYER/docs/game_mechanics/side_bet_mechanics_v2.md`
**Lines**: Variable
**Format**: Markdown

**Contents**:
- Detailed sidebet timing rules
- Cooldown mechanics explanation
- Presale vs active placement strategies
- Win conditions

**Why Important**: Detailed reference for sidebet timing rewards.

---

### 15. Project Status
**File**: `/home/nomad/Desktop/rugs-rl-bot/docs/PROJECT_STATUS.md`
**Lines**: 337
**Format**: Markdown

**Contents**:
- Current training status
- Architectural decisions
- Pattern validation results
- Success criteria
- Timeline and milestones

**Key Sections**:
- Current Approach (Socket.IO feed vs YOLO vision)
- Pattern Validation Status (3 patterns validated)
- Success Criteria (win rate, bankroll growth, drawdown targets)
- What's Working vs What Needs Work

**Why Important**: Shows context of what worked/didn't work in previous iterations. Informs design decisions.

---

### 16. Reward Calculator Tests
**File**: `/home/nomad/Desktop/rugs-rl-bot/tests/test_training/test_reward_calculator.py`
**Lines**: Variable
**Language**: Python

**Contents**:
- Unit tests for all 13 reward components
- Expected behavior validation
- Edge case testing

**Test Coverage**:
- Financial P&L calculation
- Pattern exploitation bonuses
- Sidebet timing rewards
- Drawdown/bankruptcy penalties
- Volatility exit bonuses
- Selective entry bonuses
- Configuration variants

**Why Important**: Shows expected behavior for each component. Useful for validation after changes.

---

### 17. CV Boilerplate Knowledge Base (Failure Analysis)
**File**: `/home/nomad/Desktop/CV-BOILER-PLATE-FORK/docs/projects/rugs_fun/RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md`
**Lines**: 513
**Format**: Markdown

**Duplicate of #2 but with training failure analysis**

**Key Section: Why Training Failed** (lines 439-458):
```markdown
Why Bot Went Bankrupt 94.6% of Time:
1. Bot holds positions through rugs (instant liquidation)
2. No side bet hedging mechanism
3. Doesn't recognize volatility spike warnings
4. Ignores probability curves
5. Position sizing too aggressive
6. No drawdown management
7. No presale strategy

What Bot MUST Learn to Survive:
1. Exit BEFORE rug (volatility + probability signals)
2. Use side bets as hedges (presale after patterns)
3. Respect trading zones (2-4x sweet spot)
4. Track meta-layer patterns (cross-game learning)
5. Proper position sizing (2-5% of bankroll)
6. Drawdown limits (stop trading below threshold)
7. Presale decision logic (entry timing)
8. Instarug protection (emergency exits)
```

**Why Important**: Direct lessons from 94.6% bankruptcy failure. Critical for understanding what NOT to do.

---

## 📖 RECOMMENDED READING ORDER

### **Session 1: Core Understanding** (30-45 min)
1. Read `reward_calculator.py` (405 lines)
2. Read `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` (513 lines, focus on lines 10-253 and 439-458)
3. Read `reward_config.yaml` (320 lines)

**Output**: Understand current reward system and bankruptcy problem

---

### **Session 2: Critical Signals** (30-45 min)
4. Read `volatility_tracker.py` (156 lines)
5. Read `PATTERN_EXPLOITATION_RESEARCH.md` (627 lines, focus on statistics)
6. Read `pattern_detector.py` (293 lines, focus on detection logic)

**Output**: Understand THE #1 exit signal and validated patterns

---

### **Session 3: Environment Context** (30-45 min)
7. Read `environment.py` (920 lines, focus on observation/action spaces and `_get_state_dict()`)
8. Read `sweet_spot_detector.py` (150 lines)
9. Read `sidebet_ev_calculator.py` (121 lines)

**Output**: Understand what data is available and EV calculations

---

### **Session 4: Design** (60-90 min)
10. Review REWARD_DESIGN_QUESTIONS.md
11. Propose component rebalancing
12. Design new components (if needed)
13. Document justifications

**Output**: Revised reward_config.yaml with justifications

---

## 🎯 QUICK LOOKUP REFERENCE

### **For Component Weights**:
→ See `reward_config.yaml` (lines 36-244)

### **For Statistical P-Values**:
→ See `PATTERN_EXPLOITATION_RESEARCH.md` (lines 19-252)

### **For Volatility Statistics**:
→ See `volatility_tracker.py` (docstring comments)

### **For Game Rules**:
→ See `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` (lines 10-253)

### **For Failure Analysis**:
→ See `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` (lines 439-458)

### **For Available Observations**:
→ See `environment.py` (lines 142-154 and 713-804)

### **For EV Calculations**:
→ See `sidebet_ev_calculator.py` (docstring and `calculate_ev()`)

---

## 📁 FILE PATHS SUMMARY

```
# Tier 1: Critical
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/reward_calculator.py
/home/nomad/Desktop/REPLAYER/docs/game_mechanics/RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md
/home/nomad/Desktop/rugs-rl-bot/configs/reward_config.yaml

# Tier 2: Core
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/analysis/volatility_tracker.py
/home/nomad/Desktop/rugs-rl-bot/docs/PATTERN_EXPLOITATION_RESEARCH.md
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/pattern_detector.py
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/environment/environment.py

# Tier 3: Supporting
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/analysis/sweet_spot_detector.py
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/analysis/sidebet_ev_calculator.py
/home/nomad/Desktop/rugs-rl-bot/docs/GYMNASIUM_DESIGN_SPEC.md
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/position_manager.py
/home/nomad/Desktop/rugs-rl-bot/rugs_bot/training/sidebet_manager.py

# Tier 4: Reference
/home/nomad/Desktop/REPLAYER/docs/game_mechanics/GAME_MECHANICS.md
/home/nomad/Desktop/REPLAYER/docs/game_mechanics/side_bet_mechanics_v2.md
/home/nomad/Desktop/rugs-rl-bot/docs/PROJECT_STATUS.md
/home/nomad/Desktop/rugs-rl-bot/tests/test_training/test_reward_calculator.py
/home/nomad/Desktop/CV-BOILER-PLATE-FORK/docs/projects/rugs_fun/RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md
```

---

**Total Reading**: ~5,500 lines across 17 files
**Estimated Time**: 3-4 hours for thorough comprehension
**Minimum Time**: 30-45 minutes for Tier 1 only (gets you 80% of context)

---

*Use this bundle as a reference guide during your reward design session*
