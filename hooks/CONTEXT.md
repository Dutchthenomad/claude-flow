# Hooks - Agent Context

## Purpose
This folder contains **workflow hooks** - automated scripts that execute at specific points in the Claude Code workflow. Hooks enable validation, context injection, and automation.

## Contents
| File | Description |
|------|-------------|
| `hooks.json` | Hook configuration (events, matchers, commands) |

## Available Hook Events
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool completion
- `UserPromptSubmit` - When user submits prompt
- `SessionStart` - When session begins
- `SessionEnd` - When session ends
- `Stop` - When agent finishes responding

## Integration Points
- Hooks are configured in `hooks.json`
- Hooks can be command-based (bash) or prompt-based (LLM)
- Hooks receive JSON input via stdin
- Exit codes control flow (0=success, 2=blocking error)

## Development Status
- [x] Initial structure
- [ ] Core hooks defined
- [ ] Hook scripts
- [ ] Integration tests
- [ ] Production ready

## For Future Agents
When creating hooks:
1. Define hooks in `hooks.json`
2. Use matchers to target specific tools
3. Keep hook scripts fast (< 60s timeout)
4. Use exit code 2 for blocking errors
5. Validate and sanitize all inputs
6. Test thoroughly - hooks run automatically
