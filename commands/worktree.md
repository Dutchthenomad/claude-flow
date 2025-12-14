---
description: Use to create isolated workspace for feature development. Enables parallel work without branch switching.
---

# Git Worktree Setup

## Purpose
Create isolated workspace for feature development. Work on multiple features simultaneously without `git stash` or branch switching.

## Directory Priority (Check in order)
1. `.worktrees/` (project-local, hidden)
2. `worktrees/` (project-local, visible)
3. Ask user preference

## Safety Check (REQUIRED for project-local)
```bash
grep -q ".worktrees" .gitignore || echo ".worktrees/" >> .gitignore
git add .gitignore && git commit -m "chore: ignore worktrees directory"
```

## Setup Sequence
```bash
# 1. Get project name
PROJECT=$(basename $(git rev-parse --show-toplevel))

# 2. Create worktree
git worktree add .worktrees/feature-name -b feature/feature-name

# 3. Enter worktree
cd .worktrees/feature-name

# 4. Auto-detect and run setup
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f package.json ] && npm install
[ -f Cargo.toml ] && cargo build

# 5. Run baseline tests
pytest tests/ -v  # or npm test
```

## Cleanup When Done
```bash
# Return to main worktree
cd ../..

# Remove worktree (after merge)
git worktree remove .worktrees/feature-name
```

## Pair With
- `/plan` - Create plan before starting feature
- Use `finishing-a-development-branch` pattern when complete

$ARGUMENTS
