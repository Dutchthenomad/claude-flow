# Deep Research: n8n RAG System Upgrade for Rugs-Expert Agent

## Research Objective

Identify the best n8n-based RAG architectures and workflows to upgrade the claude-flow RAG pipeline, enabling high-fidelity vectorization of real-time WebSocket feeds for aggregate data exploration, statistical anomaly detection, and novel pattern discovery.

---

## Current System Context

### Existing RAG Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CURRENT SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│ Ingestion:    Markdown chunker (256 tokens, 64 overlap)     │
│ Embeddings:   all-MiniLM-L6-v2 (384 dimensions, local)      │
│ Storage:      ChromaDB (SQLite, ~23MB, 1169 chunks)         │
│ Retrieval:    Native cosine + optional LangChain hybrid     │
│ Interface:    Python API, CLI, MCP server                   │
│ Agent:        rugs-expert (Read, Glob, Grep, Bash, LSP)     │
└─────────────────────────────────────────────────────────────┘
```

### Knowledge Sources Currently Indexed
- `knowledge/rugs-events/WEBSOCKET_EVENTS_SPEC.md` - 21 WebSocket events documented
- `knowledge/rugs-strategy/` - Trading strategy documentation
- `knowledge/anthropic-docs/` - API documentation
- Project commands, agents, skills, docs

### Current Limitations
1. **Static ingestion** - Manual re-indexing required for new data
2. **No streaming** - Cannot ingest real-time WebSocket feeds
3. **Limited analytics** - No aggregate statistics or anomaly detection
4. **Single embedding model** - No multi-modal or specialized embeddings
5. **No temporal awareness** - Chunks lack timestamp/sequence context
6. **Limited scale** - ChromaDB may bottleneck at millions of events

### Data Sources Available
- **Live WebSocket feed**: rugs.fun Socket.IO events (4+ events/sec)
- **Historical recordings**: 929+ JSONL game recordings in `~/rugs_recordings/`
- **Event types**: 21 documented (gameStateUpdate, playerUpdate, sidebetUpdate, etc.)
- **Data volume**: ~500KB-2MB per game session, thousands of events

---

## Upgrade Requirements

### Primary Goals

1. **Real-Time Ingestion**
   - Stream WebSocket events directly into vector store
   - Sub-second latency from event → searchable embedding
   - Handle bursts of 10-50 events/second during active games

2. **High-Fidelity Vectorization**
   - Preserve full event payload (no lossy summarization)
   - Maintain temporal relationships between events
   - Enable field-level semantic search (e.g., "price spikes > 50x")

3. **Aggregate Analytics**
   - Statistical summaries across thousands of games
   - Anomaly detection (unusual patterns, outliers)
   - Trend analysis (cross-game patterns over time)

4. **Agent-Powered Exploration**
   - Natural language queries over vectorized data
   - "Find all games where price exceeded 100x before rugging"
   - "What's the average time between presale and first rug?"
   - "Identify statistical anomalies in player betting patterns"

### Technical Requirements

| Requirement | Current | Target |
|-------------|---------|--------|
| Ingestion mode | Batch | Real-time streaming |
| Events/second | N/A | 50+ sustained |
| Total events | ~50K | 10M+ |
| Query latency | ~200ms | <100ms |
| Embedding model | MiniLM (384d) | Multi-model (768-1536d) |
| Analytics | None | Time-series, aggregates |
| Anomaly detection | None | Built-in |

---

## Research Questions

### 1. n8n RAG Workflow Architectures

**Q1.1**: What are the most production-ready n8n RAG workflow templates?
- Official n8n RAG templates and nodes
- Community-contributed RAG workflows
- Enterprise patterns for high-volume ingestion

**Q1.2**: How do top n8n RAG implementations handle:
- Real-time data streaming (webhooks, WebSocket bridges)
- Chunking strategies for structured JSON events
- Embedding pipeline orchestration
- Vector store population at scale

**Q1.3**: What n8n nodes are most relevant?
- Vector store nodes (Pinecone, Qdrant, Weaviate, Supabase)
- Embedding nodes (OpenAI, Cohere, local models)
- Document loaders and transformers
- AI agent nodes for retrieval

### 2. Vector Database Selection

**Q2.1**: Which vector databases have the best n8n integration?
- Native n8n nodes vs. HTTP/API integration
- Ease of setup and maintenance
- Cost at scale (10M+ vectors)

**Q2.2**: Comparison criteria:
| Database | n8n Support | Streaming | Analytics | Scale | Cost |
|----------|-------------|-----------|-----------|-------|------|
| Pinecone | ? | ? | ? | ? | ? |
| Qdrant | ? | ? | ? | ? | ? |
| Weaviate | ? | ? | ? | ? | ? |
| Supabase pgvector | ? | ? | ? | ? | ? |
| Milvus | ? | ? | ? | ? | ? |
| ChromaDB | Native | No | Limited | Medium | Free |

**Q2.3**: Which databases support:
- Hybrid search (dense + sparse/BM25)
- Metadata filtering with complex queries
- Time-series aware indexing
- Built-in aggregation functions

### 3. Embedding Strategies for Event Data

**Q3.1**: What embedding models work best for:
- Structured JSON events (not prose)
- Numerical data (prices, timestamps, percentages)
- Short text fields (player names, event types)
- Mixed content (JSON + natural language)

**Q3.2**: Should we use:
- Single model for all events?
- Specialized models per event type?
- Hybrid embeddings (semantic + structured)?

**Q3.3**: Embedding model comparison:
| Model | Dimensions | JSON Performance | n8n Integration |
|-------|------------|------------------|-----------------|
| text-embedding-3-small | 1536 | ? | ? |
| text-embedding-3-large | 3072 | ? | ? |
| Cohere embed-v3 | 1024 | ? | ? |
| Voyage-2 | 1024 | ? | ? |
| Local (MiniLM, BGE) | 384-768 | ? | ? |

### 4. Real-Time Streaming Architecture

**Q4.1**: How to bridge WebSocket → n8n?
- n8n webhook node + WebSocket proxy
- Custom n8n node for Socket.IO
- Message queue intermediary (Redis, RabbitMQ)
- Event-driven triggers

**Q4.2**: What's the recommended pattern for:
```
Socket.IO Event → ??? → n8n Workflow → Embedding → Vector Store
```

**Q4.3**: How to handle backpressure and rate limiting?
- Buffering strategies
- Batch vs. individual event processing
- Error handling and retry logic

### 5. Analytics and Anomaly Detection

**Q5.1**: What n8n integrations support aggregate analytics?
- Time-series databases (InfluxDB, TimescaleDB)
- Analytics platforms (Elasticsearch, ClickHouse)
- ML/anomaly detection services

**Q5.2**: Can vector databases provide:
- Count/sum/avg aggregations over metadata?
- Time-windowed statistics?
- Outlier detection on embeddings?

**Q5.3**: Best practices for:
- "Find games with unusual price trajectories"
- "Detect statistical anomalies in betting patterns"
- "Identify rare event sequences"

### 6. Agent Integration Patterns

**Q6.1**: How do AI agents query n8n-managed RAG systems?
- n8n AI Agent node capabilities
- Tool/function calling patterns
- Multi-step reasoning over retrieved data

**Q6.2**: What query patterns work best for:
- Aggregate questions ("average across all games")
- Comparative questions ("games where X > Y")
- Temporal questions ("events in sequence A→B→C")
- Anomaly questions ("unusual patterns")

**Q6.3**: How to expose n8n RAG to external agents (Claude Code)?
- MCP server integration
- REST API endpoints
- Webhook callbacks

---

## Specific Use Cases to Support

### Use Case 1: Real-Time Event Capture
```
As rugs-expert, I need to:
- Capture every WebSocket event in real-time
- Vectorize with full payload fidelity
- Query "what happened in the last 5 minutes?"
```

### Use Case 2: Cross-Game Analysis
```
As rugs-expert, I need to:
- Query across 1000+ historical games
- "What % of games rug before reaching 50x?"
- "Average time from presale to active phase?"
```

### Use Case 3: Anomaly Detection
```
As rugs-expert, I need to:
- Detect unusual patterns automatically
- "Flag games with abnormal price movements"
- "Identify statistical outliers in player behavior"
```

### Use Case 4: Pattern Discovery
```
As rugs-expert, I need to:
- Find novel patterns in aggregate data
- "What precedes a rug event?"
- "Are there predictive signals?"
```

---

## Evaluation Criteria

Rate each solution on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| n8n Integration | 25% | Native nodes, ease of setup, community support |
| Real-Time Capability | 20% | Streaming ingestion, latency, throughput |
| Query Power | 20% | Hybrid search, filtering, aggregations |
| Scale | 15% | Handle 10M+ events, cost efficiency |
| Analytics | 10% | Built-in stats, anomaly detection |
| Agent Compatibility | 10% | MCP/API exposure, tool calling |

---

## Deliverables Expected

1. **Top 3 n8n RAG Architectures** - Ranked with pros/cons
2. **Vector Database Recommendation** - With migration path from ChromaDB
3. **Embedding Strategy** - Model selection and chunking approach
4. **Streaming Architecture** - WebSocket → n8n → Vector Store pipeline
5. **Analytics Integration** - Anomaly detection and aggregate queries
6. **Implementation Roadmap** - Phased upgrade plan

---

## Reference Links to Explore

### n8n Resources
- n8n RAG documentation and templates
- n8n vector store integrations
- n8n AI agent capabilities
- Community workflows for RAG

### Vector Databases
- Pinecone serverless + n8n
- Qdrant cloud + n8n integration
- Weaviate hybrid search
- Supabase pgvector + n8n

### Embedding Services
- OpenAI embeddings API
- Cohere Embed v3
- Voyage AI embeddings
- Local embedding options (Ollama, etc.)

### Analytics Platforms
- Time-series integration patterns
- Anomaly detection services
- Statistical analysis in n8n

---

## Context Files

For full system understanding, the researcher should review:

```
/home/nomad/Desktop/claude-flow/
├── rag-pipeline/
│   ├── CONTEXT.md              # Pipeline architecture
│   ├── config.py               # Current configuration
│   ├── ingestion/chunker.py    # Chunking strategy
│   ├── retrieval/retrieve.py   # Query implementation
│   └── storage/store.py        # ChromaDB integration
├── knowledge/rugs-events/
│   ├── CONTEXT.md              # Canonical promotion laws
│   └── WEBSOCKET_EVENTS_SPEC.md # 21 events documented
├── agents/rugs-expert.md       # Agent definition
└── mcp-server/server.py        # MCP integration
```

---

## Success Metrics

The upgraded system should enable queries like:

```
"Across all 929 recorded games, what is the median time from
ACTIVE phase start to rug event, and identify games that deviate
more than 2 standard deviations from this median."

"Find the top 10 most anomalous price trajectories in the dataset,
ranked by statistical unusualness."

"What sequence of playerUpdate events most commonly precedes
a price spike above 100x?"
```

If the agent can answer these with sub-second latency and statistical rigor, the upgrade is successful.
