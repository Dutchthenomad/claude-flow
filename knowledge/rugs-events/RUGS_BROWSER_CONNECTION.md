# Rugs.fun Browser Connection Protocol

This document describes how to connect to the rugs.fun browser profile via Chrome DevTools Protocol (CDP) for real-time WebSocket event observation.

## Connection Parameters

```
CDP Port: 9222
Profile Path: /home/nomad/.gamebot/chrome_profiles/rugs_bot
Target URL: https://rugs.fun
```

## Starting Chrome with CDP

```bash
# Launch Chrome with the correct profile and CDP enabled
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/nomad/.gamebot/chrome_profiles/rugs_bot \
  --no-first-run \
  "https://rugs.fun"
```

## Verifying CDP Connection

```bash
# Check if Chrome is accepting CDP connections
curl -s http://localhost:9222/json/version

# List available pages/targets
curl -s http://localhost:9222/json/list
```

## Using chrome-devtools MCP Server

The chrome-devtools MCP server can connect to the running Chrome instance:

```bash
# Verify MCP server is available
claude mcp list

# The server connects automatically to localhost:9222
```

## REPLAYER Integration

REPLAYER uses these same parameters in `src/browser/manager.py`:

```python
class CDPBrowserManager:
    CDP_PORT = 9222
    TARGET_URL = "https://rugs.fun"

    def __init__(self):
        self.profile_path = Path.home() / ".gamebot" / "chrome_profiles" / "rugs_bot"
```

### Connection Sequence

1. **Connect to Chrome via CDP** (`manager.connect()`)
2. **Navigate to rugs.fun** (`manager.navigate_to_game()`)
3. **Ensure wallet extensions are ready** (`manager.ensure_wallet_ready()`)
4. **Start CDP WebSocket interception** (`bridge._start_cdp_interception()`)
5. **Refresh page** to capture WebSocket connection

### Key Events to Monitor

| Event | Description | Auth-Required |
|-------|-------------|---------------|
| `playerUpdate` | Server state (cash, positions) | Yes |
| `gameStatePlayerUpdate` | Leaderboard entry with username | No (broadcast) |
| `usernameStatus` | Identity confirmation | Yes |
| `gameStateUpdate` | Game tick data | No |
| `standard/newTrade` | Trade broadcasts | No |

## WebSocket Interception

The CDP interceptor uses these Network domain events:
- `Network.webSocketCreated` - Capture connection to backend.rugs.fun
- `Network.webSocketFrameReceived` - Parse incoming Socket.IO frames
- `Network.webSocketFrameSent` - Parse outgoing frames (for trades)

### Socket.IO Frame Format

Frames are Engine.IO/Socket.IO encoded:
- `2` = ping
- `3` = pong
- `42["eventName", {...data}]` = event message

## Profile Contents

The profile at `/home/nomad/.gamebot/chrome_profiles/rugs_bot` contains:
- Phantom wallet extension
- Wallet already connected to rugs.fun
- Player "Dutch" authenticated

## Troubleshooting

### CDP Not Responding
```bash
# Kill any existing Chrome and restart
pkill chrome
google-chrome --remote-debugging-port=9222 --user-data-dir=/home/nomad/.gamebot/chrome_profiles/rugs_bot "https://rugs.fun"
```

### Missing WebSocket Events
- Ensure page refresh after starting interception
- Check `Network.webSocketCreated` was captured
- Verify `rugs_websocket_id` is set in interceptor

### No Auth Events (usernameStatus, playerUpdate)
- These require authenticated WebSocket connection
- Must use browser's WebSocket (CDP interception), not separate connection
- Verify wallet is connected in browser
