# Claude-Flow

[![Code Review](https://github.com/Dutchthenomad/claude-flow/actions/workflows/code-review.yml/badge.svg)](https://github.com/Dutchthenomad/claude-flow/actions/workflows/code-review.yml)
[![Validation](https://github.com/Dutchthenomad/claude-flow/actions/workflows/validate.yml/badge.svg)](https://github.com/Dutchthenomad/claude-flow/actions/workflows/validate.yml)
[![Coverage](https://github.com/Dutchthenomad/claude-flow/actions/workflows/coverage.yml/badge.svg)](https://github.com/Dutchthenomad/claude-flow/actions/workflows/coverage.yml)
[![Security](https://github.com/Dutchthenomad/claude-flow/actions/workflows/security.yml/badge.svg)](https://github.com/Dutchthenomad/claude-flow/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/Dutchthenomad/claude-flow)](https://github.com/Dutchthenomad/claude-flow/releases)

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

## CI/CD Pipeline: The Recursive Loop

Claude-Flow creates a **closed-loop development system** where the methodology enforces itself both locally (via Claude Code) and remotely (via GitHub Actions).

```
LOCAL (Claude Code)              GITHUB (Actions)
─────────────────────           ─────────────────
/tdd      ◄───────────────────► Tests pass?
/verify   ◄───────────────────► Validation checks
/review   ◄───────────────────► Claude Code Action
```

### Automated Workflows

| Workflow | Purpose |
|----------|---------|
| `validate.yml` | Markdown lint, shell lint, plugin validation, self-dogfooding |
| `code-review.yml` | Complexity analysis, security scanning, impact analysis |
| `claude.yml` | AI-powered PR review using claude-flow methodology |
| `qodo-review.yml` | Qodo AI-powered intelligent code analysis |
| `coverage.yml` | Test coverage tracking with badges |
| `security.yml` | CodeQL, Trivy, Bandit, dependency scanning |
| `pr-labeler.yml` | Automatic PR labels based on changes |
| `release.yml` | Tag-based releases with changelogs |

### Claude Code Action

Mention `@claude` in any issue or PR comment to get AI-powered assistance. Add the `claude-review` label for automatic methodology review.

**Documentation**:
- [Recursive Loop](docs/ci-cd/RECURSIVE_LOOP.md) - How local and remote integrate
- [CodeRabbit Integration Guide](docs/ci-cd/CODERABBIT_INTEGRATION.md) - AI code review with methodology enforcement
- [Qodo Integration Guide](docs/ci-cd/QODO_INTEGRATION.md) - AI code review setup
- [CI/CD Guide](docs/ci-cd/CI_CD_GUIDE.md) - Complete reference
- [Quick Reference](docs/ci-cd/QUICK_REFERENCE.md) - Command cheat sheet
- [Setup Guide](docs/ci-cd/SETUP_GUIDE.md) - Activation steps
- [Onboarding](docs/ci-cd/ONBOARDING.md) - Developer guide

## Contributing

We welcome contributions! Please see:
- [Developer Onboarding](docs/ci-cd/ONBOARDING.md) - Get started
- [Pull Request Template](.github/pull_request_template.md) - PR guidelines
- [Issue Templates](.github/ISSUE_TEMPLATE/) - Report bugs or request features

All PRs are automatically reviewed for:
- AI-powered code review (CodeRabbit, Qodo)
- Code complexity (Radon)
- Security issues (Bandit, Trivy, Gitleaks)
- Test coverage (pytest)
- Change impact
- Claude-Flow methodology compliance

## MCP Server (Reduce Token Usage)

Claude-Flow includes an MCP (Model Context Protocol) server that dramatically reduces token usage when working with Claude Code. Instead of loading entire documentation into context, Claude can query specific information on-demand.

**Benefits:**
- 🚀 80% reduction in token usage
- ⚡ Faster response times
- 🔍 Semantic search over all documentation
- 📚 On-demand access to commands, agents, and knowledge

**Quick Start:**
```bash
# 1. Set up RAG pipeline (indexes knowledge base)
cd rag-pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m ingestion.ingest

# 2. Install MCP server
cd ../mcp-server
pip install -r requirements.txt

# 3. Add to Claude Code
claude mcp add --transport stdio claude-flow -- \
  python /absolute/path/to/claude-flow/mcp-server/server.py
```

**Documentation:**
- [MCP Server README](mcp-server/README.md) - Installation and usage
- [MCP Server Context](mcp-server/CONTEXT.md) - Developer documentation

## Future Roadmap

- [x] RAG pipeline for documentation retrieval
- [x] MCP server for efficient knowledge access
- [ ] Agent SDK integration for custom agents
- [ ] n8n orchestration for complex workflows
- [ ] Additional MCP server integrations

## License

MIT

## Author

nomad - https://github.com/Dutchthenomad
