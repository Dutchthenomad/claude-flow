# Anthropic Docs - Agent Context

## Purpose
Scraped official documentation from Anthropic. Primary knowledge source for Claude Code capabilities.

## Source
- URL: https://code.claude.com/docs/en/
- Scraped: 2025-12-13

## Documentation Files (12 total)

| File | Topic |
|------|-------|
| `01-overview.md` | Claude Code overview |
| `02-quickstart.md` | Getting started guide |
| `03-common-workflows.md` | Practical workflows |
| `04-mcp.md` | Model Context Protocol |
| `05-headless-mode.md` | Programmatic usage |
| `06-cli-reference.md` | CLI commands & flags |
| `07-plugins.md` | Plugin system |
| `08-skills.md` | Agent skills |
| `09-hooks.md` | Workflow hooks |
| `10-subagents.md` | Custom subagents |
| `11-settings.md` | Configuration |
| `12-slash-commands.md` | Custom commands |
| `INDEX.md` | Quick reference index |

## Scraping Status
- [x] Overview and quickstart
- [x] Plugins documentation
- [x] Skills documentation
- [x] Hooks documentation
- [x] Subagents documentation
- [x] MCP documentation
- [x] CLI reference
- [x] Settings documentation
- [x] Slash commands

## Integration Points
- Indexed by RAG pipeline (future)
- Informs plugin architecture decisions
- Guides skill and agent design
- Reference for hook patterns

## For Future Agents
When updating docs:
1. Check for documentation updates at source
2. Use numbered file naming (01-, 02-, etc.)
3. Preserve markdown formatting
4. Note scrape date in file header
5. Update INDEX.md after changes
6. Re-run RAG ingestion after updates
