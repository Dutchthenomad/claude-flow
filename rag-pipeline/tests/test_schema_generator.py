"""Tests for schema_generator module - TDD for JSON Schema generation."""
import json
from pathlib import Path

import pytest

from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


class TestGenerateEventSchema:
    """Test JSON Schema generation from discovery results."""

    def test_generate_simple_event_schema(self):
        """Generate JSON schema from simple event."""
        from ingestion.schema_generator import generate_event_schema

        event = EventInfo(
            name="usernameStatus",
            count=100,
            fields={
                "event": FieldInfo(path="event", type="string", count=100),
                "data.status": FieldInfo(
                    path="data.status",
                    type="string",
                    count=100,
                    sample_values=["available", "taken"],
                ),
                "data.username": FieldInfo(
                    path="data.username",
                    type="string",
                    count=100,
                    sample_values=["test_user"],
                ),
            },
        )

        schema = generate_event_schema(event)

        assert schema["title"] == "usernameStatus"
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "data" in schema["properties"]
        assert "status" in schema["properties"]["data"]["properties"]
        assert "username" in schema["properties"]["data"]["properties"]

    def test_schema_includes_frequency(self):
        """Schema should include occurrence frequency metadata."""
        from ingestion.schema_generator import generate_event_schema

        event = EventInfo(
            name="gameStateUpdate",
            count=5000,
            fields={
                "data.price": FieldInfo(
                    path="data.price", type="number", count=5000
                ),
            },
        )

        schema = generate_event_schema(event)

        assert schema["x-frequency"] == 5000

    def test_schema_includes_examples(self):
        """Schema should include sample values as examples."""
        from ingestion.schema_generator import generate_event_schema

        event = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "data.gameId": FieldInfo(
                    path="data.gameId",
                    type="string",
                    count=100,
                    sample_values=["20251215-abc123", "20251215-def456"],
                ),
            },
        )

        schema = generate_event_schema(event)

        # Find the gameId field in nested structure
        game_id_schema = schema["properties"]["data"]["properties"]["gameId"]
        assert "examples" in game_id_schema
        assert "20251215-abc123" in game_id_schema["examples"]

    def test_schema_handles_nested_objects(self):
        """Schema should properly nest objects like provablyFair."""
        from ingestion.schema_generator import generate_event_schema

        event = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "data.provablyFair.serverSeedHash": FieldInfo(
                    path="data.provablyFair.serverSeedHash",
                    type="string",
                    count=100,
                ),
                "data.provablyFair.version": FieldInfo(
                    path="data.provablyFair.version",
                    type="string",
                    count=100,
                ),
            },
        )

        schema = generate_event_schema(event)

        pf = schema["properties"]["data"]["properties"]["provablyFair"]
        assert pf["type"] == "object"
        assert "serverSeedHash" in pf["properties"]
        assert "version" in pf["properties"]

    def test_schema_handles_arrays(self):
        """Schema should handle array fields like leaderboard[]."""
        from ingestion.schema_generator import generate_event_schema

        event = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "data.leaderboard[]": FieldInfo(
                    path="data.leaderboard[]", type="object", count=100
                ),
                "data.leaderboard[].id": FieldInfo(
                    path="data.leaderboard[].id", type="string", count=200
                ),
                "data.leaderboard[].pnl": FieldInfo(
                    path="data.leaderboard[].pnl", type="number", count=200
                ),
            },
        )

        schema = generate_event_schema(event)

        lb = schema["properties"]["data"]["properties"]["leaderboard"]
        assert lb["type"] == "array"
        assert "items" in lb
        assert lb["items"]["type"] == "object"
        assert "id" in lb["items"]["properties"]
        assert "pnl" in lb["items"]["properties"]


class TestGenerateFieldIndex:
    """Test flat field index generation."""

    def test_generate_field_index_basic(self):
        """Generate searchable field index."""
        from ingestion.schema_generator import generate_field_index

        result = DiscoveryResult()
        result.events["gameStateUpdate"] = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "data.price": FieldInfo(
                    path="data.price",
                    type="number",
                    count=100,
                    sample_values=[1.0, 2.5, 10.0],
                ),
                "data.active": FieldInfo(
                    path="data.active",
                    type="boolean",
                    count=100,
                    sample_values=[True, False],
                ),
            },
        )

        index = generate_field_index(result)

        assert "data.price" in index
        assert index["data.price"]["event"] == "gameStateUpdate"
        assert index["data.price"]["type"] == "number"
        assert index["data.price"]["samples"] == [1.0, 2.5, 10.0]

    def test_field_index_multiple_events(self):
        """Field appearing in multiple events should list all."""
        from ingestion.schema_generator import generate_field_index

        result = DiscoveryResult()
        result.events["gameStateUpdate"] = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "event": FieldInfo(path="event", type="string", count=100),
                "data.gameId": FieldInfo(
                    path="data.gameId", type="string", count=100
                ),
            },
        )
        result.events["standard/newTrade"] = EventInfo(
            name="standard/newTrade",
            count=50,
            fields={
                "event": FieldInfo(path="event", type="string", count=50),
                "data.gameId": FieldInfo(
                    path="data.gameId", type="string", count=50
                ),
            },
        )

        index = generate_field_index(result)

        # Fields appearing in multiple events
        assert isinstance(index["event"]["events"], list)
        assert "gameStateUpdate" in index["event"]["events"]
        assert "standard/newTrade" in index["event"]["events"]

        assert isinstance(index["data.gameId"]["events"], list)
        assert len(index["data.gameId"]["events"]) == 2


class TestGenerateAllSchemas:
    """Test generating all schemas from discovery result."""

    def test_generate_all_schemas(self):
        """Generate schemas for all event types."""
        from ingestion.schema_generator import generate_all_schemas

        result = DiscoveryResult()
        result.events["gameStateUpdate"] = EventInfo(
            name="gameStateUpdate",
            count=100,
            fields={
                "data.price": FieldInfo(
                    path="data.price", type="number", count=100
                ),
            },
        )
        result.events["usernameStatus"] = EventInfo(
            name="usernameStatus",
            count=10,
            fields={
                "data.status": FieldInfo(
                    path="data.status", type="string", count=10
                ),
            },
        )

        schemas = generate_all_schemas(result)

        assert "gameStateUpdate" in schemas
        assert "usernameStatus" in schemas
        assert schemas["gameStateUpdate"]["title"] == "gameStateUpdate"
        assert schemas["usernameStatus"]["title"] == "usernameStatus"


class TestWithSampleFixture:
    """Test schema generation with sample capture fixture."""

    @pytest.fixture
    def discovery_result(self):
        """Run discovery on sample fixture."""
        from ingestion.event_discovery import scan_jsonl_file

        fixture_path = Path(__file__).parent / "fixtures" / "sample_capture.jsonl"
        if not fixture_path.exists():
            pytest.skip("Sample capture fixture not found")
        return scan_jsonl_file(fixture_path)

    def test_generate_schemas_from_fixture(self, discovery_result):
        """Generate schemas from sample fixture discovery."""
        from ingestion.schema_generator import generate_all_schemas

        schemas = generate_all_schemas(discovery_result)

        # Should have schemas for all event types
        assert "gameStateUpdate" in schemas
        assert "standard/newTrade" in schemas
        assert "playerUpdate" in schemas

        # gameStateUpdate should have complex nested structure
        gsu = schemas["gameStateUpdate"]
        assert "properties" in gsu
        assert "data" in gsu["properties"]

    def test_generate_field_index_from_fixture(self, discovery_result):
        """Generate field index from sample fixture."""
        from ingestion.schema_generator import generate_field_index

        index = generate_field_index(discovery_result)

        # Should have many field paths
        assert len(index) > 30

        # Should include key fields
        assert "data.price" in index
        assert "data.gameId" in index
        assert "data.leaderboard[].pnl" in index
