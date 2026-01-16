#!/usr/bin/env python3
"""
Create detailed CSV export of game data with all provably fair information.
"""

import json
import csv
from datetime import datetime
from pathlib import Path


def format_timestamp(ts_ms: int) -> str:
    """Convert millisecond timestamp to readable datetime string."""
    try:
        dt = datetime.fromtimestamp(ts_ms / 1000.0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts_ms)


def main():
    """Create detailed CSV from extracted JSONL."""
    # Find the most recent extracted file
    extracted_dir = Path(__file__).parent / "extracted_data"
    jsonl_files = sorted(extracted_dir.glob("extracted_games_full_*.jsonl"))
    
    if not jsonl_files:
        print("No extracted JSONL files found!")
        return
    
    latest_jsonl = jsonl_files[-1]
    print(f"Reading from: {latest_jsonl.name}")
    
    # Output CSV
    csv_filename = latest_jsonl.stem.replace("extracted_games_full_", "games_detailed_") + ".csv"
    output_csv = extracted_dir / csv_filename
    
    # CSV headers
    headers = [
        'Game ID',
        'Date/Time',
        'Timestamp (ms)',
        'Peak Multiplier',
        'Rugged',
        'Game Version',
        'Server Seed',
        'Server Seed Hash',
        'Total Trades',
        'Total Sidebets',
        'Total Price Ticks',
        'Total Candles',
        'First Price',
        'Last Price',
        'Max Price',
        'Min Price',
    ]
    
    games_written = 0
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        with open(latest_jsonl, 'r', encoding='utf-8') as f:
            for line in f:
                game = json.loads(line.strip())
                
                # Extract fields
                game_id = game.get('id', 'N/A')
                timestamp = game.get('timestamp', 0)
                date_time = format_timestamp(timestamp)
                peak = game.get('peakMultiplier', 0.0)
                rugged = 'Yes' if game.get('rugged', False) else 'No'
                version = game.get('gameVersion', 'N/A')
                
                # Provably fair data
                pf = game.get('provablyFair', {})
                server_seed = pf.get('serverSeed', 'N/A')
                server_seed_hash = pf.get('serverSeedHash', 'N/A')
                
                # Counts
                trades_count = len(game.get('globalTrades', []))
                sidebets_count = len(game.get('globalSidebets', []))
                
                # Price data
                prices = game.get('prices', [])
                price_ticks = len(prices)
                first_price = prices[0] if prices else 0
                last_price = prices[-1] if prices else 0
                max_price = max(prices) if prices else 0
                min_price = min(prices) if prices else 0
                
                # Candles
                candles = game.get('candles', [])
                candles_count = len(candles)
                
                row = [
                    game_id,
                    date_time,
                    timestamp,
                    f"{peak:.4f}",
                    rugged,
                    version,
                    server_seed,
                    server_seed_hash,
                    trades_count,
                    sidebets_count,
                    price_ticks,
                    candles_count,
                    f"{first_price:.4f}" if first_price else '0',
                    f"{last_price:.4f}" if last_price else '0',
                    f"{max_price:.4f}" if max_price else '0',
                    f"{min_price:.4f}" if min_price else '0',
                ]
                
                writer.writerow(row)
                games_written += 1
    
    print(f"✓ Wrote {games_written} games to {csv_filename}")
    print(f"Location: {output_csv}")


if __name__ == "__main__":
    main()
