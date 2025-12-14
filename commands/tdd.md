---
description: Use for ALL new features, bug fixes, and refactoring. Enforces RED-GREEN-REFACTOR cycle.
---

# Test-Driven Development

## Iron Law
**"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"**

If code exists before its test, DELETE it and restart. No exceptions.

## The Cycle

### RED Phase
1. Write ONE minimal test demonstrating required behavior
2. Run test - confirm it FAILS (not errors)
3. Verify failure is for the RIGHT reason (missing feature, not syntax)

### GREEN Phase
1. Write SIMPLEST code to pass the test
2. No feature creep, no over-engineering
3. Run test - confirm it PASSES
4. Confirm ALL other tests still pass

### REFACTOR Phase (only after GREEN)
1. Eliminate duplication
2. Improve naming
3. Extract helpers if needed
4. Maintain test passage

## Verification Checklist
- [ ] Every function has an associated test
- [ ] Observed each test fail BEFORE implementation
- [ ] Failures occurred for correct reasons
- [ ] Implemented minimal passing code
- [ ] All tests pass with clean output
- [ ] Edge cases and error conditions covered

## Red Flags (STOP and restart)
- Code exists before tests
- Tests pass immediately upon writing
- "Just this once" rationalization
- "Tests can come later" thinking

$ARGUMENTS
