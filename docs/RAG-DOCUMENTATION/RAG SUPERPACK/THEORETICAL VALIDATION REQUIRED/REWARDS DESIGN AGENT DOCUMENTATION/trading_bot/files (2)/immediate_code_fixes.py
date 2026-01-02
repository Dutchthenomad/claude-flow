"""
IMMEDIATE CODE FIXES FOR RL TRAINING PROJECT
Copy-paste these fixes directly into your codebase
Date: November 9, 2025
"""

# ==============================================================================
# FIX 1: reward_calculator.py - Add position check for rug avoidance
# Location: Around line 607 in _calculate_rug_avoidance_reward
# ==============================================================================

def _calculate_rug_avoidance_reward(
    self,
    state: Dict[str, Any],
    action: Dict[str, Any],
    next_state: Dict[str, Any]
) -> float:
    """
    Component 14: Rug Avoidance Reward (FIXED)
    
    CRITICAL FIX: Check for positions before rewarding exits
    """
    # FIX 1: CRITICAL - Must have positions to get exit rewards
    if not state.get('has_positions', False):
        return 0.0  # No reward without positions to exit!
    
    action_type = action.get('action_type')
    
    # Only reward exit actions
    if action_type not in [self.ACTION_SELL_MAIN, self.ACTION_PARTIAL_SELL, self.ACTION_EMERGENCY_EXIT]:
        return 0.0
    
    # Check if we actually avoided a rug
    if not next_state.get('game_rugged', False):
        return 0.0  # Game didn't rug, no avoidance reward
    
    # Get sidebet prediction confidence
    rug_prediction = state.get('rug_prediction', {})
    rug_prob = rug_prediction.get('probability', 0.0)
    confidence = rug_prediction.get('confidence', 0.0)
    ticks_to_rug_norm = rug_prediction.get('ticks_to_rug_norm', 1.0)
    
    # Minimum thresholds
    if confidence < self.rug_min_confidence:
        return 0.0
    
    # Calculate base reward based on risk level
    base_reward = 0.0
    if rug_prob >= 0.50:  # Critical
        base_reward = self.rug_critical_avoided  # 100.0
    elif rug_prob >= 0.40:  # High
        base_reward = self.rug_high_avoided  # 60.0
    elif rug_prob >= 0.30:  # Medium
        base_reward = self.rug_medium_avoided  # 30.0
    else:
        return 0.0  # Risk too low
    
    # Apply confidence multiplier (squared for emphasis)
    confidence_multiplier = confidence ** 2
    
    # Apply urgency multiplier (higher reward for last-second escapes)
    urgency = 1.0 + (1.0 - ticks_to_rug_norm) * (self.rug_urgency_max - 1.0)
    
    return base_reward * confidence_multiplier * urgency


# ==============================================================================
# FIX 2: environment.py - Add state tracking for opportunity cost
# Add these to the __init__ method around line 180
# ==============================================================================

class RugsMultiGameEnv(gym.Env):
    def __init__(self, ...):
        # ... existing init code ...
        
        # ADD: Episode-level tracking for opportunity cost
        self.games_completed = 0
        self.total_positions_taken = 0
        self.action_counts = np.zeros(8)  # Track action distribution
        self.bankruptcy_count = 0
        self.episode_rewards = []
        
        # ... rest of init ...


# ==============================================================================
# FIX 3: environment.py - Update state tracking in step()
# Add to step() method around line 350-400
# ==============================================================================

def step(self, action: np.ndarray) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict]:
    # ... existing step code ...
    
    # ADD: Track action distribution
    action_type = action[0]
    self.action_counts[action_type] += 1
    
    # ADD: Track position entries
    if action_type in [self.ACTION_BUY_MAIN, self.ACTION_BUY_BOTH]:
        self.total_positions_taken += 1
    
    # ... existing action handling ...
    
    # After game completion check (around line 385)
    if game_ended:
        self.games_completed += 1
    
    # In bankruptcy check
    if self.bankroll < self.bankroll_threshold:
        self.bankruptcy_count += 1
    
    # ... rest of step ...


# ==============================================================================
# FIX 4: environment.py - Add missing state fields to _get_reward_state()
# Update around line 960
# ==============================================================================

def _get_reward_state(self) -> Dict[str, Any]:
    """Get state dict for reward calculation (FIXED)"""
    # ... existing state construction ...
    
    return {
        # ... existing fields ...
        
        # ADD: Missing fields for opportunity cost
        'games_completed': self.games_completed,
        'total_positions_taken': self.total_positions_taken,
        'position_count': len(self.position_manager.positions),  # ADD if missing
        
        # ... rest of return dict ...
    }


# ==============================================================================
# FIX 5: reward_calculator.py - Handle ACTION_SKIP
# Add to calculate_reward() method around line 300
# ==============================================================================

def calculate_reward(
    self,
    state: Dict[str, Any],
    action: Dict[str, Any],
    next_state: Dict[str, Any]
) -> float:
    """Calculate total reward (FIXED)"""
    
    action_type = action.get('action_type')
    
    # ADD: Handle ACTION_SKIP
    if action_type == self.ACTION_SKIP:
        # Small penalty for skipping (encourage engagement)
        # But less than penalty for bad trades
        return -0.1
    
    # ... rest of existing calculation ...


# ==============================================================================
# FIX 6: sidebet_manager.py - Fix payout calculation
# Update line 113
# ==============================================================================

def resolve(self, game_rugged: bool, rug_tick: Optional[int], current_tick: int) -> float:
    """Resolve active side bet (FIXED)"""
    if not self.has_active_bet():
        return 0.0
    
    payout = 0.0
    
    if game_rugged and rug_tick is not None:
        ticks_after_placement = rug_tick - self.active_bet.placed_tick
        
        if ticks_after_placement <= self.TICK_WINDOW:
            # FIX: Return total payout (bet + winnings)
            # 5:1 payout means 5x profit PLUS original bet = 6x total
            payout = self.active_bet.amount * (1 + self.PAYOUT_MULTIPLIER)
        else:
            payout = 0.0  # Lost - outside window
    else:
        payout = 0.0  # Lost - didn't rug
    
    self.active_bet = None
    return payout


# ==============================================================================
# FIX 7: position_manager.py - Improve partial sell precision
# Update around line 185
# ==============================================================================

def sell_partial(self, current_price: float, percent: float) -> float:
    """Sell a percentage of all positions (FIXED)"""
    if not self.positions or percent <= 0.0:
        return 0.0
    
    if percent >= 1.0:
        return self.sell_all(current_price)
    
    # FIX: Use Decimal for precision or round appropriately
    from decimal import Decimal, ROUND_DOWN
    
    total_pnl = self.get_aggregate_pnl(current_price)
    realized_pnl = float(Decimal(str(total_pnl)) * Decimal(str(percent)))
    
    # Update positions with better precision
    new_positions = []
    for position in self.positions:
        new_amount = float(
            Decimal(str(position.amount)) * 
            (Decimal('1') - Decimal(str(percent)))
        )
        if new_amount > 0.001:  # Minimum position size (0.001 SOL)
            position.amount = new_amount
            new_positions.append(position)
    
    self.positions = new_positions
    return realized_pnl


# ==============================================================================
# FIX 8: environment.py - Add diagnostic logging
# Add new method around line 1080
# ==============================================================================

def _log_diagnostics(self):
    """Log diagnostic metrics for debugging"""
    if self.games_completed == 0:
        return
    
    metrics = {
        'episode': self.episode_count,
        'games_completed': self.games_completed,
        'avg_positions_per_game': self.total_positions_taken / self.games_completed,
        'bankruptcy_rate': self.bankruptcy_count / max(1, self.episode_count),
        'action_distribution': {
            'WAIT': float(self.action_counts[0] / max(1, self.action_counts.sum())),
            'BUY_MAIN': float(self.action_counts[1] / max(1, self.action_counts.sum())),
            'SELL_MAIN': float(self.action_counts[2] / max(1, self.action_counts.sum())),
            'BUY_SIDE': float(self.action_counts[3] / max(1, self.action_counts.sum())),
            'BUY_BOTH': float(self.action_counts[4] / max(1, self.action_counts.sum())),
            'EMERGENCY_EXIT': float(self.action_counts[5] / max(1, self.action_counts.sum())),
            'PARTIAL_SELL': float(self.action_counts[6] / max(1, self.action_counts.sum())),
            'SKIP': float(self.action_counts[7] / max(1, self.action_counts.sum())),
        },
        'current_bankroll': self.bankroll,
    }
    
    print(f"\n=== DIAGNOSTIC METRICS ===")
    print(f"Episode: {metrics['episode']}")
    print(f"Avg positions/game: {metrics['avg_positions_per_game']:.2f}")
    print(f"Bankruptcy rate: {metrics['bankruptcy_rate']:.2%}")
    print(f"Current bankroll: {metrics['current_bankroll']:.4f} SOL")
    print(f"Action distribution:")
    for action, pct in metrics['action_distribution'].items():
        print(f"  {action}: {pct:.1%}")
    print("=" * 25)

# Call in step() every 1000 steps:
if self.step_count % 1000 == 0:
    self._log_diagnostics()


# ==============================================================================
# FIX 9: Simplified reward config (save as reward_config_simplified.yaml)
# ==============================================================================

"""
# Simplified Reward Configuration
# Focus on core behaviors only

global:
  reward_clip: 50.0
  enabled_components:
    - financial
    - rug_avoidance  
    - activity
    - risk_management

# Core component: Profit/Loss
financial:
  enabled: true
  weight: 5.0
  description: "Primary objective - make money"

# Core component: Avoid rugs
rug_avoidance:
  enabled: true
  weight: 5.0
  critical_avoided: 10.0  # Reduced from 100
  high_avoided: 6.0       # Reduced from 60
  medium_avoided: 3.0     # Reduced from 30
  min_confidence: 0.60
  require_positions: true  # CRITICAL FLAG
  description: "Exit before rugs WITH positions"

# Core component: Stay active
activity:
  enabled: true
  weight: 3.0
  inactivity_penalty: -2.0
  min_positions_per_episode: 5
  description: "Prevent passive waiting"

# Core component: Risk management  
risk_management:
  enabled: true
  weight: 2.0
  bankruptcy_penalty: 10.0  # Reduced from 1000!
  drawdown_threshold: 0.5
  drawdown_penalty: 2.0
  description: "Avoid bankruptcy and large drawdowns"
"""


# ==============================================================================
# FIX 10: Quick training loop diagnostic
# Add to your training script
# ==============================================================================

def diagnose_training(env, agent, n_steps=1000):
    """Quick diagnostic to verify fixes are working"""
    
    obs, _ = env.reset()
    action_counts = np.zeros(8)
    rewards = []
    positions_taken = 0
    
    for step in range(n_steps):
        # Get action from agent
        action, _ = agent.predict(obs, deterministic=False)
        
        # Track action
        action_counts[action[0]] += 1
        if action[0] in [1, 4]:  # BUY_MAIN or BUY_BOTH
            positions_taken += 1
        
        # Step environment
        obs, reward, terminated, truncated, info = env.step(action)
        rewards.append(reward)
        
        if terminated or truncated:
            obs, _ = env.reset()
    
    # Print diagnostics
    print("\n=== TRAINING DIAGNOSTIC (1000 steps) ===")
    print(f"Avg reward: {np.mean(rewards):.4f}")
    print(f"Reward std: {np.std(rewards):.4f}")
    print(f"Positions taken: {positions_taken}")
    print(f"Action distribution:")
    for i, count in enumerate(action_counts):
        print(f"  Action {i}: {count/n_steps:.1%}")
    
    # Check for red flags
    if action_counts[2] / n_steps > 0.5:  # >50% SELL
        print("⚠️  WARNING: Excessive SELL actions!")
    if positions_taken < 10:
        print("⚠️  WARNING: Very low trading activity!")
    if np.mean(rewards) < -1:
        print("⚠️  WARNING: Very negative rewards!")
    
    print("=" * 40)
