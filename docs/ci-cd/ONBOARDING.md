# Developer Onboarding Guide

Welcome to Claude-Flow development! This guide will help you get started with contributing to the project and understanding the CI/CD pipeline.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Your First Contribution](#your-first-contribution)
- [Understanding the Workflow](#understanding-the-workflow)
- [Development Guidelines](#development-guidelines)
- [Getting Help](#getting-help)

## Prerequisites

### Required Tools

Before you begin, ensure you have the following installed:

1. **Git** (2.30+)
   ```bash
   git --version
   ```

2. **GitHub CLI** (2.0+)
   ```bash
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   
   # Authenticate
   gh auth login
   ```

3. **Python** (3.12+) - For RAG pipeline development
   ```bash
   python --version
   pip --version
   ```

4. **Text Editor / IDE**
   - VS Code (recommended)
   - Vim/Neovim
   - Your preferred editor

### Recommended Tools

These tools will improve your development experience:

1. **act** - Test GitHub Actions locally
   ```bash
   # macOS
   brew install act
   
   # Linux
   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   ```

2. **yamllint** - Validate YAML files
   ```bash
   pip install yamllint
   ```

3. **pre-commit** - Git hooks for code quality
   ```bash
   pip install pre-commit
   ```

### Knowledge Prerequisites

Familiarity with:
- Git and GitHub workflows
- Markdown documentation
- Basic shell scripting
- Python (for RAG pipeline work)
- GitHub Actions (helpful but not required)

## Initial Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
gh repo fork Dutchthenomad/claude-flow --clone

# Navigate to directory
cd claude-flow

# Add upstream remote
git remote add upstream https://github.com/Dutchthenomad/claude-flow.git
```

### 2. Install Claude-Flow

```bash
# Install for development (creates symlinks)
./install.sh

# Verify installation
ls -la ~/.config/claude-code/commands/
```

### 3. Install Development Dependencies

```bash
# Python dependencies (for RAG pipeline)
cd rag-pipeline
pip install -r requirements.txt

# Development tools
pip install pytest pytest-cov coverage radon bandit black isort

# Return to root
cd ..
```

### 4. Understand the Project Structure

```
claude-flow/
├── .claude-plugin/        # Plugin metadata
├── .github/               # CI/CD workflows and config
│   ├── workflows/         # GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   ├── CODEOWNERS         # Code ownership
│   ├── labeler.yml        # Auto-labeling rules
│   └── *.md               # Templates
├── commands/              # Slash commands (/tdd, /debug, etc.)
├── agents/                # Subagents (@QA, @Dev, etc.)
├── skills/                # Agent skills
├── hooks/                 # Workflow automation
├── docs/                  # Documentation
│   ├── ci-cd/             # CI/CD documentation
│   └── guides/            # User guides
├── rag-pipeline/          # RAG knowledge system (Python)
├── knowledge/             # Scraped documentation
├── integrations/          # External repos
├── install.sh             # Installation script
├── uninstall.sh           # Uninstallation script
└── README.md              # Project overview
```

### 5. Configure Git

```bash
# Set your name and email
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set up commit signing (recommended)
git config commit.gpgsign true

# Set default branch name
git config init.defaultBranch main
```

### 6. Set Up Development Environment

#### VS Code (Recommended)

Install extensions:
- **GitHub Actions** - Workflow syntax highlighting
- **YAML** - YAML validation
- **Python** - Python development
- **Markdown All in One** - Markdown editing
- **GitLens** - Git integration

Settings (`.vscode/settings.json`):
```json
{
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.trimTrailingWhitespace": true,
  "markdown.extension.toc.levels": "2..6",
  "yaml.schemas": {
    "https://json.schemastore.org/github-workflow.json": ".github/workflows/*.yml"
  }
}
```

## Your First Contribution

### Step 1: Find an Issue

```bash
# List good first issues
gh issue list --label "good first issue"

# View issue details
gh issue view <number>

# Assign yourself
gh issue edit <number> --add-assignee @me
```

Can't find an issue? Consider:
- Fixing typos in documentation
- Adding examples to existing docs
- Improving error messages
- Writing tests

### Step 2: Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main
git push origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch Naming Convention**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions
- `ci/` - CI/CD changes

### Step 3: Make Your Changes

```bash
# Example: Adding a new command
vim commands/new-command.md

# Add tests if applicable
vim tests/test_new_command.py

# Update documentation
vim docs/COMMANDS.md
```

**Development Checklist**:
- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CONTEXT.md files updated (if applicable)
- [ ] Changes tested locally

### Step 4: Test Locally

```bash
# For Python changes
cd rag-pipeline
pytest
pytest --cov=. --cov-report=term

# Run security scan
bandit -r .

# Check code quality
radon cc . -a -s

# Format code
black .
isort .

# Return to root
cd ..
```

### Step 5: Commit Your Changes

Use **conventional commit format**:

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(commands): add /analyze command

- Implements new analyze command
- Adds tests for analyze functionality
- Updates documentation"

# Or for fixes
git commit -m "fix(rag): resolve chunking boundary issue

Fixes #123"
```

**Commit Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactoring
- `perf`: Performance
- `ci`: CI/CD
- `chore`: Maintenance

**Scopes**:
- `commands`, `agents`, `skills`, `hooks`
- `rag`, `docs`, `ci`, `core`

### Step 6: Push and Create PR

```bash
# Push branch
git push origin feature/your-feature-name

# Create PR
gh pr create --title "feat(commands): add /analyze command" \
             --body "## Description
This PR adds a new /analyze command that...

## Changes
- Added new command file
- Implemented analysis logic
- Added tests
- Updated documentation

## Testing
- [ ] Tested locally
- [ ] All tests pass
- [ ] Documentation reviewed

Fixes #123"
```

### Step 7: Respond to Automated Review

Within ~5 minutes, automated workflows will:
1. **Label your PR** (area, type, size)
2. **Analyze complexity** (Radon metrics)
3. **Scan security** (Bandit, Trivy)
4. **Check coverage** (if tests added)
5. **Analyze impact** (files changed, areas affected)

**Review the comments and**:
- Address any complexity issues (functions with CC > 10)
- Fix security vulnerabilities
- Improve test coverage if needed
- Respond to impact warnings

### Step 8: Iterate Based on Feedback

```bash
# Make additional changes
vim commands/new-command.md

# Commit changes
git commit -m "refactor(commands): simplify analyze logic"

# Push updates
git push origin feature/your-feature-name

# PR automatically updates, workflows re-run
```

### Step 9: Get PR Merged

Once approved:
```bash
# Maintainer will merge
# Your contribution is now part of Claude-Flow! 🎉
```

## Understanding the Workflow

### Automated Checks on PRs

When you create a PR, these workflows run automatically:

1. **PR Labeler** (~30 seconds)
   - Applies area labels based on files changed
   - Applies size label based on lines changed
   - Applies type labels based on PR title
   - Warns if PR is very large (>1000 lines)

2. **Code Review** (~5 minutes)
   - **Complexity Analysis**: Checks cyclomatic complexity
   - **Security Scan**: Runs Bandit and Trivy
   - **Impact Analysis**: Summarizes changes

3. **Test Coverage** (~4 minutes, if Python changes)
   - Runs pytest with coverage
   - Generates coverage report
   - Posts coverage diff to PR

### What the Bots Check

#### Complexity Bot
Flags functions with:
- Cyclomatic Complexity > 10
- Maintainability Index < 20
- Halstead difficulty > 20

**Action**: Refactor complex functions into smaller ones

#### Security Bot
Detects:
- Hardcoded secrets
- SQL injection risks
- Command injection
- Insecure cryptography
- Known vulnerabilities

**Action**: Fix security issues before merge

#### Coverage Bot
Reports:
- Overall coverage percentage
- Coverage change (+ or -)
- Files with low coverage

**Action**: Add tests to maintain >70% coverage

### Status Checks

Required checks before merge:
- [ ] PR labeled appropriately
- [ ] Complexity analysis passed
- [ ] Security scan passed
- [ ] Coverage maintained
- [ ] Manual review approved

## Development Guidelines

### Code Style

#### Python Code
```python
# Use Black formatting (line length 100)
# Use type hints
def process_chunk(text: str, max_tokens: int) -> list[str]:
    """Process text into chunks.
    
    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of text chunks
    """
    # Implementation
    pass

# Use descriptive names
chunk_size = 512  # Good
cs = 512          # Bad

# Use docstrings for all public functions
# Follow Google or NumPy style
```

#### Shell Scripts
```bash
#!/bin/bash
# Use shellcheck-compliant code
# Add error handling
set -euo pipefail

# Use functions
install_plugin() {
    local plugin_dir="$1"
    # Implementation
}

# Add comments for complex logic
# Use meaningful variable names
```

#### Markdown Documentation
```markdown
# Use ATX-style headers (# not underlines)

# Good header

Bad header
==========

# Use fenced code blocks with language
```python
code here
```

# Use relative links
[See CI/CD Guide](./CI_CD_GUIDE.md)

# Keep lines under 100 characters
```

### Testing Guidelines

#### Write Tests for
- New commands
- New agents
- RAG pipeline functions
- Bug fixes
- Security fixes

#### Test Structure
```python
# tests/test_feature.py
import pytest
from rag_pipeline.feature import process

def test_process_basic():
    """Test basic processing."""
    result = process("input")
    assert result == "expected"

def test_process_edge_case():
    """Test edge case."""
    result = process("")
    assert result == ""

def test_process_error():
    """Test error handling."""
    with pytest.raises(ValueError):
        process(None)
```

### Documentation Guidelines

#### Update Documentation When
- Adding new commands
- Changing agent behavior
- Modifying workflows
- Adding features
- Fixing bugs (if user-facing)

#### Documentation Structure
```markdown
# Feature Name

Brief description of feature.

## Usage

How to use the feature.

## Examples

Concrete examples.

## Configuration

Configuration options.

## Troubleshooting

Common issues and solutions.
```

### PR Guidelines

#### Good PR Titles
✅ `feat(commands): add /analyze command`
✅ `fix(rag): resolve chunking boundary issue`
✅ `docs: update CI/CD guide with examples`

❌ `Update files`
❌ `Fix bug`
❌ `WIP stuff`

#### Good PR Descriptions
Include:
- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How was it tested?
- **Screenshots**: If UI/output changes

Use the PR template provided.

#### PR Size
- **Ideal**: <100 lines
- **Good**: 100-500 lines
- **Large**: 500-1000 lines (consider splitting)
- **Too large**: >1000 lines (will be flagged)

Break large PRs into smaller, focused PRs.

### Security Guidelines

#### Never Commit
- API keys or secrets
- Passwords or tokens
- Private keys
- Personal information
- Database credentials

#### Use Instead
- Environment variables
- GitHub Secrets (in workflows)
- Configuration files (gitignored)
- External secret management

#### Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation on user data
- [ ] Parameterized queries (no SQL injection)
- [ ] Secure file handling
- [ ] Dependencies reviewed

### Conventional Commits

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Benefits**:
- Automatic changelog generation
- Semantic versioning
- Better PR categorization
- Clearer history

## Getting Help

### Resources

1. **Documentation**
   - [CI/CD Guide](./CI_CD_GUIDE.md)
   - [Quick Reference](./QUICK_REFERENCE.md)
   - [Workflow Architecture](./WORKFLOW_ARCHITECTURE.md)

2. **Issues**
   - Search existing issues
   - Create new issue with template

3. **Discussions**
   - Ask questions in GitHub Discussions
   - Share ideas and feedback

4. **Code Review**
   - Request review from maintainers
   - Respond to automated feedback

### Common Questions

**Q: My PR is marked as "too large". What do I do?**
A: Break it into smaller, focused PRs. Each PR should do one thing well.

**Q: The complexity analysis flagged my function. How do I fix it?**
A: Refactor into smaller functions. Aim for CC < 10 per function.

**Q: The security scan found an issue. Is it critical?**
A: Review the specific issue. Bandit can have false positives, but always investigate.

**Q: How do I test workflows locally?**
A: Use `act` to run workflows locally before pushing.

**Q: Can I skip CI checks?**
A: No, all checks must pass. If there's a false positive, discuss in the PR.

**Q: How long does it take to get a PR reviewed?**
A: Automated review is immediate. Human review typically within 1-2 days.

### Getting Stuck?

If you're stuck:
1. Check documentation first
2. Search existing issues
3. Ask in PR comments
4. Create a new issue
5. Reach out to maintainers

## Next Steps

Now that you're set up:

1. **Explore the codebase**
   - Read existing commands
   - Review agent definitions
   - Understand the structure

2. **Make a small contribution**
   - Fix a typo
   - Add an example
   - Improve documentation

3. **Learn the workflows**
   - Watch how automation works
   - Review PR comments
   - See releases being created

4. **Take on larger tasks**
   - Implement new features
   - Add comprehensive tests
   - Write detailed documentation

## Checklist for Your First PR

Before creating your first PR, ensure:

- [ ] Fork and clone repository
- [ ] Install Claude-Flow locally
- [ ] Install development dependencies
- [ ] Understand project structure
- [ ] Create feature branch
- [ ] Make changes following guidelines
- [ ] Test changes locally
- [ ] Commit with conventional format
- [ ] Push and create PR
- [ ] Fill out PR template completely
- [ ] Respond to automated review
- [ ] Address reviewer feedback
- [ ] Wait for approval and merge

## Welcome to the Community!

Thank you for contributing to Claude-Flow! Every contribution, no matter how small, helps make the project better.

Happy coding! 🚀

---

**Last Updated**: December 2024
**Version**: 1.0.0
