"""
Claude Flow Jupyter Library

Provides integration modules for notebooks:
- cdp_notebook: Chrome DevTools Protocol event capture
- automation_bridge: RL training browser automation
- game_history_collector: Server-side game history collection for ML/RL training
"""

from .cdp_notebook import CDPCapture, MockCDPCapture
from .automation_bridge import (
    LiveTrainingSession,
    ModelEvaluator,
    MockLiveSession,
    check_dependencies,
    print_status
)
from .game_history_collector import GameHistoryCollector, MockGameHistoryCollector

__all__ = [
    'CDPCapture',
    'MockCDPCapture',
    'LiveTrainingSession',
    'ModelEvaluator',
    'MockLiveSession',
    'check_dependencies',
    'print_status',
    'GameHistoryCollector',
    'MockGameHistoryCollector'
]
