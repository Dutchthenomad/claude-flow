# Upgrading your n8n RAG pipeline for real-time WebSocket ingestion

The optimal architecture for your rugs.fun RAG system combines a **RabbitMQ message queue** as the WebSocket-to-n8n bridge, **Qdrant self-hosted** as the vector database, your existing **MiniLM embeddings** with a hybrid metadata strategy, and a **dual-write to TimescaleDB** for analytics. This stack fits comfortably within your $50/month budget on a single 8GB VPS while scaling to 10M+ events with sub-100ms queries. The critical insight is that n8n cannot natively consume WebSocket connections—you'll need an external Socket.IO client service that buffers events through RabbitMQ before n8n processes them.

---

## Top 3 n8n RAG architectures for real-time event ingestion

After evaluating n8n's capabilities against your requirements, three viable architectures emerge—ranked by production-readiness for high-volume streaming.

**Architecture 1: Queue-Buffered Pipeline (Recommended)**

This pattern uses an external Socket.IO client that publishes events to RabbitMQ, which n8n consumes via its native RabbitMQ Trigger node. At **4-50 events/second**, direct webhook calls would overwhelm n8n's execution capacity. RabbitMQ provides essential backpressure handling, message persistence, and decoupling between ingestion rate and processing capacity.

The data flow is: `Socket.IO Client → RabbitMQ → n8n RabbitMQ Trigger → Batch Processing → Embedding → Qdrant + TimescaleDB`. Key advantages include native n8n integration (no custom nodes), built-in dead-letter queues for failed events, and ability to scale horizontally with queue mode workers. The primary tradeoff is additional infrastructure complexity from running RabbitMQ alongside n8n.

**Architecture 2: Webhook Proxy with Redis Buffering**

A lightweight Node.js service maintains the Socket.IO connection and buffers events in Redis Streams, periodically flushing batches to n8n webhooks. This works with n8n's 16MB webhook payload limit but requires custom polling logic and lacks RabbitMQ's delivery guarantees. Better suited if you're already running Redis.

**Architecture 3: Direct Webhook Ingestion (Not Recommended for Scale)**

A simple proxy translates each Socket.IO event to an HTTP POST to n8n. While architecturally simpler, this pattern fails under load—n8n's concurrency limits (configurable via `N8N_CONCURRENCY_PRODUCTION_LIMIT`) create bottlenecks at peak traffic. Only viable for <5 events/second sustained throughput.

**n8n nodes most relevant for your RAG pipeline:**

The **Vector Store nodes** (Qdrant, Supabase, Pinecone, Weaviate, Milvus) support Insert, Get Many, and Retrieve operations. **Embeddings nodes** connect to OpenAI, Cohere, Ollama (self-hosted), and others. The **AI Agent node** provides multi-step reasoning with tool calling, while the **MCP Server Trigger** exposes your RAG as tools for external AI agents. Critical limitations include **no native WebSocket support**, a **16MB webhook payload maximum**, and memory constraints requiring careful batch sizing.

---

## Qdrant emerges as the clear vector database choice for your constraints

Evaluating six databases against your specific requirements—$50/month budget, 10M 384-dimensional vectors, n8n integration, and real-time streaming—Qdrant self-hosted delivers the best overall value.

**Why Qdrant wins:**

Qdrant's **scalar quantization** reduces memory requirements by 4x, allowing 10M vectors to fit in **6-8GB RAM** with vectors stored on disk. It has a **native n8n node** with full insert/retrieve functionality, excellent streaming performance with **<10ms insert latency**, and hybrid search via sparse vectors (BM42/SPLADE). The migration path from ChromaDB is straightforward: export collections via Python client, re-upload to Qdrant with preserved metadata.

**Cost modeling at 10M vectors:**

| Database | Configuration | Monthly Cost | Fits Budget? |
|----------|--------------|--------------|--------------|
| **Qdrant self-hosted** | 8GB RAM VPS + quantization | **$20-40** | ✅ Yes |
| Supabase Cloud | Pro plan + pgvector | $25-50 | ✅ Borderline |
| Pinecone Serverless | 10M vectors, moderate queries | $50-85 | ⚠️ At limit |
| Weaviate Cloud | Serverless tier | $100-200 | ❌ Over budget |

**Supabase pgvector** is a strong runner-up if you need SQL aggregation capabilities—it provides native COUNT/SUM/AVG that Qdrant lacks. The pgvectorscale extension shows **471 QPS at 99% recall** on 50M vectors in benchmarks. However, performance degrades more sharply than Qdrant beyond 10M vectors.

**ChromaDB assessment:** Your current SQLite-backed ChromaDB will not scale to 10M vectors. Benchmarks show query performance dropping to **112 QPS** at this scale, with exponential I/O degradation. Migration is essential.

---

## Keep MiniLM embeddings but restructure how you represent JSON events

Your current all-MiniLM-L6-v2 model is actually well-suited for this use case—the key improvement lies in how you prepare structured JSON for embedding, not which model you use.

**The hybrid embedding strategy:**

Text embedding models fundamentally don't understand numbers—"0.00453" and "0.00452" may produce wildly different embeddings despite being nearly identical values. The solution is a **two-channel approach**: embed semantic content (event types, action descriptions) while storing numerical values (prices, timestamps, percentages) as **filterable metadata** in the vector database.

For each event, generate embedding text using templates rather than raw JSON:
```
Raw: {"type": "trade", "price": 0.0045, "change": 12.5}
Template: "Trade event with medium price increase of 12.5 percent"
```

Store the actual numerical values in Qdrant's payload fields for range filtering: `filter: {"price": {"gte": 0.004, "lte": 0.005}}`.

**Why MiniLM remains the right choice:**

At **$0 marginal cost** (local inference), your VPS can handle 50 events/second with a 4-core CPU using sentence-transformers with ONNX backend for 2-3x speedup. OpenAI text-embedding-3-small would cost approximately **$25 to embed 10M events** (1.25B tokens × $0.02/1M)—viable for initial batch but adds ongoing cost for real-time ingestion. The 384 dimensions mean **15GB vector storage** versus 60GB+ for 1536-dimensional models.

**Upgrade path if quality issues arise:** nomic-embed-text-v1.5 provides better MTEB scores (62.3% vs 56.3%) with flexible 256-768 dimensions, runs locally on similar hardware, and supports 8K context length versus MiniLM's 256 tokens.

---

## Complete streaming architecture from Socket.IO to vector store

Since n8n cannot maintain persistent WebSocket connections, the recommended architecture uses a dedicated Node.js bridge service.

**Component layout on your VPS:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Single VPS (~$50/month)                   │
│  ┌────────────────┐     ┌──────────────┐     ┌────────────┐ │
│  │ Socket.IO      │────▶│  RabbitMQ    │────▶│    n8n     │ │
│  │ Bridge (Node)  │     │  (Queue)     │     │ Workflows  │ │
│  │ ~100MB RAM     │     │  ~200MB RAM  │     │  ~2GB RAM  │ │
│  └────────────────┘     └──────────────┘     └─────┬──────┘ │
│                                                     │       │
│         ┌───────────────────────────────────────────┤       │
│         ↓                                           ↓       │
│  ┌──────────────┐                           ┌────────────┐  │
│  │   Qdrant     │                           │TimescaleDB │  │
│  │ ~2-4GB RAM   │                           │  ~2GB RAM  │  │
│  └──────────────┘                           └────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Socket.IO bridge implementation:**

The bridge connects to rugs.fun, buffers events in memory (configurable max size), and publishes batches to RabbitMQ every 50 events or 5 seconds (whichever comes first). This micro-batching approach balances latency against API efficiency—embedding batches of 20-50 events is **10x more efficient** than individual calls.

**Backpressure handling strategy:**

Multiple layers prevent cascade failures under burst traffic. The bridge monitors RabbitMQ queue depth and pauses ingestion if it exceeds 50,000 messages. RabbitMQ uses `x-max-length: 100000` with dead-letter routing for overflow. n8n's `N8N_CONCURRENCY_PRODUCTION_LIMIT=10` prevents execution overload. Within workflows, Loop Over Items with batch size 20 and 1-second Wait nodes between batches control downstream pressure.

**Historical JSONL ingestion approach:**

For 929+ recording files, bypass n8n entirely for initial load. A Python script using sentence-transformers and qdrant-client directly inserts embeddings—processing **~5,000 events/hour** with rate limiting. Estimated completion: 186 hours (run as background process over 1-2 weeks). Once complete, n8n handles all incremental real-time updates.

---

## Dual-database architecture enables analytics and anomaly detection

Vector databases have limited analytics capabilities—Qdrant supports only counting and faceted grouping, while Weaviate offers sum/avg/min/max. For time-windowed statistics, event counting by type, and trend analysis, add **TimescaleDB** as an analytics companion.

**Dual-write pattern in n8n:**

Each ingestion workflow writes events to both databases in parallel branches:
- **Qdrant**: Embedding + full event payload for semantic search
- **TimescaleDB**: Structured metadata (timestamp, event_type, numerical fields) in a hypertable for analytics

TimescaleDB's continuous aggregates pre-compute hourly/daily statistics automatically, enabling queries like "event count by type over last 7 days" without scanning raw data.

**Anomaly detection implementation:**

For real-time detection, n8n's Code node can run statistical methods (Z-score, IQR) on numerical fields using built-in JavaScript. For embedding-based anomaly detection (identifying unusual events in vector space), **Isolation Forest** works well—but requires n8n 2.0+ with Python task runners or an external microservice.

The recommended pipeline position: `Ingestion → Embedding → Anomaly Check → Branch (Normal: silent store / Anomaly: store + alert)`. Anomaly alerts route through Slack/Discord webhook or email.

**Resource requirements:**

Adding TimescaleDB uses approximately **2GB RAM** and **10GB storage** for 10M events with 90-day retention. Combined with n8n, Qdrant, and RabbitMQ, total requirement is **5-8GB RAM**—fitting comfortably on a single $50/month 8GB VPS.

---

## Exposing your RAG to external AI agents via MCP and REST

n8n supports two primary patterns for agent integration: the **MCP Server Trigger** for native AI agent tool discovery, and **Webhook endpoints** for REST API access.

**MCP Server integration:**

The MCP Server Trigger node exposes n8n workflows as discoverable tools for Claude, ChatGPT, and other MCP-compatible agents. Configure multiple tools within a single trigger—`query_events`, `count_by_type`, `detect_anomalies`—each routing to a specialized workflow. External agents connect via SSE transport with bearer token authentication. Key limitation: **5-minute execution timeout** per tool call.

Claude Desktop configuration:
```json
{
  "mcpServers": {
    "rugs-rag": {
      "transport": { "type": "sse", "url": "https://your-n8n/mcp/xxx" },
      "headers": { "Authorization": "Bearer TOKEN" }
    }
  }
}
```

**Query patterns your agents will need:**

Design tools for these four query types: **Aggregate** (count events by type in time window, requires TimescaleDB), **Comparative** (this week vs last week metrics), **Temporal** (recent events with semantic relevance), and **Anomaly** (detect unusual patterns, flag severity). Each maps to a dedicated n8n workflow that combines vector similarity search with metadata filtering.

**n8n AI Agent node for internal reasoning:**

The built-in AI Agent node supports multi-step reasoning with tool calling, connecting to OpenAI, Anthropic, or Ollama backends. Configure it with Vector Store tools for RAG retrieval and Workflow tools that call your analytics workflows. Memory options (Buffer, Postgres-backed) maintain conversation context.

---

## Implementation roadmap for phased upgrade

Given your existing ChromaDB system, migrate incrementally rather than attempting a complete cutover.

**Phase 1 (Weeks 1-2): Infrastructure foundation**

Deploy Docker Compose stack with n8n, RabbitMQ, and Qdrant on your VPS. Configure Qdrant with scalar quantization and on-disk vectors. Set up n8n credentials and test basic Qdrant Vector Store node operations. Create a simple ingestion workflow: RabbitMQ Trigger → Code Node (format event) → Qdrant Insert.

**Phase 2 (Weeks 3-4): Socket.IO bridge and real-time pipeline**

Build the Node.js Socket.IO client connecting to rugs.fun, publishing batched events to RabbitMQ. Implement backpressure monitoring and reconnection logic. Connect to n8n ingestion workflow and verify end-to-end data flow. Monitor memory usage and adjust batch sizes.

**Phase 3 (Weeks 5-6): Historical migration and embeddings refinement**

Run the Python bulk ingestion script for 929+ JSONL files as a background process. Implement semantic text templates for each of your 21 event types. Validate embedding quality with sample queries. Keep ChromaDB running in parallel for comparison.

**Phase 4 (Weeks 7-8): Analytics and agent integration**

Add TimescaleDB and implement dual-write pattern. Create continuous aggregates for common analytics queries. Build MCP Server tools for agent access. Set up anomaly detection pipeline with alerting. Decommission ChromaDB once Qdrant is validated.

**Phase 5 (Ongoing): Optimization and scaling**

Monitor query latency and adjust HNSW parameters. Implement retention policies for old events. Consider Redis cache for hot queries if latency exceeds targets. Evaluate upgrade to larger VPS only if metrics demand it.

**Estimated monthly costs at full deployment:**

| Component | Specification | Monthly Cost |
|-----------|--------------|--------------|
| VPS (Hetzner/DigitalOcean) | 8GB RAM, 4 vCPU, 160GB NVMe | $35-48 |
| Domain/SSL | Let's Encrypt | $0 |
| OpenAI (optional, for agent LLM) | ~100K tokens/month | $0-5 |
| **Total** | | **$35-53** |

This architecture handles your 10M+ event target with sub-100ms vector queries, provides the analytics capabilities missing from pure vector search, and exposes a clean API surface for AI agent interaction—all within your stated budget constraints.