# n8n RAG Parallel Development Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a parallel n8n-based RAG system with real-time WebSocket ingestion while keeping the current ChromaDB system operational.

**Architecture:** Queue-buffered pipeline using Socket.IO bridge → RabbitMQ → n8n workflows → Qdrant vector store. New system lives in `rag-pipeline-v2/` directory, completely isolated from existing `rag-pipeline/`. Cutover happens only after validation proves the new system exceeds current capabilities.

**Tech Stack:** n8n (self-hosted), Qdrant (self-hosted with quantization), RabbitMQ (message queue), Node.js (Socket.IO bridge), MiniLM embeddings (reuse existing model)

---

## Phase Overview

| Phase | Description | Tasks | Est. Time |
|-------|-------------|-------|-----------|
| 1 | Infrastructure Setup | 1-5 | 2-3 hours |
| 2 | Socket.IO Bridge | 6-10 | 2-3 hours |
| 3 | n8n Ingestion Workflows | 11-16 | 3-4 hours |
| 4 | Data Migration | 17-20 | 2-3 hours |
| 5 | MCP Integration | 21-24 | 2-3 hours |
| 6 | Validation & Cutover | 25-28 | 2-3 hours |

**Total: ~15-20 hours across multiple sessions**

---

## Phase 1: Infrastructure Setup

### Task 1: Create v2 Directory Structure

**Files:**
- Create: `rag-pipeline-v2/`
- Create: `rag-pipeline-v2/CONTEXT.md`
- Create: `rag-pipeline-v2/.gitignore`

**Step 1: Create directory structure**

```bash
mkdir -p /home/nomad/Desktop/claude-flow/rag-pipeline-v2/{bridge,n8n-workflows,scripts,tests}
```

**Step 2: Create CONTEXT.md**

Create file `rag-pipeline-v2/CONTEXT.md`:
```markdown
# RAG Pipeline v2 - Agent Context

## Purpose
Next-generation RAG system with real-time WebSocket ingestion via n8n orchestration.

## Architecture
```
Socket.IO (rugs.fun) → Bridge (Node.js) → RabbitMQ → n8n → Qdrant
```

## Status
- [ ] Phase 1: Infrastructure
- [ ] Phase 2: Socket.IO Bridge
- [ ] Phase 3: n8n Workflows
- [ ] Phase 4: Data Migration
- [ ] Phase 5: MCP Integration
- [ ] Phase 6: Validation

## Parallel Development
This system runs alongside `rag-pipeline/` (ChromaDB).
Current system remains operational until v2 proves superior.

## Cutover Criteria
1. Query latency < 100ms (p95)
2. Real-time ingestion working (50+ events/sec)
3. All current queries return equivalent results
4. Zero data loss during 24h test period
```

**Step 3: Create .gitignore**

Create file `rag-pipeline-v2/.gitignore`:
```
# Docker volumes
docker-data/
n8n-data/
qdrant-data/
rabbitmq-data/

# Node modules
bridge/node_modules/

# Environment
.env
.env.local

# Logs
*.log
```

**Step 4: Commit**

```bash
cd /home/nomad/Desktop/claude-flow
git add rag-pipeline-v2/
git commit -m "feat(rag-v2): initialize parallel RAG pipeline structure"
```

---

### Task 2: Create Docker Compose Configuration

**Files:**
- Create: `rag-pipeline-v2/docker-compose.yml`
- Create: `rag-pipeline-v2/.env.example`

**Step 1: Create Docker Compose file**

Create file `rag-pipeline-v2/docker-compose.yml`:
```yaml
version: '3.8'

services:
  # Message Queue - buffers WebSocket events
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rag-v2-rabbitmq
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-rag}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS:-rag_secret}
    volumes:
      - ./docker-data/rabbitmq:/var/lib/rabbitmq
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Vector Database - stores embeddings
  qdrant:
    image: qdrant/qdrant:latest
    container_name: rag-v2-qdrant
    ports:
      - "6333:6333"  # REST API
      - "6334:6334"  # gRPC
    volumes:
      - ./docker-data/qdrant:/qdrant/storage
    environment:
      QDRANT__SERVICE__GRPC_PORT: 6334
      # Enable scalar quantization for memory efficiency
      QDRANT__STORAGE__ON_DISK_PAYLOAD: "true"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Workflow Orchestration
  n8n:
    image: n8nio/n8n:latest
    container_name: rag-v2-n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASS:-admin_secret}
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - N8N_CONCURRENCY_PRODUCTION_LIMIT=10
      - EXECUTIONS_TIMEOUT=300
      - EXECUTIONS_TIMEOUT_MAX=600
    volumes:
      - ./docker-data/n8n:/home/node/.n8n
      - ./n8n-workflows:/home/node/workflows
    depends_on:
      rabbitmq:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    restart: unless-stopped

networks:
  default:
    name: rag-v2-network
```

**Step 2: Create environment example**

Create file `rag-pipeline-v2/.env.example`:
```bash
# RabbitMQ
RABBITMQ_USER=rag
RABBITMQ_PASS=change_me_in_production

# n8n
N8N_USER=admin
N8N_PASS=change_me_in_production

# Qdrant (no auth by default, add if needed)
# QDRANT_API_KEY=optional_key

# Socket.IO Bridge
RUGS_WEBSOCKET_URL=wss://rugs.fun
BATCH_SIZE=50
BATCH_TIMEOUT_MS=5000
```

**Step 3: Commit**

```bash
git add rag-pipeline-v2/docker-compose.yml rag-pipeline-v2/.env.example
git commit -m "feat(rag-v2): add Docker Compose for n8n/Qdrant/RabbitMQ stack"
```

---

### Task 3: Create Infrastructure Startup Script

**Files:**
- Create: `rag-pipeline-v2/scripts/start.sh`
- Create: `rag-pipeline-v2/scripts/stop.sh`
- Create: `rag-pipeline-v2/scripts/status.sh`

**Step 1: Create start script**

Create file `rag-pipeline-v2/scripts/start.sh`:
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check for .env file
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "WARNING: Edit .env to change default passwords!"
fi

# Create data directories
mkdir -p docker-data/{rabbitmq,qdrant,n8n}

# Start services
echo "Starting RAG v2 infrastructure..."
docker compose up -d

# Wait for health checks
echo "Waiting for services to be healthy..."
sleep 10

# Check status
docker compose ps

echo ""
echo "=== RAG v2 Services ==="
echo "RabbitMQ Management: http://localhost:15672"
echo "Qdrant Dashboard:    http://localhost:6333/dashboard"
echo "n8n Workflow UI:     http://localhost:5678"
echo ""
echo "Credentials in .env file"
```

**Step 2: Create stop script**

Create file `rag-pipeline-v2/scripts/stop.sh`:
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "Stopping RAG v2 infrastructure..."
docker compose down

echo "Services stopped. Data preserved in docker-data/"
```

**Step 3: Create status script**

Create file `rag-pipeline-v2/scripts/status.sh`:
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "=== RAG v2 Service Status ==="
docker compose ps

echo ""
echo "=== RabbitMQ Queue Status ==="
curl -s -u ${RABBITMQ_USER:-rag}:${RABBITMQ_PASS:-rag_secret} \
    http://localhost:15672/api/queues 2>/dev/null | \
    python3 -c "import sys,json; queues=json.load(sys.stdin); print(f'Queues: {len(queues)}')" || \
    echo "RabbitMQ not accessible"

echo ""
echo "=== Qdrant Collections ==="
curl -s http://localhost:6333/collections 2>/dev/null | \
    python3 -c "import sys,json; cols=json.load(sys.stdin)['result']['collections']; print(f'Collections: {len(cols)}')" || \
    echo "Qdrant not accessible"
```

**Step 4: Make scripts executable**

```bash
chmod +x rag-pipeline-v2/scripts/*.sh
```

**Step 5: Commit**

```bash
git add rag-pipeline-v2/scripts/
git commit -m "feat(rag-v2): add infrastructure management scripts"
```

---

### Task 4: Test Infrastructure Startup

**Step 1: Start the infrastructure**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2
./scripts/start.sh
```

**Step 2: Verify services are running**

```bash
./scripts/status.sh
```

Expected output: All 3 services (rabbitmq, qdrant, n8n) showing as "Up"

**Step 3: Test RabbitMQ connection**

```bash
curl -s -u rag:rag_secret http://localhost:15672/api/overview | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'RabbitMQ: {d[\"rabbitmq_version\"]}')"
```

Expected: `RabbitMQ: 3.x.x`

**Step 4: Test Qdrant connection**

```bash
curl -s http://localhost:6333/ | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Qdrant: {d[\"title\"]}')"
```

Expected: `Qdrant: qdrant - vectorass database`

**Step 5: Test n8n connection**

Open browser: http://localhost:5678
Expected: n8n login page

**Step 6: Document results**

If all tests pass, infrastructure is ready. If any fail, check `docker compose logs <service>`.

---

### Task 5: Create Qdrant Collection

**Files:**
- Create: `rag-pipeline-v2/scripts/setup_qdrant.py`

**Step 1: Create setup script**

Create file `rag-pipeline-v2/scripts/setup_qdrant.py`:
```python
#!/usr/bin/env python3
"""Initialize Qdrant collection for RAG v2."""
import requests
import sys

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rugs_events_v2"
EMBEDDING_DIM = 384  # MiniLM dimensions


def create_collection():
    """Create the vector collection with optimal settings."""

    # Check if collection exists
    resp = requests.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
    if resp.status_code == 200:
        print(f"Collection '{COLLECTION_NAME}' already exists")
        info = resp.json()["result"]
        print(f"  Vectors: {info.get('vectors_count', 0)}")
        print(f"  Points: {info.get('points_count', 0)}")
        return True

    # Create collection with scalar quantization
    config = {
        "vectors": {
            "size": EMBEDDING_DIM,
            "distance": "Cosine",
            "on_disk": True,  # Store vectors on disk for memory efficiency
        },
        "quantization_config": {
            "scalar": {
                "type": "int8",
                "quantile": 0.99,
                "always_ram": True,  # Keep quantized vectors in RAM
            }
        },
        "optimizers_config": {
            "indexing_threshold": 20000,  # Build index after 20k vectors
        },
        "on_disk_payload": True,  # Store payload on disk
    }

    resp = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}",
        json=config,
    )

    if resp.status_code == 200:
        print(f"Created collection '{COLLECTION_NAME}'")
        print(f"  Dimensions: {EMBEDDING_DIM}")
        print(f"  Distance: Cosine")
        print(f"  Quantization: int8 scalar")
        return True
    else:
        print(f"Failed to create collection: {resp.text}")
        return False


def create_payload_indexes():
    """Create indexes for common filter fields."""
    indexes = [
        ("event_type", "keyword"),
        ("game_id", "keyword"),
        ("timestamp", "integer"),
        ("source", "keyword"),
    ]

    for field, field_type in indexes:
        resp = requests.put(
            f"{QDRANT_URL}/collections/{COLLECTION_NAME}/index",
            json={
                "field_name": field,
                "field_schema": field_type,
            },
        )
        if resp.status_code == 200:
            print(f"  Created index: {field} ({field_type})")
        else:
            print(f"  Index {field} may already exist or failed")


if __name__ == "__main__":
    print("=== Qdrant Collection Setup ===")

    # Test connection
    try:
        resp = requests.get(f"{QDRANT_URL}/")
        resp.raise_for_status()
    except Exception as e:
        print(f"Cannot connect to Qdrant at {QDRANT_URL}: {e}")
        sys.exit(1)

    if create_collection():
        print("\nCreating payload indexes...")
        create_payload_indexes()
        print("\nSetup complete!")
    else:
        sys.exit(1)
```

**Step 2: Run setup script**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2
python3 scripts/setup_qdrant.py
```

Expected output:
```
=== Qdrant Collection Setup ===
Created collection 'rugs_events_v2'
  Dimensions: 384
  Distance: Cosine
  Quantization: int8 scalar

Creating payload indexes...
  Created index: event_type (keyword)
  Created index: game_id (keyword)
  Created index: timestamp (integer)
  Created index: source (keyword)

Setup complete!
```

**Step 3: Verify in Qdrant dashboard**

Open http://localhost:6333/dashboard and confirm collection exists.

**Step 4: Commit**

```bash
git add rag-pipeline-v2/scripts/setup_qdrant.py
git commit -m "feat(rag-v2): add Qdrant collection setup with quantization"
```

---

## Phase 2: Socket.IO Bridge

### Task 6: Initialize Node.js Bridge Project

**Files:**
- Create: `rag-pipeline-v2/bridge/package.json`
- Create: `rag-pipeline-v2/bridge/tsconfig.json`

**Step 1: Create package.json**

Create file `rag-pipeline-v2/bridge/package.json`:
```json
{
  "name": "rugs-websocket-bridge",
  "version": "1.0.0",
  "description": "Bridge from rugs.fun WebSocket to RabbitMQ for n8n RAG pipeline",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "test": "jest"
  },
  "dependencies": {
    "amqplib": "^0.10.4",
    "dotenv": "^16.3.1",
    "socket.io-client": "^4.7.2",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "@types/amqplib": "^0.10.4",
    "@types/node": "^20.10.0",
    "typescript": "^5.3.0",
    "ts-node": "^10.9.2"
  }
}
```

**Step 2: Create tsconfig.json**

Create file `rag-pipeline-v2/bridge/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Step 3: Install dependencies**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2/bridge
npm install
```

**Step 4: Commit**

```bash
git add rag-pipeline-v2/bridge/package.json rag-pipeline-v2/bridge/tsconfig.json
git commit -m "feat(rag-v2): initialize Socket.IO bridge Node.js project"
```

---

### Task 7: Create Bridge Configuration

**Files:**
- Create: `rag-pipeline-v2/bridge/src/config.ts`

**Step 1: Create config module**

Create file `rag-pipeline-v2/bridge/src/config.ts`:
```typescript
import dotenv from 'dotenv';
import path from 'path';

// Load .env from parent directory
dotenv.config({ path: path.join(__dirname, '../../.env') });

export const config = {
  // WebSocket connection
  websocket: {
    url: process.env.RUGS_WEBSOCKET_URL || 'wss://rugs.fun',
    reconnectInterval: parseInt(process.env.RECONNECT_INTERVAL || '5000'),
    maxReconnectAttempts: parseInt(process.env.MAX_RECONNECT_ATTEMPTS || '10'),
  },

  // RabbitMQ connection
  rabbitmq: {
    url: process.env.RABBITMQ_URL || 'amqp://rag:rag_secret@localhost:5672',
    queue: process.env.RABBITMQ_QUEUE || 'rugs_events',
    exchange: process.env.RABBITMQ_EXCHANGE || 'rugs_events_exchange',
  },

  // Batching configuration
  batch: {
    size: parseInt(process.env.BATCH_SIZE || '50'),
    timeoutMs: parseInt(process.env.BATCH_TIMEOUT_MS || '5000'),
    maxQueueDepth: parseInt(process.env.MAX_QUEUE_DEPTH || '50000'),
  },

  // Logging
  log: {
    level: process.env.LOG_LEVEL || 'info',
  },
};

export type Config = typeof config;
```

**Step 2: Commit**

```bash
mkdir -p rag-pipeline-v2/bridge/src
git add rag-pipeline-v2/bridge/src/config.ts
git commit -m "feat(rag-v2): add bridge configuration module"
```

---

### Task 8: Create Logger Module

**Files:**
- Create: `rag-pipeline-v2/bridge/src/logger.ts`

**Step 1: Create logger**

Create file `rag-pipeline-v2/bridge/src/logger.ts`:
```typescript
import winston from 'winston';
import { config } from './config';

export const logger = winston.createLogger({
  level: config.log.level,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.printf(({ timestamp, level, message, ...meta }) => {
      const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
      return `${timestamp} [${level.toUpperCase()}] ${message} ${metaStr}`;
    })
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({
      filename: 'bridge-error.log',
      level: 'error',
    }),
    new winston.transports.File({
      filename: 'bridge.log',
    }),
  ],
});
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/bridge/src/logger.ts
git commit -m "feat(rag-v2): add bridge logger with Winston"
```

---

### Task 9: Create RabbitMQ Publisher

**Files:**
- Create: `rag-pipeline-v2/bridge/src/publisher.ts`

**Step 1: Create publisher module**

Create file `rag-pipeline-v2/bridge/src/publisher.ts`:
```typescript
import amqp, { Channel, Connection } from 'amqplib';
import { config } from './config';
import { logger } from './logger';

export interface EventBatch {
  events: any[];
  timestamp: number;
  batchId: string;
}

export class RabbitMQPublisher {
  private connection: Connection | null = null;
  private channel: Channel | null = null;
  private isConnected = false;

  async connect(): Promise<void> {
    try {
      logger.info('Connecting to RabbitMQ...', { url: config.rabbitmq.url.replace(/:[^:]*@/, ':***@') });

      this.connection = await amqp.connect(config.rabbitmq.url);
      this.channel = await this.connection.createChannel();

      // Declare exchange and queue
      await this.channel.assertExchange(config.rabbitmq.exchange, 'direct', { durable: true });
      await this.channel.assertQueue(config.rabbitmq.queue, {
        durable: true,
        arguments: {
          'x-max-length': config.batch.maxQueueDepth,
          'x-overflow': 'reject-publish',
        },
      });
      await this.channel.bindQueue(
        config.rabbitmq.queue,
        config.rabbitmq.exchange,
        'rugs.event'
      );

      this.isConnected = true;
      logger.info('Connected to RabbitMQ');

      // Handle connection close
      this.connection.on('close', () => {
        logger.warn('RabbitMQ connection closed');
        this.isConnected = false;
      });

      this.connection.on('error', (err) => {
        logger.error('RabbitMQ connection error', { error: err.message });
        this.isConnected = false;
      });

    } catch (error) {
      logger.error('Failed to connect to RabbitMQ', { error });
      throw error;
    }
  }

  async publish(batch: EventBatch): Promise<boolean> {
    if (!this.channel || !this.isConnected) {
      logger.error('Cannot publish: not connected to RabbitMQ');
      return false;
    }

    try {
      const message = Buffer.from(JSON.stringify(batch));

      const success = this.channel.publish(
        config.rabbitmq.exchange,
        'rugs.event',
        message,
        {
          persistent: true,
          contentType: 'application/json',
          timestamp: Date.now(),
          headers: {
            batchSize: batch.events.length,
            batchId: batch.batchId,
          },
        }
      );

      if (success) {
        logger.debug('Published batch', {
          batchId: batch.batchId,
          eventCount: batch.events.length,
        });
      } else {
        logger.warn('Channel write buffer full, batch may be delayed');
      }

      return success;

    } catch (error) {
      logger.error('Failed to publish batch', { error, batchId: batch.batchId });
      return false;
    }
  }

  async getQueueDepth(): Promise<number> {
    if (!this.channel) return -1;

    try {
      const info = await this.channel.checkQueue(config.rabbitmq.queue);
      return info.messageCount;
    } catch {
      return -1;
    }
  }

  async close(): Promise<void> {
    if (this.channel) {
      await this.channel.close();
    }
    if (this.connection) {
      await this.connection.close();
    }
    this.isConnected = false;
    logger.info('RabbitMQ connection closed');
  }
}
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/bridge/src/publisher.ts
git commit -m "feat(rag-v2): add RabbitMQ publisher with backpressure handling"
```

---

### Task 10: Create Main Bridge Entry Point

**Files:**
- Create: `rag-pipeline-v2/bridge/src/index.ts`

**Step 1: Create main entry point**

Create file `rag-pipeline-v2/bridge/src/index.ts`:
```typescript
import { io, Socket } from 'socket.io-client';
import { v4 as uuidv4 } from 'uuid';
import { config } from './config';
import { logger } from './logger';
import { RabbitMQPublisher, EventBatch } from './publisher';

class WebSocketBridge {
  private socket: Socket | null = null;
  private publisher: RabbitMQPublisher;
  private eventBuffer: any[] = [];
  private batchTimer: NodeJS.Timeout | null = null;
  private isPaused = false;
  private stats = {
    eventsReceived: 0,
    batchesPublished: 0,
    errors: 0,
  };

  constructor() {
    this.publisher = new RabbitMQPublisher();
  }

  async start(): Promise<void> {
    logger.info('Starting WebSocket bridge...');

    // Connect to RabbitMQ first
    await this.publisher.connect();

    // Connect to WebSocket
    this.connectWebSocket();

    // Start batch timer
    this.startBatchTimer();

    // Periodic stats logging
    setInterval(() => this.logStats(), 60000);

    // Backpressure monitoring
    setInterval(() => this.checkBackpressure(), 5000);

    logger.info('WebSocket bridge started');
  }

  private connectWebSocket(): void {
    logger.info('Connecting to WebSocket...', { url: config.websocket.url });

    this.socket = io(config.websocket.url, {
      transports: ['websocket'],
      reconnection: true,
      reconnectionAttempts: config.websocket.maxReconnectAttempts,
      reconnectionDelay: config.websocket.reconnectInterval,
    });

    this.socket.on('connect', () => {
      logger.info('WebSocket connected', { id: this.socket?.id });
    });

    this.socket.on('disconnect', (reason) => {
      logger.warn('WebSocket disconnected', { reason });
    });

    this.socket.on('connect_error', (error) => {
      logger.error('WebSocket connection error', { error: error.message });
      this.stats.errors++;
    });

    // Listen for all rugs.fun events
    const eventTypes = [
      'gameStateUpdate',
      'playerUpdate',
      'sidebetUpdate',
      'priceUpdate',
      'newGame',
      'gameEnded',
      'rugPull',
      'phaseChange',
    ];

    for (const eventType of eventTypes) {
      this.socket.on(eventType, (data: any) => {
        this.handleEvent(eventType, data);
      });
    }

    // Catch-all for unknown events
    this.socket.onAny((eventName: string, data: any) => {
      if (!eventTypes.includes(eventName)) {
        this.handleEvent(eventName, data);
      }
    });
  }

  private handleEvent(eventType: string, data: any): void {
    if (this.isPaused) {
      logger.debug('Event dropped (paused)', { eventType });
      return;
    }

    const enrichedEvent = {
      type: eventType,
      data,
      receivedAt: Date.now(),
      bridgeId: process.env.BRIDGE_ID || 'default',
    };

    this.eventBuffer.push(enrichedEvent);
    this.stats.eventsReceived++;

    // Flush if buffer reaches batch size
    if (this.eventBuffer.length >= config.batch.size) {
      this.flushBuffer();
    }
  }

  private startBatchTimer(): void {
    this.batchTimer = setInterval(() => {
      if (this.eventBuffer.length > 0) {
        this.flushBuffer();
      }
    }, config.batch.timeoutMs);
  }

  private async flushBuffer(): Promise<void> {
    if (this.eventBuffer.length === 0) return;

    const events = this.eventBuffer.splice(0, config.batch.size);
    const batch: EventBatch = {
      events,
      timestamp: Date.now(),
      batchId: uuidv4(),
    };

    const success = await this.publisher.publish(batch);
    if (success) {
      this.stats.batchesPublished++;
    } else {
      // Re-queue events on failure (at front of buffer)
      this.eventBuffer.unshift(...events);
      this.stats.errors++;
    }
  }

  private async checkBackpressure(): Promise<void> {
    const queueDepth = await this.publisher.getQueueDepth();

    if (queueDepth > config.batch.maxQueueDepth * 0.8) {
      if (!this.isPaused) {
        logger.warn('Pausing ingestion due to backpressure', { queueDepth });
        this.isPaused = true;
      }
    } else if (queueDepth < config.batch.maxQueueDepth * 0.5) {
      if (this.isPaused) {
        logger.info('Resuming ingestion', { queueDepth });
        this.isPaused = false;
      }
    }
  }

  private logStats(): void {
    logger.info('Bridge statistics', {
      eventsReceived: this.stats.eventsReceived,
      batchesPublished: this.stats.batchesPublished,
      errors: this.stats.errors,
      bufferSize: this.eventBuffer.length,
      isPaused: this.isPaused,
    });
  }

  async stop(): Promise<void> {
    logger.info('Stopping WebSocket bridge...');

    if (this.batchTimer) {
      clearInterval(this.batchTimer);
    }

    // Flush remaining events
    await this.flushBuffer();

    if (this.socket) {
      this.socket.disconnect();
    }

    await this.publisher.close();

    logger.info('WebSocket bridge stopped');
  }
}

// Main entry point
const bridge = new WebSocketBridge();

process.on('SIGINT', async () => {
  await bridge.stop();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await bridge.stop();
  process.exit(0);
});

bridge.start().catch((error) => {
  logger.error('Failed to start bridge', { error });
  process.exit(1);
});
```

**Step 2: Add uuid dependency**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2/bridge
npm install uuid
npm install --save-dev @types/uuid
```

**Step 3: Update package.json with uuid**

The npm install commands above will update package.json automatically.

**Step 4: Build and test**

```bash
npm run build
```

Expected: Compiles without errors to `dist/` directory.

**Step 5: Commit**

```bash
git add rag-pipeline-v2/bridge/
git commit -m "feat(rag-v2): complete Socket.IO to RabbitMQ bridge implementation"
```

---

## Phase 3: n8n Ingestion Workflows

### Task 11: Create n8n Workflow - Event Consumer

**Files:**
- Create: `rag-pipeline-v2/n8n-workflows/01-event-consumer.json`

**Step 1: Create the workflow JSON**

Create file `rag-pipeline-v2/n8n-workflows/01-event-consumer.json`:
```json
{
  "name": "RAG v2 - Event Consumer",
  "nodes": [
    {
      "parameters": {
        "queue": "rugs_events",
        "options": {
          "acknowledge": "immediately"
        }
      },
      "id": "rabbitmq-trigger",
      "name": "RabbitMQ Trigger",
      "type": "n8n-nodes-base.rabbitMqTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "jsCode": "// Parse the batch from RabbitMQ\nconst batch = JSON.parse($input.first().json.content);\n\n// Extract individual events\nconst events = batch.events.map(event => ({\n  json: {\n    ...event,\n    batchId: batch.batchId,\n    batchTimestamp: batch.timestamp\n  }\n}));\n\nreturn events;"
      },
      "id": "parse-batch",
      "name": "Parse Batch",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 300]
    },
    {
      "parameters": {
        "batchSize": 20,
        "options": {}
      },
      "id": "batch-events",
      "name": "Batch Events",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [650, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:5678/webhook/embed-events",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "events",
              "value": "={{ $json }}"
            }
          ]
        },
        "options": {}
      },
      "id": "call-embed",
      "name": "Call Embed Workflow",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [850, 300]
    }
  ],
  "connections": {
    "RabbitMQ Trigger": {
      "main": [[{ "node": "Parse Batch", "type": "main", "index": 0 }]]
    },
    "Parse Batch": {
      "main": [[{ "node": "Batch Events", "type": "main", "index": 0 }]]
    },
    "Batch Events": {
      "main": [[{ "node": "Call Embed Workflow", "type": "main", "index": 0 }]]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  }
}
```

**Step 2: Document manual import steps**

Since n8n workflows are imported via UI, document the process:
- Open http://localhost:5678
- Go to Workflows → Import from File
- Select `01-event-consumer.json`
- Configure RabbitMQ credentials
- Activate workflow

**Step 3: Commit**

```bash
git add rag-pipeline-v2/n8n-workflows/
git commit -m "feat(rag-v2): add n8n event consumer workflow template"
```

---

### Task 12: Create Embedding Service

**Files:**
- Create: `rag-pipeline-v2/scripts/embedding_service.py`

**Step 1: Create embedding HTTP service**

Create file `rag-pipeline-v2/scripts/embedding_service.py`:
```python
#!/usr/bin/env python3
"""
Embedding service for n8n RAG pipeline.
Receives events via HTTP, generates embeddings, stores in Qdrant.
"""
import json
import sys
from pathlib import Path
from typing import Any

from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import hashlib
import time

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rugs_events_v2"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Initialize
app = Flask(__name__)
model = SentenceTransformer(EMBEDDING_MODEL)
qdrant = QdrantClient(url=QDRANT_URL)


def event_to_text(event: dict) -> str:
    """Convert event to semantic text for embedding.

    Uses templates instead of raw JSON for better embedding quality.
    Numerical values are stored as metadata, not embedded.
    """
    event_type = event.get("type", "unknown")
    data = event.get("data", {})

    templates = {
        "gameStateUpdate": lambda d: f"Game state update: phase {d.get('phase', 'unknown')}, "
                                     f"players {d.get('playerCount', 0)}, "
                                     f"price movement {d.get('priceChangePercent', 0):.1f}%",

        "playerUpdate": lambda d: f"Player update: {d.get('action', 'activity')} "
                                  f"by player in game",

        "sidebetUpdate": lambda d: f"Sidebet update: {d.get('type', 'bet')} placed, "
                                   f"outcome {d.get('outcome', 'pending')}",

        "priceUpdate": lambda d: f"Price update: multiplier at {d.get('multiplier', 1)}x",

        "newGame": lambda d: f"New game started: {d.get('gameId', 'unknown')}",

        "gameEnded": lambda d: f"Game ended: final multiplier {d.get('finalMultiplier', 0)}x",

        "rugPull": lambda d: f"Rug pull event: game rugged at {d.get('multiplier', 0)}x",

        "phaseChange": lambda d: f"Phase change: transitioned to {d.get('newPhase', 'unknown')}",
    }

    template = templates.get(event_type, lambda d: f"{event_type} event occurred")

    try:
        return template(data)
    except Exception:
        return f"{event_type} event with data"


def extract_metadata(event: dict) -> dict:
    """Extract numerical and categorical metadata for filtering."""
    data = event.get("data", {})

    metadata = {
        "event_type": event.get("type", "unknown"),
        "timestamp": event.get("receivedAt", int(time.time() * 1000)),
        "source": "websocket_live",
    }

    # Extract numerical fields for filtering
    if "gameId" in data:
        metadata["game_id"] = str(data["gameId"])
    if "multiplier" in data:
        metadata["multiplier"] = float(data["multiplier"])
    if "phase" in data:
        metadata["phase"] = str(data["phase"])
    if "playerCount" in data:
        metadata["player_count"] = int(data["playerCount"])

    return metadata


def generate_id(event: dict) -> str:
    """Generate deterministic ID from event content."""
    content = json.dumps(event, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:32]


@app.route("/embed", methods=["POST"])
def embed_events():
    """Receive events, embed them, store in Qdrant."""
    try:
        events = request.json.get("events", [])
        if not events:
            return jsonify({"error": "No events provided"}), 400

        # Prepare for embedding
        texts = [event_to_text(e) for e in events]

        # Generate embeddings (batch)
        embeddings = model.encode(texts, convert_to_numpy=True)

        # Prepare Qdrant points
        points = []
        for i, event in enumerate(events):
            point = PointStruct(
                id=generate_id(event),
                vector=embeddings[i].tolist(),
                payload={
                    "text": texts[i],
                    "raw_event": json.dumps(event),
                    **extract_metadata(event),
                },
            )
            points.append(point)

        # Upsert to Qdrant
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

        return jsonify({
            "status": "success",
            "embedded": len(events),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    try:
        # Check Qdrant
        qdrant.get_collection(COLLECTION_NAME)
        return jsonify({"status": "healthy"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/stats", methods=["GET"])
def stats():
    """Get collection statistics."""
    try:
        info = qdrant.get_collection(COLLECTION_NAME)
        return jsonify({
            "collection": COLLECTION_NAME,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    # Warm up the model
    _ = model.encode(["warmup"])
    print("Model loaded, starting server...")

    app.run(host="0.0.0.0", port=5001, debug=False)
```

**Step 2: Create requirements file**

Create file `rag-pipeline-v2/requirements.txt`:
```
flask>=3.0.0
sentence-transformers>=2.2.0
qdrant-client>=1.7.0
requests>=2.31.0
```

**Step 3: Commit**

```bash
git add rag-pipeline-v2/scripts/embedding_service.py rag-pipeline-v2/requirements.txt
git commit -m "feat(rag-v2): add embedding HTTP service for n8n integration"
```

---

### Task 13: Create n8n Workflow - Embedding Webhook

**Files:**
- Create: `rag-pipeline-v2/n8n-workflows/02-embed-events.json`

**Step 1: Create webhook workflow**

Create file `rag-pipeline-v2/n8n-workflows/02-embed-events.json`:
```json
{
  "name": "RAG v2 - Embed Events",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "embed-events",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [250, 300],
      "webhookId": "embed-events"
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://host.docker.internal:5001/embed",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({ events: $json.events }) }}",
        "options": {
          "timeout": 30000
        }
      },
      "id": "call-embed-service",
      "name": "Call Embedding Service",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      },
      "id": "respond",
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Call Embedding Service", "type": "main", "index": 0 }]]
    },
    "Call Embedding Service": {
      "main": [[{ "node": "Respond", "type": "main", "index": 0 }]]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  }
}
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/n8n-workflows/02-embed-events.json
git commit -m "feat(rag-v2): add n8n embedding webhook workflow"
```

---

### Task 14: Create Query Service

**Files:**
- Create: `rag-pipeline-v2/scripts/query_service.py`

**Step 1: Create query HTTP service**

Create file `rag-pipeline-v2/scripts/query_service.py`:
```python
#!/usr/bin/env python3
"""
Query service for n8n RAG pipeline.
Provides semantic search over Qdrant vector store.
"""
import json
from typing import Any, Optional

from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rugs_events_v2"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 10

# Initialize
app = Flask(__name__)
model = SentenceTransformer(EMBEDDING_MODEL)
qdrant = QdrantClient(url=QDRANT_URL)


def build_filter(filters: dict) -> Optional[Filter]:
    """Build Qdrant filter from request parameters."""
    conditions = []

    if "event_type" in filters:
        conditions.append(
            FieldCondition(
                key="event_type",
                match=MatchValue(value=filters["event_type"]),
            )
        )

    if "game_id" in filters:
        conditions.append(
            FieldCondition(
                key="game_id",
                match=MatchValue(value=filters["game_id"]),
            )
        )

    if "min_multiplier" in filters or "max_multiplier" in filters:
        conditions.append(
            FieldCondition(
                key="multiplier",
                range=Range(
                    gte=filters.get("min_multiplier"),
                    lte=filters.get("max_multiplier"),
                ),
            )
        )

    if "phase" in filters:
        conditions.append(
            FieldCondition(
                key="phase",
                match=MatchValue(value=filters["phase"]),
            )
        )

    if "min_timestamp" in filters or "max_timestamp" in filters:
        conditions.append(
            FieldCondition(
                key="timestamp",
                range=Range(
                    gte=filters.get("min_timestamp"),
                    lte=filters.get("max_timestamp"),
                ),
            )
        )

    if not conditions:
        return None

    return Filter(must=conditions)


@app.route("/search", methods=["POST"])
def search():
    """Semantic search over events."""
    try:
        data = request.json or {}
        query = data.get("query", "")
        top_k = data.get("top_k", DEFAULT_TOP_K)
        filters = data.get("filters", {})

        if not query:
            return jsonify({"error": "Query required"}), 400

        # Generate query embedding
        query_embedding = model.encode(query).tolist()

        # Build filter
        qdrant_filter = build_filter(filters)

        # Search
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=qdrant_filter,
            limit=top_k,
            with_payload=True,
        )

        # Format results
        formatted = []
        for hit in results:
            payload = hit.payload or {}
            formatted.append({
                "score": hit.score,
                "text": payload.get("text", ""),
                "event_type": payload.get("event_type", ""),
                "game_id": payload.get("game_id", ""),
                "timestamp": payload.get("timestamp", 0),
                "multiplier": payload.get("multiplier"),
                "phase": payload.get("phase"),
                "raw_event": payload.get("raw_event", "{}"),
            })

        return jsonify({
            "query": query,
            "results": formatted,
            "count": len(formatted),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/aggregate", methods=["POST"])
def aggregate():
    """Get aggregate statistics (using scroll + compute)."""
    try:
        data = request.json or {}
        filters = data.get("filters", {})
        group_by = data.get("group_by", "event_type")

        qdrant_filter = build_filter(filters)

        # Scroll through all matching points
        counts = {}
        offset = None

        while True:
            results, offset = qdrant.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=qdrant_filter,
                limit=1000,
                offset=offset,
                with_payload=[group_by],
            )

            if not results:
                break

            for point in results:
                key = point.payload.get(group_by, "unknown")
                counts[key] = counts.get(key, 0) + 1

            if offset is None:
                break

        return jsonify({
            "group_by": group_by,
            "counts": counts,
            "total": sum(counts.values()),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/recent", methods=["GET"])
def recent():
    """Get most recent events."""
    try:
        limit = request.args.get("limit", 20, type=int)
        event_type = request.args.get("event_type")

        filters = {}
        if event_type:
            filters["event_type"] = event_type

        qdrant_filter = build_filter(filters)

        # Get recent by timestamp (scroll with filter, sort client-side)
        results, _ = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=qdrant_filter,
            limit=limit * 2,  # Over-fetch then sort
            with_payload=True,
        )

        # Sort by timestamp descending
        sorted_results = sorted(
            results,
            key=lambda p: p.payload.get("timestamp", 0),
            reverse=True,
        )[:limit]

        formatted = []
        for point in sorted_results:
            payload = point.payload or {}
            formatted.append({
                "text": payload.get("text", ""),
                "event_type": payload.get("event_type", ""),
                "timestamp": payload.get("timestamp", 0),
                "game_id": payload.get("game_id", ""),
            })

        return jsonify({
            "events": formatted,
            "count": len(formatted),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    _ = model.encode(["warmup"])
    print("Model loaded, starting query service...")

    app.run(host="0.0.0.0", port=5002, debug=False)
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/scripts/query_service.py
git commit -m "feat(rag-v2): add query HTTP service with filtering and aggregation"
```

---

### Task 15: Create Service Startup Script

**Files:**
- Create: `rag-pipeline-v2/scripts/start_services.sh`

**Step 1: Create combined startup script**

Create file `rag-pipeline-v2/scripts/start_services.sh`:
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "=== Starting RAG v2 Services ==="

# Check if Docker services are running
if ! docker compose ps | grep -q "Up"; then
    echo "Starting Docker infrastructure..."
    ./scripts/start.sh
    sleep 10
fi

# Create Python venv if needed
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Install Python dependencies
echo "Installing Python dependencies..."
.venv/bin/pip install -q -r requirements.txt

# Start embedding service in background
echo "Starting embedding service (port 5001)..."
.venv/bin/python scripts/embedding_service.py &
EMBED_PID=$!
echo "Embedding service PID: $EMBED_PID"

# Start query service in background
echo "Starting query service (port 5002)..."
.venv/bin/python scripts/query_service.py &
QUERY_PID=$!
echo "Query service PID: $QUERY_PID"

# Save PIDs for later shutdown
echo "$EMBED_PID" > /tmp/rag-v2-embed.pid
echo "$QUERY_PID" > /tmp/rag-v2-query.pid

echo ""
echo "=== RAG v2 Services Started ==="
echo "Embedding service: http://localhost:5001"
echo "Query service:     http://localhost:5002"
echo "n8n:               http://localhost:5678"
echo "RabbitMQ:          http://localhost:15672"
echo "Qdrant:            http://localhost:6333"
echo ""
echo "To stop services: ./scripts/stop_services.sh"
```

**Step 2: Create stop script**

Create file `rag-pipeline-v2/scripts/stop_services.sh`:
```bash
#!/bin/bash
set -e

echo "=== Stopping RAG v2 Services ==="

# Stop Python services
if [ -f /tmp/rag-v2-embed.pid ]; then
    kill $(cat /tmp/rag-v2-embed.pid) 2>/dev/null || true
    rm /tmp/rag-v2-embed.pid
    echo "Stopped embedding service"
fi

if [ -f /tmp/rag-v2-query.pid ]; then
    kill $(cat /tmp/rag-v2-query.pid) 2>/dev/null || true
    rm /tmp/rag-v2-query.pid
    echo "Stopped query service"
fi

# Optionally stop Docker services
read -p "Stop Docker services too? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    ./scripts/stop.sh
fi

echo "Services stopped"
```

**Step 3: Make executable**

```bash
chmod +x rag-pipeline-v2/scripts/start_services.sh
chmod +x rag-pipeline-v2/scripts/stop_services.sh
```

**Step 4: Commit**

```bash
git add rag-pipeline-v2/scripts/start_services.sh rag-pipeline-v2/scripts/stop_services.sh
git commit -m "feat(rag-v2): add unified service startup/stop scripts"
```

---

### Task 16: Test End-to-End Pipeline

**Step 1: Start all services**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2
./scripts/start_services.sh
```

**Step 2: Wait for services to initialize**

```bash
sleep 15
```

**Step 3: Test embedding service health**

```bash
curl -s http://localhost:5001/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Embedding: {d[\"status\"]}')"
```

Expected: `Embedding: healthy`

**Step 4: Test query service health**

```bash
curl -s http://localhost:5002/search -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "top_k": 1}'
```

Expected: JSON response with empty results (no data yet)

**Step 5: Test embedding a sample event**

```bash
curl -s http://localhost:5001/embed -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "type": "gameStateUpdate",
        "data": {"phase": "ACTIVE", "playerCount": 5, "priceChangePercent": 12.5},
        "receivedAt": 1703894400000
      }
    ]
  }'
```

Expected: `{"embedded": 1, "status": "success"}`

**Step 6: Verify event is searchable**

```bash
curl -s http://localhost:5002/search -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "game state active phase", "top_k": 5}'
```

Expected: Results containing the embedded event

**Step 7: Check Qdrant stats**

```bash
curl -s http://localhost:5001/stats
```

Expected: `{"collection": "rugs_events_v2", "points_count": 1, "vectors_count": 1}`

---

## Phase 4: Data Migration

### Task 17: Create ChromaDB Export Script

**Files:**
- Create: `rag-pipeline-v2/scripts/migrate_from_chroma.py`

**Step 1: Create migration script**

Create file `rag-pipeline-v2/scripts/migrate_from_chroma.py`:
```python
#!/usr/bin/env python3
"""
Migrate data from ChromaDB (v1) to Qdrant (v2).
Preserves all documents and metadata.
"""
import sys
from pathlib import Path
import json
import hashlib
from typing import Iterator

# Add v1 pipeline to path
V1_PATH = Path(__file__).parent.parent.parent / "rag-pipeline"
sys.path.insert(0, str(V1_PATH))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
import chromadb

# Configuration
CHROMA_PATH = V1_PATH / "storage" / "chroma"
V1_COLLECTION = "claude_flow_knowledge"
QDRANT_URL = "http://localhost:6333"
V2_COLLECTION = "rugs_events_v2"
BATCH_SIZE = 100


def generate_id(content: str) -> str:
    """Generate deterministic ID."""
    return hashlib.sha256(content.encode()).hexdigest()[:32]


def migrate_documents() -> None:
    """Migrate all documents from ChromaDB to Qdrant."""

    print(f"Connecting to ChromaDB at {CHROMA_PATH}")
    chroma = chromadb.PersistentClient(path=str(CHROMA_PATH))

    try:
        v1_collection = chroma.get_collection(V1_COLLECTION)
    except Exception as e:
        print(f"Cannot access v1 collection: {e}")
        return

    total = v1_collection.count()
    print(f"Found {total} documents in ChromaDB")

    print(f"Connecting to Qdrant at {QDRANT_URL}")
    qdrant = QdrantClient(url=QDRANT_URL)

    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Fetch and migrate in batches
    migrated = 0
    offset = 0

    while offset < total:
        # Get batch from ChromaDB
        results = v1_collection.get(
            limit=BATCH_SIZE,
            offset=offset,
            include=["documents", "metadatas"],
        )

        if not results["documents"]:
            break

        documents = results["documents"]
        metadatas = results["metadatas"] or [{}] * len(documents)

        # Generate embeddings
        embeddings = model.encode(documents, convert_to_numpy=True)

        # Create Qdrant points
        points = []
        for i, doc in enumerate(documents):
            meta = metadatas[i] or {}

            # Map v1 metadata to v2 format
            payload = {
                "text": doc,
                "source": meta.get("source", "migration"),
                "line_start": meta.get("line_start", 0),
                "line_end": meta.get("line_end", 0),
                "headers": meta.get("headers", ""),
                "event_type": "document",  # Mark as migrated doc
                "timestamp": 0,  # No timestamp for static docs
            }

            point = PointStruct(
                id=generate_id(doc),
                vector=embeddings[i].tolist(),
                payload=payload,
            )
            points.append(point)

        # Upsert to Qdrant
        qdrant.upsert(
            collection_name=V2_COLLECTION,
            points=points,
        )

        migrated += len(points)
        offset += BATCH_SIZE
        print(f"Migrated {migrated}/{total} documents...")

    print(f"\nMigration complete! {migrated} documents migrated to Qdrant.")

    # Verify
    v2_info = qdrant.get_collection(V2_COLLECTION)
    print(f"Qdrant collection now has {v2_info.points_count} points")


if __name__ == "__main__":
    migrate_documents()
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/scripts/migrate_from_chroma.py
git commit -m "feat(rag-v2): add ChromaDB to Qdrant migration script"
```

---

### Task 18: Run Migration

**Step 1: Ensure services are running**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2
./scripts/status.sh
```

**Step 2: Run migration**

```bash
.venv/bin/python scripts/migrate_from_chroma.py
```

Expected output:
```
Connecting to ChromaDB at /home/nomad/Desktop/claude-flow/rag-pipeline/storage/chroma
Found 1169 documents in ChromaDB
Connecting to Qdrant at http://localhost:6333
Loading embedding model...
Migrated 100/1169 documents...
Migrated 200/1169 documents...
...
Migration complete! 1169 documents migrated to Qdrant.
Qdrant collection now has 1169 points
```

**Step 3: Verify migration**

```bash
curl -s http://localhost:6333/collections/rugs_events_v2 | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'Points: {d[\"points_count\"]}')"
```

Expected: `Points: 1169`

---

### Task 19: Create Historical JSONL Ingestion Script

**Files:**
- Create: `rag-pipeline-v2/scripts/ingest_historical.py`

**Step 1: Create ingestion script**

Create file `rag-pipeline-v2/scripts/ingest_historical.py`:
```python
#!/usr/bin/env python3
"""
Ingest historical JSONL recordings into Qdrant.
Processes files from ~/rugs_recordings/ directory.
"""
import json
import hashlib
import time
from pathlib import Path
from typing import Iterator
import sys

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

# Configuration
RECORDINGS_PATH = Path.home() / "rugs_recordings"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rugs_events_v2"
BATCH_SIZE = 100
RATE_LIMIT_DELAY = 0.1  # Seconds between batches


def event_to_text(event: dict) -> str:
    """Convert event to semantic text."""
    event_type = event.get("event", event.get("type", "unknown"))
    data = event.get("data", event)

    # Simplified templates
    if "price" in str(data).lower() or "multiplier" in str(data).lower():
        return f"Price/multiplier event: {event_type}"
    elif "player" in str(data).lower():
        return f"Player activity event: {event_type}"
    elif "game" in str(data).lower():
        return f"Game state event: {event_type}"
    else:
        return f"Event: {event_type}"


def extract_metadata(event: dict, source_file: str) -> dict:
    """Extract metadata from event."""
    data = event.get("data", event)

    return {
        "event_type": event.get("event", event.get("type", "unknown")),
        "timestamp": event.get("timestamp", int(time.time() * 1000)),
        "source": f"historical:{source_file}",
        "game_id": str(data.get("gameId", data.get("game_id", ""))),
    }


def generate_id(event: dict, source: str) -> str:
    """Generate unique ID."""
    content = json.dumps(event, sort_keys=True) + source
    return hashlib.sha256(content.encode()).hexdigest()[:32]


def iter_jsonl_files() -> Iterator[Path]:
    """Iterate over JSONL files in recordings directory."""
    if not RECORDINGS_PATH.exists():
        print(f"Recordings path not found: {RECORDINGS_PATH}")
        return

    for jsonl_file in sorted(RECORDINGS_PATH.glob("**/*.jsonl")):
        yield jsonl_file


def iter_events(jsonl_file: Path) -> Iterator[dict]:
    """Iterate over events in a JSONL file."""
    with open(jsonl_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def ingest_all():
    """Ingest all historical recordings."""
    print("Initializing...")

    qdrant = QdrantClient(url=QDRANT_URL)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    files = list(iter_jsonl_files())
    print(f"Found {len(files)} JSONL files")

    total_events = 0
    total_ingested = 0

    for file_idx, jsonl_file in enumerate(files):
        print(f"\n[{file_idx+1}/{len(files)}] Processing {jsonl_file.name}...")

        batch = []
        file_events = 0

        for event in iter_events(jsonl_file):
            total_events += 1
            file_events += 1

            text = event_to_text(event)
            metadata = extract_metadata(event, jsonl_file.name)

            batch.append({
                "id": generate_id(event, jsonl_file.name),
                "text": text,
                "event": event,
                "metadata": metadata,
            })

            if len(batch) >= BATCH_SIZE:
                # Process batch
                texts = [b["text"] for b in batch]
                embeddings = model.encode(texts, convert_to_numpy=True)

                points = [
                    PointStruct(
                        id=b["id"],
                        vector=embeddings[i].tolist(),
                        payload={
                            "text": b["text"],
                            "raw_event": json.dumps(b["event"]),
                            **b["metadata"],
                        },
                    )
                    for i, b in enumerate(batch)
                ]

                qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                total_ingested += len(batch)
                batch = []

                time.sleep(RATE_LIMIT_DELAY)

        # Process remaining batch
        if batch:
            texts = [b["text"] for b in batch]
            embeddings = model.encode(texts, convert_to_numpy=True)

            points = [
                PointStruct(
                    id=b["id"],
                    vector=embeddings[i].tolist(),
                    payload={
                        "text": b["text"],
                        "raw_event": json.dumps(b["event"]),
                        **b["metadata"],
                    },
                )
                for i, b in enumerate(batch)
            ]

            qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
            total_ingested += len(batch)

        print(f"  Ingested {file_events} events from {jsonl_file.name}")

    print(f"\n=== Ingestion Complete ===")
    print(f"Total events processed: {total_events}")
    print(f"Total events ingested: {total_ingested}")

    info = qdrant.get_collection(COLLECTION_NAME)
    print(f"Qdrant collection size: {info.points_count}")


if __name__ == "__main__":
    ingest_all()
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/scripts/ingest_historical.py
git commit -m "feat(rag-v2): add historical JSONL ingestion script"
```

---

### Task 20: Run Historical Ingestion (Background)

**Step 1: Start ingestion in background**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2
nohup .venv/bin/python scripts/ingest_historical.py > ingest.log 2>&1 &
echo $! > /tmp/rag-v2-ingest.pid
```

**Step 2: Monitor progress**

```bash
tail -f ingest.log
```

**Step 3: Check completion**

When done, verify with:
```bash
curl -s http://localhost:6333/collections/rugs_events_v2 | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'Total points: {d[\"points_count\"]}')"
```

---

## Phase 5: MCP Integration

### Task 21: Create MCP Server for v2

**Files:**
- Create: `rag-pipeline-v2/mcp-server/server.py`

**Step 1: Create MCP server**

Create file `rag-pipeline-v2/mcp-server/server.py`:
```python
#!/usr/bin/env python3
"""
MCP Server for RAG Pipeline v2.
Exposes Qdrant-based search to Claude Code.
"""
import sys
from pathlib import Path
from typing import Any
import requests

from mcp.server.fastmcp import FastMCP

# Configuration
QUERY_SERVICE_URL = "http://localhost:5002"

# Initialize server
mcp = FastMCP("claude-flow-rag-v2")


@mcp.tool()
def search_events(
    query: str,
    top_k: int = 10,
    event_type: str | None = None,
    game_id: str | None = None,
    min_multiplier: float | None = None,
    max_multiplier: float | None = None,
) -> list[dict[str, Any]]:
    """Search WebSocket events using semantic similarity.

    Args:
        query: Natural language query (e.g., "games that rugged above 50x")
        top_k: Number of results (default: 10)
        event_type: Filter by event type (gameStateUpdate, playerUpdate, etc.)
        game_id: Filter by specific game ID
        min_multiplier: Minimum multiplier filter
        max_multiplier: Maximum multiplier filter

    Returns:
        List of matching events with scores and metadata
    """
    filters = {}
    if event_type:
        filters["event_type"] = event_type
    if game_id:
        filters["game_id"] = game_id
    if min_multiplier is not None:
        filters["min_multiplier"] = min_multiplier
    if max_multiplier is not None:
        filters["max_multiplier"] = max_multiplier

    try:
        resp = requests.post(
            f"{QUERY_SERVICE_URL}/search",
            json={"query": query, "top_k": top_k, "filters": filters},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def get_event_counts(
    group_by: str = "event_type",
    event_type: str | None = None,
    game_id: str | None = None,
) -> dict[str, Any]:
    """Get aggregate counts of events.

    Args:
        group_by: Field to group by (event_type, game_id, phase)
        event_type: Optional filter by event type
        game_id: Optional filter by game ID

    Returns:
        Counts grouped by the specified field
    """
    filters = {}
    if event_type:
        filters["event_type"] = event_type
    if game_id:
        filters["game_id"] = game_id

    try:
        resp = requests.post(
            f"{QUERY_SERVICE_URL}/aggregate",
            json={"group_by": group_by, "filters": filters},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_recent_events(
    limit: int = 20,
    event_type: str | None = None,
) -> list[dict[str, Any]]:
    """Get most recent events.

    Args:
        limit: Number of events to return (default: 20)
        event_type: Optional filter by event type

    Returns:
        List of recent events sorted by timestamp
    """
    try:
        params = {"limit": limit}
        if event_type:
            params["event_type"] = event_type

        resp = requests.get(
            f"{QUERY_SERVICE_URL}/recent",
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("events", [])
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def get_rag_v2_status() -> dict[str, Any]:
    """Get RAG v2 system status and statistics.

    Returns:
        System status including collection size and service health
    """
    status = {
        "version": "v2",
        "backend": "qdrant",
        "services": {},
    }

    # Check embedding service
    try:
        resp = requests.get("http://localhost:5001/health", timeout=5)
        status["services"]["embedding"] = "healthy" if resp.ok else "unhealthy"

        stats_resp = requests.get("http://localhost:5001/stats", timeout=5)
        if stats_resp.ok:
            status["collection"] = stats_resp.json()
    except Exception:
        status["services"]["embedding"] = "unavailable"

    # Check query service
    try:
        resp = requests.post(
            f"{QUERY_SERVICE_URL}/search",
            json={"query": "test", "top_k": 1},
            timeout=5,
        )
        status["services"]["query"] = "healthy" if resp.ok else "unhealthy"
    except Exception:
        status["services"]["query"] = "unavailable"

    return status


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Step 2: Create requirements**

Create file `rag-pipeline-v2/mcp-server/requirements.txt`:
```
mcp>=1.0.0
requests>=2.31.0
```

**Step 3: Commit**

```bash
mkdir -p rag-pipeline-v2/mcp-server
git add rag-pipeline-v2/mcp-server/
git commit -m "feat(rag-v2): add MCP server for Claude Code integration"
```

---

### Task 22: Create MCP Installation Script

**Files:**
- Create: `rag-pipeline-v2/mcp-server/install.sh`

**Step 1: Create installation script**

Create file `rag-pipeline-v2/mcp-server/install.sh`:
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Installing RAG v2 MCP Server ==="

# Create venv if needed
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Install dependencies
.venv/bin/pip install -q -r requirements.txt

# Get absolute path to server
SERVER_PATH="$SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/server.py"

echo ""
echo "To add to Claude Code, run:"
echo ""
echo "  claude mcp add --transport stdio claude-flow-rag-v2 -- $SERVER_PATH"
echo ""
echo "Or add to .mcp.json:"
echo ""
cat << EOF
{
  "mcpServers": {
    "claude-flow-rag-v2": {
      "command": "$SCRIPT_DIR/.venv/bin/python",
      "args": ["$SCRIPT_DIR/server.py"],
      "env": {}
    }
  }
}
EOF
```

**Step 2: Make executable**

```bash
chmod +x rag-pipeline-v2/mcp-server/install.sh
```

**Step 3: Commit**

```bash
git add rag-pipeline-v2/mcp-server/install.sh
git commit -m "feat(rag-v2): add MCP server installation script"
```

---

### Task 23: Install and Test MCP Server

**Step 1: Run installation**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2/mcp-server
./install.sh
```

**Step 2: Add to Claude Code**

```bash
claude mcp add --transport stdio claude-flow-rag-v2 -- \
  /home/nomad/Desktop/claude-flow/rag-pipeline-v2/mcp-server/.venv/bin/python \
  /home/nomad/Desktop/claude-flow/rag-pipeline-v2/mcp-server/server.py
```

**Step 3: Verify installation**

```bash
claude mcp list
```

Expected: Both `claude-flow` (v1) and `claude-flow-rag-v2` listed

**Step 4: Test MCP tools**

In Claude Code, test:
- `get_rag_v2_status` - Should show healthy services
- `search_events "game state"` - Should return results

---

### Task 24: Update rugs-expert Agent

**Files:**
- Modify: `agents/rugs-expert.md`

**Step 1: Read current agent definition**

```bash
cat /home/nomad/Desktop/claude-flow/agents/rugs-expert.md
```

**Step 2: Add v2 RAG instructions**

Add to the agent's instructions section:

```markdown
## RAG System (Dual Mode)

Two RAG backends are available:

### v1 (Current - ChromaDB)
- MCP Server: `claude-flow`
- Tool: `search_knowledge`
- Status: Production

### v2 (New - Qdrant + n8n)
- MCP Server: `claude-flow-rag-v2`
- Tools: `search_events`, `get_event_counts`, `get_recent_events`
- Status: Testing (parallel development)

**Query Strategy:**
1. For static documentation: Use v1 `search_knowledge`
2. For live/historical events: Use v2 `search_events`
3. For aggregate statistics: Use v2 `get_event_counts`
4. For recent activity: Use v2 `get_recent_events`

When v2 is validated, it will replace v1 completely.
```

**Step 3: Commit**

```bash
git add agents/rugs-expert.md
git commit -m "docs(agents): add v2 RAG instructions to rugs-expert"
```

---

## Phase 6: Validation & Cutover

### Task 25: Create Validation Test Suite

**Files:**
- Create: `rag-pipeline-v2/tests/test_validation.py`

**Step 1: Create validation tests**

Create file `rag-pipeline-v2/tests/test_validation.py`:
```python
#!/usr/bin/env python3
"""
Validation tests for RAG v2 system.
Compares performance and results against v1.
"""
import time
import sys
from pathlib import Path
import requests

# Test queries
TEST_QUERIES = [
    "gameStateUpdate event fields",
    "player betting patterns",
    "rug pull detection",
    "price multiplier above 50x",
    "game phases and transitions",
]


def test_query_latency():
    """Test that queries complete under 100ms (p95)."""
    latencies = []

    for query in TEST_QUERIES:
        start = time.time()
        resp = requests.post(
            "http://localhost:5002/search",
            json={"query": query, "top_k": 10},
        )
        elapsed = (time.time() - start) * 1000  # ms
        latencies.append(elapsed)

        assert resp.ok, f"Query failed: {query}"

    p95 = sorted(latencies)[int(len(latencies) * 0.95)]
    print(f"P95 latency: {p95:.1f}ms")
    assert p95 < 100, f"P95 latency {p95}ms exceeds 100ms target"


def test_result_quality():
    """Test that results are relevant."""
    resp = requests.post(
        "http://localhost:5002/search",
        json={"query": "gameStateUpdate event", "top_k": 5},
    )
    assert resp.ok

    results = resp.json()["results"]
    assert len(results) > 0, "No results returned"

    # Check that top result is relevant
    top_score = results[0]["score"]
    assert top_score > 0.5, f"Top result score {top_score} too low"


def test_filtering():
    """Test metadata filtering works."""
    resp = requests.post(
        "http://localhost:5002/search",
        json={
            "query": "game event",
            "top_k": 10,
            "filters": {"event_type": "gameStateUpdate"},
        },
    )
    assert resp.ok

    results = resp.json()["results"]
    for r in results:
        if r.get("event_type"):
            assert r["event_type"] == "gameStateUpdate", \
                f"Filter not applied: got {r['event_type']}"


def test_aggregation():
    """Test aggregation endpoint."""
    resp = requests.post(
        "http://localhost:5002/aggregate",
        json={"group_by": "event_type"},
    )
    assert resp.ok

    data = resp.json()
    assert "counts" in data
    assert data["total"] > 0


def test_collection_size():
    """Test that collection has expected documents."""
    resp = requests.get("http://localhost:5001/stats")
    assert resp.ok

    stats = resp.json()
    points = stats.get("points_count", 0)

    # Should have at least the migrated documents
    assert points >= 1000, f"Collection too small: {points} points"
    print(f"Collection size: {points} points")


def run_all_tests():
    """Run all validation tests."""
    tests = [
        ("Query Latency", test_query_latency),
        ("Result Quality", test_result_quality),
        ("Filtering", test_filtering),
        ("Aggregation", test_aggregation),
        ("Collection Size", test_collection_size),
    ]

    passed = 0
    failed = 0

    print("=== RAG v2 Validation Tests ===\n")

    for name, test_fn in tests:
        try:
            test_fn()
            print(f"✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: Error - {e}")
            failed += 1

    print(f"\n=== Results: {passed}/{len(tests)} passed ===")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
```

**Step 2: Commit**

```bash
mkdir -p rag-pipeline-v2/tests
git add rag-pipeline-v2/tests/test_validation.py
git commit -m "test(rag-v2): add validation test suite"
```

---

### Task 26: Run Validation Tests

**Step 1: Ensure all services are running**

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline-v2
./scripts/status.sh
```

**Step 2: Run validation**

```bash
.venv/bin/python tests/test_validation.py
```

Expected output:
```
=== RAG v2 Validation Tests ===

✓ Query Latency
✓ Result Quality
✓ Filtering
✓ Aggregation
✓ Collection Size

=== Results: 5/5 passed ===
```

**Step 3: Document results**

If all tests pass, the system is ready for extended testing.

---

### Task 27: Create Cutover Checklist

**Files:**
- Create: `rag-pipeline-v2/CUTOVER_CHECKLIST.md`

**Step 1: Create checklist**

Create file `rag-pipeline-v2/CUTOVER_CHECKLIST.md`:
```markdown
# RAG v2 Cutover Checklist

## Pre-Cutover Validation

### Performance
- [ ] P95 query latency < 100ms
- [ ] Embedding service handles 50+ events/sec
- [ ] No memory leaks after 24h run

### Data Quality
- [ ] All v1 documents migrated
- [ ] Historical JSONL files ingested
- [ ] Search results comparable to v1

### Infrastructure
- [ ] Docker services stable 24h+
- [ ] Bridge reconnects after disconnect
- [ ] Backpressure handling verified

### Integration
- [ ] MCP server tools working
- [ ] rugs-expert agent can use v2
- [ ] No regression in v1 queries

## Cutover Steps

1. **Announce Maintenance Window**
   ```
   # Notify stakeholders of cutover time
   ```

2. **Final Data Sync**
   ```bash
   # Run final migration from v1
   .venv/bin/python scripts/migrate_from_chroma.py
   ```

3. **Update MCP Configuration**
   ```bash
   # Remove v1 MCP server
   claude mcp remove claude-flow

   # Rename v2 to primary
   claude mcp remove claude-flow-rag-v2
   claude mcp add --transport stdio claude-flow -- \
     /path/to/rag-pipeline-v2/mcp-server/server.py
   ```

4. **Update Agent Definitions**
   - Remove dual-mode instructions
   - Point all queries to new system

5. **Archive v1**
   ```bash
   mv rag-pipeline rag-pipeline-v1-archive
   mv rag-pipeline-v2 rag-pipeline
   ```

6. **Verify Production**
   ```bash
   ./scripts/status.sh
   .venv/bin/python tests/test_validation.py
   ```

## Rollback Plan

If issues arise:

1. **Immediate Rollback**
   ```bash
   # Restore v1 MCP server
   claude mcp remove claude-flow
   claude mcp add --transport stdio claude-flow -- \
     python /path/to/rag-pipeline-v1-archive/mcp-server/server.py
   ```

2. **Stop v2 Services**
   ```bash
   ./scripts/stop_services.sh
   docker compose down
   ```

3. **Investigate**
   - Check logs: `docker compose logs`
   - Check validation: `tests/test_validation.py`

4. **Fix and Re-attempt**
   - Address identified issues
   - Re-run validation
   - Re-attempt cutover
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/CUTOVER_CHECKLIST.md
git commit -m "docs(rag-v2): add cutover checklist and rollback plan"
```

---

### Task 28: Final Documentation Update

**Files:**
- Update: `rag-pipeline-v2/CONTEXT.md`

**Step 1: Update CONTEXT.md with final status**

Update file `rag-pipeline-v2/CONTEXT.md`:
```markdown
# RAG Pipeline v2 - Agent Context

## Purpose
Next-generation RAG system with real-time WebSocket ingestion via n8n orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline v2                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  rugs.fun ──► Socket.IO ──► RabbitMQ ──► n8n Workflows     │
│  WebSocket     Bridge        Queue        Orchestration     │
│                                                             │
│                              │                              │
│                              ▼                              │
│                    ┌─────────────────┐                     │
│                    │ Embedding Svc   │                     │
│                    │ (MiniLM, Flask) │                     │
│                    └────────┬────────┘                     │
│                              │                              │
│                              ▼                              │
│                    ┌─────────────────┐                     │
│                    │     Qdrant      │                     │
│                    │ (Quantized,     │                     │
│                    │  384-dim)       │                     │
│                    └────────┬────────┘                     │
│                              │                              │
│              ┌───────────────┼───────────────┐             │
│              ▼               ▼               ▼             │
│        Query Svc       MCP Server      n8n Tools          │
│        (REST API)      (Claude Code)   (Webhooks)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | Port | Purpose |
|-----------|------|---------|
| RabbitMQ | 5672, 15672 | Message queue + management UI |
| Qdrant | 6333, 6334 | Vector database (REST + gRPC) |
| n8n | 5678 | Workflow orchestration |
| Embedding Service | 5001 | Generate embeddings |
| Query Service | 5002 | Semantic search API |
| Socket.IO Bridge | - | WebSocket to RabbitMQ |

## Quick Start

```bash
# Start infrastructure
./scripts/start.sh

# Start Python services
./scripts/start_services.sh

# Run validation
.venv/bin/python tests/test_validation.py

# Stop everything
./scripts/stop_services.sh
```

## Development Status

- [x] Phase 1: Infrastructure (Docker Compose)
- [x] Phase 2: Socket.IO Bridge
- [x] Phase 3: n8n Workflows
- [x] Phase 4: Data Migration
- [x] Phase 5: MCP Integration
- [x] Phase 6: Validation

## Parallel Development

This system runs alongside `rag-pipeline/` (v1 ChromaDB).
Current system remains operational until v2 proves superior.

See `CUTOVER_CHECKLIST.md` for transition plan.

## Key Improvements over v1

| Feature | v1 | v2 |
|---------|----|----|
| Real-time ingestion | No | Yes (50+ events/sec) |
| Streaming | No | RabbitMQ buffered |
| Analytics | Limited | Aggregations + filters |
| Scale | ~10k docs | 10M+ events |
| Query latency | ~200ms | <100ms (p95) |
```

**Step 2: Commit**

```bash
git add rag-pipeline-v2/CONTEXT.md
git commit -m "docs(rag-v2): update CONTEXT.md with final architecture"
```

---

## Summary

This plan creates a complete parallel RAG system:

| Phase | Deliverable |
|-------|-------------|
| 1 | Docker infrastructure (n8n, Qdrant, RabbitMQ) |
| 2 | Socket.IO to RabbitMQ bridge |
| 3 | n8n workflows + embedding/query services |
| 4 | Data migration from ChromaDB |
| 5 | MCP server for Claude Code |
| 6 | Validation suite + cutover plan |

**Zero disruption**: v1 remains fully operational throughout.

**Cutover criteria**:
- P95 latency < 100ms
- Real-time ingestion working
- All validation tests passing
- 24h stability test passed

---

Plan complete and saved to `docs/plans/2025-12-29-n8n-rag-parallel-upgrade.md`.

**Two execution options:**

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
