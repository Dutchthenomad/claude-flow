# CI/CD Setup Guide

Complete guide for activating and configuring Claude-Flow's CI/CD pipeline.

## Table of Contents

- [Quick Start](#quick-start)
- [Workflow Activation](#workflow-activation)
- [Optional Integrations](#optional-integrations)
- [Repository Configuration](#repository-configuration)
- [Label Setup](#label-setup)
- [Testing the Pipeline](#testing-the-pipeline)
- [Troubleshooting](#troubleshooting)

## Quick Start

The CI/CD pipeline is **ready to use immediately** after merging the setup PR. No additional configuration is required for basic functionality.

### What's Included Out of the Box

✅ **Automated Code Review** - Runs on every PR
✅ **PR Labeling** - Automatic labels based on changes
✅ **Test Coverage** - Python code coverage tracking
✅ **Security Scanning** - Multi-tool vulnerability detection
✅ **Automated Releases** - Tag-based release creation
✅ **Dependabot** - Weekly dependency updates

### Immediate Actions

After merge, the pipeline will automatically:
1. Label new PRs within 30 seconds
2. Post code review comments within 5 minutes
3. Track coverage on Python changes
4. Scan for security issues
5. Create releases when you push tags

## Workflow Activation

All workflows are **enabled by default** after the setup PR is merged.

### Verify Workflows are Active

```bash
# Using GitHub CLI
gh workflow list

# Expected output:
# NAME                    STATE   ID
# Automated Code Review   active  123456
# PR Labeler             active  123457
# Test Coverage          active  123458
# Automated Release      active  123459
# Security Scanning      active  123460
```

### Manually Enable/Disable Workflows

```bash
# Enable a workflow
gh workflow enable code-review.yml

# Disable a workflow
gh workflow disable code-review.yml
```

Or via GitHub web interface:
1. Go to **Actions** tab
2. Select workflow from sidebar
3. Click **•••** menu → **Enable/Disable workflow**

## Optional Integrations

### 1. Codecov (Enhanced Coverage Reports)

Codecov provides:
- Historical coverage trends
- Coverage diff visualization
- Pull request comments with detailed reports
- Team dashboards

**Setup Steps**:

1. **Sign up for Codecov**
   - Visit https://codecov.io
   - Sign in with GitHub
   - Enable for your repository

2. **Get Codecov Token**
   - Go to repository settings in Codecov
   - Copy the upload token

3. **Add Token to GitHub Secrets**
   ```bash
   # Using GitHub CLI
   gh secret set CODECOV_TOKEN
   # Paste token when prompted
   
   # Or via web interface:
   # Settings → Secrets and variables → Actions → New repository secret
   # Name: CODECOV_TOKEN
   # Value: [your token]
   ```

4. **Verify Integration**
   - Create a PR
   - Check for Codecov comment
   - View reports at codecov.io

**Status**: Optional but recommended for teams

### 2. Branch Protection Rules

Enforce quality standards by requiring checks to pass before merge.

**Recommended Settings**:

1. **Navigate to Settings**
   - Repository → Settings → Branches
   - Click "Add rule" for `main` branch

2. **Configure Protection**
   ```
   ✅ Require a pull request before merging
      ✅ Require approvals (1)
      ✅ Dismiss stale reviews
   
   ✅ Require status checks to pass before merging
      ✅ Require branches to be up to date
      Status checks:
         ✅ Review / Complexity Analysis
         ✅ Review / Security Scan
         ✅ Review / Change Impact Analysis
         ✅ Test Coverage
         ✅ CodeQL
   
   ✅ Require conversation resolution before merging
   ✅ Require signed commits (optional)
   ✅ Include administrators
   ```

3. **Save Protection Rule**

**Status**: Recommended for production repositories

### 3. Code Scanning Alerts

Enable GitHub's native security scanning features.

**Setup Steps**:

1. **Enable Dependabot Alerts**
   - Settings → Code security and analysis
   - Enable "Dependency graph"
   - Enable "Dependabot alerts"
   - Enable "Dependabot security updates"

2. **Enable Secret Scanning**
   - Enable "Secret scanning"
   - Enable "Push protection"

3. **Configure Code Scanning**
   - Already configured via `security.yml` workflow
   - View alerts in Security → Code scanning

**Status**: Highly recommended

### 4. Notifications

Configure notifications for workflow failures and security alerts.

**Email Notifications**:
1. Settings → Notifications
2. Configure email preferences
3. Enable "Actions" notifications

**Slack Integration** (Optional):
```yaml
# Add to workflow
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Workflow failed: ${{ github.workflow }}"
      }
```

**Status**: Optional

## Repository Configuration

### Required Configuration

These settings are **required** for the pipeline to function:

1. **GitHub Actions Enabled**
   - Settings → Actions → General
   - Allow all actions and reusable workflows

2. **Workflow Permissions**
   - Settings → Actions → General → Workflow permissions
   - Select "Read and write permissions"
   - Enable "Allow GitHub Actions to create and approve pull requests"

3. **Pages (for coverage badge)**
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, /root

### Recommended Configuration

These settings enhance the pipeline:

1. **Issue Templates**
   - Already configured in `.github/ISSUE_TEMPLATE/`
   - Users can select appropriate template when creating issues

2. **CODEOWNERS**
   - Already configured in `.github/CODEOWNERS`
   - Update with your team members:
   ```
   # .github/CODEOWNERS
   * @Dutchthenomad @teammate1 @teammate2
   
   /commands/ @command-experts
   /agents/ @agent-experts
   /.github/ @devops-team
   ```

3. **PR Template**
   - Already configured in `.github/pull_request_template.md`
   - Automatically shown when creating PRs

## Label Setup

Labels are used for PR organization and changelog generation.

### Create Required Labels

Run this script to create all labels:

```bash
#!/bin/bash
# create-labels.sh

# Area labels
gh label create "area: core" --color "0052CC" --description "Core system files"
gh label create "area: commands" --color "0052CC" --description "Command files"
gh label create "area: agents" --color "0052CC" --description "Agent files"
gh label create "area: skills" --color "0052CC" --description "Skill files"
gh label create "area: hooks" --color "0052CC" --description "Hook files"
gh label create "area: rag-pipeline" --color "0052CC" --description "RAG pipeline"
gh label create "area: documentation" --color "0052CC" --description "Documentation"
gh label create "area: testing" --color "0052CC" --description "Tests"
gh label create "area: ci/cd" --color "0052CC" --description "CI/CD"
gh label create "area: config" --color "0052CC" --description "Configuration"
gh label create "area: integrations" --color "0052CC" --description "Integrations"
gh label create "area: knowledge" --color "0052CC" --description "Knowledge base"
gh label create "area: scripts" --color "0052CC" --description "Scripts"

# Type labels
gh label create "type: bug" --color "d73a4a" --description "Bug fix"
gh label create "type: enhancement" --color "a2eeef" --description "New feature"
gh label create "type: documentation" --color "0075ca" --description "Documentation"
gh label create "type: testing" --color "bfd4f2" --description "Testing"
gh label create "type: refactor" --color "fbca04" --description "Refactoring"
gh label create "type: security" --color "ee0701" --description "Security"
gh label create "type: performance" --color "ffcc00" --description "Performance"
gh label create "type: ci/cd" --color "5319e7" --description "CI/CD"

# Size labels
gh label create "size/xs" --color "00ff00" --description "0-10 lines"
gh label create "size/s" --color "7fdd4c" --description "11-100 lines"
gh label create "size/m" --color "ffcc00" --description "101-500 lines"
gh label create "size/l" --color "ff9933" --description "501-1000 lines"
gh label create "size/xl" --color "ff0000" --description "1000+ lines"

# Priority labels
gh label create "priority: high" --color "d93f0b" --description "High priority"
gh label create "priority: medium" --color "fbca04" --description "Medium priority"
gh label create "priority: low" --color "0e8a16" --description "Low priority"

# Status labels
gh label create "status: wip" --color "ededed" --description "Work in progress"
gh label create "status: blocked" --color "b60205" --description "Blocked"
gh label create "status: ready" --color "0e8a16" --description "Ready for review"

# Dependency labels
gh label create "dependencies" --color "0366d6" --description "Dependency update"
gh label create "dependencies: python" --color "0366d6" --description "Python deps"

# Release label
gh label create "release" --color "5319e7" --description "Release"
gh label create "automated" --color "ededed" --description "Automated"
```

**Run the script**:
```bash
chmod +x create-labels.sh
./create-labels.sh
```

Or create labels manually in the GitHub web interface:
1. Go to Issues → Labels
2. Click "New label"
3. Enter name, color, and description
4. Click "Create label"

### Verify Labels

```bash
# List all labels
gh label list

# Should show all area, type, size, priority, and status labels
```

## Testing the Pipeline

### Test 1: PR Labeling

```bash
# Create test branch
git checkout -b test/pr-labeling

# Make small change to command
echo "# Test change" >> commands/tdd.md

# Commit and push
git add .
git commit -m "test: verify PR labeling"
git push origin test/pr-labeling

# Create PR
gh pr create --title "test: verify PR labeling" \
             --body "Testing automated PR labeling"

# Check PR for labels
gh pr view --web

# Expected labels:
# - area: commands
# - type: testing
# - size/xs
```

**Clean up**:
```bash
gh pr close --delete-branch
git checkout main
```

### Test 2: Code Review

```bash
# Create test branch
git checkout -b test/code-review

# Add Python function with high complexity
cat > rag-pipeline/test_complexity.py << 'EOF'
def complex_function(x):
    if x > 10:
        if x > 20:
            if x > 30:
                if x > 40:
                    if x > 50:
                        return "very high"
                    return "high"
                return "medium"
            return "low"
        return "very low"
    return "minimal"
EOF

# Commit and push
git add .
git commit -m "test: add complex function"
git push origin test/code-review

# Create PR
gh pr create --title "test: verify code review" \
             --body "Testing complexity analysis"

# Wait 5 minutes for code review comments
# Check PR for complexity report
gh pr view --web
```

**Expected**: Comment with high complexity warning for `complex_function`

**Clean up**:
```bash
rm rag-pipeline/test_complexity.py
gh pr close --delete-branch
git checkout main
```

### Test 3: Coverage Tracking

```bash
# Create test branch
git checkout -b test/coverage

# Add test file
mkdir -p tests
cat > tests/test_sample.py << 'EOF'
def test_example():
    assert True
EOF

# Commit and push
git add .
git commit -m "test: add sample test"
git push origin test/coverage

# Create PR
gh pr create --title "test: verify coverage tracking" \
             --body "Testing coverage workflow"

# Wait for coverage report
gh pr view --web
```

**Expected**: Coverage comment on PR

**Clean up**:
```bash
gh pr close --delete-branch
git checkout main
```

### Test 4: Automated Release

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create and push tag
git tag v0.0.1-test
git push origin v0.0.1-test

# Wait 3 minutes for release creation
# Check releases
gh release list

# View release
gh release view v0.0.1-test
```

**Expected**: 
- GitHub release created
- Artifacts attached
- Changelog generated
- Notification issue created

**Clean up**:
```bash
gh release delete v0.0.1-test --yes
git tag -d v0.0.1-test
git push origin :refs/tags/v0.0.1-test
```

### Test 5: Security Scanning

```bash
# Security scans run automatically on:
# - Push to main
# - Pull requests
# - Weekly schedule

# View security alerts
gh api repos/{owner}/{repo}/code-scanning/alerts | jq

# Or check in web interface:
# Security → Code scanning
```

## Troubleshooting

### Workflows Not Running

**Problem**: Workflows don't trigger on PR creation

**Solutions**:

1. **Check workflow files exist**
   ```bash
   ls -la .github/workflows/
   ```

2. **Verify Actions are enabled**
   - Settings → Actions → General
   - Ensure "Allow all actions" is selected

3. **Check workflow syntax**
   ```bash
   yamllint .github/workflows/*.yml
   ```

4. **View workflow logs**
   - Actions tab → Select workflow → View logs

### Labels Not Created

**Problem**: PR labeler fails because labels don't exist

**Solution**:
```bash
# Run label creation script
./create-labels.sh

# Or manually create labels
gh label create "area: commands"
```

### Coverage Badge Not Updating

**Problem**: Coverage badge doesn't update on main

**Solutions**:

1. **Check workflow permissions**
   - Settings → Actions → Workflow permissions
   - Enable "Read and write permissions"

2. **Verify badge file is committed**
   ```bash
   ls -la coverage.svg
   ```

3. **Check workflow logs**
   - Actions → Coverage → View logs

### Security Scans Failing

**Problem**: CodeQL or Trivy scans fail

**Solutions**:

1. **For CodeQL**: Ensure Python code is valid
   ```bash
   python -m py_compile rag-pipeline/**/*.py
   ```

2. **For Trivy**: Check Docker is available
   ```bash
   docker --version
   ```

3. **Review scan logs**
   - Actions → Security Scanning → View logs

### Release Creation Fails

**Problem**: Release workflow fails on tag push

**Solutions**:

1. **Verify tag format**
   ```bash
   # Should match v*.*.*
   git tag v1.0.0  # Good
   git tag 1.0.0   # Bad
   ```

2. **Check required files exist**
   ```bash
   ls .claude-plugin/ commands/ agents/ skills/
   ```

3. **View workflow logs**
   - Actions → Automated Release → View logs

## Next Steps

After setup is complete:

1. **Read the CI/CD Guide**: [CI_CD_GUIDE.md](./CI_CD_GUIDE.md)
2. **Review Quick Reference**: [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
3. **Onboard your team**: [ONBOARDING.md](./ONBOARDING.md)
4. **Understand architecture**: [WORKFLOW_ARCHITECTURE.md](./WORKFLOW_ARCHITECTURE.md)
5. **Create your first PR**: Test the pipeline with a small change

## Support

If you encounter issues:

1. Check [Troubleshooting section](#troubleshooting)
2. Review [CI/CD Guide](./CI_CD_GUIDE.md)
3. Search existing issues
4. Create new issue using CI/CD template

## Checklist

Before marking setup complete:

- [ ] All workflows visible in Actions tab
- [ ] All required labels created
- [ ] Workflow permissions configured
- [ ] Branch protection rules set (recommended)
- [ ] PR labeling tested
- [ ] Code review tested
- [ ] Coverage tracking tested
- [ ] Release creation tested
- [ ] Team members added to CODEOWNERS
- [ ] Documentation reviewed
- [ ] Optional integrations configured (if desired)

---

**Last Updated**: December 2024
**Version**: 1.0.0
