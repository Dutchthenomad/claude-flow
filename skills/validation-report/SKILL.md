---
name: validation-report
description: Generate a validation report showing all cited sources organized by validation tier. Use when user asks for /validation-report or wants to understand source reliability.
allowed-tools: Read, Glob, Grep, Bash
---

# Validation Report Skill

Generate a comprehensive validation report showing all knowledge sources organized by validation tier.

## Trigger Conditions

Use this skill when:
- User requests `/validation-report`
- User asks "what sources did you use?"
- User questions the reliability of cited information
- User wants to understand which claims are verified vs theoretical

## Execution Protocol

### Step 1: Scan Strategy Knowledge Base

```bash
# Find all files with validation_tier in frontmatter
grep -r "validation_tier:" /home/nomad/Desktop/claude-flow/knowledge/rugs-strategy/ --include="*.md" -l
```

### Step 2: Extract Tiers

```bash
# For each file, extract the validation tier
for file in $(find /home/nomad/Desktop/claude-flow/knowledge/rugs-strategy -name "*.md" -type f); do
    tier=$(head -20 "$file" | grep "validation_tier:" | cut -d: -f2 | tr -d ' ')
    if [ -n "$tier" ]; then
        echo "$tier|$file"
    fi
done | sort
```

### Step 3: Categorize by Tier

Organize files into four categories:
1. **Canonical** - `validation_tier: canonical`
2. **Verified** - `validation_tier: verified`
3. **Reviewed** - `validation_tier: reviewed`
4. **Theoretical** - `validation_tier: theoretical`

### Step 4: Generate Report

Output format:

```markdown
## Validation Report

**Generated**: [timestamp]
**Knowledge Base**: rugs-strategy (L1-L7)

---

### Canonical Sources - Cite as Fact

| File | Domain | Key Claims |
|------|--------|------------|
| L1-game-mechanics/provably-fair.md | game-mechanics | RUG_PROB=0.005, DRIFT formula |
| L2-protocol/websocket-spec.md | protocol | Event schemas, field definitions |

---

### Verified Sources - Cite as Fact

| File | Domain | Key Claims |
|------|--------|------------|
| (none yet - requires 1000+ game validation) |

---

### Reviewed Sources - Mark with †

| File | Domain | Needs Validation |
|------|--------|------------------|
| L5-strategy-tactics/probability-framework.md | strategy | 50-70% probability claim needs 10K+ games |
| L7-advanced-analytics/prng-analysis.md | analytics | Trading zones, volatility spike claims |

---

### Theoretical Sources - Mark with *

| File | Domain | Status |
|------|--------|--------|
| L7-advanced-analytics/bayesian-models.md | research | Hypothesis only |
| L7-advanced-analytics/prng-reverse-engineering.md | research | No empirical validation |

---

### Usage Guidelines

- **Canonical/Verified**: Cite freely without markers
- **Reviewed (†)**: Human reviewed logic, awaiting empirical validation
- **Theoretical (*)**: Hypothesis or conjecture, may be speculation

### Next Steps for Validation

See: `_metadata/RUGOPEDIA_VALIDATION_PLAN.md` for the full validation workflow.
```

## Supporting Commands

### Quick Tier Check
```bash
# Check a specific file's tier
head -15 /home/nomad/Desktop/claude-flow/knowledge/rugs-strategy/L7-advanced-analytics/prng-analysis.md | grep validation_tier
```

### Count by Tier
```bash
# Count files by validation tier
for tier in canonical verified reviewed theoretical; do
    count=$(grep -r "validation_tier: $tier" /home/nomad/Desktop/claude-flow/knowledge/rugs-strategy/ --include="*.md" | wc -l)
    echo "$tier: $count files"
done
```

## Example Output

When user runs `/validation-report`:

```
## Validation Report

**Generated**: 2025-12-24

---

### Canonical (4 files)
- L1-game-mechanics/provably-fair.md
- L1-game-mechanics/game-phases.md
- L2-protocol/websocket-spec.md
- L2-protocol/field-dictionary.md

### Verified (0 files)
(None - validation pipeline pending)

### Reviewed (4 files)
- L5-strategy-tactics/probability-framework.md
- L5-strategy-tactics/bankroll-management.md
- L5-strategy-tactics/risk-hedging.md
- L7-advanced-analytics/prng-analysis.md

### Theoretical (3 files)
- L7-advanced-analytics/bayesian-models.md
- L7-advanced-analytics/prng-reverse-engineering.md
- L6-statistical-baselines/volatility-reference.md

---

**Citation Guide:**
- 4 files can be cited as fact
- 4 files require † marker
- 3 files require * marker
```

## Integration with rugs-expert Agent

The rugs-expert agent uses this skill when:
1. User explicitly requests `/validation-report`
2. Agent has cited multiple sources and wants to provide transparency
3. User questions the reliability of information

The agent's response footer (`**Validation Notes**`) is a mini version of this report, showing only the sources cited in that specific response.
