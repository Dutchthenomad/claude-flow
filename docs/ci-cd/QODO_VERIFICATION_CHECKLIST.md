# Qodo Integration Verification Checklist

This checklist helps verify the Qodo integration is working correctly and has no conflicts.

## Pre-Merge Verification

### Configuration Validation ✅
- [x] `.qodo_merge.toml` has valid TOML syntax
- [x] `.github/workflows/qodo-review.yml` has valid YAML syntax
- [x] `.github/workflows/code-review.yml` modifications are valid
- [x] All workflow permissions are appropriate

### Documentation Completeness ✅
- [x] README.md mentions Qodo integration
- [x] CI/CD Guide includes Qodo workflow section
- [x] Setup Guide includes Qodo configuration
- [x] Quick Reference includes Qodo commands
- [x] Standalone Qodo Integration Guide created
- [x] Implementation Summary document created

### Conflict Resolution ✅
- [x] Duplicate Trivy scan removed from code-review.yml
- [x] Concurrency groups configured for all workflows
- [x] Comment spam prevention configured in Qodo
- [x] Workflow timing documented

## Post-Merge Testing

### Workflow Activation
- [ ] **Check workflow is visible**
  ```bash
  gh workflow list | grep -i qodo
  # Should show: Qodo AI Code Review
  ```

- [ ] **Verify workflow is enabled**
  ```bash
  gh workflow view qodo-review.yml
  # Should show: state: enabled
  ```

### Test PR Scenarios

#### Scenario 1: Qodo Not Configured (Default)
**Expected**: Workflow skips or fails gracefully with helpful message

1. Create test PR without API key configured
   ```bash
   git checkout -b test/qodo-no-config
   echo "# Test" > TEST.md
   git add TEST.md
   git commit -m "test: verify Qodo behavior without config"
   git push origin test/qodo-no-config
   gh pr create --title "test: Qodo without config"
   ```

2. Check workflow result:
   ```bash
   gh run list --workflow=qodo-review.yml --limit 1
   # Should show: completed with failure
   ```

3. Verify failure notification:
   ```bash
   gh pr view <pr-number> --comments
   # Should see: "Qodo AI Review Failed" comment with setup instructions
   ```

4. Clean up:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/qodo-no-config
   ```

✅ **Pass Criteria**: Workflow fails gracefully, posts helpful comment

---

#### Scenario 2: Qodo Configured (If API Key Added)
**Expected**: AI review completes successfully

1. Add API key to repository secrets:
   ```bash
   gh secret set OPENAI_KEY
   # Or: gh secret set ANTHROPIC_API_KEY
   ```

2. Create test PR:
   ```bash
   git checkout -b test/qodo-with-config
   echo "def hello():\n    print('world')" > test.py
   git add test.py
   git commit -m "test: verify Qodo with config"
   git push origin test/qodo-with-config
   gh pr create --title "test: Qodo with API key"
   ```

3. Monitor workflow:
   ```bash
   gh run watch
   # Wait for completion (~2-3 minutes)
   ```

4. Verify AI review:
   ```bash
   gh pr view <pr-number> --comments
   # Should see: AI-generated review comments
   ```

5. Test interactive commands:
   ```bash
   gh pr comment <pr-number> --body "/review"
   # Wait ~1 minute
   gh pr view <pr-number> --comments
   # Should see: Updated AI review
   ```

6. Clean up:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/qodo-with-config
   ```

✅ **Pass Criteria**: AI review appears, interactive commands work

---

### Security Scan Deduplication

**Check for single Trivy scan per PR**:

1. Create test PR:
   ```bash
   git checkout -b test/security-dedupe
   echo "# Security Test" > SECURITY_TEST.md
   git add SECURITY_TEST.md
   git commit -m "test: verify single Trivy scan"
   git push origin test/security-dedupe
   gh pr create --title "test: security deduplication"
   ```

2. Wait for workflows to complete (~5 minutes)

3. Check Security tab:
   ```bash
   gh api repos/Dutchthenomad/claude-flow/code-scanning/alerts \
     | jq '[.[] | select(.tool.name == "Trivy")] | length'
   # Should be: 1 (not 2)
   ```

4. Verify workflow runs:
   ```bash
   gh run list --workflow=security.yml --limit 1
   # Should show: Trivy ran once
   
   gh run list --workflow=code-review.yml --limit 1
   # Should show: No Trivy step
   ```

5. Clean up:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/security-dedupe
   ```

✅ **Pass Criteria**: Only one Trivy scan per PR

---

### Comment Count Verification

**Check PR doesn't have excessive comments**:

1. Create realistic test PR:
   ```bash
   git checkout -b test/comment-count
   echo "def complex_function():\n    x = 1\n    y = 2\n    return x + y" > complex.py
   git add complex.py
   git commit -m "feat: add complex function"
   git push origin test/comment-count
   gh pr create --title "feat: add complex function"
   ```

2. Wait for all workflows to complete

3. Count comments:
   ```bash
   gh pr view <pr-number> --comments | grep -c "^#"
   # Should be: 5-7 total
   # Breakdown:
   # - PR description: 1
   # - PR labels (not a comment): 0
   # - Qodo review (if configured): 1-2
   # - Code review (complexity): 1
   # - Code review (security): 1
   # - Code review (impact): 1
   # - Code review (summary): 1
   # - Coverage (if applicable): 1
   ```

4. Verify inline suggestions (if Qodo configured):
   ```bash
   gh pr view <pr-number> --web
   # Check: Inline comments appear contextually, not as separate top-level comments
   ```

5. Clean up:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/comment-count
   ```

✅ **Pass Criteria**: 5-7 comments total, inline suggestions are contextual

---

### Workflow Timing

**Verify parallel execution and reasonable timing**:

1. Create test PR:
   ```bash
   git checkout -b test/timing
   echo "# Timing Test" > TIMING.md
   git add TIMING.md
   git commit -m "test: verify workflow timing"
   git push origin test/timing
   gh pr create --title "test: workflow timing"
   ```

2. Monitor workflow execution:
   ```bash
   gh run list --limit 5 --json name,status,conclusion,startedAt,completedAt
   ```

3. Check timing expectations:
   - **Qodo**: ~2-3 minutes (if configured)
   - **Code Review**: ~5 minutes
   - **PR Labeler**: ~30 seconds
   - **Coverage**: ~4 minutes
   - **Total (parallel)**: ~5 minutes max

4. Verify no workflow blocking:
   ```bash
   # All workflows should start within 30 seconds of each other
   gh run list --limit 5 --json name,startedAt | jq
   ```

5. Clean up:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/timing
   ```

✅ **Pass Criteria**: Workflows run in parallel, complete within 5-6 minutes

---

### Concurrency Group Testing

**Verify no race conditions**:

1. Create test PR:
   ```bash
   git checkout -b test/concurrency
   echo "# Test 1" > TEST1.md
   git add TEST1.md
   git commit -m "test: concurrency test 1"
   git push origin test/concurrency
   gh pr create --title "test: concurrency"
   ```

2. Immediately push another commit:
   ```bash
   echo "# Test 2" > TEST2.md
   git add TEST2.md
   git commit -m "test: concurrency test 2"
   git push origin test/concurrency
   ```

3. Check workflow cancellation:
   ```bash
   gh run list --workflow=qodo-review.yml --limit 2
   # Should show: First run cancelled, second run running/completed
   ```

4. Verify no duplicate comments:
   ```bash
   gh pr view <pr-number> --comments | grep -c "Code Review"
   # Should be: 1 (not 2)
   ```

5. Clean up:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/concurrency
   ```

✅ **Pass Criteria**: Old runs cancelled, no duplicate comments

---

## Performance Validation

### CI/CD Resource Usage

Check that integration doesn't significantly increase resource usage:

```bash
# Compare average workflow duration before/after
gh run list --workflow=code-review.yml --limit 10 --json conclusion,startedAt,completedAt
# Calculate average duration

# Check for increased failure rates
gh run list --limit 50 --json conclusion | jq '[.[] | select(.conclusion == "failure")] | length'
# Should be: Low (<10%)
```

✅ **Pass Criteria**: Similar resource usage, no increased failures

---

## Rollback Verification

### Test Rollback Procedure

If any issues occur, verify rollback works:

1. **Create rollback commit**:
   ```bash
   git revert HEAD~1  # Revert Qodo integration
   git push origin copilot/review-qodo-integration-workflow
   ```

2. **Verify workflows still work**:
   ```bash
   # Create test PR
   git checkout -b test/rollback
   echo "# Rollback Test" > ROLLBACK.md
   git add ROLLBACK.md
   git commit -m "test: verify rollback"
   git push origin test/rollback
   gh pr create --title "test: post-rollback"
   ```

3. **Check existing workflows**:
   ```bash
   gh run list --workflow=code-review.yml --limit 1
   # Should show: Success
   ```

4. **Clean up**:
   ```bash
   gh pr close <pr-number>
   git checkout main
   git branch -D test/rollback
   ```

✅ **Pass Criteria**: Existing workflows unaffected by rollback

---

## Production Monitoring

### First Week Monitoring

After merge, monitor these metrics:

1. **Workflow Success Rate**:
   ```bash
   gh run list --workflow=qodo-review.yml --limit 20 --json conclusion
   # Track: Success rate should be >90%
   ```

2. **Developer Feedback**:
   - Survey team about Qodo suggestion quality
   - Check if suggestions are being addressed
   - Monitor for complaints about comment spam

3. **Cost Tracking** (if using API):
   - Monitor API usage in OpenAI/Anthropic dashboard
   - Compare against expected $0.01-0.08 per review
   - Adjust model or configuration if costs exceed budget

4. **Security Tab Health**:
   ```bash
   gh api repos/Dutchthenomad/claude-flow/code-scanning/alerts
   # Verify: No duplicate alerts, clean organization
   ```

---

## Issue Reporting

If problems occur, gather this information:

```bash
# Workflow run details
gh run view <run-id> --log > workflow.log

# PR details
gh pr view <pr-number> --json number,title,state,comments > pr.json

# Workflow configuration
cat .github/workflows/qodo-review.yml
cat .qodo_merge.toml

# Recent changes
git log --oneline -10

# Create issue with:
# - Problem description
# - workflow.log
# - pr.json
# - Configuration files
# - Steps to reproduce
```

---

## Success Criteria Summary

Integration is successful when:

- ✅ All workflows run without errors (or fail gracefully)
- ✅ No duplicate security scans in Security tab
- ✅ PR comment count remains reasonable (5-7)
- ✅ Workflows complete in parallel (~5 min total)
- ✅ No race conditions or conflicting updates
- ✅ Documentation is complete and accurate
- ✅ Developer feedback is positive
- ✅ Costs are within expected range

---

**Last Updated**: 2025-12-17  
**Status**: Ready for testing  
**Owner**: @Dutchthenomad
