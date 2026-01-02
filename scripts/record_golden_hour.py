#!/home/nomad/Desktop/claude-flow/rag-pipeline/.venv/bin/python
"""
Golden Hour Event Recorder
Records all WebSocket events from rugs.fun during Golden Hour events.

Usage:
    python scripts/record_golden_hour.py

    # Or with custom output:
    python scripts/record_golden_hour.py --output ~/rugs_recordings/golden_hour_2025-12-28.jsonl

Press Ctrl+C to stop recording.
"""

import argparse
import json
import signal
import sys
from datetime import datetime
from pathlib import Path

try:
    import socketio
except ImportError:
    print("ERROR: python-socketio not installed")
    print("Run: pip install 'python-socketio[client]'")
    sys.exit(1)


class GoldenHourRecorder:
    """Records all rugs.fun WebSocket events to JSONL file."""

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.sio = socketio.Client(logger=False, engineio_logger=False)
        self.event_count = 0
        self.game_count = 0
        self.golden_hour_active = False
        self.start_time = None
        self.file_handle = None

        # Track game state
        self.current_game_id = None
        self.games_recorded = []

        self._setup_handlers()

    def _setup_handlers(self):
        """Register Socket.IO event handlers."""

        @self.sio.event
        def connect():
            self.start_time = datetime.now()
            print(f"\n{'='*60}")
            print(f"CONNECTED to backend.rugs.fun")
            print(f"Recording to: {self.output_path}")
            print(f"Started: {self.start_time.isoformat()}")
            print(f"{'='*60}")
            print(f"\nPress Ctrl+C to stop recording.\n")

        @self.sio.event
        def disconnect():
            print(f"\nDISCONNECTED after {self.event_count} events")

        # Catch ALL events with wildcard handler
        @self.sio.on('*')
        def catch_all(event, *args):
            self._record_event(event, args)

        # Explicitly register known events (some Socket.IO versions need this)
        known_events = [
            'gameStateUpdate',
            'gameStatePlayerUpdate',
            'playerUpdate',
            'standard/newTrade',
            'goldenHourUpdate',
            'goldenHourDrawing',
            'currentSidebet',
            'currentSidebetResult',
            'usernameStatus',
            'playerLeaderboardPosition',
            'rugRoyaleUpdate',
            'newChatMessage',
            'rugPassQuestCompleted',
        ]

        for event_name in known_events:
            self.sio.on(event_name, lambda *args, e=event_name: self._record_event(e, args))

    def _record_event(self, event_name: str, args: tuple):
        """Record a single event to JSONL file."""
        timestamp = datetime.now()

        # Build record
        record = {
            'ts': timestamp.isoformat(),
            'ts_ms': int(timestamp.timestamp() * 1000),
            'event': event_name,
            'data': list(args) if args else None
        }

        # Write to file
        if self.file_handle:
            self.file_handle.write(json.dumps(record) + '\n')
            self.file_handle.flush()

        self.event_count += 1

        # Track special events
        self._track_event(event_name, args)

        # Progress indicator
        if self.event_count % 100 == 0:
            elapsed = (timestamp - self.start_time).total_seconds()
            rate = self.event_count / elapsed if elapsed > 0 else 0
            print(f"  [{self.event_count:,} events | {rate:.1f}/sec | {self.game_count} games]")

    def _track_event(self, event_name: str, args: tuple):
        """Track interesting events for live display."""

        if event_name == 'goldenHourUpdate' and args:
            data = args[-1] if args else {}
            status = data.get('status', 'UNKNOWN')
            is_golden = data.get('currentGameIsGolden', False)

            if status == 'ACTIVE' and not self.golden_hour_active:
                self.golden_hour_active = True
                print(f"\n  GOLDEN HOUR ACTIVE!")

            if is_golden:
                print(f"  Current game IS GOLDEN")

        elif event_name == 'gameStateUpdate' and args:
            data = args[-1] if args else {}
            game_id = data.get('gameId')
            active = data.get('active', False)
            rugged = data.get('rugged', False)
            tick = data.get('tickCount', 0)
            price = data.get('price', 1.0)

            # New game started
            if game_id != self.current_game_id and active:
                self.current_game_id = game_id
                self.game_count += 1
                print(f"\n  GAME {self.game_count}: {game_id}")

            # Game rugged
            if rugged and game_id == self.current_game_id:
                print(f"    RUGGED at tick {tick}, price {price:.4f}")
                self.games_recorded.append({
                    'game_id': game_id,
                    'rug_tick': tick,
                    'rug_price': price
                })

        elif event_name == 'goldenHourDrawing' and args:
            print(f"\n  GOLDEN HOUR DRAWING EVENT!")

    def start(self):
        """Connect and start recording."""
        self.file_handle = open(self.output_path, 'a')

        # Write session header
        header = {
            'session_start': datetime.now().isoformat(),
            'type': 'golden_hour_recording',
            'version': '1.0'
        }
        self.file_handle.write(f"# Session: {json.dumps(header)}\n")
        self.file_handle.flush()

        try:
            print("Connecting to backend.rugs.fun...")
            self.sio.connect(
                'https://backend.rugs.fun',
                transports=['polling', 'websocket'],
                wait_timeout=10,
                headers={
                    'Origin': 'https://rugs.fun',
                    'Referer': 'https://rugs.fun/',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                },
                socketio_path='/socket.io/'
            )
            self.sio.wait()
        except KeyboardInterrupt:
            print("\n\nStopping recording...")
        finally:
            self.stop()

    def stop(self):
        """Disconnect and finalize recording."""
        # Close file first to prevent writes during disconnect
        if self.file_handle and not self.file_handle.closed:
            try:
                # Write session footer
                footer = {
                    'session_end': datetime.now().isoformat(),
                    'total_events': self.event_count,
                    'total_games': self.game_count,
                    'games': self.games_recorded
                }
                self.file_handle.write(f"# Session End: {json.dumps(footer)}\n")
                self.file_handle.close()
            except:
                pass
            self.file_handle = None

        if self.sio.connected:
            try:
                self.sio.disconnect()
            except:
                pass

        if False:  # Skip duplicate footer write
            # Write session footer
            footer = {
                'session_end': datetime.now().isoformat(),
                'total_events': self.event_count,
                'total_games': self.game_count,
                'games': self.games_recorded
            }
            self.file_handle.write(f"# Session End: {json.dumps(footer)}\n")
            self.file_handle.close()

        # Print summary
        print(f"\n{'='*60}")
        print(f"RECORDING COMPLETE")
        print(f"{'='*60}")
        print(f"Total events: {self.event_count:,}")
        print(f"Total games:  {self.game_count}")
        print(f"Output file:  {self.output_path}")

        if self.games_recorded:
            ticks = [g['rug_tick'] for g in self.games_recorded]
            avg_tick = sum(ticks) / len(ticks)
            print(f"\nGolden Hour Game Stats:")
            print(f"  Games recorded: {len(ticks)}")
            print(f"  Avg rug tick:   {avg_tick:.1f}")
            print(f"  Min rug tick:   {min(ticks)}")
            print(f"  Max rug tick:   {max(ticks)}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Record Golden Hour events from rugs.fun')
    parser.add_argument(
        '--output', '-o',
        default=f"~/rugs_recordings/golden_hour_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.jsonl",
        help='Output JSONL file path'
    )
    args = parser.parse_args()

    output_path = Path(args.output).expanduser()

    recorder = GoldenHourRecorder(str(output_path))

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n\nReceived interrupt signal...")
        recorder.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    recorder.start()


if __name__ == '__main__':
    main()
