# Claude-Flow

A systematic development workflow for producing high-quality, test-driven software with Claude Code.

## Overview

Claude-Flow is a comprehensive development methodology that integrates:
- **Test-Driven Development (TDD)** - RED-GREEN-REFACTOR cycle
- **Systematic Debugging** - 4-phase root cause analysis
- **Verification Gates** - Evidence before claims
- **Agentic Orchestration** - Specialized agents for different tasks

## The 5 Iron Laws

| Principle | Command | Rule |
|-----------|---------|------|
| TDD | `/tdd` | NO production code without failing test first |
| Verification | `/verify` | Evidence before claims, always |
| Debugging | `/debug` | NO fixes without root cause investigation |
| Planning | `/plan` | Plans must be executable with ZERO context |
| Isolation | `/worktree` | Isolated workspace for each feature |

## Installation

### Quick Install (Symlinks - Recommended for Development)

```bash
cd ~/Desktop/claude-flow
./install.sh
```

### Plugin Install (Recommended for Distribution)

```bash
# In Claude Code:
/plugin marketplace add ~/Desktop/claude-flow
/plugin install claude-flow@claude-flow-marketplace
```

## Project Structure

```
claude-flow/
├── commands/           # Slash commands (/tdd, /debug, /verify, etc.)
├── agents/             # Specialized subagents (QA, Dev, GitHub, etc.)
├── skills/             # Agent skills (auto-invoked capabilities)
├── hooks/              # Workflow automation hooks
├── docs/               # Documentation
├── rag-pipeline/       # RAG knowledge system (future)
├── knowledge/          # Scraped documentation
└── integrations/       # External repos & tools
```

## Commands

| Command | Description |
|---------|-------------|
| `/tdd` | Test-Driven Development workflow |
| `/debug` | 4-phase systematic debugging |
| `/verify` | Verification before completion |
| `/plan` | ULTRATHINK planning from GitHub Issues |
| `/worktree` | Git worktree for isolated development |
| `/review` | Code review before proceeding |
| `/run-tests` | Auto-detect and run test suite |
| `/scratchpad` | Save/restore context |
| `/autotest` | Quick test runner |

## Agents

| Agent | Role |
|-------|------|
| `@QA` | Write tests, validate coverage |
| `@Dev` | Implement features, write code |
| `@GitHub` | PRs, issues, branches |
| `@ML-Engineer` | ML/RL training, models |
| `@Sysadmin` | System operations |

## Thinking Budget

Control Claude's reasoning depth with keywords:

| Keyword | Tokens | Use For |
|---------|--------|---------|
| `think` | ~4k | Simple tasks |
| `think hard` | ~10k | Debugging |
| `think harder` | ~20k | Complex changes |
| `ultrathink` | ~32k | Architecture |

## Future Roadmap

- [ ] RAG pipeline for documentation retrieval
- [ ] Agent SDK integration for custom agents
- [ ] n8n orchestration for complex workflows
- [ ] MCP server integrations

## License

MIT

## Author

nomad - https://github.com/Dutchthenomad
