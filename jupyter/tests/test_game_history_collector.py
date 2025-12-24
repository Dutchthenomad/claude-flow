"""
Tests for GameHistoryCollector

Tests the game history collection system including:
- Deduplication logic
- Rolling window handling
- Storage persistence
- Integration with CDPCapture
- Data structure validation
"""

import json
import tempfile
import time
from pathlib import Path
from datetime import datetime

import pytest

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.game_history_collector import GameHistoryCollector, MockGameHistoryCollector


class TestGameHistoryCollector:
    """Test basic GameHistoryCollector functionality."""
    
    def test_initialization(self, tmp_path):
        """Test collector initialization."""
        collector = GameHistoryCollector(storage_dir=tmp_path)
        
        assert collector.storage_dir == tmp_path
        assert collector.auto_save is True
        assert not collector.is_collecting
        assert collector.stats['total_collected'] == 0
        assert len(collector.seen_game_ids) == 0
    
    def test_start_stop_collecting(self, tmp_path):
        """Test starting and stopping collection."""
        collector = GameHistoryCollector(storage_dir=tmp_path)
        
        # Start collecting
        collector.start_collecting("test_session")
        assert collector.is_collecting
        assert collector.stats['collection_started'] is not None
        
        # Stop collecting
        stats = collector.stop_collecting()
        assert not collector.is_collecting
        assert 'total_collected' in stats
    
    def test_deduplication(self, tmp_path):
        """Test that duplicate games are filtered out."""
        collector = GameHistoryCollector(storage_dir=tmp_path, auto_save=False)
        collector.start_collecting()
        
        # Create a mock game
        game = {
            'id': 'test-game-001',
            'timestamp': int(time.time() * 1000),
            'prices': [1.0, 1.1, 1.2],
            'rugged': True,
            'rugPoint': 1.2
        }
        
        # Process same game twice
        collector._process_game(game)
        collector._process_game(game)
        
        # Should only collect once
        assert collector.stats['total_collected'] == 1
        assert collector.stats['duplicates_skipped'] == 1
        assert len(collector.collected_games) == 1
    
    def test_process_game_state_update(self, tmp_path):
        """Test processing gameStateUpdate events."""
        collector = GameHistoryCollector(storage_dir=tmp_path, auto_save=False)
        collector.start_collecting()
        
        # Mock gameStateUpdate event
        event = {
            'event_name': 'gameStateUpdate',
            'data': {
                'gameHistory': [
                    {
                        'id': 'game-001',
                        'timestamp': 1234567890,
                        'prices': [1.0, 1.5, 2.0],
                        'rugged': True,
                        'rugPoint': 2.0
                    },
                    {
                        'id': 'game-002',
                        'timestamp': 1234567900,
                        'prices': [1.0, 1.2],
                        'rugged': True,
                        'rugPoint': 1.2
                    }
                ]
            }
        }
        
        collector.process_game_state_update(event)
        
        # Should collect both games
        assert collector.stats['total_collected'] == 2
        assert len(collector.collected_games) == 2
        assert 'game-001' in collector.seen_game_ids
        assert 'game-002' in collector.seen_game_ids
    
    def test_auto_save(self, tmp_path):
        """Test automatic saving to disk."""
        collector = GameHistoryCollector(storage_dir=tmp_path, auto_save=True)
        collector.start_collecting("test_autosave")
        
        # Process a game
        game = {
            'id': 'test-game-autosave',
            'timestamp': int(time.time() * 1000),
            'prices': [1.0, 1.5],
            'rugged': True,
            'rugPoint': 1.5
        }
        
        collector._process_game(game)
        collector.stop_collecting()
        
        # Check that file was created
        jsonl_files = list(tmp_path.glob("*.jsonl"))
        assert len(jsonl_files) == 1
        
        # Verify content
        with open(jsonl_files[0], 'r') as f:
            saved_game = json.loads(f.read().strip())
            assert saved_game['id'] == 'test-game-autosave'
            assert 'collected_at' in saved_game
            assert saved_game['source'] == 'gameHistory_rolling_window'


class TestMockGameHistoryCollector:
    """Test MockGameHistoryCollector for testing without live connection."""
    
    def test_mock_collector_generates_games(self, tmp_path):
        """Test that mock collector generates synthetic games."""
        collector = MockGameHistoryCollector(storage_dir=tmp_path, auto_save=False)
        
        # Start should generate mock games
        collector.start_collecting()
        
        # Should have generated games
        assert collector.stats['total_collected'] > 0
        assert len(collector.collected_games) > 0
        
        # Verify game structure
        game = collector.collected_games[0]
        assert 'id' in game
        assert 'prices' in game
        assert 'rugged' in game
        assert game['id'].startswith('20251224-mock')


@pytest.fixture
def tmp_path():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
