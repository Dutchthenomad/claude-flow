#!/bin/bash
# MCP Server Installation Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "Claude-Flow MCP Server Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Error: Python 3.10+ required (found: $PYTHON_VERSION)"
    exit 1
fi
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Step 1: Install RAG Pipeline
echo "Step 1: Setting up RAG Pipeline..."
echo "------------------------------------"
cd "$PROJECT_ROOT/rag-pipeline"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing RAG dependencies..."
pip install -q -r requirements.txt

echo "✓ RAG pipeline dependencies installed"
echo ""

# Step 2: Index Knowledge Base
echo "Step 2: Indexing Knowledge Base..."
echo "------------------------------------"
echo "This may take a few minutes..."

if python -m ingestion.ingest 2>&1 | tee /tmp/ingest.log; then
    echo "✓ Knowledge base indexed successfully"
else
    echo "⚠ Warning: Indexing encountered issues (see /tmp/ingest.log)"
    echo "  You can re-run indexing later with: cd rag-pipeline && python -m ingestion.ingest"
fi
echo ""

# Step 3: Install MCP Server
echo "Step 3: Installing MCP Server..."
echo "------------------------------------"
cd "$PROJECT_ROOT/mcp-server"

echo "Installing MCP server dependencies..."
pip install -q -r requirements.txt

echo "✓ MCP server dependencies installed"
echo ""

# Step 4: Test Installation
echo "Step 4: Testing Installation..."
echo "------------------------------------"
if python test_tools.py; then
    echo "✓ All tests passed"
else
    echo "❌ Some tests failed"
    exit 1
fi
echo ""

# Step 5: Show Installation Commands
echo "=========================================="
echo "Installation Complete! 🎉"
echo "=========================================="
echo ""
echo "To add the MCP server to Claude Code, run:"
echo ""
echo "  # Local scope (this project only)"
echo "  claude mcp add --transport stdio claude-flow -- \\"
echo "    python $PROJECT_ROOT/mcp-server/server.py"
echo ""
echo "  # OR user scope (all projects)"
echo "  claude mcp add --transport stdio --scope user claude-flow -- \\"
echo "    python $PROJECT_ROOT/mcp-server/server.py"
echo ""
echo "Then in Claude Code, verify with: /mcp"
echo ""
echo "Documentation:"
echo "  - MCP Server README: $PROJECT_ROOT/mcp-server/README.md"
echo "  - Usage examples: $PROJECT_ROOT/mcp-server/CONTEXT.md"
echo ""
