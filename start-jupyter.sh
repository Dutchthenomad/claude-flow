#!/bin/bash
# Claude Flow JupyterLab Server
# ONE COMMAND startup from fresh PC state
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/rag-pipeline/.venv"
CONFIG_FILE="$SCRIPT_DIR/jupyter/config.env"

# Load configuration (create default if missing)
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Creating default configuration..."
    cat > "$CONFIG_FILE" << 'EOF'
# Claude Flow Jupyter Configuration
# Edit these paths as needed

# Port for JupyterLab (default: 8765)
JUPYTER_PORT=8765

# Data directories
RUGS_DATA_DIR="$HOME/rugs_data"
RUGS_RECORDINGS_DIR="$HOME/rugs_recordings"

# Related projects (set to empty string if not available)
RUGS_RL_BOT_PATH="$HOME/Desktop/rugs-rl-bot"
VECTRA_PLAYER_PATH="$HOME/Desktop/VECTRA-PLAYER"
REPLAYER_PATH="$HOME/Desktop/REPLAYER"

# Chrome DevTools Protocol (CDP) - for event capture
# Set CDP_ENABLED=true to launch automation browser alongside JupyterLab
CDP_ENABLED=false
CDP_PORT=9222
CDP_PROFILE="$HOME/.gamebot/chrome_profiles/rugs_bot"
EOF
fi

# Source the config
source "$CONFIG_FILE"

# Export environment variables
export CLAUDE_FLOW_ROOT="$SCRIPT_DIR"
export JUPYTER_PORT="${JUPYTER_PORT:-8765}"
export RUGS_DATA_DIR="${RUGS_DATA_DIR:-$HOME/rugs_data}"
export RUGS_RECORDINGS_DIR="${RUGS_RECORDINGS_DIR:-$HOME/rugs_recordings}"
export RUGS_RL_BOT_PATH="${RUGS_RL_BOT_PATH:-}"
export VECTRA_PLAYER_PATH="${VECTRA_PLAYER_PATH:-}"
export REPLAYER_PATH="${REPLAYER_PATH:-}"
export CHROMADB_PATH="$SCRIPT_DIR/rag-pipeline/storage/chroma"
export KNOWLEDGE_PATH="$SCRIPT_DIR/knowledge/rugs-events"

# CDP exports
export CDP_ENABLED="${CDP_ENABLED:-false}"
export CDP_PORT="${CDP_PORT:-9222}"
export CDP_PROFILE="${CDP_PROFILE:-$HOME/.gamebot/chrome_profiles/rugs_bot}"

echo "========================================"
echo "  Claude Flow JupyterLab Server"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "[1/4] Virtual environment exists"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install/update dependencies
echo "[2/4] Checking dependencies..."
pip install -q --upgrade pip
pip install -q -r "$SCRIPT_DIR/rag-pipeline/requirements.txt" 2>/dev/null || true
pip install -q -r "$SCRIPT_DIR/jupyter/requirements.txt"

# Install kernel if not present
echo "[3/4] Checking kernel..."
if ! jupyter kernelspec list 2>/dev/null | grep -q "claude-flow"; then
    python -m ipykernel install --user --name=claude-flow \
        --display-name="Claude Flow (Python)" --env CLAUDE_FLOW_ROOT "$SCRIPT_DIR"
    echo "       Kernel installed: claude-flow"
else
    echo "       Kernel exists: claude-flow"
fi

# Setup nbstripout if not configured
if ! git config --get filter.nbstripout.clean >/dev/null 2>&1; then
    echo "       Setting up nbstripout for clean git commits..."
    nbstripout --install --attributes .gitattributes 2>/dev/null || true
fi

# Start JupyterLab
echo "[4/4] Starting JupyterLab..."
echo ""
echo "========================================"
echo "  Access at: http://localhost:$JUPYTER_PORT"
echo "  Config:    $CONFIG_FILE"
echo "  Logs:      jupyter/jupyter.log"
echo "========================================"
echo ""

jupyter lab \
    --notebook-dir="$SCRIPT_DIR/jupyter/notebooks" \
    --port="$JUPYTER_PORT" \
    --no-browser \
    --ServerApp.token='' \
    --ServerApp.password='' \
    --ServerApp.ip='127.0.0.1' \
    2>&1 | tee "$SCRIPT_DIR/jupyter/jupyter.log" &

JUPYTER_PID=$!

# Wait a moment then open browser
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:$JUPYTER_PORT" 2>/dev/null &
elif command -v open &> /dev/null; then
    open "http://localhost:$JUPYTER_PORT" 2>/dev/null &
fi

# Launch CDP browser if enabled
CDP_PORT="${CDP_PORT:-9222}"
CDP_PROFILE="${CDP_PROFILE:-$HOME/.gamebot/chrome_profiles/rugs_bot}"
CDP_ENABLED="${CDP_ENABLED:-false}"

if [ "$CDP_ENABLED" = "true" ]; then
    echo ""
    echo "========================================"
    echo "  Launching CDP Browser (port $CDP_PORT)"
    echo "========================================"

    # Ensure profile directory exists
    mkdir -p "$CDP_PROFILE"

    # Launch Chrome with CDP
    google-chrome \
        --remote-debugging-port="$CDP_PORT" \
        --user-data-dir="$CDP_PROFILE" \
        --no-first-run \
        --new-window \
        "https://rugs.fun" 2>/dev/null &

    CDP_PID=$!
    echo "CDP Browser PID: $CDP_PID"
    echo "Profile: $CDP_PROFILE"
    echo "========================================"
fi

echo ""
echo "JupyterLab PID: $JUPYTER_PID"
echo "Press Ctrl+C to stop all services"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $JUPYTER_PID 2>/dev/null
    [ -n "$CDP_PID" ] && kill $CDP_PID 2>/dev/null
    pkill -f "jupyter-lab.*$JUPYTER_PORT" 2>/dev/null
    echo "Done."
}

trap cleanup EXIT INT TERM

# Keep script running
wait
