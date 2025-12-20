"""WebSocket event chunking for rugs.fun raw captures."""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass
class EventChunk:
    """A WebSocket event chunk with rich metadata."""
    text: str
    source: str
    event_type: str
    game_id: str
    timestamp: str
    seq: int
    doc_type: str = "raw_event"


def extract_game_id(data: dict) -> str:
    """Extract game_id from event data."""
    if not data:
        return ""

    # Direct gameId field
    if isinstance(data, dict):
        if "gameId" in data:
            return data["gameId"]
        # Nested in gameStateUpdate
        if "gameStateUpdate" in data:
            return data["gameStateUpdate"].get("gameId", "")

    # Array format [trace, payload]
    if isinstance(data, list) and len(data) > 1:
        payload = data[1]
        if isinstance(payload, dict):
            return payload.get("gameId", "")

    return ""


def format_event_for_embedding(event: dict) -> str:
    """Convert event to searchable text representation.

    Formats the event in a way that's useful for semantic search.
    """
    event_type = event.get("event", "unknown")
    timestamp = event.get("ts", "")
    seq = event.get("seq", 0)
    data = event.get("data")

    lines = [
        f"Event Type: {event_type}",
        f"Timestamp: {timestamp}",
        f"Sequence: {seq}",
    ]

    if not data:
        lines.append("Data: null")
        return "\n".join(lines)

    # Handle array format [trace, payload]
    payload = data
    if isinstance(data, list) and len(data) > 1:
        payload = data[1]

    if not isinstance(payload, dict):
        lines.append(f"Data: {str(payload)[:500]}")
        return "\n".join(lines)

    # Extract key fields based on event type
    if event_type == "gameStateUpdate":
        lines.extend(_format_game_state_update(payload))
    elif event_type == "standard/newTrade":
        lines.extend(_format_trade(payload))
    elif event_type == "newChatMessage":
        lines.extend(_format_chat(payload))
    elif event_type == "goldenHourUpdate":
        lines.extend(_format_golden_hour(payload))
    elif event_type == "goldenHourDrawing":
        lines.extend(_format_golden_hour_drawing(payload))
    elif event_type == "battleEventUpdate":
        lines.extend(_format_battle_update(payload))
    else:
        # Generic formatting for unknown events
        for key, value in list(payload.items())[:10]:
            if isinstance(value, (str, int, float, bool)):
                lines.append(f"{key}: {value}")

    return "\n".join(lines)


def _format_game_state_update(data: dict) -> list[str]:
    """Format gameStateUpdate event fields."""
    lines = []

    # Core game state
    lines.append(f"Game ID: {data.get('gameId', 'unknown')}")
    lines.append(f"Active: {data.get('active', False)}")
    lines.append(f"Rugged: {data.get('rugged', False)}")
    lines.append(f"Price: {data.get('price', 0)}")
    lines.append(f"Tick Count: {data.get('tickCount', 0)}")
    lines.append(f"Cooldown Timer: {data.get('cooldownTimer', 0)}")
    lines.append(f"Trade Count: {data.get('tradeCount', 0)}")
    lines.append(f"Connected Players: {data.get('connectedPlayers', 0)}")

    # Statistics
    lines.append(f"Average Multiplier: {data.get('averageMultiplier', 0)}")
    lines.append(f"Count 2x: {data.get('count2x', 0)}")
    lines.append(f"Count 10x: {data.get('count10x', 0)}")
    lines.append(f"Count 50x: {data.get('count50x', 0)}")
    lines.append(f"Count 100x: {data.get('count100x', 0)}")

    # Rugpool
    rugpool = data.get("rugpool", {})
    if rugpool:
        lines.append(f"Rugpool Amount: {rugpool.get('rugpoolAmount', 0)}")
        lines.append(f"Instarug Count: {rugpool.get('instarugCount', 0)}")

    # Leaderboard summary
    leaderboard = data.get("leaderboard", [])
    if leaderboard:
        lines.append(f"Leaderboard Size: {len(leaderboard)}")
        top = leaderboard[0] if leaderboard else {}
        lines.append(f"Top Player: {top.get('username', 'unknown')} (PnL: {top.get('pnl', 0)})")

    return lines


def _format_trade(data: dict) -> list[str]:
    """Format standard/newTrade event fields."""
    return [
        f"Trade Type: {data.get('type', 'unknown')}",
        f"Game ID: {data.get('gameId', 'unknown')}",
        f"Player: {data.get('username', 'unknown')} (Level {data.get('level', 0)})",
        f"Price: {data.get('price', 0)}",
        f"Amount: {data.get('amount', 0)} SOL",
        f"Quantity: {data.get('qty', 0)}",
        f"Tick Index: {data.get('tickIndex', 0)}",
        f"Coin: {data.get('coin', 'unknown')}",
    ]


def _format_chat(data: dict) -> list[str]:
    """Format newChatMessage event fields."""
    return [
        f"Player: {data.get('username', 'unknown')} (Level {data.get('level', 0)})",
        f"Message: {data.get('message', '')}",
        f"Tag: {data.get('tag', 'none')}",
        f"Verified: {data.get('verified', False)}",
        f"Role: {data.get('role', 'none')}",
    ]


def _format_golden_hour(data: dict) -> list[str]:
    """Format goldenHourUpdate event fields."""
    lines = [
        f"Status: {data.get('status', 'unknown')}",
        f"Active Event ID: {data.get('activeEventId', 'none')}",
    ]

    current = data.get("currentEvent", {})
    if current:
        lines.append(f"Event Start: {current.get('startTime', 'unknown')}")
        lines.append(f"Event End: {current.get('endTime', 'unknown')}")
        lines.append(f"Prize Amount: {current.get('prizeAmount', 0)} SOL")
        lines.append(f"Max Entries: {current.get('maxEntries', 0)}")
        lines.append(f"Level Required: {current.get('levelRequired', 0)}")

    return lines


def _format_golden_hour_drawing(data: dict) -> list[str]:
    """Format goldenHourDrawing event fields."""
    lines = [
        f"Drawing ID: {data.get('id', 'unknown')}",
        f"Game ID: {data.get('gameId', 'unknown')}",
        f"Timestamp: {data.get('timestamp', 0)}",
    ]

    entries = data.get("entries", [])
    lines.append(f"Total Entries: {len(entries)}")

    if entries:
        top = entries[0]
        lines.append(f"Top Entry: {top.get('username', 'unknown')} ({top.get('entryCount', 0)} entries, {top.get('entryPercentage', 0):.1f}%)")

    return lines


def _format_battle_update(data: dict) -> list[str]:
    """Format battleEventUpdate event fields."""
    return [
        f"Status: {data.get('status', 'unknown')}",
        f"Event ID: {data.get('activeEventId', 'none')}",
    ]


def chunk_raw_capture(
    file_path: Path,
    sample_rate: int = 1,
) -> Iterator[EventChunk]:
    """Chunk raw WebSocket capture JSONL file.

    Args:
        file_path: Path to JSONL file
        sample_rate: Only process every Nth event (1 = all, 10 = every 10th)
                     Useful for large gameStateUpdate streams

    Yields:
        EventChunk for each event
    """
    source = str(file_path)

    with open(file_path) as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue

            # Apply sample rate
            if sample_rate > 1 and line_num % sample_rate != 0:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            event_type = event.get("event", "unknown")
            timestamp = event.get("ts", "")
            seq = event.get("seq", 0)
            data = event.get("data")

            # Extract game_id
            game_id = extract_game_id(data)

            # Format for embedding
            text = format_event_for_embedding(event)

            yield EventChunk(
                text=text,
                source=source,
                event_type=event_type,
                game_id=game_id,
                timestamp=timestamp,
                seq=seq,
                doc_type="raw_event",
            )


def chunk_raw_capture_by_type(
    file_path: Path,
    event_types: list[str] | None = None,
) -> Iterator[EventChunk]:
    """Chunk raw capture, filtering by event type.

    Args:
        file_path: Path to JSONL file
        event_types: List of event types to include (None = all)

    Yields:
        EventChunk for matching events
    """
    for chunk in chunk_raw_capture(file_path):
        if event_types is None or chunk.event_type in event_types:
            yield chunk


def get_capture_summary(file_path: Path) -> dict:
    """Get summary statistics for a raw capture file.

    Returns:
        Dict with event counts, games, time range, etc.
    """
    from collections import Counter

    event_counts = Counter()
    games = set()
    timestamps = []

    with open(file_path) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                event_counts[event.get("event", "unknown")] += 1
                timestamps.append(event.get("ts", ""))

                game_id = extract_game_id(event.get("data"))
                if game_id:
                    games.add(game_id)
            except json.JSONDecodeError:
                continue

    return {
        "total_events": sum(event_counts.values()),
        "event_types": dict(event_counts),
        "unique_games": len(games),
        "games": list(games),
        "first_timestamp": timestamps[0] if timestamps else None,
        "last_timestamp": timestamps[-1] if timestamps else None,
    }


# =============================================================================
# Schema Chunking (for discovered schemas and field indexes)
# =============================================================================


@dataclass
class SchemaChunk:
    """A chunk of schema/field documentation for embedding."""

    text: str
    source: str
    event_type: str
    doc_type: str  # "schema", "field", "overview"
    field_path: str | None = None


def chunk_event_schema(schema: dict) -> Iterator[SchemaChunk]:
    """Chunk event schema for vector embedding.

    Creates semantic chunks from a generated JSON schema that are
    useful for RAG retrieval.

    Args:
        schema: JSON Schema dict from schema_generator

    Yields:
        SchemaChunk for each semantic unit
    """
    event_name = schema.get("title", "unknown")
    frequency = schema.get("x-frequency", 0)

    # Overview chunk
    overview_lines = [
        f"Event: {event_name}",
        f"Type: WebSocket broadcast event",
        f"Frequency: {frequency:,} occurrences in recordings",
        "",
        "This event is part of the rugs.fun WebSocket protocol.",
    ]

    yield SchemaChunk(
        text="\n".join(overview_lines),
        source=f"schemas/{event_name}.json",
        event_type=event_name,
        doc_type="schema",
    )

    # Field chunks from properties
    if "properties" in schema:
        yield from _chunk_schema_properties(
            schema["properties"],
            event_name,
            prefix="",
        )


def _chunk_schema_properties(
    properties: dict,
    event_name: str,
    prefix: str,
) -> Iterator[SchemaChunk]:
    """Recursively chunk schema properties.

    Args:
        properties: Properties dict from schema
        event_name: Parent event name
        prefix: Current path prefix

    Yields:
        SchemaChunk for each field
    """
    for name, prop in properties.items():
        path = f"{prefix}.{name}" if prefix else name
        prop_type = prop.get("type", "unknown")

        # Build field description
        lines = [
            f"Field: {path}",
            f"Event: {event_name}",
            f"Type: {prop_type}",
        ]

        if "x-frequency" in prop:
            lines.append(f"Frequency: {prop['x-frequency']:,} occurrences")

        if "examples" in prop:
            examples = prop["examples"][:3]
            lines.append(f"Example values: {examples}")

        yield SchemaChunk(
            text="\n".join(lines),
            source=f"schemas/{event_name}.json#{path}",
            event_type=event_name,
            doc_type="field",
            field_path=path,
        )

        # Recurse into nested objects
        if prop_type == "object" and "properties" in prop:
            yield from _chunk_schema_properties(
                prop["properties"],
                event_name,
                path,
            )

        # Recurse into array items
        if prop_type == "array" and "items" in prop:
            items = prop["items"]
            if items.get("type") == "object" and "properties" in items:
                yield from _chunk_schema_properties(
                    items["properties"],
                    event_name,
                    f"{path}[]",
                )


def chunk_field_index(index: dict) -> Iterator[SchemaChunk]:
    """Chunk field index for vector embedding.

    Creates chunks from the flat field index that enable
    semantic search for field information.

    Args:
        index: Field index dict from schema_generator

    Yields:
        SchemaChunk for each field entry
    """
    for path, info in sorted(index.items()):
        # Get event(s) this field appears in
        events = info.get("events", [info.get("event", "unknown")])
        if isinstance(events, str):
            events = [events]

        lines = [
            f"Field Path: {path}",
            f"Type: {info.get('type', 'unknown')}",
            f"Events: {', '.join(events)}",
            f"Frequency: {info.get('frequency', 0):,} occurrences",
        ]

        samples = info.get("samples", [])
        if samples:
            lines.append(f"Sample values: {samples[:3]}")

        yield SchemaChunk(
            text="\n".join(lines),
            source=f"field_index.json#{path}",
            event_type=events[0],
            doc_type="field",
            field_path=path,
        )


def chunk_discovery_result(result) -> Iterator[SchemaChunk]:
    """Chunk all events from a discovery result.

    Convenience function that generates schemas and chunks them.

    Args:
        result: DiscoveryResult from event_discovery

    Yields:
        SchemaChunk for each event and field
    """
    from ingestion.schema_generator import generate_all_schemas

    schemas = generate_all_schemas(result)

    for event_name, schema in schemas.items():
        yield from chunk_event_schema(schema)


if __name__ == "__main__":
    # Test with sample capture
    import sys

    if len(sys.argv) > 1:
        capture_path = Path(sys.argv[1])
    else:
        capture_path = Path("/home/nomad/rugs_recordings/raw_captures/2025-12-14_11-51-33_raw.jsonl")

    if not capture_path.exists():
        print(f"File not found: {capture_path}")
        sys.exit(1)

    print(f"Analyzing: {capture_path}")
    print()

    # Get summary
    summary = get_capture_summary(capture_path)
    print(f"Total events: {summary['total_events']}")
    print(f"Unique games: {summary['unique_games']}")
    print(f"Time range: {summary['first_timestamp']} to {summary['last_timestamp']}")
    print()
    print("Event types:")
    for event_type, count in sorted(summary['event_types'].items(), key=lambda x: -x[1]):
        print(f"  {event_type}: {count}")
    print()

    # Show sample chunks
    print("Sample chunks (first 3):")
    for i, chunk in enumerate(chunk_raw_capture(capture_path)):
        if i >= 3:
            break
        print(f"\n--- Chunk {i+1} ---")
        print(f"Event: {chunk.event_type}")
        print(f"Game: {chunk.game_id}")
        print(f"Text preview: {chunk.text[:200]}...")
