# Agents - Agent Context

## Purpose
This folder contains **subagent definitions** - specialized AI assistants that Claude Code can delegate tasks to. Each agent has specific expertise and tool access.

## Contents
| Agent | Description |
|-------|-------------|
| `flow-keeper.md` | **RAG-powered project specialist** - answers questions, creates components, maintains CONTEXT.md |
| `rugs-expert.md` | **RAG-powered rugs.fun specialist** - WebSocket events, game mechanics, REPLAYER (auto-delegates for rugs.fun/REPLAYER questions) |
| `qa.md` | QA specialist - writes tests, validates coverage |
| `dev.md` | Developer - implements features, writes code |
| `github.md` | GitHub operations - PRs, issues, branches |
| `ml-engineer.md` | ML/RL specialist - training, models |
| `sysadmin.md` | System operations - Linux, services |
| `project-cleanup-agent.md` | Cleanup specialist - removes unused files |

## Integration Points
- Agents are invoked via the `Task` tool or `/agents` command
- Each agent operates in its own context window
- Agents can have restricted tool access via `tools:` frontmatter
- Agents can specify their model via `model:` frontmatter

## Development Status
- [x] Initial structure
- [x] Core agents migrated
- [ ] Agent documentation
- [ ] Tool permission audit
- [ ] Production ready

## For Future Agents
When creating or modifying agents:
1. Use the YAML frontmatter format with `name`, `description`, `tools`
2. Write clear system prompts defining the agent's role
3. Restrict tools to only what's needed (principle of least privilege)
4. Include "use PROACTIVELY" in description for auto-delegation
5. Test by explicitly invoking the agent
