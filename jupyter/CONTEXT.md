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
└── notebooks/
    ├── 00_quickstart.ipynb        # Setup verification
    ├── 01_event_explorer.ipynb    # Browse captured events
    ├── 02_canonical_review.ipynb  # CANONICAL validation workflow
    ├── 03_coverage_dashboard.ipynb # Documentation coverage
    ├── 04_rl_bot_analysis.ipynb   # RL model evaluation
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
