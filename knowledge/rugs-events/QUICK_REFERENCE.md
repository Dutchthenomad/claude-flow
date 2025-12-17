# Rugs.fun Quick Reference

> Fast lookup for common protocol questions
> Last updated: 2025-12-15

---

## Connection Quick Start

### Start Chrome with CDP
```bash
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/nomad/.gamebot/chrome_profiles/rugs_bot \
  --no-first-run \
  "https://rugs.fun"
```

### Verify Connection
```bash
curl -s http://localhost:9222/json/version | jq .
curl -s http://localhost:9222/json/list | jq .
```

### Key Parameters
- **CDP Port**: 9222
- **Profile**: `/home/nomad/.gamebot/chrome_profiles/rugs_bot`
- **Player**: Dutch (`did:privy:cmaibr7rt0094jp0mc2mbpfu4`)

---

## Event Categories

### Auth-Required Events (Need CDP)
```
usernameStatus          - Player identity
playerUpdate            - Balance/position sync
buyOrderResponse        - Buy confirmation
sellOrderResponse       - Sell confirmation
sidebetResponse         - Sidebet confirmation
playerLeaderboardPosition - 7-day rank
```

### Public Events (No Auth)
```
gameStateUpdate         - Core game state (~4/sec)
gameStatePlayerUpdate   - Your leaderboard entry (~4/sec)
standard/newTrade       - Trade broadcasts (sporadic)
newChatMessage          - Chat (sporadic)
```

---

## Socket.IO Frame Format

### Message Type Prefixes
```
0   - OPEN (handshake)
2   - PING
3   - PONG
4   - MESSAGE
42  - EVENT (most common)
```

### Parsing Example
```python
# Raw frame: 42["gameStateUpdate",{"gameId":"20251215-xxx",...}]

# Strip "42" prefix
json_str = payload[2:]

# Parse JSON array
event_name, data = json.loads(json_str)
# event_name = "gameStateUpdate"
# data = {"gameId": "20251215-xxx", ...}
```

---

## Critical Game State Fields

### Root Fields (gameStateUpdate)
```python
{
    "gameId": "20251215-xxx",
    "active": true,           # Game in progress
    "rugged": false,          # Has ended
    "price": 1.5,             # Current multiplier
    "tickCount": 42,          # Ticks since start
    "cooldownTimer": 0,       # Milliseconds to next game
    "leaderboard": [...],     # Top 10 players
    "partialPrices": {...}    # Backfill data
}
```

### Leaderboard Entry
```python
{
    "id": "did:privy:xxx",
    "username": "Dutch",
    "pnl": 0.123,             # Total P&L (SOL)
    "pnlPercent": 12.3,       # P&L percentage
    "hasActiveTrades": true,
    "positionQty": 5,
    "avgCost": 1.2,
    "totalInvested": 0.1,
    "sidebetActive": false,
    "sideBet": null           # Or sidebet object
}
```

### Sidebet Object
```python
{
    "startedAtTick": 10,
    "end": 50,                # Resolves at tick 50
    "betAmount": 0.01,
    "xPayout": 5,             # 5x multiplier
    "bonusPortion": 0.005,
    "realPortion": 0.005
}
```

---

## Game Phase Detection

```python
if event['cooldownTimer'] > 0:
    phase = 'COOLDOWN'
elif event['active'] and not event['rugged']:
    phase = 'ACTIVE_GAMEPLAY'
elif event['rugged']:
    phase = 'RUG_EVENT'
else:
    phase = 'IDLE'
```

### Detecting Events
```python
# Game start
if event['active'] == True and prev['active'] == False:
    print("GAME_START")

# Rug event
if event['rugged'] == True and prev['rugged'] == False:
    print("RUG_EVENT")

# Sidebet resolution
player = event['leaderboard'][0]  # Assuming Dutch is in top 10
if player['sidebetActive'] == False and prev_sidebet == True:
    print("SIDEBET_RESOLVED")
```

---

## Common Patterns

### Get Current Price
```python
price = event['price']  # Float, 1.0 = entry price
```

### Get Your Position
```python
# Find yourself in leaderboard
player = next((p for p in event['leaderboard'] if p['id'] == PLAYER_ID), None)

if player and player['hasActiveTrades']:
    qty = player['positionQty']
    avg_cost = player['avgCost']
    current_value = qty * event['price']
    pnl = player['pnl']
```

### Get Backfill Prices
```python
partial = event.get('partialPrices', {})
if partial:
    start = partial['startTick']
    end = partial['endTick']
    values = partial['values']  # {tick: price, ...}

    for tick in range(start, end + 1):
        price = values.get(str(tick))
```

### Track Trade Latency
```python
# Send trade request
request_time = time.time()

# Wait for response
def on_buy_response(data):
    response_time = time.time()
    latency_ms = (response_time - request_time) * 1000
    print(f"Buy latency: {latency_ms:.0f}ms")
```

---

## CDP Python Example

```python
import asyncio
import websockets
import json

async def connect_cdp():
    # 1. Get CDP WebSocket URL
    ws_url = "ws://localhost:9222/devtools/page/..."  # From /json/list

    # 2. Connect
    ws = await websockets.connect(ws_url)

    # 3. Enable Network domain
    await ws.send(json.dumps({
        'id': 1,
        'method': 'Network.enable'
    }))

    # 4. Listen for events
    async for message in ws:
        event = json.loads(message)

        if event.get('method') == 'Network.webSocketFrameReceived':
            payload = event['params']['response']['payloadData']

            # Parse Socket.IO frame
            if payload.startswith('42'):
                json_str = payload[2:]
                event_name, data = json.loads(json_str)
                print(f"Event: {event_name}")
```

---

## Troubleshooting

### No Events Received
1. Check Network domain enabled: `Network.enable`
2. Verify WebSocket connected in browser DevTools
3. Refresh rugs.fun page

### No Auth Events
1. Check Phantom shows "Connected"
2. Verify username in top-right of UI
3. Place manual trade and watch for response

### Profile in Use
```bash
pkill -9 chrome
rm -f /home/nomad/.gamebot/chrome_profiles/rugs_bot/.lock
```

---

## File Locations

### Documentation
- **Events Index**: `knowledge/rugs-events/EVENTS_INDEX.md`
- **Connection Guide**: `knowledge/rugs-events/BROWSER_CONNECTION_PROTOCOL.md`
- **This File**: `knowledge/rugs-events/QUICK_REFERENCE.md`

### Implementation (REPLAYER)
- **CDP Interceptor**: `src/sources/cdp_websocket_interceptor.py`
- **Socket.IO Parser**: `src/sources/socketio_parser.py`
- **CDP Manager**: `browser_automation/cdp_browser_manager.py`

### Data
- **Raw Captures**: `/home/nomad/rugs_recordings/raw_captures/`
- **RAG Catalog**: `/home/nomad/rugs_recordings/rag_events/`
- **Game Recordings**: `/home/nomad/rugs_recordings/*.jsonl`

---

## Next Steps

For detailed information, see:
1. **BROWSER_CONNECTION_PROTOCOL.md** - Complete CDP setup guide
2. **EVENTS_INDEX.md** - Full event catalog with all fields
3. **CONTEXT.md** - Knowledge base overview and integration points

---

*Quick reference for rugs.fun protocol - see full docs for comprehensive details.*
