# Claude-Flow MCP Server

A Model Context Protocol (MCP) server that provides efficient access to claude-flow knowledge, commands, and agents. Reduces token usage by up to 80% when working with Claude Code.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that allows AI assistants like Claude to access external tools and data through a standardized interface. Instead of loading entire documentation into context, Claude can call specific tools on-demand.

## Why Use the MCP Server?

### Token Efficiency
- **Without MCP**: Load all commands and docs → 50k+ tokens
- **With MCP**: Call specific tools → 5-10k tokens
- **Savings**: 80% reduction in context usage

### Benefits
- ✅ Faster response times
- ✅ Lower costs (fewer tokens)
- ✅ On-demand knowledge retrieval
- ✅ Semantic search over documentation
- ✅ Always up-to-date (reads live files)

## Installation

### Step 1: Set Up RAG Pipeline (Required)

The MCP server uses the RAG pipeline for semantic search:

```bash
# Navigate to RAG pipeline
cd ../rag-pipeline

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Index the knowledge base (this may take a few minutes)
python -m ingestion.ingest
```

### Step 2: Install MCP Server Dependencies

```bash
# Navigate to MCP server
cd ../mcp-server

# Install dependencies (use same venv or create new one)
pip install -r requirements.txt
```

### Step 3: Add to Claude Code

Replace `/absolute/path/to/claude-flow` with your actual path:

```bash
# Option A: Local scope (this project only)
claude mcp add --transport stdio claude-flow -- \
  python /absolute/path/to/claude-flow/mcp-server/server.py

# Option B: User scope (available in all projects)
claude mcp add --transport stdio --scope user claude-flow -- \
  python /absolute/path/to/claude-flow/mcp-server/server.py
```

### Step 4: Verify Installation

In Claude Code, run:
```
/mcp
```

You should see `claude-flow` listed with 8 available tools.

## Available Tools

### Knowledge Search
- **`search_knowledge(query, top_k=5)`** - Semantic search over all documentation
- **`search_by_topic(topic, source_filter, top_k=5)`** - Search with source filtering

### Commands
- **`list_commands()`** - List all available slash commands
- **`get_command_details(command_name)`** - Get full command documentation

### Agents
- **`list_agents()`** - List all available agents
- **`get_agent_details(agent_name)`** - Get full agent prompt

### Workflow
- **`get_workflow_context()`** - Get the 5 Iron Laws and workflow overview
- **`get_quick_reference()`** - Get common workflows cheatsheet

## Usage Examples

### Example 1: Discover Available Commands

```
User: What commands are available?
Claude: [Calls list_commands()]
Returns:
[
  {"name": "tdd", "description": "Test-Driven Development workflow"},
  {"name": "debug", "description": "4-phase systematic debugging"},
  ...
]
```

### Example 2: Get Command Details

```
User: Show me how to use the /tdd command
Claude: [Calls get_command_details("tdd")]
Returns: Full command documentation with examples
```

### Example 3: Search for Information

```
User: How do I verify my implementation?
Claude: [Calls search_knowledge("how to verify implementation")]
Returns: Relevant documentation chunks from verification guides
```

### Example 4: Filtered Search

```
User: Find debugging commands
Claude: [Calls search_by_topic("debugging", source_filter="commands")]
Returns: Debugging-related content from commands directory
```

## Token Savings in Practice

### Scenario: Learning TDD Workflow

**Traditional Approach:**
```
1. Load /tdd command → 3k tokens
2. Load TDD examples → 5k tokens
3. Load related docs → 8k tokens
4. Load agent prompts → 6k tokens
Total: 22k tokens
```

**With MCP Server:**
```
1. list_commands() → 1k tokens
2. get_command_details("tdd") → 3k tokens
3. search_knowledge("tdd examples") → 2k tokens (top 3 results)
Total: 6k tokens
Savings: 73%
```

## Architecture

```
┌─────────────────┐
│   Claude Code   │
└────────┬────────┘
         │ MCP Protocol (stdio)
         ▼
┌─────────────────┐
│   MCP Server    │
│   (server.py)   │
└────────┬────────┘
         │
         ├─────► RAG Pipeline (semantic search)
         ├─────► Commands directory (list/get)
         └─────► Agents directory (list/get)
```

## Troubleshooting

### Server Won't Start
- Verify Python 3.10+ is installed: `python --version`
- Check dependencies: `pip list | grep mcp`
- Ensure RAG pipeline is set up (see Step 1)

### No Search Results
- Verify RAG index exists: `ls ../rag-pipeline/storage/chroma/`
- Re-index if needed: `cd ../rag-pipeline && python -m ingestion.ingest`

### Tools Not Showing in Claude Code
- Check server status: `/mcp`
- Verify path in add command is absolute
- Try removing and re-adding: `claude mcp remove claude-flow`

## Development

### Adding New Tools

1. Edit `server.py`
2. Add new function with `@mcp.tool()` decorator
3. Include docstring with Args and Returns
4. Handle errors gracefully
5. Test through Claude Code

Example:
```python
@mcp.tool()
def my_new_tool(param: str) -> dict:
    """Tool description.
    
    Args:
        param: Parameter description
    
    Returns:
        Result description
    """
    try:
        # Implementation
        return {"result": "success"}
    except Exception as e:
        return {"error": str(e)}
```

### Testing Locally

```bash
# Run server (will wait for stdin)
python server.py

# In another terminal, test through Claude Code
# Or send JSON-RPC requests manually
```

## Performance

- **Startup time**: <2 seconds
- **Search latency**: ~100ms per query
- **Memory usage**: ~200MB (with embeddings loaded)
- **Concurrent requests**: Supports multiple tools calls

## Roadmap

- [ ] Add resource support for `@claude-flow:command://tdd` syntax
- [ ] Implement prompt templates for common workflows
- [ ] Add HTTP transport option for remote access
- [ ] Add caching layer for frequently accessed data
- [ ] Create dashboard for usage metrics

## Support

- **Issues**: https://github.com/Dutchthenomad/claude-flow/issues
- **Documentation**: See `CONTEXT.md` for developer docs
- **RAG Pipeline**: See `../rag-pipeline/CONTEXT.md`

## License

MIT - See main repository LICENSE file
