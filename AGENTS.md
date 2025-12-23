# Repository Guidelines

## Project Overview

Claude-Flow is a systematic development workflow for Claude Code, providing commands, agents, skills, and automation hooks that enforce best practices.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `commands/` | Slash-command definitions (Markdown with YAML frontmatter) |
| `agents/` | Subagent prompts/roles |
| `skills/`, `hooks/` | Model-invoked skills and automation |
| `.claude-plugin/` | Plugin manifests for Claude Code |
| `docs/` | Human-facing documentation |
| `knowledge/` | Scraped/reference documentation |
| `rag-pipeline/` | Python RAG (ingestion -> ChromaDB -> retrieval) |
| `jupyter/` | Browser-based review environment |
| `integrations/` | External tools and reference repos |

## Quick Start

### JupyterLab (Review Environment)
```bash
./start-jupyter.sh
# Opens http://localhost:8765
```

### RAG Pipeline
```bash
cd rag-pipeline
source .venv/bin/activate
python -m ingestion.ingest        # Index knowledge
python -m retrieval.retrieve "query" -k 5  # Search
```

### Install as Plugin
```bash
./install.sh --symlink   # Development (symlinks to ~/.claude/)
./install.sh --plugin    # Distribution
```

## Coding Conventions

- **Markdown**: YAML frontmatter for commands/agents
- **Python**: 4-space indent, type hints
- **Commits**: `feat:`, `docs:`, `fix:`, `chore:`
- **CONTEXT.md**: Update when changing directory purpose

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project context for Claude |
| `knowledge/rugs-events/CONTEXT.md` | CANONICAL promotion laws |
| `jupyter/config.env` | JupyterLab configuration |
| `docs/WORKFLOW_QUICKREF.md` | Development workflow reference |

## Version Control

- Notebooks auto-stripped of outputs via `nbstripout`
- RAG indices are regeneratable (gitignored)
- Local configs (`.env`, `*.local.json`) are gitignored

---

*Last updated: December 22, 2025*
