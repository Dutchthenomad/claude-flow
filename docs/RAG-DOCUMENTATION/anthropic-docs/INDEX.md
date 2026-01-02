# Anthropic Documentation Index

> Scraped: 2025-12-13
> Source: https://code.claude.com/docs/en/

## Documentation Files

### Getting Started
| File | Topic | Key Content |
|------|-------|-------------|
| `01-overview.md` | Overview | Installation, features, why developers love it |
| `02-quickstart.md` | Quickstart | Step-by-step first session guide |
| `03-common-workflows.md` | Workflows | Debugging, refactoring, testing, PRs, images |

### Build with Claude Code
| File | Topic | Key Content |
|------|-------|-------------|
| `04-mcp.md` | MCP | Model Context Protocol, server setup, tools |
| `05-headless-mode.md` | Headless | Programmatic usage, CI/CD integration |
| `06-cli-reference.md` | CLI | All commands, flags, options |
| `07-plugins.md` | Plugins | Plugin structure, creation, management |
| `08-skills.md` | Skills | SKILL.md format, creation, best practices |
| `09-hooks.md` | Hooks | Event hooks, automation, security |
| `10-subagents.md` | Subagents | Custom agents, delegation, configuration |

### Configuration
| File | Topic | Key Content |
|------|-------|-------------|
| `11-settings.md` | Settings | All settings, permissions, environment vars |
| `12-slash-commands.md` | Commands | Custom commands, frontmatter, arguments |

## Quick Reference

### Plugin Structure
```
my-plugin/
├── .claude-plugin/plugin.json
├── commands/
├── agents/
├── skills/
└── hooks/hooks.json
```

### Skill Structure
```
my-skill/
├── SKILL.md (required)
├── reference.md (optional)
└── scripts/ (optional)
```

### Settings Hierarchy
1. Enterprise managed policies (highest)
2. Command line arguments
3. Local project settings
4. Shared project settings
5. User settings (lowest)

### Hook Events
- `PreToolUse` / `PostToolUse`
- `UserPromptSubmit`
- `SessionStart` / `SessionEnd`
- `Stop` / `SubagentStop`
- `PermissionRequest`

### Key Environment Variables
- `ANTHROPIC_API_KEY` - API authentication
- `MAX_THINKING_TOKENS` - Extended thinking budget
- `CLAUDE_CODE_USE_BEDROCK` - AWS Bedrock
- `CLAUDE_CODE_USE_VERTEX` - Google Vertex AI

## Repos to Clone (Based on Docs)

| Repo | Why | Priority |
|------|-----|----------|
| `claude-agent-sdk-python` | Build custom agents | High |
| `skills` | Official skill examples | High |
| `claude-plugins-official` | Official plugin examples | High |
| `claude-cookbooks` | Recipes and examples | Medium |
| `github-mcp-server` | GitHub integration | Medium |
| `claude-code-action` | CI/CD automation | Medium |
| `claude-quickstarts` | Starter templates | Low |
| `courses` | Learning materials | Low |

## Usage Notes

These docs inform:
1. **Plugin architecture** - How to structure claude-flow as a proper plugin
2. **Skill design** - How to create effective skills for the methodology
3. **Hook patterns** - How to automate workflow enforcement
4. **Agent creation** - How to build specialized subagents
5. **Settings** - How to configure permissions and behavior
