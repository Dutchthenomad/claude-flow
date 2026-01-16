# Game Data Extraction Results

## Overview

This directory contains extracted and processed game data from Rugs.fun websocket captures. The data has been parsed from raw JSONL files containing `gameStateUpdate` events with `gameHistory` information.

## Extraction Date

**Extracted:** 2026-01-16 22:13:12 UTC

## Files

### 1. `extracted_games_full_YYYYMMDD_HHMMSS.jsonl`

Complete game records in JSONL format (one JSON object per line). Each record contains:

- **Game identification**: `id`, `timestamp`, `gameVersion`
- **Outcome data**: `peakMultiplier`, `rugged`, `prices`, `candles`
- **Provably fair cryptography**: `provablyFair` object with `serverSeed` and `serverSeedHash`
- **Trading activity**: `globalTrades` and `globalSidebets` arrays
- **Price history**: Complete tick-by-tick price array

**Format:** JSONL (newline-delimited JSON)  
**Encoding:** UTF-8  
**Size:** 158 games

### 2. `games_detailed_YYYYMMDD_HHMMSS.csv`

Spreadsheet-friendly format with key fields extracted for analysis.

**Columns:**
- Game ID
- Date/Time
- Timestamp (ms)
- Peak Multiplier
- Rugged (Yes/No)
- Game Version
- Server Seed (full hex string)
- Server Seed Hash (full hex string)
- Total Trades
- Total Sidebets
- Total Price Ticks
- Total Candles
- First Price
- Last Price
- Max Price
- Min Price

**Format:** CSV  
**Encoding:** UTF-8  
**Size:** 158 games

### 3. `game_extraction_report_YYYYMMDD_HHMMSS.md`

Human-readable summary report with:
- Extraction statistics
- Date range of games
- Files processed
- Aggregate statistics (rug rate, average peak multiplier, etc.)
- Top 100 games in chronological order (markdown table)

## Key Statistics

- **Total unique games extracted:** 158
- **Date range:** 2025-03-23 21:37:15 to 2025-12-15 17:22:34
- **Rug rate:** 100.0% (all games ended in a crash)
- **Average peak multiplier:** 21.1374x
- **Maximum peak multiplier:** 1885.8381x (Game: 20251215-206ea330cf7f4f5d)
- **Minimum peak multiplier:** 1.0000x (instant rug)

## Data Sources

The data was extracted from 14 JSONL files in the `raw_captures/` directory:

| File | Games Found | Notes |
|------|------------|-------|
| 2025-12-14_23-04-44_cdp.jsonl | 260 | Largest source (deduplicated) |
| 2025-12-14_19-18-09_raw.jsonl | 110 | |
| 2025-12-14_19-35-37_raw.jsonl | 100 | |
| 2025-12-14_19-46-57_raw.jsonl | 100 | |
| 2025-12-15_00-02-09_raw.jsonl | 100 | |
| 2025-12-14_11-51-33_raw.jsonl | 90 | |
| 2025-12-14_20-17-10_raw.jsonl | 70 | |
| 2025-12-14_22-44-58_cdp.jsonl | 70 | |
| 2025-12-15_12-22-03_cdp.jsonl | 60 | |
| 2025-12-15_00-15-50_cdp.jsonl | 50 | |
| 2025-12-12_17-16-58_raw.jsonl | 40 | |
| 2025-12-15_00-39-17_cdp.jsonl | 30 | |
| 2025-12-14_22-43-04_cdp.jsonl | 20 | |
| 2025-12-15_00-52-20_cdp.jsonl | 20 | |

**Note:** The total raw game records (1,120) were deduplicated to 158 unique games based on game ID. Many websocket captures contained overlapping game history data.

## Provably Fair Verification

Each game record includes provably fair cryptographic data:

- **Server Seed:** The revealed random seed used to generate game outcomes
- **Server Seed Hash:** SHA-256 hash of the server seed (provided pre-game for verification)

These values can be used to independently verify that game outcomes were determined fairly and were not manipulated after player bets were placed.

### Verification Process

1. Take the revealed `serverSeed` from a completed game
2. Calculate SHA-256 hash of the server seed
3. Compare with the pre-game `serverSeedHash`
4. If they match, the outcome was provably fair
5. Use the seed to regenerate the price curve and verify the peak multiplier

**IMPORTANT FINDING:** Initial verification testing (using `verify_provably_fair.py`) shows that simple SHA-256 hashing of the server seeds does not match the provided hashes. This suggests:
- The server seed may need to be salted, prefixed, or combined with additional data before hashing
- A different hash algorithm or process may be used
- Game version differences may affect the hashing procedure
- Further investigation of Rugs.fun's provably fair implementation is needed for proper verification

## Usage Examples

### Loading Data in Python

```python
import json

# Load all games
games = []
with open('extracted_games_full_20260116_221312.jsonl', 'r') as f:
    for line in f:
        games.append(json.loads(line))

# Analyze peak multipliers
peaks = [g['peakMultiplier'] for g in games]
print(f"Average peak: {sum(peaks)/len(peaks):.2f}x")

# Find high multiplier games
high_mult_games = [g for g in games if g['peakMultiplier'] > 100]
print(f"Found {len(high_mult_games)} games with >100x multiplier")
```

### Loading CSV in Python/Pandas

```python
import pandas as pd

df = pd.read_csv('games_detailed_20260116_221312.csv')
print(df.describe())

# Filter games by date
df['Date/Time'] = pd.to_datetime(df['Date/Time'])
recent_games = df[df['Date/Time'] >= '2025-12-15']
```

### Opening CSV in Excel/Google Sheets

Simply open the CSV file in your preferred spreadsheet application. All fields are properly formatted with headers.

## Data Integrity

- **Deduplication:** Games with duplicate IDs were removed (kept first occurrence)
- **Chronological sorting:** Games are sorted by timestamp (ascending, oldest first)
- **Completeness:** All games include minimum required fields (id, timestamp)
- **Validation:** All JSON records are valid and parseable

## Notes

- All 158 games in this dataset ended in a crash (rugged = true)
- No games have the "didn't rug" outcome in this particular dataset
- Price data includes tick-by-tick prices (high frequency) and candles (aggregated)
- The `globalTrades` array is empty for all games in this dataset (no token trades recorded)
- `globalSidebets` contains player betting activity when present

## Scripts

The following scripts were used to generate and analyze this data:

1. **extract_game_data.py** - Main extraction script that parses JSONL files and outputs organized data
2. **create_detailed_csv.py** - Converts JSONL to CSV format for spreadsheet analysis
3. **verify_provably_fair.py** - Verification script to test server seed hashes (see finding above)

Both scripts are located in the parent directory (`/rag-pipeline/RAW SOCKETS/rugs_recordings/`).

## Regenerating Data

To regenerate the extraction with updated source files:

```bash
cd "/path/to/rag-pipeline/RAW SOCKETS/rugs_recordings"
python3 extract_game_data.py
python3 create_detailed_csv.py
```

New timestamped files will be created in the `extracted_data/` directory.

---

**Generated by:** Game Data Extraction System  
**Repository:** Dutchthenomad/claude-flow  
**Purpose:** CTF/Red-team analysis of Rugs.fun provably fair game logs
