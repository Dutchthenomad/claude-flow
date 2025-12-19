#!/usr/bin/env python3
"""Claude-Flow MCP Server.

Provides efficient access to claude-flow knowledge, commands, and agents
through the Model Context Protocol, reducing token usage in Claude Code.
"""
import sys
from pathlib import Path
from typing import Any

# Add parent and rag-pipeline to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "rag-pipeline"))

from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("claude-flow")


def _extract_yaml_description(content: str) -> str:
    """Extract description from YAML frontmatter.
    
    Args:
        content: File content with potential YAML frontmatter
    
    Returns:
        Description string or "No description"
    """
    if not content.startswith("---"):
        return "No description"
    
    lines = content.split("\n")
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    
    return "No description"


@mcp.tool()
def search_knowledge(
    query: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Search the claude-flow knowledge base using semantic search.
    
    Args:
        query: Natural language query (e.g., "How do I use TDD workflow?")
        top_k: Number of results to return (default: 5)
    
    Returns:
        List of relevant document chunks with source, text, and score
    """
    try:
        from retrieval.retrieve import search
        results = search(query, top_k=top_k)
        return results
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


@mcp.tool()
def list_commands() -> list[dict[str, str]]:
    """List all available slash commands in claude-flow.
    
    Returns:
        List of commands with name, description, and file path
    """
    commands_dir = PROJECT_ROOT / "commands"
    commands = []
    
    if not commands_dir.exists():
        return [{"error": "Commands directory not found"}]
    
    for cmd_file in sorted(commands_dir.glob("*.md")):
        if cmd_file.name == "CONTEXT.md":
            continue
        try:
            content = cmd_file.read_text()
            description = _extract_yaml_description(content)
            
            commands.append({
                "name": cmd_file.stem,
                "description": description,
                "file": str(cmd_file.relative_to(PROJECT_ROOT)),
            })
        except Exception as e:
            commands.append({
                "name": cmd_file.stem,
                "error": str(e),
            })
    
    return commands


@mcp.tool()
def get_command_details(command_name: str) -> dict[str, str]:
    """Get detailed information about a specific slash command.
    
    Args:
        command_name: Name of the command (without leading slash)
    
    Returns:
        Command details including full content and metadata
    """
    cmd_file = PROJECT_ROOT / "commands" / f"{command_name}.md"
    
    if not cmd_file.exists():
        return {"error": f"Command '{command_name}' not found"}
    
    try:
        content = cmd_file.read_text()
        return {
            "name": command_name,
            "file": str(cmd_file.relative_to(PROJECT_ROOT)),
            "content": content,
        }
    except Exception as e:
        return {"error": f"Failed to read command: {str(e)}"}


@mcp.tool()
def list_agents() -> list[dict[str, str]]:
    """List all available agents in claude-flow.
    
    Returns:
        List of agents with name, description, and file path
    """
    agents_dir = PROJECT_ROOT / "agents"
    agents = []
    
    if not agents_dir.exists():
        return [{"error": "Agents directory not found"}]
    
    for agent_file in sorted(agents_dir.glob("*.md")):
        if agent_file.name == "CONTEXT.md":
            continue
        try:
            content = agent_file.read_text()
            description = _extract_yaml_description(content)
            
            agents.append({
                "name": agent_file.stem,
                "description": description,
                "file": str(agent_file.relative_to(PROJECT_ROOT)),
            })
        except Exception as e:
            agents.append({
                "name": agent_file.stem,
                "error": str(e),
            })
    
    return agents


@mcp.tool()
def get_agent_details(agent_name: str) -> dict[str, str]:
    """Get detailed information about a specific agent.
    
    Args:
        agent_name: Name of the agent
    
    Returns:
        Agent details including full prompt and metadata
    """
    agent_file = PROJECT_ROOT / "agents" / f"{agent_name}.md"
    
    if not agent_file.exists():
        return {"error": f"Agent '{agent_name}' not found"}
    
    try:
        content = agent_file.read_text()
        return {
            "name": agent_name,
            "file": str(agent_file.relative_to(PROJECT_ROOT)),
            "content": content,
        }
    except Exception as e:
        return {"error": f"Failed to read agent: {str(e)}"}


@mcp.tool()
def get_workflow_context() -> dict[str, Any]:
    """Get an overview of the claude-flow workflow and methodology.
    
    Returns:
        Summary of the 5 Iron Laws, key principles, and workflow structure
    """
    return {
        "iron_laws": [
            {
                "name": "TDD",
                "command": "/tdd",
                "rule": "NO production code without failing test first",
            },
            {
                "name": "Verification",
                "command": "/verify",
                "rule": "Evidence before claims, always",
            },
            {
                "name": "Debugging",
                "command": "/debug",
                "rule": "NO fixes without root cause investigation",
            },
            {
                "name": "Planning",
                "command": "/plan",
                "rule": "Plans must be executable with ZERO context",
            },
            {
                "name": "Isolation",
                "command": "/worktree",
                "rule": "Isolated workspace for each feature",
            },
        ],
        "thinking_budget": {
            "think": {"tokens": "~4k", "use_for": "Simple tasks"},
            "think_hard": {"tokens": "~10k", "use_for": "Debugging"},
            "think_harder": {"tokens": "~20k", "use_for": "Complex changes"},
            "ultrathink": {"tokens": "~32k", "use_for": "Architecture"},
        },
        "workflow_phases": [
            "Inception - Create/find work items",
            "Planning - Gather requirements",
            "Development - Branch and commit",
            "Review - PR workflow",
            "Merge - Complete work",
        ],
    }


@mcp.tool()
def search_by_topic(
    topic: str,
    source_filter: str | None = None,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Search knowledge base with optional source filtering.
    
    Args:
        topic: Topic or question to search for
        source_filter: Optional filter for source paths (e.g., "commands", "agents", "docs")
        top_k: Number of results to return
    
    Returns:
        Filtered search results
    """
    try:
        from retrieval.retrieve import search_with_filter
        results = search_with_filter(topic, source_filter, top_k)
        return results
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]


@mcp.tool()
def get_quick_reference() -> dict[str, Any]:
    """Get quick reference guide for common commands and workflows.
    
    Returns:
        Quick reference with command syntax and usage patterns
    """
    return {
        "common_workflows": {
            "tdd_cycle": [
                "/tdd - Start TDD workflow",
                "Write failing test first",
                "Implement minimal code",
                "Run tests to verify",
                "Refactor if needed",
            ],
            "debugging": [
                "/debug - Start systematic debugging",
                "Phase 1: Reproduce the issue",
                "Phase 2: Isolate root cause",
                "Phase 3: Implement fix",
                "Phase 4: Verify and prevent regression",
            ],
            "verification": [
                "/verify - Verify implementation",
                "Provide evidence for claims",
                "Test all edge cases",
                "Check for regressions",
            ],
        },
        "key_commands": [
            "/tdd - Test-Driven Development",
            "/debug - Systematic debugging",
            "/verify - Verification gates",
            "/plan - ULTRATHINK planning",
            "/worktree - Git worktree isolation",
            "/review - Code review",
            "/run-tests - Auto-detect tests",
        ],
    }


if __name__ == "__main__":
    # Run server using stdio transport
    mcp.run(transport="stdio")
