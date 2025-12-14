# RAG Pipeline Replication Guide

> How to create RAG-powered knowledge systems for any project

## Overview

This guide documents the pattern used in claude-flow's RAG pipeline and provides step-by-step instructions for replicating it in other projects.

**Reference Implementation:** `/home/nomad/Desktop/claude-flow/rag-pipeline/`

---

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                      RAG Pipeline                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ Ingest  │───▶│  Chunk  │───▶│  Embed  │───▶│  Store  │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│       │                                            │        │
│       │         Documents                    ChromaDB       │
│       ▼                                            │        │
│  ┌─────────────────────────────────────────────────┴───┐   │
│  │                    Retrieval                         │   │
│  │                                                      │   │
│  │   Query ──▶ Embed ──▶ Similarity Search ──▶ Results  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Component | Library | Why |
|-----------|---------|-----|
| Vector DB | ChromaDB | Local, serverless, no setup |
| Embeddings | sentence-transformers | Local, no API key, fast |
| Model | all-MiniLM-L6-v2 | 384 dims, good quality, small |
| Tokenizer | tiktoken | Accurate token counting |

**Total dependencies:** ~1GB (mostly PyTorch)

---

## Step-by-Step Replication

### Step 1: Create Directory Structure

```bash
mkdir -p your-project/rag-pipeline/{ingestion,embeddings,storage/chroma,retrieval}
```

### Step 2: Create requirements.txt

```txt
chromadb>=0.4.0
sentence-transformers>=2.2.0
tiktoken>=0.5.0
tqdm>=4.66.0
```

### Step 3: Create config.py

Customize for your project:

```python
"""RAG Pipeline Configuration."""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
RAG_ROOT = Path(__file__).parent
CHROMA_PATH = RAG_ROOT / "storage" / "chroma"

# Knowledge sources - CUSTOMIZE THIS
KNOWLEDGE_PATHS = [
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "your-data-folder",
]

# File patterns - CUSTOMIZE THIS
INCLUDE_PATTERNS = ["*.md", "*.json", "*.py"]

# Chunking settings
CHUNK_SIZE = 512  # tokens
CHUNK_OVERLAP = 50  # tokens

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

# ChromaDB collection - CUSTOMIZE THIS
COLLECTION_NAME = "your_project_knowledge"

# Retrieval defaults
DEFAULT_TOP_K = 5
```

### Step 4: Copy Core Modules

Copy these files from claude-flow reference:

```
claude-flow/rag-pipeline/
├── ingestion/
│   ├── __init__.py
│   ├── chunker.py      # Text splitting logic
│   └── ingest.py       # Main ingestion script
├── embeddings/
│   ├── __init__.py
│   └── embedder.py     # Sentence-transformers wrapper
├── storage/
│   ├── __init__.py
│   └── store.py        # ChromaDB abstraction
└── retrieval/
    ├── __init__.py
    └── retrieve.py     # Query interface
```

### Step 5: Customize Chunker (if needed)

The default chunker handles markdown and plain text. For specialized formats (JSON, logs, etc.), extend `chunker.py`:

```python
def chunk_json_events(
    data: list[dict],
    source: str,
    fields_to_embed: list[str],
) -> Iterator[Chunk]:
    """Chunk JSON event data.
    
    Args:
        data: List of event dicts
        source: Source identifier
        fields_to_embed: Which fields to include in text
    """
    for i, event in enumerate(data):
        text_parts = []
        for field in fields_to_embed:
            if field in event:
                text_parts.append(f"{field}: {event[field]}")
        
        yield Chunk(
            text="\n".join(text_parts),
            source=source,
            line_start=i,
            line_end=i,
            headers=[event.get("type", "unknown")],
        )
```

### Step 6: Setup and Run

```bash
cd your-project/rag-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Index
python -m ingestion.ingest

# Query
python -m retrieval.retrieve "your query"
```

---

## Customization Points

### 1. Different Data Formats

| Format | Chunking Strategy |
|--------|-------------------|
| Markdown | Header-aware chunking (default) |
| JSON/JSONL | Event-based chunking |
| Logs | Line-based with timestamp grouping |
| Code | Function/class-based chunking |
| CSV | Row-based with header context |

### 2. Different Embedding Models

| Model | Dimensions | Speed | Quality | Size |
|-------|------------|-------|---------|------|
| all-MiniLM-L6-v2 | 384 | Fast | Good | 80MB |
| all-mpnet-base-v2 | 768 | Medium | Better | 420MB |
| all-MiniLM-L12-v2 | 384 | Fast | Good | 120MB |

Change in `config.py`:
```python
EMBEDDING_MODEL = "all-mpnet-base-v2"
EMBEDDING_DIMENSIONS = 768
```

### 3. Metadata Filtering

Add custom metadata for filtering:

```python
# In store.py add_documents()
metadatas = [
    {
        "source": c["source"],
        "event_type": c.get("event_type"),
        "timestamp": c.get("timestamp"),
        "category": c.get("category"),
    }
    for c in chunks
]

# In retrieve.py query with filter
results = query(
    embedding,
    top_k=10,
    where={"event_type": "price_update"}
)
```

---

## Example: REPLAYER WebSocket Events

### Use Case
Document, sort, and group WebSocket events from rugs.fun gameplay for the REPLAYER project.

### Data Structure (example)
```json
{
    "type": "price_update",
    "timestamp": 1699234567890,
    "game_id": "abc123",
    "data": {
        "price": 45.5,
        "multiplier": 1.82,
        "trend": "up"
    }
}
```

### Recommended Configuration

```python
# config.py for REPLAYER
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAG_ROOT = Path(__file__).parent
CHROMA_PATH = RAG_ROOT / "storage" / "chroma"

# WebSocket event recordings
KNOWLEDGE_PATHS = [
    Path("/home/nomad/rugs_recordings"),  # JSONL recordings
    PROJECT_ROOT / "docs" / "events",      # Event documentation
]

INCLUDE_PATTERNS = ["*.jsonl", "*.json", "*.md"]

# Smaller chunks for events
CHUNK_SIZE = 256
CHUNK_OVERLAP = 0  # Events are discrete, no overlap needed

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

COLLECTION_NAME = "replayer_websocket_events"

DEFAULT_TOP_K = 10
```

### Custom Event Chunker

```python
# ingestion/event_chunker.py
import json
from dataclasses import dataclass
from typing import Iterator
from pathlib import Path


@dataclass
class EventChunk:
    """A WebSocket event chunk."""
    text: str
    source: str
    event_type: str
    game_id: str
    timestamp: int
    metadata: dict


def chunk_websocket_events(
    file_path: Path,
) -> Iterator[EventChunk]:
    """Chunk JSONL WebSocket event recordings.
    
    Args:
        file_path: Path to JSONL file
    
    Yields:
        EventChunk for each event
    """
    source = str(file_path)
    
    with open(file_path) as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            # Build searchable text representation
            event_type = event.get("type", "unknown")
            game_id = event.get("game_id", "")
            timestamp = event.get("timestamp", 0)
            data = event.get("data", {})
            
            # Format for embedding
            text_parts = [
                f"Event Type: {event_type}",
                f"Game ID: {game_id}",
            ]
            
            # Include data fields
            for key, value in data.items():
                text_parts.append(f"{key}: {value}")
            
            yield EventChunk(
                text="\n".join(text_parts),
                source=source,
                event_type=event_type,
                game_id=game_id,
                timestamp=timestamp,
                metadata={
                    "line": line_num,
                    "raw_data": data,
                }
            )


def chunk_event_documentation(
    file_path: Path,
) -> Iterator[EventChunk]:
    """Chunk markdown documentation about events."""
    # Use standard markdown chunker but tag as documentation
    from .chunker import chunk_markdown
    
    text = file_path.read_text()
    source = str(file_path)
    
    for chunk in chunk_markdown(text, source):
        yield EventChunk(
            text=chunk.text,
            source=chunk.source,
            event_type="documentation",
            game_id="",
            timestamp=0,
            metadata={
                "line_start": chunk.line_start,
                "line_end": chunk.line_end,
                "headers": chunk.headers,
            }
        )
```

### Modified Store for Events

```python
# storage/store.py additions for REPLAYER

def add_event_documents(
    chunks: list[dict],
    embeddings: list[list[float]],
) -> int:
    """Add event documents with rich metadata."""
    collection = get_collection()
    
    ids = [f"{c['source']}:{c['timestamp']}:{c['event_type']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "source": c["source"],
            "event_type": c["event_type"],
            "game_id": c["game_id"],
            "timestamp": c["timestamp"],
        }
        for c in chunks
    ]
    
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    
    return len(chunks)


def query_by_event_type(
    query_text: str,
    event_type: str,
    top_k: int = 10,
) -> list[dict]:
    """Query events filtered by type."""
    from embeddings.embedder import embed_text
    
    embedding = embed_text(query_text)
    return query(
        embedding,
        top_k=top_k,
        where={"event_type": event_type}
    )


def query_by_game(
    query_text: str,
    game_id: str,
    top_k: int = 10,
) -> list[dict]:
    """Query events for a specific game."""
    from embeddings.embedder import embed_text
    
    embedding = embed_text(query_text)
    return query(
        embedding,
        top_k=top_k,
        where={"game_id": game_id}
    )
```

### Example Queries

```python
from retrieval.retrieve import search
from storage.store import query_by_event_type, query_by_game

# General search
results = search("price spike above 100x")

# Search only price updates
results = query_by_event_type("rapid increase", "price_update")

# Search specific game
results = query_by_game("rug event", "game_abc123")

# Search documentation
results = query_by_event_type("what causes a rug", "documentation")
```

---

## Event Type Taxonomy (REPLAYER)

Based on rugs.fun gameplay, suggested event categories:

| Event Type | Description | Key Fields |
|------------|-------------|------------|
| `game_start` | New game initiated | game_id, initial_price |
| `price_update` | Price/multiplier change | price, multiplier, trend |
| `bet_placed` | User places bet | amount, position, odds |
| `bet_result` | Bet outcome | win/loss, payout |
| `rug_event` | Game ends (rug pull) | final_price, duration |
| `player_action` | Buy/sell actions | action_type, amount |
| `game_state` | Periodic state snapshot | all_positions, pot_size |

---

## Testing Your Pipeline

```bash
# 1. Index a small sample first
python -m ingestion.ingest --test  # Add a test flag

# 2. Check document count
python -c "from storage.store import count; print(f'Documents: {count()}')"

# 3. Test queries
python -m retrieval.retrieve "price update event"
python -m retrieval.retrieve "rug pull pattern"
python -m retrieval.retrieve "high multiplier"

# 4. Verify metadata filtering works
python -c "
from storage.store import query_by_event_type
results = query_by_event_type('spike', 'price_update')
print(f'Found {len(results)} price_update events')
"
```

---

## Maintenance

### Re-indexing
```bash
# Full re-index (clears existing)
python -m ingestion.ingest

# Incremental (add without clear)
python -m ingestion.ingest --no-clear
```

### Clearing Index
```bash
python -c "from storage.store import clear; clear(); print('Cleared')"
```

### Checking Health
```bash
python -c "
from storage.store import count, get_collection
c = get_collection()
print(f'Documents: {count()}')
print(f'Collection: {c.name}')
"
```

---

## File Checklist for New RAG Pipeline

```
your-project/rag-pipeline/
├── CONTEXT.md              # Agent context for this folder
├── requirements.txt        # Dependencies
├── config.py               # Project-specific configuration
├── ingestion/
│   ├── __init__.py
│   ├── chunker.py          # Default chunker
│   ├── event_chunker.py    # Custom chunker (if needed)
│   └── ingest.py           # Main ingestion script
├── embeddings/
│   ├── __init__.py
│   └── embedder.py         # Embedding wrapper
├── storage/
│   ├── __init__.py
│   ├── chroma/             # Database files (auto-created)
│   └── store.py            # Storage abstraction
└── retrieval/
    ├── __init__.py
    └── retrieve.py         # Query interface
```

---

## Reference

- **Claude-flow RAG:** `/home/nomad/Desktop/claude-flow/rag-pipeline/`
- **ChromaDB docs:** https://docs.trychroma.com/
- **Sentence-transformers:** https://www.sbert.net/
- **Embedding models:** https://huggingface.co/sentence-transformers
