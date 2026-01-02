# RAG Pipeline Repair Report

**Date**: December 25, 2025
**Status**: NEEDS REPAIR
**Priority**: HIGH

---

## Executive Summary

The RAG pipeline is **functional but underperforming**. Retrieval scores are 0.24-0.37 when they should be 0.70+. The rugs-expert agent exists but is not being invoked. Immediate repairs needed before the system can reliably answer domain questions.

---

## Current State

| Component | Status | Details |
|-----------|--------|---------|
| ChromaDB | ✅ Running | `storage/chroma/chroma.sqlite3` (persisted) |
| Documents | ✅ 610 indexed | From 105 unique sources |
| Rugs Knowledge | ✅ 49 sources | Including canonical `WEBSOCKET_EVENTS_SPEC.md` (22 chunks) |
| Embeddings | ⚠️ Working but weak | `all-MiniLM-L6-v2` - general purpose model |
| Retrieval Scores | ❌ Poor | 0.24-0.37 for exact phrase matches (should be 0.70+) |
| Agent Integration | ❌ Not Used | `rugs-expert` agent defined but never invoked |

---

## Root Cause Analysis

### Issue 1: Embedding Model Not Domain-Optimized

**Current**: `all-MiniLM-L6-v2` (384 dimensions)
- Fast, general-purpose model
- Poor performance on technical/protocol documentation
- WebSocket event names, field names, and protocol terms don't embed well

**Impact**: Queries like "gameStateUpdate fields" return low similarity (0.53) to the actual spec.

**Fix**: Switch to domain-appropriate model:
```python
# Option A: Better general model
EMBEDDING_MODEL = "all-mpnet-base-v2"  # 768 dims, better quality

# Option B: Code/technical optimized
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"  # State-of-art retrieval

# Option C: Instruction-following (best for Q&A)
EMBEDDING_MODEL = "intfloat/e5-base-v2"  # Add "query: " prefix
```

### Issue 2: Headers Not Prepended to Chunk Text

**Current**: Headers stored in metadata but NOT in searchable text.

```python
# Current behavior
Chunk.text = "Content without header context..."
Chunk.headers = ["WebSocket Events Specification", "RUGGED Phase"]  # Metadata only!
```

**Impact**: Searching for "RUGGED Phase" doesn't match chunks ABOUT the RUGGED phase because the header text isn't in the embedding.

**Fix**: Prepend headers to chunk text before embedding:
```python
def chunk_markdown(...):
    # ... existing code ...

    # CHANGE: Prepend headers to chunk text
    header_prefix = " > ".join([h[1] for h in current_headers])
    chunk_text = f"[{header_prefix}]\n{'\n'.join(current_chunk_lines)}"

    yield Chunk(
        text=chunk_text,  # Now includes header context
        source=source,
        # ...
    )
```

### Issue 3: Chunk Size Too Large

**Current**: 512 tokens with 50-token overlap
- Results in ~2000-2500 char chunks
- Mixing multiple concepts per chunk
- Dilutes specificity for search

**Fix**: Reduce chunk size, increase overlap:
```python
CHUNK_SIZE = 256  # Half current size
CHUNK_OVERLAP = 64  # 25% overlap
```

### Issue 4: No Semantic Chunking

**Current**: Splits by token count, ignoring document structure.

**Impact**: Code blocks, tables, and field definitions get split mid-content.

**Fix**: Add semantic boundary detection:
```python
SEMANTIC_BOUNDARIES = [
    r'^#{1,3}\s',           # Markdown headers
    r'^```',                # Code block boundaries
    r'^\|.*\|$',            # Table rows (keep together)
    r'^---$',               # Horizontal rules
]
```

### Issue 5: No Re-ranking

**Current**: Returns raw cosine similarity scores.

**Impact**: First-pass retrieval misses nuanced matches.

**Fix**: Add cross-encoder re-ranking:
```python
from sentence_transformers import CrossEncoder

RERANKER = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def search_with_rerank(query: str, top_k: int = 5):
    # Get more candidates
    candidates = search(query, top_k=top_k * 3)

    # Re-rank with cross-encoder
    pairs = [(query, c["text"]) for c in candidates]
    scores = RERANKER.predict(pairs)

    # Sort by re-ranked score
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [c for c, s in ranked[:top_k]]
```

### Issue 6: rugs-expert Agent Not Invoked

**Current**: The `agents/rugs-expert.md` agent is defined but Claude Code doesn't automatically invoke it.

**Impact**: I read files directly instead of using RAG-powered retrieval.

**Fix**: Update agent configuration to auto-invoke:

1. Ensure `rugs-expert` is in the Task tool's available agents
2. Add trigger patterns to system prompt:
```markdown
When user asks about:
- rugs.fun protocol, WebSocket events, game mechanics
- Sidebet, rug, multiplier, leaderboard, or trading
Invoke: Task(subagent_type='rugs-expert', prompt='...')
```

---

## Repair Checklist

### Phase 1: Quick Wins (30 min)

- [ ] **1.1** Prepend headers to chunk text in `chunker.py`
- [ ] **1.2** Reduce chunk size: 512 → 256 tokens
- [ ] **1.3** Increase overlap: 50 → 64 tokens
- [ ] **1.4** Re-run ingestion: `python -m ingestion.ingest`
- [ ] **1.5** Test retrieval scores (target: 0.50+)

### Phase 2: Model Upgrade (1 hour)

- [ ] **2.1** Install better embedding model: `pip install sentence-transformers`
- [ ] **2.2** Update `config.py`: `EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"`
- [ ] **2.3** Update `embedder.py` for new model API
- [ ] **2.4** Re-run ingestion with new model
- [ ] **2.5** Test retrieval scores (target: 0.65+)

### Phase 3: Re-ranking (1 hour)

- [ ] **3.1** Add cross-encoder dependency: `pip install sentence-transformers`
- [ ] **3.2** Create `retrieval/reranker.py`
- [ ] **3.3** Integrate re-ranking into `search()` function
- [ ] **3.4** Test retrieval scores (target: 0.75+)

### Phase 4: Agent Integration (30 min)

- [ ] **4.1** Verify `rugs-expert` agent is in Task tool config
- [ ] **4.2** Add auto-invocation triggers to CLAUDE.md
- [ ] **4.3** Test: "What fields are in gameStateUpdate?" should invoke agent
- [ ] **4.4** Document agent usage in this project's CONTEXT.md

### Phase 5: Semantic Chunking (2 hours)

- [ ] **5.1** Add markdown-aware boundary detection
- [ ] **5.2** Keep code blocks intact
- [ ] **5.3** Keep tables intact
- [ ] **5.4** Add front-matter YAML parsing for metadata
- [ ] **5.5** Re-run ingestion
- [ ] **5.6** Final retrieval test (target: 0.80+)

---

## Ingestion Standards

To maintain high-quality indexing going forward:

### Pre-Ingestion Checklist

1. **Validate source files exist**: All paths in `KNOWLEDGE_PATHS` must exist
2. **Check for duplicates**: No file should be indexed twice
3. **Verify chunk quality**: Sample chunks should be coherent, not mid-sentence

### Post-Ingestion Validation

```bash
# Run after every ingestion
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate

# 1. Check document count
python3 -c "from storage.store import count; print(f'Documents: {count()}')"

# 2. Test retrieval quality (all should score > 0.60)
python3 -c "
from retrieval.retrieve import search
TEST_QUERIES = [
    ('gameStateUpdate fields', 'WEBSOCKET_EVENTS_SPEC'),
    ('RUGGED phase liquidation', 'WEBSOCKET_EVENTS_SPEC'),
    ('sidebet 5x payout', 'rugs'),
    ('price goes to zero', 'rugs'),
]
for query, expected_source in TEST_QUERIES:
    results = search(query, top_k=1)
    if results:
        score = results[0]['score']
        source = results[0]['source']
        status = '✅' if score > 0.60 and expected_source in source else '❌'
        print(f'{status} [{score:.2f}] {query[:30]}: {source}')
    else:
        print(f'❌ No results: {query}')
"
```

### Continuous Quality Metrics

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Avg retrieval score | > 0.60 | Re-tune chunking/model |
| Top-1 accuracy | > 80% | Add more training queries |
| Latency (search) | < 500ms | Reduce chunk count or optimize |
| Document count | ~600-800 | Check for missing sources |

---

## Files to Modify

| File | Changes |
|------|---------|
| `config.py` | `CHUNK_SIZE=256`, `CHUNK_OVERLAP=64`, `EMBEDDING_MODEL` |
| `ingestion/chunker.py` | Header prepending, semantic boundaries |
| `embeddings/embedder.py` | New model loading (if upgraded) |
| `retrieval/retrieve.py` | Add re-ranking step |
| `retrieval/reranker.py` | New file for cross-encoder |
| `requirements.txt` | Add `sentence-transformers>=2.2.0` |

---

## Testing Commands

```bash
cd /home/nomad/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate

# Full re-ingestion
python -m ingestion.ingest

# Quick search test
python -m retrieval.retrieve "gameStateUpdate rugged"

# Check count
python -c "from storage.store import count; print(count())"
```

---

## Priority Order

1. **Header prepending** - Biggest impact, smallest change
2. **Chunk size reduction** - Easy config change
3. **Model upgrade** - Significant improvement
4. **Re-ranking** - Final polish for production quality
5. **Semantic chunking** - Long-term maintainability

---

*Report generated: 2025-12-25*
*Author: Claude Code (Opus 4.5)*
