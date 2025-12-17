# Repository Guidelines

## Project Structure & Module Organization
This repo is a Claude Code plugin/workflow toolkit.

- `commands/`: Slash-command definitions (Markdown with YAML frontmatter, e.g. `commands/tdd.md`).
- `agents/`: Subagent prompts/roles used by the workflow (e.g. `agents/qa.md`).
- `skills/`, `hooks/`: Model-invoked skills and automation hooks.
- `.claude-plugin/`: Plugin manifests for Claude Code (`plugin.json`, `marketplace.json`).
- `docs/`: Human-facing documentation and `docs/WORKFLOW_QUICKREF.md`.
- `knowledge/`: Scraped/reference documentation used for retrieval.
- `integrations/`: Pointers/clones of external tools and reference repos (often gitignored).
- `rag-pipeline/`: Python RAG prototype (ingestion → embeddings → ChromaDB → retrieval).

## Build, Test, and Development Commands
- Install for local development (symlinks into `~/.claude/`): `./install.sh --symlink`
- Install as a plugin (for distribution): `./install.sh --plugin`
- Uninstall symlinks: `./uninstall.sh` (use `./uninstall.sh --restore` to restore backups)

RAG pipeline setup and usage:
- Setup: `cd rag-pipeline && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Index knowledge: `python -m ingestion.ingest`
- Query index: `python -m retrieval.retrieve "your question" -k 5`

## Coding Style & Naming Conventions
- Markdown: keep headings consistent; command/agent files start with YAML frontmatter (`---`, `description: ...`, `---`).
- Python (`rag-pipeline/`): 4-space indentation, type hints where practical, small single-purpose modules.
- Prefer repository-relative paths; avoid committing machine-specific paths or generated artifacts.

## Testing Guidelines
There is no repo-wide test suite today. When adding behavior (especially under `rag-pipeline/`), add `pytest` tests (suggested: `rag-pipeline/tests/test_*.py`) and run: `python -m pytest -v`.
Follow the workflow’s TDD rule: tests should fail before implementation.

## Commit & Pull Request Guidelines
- Commits follow a conventional pattern (seen in history): `feat: ...`, `docs: ...`, `chore: ...`, `fix: ...`.
- Keep commits small and scoped; update `CONTEXT.md` files when you change directory intent/contents.
- PRs should include: what/why, how to verify (commands), and screenshots for doc/UX changes when relevant.

## Security & Configuration Tips
- Do not commit secrets or local settings (`.env`, `*.local.json` are ignored by default).
- RAG indices are regeneratable; keep `rag-pipeline/storage/` and caches out of commits.
