"""
Automation Bridge - Connect Jupyter notebooks to RL training

Provides unified interface for:
1. Launching Playwright-controlled browser sessions
2. Running RL training loops with live game observation
3. Real-time model evaluation against live games
4. Screenshot capture for observation analysis

Requires:
- CV-BOILER-PLATE-FORK for browser automation
- rugs-rl-bot for RL models
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configurable paths
CV_BOILERPLATE_PATH = Path(os.environ.get(
    'CV_BOILERPLATE_PATH',
    Path.home() / 'Desktop' / 'CV-BOILER-PLATE-FORK'
))

RUGS_RL_BOT_PATH = Path(os.environ.get(
    'RUGS_RL_BOT_PATH',
    Path.home() / 'Desktop' / 'rugs-rl-bot'
))


def check_dependencies() -> Dict[str, bool]:
    """Check which integration dependencies are available."""
    deps = {
        'cv_boilerplate': CV_BOILERPLATE_PATH.exists(),
        'rugs_rl_bot': RUGS_RL_BOT_PATH.exists(),
        'playwright': False,
        'stable_baselines3': False,
    }

    try:
        import playwright
        deps['playwright'] = True
    except ImportError:
        pass

    try:
        import stable_baselines3
        deps['stable_baselines3'] = True
    except ImportError:
        pass

    return deps


class LiveTrainingSession:
    """
    Manage a live RL training session with browser automation.

    Usage:
        session = LiveTrainingSession()
        session.start()  # Launches browser, connects to rugs.fun

        # Run training loop
        for episode in range(100):
            obs = session.get_observation()  # Screenshot
            action = model.predict(obs)
            reward = session.execute_action(action)
            session.record_step(obs, action, reward)

        session.stop()  # Cleanup
    """

    def __init__(self, headless: bool = False):
        """
        Initialize training session.

        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.controller = None
        self.automation = None
        self.is_running = False
        self._steps: List[Dict] = []

        # Try to import browser controller
        if CV_BOILERPLATE_PATH.exists():
            sys.path.insert(0, str(CV_BOILERPLATE_PATH))
            try:
                from core.browser.controller import BrowserController
                from core.rugs.automation import RugsAutomation
                self._BrowserController = BrowserController
                self._RugsAutomation = RugsAutomation
            except ImportError:
                self._BrowserController = None
                self._RugsAutomation = None
        else:
            self._BrowserController = None
            self._RugsAutomation = None

    def start(self, url: str = "https://rugs.fun") -> bool:
        """
        Launch browser and connect to game.

        Args:
            url: Game URL

        Returns:
            True if connected successfully
        """
        if self._BrowserController is None:
            print("Error: CV-BOILER-PLATE not available")
            print(f"Expected at: {CV_BOILERPLATE_PATH}")
            return False

        try:
            self.controller = self._BrowserController(headless=self.headless)
            success = self.controller.connect(url)

            if success:
                self.automation = self._RugsAutomation(self.controller)
                self.is_running = True
                print(f"Connected to {url}")
                return True
            else:
                print("Browser connection failed")
                return False

        except Exception as e:
            print(f"Start failed: {e}")
            return False

    def get_observation(self) -> Optional[Any]:
        """
        Get current game state as screenshot.

        Returns:
            Screenshot as numpy array, or None if not running
        """
        if not self.is_running:
            return None

        try:
            return self.controller.take_screenshot()
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None

    def execute_action(self, action: int) -> float:
        """
        Execute RL action in browser.

        Args:
            action: Integer action code
                0 = WAIT
                1 = BUY_MAIN_10
                2 = BUY_MAIN_25
                3 = BUY_MAIN_50
                4 = BUY_MAIN_100
                5 = SELL_MAIN_10
                6 = SELL_MAIN_25
                7 = SELL_MAIN_50
                8 = SELL_MAIN_100

        Returns:
            Immediate reward (P&L change)
        """
        if not self.is_running:
            return 0.0

        try:
            if action == 0:
                pass  # WAIT
            elif action in [1, 2, 3, 4]:
                bet_amounts = [10, 25, 50, 100]
                self.automation.place_bet(bet_amounts[action - 1], side="main")
            elif action in [5, 6, 7, 8]:
                percentages = [10, 25, 50, 100]
                self.automation.sell_position(percentages[action - 5])

            return self._calculate_reward()

        except Exception as e:
            print(f"Action failed: {e}")
            return 0.0

    def _calculate_reward(self) -> float:
        """Extract P&L from page to calculate reward."""
        try:
            pnl = self.controller.execute_javascript(
                "return parseFloat(document.querySelector('.pnl')?.textContent || '0')"
            )
            return float(pnl) if pnl else 0.0
        except:
            return 0.0

    def record_step(self, obs: Any, action: int, reward: float):
        """Record a training step for analysis."""
        self._steps.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'reward': reward,
            'obs_shape': obs.shape if hasattr(obs, 'shape') else None
        })

    def get_step_history(self) -> List[Dict]:
        """Get recorded step history."""
        return self._steps.copy()

    def stop(self):
        """Cleanup browser resources."""
        self.is_running = False
        if self.controller:
            try:
                self.controller.cleanup()
            except:
                pass
        print("Session stopped")


class ModelEvaluator:
    """
    Evaluate trained RL models against live games.

    Usage:
        evaluator = ModelEvaluator("models/phase0_final.zip")
        results = evaluator.run_live_evaluation(n_episodes=10)
    """

    def __init__(self, model_path: str):
        """
        Initialize evaluator with trained model.

        Args:
            model_path: Path to trained model file (.zip)
        """
        self.model_path = Path(model_path)
        self.model = None
        self.session = None

        # Try to load model
        try:
            from stable_baselines3 import PPO
            self.model = PPO.load(str(self.model_path))
            print(f"Model loaded: {self.model_path.name}")
        except ImportError:
            print("stable_baselines3 not installed")
        except Exception as e:
            print(f"Model load failed: {e}")

    def run_live_evaluation(
        self,
        n_episodes: int = 10,
        max_steps: int = 1000,
        headless: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluate model on live games.

        Args:
            n_episodes: Number of episodes to run
            max_steps: Maximum steps per episode
            headless: Run browser in headless mode

        Returns:
            Dictionary with evaluation metrics
        """
        if self.model is None:
            return {'error': 'No model loaded'}

        self.session = LiveTrainingSession(headless=headless)

        if not self.session.start():
            return {'error': 'Browser connection failed'}

        results = []

        try:
            for ep in range(n_episodes):
                obs = self.session.get_observation()
                total_reward = 0
                steps = 0

                while steps < max_steps:
                    action, _ = self.model.predict(obs, deterministic=True)
                    reward = self.session.execute_action(int(action))
                    total_reward += reward
                    steps += 1

                    obs = self.session.get_observation()
                    if obs is None:
                        break

                    # Check game over (would need DOM check)
                    # if self._check_game_over():
                    #     break

                results.append({
                    'episode': ep,
                    'total_reward': total_reward,
                    'steps': steps
                })

                print(f"Episode {ep+1}/{n_episodes}: reward={total_reward:.2f}, steps={steps}")

        finally:
            self.session.stop()

        return self._aggregate_results(results)

    def _aggregate_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate aggregate metrics."""
        if not results:
            return {'error': 'No results'}

        import numpy as np

        rewards = [r['total_reward'] for r in results]

        return {
            'n_episodes': len(results),
            'avg_reward': float(np.mean(rewards)),
            'std_reward': float(np.std(rewards)),
            'min_reward': float(np.min(rewards)),
            'max_reward': float(np.max(rewards)),
            'win_rate': sum(1 for r in rewards if r > 0) / len(rewards),
            'raw_results': results
        }


class MockLiveSession(LiveTrainingSession):
    """Mock session for testing without browser."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mock_reward = 0.0

    def start(self, url: str = None) -> bool:
        print("[MOCK] Simulated browser session")
        self.is_running = True
        return True

    def get_observation(self):
        import numpy as np
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    def execute_action(self, action: int) -> float:
        import random
        self._mock_reward = random.uniform(-10, 20)
        return self._mock_reward

    def stop(self):
        self.is_running = False
        print("[MOCK] Session stopped")


def print_status():
    """Print integration status."""
    deps = check_dependencies()

    print("Automation Bridge Status")
    print("=" * 40)
    print(f"CV-BOILER-PLATE: {'OK' if deps['cv_boilerplate'] else 'NOT FOUND'}")
    print(f"  Path: {CV_BOILERPLATE_PATH}")
    print(f"rugs-rl-bot:     {'OK' if deps['rugs_rl_bot'] else 'NOT FOUND'}")
    print(f"  Path: {RUGS_RL_BOT_PATH}")
    print(f"Playwright:      {'OK' if deps['playwright'] else 'NOT INSTALLED'}")
    print(f"Stable-Baselines3: {'OK' if deps['stable_baselines3'] else 'NOT INSTALLED'}")
