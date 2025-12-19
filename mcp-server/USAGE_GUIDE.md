# MCP Server Usage Guide

Complete guide for using the claude-flow MCP server with Claude Code.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Tool Reference](#tool-reference)
- [Usage Patterns](#usage-patterns)
- [Token Optimization](#token-optimization)
- [Troubleshooting](#troubleshooting)

## Prerequisites

1. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Claude Code installed**
   ```bash
   claude --version
   ```

3. **Git clone of claude-flow repository**
   ```bash
   git clone https://github.com/Dutchthenomad/claude-flow.git
   cd claude-flow
   ```

## Installation

### Option 1: Automated Installation (Recommended)

```bash
cd mcp-server
./install.sh
```

This script will:
1. Set up the RAG pipeline with dependencies
2. Index the knowledge base
3. Install MCP server dependencies
4. Run tests to verify installation

### Option 2: Manual Installation

#### Step 1: Set up RAG Pipeline

```bash
cd rag-pipeline
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ingestion.ingest
```

#### Step 2: Install MCP Server

```bash
cd ../mcp-server
pip install -r requirements.txt
```

#### Step 3: Test Installation

```bash
python test_tools.py
```

### Add to Claude Code

```bash
# Replace /path/to/claude-flow with your actual path

# Local scope (this project only)
claude mcp add --transport stdio claude-flow -- \
  python /path/to/claude-flow/mcp-server/server.py

# OR user scope (all projects)
claude mcp add --transport stdio --scope user claude-flow -- \
  python /path/to/claude-flow/mcp-server/server.py
```

### Verify Installation

In Claude Code:
```
/mcp
```

You should see:
```
claude-flow - 8 tools available
  - search_knowledge
  - list_commands
  - get_command_details
  - list_agents
  - get_agent_details
  - get_workflow_context
  - search_by_topic
  - get_quick_reference
```

## Quick Start

### Example 1: Discover Commands

**User:** What commands are available in claude-flow?

**Claude uses:** `list_commands()`

**Result:**
```json
[
  {"name": "tdd", "description": "Test-Driven Development workflow"},
  {"name": "debug", "description": "4-phase systematic debugging"},
  {"name": "verify", "description": "Verification before completion"},
  ...
]
```

### Example 2: Learn TDD Workflow

**User:** How do I use the TDD workflow?

**Claude uses:** `get_command_details("tdd")`

**Result:** Full TDD command documentation with examples

### Example 3: Search Knowledge Base

**User:** How do I verify my implementation?

**Claude uses:** `search_knowledge("verify implementation", top_k=3)`

**Result:** Top 3 relevant documentation chunks about verification

## Tool Reference

### 1. search_knowledge

Semantic search across all documentation.

```python
search_knowledge(
    query: str,           # Natural language query
    top_k: int = 5        # Number of results (default: 5)
)
```

**Use cases:**
- "How do I debug issues?"
- "What is the TDD workflow?"
- "How to create GitHub issues?"

**Returns:** List of document chunks with:
- `text`: Content of the chunk
- `source`: File path
- `line_start` / `line_end`: Location in file
- `headers`: Markdown headers for context
- `score`: Relevance score (0-1)

### 2. list_commands

Get all available slash commands.

```python
list_commands()
```

**Returns:** List of commands with:
- `name`: Command name (without `/`)
- `description`: Brief description
- `file`: Path to command file

### 3. get_command_details

Get full documentation for a specific command.

```python
get_command_details(
    command_name: str     # Command name without "/"
)
```

**Example:**
```python
get_command_details("tdd")
get_command_details("debug")
```

**Returns:**
- `name`: Command name
- `file`: File path
- `content`: Full markdown content

### 4. list_agents

Get all available agents.

```python
list_agents()
```

**Returns:** List of agents with:
- `name`: Agent name
- `description`: Brief description
- `file`: Path to agent file

### 5. get_agent_details

Get full prompt for a specific agent.

```python
get_agent_details(
    agent_name: str       # Agent name
)
```

**Example:**
```python
get_agent_details("qa")
get_agent_details("dev")
```

**Returns:**
- `name`: Agent name
- `file`: File path
- `content`: Full agent prompt

### 6. get_workflow_context

Get overview of claude-flow methodology.

```python
get_workflow_context()
```

**Returns:**
- `iron_laws`: The 5 Iron Laws with commands and rules
- `thinking_budget`: Token budgets for different thinking levels
- `workflow_phases`: Development lifecycle phases

### 7. search_by_topic

Semantic search with source filtering.

```python
search_by_topic(
    topic: str,               # Topic or question
    source_filter: str = None, # Filter by path (e.g., "commands", "agents")
    top_k: int = 5            # Number of results
)
```

**Examples:**
```python
search_by_topic("debugging", source_filter="commands")
search_by_topic("test writing", source_filter="agents")
```

### 8. get_quick_reference

Get cheatsheet of common workflows.

```python
get_quick_reference()
```

**Returns:**
- `common_workflows`: TDD, debugging, verification workflows
- `key_commands`: List of essential commands

## Usage Patterns

### Pattern 1: Discovery → Detail → Use

```
User: "I need to debug an issue"

Step 1: list_commands()
  → See "debug" command available

Step 2: get_command_details("debug")
  → Get full 4-phase debugging workflow

Step 3: Apply workflow
  → Follow the steps in the documentation
```

### Pattern 2: Search → Explore → Apply

```
User: "How do I ensure code quality?"

Step 1: search_knowledge("code quality")
  → Get relevant docs about TDD, review, verify

Step 2: get_command_details("tdd")
  → Learn TDD workflow

Step 3: get_command_details("review")
  → Learn code review process
```

### Pattern 3: Context → Filter → Detail

```
User: "What QA tools are available?"

Step 1: get_workflow_context()
  → Understand overall methodology

Step 2: search_by_topic("testing", source_filter="agents")
  → Find QA agent

Step 3: get_agent_details("qa")
  → Get full QA agent prompt
```

## Token Optimization

### Before MCP Server

Loading TDD workflow traditionally:
```
1. Load /tdd command file → 3k tokens
2. Load TDD examples → 5k tokens
3. Load related agents → 6k tokens
4. Load verification docs → 4k tokens
Total: 18k tokens
```

### With MCP Server

Same information via MCP:
```
1. list_commands() → 1k tokens (structured JSON)
2. get_command_details("tdd") → 3k tokens
3. search_knowledge("tdd examples") → 2k tokens (top 3 results)
Total: 6k tokens
Savings: 67%
```

### Best Practices for Token Efficiency

1. **Use list first, detail later**
   ```
   ✓ list_commands() → get_command_details("tdd")
   ✗ Load all command files upfront
   ```

2. **Limit search results**
   ```
   ✓ search_knowledge("query", top_k=3)
   ✗ search_knowledge("query", top_k=20)
   ```

3. **Use source filters**
   ```
   ✓ search_by_topic("agents", source_filter="agents")
   ✗ search_knowledge("agents")  # searches everywhere
   ```

4. **Cache workflow context**
   ```
   ✓ get_workflow_context() once, reuse
   ✗ Call repeatedly for same info
   ```

## Troubleshooting

### Server Not Found in Claude Code

**Symptom:** `/mcp` doesn't show `claude-flow`

**Solutions:**
1. Verify installation:
   ```bash
   claude mcp list
   ```

2. Check path is absolute:
   ```bash
   # Wrong (relative path)
   claude mcp add --transport stdio claude-flow -- python ./server.py
   
   # Correct (absolute path)
   claude mcp add --transport stdio claude-flow -- python /full/path/to/server.py
   ```

3. Test server manually:
   ```bash
   cd /path/to/claude-flow/mcp-server
   python server.py
   # Should not crash, waits for input
   # Press Ctrl+C to exit
   ```

### No Search Results

**Symptom:** `search_knowledge()` returns empty list

**Solutions:**
1. Check RAG index exists:
   ```bash
   ls ../rag-pipeline/storage/chroma/
   # Should show database files
   ```

2. Re-index knowledge base:
   ```bash
   cd ../rag-pipeline
   source .venv/bin/activate
   python -m ingestion.ingest
   ```

3. Verify document count:
   ```bash
   cd ../rag-pipeline
   python -m retrieval.retrieve
   # Should show: "Index contains N documents"
   ```

### Import Errors

**Symptom:** Server crashes with `ModuleNotFoundError`

**Solutions:**
1. Verify virtual environment:
   ```bash
   cd ../rag-pipeline
   source .venv/bin/activate
   pip list | grep -E "mcp|chromadb|sentence"
   ```

2. Reinstall dependencies:
   ```bash
   cd ../mcp-server
   pip install -r requirements.txt
   ```

3. Check Python version:
   ```bash
   python --version  # Must be 3.10+
   ```

### Slow Performance

**Symptom:** Tools take >5 seconds to respond

**Solutions:**
1. **First call is slow (expected)**
   - Loading embedding model takes ~2-3 seconds
   - Subsequent calls are fast (~100ms)

2. **Check embeddings cached:**
   - Model downloads on first use (~400MB)
   - Stored in `~/.cache/huggingface/`

3. **Reduce search results:**
   ```python
   # Slower
   search_knowledge("query", top_k=20)
   
   # Faster
   search_knowledge("query", top_k=3)
   ```

### Permission Errors

**Symptom:** Cannot write to storage directory

**Solutions:**
1. Check permissions:
   ```bash
   ls -la ../rag-pipeline/storage/
   ```

2. Fix permissions:
   ```bash
   chmod -R u+w ../rag-pipeline/storage/
   ```

## Advanced Usage

### Custom Tool Invocation from Code

If you want to test tools directly:

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path("/path/to/claude-flow")
sys.path.insert(0, str(PROJECT_ROOT / "mcp-server"))
sys.path.insert(0, str(PROJECT_ROOT / "rag-pipeline"))

# Import after path setup
from server import (
    search_knowledge,
    list_commands,
    get_workflow_context,
)

# Use tools
results = search_knowledge("debugging", top_k=3)
commands = list_commands()
context = get_workflow_context()
```

### Updating Knowledge Base

When documentation changes:

```bash
cd ../rag-pipeline
source .venv/bin/activate
python -m ingestion.ingest  # Re-indexes everything
```

### Integration with CI/CD

Add to `.github/workflows/update-mcp.yml`:

```yaml
name: Update MCP Index
on:
  push:
    paths:
      - 'docs/**'
      - 'commands/**'
      - 'agents/**'
      - 'knowledge/**'

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Update RAG index
        run: |
          cd rag-pipeline
          pip install -r requirements.txt
          python -m ingestion.ingest
```

## Support

- **Issues**: https://github.com/Dutchthenomad/claude-flow/issues
- **Documentation**: See `README.md` and `CONTEXT.md`
- **RAG Pipeline**: See `../rag-pipeline/CONTEXT.md`
