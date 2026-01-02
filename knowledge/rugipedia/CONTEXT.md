# RUGIPEDIA - Rugs.fun Protocol Knowledge Base

**Version:** 1.0
**Created:** January 1, 2026
**Status:** CANONICAL

---

## Purpose

RUGIPEDIA is the **single source of truth** for rugs.fun protocol knowledge. It provides Oxford Dictionary-level documentation for:

- WebSocket events and field schemas
- Game mechanics and phases
- Blockchain integration architecture
- RL observation/action space design

## Structure

```
rugipedia/
├── CONTEXT.md           # This file (entry point)
├── canon/               # CANONICAL protocol documentation
│   ├── WEBSOCKET_EVENTS_SPEC.md    # Master spec (v3.0)
│   ├── CONNECTION_DIAGRAM.md       # Architecture diagrams
│   └── PROVABLY_FAIR.md            # PRNG verification
├── blockchain/          # Blockchain-level documentation
│   ├── INITIAL_BLOCKCHAIN_PROGRAM_WALLET_AUDIT
│   └── INITIAL_FORENSIC_AUDIT_REPORT
├── game-modes/          # Game mode documentation
│   ├── BBC_BEAR_BULL_CRAB.md
│   ├── CANDLEFLIP_GAME.md
│   └── OFFICIAL_FAQ.md
├── glossary/            # Term definitions (future)
│   ├── events/
│   └── fields/
├── generated/           # Auto-generated indexes
│   ├── events.jsonl
│   ├── phase_matrix.json
│   └── field_index.json
├── raw-data/            # Source captures
└── scripts/             # Build tools
```

## Validation Tiers

| Tier | Symbol | Meaning |
|------|--------|---------|
| `canonical` | ✓ | Verified against live protocol |
| `verified` | ✓ | Validated against 1000+ games |
| `reviewed` | † | Human reviewed, not validated |
| `theoretical` | * | Hypothesis, needs validation |

## CANONICAL PROMOTION LAWS

1. **No field is CANONICAL without live protocol evidence**
2. **All modifications to spec require explicit user approval**
3. **Theoretical claims must be marked with `*`**
4. **WEBSOCKET_EVENTS_SPEC.md is the master document**

## Related Locations

| Location | Purpose |
|----------|---------|
| `knowledge/rl-design/` | RL observation/action space design |
| `docs/n8n/` | n8n RAG pipeline documentation |
| `/home/nomad/Desktop/rugs-rl-bot/` | RL trading bot implementation |
| `/home/nomad/Desktop/VECTRA-PLAYER/` | Browser automation + live trading |

## Usage

**For agents:** Read `canon/WEBSOCKET_EVENTS_SPEC.md` first.

**For humans:** Browse game-modes/ for gameplay info, blockchain/ for trust model.

**For RAG ingestion:** Use generated/ folder for structured indexes.

---

*RUGIPEDIA replaces the scattered knowledge across claude-flow, VECTRA-PLAYER, and rugs-rl-bot.*
