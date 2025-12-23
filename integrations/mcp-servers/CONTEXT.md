# MCP Servers - Agent Context

## Purpose
Model Context Protocol server integrations. MCP servers extend Claude's tool capabilities with external services.

## ⚠️ CRITICAL: Local Sync After GitHub MCP Push

**GitHub MCP bypasses local git entirely.** After ANY `create_or_update_file` or `push_files` operation:

```bash
git pull origin <branch>  # MANDATORY after MCP push
```

**Why:** MCP commits directly via GitHub API. Local repo doesn't know about it. Failure to sync causes divergence and merge conflicts.

**Correct Workflow:**
```
1. mcp__github__get_file_contents → get current SHA
2. mcp__github__create_or_update_file → push changes
3. git pull origin <branch> → SYNC LOCAL (don't forget!)
```

## Available MCP Servers

| Server | Tools | Purpose | Status |
|--------|-------|---------|--------|
| `github` | 25+ | Repository, Issues, PRs, Code Search | ✅ Active |
| `chrome-devtools` | 25+ | Browser debugging, performance, DOM | ✅ Active |
| `puppeteer` | 7 | Basic browser automation | ✅ Active |
| `ClaudeTalkToFigma` | 40+ | Figma design automation via plugin | ✅ Active |

### GitHub MCP Server (25+ tools)

**Repository Operations:**
- `mcp__github__create_repository` - Create new repos
- `mcp__github__search_repositories` - Search GitHub repos
- `mcp__github__fork_repository` - Fork repos
- `mcp__github__get_file_contents` - Read files from repos
- `mcp__github__create_or_update_file` - Write single file
- `mcp__github__push_files` - Push multiple files in one commit

**Issue Management:**
- `mcp__github__create_issue` - Create issues
- `mcp__github__get_issue` - Get issue details
- `mcp__github__list_issues` - List repo issues
- `mcp__github__update_issue` - Update issue state/content
- `mcp__github__add_issue_comment` - Comment on issues
- `mcp__github__search_issues` - Search issues/PRs across GitHub

**Pull Request Operations:**
- `mcp__github__create_pull_request` - Create PRs
- `mcp__github__get_pull_request` - Get PR details
- `mcp__github__list_pull_requests` - List repo PRs
- `mcp__github__get_pull_request_files` - Get changed files
- `mcp__github__get_pull_request_status` - Check CI status
- `mcp__github__get_pull_request_comments` - Get review comments
- `mcp__github__get_pull_request_reviews` - Get reviews
- `mcp__github__create_pull_request_review` - Submit review
- `mcp__github__merge_pull_request` - Merge PR
- `mcp__github__update_pull_request_branch` - Update from base

**Branch & Commit:**
- `mcp__github__create_branch` - Create branches
- `mcp__github__list_commits` - List commit history

**Search:**
- `mcp__github__search_code` - Search code across GitHub
- `mcp__github__search_users` - Search users

### Chrome DevTools MCP Server (25+ tools)

**Page Management:**
- `mcp__chrome-devtools__list_pages` - List open browser tabs
- `mcp__chrome-devtools__select_page` - Switch active tab
- `mcp__chrome-devtools__new_page` - Open new tab
- `mcp__chrome-devtools__close_page` - Close tab
- `mcp__chrome-devtools__navigate_page` - Navigate/reload/back/forward
- `mcp__chrome-devtools__resize_page` - Set viewport size

**Interaction:**
- `mcp__chrome-devtools__click` - Click elements by UID
- `mcp__chrome-devtools__fill` - Fill inputs/selects
- `mcp__chrome-devtools__fill_form` - Fill multiple fields
- `mcp__chrome-devtools__hover` - Hover elements
- `mcp__chrome-devtools__drag` - Drag and drop
- `mcp__chrome-devtools__press_key` - Keyboard input
- `mcp__chrome-devtools__handle_dialog` - Accept/dismiss dialogs
- `mcp__chrome-devtools__upload_file` - File uploads

**Content Capture:**
- `mcp__chrome-devtools__take_snapshot` - A11y tree (preferred over screenshot)
- `mcp__chrome-devtools__take_screenshot` - Visual capture
- `mcp__chrome-devtools__wait_for` - Wait for text to appear

**Debugging:**
- `mcp__chrome-devtools__list_console_messages` - Get console logs
- `mcp__chrome-devtools__get_console_message` - Get specific message
- `mcp__chrome-devtools__list_network_requests` - Get network activity
- `mcp__chrome-devtools__get_network_request` - Get request details
- `mcp__chrome-devtools__evaluate_script` - Execute JS in page

**Performance:**
- `mcp__chrome-devtools__performance_start_trace` - Start recording
- `mcp__chrome-devtools__performance_stop_trace` - Stop recording
- `mcp__chrome-devtools__performance_analyze_insight` - Analyze specific insights

**Emulation:**
- `mcp__chrome-devtools__emulate` - CPU throttling, network conditions, geolocation

### Puppeteer MCP Server (7 tools)

- `mcp__puppeteer__puppeteer_navigate` - Navigate to URL
- `mcp__puppeteer__puppeteer_screenshot` - Take screenshot
- `mcp__puppeteer__puppeteer_click` - Click by CSS selector
- `mcp__puppeteer__puppeteer_fill` - Fill input by selector
- `mcp__puppeteer__puppeteer_select` - Select dropdown option
- `mcp__puppeteer__puppeteer_hover` - Hover element
- `mcp__puppeteer__puppeteer_evaluate` - Execute JS

### Figma MCP Server (40+ tools)

- Requires Figma desktop plugin + local WebSocket server on port 3055
- MCP server runs via `bunx claude-talk-to-figma-mcp@latest`

## Workflow Integration

### GitHub MCP → Development Lifecycle

| Phase | MCP Tools | Use Case |
|-------|-----------|----------|
| **Inception** | `create_issue`, `search_issues` | Create/find work items |
| **Planning** | `get_issue`, `list_issues` | Gather requirements |
| **Development** | `create_branch`, `push_files` | Branch and commit |
| **Review** | `create_pull_request`, `get_pull_request_files` | PR workflow |
| **Merge** | `merge_pull_request`, `update_issue` | Complete work |

**When to use MCP vs `gh` CLI:**
- **MCP**: Structured data, cross-repo operations, automation
- **CLI**: Interactive workflows, complex queries, local operations

### Chrome DevTools → Verification & Debugging

| Workflow | MCP Tools | Use Case |
|----------|-----------|----------|
| `/verify` | `take_snapshot`, `list_console_messages` | Verify UI state, check for errors |
| `/debug` | `list_network_requests`, `evaluate_script` | Inspect API calls, debug JS |
| **Performance** | `performance_*` tools | Core Web Vitals, bottleneck detection |
| **E2E Testing** | `fill_form`, `click`, `wait_for` | Automated UI verification |

**Best Practice:** Prefer `take_snapshot` over `take_screenshot` for text-based verification (faster, more reliable for assertions).

### Puppeteer → Quick Automation

- Simple navigation and form filling
- Quick screenshots for visual documentation
- When DevTools integration not needed

## Configuration

MCP servers are configured in Claude Code settings or `.mcp.json`:

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
      }
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-chrome-devtools"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-puppeteer"]
    }
  }
}
```

## Development Status
- [x] Initial structure
- [x] MCP servers documented
- [x] Tool inventory complete
- [x] Workflow integration mapped
- [ ] Custom agents using MCP
- [ ] Hook automation for MCP tools

## For Future Agents

### When Adding MCP Servers
1. Test server locally first
2. Document all available tools
3. Map tools to workflow phases
4. Add to project `.mcp.json`
5. Create usage examples
6. Add hooks if automation needed

### MCP Tool Selection Guidelines
- **GitHub MCP**: Always prefer for GitHub operations (more reliable than CLI)
- **Chrome DevTools**: Use for debugging, performance, complex browser interactions
- **Puppeteer**: Use for simple automation, when DevTools overkill
