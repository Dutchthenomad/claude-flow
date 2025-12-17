# The Recursive Loop: Local + GitHub Integration

This document explains how claude-flow creates a **closed-loop development system** where the methodology enforces itself both locally (via Claude Code) and remotely (via GitHub Actions).

## Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         THE RECURSIVE LOOP                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│    LOCAL DEVELOPMENT                     GITHUB CI/CD                      │
│    ─────────────────                     ───────────                       │
│                                                                            │
│    ┌─────────────┐                       ┌─────────────┐                   │
│    │ Claude Code │                       │   GitHub    │                   │
│    │  + claude-  │  ──── git push ────►  │   Actions   │                   │
│    │    flow     │                       │             │                   │
│    └─────────────┘                       └─────────────┘                   │
│           │                                     │                          │
│           │                                     │                          │
│    ┌──────▼──────┐                       ┌──────▼──────┐                   │
│    │   /tdd      │◄─────────────────────►│  Coverage   │                   │
│    │   /verify   │◄─────────────────────►│  Validation │                   │
│    │   /review   │◄─────────────────────►│  Claude     │                   │
│    │   /debug    │◄─────────────────────►│  Code       │                   │
│    └─────────────┘                       │  Action     │                   │
│                                          └─────────────┘                   │
│                                                 │                          │
│                         ◄── PR Comments ────────┘                          │
│                         ◄── Status Checks ──────┘                          │
│                         ◄── Review Feedback ────┘                          │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## How It Works

### 1. Local Development (Claude Code)

When you develop locally with Claude Code and the claude-flow plugin installed:

| Command | What It Does | GitHub Equivalent |
|---------|--------------|-------------------|
| `/tdd` | Enforces RED-GREEN-REFACTOR | `coverage.yml` verifies tests exist |
| `/verify` | Requires evidence before claims | `validate.yml` checks self-dogfooding |
| `/review` | Code review checklist | `claude.yml` AI-powered review |
| `/debug` | 4-phase root cause analysis | `code-review.yml` complexity analysis |
| `/worktree` | Isolated workspace | Branch protection rules |

### 2. GitHub Actions (Remote Enforcement)

When you push to GitHub, the CI/CD pipeline mirrors these checks:

| Workflow | Purpose | Triggers |
|----------|---------|----------|
| `validate.yml` | Markdown, shell, plugin validation | PR, push |
| `code-review.yml` | Complexity, security, impact | PR |
| `coverage.yml` | Test coverage tracking | PR, push |
| `claude.yml` | AI-powered methodology review | @claude mention, claude-review label |
| `security.yml` | Multi-layer security scanning | PR, push, weekly |
| `pr-labeler.yml` | Auto-labeling | PR |
| `release.yml` | Automated releases | Tag push |

### 3. The Claude Code Action Bridge

The key to closing the loop is `claude.yml`, which uses `anthropics/claude-code-action`:

```yaml
# Triggered by @claude mentions
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      You are reviewing a PR for the claude-flow repository.
      Please review with these principles:
      1. TDD - Are there tests?
      2. Verification - Is there evidence?
      3. Self-dogfooding - Does it follow patterns?
```

This means **the same Claude that helps you locally can review PRs on GitHub**.

## Self-Dogfooding

Claude-flow practices what it preaches:

### What We Validate

1. **CONTEXT.md Files**: Every major directory must have one
2. **Command Frontmatter**: All commands must have YAML frontmatter
3. **Plugin Structure**: plugin.json must be valid
4. **No Hardcoded Paths**: Can't have `/home/nomad` in methodology files
5. **TODO Tracking**: TODOs should reference issues

### Validation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    validate.yml Jobs                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  markdown-   │  │   shell-     │  │   plugin-    │      │
│  │    lint      │  │    lint      │  │  structure   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                 │               │
│         ▼                 ▼                 ▼               │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  self-       │  │  guardrails  │                        │
│  │  dogfood     │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
│         │                 │                                 │
│         └────────┬────────┘                                 │
│                  ▼                                          │
│         ┌──────────────┐                                    │
│         │  validation- │                                    │
│         │   summary    │ ──► PR Comment                     │
│         └──────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Using Claude for PR Review

### Option 1: Mention @claude

In any issue or PR comment, write:

```
@claude Can you review this PR for TDD compliance?
```

Claude will analyze the PR and respond.

### Option 2: Add claude-review Label

Add the `claude-review` label to a PR to trigger automatic AI review on every push.

### Option 3: Automatic Methodology Reminder

When PRs touch methodology files (commands/, agents/, skills/, hooks/), an automatic reminder is posted with a checklist.

## Setup Requirements

### Required Secrets

Add to Repository Settings > Secrets and variables > Actions:

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude |

### Required Labels

Create these labels in your repository:

| Label | Description | Color |
|-------|-------------|-------|
| `claude-review` | Triggers automatic Claude review | `#7c3aed` (purple) |
| `methodology` | Auto-applied to methodology files | `#10b981` (green) |

## The Complete Flow

Here's a typical development cycle with the recursive loop:

```
1. Local: /plan "new feature"           ← Claude helps plan
   ↓
2. Local: /worktree feature-x           ← Isolated workspace
   ↓
3. Local: /tdd "first requirement"      ← Write test first
   ↓
4. Local: Implement code                ← Make test pass
   ↓
5. Local: /verify                       ← Prove it works
   ↓
6. Local: /review                       ← Self-review
   ↓
7. git push origin feature-x            ← Push to GitHub
   ↓
8. GitHub: PR created                   ← Auto-labeled
   ↓
9. GitHub: validate.yml runs            ← Content validation
   ↓
10. GitHub: code-review.yml runs        ← Complexity/security
   ↓
11. GitHub: claude.yml posts reminder   ← Methodology checklist
   ↓
12. Developer: @claude please review    ← Request AI review
   ↓
13. GitHub: Claude analyzes PR          ← Same Claude, different context
   ↓
14. Developer: Address feedback         ← Loop continues
   ↓
15. Merge to main                       ← Full CI passes
   ↓
16. Tag release                         ← release.yml creates release
```

## Benefits

### Consistency
- Same methodology enforced everywhere
- No "works on my machine" for process

### Speed
- Automated checks run in ~5 minutes
- Claude available 24/7 for review

### Quality
- Multi-layer validation catches issues early
- AI understands context and patterns

### Documentation
- Process is documented in code
- New contributors learn by seeing checks

## Troubleshooting

### Claude Not Responding

1. Check `ANTHROPIC_API_KEY` secret is set
2. Ensure @claude is spelled correctly
3. Check Actions tab for workflow run status

### Validation Failing

1. Run validation locally first
2. Check the specific job output
3. Fix issues, push, re-run

### Coverage Not Updating

1. Ensure tests exist in expected locations
2. Check coverage.yml for path patterns
3. Verify pytest is finding tests

## Future Enhancements

- [ ] Slack/Discord notifications on CI failures
- [ ] Auto-merge for Dependabot with passing checks
- [ ] Custom Claude prompts per area (commands vs agents)
- [ ] Metrics dashboard for methodology compliance
- [ ] Integration with project management tools

---

**The recursive loop ensures that claude-flow's methodology is enforced by claude-flow's methodology, creating a self-improving system.**
