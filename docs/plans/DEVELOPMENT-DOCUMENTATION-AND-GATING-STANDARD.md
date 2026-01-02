# DEVELOPMENT DOCUMENTATION AND GATING STANDARD

**Date:** 2025-12-27
**Status:** IMPLEMENTATION REQUIRED
**Owner:** claude-flow Development Team
**Scope:** All projects using claude-flow orchestration (VECTRA-PLAYER, rugs-rl-bot, etc.)

---

## Executive Summary

This document defines the comprehensive standard for development documentation, requirements gating, and knowledge management across the claude-flow ecosystem. The goal is to establish a lightweight but rigorous system that:

1. Prevents scope creep and undocumented feature additions
2. Ensures all development work is properly tracked and gated
3. Maintains canonical knowledge bases that stay synchronized
4. Provides clear ownership and responsibility boundaries
5. Enables agile updates without circumventing quality controls

---

## Problem Statement

### Observed Failures

1. **Documentation Fragmentation:** Multiple "canonical" documents claiming authority, leading to conflicts
2. **Silent Circumvention:** Features added without updating plans, gates bypassed "temporarily"
3. **Status Drift:** Documentation says "complete" but production is broken
4. **Knowledge Silos:** Critical information trapped in session scratchpads, not propagated
5. **Gate Erosion:** Requirements gates weakened over time as "exceptions" accumulate

### Root Cause

No enforced system for:
- Document hierarchy and ownership
- Gate verification before phase completion
- Knowledge promotion workflows
- Plan update protocols when new work is identified

---

## Part 1: Document Hierarchy and Ownership

### 1.1 Three-Tier Document System

```
TIER 1: CANONICAL (Single Source of Truth)
├── Production Plans (per-project)
│   └── Example: VECTRA-PLAYER/docs/plans/GLOBAL-DEVELOPMENT-PLAN.md
└── Knowledge Bases (in claude-flow)
    └── Example: claude-flow/knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md

TIER 2: REFERENCE (Read-Only Historical)
├── Deprecated plans (in sandbox/DEVELOPMENT DEPRECATIONS/)
├── Completed phase specs
└── Resolved bug hunts

TIER 3: SESSION (Ephemeral Working State)
├── .claude/scratchpad.md (per-project)
├── GitHub Issues (active work)
└── PR descriptions
```

### 1.2 Ownership Matrix

| Document Type | Owner | Can Modify | Modification Requires |
|--------------|-------|------------|----------------------|
| GLOBAL-DEVELOPMENT-PLAN.md | Project Lead | Project Lead only | Phase gate verification |
| WEBSOCKET_EVENTS_SPEC.md | claude-flow team | Human approval | CANONICAL promotion workflow |
| Reference docs | Nobody | Archive only | Move to deprecation folder |
| Session scratchpad | Current session | Any session | None (ephemeral) |

### 1.3 Conflict Resolution

When documents conflict:
1. TIER 1 wins over TIER 2
2. Within TIER 1: Production plan wins for implementation, Knowledge base wins for protocol facts
3. Session state is NEVER authoritative beyond current session

---

## Part 2: Requirements Gating System

### 2.1 Gate Definition

A **Gate** is a set of verifiable conditions that MUST be met before proceeding to the next phase.

```yaml
gate:
  name: "Pipeline B: ButtonEvent Implementation"
  prerequisites:
    - "Pipeline A gate passed"
  verification:
    automated:
      - command: "python -m pytest tests/ -v"
        expect: "all tests pass"
      - command: "python -c 'check_button_events()'"
        expect: "tick > 0, price != 1.0, game_id != 'unknown'"
    manual:
      - "Run ./run.sh and click buttons during ACTIVE game"
      - "Verify Parquet files contain real game context"
  gate_criteria:
    - "All automated checks pass"
    - "Manual verification completed by human"
    - "Results logged in GLOBAL-DEVELOPMENT-PLAN.md"
```

### 2.2 Gate Enforcement Protocol

```
BEFORE claiming phase complete:
1. Run ALL automated verification checks
2. Complete ALL manual verification steps
3. Document results in GLOBAL-DEVELOPMENT-PLAN.md
4. Update phase status with verification date
5. ONLY THEN proceed to next phase

VIOLATION: Claiming complete without verification = PHASE REVERTED
```

### 2.3 Gate Status Indicators

| Status | Symbol | Meaning |
|--------|--------|---------|
| BLOCKED | ⏳ | Prerequisites not met |
| IN_PROGRESS | 🔄 | Work started, gate not passed |
| READY_FOR_VERIFICATION | ⚠️ | Code complete, verification pending |
| VERIFIED | ✅ | Gate passed with documented evidence |

### 2.4 Gate Bypass Prevention

**NEVER ALLOWED:**
- Marking phase complete without running verification
- Proceeding to dependent phase while predecessor is not VERIFIED
- Adding features not in the current phase plan

**EXCEPTION PROCESS:**
If a bypass is truly necessary:
1. Document WHY in GLOBAL-DEVELOPMENT-PLAN.md
2. Create GitHub Issue for the bypass
3. Add to "Technical Debt" section
4. Schedule remediation in next sprint

---

## Part 3: Knowledge Canonicalization System

### 3.1 Canonical Promotion Workflow

```
THEORETICAL → OBSERVED → VERIFIED → CANONICAL
     ↓            ↓           ↓           ↓
  (claimed)   (captured)  (validated) (HUMAN APPROVES)
    auto         auto        auto      HUMAN GATE
```

### 3.2 Promotion Requirements

| Status | Requirements |
|--------|--------------|
| THEORETICAL | Claimed to exist (documentation, hearsay) |
| OBSERVED | Raw capture evidence (file:line reference) |
| VERIFIED | Multiple captures, type validated, examples real |
| CANONICAL | Human explicitly approves, added to spec |

### 3.3 Knowledge Base Update Protocol

```python
# CORRECT: Proper canonicalization
def promote_to_canonical(field: str, evidence: dict) -> bool:
    """
    1. Present evidence to human
    2. Wait for explicit "approved" response
    3. Only then modify WEBSOCKET_EVENTS_SPEC.md
    4. Log promotion with date, evidence, authorization
    """
    pass

# WRONG: Silent modification
def wrong_approach(field: str):
    """
    NEVER directly modify canonical spec without human approval.
    This is a SYSTEM FAILURE.
    """
    raise PermissionError("Human approval required")
```

### 3.4 RAG Ingestion Standards

| Source | Ingestion Target | Metadata Required |
|--------|-----------------|-------------------|
| WEBSOCKET_EVENTS_SPEC.md | ChromaDB: rugs_events | scope, priority, phase |
| Codebase docs | ChromaDB: vectra_codebase | component, layer |
| Session learnings | MUST BE PROMOTED FIRST | Cannot ingest ephemeral data |

---

## Part 4: Agile Plan Update Protocol

### 4.1 When New Work is Identified

During development, new work is often discovered. This MUST be handled properly:

```
NEW WORK IDENTIFIED:
1. STOP current task
2. Document finding in session scratchpad
3. Determine scope:
   - Bug in current phase? → Fix now, document
   - New requirement? → Create GitHub Issue
   - Architecture change? → Requires plan update
4. If plan update needed:
   - Update GLOBAL-DEVELOPMENT-PLAN.md FIRST
   - Add new gate if appropriate
   - Then continue work
5. NEVER silently add work without documentation
```

### 4.2 Plan Update Checklist

When modifying GLOBAL-DEVELOPMENT-PLAN.md:

```markdown
- [ ] Is this change necessary? (not just nice-to-have)
- [ ] Does it affect existing gates? (if yes, update them)
- [ ] Does it add new phases? (if yes, define gates)
- [ ] Is the change tracked? (GitHub Issue or commit message)
- [ ] Is the modification date updated?
- [ ] Are dependent phases updated if affected?
```

### 4.3 Lightweight Update vs Full Revision

| Change Type | Action | Approval |
|-------------|--------|----------|
| Status update (phase complete) | Update inline | Self-approved with evidence |
| Bug fix within phase | Add to phase notes | Self-approved |
| New task within phase | Add to phase checklist | Self-approved |
| New phase or gate | Add new section | Requires discussion |
| Architecture change | Full revision | Requires explicit approval |

---

## Part 5: Anti-Circumvention Measures

### 5.1 Common Circumvention Patterns

| Pattern | How to Detect | Prevention |
|---------|--------------|------------|
| "I'll document it later" | Missing gate evidence | Gate verification is BLOCKING |
| "It's just a small fix" | Untracked commits | All work needs issue/phase reference |
| "The tests pass so it's fine" | No manual verification | Manual verification is REQUIRED |
| "We can skip this gate" | Gate bypassed | No gate bypass without exception process |
| "I remember the spec" | Knowledge not in canonical source | Must reference canonical docs |

### 5.2 Session Start Protocol

Every new session MUST:

```bash
# 1. Read the canonical plan
cat PROJECT/docs/plans/GLOBAL-DEVELOPMENT-PLAN.md

# 2. Check current phase status
# (Look for ⚠️ READY_FOR_VERIFICATION or 🔄 IN_PROGRESS)

# 3. Resume from documented state
# (Not from memory or scratchpad claims)

# 4. Verify any "complete" claims from previous session
# (If previous session claimed complete but no evidence, REVERT)
```

### 5.3 Session End Protocol

Before ending session:

```markdown
- [ ] All work documented in appropriate tier
- [ ] Phase status updated in GLOBAL-DEVELOPMENT-PLAN.md
- [ ] Any new findings added to scratchpad OR escalated to plan
- [ ] No orphan work (everything tracked)
- [ ] Next actions clearly stated
```

### 5.4 Audit Trail Requirements

All phase transitions must include:

```yaml
phase_transition:
  from: "Pipeline A"
  to: "Pipeline B"
  date: "2025-12-27"
  evidence:
    automated: "1138 tests passed"
    manual: "Clicked buttons during ACTIVE game, verified Parquet"
  verified_by: "Human + automated checks"
  documented_in: "GLOBAL-DEVELOPMENT-PLAN.md line 145"
```

---

## Part 6: Implementation Checklist

### 6.1 For claude-flow Team

- [ ] Create CANONICAL_PROMOTION_LOG.md in knowledge/rugs-events/
- [ ] Add gate verification scripts to commands/
- [ ] Create session-start hook that reads canonical plan
- [ ] Create session-end hook that validates documentation
- [ ] Update rugs-expert agent to enforce canonicalization
- [ ] Add RAG ingestion pipeline for verified knowledge only

### 6.2 For Project Teams (VECTRA-PLAYER, etc.)

- [ ] Maintain single GLOBAL-DEVELOPMENT-PLAN.md
- [ ] Move all superseded docs to deprecation folder
- [ ] Add gate verification commands to project
- [ ] Reference claude-flow commands for workflow
- [ ] Update scratchpad at session end

### 6.3 Validation Criteria

This system is working when:

1. **No orphan work:** Every commit traces to a phase/issue
2. **No status drift:** Claimed status matches reality
3. **No knowledge silos:** All learnings in canonical sources
4. **No gate bypasses:** All phases have verification evidence
5. **No documentation conflicts:** Single source of truth is clear

---

## Part 7: Quick Reference

### Document Locations

| Type | Location | Purpose |
|------|----------|---------|
| Production Plan | `PROJECT/docs/plans/GLOBAL-DEVELOPMENT-PLAN.md` | Single source of truth for development |
| Knowledge Base | `claude-flow/knowledge/*/` | Canonical protocol/domain knowledge |
| Session State | `PROJECT/.claude/scratchpad.md` | Ephemeral session context |
| Deprecated | `PROJECT/sandbox/DEVELOPMENT DEPRECATIONS/` | Historical reference only |

### Workflow Commands

```bash
/plan          # Enter planning mode (use for significant changes)
/verify        # Run gate verification before claiming complete
/tdd           # Enforce test-first development
/worktree      # Create isolated workspace for feature
```

### Gate Status Quick Check

```python
# Check if phase is truly complete
def is_phase_complete(phase_name: str) -> bool:
    """
    Phase is complete ONLY IF:
    1. All automated checks pass
    2. Manual verification documented
    3. Status is ✅ VERIFIED in GLOBAL-DEVELOPMENT-PLAN.md
    4. Date and evidence recorded
    """
    pass
```

---

## Appendix A: Example Gate Definition

```yaml
# Example from VECTRA-PLAYER
gate:
  name: "Pipeline B: ButtonEvent Implementation"
  phase: "FEATURES"

  prerequisites:
    - phase: "Pipeline A"
      status: "✅ VERIFIED"

  deliverables:
    - "ButtonEvent dataclass in src/models/events/button_event.py"
    - "BUTTON_PRESS event in EventBus"
    - "BUTTON_EVENT doc_type in EventStore"
    - "TradingController emits ButtonEvents"

  automated_checks:
    - command: "python -m pytest tests/ -v"
      expect: "all pass"
    - command: |
        python -c "
        import duckdb, json
        result = duckdb.query('''
            SELECT raw_json FROM read_parquet(
                '~/rugs_data/events_parquet/doc_type=button_event/**/*.parquet'
            ) ORDER BY ts DESC LIMIT 1
        ''').fetchone()
        d = json.loads(result[0])
        assert d['tick'] > 0
        assert d['price'] != 1.0
        assert d['game_id'] != 'unknown'
        print('GATE PASSED')
        "
      expect: "GATE PASSED"

  manual_checks:
    - "Run ./run.sh"
    - "Wait for browser connection"
    - "Click buttons during ACTIVE game"
    - "Verify ButtonEvents captured with real game context"

  gate_passed:
    date: null  # Set when verified
    evidence: null  # Document verification results
    verified_by: null  # Human + automated
```

---

## Appendix B: Anti-Pattern Examples

### BAD: Undocumented Phase Completion

```markdown
# WRONG - No evidence, just claim
| Pipeline B | ButtonEvent Implementation | ✅ COMPLETE |
```

### GOOD: Documented Phase Completion

```markdown
# CORRECT - Evidence and date
| Pipeline B | ButtonEvent Implementation | ✅ VERIFIED (2025-12-27) |

**Pipeline B Evidence:**
- Automated: 1138 tests pass
- Manual: Clicked BUY during ACTIVE game, verified Parquet:
  - tick=145, price=2.34, game_id=abc123
- Verified by: Session 2025-12-27
```

### BAD: Silent Feature Addition

```python
# WRONG - Feature not in plan, no issue, no gate
def new_cool_feature():
    pass  # Just added it
```

### GOOD: Tracked Feature Addition

```python
# CORRECT - Issue created, plan updated, gate defined
# GitHub Issue #42: Add cool feature
# Added to GLOBAL-DEVELOPMENT-PLAN.md Pipeline C
# Gate: Must pass feature_tests.py
def new_cool_feature():
    pass
```

---

## Summary

This standard ensures:

1. **Single Source of Truth:** GLOBAL-DEVELOPMENT-PLAN.md per project
2. **Verified Gates:** No phase complete without evidence
3. **Canonical Knowledge:** Human-approved promotions only
4. **Agile Updates:** Lightweight protocol for adding work
5. **Anti-Circumvention:** Hooks and audits prevent drift

**Implementation Owner:** claude-flow Development Team
**Enforcement:** All projects using claude-flow orchestration

---

*This document defines the development documentation and gating standard for the claude-flow ecosystem.*
*Implementation should begin immediately in a dedicated session.*
