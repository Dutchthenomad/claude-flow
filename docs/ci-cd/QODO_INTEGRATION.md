# Qodo Integration Guide

## Overview

Claude-Flow now integrates **Qodo Merge** (formerly PR-Agent) for AI-powered code reviews. Qodo provides intelligent, context-aware code review suggestions that complement our existing automated checks.

## What is Qodo?

Qodo Merge is an AI-powered code review tool that:
- 🤖 Provides intelligent code review suggestions
- 📝 Automatically generates PR descriptions
- 🔍 Identifies potential bugs and code smells
- ✅ Suggests code improvements
- 🔒 Flags security concerns
- 📊 Estimates review effort

## Integration Architecture

### Workflow Coordination

```
PR Opened/Updated
    │
    ├── Qodo AI Review (qodo-review.yml)
    │   └── AI-powered code analysis & suggestions
    │
    ├── Automated Review (code-review.yml)
    │   ├── Complexity analysis (Radon)
    │   ├── Security scan (Bandit)
    │   └── Impact analysis
    │
    ├── Security Scanning (security.yml)
    │   ├── CodeQL
    │   ├── Trivy
    │   └── Dependency Review
    │
    └── Test Coverage (coverage.yml)
        └── Coverage reporting & badges
```

### Conflict Resolution

**Problem**: Multiple workflows posting comments could cause spam.

**Solution**: 
- ✅ Each workflow uses unique concurrency groups
- ✅ Qodo comments are consolidated and actionable
- ✅ Traditional checks provide metrics/reports
- ✅ Summary comments reference all review types

**Problem**: Duplicate security scans (Trivy in multiple workflows).

**Solution**:
- ✅ Removed Trivy from `code-review.yml`
- ✅ Kept Trivy in `security.yml` (dedicated security workflow)
- ✅ All security results aggregate in GitHub Security tab

## Setup Instructions

### Option 1: GitHub App (Recommended)

1. **Install the Qodo GitHub App**:
   - Visit: https://github.com/apps/qodo-code-review
   - Click "Configure"
   - Select `Dutchthenomad/claude-flow` repository
   - Grant required permissions

2. **Benefits**:
   - ✅ No API key management needed
   - ✅ Automatic updates
   - ✅ Interactive PR comments
   - ✅ Free tier available

### Option 2: GitHub Actions with API Key

1. **Get an API Key**:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic Claude: https://console.anthropic.com/
   - Gemini: https://makersuite.google.com/app/apikey

2. **Add Secret to Repository**:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `OPENAI_KEY` (or `ANTHROPIC_API_KEY`)
   - Value: Your API key
   - Click "Add secret"

3. **Workflow Activation**:
   - The workflow is already configured in `.github/workflows/qodo-review.yml`
   - It will automatically run on all PRs once the API key is added

## Configuration

### Qodo Settings (`.qodo_merge.toml`)

```toml
[config]
model = "gpt-4o"  # AI model to use

[github_app]
auto_review = true
auto_describe = true
pr_commands = ["/describe", "/review"]

[pr_reviewer]
num_code_suggestions = 3
inline_code_comments = true
extra_instructions = "Follow Claude-Flow's 5 Iron Laws..."
```

**Key Settings**:
- `auto_review`: Automatically review PRs when opened
- `auto_describe`: Generate PR descriptions
- `num_code_suggestions`: Limit suggestions to avoid noise
- `extra_instructions`: Claude-Flow specific guidelines

### Customizing for Your Needs

Edit `.qodo_merge.toml` to adjust:
- Review frequency (`handle_pr_actions`)
- Number of suggestions (`num_code_suggestions`)
- Commands to run automatically (`pr_commands`)
- Organization best practices (`extra_instructions`)

## Usage

### Automatic Reviews

Qodo runs automatically on:
- PR opened
- PR reopened
- PR marked as ready for review
- New commits pushed (synchronize)

### Manual Commands

Comment these on any PR to trigger Qodo:

| Command | Description |
|---------|-------------|
| `/review` | Full code review |
| `/describe` | Generate PR description |
| `/improve` | Code improvement suggestions |
| `/ask <question>` | Ask Qodo about the code |
| `/update_changelog` | Update CHANGELOG.md |
| `/help` | List all commands |

### Example Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-command

# 2. Make changes following TDD
# (write test first, then implementation)

# 3. Push and create PR
git push origin feature/new-command
gh pr create --title "feat: Add new command"

# 4. Automated reviews run:
# - Qodo AI analyzes code
# - Complexity checks run
# - Security scans execute
# - Coverage reports generated

# 5. Review Qodo suggestions in PR comments
# 6. Address feedback, push updates
# 7. Re-review happens automatically
```

## Integration with Claude-Flow Principles

Qodo complements the 5 Iron Laws:

### 1. TDD (Test-Driven Development)
- Qodo flags missing tests
- Suggests test cases for edge conditions
- Validates test coverage

### 2. Verification
- Provides evidence-based review comments
- References specific code locations
- Links to documentation for suggestions

### 3. Debugging
- Identifies potential bugs before runtime
- Suggests root cause investigations
- Flags error handling issues

### 4. Planning
- Reviews code against PR description
- Ensures implementation matches intent
- Checks for scope creep

### 5. Isolation
- Reviews changes in context of branch
- Identifies conflicts with main branch
- Suggests refactoring for modularity

## Monitoring & Troubleshooting

### Check Workflow Status

```bash
# View recent workflow runs
gh run list --workflow=qodo-review.yml

# View specific run logs
gh run view <run-id> --log
```

### Common Issues

**Issue**: Qodo workflow fails with "missing API key"

**Solution**: Add `OPENAI_KEY` or `ANTHROPIC_API_KEY` to repository secrets

---

**Issue**: Too many comments on PRs

**Solution**: Adjust `.qodo_merge.toml`:
```toml
[pr_reviewer]
num_code_suggestions = 2  # Reduce from 3
inline_code_comments = false  # Only summary comments
```

---

**Issue**: Qodo suggestions don't align with Claude-Flow practices

**Solution**: Update `extra_instructions` in `.qodo_merge.toml` with more specific guidelines

---

**Issue**: Rate limiting errors

**Solution**: 
- Option 1: Upgrade API plan
- Option 2: Use GitHub App instead of Actions
- Option 3: Adjust `handle_pr_actions` to reduce frequency

## Cost Considerations

### GitHub App (Recommended)
- **Free tier**: 100 reviews/month for public repos
- **Pro**: $19/month per user for private repos
- **Team**: Custom pricing for organizations

### GitHub Actions with API
- **OpenAI GPT-4o**: ~$0.01-0.05 per review
- **Anthropic Claude**: ~$0.02-0.08 per review
- **Gemini**: Variable, generally lower cost

**Recommendation**: Start with GitHub App free tier, evaluate value before scaling.

## Privacy & Security

✅ **Data Handling**:
- Code is sent to AI provider for analysis
- No code is stored or used for training (per Qodo privacy policy)
- Results are only visible to repository collaborators

✅ **Permissions**:
- Read access to repository code
- Write access to PR comments
- No access to secrets or credentials

❌ **Not Recommended For**:
- Repositories with strict data residency requirements
- Code that cannot leave your infrastructure
- Highly confidential proprietary algorithms

For sensitive repos, consider self-hosted Qodo or disable AI reviews.

## Comparison with Existing Tools

| Feature | Qodo | Existing Workflows | Winner |
|---------|------|-------------------|--------|
| Code complexity | AI-suggested refactors | Radon metrics | Both complement |
| Security | Pattern detection | Bandit + Trivy + CodeQL | Existing |
| Test coverage | Suggests tests | Pytest reports | Both complement |
| Code style | Context-aware | N/A | Qodo |
| Logic bugs | AI detection | N/A | Qodo |
| Change impact | AI explanation | Git stats | Both complement |
| Review speed | Real-time | ~5 minutes | Qodo |

**Conclusion**: Qodo enhances rather than replaces existing checks.

## Future Enhancements

- [ ] Custom Qodo rules for Claude-Flow specific patterns
- [ ] Integration with `/review` command in commands/
- [ ] Qodo test generation integration with `/tdd` command
- [ ] Aggregate review dashboard combining all checks
- [ ] Qodo coverage expansion for Python in rag-pipeline/

## References

- [Qodo Merge Documentation](https://docs.qodo.ai/qodo-documentation/qodo-merge)
- [Qodo GitHub App](https://github.com/apps/qodo-code-review)
- [Qodo CI Examples](https://github.com/qodo-ai/qodo-ci-example)
- [Claude-Flow CI/CD Guide](./CI_CD_GUIDE.md)

## Support

**Issues with Qodo Integration**: Open an issue with label `type: ci/cd`

**Qodo-specific problems**: Contact Qodo support or check their [documentation](https://docs.qodo.ai)

---

**Last Updated**: 2025-12-17  
**Maintainer**: @Dutchthenomad
