# Claude-Flow

[![Code Review](https://github.com/Dutchthenomad/claude-flow/actions/workflows/code-review.yml/badge.svg)](https://github.com/Dutchthenomad/claude-flow/actions/workflows/code-review.yml)
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

## CI/CD Pipeline

Claude-Flow includes a comprehensive automated CI/CD pipeline:

- **Qodo AI Code Review** - AI-powered intelligent code analysis (NEW ✨)
- **Automated Code Review** - Complexity analysis, security scanning, impact analysis
- **Smart PR Labeling** - Automatic labels based on changes, size, and type
- **Test Coverage** - Coverage tracking with badges and PR comments
- **Automated Releases** - Tag-based releases with changelogs
- **Security Scanning** - CodeQL, Trivy, Bandit, and Dependabot

**Documentation**:
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
- AI-powered code review (Qodo)
- Code complexity (Radon)
- Security issues (Bandit, Trivy)
- Test coverage (pytest)
- Change impact

## Future Roadmap

- [ ] RAG pipeline for documentation retrieval
- [ ] Agent SDK integration for custom agents
- [ ] n8n orchestration for complex workflows
- [ ] MCP server integrations

## License

MIT

## Author

nomad - https://github.com/Dutchthenomad
