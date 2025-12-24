---
layer: 2
domain: protocol/confirmation-mapping
priority: P0
bot_relevant: true
validation_tier: verified
source_file: "Empirical capture 2025-12-24"
cross_refs:
  - L2-protocol/events-index.md
  - L5-strategy-tactics/bot-action-interface.md
last_validated: 2025-12-24
---

# Action Confirmation Mapping for Rugs.fun

**Purpose:** Map button actions to their WebSocket confirmation events for bot automation.

**Data Source:** Empirical capture from December 24, 2025 (8,819 events, 94 playerUpdate, 19 sidebets)

---

## Critical Discovery: HTTP vs WebSocket

**Button clicks do NOT send WebSocket messages.** Trade actions use HTTP POST to REST API endpoints:
- Client TX WebSocket events are only `getLeaderboard` and `getPlayerLeaderboardPosition` queries
- All BUY/SELL/SIDEBET confirmations come via WebSocket RX (server push)

---

## 1. BUY Confirmation

### Primary Event: `playerUpdate`

**Detection Logic:**
```python
if positionQty > prev_positionQty and cash < prev_cash:
    action = "BUY"
```

**Key Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `cash` | float | New balance (decreased by bet amount) |
| `positionQty` | float | New position size (increased) |
| `avgCost` | float | VWAP entry price |
| `totalInvested` | float | Total capital in position |
| `cumulativePnL` | float | Overall session P&L |

**Example Sequence:**
```
10:55:20 | cash: 0.264684 → 0.262684 (Δ-0.002000) | position: 0.0000 → 0.0020
         | avgCost: 0 → 1.0 | BUY during presale @ 1.0x
```

**Latency:** Server pushes `playerUpdate` within ~1 second of button click

---

## 2. SELL Confirmation

### Primary Event: `playerUpdate`

**Detection Logic:**
```python
if positionQty < prev_positionQty and cash > prev_cash:
    action = "SELL"

# For partial sell:
sell_percentage = (prev_positionQty - positionQty) / prev_positionQty * 100
```

**Key Fields (Position Closed):**
| Field | Value | Description |
|-------|-------|-------------|
| `positionQty` | 0 | Position fully closed |
| `avgCost` | 0 | No active position |
| `cash` | increased | Proceeds added |

**Example Sequence:**
```
10:55:28 | cash: 0.262684 → 0.264173 (Δ+0.001489) | position: 0.0010 → 0.0000
         | avgCost: 1.0 → 0 | SELL 100% with 48.9% profit
```

**Profit Calculation:**
```python
proceeds = new_cash - prev_cash  # 0.001489
cost_basis = prev_positionQty * prev_avgCost  # 0.001
profit_pct = (proceeds - cost_basis) / cost_basis * 100  # 48.9%
```

---

## 3. SIDEBET Placement Confirmation

### Primary Event: `currentSidebet`

**Detection Logic:**
```python
if event == "currentSidebet" and data.get("type") == "placed":
    sidebet_confirmed = True
```

**Key Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `playerId` | string | Your DID identity |
| `gameId` | string | Current game identifier |
| `betAmount` | float | Amount wagered |
| `price` | float | Price when sidebet placed |
| `xPayout` | int | Payout multiplier (always 5) |
| `startTick` | int | Window start tick |
| `endTick` | int | Window end tick (startTick + 40) |
| `tickIndex` | int | Tick when placed |
| `timestamp` | int | Server timestamp (ms) |
| `type` | string | "placed" |

**Secondary Signal:** `playerUpdate` shows `cash` decrease WITHOUT `positionQty` change

**Presale vs Active Placement:**
- **Presale:** `startTick=0`, `endTick=40`, `price=1.0`
- **Active:** `startTick=currentTick`, `endTick=currentTick+40`, `price=currentPrice`

**Example:**
```json
{
  "playerId": "did:privy:cmaibr7rt0094jp0mc2mbpfu4",
  "gameId": "20251224-7431411f",
  "betAmount": 0.004,
  "price": 2.37,
  "xPayout": 5,
  "startTick": 78,
  "endTick": 118,
  "tickIndex": 78,
  "type": "placed"
}
```

---

## 4. SIDEBET Result

### Primary Event: `currentSidebetResult`

**Key Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `won` | boolean | Win/loss status |
| `payout` | float | Amount returned (5x on win, 0 on loss) |
| `resultPrice` | float | Price at tick 40 resolution |
| `betAmount` | float | Original wager |
| `type` | string | "result" |

**Win Detection in playerUpdate:**
```python
# Sidebet WIN shows as cash increase without position change
if cash > prev_cash and positionQty == prev_positionQty == 0:
    # Could be sidebet win
    expected_payout = last_sidebet_amount * 5
    if abs(cash_delta - expected_payout) < 0.0001:
        action = "SIDEBET_WIN"
```

**Example Win:**
```
10:55:34 | cash: 0.262173 → 0.267173 (Δ+0.005000) | position unchanged
         | Sidebet WIN: 0.001 bet → 0.005 payout (5x)
```

---

## 5. Latency Measurements

### Action → Confirmation Latency

Based on empirical data:

| Action | Typical Latency | Notes |
|--------|-----------------|-------|
| BUY | ~1-2 seconds | HTTP POST → `playerUpdate` |
| SELL | ~1-2 seconds | HTTP POST → `playerUpdate` |
| SIDEBET | ~1 second | HTTP POST → `currentSidebet` |
| SIDEBET_RESULT | ~14 seconds | 40 ticks @ ~250ms + server processing |

### Sidebet Placement → Result Timeline

| Event | Timestamp | Delta |
|-------|-----------|-------|
| SIDEBET placed | 10:55:20.961 | +0.0s |
| currentSidebet received | 10:55:20.961 | +0.0s (instant) |
| currentSidebetResult | 10:55:34.421 | +13.5s |

**40 ticks × 250ms = 10 seconds theoretical**
**Actual: ~13-14 seconds** (includes server processing)

---

## 6. State Reconciliation Strategy

### For BotActionInterface

```python
class ConfirmationMonitor:
    def __init__(self):
        self.pending_actions = {}  # action_id → expected_change

    async def expect_buy(self, action_id: str, amount: float):
        self.pending_actions[action_id] = {
            "type": "BUY",
            "expected_cash_delta": -amount,
            "expected_position_delta": amount,  # Approximate at price 1.0
            "timeout": time.time() + 5.0
        }

    def on_player_update(self, data: dict):
        # Check if this confirms any pending action
        for action_id, expected in list(self.pending_actions.items()):
            if self._matches(expected, data):
                del self.pending_actions[action_id]
                return Confirmation(action_id, latency=...)
```

### Field Priority for Confirmation

1. **positionQty** - Most reliable indicator of BUY/SELL
2. **cash** - Confirms capital flow
3. **avgCost** - Confirms entry price accuracy
4. **currentSidebet.type == "placed"** - Sidebet confirmation

---

## 7. Edge Cases & Warnings

### DCA (Multiple BUYs)
```
10:57:23 | BUY | position: 0.0000 → 0.0020 | avgCost: 0 → 1.0
10:57:24 | BUY | position: 0.0020 → 0.0040 | avgCost: 1.0 → 1.0
```
- Rapid BUYs may arrive as separate `playerUpdate` events
- `avgCost` recalculates as VWAP

### Sidebet During Position
```
10:56:43 | SIDEBET | cash: 0.261037 → 0.259037 | position: 0.0047 (unchanged)
```
- Sidebets deduct from cash but don't affect position

### Sidebet WIN During Position
```
10:03:19 | cash: 0.246133 → 0.247603 (+0.001469) | position: 0.0031 (unchanged)
```
- Cash increases without position change = sidebet win or other bonus

---

## 8. Summary: Event → Action Mapping

| WebSocket Event | Action Detected | Key Field Check |
|-----------------|-----------------|-----------------|
| `playerUpdate` | BUY | positionQty ↑, cash ↓ |
| `playerUpdate` | SELL | positionQty ↓, cash ↑ |
| `playerUpdate` | SIDEBET | cash ↓, position unchanged |
| `playerUpdate` | SIDEBET_WIN | cash ↑, position unchanged |
| `currentSidebet` | SIDEBET_PLACED | type == "placed" |
| `currentSidebetResult` | SIDEBET_RESOLVED | won, payout fields |

---

*Last updated: December 24, 2025 | Empirical validation complete*
