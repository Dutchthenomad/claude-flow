---
name: CI/CD Troubleshooting
about: Report issues with workflows, automation, or CI/CD pipeline
title: '[CI/CD] '
labels: ['type: ci/cd', 'area: ci/cd']
assignees: ''
---

## Issue Description
<!-- Describe the CI/CD issue you're experiencing -->



## Workflow Affected
<!-- Which workflow is having issues? -->

- [ ] Automated Code Review (`code-review.yml`)
- [ ] PR Labeler (`pr-labeler.yml`)
- [ ] Test Coverage (`coverage.yml`)
- [ ] Automated Release (`release.yml`)
- [ ] Security Scanning (`security.yml`)
- [ ] Other: 

## Event Trigger
<!-- What triggered the workflow? -->

- [ ] Pull Request (opened/synchronized/reopened)
- [ ] Push to main branch
- [ ] Tag creation
- [ ] Manual workflow dispatch
- [ ] Scheduled run
- [ ] Other: 

## Failure Details
<!-- Provide details about the failure -->

### Workflow Run URL
<!-- Link to the failed workflow run -->



### Error Messages
<!-- Paste relevant error messages -->

```
<!-- Error messages here -->
```

### Failed Step
<!-- Which step in the workflow failed? -->



## Expected Behavior
<!-- What should have happened? -->



## Actual Behavior
<!-- What actually happened? -->



## Recent Changes
<!-- Were there any recent changes that might have caused this? -->

- [ ] Workflow file changes
- [ ] Dependency updates
- [ ] Configuration changes
- [ ] Repository settings changes
- [ ] GitHub Actions changes
- [ ] No recent changes

## Environment
<!-- Information about the environment -->

- Runner: [e.g., ubuntu-latest, self-hosted]
- Branch: [e.g., main, feature-branch]
- PR Number (if applicable): 

## Logs
<!-- Attach or paste relevant logs -->

<details>
<summary>Full Logs</summary>

```
<!-- Paste logs here -->
```

</details>

## Attempted Solutions
<!-- Have you tried any fixes? What happened? -->

1. 
2. 
3. 

## Impact
<!-- How is this affecting development/releases? -->

- [ ] Blocking PRs from being merged
- [ ] Preventing releases
- [ ] Causing false positives
- [ ] Slowing down workflow execution
- [ ] Other: 

## Additional Context
<!-- Any other relevant information -->



---

**Priority**: Low / Medium / High / Critical
**Blocking**: Yes / No
