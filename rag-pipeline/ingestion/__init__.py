"""Ingestion module for RAG pipeline."""
from .chunker import chunk_text, chunk_markdown
from .ingest import ingest_all, ingest_file, clear_index

# WebSocket recording ingestion pipeline
from .event_discovery import (
    discover_fields,
    scan_jsonl_file,
    scan_recordings,
    DiscoveryResult,
    EventInfo,
    FieldInfo,
)
from .schema_generator import (
    generate_event_schema,
    generate_all_schemas,
    generate_field_index,
)
from .coverage_report import (
    generate_coverage_report,
    generate_diff_report,
    parse_field_dictionary,
)
from .event_chunker import (
    EventChunk,
    SchemaChunk,
    chunk_raw_capture,
    chunk_event_schema,
    chunk_field_index,
    chunk_discovery_result,
)
from .jsonl_ingest import (
    ingest_websocket_recordings,
    IngestionResult,
)

__all__ = [
    # Core ingestion
    "chunk_text",
    "chunk_markdown",
    "ingest_all",
    "ingest_file",
    "clear_index",
    # WebSocket discovery
    "discover_fields",
    "scan_jsonl_file",
    "scan_recordings",
    "DiscoveryResult",
    "EventInfo",
    "FieldInfo",
    # Schema generation
    "generate_event_schema",
    "generate_all_schemas",
    "generate_field_index",
    # Coverage reporting
    "generate_coverage_report",
    "generate_diff_report",
    "parse_field_dictionary",
    # Event chunking
    "EventChunk",
    "SchemaChunk",
    "chunk_raw_capture",
    "chunk_event_schema",
    "chunk_field_index",
    "chunk_discovery_result",
    # Orchestrator
    "ingest_websocket_recordings",
    "IngestionResult",
]
