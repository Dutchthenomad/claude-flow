# Jupyter Directory Context

## Purpose
Browser-based review environment for the claude-flow knowledge pipeline and RL bot analysis.

## Quick Start
```bash
# From repo root
./start-jupyter.sh
# Opens http://localhost:8765
```

## Configuration
Edit `config.env` to customize:
- `JUPYTER_PORT` - Server port (default: 8765)
- `RUGS_RL_BOT_PATH` - Path to rugs-rl-bot (for model analysis)
- `VECTRA_PLAYER_PATH` - Path to VECTRA-PLAYER
- `REPLAYER_PATH` - Path to REPLAYER

## Directory Structure

```
jupyter/
├── config.env           # User configuration (git-ignored)
├── requirements.txt     # Python dependencies
├── jupyter.log          # Server logs (git-ignored)
├── CONTEXT.md           # This file
├── GAME_HISTORY_COLLECTOR_GUIDE.md  # GameHistoryCollector documentation
├── lib/                 # Python library modules
│   ├── __init__.py
│   ├── cdp_notebook.py           # CDP event capture
│   ├── game_history_collector.py # Game history collection
│   ├── automation_bridge.py      # Browser automation & RL
│   └── README.md                 # Library documentation
├── tests/
│   ├── test_game_history_collector.py
│   └── demo_game_history_collector.py
└── notebooks/
    ├── _paths.py                  # Shared paths & utilities
    ├── 00_quickstart.ipynb        # Setup verification
    ├── 01_event_explorer.ipynb    # Browse captured events
    ├── 02_canonical_review.ipynb  # CANONICAL validation workflow
    ├── 03_coverage_dashboard.ipynb # Documentation coverage
    ├── 04_rl_bot_analysis.ipynb   # RL model evaluation
    ├── game_history_collector_example.ipynb  # GameHistory demo
    └── templates/                 # Notebook templates
```

## Notebooks

| Notebook | Purpose |
|----------|---------|
| 00_quickstart | Verify environment, test ChromaDB connection |
| 01_event_explorer | Browse discovered events, filter by type/tier |
| 02_canonical_review | Review and approve field promotions |
| 03_coverage_dashboard | Visualize documentation gaps |
| 04_rl_bot_analysis | Load and evaluate trained RL models |
| game_history_collector_example | Demo GameHistoryCollector usage |

## Library Modules

The `lib/` directory provides Python modules for notebooks and automation:

| Module | Purpose |
|--------|---------|
| `cdp_notebook` | Chrome DevTools Protocol event capture |
| `game_history_collector` | Server-side game history collection for ML/RL |
| `automation_bridge` | Browser automation and RL training integration |

See `lib/README.md` for detailed documentation.

## Version Control

Notebooks use `nbstripout` to automatically remove outputs before git commit.
This prevents:
- Massive diffs from output changes
- Merge conflicts
- Accidental data leakage

Setup is automatic via `start-jupyter.sh`.

## Environment Variables

Available in all notebooks via `_paths.py`:

| Variable | Description |
|----------|-------------|
| `CLAUDE_FLOW_ROOT` | Repo root path |
| `CHROMADB_PATH` | ChromaDB storage location |
| `KNOWLEDGE_PATH` | knowledge/rugs-events path |
| `RUGS_DATA_DIR` | ~/rugs_data (game recordings) |
| `RUGS_RECORDINGS_DIR` | ~/rugs_recordings (raw captures) |
| `RUGS_RL_BOT_PATH` | rugs-rl-bot repo (optional) |

## Integration

### ChromaDB
```python
from _paths import get_chromadb_client
client = get_chromadb_client()
collection = client.get_collection("knowledge_base")
```

### RAG Pipeline
```python
from _paths import CLAUDE_FLOW_ROOT
import sys
sys.path.insert(0, str(CLAUDE_FLOW_ROOT / "rag-pipeline"))
from retrieval.retrieve import search
```

### RL Bot (if available)
```python
from _paths import RUGS_RL_BOT_PATH
if RUGS_RL_BOT_PATH:
    sys.path.insert(0, str(RUGS_RL_BOT_PATH))
    from rugs_bot.sidebet.predictor import SidebetPredictor
```

### Game History Collection (NEW)
```python
from lib import GameHistoryCollector, CDPCapture

# Automatic game collection from gameHistory[] rolling window
collector = GameHistoryCollector()

# Option 1: Standalone
collector.start_collecting()
# ... manually process gameStateUpdate events ...

# Option 2: Integrate with CDP
capture = CDPCapture()
capture.connect()
collector.attach_to_capture(capture)
# Games automatically collected!

# Export for RL training
collector.export_for_rl_training()
```

See `GAME_HISTORY_COLLECTOR_GUIDE.md` for complete documentation.

## Kernel

The "Claude Flow (Python)" kernel includes:
- Correct PYTHONPATH for imports
- Environment variables pre-loaded
- Same venv as rag-pipeline

## Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :8765

# Kill existing jupyter
pkill -f jupyter

# Restart
./start-jupyter.sh
```

### Kernel not found
```bash
# Reinstall kernel
source rag-pipeline/.venv/bin/activate
python -m ipykernel install --user --name=claude-flow
```

### Outputs appearing in git diff
```bash
# Reinstall nbstripout
nbstripout --install --attributes .gitattributes
```
