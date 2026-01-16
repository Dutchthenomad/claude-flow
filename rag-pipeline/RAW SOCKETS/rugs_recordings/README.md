# Rugs.fun Game History Extraction

This directory contains tools and results for extracting provably fair game records from raw WebSocket recordings of the Rugs.fun crash game.

## 📊 Extraction Results

**Data Source**: Raw WebSocket recordings in `raw_captures/` directory  
**Extraction Date**: January 16, 2026  
**Games Extracted**: 158 unique games  
**Date Range**: March 23, 2025 - December 15, 2025

### Key Statistics

- **Total Unique Games**: 158 (deduplicated by gameId)
- **Game Outcomes**: 100% rugged (all games crashed)
- **Average Peak Multiplier**: 21.14x
- **Highest Peak Recorded**: 1,885.84x
- **Game Version Distribution**:
  - v3: 155 games (98.1%)
  - Legacy/Unknown: 3 games (1.9%)

### Notable Games

| Rank | Game ID | Peak Multiplier | Duration (ticks) | Date |
|------|---------|-----------------|------------------|------|
| 1 | 20251215-206ea330cf7f4f5d | 1,885.84x | 920 | 2025-12-15 |
| 2 | 20251215-7233f8519253401d | 886.75x | 735 | 2025-12-15 |
| 3 | 20251215-14132053defa41b0 | 20.87x | 242 | 2025-12-15 |
| 4 | 20251215-338d5f498d7045f5 | 18.62x | 1,118 | 2025-12-15 |
| 5 | 20251215-7f0a5a0a7d21426f | 17.28x | 283 | 2025-12-15 |

## 📁 Files

### Data Files

- **`extracted_games_full.jsonl`** - Complete game records in JSONL format (one game per line)
  - Contains full game data including:
    - Game ID and timestamp
    - Provably fair data (serverSeed, serverSeedHash)
    - Price history array
    - Peak multiplier and crash point
    - Trade and sidebet data
    - Game version and metadata

### Report Files

- **`game_statistics.md`** - Summary statistics and analysis
- **`game_records_table.md`** - Formatted markdown table of all 158 games

### Tools

- **`extract_game_history.py`** - Python extraction script
  - Parses JSONL and JSON files from `raw_captures/`
  - Extracts `gameHistory` events from `gameStateUpdate` WebSocket messages
  - Deduplicates by gameId
  - Sorts chronologically
  - Outputs formatted results

## 🔧 Usage

### Run the Extraction

```bash
cd "rag-pipeline/RAW SOCKETS/rugs_recordings"
python3 extract_game_history.py
```

The script will:
1. Scan all `.json` and `.jsonl` files in `raw_captures/`
2. Extract game records from WebSocket events
3. Deduplicate by gameId
4. Sort chronologically
5. Generate output files:
   - `extracted_games_full.jsonl`
   - `game_statistics.md`
   - `game_records_table.md`

### Working with the Data

#### Load games in Python

```python
import json

games = []
with open('extracted_games_full.jsonl', 'r') as f:
    for line in f:
        games.append(json.loads(line))

# Example: Find high multiplier games
high_mult_games = [g for g in games if g.get('peakMultiplier', 0) > 100]
print(f"Found {len(high_mult_games)} games with 100x+ multipliers")
```

#### Query with jq

```bash
# Get all game IDs
cat extracted_games_full.jsonl | jq -r '.id'

# Find games with peak > 50x
cat extracted_games_full.jsonl | jq 'select(.peakMultiplier > 50)'

# Get average peak multiplier
cat extracted_games_full.jsonl | jq -s 'map(.peakMultiplier) | add / length'

# Extract provably fair data
cat extracted_games_full.jsonl | jq '{id, serverSeed: .provablyFair.serverSeed, hash: .provablyFair.serverSeedHash}'
```

## 🎯 Data Structure

### Game Record Schema

```json
{
  "id": "20251215-206ea330cf7f4f5d",
  "timestamp": 1765577075000,
  "prices": [1.0, 1.023, ...],
  "peakMultiplier": 1885.8381,
  "rugged": true,
  "provablyFair": {
    "serverSeed": "2ac3bb0a...",
    "serverSeedHash": "46d83252..."
  },
  "gameVersion": "v3",
  "globalTrades": [...],
  "globalSidebets": [...]
}
```

### Key Fields

- **id** (string): Unique game identifier (format: `YYYYMMDD-{hash}`)
- **timestamp** (int): Unix timestamp in milliseconds
- **prices** (array): Price tick history (1.0 = starting price)
- **peakMultiplier** (float): Highest multiplier reached before crash
- **rugged** (boolean): Whether game crashed (true) or not (false)
- **provablyFair** (object): Cryptographic proof data
  - **serverSeed** (string): Revealed server seed (hex)
  - **serverSeedHash** (string): Pre-commitment hash (hex)
- **gameVersion** (string): Game version identifier (e.g., "v3")
- **globalTrades** (array): Player trade records
- **globalSidebets** (array): Player sidebet records

## 🔐 Provably Fair Verification

Each game includes provably fair cryptographic data that can be independently verified:

1. **Pre-game Commitment**: `serverSeedHash` is shown before the game starts
2. **Post-game Reveal**: `serverSeed` is revealed after the game ends
3. **Verification**: Hash of `serverSeed` should match `serverSeedHash`

This ensures the outcome was predetermined and not manipulated based on player actions.

### Example Verification (Python)

```python
import hashlib
import json

# Load a game
with open('extracted_games_full.jsonl') as f:
    game = json.loads(f.readline())

# Get provably fair data
server_seed = game['provablyFair']['serverSeed']
server_seed_hash = game['provablyFair']['serverSeedHash']

# Verify the hash
computed_hash = hashlib.sha256(server_seed.encode()).hexdigest()
is_valid = computed_hash == server_seed_hash

print(f"Game ID: {game['id']}")
print(f"Hash Valid: {is_valid}")
print(f"Peak Multiplier: {game['peakMultiplier']}x")
```

## 🎲 CTF/Red Team Analysis Notes

This dataset is useful for:

- **Provably Fair Analysis**: Verify game fairness claims
- **Pattern Detection**: Identify anomalies in crash points
- **RNG Analysis**: Examine randomness quality
- **Statistical Testing**: Chi-square, distribution analysis
- **Exploit Detection**: Look for manipulation patterns

### Potential Analysis Vectors

1. **Hash Collision Testing**: Verify serverSeed uniqueness
2. **Distribution Analysis**: Test if crash points follow expected distribution
3. **Temporal Patterns**: Check for time-based biases
4. **Seed Predictability**: Analyze entropy of server seeds
5. **Game Duration Patterns**: Compare tick counts vs multipliers

## 📝 Data Quality Notes

### Known Issues

1. **Parse Errors**: The `2025-12-12_17-16-58_events.json` file contains malformed JSON
   - Many lines failed to parse (indicated in extraction warnings)
   - Valid games were still extracted from other files

2. **100% Crash Rate**: All 158 games ended in a crash (rugged=true)
   - This is expected behavior for this game type
   - No "moon shots" (infinite multiplier games) in this sample

3. **Date Gap**: Large gap between March and December 2025 data
   - March games: 3 games (legacy format)
   - December games: 155 games (v3 format)

### Recommendations

- For production analysis, collect more data over longer time periods
- Verify provably fair data for random sample of games
- Compare against published house edge statistics
- Cross-reference with blockchain transaction data if available

## 🤝 Contributing

To add more data:

1. Place new WebSocket recordings in `raw_captures/`
2. Run `python3 extract_game_history.py`
3. Script will automatically process new files and update outputs

### Recording Format

Expected file formats:
- **JSONL**: One JSON event per line
- **JSON**: Array of events or structured event log

Expected event structure:
```json
{
  "gameStateUpdate": {
    "gameHistory": [
      {
        "id": "...",
        "timestamp": 123456789,
        "provablyFair": {...},
        "peakMultiplier": 1.23,
        ...
      }
    ]
  }
}
```

## 📖 References

- [Rugs.fun Official Site](https://rugs.fun)
- [Provably Fair Gaming Explained](https://en.wikipedia.org/wiki/Provably_fair_gambling)
- [SHA-256 Hashing](https://en.wikipedia.org/wiki/SHA-2)

---

*Last Updated: January 16, 2026*
