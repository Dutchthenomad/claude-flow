#!/usr/bin/env python3
"""
Extract and deduplicate game records from raw socket recording files.

This script:
1. Scans all JSONL files in raw_captures directory
2. Extracts gameHistory events from gameStateUpdate messages  
3. Deduplicates games by gameId
4. Sorts chronologically by timestamp
5. Outputs formatted results
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any


def parse_jsonl_file(filepath: Path) -> List[Dict[str, Any]]:
    """Parse a JSONL file and extract gameHistory records."""
    games = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    # Parse the JSON line
                    event = json.loads(line)
                    
                    # Check if this is a gameStateUpdate event
                    if isinstance(event, dict) and len(event) == 2:
                        # Socket.io format: [event_name, data]
                        if isinstance(event, list) and len(event) == 2:
                            event_name, event_data = event
                        else:
                            # Try to find nested structure
                            event_keys = list(event.keys())
                            if 'gameStateUpdate' in event_keys or any('game' in k.lower() for k in event_keys):
                                event_data = event
                            else:
                                continue
                    else:
                        event_data = event
                    
                    # Look for gameHistory in the event data
                    game_history = None
                    if isinstance(event_data, dict):
                        game_history = event_data.get('gameHistory')
                        
                        # Sometimes it's nested in different structures
                        if not game_history and 'data' in event_data:
                            nested_data = event_data['data']
                            if isinstance(nested_data, dict):
                                game_history = nested_data.get('gameHistory')
                    
                    # Extract games from gameHistory array
                    if game_history and isinstance(game_history, list):
                        for game in game_history:
                            if isinstance(game, dict) and 'id' in game and 'timestamp' in game:
                                games.append(game)
                                
                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse line {line_num} in {filepath.name}: {e}", file=sys.stderr)
                    continue
                except Exception as e:
                    print(f"Warning: Error processing line {line_num} in {filepath.name}: {e}", file=sys.stderr)
                    continue
    
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
    
    return games


def extract_games_from_directory(directory: Path) -> Dict[str, Dict[str, Any]]:
    """
    Extract all games from JSONL files in directory.
    Returns dict mapping gameId -> game record.
    """
    games_dict = {}
    files_processed = 0
    total_games_found = 0
    
    # Find all JSONL files
    jsonl_files = sorted(directory.glob('*.jsonl'))
    json_files = sorted(directory.glob('*.json'))
    all_files = jsonl_files + json_files
    
    print(f"Found {len(all_files)} data files to process")
    
    for filepath in all_files:
        print(f"Processing: {filepath.name}")
        games = parse_jsonl_file(filepath)
        total_games_found += len(games)
        
        # Deduplicate by gameId
        for game in games:
            game_id = game.get('id')
            if game_id:
                # Keep the first occurrence (or latest, depending on your preference)
                if game_id not in games_dict:
                    games_dict[game_id] = game
        
        files_processed += 1
        print(f"  - Found {len(games)} games, {len(games_dict)} unique so far")
    
    print(f"\nProcessed {files_processed} files")
    print(f"Total games found: {total_games_found}")
    print(f"Unique games (deduplicated): {len(games_dict)}")
    
    return games_dict


def format_timestamp(ts: int) -> str:
    """Convert timestamp milliseconds to readable datetime."""
    try:
        dt = datetime.fromtimestamp(ts / 1000.0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)


def format_game_id_date(game_id: str) -> str:
    """Extract date from gameId format: YYYYMMDD-hash"""
    try:
        date_part = game_id.split('-')[0]
        # Format: 20251212 -> 2025-12-12
        if len(date_part) == 8 and date_part.isdigit():
            return f"{date_part[0:4]}-{date_part[4:6]}-{date_part[6:8]}"
    except:
        pass
    return "N/A"


def generate_markdown_table(games: List[Dict[str, Any]], max_rows: int = 100) -> str:
    """Generate a markdown table with game information."""
    
    lines = [
        "# Extracted Game Records",
        "",
        f"**Total Games**: {len(games)}",
        "",
        "| # | Date/Time | gameId | serverSeed | serverSeedHash | peakMultiplier | rugged | finalTick | version |",
        "|---|-----------|--------|------------|----------------|----------------|--------|-----------|---------|"
    ]
    
    for i, game in enumerate(games[:max_rows], 1):
        game_id = game.get('id', 'N/A')
        timestamp = format_timestamp(game.get('timestamp', 0))
        
        # Extract provablyFair data
        provably_fair = game.get('provablyFair', {}) or {}
        server_seed = provably_fair.get('serverSeed', 'N/A')
        server_seed_hash = provably_fair.get('serverSeedHash', 'N/A')
        
        # Truncate hashes for display
        if server_seed != 'N/A' and len(server_seed) > 12:
            server_seed = server_seed[:8] + "..."
        if server_seed_hash != 'N/A' and len(server_seed_hash) > 12:
            server_seed_hash = server_seed_hash[:8] + "..."
        
        peak_multiplier = game.get('peakMultiplier', 'N/A')
        if isinstance(peak_multiplier, (int, float)):
            peak_multiplier = f"{peak_multiplier:.4f}"
        
        rugged = "Yes" if game.get('rugged') else "No"
        
        # Get final tick or game duration
        prices = game.get('prices', [])
        final_tick = len(prices) - 1 if prices else 'N/A'
        
        version = game.get('gameVersion', 'N/A')
        
        lines.append(
            f"| {i} | {timestamp} | {game_id} | {server_seed} | {server_seed_hash} | "
            f"{peak_multiplier} | {rugged} | {final_tick} | {version} |"
        )
    
    if len(games) > max_rows:
        lines.append("")
        lines.append(f"*Showing first {max_rows} of {len(games)} games. See full export file for all records.*")
    
    return "\n".join(lines)


def generate_statistics(games: List[Dict[str, Any]]) -> str:
    """Generate summary statistics."""
    if not games:
        return "No games found."
    
    # Calculate stats
    timestamps = [g.get('timestamp', 0) for g in games if g.get('timestamp')]
    earliest = min(timestamps) if timestamps else 0
    latest = max(timestamps) if timestamps else 0
    
    rugged_count = sum(1 for g in games if g.get('rugged'))
    not_rugged_count = len(games) - rugged_count
    
    # Peak multipliers
    multipliers = [g.get('peakMultiplier') for g in games if isinstance(g.get('peakMultiplier'), (int, float))]
    avg_multiplier = sum(multipliers) / len(multipliers) if multipliers else 0
    max_multiplier = max(multipliers) if multipliers else 0
    
    # Versions
    versions = defaultdict(int)
    for g in games:
        ver = g.get('gameVersion', 'unknown')
        versions[ver] += 1
    
    lines = [
        "# Game Data Statistics",
        "",
        f"**Total Unique Games**: {len(games)}",
        f"**Date Range**: {format_timestamp(earliest)} to {format_timestamp(latest)}",
        "",
        "## Outcomes",
        f"- Rugged: {rugged_count} ({rugged_count/len(games)*100:.1f}%)",
        f"- Not Rugged: {not_rugged_count} ({not_rugged_count/len(games)*100:.1f}%)",
        "",
        "## Multipliers",
        f"- Average Peak: {avg_multiplier:.4f}x",
        f"- Highest Peak: {max_multiplier:.4f}x",
        "",
        "## Game Versions",
    ]
    
    for ver, count in sorted(versions.items()):
        lines.append(f"- {ver}: {count} games")
    
    return "\n".join(lines)


def main():
    """Main extraction process."""
    # Determine the raw_captures directory
    script_dir = Path(__file__).parent
    raw_captures_dir = script_dir / 'raw_captures'
    
    if not raw_captures_dir.exists():
        print(f"Error: Directory not found: {raw_captures_dir}")
        sys.exit(1)
    
    print("=" * 70)
    print("Game History Extraction Tool")
    print("=" * 70)
    print()
    
    # Extract all games
    games_dict = extract_games_from_directory(raw_captures_dir)
    
    if not games_dict:
        print("\nNo games found!")
        sys.exit(1)
    
    # Sort by timestamp
    games_list = sorted(games_dict.values(), key=lambda g: g.get('timestamp', 0))
    
    print(f"\nSorted {len(games_list)} games chronologically")
    
    # Generate outputs
    output_dir = script_dir
    
    # 1. Full JSONL export
    output_jsonl = output_dir / 'extracted_games_full.jsonl'
    print(f"\nWriting full export to: {output_jsonl}")
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for game in games_list:
            json.dump(game, f)
            f.write('\n')
    
    # 2. Statistics report
    output_stats = output_dir / 'game_statistics.md'
    print(f"Writing statistics to: {output_stats}")
    stats_text = generate_statistics(games_list)
    with open(output_stats, 'w', encoding='utf-8') as f:
        f.write(stats_text)
    
    # 3. Markdown table with top 100
    output_table = output_dir / 'game_records_table.md'
    print(f"Writing table to: {output_table}")
    table_text = generate_markdown_table(games_list, max_rows=100)
    with open(output_table, 'w', encoding='utf-8') as f:
        f.write(table_text)
    
    print("\n" + "=" * 70)
    print("Extraction Complete!")
    print("=" * 70)
    print(f"\nFiles created:")
    print(f"  - {output_jsonl.name} - Full game data export ({len(games_list)} games)")
    print(f"  - {output_stats.name} - Summary statistics")
    print(f"  - {output_table.name} - Top 100 games table")
    print()


if __name__ == '__main__':
    main()
