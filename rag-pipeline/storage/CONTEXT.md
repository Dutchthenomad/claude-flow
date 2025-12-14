# Storage - Agent Context

## Purpose
Vector database storage layer. Stores document chunks and their embeddings for efficient similarity search.

## Responsibilities
- Store document metadata
- Store chunk embeddings
- Provide similarity search API
- Handle database connections

## Planned Components
| File | Description |
|------|-------------|
| `db.py` | Database connection and pooling |
| `schema.sql` | Database schema (documents, chunks) |
| `operations.py` | CRUD operations |

## Database Schema (Planned)
```sql
-- Documents table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    source_path TEXT,
    doc_type TEXT,
    created_at TIMESTAMP
);

-- Chunks table with vector
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    content TEXT,
    embedding VECTOR(1536),
    metadata JSONB
);
```

## Development Status
- [x] Initial structure
- [ ] Schema design
- [ ] PGVector setup
- [ ] Connection pooling
- [ ] Integration tests
