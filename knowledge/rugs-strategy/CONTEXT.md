# Rugs Strategy Knowledge Base

**Status:** Draft | **Date:** 2025-12-24 | **Version:** 1.0.0

---

## Purpose

This knowledge base powers the `rugs-expert` RAG agent with comprehensive game expertise:
- **80% Bot Development** - Strategy, ML/RL, feature engineering
- **20% Manual Trading + Research** - Tactics, statistical analysis

---

## Layer Architecture

| Layer | Domain | Bot Relevance |
|-------|--------|---------------|
| L1 | Game Mechanics | Critical |
| L2 | Protocol & Events | Critical |
| L3 | ML/RL Knowledge | Critical |
| L4 | VECTRA Codebase | High |
| L5 | Strategy & Tactics | High |
| L6 | Statistical Baselines | Critical |
| L7 | Advanced Analytics | Medium |

---

## Validation Tiers

| Tier | Meaning | Promotion Path |
|------|---------|----------------|
| CANONICAL | Single source of truth | Human approval required |
| VERIFIED | Validated against data | Auto from empirical |
| REVIEWED | Human reviewed | Manual review |
| THEORETICAL | Needs validation | Validate → promote |

---

## YAML Frontmatter Schema

All documents MUST include:

```yaml
---
layer: 1-7
domain: category/subcategory
priority: P0|P1|P2
bot_relevant: true|false
validation_tier: canonical|verified|reviewed|theoretical
cross_refs:
  - L1-game-mechanics/related.md
last_validated: YYYY-MM-DD
---
```

---

## Critical: WHAT-IT-IS-NOT

Before applying ANY financial market reasoning, the agent MUST check:
`L1-game-mechanics/WHAT-IT-IS-NOT.md`

Rugs.fun is NOT a real market. No whales, no liquidity pools, no technical analysis.

---

## Query Examples

```bash
# Layer-filtered queries
python -m retrieval.retrieve "entry timing" --filter "layer:5"

# Bot-relevant only
python -m retrieval.retrieve "reward shaping" --filter "bot_relevant:true"

# Cross-reference lookup
python -m retrieval.retrieve "what confirms BUY" --filter "domain:protocol/*"
```

---

## Integration Points

- **ChromaDB**: `~/Desktop/claude-flow/rag-pipeline/storage/chroma/`
- **Canonical Events**: `~/Desktop/VECTRA-PLAYER/docs/specs/WEBSOCKET_EVENTS_SPEC.md`
- **Raw Data**: `~/rugs_data/`
- **N8N Pipeline**: (future) Layer-based routing

---

*Last Updated: 2025-12-24*
