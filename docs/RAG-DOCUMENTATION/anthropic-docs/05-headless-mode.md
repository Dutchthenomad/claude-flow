# Headless Mode - Claude Code

> Source: https://code.claude.com/docs/en/headless
> Scraped: 2025-12-13

Run Claude Code programmatically without interactive UI.

## Basic Usage

Use `--print` (or `-p`) flag for non-interactive mode:

```bash
claude -p "Stage my changes and write a set of commits for them" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```

## Configuration Options

| Flag | Description | Example |
|------|-------------|---------|
| `--print`, `-p` | Run in non-interactive mode | `claude -p "query"` |
| `--output-format` | Output format (`text`, `json`, `stream-json`) | `claude -p --output-format json` |
| `--resume`, `-r` | Resume conversation by session ID | `claude --resume abc123` |
| `--continue`, `-c` | Continue most recent conversation | `claude --continue` |
| `--verbose` | Enable verbose logging | `claude --verbose` |
| `--append-system-prompt` | Append to system prompt | `claude --append-system-prompt "Custom instruction"` |
| `--allowedTools` | List of allowed tools | `claude --allowedTools "Bash,Read"` |
| `--disallowedTools` | List of denied tools | `claude --disallowedTools "mcp__github"` |
| `--mcp-config` | Load MCP servers from JSON | `claude --mcp-config servers.json` |

## Multi-Turn Conversations

```bash
# Continue most recent conversation
claude --continue "Now refactor this for better performance"

# Resume specific conversation
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"

# Resume in non-interactive mode
claude --resume abc123 "Fix all linting issues" --no-interactive
```

## Output Formats

### Text Output (Default)
```bash
claude -p "Explain file src/components/Header.tsx"
```

### JSON Output
```bash
claude -p "How does the data layer work?" --output-format json
```

Response format:
```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

### Streaming JSON Output
```bash
claude -p "Build an application" --output-format stream-json
```

## Agent Integration Examples

### SRE Incident Response Bot

```bash
#!/bin/bash
investigate_incident() {
    local incident_description="$1"
    local severity="${2:-medium}"

    claude -p "Incident: $incident_description (Severity: $severity)" \
      --append-system-prompt "You are an SRE expert. Diagnose the issue." \
      --output-format json \
      --allowedTools "Bash,Read,WebSearch,mcp__datadog" \
      --mcp-config monitoring-tools.json
}

investigate_incident "Payment API returning 500 errors" "high"
```

### Automated Security Review

```bash
audit_pr() {
    local pr_number="$1"
    gh pr diff "$pr_number" | claude -p \
      --append-system-prompt "Review this PR for vulnerabilities." \
      --output-format json \
      --allowedTools "Read,Grep,WebSearch"
}

audit_pr 123 > security-report.json
```

### Multi-Turn Legal Assistant

```bash
session_id=$(claude -p "Start legal review session" --output-format json | jq -r '.session_id')
claude -p --resume "$session_id" "Review contract.pdf for liability clauses"
claude -p --resume "$session_id" "Check compliance with GDPR requirements"
claude -p --resume "$session_id" "Generate executive summary of risks"
```

## Best Practices

- **Use JSON output format** for programmatic parsing
- **Handle errors gracefully** - check exit codes and stderr
- **Use session management** for multi-turn context
- **Consider timeouts** for long operations:
  ```bash
  timeout 300 claude -p "$complex_prompt" || echo "Timed out"
  ```
- **Respect rate limits** with delays between calls
