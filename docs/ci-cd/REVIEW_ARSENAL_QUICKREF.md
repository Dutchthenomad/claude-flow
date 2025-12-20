# Code Review Arsenal - Quick Reference

A quick guide to Claude-Flow's multi-layered code review system.

## Review Tools Overview

| Tool | Type | Speed | Focus | When to Use |
|------|------|-------|-------|-------------|
| **CodeRabbit** 🐰 | AI | 1-2 min | Methodology enforcement | Always (automatic) |
| **Qodo** | AI | 1-2 min | Best practices | Always (if configured) |
| **Automated Checks** | Static | 5 min | Metrics & security | Always (automatic) |
| **Human Review** | Manual | Hours-days | Context & design | Final approval |

## CodeRabbit (🐰) - Methodology Enforcer

**What it does:**
- ✅ Validates 5 Iron Laws (TDD, Verification, Debugging, Planning, Isolation)
- ✅ Path-specific rules (Python, workflows, docs, commands)
- ✅ Learns from your decisions over time
- ✅ Built-in tools (ruff, shellcheck, markdownlint, gitleaks)

**How to interact:**
```bash
# In PR comments:
@coderabbitai explain src/feature.py:42
@coderabbitai generate tests
@coderabbitai suggest improvements for error handling
@coderabbitai help
```

**What to look for:**
- Comments with 🐰 emoji
- Methodology violations (TDD, Isolation, etc.)
- Security patterns
- Learning-based suggestions

**Setup:** Install [CodeRabbit GitHub App](https://github.com/apps/coderabbit-ai) - Free for public repos

## Qodo - General Quality

**What it does:**
- ✅ General code quality analysis
- ✅ Bug detection
- ✅ Auto-generate PR descriptions
- ✅ Code improvement suggestions

**How to interact:**
```bash
# In PR comments:
/review
/improve
/describe
/ask <question>
```

**What to look for:**
- General best practices
- Potential bugs
- Performance suggestions
- Alternative approaches

**Setup:** Install [Qodo GitHub App](https://github.com/apps/qodo-code-review) or configure API key

## Automated Checks - Metrics & Security

**What it does:**
- ✅ Code complexity (Radon, Lizard)
- ✅ Security scanning (Bandit, Trivy, CodeQL)
- ✅ Test coverage (pytest)
- ✅ Impact analysis (git stats)

**How to review:**
- Check PR comments for reports
- Look at GitHub Actions workflow results
- Review Security tab for alerts

**What to look for:**
- Coverage drops
- Complexity spikes
- Security vulnerabilities
- Large change warnings

**Setup:** Automatic - no configuration needed

## Review Workflow

### 1. PR Created
```
You create PR → All tools run automatically (1-5 minutes)
```

### 2. Initial Review (Minutes 0-5)
```
CodeRabbit 🐰   → Methodology check (1-2 min)
Qodo            → Quality check (1-2 min)
PR Labeler      → Auto-labels (30 sec)
Automated       → Metrics (5 min)
Coverage        → Test reports (4 min)
```

### 3. Address Feedback (Hours-Days)
```
Priority 1: Methodology violations (CodeRabbit 🐰)
  - Missing tests (TDD)
  - Unverified claims (Verification)
  - No root cause (Debugging)
  - Scope creep (Isolation)

Priority 2: Security issues (Automated + CodeRabbit)
  - High/Critical vulnerabilities
  - Secret leaks
  - Injection risks

Priority 3: Quality improvements (Qodo + CodeRabbit)
  - Code smells
  - Performance suggestions
  - Best practices

Priority 4: Metrics (Automated)
  - Coverage drops
  - Complexity increases
```

### 4. Iterate
```
Push updates → All tools re-run automatically
Discuss with reviewers using @mentions
Use @coderabbitai for clarifications
```

### 5. Merge
```
All checks pass ✅
Human approval obtained ✅
Methodology compliant ✅
No blocking issues ✅
```

## Handling Conflicting Feedback

**CodeRabbit vs Qodo:**
- **Methodology issues**: Prioritize CodeRabbit (it knows Claude-Flow)
- **General quality**: Consider both perspectives
- **Conflicts**: Use your judgment - both are suggestions

**AI vs Automated:**
- **Security**: Trust automated tools (deterministic)
- **Complexity**: AI provides context, metrics provide data
- **Coverage**: Automated tools are source of truth

**AI vs Human:**
- **Design decisions**: Human review wins
- **Methodology interpretation**: Discuss with humans
- **Tactical fixes**: AI suggestions often helpful

## Best Practices

### Do's ✅
- ✅ Address methodology violations immediately
- ✅ Fix security issues before anything else
- ✅ Respond to AI feedback (helps learning)
- ✅ Use chat commands for clarifications
- ✅ Group related changes in single commit
- ✅ Update docs alongside code changes

### Don'ts ❌
- ❌ Ignore CodeRabbit methodology violations
- ❌ Merge with failing security checks
- ❌ Remove tests to increase coverage
- ❌ Add unrelated changes to PR
- ❌ Dismiss all AI feedback without consideration
- ❌ Wait for all reviews before addressing obvious issues

## Troubleshooting

### CodeRabbit not commenting
```bash
# Check:
1. App installed? https://github.com/settings/installations
2. PR is not draft?
3. PR has actual changes?
4. Refresh PR page and wait 2-3 minutes
```

### Too many review comments
```yaml
# Edit .coderabbit.yaml:
reviews:
  profile: "chill"
  collapse_walkthrough: true

# Edit .qodo_merge.toml:
[pr_reviewer]
num_code_suggestions = 1
inline_code_comments = false
```

### Conflicting suggestions
```bash
# Ask for clarification:
@coderabbitai why do you suggest X when Qodo suggested Y?

# Or discuss in PR comments with team
```

### False positive from AI
```bash
# Reply to the comment explaining why it's wrong
# This helps the AI learn

# For CodeRabbit, it will learn from your feedback
# For Qodo, you can use /ask to discuss
```

## Quick Command Reference

### CodeRabbit Commands
```bash
@coderabbitai review              # Full re-review
@coderabbitai resolve             # Mark as resolved
@coderabbitai explain <file:line> # Explain code
@coderabbitai suggest <request>   # Ask for suggestions
@coderabbitai generate tests      # Generate test cases
@coderabbitai help                # Show all commands
```

### Qodo Commands
```bash
/review           # Full code review
/describe         # Generate PR description
/improve          # Code improvement suggestions
/ask <question>   # Ask about the code
/help             # List all commands
```

### GitHub Labels
PR Labeler automatically adds:
- `area:*` - Changed areas (workflows, docs, etc.)
- `size:*` - PR size (XS, S, M, L, XL)
- `type:*` - Change type (feature, bugfix, etc.)

## Resources

- **CodeRabbit Guide**: [docs/ci-cd/CODERABBIT_INTEGRATION.md](./CODERABBIT_INTEGRATION.md)
- **Qodo Guide**: [docs/ci-cd/QODO_INTEGRATION.md](./QODO_INTEGRATION.md)
- **CI/CD Guide**: [docs/ci-cd/CI_CD_GUIDE.md](./CI_CD_GUIDE.md)
- **Workflow Architecture**: [docs/ci-cd/WORKFLOW_ARCHITECTURE.md](./WORKFLOW_ARCHITECTURE.md)

## Support

**Issues**: Open issue with label `type: ci/cd`  
**Questions**: Ask in PR comments or tag @Dutchthenomad  
**Bugs**: Report in issues with reproduction steps

---

**Last Updated**: 2025-12-20  
**Version**: 2.0 (with CodeRabbit)
