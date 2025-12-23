# CodeRabbit Integration Guide

## Overview

Claude-Flow integrates **CodeRabbit** for AI-powered code reviews that complement our existing automated checks and Qodo reviews. CodeRabbit provides intelligent, context-aware analysis specifically tuned to Claude-Flow's methodology.

## What is CodeRabbit?

CodeRabbit is an AI code reviewer that:
- 🤖 Provides intelligent, context-aware code reviews
- 📝 Analyzes code against custom guidelines and best practices
- 🔍 Identifies bugs, security issues, and code smells
- ✅ Validates adherence to project methodology (5 Iron Laws)
- 🔒 Integrates with security scanning tools
- 📊 Learns from your codebase over time
- 💬 Responds to chat commands in PR comments

## Why Both CodeRabbit and Qodo?

While both are AI code reviewers, they complement each other:

| Feature | CodeRabbit | Qodo | Purpose |
|---------|-----------|------|---------|
| Custom methodology | ✅ Deep integration | ⚠️ Via extra_instructions | Claude-Flow compliance |
| Learning system | ✅ Persistent learnings | ❌ Stateless | Improves over time |
| Tool integration | ✅ Built-in (ruff, shellcheck) | ⚠️ Limited | Automated fixes |
| Chat commands | ✅ Interactive | ✅ Interactive | Developer flexibility |
| Setup complexity | ✅ GitHub App only | ⚠️ App or API key | Easier setup |
| Focus area | Methodology + Quality | General quality | Different perspectives |

**Strategy**: Use both for comprehensive coverage. CodeRabbit enforces Claude-Flow principles, Qodo provides general best practices.

## Integration Architecture

### Review Workflow Coordination

```
PR Opened/Updated
    │
    ├── CodeRabbit AI Review (GitHub App)
    │   ├── Claude-Flow methodology enforcement
    │   ├── Context-aware code analysis
    │   ├── Security pattern detection
    │   └── Learning-based suggestions
    │
    ├── Qodo AI Review (qodo-review.yml)
    │   ├── General code quality
    │   ├── Bug detection
    │   └── Improvement suggestions
    │
    ├── Automated Review (code-review.yml)
    │   ├── Complexity metrics (Radon)
    │   ├── Security scan (Bandit)
    │   └── Impact analysis
    │
    ├── Security Scanning (security.yml)
    │   ├── CodeQL
    │   ├── Trivy
    │   ├── Gitleaks (via CodeRabbit)
    │   └── Dependency Review
    │
    └── Test Coverage (coverage.yml)
        └── Coverage reporting & badges
```

### No Workflow File Needed

Unlike Qodo, CodeRabbit operates entirely as a GitHub App - no workflow file is required. This simplifies setup and reduces CI/CD maintenance.

## Setup Instructions

### Step 1: Install CodeRabbit GitHub App

1. **Visit the CodeRabbit installation page**:
   - URL: https://github.com/apps/coderabbit-ai
   - Click "Configure" or "Install"

2. **Select repository**:
   - Choose `Dutchthenomad/claude-flow`
   - Or select your organization and choose repositories

3. **Grant permissions**:
   - Read access to code
   - Write access to pull requests (for comments)
   - Read access to issues (for context)

4. **Complete installation**:
   - Click "Install & Authorize"
   - CodeRabbit will immediately start reviewing new PRs

### Step 2: Verify Configuration

1. **Check configuration file**:
   ```bash
   cat .coderabbit.yaml
   ```
   
2. **Verify the file contains**:
   - Claude-Flow 5 Iron Laws instructions
   - Path-based review instructions
   - Tool integrations (ruff, shellcheck, markdownlint)
   - Security scanning (gitleaks)

3. **Test on a PR**:
   - Create or update any PR
   - CodeRabbit should comment within 1-2 minutes
   - Look for the 🐰 emoji in comments

### Step 3: Configure Team Access (Optional)

1. **Invite team members**:
   - Go to CodeRabbit dashboard: https://coderabbit.ai/dashboard
   - Add team members who should see review insights
   - Set role permissions (reviewer, admin)

2. **Configure notification preferences**:
   - Email digests
   - Slack/Discord webhooks
   - Review reminders

## Configuration

### Main Configuration File (`.coderabbit.yaml`)

The configuration is already set up in the repository root. Key sections:

```yaml
# Review behavior
reviews:
  enabled: true
  profile: "chill"  # Balanced feedback
  auto_review:
    enabled: true
    drafts: false  # Skip draft PRs

# Tool integrations
tools:
  ruff: { enabled: true }        # Python linting
  shellcheck: { enabled: true }  # Shell script linting
  markdownlint: { enabled: true }# Markdown linting
  gitleaks: { enabled: true }    # Secret scanning

# Claude-Flow specific instructions
instructions: |
  [5 Iron Laws enforcement]
  [Code quality standards]
  [Security requirements]
  [Testing requirements]
```

### Customizing for Your Needs

Edit `.coderabbit.yaml` to adjust:

1. **Review intensity**:
   ```yaml
   reviews:
     profile: "assertive"  # More detailed reviews
     # or
     profile: "chill"      # Balanced (default)
   ```

2. **Auto-review triggers**:
   ```yaml
   reviews:
     auto_review:
       base_branches:
         - main
         - develop
         - release/*  # Add more branches
   ```

3. **Path-specific instructions**:
   ```yaml
   path_instructions:
     - path: "your-directory/**"
       instructions: |
         Custom guidelines for this directory
   ```

4. **Tool enablement**:
   ```yaml
   tools:
     your-tool:
       enabled: true
   ```

## Usage

### Automatic Reviews

CodeRabbit runs automatically on:
- ✅ PR opened
- ✅ PR reopened
- ✅ New commits pushed
- ❌ Draft PRs (skipped by default)

### Chat Commands

Comment these on any PR to interact with CodeRabbit:

| Command | Description |
|---------|-------------|
| `@coderabbitai review` | Request full review |
| `@coderabbitai resolve` | Mark conversation as resolved |
| `@coderabbitai help` | Show all available commands |
| `@coderabbitai explain <file>:<line>` | Explain specific code |
| `@coderabbitai suggest <request>` | Ask for improvement suggestions |
| `@coderabbitai generate tests` | Generate test cases |
| `@coderabbitai ignore` | Skip review for this PR |
| `@coderabbitai reset` | Clear learnings for this PR |

### Example Workflow

```bash
# 1. Create feature branch (following Isolation principle)
git checkout -b feature/new-skill

# 2. Write test first (TDD principle)
# Create test file with failing tests
pytest  # Should fail - RED

# 3. Implement feature
# Write minimal code to pass tests
pytest  # Should pass - GREEN

# 4. Refactor if needed
# Clean up code while keeping tests green
pytest  # Should still pass - REFACTOR

# 5. Push and create PR
git push origin feature/new-skill
gh pr create --title "feat: Add new skill for workflow automation"

# 6. Automated reviews run:
# - CodeRabbit: Methodology enforcement, code quality
# - Qodo: General best practices, suggestions
# - Automated checks: Complexity, security, coverage

# 7. Review feedback from all sources
# - CodeRabbit: Inline comments with 🐰 emoji
# - Qodo: Summary and suggestions
# - Automated: Metrics and reports

# 8. Address feedback, push updates
# All reviews re-trigger automatically

# 9. Interact with CodeRabbit if needed
# Comment: @coderabbitai explain src/new_skill.py:42

# 10. Merge when all checks pass and reviews are satisfied
```

## Integration with Claude-Flow Principles

CodeRabbit is specifically configured to enforce the 5 Iron Laws:

### 1. TDD (Test-Driven Development)

**CodeRabbit checks**:
- 🔍 Flags production code without corresponding tests
- 🔍 Verifies test coverage for new functionality
- 🔍 Suggests test cases for edge conditions
- 🔍 Validates test naming conventions

**Example feedback**:
> 🐰 This function in `rag-pipeline/ingestion/ingest.py` appears to be new but has no corresponding test. Per the TDD principle, please add tests in `rag-pipeline/tests/test_ingest.py` before implementing the functionality.

### 2. Verification (Evidence Before Claims)

**CodeRabbit checks**:
- 🔍 Requires PR descriptions to include verification steps
- 🔍 Flags unverified assumptions in code comments
- 🔍 Ensures changes have observable effects (tests, logs, outputs)

**Example feedback**:
> 🐰 The PR description claims "improves performance" but provides no measurements. Please add before/after metrics to verify this claim (Verification principle).

### 3. Debugging (Root Cause Analysis)

**CodeRabbit checks**:
- 🔍 Bug fixes must explain root cause
- 🔍 Temporary workarounds must be marked as TODO
- 🔍 Error handling should be comprehensive

**Example feedback**:
> 🐰 This fix addresses a symptom but doesn't explain the root cause. Why was the variable undefined? Add a comment explaining the underlying issue (Debugging principle).

### 4. Planning (Zero-Context Executability)

**CodeRabbit checks**:
- 🔍 PR descriptions should be self-contained
- 🔍 Commands should be explicit and copy-pasteable
- 🔍 No implicit assumptions about environment

**Example feedback**:
> 🐰 The setup instructions assume Python 3.12 is installed but don't state this. Make requirements explicit (Planning principle).

### 5. Isolation (One Feature Per PR)

**CodeRabbit checks**:
- 🔍 Flags unrelated changes in PR
- 🔍 Detects scope creep
- 🔍 Ensures focused, reviewable changes

**Example feedback**:
> 🐰 This PR includes changes to both the RAG pipeline and GitHub workflows. These are unrelated - split into separate PRs (Isolation principle).

## Monitoring & Troubleshooting

### Check CodeRabbit Status

1. **Dashboard**:
   - Visit: https://coderabbit.ai/dashboard
   - View review history
   - Check credit usage
   - See learning insights

2. **PR Comments**:
   - CodeRabbit comments appear with 🐰 emoji
   - Check for errors or warnings in review status comment
   - Look for "CodeRabbit AI" in PR timeline

3. **GitHub Checks**:
   - CodeRabbit appears as a check in PR
   - Green check = review completed
   - Red X = review failed (rare)
   - Yellow circle = review in progress

### Common Issues

#### Issue: CodeRabbit not commenting on PRs

**Possible causes**:
- App not installed or permissions revoked
- Draft PR (skipped by default)
- No changes in PR (empty diff)
- PR from fork (limited permissions)

**Solutions**:
1. Verify app installation: https://github.com/settings/installations
2. Check PR is not marked as draft
3. Ensure PR has actual code changes
4. For forks, contributor must have app installed on their account

---

#### Issue: Too many comments from all review tools

**Solution**: Adjust review density
```yaml
# .coderabbit.yaml
reviews:
  profile: "chill"  # Less verbose
  high_level_summary: true  # Summary instead of many inline comments
  collapse_walkthrough: true  # Collapse details
```

**Solution**: Adjust Qodo settings
```toml
# .qodo_merge.toml
[pr_reviewer]
num_code_suggestions = 1  # Reduce suggestions
inline_code_comments = false  # Only summary
```

---

#### Issue: CodeRabbit suggestions conflict with Qodo

**Understanding**:
- This is expected - different AI models have different perspectives
- CodeRabbit focuses on Claude-Flow methodology
- Qodo focuses on general best practices

**Resolution**:
1. Prioritize CodeRabbit for methodology issues (TDD, Verification, etc.)
2. Prioritize Qodo for general quality suggestions
3. Use your judgment - both are suggestions, not mandates
4. Discuss conflicting advice in PR comments

---

#### Issue: CodeRabbit feedback seems incorrect

**Options**:
1. **Reply to the comment**: `@coderabbitai explain why you suggested this`
2. **Provide context**: Reply with additional information CodeRabbit may have missed
3. **Dismiss if wrong**: CodeRabbit's comments are suggestions - you can disagree
4. **Improve configuration**: Add clarifications to `.coderabbit.yaml` instructions

---

#### Issue: Learnings causing unwanted suggestions

**Solution**: Reset learnings for this PR
```
@coderabbitai reset
```

**Solution**: Disable learnings globally
```yaml
# .coderabbit.yaml
knowledge_base:
  learnings:
    enabled: false
```

## Cost Considerations

### Pricing Tiers

- **Free (Public repos)**: 
  - Unlimited reviews for open-source projects
  - Full feature access
  - Community support

- **Pro ($12/month per user)**:
  - Private repositories
  - Priority support
  - Advanced analytics
  - Team collaboration features

- **Enterprise (Custom pricing)**:
  - Self-hosted option
  - Custom integrations
  - Dedicated support
  - SLA guarantees

**Recommendation**: Free tier is sufficient for claude-flow (public repo).

### Token Usage

CodeRabbit uses its own AI infrastructure - no API keys needed. Usage is covered by the subscription tier.

## Privacy & Security

✅ **Data Handling**:
- Code is sent to CodeRabbit AI for analysis
- Data is encrypted in transit (TLS)
- Not used for training models (per privacy policy)
- Stored temporarily for review context
- Automatically deleted after retention period

✅ **Permissions**:
- Read access to repository code
- Write access to PR comments and reviews
- Read access to issues for context
- No access to secrets or credentials

✅ **Compliance**:
- SOC 2 Type II certified
- GDPR compliant
- Data residency options available (Enterprise)

❌ **Not Recommended For**:
- Repositories with strict data residency requirements
- Code that cannot leave your infrastructure
- Highly classified or confidential projects

For sensitive repositories, consider self-hosted Enterprise option or disable CodeRabbit.

## Comparison with Other Tools

| Feature | CodeRabbit | Qodo | Automated Checks | Winner |
|---------|-----------|------|------------------|--------|
| Methodology enforcement | ✅ Custom instructions | ⚠️ Limited | ❌ N/A | CodeRabbit |
| Tool integration | ✅ Built-in | ❌ N/A | ✅ Dedicated workflows | Both |
| Learning system | ✅ Persistent | ❌ Stateless | ❌ Static | CodeRabbit |
| Security scanning | ✅ Gitleaks | ❌ N/A | ✅ Bandit, Trivy, CodeQL | Automated |
| Code complexity | ⚠️ AI-based | ⚠️ AI-based | ✅ Radon metrics | Automated |
| Setup complexity | ✅ GitHub App only | ⚠️ App or Actions | ⚠️ Workflow maintenance | CodeRabbit |
| Interactivity | ✅ Chat commands | ✅ Slash commands | ❌ Static | Both AI |
| Review speed | ⚡ 1-2 min | ⚡ 1-2 min | ⏱️ 5+ min | Both AI |
| Cost (public) | ✅ Free | ⚠️ Freemium | ✅ Free | CodeRabbit |

**Conclusion**: All tools serve different purposes:
- **CodeRabbit**: Methodology + Learning + Quality
- **Qodo**: General best practices + Suggestions
- **Automated**: Metrics + Deterministic checks

## Best Practices

### 1. Respond to CodeRabbit Feedback

CodeRabbit learns from interactions. When you:
- ✅ **Accept**: Implement suggestion (CodeRabbit learns it's helpful)
- 🔄 **Discuss**: Ask for clarification (CodeRabbit refines understanding)
- ❌ **Reject**: Explain why not (CodeRabbit learns your preferences)

### 2. Use Chat Commands Effectively

```bash
# When CodeRabbit flags something unclear
@coderabbitai explain <file>:<line>

# When you need test suggestions
@coderabbitai generate tests for src/new_feature.py

# When you disagree with a suggestion
@coderabbitai I chose this approach because [reason]. 
```

### 3. Keep Configuration Updated

When project practices evolve:
```yaml
# .coderabbit.yaml - add new path instructions
path_instructions:
  - path: "new-component/**"
    instructions: |
      New component-specific guidelines
```

### 4. Coordinate with Other Reviews

- Don't wait for all reviews to complete before addressing feedback
- Address blocking issues (TDD violations, security) immediately
- Group related feedback from multiple tools
- Use PR comments to explain decisions to all reviewers (human and AI)

### 5. Leverage Learnings

CodeRabbit remembers:
- Accepted/rejected suggestions
- Project-specific patterns
- Code style preferences

Over time, reviews become more aligned with your codebase.

## Integration with Commands

### `/review` Command

The `/review` command in Claude-Flow can work alongside CodeRabbit:

```markdown
# commands/review.md
When invoked:
1. Check CodeRabbit feedback first
2. Address methodology violations
3. Run automated checks
4. Perform manual review
```

### `/tdd` Command

CodeRabbit validates TDD compliance:
```markdown
# commands/tdd.md
CodeRabbit will:
- Verify tests exist before implementation
- Flag missing test coverage
- Suggest additional test cases
```

## Future Enhancements

- [ ] Custom CodeRabbit rules for Claude-Flow patterns
- [ ] Integration with `/review` command for unified experience
- [ ] Dashboard aggregating all review sources
- [ ] Automated response to common CodeRabbit patterns
- [ ] Learning feedback loop from merged PRs
- [ ] Custom metrics based on 5 Iron Laws compliance

## References

- [CodeRabbit Documentation](https://docs.coderabbit.ai/)
- [CodeRabbit GitHub App](https://github.com/apps/coderabbit-ai)
- [CodeRabbit Configuration Reference](https://docs.coderabbit.ai/guides/configure-coderabbit)
- [Claude-Flow CI/CD Guide](./CI_CD_GUIDE.md)
- [Qodo Integration Guide](./QODO_INTEGRATION.md)

## Support

**Issues with CodeRabbit Integration**: 
- Open an issue with label `type: ci/cd`
- Tag @Dutchthenomad for maintainer attention

**CodeRabbit-specific problems**: 
- Contact CodeRabbit support: support@coderabbit.ai
- Check their documentation: https://docs.coderabbit.ai
- Community Discord: https://discord.gg/coderabbit

---

**Last Updated**: 2025-12-20  
**Maintainer**: @Dutchthenomad  
**Status**: Active ✅
