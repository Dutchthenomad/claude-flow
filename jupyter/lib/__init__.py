"""
Claude Flow Jupyter Library

Provides integration modules for notebooks:
- cdp_notebook: Chrome DevTools Protocol event capture
- automation_bridge: RL training browser automation
"""

from .cdp_notebook import CDPCapture, MockCDPCapture
from .automation_bridge import (
    LiveTrainingSession,
    ModelEvaluator,
    MockLiveSession,
    check_dependencies,
    print_status
)

__all__ = [
    'CDPCapture',
    'MockCDPCapture',
    'LiveTrainingSession',
    'ModelEvaluator',
    'MockLiveSession',
    'check_dependencies',
    'print_status'
]
