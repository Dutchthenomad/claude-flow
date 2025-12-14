#!/bin/bash
#
# Claude-Flow Installer
#
# This script installs claude-flow by creating symlinks from ~/.claude/
# to the claude-flow source directory. This enables rapid development
# while keeping Claude Code working.
#
# Usage: ./install.sh [--plugin | --symlink]
#   --plugin   Install as a Claude Code plugin (recommended for distribution)
#   --symlink  Install via symlinks (recommended for development)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Claude-Flow Installer${NC}"
echo "====================="
echo ""

# Parse arguments
INSTALL_MODE="symlink"
if [[ "$1" == "--plugin" ]]; then
    INSTALL_MODE="plugin"
elif [[ "$1" == "--symlink" ]]; then
    INSTALL_MODE="symlink"
fi

echo -e "Install mode: ${YELLOW}$INSTALL_MODE${NC}"
echo ""

if [[ "$INSTALL_MODE" == "plugin" ]]; then
    echo "Installing as Claude Code plugin..."
    echo ""
    echo "Run the following commands in Claude Code:"
    echo ""
    echo "  /plugin marketplace add $SCRIPT_DIR"
    echo "  /plugin install claude-flow@claude-flow-marketplace"
    echo ""
    echo -e "${YELLOW}Note: Restart Claude Code after installation.${NC}"
    exit 0
fi

# Symlink installation
echo "Installing via symlinks..."
echo ""

# Backup existing directories if they exist and aren't symlinks
backup_if_exists() {
    local target="$1"
    if [[ -e "$target" && ! -L "$target" ]]; then
        local backup="${target}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}Backing up $target to $backup${NC}"
        mv "$target" "$backup"
    elif [[ -L "$target" ]]; then
        echo -e "${YELLOW}Removing existing symlink: $target${NC}"
        rm "$target"
    fi
}

# Create ~/.claude if it doesn't exist
mkdir -p "$CLAUDE_DIR"

# Install commands
echo "Installing commands..."
backup_if_exists "$CLAUDE_DIR/commands"
ln -s "$SCRIPT_DIR/commands" "$CLAUDE_DIR/commands"
echo -e "${GREEN}✓ Commands linked${NC}"

# Install agents
echo "Installing agents..."
backup_if_exists "$CLAUDE_DIR/agents"
ln -s "$SCRIPT_DIR/agents" "$CLAUDE_DIR/agents"
echo -e "${GREEN}✓ Agents linked${NC}"

# Install WORKFLOW_QUICKREF.md
echo "Installing workflow reference..."
backup_if_exists "$CLAUDE_DIR/WORKFLOW_QUICKREF.md"
ln -s "$SCRIPT_DIR/docs/WORKFLOW_QUICKREF.md" "$CLAUDE_DIR/WORKFLOW_QUICKREF.md"
echo -e "${GREEN}✓ Workflow reference linked${NC}"

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Claude-flow is now installed via symlinks."
echo "Changes to files in $SCRIPT_DIR will be reflected immediately."
echo ""
echo -e "${YELLOW}Note: Restart Claude Code to ensure changes take effect.${NC}"
