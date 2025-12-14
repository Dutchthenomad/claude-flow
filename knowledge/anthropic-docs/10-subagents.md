# Subagents in Claude Code

> Source: https://code.claude.com/docs/en/subagents
> Scraped: 2025-12-13

Subagents are specialized AI assistants that Claude Code can delegate tasks to.

## Key Benefits

- **Context Preservation** - Each subagent has its own context window
- **Specialized Expertise** - Fine-tuned for specific domains
- **Reusability** - Use across projects, share with teams
- **Flexible Permissions** - Different tool access levels

## Creating Subagents

### Quick Start
```bash
/agents
```

Opens interactive menu to view, create, edit, or delete subagents.

### File Format

Markdown files with YAML frontmatter:

```yaml
---
name: your-sub-agent-name
description: When this subagent should be invoked
tools: tool1, tool2, tool3  # Optional
model: sonnet  # Optional
permissionMode: default  # Optional
skills: skill1, skill2  # Optional
---

Your subagent's system prompt goes here.
```

### File Locations

| Type | Location | Scope |
|------|----------|-------|
| **Project** | `.claude/agents/` | Current project (highest priority) |
| **User** | `~/.claude/agents/` | All projects |

### CLI-Based Configuration

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | When Claude should use this agent |
| `tools` | No | Comma-separated tools (inherits all if omitted) |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | No | Comma-separated skill names |

## Built-In Subagents

### General-Purpose
- Model: Sonnet
- Complex research, multi-step operations, code modifications

### Plan Subagent
- Read-only exploration
- Tools: Read, Glob, Grep, Bash (exploration only)

### Explore Subagent
- Model: Haiku (fast)
- Strictly read-only
- Thoroughness levels: Quick, Medium, Very thorough

## Using Subagents

### Automatic Delegation
Claude delegates based on task description and subagent descriptions.

**Tip:** Include "use PROACTIVELY" in description for auto-delegation.

### Explicit Invocation
```bash
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my changes
```

## Example Subagents

### Code Reviewer

```yaml
---
name: code-reviewer
description: Expert code review. Use immediately after writing code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code clarity and readability
- Well-named functions/variables
- No duplicated code
- Proper error handling
- No exposed secrets
- Input validation
- Test coverage
- Performance considerations

Provide feedback by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)
```

### Debugger

```yaml
---
name: debugger
description: Debugging specialist. Use when encountering issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states
```

## Advanced Usage

### Chaining Subagents
```bash
> First use code-analyzer to find issues, then use optimizer to fix them
```

### Resumable Subagents
```bash
> Resume agent abc123 and analyze authorization logic as well
```

## Best Practices

- **Start with Claude-generated agents** - Generate first, then customize
- **Design focused subagents** - Single, clear responsibilities
- **Write detailed prompts** - Specific instructions and constraints
- **Limit tool access** - Only grant necessary tools
- **Version control** - Check project subagents into git
