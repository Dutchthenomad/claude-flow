# MCP Servers - Agent Context

## Purpose
Model Context Protocol server integrations. MCP servers extend Claude's tool capabilities with external services.

## Available MCP Servers
| Server | Purpose | Status |
|--------|---------|--------|
| `puppeteer` | Browser automation | Installed |
| `github` | GitHub API access | Planned |
| `filesystem` | Enhanced file operations | Planned |
| `memory` | Persistent memory | Planned |

## Configuration
MCP servers are configured in `.mcp.json`:
```json
{
  "servers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-puppeteer"]
    }
  }
}
```

## Integration Points
- MCP tools appear as `mcp__<server>__<tool>`
- Can be targeted by hooks via matchers
- Extend agent capabilities for specific tasks

## Development Status
- [x] Initial structure
- [ ] MCP configuration documented
- [ ] Server inventory complete
- [ ] Custom servers developed

## For Future Agents
When adding MCP servers:
1. Test server locally first
2. Document required environment variables
3. Add to project `.mcp.json`
4. Create usage examples
5. Add hooks if automation needed
