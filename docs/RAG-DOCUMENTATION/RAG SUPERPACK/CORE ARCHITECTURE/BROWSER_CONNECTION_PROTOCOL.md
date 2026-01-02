# Rugs.fun Browser Connection Protocol

> Complete guide for connecting to rugs.fun via Chrome DevTools Protocol (CDP)
> Last updated: 2025-12-15

---

## Overview

Rugs.fun requires browser-based authentication via Phantom wallet. To capture authenticated WebSocket events, we connect to Chrome via CDP (Chrome DevTools Protocol) rather than establishing a separate WebSocket connection.

**Why CDP?**
- Rugs.fun server only sends auth-required events (`usernameStatus`, `playerUpdate`) to authenticated clients
- Browser maintains the authenticated WebSocket connection via Phantom wallet
- CDP allows us to intercept WebSocket frames from the browser's connection
- Captures ALL events (both public and authenticated)

---

## Connection Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     CDP Connection Flow                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────┐   CDP    ┌──────────────────┐   WebSocket   │
│  │  Your App   │◄────────►│  Chrome Browser  │◄──────────────►│
│  │ (REPLAYER)  │  :9222   │  (rugs.fun tab)  │  wss://api...  │
│  └─────────────┘          └──────────────────┘                │
│                                  │                             │
│                                  │ Phantom Extension           │
│                                  ▼                             │
│                           ┌──────────────┐                     │
│                           │ Wallet Auth  │                     │
│                           │ (Player ID)  │                     │
│                           └──────────────┘                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Critical Connection Parameters

### CDP Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| **CDP Port** | `9222` | Chrome remote debugging port |
| **Profile Path** | `/home/nomad/.gamebot/chrome_profiles/rugs_bot` | Persistent Chrome profile |
| **Target URL** | `https://rugs.fun` | Game URL |
| **WebSocket URL** | `wss://api.rugs.fun/socket.io/` | (Auto-detected by CDP) |

### Profile Contents

The persistent Chrome profile contains:
- **Phantom Wallet Extension** - Pre-installed and configured
- **Wallet Connection** - Already authenticated to rugs.fun
- **Player Identity** - User "Dutch" (`did:privy:cmaibr7rt0094jp0mc2mbpfu4`)
- **Cookies/LocalStorage** - Session persistence

---

## Starting Chrome with CDP

### Command Line

```bash
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/nomad/.gamebot/chrome_profiles/rugs_bot \
  --no-first-run \
  "https://rugs.fun"
```

### Parameters Explained

| Flag | Purpose |
|------|---------|
| `--remote-debugging-port=9222` | Enable CDP server on port 9222 |
| `--user-data-dir=<path>` | Use persistent profile (wallet, cookies) |
| `--no-first-run` | Skip first-run wizard |
| URL argument | Navigate to rugs.fun on startup |

### Important Notes

1. **Profile Lock**: Only ONE Chrome instance can use the profile at a time
2. **Headless Not Recommended**: Wallet extensions often fail in headless mode
3. **Port Conflicts**: Ensure port 9222 is available (not used by other Chrome instances)
4. **Window Visibility**: Keep browser window visible for wallet interaction

---

## Verifying CDP Connection

### Check CDP Server

```bash
# Get Chrome version and protocol info
curl -s http://localhost:9222/json/version | jq .

# Example output:
{
  "Browser": "Chrome/131.0.6778.85",
  "Protocol-Version": "1.3",
  "User-Agent": "Mozilla/5.0...",
  "V8-Version": "13.1.201.13",
  "WebKit-Version": "537.36",
  "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/..."
}
```

### List Open Tabs

```bash
# Get all inspectable pages (tabs)
curl -s http://localhost:9222/json/list | jq .

# Example output (rugs.fun tab):
[
  {
    "description": "",
    "devtoolsFrontendUrl": "/devtools/inspector.html?ws=localhost:9222/devtools/page/...",
    "id": "E4B1F...",
    "title": "Rugs.fun",
    "type": "page",
    "url": "https://rugs.fun/",
    "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/..."
  }
]
```

### Verify WebSocket Connection

Once connected via CDP, enable Network domain and filter for WebSocket frames:

```python
# Python example using chrome-remote-interface
import asyncio
import websockets

async def verify_websocket():
    ws = await websockets.connect('ws://localhost:9222/devtools/page/...')

    # Enable Network tracking
    await ws.send(json.dumps({
        'id': 1,
        'method': 'Network.enable'
    }))

    # Listen for WebSocket frames
    # You should see Network.webSocketFrameReceived events
```

---

## MCP Server Integration

### chrome-devtools MCP Server

The `chrome-devtools` MCP server (if installed) connects automatically to `localhost:9222`.

**Configuration** (in Claude Desktop `config.json`):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-chrome-devtools"],
      "env": {
        "CDP_PORT": "9222"
      }
    }
  }
}
```

**Tools Provided**:
- `chrome_navigate` - Navigate to URL
- `chrome_screenshot` - Capture page screenshot
- `chrome_execute` - Execute JavaScript
- `chrome_click` - Click elements
- `chrome_type` - Type text into inputs

**Note**: The MCP server provides UI automation, not WebSocket interception. For event capture, use the CDP WebSocket Interceptor directly.

---

## Event Interception Flow

### 1. Connect to CDP

```python
from browser_automation.cdp_browser_manager import CDPBrowserManager

manager = CDPBrowserManager(
    profile_path="/home/nomad/.gamebot/chrome_profiles/rugs_bot",
    cdp_port=9222
)

await manager.connect()
```

### 2. Enable Network Domain

```python
await manager.page.send("Network.enable")
```

### 3. Listen for WebSocket Frames

```python
async def on_websocket_frame(event):
    if event['method'] == 'Network.webSocketFrameReceived':
        payload = event['params']['response']['payloadData']
        # Parse Socket.IO frame
        parsed = SocketIOParser.parse(payload)
        print(f"Event: {parsed['event_name']}, Data: {parsed['data']}")

manager.page.on("Network.webSocketFrameReceived", on_websocket_frame)
```

### 4. Parse Socket.IO Frames

Socket.IO uses Engine.IO protocol with message type prefixes:

| Prefix | Type | Description |
|--------|------|-------------|
| `0` | OPEN | Connection handshake |
| `2` | PING | Keep-alive ping |
| `3` | PONG | Keep-alive pong |
| `4` | MESSAGE | Socket.IO event |
| `42` | EVENT | Socket.IO event (JSON array) |

**Example Frame**:
```
42["gameStateUpdate",{"gameId":"20251215-xxx","price":1.5,...}]
```

**Parsing**:
```python
# Strip "42" prefix
json_str = payload[2:]
# Parse JSON array: [event_name, data]
event_name, data = json.loads(json_str)
```

---

## Key Events to Monitor

### Auth-Required Events (Why CDP is Necessary)

| Event | Description | Typical Frequency |
|-------|-------------|-------------------|
| `usernameStatus` | Player identity confirmation | Once on connect |
| `playerUpdate` | Server-side balance/position sync | Sporadic (after trades) |
| `buyOrderResponse` | Buy trade confirmation | On action |
| `sellOrderResponse` | Sell trade confirmation | On action |
| `sidebetResponse` | Sidebet confirmation | On action |
| `playerLeaderboardPosition` | 7-day leaderboard rank | Sporadic |

### Public Events (Also Captured)

| Event | Description | Frequency |
|-------|-------------|-----------|
| `gameStateUpdate` | Core game state | ~4/sec |
| `gameStatePlayerUpdate` | Your leaderboard entry | ~4/sec |
| `standard/newTrade` | Trade broadcasts | Sporadic |
| `newChatMessage` | Chat messages | Sporadic |

**See**: `EVENTS_INDEX.md` for complete event reference

---

## Player Profile Structure

### Dutch's Profile

| Field | Value |
|-------|-------|
| **Player ID** | `did:privy:cmaibr7rt0094jp0mc2mbpfu4` |
| **Username** | `Dutch` |
| **Wallet** | Phantom (Solana) |
| **Auth Method** | Privy (wallet-based) |

### Profile Directory Contents

```
/home/nomad/.gamebot/chrome_profiles/rugs_bot/
├── Default/
│   ├── Extensions/          # Phantom wallet extension
│   ├── Local Storage/       # Session tokens
│   ├── Cookies              # Auth cookies
│   └── Preferences          # Extension settings
└── ...
```

### First-Time Setup (Already Complete)

If setting up a NEW profile:

1. **Launch Chrome with empty profile**:
   ```bash
   google-chrome --remote-debugging-port=9222 \
     --user-data-dir=/path/to/new/profile \
     "https://rugs.fun"
   ```

2. **Install Phantom** (if not already installed):
   - Visit Chrome Web Store
   - Install Phantom wallet extension
   - Import or create wallet

3. **Connect to rugs.fun**:
   - Click "Connect Wallet" on rugs.fun
   - Select Phantom
   - Approve connection
   - Verify username appears

4. **Test Authentication**:
   - Check for `usernameStatus` event in CDP Network tab
   - Verify `playerUpdate` events appear after trades

---

## Troubleshooting

### No WebSocket Events Received

**Problem**: CDP connected but no `Network.webSocketFrameReceived` events

**Solutions**:
1. Verify Network domain enabled: `await page.send("Network.enable")`
2. Check WebSocket connection in browser DevTools (Network → WS filter)
3. Ensure rugs.fun tab is active (background tabs may throttle events)
4. Refresh rugs.fun page to re-establish WebSocket connection

### "Profile in use" Error

**Problem**: Chrome refuses to start with profile

**Solutions**:
1. Close all Chrome instances using that profile
2. Kill lingering Chrome processes: `pkill -9 chrome`
3. Check for `.lock` file in profile directory: `rm -f profile_path/.lock`

### Phantom Wallet Not Responding

**Problem**: Wallet extension doesn't auto-connect to rugs.fun

**Solutions**:
1. Manually click wallet icon and approve connection
2. Check extension is enabled in `chrome://extensions`
3. Verify wallet has SOL balance (rugs.fun requires small amount)
4. Check browser console for wallet errors

### Auth Events Not Appearing

**Problem**: Only seeing `gameStateUpdate`, no `usernameStatus` or `playerUpdate`

**Root Cause**: Likely not authenticated or intercepting wrong WebSocket connection

**Solutions**:
1. Verify Phantom shows "Connected" on rugs.fun
2. Check username appears in top-right corner of rugs.fun UI
3. Manually place a trade and watch for `buyOrderResponse` event
4. Verify intercepting correct WebSocket URL: `wss://api.rugs.fun/socket.io/`

---

## Security Considerations

### Profile Protection

The Chrome profile contains:
- **Private wallet keys** (encrypted by Phantom)
- **Session tokens** (auth cookies)
- **Player identity** (privy DID)

**Best Practices**:
1. Never commit profile directory to git
2. Use restricted permissions: `chmod 700 /path/to/profile`
3. Backup profile before major changes
4. Separate profiles for testing vs production

### CDP Port Security

Port 9222 allows FULL browser control, including:
- JavaScript execution
- Cookie access
- Navigation control
- File system access (via downloads)

**Best Practices**:
1. Only expose CDP on localhost (never `0.0.0.0`)
2. Use firewall to block external access to port 9222
3. Close CDP when not in use
4. Never share CDP WebSocket URL publicly

---

## Implementation References

### REPLAYER Project

**Location**: `/home/nomad/Desktop/REPLAYER/`

**Key Files**:

| File | Purpose | Lines |
|------|---------|-------|
| `src/sources/cdp_websocket_interceptor.py` | CDP frame interception | 205 |
| `src/sources/socketio_parser.py` | Socket.IO frame parsing | 151 |
| `browser_automation/cdp_browser_manager.py` | CDP connection manager | 270 |
| `browser_automation/rugs_browser.py` | Browser lifecycle management | 268 |
| `browser_automation/persistent_profile.py` | Profile configuration | ~100 |

**Test Files**:
- `src/tests/test_sources/test_cdp_websocket_interceptor.py` (12 tests)
- `src/tests/test_sources/test_socketio_parser.py` (8 tests)
- `browser_automation/tests/test_cdp_browser_manager.py` (20 tests)

### CV-BOILER-PLATE-FORK Project

**Location**: `/home/nomad/Desktop/CV-BOILER-PLATE-FORK/`

**Key Files**:
- `core/browser/persistent_profile.py` - Shared profile manager
- `scripts/setup_phantom_profile.py` - Interactive profile setup tool

---

## Quick Start Checklist

For connecting to rugs.fun via CDP:

- [ ] Chrome installed with version ≥120
- [ ] Profile exists at `/home/nomad/.gamebot/chrome_profiles/rugs_bot`
- [ ] Phantom wallet extension installed in profile
- [ ] Wallet connected to rugs.fun (username visible)
- [ ] Port 9222 available (no other Chrome instances)
- [ ] Start Chrome with CDP flags: `--remote-debugging-port=9222`
- [ ] Verify CDP server: `curl http://localhost:9222/json/version`
- [ ] Connect to CDP WebSocket: `ws://localhost:9222/devtools/page/...`
- [ ] Enable Network domain: `Network.enable`
- [ ] Listen for `Network.webSocketFrameReceived` events
- [ ] Parse Socket.IO frames: Strip `42` prefix, parse JSON array
- [ ] Filter for auth events: `usernameStatus`, `playerUpdate`, trade responses

---

## Related Documentation

- **Event Catalog**: `EVENTS_INDEX.md` - Complete WebSocket event reference
- **WebSocket Spec**: `/home/nomad/Desktop/REPLAYER/docs/specs/WEBSOCKET_EVENTS_SPEC.md`
- **CDP Protocol**: https://chromedevtools.github.io/devtools-protocol/
- **Socket.IO Protocol**: https://socket.io/docs/v4/engine-io-protocol/
- **Phantom Docs**: https://docs.phantom.app/

---

*For questions about this protocol, reference the REPLAYER Phase 11 implementation (CDP WebSocket Interception) completed 2025-12-14.*
