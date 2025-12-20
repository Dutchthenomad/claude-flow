# CI/CD Workflow Architecture

Technical architecture and execution flow of Claude-Flow's CI/CD pipeline.

## Table of Contents

- [System Overview](#system-overview)
- [Workflow Diagrams](#workflow-diagrams)
- [Technical Details](#technical-details)
- [Integration Points](#integration-points)
- [Performance Characteristics](#performance-characteristics)
- [Extensibility](#extensibility)

## System Overview

### Architecture Principles

1. **Parallel Execution** - Independent jobs run concurrently for speed
2. **Fail-Fast** - Early detection of issues
3. **Idempotent** - Workflows can be re-run safely
4. **Declarative** - YAML configuration is version-controlled
5. **Observable** - Comprehensive logging and reporting

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Repository                      │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │  .github/  │  │  commands/ │  │  rag-pipeline/  │  │
│  │ workflows/ │  │   agents/  │  │     docs/       │  │
│  └────────────┘  └────────────┘  └─────────────────┘  │
└────────────┬─────────────────────────────────────┬─────┘
             │                                     │
             ▼                                     ▼
┌─────────────────────────────┐    ┌────────────────────────┐
│    GitHub Actions Runner     │    │   External Services    │
│  ┌────────────────────────┐ │    │  ┌──────────────────┐ │
│  │  Workflow Orchestrator │ │    │  │    CodeRabbit    │ │
│  └────────────────────────┘ │    │  │    Qodo AI       │ │
│  ┌────────────────────────┐ │    │  │    Codecov       │ │
│  │   Job Executor         │ │    │  │    Trivy DB      │ │
│  │  - Code Review         │ │    │  │    CodeQL DB     │ │
│  │  - PR Labeler          │ │    │  └──────────────────┘ │
│  │  - Coverage            │ │    └────────────────────────┘
│  │  - Security            │ │                │
│  │  - Release             │ │                │
│  └────────────────────────┘ │                │
└──────────────┬──────────────┘                │
               │                                │
               ▼                                │
┌─────────────────────────────────────────────┴┐
│            GitHub API / UI                    │
│  - PR Comments (CodeRabbit 🐰, Qodo)         │
│  - Status Checks                              │
│  - Security Alerts                            │
│  - Releases                                   │
│  - Artifacts                                  │
└───────────────────────────────────────────────┘
```

## Workflow Diagrams

### PR Creation Flow

```
Developer creates PR
        │
        ├─→ [CodeRabbit AI] (1-2 min, GitHub App)
        │   ├─ 5 Iron Laws validation
        │   ├─ Context-aware analysis
        │   ├─ Tool checks (ruff, shellcheck, etc.)
        │   └─ Learning-based suggestions
        │
        ├─→ [Qodo AI Workflow] (1-2 min, if configured)
        │   ├─ AI code review
        │   ├─ PR description generation
        │   └─ Improvement suggestions
        │
        ├─→ [PR Labeler Workflow] (30 sec)
        │   ├─ File-based labeling
        │   ├─ Size labeling
        │   └─ Title-based labeling
        │
        ├─→ [Code Review Workflow] (5 min)
        │   ├─ Complexity Analysis (parallel)
        │   │   └─ Radon, Lizard
        │   ├─ Security Scan (parallel)
        │   │   └─ Bandit
        │   └─ Impact Analysis (parallel)
        │       └─ Git diff analysis
        │
        └─→ [Coverage Workflow] (4 min)
            ├─ Run tests
            ├─ Generate coverage
            └─ Post PR comment
```

### Tag Push Flow

```
Developer pushes tag (v*.*.*)
        │
        └─→ [Release Workflow] (3 min)
            ├─ Detect tag format
            ├─ Build artifacts (parallel)
            │   ├─ Plugin package
            │   ├─ Docs package
            │   └─ Checksums
            ├─ Generate changelog
            ├─ Create GitHub release
            └─ Create notification issue
```

### Scheduled Security Scan Flow

```
Sunday 00:00 UTC (weekly)
        │
        └─→ [Security Workflow] (10 min)
            ├─ CodeQL Analysis (parallel)
            ├─ Trivy Scan (parallel)
            ├─ Bandit Scan (parallel)
            └─ Upload SARIF to Security tab
```

### Dependabot Flow

```
Monday morning (weekly)
        │
        └─→ [Dependabot] (automatic)
            ├─ Check for updates
            ├─ Create PRs (max 5)
            │   └─ Triggers PR workflows
            └─ Apply labels
```

## Technical Details

### Workflow: Code Review

**File**: `.github/workflows/code-review.yml`

**Trigger Events**:
- `pull_request` (opened, synchronize, reopened)
- `workflow_dispatch` (manual)

**Concurrency**: `code-review-${{ github.ref }}`
- Cancels in-progress runs for same ref
- Prevents duplicate runs

**Jobs Breakdown**:

#### Job: review-complexity
```yaml
Runner: ubuntu-latest
Timeout: 15 minutes
Permissions: contents: read, pull-requests: write

Steps:
1. Checkout (with full history)
2. Set up Python 3.12
3. Install radon, lizard
4. Run complexity analysis
   - Cyclomatic complexity (radon cc)
   - Maintainability index (radon mi)
   - Halstead metrics (radon hal)
5. Generate markdown report
6. Upload artifact
7. Post PR comment

Dependencies: None (runs in parallel)
```

#### Job: review-security
```yaml
Runner: ubuntu-latest
Timeout: 15 minutes
Permissions: contents: read, pull-requests: write, security-events: write

Steps:
1. Checkout
2. Set up Python 3.12
3. Install Bandit
4. Run Bandit scan (Python)
5. Run Trivy scan (filesystem)
6. Upload SARIF to Security tab
7. Post PR comment

Dependencies: None (runs in parallel)
```

#### Job: review-impact
```yaml
Runner: ubuntu-latest
Timeout: 10 minutes
Permissions: contents: read, pull-requests: write

Steps:
1. Checkout (with full history)
2. Analyze changes
   - Count files
   - Identify areas
   - Calculate line changes
   - Detect large PRs
3. Generate report
4. Post PR comment

Dependencies: None (runs in parallel)
```

#### Job: review-summary
```yaml
Runner: ubuntu-latest
Timeout: 5 minutes
Permissions: pull-requests: write

Steps:
1. Post summary comment

Dependencies: All other jobs (waits for completion)
Condition: always() (runs even if others fail)
```

**Performance**:
- Total time: ~5 minutes
- Parallelization: 3 jobs run concurrently
- Artifact size: ~10 KB

### Workflow: PR Labeler

**File**: `.github/workflows/pr-labeler.yml`

**Trigger Events**:
- `pull_request` (opened, edited, synchronize, reopened)

**Jobs Breakdown**:

#### Job: label
```yaml
Runner: ubuntu-latest
Timeout: 5 minutes
Permissions: contents: read, pull-requests: write

Steps:
1. Checkout
2. Run actions/labeler@v5
   - Uses .github/labeler.yml
   - Matches file patterns
3. Run pr-size-labeler@v1
   - Calculates lines changed
   - Applies size labels
4. Run github-script for title labels
   - Parses PR title
   - Applies type/priority labels

Dependencies: None
```

**Performance**:
- Total time: ~30 seconds
- No parallelization needed
- Minimal resource usage

### Workflow: Coverage

**File**: `.github/workflows/coverage.yml`

**Trigger Events**:
- `push` (main branch)
- `pull_request`
- `workflow_dispatch`

**Jobs Breakdown**:

#### Job: coverage
```yaml
Runner: ubuntu-latest
Timeout: 20 minutes
Permissions: contents: write, pull-requests: write

Steps:
1. Checkout (with history)
2. Set up Python 3.12 (with pip cache)
3. Install dependencies
   - Project dependencies
   - Test dependencies
4. Run pytest with coverage
   - XML report
   - HTML report
   - Terminal report
5. Generate coverage badge (main only)
6. Commit badge (main only)
7. Upload to Codecov (if token)
8. Post PR comment (PR only)
9. Upload HTML artifact

Dependencies: None
```

**Performance**:
- Total time: ~4 minutes
- Test execution: ~2 minutes
- Report generation: ~1 minute
- Artifact upload: ~1 minute

### Workflow: Release

**File**: `.github/workflows/release.yml`

**Trigger Events**:
- `push` (tags: v*.*.*)
- `workflow_dispatch`

**Jobs Breakdown**:

#### Job: release
```yaml
Runner: ubuntu-latest
Timeout: 15 minutes
Permissions: contents: write, issues: write

Steps:
1. Checkout (with full history)
2. Extract tag name
3. Determine if prerelease
4. Build release artifacts
   - Plugin tarball
   - Docs tarball
   - SHA256 checksums
5. Generate changelog
   - Uses release-changelog-config.json
   - Groups by label categories
6. Create GitHub release
   - Attach artifacts
   - Include changelog
   - Mark prerelease if applicable
7. Create notification issue

Dependencies: None
```

**Performance**:
- Total time: ~3 minutes
- Artifact creation: ~1 minute
- Changelog generation: ~30 seconds
- Release upload: ~1 minute

### Workflow: Security

**File**: `.github/workflows/security.yml`

**Trigger Events**:
- `push` (main branch)
- `pull_request`
- `schedule` (weekly, Sundays)
- `workflow_dispatch`

**Jobs Breakdown**:

#### Job: codeql
```yaml
Runner: ubuntu-latest
Timeout: 30 minutes
Permissions: contents: read, security-events: write

Steps:
1. Checkout
2. Initialize CodeQL (Python)
   - Uses security-extended queries
3. Autobuild
4. Perform CodeQL analysis
5. Upload SARIF

Dependencies: None (runs in parallel)
```

#### Job: dependency-review
```yaml
Runner: ubuntu-latest
Timeout: 10 minutes
Permissions: contents: read

Steps:
1. Checkout
2. Run dependency review
   - Fails on moderate+ severity
   - Checks licenses

Dependencies: None (runs in parallel)
Condition: Pull requests only
```

#### Job: trivy
```yaml
Runner: ubuntu-latest
Timeout: 15 minutes
Permissions: contents: read, security-events: write

Steps:
1. Checkout
2. Run Trivy filesystem scan
3. Upload SARIF

Dependencies: None (runs in parallel)
```

#### Job: bandit
```yaml
Runner: ubuntu-latest
Timeout: 10 minutes
Permissions: contents: read, security-events: write

Steps:
1. Checkout
2. Set up Python 3.12
3. Install Bandit
4. Run Bandit scan
5. Upload SARIF

Dependencies: None (runs in parallel)
```

**Performance**:
- Total time: ~10 minutes
- CodeQL: ~5 minutes
- Trivy: ~3 minutes
- Bandit: ~2 minutes
- Parallelization: 4 jobs concurrent (PR), 3 jobs (push)

## Integration Points

### GitHub API Integration

**Used by**:
- PR comments (all review workflows)
- Label management (pr-labeler)
- Release creation (release workflow)
- Issue creation (release workflow)

**Rate Limits**:
- 1000 requests/hour per workflow
- Uses `GITHUB_TOKEN` (auto-generated)

### External Services

#### Codecov
**Purpose**: Enhanced coverage reporting
**Integration**: Optional, via `CODECOV_TOKEN`
**Data Flow**: XML report → Codecov API → PR comment

#### Trivy
**Purpose**: Vulnerability scanning
**Integration**: Public Trivy database
**Data Flow**: File scan → Trivy DB → SARIF output

#### CodeQL
**Purpose**: Semantic code analysis
**Integration**: GitHub's CodeQL service
**Data Flow**: Code → CodeQL engine → Security alerts

### Artifact Storage

**GitHub Artifacts**:
- Complexity reports
- Coverage HTML reports
- Release packages

**Retention**: 90 days default

**Size Limits**: 500 MB per artifact

### Security Tab Integration

**SARIF Upload**:
- CodeQL results
- Trivy results
- Bandit results

**View**: Security → Code scanning alerts

## Performance Characteristics

### Execution Times

| Workflow | Min | Avg | Max | Parallelization |
|----------|-----|-----|-----|-----------------|
| PR Labeler | 20s | 30s | 1m | No parallelization |
| Code Review | 3m | 5m | 8m | 3 parallel jobs |
| Coverage | 2m | 4m | 10m | No parallelization |
| Release | 2m | 3m | 5m | No parallelization |
| Security | 5m | 10m | 30m | 4 parallel jobs |

### Resource Usage

**Compute**:
- Runner: ubuntu-latest (2-core CPU, 7 GB RAM)
- Python setup: ~30 seconds
- Dependency installation: ~1-2 minutes

**Storage**:
- Artifacts per PR: ~5 MB
- Release artifacts: ~50 MB
- Monthly usage: ~500 MB

**API Calls**:
- Per PR: ~10-15 API calls
- Per release: ~5 API calls
- Well within rate limits

### Optimization Strategies

1. **Caching**: Pip cache for dependencies
2. **Parallelization**: Independent jobs run concurrently
3. **Conditional execution**: Skip unnecessary steps
4. **Concurrency groups**: Cancel outdated runs
5. **continue-on-error**: Don't block on non-critical failures

## Extensibility

### Adding New Workflows

**Template**:
```yaml
name: Custom Workflow

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

concurrency:
  group: custom-${{ github.ref }}
  cancel-in-progress: true

jobs:
  custom-job:
    name: Custom Job
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Custom action
        run: echo "Custom workflow"
```

### Adding New Jobs to Existing Workflows

**Example**: Add linting to code review
```yaml
lint:
  name: Review / Linting
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - name: Install linters
      run: pip install black isort flake8
    - name: Run black
      run: black --check rag-pipeline/
    - name: Run isort
      run: isort --check rag-pipeline/
    - name: Run flake8
      run: flake8 rag-pipeline/
```

### Adding New Security Tools

**Example**: Add ShellCheck for shell scripts
```yaml
shellcheck:
  name: ShellCheck
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run ShellCheck
      uses: ludeeus/action-shellcheck@master
      with:
        format: sarif
        output: shellcheck.sarif
    - name: Upload results
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: shellcheck.sarif
        category: shellcheck
```

### Custom Actions

**Create reusable actions**:
```yaml
# .github/actions/custom-check/action.yml
name: 'Custom Check'
description: 'Performs custom validation'
inputs:
  path:
    description: 'Path to check'
    required: true
runs:
  using: 'composite'
  steps:
    - name: Run check
      shell: bash
      run: |
        echo "Checking ${{ inputs.path }}"
```

**Use in workflow**:
```yaml
- name: Custom check
  uses: ./.github/actions/custom-check
  with:
    path: 'rag-pipeline/'
```

## Data Flow Diagrams

### Code Review Data Flow

```
PR Created
    ↓
[GitHub Event] → [Workflow Trigger]
    ↓
[Checkout Code] → [Repository Files]
    ↓
[Parallel Execution]
    ├─→ [Radon] → [Complexity Metrics] → [Markdown Report]
    ├─→ [Bandit] → [Security Issues] → [SARIF + Markdown]
    └─→ [Git Diff] → [Change Stats] → [Impact Report]
    ↓
[Combine Reports]
    ↓
[GitHub API] → [PR Comment] → [Developer Notification]
```

### Release Data Flow

```
Git Tag Pushed (v*.*.*)
    ↓
[GitHub Event] → [Workflow Trigger]
    ↓
[Checkout Code] → [Full History]
    ↓
[Build Artifacts]
    ├─→ [Tar Plugin] → plugin.tar.gz
    ├─→ [Tar Docs] → docs.tar.gz
    └─→ [Calculate SHA256] → checksums.txt
    ↓
[Generate Changelog]
    ├─→ [Fetch PRs] → [GitHub API]
    ├─→ [Group by Labels] → [Categories]
    └─→ [Format Markdown] → changelog.md
    ↓
[Create Release]
    ├─→ [Attach Artifacts]
    ├─→ [Add Changelog]
    └─→ [Publish]
    ↓
[Create Issue] → [Team Notification]
```

## Advanced Topics

### Workflow Debugging

**Enable debug logging**:
```bash
# Set repository secrets
gh secret set ACTIONS_STEP_DEBUG --body "true"
gh secret set ACTIONS_RUNNER_DEBUG --body "true"
```

**Local testing with act**:
```bash
# Test pull request workflow
act pull_request -W .github/workflows/code-review.yml

# Test with specific event
act -e event.json
```

### Performance Monitoring

**Track workflow metrics**:
- Actions → Insights → Workflows
- Duration trends
- Success/failure rates
- Runner usage

### Dependency Management

**Dependabot configuration**:
- Weekly updates
- Grouped minor/patch updates
- Automatic labeling
- Security updates prioritized

### Security Hardening

**Best practices**:
- Pin action versions (not `@main`)
- Minimize permissions
- Use `secrets` not hardcoded values
- Enable branch protection
- Review Dependabot PRs

---

**Last Updated**: December 2024
**Version**: 1.0.0
