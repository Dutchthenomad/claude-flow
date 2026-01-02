# Claude Code Quickstart Guide

> Source: https://code.claude.com/docs/en/quickstart
> Scraped: 2025-12-13

Welcome to Claude Code! This is Anthropic's official CLI for AI-powered coding assistance directly in your terminal.

## Before You Begin

Make sure you have:
- A terminal or command prompt open
- A code project to work with
- A Claude.ai (recommended) or Claude Console account

## Step 1: Install Claude Code

### Native Install (Recommended)

**Homebrew (macOS, Linux):**
```bash
brew install --cask claude-code
```

**macOS, Linux, WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**
```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### NPM Install

If you have Node.js 18 or newer:
```bash
npm install -g @anthropic-ai/claude-code
```

## Step 2: Log In to Your Account

When you start an interactive session, you'll need to authenticate:

```bash
claude
# You'll be prompted to log in on first use
```

Or use the login command:
```bash
/login
# Follow the prompts to log in with your account
```

You can log in using either:
- **Claude.ai** (subscription plans - recommended)
- **Claude Console** (API access with pre-paid credits)

**Note:** When you first authenticate with your Claude Console account, a workspace called "Claude Code" is automatically created for centralized cost tracking.

## Step 3: Start Your First Session

```bash
cd /path/to/your/project
claude
```

You'll see the Claude Code welcome screen with session information, recent conversations, and updates. Type `/help` for available commands or `/resume` to continue a previous conversation.

## Step 4: Ask Your First Question

Let Claude analyze your codebase:

```bash
> what does this project do?
```

Other useful questions:
```bash
> what technologies does this project use?
> where is the main entry point?
> explain the folder structure
> what can Claude Code do?
> how do I use slash commands in Claude Code?
> can Claude Code work with Docker?
```

Claude reads your files as needed—you don't have to manually add context.

## Step 5: Make Your First Code Change

Try a simple task:

```bash
> add a hello world function to the main file
```

Claude Code will:
1. Find the appropriate file
2. Show you the proposed changes
3. Ask for your approval
4. Make the edit

**Claude always asks for permission before modifying files.** You can approve individual changes or enable "Accept all" mode.

## Step 6: Use Git with Claude Code

Make Git operations conversational:

```bash
> what files have I changed?
> commit my changes with a descriptive message
> create a new branch called feature/quickstart
> show me the last 5 commits
> help me resolve merge conflicts
```

## Step 7: Fix a Bug or Add a Feature

Describe what you want in natural language:

```bash
> add input validation to the user registration form
```

Or fix existing issues:

```bash
> there's a bug where users can submit empty forms - fix it
```

Claude Code will:
- Locate the relevant code
- Understand the context
- Implement a solution
- Run tests if available

## Step 8: Test Out Other Common Workflows

### Refactor code
```bash
> refactor the authentication module to use async/await instead of callbacks
```

### Write tests
```bash
> write unit tests for the calculator functions
```

### Update documentation
```bash
> update the README with installation instructions
```

### Code review
```bash
> review my changes and suggest improvements
```

## Essential Commands

| Command | What it does | Example |
|---------|-------------|---------|
| `claude` | Start interactive mode | `claude` |
| `claude "task"` | Run a one-time task | `claude "fix the build error"` |
| `claude -p "query"` | Run one-off query, then exit | `claude -p "explain this function"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -r` | Resume a previous conversation | `claude -r` |
| `claude commit` | Create a Git commit | `claude commit` |
| `/clear` | Clear conversation history | `> /clear` |
| `/help` | Show available commands | `> /help` |
| `exit` or Ctrl+C | Exit Claude Code | `> exit` |

## Pro Tips for Beginners

### Be specific with your requests
Instead of: "fix the bug"
Try: "fix the login bug where users see a blank screen after entering wrong credentials"

### Use step-by-step instructions
Break complex tasks into steps:
```bash
> 1. create a new database table for user profiles
> 2. create an API endpoint to get and update user profiles
> 3. build a webpage that allows users to see and edit their information
```

### Let Claude explore first
Before making changes, let Claude understand your code:
```bash
> analyze the database schema
> build a dashboard showing products that are most frequently returned by our UK customers
```

### Save time with shortcuts
- Press `?` to see all available keyboard shortcuts
- Use Tab for command completion
- Press ↑ for command history
- Type `/` to see all slash commands

## What's Next?

Now that you've learned the basics, explore more advanced features:

- **Common workflows** - Step-by-step guides for common tasks
- **CLI reference** - Master all commands and options
- **Configuration** - Customize Claude Code for your workflow
- **Claude Code on the web** - Run tasks asynchronously in the cloud

## Getting Help

- **In Claude Code**: Type `/help` or ask "how do I…"
- **Documentation**: Browse other guides on this site
- **Community**: Join the Discord for tips and support
