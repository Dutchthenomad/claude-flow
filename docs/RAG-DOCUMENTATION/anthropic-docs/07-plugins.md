# Claude Code Plugins

> Source: https://code.claude.com/docs/en/plugins
> Scraped: 2025-12-13

Plugins extend Claude Code with custom commands, agents, hooks, Skills, and MCP servers.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Custom slash commands (optional)
│   └── hello.md
├── agents/                   # Custom agents (optional)
│   └── helper.md
├── skills/                   # Agent Skills (optional)
│   └── my-skill/
│       └── SKILL.md
└── hooks/                    # Event handlers (optional)
    └── hooks.json
```

## Plugin Manifest (plugin.json)

```json
{
  "name": "my-first-plugin",
  "description": "A simple greeting plugin",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

## Creating Your First Plugin

### Step 1: Create Marketplace Structure
```bash
mkdir test-marketplace
cd test-marketplace
mkdir my-first-plugin
cd my-first-plugin
```

### Step 2: Create Plugin Manifest
```bash
mkdir .claude-plugin
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-first-plugin",
  "description": "A simple greeting plugin",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
EOF
```

### Step 3: Add Custom Commands
Create `commands/hello.md`:
```markdown
---
description: Greet the user with a personalized message
---

# Hello Command

Greet the user warmly and ask how you can help them today.
```

### Step 4: Create Marketplace Manifest
Create `../.claude-plugin/marketplace.json`:
```json
{
  "name": "test-marketplace",
  "owner": { "name": "Test User" },
  "plugins": [
    {
      "name": "my-first-plugin",
      "source": "./my-first-plugin",
      "description": "My first test plugin"
    }
  ]
}
```

### Step 5: Install and Test
```bash
cd ..
claude

# In Claude Code:
/plugin marketplace add ./test-marketplace
/plugin install my-first-plugin@test-marketplace
# Restart Claude Code
/hello
```

## Installing and Managing Plugins

```bash
# Add marketplaces
/plugin marketplace add your-org/claude-plugins

# Browse plugins
/plugin

# Install plugins
/plugin install formatter@your-org

# Enable/disable plugins
/plugin enable plugin-name@marketplace-name
/plugin disable plugin-name@marketplace-name
/plugin uninstall plugin-name@marketplace-name
```

## Plugin Components

### Commands
- Located in `commands/` directory
- Markdown files defining slash commands
- Invoked manually by users

### Agents
- Located in `agents/` directory
- Custom agent definitions
- Appear in `/agents`

### Skills
- Located in `skills/` directory
- Model-invoked based on context

### Hooks
- Located as `hooks/hooks.json`
- Event handlers for automation

### MCP Servers
- Defined in `.mcp.json`
- External tool integration

## Team Plugin Workflows

Configure in `.claude/settings.json`:
```json
{
  "marketplaces": [
    {
      "name": "team-marketplace",
      "source": "your-org/claude-plugins"
    }
  ],
  "plugins": [
    {
      "name": "formatter",
      "marketplace": "team-marketplace"
    }
  ]
}
```
