# CANONICAL REVIEW SESSION PLAN

**Prepared**: 2025-12-28
**For Session**: WebSocket Documentation Canonical Review
**Status**: READY FOR REVIEW

---

## PURPOSE

This document provides the structured plan for a dedicated canonical review session to promote all OBSERVED findings from the 2025-12-27/28 WebSocket documentation sessions to CANONICAL status in the RAG pedia.

---

## PRE-REQUISITES FOR REVIEW SESSION

### Required Reading (In Order)

1. **MASTER_STAGING_VERBATIM_INPUT.md** - Raw truth, all user input preserved verbatim
2. **Current WEBSOCKET_EVENTS_SPEC.md** - Existing canonical documentation
3. **Q1_position_opening_events.md** - Position opening analysis
4. **Q2_adding_to_position_events.md** - Add-to-position analysis
5. **Q3_Q4_closing_position_rug_events.md** - Rug sequence analysis

### Location of All Files

```
/home/nomad/Desktop/claude-flow/knowledge/temp/
├── MASTER_STAGING_VERBATIM_INPUT.md    # RAW TRUTH
├── Q1_position_opening_events.md        # Structured Q1
├── Q2_adding_to_position_events.md      # Structured Q2
├── Q3_Q4_closing_position_rug_events.md # Structured Q3/Q4
└── CANONICAL_REVIEW_SESSION_PLAN.md     # THIS FILE
```

### Canonical Spec Location

```
/home/nomad/Desktop/claude-flow/knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md
```

---

## REVIEW SESSION PHASES

### Phase 1: Event Type Additions (Priority P0-P1)

**Objective**: Add 6 new event types to canonical documentation

| # | Event | Direction | Priority | Action |
|---|-------|-----------|:--------:|--------|
| 1 | `buyOrder` | Client → Server | P0 | CREATE new section |
| 2 | `standard/newTrade` | Server → Client | P0 | CREATE new section |
| 3 | `currentSidebetResult` | Server → Client | P0 | CREATE new section |
| 4 | `success` | Server → Client (ACK) | P1 | CREATE new section |
| 5 | `ping` | Client → Server | P2 | CREATE new section |
| 6 | `rugPassQuestCompleted` | Server → Client | P3 | CREATE stub (incomplete data) |

**Verification**: Each event section must include:
- [ ] Event name and Socket.IO format
- [ ] Direction (Client→Server or Server→Client)
- [ ] Category classification
- [ ] Full field table with types and descriptions
- [ ] At least one verbatim example from staging docs
- [ ] Frequency/timing notes

---

### Phase 2: Field Additions to Existing Events

**Objective**: Add 72+ new fields to existing event documentation

#### 2.1 gameStatePlayerUpdate Additions

| Field Path | Type | Priority |
|------------|------|:--------:|
| `gameId` | string | P1 |
| `leaderboardEntry.regularPnl` | number | P1 |
| `leaderboardEntry.shortPnl` | number | P1 |
| `leaderboardEntry.sidebetPnl` | number | P1 |
| `leaderboardEntry.sideBet.bonusPortion` | number | P1 |
| `leaderboardEntry.sideBet.coinAddress` | string | P1 |
| `leaderboardEntry.sideBet.realPortion` | number | P1 |
| `rugpool.totalEntries` | int | P3 |

**Structure Correction Required**:
- Current spec says "same fields as leaderboard entry"
- ACTUAL: Container with `gameId`, `leaderboardEntry`, `rugpool`

#### 2.2 playerUpdate Additions (84% Undocumented!)

**Identity & Authentication (P0)**:
- `id`, `role`, `authenticated`

**Trading Configuration (P1)**:
- `autobuysEnabled`, `autosellPrice`, `hasInteracted`, `hitMaxWin`, `selectedCoin`

**Position Tracking (P1)**:
- `pnlPercent`, `sidebetPnl`, `shortPosition`, `leveragedPositions`, `sidebets`

**Bonus System (P2)**:
- `bonusBalance`, `bonusWagerReq`, `bonusWagered`, `shitcoinBalances`

**Gamification (P3 - OUT_OF_SCOPE)**:
- `levelInfo.*`, `xpBoost.*`, `crateKeys.*`, `recentCrateRewards`

#### 2.3 gameStateUpdate Additions

| Field | Type | Priority |
|-------|------|:--------:|
| `tradeCount` | int | P2 |
| `rugRoyale` | object | P2 |
| `rugRoyale.status` | string | P2 |
| `rugRoyale.activeEventId` | null/string | P2 |
| `rugRoyale.currentEvent` | null/object | P2 |
| `rugRoyale.upcomingEvents` | array | P2 |
| `rugRoyale.events` | array | P2 |
| `availableShitcoins` | array | P1 |
| `availableShitcoins[].address` | string | P1 |
| `availableShitcoins[].ticker` | string | P1 |
| `availableShitcoins[].name` | string | P1 |
| `availableShitcoins[].max_bet` | int | P1 |
| `availableShitcoins[].max_win` | int | P1 |
| `godCandle2x` | null/object | P2 |
| `godCandle2xMassiveJump` | null/bool | P2 |
| `godCandle2xPrices` | array | P2 |
| `godCandle2xTimestamp` | null/int | P2 |
| `godCandle10x` | null/object | P2 |
| `godCandle10xMassiveJump` | null/bool | P2 |
| `godCandle10xPrices` | array | P2 |
| `godCandle10xTimestamp` | null/int | P2 |
| `godCandle50x` | null/object | P2 |
| `godCandle50xMassiveJump` | null/bool | P2 |
| `godCandle50xPrices` | array | P2 |
| `godCandle50xTimestamp` | null/int | P2 |
| `highestTodayPrices` | array | P2 |

---

### Phase 3: Behavioral Pattern Documentation

**Objective**: Document 8 critical behavioral patterns

| # | Pattern | Priority | Notes |
|---|---------|:--------:|-------|
| 1 | Position Opening Sequence | P0 | 3-event order after coolDownTimer:100 |
| 2 | Add-to-Position Flow | P0 | buyOrder → newTrade → playerUpdate → success |
| 3 | Socket.IO ACK Pattern | P1 | 42XX request → 43XX response |
| 4 | Forced Rug Liquidation | P0 | Server auto-sells all positions |
| 5 | Delayed active:false | P0 | ~2 sec delay after rug |
| 6 | Cooldown Timer States | P1 | 15000→10000 (allowPreRound)→0 |
| 7 | Position Closed Indicators | P1 | positionQty=0, avgCost=0 |
| 8 | Sidebet Win Logic | P0 | Rug before endTick = WIN |

---

### Phase 4: Event Category Taxonomy

**Objective**: Create standardized event classification

| Category | Events | Direction |
|----------|--------|-----------|
| TRADING_ACTION | `buyOrder`, `sellOrder` | Client → Server |
| TRADING_EVENT | `standard/newTrade` | Server → Client (broadcast) |
| SIDEBET_EVENT | `currentSidebetResult` | Server → Client |
| PLAYER_STATE | `playerUpdate`, `gameStatePlayerUpdate` | Server → Client (personal) |
| GAME_STATE | `gameStateUpdate` | Server → Client (broadcast) |
| GAMIFICATION | `rugPassQuestCompleted` | Server → Client |
| SYSTEM_HEARTBEAT | `ping` | Client → Server |
| SYSTEM_ACK | `success`, empty ACK (`4358[]`) | Server → Client |

---

### Phase 5: Derived File Regeneration

After canonical updates, regenerate:

1. `events.jsonl` - Event definitions for ingestion
2. `phase_matrix.json` - Game phase → event mapping
3. `field_index.json` - Field path → event lookup

---

## QUALITY CHECKLIST

Before promoting to CANONICAL:

- [ ] All examples copied VERBATIM from MASTER_STAGING doc
- [ ] All field types verified against multiple examples
- [ ] All timestamps and lengths preserved where provided
- [ ] User observations/hypotheses clearly marked as such
- [ ] Open questions documented for future investigation
- [ ] No information loss from staging to canonical

---

## SESSION BOOTSTRAP PROMPT

Copy this to start the canonical review session:

```
I need to perform a CANONICAL REVIEW session for rugs.fun WebSocket documentation.

Read the following files in order:
1. /home/nomad/Desktop/claude-flow/knowledge/temp/CANONICAL_REVIEW_SESSION_PLAN.md
2. /home/nomad/Desktop/claude-flow/knowledge/temp/MASTER_STAGING_VERBATIM_INPUT.md
3. /home/nomad/Desktop/claude-flow/knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md

This session will:
1. Add 6 new event types (buyOrder, standard/newTrade, currentSidebetResult, success, ping, rugPassQuestCompleted)
2. Add 72+ new fields to existing events
3. Document 8 behavioral patterns
4. Create event category taxonomy
5. Regenerate derived files

Follow the CANONICAL PROMOTION LAWS in knowledge/rugs-events/CONTEXT.md exactly.
All examples must be preserved VERBATIM from the staging documents.
```

---

## EXPECTED OUTCOMES

After canonical review session:

1. **WEBSOCKET_EVENTS_SPEC.md** updated with all new content
2. **events.jsonl** regenerated with new events
3. **phase_matrix.json** updated with event→phase mappings
4. **field_index.json** updated with new field paths
5. All staging docs moved to `staging/archived/` with completion date

---

## POST-REVIEW CLEANUP

After successful canonical promotion:

```bash
# Create archive directory
mkdir -p /home/nomad/Desktop/claude-flow/knowledge/temp/archived/2025-12-28-position-transitions

# Move staging docs to archive
mv /home/nomad/Desktop/claude-flow/knowledge/temp/Q*.md \
   /home/nomad/Desktop/claude-flow/knowledge/temp/archived/2025-12-28-position-transitions/

mv /home/nomad/Desktop/claude-flow/knowledge/temp/MASTER_STAGING*.md \
   /home/nomad/Desktop/claude-flow/knowledge/temp/archived/2025-12-28-position-transitions/

mv /home/nomad/Desktop/claude-flow/knowledge/temp/CANONICAL_REVIEW*.md \
   /home/nomad/Desktop/claude-flow/knowledge/temp/archived/2025-12-28-position-transitions/
```

---

# END OF CANONICAL REVIEW SESSION PLAN
