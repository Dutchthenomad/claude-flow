# Claude-Flow - Project Context

## Project Overview
Claude-Flow is a systematic development workflow for Claude Code. It provides commands, agents, skills, and automation hooks that enforce best practices like TDD, systematic debugging, and verification gates.

## Architecture

### Plugin Structure
This project is structured as a Claude Code plugin:
- `.claude-plugin/plugin.json` - Plugin manifest
- `.claude-plugin/marketplace.json` - Self-hosted marketplace
- `commands/` - Slash commands
- `agents/` - Subagent definitions
- `skills/` - Agent skills
- `hooks/` - Workflow hooks

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `commands/` | User-invoked slash commands |
| `agents/` | Specialized subagents |
| `skills/` | Model-invoked capabilities |
| `hooks/` | Workflow automation |
| `docs/` | Human + agent documentation |
| `rag-pipeline/` | Future RAG knowledge system |
| `knowledge/` | Scraped documentation |
| `integrations/` | External repos & tools |

## Development Workflow

### The 5 Iron Laws
1. **TDD**: NO code without failing test first
2. **Verification**: Evidence before claims
3. **Debugging**: 4-phase root cause analysis
4. **Planning**: Zero-context executable plans
5. **Isolation**: Git worktrees for features

### Commands
- `/tdd` - Test-Driven Development
- `/debug` - Systematic debugging
- `/verify` - Verification gate
- `/plan` - ULTRATHINK planning
- `/worktree` - Isolated workspace

## Testing
```bash
# Verify plugin structure
ls -la .claude-plugin/

# Test installation
./install.sh --symlink

# Verify commands work
# (In Claude Code) /tdd "test"
```

## Context Files
Each folder contains a `CONTEXT.md` that provides:
- Purpose of the folder
- Contents description
- Integration points
- Development status
- Guidance for future agents

## Future Development

### RAG Pipeline
Location: `rag-pipeline/`
- Document ingestion
- Vector embeddings
- Semantic search
- Knowledge retrieval

### Integrations
Location: `integrations/`
- Anthropic official repos (Agent SDK, cookbooks, etc.)
- Community tools (superpowers, etc.)
- MCP servers

## Contributing
1. Follow the 5 Iron Laws
2. Use `/tdd` for all new features
3. Run `/verify` before completing
4. Update relevant CONTEXT.md files
