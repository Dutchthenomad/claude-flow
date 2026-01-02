# 🎯 REWARD FUNCTION DESIGN SESSION: Rugs.fun RL Trading Bot

**Date**: November 7, 2025
**Purpose**: Deep dive reward function design for RL training
**Project**: Rugs.fun autonomous trading bot using Reinforcement Learning
**Context**: Previous training achieved 94.6% bankruptcy rate - need complete reward redesign

---

## 🎮 PROJECT OVERVIEW

### What is Rugs.fun?
A cryptocurrency trading game where:
- Players buy/sell positions with SOL tokens
- Games end randomly in "rugs" (instant liquidation events)
- Side bets allow hedging against rugs (5:1 payout)
- Each game lasts 2-8 minutes (50-600 ticks)
- Price multiplier starts at 1.0x and can reach 50x+

### What Are We Building?
An autonomous RL trading bot that:
- Learns from 857 recorded games
- Makes real-time BUY/SELL/SIDEBET decisions
- Manages multi-position portfolio (up to 10 positions)
- Maximizes profit while avoiding bankruptcy

### Why Reward Design Matters
**The Problem**: Previous training run ended in 94.6% bankruptcy because:
1. Bot holds positions through rugs (instant 100% loss)
2. Immediate rewards (+1.3) > delayed penalties (-2.5)
3. Bot doesn't recognize volatility spike warnings
4. No incentive to use sidebets strategically
5. Aggressive position sizing with no risk management

**The Goal**: Design a reward function that teaches the bot to:
- Exit positions BEFORE rugs (using volatility signals)
- Use sidebets as strategic hedges
- Be selective about entries (skip bad games)
- Manage risk and avoid bankruptcy
- Exploit validated statistical patterns

---

## 🎲 CRITICAL GAME MECHANICS

### **Rule #1: Instant Liquidation (THE MOST IMPORTANT)**
When game "rugs":
- ALL open positions → instant 100% loss
- Bankroll updates instantly
- No warning, no grace period
- Example: $1.00 bankroll + 1 position → $0 bankroll after rug

**Implication**: Holding through rug is CATASTROPHIC. Must exit early or hedge with sidebet.

### **Rule #2: Side Bets (5:1 Hedge)**
- Cost: 1 bet unit (e.g., 0.005 SOL)
- Payout: 5x if game rugs within 40 ticks
- Only 1 active sidebet at a time
- 5-tick cooldown between sidebets
- Can be placed in presale (-5 to 0) or active (0+)

**Implication**: Sidebets are INSURANCE against rugs. Strategic use = survival.

### **Rule #3: Presale Phase**
- Ticks -5 to 0 (before active trading)
- Guaranteed entry at 1.0x price
- Cannot sell during presale
- Strategic window for positioning

**Implication**: Presale offers safe entry but commits you to the game.

### **Rule #4: Multi-Position Management**
- Can hold up to 10 positions simultaneously
- Each position tracks: entry price, current P&L, hold duration
- Bankroll updates instantly on close
- Can partial sell (50%, 75%, 100%)

**Implication**: Portfolio management matters. Diversification vs concentration.

### **Rule #5: Volatility as Warning Signal**
- **CRITICAL FINDING**: 94.7% of games show >100% volatility spike before rug
- Mean spike: 664.7% (6.6x baseline volatility)
- Median: 551.6%, Max observed: 1,690%

**Implication**: Volatility is THE #1 exit signal. Must reward acting on it.

---

## 📊 CURRENT REWARD SYSTEM (13 Components)

### **Component Breakdown**:

1. **Financial P&L** (Primary) - Weight: 1.0
   - Direct profit/loss from trades
   - Realized P&L when positions close

2. **Pattern Exploitation** - Weight: 0.5-1.0
   - Bonuses for trading during validated patterns
   - 3 patterns: Post-Max-Payout, Ultra-Short, Moonshot

3. **Sidebet Timing** - Weight: 0.5-1.0
   - Bonuses for optimal sidebet placement
   - Presale vs active placement strategy

4. **Drawdown Penalties** - Weight: -0.5 to -2.0
   - Penalties for large bankroll losses
   - Progressive: -20% = -0.5, -50% = -2.0

5. **Bankruptcy Penalty** - Weight: -10.0
   - Massive penalty for going bankrupt
   - Terminal state penalty

6. **Invalid Action Penalty** - Weight: -0.1
   - Small penalties for rejected trades
   - Encourages learning valid actions

7. **Late Zone Entry Bonus** - Weight: +0.3
   - Rewards entering in profitable zone (2-4x)
   - Scalping strategy incentive

8. **Quick Exit Bonus** - Weight: +0.2
   - Rewards 10-15 tick holds (optimal)
   - Discourages holding too long

9. **Hold Too Long Penalty** - Weight: -0.1 to -0.5
   - Penalties for >30 tick holds
   - Risk increases with time

10. **Progressive Rug Hold Penalty** (AUDIT FIX) - Weight: -0.1 → -2.5 → -5.0
    - Escalating penalties for holding during danger signs
    - Volatility-based thresholds

11. **Volatility Exit Bonus** (THE #1 SIGNAL) - Weight: +0.5 to +3.0
    - Massive bonuses for exiting during volatility spikes
    - 2x baseline: +0.5, 5x: +1.5, 10x: +3.0

12. **Selective Entry Rewards** (SKIP 73%) - Weight: +0.2 to +0.5
    - Bonuses for skipping unprofitable games
    - Only 43.3% of games reach sweet spot
    - +0.2 for skipping, +0.5 for entering sweet spot

13. **Enhanced Sidebet Bonuses** (PRESALE +4.0 EV) - Weight: +1.0 to +2.0
    - Presale sidebets after patterns: +1.0
    - Pattern-guided sidebets: +0.5
    - Reduced loss penalties when hedged

### **Current Parameter Values** (from reward_config.yaml):
```yaml
financial_pnl:
  enabled: true
  weight: 1.0
  scale_factor: 1.0

pattern_exploitation:
  enabled: true
  base_bonus: 0.5
  high_value_bonus: 0.2
  confidence_threshold: 0.6

sidebet_timing:
  enabled: true
  presale_bonus: 1.0
  active_bonus: 0.5
  pattern_bonus: 0.2

drawdown_penalty:
  enabled: true
  moderate: -0.5  # 20-30% loss
  severe: -1.0    # 30-40% loss
  critical: -2.0  # 40%+ loss

bankruptcy_penalty:
  enabled: true
  value: -10.0

progressive_rug_hold:
  enabled: true
  levels:
    - threshold: 0.5      # 50% volatility
      penalty: -0.1
    - threshold: 1.0      # 100% volatility
      penalty: -2.5
    - threshold: 2.0      # 200% volatility
      penalty: -5.0

volatility_exit_bonus:
  enabled: true
  levels:
    - threshold: 2.0      # 2x baseline
      bonus: 0.5
    - threshold: 5.0      # 5x baseline
      bonus: 1.5
    - threshold: 10.0     # 10x baseline
      bonus: 3.0

selective_entry:
  enabled: true
  skip_bonus: 0.2
  sweet_spot_entry: 0.5
  bad_entry_penalty: -0.3
```

---

## 🔍 KEY STATISTICAL FINDINGS

### **Finding #1: Volatility Predicts Rugs (94.7% accuracy)**
**Source**: `volatility_tracker.py` analysis of 528 games

**Statistics**:
- Games with volatility spike before rug: 499/528 (94.7%)
- Mean volatility spike: 664.7% (6.6x baseline)
- Median spike: 551.6%
- 95th percentile: 1,173%
- Maximum observed: 1,690%

**Thresholds**:
- 2x baseline: Caution (early warning)
- 5x baseline: Warning (strong signal)
- 10x baseline: Emergency (exit immediately)

**Implication**: Volatility is THE most reliable exit signal. Rewards must heavily incentivize exits at high volatility.

---

### **Finding #2: Selective Entry (Only 43.3% Profitable)**
**Source**: `sweet_spot_detector.py` analysis

**Statistics**:
- Games reaching sweet spot (2-4x): 229/528 (43.3%)
- Games profitable overall: 27%
- Average duration in sweet spot: 68.7 ticks
- Skip rate to achieve 55% win rate: 73%

**Implication**: Patience is profitable. Bot must learn to skip bad games and only enter during favorable conditions.

---

### **Finding #3: Pattern Exploitation (Statistically Validated)**
**Source**: `PATTERN_EXPLOITATION_RESEARCH.md`

**Pattern 1: Post-Max-Payout Recovery**
- Ultra-short rate after high-peak games: 21.1% (vs 12.2% baseline)
- Edge: +72.7%
- Statistical significance: p = 0.0038
- Sample size: 155 games

**Pattern 2: Ultra-Short Arbitrage**
- Sidebet probability after ultra-short: 8.1% (vs 12.2% baseline)
- Edge: +25-50% in optimal conditions
- Weakly significant: p ≈ 0.05

**Pattern 3: Moonshot Momentum**
- Probability of reaching 20x given 8x: 50%
- Probability of reaching 20x given 12x: 65%
- Thresholds: 8x, 12x, 20x

**Implication**: Pattern-guided trading has proven edge. Rewards should incentivize pattern recognition.

---

### **Finding #4: Sidebet EV Analysis**
**Source**: `sidebet_ev_calculator.py`

**Formula**: EV = (P(win) × 5.0) - (P(lose) × 1.0)
**Breakeven**: P(win) = 16.67% (1 in 6)

**Pattern-Adjusted Probabilities**:
- Baseline: 12.2% → EV = -0.39 (NEGATIVE)
- Post-max-payout: 21.1% → EV = +0.16 (POSITIVE!)
- Post-long-game: 8.1% → EV = -0.59 (NEGATIVE)
- Presale (after pattern): 21%+ → EV = +4.0 (MASSIVE!)

**Implication**: Sidebets are profitable ONLY in specific conditions. Rewards must teach selectivity.

---

### **Finding #5: Optimal Hold Duration**
**Source**: `position_manager.py` analysis

**Statistics**:
- Optimal hold: 10-15 ticks (quick scalp)
- Average profitable hold: 23 ticks
- Hold >30 ticks: 68% rug rate
- Hold >50 ticks: 89% rug rate

**Implication**: Time in position = risk. Rewards should incentivize quick exits.

---

## ❌ WHAT FAILED IN PREVIOUS TRAINING

### **Failure Mode: 94.6% Bankruptcy Rate**

**Root Causes**:

1. **Immediate vs Delayed Rewards**
   - Pattern bonus: +1.3 (immediate)
   - Rug penalty: -2.5 (delayed by 20+ ticks)
   - Bot learned: "Take pattern bonus now, worry about rug later"

2. **No Volatility Awareness**
   - Volatility exit bonus: +0.5 to +3.0
   - Bot never learned to check volatility
   - Held positions through 664.7% spikes

3. **No Selective Entry**
   - Skip bonus: +0.2 (weak)
   - Bad entry penalty: -0.3 (weak)
   - Bot tried to trade every game

4. **Inadequate Sidebet Incentives**
   - Sidebet bonuses: +0.5 to +1.0
   - Not enough to overcome cost (1.0)
   - Bot rarely used sidebets

5. **Weak Rug Hold Penalties**
   - Progressive penalties: -0.1 → -2.5 → -5.0
   - Not steep enough vs potential profits
   - Bot ignored warnings

---

## 🎯 DESIGN OBJECTIVES

### **Primary Objective: Prevent Bankruptcy**
- Target: <5% bankruptcy rate (vs 94.6% current)
- Strategies: Early exits, sidebet hedging, risk management

### **Secondary Objective: Profitable Trading**
- Target: >55% win rate (vs 27% baseline)
- Target: >5% bankroll growth per 15-game episode
- Target: <30% max drawdown

### **Tertiary Objective: Pattern Exploitation**
- Target: >80% pattern recognition rate
- Target: 2x improvement early vs late training
- Target: Cross-game learning visible

---

## 🔧 AVAILABLE OBSERVATIONS (What the Bot Can See)

### **Current State** (10 features):
- `price`: Current multiplier (1.0x to 50x+)
- `tick`: Current tick number (-5 to 600)
- `phase`: PRESALE, ACTIVE, RUGGED
- `has_positions`: Boolean
- `bankroll`: Current SOL balance
- `rugged`: Boolean (game ended)
- `position_count`: Number of open positions (0-10)
- `volatility_baseline`: Rolling baseline volatility
- `volatility_current`: Current volatility
- `volatility_ratio`: Current / baseline (THE #1 SIGNAL)

### **Price History** (20 features):
- Last 20 tick prices
- For trend and pattern detection

### **Positions** (30 features - 10 positions × 3 each):
- `entry_price`: Price when bought
- `current_pnl`: Unrealized profit/loss
- `ticks_held`: How long position has been open

### **Sidebets** (3 features):
- `has_active_sidebet`: Boolean
- `sidebet_ticks_remaining`: Time left (0-40)
- `sidebet_amount`: Bet size

### **Meta Context** (24 features):
- Pattern signals (post-max-payout, ultra-short, moonshot)
- Pattern confidence scores
- Sweet spot detection
- Last 5 games history
- Cross-game patterns

**Total**: 70 dimensions of observation space

---

## 🎮 AVAILABLE ACTIONS (What the Bot Can Do)

### **Simple Action Space** (3 actions):
- 0 = WAIT (do nothing)
- 1 = BUY (open position, 0.005 SOL)
- 2 = SELL (close all positions)

### **Advanced Action Space** (8 actions - optional):
- 0 = WAIT
- 1 = BUY_SMALL (0.002 SOL)
- 2 = BUY_MEDIUM (0.005 SOL)
- 3 = BUY_LARGE (0.010 SOL)
- 4 = SELL_PARTIAL (50%)
- 5 = SELL_ALL
- 6 = PLACE_SIDEBET
- 7 = EMERGENCY_EXIT

**Note**: Currently using simple 3-action space. Can expand if needed.

---

## 🧪 TRAINING SETUP

### **Algorithm**: PPO (Proximal Policy Optimization)
- Stable-Baselines3 implementation
- Clips gradients (prevents large policy updates)
- Benefits from shaped rewards
- Epochs: 10, Batch: 64, Learning rate: 3e-4

### **Episodes**: 15 consecutive games per episode
- Persistent bankroll across games
- Cross-game pattern learning
- Episode terminates on bankruptcy or 15 games

### **Data**: 857 recorded games
- Real game data (JSONL format)
- Socket.IO feed (100% accurate)
- Covers wide variety of game outcomes

### **Environment**: ReplayerGymEnv
- Uses REPLAYER's actual GameState, TradeManager, ReplayEngine
- NO simulation - direct integration with ground truth
- Zero sim-to-real gap

---

## 🎯 DESIGN QUESTIONS TO ADDRESS

### **Q1: Component Rebalancing**
Given the bankruptcy problem and statistical findings, **which reward components need weight adjustments?**

**Consider**:
- Should volatility exit bonuses be even higher? (+3.0 → +5.0?)
- Should rug hold penalties be more aggressive? (-5.0 → -10.0?)
- Should selective entry bonuses be stronger? (+0.2 → +1.0?)

---

### **Q2: Missing Components**
Are there reward components we **SHOULD have but don't?**

**Candidates**:
- Presale entry timing (strategic presale buys)
- Emergency exit rewards (panic sell during danger)
- Cross-game learning rewards (pattern recognition improving)
- Risk-adjusted returns (Sharpe ratio bonuses)
- Drawdown recovery bonuses (bounce back from losses)
- Portfolio diversity rewards (multiple positions vs concentration)
- Time-in-market penalties (opportunity cost)

---

### **Q3: Penalty Structure**
**Is the progressive rug hold penalty aggressive enough?**

**Current**: -0.1 (50% vol) → -2.5 (100% vol) → -5.0 (200% vol)

**Questions**:
- Should it scale exponentially instead of linearly?
- Should it compound with time (longer hold = worse penalty)?
- Should it vary with position size (larger position = worse penalty)?
- Should it consider portfolio exposure (all-in vs diversified)?

---

### **Q4: Immediate vs Delayed Rewards**
**How to balance immediate rewards with delayed penalties?**

**Problem**: Bot takes +1.3 pattern bonus (immediate) and ignores -2.5 rug penalty (delayed 20+ ticks)

**Solutions to consider**:
- Temporal discounting (γ = 0.99 already applied by PPO)
- Increase delayed penalties to overwhelm immediate rewards
- Add immediate warnings (penalty for ignoring volatility spike)
- Reward anticipation (bonus for exiting BEFORE high volatility)

---

### **Q5: Pattern Integration**
**How should statistical significance affect reward magnitude?**

**Current patterns**:
- Post-max-payout: p = 0.0038 (highly significant) → +0.5 bonus
- Ultra-short: p ≈ 0.05 (weakly significant) → +0.5 bonus
- Moonshot: p ≈ 0.01 (significant) → +0.25 bonus

**Questions**:
- Should reward scale with p-value? (p=0.0038 gets +1.0, p=0.05 gets +0.2)
- Should confidence threshold matter? (only reward high-confidence patterns)
- Should pattern bonuses compound? (multiple patterns = multiplicative bonus)

---

### **Q6: Sidebet Strategy**
**How to incentivize sidebets WITHOUT over-encouraging?**

**Facts**:
- Presale sidebets after patterns: +4.0 EV (AMAZING)
- Random sidebets: -0.39 EV (TERRIBLE)
- Cost: 1.0 per sidebet

**Current rewards**:
- Presale sidebet: +1.0
- Active sidebet: +0.5
- Pattern-guided: +0.2

**Questions**:
- Should presale sidebet bonus be MUCH higher? (+1.0 → +3.0?)
- Should random sidebets be penalized more? (no pattern → -0.5 penalty)
- Should sidebet success affect future sidebet rewards? (winning streak bonuses)

---

### **Q7: Risk Management**
**How to reward conservative play (survival) while encouraging profitable trades?**

**Tension**:
- Conservative play: Skip games, use sidebets, exit early → survival
- Aggressive play: Enter every game, hold longer → potentially higher profits

**Questions**:
- Should there be a "survival bonus" for maintaining bankroll above threshold?
- Should risk-adjusted returns (Sharpe ratio) be rewarded?
- Should drawdown limits trigger protective behaviors?
- Should bankroll growth rate matter? (slow steady vs volatile)

---

### **Q8: Multi-Game Episodes**
**How to reward long-term bankroll growth vs short-term P&L?**

**Current**: Episodes = 15 games with persistent bankroll

**Questions**:
- Should rewards care about episode-level performance? (end-of-episode bonus)
- Should bankroll growth rate be rewarded separately? (beyond P&L)
- Should consecutive wins/losses affect rewards? (streak bonuses/penalties)
- Should cross-game patterns be rewarded? (recognizing post-max-payout)

---

## 🚧 DESIGN CONSTRAINTS

### **Hard Constraints (CANNOT change)**:
1. Rug = instant 100% loss (game mechanic)
2. Sidebet window = 40 ticks (game mechanic)
3. Sidebet cooldown = 5 ticks (game mechanic)
4. Only 1 active sidebet (game mechanic)
5. Observation space = 70 dimensions (fixed)
6. Action space = 3 actions (fixed for now)
7. PPO algorithm (clips gradients, uses advantage function)
8. Episode length = 15 games (design choice)

### **Soft Constraints (CAN change)**:
1. Reward component weights (fully tunable)
2. Reward scaling factors (can adjust)
3. Threshold values (volatility levels, hold duration, etc.)
4. Bonus/penalty magnitudes (can increase/decrease)
5. Component enable/disable (can add/remove)

---

## 📝 EXPECTED OUTPUTS

### **Primary Deliverables**:

1. **Revised reward_config.yaml**
   - New parameter values for all components
   - Added components (if any)
   - Removed components (if any)
   - Justification comments in YAML

2. **Justification Document**
   - Why each change was made
   - Expected behavioral impact
   - Risk analysis

3. **Testing Strategy**
   - How to validate new reward function
   - Metrics to monitor
   - Success criteria

---

## 🔗 REFERENCE MATERIALS

### **Must Read** (Priority 1):
1. `reward_calculator.py` (405 lines) - Current implementation
2. `RUGS_GAME_MECHANICS_KNOWLEDGE_BASE.md` (513 lines) - Game rules + bankruptcy lessons
3. `reward_config.yaml` (320 lines) - All parameters

### **Core Context** (Priority 2):
4. `volatility_tracker.py` (156 lines) - THE #1 exit signal
5. `PATTERN_EXPLOITATION_RESEARCH.md` (627 lines) - Statistical validation
6. `pattern_detector.py` (293 lines) - Pattern implementation
7. `environment.py` (920 lines) - Observations/actions available

### **Supporting** (Priority 3):
8. `sweet_spot_detector.py` (150 lines) - Selective entry
9. `sidebet_ev_calculator.py` (121 lines) - EV formulas
10. `GYMNASIUM_DESIGN_SPEC.md` (1,341 lines) - Technical spec

(See REWARD_DESIGN_BUNDLE.md for complete list with paths)

---

## 🎓 KEY INSIGHTS FOR DESIGN

1. **Bankruptcy is the #1 problem** - Must be solved first
2. **Volatility is the #1 signal** - 94.7% predictive accuracy
3. **Selective entry matters** - Skip 73% of unprofitable games
4. **Sidebets need strategy** - +4.0 EV when done right, -0.39 EV when random
5. **Immediate > Delayed** - Bot prefers immediate rewards over delayed penalties
6. **Patterns have proven edge** - +72.7% for post-max-payout (p=0.0038)
7. **Time = Risk** - Holding >30 ticks = 68% rug rate
8. **Multi-game learning** - Episodes span 15 games, cross-game patterns exist

---

## 🚀 SUCCESS CRITERIA

### **Performance Targets**:
- Bankruptcy rate: <5% (vs 94.6% current) ✓ PRIMARY
- Win rate: >55% (vs 27% baseline) ✓
- Bankroll growth: >5% per episode ✓
- Max drawdown: <30% ✓
- Pattern recognition: >80% of opportunities ✓

### **Behavioral Targets**:
- Bot exits during volatility spikes (10x = emergency exit)
- Bot skips unprofitable games (selective entry)
- Bot uses sidebets strategically (presale after patterns)
- Bot manages risk (position sizing, diversification)
- Bot learns cross-game patterns (improves over episode)

---

**BEGIN REWARD DESIGN SESSION**

You have all the context. Now design the optimal reward function for this RL trading bot.

Focus on solving the bankruptcy problem while maintaining profitability.

Good luck! 🎯
