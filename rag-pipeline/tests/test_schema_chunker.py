"""Tests for schema chunking functions in event_chunker module."""
from pathlib import Path

import pytest

from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


class TestChunkSchemaForEmbedding:
    """Test chunking generated schemas for vector embedding."""

    def test_chunk_event_schema_basic(self):
        """Chunk a simple event schema for embedding."""
        from ingestion.event_chunker import chunk_event_schema, SchemaChunk

        schema = {
            "title": "usernameStatus",
            "type": "object",
            "x-frequency": 100,
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "examples": ["available", "taken"],
                        },
                        "username": {
                            "type": "string",
                            "examples": ["test_user"],
                        },
                    },
                },
            },
        }

        chunks = list(chunk_event_schema(schema))

        # Should create at least one chunk
        assert len(chunks) >= 1

        # Overview chunk should mention event name
        overview = chunks[0]
        assert "usernameStatus" in overview.text
        assert overview.event_type == "usernameStatus"
        assert overview.doc_type == "schema"

    def test_chunk_event_schema_includes_fields(self):
        """Schema chunks should include field information."""
        from ingestion.event_chunker import chunk_event_schema

        schema = {
            "title": "gameStateUpdate",
            "type": "object",
            "x-frequency": 5000,
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "x-frequency": 5000,
                            "examples": [1.0, 2.5],
                        },
                        "active": {
                            "type": "boolean",
                            "x-frequency": 5000,
                        },
                    },
                },
            },
        }

        chunks = list(chunk_event_schema(schema))
        all_text = " ".join(c.text for c in chunks)

        assert "price" in all_text
        assert "active" in all_text
        assert "number" in all_text
        assert "boolean" in all_text


class TestChunkFieldIndex:
    """Test chunking field index for vector embedding."""

    def test_chunk_field_index_basic(self):
        """Chunk field index entries for embedding."""
        from ingestion.event_chunker import chunk_field_index, SchemaChunk

        index = {
            "data.price": {
                "event": "gameStateUpdate",
                "type": "number",
                "frequency": 5000,
                "samples": [1.0, 2.5, 10.0],
            },
            "data.active": {
                "event": "gameStateUpdate",
                "type": "boolean",
                "frequency": 5000,
                "samples": [True, False],
            },
        }

        chunks = list(chunk_field_index(index))

        assert len(chunks) >= 1

        # Should have chunks with field information
        all_text = " ".join(c.text for c in chunks)
        assert "data.price" in all_text
        assert "data.active" in all_text

    def test_chunk_field_index_multi_event(self):
        """Handle fields appearing in multiple events."""
        from ingestion.event_chunker import chunk_field_index

        index = {
            "data.gameId": {
                "events": ["gameStateUpdate", "standard/newTrade"],
                "type": "string",
                "frequency": 6000,
                "samples": ["20251215-abc123"],
            },
        }

        chunks = list(chunk_field_index(index))
        all_text = " ".join(c.text for c in chunks)

        assert "data.gameId" in all_text
        assert "gameStateUpdate" in all_text
        assert "standard/newTrade" in all_text


class TestChunkDiscoveryResult:
    """Test chunking complete discovery results."""

    def test_chunk_discovery_result(self):
        """Chunk all events from discovery result."""
        from ingestion.event_chunker import chunk_discovery_result

        result = DiscoveryResult()
        result.events["gameStateUpdate"] = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "data.price": FieldInfo(
                    path="data.price",
                    type="number",
                    count=100,
                    sample_values=[1.0, 2.5],
                ),
            },
        )
        result.events["playerUpdate"] = EventInfo(
            name="playerUpdate",
            count=50,
            fields={
                "data.cash": FieldInfo(
                    path="data.cash",
                    type="number",
                    count=50,
                    sample_values=[10.5],
                ),
            },
        )

        chunks = list(chunk_discovery_result(result))

        # Should have chunks for both events
        event_types = {c.event_type for c in chunks}
        assert "gameStateUpdate" in event_types
        assert "playerUpdate" in event_types
