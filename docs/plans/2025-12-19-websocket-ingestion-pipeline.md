# Implementation Plan: WebSocket Recording Ingestion Pipeline

## Goal

Build a comprehensive ingestion pipeline that converts raw WebSocket recordings into a vectorized knowledge base with **100% coverage guarantee** of all unique events, fields, and data patterns - creating a canonical "Rosetta Stone" for the rugs.fun protocol.

## GitHub Issue

None - create issue first with title: "feat(rag): WebSocket recording ingestion pipeline with 100% coverage guarantee"

## Architecture Impact

| Component | Change | Description |
|-----------|--------|-------------|
| `rag-pipeline/ingestion/` | Create | New `event_chunker.py`, `event_discovery.py`, `jsonl_ingest.py` |
| `rag-pipeline/storage/` | Extend | New collection for event-specific knowledge |
| `knowledge/rugs-events/generated/` | Create | Auto-generated field dictionary, event schemas |
| `rag-pipeline/config.py` | Modify | Add JSONL ingestion paths and settings |

## Data Flow Architecture

```
Raw JSONL Recordings
~/rugs_recordings/raw_captures/*.jsonl
         │
         ▼
┌─────────────────────────┐
│  1. DISCOVERY PHASE     │ ← event_discovery.py
│  - Parse all recordings │
│  - Extract unique events│
│  - Map all field paths  │
│  - Track value types    │
│  - Count frequencies    │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  2. SCHEMA GENERATION   │ ← schema_generator.py
│  - Build event schemas  │
│  - Document all fields  │
│  - Generate examples    │
│  - Create field index   │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  3. DOCUMENTATION GEN   │ ← doc_generator.py
│  - Auto-gen markdown    │
│  - Update CONTEXT.md    │
│  - Create quick refs    │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  4. VECTORIZATION       │ ← event_chunker.py
│  - Semantic chunking    │
│  - Field-aware chunks   │
│  - Embed to ChromaDB    │
└─────────────────────────┘
         │
         ▼
ChromaDB (rugs_events collection)
```

## Coverage Guarantee Strategy

### How We Ensure 100% Coverage

1. **Discovery First**: Before chunking, we scan ALL recordings and build a complete inventory
2. **Field Path Tracking**: Every unique JSON path is extracted and catalogued
3. **Schema Validation**: Auto-generated schemas are validated against ALL recordings
4. **Coverage Report**: Generate a coverage report showing:
   - Total unique events discovered
   - Total unique field paths per event
   - Sample values for each field
   - Frequency statistics
5. **Diff Detection**: When new recordings are added, detect NEW fields automatically
6. **Integrity Hash**: Each recording gets a hash; re-ingestion is idempotent

## Files to Modify/Create

| File | Change Type | Description |
|------|-------------|-------------|
| `rag-pipeline/ingestion/event_discovery.py` | Create | Scan recordings, extract all unique events/fields |
| `rag-pipeline/ingestion/schema_generator.py` | Create | Generate JSON schemas from discovered data |
| `rag-pipeline/ingestion/event_chunker.py` | Create | Semantic chunking for WebSocket events |
| `rag-pipeline/ingestion/jsonl_ingest.py` | Create | Main ingestion orchestrator |
| `rag-pipeline/config.py` | Modify | Add JSONL paths and new collection config |
| `rag-pipeline/storage/store.py` | Modify | Add support for `rugs_events` collection |
| `knowledge/rugs-events/generated/event_schemas.json` | Generate | Auto-generated schemas |
| `knowledge/rugs-events/generated/field_index.json` | Generate | Complete field dictionary |
| `knowledge/rugs-events/generated/coverage_report.md` | Generate | 100% coverage verification |
| `tests/test_event_discovery.py` | Create | TDD tests for discovery |
| `tests/test_schema_generator.py` | Create | TDD tests for schema generation |
| `tests/test_event_chunker.py` | Create | TDD tests for chunking |
| `tests/test_jsonl_ingest.py` | Create | TDD tests for orchestrator |

## Tasks (TDD Order)

### Task 1: Event Discovery - Field Path Extraction

**Test First:**
```python
# tests/test_event_discovery.py
import pytest
from ingestion.event_discovery import discover_fields, FieldInfo

def test_discover_fields_from_simple_event():
    """Extract all field paths from a simple event."""
    event = {
        "event": "gameStateUpdate",
        "data": {
            "gameId": "20251215-abc123",
            "price": 1.234,
            "active": True
        }
    }

    fields = discover_fields(event)

    assert "event" in fields
    assert "data.gameId" in fields
    assert "data.price" in fields
    assert "data.active" in fields
    assert fields["data.gameId"].type == "string"
    assert fields["data.price"].type == "number"
    assert fields["data.active"].type == "boolean"


def test_discover_fields_with_nested_arrays():
    """Handle nested arrays like leaderboard entries."""
    event = {
        "event": "gameStateUpdate",
        "data": {
            "leaderboard": [
                {"id": "player1", "pnl": 1.5},
                {"id": "player2", "pnl": -0.5}
            ]
        }
    }

    fields = discover_fields(event)

    assert "data.leaderboard[]" in fields
    assert "data.leaderboard[].id" in fields
    assert "data.leaderboard[].pnl" in fields


def test_discover_fields_with_nested_objects():
    """Handle deeply nested objects like provablyFair."""
    event = {
        "event": "gameStateUpdate",
        "data": {
            "provablyFair": {
                "serverSeedHash": "abc123",
                "version": "v3"
            }
        }
    }

    fields = discover_fields(event)

    assert "data.provablyFair.serverSeedHash" in fields
    assert "data.provablyFair.version" in fields


def test_discover_fields_tracks_sample_values():
    """Keep sample values for documentation."""
    event = {
        "event": "gameStateUpdate",
        "data": {"gameId": "20251215-abc123"}
    }

    fields = discover_fields(event)

    assert fields["data.gameId"].sample_values == ["20251215-abc123"]
```

**Implementation:**
```python
# rag-pipeline/ingestion/event_discovery.py
"""Discover all unique events and fields from WebSocket recordings."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator
import json

@dataclass
class FieldInfo:
    """Information about a discovered field."""
    path: str
    type: str  # string, number, boolean, object, array, null
    count: int = 0
    sample_values: list = field(default_factory=list)
    max_samples: int = 5

    def add_sample(self, value: Any) -> None:
        """Add a sample value if we haven't reached max."""
        if len(self.sample_values) < self.max_samples:
            # Truncate large values
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            if value not in self.sample_values:
                self.sample_values.append(value)


def get_type(value: Any) -> str:
    """Get JSON type name for a value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


def discover_fields(event: dict, prefix: str = "") -> dict[str, FieldInfo]:
    """Extract all field paths from an event.

    Args:
        event: Event dictionary to analyze
        prefix: Current path prefix for recursion

    Returns:
        Dictionary mapping field paths to FieldInfo
    """
    fields = {}

    for key, value in event.items():
        path = f"{prefix}.{key}" if prefix else key
        value_type = get_type(value)

        if path not in fields:
            fields[path] = FieldInfo(path=path, type=value_type)
        fields[path].count += 1
        fields[path].add_sample(value)

        # Recurse into nested structures
        if isinstance(value, dict):
            nested = discover_fields(value, path)
            for nested_path, nested_info in nested.items():
                if nested_path not in fields:
                    fields[nested_path] = nested_info
                else:
                    fields[nested_path].count += nested_info.count

        elif isinstance(value, list) and value:
            # Mark as array and explore first element structure
            array_path = f"{path}[]"
            if array_path not in fields:
                elem_type = get_type(value[0])
                fields[array_path] = FieldInfo(path=array_path, type=elem_type)

            # If array contains objects, discover their fields
            for item in value:
                if isinstance(item, dict):
                    nested = discover_fields(item, array_path)
                    for nested_path, nested_info in nested.items():
                        if nested_path not in fields:
                            fields[nested_path] = nested_info
                        else:
                            fields[nested_path].count += nested_info.count

    return fields
```

**Verify:**
```bash
cd ~/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m pytest tests/test_event_discovery.py::test_discover_fields_from_simple_event -v
python -m pytest tests/test_event_discovery.py -v
```

---

### Task 2: Event Discovery - JSONL Scanning

**Test First:**
```python
# tests/test_event_discovery.py (continued)

def test_scan_jsonl_file():
    """Scan a JSONL file and aggregate field discoveries."""
    from ingestion.event_discovery import scan_jsonl_file
    from pathlib import Path
    import tempfile
    import json

    # Create test JSONL
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(json.dumps({"event": "gameStateUpdate", "data": {"price": 1.0}}) + "\n")
        f.write(json.dumps({"event": "gameStateUpdate", "data": {"price": 2.0}}) + "\n")
        f.write(json.dumps({"event": "usernameStatus", "data": {"username": "test"}}) + "\n")
        test_file = Path(f.name)

    try:
        result = scan_jsonl_file(test_file)

        assert "gameStateUpdate" in result.events
        assert "usernameStatus" in result.events
        assert result.events["gameStateUpdate"].count == 2
        assert result.events["usernameStatus"].count == 1
        assert "data.price" in result.events["gameStateUpdate"].fields
        assert "data.username" in result.events["usernameStatus"].fields
    finally:
        test_file.unlink()


def test_scan_multiple_files():
    """Aggregate discoveries across multiple recordings."""
    from ingestion.event_discovery import scan_recordings
    # ... similar test with multiple files
```

**Implementation:**
```python
# rag-pipeline/ingestion/event_discovery.py (continued)

@dataclass
class EventInfo:
    """Information about a discovered event type."""
    name: str
    count: int = 0
    fields: dict[str, FieldInfo] = field(default_factory=dict)


@dataclass
class DiscoveryResult:
    """Complete discovery results from scanning."""
    events: dict[str, EventInfo] = field(default_factory=dict)
    total_lines: int = 0
    files_scanned: int = 0
    errors: list[str] = field(default_factory=list)


def scan_jsonl_file(file_path: Path) -> DiscoveryResult:
    """Scan a JSONL file for events and fields.

    Args:
        file_path: Path to JSONL file

    Returns:
        DiscoveryResult with all discovered events/fields
    """
    result = DiscoveryResult()
    result.files_scanned = 1

    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            result.total_lines += 1
            try:
                record = json.loads(line.strip())
                event_name = record.get("event", "unknown")

                if event_name not in result.events:
                    result.events[event_name] = EventInfo(name=event_name)

                result.events[event_name].count += 1

                # Discover fields in this event
                fields = discover_fields(record)
                for path, info in fields.items():
                    if path not in result.events[event_name].fields:
                        result.events[event_name].fields[path] = info
                    else:
                        existing = result.events[event_name].fields[path]
                        existing.count += info.count
                        for sample in info.sample_values:
                            existing.add_sample(sample)

            except json.JSONDecodeError as e:
                result.errors.append(f"{file_path}:{line_num}: {e}")

    return result


def scan_recordings(directory: Path, pattern: str = "*.jsonl") -> DiscoveryResult:
    """Scan all JSONL files in a directory.

    Args:
        directory: Directory containing recordings
        pattern: Glob pattern for files

    Returns:
        Aggregated DiscoveryResult
    """
    combined = DiscoveryResult()

    for file_path in sorted(directory.glob(pattern)):
        file_result = scan_jsonl_file(file_path)
        combined.files_scanned += 1
        combined.total_lines += file_result.total_lines
        combined.errors.extend(file_result.errors)

        for event_name, event_info in file_result.events.items():
            if event_name not in combined.events:
                combined.events[event_name] = EventInfo(name=event_name)

            combined.events[event_name].count += event_info.count

            for path, field_info in event_info.fields.items():
                if path not in combined.events[event_name].fields:
                    combined.events[event_name].fields[path] = field_info
                else:
                    existing = combined.events[event_name].fields[path]
                    existing.count += field_info.count
                    for sample in field_info.sample_values:
                        existing.add_sample(sample)

    return combined
```

**Verify:**
```bash
python -m pytest tests/test_event_discovery.py::test_scan_jsonl_file -v
python -m pytest tests/test_event_discovery.py -v
```

---

### Task 3: Schema Generator

**Test First:**
```python
# tests/test_schema_generator.py
import pytest
from ingestion.schema_generator import generate_event_schema, generate_field_index
from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


def test_generate_event_schema():
    """Generate JSON schema from discovery results."""
    result = DiscoveryResult()
    result.events["gameStateUpdate"] = EventInfo(
        name="gameStateUpdate",
        count=100,
        fields={
            "data.gameId": FieldInfo(path="data.gameId", type="string", count=100),
            "data.price": FieldInfo(path="data.price", type="number", count=100),
            "data.active": FieldInfo(path="data.active", type="boolean", count=100),
        }
    )

    schema = generate_event_schema(result.events["gameStateUpdate"])

    assert schema["title"] == "gameStateUpdate"
    assert "properties" in schema
    assert "data" in schema["properties"]
    assert schema["properties"]["data"]["properties"]["gameId"]["type"] == "string"


def test_generate_field_index():
    """Generate searchable field index."""
    result = DiscoveryResult()
    result.events["gameStateUpdate"] = EventInfo(
        name="gameStateUpdate",
        count=100,
        fields={
            "data.price": FieldInfo(
                path="data.price",
                type="number",
                count=100,
                sample_values=[1.0, 2.5, 10.0]
            ),
        }
    )

    index = generate_field_index(result)

    assert "data.price" in index
    assert index["data.price"]["event"] == "gameStateUpdate"
    assert index["data.price"]["type"] == "number"
    assert index["data.price"]["samples"] == [1.0, 2.5, 10.0]
```

**Implementation:**
```python
# rag-pipeline/ingestion/schema_generator.py
"""Generate JSON schemas and documentation from discovery results."""
import json
from typing import Any
from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


def generate_event_schema(event: EventInfo) -> dict:
    """Generate JSON Schema for an event type.

    Args:
        event: EventInfo from discovery

    Returns:
        JSON Schema dict
    """
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": event.name,
        "type": "object",
        "properties": {},
        "x-frequency": event.count,
    }

    # Build nested property structure from flat paths
    for path, field in sorted(event.fields.items()):
        parts = path.replace("[]", "").split(".")
        current = schema["properties"]

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {"type": "object", "properties": {}}
            if "properties" not in current[part]:
                current[part]["properties"] = {}
            current = current[part]["properties"]

        last_part = parts[-1]
        current[last_part] = {
            "type": field.type,
            "x-frequency": field.count,
        }
        if field.sample_values:
            current[last_part]["examples"] = field.sample_values

    return schema


def generate_field_index(result: DiscoveryResult) -> dict[str, dict]:
    """Generate flat field index for fast lookups.

    Args:
        result: Complete discovery result

    Returns:
        Dict mapping field paths to metadata
    """
    index = {}

    for event_name, event in result.events.items():
        for path, field in event.fields.items():
            if path not in index:
                index[path] = {
                    "event": event_name,
                    "type": field.type,
                    "frequency": field.count,
                    "samples": field.sample_values,
                }
            else:
                # Field appears in multiple events
                if isinstance(index[path]["event"], str):
                    index[path]["event"] = [index[path]["event"]]
                if event_name not in index[path]["event"]:
                    index[path]["event"].append(event_name)
                index[path]["frequency"] += field.count

    return index
```

**Verify:**
```bash
python -m pytest tests/test_schema_generator.py -v
```

---

### Task 4: Coverage Report Generator

**Test First:**
```python
# tests/test_coverage_report.py
from ingestion.coverage_report import generate_coverage_report
from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


def test_generate_coverage_report():
    """Generate markdown coverage report."""
    result = DiscoveryResult()
    result.files_scanned = 10
    result.total_lines = 5000
    result.events = {
        "gameStateUpdate": EventInfo(
            name="gameStateUpdate",
            count=4000,
            fields={"data.price": FieldInfo("data.price", "number", 4000)}
        ),
        "usernameStatus": EventInfo(
            name="usernameStatus",
            count=10,
            fields={"data.username": FieldInfo("data.username", "string", 10)}
        ),
    }

    report = generate_coverage_report(result)

    assert "## Coverage Summary" in report
    assert "10 files" in report
    assert "5,000 events" in report
    assert "2 unique event types" in report
    assert "gameStateUpdate" in report
    assert "usernameStatus" in report
```

**Implementation:**
```python
# rag-pipeline/ingestion/coverage_report.py
"""Generate coverage verification reports."""
from datetime import datetime
from ingestion.event_discovery import DiscoveryResult


def generate_coverage_report(result: DiscoveryResult) -> str:
    """Generate markdown coverage report.

    Args:
        result: Discovery results

    Returns:
        Markdown formatted report
    """
    lines = [
        "# WebSocket Recording Coverage Report",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "## Coverage Summary",
        "",
        f"- **Files Scanned**: {result.files_scanned} files",
        f"- **Total Events**: {result.total_lines:,} events",
        f"- **Unique Event Types**: {len(result.events)} unique event types",
        f"- **Parse Errors**: {len(result.errors)}",
        "",
    ]

    # Event breakdown
    lines.append("## Event Types")
    lines.append("")
    lines.append("| Event | Count | % of Total | Unique Fields |")
    lines.append("|-------|-------|------------|---------------|")

    for name, event in sorted(result.events.items(), key=lambda x: -x[1].count):
        pct = (event.count / result.total_lines * 100) if result.total_lines else 0
        lines.append(f"| `{name}` | {event.count:,} | {pct:.1f}% | {len(event.fields)} |")

    lines.append("")

    # Field details per event
    lines.append("## Field Coverage by Event")
    lines.append("")

    for name, event in sorted(result.events.items()):
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"**Occurrences**: {event.count:,}")
        lines.append("")
        lines.append("| Field Path | Type | Count | Sample Values |")
        lines.append("|------------|------|-------|---------------|")

        for path, field in sorted(event.fields.items()):
            samples = ", ".join(str(s)[:30] for s in field.sample_values[:3])
            lines.append(f"| `{path}` | {field.type} | {field.count:,} | {samples} |")

        lines.append("")

    # Errors
    if result.errors:
        lines.append("## Parse Errors")
        lines.append("")
        for error in result.errors[:20]:  # Limit to 20
            lines.append(f"- {error}")
        if len(result.errors) > 20:
            lines.append(f"- ... and {len(result.errors) - 20} more")

    return "\n".join(lines)
```

**Verify:**
```bash
python -m pytest tests/test_coverage_report.py -v
```

---

### Task 5: Event Chunker - Semantic Chunking for Events

**Test First:**
```python
# tests/test_event_chunker.py
from ingestion.event_chunker import chunk_event_schema, chunk_field_index


def test_chunk_event_schema():
    """Chunk event schema for embedding."""
    schema = {
        "title": "gameStateUpdate",
        "properties": {
            "data": {
                "properties": {
                    "price": {"type": "number", "examples": [1.0, 2.5]},
                    "active": {"type": "boolean"},
                }
            }
        }
    }

    chunks = list(chunk_event_schema(schema))

    assert len(chunks) >= 1
    assert any("gameStateUpdate" in c.text for c in chunks)
    assert any("price" in c.text for c in chunks)


def test_chunk_field_index():
    """Chunk field index entries for embedding."""
    index = {
        "data.price": {
            "event": "gameStateUpdate",
            "type": "number",
            "frequency": 1000,
            "samples": [1.0, 2.5, 10.0],
        }
    }

    chunks = list(chunk_field_index(index))

    assert len(chunks) >= 1
    assert any("data.price" in c.text for c in chunks)
```

**Implementation:**
```python
# rag-pipeline/ingestion/event_chunker.py
"""Semantic chunking for WebSocket event documentation."""
from dataclasses import dataclass
from typing import Iterator
import json


@dataclass
class EventChunk:
    """A chunk of event documentation."""
    text: str
    source: str
    event_type: str
    chunk_type: str  # "schema", "field", "example"
    field_path: str | None = None


def chunk_event_schema(schema: dict, max_chunk_size: int = 500) -> Iterator[EventChunk]:
    """Chunk event schema for embedding.

    Creates chunks that are semantically meaningful for search.
    """
    event_name = schema.get("title", "unknown")

    # Overview chunk
    overview = f"Event: {event_name}\n"
    overview += f"Frequency: {schema.get('x-frequency', 'unknown')} occurrences\n"
    overview += f"Type: WebSocket broadcast event\n\n"
    overview += "This event contains the following data structure:\n"

    yield EventChunk(
        text=overview,
        source=f"schemas/{event_name}.json",
        event_type=event_name,
        chunk_type="schema",
    )

    # Chunk each major section
    if "properties" in schema:
        _chunk_properties(schema["properties"], event_name, "", max_chunk_size)


def _chunk_properties(
    props: dict,
    event_name: str,
    prefix: str,
    max_chunk_size: int
) -> Iterator[EventChunk]:
    """Recursively chunk property definitions."""
    for name, prop in props.items():
        path = f"{prefix}.{name}" if prefix else name

        text = f"Field: {path}\n"
        text += f"Event: {event_name}\n"
        text += f"Type: {prop.get('type', 'unknown')}\n"

        if "examples" in prop:
            text += f"Examples: {prop['examples']}\n"

        if "x-frequency" in prop:
            text += f"Frequency: {prop['x-frequency']} occurrences\n"

        yield EventChunk(
            text=text,
            source=f"schemas/{event_name}.json#{path}",
            event_type=event_name,
            chunk_type="field",
            field_path=path,
        )

        # Recurse into nested properties
        if "properties" in prop:
            yield from _chunk_properties(
                prop["properties"], event_name, path, max_chunk_size
            )


def chunk_field_index(index: dict) -> Iterator[EventChunk]:
    """Chunk field index for fast field lookups."""
    for path, info in index.items():
        events = info["event"]
        if isinstance(events, str):
            events = [events]

        text = f"Field Path: {path}\n"
        text += f"Type: {info['type']}\n"
        text += f"Events: {', '.join(events)}\n"
        text += f"Frequency: {info['frequency']} occurrences\n"

        if info.get("samples"):
            text += f"Sample Values: {info['samples']}\n"

        yield EventChunk(
            text=text,
            source=f"field_index.json#{path}",
            event_type=events[0],
            chunk_type="field",
            field_path=path,
        )
```

**Verify:**
```bash
python -m pytest tests/test_event_chunker.py -v
```

---

### Task 6: Main Ingestion Orchestrator

**Test First:**
```python
# tests/test_jsonl_ingest.py
from ingestion.jsonl_ingest import ingest_websocket_recordings
from pathlib import Path
import tempfile
import json


def test_full_ingestion_pipeline():
    """End-to-end test of ingestion pipeline."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test recordings
        recordings_dir = Path(tmpdir) / "recordings"
        recordings_dir.mkdir()

        with open(recordings_dir / "test.jsonl", "w") as f:
            f.write(json.dumps({
                "event": "gameStateUpdate",
                "data": {"price": 1.0, "active": True}
            }) + "\n")

        output_dir = Path(tmpdir) / "output"

        result = ingest_websocket_recordings(
            recordings_dir=recordings_dir,
            output_dir=output_dir,
            embed=False,  # Skip embedding for test
        )

        assert result.events_discovered == 1
        assert result.fields_discovered > 0
        assert (output_dir / "event_schemas.json").exists()
        assert (output_dir / "field_index.json").exists()
        assert (output_dir / "coverage_report.md").exists()
```

**Implementation:**
```python
# rag-pipeline/ingestion/jsonl_ingest.py
"""Main orchestrator for WebSocket recording ingestion."""
from dataclasses import dataclass
from pathlib import Path
import json

from ingestion.event_discovery import scan_recordings
from ingestion.schema_generator import generate_event_schema, generate_field_index
from ingestion.coverage_report import generate_coverage_report


@dataclass
class IngestionResult:
    """Results from ingestion run."""
    files_scanned: int
    events_discovered: int
    fields_discovered: int
    chunks_embedded: int
    errors: list[str]


def ingest_websocket_recordings(
    recordings_dir: Path,
    output_dir: Path,
    embed: bool = True,
) -> IngestionResult:
    """Run full ingestion pipeline.

    Args:
        recordings_dir: Directory containing JSONL recordings
        output_dir: Directory for generated outputs
        embed: Whether to generate embeddings

    Returns:
        IngestionResult with statistics
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: Discovery
    print(f"Scanning recordings in {recordings_dir}...")
    discovery = scan_recordings(recordings_dir)

    print(f"  Found {len(discovery.events)} event types")
    print(f"  Scanned {discovery.total_lines:,} events")

    # Phase 2: Schema Generation
    print("Generating schemas...")
    schemas = {}
    total_fields = 0

    for event_name, event_info in discovery.events.items():
        schemas[event_name] = generate_event_schema(event_info)
        total_fields += len(event_info.fields)

    with open(output_dir / "event_schemas.json", "w") as f:
        json.dump(schemas, f, indent=2)

    # Phase 3: Field Index
    print("Generating field index...")
    field_index = generate_field_index(discovery)

    with open(output_dir / "field_index.json", "w") as f:
        json.dump(field_index, f, indent=2)

    # Phase 4: Coverage Report
    print("Generating coverage report...")
    report = generate_coverage_report(discovery)

    with open(output_dir / "coverage_report.md", "w") as f:
        f.write(report)

    # Phase 5: Embedding (optional)
    chunks_embedded = 0
    if embed:
        print("Generating embeddings...")
        # TODO: Implement embedding logic
        pass

    return IngestionResult(
        files_scanned=discovery.files_scanned,
        events_discovered=len(discovery.events),
        fields_discovered=total_fields,
        chunks_embedded=chunks_embedded,
        errors=discovery.errors,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest WebSocket recordings")
    parser.add_argument(
        "--recordings",
        type=Path,
        default=Path.home() / "rugs_recordings" / "raw_captures",
        help="Directory containing JSONL recordings"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent.parent / "knowledge" / "rugs-events" / "generated",
        help="Output directory for generated files"
    )
    parser.add_argument(
        "--no-embed",
        action="store_true",
        help="Skip embedding generation"
    )

    args = parser.parse_args()

    result = ingest_websocket_recordings(
        recordings_dir=args.recordings,
        output_dir=args.output,
        embed=not args.no_embed,
    )

    print(f"\nIngestion complete:")
    print(f"  Files scanned: {result.files_scanned}")
    print(f"  Events discovered: {result.events_discovered}")
    print(f"  Fields discovered: {result.fields_discovered}")
    print(f"  Chunks embedded: {result.chunks_embedded}")
    if result.errors:
        print(f"  Errors: {len(result.errors)}")
```

**Verify:**
```bash
python -m pytest tests/test_jsonl_ingest.py -v
```

---

### Task 7: Integration with Existing RAG Pipeline

**Implementation:**
Update `config.py` and `store.py` to support the new collection.

```python
# config.py additions
RUGS_EVENTS_COLLECTION = "rugs_events"
RUGS_RAW_CAPTURES_PATH = Path("/home/nomad/rugs_recordings/raw_captures")
RUGS_GENERATED_PATH = PROJECT_ROOT / "knowledge" / "rugs-events" / "generated"
```

**Verify:**
```bash
# Full integration test
cd ~/Desktop/claude-flow/rag-pipeline
python -m ingestion.jsonl_ingest --recordings ~/rugs_recordings/raw_captures --output ../knowledge/rugs-events/generated
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| Large recordings cause memory issues | Stream JSONL line-by-line, don't load entire file |
| Nested arrays create exponential paths | Cap recursion depth at 10 levels |
| Embedding generation slow | Add progress bar, support incremental updates |
| ChromaDB schema changes break index | Version the collection, add migration script |
| New events in future recordings | Diff detection alerts when new fields discovered |

## Definition of Done

- [ ] All 7 task test suites pass
- [ ] Coverage report shows 100% of recorded events documented
- [ ] `field_index.json` contains every unique field path
- [ ] ChromaDB collection populated with event chunks
- [ ] `rugs-expert` agent can answer "what is data.price?" queries
- [ ] PR created with `Closes #<issue>`
- [ ] CONTEXT.md files updated
- [ ] Code reviewed

## Usage After Implementation

```bash
# Full ingestion
cd ~/Desktop/claude-flow/rag-pipeline
source .venv/bin/activate
python -m ingestion.jsonl_ingest

# Query events
python -c "
from retrieval.retrieve import search
results = search('what is the data.price field?', collection='rugs_events')
for r in results:
    print(f'{r[\"source\"]}: {r[\"text\"][:200]}')
"
```

## Estimated Size

| Component | Lines of Code |
|-----------|---------------|
| event_discovery.py | ~150 |
| schema_generator.py | ~100 |
| coverage_report.py | ~80 |
| event_chunker.py | ~120 |
| jsonl_ingest.py | ~100 |
| Tests | ~200 |
| **Total** | **~750** |

---

*Plan created: December 19, 2025*
*Ready for user approval before implementation*
