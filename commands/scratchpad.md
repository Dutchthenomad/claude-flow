---
description: Save/restore context across /clear commands and sessions. Use before clearing context.
---

# Memory Persistence Protocol

## On Session Start:
Read `.claude/scratchpad.md` (project-specific) or `~/.claude/scratchpad.md` (global) to restore context.

## On Session End (before /clear):
Update the scratchpad with:
- Current SDLC phase
- Active GitHub Issue number
- Key decisions made
- Next steps
- Any state that must survive

## Scratchpad Format:

```markdown
# Session Scratchpad

Last Updated: [YYYY-MM-DD HH:MM]

## Active Issue
GitHub Issue #[number]: [title]
Branch: [branch-name]

## Current SDLC Phase
[Inception | Context | TDD | Implementation | Review]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Next Steps
1. [ ] Step 1
2. [ ] Step 2

## Context to Preserve
[Critical state, test results, blockers]
```

## Actions:

### To Save Context:
1. Read current scratchpad
2. Update with current state
3. Write back to file

### To Restore Context:
1. Read scratchpad
2. Summarize key points
3. Resume from "Next Steps"

$ARGUMENTS
