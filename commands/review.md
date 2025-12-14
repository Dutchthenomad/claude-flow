---
description: Use after completing a task to get code review before proceeding.
---

# Code Review

## Review Scope
$ARGUMENTS

## Checklist

### Critical (Must Fix)
- [ ] Security vulnerabilities (injection, XSS, secrets in code)
- [ ] Data loss risks
- [ ] Breaking changes without migration
- [ ] Tests missing for new functionality

### Important (Should Fix)
- [ ] Type hint coverage on public functions
- [ ] Exception handling (no bare `except:`)
- [ ] Edge cases not covered
- [ ] Performance issues (N+1 queries, unnecessary loops)

### Minor (Nice to Have)
- [ ] Naming improvements
- [ ] Documentation gaps
- [ ] Code style inconsistencies

## Review Output Format
```
## Critical Issues
[List or "None found"]

## Important Issues
[List or "None found"]

## Minor Suggestions
[List or "None found"]

## Verdict
[ ] APPROVED - Ready to merge
[ ] CHANGES REQUESTED - Fix critical/important issues first
```
