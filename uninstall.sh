#!/bin/bash
#
# Claude-Flow Uninstaller
#
# This script removes claude-flow symlinks from ~/.claude/
# and optionally restores backups.
#
# Usage: ./uninstall.sh [--restore]
#   --restore  Restore backed up files after removing symlinks
#

set -e

CLAUDE_DIR="$HOME/.claude"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${RED}Claude-Flow Uninstaller${NC}"
echo "======================="
echo ""

RESTORE_BACKUPS=false
if [[ "$1" == "--restore" ]]; then
    RESTORE_BACKUPS=true
fi

# Remove symlink and optionally restore backup
remove_symlink() {
    local target="$1"
    local name="$2"

    if [[ -L "$target" ]]; then
        echo "Removing symlink: $target"
        rm "$target"
        echo -e "${GREEN}✓ $name symlink removed${NC}"

        if [[ "$RESTORE_BACKUPS" == true ]]; then
            # Find most recent backup
            local backup=$(ls -t "${target}.backup."* 2>/dev/null | head -1)
            if [[ -n "$backup" ]]; then
                echo -e "${YELLOW}Restoring backup: $backup${NC}"
                mv "$backup" "$target"
                echo -e "${GREEN}✓ $name backup restored${NC}"
            fi
        fi
    elif [[ -e "$target" ]]; then
        echo -e "${YELLOW}$target exists but is not a symlink, skipping${NC}"
    else
        echo -e "${YELLOW}$target does not exist, skipping${NC}"
    fi
}

# Remove symlinks
remove_symlink "$CLAUDE_DIR/commands" "Commands"
remove_symlink "$CLAUDE_DIR/agents" "Agents"
remove_symlink "$CLAUDE_DIR/WORKFLOW_QUICKREF.md" "Workflow reference"

echo ""
echo -e "${GREEN}Uninstallation complete!${NC}"
echo ""

if [[ "$RESTORE_BACKUPS" == true ]]; then
    echo "Backups have been restored where available."
else
    echo "Run with --restore to restore backed up files."
fi

echo ""
echo -e "${YELLOW}Note: Restart Claude Code to ensure changes take effect.${NC}"
