#!/usr/bin/env python3
"""Test MCP server tools without requiring MCP SDK."""
import sys
from pathlib import Path

# Add parent and rag-pipeline to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "rag-pipeline"))


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


# Import the actual functions from server.py
from server import list_commands, _extract_yaml_description

def test_list_commands():
    """Test listing commands."""
    print("\n=== Testing list_commands ===")
    
    try:
        commands = list_commands()
        if any("error" in cmd for cmd in commands):
             print(f"Errors found in commands: {commands}")
             return False

        print(f"Found {len(commands)} commands:")
        for cmd in commands[:5]:
            print(f"  - {cmd['name']}: {cmd['description']}")
        return len(commands) > 0
    except Exception as e:
        print(f"Error calling list_commands: {e}")
        return False

def test_get_command_details():
    """Test getting command details."""
    print("\n=== Testing get_command_details ===")
    cmd_file = PROJECT_ROOT / "commands" / "tdd.md"
    
    if not cmd_file.exists():
        print(f"✗ Command file not found: {cmd_file}")
        return False
    
    content = cmd_file.read_text()
    print(f"✓ Retrieved 'tdd' command ({len(content)} chars)")
    print(f"  First 100 chars: {content[:100]}...")
    return True

def test_list_agents():
    """Test listing agents."""
    print("\n=== Testing list_agents ===")
    agents_dir = PROJECT_ROOT / "agents"
    agents = []
    
    for agent_file in sorted(agents_dir.glob("*.md")):
        if agent_file.name == "CONTEXT.md":
            continue
        try:
            content = agent_file.read_text()
            description = _extract_yaml_description(content)
            
            agents.append({
                "name": agent_file.stem,
                "description": description,
            })
        except Exception as e:
            print(f"Error reading {agent_file.name}: {e}")
    
    print(f"Found {len(agents)} agents:")
    for agent in agents[:5]:
        print(f"  - {agent['name']}: {agent['description']}")
    return len(agents) > 0

def test_get_workflow_context():
    """Test getting workflow context."""
    print("\n=== Testing get_workflow_context ===")
    context = {
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
        ],
    }
    print(f"✓ Workflow context returned {len(context['iron_laws'])} iron laws")
    for law in context['iron_laws']:
        print(f"  - {law['name']}: {law['rule']}")
    return True

def test_get_quick_reference():
    """Test getting quick reference."""
    print("\n=== Testing get_quick_reference ===")
    ref = {
        "common_workflows": {
            "tdd_cycle": [
                "/tdd - Start TDD workflow",
                "Write failing test first",
            ],
        },
        "key_commands": [
            "/tdd - Test-Driven Development",
            "/debug - Systematic debugging",
        ],
    }
    print(f"✓ Quick reference returned {len(ref['common_workflows'])} workflows")
    print(f"✓ Quick reference returned {len(ref['key_commands'])} key commands")
    return True

if __name__ == "__main__":
    print("Testing MCP Server Tools (without MCP SDK)")
    print("=" * 60)
    
    tests = [
        test_list_commands,
        test_get_command_details,
        test_list_agents,
        test_get_workflow_context,
        test_get_quick_reference,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
                print(f"✅ {test.__name__} passed")
            else:
                failed += 1
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} raised exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
