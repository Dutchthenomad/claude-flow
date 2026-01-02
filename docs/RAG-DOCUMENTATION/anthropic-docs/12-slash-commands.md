# Slash Commands - Claude Code

> Source: https://code.claude.com/docs/en/slash-commands
> Scraped: 2025-12-13

## Built-in Commands

| Command | Purpose |
|---------|---------|
| `/agents` | Manage custom subagents |
| `/clear` | Clear conversation history |
| `/compact` | Compact conversation |
| `/config` | Open settings |
| `/context` | Visualize context usage |
| `/cost` | Show token usage |
| `/doctor` | Check installation health |
| `/exit` | Exit REPL |
| `/help` | Get usage help |
| `/hooks` | Manage hooks |
| `/ide` | Manage IDE integrations |
| `/init` | Initialize project with CLAUDE.md |
| `/login` | Switch accounts |
| `/mcp` | Manage MCP servers |
| `/memory` | Edit CLAUDE.md files |
| `/model` | Select model |
| `/permissions` | View/update permissions |
| `/plugin` | Manage plugins |
| `/resume` | Resume conversation |
| `/review` | Request code review |
| `/vim` | Enter vim mode |

## Custom Commands

### Project Commands
Shared with team via repository.

**Location**: `.claude/commands/`

```bash
mkdir -p .claude/commands
echo "Analyze for performance issues:" > .claude/commands/optimize.md
```

### Personal Commands
Available across all projects.

**Location**: `~/.claude/commands/`

```bash
mkdir -p ~/.claude/commands
echo "Review for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

## Arguments

### All Arguments: `$ARGUMENTS`
```markdown
Fix issue #$ARGUMENTS following our standards
```
Usage: `/fix-issue 123 high-priority`

### Positional: `$1`, `$2`, etc.
```markdown
Review PR #$1 with priority $2
```
Usage: `/review-pr 456 high`

## Bash Command Execution

Use `!` prefix to execute bash and include output:

```markdown
---
allowed-tools: Bash(git:*)
description: Create a git commit
---

## Context
- Git status: !`git status`
- Git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Task
Create a commit based on the above changes.
```

## File References

Use `@` to include files:
```markdown
Review @src/utils/helpers.js
Compare @src/old.js with @src/new.js
```

## Frontmatter Options

| Field | Purpose | Default |
|-------|---------|---------|
| `allowed-tools` | Tools the command can use | Inherits |
| `argument-hint` | Expected arguments | None |
| `description` | Brief description | First line |
| `model` | Specific model | Inherits |
| `disable-model-invocation` | Prevent SlashCommand tool | false |

### Example

```markdown
---
allowed-tools: Bash(git:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

Create a git commit with message: $ARGUMENTS
```

## Skills vs Slash Commands

| Aspect | Slash Commands | Skills |
|--------|----------------|--------|
| **Complexity** | Simple prompts | Complex capabilities |
| **Structure** | Single .md file | Directory + SKILL.md |
| **Discovery** | Explicit (`/command`) | Automatic (context) |
| **Use Case** | Quick, frequent prompts | Multi-step workflows |

## SlashCommand Tool

Claude can execute custom commands programmatically:

```
> Run /write-unit-test when starting tests.
```

### Permission Rules
- Exact: `SlashCommand:/commit`
- Prefix: `SlashCommand:/review-pr:*`

### Disable
- All: Add `SlashCommand` to deny rules
- Specific: Add `disable-model-invocation: true` to frontmatter
