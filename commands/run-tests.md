---
description: Run project test suite with auto-detection of test framework.
---

# Run Project Tests

## Auto-Detection
Based on current directory, detect and run appropriate test command:

| Project | Command |
|---------|---------|
| CV-BOILER-PLATE-FORK | `.venv/bin/python -m pytest tests/ -v` |
| rugs-rl-bot | `.venv/bin/python -m pytest tests/ -v` |
| REPLAYER | `cd src && python -m pytest tests/ -v` |
| hyperliquid-data-system | `npm test` |

## Execution
1. Detect project from `pwd`
2. Activate virtual environment if needed
3. Run tests with verbose output
4. Report summary: PASSED/FAILED count, exit code

## Generic Detection
If project not in table above:
- Check for `pytest.ini` or `pyproject.toml` → run pytest
- Check for `package.json` with test script → run npm test
- Check for `Cargo.toml` → run cargo test
- Check for `go.mod` → run go test ./...

$ARGUMENTS
