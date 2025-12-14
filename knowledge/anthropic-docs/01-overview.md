# Claude Code Overview

> Source: https://code.claude.com/docs/en/overview
> Scraped: 2025-12-13

Claude Code is Anthropic's official CLI for Claude, an agentic coding tool that lives in your terminal.

## Get Started in 30 Seconds

### Prerequisites
- A [Claude.ai](https://claude.ai) (recommended) or [Claude Console](https://console.anthropic.com/) account

### Installation

**macOS/Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**macOS (Homebrew):**
```bash
brew install --cask claude-code
```

**Windows:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**NPM (Node.js 18+ required):**
```bash
npm install -g @anthropic-ai/claude-code
```

### Start Using Claude Code
```bash
cd your-project
claude
```

You'll be prompted to log in on first use. Claude Code automatically keeps itself up to date.

## What Claude Code Does for You

- **Build features from descriptions**: Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.

- **Debug and fix issues**: Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.

- **Navigate any codebase**: Ask anything about your team's codebase and get thoughtful answers. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with MCP can pull from external data sources like Google Drive, Figma, and Slack.

- **Automate tedious tasks**: Fix fiddly lint issues, resolve merge conflicts, and write release notes—all in a single command from your developer machine, or automatically in CI.

## Why Developers Love Claude Code

- **Works in your terminal**: Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.

- **Takes action**: Claude Code can directly edit files, run commands, and create commits. Need more? MCP lets Claude read your design docs in Google Drive, update your tickets in Jira, or use your custom developer tooling.

- **Unix philosophy**: Claude Code is composable and scriptable. For example:
  ```bash
  tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"
  ```
  Your CI can run:
  ```bash
  claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"
  ```

- **Enterprise-ready**: Use the Claude API, or host on AWS or GCP. Enterprise-grade security, privacy, and compliance is built-in.

## Next Steps

- **Quickstart** - See Claude Code in action with practical examples
- **Common workflows** - Step-by-step guides for common workflows
- **Troubleshooting** - Solutions for common issues
- **IDE setup** - Add Claude Code to your IDE

## Additional Resources

- **Build with the Agent SDK** - Create custom AI agents
- **Host on AWS or GCP** - Configure with Amazon Bedrock or Google Vertex AI
- **Settings** - Customize Claude Code for your workflow
- **Commands** - Learn about CLI commands and controls
- **Reference implementation** - Clone development container reference
- **Security** - Discover safeguards and best practices
- **Privacy and data usage** - Understand data handling
