# Embeddings - Agent Context

## Purpose
Vector embedding generation using sentence-transformers. Converts text chunks to 384-dimensional vectors for semantic search.

## Contents
| File | Description |
|------|-------------|
| `embedder.py` | Sentence-transformers wrapper |
| `__init__.py` | Package exports |

## Key Functions

### `embedder.py`
- `get_embedder()` - Get or create singleton embedder
- `embed_text(text)` - Embed single text string
- `embed_batch(texts)` - Embed list of texts efficiently

## Model Details
- **Model**: `all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Speed**: ~14,000 sentences/sec on CPU
- **Size**: ~80MB download on first use

## Why This Model?
1. Runs entirely locally (no API key)
2. Fast enough for interactive queries
3. Good quality for code/documentation
4. Small memory footprint

## Usage
```python
from embeddings.embedder import embed_text, embed_batch

# Single text
vector = embed_text("How do slash commands work?")

# Batch (more efficient)
vectors = embed_batch(["text1", "text2", "text3"])
```

## For Future Agents
- Model downloads on first use (~80MB)
- Embedder is cached as singleton
- Batch embedding is 10x faster than individual calls
