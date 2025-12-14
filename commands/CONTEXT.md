# Commands - Agent Context

## Purpose
This folder contains **slash commands** - user-invoked prompts that execute specific workflows. Each `.md` file defines a command accessible via `/command-name` in Claude Code.

## Contents
| Command | Description |
|---------|-------------|
| `/tdd` | Test-Driven Development - RED-GREEN-REFACTOR cycle |
| `/debug` | 4-phase systematic debugging protocol |
| `/verify` | Verification gate before claiming completion |
| `/plan` | ULTRATHINK planning from GitHub Issues |
| `/worktree` | Git worktree creation for isolated development |
| `/review` | Code review before proceeding |
| `/run-tests` | Auto-detect and run project test suite |
| `/scratchpad` | Save/restore context across sessions |
| `/autotest` | Quick test runner without prompts |

## Integration Points
- Commands are loaded by Claude Code from this directory (via plugin or symlink)
- Commands can reference skills via the `Skill` tool
- Commands support `$ARGUMENTS` for user input
- Commands can use frontmatter for tool restrictions and model selection

## Development Status
- [x] Initial structure
- [x] Core commands migrated
- [ ] Command documentation
- [ ] Integration tests
- [ ] Production ready

## For Future Agents
When modifying commands:
1. Follow the existing frontmatter format
2. Keep commands focused on ONE workflow
3. Use `$ARGUMENTS` for user input
4. Test changes by running the command in Claude Code
5. Update this CONTEXT.md if adding new commands
