# MCP Server - Agent Context

## Purpose
Model Context Protocol server that exposes claude-flow knowledge, commands, and agents through a standardized API. Dramatically reduces token usage and context window consumption in Claude Code by providing efficient access to workflow documentation.

## Architecture

```
mcp-server/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
├── CONTEXT.md         # This file
└── README.md          # User documentation
```

## Available Tools

| Tool | Purpose | Returns |
|------|---------|---------|
| `search_knowledge` | Semantic search over all docs | Ranked document chunks |
| `list_commands` | List all slash commands | Command names + descriptions |
| `get_command_details` | Get full command content | Complete command markdown |
| `list_agents` | List all agents | Agent names + descriptions |
| `get_agent_details` | Get full agent prompt | Complete agent markdown |
| `get_workflow_context` | Get 5 Iron Laws overview | Workflow structure + principles |
| `search_by_topic` | Filtered semantic search | Topic-specific results |
| `get_quick_reference` | Common workflows cheatsheet | Quick reference guide |

## How It Reduces Token Usage

**Before MCP Server:**
- Claude Code needs entire command/agent files in context
- Repeated loading of documentation
- Large context windows (50k+ tokens)
- Slow response times

**With MCP Server:**
- Claude Code calls tools on-demand
- Only relevant chunks loaded
- Compact JSON responses
- Fast semantic retrieval
- Context stays under 10k tokens

**Token Savings Example:**
```
Traditional: Load all commands → 25k tokens
MCP Server: list_commands() → 2k tokens
            get_command_details("tdd") → 3k tokens
Total saved: 20k tokens (80% reduction)
```

## Integration with RAG Pipeline

The MCP server leverages the existing RAG pipeline:
- Uses ChromaDB for semantic search
- Shares embeddings infrastructure
- Reuses chunking and retrieval logic
- No duplication of indexing work

## Usage Patterns

### Discovery Pattern
```
1. list_commands() → See what's available
2. get_command_details("tdd") → Get specific command
3. Use command in workflow
```

### Search Pattern
```
1. search_knowledge("how to debug") → Find relevant docs
2. Review top 3 results
3. get_command_details("debug") → Get full details
```

### Workflow Pattern
```
1. get_workflow_context() → Understand iron laws
2. search_by_topic("verification", "commands") → Find verification commands
3. get_quick_reference() → Get workflow cheatsheet
```

## Installation

### Prerequisites
```bash
# Install RAG pipeline dependencies first
cd ../rag-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Index knowledge base
python -m ingestion.ingest
```

### Install MCP Server
```bash
cd ../mcp-server
pip install -r requirements.txt
```

### Add to Claude Code
```bash
# Local scope (this project only)
claude mcp add --transport stdio claude-flow -- \
  python /absolute/path/to/claude-flow/mcp-server/server.py

# User scope (all projects)
claude mcp add --transport stdio --scope user claude-flow -- \
  python /absolute/path/to/claude-flow/mcp-server/server.py
```

### Verify Installation
```bash
# In Claude Code
/mcp
# Should show "claude-flow" server with 8 tools
```

## Development Status
- [x] Core server structure
- [x] Knowledge search tools
- [x] Command/agent listing tools
- [x] Workflow context tools
- [x] RAG integration
- [ ] Resource support (for @ mentions)
- [ ] Prompt templates
- [ ] HTTP transport option
- [ ] Caching layer

## For Future Agents

### When Adding Tools
1. Define tool with `@mcp.tool()` decorator
2. Add comprehensive docstring
3. Include type hints
4. Handle errors gracefully
5. Return structured data (not raw text)
6. Update this CONTEXT.md

### Best Practices
- Keep tool responses compact
- Use JSON for structured data
- Provide meaningful error messages
- Don't load entire files unless needed
- Prefer search over bulk listing
- Cache frequently accessed data

### Testing Tools
```bash
# Test server starts
python server.py &
PID=$!

# Test tool manually (if MCP SDK provides inspector)
# Otherwise, test through Claude Code

kill $PID
```
