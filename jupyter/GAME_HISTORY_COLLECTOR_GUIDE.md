# GameHistoryCollector Usage Guide

## Overview

The `GameHistoryCollector` provides automatic collection of historical game data from the `gameHistory[]` array in `gameStateUpdate` events. This replaces manual CDP recording with passive, zero-effort data collection for ML/RL training.

## Key Features

- **Automatic Deduplication**: Tracks games by `gameId` to avoid duplicates
- **Rolling Window Tracking**: Monitors the ~10 game rolling window
- **JSONL Storage**: Compatible with existing recording format
- **Passive Collection**: Zero-configuration during live sessions
- **RL Training Ready**: Export in format suitable for RL pipelines

## Installation

The collector is already integrated into the jupyter library:

```python
from jupyter.lib import GameHistoryCollector, MockGameHistoryCollector
```

## Basic Usage

### Standalone Collection

```python
from jupyter.lib import GameHistoryCollector

# Initialize collector
collector = GameHistoryCollector()

# Start collecting
collector.start_collecting()

# ... let it run during your session ...

# Stop and get statistics
stats = collector.stop_collecting()
print(f"Collected {stats['total_collected']} games")
```

### Integration with CDPCapture

```python
from jupyter.lib import CDPCapture, GameHistoryCollector

# Set up CDP capture
capture = CDPCapture()
capture.connect()

# Attach game history collector
collector = GameHistoryCollector()
collector.attach_to_capture(capture)

# Games are now automatically collected from gameStateUpdate events!
# No further action needed - collection happens passively

# Later, check statistics
stats = collector.get_statistics()
print(f"Total collected: {stats['total_collected']}")
print(f"Duplicates skipped: {stats['duplicates_skipped']}")
```

### Context Manager Style

```python
with GameHistoryCollector() as collector:
    # Automatically starts collecting
    # ... your code here ...
    pass
# Automatically stops collecting
```

## Storage

### Default Storage Location

By default, games are stored in `~/rugs_recordings/game_history/`:

```python
collector = GameHistoryCollector()
# Stores in ~/rugs_recordings/game_history/
```

### Custom Storage Location

```python
from pathlib import Path

collector = GameHistoryCollector(
    storage_dir=Path("/custom/path/game_history"),
    auto_save=True
)
```

### Storage Format

Games are stored as JSONL (one JSON object per line):

```json
{"id": "20251207-1e01ac417e8043ca", "timestamp": 1765068982439, "prices": [1.0, 0.99, 1.01, ...], "rugged": true, "rugPoint": 45.23, "collected_at": "2025-12-24T10:30:00", "source": "gameHistory_rolling_window"}
```

## Retrieving Games

### Get All Collected Games

```python
# Get all games in memory
games = collector.get_collected_games()

# Get most recent N games
recent_games = collector.get_collected_games(limit=10)
```

### Get Specific Game

```python
game = collector.get_game_by_id("20251207-1e01ac417e8043ca")
if game:
    print(f"Found game with {len(game['prices'])} price ticks")
```

### Get Statistics

```python
stats = collector.get_statistics()

print(f"Total collected: {stats['total_collected']}")
print(f"Games in memory: {stats['games_in_memory']}")
print(f"Unique games seen: {stats['unique_games_seen']}")
print(f"Is collecting: {stats['is_collecting']}")
print(f"Last game: {stats['last_game_collected']}")
```

## Data Validation

### Validate Game Structure

```python
validation = collector.validate_game_structure(sample_size=10)

print(f"Analyzed {validation['games_analyzed']} games")
print(f"Found {validation['total_unique_fields']} unique fields")

for field, info in validation['fields'].items():
    print(f"{field}: {info['coverage']} coverage, types: {info['types']}")
```

Example output:
```
Analyzed 10 games
Found 8 unique fields
id: 100.0% coverage, types: ['str']
timestamp: 100.0% coverage, types: ['int']
prices: 100.0% coverage, types: ['list']
rugged: 100.0% coverage, types: ['bool']
rugPoint: 100.0% coverage, types: ['float']
peakMultiplier: 80.0% coverage, types: ['float']
gameVersion: 100.0% coverage, types: ['str']
provablyFair: 50.0% coverage, types: ['dict']
```

## Export for RL Training

### Export All Games

```python
export_path = collector.export_for_rl_training()
print(f"Exported to: {export_path}")
```

### Export Specific Fields

```python
export_path = collector.export_for_rl_training(
    output_file=Path("/path/to/rl_training_data.jsonl"),
    include_fields=['id', 'timestamp', 'prices', 'rugPoint']
)
```

## Advanced Usage

### Manual Event Processing

If you're capturing events manually:

```python
collector = GameHistoryCollector()
collector.start_collecting()

# When you receive a gameStateUpdate event
gameStateUpdate_event = {
    'event_name': 'gameStateUpdate',
    'data': {
        'price': 1.5,
        'active': True,
        'gameHistory': [
            {
                'id': 'game-001',
                'timestamp': 1234567890,
                'prices': [1.0, 1.5, 2.0],
                'rugged': True,
                'rugPoint': 2.0
            }
        ]
    }
}

collector.process_game_state_update(gameStateUpdate_event)
```

### Clear Memory

If you need to free up memory but keep disk storage:

```python
collector.clear_memory()
# In-memory games cleared, but disk storage remains
```

## Testing Without Live Connection

For testing or development without a live connection:

```python
from jupyter.lib import MockGameHistoryCollector

# Creates mock games automatically
collector = MockGameHistoryCollector()
collector.start_collecting()

# Mock games are generated
games = collector.get_collected_games()
print(f"Generated {len(games)} mock games")
```

## Integration with Existing Workflows

### With Existing JSONL Recordings

The collector stores games in the same JSONL format as existing recordings:

```python
# Your existing recordings
# ~/rugs_recordings/session_2024*.jsonl

# GameHistoryCollector storage (compatible format)
# ~/rugs_recordings/game_history/session_*.jsonl
```

### Load Previously Collected Games

When you create a new collector instance, it automatically loads previously seen game IDs:

```python
# Session 1
collector1 = GameHistoryCollector()
collector1.start_collecting()
# ... collect games ...
collector1.stop_collecting()

# Session 2 (later)
collector2 = GameHistoryCollector()
# Automatically loads previous game IDs
# Will skip any games already collected
```

## Value Proposition

| Metric | Current (Manual CDP) | GameHistoryCollector |
|--------|---------------------|----------------------|
| Collection effort | High (active monitoring) | Zero (passive) |
| Data completeness | Depends on uptime | Rolling window always available |
| Deduplication | Manual | Automatic |
| Storage format | JSONL | JSONL (compatible) |
| Integration | CDP WebSocket intercept | EventBus + CDP (both supported) |

## Performance Characteristics

- **Memory**: Default limit of 1000 games in memory (configurable)
- **Storage**: JSONL format, one line per game
- **Deduplication**: O(1) lookup using set of game IDs
- **Processing**: Minimal overhead, processes only new games

## Configuration Options

```python
collector = GameHistoryCollector(
    storage_dir=Path("/custom/path"),     # Storage directory
    auto_save=True,                        # Auto-save to disk
    max_memory_games=1000                  # Max games in memory
)
```

## Troubleshooting

### No Games Being Collected

1. Check if collector is running: `collector.is_collecting`
2. Verify gameStateUpdate events have gameHistory field
3. Check if games are duplicates (already seen)

### Storage Issues

1. Verify storage directory exists and is writable
2. Check disk space
3. Verify JSONL files are being created

### Memory Usage

If memory usage is high:
```python
# Reduce memory limit
collector = GameHistoryCollector(max_memory_games=100)

# Or clear memory periodically
collector.clear_memory()
```

## Example: Complete Workflow

```python
from jupyter.lib import CDPCapture, GameHistoryCollector

# 1. Set up CDP capture
capture = CDPCapture()
if not capture.connect():
    print("Failed to connect to CDP")
    exit(1)

# 2. Attach game history collector
collector = GameHistoryCollector()
collector.attach_to_capture(capture)

print("Collecting game history... (Ctrl+C to stop)")

try:
    # 3. Let it run (games collected passively)
    while True:
        time.sleep(60)
        stats = collector.get_statistics()
        print(f"Collected: {stats['total_collected']}, Skipped: {stats['duplicates_skipped']}")
        
except KeyboardInterrupt:
    print("\nStopping collection...")

# 4. Export for RL training
export_path = collector.export_for_rl_training()
print(f"Exported to: {export_path}")

# 5. Cleanup
collector.stop_collecting()
capture.disconnect()

print("Done!")
```

## Related Documentation

- **Canonical Spec**: `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md` (lines 397-434)
- **CDP Integration**: `jupyter/lib/cdp_notebook.py`
- **Automation Bridge**: `jupyter/lib/automation_bridge.py`
- **Current Recordings**: `~/rugs_recordings/*.jsonl`
