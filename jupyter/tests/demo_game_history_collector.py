#!/usr/bin/env python3
"""
Demo script for GameHistoryCollector

Demonstrates basic usage and functionality without requiring pytest.
"""

import sys
import json
import tempfile
import time
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.game_history_collector import GameHistoryCollector, MockGameHistoryCollector


def test_basic_collection():
    """Test basic game collection."""
    print("\n=== Test 1: Basic Collection ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = GameHistoryCollector(storage_dir=tmpdir, auto_save=False)
        collector.start_collecting()
        
        # Create mock games
        games = [
            {
                'id': f'demo-game-{i:03d}',
                'timestamp': int(time.time() * 1000) + i * 1000,
                'prices': [1.0, 1.5 + i * 0.1, 2.0 + i * 0.2],
                'rugged': True,
                'rugPoint': 2.0 + i * 0.2
            }
            for i in range(5)
        ]
        
        # Process games
        for game in games:
            collector._process_game(game)
        
        stats = collector.get_statistics()
        print(f"✓ Collected {stats['total_collected']} games")
        print(f"✓ Games in memory: {stats['games_in_memory']}")
        print(f"✓ Unique games: {stats['unique_games_seen']}")
        
        collector.stop_collecting()
        assert stats['total_collected'] == 5, "Should collect all games"
        print("✓ Test passed!")


def test_deduplication():
    """Test game deduplication."""
    print("\n=== Test 2: Deduplication ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = GameHistoryCollector(storage_dir=tmpdir, auto_save=False)
        collector.start_collecting()
        
        game = {
            'id': 'duplicate-test-001',
            'timestamp': int(time.time() * 1000),
            'prices': [1.0, 1.5],
            'rugged': True,
            'rugPoint': 1.5
        }
        
        # Process same game 3 times
        collector._process_game(game)
        collector._process_game(game)
        collector._process_game(game)
        
        stats = collector.get_statistics()
        print(f"✓ Total collected: {stats['total_collected']}")
        print(f"✓ Duplicates skipped: {collector.stats['duplicates_skipped']}")
        
        assert stats['total_collected'] == 1, "Should only collect once"
        assert collector.stats['duplicates_skipped'] == 2, "Should skip 2 duplicates"
        print("✓ Test passed!")


def test_game_state_update_processing():
    """Test processing gameStateUpdate events."""
    print("\n=== Test 3: GameStateUpdate Processing ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = GameHistoryCollector(storage_dir=tmpdir, auto_save=False)
        collector.start_collecting()
        
        # Mock gameStateUpdate event
        event = {
            'event_name': 'gameStateUpdate',
            'data': {
                'price': 1.5,
                'active': True,
                'gameHistory': [
                    {
                        'id': 'gsu-game-001',
                        'timestamp': 1234567890,
                        'prices': [1.0, 1.5, 2.0],
                        'rugged': True,
                        'rugPoint': 2.0
                    },
                    {
                        'id': 'gsu-game-002',
                        'timestamp': 1234567900,
                        'prices': [1.0, 1.2],
                        'rugged': True,
                        'rugPoint': 1.2
                    }
                ]
            }
        }
        
        collector.process_game_state_update(event)
        
        stats = collector.get_statistics()
        print(f"✓ Extracted {stats['total_collected']} games from gameHistory[]")
        
        games = collector.get_collected_games()
        print(f"✓ Game IDs: {[g['id'] for g in games]}")
        
        assert stats['total_collected'] == 2, "Should extract both games"
        print("✓ Test passed!")


def test_persistence():
    """Test persistence to disk."""
    print("\n=== Test 4: Disk Persistence ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Session 1: Save games
        collector1 = GameHistoryCollector(storage_dir=tmpdir, auto_save=True)
        collector1.start_collecting("persist_session")
        
        game = {
            'id': 'persist-game-001',
            'timestamp': int(time.time() * 1000),
            'prices': [1.0, 1.5],
            'rugged': True,
            'rugPoint': 1.5
        }
        
        collector1._process_game(game)
        collector1.stop_collecting()
        
        # Check file was created
        jsonl_files = list(Path(tmpdir).glob("*.jsonl"))
        print(f"✓ Created {len(jsonl_files)} file(s)")
        
        # Session 2: Load and check
        collector2 = GameHistoryCollector(storage_dir=tmpdir, auto_save=False)
        
        print(f"✓ Loaded {len(collector2.seen_game_ids)} previously seen game IDs")
        assert 'persist-game-001' in collector2.seen_game_ids, "Should load previous IDs"
        
        # Verify content
        with open(jsonl_files[0], 'r') as f:
            saved_game = json.loads(f.read().strip())
            print(f"✓ Saved game ID: {saved_game['id']}")
            print(f"✓ Metadata added: collected_at={saved_game.get('collected_at', 'N/A')[:19]}")
            assert saved_game['id'] == 'persist-game-001'
        
        print("✓ Test passed!")


def test_mock_collector():
    """Test MockGameHistoryCollector."""
    print("\n=== Test 5: Mock Collector ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = MockGameHistoryCollector(storage_dir=tmpdir, auto_save=False)
        collector.start_collecting()
        
        stats = collector.get_statistics()
        print(f"✓ Mock generated {stats['total_collected']} games")
        
        games = collector.get_collected_games()
        if games:
            print(f"✓ Sample game ID: {games[0]['id']}")
            print(f"✓ Sample prices length: {len(games[0]['prices'])}")
        
        assert stats['total_collected'] > 0, "Should generate mock games"
        print("✓ Test passed!")


def test_validation():
    """Test game structure validation."""
    print("\n=== Test 6: Structure Validation ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = GameHistoryCollector(storage_dir=tmpdir, auto_save=False)
        collector.start_collecting()
        
        # Add games with varying fields
        games = [
            {
                'id': 'validate-001',
                'timestamp': 1234567890,
                'prices': [1.0, 1.5],
                'rugged': True,
                'rugPoint': 1.5
            },
            {
                'id': 'validate-002',
                'timestamp': 1234567900,
                'prices': [1.0, 2.0],
                'rugged': True,
                'rugPoint': 2.0,
                'peakMultiplier': 2.5
            }
        ]
        
        for game in games:
            collector._process_game(game)
        
        validation = collector.validate_game_structure(sample_size=10)
        
        print(f"✓ Analyzed {validation['games_analyzed']} games")
        print(f"✓ Found {validation['total_unique_fields']} unique fields")
        print(f"\nField coverage:")
        for field, info in validation['fields'].items():
            print(f"  - {field}: {info['coverage']} ({info['types']})")
        
        assert 'id' in validation['fields']
        assert 'prices' in validation['fields']
        print("✓ Test passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("GameHistoryCollector Demo & Verification")
    print("=" * 60)
    
    tests = [
        test_basic_collection,
        test_deduplication,
        test_game_state_update_processing,
        test_persistence,
        test_mock_collector,
        test_validation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ Test failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
