"""Generate JSON Schemas and field indexes from discovery results.

This module converts the raw field discovery data into structured
JSON Schemas and searchable field indexes for documentation and
RAG retrieval.

Example:
    >>> from ingestion.event_discovery import scan_recordings
    >>> from ingestion.schema_generator import generate_all_schemas, generate_field_index
    >>> result = scan_recordings(Path("./raw_captures"))
    >>> schemas = generate_all_schemas(result)
    >>> index = generate_field_index(result)
"""
from __future__ import annotations

import json
from typing import Any

from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


def generate_event_schema(event: EventInfo) -> dict[str, Any]:
    """Generate JSON Schema for an event type.

    Converts the flat field paths discovered into a properly nested
    JSON Schema structure with type information and examples.

    Args:
        event: EventInfo from discovery

    Returns:
        JSON Schema dict conforming to draft-07
    """
    schema: dict[str, Any] = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": event.name,
        "type": "object",
        "properties": {},
        "x-frequency": event.count,
    }

    # Group fields by their path structure
    for path, field in sorted(event.fields.items()):
        _add_field_to_schema(schema["properties"], path, field)

    return schema


def _add_field_to_schema(
    properties: dict[str, Any],
    path: str,
    field: FieldInfo,
) -> None:
    """Add a field to the schema properties at the correct nested location.

    Handles paths like:
    - "data.price" -> properties.data.properties.price
    - "data.leaderboard[]" -> properties.data.properties.leaderboard (array)
    - "data.leaderboard[].id" -> properties.data.properties.leaderboard.items.properties.id

    Args:
        properties: Current properties dict to add to
        path: Full field path
        field: FieldInfo for this field
    """
    parts = path.split(".")
    current = properties

    for i, part in enumerate(parts):
        is_last = i == len(parts) - 1
        is_array = part.endswith("[]")
        clean_part = part.rstrip("[]")

        if is_last:
            # Final field - add the actual type info
            if is_array:
                # This is an array field
                if clean_part not in current:
                    current[clean_part] = {
                        "type": "array",
                        "items": {"type": field.type, "properties": {}},
                    }
                else:
                    # Update existing array definition
                    if "items" not in current[clean_part]:
                        current[clean_part]["items"] = {
                            "type": field.type,
                            "properties": {},
                        }
            else:
                # Regular field
                field_schema: dict[str, Any] = {
                    "type": field.type,
                    "x-frequency": field.count,
                }
                if field.sample_values:
                    field_schema["examples"] = field.sample_values
                current[clean_part] = field_schema
        else:
            # Intermediate path - ensure structure exists
            if is_array:
                # This is an intermediate array (e.g., leaderboard[] in leaderboard[].id)
                if clean_part not in current:
                    current[clean_part] = {
                        "type": "array",
                        "items": {"type": "object", "properties": {}},
                    }
                current = current[clean_part]["items"]["properties"]
            else:
                # Regular nested object
                if clean_part not in current:
                    current[clean_part] = {"type": "object", "properties": {}}
                if "properties" not in current[clean_part]:
                    current[clean_part]["properties"] = {}
                current = current[clean_part]["properties"]


def generate_field_index(result: DiscoveryResult) -> dict[str, dict[str, Any]]:
    """Generate flat field index for fast lookups.

    Creates a searchable index where each unique field path maps to
    metadata about that field including which events it appears in,
    its type, frequency, and sample values.

    Args:
        result: Complete discovery result

    Returns:
        Dict mapping field paths to metadata
    """
    index: dict[str, dict[str, Any]] = {}

    for event_name, event in result.events.items():
        for path, field in event.fields.items():
            if path not in index:
                index[path] = {
                    "events": [event_name],
                    "type": field.type,
                    "frequency": field.count,
                    "samples": field.sample_values[:5],
                }
            else:
                # Field appears in multiple events
                if event_name not in index[path]["events"]:
                    index[path]["events"].append(event_name)
                index[path]["frequency"] += field.count

                # Merge sample values
                for sample in field.sample_values:
                    if (
                        sample not in index[path]["samples"]
                        and len(index[path]["samples"]) < 5
                    ):
                        index[path]["samples"].append(sample)

    # Simplify single-event fields
    for path, info in index.items():
        if len(info["events"]) == 1:
            info["event"] = info["events"][0]
            del info["events"]

    return index


def generate_all_schemas(result: DiscoveryResult) -> dict[str, dict[str, Any]]:
    """Generate JSON Schemas for all discovered event types.

    Args:
        result: Complete discovery result

    Returns:
        Dict mapping event names to their JSON Schemas
    """
    schemas = {}
    for event_name, event_info in result.events.items():
        schemas[event_name] = generate_event_schema(event_info)
    return schemas


def save_schemas(
    schemas: dict[str, dict],
    output_path: str | None = None,
) -> str:
    """Save schemas to JSON file.

    Args:
        schemas: Dict of event name -> schema
        output_path: Output file path (default: discovered_schemas.json)

    Returns:
        Path to saved file
    """
    from pathlib import Path

    if output_path is None:
        output_path = "discovered_schemas.json"

    path = Path(output_path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(schemas, f, indent=2)

    return str(path)


def save_field_index(
    index: dict[str, dict],
    output_path: str | None = None,
) -> str:
    """Save field index to JSON file.

    Args:
        index: Field index dict
        output_path: Output file path (default: discovered_fields.json)

    Returns:
        Path to saved file
    """
    from pathlib import Path

    if output_path is None:
        output_path = "discovered_fields.json"

    path = Path(output_path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return str(path)


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    from ingestion.event_discovery import scan_recordings, scan_jsonl_file

    parser = argparse.ArgumentParser(
        description="Generate schemas from WebSocket recordings"
    )
    parser.add_argument(
        "path",
        type=Path,
        help="JSONL file or directory to process",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for generated files",
    )

    args = parser.parse_args()

    # Discover fields
    if args.path.is_file():
        result = scan_jsonl_file(args.path)
    else:
        result = scan_recordings(args.path)

    # Generate schemas
    schemas = generate_all_schemas(result)
    schema_path = args.output_dir / "discovered_schemas.json"
    save_schemas(schemas, str(schema_path))
    print(f"Saved {len(schemas)} schemas to {schema_path}")

    # Generate field index
    index = generate_field_index(result)
    index_path = args.output_dir / "discovered_fields.json"
    save_field_index(index, str(index_path))
    print(f"Saved {len(index)} field paths to {index_path}")
