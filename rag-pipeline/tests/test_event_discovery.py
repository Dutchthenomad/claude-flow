"""Tests for event_discovery module - TDD for WebSocket field path extraction."""
import json
import tempfile
from pathlib import Path

import pytest


class TestDiscoverFields:
    """Test field path extraction from nested JSON events."""

    def test_discover_fields_from_simple_event(self):
        """Extract all field paths from a simple flat event."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "gameStateUpdate",
            "data": {
                "gameId": "20251215-abc123",
                "price": 1.234,
                "active": True,
            },
        }

        fields = discover_fields(event)

        assert "event" in fields
        assert "data.gameId" in fields
        assert "data.price" in fields
        assert "data.active" in fields
        assert fields["data.gameId"].type == "string"
        assert fields["data.price"].type == "number"
        assert fields["data.active"].type == "boolean"

    def test_discover_fields_with_nested_arrays(self):
        """Handle nested arrays like leaderboard entries."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "gameStateUpdate",
            "data": {
                "leaderboard": [
                    {"id": "player1", "pnl": 1.5, "level": 42},
                    {"id": "player2", "pnl": -0.5, "level": 15},
                ]
            },
        }

        fields = discover_fields(event)

        assert "data.leaderboard[]" in fields
        assert "data.leaderboard[].id" in fields
        assert "data.leaderboard[].pnl" in fields
        assert "data.leaderboard[].level" in fields
        assert fields["data.leaderboard[].id"].type == "string"
        assert fields["data.leaderboard[].pnl"].type == "number"

    def test_discover_fields_with_nested_objects(self):
        """Handle deeply nested objects like provablyFair."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "gameStateUpdate",
            "data": {
                "provablyFair": {
                    "serverSeedHash": "abc123",
                    "version": "v3",
                },
                "rugpool": {
                    "rugpoolAmount": 5.5,
                    "instarugCount": 2,
                },
            },
        }

        fields = discover_fields(event)

        assert "data.provablyFair.serverSeedHash" in fields
        assert "data.provablyFair.version" in fields
        assert "data.rugpool.rugpoolAmount" in fields
        assert "data.rugpool.instarugCount" in fields

    def test_discover_fields_tracks_sample_values(self):
        """Keep sample values for documentation."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "gameStateUpdate",
            "data": {"gameId": "20251215-abc123"},
        }

        fields = discover_fields(event)

        assert "20251215-abc123" in fields["data.gameId"].sample_values

    def test_discover_fields_handles_null_values(self):
        """Handle null/None values correctly."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "battleEventUpdate",
            "data": {"activeEventId": None, "status": "waiting"},
        }

        fields = discover_fields(event)

        assert "data.activeEventId" in fields
        assert fields["data.activeEventId"].type == "null"
        assert fields["data.status"].type == "string"

    def test_discover_fields_with_partialPrices_dict(self):
        """Handle objects with dynamic string keys like partialPrices.values."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "gameStateUpdate",
            "data": {
                "partialPrices": {
                    "startTick": 40,
                    "endTick": 45,
                    "values": {"40": 1.1, "41": 1.15, "42": 1.2},
                }
            },
        }

        fields = discover_fields(event)

        assert "data.partialPrices.startTick" in fields
        assert "data.partialPrices.endTick" in fields
        assert "data.partialPrices.values" in fields
        # Dynamic keys should be tracked as object type
        assert fields["data.partialPrices.values"].type == "object"

    def test_discover_fields_with_gameHistory_array(self):
        """Handle complex nested arrays like gameHistory."""
        from ingestion.event_discovery import discover_fields

        event = {
            "event": "gameStateUpdate",
            "data": {
                "gameHistory": [
                    {
                        "id": "20251215-abc123",
                        "timestamp": 1734234310000,
                        "rugged": True,
                        "peakMultiplier": 1.256,
                        "prices": [1.0, 1.05, 1.1],
                        "provablyFair": {"serverSeedHash": "abc123"},
                    }
                ]
            },
        }

        fields = discover_fields(event)

        assert "data.gameHistory[]" in fields
        assert "data.gameHistory[].id" in fields
        assert "data.gameHistory[].timestamp" in fields
        assert "data.gameHistory[].peakMultiplier" in fields
        assert "data.gameHistory[].prices[]" in fields
        assert "data.gameHistory[].provablyFair.serverSeedHash" in fields


class TestScanJsonlFile:
    """Test JSONL file scanning and aggregation."""

    def test_scan_jsonl_file_basic(self):
        """Scan a JSONL file and aggregate field discoveries."""
        from ingestion.event_discovery import scan_jsonl_file

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as f:
            f.write(
                json.dumps(
                    {"event": "gameStateUpdate", "data": {"price": 1.0}}
                )
                + "\n"
            )
            f.write(
                json.dumps(
                    {"event": "gameStateUpdate", "data": {"price": 2.0}}
                )
                + "\n"
            )
            f.write(
                json.dumps(
                    {"event": "usernameStatus", "data": {"username": "test"}}
                )
                + "\n"
            )
            test_file = Path(f.name)

        try:
            result = scan_jsonl_file(test_file)

            assert "gameStateUpdate" in result.events
            assert "usernameStatus" in result.events
            assert result.events["gameStateUpdate"].count == 2
            assert result.events["usernameStatus"].count == 1
            assert "data.price" in result.events["gameStateUpdate"].fields
            assert "data.username" in result.events["usernameStatus"].fields
            assert result.total_lines == 3
            assert result.files_scanned == 1
        finally:
            test_file.unlink()

    def test_scan_jsonl_handles_malformed_lines(self):
        """Handle malformed JSON lines gracefully."""
        from ingestion.event_discovery import scan_jsonl_file

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as f:
            f.write(
                json.dumps({"event": "gameStateUpdate", "data": {"price": 1.0}})
                + "\n"
            )
            f.write("this is not valid json\n")
            f.write(
                json.dumps({"event": "gameStateUpdate", "data": {"price": 2.0}})
                + "\n"
            )
            test_file = Path(f.name)

        try:
            result = scan_jsonl_file(test_file)

            assert result.events["gameStateUpdate"].count == 2
            assert len(result.errors) == 1
            assert "not valid json" in result.errors[0] or "line" in result.errors[0].lower()
        finally:
            test_file.unlink()

    def test_scan_aggregates_sample_values(self):
        """Aggregate sample values across events."""
        from ingestion.event_discovery import scan_jsonl_file

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as f:
            for i in range(10):
                f.write(
                    json.dumps(
                        {"event": "gameStateUpdate", "data": {"price": float(i)}}
                    )
                    + "\n"
                )
            test_file = Path(f.name)

        try:
            result = scan_jsonl_file(test_file)

            price_field = result.events["gameStateUpdate"].fields["data.price"]
            # Should have max 5 samples (capped)
            assert len(price_field.sample_values) <= 5
            assert price_field.count == 10
        finally:
            test_file.unlink()


class TestScanRecordings:
    """Test scanning multiple JSONL files."""

    def test_scan_multiple_files(self):
        """Aggregate discoveries across multiple recordings."""
        from ingestion.event_discovery import scan_recordings

        with tempfile.TemporaryDirectory() as tmpdir:
            recordings_dir = Path(tmpdir)

            # File 1
            with open(recordings_dir / "capture1.jsonl", "w") as f:
                f.write(
                    json.dumps(
                        {"event": "gameStateUpdate", "data": {"price": 1.0}}
                    )
                    + "\n"
                )
                f.write(
                    json.dumps(
                        {"event": "gameStateUpdate", "data": {"price": 2.0}}
                    )
                    + "\n"
                )

            # File 2
            with open(recordings_dir / "capture2.jsonl", "w") as f:
                f.write(
                    json.dumps(
                        {"event": "gameStateUpdate", "data": {"price": 3.0}}
                    )
                    + "\n"
                )
                f.write(
                    json.dumps(
                        {"event": "standard/newTrade", "data": {"amount": 0.5}}
                    )
                    + "\n"
                )

            result = scan_recordings(recordings_dir)

            assert result.files_scanned == 2
            assert result.total_lines == 4
            assert "gameStateUpdate" in result.events
            assert "standard/newTrade" in result.events
            assert result.events["gameStateUpdate"].count == 3
            assert result.events["standard/newTrade"].count == 1


class TestWithSampleFixture:
    """Test with the sample_capture.jsonl fixture."""

    @pytest.fixture
    def sample_capture_path(self):
        """Path to sample capture fixture."""
        return Path(__file__).parent / "fixtures" / "sample_capture.jsonl"

    def test_scan_sample_capture(self, sample_capture_path):
        """Scan the sample capture fixture."""
        from ingestion.event_discovery import scan_jsonl_file

        if not sample_capture_path.exists():
            pytest.skip("Sample capture fixture not found")

        result = scan_jsonl_file(sample_capture_path)

        # Should find all event types from fixture
        expected_events = {
            "gameStateUpdate",
            "standard/newTrade",
            "newChatMessage",
            "usernameStatus",
            "playerUpdate",
            "goldenHourUpdate",
            "sidebetResponse",
            "battleEventUpdate",
        }
        assert set(result.events.keys()) == expected_events

        # gameStateUpdate should have complex nested fields
        gsu_fields = result.events["gameStateUpdate"].fields
        assert "data.leaderboard[].pnl" in gsu_fields
        assert "data.rugpool.rugpoolAmount" in gsu_fields
        assert "data.provablyFair.serverSeedHash" in gsu_fields

    def test_field_count_in_sample(self, sample_capture_path):
        """Verify we discover all unique fields."""
        from ingestion.event_discovery import scan_jsonl_file

        if not sample_capture_path.exists():
            pytest.skip("Sample capture fixture not found")

        result = scan_jsonl_file(sample_capture_path)

        # Count total unique field paths discovered
        total_fields = sum(
            len(event.fields) for event in result.events.values()
        )

        # Should discover many fields from the rich fixture
        assert total_fields > 50, f"Expected 50+ fields, got {total_fields}"
