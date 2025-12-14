# Connect Claude Code to Tools via MCP

> Source: https://code.claude.com/docs/en/mcp
> Scraped: 2025-12-13

Learn how to connect Claude Code to your tools with the Model Context Protocol.

Claude Code can connect to hundreds of external tools and data sources through the Model Context Protocol (MCP), an open source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs.

## What You Can Do with MCP

With MCP servers connected, you can ask Claude Code to:

- **Implement features from issue trackers**: "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
- **Analyze monitoring data**: "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
- **Query databases**: "Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database."
- **Integrate designs**: "Update our standard email template based on the new Figma designs that were posted in Slack"
- **Automate workflows**: "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."

## Installing MCP Servers

### Option 1: Add a Remote HTTP Server (Recommended)

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Option 2: Add a Remote SSE Server (Deprecated)

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

### Option 3: Add a Local Stdio Server

```bash
# Basic syntax
claude mcp add --transport stdio <name> <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

**Understanding the "—" parameter:** The `--` separates Claude's CLI flags from the command that runs the MCP server.

### Managing Servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

## MCP Installation Scopes

### Local Scope (Default)
Private to you, only accessible in current project directory.

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
```

### Project Scope
Shared with team via `.mcp.json` file at project root.

```bash
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

### User Scope
Available to you across all projects.

```bash
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

## Environment Variable Expansion

Supported syntax:
- `${VAR}` - Expands to value of VAR
- `${VAR:-default}` - Uses default if VAR not set

Example:
```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

## Practical Examples

### Monitor Errors with Sentry

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
> /mcp  # authenticate
> "What are the most common errors in the last 24 hours?"
```

### Connect to GitHub

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
> /mcp  # authenticate
> "Review PR #456 and suggest improvements"
```

### Query PostgreSQL Database

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@localhost:5432/analytics"
> "What's our total revenue this month?"
```

## Authentication

Many cloud-based MCP servers require OAuth 2.0 authentication:

1. Add the server
2. Use `/mcp` command in Claude Code
3. Follow browser prompts to login

## Use MCP Resources with @ Mentions

Reference MCP resources using `@server:protocol://resource/path`:

```bash
> Can you analyze @github:issue://123 and suggest a fix?
> Compare @postgres:schema://users with @docs:file://database/user-model
```

## Use MCP Prompts as Slash Commands

MCP servers can expose prompts as slash commands:

```bash
> /mcp__github__list_prs
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug in login flow" high
```

## Plugin-Provided MCP Servers

Plugins can bundle MCP servers in `.mcp.json` at plugin root or inline in `plugin.json`:

```json
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

## Enterprise MCP Configuration

Administrators can deploy centralized MCP configs and restrict servers:

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" }
  ]
}
```

## Use Claude Code as an MCP Server

```bash
claude mcp serve
```

Add to Claude Desktop's config:
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"]
    }
  }
}
```
