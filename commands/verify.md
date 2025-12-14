---
description: Use BEFORE claiming any task is complete. Evidence before claims, always.
---

# Verification Before Completion

## Core Principle
**"Evidence before claims, always."**

Run FRESH verification commands before asserting work is complete.

## The 5-Step Gate

1. **Identify** the proof command (test, build, lint, etc.)
2. **Execute** it fully (no partial runs)
3. **Read** complete output AND exit codes
4. **Confirm** output matches the claim
5. **State** result with evidence

## What DOESN'T Count as Verification
- Previous test runs ("it passed before")
- "Should pass" reasoning
- Partial checks or extrapolation
- Agent success reports without independent verification
- Code changes without testing original symptom

## What DOES Count
- Fresh command execution
- Exit code 0 confirmation
- 0 failures, 0 errors in output
- Red-green regression (fail → fix → pass cycle)

## Verification Commands by Project

**Python/pytest:**
```bash
pytest tests/ -v --tb=short
echo "Exit code: $?"
```

**Node.js:**
```bash
npm test
echo "Exit code: $?"
```

**Build verification:**
```bash
npm run build  # or python -m build
echo "Exit code: $?"
```

## Red Flags (DO NOT proceed)
- Using words: "should," "probably," "seems to"
- Feeling tired and wanting to be done
- Relying on partial evidence

$ARGUMENTS
