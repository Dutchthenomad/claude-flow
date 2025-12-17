# CI/CD Quick Reference

Quick command reference and common scenarios for Claude-Flow's CI/CD pipeline.

## Table of Contents

- [Quick Commands](#quick-commands)
- [Common Scenarios](#common-scenarios)
- [Label Reference](#label-reference)
- [Badge Reference](#badge-reference)
- [Cheat Sheets](#cheat-sheets)

## Quick Commands

### Creating a Release

```bash
# Production release
git tag v1.0.0
git push origin v1.0.0

# Pre-release versions
git tag v1.0.0-alpha1    # Alpha
git tag v1.0.0-beta2     # Beta
git tag v1.0.0-rc3       # Release candidate
git push origin v1.0.0-alpha1
```

### Testing Workflows Locally

```bash
# Install act (GitHub Actions local runner)
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act pull_request -W .github/workflows/code-review.yml

# Run with specific event
act push -W .github/workflows/coverage.yml
```

### Manual Workflow Triggers

```bash
# Using GitHub CLI
gh workflow run code-review.yml
gh workflow run coverage.yml
gh workflow run security.yml

# View workflow runs
gh run list --workflow=code-review.yml

# View workflow details
gh run view <run-id>

# Download artifacts
gh run download <run-id>
```

### Checking Workflow Status

```bash
# List all workflows
gh workflow list

# View specific workflow runs
gh run list --workflow=code-review.yml --limit 10

# Watch workflow execution
gh run watch <run-id>

# View workflow logs
gh run view <run-id> --log
```

### Managing Labels

```bash
# List all labels
gh label list

# Create new label
gh label create "priority: high" --color "d73a4a" --description "High priority issue"

# Edit existing label
gh label edit "type: bug" --color "ee0701"

# Delete label
gh label delete "old-label"
```

### Checking Security Alerts

```bash
# List code scanning alerts
gh api repos/{owner}/{repo}/code-scanning/alerts

# List Dependabot alerts
gh api repos/{owner}/{repo}/dependabot/alerts

# View specific alert
gh api repos/{owner}/{repo}/code-scanning/alerts/{alert-number}
```

## Common Scenarios

### Scenario 1: Creating a PR with Automatic Review

```bash
# 1. Create feature branch
git checkout -b feature/new-command

# 2. Make changes
vim commands/new-command.md

# 3. Commit with conventional format
git commit -m "feat(commands): add new command for X"

# 4. Push branch
git push origin feature/new-command

# 5. Create PR
gh pr create --title "feat(commands): add new command for X" \
             --body "Adds new command that does X, Y, Z"

# Automated workflows trigger:
# - Code review (complexity, security, impact)
# - PR labeling (area: commands, type: enhancement)
# - Coverage (if tests added)
```

**Expected Results**:
- PR automatically labeled with `area: commands`, `type: enhancement`, size label
- Code review comment with complexity analysis (~2 min)
- Security scan comment (~3 min)
- Impact analysis comment (~1 min)
- Coverage comment if tests modified (~4 min)

### Scenario 2: Fixing a Bug with High Priority

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-bug

# 2. Fix the bug
vim rag-pipeline/retrieval/retrieve.py

# 3. Add test
vim tests/test_retrieve.py

# 4. Commit
git commit -m "fix(rag): resolve critical retrieval bug"

# 5. Create PR with priority keywords
gh pr create --title "fix(rag): URGENT - resolve critical retrieval bug" \
             --body "Fixes critical bug in retrieval logic..."

# Automated workflows trigger:
# - Labels: area: rag-pipeline, type: bug, priority: high
# - Full code review with security focus
# - Coverage check ensures bug is tested
```

### Scenario 3: Releasing a New Version

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create and push tag
git tag v1.2.0
git push origin v1.2.0

# Automated release workflow triggers:
# - Builds plugin and docs packages
# - Generates changelog from PR labels
# - Creates GitHub release with artifacts
# - Creates notification issue (~3 min)

# 3. Verify release
gh release view v1.2.0

# 4. Download artifacts (optional)
gh release download v1.2.0
```

### Scenario 4: Investigating Security Alert

```bash
# 1. View security alerts
gh api repos/{owner}/{repo}/code-scanning/alerts | jq

# 2. Get alert details
gh api repos/{owner}/{repo}/code-scanning/alerts/1 | jq

# 3. Fix the issue
vim rag-pipeline/affected-file.py

# 4. Commit fix
git commit -m "fix(security): resolve SQL injection in X"

# 5. Create PR
gh pr create --title "fix(security): resolve SQL injection vulnerability"

# Security scan will verify fix on PR
```

### Scenario 5: Updating Dependencies

```bash
# Dependabot creates PR automatically each Monday

# 1. Review Dependabot PR
gh pr view <pr-number>

# 2. Check for vulnerabilities
gh pr checks <pr-number>

# 3. Approve and merge if safe
gh pr review <pr-number> --approve
gh pr merge <pr-number> --squash

# Alternative: Manual dependency update
# 1. Update requirements
vim rag-pipeline/requirements.txt

# 2. Test locally
pip install -r rag-pipeline/requirements.txt
pytest

# 3. Create PR
git commit -m "chore(deps): update dependencies"
gh pr create --title "chore(deps): update Python dependencies"
```

### Scenario 6: Adding New Documentation

```bash
# 1. Create branch
git checkout -b docs/new-guide

# 2. Add documentation
vim docs/new-guide.md

# 3. Commit
git commit -m "docs: add new developer guide"

# 4. Create PR
gh pr create --title "docs: add new developer guide"

# Automated results:
# - Labels: area: documentation, type: documentation
# - Size label based on lines
# - No complexity/security checks (docs only)
# - Fast merge (~1 min for labeling only)
```

### Scenario 7: Working on Large Feature (WIP)

```bash
# 1. Create feature branch
git checkout -b feature/large-refactor

# 2. Create WIP PR early
gh pr create --title "WIP: large refactor of command system" \
             --draft

# Benefits:
# - Early feedback from automated review
# - CI runs on each push
# - Track progress publicly
# - Labels: status: wip

# 3. Push incremental changes
git push origin feature/large-refactor

# 4. When ready, mark as ready for review
gh pr ready <pr-number>

# 5. Remove WIP from title
gh pr edit <pr-number> --title "feat: refactor command system"
```

## Label Reference

### Area Labels
| Label | Description | Auto-applied when |
|-------|-------------|-------------------|
| `area: core` | Core system files | Changes to .claude-plugin/, install.sh |
| `area: commands` | Commands | Changes to commands/ |
| `area: agents` | Agents | Changes to agents/ |
| `area: skills` | Skills | Changes to skills/ |
| `area: hooks` | Hooks | Changes to hooks/ |
| `area: rag-pipeline` | RAG Pipeline | Changes to rag-pipeline/ |
| `area: documentation` | Documentation | Changes to docs/, *.md |
| `area: testing` | Tests | Changes to tests/, test files |
| `area: ci/cd` | CI/CD | Changes to .github/ |

### Type Labels
| Label | Description | Title keywords |
|-------|-------------|----------------|
| `type: bug` | Bug fix | "fix", "bug" |
| `type: enhancement` | New feature | "feat", "feature", "enhancement" |
| `type: documentation` | Documentation | "docs", "documentation" |
| `type: testing` | Testing | "test" |
| `type: refactor` | Refactoring | "refactor", "cleanup" |
| `type: security` | Security fix | "security", "vuln" |
| `type: performance` | Performance | "perf", "performance" |
| `type: ci/cd` | CI/CD changes | "ci", "workflow" |

### Size Labels
| Label | Lines Changed | Warning |
|-------|---------------|---------|
| `size/xs` | 0-10 | None |
| `size/s` | 11-100 | None |
| `size/m` | 101-500 | None |
| `size/l` | 501-1000 | None |
| `size/xl` | 1000+ | Large PR warning |

### Priority Labels
| Label | Description | Title keywords |
|-------|-------------|----------------|
| `priority: high` | High priority | "urgent", "hotfix", "critical" |

### Status Labels
| Label | Description | Title keywords |
|-------|-------------|----------------|
| `status: wip` | Work in progress | "wip", "[wip]", "wip:" |

### Dependency Labels
| Label | Description | Auto-applied when |
|-------|-------------|-------------------|
| `dependencies` | Dependency update | Dependabot PRs |
| `dependencies: python` | Python deps | Changes to requirements.txt |

## Badge Reference

### Adding Badges to README

```markdown
<!-- Workflow status badges -->
![Code Review](https://github.com/Dutchthenomad/claude-flow/actions/workflows/code-review.yml/badge.svg)
![Coverage](https://github.com/Dutchthenomad/claude-flow/actions/workflows/coverage.yml/badge.svg)
![Security](https://github.com/Dutchthenomad/claude-flow/actions/workflows/security.yml/badge.svg)

<!-- Coverage badge (auto-generated) -->
![Coverage](./coverage.svg)

<!-- Version badge -->
![Version](https://img.shields.io/github/v/release/Dutchthenomad/claude-flow)

<!-- License badge -->
![License](https://img.shields.io/github/license/Dutchthenomad/claude-flow)

<!-- Issues badge -->
![Issues](https://img.shields.io/github/issues/Dutchthenomad/claude-flow)

<!-- PR badge -->
![PRs](https://img.shields.io/github/issues-pr/Dutchthenomad/claude-flow)
```

### Badge URLs

**Workflow Status**:
```
https://github.com/{owner}/{repo}/actions/workflows/{workflow}.yml/badge.svg
```

**Coverage** (auto-generated):
```
./coverage.svg
```

**Version**:
```
https://img.shields.io/github/v/release/{owner}/{repo}
```

**Custom Badges** (shields.io):
```
https://img.shields.io/badge/{label}-{message}-{color}
```

## Cheat Sheets

### PR Title Formats

Use conventional commits format for automatic labeling:

```
feat: add new feature
fix: resolve bug
docs: update documentation
test: add tests
refactor: restructure code
perf: improve performance
ci: update workflows
chore: maintenance tasks
security: fix vulnerability
```

**With scope**:
```
feat(commands): add /analyze command
fix(rag): resolve chunking bug
docs(ci-cd): update workflow guide
```

**With priority**:
```
fix: URGENT - critical security issue
feat: HOTFIX - patch deployment script
```

### Workflow YAML Snippets

**Basic workflow structure**:
```yaml
name: My Workflow

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run script
        run: echo "Hello"
```

**Python setup**:
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip

- name: Install dependencies
  run: |
    pip install -r requirements.txt
```

**Conditional execution**:
```yaml
- name: Run on main only
  if: github.ref == 'refs/heads/main'
  run: echo "Main branch"

- name: Run on PR only
  if: github.event_name == 'pull_request'
  run: echo "Pull request"
```

**Artifact upload**:
```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: my-artifact
    path: path/to/files
```

**PR comment**:
```yaml
- name: Comment on PR
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: 'Comment text'
      });
```

### Git Tag Commands

```bash
# List tags
git tag -l

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Create lightweight tag
git tag v1.0.0

# Push tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0
```

### GitHub CLI Commands

```bash
# PR operations
gh pr create                    # Create PR
gh pr list                      # List PRs
gh pr view <number>            # View PR
gh pr checkout <number>        # Checkout PR branch
gh pr review <number>          # Review PR
gh pr merge <number>           # Merge PR
gh pr close <number>           # Close PR

# Workflow operations
gh workflow list               # List workflows
gh workflow view <name>        # View workflow
gh workflow run <name>         # Trigger workflow
gh run list                    # List runs
gh run view <id>               # View run
gh run watch <id>              # Watch run

# Release operations
gh release create <tag>        # Create release
gh release list                # List releases
gh release view <tag>          # View release
gh release download <tag>      # Download assets

# Issue operations
gh issue create                # Create issue
gh issue list                  # List issues
gh issue view <number>         # View issue
gh issue close <number>        # Close issue

# Label operations
gh label create <name>         # Create label
gh label list                  # List labels
gh label edit <name>           # Edit label
gh label delete <name>         # Delete label
```

### Coverage Commands

```bash
# Run tests with coverage
pytest --cov=rag-pipeline --cov-report=term

# Generate HTML report
pytest --cov=rag-pipeline --cov-report=html

# Generate XML report
pytest --cov=rag-pipeline --cov-report=xml

# Run with minimum coverage threshold
pytest --cov=rag-pipeline --cov-fail-under=70

# Show coverage for specific module
pytest --cov=rag-pipeline.retrieval --cov-report=term

# Generate coverage badge
coverage-badge -o coverage.svg
```

### Security Scanning Commands

```bash
# Bandit - Python security
bandit -r rag-pipeline/
bandit -r rag-pipeline/ -f json -o report.json
bandit -r rag-pipeline/ -f sarif -o report.sarif

# Trivy - Filesystem scan
trivy fs .
trivy fs --severity CRITICAL,HIGH .
trivy fs --format sarif -o results.sarif .

# CodeQL (requires codeql CLI)
codeql database create codeql-db --language=python
codeql database analyze codeql-db --format=sarif-latest --output=results.sarif

# Safety - Python dependency check
pip install safety
safety check
safety check --json
```

## Environment Variables

### Workflow Environment Variables

Available in all workflows:

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_TOKEN` | Auto-generated token | `${{ secrets.GITHUB_TOKEN }}` |
| `GITHUB_REPOSITORY` | Owner/repo | `Dutchthenomad/claude-flow` |
| `GITHUB_REF` | Full ref | `refs/heads/main` |
| `GITHUB_SHA` | Commit SHA | `abc123...` |
| `GITHUB_WORKFLOW` | Workflow name | `Automated Code Review` |
| `GITHUB_RUN_ID` | Run ID | `123456789` |
| `GITHUB_RUN_NUMBER` | Run number | `42` |
| `GITHUB_ACTOR` | User who triggered | `Dutchthenomad` |

### Custom Secrets

Set in repository settings:

| Secret | Purpose | Required |
|--------|---------|----------|
| `CODECOV_TOKEN` | Codecov integration | Optional |

## Troubleshooting Quick Fixes

### Workflow won't trigger
```bash
# Check workflow syntax
yamllint .github/workflows/your-workflow.yml

# Check workflow is enabled
gh workflow list

# Manually trigger
gh workflow run your-workflow.yml
```

### Labels not applying
```bash
# Verify labeler config
yamllint .github/labeler.yml

# Check labels exist
gh label list

# Create missing labels
gh label create "area: new-area"
```

### Coverage not updating
```bash
# Check coverage file exists
ls -la coverage.xml coverage.svg

# Verify tests run
pytest --cov=rag-pipeline --cov-report=term

# Check permissions
# Ensure workflow has `contents: write`
```

### Security scan fails
```bash
# Test tools locally
pip install bandit
bandit -r rag-pipeline/

# Check SARIF format
cat results.sarif | jq

# Verify permissions
# Ensure workflow has `security-events: write`
```

## Performance Tips

1. **Use caching**: Cache dependencies to speed up workflows
2. **Parallel jobs**: Run independent jobs in parallel
3. **Concurrency groups**: Cancel outdated runs
4. **Conditional execution**: Skip unnecessary steps
5. **Artifact cleanup**: Remove old artifacts regularly

## Additional Resources

- [CI/CD Guide](./CI_CD_GUIDE.md) - Complete reference
- [Setup Guide](./SETUP_GUIDE.md) - Getting started
- [Onboarding](./ONBOARDING.md) - Developer onboarding
- [Workflow Architecture](./WORKFLOW_ARCHITECTURE.md) - Technical details

---

**Last Updated**: December 2024
**Version**: 1.0.0
