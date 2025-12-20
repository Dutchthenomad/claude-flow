# CI/CD Guide

Complete reference for Claude-Flow's automated workflows and CI/CD pipeline.

## Table of Contents

- [Overview](#overview)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)

## Overview

Claude-Flow uses GitHub Actions and AI tools for comprehensive automation including:

- **CodeRabbit AI Review** - Methodology-enforced code review with learning (NEW ✨)
- **Qodo AI Code Review** - AI-powered code analysis and suggestions
- **Automated Code Review** - Complexity analysis, security scanning, impact analysis
- **Smart PR Labeling** - Area, size, and type-based automatic labels
- **Test Coverage Tracking** - Coverage reports, badges, and PR comments
- **Automated Releases** - Tag-based releases with changelogs
- **Security Scanning** - CodeQL, Trivy, Bandit, Gitleaks, and Dependabot

### Architecture

All workflows run in parallel where possible, completing in ~5 minutes:

```
PR Event → [CodeRabbit, Qodo AI Review, Code Review, PR Labeler, Coverage] → Results
Tag Push → [Release Builder] → GitHub Release
Schedule → [Security Scans] → Security Tab
```

### Key Features

✅ **AI-Powered** - CodeRabbit and Qodo provide intelligent, multi-perspective reviews
✅ **Methodology-Enforced** - CodeRabbit validates Claude-Flow's 5 Iron Laws
✅ **Fast** - Parallel execution, ~5 minutes total
✅ **Comprehensive** - Multi-layer security and quality checks
✅ **Learning** - CodeRabbit improves over time based on your decisions
✅ **Informative** - Detailed PR comments with actionable insights
✅ **Automated** - Zero manual intervention required
✅ **Extensible** - Easy to customize and extend

## Workflows

### 1. CodeRabbit AI Review (GitHub App) ✨ NEW

**Triggers**: Pull requests (opened, synchronize, reopened), automatically via GitHub App

**Purpose**: Methodology-enforced code review with persistent learning

**Features**:
- **5 Iron Laws Enforcement** - Validates TDD, Verification, Debugging, Planning, Isolation
- **Context-Aware Analysis** - Deep understanding of Claude-Flow principles
- **Persistent Learning** - Improves over time based on your decisions
- **Tool Integration** - Built-in ruff, shellcheck, markdownlint, gitleaks
- **Interactive Chat** - `@coderabbitai` commands for explanations and suggestions
- **Path-Based Rules** - Custom instructions per directory/file type
- **Zero Setup** - No workflow file or API keys needed

**Configuration**: `.coderabbit.yaml` in repository root

**Setup Required**: 
- Install [CodeRabbit GitHub App](https://github.com/apps/coderabbit-ai)
- Free for public repositories
- No API keys needed

**Output**: Inline comments with 🐰 emoji, summary review, GitHub checks

**Learn More**: See [CodeRabbit Integration Guide](./CODERABBIT_INTEGRATION.md)

---

### 2. Qodo AI Code Review (`.github/workflows/qodo-review.yml`)

**Triggers**: Pull requests (opened, synchronize, reopened, ready_for_review), issue comments

**Purpose**: AI-powered code review with intelligent suggestions

**Features**:
- **Smart Analysis** - Context-aware code review using GPT-4o or Claude
- **Auto-describe** - Generates comprehensive PR descriptions
- **Code Suggestions** - Actionable improvement recommendations
- **Security Detection** - Identifies potential vulnerabilities
- **Interactive** - Respond to `/review`, `/improve`, `/ask` commands

**Configuration**: `.qodo_merge.toml` in repository root

**Setup Required**: 
- Option 1: Install [Qodo GitHub App](https://github.com/apps/qodo-code-review) (recommended)
- Option 2: Add `OPENAI_KEY` or `ANTHROPIC_API_KEY` to repository secrets

**Output**: Inline code comments and summary review on PR

**Learn More**: See [Qodo Integration Guide](./QODO_INTEGRATION.md)

---

### 3. Automated Code Review (`.github/workflows/code-review.yml`)

**Triggers**: Pull requests (opened, synchronize, reopened), manual dispatch

**Purpose**: Provides comprehensive automated code review feedback

**Jobs**:

#### review-complexity
Analyzes code complexity using Radon and Lizard:
- **Cyclomatic Complexity** - Flags functions with complexity > 10
- **Maintainability Index** - Measures code maintainability
- **Halstead Metrics** - Analyzes code difficulty and effort

**What it checks**:
- Python files in `rag-pipeline/`
- Function-level complexity
- Overall maintainability scores

**Output**: Posted as PR comment with detailed metrics

#### review-security
Multi-tool security scanning:
- **Bandit** - Python-specific security issues (SQL injection, hardcoded secrets, etc.)
- **Trivy** - Comprehensive filesystem vulnerability scanning

**What it checks**:
- Known vulnerabilities in dependencies
- Common security anti-patterns
- Hardcoded credentials
- Unsafe function usage

**Output**: 
- PR comment with Bandit results
- SARIF upload to GitHub Security tab

#### review-impact
Analyzes the scope and impact of changes:
- Files changed count
- Areas affected (commands, agents, skills, etc.)
- File type breakdown
- Lines added/deleted
- Large PR warnings (>1000 lines)

**Output**: Posted as PR comment with change statistics

#### review-summary
Aggregates all review results into a single summary comment.

**Example Output**:
```markdown
## 🤖 Automated Code Review Complete

- ✅ Code complexity analysis
- 🔒 Security scan results
- 📊 Change impact analysis

All checks completed in approximately 5 minutes.
```

**Artifacts**: `complexity-report` - Detailed complexity analysis

**Note**: Trivy security scan removed from this workflow to avoid duplication with security.yml

---

### 3. PR Labeler (`.github/workflows/pr-labeler.yml`)

**Triggers**: Pull requests (opened, edited, synchronize, reopened)

**Purpose**: Automatically labels PRs for easy organization and filtering

**Labels Applied**:

#### File-based Labels
Based on `.github/labeler.yml` configuration:
- `area: commands` - Changes to commands/
- `area: agents` - Changes to agents/
- `area: skills` - Changes to skills/
- `area: hooks` - Changes to hooks/
- `area: rag-pipeline` - Changes to rag-pipeline/
- `area: documentation` - Changes to docs/
- `area: ci/cd` - Changes to .github/
- `area: testing` - Changes to tests/

#### Size Labels
Based on lines changed:
- `size/xs` - 0-10 lines
- `size/s` - 11-100 lines
- `size/m` - 101-500 lines
- `size/l` - 501-1000 lines
- `size/xl` - 1000+ lines (with warning comment)

#### Type Labels
Based on PR title keywords:
- `type: bug` - "fix", "bug"
- `type: enhancement` - "feat", "feature", "enhancement"
- `type: documentation` - "docs", "documentation"
- `type: testing` - "test"
- `type: refactor` - "refactor", "cleanup"
- `type: security` - "security", "vuln"
- `type: performance` - "perf", "performance"
- `type: ci/cd` - "ci", "workflow"

#### Priority Labels
Based on PR title:
- `priority: high` - "urgent", "hotfix", "critical"

#### Status Labels
- `status: wip` - "wip", "[wip]", "wip:"

**Best Practices**:
- Use conventional commit format in PR titles: `feat: add new command`
- Mark work-in-progress PRs with "WIP" prefix
- Keep PRs under 500 lines when possible

---

### 4. Test Coverage (`.github/workflows/coverage.yml`)

**Triggers**: Push to main, pull requests, manual dispatch

**Purpose**: Tracks test coverage and generates reports

**Jobs**:

#### coverage
Runs tests with coverage tracking:
1. Sets up Python 3.12
2. Installs dependencies from `rag-pipeline/requirements.txt`
3. Runs pytest with coverage for Python code
4. Generates coverage reports (XML, HTML, terminal)
5. Updates coverage badge (on main branch only)
6. Uploads to Codecov (if token configured)
7. Posts coverage summary to PR

**Coverage Thresholds**:
- ✅ **Green**: 70%+ coverage
- ⚠️ **Orange**: 50-70% coverage
- ❌ **Red**: <50% coverage

**Artifacts**: `coverage-html-report` - Interactive HTML coverage report

**Badge**: Auto-updated `coverage.svg` in repository root

**Configuration**:
- Minimum green: 70%
- Minimum orange: 50%

**Optional**: Set `CODECOV_TOKEN` secret for enhanced Codecov integration

---

### 5. Automated Release (`.github/workflows/release.yml`)

**Triggers**: Tag push (v*.*.*), manual dispatch

**Purpose**: Creates GitHub releases automatically from tags

**Supported Tag Formats**:
- `v1.0.0` - Production release
- `v1.0.0-alpha1` - Alpha release
- `v1.0.0-beta2` - Beta release
- `v1.0.0-rc3` - Release candidate

**Release Process**:
1. Detects tag and determines if prerelease
2. Builds release artifacts:
   - `claude-flow-plugin.tar.gz` - Complete plugin package
   - `claude-flow-docs.tar.gz` - Documentation package
   - `checksums.txt` - SHA256 checksums
3. Generates changelog from PR labels
4. Creates GitHub release with:
   - Auto-generated changelog
   - Installation instructions
   - Artifact downloads
   - SHA256 checksums
5. Creates notification issue for team

**Creating a Release**:

```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0

# For pre-release
git tag v1.0.0-beta1
git push origin v1.0.0-beta1
```

**Changelog Configuration**: `.github/release-changelog-config.json`

Categories:
- 🚀 Features
- 🐛 Bug Fixes
- 🔒 Security
- 📚 Documentation
- ⚡ Performance
- 🧪 Testing
- 🔧 Refactoring
- 🛠️ CI/CD
- 📦 Dependencies
- Area-specific changes

---

### 6. Security Scanning (`.github/workflows/security.yml`)

**Triggers**: Push to main, pull requests, weekly schedule (Sundays), manual dispatch

**Purpose**: Multi-layer security vulnerability detection

**Jobs**:

#### codeql
GitHub's semantic code analysis:
- Scans Python code
- Uses `security-extended` and `security-and-quality` query packs
- Detects code-level vulnerabilities
- Uploads results to Security tab

**Detected Issues**:
- SQL injection
- Command injection
- Path traversal
- XSS vulnerabilities
- Insecure cryptography

#### dependency-review
Reviews dependency changes in PRs:
- Checks for known vulnerabilities
- Blocks PRs with moderate+ severity issues
- Flags restrictive licenses (GPL-3.0, AGPL-3.0)

#### trivy
Comprehensive filesystem scanning:
- Scans entire repository
- Detects vulnerabilities in:
  - Dependencies
  - Container images
  - Infrastructure as Code
  - Misconfigurations
- Reports CRITICAL, HIGH, MEDIUM severity

#### bandit
Python-specific security linting:
- Scans `rag-pipeline/` Python code
- Detects:
  - Hardcoded passwords
  - SQL injection risks
  - Unsafe YAML loading
  - Weak cryptography
  - Shell injection
- SARIF output to Security tab

**Security Schedule**: Weekly scans every Sunday at midnight UTC

**Viewing Results**: GitHub Security tab → Code scanning alerts

## Configuration

### CODEOWNERS (`.github/CODEOWNERS`)

Defines automatic reviewer assignment:

```
# Default owner
* @Dutchthenomad

# Specific areas
/commands/ @Dutchthenomad
/agents/ @Dutchthenomad
/.github/ @Dutchthenomad
```

**Customization**: Add team members or create team-based ownership

### Labeler (`.github/labeler.yml`)

File pattern matching for automatic labels:

```yaml
'area: commands':
  - 'commands/**/*'

'area: agents':
  - 'agents/**/*'
```

**Customization**: Add new areas or adjust patterns

### Release Changelog (`.github/release-changelog-config.json`)

Configures changelog generation:

```json
{
  "categories": [
    {
      "title": "## 🚀 Features",
      "labels": ["type: enhancement", "type: feature"]
    }
  ]
}
```

**Customization**: Add categories or change emojis

### Dependabot (`.github/dependabot.yml`)

Automated dependency updates:

```yaml
updates:
  - package-ecosystem: "pip"
    directory: "/rag-pipeline"
    schedule:
      interval: "weekly"
```

**Customization**: Adjust frequency or add package ecosystems

## Troubleshooting

### Workflow Failures

#### Code Review Fails

**Symptom**: Code review workflow fails to complete

**Common Causes**:
1. **No Python code**: If `rag-pipeline/` doesn't exist
   - *Fix*: Workflow handles this gracefully with placeholder messages

2. **Radon/Bandit installation fails**
   - *Fix*: Check Python version compatibility (requires 3.12)

3. **Permission issues**
   - *Fix*: Ensure workflow has `pull-requests: write` permission

**Debug Steps**:
```bash
# Test locally
pip install radon bandit
radon cc rag-pipeline/ -a -s
bandit -r rag-pipeline/
```

#### Coverage Workflow Issues

**Symptom**: Coverage report not generated

**Common Causes**:
1. **No tests found**
   - *Fix*: Create tests or accept placeholder coverage

2. **Dependencies missing**
   - *Fix*: Ensure `rag-pipeline/requirements.txt` exists

3. **Badge not updating**
   - *Fix*: Check write permissions on main branch

**Debug Steps**:
```bash
# Test locally
pip install -r rag-pipeline/requirements.txt
pip install pytest pytest-cov
pytest --cov=rag-pipeline --cov-report=term
```

#### PR Labeler Not Working

**Symptom**: Labels not applied automatically

**Common Causes**:
1. **Labeler config syntax error**
   - *Fix*: Validate `.github/labeler.yml` YAML syntax

2. **Labels don't exist in repository**
   - *Fix*: Create missing labels in repository settings

3. **Permission denied**
   - *Fix*: Ensure `pull-requests: write` permission

**Debug Steps**:
```bash
# Validate YAML syntax
yamllint .github/labeler.yml

# Check labels
gh label list
```

#### Release Workflow Issues

**Symptom**: Release not created from tag

**Common Causes**:
1. **Invalid tag format**
   - *Fix*: Use `v*.*.*` format (e.g., `v1.0.0`)

2. **Changelog generation fails**
   - *Fix*: Check `.github/release-changelog-config.json` syntax

3. **Artifact build fails**
   - *Fix*: Ensure required directories exist

**Debug Steps**:
```bash
# Test artifact creation locally
tar -czf test.tar.gz .claude-plugin/ commands/ agents/ skills/

# Verify tag format
git tag -l "v*"
```

#### Security Scan Failures

**Symptom**: Security scans fail or timeout

**Common Causes**:
1. **CodeQL build fails**
   - *Fix*: Ensure Python code is valid and dependencies installable

2. **Trivy scan timeout**
   - *Fix*: Large repositories may need increased timeout

3. **SARIF upload fails**
   - *Fix*: Check file format and permissions

**Debug Steps**:
```bash
# Test Bandit locally
pip install bandit
bandit -r rag-pipeline/ -f sarif -o results.sarif

# Test Trivy locally (requires Docker)
docker run aquasec/trivy fs .
```

### Common Issues

#### Workflow Permissions

**Error**: "Resource not accessible by integration"

**Fix**: Add required permissions to workflow:
```yaml
permissions:
  contents: read
  pull-requests: write
  security-events: write
```

#### Rate Limiting

**Error**: GitHub API rate limit exceeded

**Fix**:
- Use `GITHUB_TOKEN` instead of PAT where possible
- Add delays between API calls
- Use conditional execution

#### Concurrent Workflows

**Issue**: Multiple workflows running simultaneously

**Fix**: Use concurrency groups:
```yaml
concurrency:
  group: workflow-${{ github.ref }}
  cancel-in-progress: true
```

#### Artifact Upload Issues

**Error**: Artifact upload fails

**Fix**:
- Check artifact size (<500MB)
- Ensure artifact name is unique
- Verify file paths exist

### Getting Help

1. **Check workflow logs**: Actions tab → Failed workflow → View logs
2. **Review workflow YAML**: Ensure syntax is valid
3. **Test locally**: Run tools locally before pushing
4. **Open issue**: Use CI/CD issue template
5. **GitHub Actions docs**: https://docs.github.com/actions

## Customization

### Adding New Workflows

1. Create YAML file in `.github/workflows/`
2. Define triggers, permissions, jobs
3. Test with `workflow_dispatch` trigger first
4. Document in this guide

**Example**:
```yaml
name: Custom Workflow

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  custom-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom step
        run: echo "Custom action"
```

### Adding New Labels

1. Create labels in repository settings
2. Update `.github/labeler.yml` with patterns
3. Update PR labeler workflow if needed
4. Update release changelog config

### Adding New Security Tools

1. Add tool installation in security workflow
2. Run tool and generate SARIF output
3. Upload SARIF to Security tab
4. Document configuration

**Example** (adding ShellCheck):
```yaml
- name: Run ShellCheck
  uses: ludeeus/action-shellcheck@master
  with:
    format: sarif
    output: shellcheck.sarif

- name: Upload ShellCheck results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: shellcheck.sarif
```

### Customizing Coverage Thresholds

Edit `.github/workflows/coverage.yml`:

```yaml
- name: Coverage comment on PR
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    MINIMUM_GREEN: 80  # Changed from 70
    MINIMUM_ORANGE: 60  # Changed from 50
```

### Adding Test Frameworks

For additional test frameworks, update coverage workflow:

```yaml
- name: Run additional tests
  run: |
    npm test  # For Node.js tests
    go test ./...  # For Go tests
```

### Customizing Release Assets

Edit `.github/workflows/release.yml` to add/remove artifacts:

```yaml
- name: Build additional artifacts
  run: |
    # Create custom packages
    zip -r custom-package.zip custom-dir/
    
    # Move to artifacts directory
    mv custom-package.zip release-artifacts/
```

### Branch Protection Rules

Recommended settings for main branch:

1. **Require pull request reviews**: At least 1 approval
2. **Require status checks**: 
   - `Review / Complexity Analysis`
   - `Review / Security Scan`
   - `Test Coverage`
3. **Require branches to be up to date**: Yes
4. **Require conversation resolution**: Yes
5. **Require signed commits**: Optional but recommended

### Secrets Management

Required secrets (optional):
- `CODECOV_TOKEN` - For enhanced Codecov integration

**Setting secrets**:
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value
4. Update workflow to use: `${{ secrets.SECRET_NAME }}`

## Best Practices

### PR Guidelines

1. **Write descriptive titles**: Use conventional commits format
2. **Keep PRs focused**: Single purpose, <500 lines
3. **Add tests**: Maintain coverage above 70%
4. **Review automation feedback**: Address complexity and security issues
5. **Update documentation**: Keep docs in sync with code

### Workflow Maintenance

1. **Regular updates**: Keep actions versions current
2. **Monitor execution time**: Optimize slow workflows
3. **Review security alerts**: Act on Dependabot PRs
4. **Clean up artifacts**: Remove old workflow artifacts
5. **Test changes**: Use `workflow_dispatch` for testing

### Release Management

1. **Use semantic versioning**: Major.Minor.Patch
2. **Tag appropriately**: Production vs prerelease
3. **Write good PR descriptions**: Powers changelog
4. **Label PRs correctly**: Ensures proper categorization
5. **Test releases**: Use beta/rc tags before production

### Security Practices

1. **Review security alerts**: Check Security tab weekly
2. **Keep dependencies updated**: Merge Dependabot PRs
3. **Run scans locally**: Before pushing sensitive changes
4. **Use secrets properly**: Never hardcode credentials
5. **Monitor permissions**: Minimize workflow permissions

## Metrics and Reporting

### Workflow Success Rate

View in Actions tab:
- Overall success rate
- Per-workflow statistics
- Failure trends

### Coverage Trends

Track over time:
- Coverage badge shows current state
- Codecov provides historical data
- PR comments show coverage changes

### Security Posture

Monitor in Security tab:
- Open alerts by severity
- Time to remediation
- Dependency health

### Release Cadence

Track releases:
- Frequency of releases
- Time between releases
- Pre-release vs production ratio

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/code-security/dependabot)
- [SARIF Format](https://docs.github.com/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
- [Radon Documentation](https://radon.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

---

**Last Updated**: December 2024
**Version**: 1.0.0
