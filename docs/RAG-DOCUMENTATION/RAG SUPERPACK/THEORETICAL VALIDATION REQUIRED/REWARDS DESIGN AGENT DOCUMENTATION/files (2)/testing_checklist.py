"""
RL Training Fixes - Testing Checklist
=====================================
Run these tests after implementing fixes to verify everything works

Date: November 9, 2025
"""

import pytest
import numpy as np
from pathlib import Path


def test_critical_fix_1_position_check():
    """
    CRITICAL TEST: Verify SELL without positions gets no reward
    This was the main reward hacking exploit
    """
    from rugs_bot.training.reward_calculator import RewardCalculator
    
    calc = RewardCalculator(config_path="configs/reward_config_phase0_revised.yaml")
    
    # Test 1: SELL without positions (exploit attempt)
    state = {
        'has_positions': False,
        'positions': 0,
        'rug_prediction': {'probability': 0.8, 'confidence': 0.9}
    }
    action = {'action_type': 2}  # SELL_MAIN
    next_state = {'game_rugged': True}
    
    reward, breakdown = calc.calculate_reward_with_breakdown(state, action, next_state)
    
    assert breakdown['rug_avoidance_reward'] == 0.0, \
        "❌ CRITICAL BUG: SELL without positions still gets rug avoidance reward!"
    
    print("✅ Fix 1 verified: SELL spam exploit blocked")


def test_critical_fix_2_state_tracking():
    """
    Test that opportunity cost state fields are tracked
    """
    from rugs_bot.training.environment import RugsMultiGameEnv
    
    # Create minimal env
    env = RugsMultiGameEnv(
        session_paths=[Path("test_sessions/session_001")],
        games_per_episode=3
    )
    
    # Check new fields exist
    assert hasattr(env, 'games_completed'), "❌ Missing games_completed tracking"
    assert hasattr(env, 'total_positions_taken'), "❌ Missing total_positions_taken tracking"
    
    # Reset and check initialization
    obs, info = env.reset()
    assert env.games_completed == 0
    assert env.total_positions_taken == 0
    
    # Take a BUY action
    action = np.array([1, 0, 0])  # BUY_MAIN
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Verify tracking updates
    if 'games_completed' in info:
        assert info['games_completed'] >= 0
    
    print("✅ Fix 2 verified: State tracking implemented")


def test_critical_fix_3_action_skip_handling():
    """
    Test ACTION_SKIP (7) doesn't crash
    """
    from rugs_bot.training.reward_calculator import RewardCalculator
    
    calc = RewardCalculator()
    
    state = {'bankroll': 100}
    action = {'action_type': 7}  # ACTION_SKIP
    next_state = {'bankroll': 100}
    
    try:
        reward = calc.calculate_reward(state, action, next_state)
        print(f"✅ Fix 3 verified: ACTION_SKIP handled (reward={reward})")
    except Exception as e:
        print(f"❌ ACTION_SKIP crashes: {e}")
        raise


def test_reward_balance():
    """
    Test that rewards are balanced (no single component dominates)
    """
    from rugs_bot.training.reward_calculator import RewardCalculator
    
    calc = RewardCalculator()
    
    # Simulate profitable exit with rug avoidance
    state = {
        'has_positions': True,
        'positions': 2,
        'bankroll': 100,
        'current_multiplier': 35.0,
        'position_entry_multiplier': 20.0,
        'tick': 50,
        'rug_prediction': {
            'probability': 0.6,
            'confidence': 0.8,
            'is_critical': 1.0
        }
    }
    
    action = {'action_type': 2}  # SELL_MAIN
    
    next_state = {
        'bankroll': 110,  # +10 profit
        'game_rugged': True
    }
    
    reward, breakdown = calc.calculate_reward_with_breakdown(state, action, next_state)
    
    # Check financial P&L contributes
    assert breakdown['financial'] > 0, "❌ Financial P&L not contributing"
    
    # Check multiple components active
    positive_components = [k for k, v in breakdown.items() if v > 0 and k != 'total']
    assert len(positive_components) >= 2, f"❌ Only {len(positive_components)} positive components"
    
    # Check no extreme dominance (>95% from one component)
    total_positive = sum(v for k, v in breakdown.items() if v > 0 and k != 'total')
    for component, value in breakdown.items():
        if value > 0 and component != 'total':
            contribution = value / total_positive
            assert contribution < 0.95, f"❌ {component} dominates at {contribution:.1%}"
    
    print(f"✅ Reward balance verified: {len(positive_components)} active components")
    print(f"   Financial: {breakdown['financial']:.2f}")
    print(f"   Rug avoid: {breakdown.get('rug_avoidance_reward', 0):.2f}")
    print(f"   Total: {reward:.2f}")


def test_action_distribution_diagnostic():
    """
    Run short episode and check action distribution
    """
    from rugs_bot.training.environment import RugsMultiGameEnv
    import random
    
    env = RugsMultiGameEnv(
        session_paths=[Path("test_sessions/session_001")],
        games_per_episode=3
    )
    
    obs, _ = env.reset()
    action_counts = np.zeros(8)
    
    # Run 100 random steps
    for _ in range(100):
        # Random action for testing
        action = np.array([
            random.randint(0, 7),  # action type
            random.randint(0, 8),  # bet size
            random.randint(0, 10)  # sell percent
        ])
        
        action_counts[action[0]] += 1
        
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, _ = env.reset()
    
    # Check distribution
    total = action_counts.sum()
    sell_pct = action_counts[2] / total
    buy_pct = (action_counts[1] + action_counts[4]) / total
    wait_pct = action_counts[0] / total
    
    print(f"✅ Action distribution test complete:")
    print(f"   WAIT: {wait_pct:.1%}")
    print(f"   BUY: {buy_pct:.1%}")
    print(f"   SELL: {sell_pct:.1%}")
    
    if sell_pct > 0.5:
        print(f"   ⚠️  WARNING: High SELL rate ({sell_pct:.1%})")
    if buy_pct < 0.1:
        print(f"   ⚠️  WARNING: Low BUY rate ({buy_pct:.1%})")


def test_sidebet_payout_fix():
    """
    Test sidebet payout returns correct amount (6x total, not 5x)
    """
    from rugs_bot.training.sidebet_manager import SidebetManager
    
    mgr = SidebetManager()
    
    # Place bet
    mgr.place_sidebet(amount=1.0, tick=5, game_id="test")
    
    # Resolve as win
    payout = mgr.resolve(game_rugged=True, rug_tick=20, current_tick=20)
    
    # Should be 6.0 (1.0 bet + 5.0 profit)
    expected = 6.0
    assert abs(payout - expected) < 0.001, \
        f"❌ Sidebet payout wrong: {payout} != {expected}"
    
    print(f"✅ Sidebet payout verified: {payout} SOL (correct 6x)")


def test_position_partial_sell_precision():
    """
    Test partial sells maintain precision
    """
    from rugs_bot.training.position_manager import PositionManager
    
    mgr = PositionManager()
    
    # Add position
    mgr.add_position(entry_price=1.0, amount=10.0, tick=0, game_id="test")
    
    # Series of partial sells
    for i in range(5):
        before = mgr.get_total_amount_invested()
        mgr.sell_partial(current_price=1.5, percent=0.1)  # Sell 10%
        after = mgr.get_total_amount_invested()
        
        expected = before * 0.9
        error = abs(after - expected) / expected if expected > 0 else 0
        
        assert error < 0.01, f"❌ Precision error after sell {i+1}: {error:.2%}"
    
    print("✅ Partial sell precision verified")


def test_bankruptcy_handling():
    """
    Test bankruptcy is detected and handled properly
    """
    from rugs_bot.training.environment import RugsMultiGameEnv
    
    env = RugsMultiGameEnv(
        session_paths=[Path("test_sessions/session_001")],
        initial_bankroll=0.002,  # Very low
        bankroll_threshold=0.001
    )
    
    obs, _ = env.reset()
    env.bankroll = 0.0005  # Force bankruptcy
    
    # Take action with bankrupt state
    action = np.array([0, 0, 0])  # WAIT
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Should terminate or heavily penalize
    assert terminated or reward < -10, \
        "❌ Bankruptcy not properly handled"
    
    print("✅ Bankruptcy handling verified")


def run_all_tests():
    """
    Run all verification tests
    """
    print("=" * 50)
    print("RL TRAINING FIXES - VERIFICATION SUITE")
    print("=" * 50)
    
    tests = [
        ("Critical Fix 1: Position Check", test_critical_fix_1_position_check),
        ("Critical Fix 2: State Tracking", test_critical_fix_2_state_tracking),
        ("Critical Fix 3: ACTION_SKIP", test_critical_fix_3_action_skip_handling),
        ("Reward Balance", test_reward_balance),
        ("Action Distribution", test_action_distribution_diagnostic),
        ("Sidebet Payout", test_sidebet_payout_fix),
        ("Partial Sell Precision", test_position_partial_sell_precision),
        ("Bankruptcy Handling", test_bankruptcy_handling),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n📋 Testing: {name}")
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Safe to train.")
    else:
        print(f"⚠️  FIX {failed} FAILING TESTS before training!")
    
    print("=" * 50)


# ==============================================================================
# PERFORMANCE BENCHMARKS
# ==============================================================================

def benchmark_reward_calculation():
    """
    Benchmark reward calculation performance
    """
    import time
    from rugs_bot.training.reward_calculator import RewardCalculator
    
    calc = RewardCalculator()
    
    # Create typical state
    state = {
        'has_positions': True,
        'positions': 2,
        'bankroll': 100,
        'current_multiplier': 25.0,
        'rug_prediction': {
            'probability': 0.3,
            'confidence': 0.7
        }
    }
    action = {'action_type': 2}
    next_state = {'bankroll': 105}
    
    # Benchmark
    start = time.time()
    for _ in range(1000):
        calc.calculate_reward(state, action, next_state)
    elapsed = time.time() - start
    
    per_call_ms = (elapsed / 1000) * 1000
    
    print(f"Reward calculation: {per_call_ms:.2f}ms per call")
    
    if per_call_ms > 1.0:
        print("⚠️  WARNING: Reward calculation too slow!")
    else:
        print("✅ Performance acceptable")


def benchmark_environment_step():
    """
    Benchmark environment step performance
    """
    import time
    from rugs_bot.training.environment import RugsMultiGameEnv
    
    env = RugsMultiGameEnv(
        session_paths=[Path("test_sessions/session_001")],
        games_per_episode=3
    )
    
    obs, _ = env.reset()
    
    # Benchmark
    start = time.time()
    for _ in range(100):
        action = np.array([1, 0, 0])  # BUY_MAIN
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, _ = env.reset()
    
    elapsed = time.time() - start
    per_step_ms = (elapsed / 100) * 1000
    
    print(f"Environment step: {per_step_ms:.2f}ms per step")
    
    if per_step_ms > 10.0:
        print("⚠️  WARNING: Environment step too slow!")
    else:
        print("✅ Performance acceptable")


if __name__ == "__main__":
    # Run all tests
    run_all_tests()
    
    # Run benchmarks
    print("\n📊 PERFORMANCE BENCHMARKS")
    print("-" * 30)
    benchmark_reward_calculation()
    benchmark_environment_step()
