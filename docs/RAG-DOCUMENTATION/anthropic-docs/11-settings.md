# Claude Code Settings

> Source: https://code.claude.com/docs/en/settings
> Scraped: 2025-12-13

## Overview

Settings are defined in JSON files at different levels:

- **User settings**: `~/.claude/settings.json`
- **Project settings**:
  - `.claude/settings.json` (shared, checked in)
  - `.claude/settings.local.json` (personal, not checked in)
- **Enterprise policies**:
  - macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
  - Linux: `/etc/claude-code/managed-settings.json`
  - Windows: `C:\Program Files\ClaudeCode\managed-settings.json`

## Settings Precedence (Highest to Lowest)

1. Enterprise managed policies
2. Command line arguments
3. Local project settings
4. Shared project settings
5. User settings

## Core Configuration Options

| Key | Description | Example |
|-----|-------------|---------|
| `apiKeyHelper` | Custom auth script | `/bin/generate_api_key.sh` |
| `cleanupPeriodDays` | Session cleanup period | `20` |
| `companyAnnouncements` | Startup announcements | `["Welcome!"]` |
| `env` | Environment variables | `{"FOO": "bar"}` |
| `model` | Override default model | `"claude-sonnet-4-5-20250929"` |
| `alwaysThinkingEnabled` | Enable extended thinking | `true` |
| `disableAllHooks` | Disable all hooks | `true` |

## Permission Settings

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./secrets/**)"
    ],
    "ask": [
      "Bash(git push:*)"
    ],
    "additionalDirectories": [
      "../docs/"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

## Sandbox Settings (macOS/Linux)

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowLocalBinding": true
    }
  }
}
```

## Plugin Configuration

```json
{
  "enabledPlugins": {
    "formatter@company-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  }
}
```

## Attribution Settings

```json
{
  "attribution": {
    "commit": "🤖 Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
    "pr": "🤖 Generated with Claude Code"
  }
}
```

## Environment Variables

### Authentication
| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key |
| `ANTHROPIC_AUTH_TOKEN` | Custom Authorization header |

### Model Configuration
| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_MODEL` | Model setting |
| `MAX_THINKING_TOKENS` | Extended thinking budget |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Subagent model |

### Deployment
| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI |

### Bash Configuration
| Variable | Purpose |
|----------|---------|
| `BASH_DEFAULT_TIMEOUT_MS` | Default timeout |
| `BASH_MAX_OUTPUT_LENGTH` | Max output chars |

### Security
| Variable | Purpose |
|----------|---------|
| `DISABLE_TELEMETRY` | Opt out of telemetry |
| `DISABLE_AUTOUPDATER` | Disable auto-updates |

## Tools Available to Claude

| Tool | Permission Required |
|------|-------------------|
| **AskUserQuestion** | No |
| **Bash** | Yes |
| **Edit** | Yes |
| **Glob** | No |
| **Grep** | No |
| **Read** | No |
| **Write** | Yes |
| **NotebookEdit** | Yes |
| **WebFetch** | Yes |
| **WebSearch** | Yes |
| **Task** | No |
| **Skill** | Yes |
| **SlashCommand** | Yes |

## Complete Example

```json
{
  "permissions": {
    "allow": ["Bash(git diff:*)", "Bash(npm run:*)"],
    "deny": ["Read(./.env)", "Read(./secrets/**)"],
    "ask": ["Bash(git push:*)"]
  },
  "env": {
    "NODE_ENV": "development"
  },
  "attribution": {
    "commit": "🤖 Generated with Claude Code",
    "pr": "Generated with Claude Code"
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  },
  "model": "claude-sonnet-4-5-20250929"
}
```
