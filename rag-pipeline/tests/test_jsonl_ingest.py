"""Tests for jsonl_ingest orchestrator module."""
import json
import tempfile
from pathlib import Path

import pytest


class TestIngestionPipeline:
    """Test the full ingestion pipeline."""

    def test_ingest_creates_outputs(self):
        """Full ingestion creates all expected output files."""
        from ingestion.jsonl_ingest import ingest_websocket_recordings

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test recordings
            recordings_dir = Path(tmpdir) / "recordings"
            recordings_dir.mkdir()

            with open(recordings_dir / "test.jsonl", "w") as f:
                f.write(
                    json.dumps(
                        {
                            "event": "gameStateUpdate",
                            "data": {"price": 1.0, "active": True},
                        }
                    )
                    + "\n"
                )
                f.write(
                    json.dumps(
                        {
                            "event": "playerUpdate",
                            "data": {"cash": 10.5},
                        }
                    )
                    + "\n"
                )

            output_dir = Path(tmpdir) / "output"

            result = ingest_websocket_recordings(
                recordings_dir=recordings_dir,
                output_dir=output_dir,
                embed=False,
            )

            # Check result statistics
            assert result.files_scanned == 1
            assert result.events_discovered == 2
            assert result.fields_discovered > 0

            # Check output files exist
            assert (output_dir / "discovered_schemas.json").exists()
            assert (output_dir / "discovered_fields.json").exists()
            assert (output_dir / "coverage_report.md").exists()

    def test_ingest_schema_content(self):
        """Ingestion produces valid schema content."""
        from ingestion.jsonl_ingest import ingest_websocket_recordings

        with tempfile.TemporaryDirectory() as tmpdir:
            recordings_dir = Path(tmpdir) / "recordings"
            recordings_dir.mkdir()

            with open(recordings_dir / "test.jsonl", "w") as f:
                f.write(
                    json.dumps(
                        {
                            "event": "gameStateUpdate",
                            "data": {
                                "gameId": "20251215-abc123",
                                "price": 1.234,
                            },
                        }
                    )
                    + "\n"
                )

            output_dir = Path(tmpdir) / "output"

            ingest_websocket_recordings(
                recordings_dir=recordings_dir,
                output_dir=output_dir,
                embed=False,
            )

            # Verify schema content
            schemas = json.loads(
                (output_dir / "discovered_schemas.json").read_text()
            )
            assert "gameStateUpdate" in schemas
            assert schemas["gameStateUpdate"]["title"] == "gameStateUpdate"

            # Verify field index content
            fields = json.loads(
                (output_dir / "discovered_fields.json").read_text()
            )
            assert "data.price" in fields
            assert "data.gameId" in fields

    def test_ingest_with_dictionary_diff(self):
        """Ingestion with FIELD_DICTIONARY.md comparison."""
        from ingestion.jsonl_ingest import ingest_websocket_recordings

        with tempfile.TemporaryDirectory() as tmpdir:
            recordings_dir = Path(tmpdir) / "recordings"
            recordings_dir.mkdir()

            with open(recordings_dir / "test.jsonl", "w") as f:
                f.write(
                    json.dumps(
                        {
                            "event": "gameStateUpdate",
                            "data": {"price": 1.0, "newField": "value"},
                        }
                    )
                    + "\n"
                )

            # Create mock FIELD_DICTIONARY.md
            dictionary_path = Path(tmpdir) / "FIELD_DICTIONARY.md"
            dictionary_path.write_text(
                """
# Field Dictionary

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.price` | number | - | Price field |
| `$.data.oldField` | string | - | Old field |
"""
            )

            output_dir = Path(tmpdir) / "output"

            result = ingest_websocket_recordings(
                recordings_dir=recordings_dir,
                output_dir=output_dir,
                dictionary_path=dictionary_path,
                embed=False,
            )

            # Should have diff report
            assert (output_dir / "diff_report.md").exists()

            diff_content = (output_dir / "diff_report.md").read_text()
            assert "newField" in diff_content  # New field found
            assert "oldField" in diff_content  # Stale field


class TestIngestionResult:
    """Test IngestionResult dataclass."""

    def test_result_has_expected_fields(self):
        """IngestionResult has all expected fields."""
        from ingestion.jsonl_ingest import IngestionResult

        result = IngestionResult(
            files_scanned=5,
            events_discovered=1000,
            fields_discovered=50,
            chunks_embedded=200,
            errors=[],
        )

        assert result.files_scanned == 5
        assert result.events_discovered == 1000
        assert result.fields_discovered == 50
        assert result.chunks_embedded == 200
        assert result.errors == []


class TestWithSampleFixture:
    """Test with sample capture fixture."""

    @pytest.fixture
    def sample_capture_dir(self, tmp_path):
        """Create temp dir with sample capture."""
        from shutil import copy

        fixture = Path(__file__).parent / "fixtures" / "sample_capture.jsonl"
        if not fixture.exists():
            pytest.skip("Sample capture fixture not found")

        recordings_dir = tmp_path / "recordings"
        recordings_dir.mkdir()
        copy(fixture, recordings_dir / "sample.jsonl")
        return recordings_dir

    def test_ingest_sample_fixture(self, sample_capture_dir, tmp_path):
        """Full ingestion of sample fixture."""
        from ingestion.jsonl_ingest import ingest_websocket_recordings

        output_dir = tmp_path / "output"

        result = ingest_websocket_recordings(
            recordings_dir=sample_capture_dir,
            output_dir=output_dir,
            embed=False,
        )

        # Should find all events from fixture
        assert result.events_discovered == 8  # 8 unique event types
        assert result.fields_discovered > 50  # Rich field coverage

        # Coverage report should mention all events
        report = (output_dir / "coverage_report.md").read_text()
        assert "gameStateUpdate" in report
        assert "standard/newTrade" in report
        assert "playerUpdate" in report
