# Integrations - Agent Context

## Purpose
External repositories and tools that extend claude-flow capabilities. This folder contains cloned repos and integration adapters.

## Contents
| Folder | Description |
|--------|-------------|
| `anthropic/` | Official Anthropic repositories |
| `community/` | Community tools and frameworks |
| `mcp-servers/` | MCP server integrations |

## Integration Philosophy
1. **Clone, don't fork** - Keep originals pristine for easy updates
2. **Adapt via wrappers** - Create adapters in parent folders
3. **Version pin** - Document specific versions used
4. **Update carefully** - Test after pulling updates

## Development Status
- [x] Initial structure
- [ ] Anthropic repos cloned
- [ ] Community tools integrated
- [ ] MCP servers configured
- [ ] Production ready

## For Future Agents
When adding integrations:
1. Clone into appropriate subfolder
2. Document the integration in CONTEXT.md
3. Create wrapper/adapter if needed
4. Add to .gitignore if large/binary
5. Test integration before committing
