# Common Workflows - Claude Code

> Source: https://code.claude.com/docs/en/common-workflows
> Scraped: 2025-12-13

This documentation provides practical workflows and best practices for using Claude Code CLI.

---

## Understand New Codebases

### Get a Quick Codebase Overview

When joining a new project:

```bash
cd /path/to/project
claude
> give me an overview of this codebase
> explain the main architecture patterns used here
> what are the key data models?
> how is authentication handled?
```

**Tips:**
- Start with broad questions, then narrow down to specific areas
- Ask about coding conventions and patterns used in the project
- Request a glossary of project-specific terms

### Find Relevant Code

```bash
> find the files that handle user authentication
> how do these authentication files work together?
> trace the login process from front-end to database
```

---

## Fix Bugs Efficiently

```bash
> I'm seeing an error when I run npm test
> suggest a few ways to fix the @ts-ignore in user.ts
> update user.ts to add the null check you suggested
```

**Tips:**
- Tell Claude the command to reproduce the issue and get a stack trace
- Mention any steps to reproduce the error
- Let Claude know if the error is intermittent or consistent

---

## Refactor Code

```bash
> find deprecated API usage in our codebase
> suggest how to refactor utils.js to use modern JavaScript features
> refactor utils.js to use ES2024 features while maintaining the same behavior
> run tests for the refactored code
```

**Tips:**
- Ask Claude to explain the benefits of the modern approach
- Request that changes maintain backward compatibility when needed
- Do refactoring in small, testable increments

---

## Use Specialized Subagents

### View and Create Subagents

```bash
> /agents
```

### Automatically Delegate Tasks

Claude Code automatically delegates appropriate tasks:

```bash
> review my recent code changes for security issues
> run all tests and fix any failures
```

### Explicitly Request Subagents

```bash
> use the code-reviewer subagent to check the auth module
> have the debugger subagent investigate why users can't log in
```

### Create Custom Subagents

Use `/agents` command to create new subagents with:
- Unique identifier describing the subagent's purpose
- When Claude should use this agent
- Which tools it can access
- A system prompt describing the agent's role and behavior

**Tips:**
- Create project-specific subagents in `.claude/agents/` for team sharing
- Use descriptive `description` fields to enable automatic delegation
- Limit tool access to what each subagent actually needs

---

## Use Plan Mode for Safe Code Analysis

Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations.

### When to Use Plan Mode

- **Multi-step implementation**: When your feature requires making edits to many files
- **Code exploration**: When you want to research the codebase thoroughly before changing anything
- **Interactive development**: When you want to iterate on the direction with Claude

### How to Use Plan Mode

**Turn on Plan Mode during a session:**
- Use **Shift+Tab** to cycle through permission modes
- First **Shift+Tab** switches to Auto-Accept Mode (`⏵⏵ accept edits on`)
- Second **Shift+Tab** switches to Plan Mode (`⏸ plan mode on`)

**Start a new session in Plan Mode:**

```bash
claude --permission-mode plan
```

**Run "headless" queries in Plan Mode:**

```bash
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Example: Planning a Complex Refactor

```bash
claude --permission-mode plan
> I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.

# Refine with follow-ups:
> What about backward compatibility?
> How should we handle database migration?
```

### Configure Plan Mode as Default

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

---

## Work with Tests

```bash
> find functions in NotificationsService.swift that are not covered by tests
> add tests for the notification service
> add test cases for edge conditions in the notification service
> run the new tests and fix any failures
```

Claude examines existing test files to match the style, frameworks, and assertion patterns already in use.

---

## Create Pull Requests

```bash
> summarize the changes I've made to the authentication module
> create a pr
> enhance the PR description with more context about the security improvements
> add information about how these changes were tested
```

---

## Handle Documentation

```bash
> find functions without proper JSDoc comments in the auth module
> add JSDoc comments to the undocumented functions in auth.js
> improve the generated documentation with more context and examples
> check if the documentation follows our project standards
```

---

## Work with Images

### Add an Image to the Conversation

1. Drag and drop an image into the Claude Code window
2. Copy an image and paste it with **Ctrl+V** (not Cmd+V)
3. Provide an image path: "Analyze this image: /path/to/your/image.png"

### Analyze Images

```bash
> What does this image show?
> Describe the UI elements in this screenshot
> Are there any problematic elements in this diagram?
> Here's a screenshot of the error. What's causing it?
> This is our current database schema. How should we modify it for the new feature?
> Generate CSS to match this design mockup
> What HTML structure would recreate this component?
```

---

## Reference Files and Directories

Use `@` to quickly include files or directories without waiting for Claude to read them.

### Reference a Single File

```bash
> Explain the logic in @src/utils/auth.js
```

### Reference a Directory

```bash
> What's the structure of @src/components?
```

### Reference MCP Resources

```bash
> Show me the data from @github:repos/owner/repo/issues
```

**Tips:**
- File paths can be relative or absolute
- @ file references add `CLAUDE.md` in the file's directory and parent directories to context
- Directory references show file listings, not contents

---

## Use Extended Thinking (Thinking Mode)

Extended thinking reserves a portion of the output token budget for Claude to reason through complex problems step-by-step.

### Enable Thinking Mode

**Global default:**
```bash
/config
```

**Environment variable override:**
```bash
export MAX_THINKING_TOKENS=1024
```

### Per-Request Thinking with `ultrathink`

```bash
> ultrathink: design a caching layer for our API
```

**Note:** `ultrathink` both allocates the thinking budget AND signals to Claude to reason more thoroughly. Other phrases like "think" or "think hard" are interpreted as regular prompt instructions.

### View Thinking Process

Press **Ctrl+O** to toggle verbose mode and see internal reasoning displayed as gray italic text.

### Token Budget Information

- When **enabled**: Claude can use up to **31,999 tokens** from output budget for internal reasoning
- When **disabled**: Claude uses **0 tokens** for thinking
- Custom budgets can be set via `MAX_THINKING_TOKENS` environment variable
- You're charged for all thinking tokens used

---

## Resume Previous Conversations

### Continue Most Recent Conversation

```bash
claude --continue
```

### Continue in Non-Interactive Mode

```bash
claude --continue --print "Continue with my task"
```

### Show Conversation Picker

```bash
claude --resume
```

Displays an interactive selector showing session summary, time elapsed, message count, and git branch.

**Tips:**
- Conversation history is stored locally on your machine
- Use `--continue` for quick access to your most recent conversation
- Use `--resume` when you need to select a specific past conversation

---

## Run Parallel Claude Code Sessions with Git Worktrees

### Create a New Worktree

```bash
# Create a new worktree with a new branch
git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123
```

### Run Claude Code in Each Worktree

```bash
cd ../project-feature-a
claude
```

### Manage Worktrees

```bash
# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a
```

**Tips:**
- Each worktree has its own independent file state
- Changes in one worktree won't affect others
- All worktrees share the same Git history
- Use descriptive directory names for each task
- Initialize your development environment in each new worktree (npm install, pip install, etc.)

---

## Use Claude as a Unix-Style Utility

### Add Claude to Your Verification Process

```json
// package.json
{
  "scripts": {
    "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
  }
}
```

### Pipe In, Pipe Out

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

### Control Output Format

**Text format (default):**
```bash
cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
```

**JSON format:**
```bash
cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
```

**Streaming JSON format:**
```bash
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```

---

## Create Custom Slash Commands

### Create Project-Specific Commands

```bash
mkdir -p .claude/commands
echo "Analyze the performance of this code and suggest three specific optimizations:" > .claude/commands/optimize.md
```

Use your command:
```bash
> /optimize
```

### Add Command Arguments with $ARGUMENTS

```bash
echo 'Find and fix issue #$ARGUMENTS. Follow these steps: 1. Understand the issue described in the ticket 2. Locate the relevant code in our codebase 3. Implement a solution that addresses the root cause 4. Add appropriate tests 5. Prepare a concise PR description' > .claude/commands/fix-issue.md
```

Use the command with arguments:
```bash
> /fix-issue 123
```

### Create Personal Slash Commands

```bash
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities, focusing on:" > ~/.claude/commands/security-review.md
```

**Tips:**
- Personal commands show "(user)" in their description
- Personal commands work across all your projects
- Project commands show "(project:frontend)" for subdirectory organization

---

## Ask Claude About Its Capabilities

### Example Questions

```bash
> can Claude Code create pull requests?
> how does Claude Code handle permissions?
> what slash commands are available?
> how do I use MCP with Claude Code?
> how do I configure Claude Code for Amazon Bedrock?
> what are the limitations of Claude Code?
```

Claude provides documentation-based answers and has access to the latest Claude Code documentation.
