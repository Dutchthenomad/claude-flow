# Rugopedia Volume 1: Validation Workflow

**Status:** Planning | **Date:** 2025-12-24 | **Target:** Q1 2025

---

## Problem Statement

The rugs-expert agent currently cites `reviewed` and `theoretical` tier content as verified fact. This creates misinformation risk, particularly for:
- PRNG analysis claims (theoretical)
- Meta-algorithm hypotheses (unproven)
- Probability frameworks (derived, not empirically validated)

---

## Validation Tier Definitions

| Tier | Symbol | Meaning | Agent Behavior |
|------|--------|---------|----------------|
| `canonical` | ✓ | Verified against live protocol | Cite as fact |
| `verified` | ✓ | Validated against empirical data | Cite as fact |
| `reviewed` | † | Human reviewed, not validated | Mark with † |
| `theoretical` | * | Requires validation | Mark with * |

---

## Citation Discipline System

### Inline Notation (Minimal)
- **Verified content**: No marker needed
- **Reviewed content**: Append `†` to claim
- **Theoretical content**: Append `*` to claim

**Example Output:**
```
The rug probability is 0.5% per tick (RUG_PROB = 0.005).
Volatility increases ~78% in final 5 ticks before rug.*

† Reviewed but not empirically validated
* Theoretical - requires validation against recorded data
```

### Citation Footer
When unverified content is cited, append a footer:

```
---
**Validation Notes:**
- † 1 reviewed claim (L5-strategy-tactics/probability-framework.md)
- * 2 theoretical claims (L7-advanced-analytics/prng-analysis.md)
Use `/validation-report` for detailed source analysis.
```

### Validation Report Command
On request, generate detailed report:

```
## Validation Report

### Canonical (✓) - 3 sources
- L1-game-mechanics/provably-fair.md: RUG_PROB, DRIFT values
- L2-protocol/websocket-spec.md: Event schemas
- L2-protocol/field-dictionary.md: Field definitions

### Reviewed (†) - 2 sources
- L5-strategy-tactics/probability-framework.md
  - Claim: "50-70% probability at tick 100-200"
  - Status: Derived from 100 games, needs 10,000+ for confidence

### Theoretical (*) - 1 source
- L7-advanced-analytics/prng-analysis.md
  - Claim: "78% volatility spike before rug"
  - Status: Hypothesis, requires tick-by-tick validation
```

---

## Rugopedia Volume 1: Validation Workflow

### Phase 1: Empirical Baseline (Week 1-2)

**Objective:** Process all 100+ recorded games to establish statistical ground truth.

**Outputs:**
1. `L6-statistical-baselines/survival-curves.md` (VERIFIED)
   - Empirical survival probability by tick
   - Sample size, confidence intervals

2. `L6-statistical-baselines/game-duration-distribution.md` (VERIFIED)
   - Mean/median game duration
   - Instarug frequency

3. `L6-statistical-baselines/price-volatility-empirical.md` (VERIFIED)
   - Actual volatility by price zone
   - Comparison to theoretical model

### Phase 2: Claim Validation (Week 3-4)

**Objective:** Test specific claims against empirical data.

| Claim | Source | Test Method | Target |
|-------|--------|-------------|--------|
| "0.5% rug chance per tick" | L1/provably-fair.md | Compare to empirical survival curve | VERIFY or REFUTE |
| "78% volatility spike before rug" | L7/prng-analysis.md | Calculate volatility in final 5 ticks | VERIFY or REFUTE |
| "50-70% probability at tick 100-200" | L5/probability-framework.md | Compare to empirical CDF | CALIBRATE |
| "Breakeven at 16.67%" | L1/side-bet-mechanics.md | Mathematical proof (not empirical) | CANONICAL |

### Phase 3: Content Consolidation (Week 5-6)

**Objective:** Merge validated content into Rugopedia Volume 1.

**Structure:**
```
rugs-strategy/
├── RUGOPEDIA.md                    # Master index
├── L1-game-mechanics/
│   ├── provably-fair.md            # CANONICAL
│   ├── side-bet-mechanics.md       # CANONICAL
│   └── WHAT-IT-IS-NOT.md          # CANONICAL (misconception guard)
├── L2-protocol/
│   └── [all files]                 # CANONICAL (from live protocol)
├── L5-strategy-tactics/
│   ├── probability-framework.md    # VERIFIED (after validation)
│   └── [others]                    # Status TBD
├── L6-statistical-baselines/
│   └── [new empirical files]       # VERIFIED (from recordings)
└── L7-advanced-analytics/
    └── [mark as THEORETICAL]       # Research/hypothesis zone
```

### Phase 4: Agent Training (Week 7)

**Objective:** Update rugs-expert to respect validation tiers.

1. Read frontmatter on every query
2. Apply citation discipline
3. Generate validation reports on demand
4. Refuse to cite THEORETICAL as fact

---

## Validation Criteria

### For CANONICAL Status
- Source is the live rugs.fun protocol (captured)
- Source is the provably fair verification page
- Mathematical proofs (breakeven calculations)

### For VERIFIED Status
- Tested against 1,000+ game recordings
- 95% confidence interval documented
- Reproducible methodology

### For REVIEWED Status
- Human reviewed the logic
- Sample size < 1,000 games
- Awaiting larger dataset

### For THEORETICAL Status
- Hypothesis or conjecture
- No empirical validation
- May be speculation

---

## Implementation Checklist

- [ ] Create empirical analysis pipeline for recordings
- [ ] Generate L6-statistical-baselines from 100+ games
- [ ] Test specific claims against data
- [ ] Update frontmatter with validation results
- [ ] Update rugs-expert agent with citation discipline
- [ ] Create /validation-report skill
- [ ] Document methodology in Rugopedia index

---

*Last updated: December 24, 2025*
