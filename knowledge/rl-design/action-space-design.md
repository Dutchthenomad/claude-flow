# Action Space Design

**Date:** 2025-12-25
**Status:** DRAFT
**Principle:** Binary actions first (100% sells only), then complexity

---

## Design Principles

1. **Start Simple**: 100% sells only, no partial sells
2. **Human-First**: Action space mirrors actual UI buttons
3. **Button Logging**: Record full button press sequences with timestamps
4. **Multi-Discrete**: Gymnasium-compatible action space

---

## Key Learnings (from V3 Success + Empirical Data)

### V3 Sidebet Model
- **39.4% win rate** (Gradient Boosting)
- **Dominant feature**: z_score (game duration outlier)
- **Critical insight**: Single bug fix transformed model

### Empirical Data (899 games)
- **100% of entries rug** - exit timing is EVERYTHING
- **Sweet spot**: 25-50x entry (75% achieve 100% profit)
- **50% rug by tick 138**, 79.3% by tick 300
- **Optimal hold**: 48-60 ticks for sweet spot entries

---

## UI Button Inventory

### Action Buttons
| Button | ID | Category |
|--------|-----|----------|
| BUY | `BUY` | action |
| SELL | `SELL` | action |
| SIDEBET | `SIDEBET` | action |

### Bet Adjustment Buttons
| Button | ID | Category |
|--------|-----|----------|
| X (clear) | `CLEAR` | bet_adjust |
| +0.001 | `INC_001` | bet_adjust |
| +0.01 | `INC_01` | bet_adjust |
| +0.1 | `INC_10` | bet_adjust |
| +1 | `INC_1` | bet_adjust |
| 1/2 | `HALF` | bet_adjust |
| X2 | `DOUBLE` | bet_adjust |
| MAX | `MAX` | bet_adjust |

### Sell Percentage Buttons (DEFERRED - v2.0)
| Button | ID | Category |
|--------|-----|----------|
| 10% | `SELL_10` | percentage |
| 25% | `SELL_25` | percentage |
| 50% | `SELL_50` | percentage |
| 100% | `SELL_100` | percentage |

---

## Multi-Discrete Action Space (v1.0 - Binary)

```python
from gymnasium import spaces

# [action_type, bet_adjustment]
action_space = spaces.MultiDiscrete([
    4,  # Action type
    9,  # Bet adjustment
])

# Action type encoding
ACTION_TYPE = {
    0: "WAIT",       # Do nothing this tick
    1: "BUY",        # Buy with current bet amount
    2: "SELL_100",   # Sell 100% of position
    3: "SIDEBET",    # Place sidebet with current amount
}

# Bet adjustment encoding
BET_ADJUST = {
    0: "NONE",       # No adjustment
    1: "CLEAR",      # Clear bet amount (X button)
    2: "INC_001",    # +0.001 SOL
    3: "INC_01",     # +0.01 SOL
    4: "INC_10",     # +0.1 SOL
    5: "INC_1",      # +1.0 SOL
    6: "HALF",       # 1/2 current amount
    7: "DOUBLE",     # X2 current amount
    8: "MAX",        # MAX (all balance)
}
```

### Example Action Sequences

| Human Behavior | Multi-Discrete | Description |
|----------------|----------------|-------------|
| Wait | `[0, 0]` | WAIT, no adjustment |
| Quick buy 0.001 | `[1, 2]` | BUY, +0.001 |
| Larger buy 0.01 | `[1, 3]` | BUY, +0.01 |
| Sell all | `[2, 0]` | SELL_100, no adjustment |
| Sidebet min | `[3, 2]` | SIDEBET, +0.001 |
| Build amount only | `[0, 4]` | WAIT, +0.1 (prepare next tick) |

---

## Human Button Logging Schema

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

@dataclass
class ButtonEvent:
    """
    Record a single button press with full context.

    This is the atomic unit of human gameplay recording.
    """

    # === TIMESTAMP ===
    ts: datetime              # When button was pressed (client time)
    server_ts: Optional[int]  # Server timestamp if confirmed

    # === BUTTON IDENTITY ===
    button_id: str            # "BUY", "SELL", "+0.001", etc.
    button_category: str      # "action", "bet_adjust", "percentage"

    # === GAME CONTEXT ===
    tick: int                 # Current tick when pressed
    price: float              # Current multiplier
    game_phase: int           # 0=cooldown, 1=presale, 2=active, 3=rugged
    game_id: str              # Game identifier

    # === PLAYER STATE (before action) ===
    balance: Decimal          # Available SOL
    position_qty: Decimal     # Position size
    bet_amount: Decimal       # Current bet amount in entry field

    # === DERIVED ===
    ticks_since_last_action: int  # Time since last button press

    # === ACTION SEQUENCE ===
    sequence_id: str          # UUID for grouping related presses
    sequence_position: int    # Position in sequence (0, 1, 2...)


@dataclass
class ActionSequence:
    """
    Group of button presses forming a complete action.

    Example: ["+0.01", "+0.01", "BUY"] = build to 0.02, then buy
    """

    sequence_id: str
    button_events: List[ButtonEvent]

    # Final action
    final_action: str         # "BUY", "SELL", "SIDEBET", or "INCOMPLETE"
    total_duration_ms: int    # Time from first to last press

    # Outcome (filled after server confirmation)
    success: bool
    executed_price: Optional[float]
    latency_ms: Optional[int]
```

---

## Recording Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    HUMAN PLAYS GAME                               │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│               HumanActionInterceptor                              │
│   - Intercepts button clicks                                      │
│   - Captures GameContext at press time                            │
│   - Groups into ActionSequence                                    │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   ButtonEvent Records                             │
│   - One per button press                                          │
│   - Full context preserved                                        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                     EventStore                                    │
│   - Parquet storage                                               │
│   - doc_type = "button_event"                                     │
│   - Queryable for training                                        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Training Pipeline                               │
│   - Convert sequences to Multi-Discrete actions                   │
│   - Pair with observations                                        │
│   - Create (s, a, r, s') tuples                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Action Validation Rules

```python
def is_valid_action(action: list[int], state: Observation) -> bool:
    """
    Validate action against current game state.

    Returns:
        True if action is legal, False otherwise
    """
    action_type, bet_adjust = action

    # WAIT is always valid
    if action_type == 0:
        return True

    # BUY requires: active game, no position, sufficient balance
    if action_type == 1:  # BUY
        if state.game_phase != 2:  # Not active
            return False
        if state.position_qty > 0:  # Already have position
            return False
        if state.balance < 0.001:  # Minimum buy
            return False
        return True

    # SELL requires: active game, have position
    if action_type == 2:  # SELL_100
        if state.game_phase != 2:  # Not active
            return False
        if state.position_qty <= 0:  # No position
            return False
        return True

    # SIDEBET requires: active game, not already bet, sufficient balance
    if action_type == 3:  # SIDEBET
        if state.game_phase != 2:  # Not active
            return False
        if state.balance < 0.001:  # Minimum sidebet
            return False
        # Additional: check if already placed sidebet this game
        return True

    return False
```

---

## Future Extensions (v2.0+)

### Partial Sells
```python
# Extended action type for v2.0
ACTION_TYPE_V2 = {
    0: "WAIT",
    1: "BUY",
    2: "SELL_10",
    3: "SELL_25",
    4: "SELL_50",
    5: "SELL_100",
    6: "SIDEBET",
}
```

### Position Sizing
```python
# Extended for dynamic position sizing
action_space_v2 = spaces.MultiDiscrete([
    7,   # Action type (with partial sells)
    9,   # Bet adjustment
    5,   # Position size bucket: 10%, 25%, 50%, 75%, 100%
])
```

---

## Mapping to Reward Function

Based on V3 success and empirical data:

```python
def calculate_reward(
    action: list[int],
    state_before: Observation,
    state_after: Observation,
    game_outcome: str  # "active", "rugged", "profitable_exit"
) -> float:
    """
    Reward function aligned with empirical findings.
    """
    action_type, _ = action

    # Base: P&L delta
    pnl_delta = state_after.cumulative_pnl - state_before.cumulative_pnl
    reward = float(pnl_delta) * 10.0  # Scale for learning

    # Sweet spot entry bonus (25-50x)
    if action_type == 1:  # BUY
        if 25 <= state_before.price <= 50:
            reward += 0.5  # Empirical sweet spot

    # Exit before rug bonus
    if action_type == 2 and game_outcome == "rugged":
        if state_before.position_qty == 0:  # Sold before rug
            reward += 2.0  # Critical success

    # Temporal risk penalty (past tick 138)
    if state_before.tick > 138 and state_before.position_qty > 0:
        reward -= 0.1 * (state_before.tick - 138) / 100  # Escalating penalty

    return reward
```

---

## Next Steps

1. [ ] Implement ButtonEvent logging in HumanActionInterceptor
2. [ ] Add button_event doc_type to EventStore
3. [ ] Create ActionSequence aggregator
4. [ ] Build training data converter (sequences → Multi-Discrete)
5. [ ] Wire interceptor to UI buttons

---

*Created: 2025-12-25*
*Based on: V3 Success Report, Empirical Data Analysis, Volatility Studies*
