#!/usr/bin/env python3
"""
Example: Verify provably fair data from extracted games.

This script demonstrates how to verify that game outcomes were provably fair
by checking that the revealed server seed matches its pre-game hash.
"""

import json
import hashlib
from pathlib import Path


def verify_server_seed(server_seed: str, server_seed_hash: str) -> bool:
    """
    Verify that a server seed matches its hash.
    
    Args:
        server_seed: The revealed server seed (hex string)
        server_seed_hash: The pre-game hash of the server seed (hex string)
    
    Returns:
        True if the seed matches the hash, False otherwise
    """
    # Convert hex string to bytes
    seed_bytes = bytes.fromhex(server_seed)
    
    # Calculate SHA-256 hash
    calculated_hash = hashlib.sha256(seed_bytes).hexdigest()
    
    # Compare with provided hash
    return calculated_hash == server_seed_hash


def main():
    """Verify provably fair data for all extracted games."""
    # Find the most recent extracted file
    extracted_dir = Path(__file__).parent / "extracted_data"
    jsonl_files = sorted(extracted_dir.glob("extracted_games_full_*.jsonl"))
    
    if not jsonl_files:
        print("No extracted JSONL files found!")
        return
    
    latest_jsonl = jsonl_files[-1]
    print(f"Verifying games from: {latest_jsonl.name}")
    print("=" * 80)
    print()
    
    verified_count = 0
    failed_count = 0
    missing_data_count = 0
    total_count = 0
    
    with open(latest_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            total_count += 1
            game = json.loads(line.strip())
            
            game_id = game.get('id', 'Unknown')
            pf = game.get('provablyFair', {})
            
            server_seed = pf.get('serverSeed')
            server_seed_hash = pf.get('serverSeedHash')
            
            if not server_seed or not server_seed_hash:
                missing_data_count += 1
                print(f"⚠️  Game {game_id}: Missing provably fair data")
                continue
            
            # Verify the seed
            is_valid = verify_server_seed(server_seed, server_seed_hash)
            
            if is_valid:
                verified_count += 1
                if verified_count <= 5:  # Show first 5 as examples
                    print(f"✓  Game {game_id}: VERIFIED")
                    print(f"   Server Seed: {server_seed[:32]}...")
                    print(f"   Hash: {server_seed_hash[:32]}...")
                    print()
            else:
                failed_count += 1
                print(f"✗  Game {game_id}: VERIFICATION FAILED!")
                print(f"   Server Seed: {server_seed[:32]}...")
                print(f"   Expected Hash: {server_seed_hash[:32]}...")
                print()
    
    # Summary
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total games: {total_count}")
    
    if total_count > 0:
        print(f"Verified: {verified_count} ({verified_count/total_count*100:.1f}%)")
        print(f"Failed: {failed_count} ({failed_count/total_count*100:.1f}%)")
        print(f"Missing data: {missing_data_count} ({missing_data_count/total_count*100:.1f}%)")
    else:
        print("No games found to verify.")
    print()
    
    if verified_count == total_count:
        print("🎉 ALL GAMES VERIFIED! All server seeds match their hashes.")
    elif failed_count > 0:
        print("⚠️  FINDING: All games failed SHA-256 verification!")
        print()
        print("POSSIBLE REASONS:")
        print("1. Server seed may need to be salted/prefixed before hashing")
        print("2. Different hash algorithm or additional data may be included")
        print("3. Game version differences (v3 vs older versions)")
        print("4. Hash format/encoding issues (UTF-8 vs hex vs bytes)")
        print()
        print("RECOMMENDATION: Review Rugs.fun provably fair documentation")
        print("to understand the exact hashing procedure used.")
    else:
        print("ℹ️  Some games are missing provably fair data.")


if __name__ == "__main__":
    main()
