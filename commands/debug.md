---
description: Use for ALL technical failures. 4-phase root cause analysis before ANY fix attempts.
---

# Systematic Debugging

## Iron Law
**"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"**

Attempting to fix symptoms without understanding causes wastes time and creates new problems.

## Phase 1: Root Cause Investigation
1. Read error messages and stack traces CAREFULLY
2. Reproduce the issue consistently
3. Examine recent changes via `git diff` and `git log`
4. Add diagnostic logging at component boundaries
5. Trace data flow through the system

**Output:** "The failure occurs at [location] because [specific reason]"

## Phase 2: Pattern Analysis
1. Find WORKING examples in the codebase
2. Study reference implementations completely
3. Compare differences between working and broken code
4. Map dependencies and assumptions

**Output:** "Working code does X, broken code does Y, the difference is Z"

## Phase 3: Hypothesis Testing
1. Form SPECIFIC hypothesis: "I think X causes Y because Z"
2. Test with MINIMAL changes (one thing at a time)
3. If fix fails, REVERT before trying another

**Critical:** After 3 failed attempts, STOP. Question if the architecture is fundamentally flawed.

## Phase 4: Implementation
1. Write a FAILING test that reproduces the bug
2. Implement SINGLE fix addressing root cause
3. Verify test now passes
4. Verify all other tests still pass

## Red Flags (STOP immediately)
- Proposing fixes before understanding the issue
- Making multiple simultaneous changes
- Third fix attempt failed → architecture review needed

$ARGUMENTS
