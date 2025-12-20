"""Discover all unique events and fields from WebSocket recordings.

This module provides 100% coverage discovery of all field paths in raw
WebSocket JSONL recordings. It extracts every unique JSON path, tracks
types, frequencies, and sample values for documentation and validation.

Example:
    >>> from ingestion.event_discovery import scan_recordings
    >>> result = scan_recordings(Path("./raw_captures"))
    >>> print(f"Found {len(result.events)} event types")
    >>> for event in result.events.values():
    ...     print(f"  {event.name}: {len(event.fields)} fields")
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator


@dataclass
class FieldInfo:
    """Information about a discovered field path.

    Tracks the JSON path, inferred type, occurrence count, and
    sample values for documentation.

    Attributes:
        path: Full JSON path (e.g., "data.leaderboard[].pnl")
        type: JSON type name (string, number, boolean, object, array, null)
        count: Number of times this field was observed
        sample_values: Up to max_samples example values
        max_samples: Maximum sample values to keep (default 5)
    """

    path: str
    type: str
    count: int = 0
    sample_values: list = field(default_factory=list)
    max_samples: int = 5

    def add_sample(self, value: Any) -> None:
        """Add a sample value if we haven't reached max.

        Truncates large string values and avoids duplicates.
        """
        if len(self.sample_values) >= self.max_samples:
            return

        # Truncate large string values
        display_value = value
        if isinstance(value, str) and len(value) > 100:
            display_value = value[:100] + "..."

        # Avoid duplicate samples
        if display_value not in self.sample_values:
            self.sample_values.append(display_value)


@dataclass
class EventInfo:
    """Information about a discovered event type.

    Aggregates all field paths discovered for a specific event type
    (e.g., "gameStateUpdate", "standard/newTrade").

    Attributes:
        name: Event type name
        count: Number of times this event was observed
        fields: Dict mapping field paths to FieldInfo
    """

    name: str
    count: int = 0
    fields: dict[str, FieldInfo] = field(default_factory=dict)


@dataclass
class DiscoveryResult:
    """Complete discovery results from scanning recordings.

    Aggregates all events, fields, and statistics from one or more
    JSONL files.

    Attributes:
        events: Dict mapping event names to EventInfo
        total_lines: Total JSONL lines processed
        files_scanned: Number of files scanned
        errors: List of parse error messages
    """

    events: dict[str, EventInfo] = field(default_factory=dict)
    total_lines: int = 0
    files_scanned: int = 0
    errors: list[str] = field(default_factory=list)


def get_type(value: Any) -> str:
    """Get JSON type name for a Python value.

    Args:
        value: Any Python value

    Returns:
        JSON type name: string, number, boolean, object, array, null
    """
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


def discover_fields(
    obj: dict,
    prefix: str = "",
    max_depth: int = 10,
    _current_depth: int = 0,
) -> dict[str, FieldInfo]:
    """Extract all field paths from a JSON object.

    Recursively traverses the object, building full JSON paths like:
    - "data.gameId"
    - "data.leaderboard[].pnl"
    - "data.provablyFair.serverSeedHash"

    Args:
        obj: Dictionary to analyze
        prefix: Current path prefix for recursion
        max_depth: Maximum recursion depth (prevents infinite loops)
        _current_depth: Internal depth counter

    Returns:
        Dictionary mapping field paths to FieldInfo objects
    """
    if _current_depth >= max_depth:
        return {}

    fields: dict[str, FieldInfo] = {}

    for key, value in obj.items():
        # Build the path
        path = f"{prefix}.{key}" if prefix else key
        value_type = get_type(value)

        # Create or update field info
        if path not in fields:
            fields[path] = FieldInfo(path=path, type=value_type)
        fields[path].count += 1

        # Add sample value for primitives
        if value_type in ("string", "number", "boolean", "null"):
            fields[path].add_sample(value)

        # Recurse into nested structures
        if isinstance(value, dict):
            # For objects with many dynamic keys (like partialPrices.values),
            # don't recurse into each key - treat as object type
            if _is_dynamic_keys_object(value):
                fields[path].add_sample(f"<object with {len(value)} keys>")
            else:
                nested = discover_fields(
                    value, path, max_depth, _current_depth + 1
                )
                fields.update(nested)

        elif isinstance(value, list) and value:
            # Mark the array itself
            array_path = f"{path}[]"
            first_elem = value[0]
            elem_type = get_type(first_elem)

            if array_path not in fields:
                fields[array_path] = FieldInfo(path=array_path, type=elem_type)
            fields[array_path].count += 1

            # If array contains primitives, sample them
            if elem_type in ("string", "number", "boolean"):
                for item in value[:3]:  # Sample first 3
                    fields[array_path].add_sample(item)

            # If array contains objects, discover their fields
            elif elem_type == "object":
                for item in value:
                    if isinstance(item, dict):
                        nested = discover_fields(
                            item, array_path, max_depth, _current_depth + 1
                        )
                        for nested_path, nested_info in nested.items():
                            if nested_path not in fields:
                                fields[nested_path] = nested_info
                            else:
                                fields[nested_path].count += nested_info.count
                                for sample in nested_info.sample_values:
                                    fields[nested_path].add_sample(sample)

    return fields


def _is_dynamic_keys_object(obj: dict) -> bool:
    """Check if object has dynamic/numeric keys (like partialPrices.values).

    These objects shouldn't have their keys recursed as field paths.
    """
    if not obj:
        return False

    keys = list(obj.keys())

    # Check if keys look like tick numbers or other dynamic values
    if all(k.isdigit() for k in keys):
        return True

    # More than 20 keys suggests dynamic data
    if len(keys) > 20:
        return True

    return False


def scan_jsonl_file(file_path: Path) -> DiscoveryResult:
    """Scan a JSONL file for events and fields.

    Processes each line, extracts the event type, and discovers
    all field paths. Handles malformed lines gracefully.

    Args:
        file_path: Path to JSONL file

    Returns:
        DiscoveryResult with all discovered events/fields
    """
    result = DiscoveryResult()
    result.files_scanned = 1

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            result.total_lines += 1

            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                result.errors.append(f"{file_path}:{line_num}: {e}")
                continue

            # Extract event name
            event_name = record.get("event", "unknown")

            # Initialize event info if new
            if event_name not in result.events:
                result.events[event_name] = EventInfo(name=event_name)

            result.events[event_name].count += 1

            # Discover all fields in this record
            fields = discover_fields(record)

            for path, info in fields.items():
                event_fields = result.events[event_name].fields
                if path not in event_fields:
                    event_fields[path] = info
                else:
                    existing = event_fields[path]
                    existing.count += info.count
                    for sample in info.sample_values:
                        existing.add_sample(sample)

    return result


def scan_recordings(
    directory: Path,
    pattern: str = "*.jsonl",
) -> DiscoveryResult:
    """Scan all JSONL files in a directory.

    Aggregates discoveries across multiple recording files.

    Args:
        directory: Directory containing JSONL recordings
        pattern: Glob pattern for files (default: *.jsonl)

    Returns:
        Aggregated DiscoveryResult from all files
    """
    combined = DiscoveryResult()

    for file_path in sorted(directory.glob(pattern)):
        file_result = scan_jsonl_file(file_path)

        combined.files_scanned += 1
        combined.total_lines += file_result.total_lines
        combined.errors.extend(file_result.errors)

        # Merge events
        for event_name, event_info in file_result.events.items():
            if event_name not in combined.events:
                combined.events[event_name] = EventInfo(name=event_name)

            combined.events[event_name].count += event_info.count

            # Merge fields
            for path, field_info in event_info.fields.items():
                combined_fields = combined.events[event_name].fields
                if path not in combined_fields:
                    combined_fields[path] = field_info
                else:
                    existing = combined_fields[path]
                    existing.count += field_info.count
                    for sample in field_info.sample_values:
                        existing.add_sample(sample)

    return combined


def get_all_field_paths(result: DiscoveryResult) -> set[str]:
    """Get all unique field paths across all events.

    Useful for comparing against documented fields.

    Args:
        result: Discovery result

    Returns:
        Set of all unique field paths
    """
    paths = set()
    for event in result.events.values():
        paths.update(event.fields.keys())
    return paths


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Discover fields from WebSocket recordings"
    )
    parser.add_argument(
        "path",
        type=Path,
        help="JSONL file or directory to scan",
    )
    parser.add_argument(
        "--pattern",
        default="*.jsonl",
        help="Glob pattern for files (default: *.jsonl)",
    )

    args = parser.parse_args()

    if args.path.is_file():
        result = scan_jsonl_file(args.path)
    elif args.path.is_dir():
        result = scan_recordings(args.path, args.pattern)
    else:
        print(f"Error: {args.path} not found")
        sys.exit(1)

    print(f"Files scanned: {result.files_scanned}")
    print(f"Total events: {result.total_lines}")
    print(f"Unique event types: {len(result.events)}")
    print(f"Parse errors: {len(result.errors)}")
    print()

    for name, event in sorted(result.events.items(), key=lambda x: -x[1].count):
        print(f"{name}: {event.count} occurrences, {len(event.fields)} fields")

    print()
    print(f"Total unique field paths: {len(get_all_field_paths(result))}")
