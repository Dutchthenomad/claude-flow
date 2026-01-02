# Implementation Plan: Human Recording → RL Training Pipeline

**Date:** 2025-12-26
**Status:** READY FOR IMPLEMENTATION
**Based on:** observation-space-design.md, action-space-design.md

---

## Phase Summary

```
PHASE 1: ButtonEvent Logging (HumanActionInterceptor)
    ↓
PHASE 2: EventStore Integration (button_event doc_type)
    ↓
PHASE 3: Training Data Converter (sequences → Multi-Discrete)
    ↓
PHASE 4: Gymnasium Environment Update
    ↓
PHASE 5: Model Training & Validation
```

---

## Phase 1: ButtonEvent Logging

**Goal:** Capture every human button press with full game context.

### Files to Modify

| File | Change |
|------|--------|
| `src/bot/action_interface/recording/human_interceptor.py` | Add ButtonEvent creation |
| `src/models/events/__init__.py` | Export ButtonEvent, ActionSequence |
| `src/models/events/button_event.py` | **NEW** - ButtonEvent dataclass |
| `src/models/events/action_sequence.py` | **NEW** - ActionSequence dataclass |

### ButtonEvent Schema

```python
@dataclass
class ButtonEvent:
    # Timestamp
    ts: datetime
    server_ts: Optional[int]

    # Button identity
    button_id: str          # "BUY", "SELL", "+0.001", etc.
    button_category: str    # "action", "bet_adjust", "percentage"

    # Game context (at press time)
    tick: int
    price: float
    game_phase: int         # 0=cooldown, 1=presale, 2=active, 3=rugged
    game_id: str

    # Player state (before action)
    balance: Decimal
    position_qty: Decimal
    bet_amount: Decimal

    # Derived
    ticks_since_last_action: int

    # Sequence tracking
    sequence_id: str
    sequence_position: int
```

### Button ID Mapping

| UI Button | button_id | button_category |
|-----------|-----------|-----------------|
| BUY | `BUY` | action |
| SELL | `SELL` | action |
| SIDEBET | `SIDEBET` | action |
| X (clear) | `CLEAR` | bet_adjust |
| +0.001 | `INC_001` | bet_adjust |
| +0.01 | `INC_01` | bet_adjust |
| +0.1 | `INC_10` | bet_adjust |
| +1 | `INC_1` | bet_adjust |
| 1/2 | `HALF` | bet_adjust |
| X2 | `DOUBLE` | bet_adjust |
| MAX | `MAX` | bet_adjust |

### Tests Required

- [ ] `test_button_event_creation.py` - ButtonEvent dataclass validation
- [ ] `test_human_interceptor_logging.py` - Integration with interceptor
- [ ] `test_action_sequence_grouping.py` - Sequence aggregation logic

---

## Phase 2: EventStore Integration

**Goal:** Persist ButtonEvents to Parquet via EventStore.

### Schema Addition

```python
# In src/services/event_store/schema.py

class DocType(str, Enum):
    # ... existing types ...
    BUTTON_EVENT = "button_event"
```

### EventBus Integration

```python
# New event type
class Events(str, Enum):
    # ... existing events ...
    BUTTON_PRESS = "button_press"

# HumanActionInterceptor publishes:
event_bus.publish(Events.BUTTON_PRESS, button_event)

# EventStore subscribes:
event_bus.subscribe(Events.BUTTON_PRESS, self._handle_button_event)
```

### Parquet Schema

| Column | Type | Notes |
|--------|------|-------|
| ts | timestamp | Client time |
| server_ts | int64 | Server timestamp |
| button_id | string | Button identifier |
| button_category | string | action/bet_adjust/percentage |
| tick | int32 | Game tick |
| price | float64 | Current multiplier |
| game_phase | int8 | 0-3 |
| game_id | string | UUID |
| balance | decimal | SOL balance |
| position_qty | decimal | Position size |
| bet_amount | decimal | Bet field value |
| ticks_since_last_action | int32 | Timing |
| sequence_id | string | UUID |
| sequence_position | int32 | 0, 1, 2... |

---

## Phase 3: Training Data Converter

**Goal:** Convert ButtonEvent sequences to (observation, action) pairs.

### Conversion Logic

```python
def sequence_to_training_pair(
    sequence: ActionSequence,
    game_state: Observation
) -> tuple[np.ndarray, np.ndarray]:
    """
    Convert a human action sequence to RL training format.

    Returns:
        (observation_vector, action_vector)
        - observation: 45-dimensional feature vector
        - action: [action_type, bet_adjustment] Multi-Discrete
    """
    # Map final action to action_type
    action_type = ACTION_TYPE_MAP[sequence.final_action]  # 0-3

    # Extract bet adjustment from sequence
    bet_adjust = extract_bet_adjustment(sequence.button_events)  # 0-8

    # Build observation from game state
    obs = build_observation_vector(game_state)  # 45 features

    return obs, np.array([action_type, bet_adjust])
```

### Output Format

```
~/rugs_training_data/
├── v2/                              # New format
│   ├── sessions/
│   │   └── <session_id>/
│   │       ├── metadata.json        # Session info
│   │       ├── observations.parquet # Observation vectors
│   │       ├── actions.parquet      # Multi-Discrete actions
│   │       └── rewards.parquet      # Calculated rewards
│   └── manifest.json
```

---

## Phase 4: Gymnasium Environment Update

**Goal:** Update RugsEnv to use new observation/action spaces.

### Changes Required

```python
# In rugs_bot/env/rugs_env.py

class RugsMultiGameEnv(gym.Env):
    def __init__(self):
        # New observation space (~45 features)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(45,), dtype=np.float32
        )

        # New action space (Multi-Discrete)
        self.action_space = spaces.MultiDiscrete([4, 9])
```

### Observation Builder

```python
def _build_observation(self) -> np.ndarray:
    """Build 45-dimensional observation vector."""
    return np.array([
        # Game state (7)
        self.tick,
        self.price,
        self.price_velocity,
        self.price_acceleration,
        self.game_phase,
        self.cooldown_timer_ms,
        float(self.allow_pre_round_buys),

        # Player state (5)
        float(self.balance),
        float(self.position_qty),
        float(self.avg_entry_price),
        float(self.cumulative_pnl),
        float(self.total_invested),

        # Derived (4)
        float(self.unrealized_pnl),
        self.position_pnl_pct,
        self.time_in_position,
        self.balance_at_risk_pct,

        # Market context (7)
        self.players_in_game,
        self.players_with_positions,
        float(self.total_market_capital),
        float(self.recent_buy_volume),
        float(self.recent_sell_volume),
        self.trade_flow_ratio,
        float(self.whale_activity_flag),

        # Rugpool (3)
        float(self.rugpool_amount),
        float(self.rugpool_threshold),
        self.rugpool_ratio,

        # Historical (flattened, 20 each = 40 total... OR use separate)
        # For now, use statistics instead: mean, std, min, max
        *self._price_history_stats(),  # 4 features
        *self._volume_history_stats(), # 4 features

        # Session context (6)
        self.average_multiplier,
        self.count_2x,
        self.count_10x,
        self.count_50x,
        self.count_100x,
        self.highest_today,
    ], dtype=np.float32)
```

---

## Phase 5: Model Training & Validation

**Goal:** Train RL model on human gameplay data.

### Training Pipeline

```bash
# 1. Convert legacy recordings to new format
python scripts/convert_legacy_recordings.py

# 2. Train imitation learning model
python scripts/train_imitation.py --data ~/rugs_training_data/v2/

# 3. Validate on held-out sessions
python scripts/validate_model.py --model models/imitation_v1.zip

# 4. Fine-tune with RL
python scripts/train_rl.py --pretrained models/imitation_v1.zip
```

### Success Criteria

| Metric | Target | Notes |
|--------|--------|-------|
| Action accuracy | >80% | Match human actions |
| Entry timing | 25-50x zone | Sweet spot alignment |
| Exit before rug | >90% | Critical safety |
| ROI simulation | >5% | On validation set |

---

## Dependency Graph

```
observation-space-design.md ──┐
                              ├──► Phase 1: ButtonEvent
action-space-design.md ───────┘        │
                                       ▼
                              Phase 2: EventStore
                                       │
                                       ▼
                              Phase 3: Converter
                                       │
                                       ▼
                              Phase 4: Gymnasium
                                       │
                                       ▼
                              Phase 5: Training
```

---

## Estimated Scope

| Phase | Complexity | Files |
|-------|------------|-------|
| Phase 1 | Medium | 4 new, 2 modified |
| Phase 2 | Low | 2 modified |
| Phase 3 | Medium | 3 new |
| Phase 4 | Medium | 2 modified |
| Phase 5 | High | 4 new scripts |

---

*Created: 2025-12-26*
*Based on: V3 Success Report, Empirical Data Analysis, Unified System Design*
