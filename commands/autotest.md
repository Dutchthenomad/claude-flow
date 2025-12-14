---
description: Quick test runner - run pytest and analyze results without permission prompts
---

# Autotest Protocol

Run the project's test suite and analyze the output.

## Steps:

### 1. Identify Test Command
Check CLAUDE.md or use common patterns:
- Python: `pytest tests/ -v --tb=short`
- REPLAYER: `cd src && python3 -m pytest tests/ -v`
- With venv: `.venv/bin/python -m pytest tests/ -v`

### 2. Run Tests
Execute the test command. Do NOT ask for permission.

### 3. Analyze Output

**If ALL PASS:**
```
✅ All tests passing ([count] tests)
Ready for: [next SDLC phase]
```

**If FAILURES:**
```
❌ [count] tests failed

## Failures:
- test_name: [brief reason]

## Suggested Actions:
1. [action 1]
2. [action 2]
```

### 4. Update Scratchpad
Record test results in scratchpad if significant.

## Common Issues:
- Missing dependencies: Check venv activation
- Import errors: Check PYTHONPATH or run from correct directory
- Fixture errors: Check conftest.py

$ARGUMENTS
