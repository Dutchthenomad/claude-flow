# MCP Server for Real-Time Socket.IO Feed Observation

**Status**: Research Complete, Architecture Selected
**Created**: 2025-12-25
**Next Step**: Connection pattern decision, then implementation planning

---

## Problem Statement

Enable Claude Code to observe the rugs.fun live Socket.IO feed in real-time while the user plays the game. The goal is bidirectional collaboration: user interacts with the game, Claude observes events, both can discuss and debug together.

### Current Gap

- VECTRA-PLAYER and REPLAYER can connect to the feed
- Claude Code cannot subscribe to real-time events during conversation
- No persistent API endpoint for external consumers to tap into

### Success Criteria

1. Claude can observe live `gameStateUpdate`, `playerUpdate`, and trade events
2. User can play normally while Claude watches
3. Events stream with minimal latency (<500ms)
4. System is persistent and reusable across sessions

---

## Research Summary

### Approaches Evaluated

| Approach | Description | Verdict |
|----------|-------------|---------|
| **MCP Server (SSE)** | Native Claude Code integration via Model Context Protocol | **SELECTED** |
| WebSocket Relay | Standalone server rebroadcasting to multiple consumers | Viable fallback |
| Chrome Extension | Capture at browser level, stream out | Too complex |
| mitmproxy | MITM proxy for WebSocket interception | Overkill for this use case |

### MCP Transport Options

| Transport | Duplex | Claude Code Support | Status |
|-----------|--------|---------------------|--------|
| stdio | Full | Native | For local processes |
| **SSE** | Server→Client | **Native** | **SELECTED** |
| Streamable HTTP | Full | Native | Alternative |
| WebSocket | Full | Proposed (SEP-1288) | In-review, future upgrade path |

### Key Resources Discovered

**Official SDKs**:
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - FastMCP framework with SSE support
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

**Reference Implementations**:
- [mcp-websocket](https://github.com/virajsharma2000/mcp-websocket) - Dual-port pattern (MCP + WebSocket)
- [mcp-weather-sse](https://github.com/justjoehere/mcp-weather-sse) - SSE MCP server tutorial

**Specifications**:
- [SEP-1288: WebSocket Transport](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1288) - Future upgrade path
- [MCP Transports Spec](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)

**Tutorials**:
- [FreeCodeCamp MCP Handbook](https://www.freecodecamp.org/news/how-to-build-a-custom-mcp-server-with-typescript-a-handbook-for-developers/)
- [MCP Practical Guide with SSE](https://www.f22labs.com/blogs/mcp-practical-guide-with-sse-transport/)

---

## Architecture Decision

### Selected: Single-Port SSE MCP Server

```
┌─────────────────┐     CDP 9222      ┌──────────────────┐
│  Chrome Browser │◄─────────────────►│  MCP Server      │
│  (rugs.fun)     │  WebSocket frames │  (Python/FastMCP)│
│  + Phantom      │                   │                  │
└─────────────────┘                   │  SSE Transport   │
                                      │  Port 8000       │
                                      └────────┬─────────┘
                                               │
                                               ▼ SSE Stream
                                      ┌──────────────────┐
                                      │  Claude Code     │
                                      │  (subscriber)    │
                                      └──────────────────┘
```

### Why SSE (Not WebSocket)?

1. **Native Claude Code support** - Works today, no waiting for SEP-1288
2. **Simpler implementation** - Server pushes events, client receives
3. **Sufficient for use case** - We primarily need server→client event streaming
4. **Upgrade path exists** - Can migrate to WebSocket transport when SEP-1288 lands

### Future Upgrade Path

When bidirectional communication is needed:
1. SEP-1288 WebSocket transport becomes available
2. Or implement dual-port pattern (MCP tools + WebSocket feed)

---

## Open Questions (For Next Session)

### Connection Pattern (TO BE DECIDED)

How should the MCP server receive Socket.IO events?

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. CDP Tap** | Connect directly to Chrome's CDP port 9222 | Standalone, no VECTRA changes | Requires Chrome running with CDP |
| **B. VECTRA Relay** | VECTRA publishes to local socket, MCP subscribes | Reuses existing connection | Couples to VECTRA |
| **C. Event Bus** | Shared pub/sub (Redis/ZeroMQ/Unix socket) | Clean separation, multiple consumers | More infrastructure |

**Recommendation**: Start with Option A (CDP Tap) for simplicity.

### MCP Server Tools to Expose

Candidates:
- `subscribe_feed()` - Start receiving events
- `get_recent_events(n)` - Query last N events from buffer
- `get_game_state()` - Current game phase, price, leaderboard
- `get_player_state()` - Your balance, positions (auth events)
- `filter_events(type)` - Subscribe to specific event types only

### Integration Points

- **rugs-expert agent**: Should use this MCP server for live data
- **RAG pipeline**: Future integration with LangChain (`/home/nomad/Desktop/LANGCHAIN`)
- **REPLAYER**: Could share the same event source

---

## Related Context

### Existing Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| CDP Browser Connection | Port 9222 | Chrome DevTools Protocol |
| VECTRA-PLAYER | `/home/nomad/Desktop/VECTRA-PLAYER/` | Game automation |
| REPLAYER | `/home/nomad/Desktop/REPLAYER/` | Replay/live viewer |
| rugs-expert agent | `agents/rugs-expert.md` | Protocol knowledge |
| LangChain monorepo | `/home/nomad/Desktop/LANGCHAIN/` | Future RAG upgrade |

### Protocol Documentation

| Document | Location |
|----------|----------|
| WebSocket Events Spec | `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md` |
| Browser Connection | `knowledge/rugs-events/RUGS_BROWSER_CONNECTION.md` |
| Event Context | `knowledge/rugs-events/CONTEXT.md` |

---

## Implementation Phases (Draft)

### Phase 1: Minimal Viable MCP Server
- [ ] FastMCP server skeleton with SSE transport
- [ ] CDP client connecting to port 9222
- [ ] Parse Socket.IO frames from `Network.webSocketFrameReceived`
- [ ] Single tool: `get_recent_events(n)`
- [ ] Test with Claude Code: `claude mcp add`

### Phase 2: Live Streaming
- [ ] SSE event stream for real-time push
- [ ] Ring buffer for last N events
- [ ] Event type filtering
- [ ] Progress notifications during stream

### Phase 3: Integration
- [ ] Update rugs-expert agent to use MCP server
- [ ] Add to claude-flow plugin configuration
- [ ] Documentation and usage examples

### Phase 4: Future Enhancements
- [ ] Bidirectional communication (when SEP-1288 lands)
- [ ] LangChain/n8n RAG pipeline integration
- [ ] Multi-consumer event bus architecture

---

## References

### MCP Documentation
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Build an MCP Client](https://modelcontextprotocol.io/docs/develop/build-client)
- [Connect to Remote MCP Servers](https://modelcontextprotocol.io/docs/develop/connect-remote-servers)

### Transport & Streaming
- [MCP Transports Specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
- [SEP-1288: WebSocket Transport Proposal](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1288)
- [MCP SSE Transport Guide](https://www.f22labs.com/blogs/mcp-practical-guide-with-sse-transport/)

### Reference Implementations
- [mcp-websocket (dual-port pattern)](https://github.com/virajsharma2000/mcp-websocket)
- [mcp-weather-sse (SSE tutorial)](https://github.com/justjoehere/mcp-weather-sse)
- [StreamNative MCP Server](https://streamnative.io/blog/introducing-the-streamnative-mcp-server-connecting-streaming-data-to-ai-agents)

### WebSocket Tools (Evaluated)
- [WSSiP (NCC Group)](https://github.com/nccgroup/wssip) - WebSocket interception
- [mitmproxy](https://www.mitmproxy.org/) - MITM proxy with WebSocket support
- [node-http-mitm-proxy](https://github.com/joeferner/node-http-mitm-proxy) - Node.js MITM

### Claude Code Integration
- [Claude Code Remote MCP Servers](https://www.infoq.com/news/2025/06/anthropic-claude-remote-mcp/)
- [MCP Servers for Claude Code](https://mcpcat.io/guides/best-mcp-servers-for-claude-code/)

---

*Document created during brainstorming session 2025-12-25*
