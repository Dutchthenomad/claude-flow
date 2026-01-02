# Advanced Reward Systems Documentation

**Date**: 2025-11-09
**Purpose**: Preserve knowledge of sophisticated 17-component reward system before simplification
**Context**: Phase 0 Revision encountered reward hacking bugs, simplified to 6 components for stability

---

## Executive Summary

This document maps the location of all advanced reward system components designed during Phase 3 (Empirical Analysis & Rewards Design). While the production system has been simplified to 6 core components for stability and debuggability, the sophisticated features described here represent empirically-validated patterns that can be reintegrated once the basic system is proven stable.

**Simplification Rationale**:
- 17-component system was too complex to debug (reward hacking vulnerability)
- Multiple redundant components (inactivity/opportunity_cost, zone_entry/position_courage)
- Weight imbalance (bankruptcy 1000.0 vs financial 3.0) caused instability
- Missing state tracking made opportunity cost unreliable
- ACTION_SKIP not handled, causing crashes

**Reintegration Path**:
1. Prove simplified 6-component system works (Phase 0 Revision)
2. Add back merged components one at a time (activity, entry_quality)
3. Reintroduce advanced features (volatility exit, pattern recognition)
4. Fine-tune weights with A/B testing

---

## Original 17-Component Reward System

### Configuration File Locations

**Original Complex Config** (17 components):
`/home/nomad/Desktop/rugs-rl-bot/configs/reward_config_phase0_revised.yaml`

**Simplified Config** (6 components):
`/home/nomad/Desktop/rugs-rl-bot/configs/reward_config_simplified.yaml`

### Component Mapping Table

| Component | Weight | Status | Simplified Into | Lines in reward_calculator.py |
|-----------|--------|--------|-----------------|-------------------------------|
| **financial** | 3.0 → 5.0 | ✅ Kept | Core Component 1 | 544-597 |
| **rug_avoidance** | 8.0 → 5.0 | ✅ Kept | Core Component 2 | 598-691 |
| **inactivity** | 5.0 | ⚠️ Merged | → activity | 914-960 |
| **opportunity_cost** | 3.0 | ⚠️ Merged | → activity | 1008-1043 |
| **zone_entry** | 2.0 | ⚠️ Merged | → entry_quality | 692-739 |
| **position_courage** | 4.0 | ⚠️ Merged | → entry_quality | 961-1007 |
| **temporal_penalty** | 3.0 | ❌ Removed | (redundant) | 740-789 |
| **survival_bonus** | 0.1 | ❌ Removed | (redundant with financial) | 790-833 |
| **sweet_spot** | 1.0 | ⚠️ Merged | → entry_quality zones | 834-878 |
| **pattern_boost** | 1.0 | ❌ Disabled | pattern (optional) | 879-913 |
| **volatility_exit** | 2.0 | ❌ Removed | (use sidebet predictor) | Not implemented yet |
| **scalping_bonuses** | 1.5 | ❌ Removed | (too complex for Phase 0) | Not implemented yet |
| **risk_management** | 10.0 | ✅ Kept | Core Component 5 | Partial implementation |
| **invalid_action** | 0.1 | ✅ Kept | Unchanged | 526-543 |

**Total**: 17 components → 6 core components + 2 disabled/optional

---

## Core Component Locations (Simplified System)

### 1. Financial P&L (Primary Signal)
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_financial_reward()` (lines 544-597)
**Weight**: 5.0 (increased from 3.0)
**Purpose**: Direct P&L from position changes

**Key Logic**:
```python
def _calculate_financial_reward(self, state_dict, prev_state):
    pnl_change = state_dict['pnl'] - prev_state['pnl']
    return pnl_change * self.config.get('pnl_multiplier', 1.0)
```

**Advanced Features (Future)**:
- Risk-adjusted returns (Sharpe ratio)
- Max drawdown tracking
- Per-position attribution

---

### 2. Rug Avoidance (Key Skill)
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_rug_avoidance_reward()` (lines 598-691)
**Weight**: 5.0 (reduced from 8.0 after bug fix)
**Purpose**: Reward emergency exits and selling before rug

**Critical Fix** (Line 607):
```python
# BUG FIX: Check positions before rewarding SELL
if action in ['SELL_MAIN_25', 'SELL_MAIN_100', 'PARTIAL_SELL']:
    if not state_dict.get('had_positions', False):  # ← CRITICAL
        return 0.0  # Don't reward SELL spam
```

**Rewards**:
- Emergency exit: +15.0
- Partial sell bonus: +10.0
- Full exit bonus: +12.0
- Early exit safe: +8.0

**Penalties**:
- Rugged with positions: -20.0
- Late exit: -5.0

**Advanced Features (Original Design)**:
- Temporal rug probability integration (cumulative risk by tick)
- Confidence-weighted exit timing
- Multi-position exit coordination

---

### 3. Activity (Merged: inactivity + opportunity_cost)
**Status**: ⚠️ Pending implementation in simplified system
**Original Components**:

#### 3A. Inactivity Penalty
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_inactivity_penalty()` (lines 914-960)
**Original Weight**: 5.0
**Purpose**: Penalize waiting without positions in favorable zones

**Key Logic** (Phase 0 Fix 2):
```python
def _calculate_inactivity_penalty(self, state_dict):
    if state_dict['action'] != 'WAIT':
        return 0.0

    if state_dict['has_positions']:
        return 0.0  # OK to wait with positions

    multiplier = state_dict.get('current_price', 1.0)

    # Penalize WAIT without positions in good zones
    if 25.0 <= multiplier <= 50.0:  # Optimal zone
        return -10.0
    elif 10.0 <= multiplier <= 25.0:  # Good zone
        return -5.0
    else:
        return -2.0  # Other zones
```

**Empirical Basis**:
- 25-50x zone: 75% success rate, 186-427% median returns
- Opportunity cost of missing sweet spot entries

#### 3B. Opportunity Cost
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_opportunity_cost()` (lines 1008-1043)
**Original Weight**: 3.0
**Purpose**: Penalize consistently idle bankroll

**Key Logic** (Phase 0 Fix 4):
```python
def _calculate_opportunity_cost(self, state_dict):
    games_completed = state_dict.get('games_completed', 0)
    total_positions = state_dict.get('total_positions_taken', 0)

    if games_completed < 3:  # Grace period
        return 0.0

    position_rate = total_positions / games_completed
    min_rate = 0.3  # At least 30% of games should have positions

    if position_rate < min_rate:
        shortfall = min_rate - position_rate
        return -10.0 * shortfall  # Max -10.0

    return 0.0
```

**State Tracking Required**:
- `games_completed` (environment.py line 182)
- `total_positions_taken` (environment.py line 183)

**Simplified Version** (reward_config_simplified.yaml):
```yaml
activity:
  weight: 3.0
  inactivity_penalties:
    optimal_zone_wait: -5.0
    good_zone_wait: -3.0
    other_zones_wait: -1.0
  min_positions_per_game: 0.3
  grace_period: 3
  max_penalty: -5.0
```

---

### 4. Entry Quality (Merged: zone_entry + position_courage)
**Status**: ⚠️ Pending implementation in simplified system
**Original Components**:

#### 4A. Zone Entry Rewards
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_zone_entry_reward()` (lines 692-739)
**Original Weight**: 2.0
**Purpose**: Reward entries in empirically validated zones

**Empirical Zones** (from trading_pattern_analysis.json):
```yaml
optimal_zone: [25.0, 50.0]   # 75% success, 186-427% returns
good_zone: [10.0, 25.0]      # 61% success, 63-141% returns
conservative_zone: [1.0, 10.0]  # 36% success, 22-65% returns
```

**Key Logic**:
```python
def _calculate_zone_entry_reward(self, state_dict):
    if state_dict['action'] not in ['BUY_MAIN', 'BUY_SIDE', 'BUY_BOTH']:
        return 0.0

    multiplier = state_dict.get('current_price', 1.0)

    if 25.0 <= multiplier <= 50.0:
        return 10.0  # Optimal zone
    elif 10.0 <= multiplier <= 25.0:
        return 5.0   # Good zone
    elif 1.0 <= multiplier <= 10.0:
        return 2.0   # Conservative zone
    else:
        return 0.0   # Risky zone
```

#### 4B. Position Courage
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_position_courage_reward()` (lines 961-1007)
**Original Weight**: 4.0
**Purpose**: Reward BUY actions when conditions are favorable

**Key Logic** (Phase 0 Fix 3):
```python
def _calculate_position_courage_reward(self, state_dict):
    if state_dict['action'] not in ['BUY_MAIN', 'BUY_SIDE', 'BUY_BOTH']:
        return 0.0

    multiplier = state_dict.get('current_price', 1.0)
    rug_prob = state_dict.get('sidebet_rug_prob', 0.5)

    # Only reward if favorable conditions
    if rug_prob > 0.3:  # Too risky
        return 0.0

    # Zone-based rewards
    if 25.0 <= multiplier <= 50.0:
        return 20.0  # Optimal zone courage
    elif 10.0 <= multiplier <= 25.0:
        return 10.0  # Good zone courage
    else:
        return 5.0   # Any entry better than none
```

**Simplified Version** (reward_config_simplified.yaml):
```yaml
entry_quality:
  weight: 2.0
  zone_rewards:
    optimal_entry: 10.0    # 25-50x sweet spot
    good_entry: 5.0
    conservative_entry: 2.0
  optimal_zone: [25.0, 50.0]
  max_positions: 5
  min_confidence: 0.3  # Don't enter if rug_prob > 30%
```

---

### 5. Risk Management
**File**: `rugs_bot/training/reward_calculator.py`
**Weight**: 10.0
**Purpose**: Prevent catastrophic failures

**Critical Fix**:
```yaml
bankruptcy_penalty: -10.0  # REDUCED from -1000.0!
```

**Rationale**:
- Original -1000.0 dominated all other rewards
- Financial weight was only 3.0 → agent feared bankruptcy more than pursuing profit
- New balance: bankruptcy -10.0, financial +5.0 → profit-seeking with caution

**Components**:
- Bankruptcy penalty: -10.0
- Max drawdown threshold: 50%
- Drawdown penalty: -5.0

---

### 6. Pattern Bonus (Optional)
**File**: `rugs_bot/training/reward_calculator.py`
**Method**: `_calculate_pattern_boost()` (lines 879-913)
**Status**: Disabled in simplified config
**Purpose**: Reward complex multi-step patterns

**Patterns Tracked**:
- Quick profits (enter/exit < 20 ticks)
- Scalping (small gains, high frequency)
- Position scaling (partial sells)
- Emergency exits

**Reintegration**: Enable after basic system stable

---

## Removed Components (Advanced Features)

### 7. Temporal Penalty (REMOVED - Redundant)
**Original Location**: Lines 740-789
**Original Weight**: 3.0
**Purpose**: Increase exit urgency as game age increases

**Why Removed**: Redundant with rug_avoidance component (already penalizes late exits)

**Temporal Risk Model** (Empirical Data):
```python
TEMPORAL_RUG_PROB = {
    50: 0.234,   # 23.4% cumulative rug probability
    100: 0.386,  # 38.6%
    138: 0.500,  # 50% (median)
    200: 0.644,  # 64.4%
    300: 0.793   # 79.3%
}
```

**Reintegration Path**:
- Add tick-based urgency multiplier to rug_avoidance component
- Increase penalties linearly after median (138 ticks)

---

### 8. Survival Bonus (REMOVED - Redundant)
**Original Location**: Lines 790-833
**Original Weight**: 0.1
**Purpose**: Small reward for each tick survived

**Why Removed**: Redundant with financial component (holding profitable positions already rewarded through P&L)

---

### 9. Sweet Spot (MERGED into entry_quality)
**Original Location**: Lines 834-878
**Original Weight**: 1.0
**Purpose**: Extra reward for 25-50x entries

**Why Merged**: Now part of entry_quality zone rewards

---

### 10. Volatility Exit (NOT IMPLEMENTED - Use Sidebet Predictor)
**Planned Location**: Would be new method in reward_calculator.py
**Planned Weight**: 2.0
**Purpose**: Reward selling when sidebet predictor shows high rug risk

**Design**:
```python
def _calculate_volatility_exit_reward(self, state_dict):
    if state_dict['action'] not in ['SELL_MAIN_25', 'SELL_MAIN_100']:
        return 0.0

    rug_prob = state_dict.get('sidebet_rug_prob', 0.5)
    confidence = state_dict.get('sidebet_confidence', 0.0)

    # Reward selling when predictor says rug imminent
    if rug_prob >= 0.50 and confidence >= 0.7:
        return 15.0  # Critical exit
    elif rug_prob >= 0.40 and confidence >= 0.6:
        return 10.0  # Caution exit

    return 0.0
```

**Why Not Implemented**:
- Sidebet predictor integration pending
- Should add after basic system stable
- Requires 5 new observation features (probability, confidence, timing, flags)

**Reintegration Path**:
1. Complete SidebetPredictor integration (already in environment.py lines 79-96)
2. Add sidebet features to observation space (5 features)
3. Implement volatility_exit component
4. A/B test with/without

---

### 11. Scalping Bonuses (NOT IMPLEMENTED - Too Complex)
**Planned Weight**: 1.5
**Purpose**: Reward high-frequency small-profit trades

**Design**:
```python
scalping_bonuses:
  enabled: false  # Too complex for Phase 0
  quick_profit_bonus: 5.0   # < 20 tick hold
  min_profit_threshold: 0.0005  # 0.0005 SOL minimum
  frequency_multiplier: 1.2  # Bonus for multiple scalps
```

**Why Not Implemented**:
- Adds complexity without empirical validation
- May conflict with rug avoidance (encourages staying in game longer)
- Better to focus on core profitability first

**Reintegration Path**:
- Only add if data shows scalping is profitable
- Requires game-level state tracking (scalp_count)
- Risk: May encourage overtrading

---

## Empirical Analysis Data Sources

All advanced features are grounded in empirical analysis of 899 recorded games.

### Analysis Scripts

**Trading Patterns Analysis** (Entry opportunities, volatility, survival curves, profit distributions):
`/home/nomad/Desktop/REPLAYER/analyze_trading_patterns.py` (870 lines)
**Output**: `trading_pattern_analysis.json` (12KB)

**Position Duration Analysis** (Temporal risk, optimal hold times):
`/home/nomad/Desktop/REPLAYER/analyze_position_duration.py` (600 lines)
**Output**: `position_duration_analysis.json` (24KB)

### Key Empirical Findings

**1. Entry Zones** (140,611 samples):
```
1-10x:   36.3% success, 22-65% median returns
10-25x:  61.3% success, 63-141% median returns
25-50x:  75.0% success, 186-427% median returns ← SWEET SPOT
50-100x: 48.6% success, 107-273% median returns
100x+:   36.2% success, 10-25% median returns
```

**2. Temporal Risk Model**:
```
Median game lifespan: 138 ticks (50% of games rug by this point)
P25: 69 ticks (25% already dead)
P75: 268 ticks (75% already dead)
```

**3. Optimal Hold Times**:
```
1x entry:   65 ticks (61% success)
25x entry:  60 ticks (75% success) ← SWEET SPOT
50x entry:  48 ticks (75% success) ← SWEET SPOT
100x entry: 71 ticks (36% success)
```

**4. Drawdown Patterns**:
```
Average drawdown: 8-25% (varies by entry zone)
Recovery rate: 85-91% if game doesn't rug
Stop loss recommendation: 30-50% (not 10%)
```

**5. Survivor Bias Warning**:
```
Cannot plan "hold 300 ticks" - 79% of games already dead by then
Exit timing is EVERYTHING (100% of games eventually rug)
```

---

## Sidebet Predictor Integration

### Status
✅ **Phase 2 Complete**: Model trained (v3), wrapper class created, tests passing (38/38)
⏳ **Phase 3 Pending**: Integration into environment observation space

### Model Performance
- **Win Rate**: 38.1% (vs 16.7% random baseline)
- **ROI**: 754% (Martingale strategy)
- **Bankruptcy Rate**: 0% (200-game backtest)

### Integration Points

**Environment** (`rugs_bot/environment/environment.py`):
```python
# Lines 79-96: SidebetPredictor initialization
from rugs_bot.sidebet.predictor import SidebetPredictor

self.sidebet_predictor = SidebetPredictor(
    model_path='models/sidebet_v3_gb_model.pkl',
    scaler_path='models/sidebet_v3_gb_scaler.pkl'
)
```

**Observation Features** (5 per tick):
```python
{
    'probability': 0.0-1.0,        # Rug probability
    'confidence': 0.0-1.0,         # Prediction reliability
    'ticks_to_rug_norm': 0.0-1.0,  # Normalized timing estimate
    'is_critical': 0/1,            # Emergency flag (prob ≥ 0.50)
    'should_exit': 0/1             # Exit recommendation (prob ≥ 0.40)
}
```

**Predictor Class**:
`/home/nomad/Desktop/rugs-rl-bot/rugs_bot/sidebet/predictor.py` (365 lines)

**Tests**:
`/home/nomad/Desktop/rugs-rl-bot/tests/test_sidebet/test_predictor.py` (29 unit tests)
`/home/nomad/Desktop/rugs-rl-bot/tests/test_environment/test_sidebet_integration.py` (9 integration tests)

**Documentation**:
`/home/nomad/Desktop/rugs-rl-bot/REWARDS DESIGN AGENT DOCUMENTATION/sidebet_training/`

---

## Documentation Hierarchy

### Phase 1: Environment & Data Collection
- Session recordings: `/home/nomad/rugs_recordings/` (929 games)
- Data loader: `rugs_bot/data/session_data_loader.py`

### Phase 2: Sidebet Model Training
**Location**: `/home/nomad/Desktop/rugs-rl-bot/REWARDS DESIGN AGENT DOCUMENTATION/sidebet_training/`

- `TRAINING_RESULTS.md` - v1/v2/v3 model comparison
- `BACKTEST_RESULTS.md` - 200-game validation
- `FEATURE_ENGINEERING.md` - 14-dimensional feature vector
- `MARTINGALE_STRATEGY.md` - Bankroll management

### Phase 3: Empirical Analysis & Rewards Design
**Location**: `/home/nomad/Desktop/rugs-rl-bot/REWARDS DESIGN AGENT DOCUMENTATION/trading_bot/`

- `FILE_SHARING_CHECKLIST.md` (450 lines) - Session workflow
- `KEY_INSIGHTS.md` (267 lines) - Executive summary
- `EMPIRICAL_DATA.md` (1,252 lines) - Complete empirical findings
- `LLM_INSTRUCTIONS.md` (270 lines) - Agent role + deliverables
- `REWARD_DESIGN_PROMPT.md` (645 lines) - Master context
- ⏳ `QUESTIONS.md` (~700 lines) - Pending
- ⏳ `BUNDLE.md` (~700 lines) - Pending

### Phase 0: Initial Training (FAILED - Reward Hacking)
**Location**: `/home/nomad/Desktop/rugs-rl-bot/docs/`

- `PHASE0_EVALUATION_RESULTS.md` - Why the model failed
- `REWARD_HACKING_ANALYSIS.md` - SELL spam exploit

### Phase 0 Revision: This Session
**Location**: `/home/nomad/Desktop/rugs-rl-bot/`

- `ENVIRONMENT_AUDIT_REPORT.md` (500+ lines) - Comprehensive bug analysis
- `SCRIPTS_AUDIT_CHECKLIST.md` (278 lines) - Quick reference
- `REWARDS DESIGN AGENT DOCUMENTATION/trading_bot/CLAUDE.md` (this file)
- `REWARDS DESIGN AGENT DOCUMENTATION/trading_bot/CHANGELOG.md` (see next file)

---

## Implementation Files

### Core Environment
**File**: `rugs_bot/environment/environment.py` (1,019 lines)

**Key Methods**:
- `step()` (line 268) - Main Gymnasium interface
- `_execute_action()` (line 400) - Action execution logic
- `_validate_action()` (line 359) - Action validation
- `_get_state_dict()` (line 780) - State for reward calculation
- `reset()` (line 207) - Episode initialization

**Recent Changes**:
- Added BUY_BOTH handler (lines 518-570)
- Added EMERGENCY_EXIT handler (lines 571-584)
- Added state tracking (lines 182-184)

### Reward Calculator
**File**: `rugs_bot/training/reward_calculator.py` (1,043 lines)

**Architecture**:
```python
def calculate_reward(self, state_dict, prev_state):
    """Main entry point - calls all component methods"""
    total_reward = 0.0
    breakdown = {}

    for component_name, component_config in self.config.items():
        if not component_config.get('enabled', True):
            continue

        method_name = f"_calculate_{component_name}_reward"
        component_reward = getattr(self, method_name)(state_dict, prev_state)

        weight = component_config.get('weight', 1.0)
        weighted_reward = component_reward * weight

        breakdown[component_name] = weighted_reward
        total_reward += weighted_reward

    return total_reward, breakdown
```

**Component Methods** (all follow pattern `_calculate_<name>_reward()`):
- Financial (lines 544-597)
- Rug avoidance (lines 598-691)
- Zone entry (lines 692-739)
- Temporal penalty (lines 740-789)
- Survival bonus (lines 790-833)
- Sweet spot (lines 834-878)
- Pattern boost (lines 879-913)
- Inactivity (lines 914-960)
- Position courage (lines 961-1007)
- Opportunity cost (lines 1008-1043)

### Position Manager
**File**: `rugs_bot/training/position_manager.py` (233 lines)

**Key Methods**:
- `add_position()` (line 60) - Opens new position
- `has_positions()` (line 100) - Check if positions exist
- `sell_all()` (line 125) - Close all positions
- `sell_partial()` (line 139) - Close partial positions

### Sidebet Manager
**File**: `rugs_bot/training/sidebet_manager.py` (217 lines)

**Key Methods**:
- `place_sidebet()` (line 84) - Place new sidebet
- `has_active_bet()` (line 75) - Check if bet exists
- `resolve()` (line 119) - Resolve bet at game end

---

## Testing Infrastructure

### Unit Tests
**Location**: `/home/nomad/Desktop/rugs-rl-bot/tests/`

- `test_reward_fixes.py` (485 lines) - 16/16 tests passing
  - Fix 1: SELL with/without positions
  - Fix 2: Inactivity penalty in different zones
  - Fix 3: Position courage in different zones
  - Fix 4: Opportunity cost with/without positions

### Diagnostic Scripts
**Location**: `/home/nomad/Desktop/rugs-rl-bot/scripts/`

- `diagnose_trading_behavior.py` (189 lines) - Step-by-step action logging
- `evaluate_phase0_revised.py` (278 lines) - Reward hacking detection
- `train_phase0_revised.py` (139 lines) - Training script

### Evaluation Metrics
**Profitability**:
- ROI (bankroll growth)
- Total positions opened
- Engagement rate (% games with positions)

**Reward Hacking Detection**:
- SELL spam (>80% SELL actions)
- BUY spam (>80% BUY actions)
- Zero positions (ROI = 0%, positions = 0)
- Reward dominance (single component >98%)

---

## Known Bugs and Issues

### CRITICAL: Positions Not Opening
**Status**: ❌ UNRESOLVED
**Symptoms**:
- BUY_BOTH handlers execute (money deducts from bankroll)
- `position_manager.positions` remains empty (0 positions)
- 96% BUY_BOTH actions but 0% ROI, 0% engagement

**Evidence**:
```bash
Step 0: BUY_BOTH → NO position! (bankroll: 0.010000 → 0.009000)
Step 1: BUY_BOTH → NO position! (bankroll: 0.009000 → 0.009000)
...
Total BUY attempts: 223
Positions opened: 0
```

**Hypothesis**:
- `position_manager.add_position()` returns True but doesn't actually append to list
- OR tick/game_id parameters are invalid
- OR position list is being cleared somewhere unexpected

**Next Steps**:
1. Add debug logging inside `position_manager.add_position()`
2. Print `len(self.positions)` before and after append
3. Verify tick/game_id values are valid

### ACTION_SKIP Not Handled
**Status**: ⚠️ Pending fix
**File**: `rugs_bot/training/reward_calculator.py`
**Issue**: If agent selects ACTION_SKIP (type 7), reward calculator will error

**Fix**:
```python
def calculate_reward(self, state_dict, prev_state):
    action = state_dict.get('action')

    # Handle ACTION_SKIP early
    if action == 'SKIP':
        return 0.0, {}

    # ... rest of reward calculation
```

---

## Reintegration Roadmap

### Phase 0 Revision (Current)
**Goal**: Prove simplified 6-component system works

**Tasks**:
1. ✅ Add state tracking (games_completed, total_positions_taken)
2. ✅ Create simplified config (6 components)
3. ⏳ Handle ACTION_SKIP
4. ⏳ Debug position opening bug
5. ⏳ Train with simplified config (10k timesteps)
6. ⏳ Evaluate (must pass: ROI >5%, engagement >50%, no reward hacking)

### Phase 1: Merged Components
**Goal**: Add back activity and entry_quality

**Tasks**:
1. Implement `_calculate_activity_penalty()` (merge inactivity + opportunity_cost)
2. Implement `_calculate_entry_quality_reward()` (merge zone_entry + position_courage)
3. A/B test: 6-component vs 8-component
4. Target: ROI >10%, engagement >70%

### Phase 2: Advanced Features
**Goal**: Reintroduce sophisticated patterns

**Tasks**:
1. Complete SidebetPredictor integration (5 observation features)
2. Implement volatility_exit component
3. Re-enable pattern_boost component
4. A/B test each feature independently
5. Target: ROI >15%, rug avoidance >90%

### Phase 3: Meta Bot Coordination
**Goal**: Dual-strategy system (sidebet + trading bot)

**Tasks**:
1. Coordinate sidebet placements with position entries
2. Hedging strategies
3. Win multiplication (use sidebet profits for larger positions)
4. Portfolio optimization
5. Target: Combined ROI >25%

---

## References

### External Documentation
- Stable-Baselines3 docs: https://stable-baselines3.readthedocs.io/
- Gymnasium docs: https://gymnasium.farama.org/
- PPO paper: https://arxiv.org/abs/1707.06347

### Internal Documentation
- Project README: `/home/nomad/Desktop/rugs-rl-bot/README.md`
- Main CLAUDE.md: `/home/nomad/CLAUDE.md` (project overview)

---

## Changelog Reference

For chronological changes made during this session, see:
**`CHANGELOG.md`** (in this directory)

---

**Last Updated**: 2025-11-09
**Author**: Claude Code (AI Agent)
**Session**: Phase 0 Revision - Simplification and Bug Fixing
