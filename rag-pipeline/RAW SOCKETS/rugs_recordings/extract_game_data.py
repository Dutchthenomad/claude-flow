#!/usr/bin/env python3
"""
Extract game data from raw websocket capture JSONL files.

This script searches through raw websocket captures for gameStateUpdate events
containing gameHistory data, extracts complete game records, and outputs them
in a chronological list with statistics.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def parse_jsonl_file(filepath: str) -> List[Dict[str, Any]]:
    """Parse a JSONL file and extract all gameHistory records."""
    games = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    event = json.loads(line)
                    
                    # Check if this is a gameStateUpdate event with gameHistory
                    if (event.get('event') == 'gameStateUpdate' and 
                        'data' in event and 
                        'gameHistory' in event['data']):
                        
                        game_history = event['data']['gameHistory']
                        if isinstance(game_history, list):
                            games.extend(game_history)
                            
                except json.JSONDecodeError as e:
                    print(f"  Warning: JSON error in {os.path.basename(filepath)} line {line_num}: {e}")
                except Exception as e:
                    print(f"  Warning: Error processing {os.path.basename(filepath)} line {line_num}: {e}")
                    
    except Exception as e:
        print(f"  Error reading file {filepath}: {e}")
    
    return games


def extract_all_games(raw_captures_dir: str) -> tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Extract all games from all JSONL files in the directory."""
    all_games = []
    files_processed = {}
    
    raw_captures_path = Path(raw_captures_dir)
    
    # Find all JSONL files
    jsonl_files = sorted(raw_captures_path.glob('*.jsonl'))
    
    print(f"Found {len(jsonl_files)} JSONL files to process")
    print()
    
    for jsonl_file in jsonl_files:
        # Skip CDP files and other non-raw files if they don't have game data
        filename = jsonl_file.name
        print(f"Processing: {filename}")
        
        games = parse_jsonl_file(str(jsonl_file))
        
        if games:
            all_games.extend(games)
            files_processed[filename] = len(games)
            print(f"  ✓ Extracted {len(games)} games")
        else:
            print(f"  - No games found")
        print()
    
    return all_games, files_processed


def deduplicate_games(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate games based on game ID."""
    seen_ids = set()
    unique_games = []
    
    for game in games:
        game_id = game.get('id')
        if game_id and game_id not in seen_ids:
            seen_ids.add(game_id)
            unique_games.append(game)
    
    return unique_games


def sort_games_chronologically(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort games by timestamp (ascending - oldest first)."""
    return sorted(games, key=lambda g: g.get('timestamp', 0))


def format_timestamp(ts_ms: int) -> str:
    """Convert millisecond timestamp to readable datetime string."""
    try:
        dt = datetime.fromtimestamp(ts_ms / 1000.0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts_ms)


def format_game_id_date(game_id: str) -> str:
    """Extract date from game ID (format: YYYYMMDD-hash)."""
    try:
        date_part = game_id.split('-')[0]
        if len(date_part) == 8:
            return f"{date_part[0:4]}-{date_part[4:6]}-{date_part[6:8]}"
        return date_part
    except:
        return game_id


def generate_summary(games: List[Dict[str, Any]], files_processed: Dict[str, int]) -> str:
    """Generate summary statistics."""
    if not games:
        return "No games found."
    
    timestamps = [g.get('timestamp', 0) for g in games if g.get('timestamp')]
    
    earliest = min(timestamps) if timestamps else 0
    latest = max(timestamps) if timestamps else 0
    
    summary = []
    summary.append("=" * 80)
    summary.append("GAME DATA EXTRACTION SUMMARY")
    summary.append("=" * 80)
    summary.append("")
    summary.append(f"Total games found: {len(games)}")
    summary.append(f"Date range: {format_timestamp(earliest)} to {format_timestamp(latest)}")
    summary.append("")
    summary.append(f"Files processed: {len(files_processed)}")
    summary.append("")
    summary.append("Games per file:")
    for filename, count in sorted(files_processed.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            summary.append(f"  {filename}: {count} games")
    summary.append("")
    
    # Additional statistics
    rugged_count = sum(1 for g in games if g.get('rugged', False))
    not_rugged_count = len(games) - rugged_count
    
    summary.append(f"Games that rugged: {rugged_count} ({rugged_count/len(games)*100:.1f}%)")
    summary.append(f"Games that didn't rug: {not_rugged_count} ({not_rugged_count/len(games)*100:.1f}%)")
    summary.append("")
    
    # Peak multiplier stats
    peak_multipliers = [g.get('peakMultiplier', 0) for g in games if g.get('peakMultiplier')]
    if peak_multipliers:
        avg_peak = sum(peak_multipliers) / len(peak_multipliers)
        max_peak = max(peak_multipliers)
        min_peak = min(peak_multipliers)
        summary.append(f"Peak multiplier stats:")
        summary.append(f"  Average: {avg_peak:.4f}x")
        summary.append(f"  Maximum: {max_peak:.4f}x")
        summary.append(f"  Minimum: {min_peak:.4f}x")
        summary.append("")
    
    summary.append("=" * 80)
    return "\n".join(summary)


def generate_markdown_table(games: List[Dict[str, Any]], max_rows: int = 100) -> str:
    """Generate markdown table of game data."""
    if not games:
        return "No games to display."
    
    lines = []
    lines.append("")
    lines.append("## Game Records (Chronological)")
    lines.append("")
    
    # Show warning if truncating
    if len(games) > max_rows:
        lines.append(f"**Note:** Showing first {max_rows} of {len(games)} games. ")
        lines.append(f"See `extracted_games_full.jsonl` for complete data.")
        lines.append("")
    
    # Table header
    lines.append("| # | Date/Time | Game ID | Peak Multiplier | Rugged | Trades | Sidebets | Server Seed (first 16 chars) |")
    lines.append("|---|-----------|---------|-----------------|--------|--------|----------|------------------------------|")
    
    # Table rows
    for i, game in enumerate(games[:max_rows], 1):
        game_id = game.get('id', 'N/A')
        timestamp = game.get('timestamp', 0)
        date_time = format_timestamp(timestamp)
        peak = game.get('peakMultiplier', 0.0)
        rugged = "Yes" if game.get('rugged', False) else "No"
        
        # Count trades and sidebets
        trades_count = len(game.get('globalTrades', []))
        sidebets_count = len(game.get('globalSidebets', []))
        
        # Get server seed (abbreviated)
        server_seed = game.get('provablyFair', {}).get('serverSeed', 'N/A')
        if len(server_seed) > 16:
            server_seed = server_seed[:16] + "..."
        
        lines.append(f"| {i} | {date_time} | {game_id} | {peak:.4f}x | {rugged} | {trades_count} | {sidebets_count} | {server_seed} |")
    
    lines.append("")
    return "\n".join(lines)


def save_full_data(games: List[Dict[str, Any]], output_file: str):
    """Save complete game data as JSONL."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for game in games:
                f.write(json.dumps(game, ensure_ascii=False) + '\n')
        print(f"✓ Full data saved to: {output_file}")
    except Exception as e:
        print(f"✗ Error saving full data: {e}")


def save_summary_report(summary: str, table: str, output_file: str):
    """Save summary report as markdown."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
            f.write("\n\n")
            f.write(table)
        print(f"✓ Summary report saved to: {output_file}")
    except Exception as e:
        print(f"✗ Error saving summary report: {e}")


def main():
    """Main extraction process."""
    print("=" * 80)
    print("RUGS.FUN GAME DATA EXTRACTOR")
    print("=" * 80)
    print()
    
    # Determine the raw captures directory
    script_dir = Path(__file__).parent
    raw_captures_dir = script_dir / "raw_captures"
    
    if not raw_captures_dir.exists():
        print(f"Error: Directory not found: {raw_captures_dir}")
        return
    
    print(f"Scanning directory: {raw_captures_dir}")
    print()
    
    # Extract all games
    all_games, files_processed = extract_all_games(str(raw_captures_dir))
    
    print("=" * 80)
    print(f"Extracted {len(all_games)} total game records")
    print()
    
    # Deduplicate
    print("Deduplicating games...")
    unique_games = deduplicate_games(all_games)
    print(f"✓ Found {len(unique_games)} unique games")
    print()
    
    # Sort chronologically
    print("Sorting chronologically...")
    sorted_games = sort_games_chronologically(unique_games)
    print(f"✓ Sorted {len(sorted_games)} games by timestamp")
    print()
    
    # Generate outputs
    print("Generating reports...")
    print()
    
    summary = generate_summary(sorted_games, files_processed)
    print(summary)
    print()
    
    table = generate_markdown_table(sorted_games, max_rows=100)
    
    # Save outputs
    output_dir = script_dir / "extracted_data"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    full_data_file = output_dir / f"extracted_games_full_{timestamp}.jsonl"
    summary_report_file = output_dir / f"game_extraction_report_{timestamp}.md"
    
    print("Saving output files...")
    save_full_data(sorted_games, str(full_data_file))
    save_summary_report(summary, table, str(summary_report_file))
    print()
    
    print("=" * 80)
    print("EXTRACTION COMPLETE")
    print("=" * 80)
    print()
    print("Output files:")
    print(f"  1. Full data (JSONL): {full_data_file.name}")
    print(f"  2. Summary report (MD): {summary_report_file.name}")
    print()
    print(f"Location: {output_dir}")
    print()


if __name__ == "__main__":
    main()
