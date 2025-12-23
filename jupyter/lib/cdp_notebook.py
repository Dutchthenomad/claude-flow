"""
CDP Notebook Integration
Chrome DevTools Protocol event capture for Jupyter notebooks.

Usage:
    from jupyter.lib import CDPCapture

    capture = CDPCapture()
    capture.connect()
    capture.start_recording("session.jsonl")

    # Later...
    capture.show_recent_events()
    capture.stop_recording()
    capture.disconnect()
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from collections import deque

# Optional: Rich display for notebooks
try:
    import pandas as pd
    from IPython.display import display, HTML, clear_output
    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False


class CDPCapture:
    """
    Chrome DevTools Protocol event capture for notebooks.

    Connects to Chrome running with --remote-debugging-port and
    intercepts WebSocket frames from rugs.fun backend.
    """

    def __init__(self, cdp_port: int = None, max_events: int = 10000):
        """
        Initialize CDP capture.

        Args:
            cdp_port: CDP port (default: from CDP_PORT env or 9222)
            max_events: Maximum events to keep in memory
        """
        self.cdp_port = cdp_port or int(os.environ.get('CDP_PORT', 9222))
        self.max_events = max_events

        self.events: deque = deque(maxlen=max_events)
        self.is_connected = False
        self._recording_file = None
        self._ws = None
        self._thread = None
        self._stop_event = threading.Event()
        self._on_event_callback: Optional[Callable] = None

        # Try to import pychrome for CDP connection
        try:
            import pychrome
            self._pychrome = pychrome
        except ImportError:
            self._pychrome = None

    def connect(self) -> bool:
        """
        Connect to Chrome CDP.

        Returns:
            True if connected successfully
        """
        if self._pychrome is None:
            print("Error: pychrome not installed")
            print("Run: pip install pychrome")
            return False

        try:
            # Connect to Chrome
            browser = self._pychrome.Browser(url=f"http://127.0.0.1:{self.cdp_port}")

            # Find rugs.fun tab
            tabs = browser.list_tab()
            rugs_tab = None

            for tab in tabs:
                if 'rugs.fun' in tab.get('url', ''):
                    rugs_tab = tab
                    break

            if not rugs_tab:
                print(f"No rugs.fun tab found in Chrome")
                print(f"Available tabs: {[t.get('url', '') for t in tabs]}")
                return False

            # Connect to tab
            tab = browser.activate_tab(rugs_tab['id'])
            tab.start()

            # Enable Network domain for WebSocket interception
            tab.Network.enable()

            # Set up WebSocket frame handler
            tab.Network.webSocketFrameReceived = self._on_ws_frame

            self._tab = tab
            self.is_connected = True

            print(f"Connected to Chrome CDP on port {self.cdp_port}")
            print(f"Monitoring: {rugs_tab.get('url', '')}")
            return True

        except Exception as e:
            print(f"Connection failed: {e}")
            print(f"\nMake sure Chrome is running with:")
            print(f"  --remote-debugging-port={self.cdp_port}")
            return False

    def _on_ws_frame(self, requestId, timestamp, response):
        """Handle incoming WebSocket frame."""
        try:
            payload = response.get('payloadData', '')

            # Parse Socket.IO frame format: 42["eventName", {...}]
            if payload.startswith('42['):
                event = self._parse_socketio_frame(payload)
                if event:
                    self._process_event(event, timestamp)

        except Exception as e:
            pass  # Silently ignore parse errors

    def _parse_socketio_frame(self, payload: str) -> Optional[Dict]:
        """Parse Socket.IO message frame."""
        try:
            # Remove 42 prefix
            json_str = payload[2:]
            data = json.loads(json_str)

            if isinstance(data, list) and len(data) >= 2:
                return {
                    'event_name': data[0],
                    'data': data[1] if len(data) > 1 else {},
                    'raw': payload
                }
        except:
            pass
        return None

    def _process_event(self, event: Dict, timestamp: float):
        """Process captured event."""
        event['timestamp'] = timestamp
        event['captured_at'] = datetime.now().isoformat()

        # Add to buffer
        self.events.append(event)

        # Write to recording file if active
        if self._recording_file:
            self._recording_file.write(json.dumps(event) + '\n')
            self._recording_file.flush()

        # Call callback if registered
        if self._on_event_callback:
            try:
                self._on_event_callback(event)
            except:
                pass

    def start_recording(self, filepath: str):
        """
        Start recording events to JSONL file.

        Args:
            filepath: Path to output file
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._recording_file = open(path, 'a')
        print(f"Recording to: {filepath}")

    def stop_recording(self) -> Optional[str]:
        """
        Stop recording events.

        Returns:
            Path to recording file, or None if not recording
        """
        if self._recording_file:
            path = self._recording_file.name
            self._recording_file.close()
            self._recording_file = None
            print(f"Recording stopped: {path}")
            return path
        return None

    def on_event(self, callback: Callable[[Dict], None]):
        """
        Register callback for new events.

        Args:
            callback: Function called with each new event
        """
        self._on_event_callback = callback

    def get_events(self, limit: int = None) -> List[Dict]:
        """
        Get captured events.

        Args:
            limit: Maximum number of events to return (most recent)

        Returns:
            List of event dictionaries
        """
        events = list(self.events)
        if limit:
            events = events[-limit:]
        return events

    def filter_events(self, event_name: str) -> List[Dict]:
        """
        Get events matching a name.

        Args:
            event_name: Event name to filter by

        Returns:
            List of matching events
        """
        return [e for e in self.events if e.get('event_name') == event_name]

    def get_event_counts(self) -> Dict[str, int]:
        """Get count of each event type."""
        counts = {}
        for event in self.events:
            name = event.get('event_name', 'unknown')
            counts[name] = counts.get(name, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: -x[1]))

    def show_recent_events(self, limit: int = 20):
        """
        Display recent events in a table (for notebooks).

        Args:
            limit: Number of events to show
        """
        if not HAS_IPYTHON:
            print("IPython not available - use get_events() instead")
            return

        events = self.get_events(limit)

        if not events:
            print("No events captured yet")
            return

        # Create DataFrame
        rows = []
        for e in events:
            rows.append({
                'time': e.get('captured_at', '')[-12:-4],  # HH:MM:SS
                'event': e.get('event_name', ''),
                'fields': len(e.get('data', {})),
            })

        df = pd.DataFrame(rows)
        display(HTML(df.to_html(index=False)))
        print(f"\nShowing {len(events)} of {len(self.events)} total events")

    def show_event_distribution(self):
        """Display event type distribution (for notebooks)."""
        if not HAS_IPYTHON:
            counts = self.get_event_counts()
            for name, count in counts.items():
                print(f"  {name}: {count}")
            return

        counts = self.get_event_counts()
        if not counts:
            print("No events captured yet")
            return

        df = pd.DataFrame([
            {'event': name, 'count': count}
            for name, count in counts.items()
        ])
        display(HTML(df.to_html(index=False)))

    def clear(self):
        """Clear event buffer."""
        self.events.clear()
        print("Event buffer cleared")

    def disconnect(self):
        """Disconnect from CDP."""
        self.stop_recording()

        if hasattr(self, '_tab') and self._tab:
            try:
                self._tab.stop()
            except:
                pass

        self.is_connected = False
        print("Disconnected from CDP")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.disconnect()


class MockCDPCapture(CDPCapture):
    """
    Mock CDP capture for testing without Chrome.
    Generates simulated rugs.fun events.
    """

    def connect(self) -> bool:
        """Simulate connection."""
        print("[MOCK] Simulated CDP connection")
        self.is_connected = True
        self._start_simulator()
        return True

    def _start_simulator(self):
        """Start event simulation thread."""
        import random

        def simulate():
            event_types = [
                ('gameStateUpdate', {'price': 0, 'volume': 0}),
                ('playerUpdate', {'balance': 100}),
                ('usernameStatus', {'username': 'test'}),
            ]

            while not self._stop_event.is_set():
                name, data = random.choice(event_types)
                event = {
                    'event_name': name,
                    'data': {**data, 'tick': int(time.time())},
                }
                self._process_event(event, time.time())
                time.sleep(random.uniform(0.5, 2.0))

        self._stop_event.clear()
        self._thread = threading.Thread(target=simulate, daemon=True)
        self._thread.start()

    def disconnect(self):
        """Stop simulation."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1)
        super().disconnect()
        print("[MOCK] Simulation stopped")
