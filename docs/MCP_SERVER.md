# Claude-Flow MCP Server

## Executive Summary

The claude-flow MCP (Model Context Protocol) server provides efficient, on-demand access to the workflow's knowledge base, reducing token consumption by up to 80% when working with Claude Code.

## The Problem

When working with Claude Code on the claude-flow methodology, a typical session requires:

- **Commands documentation**: 9 command files (~15k tokens)
- **Agent prompts**: 8 agent files (~25k tokens)
- **Workflow documentation**: Multiple guide files (~20k tokens)
- **Knowledge base**: Anthropic docs and examples (~30k tokens)

**Total**: ~90k tokens loaded into context for comprehensive understanding.

With Claude Code's context limit and token costs, this creates:
- Slow response times
- High costs per session
- Context window exhaustion
- Repeated documentation loading

## The Solution

The MCP server acts as a smart knowledge retrieval system:

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code                          │
│  "How do I use the TDD workflow?"                       │
└──────────────────────┬──────────────────────────────────┘
                       │ MCP Protocol
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  MCP Server                             │
│  • Semantic search (RAG pipeline)                       │
│  • Command/agent metadata                               │
│  • Workflow context                                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Returns: 3k tokens                         │
│  • TDD command details                                  │
│  • Related examples                                     │
│  • Quick reference                                      │
└─────────────────────────────────────────────────────────┘
```

Instead of loading everything, Claude Code:
1. Calls MCP tools on-demand
2. Gets compact, structured responses
3. Only loads what's needed for the current task

## Token Savings Analysis

### Scenario 1: Learning TDD

**Traditional Approach:**
```
Load /tdd command          →  3k tokens
Load TDD examples          →  5k tokens
Load QA agent              →  6k tokens
Load verification docs     →  4k tokens
Load debugging guide       →  3k tokens
──────────────────────────────────────
Total:                       21k tokens
```

**With MCP Server:**
```
list_commands()            →  1k tokens (JSON list)
get_command_details("tdd") →  3k tokens
search_knowledge("tdd")    →  2k tokens (top 3 chunks)
──────────────────────────────────────
Total:                        6k tokens
Savings:                     15k tokens (71%)
```

### Scenario 2: Debugging Issues

**Traditional Approach:**
```
Load /debug command        →  2k tokens
Load debugging guide       →  8k tokens
Load all agent prompts     → 25k tokens
Load related examples      → 10k tokens
──────────────────────────────────────
Total:                       45k tokens
```

**With MCP Server:**
```
get_workflow_context()     →  1k tokens
search_by_topic("debug")   →  2k tokens
get_command_details("debug") → 2k tokens
──────────────────────────────────────
Total:                        5k tokens
Savings:                     40k tokens (89%)
```

### Scenario 3: Discovering Agents

**Traditional Approach:**
```
Load all agent files       → 25k tokens
Load agent documentation   →  5k tokens
──────────────────────────────────────
Total:                       30k tokens
```

**With MCP Server:**
```
list_agents()              →  1k tokens (JSON list)
get_agent_details("qa")    →  3k tokens
──────────────────────────────────────
Total:                        4k tokens
Savings:                     26k tokens (87%)
```

## Architecture

### Components

1. **MCP Server** (`mcp-server/server.py`)
   - 8 tools for knowledge access
   - FastMCP-based implementation
   - Stdio transport for Claude Code

2. **RAG Pipeline** (`rag-pipeline/`)
   - ChromaDB for vector storage
   - Sentence-transformers for embeddings
   - Semantic search with <100ms latency

3. **Knowledge Base**
   - Commands: 9 workflow commands
   - Agents: 8 specialized agents
   - Docs: Methodology documentation
   - Anthropic: Official Claude docs

### Available Tools

| Tool | Purpose | Avg Response |
|------|---------|--------------|
| `search_knowledge` | Semantic search across all docs | ~2k tokens |
| `list_commands` | List all commands | ~1k tokens |
| `get_command_details` | Get specific command | ~3k tokens |
| `list_agents` | List all agents | ~1k tokens |
| `get_agent_details` | Get specific agent | ~4k tokens |
| `get_workflow_context` | Get methodology overview | ~1k tokens |
| `search_by_topic` | Filtered semantic search | ~2k tokens |
| `get_quick_reference` | Common workflows cheatsheet | ~1k tokens |

## Benefits

### 1. Token Efficiency
- **70-90% reduction** in context usage
- **Faster responses** (less to process)
- **Lower costs** (fewer tokens)

### 2. Improved Workflow
- **On-demand access** to documentation
- **Semantic search** finds relevant info
- **Structured responses** (JSON, not raw markdown)

### 3. Always Up-to-Date
- **Reads live files** (no stale caches)
- **Re-index on changes** (simple workflow)
- **No sync issues** (single source of truth)

### 4. Developer Experience
- **Easy installation** (automated script)
- **Clear documentation** (3 guides)
- **Comprehensive testing** (test suite included)

## Real-World Impact

### Before MCP Server

A developer working on a new feature:

```
Session 1: Understanding TDD      → 25k tokens
Session 2: Implementing feature   → 30k tokens
Session 3: Debugging issues       → 45k tokens
Session 4: Code review           → 20k tokens
Session 5: Verification          → 15k tokens
────────────────────────────────────────────
Total:                            135k tokens
Cost (at $3/1M input tokens):    $0.41
Time: ~5 minutes processing
```

### With MCP Server

Same workflow with MCP:

```
Session 1: Understanding TDD      →  6k tokens
Session 2: Implementing feature   →  8k tokens
Session 3: Debugging issues       →  5k tokens
Session 4: Code review           →  7k tokens
Session 5: Verification          →  4k tokens
────────────────────────────────────────────
Total:                             30k tokens
Cost (at $3/1M input tokens):    $0.09
Time: ~1 minute processing

Savings: 105k tokens (78%)
         $0.32 (78%)
         4 minutes (80%)
```

## Installation

See [MCP Server README](../mcp-server/README.md) for detailed installation instructions.

Quick start:
```bash
cd mcp-server
./install.sh
```

## Usage

See [Usage Guide](../mcp-server/USAGE_GUIDE.md) for complete documentation.

Quick example:
```
User: "Show me the TDD workflow"
Claude: [Calls get_command_details("tdd")]
Result: Full TDD documentation in ~3k tokens
```

## Future Enhancements

- [ ] Resource support for `@claude-flow:command://tdd` syntax
- [ ] Prompt templates for common workflows
- [ ] HTTP transport for remote access
- [ ] Caching layer for frequently accessed data
- [ ] Usage analytics dashboard
- [ ] Custom embedding models
- [ ] Multi-language support

## Technical Details

- **Python 3.10+** required
- **FastMCP SDK** for server implementation
- **ChromaDB** for vector storage (local, no cloud)
- **sentence-transformers** for embeddings (runs locally)
- **Stdio transport** for Claude Code integration

## Performance

- **Startup**: <2 seconds (first call loads model)
- **Search**: ~100ms per query
- **Memory**: ~200MB with embeddings loaded
- **Disk**: ~50MB for index storage

## Contributing

See [CONTEXT.md](../mcp-server/CONTEXT.md) for developer documentation.

To add new tools:
1. Edit `server.py`
2. Add function with `@mcp.tool()` decorator
3. Update tests in `test_tools.py`
4. Update documentation

## Support

- **Issues**: https://github.com/Dutchthenomad/claude-flow/issues
- **Documentation**: See `mcp-server/` directory
- **Questions**: Open a discussion on GitHub

## License

MIT - Same as parent repository
