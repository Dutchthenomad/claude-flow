# Game Data Extraction Summary

## Mission Complete ✓

Successfully extracted and processed 158 unique Rugs.fun crash game records from websocket captures.

## Quick Stats

- **Total Games:** 158 unique (deduplicated from 1,120 raw records)
- **Date Range:** 2025-03-23 to 2025-12-15 (~9 months)
- **Files Processed:** 14 JSONL files from raw_captures/
- **Data Size:** 5.4 MB full JSONL + 38 KB CSV
- **Rug Rate:** 100% (all games crashed)
- **Peak Multipliers:**
  - Average: 21.14x
  - Maximum: 1,885.84x
  - Minimum: 1.00x

## Output Files Location

```
rag-pipeline/RAW SOCKETS/rugs_recordings/extracted_data/
├── README.md                                    # Full documentation
├── extracted_games_full_20260116_221312.jsonl   # Complete JSON records
├── games_detailed_20260116_221312.csv           # Spreadsheet format
└── game_extraction_report_20260116_221312.md    # Human-readable report
```

## Data Fields Extracted

Each game record includes:

### Identification
- Game ID (format: YYYYMMDD-hexhash)
- Timestamp (milliseconds)
- Game version (v3 or N/A)

### Outcome Data
- Peak multiplier (highest price reached)
- Rugged status (true/false)
- Complete price tick array
- Candlestick data

### Provably Fair
- Server seed (revealed post-game)
- Server seed hash (pre-game commitment)

### Player Activity
- Global trades array
- Global sidebets array (bet placements and payouts)

## Usage Examples

### Python - Load and Analyze

```python
import json

# Load all games
games = []
with open('extracted_data/extracted_games_full_20260116_221312.jsonl', 'r') as f:
    for line in f:
        games.append(json.loads(line))

# Find high multiplier games
high_mult = [g for g in games if g['peakMultiplier'] > 100]
print(f"Games with >100x: {len(high_mult)}")

# Analyze sidebets
total_bets = sum(len(g.get('globalSidebets', [])) for g in games)
print(f"Total sidebets recorded: {total_bets}")
```

### Pandas - Statistical Analysis

```python
import pandas as pd

df = pd.read_csv('extracted_data/games_detailed_20260116_221312.csv')

# Peak multiplier distribution
print(df['Peak Multiplier'].describe())

# Games by date
df['Date'] = pd.to_datetime(df['Date/Time']).dt.date
daily_games = df.groupby('Date').size()
print(daily_games)
```

### Excel/Sheets
Simply open `games_detailed_20260116_221312.csv` in your spreadsheet application.

## Scripts

Three Python scripts are provided:

1. **extract_game_data.py** - Main extraction engine
   - Parses JSONL files
   - Deduplicates games
   - Sorts chronologically
   - Generates all outputs

2. **create_detailed_csv.py** - CSV export
   - Converts JSONL to spreadsheet format
   - Extracts key fields for analysis

3. **verify_provably_fair.py** - Verification tool
   - Tests server seed hashes
   - Validates provably fair claims

## Key Finding: Provably Fair Investigation Needed

Verification testing revealed that standard SHA-256 hashing of server seeds does **not** match the provided server seed hashes. This warrants further investigation:

**Possible explanations:**
- Server seed requires salt/prefix before hashing
- Additional data (client seed, nonce, etc.) may be included
- Different hash algorithm or multi-step process
- Game version differences (v3 vs earlier)

**Next steps for CTF/red-team:**
- Obtain official provably fair documentation from Rugs.fun
- Analyze game client code for hashing implementation
- Test different hashing procedures
- Compare with other provably fair implementations

## Data Integrity

- ✓ All records are valid JSON
- ✓ Duplicate games removed (by game ID)
- ✓ Chronologically sorted (oldest to newest)
- ✓ All required fields present
- ✓ Provably fair data included for all games

## Regenerating Data

To extract new data after capturing more websocket logs:

```bash
cd "rag-pipeline/RAW SOCKETS/rugs_recordings"
python3 extract_game_data.py      # Extract games
python3 create_detailed_csv.py     # Generate CSV
python3 verify_provably_fair.py    # Test verification
```

New timestamped files will be created in `extracted_data/`.

## Additional Notes

- All games in this dataset ended in crashes (rugged = true)
- No successful cashouts/exits were recorded
- `globalTrades` arrays are empty (no token trading recorded)
- Sidebets show player wagering activity when present
- Price tick arrays vary from 17 to 416 ticks per game

---

**Extracted:** 2026-01-16 22:13:12 UTC  
**Repository:** Dutchthenomad/claude-flow  
**Purpose:** CTF/Red-team analysis of Rugs.fun provably fair game logs
