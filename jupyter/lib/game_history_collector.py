"""
Game History Collector - Server-side ML/RL data collection

Replaces passive CDP WebSocket recording with active gameHistory[] collection
from gameStateUpdate events. This rolling window of recent completed games
provides high-value training data with zero manual effort.

Key Features:
- Automatic deduplication by gameId
- Rolling window tracking (~10 games)
- JSONL storage compatible with existing recordings
- Passive collection during any live session
- Full game data: prices, trades, sidebets, provablyFair

Usage:
    from jupyter.lib import GameHistoryCollector
    
    collector = GameHistoryCollector()
    
    # Option 1: Standalone collection
    collector.connect()
    collector.start_collecting()
    # ... let it run ...
    collector.stop_collecting()
    
    # Option 2: Integrate with CDPCapture
    from jupyter.lib import CDPCapture
    capture = CDPCapture()
    capture.connect()
    
    collector.attach_to_capture(capture)
    # Games automatically collected from gameStateUpdate events
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from collections import deque


class GameHistoryCollector:
    """
    Collects historical game data from gameHistory[] rolling window.
    
    Monitors gameStateUpdate events and extracts completed games from
    the gameHistory[] array, automatically deduplicating by gameId.
    """
    
    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        auto_save: bool = True,
        max_memory_games: int = 1000
    ):
        """
        Initialize game history collector.
        
        Args:
            storage_dir: Directory for storing collected games (default: ~/rugs_recordings/game_history)
            auto_save: Automatically save games to disk as they're collected
            max_memory_games: Maximum number of games to keep in memory
        """
        # Storage configuration
        if storage_dir is None:
            from jupyter.notebooks._paths import RUGS_RECORDINGS_DIR
            storage_dir = RUGS_RECORDINGS_DIR / "game_history"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.auto_save = auto_save
        self.max_memory_games = max_memory_games
        
        # State tracking
        self.seen_game_ids: Set[str] = set()
        self.collected_games: deque = deque(maxlen=max_memory_games)
        self.is_collecting = False
        
        # Statistics
        self.stats = {
            'total_collected': 0,
            'duplicates_skipped': 0,
            'collection_started': None,
            'last_game_collected': None
        }
        
        # Session file for current collection run
        self._session_file = None
        self._cdp_capture = None
        
        # Load previously seen game IDs to avoid re-collecting
        self._load_seen_game_ids()
    
    def _load_seen_game_ids(self):
        """Load previously collected game IDs from storage directory."""
        if not self.storage_dir.exists():
            return
        
        for filepath in self.storage_dir.glob("*.jsonl"):
            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.strip():
                            game = json.loads(line)
                            if 'id' in game:
                                self.seen_game_ids.add(game['id'])
            except Exception as e:
                print(f"Warning: Could not load game IDs from {filepath}: {e}")
    
    def start_collecting(self, session_name: Optional[str] = None):
        """
        Start collecting games.
        
        Args:
            session_name: Optional name for this collection session
        """
        if self.is_collecting:
            print("Already collecting games")
            return
        
        self.is_collecting = True
        self.stats['collection_started'] = datetime.now().isoformat()
        
        # Create session file
        if self.auto_save:
            if session_name is None:
                session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            session_file = self.storage_dir / f"{session_name}.jsonl"
            self._session_file = open(session_file, 'a')
            print(f"Collecting games to: {session_file}")
        
        print("Game history collection started")
    
    def stop_collecting(self) -> Dict[str, Any]:
        """
        Stop collecting games and return statistics.
        
        Returns:
            Dictionary with collection statistics
        """
        if not self.is_collecting:
            print("Not currently collecting")
            return self.stats
        
        self.is_collecting = False
        
        # Close session file
        if self._session_file:
            self._session_file.close()
            self._session_file = None
        
        print(f"Collection stopped. Total collected: {self.stats['total_collected']}")
        return self.stats.copy()
    
    def process_game_state_update(self, event: Dict[str, Any]):
        """
        Process a gameStateUpdate event to extract gameHistory.
        
        Args:
            event: gameStateUpdate event data
        """
        if not self.is_collecting:
            return
        
        # Extract gameHistory array from event
        data = event.get('data', {})
        game_history = data.get('gameHistory', [])
        
        if not game_history:
            return
        
        # Process each game in the history
        for game in game_history:
            self._process_game(game)
    
    def _process_game(self, game: Dict[str, Any]):
        """
        Process a single game from gameHistory array.
        
        Args:
            game: Game data from gameHistory[]
        """
        game_id = game.get('id')
        
        if not game_id:
            return
        
        # Check for duplicate
        if game_id in self.seen_game_ids:
            self.stats['duplicates_skipped'] += 1
            return
        
        # Mark as seen
        self.seen_game_ids.add(game_id)
        
        # Add metadata
        game_record = {
            **game,
            'collected_at': datetime.now().isoformat(),
            'source': 'gameHistory_rolling_window'
        }
        
        # Store in memory
        self.collected_games.append(game_record)
        
        # Update statistics
        self.stats['total_collected'] += 1
        self.stats['last_game_collected'] = game_id
        
        # Auto-save if enabled
        if self.auto_save and self._session_file:
            self._session_file.write(json.dumps(game_record) + '\n')
            self._session_file.flush()
    
    def attach_to_capture(self, cdp_capture):
        """
        Attach to an existing CDPCapture instance.
        
        Args:
            cdp_capture: CDPCapture instance to attach to
        """
        self._cdp_capture = cdp_capture
        
        # Register callback for gameStateUpdate events
        original_callback = cdp_capture._on_event_callback
        
        def combined_callback(event):
            # Process for game history collection
            if event.get('event_name') == 'gameStateUpdate':
                self.process_game_state_update(event)
            
            # Call original callback if exists
            if original_callback:
                original_callback(event)
        
        cdp_capture.on_event(combined_callback)
        
        # Start collecting
        if not self.is_collecting:
            self.start_collecting("cdp_integrated")
        
        print(f"GameHistoryCollector attached to CDPCapture")
    
    def get_collected_games(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get collected games from memory.
        
        Args:
            limit: Maximum number of games to return (most recent)
        
        Returns:
            List of game records
        """
        games = list(self.collected_games)
        if limit:
            games = games[-limit:]
        return games
    
    def get_game_by_id(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific game by ID from memory.
        
        Args:
            game_id: Game ID to search for
        
        Returns:
            Game record or None if not found
        """
        for game in self.collected_games:
            if game.get('id') == game_id:
                return game
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            **self.stats,
            'games_in_memory': len(self.collected_games),
            'unique_games_seen': len(self.seen_game_ids),
            'is_collecting': self.is_collecting
        }
    
    def export_for_rl_training(
        self,
        output_file: Optional[Path] = None,
        include_fields: Optional[List[str]] = None
    ) -> Path:
        """
        Export collected games in format suitable for RL training.
        
        Args:
            output_file: Output file path (default: auto-generated)
            include_fields: List of fields to include (default: all)
        
        Returns:
            Path to exported file
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.storage_dir / f"rl_export_{timestamp}.jsonl"
        
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        games = self.get_collected_games()
        
        with open(output_file, 'w') as f:
            for game in games:
                # Filter fields if specified
                if include_fields:
                    filtered_game = {k: v for k, v in game.items() if k in include_fields}
                else:
                    filtered_game = game
                
                f.write(json.dumps(filtered_game) + '\n')
        
        print(f"Exported {len(games)} games to: {output_file}")
        return output_file
    
    def clear_memory(self):
        """Clear in-memory game collection (keeps disk storage)."""
        self.collected_games.clear()
        print("In-memory game collection cleared")
    
    def validate_game_structure(self, sample_size: int = 10) -> Dict[str, Any]:
        """
        Validate the structure of collected games.
        
        Args:
            sample_size: Number of games to sample for validation
        
        Returns:
            Dictionary with field analysis
        """
        games = self.get_collected_games(limit=sample_size)
        
        if not games:
            return {'error': 'No games collected yet'}
        
        # Analyze fields across all games
        field_counts = {}
        field_types = {}
        
        for game in games:
            for field, value in game.items():
                field_counts[field] = field_counts.get(field, 0) + 1
                
                value_type = type(value).__name__
                if field not in field_types:
                    field_types[field] = set()
                field_types[field].add(value_type)
        
        # Build report
        fields = {}
        for field in sorted(field_counts.keys()):
            fields[field] = {
                'present_in': f"{field_counts[field]}/{len(games)} games",
                'types': list(field_types[field]),
                'coverage': f"{(field_counts[field]/len(games)*100):.1f}%"
            }
        
        return {
            'games_analyzed': len(games),
            'fields': fields,
            'total_unique_fields': len(fields)
        }
    
    def __enter__(self):
        """Context manager entry."""
        self.start_collecting()
        return self
    
    def __exit__(self, *args):
        """Context manager exit."""
        self.stop_collecting()


class MockGameHistoryCollector(GameHistoryCollector):
    """
    Mock collector for testing without live connection.
    Simulates gameHistory collection with synthetic data.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mock_game_counter = 0
    
    def start_collecting(self, session_name: Optional[str] = None):
        """Start mock collection."""
        super().start_collecting(session_name or "mock_session")
        self._generate_mock_games()
    
    def _generate_mock_games(self, count: int = 5):
        """Generate mock game data."""
        import random
        
        for i in range(count):
            self._mock_game_counter += 1
            
            game_id = f"20251224-mock{self._mock_game_counter:04d}"
            
            # Generate mock price history
            prices = [1.0]
            current_price = 1.0
            
            for _ in range(random.randint(20, 100)):
                current_price *= random.uniform(0.98, 1.05)
                prices.append(round(current_price, 4))
            
            rug_point = prices[-1]
            
            mock_game = {
                'id': game_id,
                'timestamp': int(time.time() * 1000) - random.randint(0, 3600000),
                'prices': prices,
                'rugged': True,
                'rugPoint': rug_point,
                'peakMultiplier': max(prices),
                'gameVersion': 'mock-v1'
            }
            
            self._process_game(mock_game)
        
        print(f"Generated {count} mock games")
