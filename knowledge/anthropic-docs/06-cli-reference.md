# Claude Code CLI Reference

> Source: https://code.claude.com/docs/en/cli-reference
> Scraped: 2025-12-13

Complete reference for Claude Code command-line interface.

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"` |
| `cat file \| claude -p` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -r "<id>" "query"` | Resume session by ID | `claude -r "abc123" "Finish PR"` |
| `claude update` | Update to latest version | `claude update` |
| `claude mcp` | Configure MCP servers | See MCP documentation |

## Core Flags

| Flag | Description |
|------|-------------|
| `--add-dir` | Add additional working directories |
| `--agent` | Specify an agent for the session |
| `--agents` | Define custom subagents via JSON |
| `--allowedTools` | Tools allowed without prompting |
| `--append-system-prompt` | Append to default system prompt |
| `--continue`, `-c` | Load most recent conversation |
| `--dangerously-skip-permissions` | Skip permission prompts |
| `--debug` | Enable debug mode |
| `--disallowedTools` | Tools disallowed without prompting |

## Model & Output Flags

| Flag | Description |
|------|-------------|
| `--fallback-model` | Enable automatic fallback model |
| `--model` | Set model (sonnet/opus or full name) |
| `--output-format` | Output format (text/json/stream-json) |
| `--print`, `-p` | Print response, non-interactive |
| `--json-schema` | Get validated JSON matching schema |

## Session Flags

| Flag | Description |
|------|-------------|
| `--resume`, `-r` | Resume specific session by ID |
| `--session-id` | Use specific session ID (UUID) |
| `--fork-session` | Create new session instead of reusing |

## System Prompt Flags

| Flag | Behavior |
|------|----------|
| `--system-prompt` | **Replaces** entire default prompt |
| `--system-prompt-file` | **Replaces** with file contents (print only) |
| `--append-system-prompt` | **Appends** to default prompt |

## Tool & Permission Flags

| Flag | Description |
|------|-------------|
| `--ide` | Auto-connect to IDE on startup |
| `--permission-mode` | Begin in specified mode (plan, acceptEdits) |
| `--permission-prompt-tool` | MCP tool for permission prompts |
| `--tools` | Specify available tools |

## Configuration Flags

| Flag | Description |
|------|-------------|
| `--mcp-config` | Load MCP servers from JSON |
| `--plugin-dir` | Load plugins from directories |
| `--settings` | Path to settings JSON |
| `--strict-mcp-config` | Only use MCP from --mcp-config |

## Advanced Flags

| Flag | Description |
|------|-------------|
| `--include-partial-messages` | Include partial streaming events |
| `--input-format` | Input format (text/stream-json) |
| `--max-turns` | Limit agentic turns |
| `--verbose` | Enable verbose logging |
| `--version`, `-v` | Output version number |

## Agents Flag Format

```json
{
  "code-reviewer": {
    "description": "Expert code reviewer.",
    "prompt": "You are a senior code reviewer.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}
```

### Agents Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | When to invoke |
| `prompt` | Yes | System prompt |
| `tools` | No | Specific tools array |
| `model` | No | Model alias (sonnet/opus/haiku) |

## Common Usage Patterns

```bash
# Print mode with JSON output
claude -p "query" --output-format json

# Continue previous session
claude -c "Add TypeScript types"

# Use custom subagents
claude --agents '{"reviewer":{...}}' "Check my code"

# Set model explicitly
claude --model claude-opus-4-1-20250805 "Generate docs"

# Stream JSON with partial messages
claude -p --output-format stream-json --include-partial-messages "query"
```
