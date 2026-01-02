# Claude Code Hooks

> Source: https://code.claude.com/docs/en/hooks
> Scraped: 2025-12-13

Hooks are automated scripts that execute at specific points in your workflow.

## Configuration

Hooks are configured in settings files:
- `~/.claude/settings.json` - User settings
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local project settings

### Basic Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

## Hook Types

### Command Hooks (`type: "command"`)
Execute bash scripts with JSON input via stdin.

**Exit codes:**
- **0**: Success
- **2**: Blocking error (feedback to Claude)
- **Other**: Non-blocking error

### Prompt-Based Hooks (`type: "prompt"`)
Use LLM evaluation for intelligent decisions.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop. Check if all tasks complete.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Available Hook Events

| Event | When | Use Case |
|-------|------|----------|
| `PreToolUse` | Before tool execution | Validate inputs, modify parameters |
| `PostToolUse` | After tool completion | Add context, validate results |
| `UserPromptSubmit` | User submits prompt | Inject context, validate input |
| `SessionStart` | Session begins | Load context, setup environment |
| `SessionEnd` | Session ends | Cleanup |
| `Stop` | Agent finishes | Verify completion |
| `SubagentStop` | Subagent finishes | Verify subagent work |
| `Notification` | Notification sent | Custom notifications |
| `PreCompact` | Before compact | Custom handling |
| `PermissionRequest` | Permission dialog shown | Auto-approve/deny |

## Hook Input

Hooks receive JSON via stdin:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": { /* tool-specific */ },
  "tool_use_id": "toolu_01ABC123..."
}
```

## Practical Examples

### Bash Command Validation

```python
#!/usr/bin/env python3
import json, re, sys

VALIDATION_RULES = [
    (r"\bgrep\b(?!.*\|)", "Use 'rg' instead of 'grep'"),
    (r"\bfind\s+\S+\s+-name\b", "Use 'rg --files' instead"),
]

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
command = input_data.get("tool_input", {}).get("command", "")

if tool_name != "Bash":
    sys.exit(0)

issues = [msg for pattern, msg in VALIDATION_RULES if re.search(pattern, command)]

if issues:
    for msg in issues:
        print(f"• {msg}", file=sys.stderr)
    sys.exit(2)  # Blocking error
```

### Context Injection

```python
#!/usr/bin/env python3
import json, sys, datetime

input_data = json.load(sys.stdin)
context = f"Current time: {datetime.datetime.now()}"
print(json.dumps({
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": context,
  },
}))
sys.exit(0)
```

## Security Best Practices

1. **Validate and sanitize inputs**
2. **Always quote shell variables** - `"$VAR"` not `$VAR`
3. **Block path traversal** - Check for `..`
4. **Use absolute paths** - `$CLAUDE_PROJECT_DIR`
5. **Skip sensitive files** - `.env`, `.git/`, keys

## Working with MCP Tools

MCP tools follow pattern `mcp__<server>__<tool>`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation' >> ~/log"
          }
        ]
      }
    ]
  }
}
```

## Debugging

```bash
claude --debug
```

Shows hook execution, commands, success/failure, and output.
