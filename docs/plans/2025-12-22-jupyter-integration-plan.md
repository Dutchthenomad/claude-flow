# JupyterLab Integration Plan

**Created:** December 22, 2025
**Status:** PLANNING
**Goal:** Single-server review environment for knowledge pipeline + RL bot integration

---

## Executive Summary

Create a ONE-COMMAND JupyterLab server that:
- Starts from fresh PC state with `./start-jupyter.sh`
- Integrates with claude-flow knowledge pipeline
- Shares infrastructure with rugs-rl-bot
- Follows ML best practices for version control
- Provides browser-based review for CANONICAL validation

---

## Design Principles

1. **One Command Startup**: `./start-jupyter.sh` from repo root
2. **Zero Configuration**: Works immediately after clone + install
3. **Version Control Safe**: Notebooks stripped of outputs before commit
4. **Shared Infrastructure**: Same venv, same ChromaDB, same paths as rag-pipeline
5. **ML Scientist Standards**: Reproducible, documented, testable

---

## Architecture

```
claude-flow/
├── start-jupyter.sh           # ONE COMMAND entry point
├── jupyter/
│   ├── CONTEXT.md             # Directory documentation
│   ├── requirements.txt       # Jupyter-specific deps (extends rag-pipeline)
│   ├── jupyter_config.py      # Server configuration
│   ├── kernels/               # Custom kernel definitions
│   │   └── claude-flow/       # Kernel with correct paths
│   └── notebooks/
│       ├── 00_quickstart.ipynb           # Getting started
│       ├── 01_event_explorer.ipynb       # Browse captured events
│       ├── 02_canonical_review.ipynb     # Review + approve promotions
│       ├── 03_coverage_dashboard.ipynb   # What's documented vs missing
│       ├── 04_rl_bot_analysis.ipynb      # RL model evaluation
│       └── templates/                    # Notebook templates
│           └── new_analysis.ipynb
├── rag-pipeline/              # Existing (shared venv)
│   └── .venv/                 # Extended with jupyter deps
└── knowledge/
    └── rugs-events/
        └── generated/         # Where discoveries land
```

---

## Single Entry Point

### `start-jupyter.sh`

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/rag-pipeline/.venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install/update dependencies (idempotent)
pip install -q -r "$SCRIPT_DIR/rag-pipeline/requirements.txt"
pip install -q -r "$SCRIPT_DIR/jupyter/requirements.txt"

# Install kernel if not present
if ! jupyter kernelspec list | grep -q "claude-flow"; then
    python -m ipykernel install --user --name=claude-flow \
        --display-name="Claude Flow (Python)"
fi

# Start JupyterLab
echo "Starting JupyterLab..."
echo "Access at: http://localhost:8888"
jupyter lab \
    --notebook-dir="$SCRIPT_DIR/jupyter/notebooks" \
    --config="$SCRIPT_DIR/jupyter/jupyter_config.py" \
    --no-browser \
    2>&1 | tee "$SCRIPT_DIR/jupyter/jupyter.log"
```

### First Run (fresh PC)

```bash
git clone <repo>
cd claude-flow
./start-jupyter.sh
# Opens browser to http://localhost:8888
```

---

## Dependencies

### `jupyter/requirements.txt`

```
# JupyterLab (modern interface)
jupyterlab>=4.0.0
ipykernel>=6.0.0

# Widgets for interactive review
ipywidgets>=8.0.0
jupyterlab-widgets>=3.0.0

# Data display
pandas>=2.0.0
tabulate>=0.9.0

# Visualization
matplotlib>=3.7.0
plotly>=5.0.0

# ChromaDB integration (already in rag-pipeline, but explicit)
chromadb>=0.4.0

# Notebook version control
nbstripout>=0.6.0

# Code quality in notebooks
black[jupyter]>=23.0.0
```

---

## Version Control (Critical for ML)

### Problem
Jupyter notebooks contain outputs (images, tables, execution counts) that:
- Create massive git diffs
- Cause merge conflicts
- Leak data into repo

### Solution: nbstripout

```bash
# One-time setup (in install.sh)
nbstripout --install --attributes .gitattributes

# Creates .gitattributes:
*.ipynb filter=nbstripout
```

### Pre-commit Hook

Add to `.claude/hooks/pre-commit`:
```bash
# Strip notebook outputs before commit
nbstripout jupyter/notebooks/*.ipynb
```

### .gitignore Additions

```
# Jupyter
jupyter/jupyter.log
jupyter/.ipynb_checkpoints/
*.ipynb_checkpoints/
.virtual_documents/

# Never commit notebook outputs (backup)
jupyter/notebooks/**/*-output.ipynb
```

---

## Shared Infrastructure

### Environment Variables

Set in `start-jupyter.sh`:
```bash
export CLAUDE_FLOW_ROOT="$SCRIPT_DIR"
export RUGS_DATA_DIR="$HOME/rugs_data"
export RUGS_RECORDINGS_DIR="$HOME/rugs_recordings"
export CHROMADB_PATH="$SCRIPT_DIR/rag-pipeline/storage/chroma"
export KNOWLEDGE_PATH="$SCRIPT_DIR/knowledge/rugs-events"
```

### Shared Paths (available in all notebooks)

```python
# jupyter/notebooks/_paths.py (auto-imported)
import os
from pathlib import Path

CLAUDE_FLOW_ROOT = Path(os.environ.get("CLAUDE_FLOW_ROOT", "~/Desktop/claude-flow")).expanduser()
RUGS_DATA = Path(os.environ.get("RUGS_DATA_DIR", "~/rugs_data")).expanduser()
RUGS_RECORDINGS = Path(os.environ.get("RUGS_RECORDINGS_DIR", "~/rugs_recordings")).expanduser()
CHROMADB_PATH = Path(os.environ.get("CHROMADB_PATH", CLAUDE_FLOW_ROOT / "rag-pipeline/storage/chroma"))
KNOWLEDGE_PATH = Path(os.environ.get("KNOWLEDGE_PATH", CLAUDE_FLOW_ROOT / "knowledge/rugs-events"))
```

---

## Notebooks

### 00_quickstart.ipynb
- Verify environment setup
- Test ChromaDB connection
- Load sample data
- Introduction to workflow

### 01_event_explorer.ipynb
- Browse `discovered_schemas.json`
- Filter by event type, tier, auth requirement
- View sample payloads
- Search fields

### 02_canonical_review.ipynb
- Load `promotion_queue.json`
- Side-by-side: OBSERVED data vs CANONICAL spec
- Interactive approve/reject widgets
- Save decisions
- Generate spec update drafts

### 03_coverage_dashboard.ipynb
- What % of events are documented?
- Which fields are missing?
- Priority matrix (P0/P1/P2 coverage)
- Visualization of gaps

### 04_rl_bot_analysis.ipynb
- Load trained models from `rugs-rl-bot/models/`
- Evaluate on recorded games
- Visualize reward components
- Compare strategies

---

## Integration Points

### With rag-pipeline

```python
# In any notebook
import sys
sys.path.insert(0, str(CLAUDE_FLOW_ROOT / "rag-pipeline"))

from retrieval.retrieve import search, search_with_filter
results = search("playerUpdate balance", top_k=5)
```

### With rugs-rl-bot

```python
# In 04_rl_bot_analysis.ipynb
sys.path.insert(0, "/home/nomad/Desktop/rugs-rl-bot")

from rugs_bot.sidebet.predictor import SidebetPredictor
predictor = SidebetPredictor()
```

### With ChromaDB MCP

```python
# Query via MCP (when available)
# Or direct Python access:
import chromadb
client = chromadb.PersistentClient(path=str(CHROMADB_PATH))
collection = client.get_collection("knowledge_base")
```

---

## Installation Integration

### Update `install.sh`

```bash
# Add to existing install.sh

echo "Setting up Jupyter environment..."

# Install jupyter requirements
if [ -f "jupyter/requirements.txt" ]; then
    pip install -r jupyter/requirements.txt
fi

# Install nbstripout for version control
nbstripout --install --attributes .gitattributes

# Install kernel
python -m ipykernel install --user --name=claude-flow --display-name="Claude Flow (Python)"

echo "Jupyter setup complete. Run ./start-jupyter.sh to start."
```

---

## Security

### `jupyter/jupyter_config.py`

```python
c = get_config()

# Bind to localhost only (not exposed to network)
c.ServerApp.ip = '127.0.0.1'
c.ServerApp.port = 8888

# Disable token for local development (optional, can enable for security)
c.ServerApp.token = ''
c.ServerApp.password = ''

# Open browser automatically
c.ServerApp.open_browser = True

# Trust notebooks in this directory
c.ServerApp.root_dir = 'notebooks'
```

---

## Implementation Phases

### Phase 1: Infrastructure (Day 1)
- [ ] Create `jupyter/` directory structure
- [ ] Write `start-jupyter.sh`
- [ ] Create `jupyter/requirements.txt`
- [ ] Create `jupyter/jupyter_config.py`
- [ ] Create `jupyter/CONTEXT.md`
- [ ] Update `.gitignore`
- [ ] Setup nbstripout

### Phase 2: Quickstart Notebook (Day 1)
- [ ] Create `00_quickstart.ipynb`
- [ ] Verify environment
- [ ] Test ChromaDB connection
- [ ] Document setup verification

### Phase 3: Event Explorer (Day 2)
- [ ] Create `01_event_explorer.ipynb`
- [ ] Load discovered_schemas.json
- [ ] Interactive filtering
- [ ] Field search

### Phase 4: Canonical Review (Day 2-3)
- [ ] Create `02_canonical_review.ipynb`
- [ ] Create `promotion_queue.json` schema
- [ ] Build approval widgets
- [ ] Save decisions workflow

### Phase 5: RL Integration (Day 3)
- [ ] Create `04_rl_bot_analysis.ipynb`
- [ ] Model loading
- [ ] Evaluation helpers
- [ ] Visualization

### Phase 6: Documentation (Day 3)
- [ ] Update AGENTS.md (remove Codex coordination)
- [ ] Create jupyter/README.md
- [ ] Update claude-flow CLAUDE.md

---

## Testing

### Verification Commands

```bash
# Test fresh install
rm -rf rag-pipeline/.venv
./start-jupyter.sh
# Should create venv, install deps, start server

# Test kernel
jupyter kernelspec list | grep claude-flow

# Test nbstripout
echo "*.ipynb filter=nbstripout" | grep -q nbstripout && echo "OK"

# Test notebook loads
jupyter nbconvert --execute jupyter/notebooks/00_quickstart.ipynb --to html
```

---

## Success Criteria

- [ ] `./start-jupyter.sh` works from fresh clone
- [ ] Notebooks have no outputs in git
- [ ] ChromaDB queryable from notebooks
- [ ] Can load rugs-rl-bot models
- [ ] Event explorer shows discovered events
- [ ] Canonical review workflow functional
- [ ] All notebooks use shared paths
- [ ] Documentation complete

---

## Questions for Review

1. **Port**: 8888 default, or different?
2. **Browser auto-open**: Enable or disable?
3. **Token auth**: Enable for security or disable for convenience?
4. **Notebook naming**: Current scheme ok?
5. **RL bot path**: Hardcoded `/home/nomad/Desktop/rugs-rl-bot` or env var?

---

*Plan ready for review*
