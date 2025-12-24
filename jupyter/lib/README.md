# Claude Flow Jupyter Library

Python library providing integration modules for Claude Flow notebooks and automation.

## Modules

### CDP Integration

#### `cdp_notebook.py`

Chrome DevTools Protocol event capture for notebooks.

**Classes:**
- `CDPCapture` - Connect to Chrome CDP and intercept WebSocket events
- `MockCDPCapture` - Mock CDP capture for testing without Chrome

**Key Features:**
- WebSocket frame interception from rugs.fun
- Event buffering and filtering
- JSONL recording to disk
- Event callbacks for custom processing
- IPython/Jupyter integration for rich display

**Basic Usage:**
```python
from jupyter.lib import CDPCapture

capture = CDPCapture()
capture.connect()
capture.start_recording("session.jsonl")

# Later...
capture.show_recent_events()
capture.stop_recording()
capture.disconnect()
```

### Game History Collection

#### `game_history_collector.py`

Server-side game history collection from gameHistory[] rolling window.

**Classes:**
- `GameHistoryCollector` - Collect historical game data for ML/RL training
- `MockGameHistoryCollector` - Generate mock game data for testing

**Key Features:**
- Automatic deduplication by gameId
- Rolling window tracking (~10 games)
- JSONL storage compatible with existing recordings
- Passive collection during live sessions
- RL training export functionality
- Data structure validation

**Basic Usage:**
```python
from jupyter.lib import GameHistoryCollector

collector = GameHistoryCollector()
collector.start_collecting()

# Integrate with CDPCapture
capture = CDPCapture()
capture.connect()
collector.attach_to_capture(capture)

# Games automatically collected!
stats = collector.get_statistics()
```

**See Also:** `GAME_HISTORY_COLLECTOR_GUIDE.md` for complete documentation

### Automation & RL Training

#### `automation_bridge.py`

Browser automation and RL training integration.

**Classes:**
- `LiveTrainingSession` - Manage live RL training with browser automation
- `ModelEvaluator` - Evaluate trained RL models against live games
- `MockLiveSession` - Mock session for testing without browser

**Key Features:**
- Playwright-controlled browser sessions
- RL training loops with live game observation
- Real-time model evaluation
- Screenshot capture for observation analysis

**Requirements:**
- CV-BOILER-PLATE-FORK for browser automation
- rugs-rl-bot for RL models
- Playwright
- Stable-Baselines3

**Basic Usage:**
```python
from jupyter.lib import LiveTrainingSession

session = LiveTrainingSession()
session.start()

for episode in range(100):
    obs = session.get_observation()
    action = model.predict(obs)
    reward = session.execute_action(action)
    session.record_step(obs, action, reward)

session.stop()
```

## Installation

The library is automatically available in Jupyter notebooks when using the provided environment:

```python
# In notebooks, import from lib
from jupyter.lib import CDPCapture, GameHistoryCollector, LiveTrainingSession
```

For standalone Python scripts:

```python
import sys
from pathlib import Path

# Add jupyter directory to path
sys.path.insert(0, str(Path('/path/to/claude-flow/jupyter')))

from lib import CDPCapture, GameHistoryCollector
```

## Dependencies

Core requirements (see `requirements.txt`):
- `pychrome>=0.2.4` - Chrome DevTools Protocol
- `websocket-client>=1.0.0` - WebSocket support
- `pandas>=2.0.0` - Data handling
- `ipywidgets>=8.0.0` - Notebook widgets

Optional for automation:
- `playwright` - Browser automation
- `stable-baselines3` - RL models

## Environment Variables

Configure paths via environment variables (see `notebooks/_paths.py`):

```bash
# Default paths
CLAUDE_FLOW_ROOT=/path/to/claude-flow
RUGS_RECORDINGS_DIR=~/rugs_recordings
RUGS_DATA_DIR=~/rugs_data

# Related projects (optional)
RUGS_RL_BOT_PATH=/path/to/rugs-rl-bot
CV_BOILERPLATE_PATH=/path/to/CV-BOILER-PLATE-FORK
```

## Testing

### Run Tests

For modules with pytest tests:
```bash
cd jupyter
python -m pytest tests/ -v
```

### Run Demo Scripts

For modules with demo scripts:
```bash
cd jupyter/tests
python demo_game_history_collector.py
```

## Common Patterns

### CDP Event Capture with Game History Collection

```python
from jupyter.lib import CDPCapture, GameHistoryCollector

# Set up CDP capture
capture = CDPCapture()
capture.connect()

# Attach game history collector
collector = GameHistoryCollector()
collector.attach_to_capture(capture)

# Both capture and collection now happen automatically
# Check progress
print(f"Events: {len(capture.events)}")
print(f"Games: {collector.stats['total_collected']}")

# Export collected games
collector.export_for_rl_training()

# Cleanup
collector.stop_collecting()
capture.disconnect()
```

### Mock Testing Without Live Connection

```python
from jupyter.lib import MockCDPCapture, MockGameHistoryCollector

# Mock CDP
capture = MockCDPCapture()
capture.connect()  # Starts simulation

# Mock games
collector = MockGameHistoryCollector()
collector.start_collecting()  # Generates mock games

# Both work without live connection
print(f"Mock events: {len(capture.events)}")
print(f"Mock games: {len(collector.collected_games)}")
```

## Architecture

```
jupyter/lib/
├── __init__.py                    # Public API exports
├── cdp_notebook.py                # CDP event capture
├── game_history_collector.py      # Game history collection
└── automation_bridge.py           # Browser automation & RL

jupyter/notebooks/
├── _paths.py                      # Shared paths & utilities
└── game_history_collector_example.ipynb

jupyter/tests/
├── test_game_history_collector.py
└── demo_game_history_collector.py
```

## Integration Points

### With Existing Recordings

GameHistoryCollector stores games in JSONL format compatible with existing manual recordings:

```
~/rugs_recordings/
├── session_20241220_*.jsonl        # Manual CDP recordings
└── game_history/
    └── session_*.jsonl             # GameHistoryCollector output
```

### With RL Training Pipeline

Export games directly for training:

```python
collector.export_for_rl_training(
    output_file="/path/to/rugs-rl-bot/data/games.jsonl",
    include_fields=['id', 'prices', 'rugPoint']
)
```

### With RAG Pipeline

Game data can be indexed into ChromaDB for retrieval:

```python
from ingestion.jsonl_ingest import index_jsonl_to_chroma

games_file = collector.export_for_rl_training()
index_jsonl_to_chroma(games_file, collection_name="game_history")
```

## Status

| Module | Status | Tests | Documentation |
|--------|--------|-------|---------------|
| `cdp_notebook` | ✅ Stable | Manual | Inline |
| `game_history_collector` | ✅ Complete | ✅ 6/6 passing | ✅ Complete |
| `automation_bridge` | ✅ Stable | Manual | Inline |

## Related Documentation

- **WebSocket Events Spec**: `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md`
- **Game History Guide**: `jupyter/GAME_HISTORY_COLLECTOR_GUIDE.md`
- **Jupyter Context**: `jupyter/CONTEXT.md`
- **Notebook Paths**: `jupyter/notebooks/_paths.py`

## Development

### Adding New Modules

1. Create module in `jupyter/lib/`
2. Export classes in `__init__.py`
3. Add tests in `jupyter/tests/`
4. Update this README
5. Add usage examples to notebooks

### Code Style

- Python 3.12+
- Type hints where appropriate
- Docstrings for all public classes/methods
- Follow existing patterns for consistency

---

*Last updated: December 24, 2025*
