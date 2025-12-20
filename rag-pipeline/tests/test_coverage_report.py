"""Tests for coverage_report module - TDD for coverage verification."""
from pathlib import Path

import pytest

from ingestion.event_discovery import DiscoveryResult, EventInfo, FieldInfo


class TestGenerateCoverageReport:
    """Test coverage report generation."""

    def test_generate_basic_report(self):
        """Generate markdown coverage report."""
        from ingestion.coverage_report import generate_coverage_report

        result = DiscoveryResult()
        result.files_scanned = 10
        result.total_lines = 5000
        result.events = {
            "gameStateUpdate": EventInfo(
                name="gameStateUpdate",
                count=4000,
                fields={
                    "data.price": FieldInfo("data.price", "number", 4000),
                    "data.active": FieldInfo("data.active", "boolean", 4000),
                },
            ),
            "usernameStatus": EventInfo(
                name="usernameStatus",
                count=10,
                fields={
                    "data.username": FieldInfo("data.username", "string", 10)
                },
            ),
        }

        report = generate_coverage_report(result)

        assert "## Coverage Summary" in report
        assert "10 files" in report
        assert "5,000" in report  # total events formatted
        assert "2 unique event types" in report
        assert "gameStateUpdate" in report
        assert "usernameStatus" in report

    def test_report_includes_event_table(self):
        """Report should include event breakdown table."""
        from ingestion.coverage_report import generate_coverage_report

        result = DiscoveryResult()
        result.total_lines = 100
        result.events = {
            "gameStateUpdate": EventInfo(
                name="gameStateUpdate",
                count=90,
                fields={"data.price": FieldInfo("data.price", "number", 90)},
            ),
            "playerUpdate": EventInfo(
                name="playerUpdate",
                count=10,
                fields={"data.cash": FieldInfo("data.cash", "number", 10)},
            ),
        }

        report = generate_coverage_report(result)

        # Should have percentage calculations
        assert "90.0%" in report
        assert "10.0%" in report

    def test_report_includes_field_details(self):
        """Report should include field details per event."""
        from ingestion.coverage_report import generate_coverage_report

        result = DiscoveryResult()
        result.total_lines = 100
        result.events = {
            "gameStateUpdate": EventInfo(
                name="gameStateUpdate",
                count=100,
                fields={
                    "data.price": FieldInfo(
                        "data.price",
                        "number",
                        100,
                        sample_values=[1.0, 2.5, 10.0],
                    ),
                },
            ),
        }

        report = generate_coverage_report(result)

        assert "data.price" in report
        assert "number" in report
        assert "1.0" in report or "2.5" in report  # Sample values

    def test_report_includes_errors(self):
        """Report should include parse errors if any."""
        from ingestion.coverage_report import generate_coverage_report

        result = DiscoveryResult()
        result.total_lines = 100
        result.errors = [
            "file1.jsonl:10: Invalid JSON",
            "file2.jsonl:5: Unexpected token",
        ]
        result.events = {}

        report = generate_coverage_report(result)

        assert "## Parse Errors" in report
        assert "Invalid JSON" in report


class TestParseDictionaryFields:
    """Test parsing documented fields from FIELD_DICTIONARY.md."""

    def test_parse_field_dictionary(self):
        """Parse field paths from FIELD_DICTIONARY.md format."""
        from ingestion.coverage_report import parse_field_dictionary

        # Sample content matching FIELD_DICTIONARY.md format
        content = """
# WebSocket Event Field Dictionary

## gameStateUpdate Fields

### Core State (P0)

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.gameId` | string | - | Unique identifier |
| `$.data.active` | boolean | - | Whether game is active |
| `$.data.price` | number | multiplier | Current token multiplier |

### Leaderboard (Server-Authoritative)

| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.leaderboard[*].id` | string | - | Player's unique DID |
| `$.data.leaderboard[*].pnl` | number | SOL | Player profit/loss |
"""

        fields = parse_field_dictionary(content)

        # Should extract field paths (normalized)
        assert "data.gameId" in fields
        assert "data.active" in fields
        assert "data.price" in fields
        assert "data.leaderboard[].id" in fields
        assert "data.leaderboard[].pnl" in fields

    def test_parse_normalizes_paths(self):
        """Field paths should be normalized (remove $., convert [*] to [])."""
        from ingestion.coverage_report import parse_field_dictionary

        content = """
| Field | Type | Units | Meaning |
|-------|------|-------|---------|
| `$.data.leaderboard[*].avgCost` | number | - | Average |
| `$.data.gameHistory[*].prices[*]` | number | - | Prices |
"""

        fields = parse_field_dictionary(content)

        # [*] should become []
        assert "data.leaderboard[].avgCost" in fields
        assert "data.gameHistory[].prices[]" in fields


class TestGenerateDiffReport:
    """Test diff report comparing discovered vs documented fields."""

    def test_diff_finds_undocumented_fields(self):
        """Identify fields in recordings but NOT in documentation."""
        from ingestion.coverage_report import generate_diff_report

        discovered = {"data.price", "data.active", "data.newField"}
        documented = {"data.price", "data.active"}

        report = generate_diff_report(discovered, documented)

        assert "## Undocumented Fields" in report or "## New Fields" in report
        assert "data.newField" in report

    def test_diff_finds_stale_fields(self):
        """Identify fields in docs but NOT in recordings."""
        from ingestion.coverage_report import generate_diff_report

        discovered = {"data.price"}
        documented = {"data.price", "data.deprecatedField"}

        report = generate_diff_report(discovered, documented)

        assert "## Stale Fields" in report or "## Missing from Recordings" in report
        assert "data.deprecatedField" in report

    def test_diff_shows_matched_fields(self):
        """Show count of matched/validated fields."""
        from ingestion.coverage_report import generate_diff_report

        discovered = {"data.price", "data.active", "data.gameId"}
        documented = {"data.price", "data.active", "data.gameId"}

        report = generate_diff_report(discovered, documented)

        assert "3" in report  # 3 matched fields
        assert "100%" in report or "validated" in report.lower()


class TestWithSampleFixture:
    """Test with sample capture fixture."""

    @pytest.fixture
    def discovery_result(self):
        """Run discovery on sample fixture."""
        from ingestion.event_discovery import scan_jsonl_file

        fixture_path = Path(__file__).parent / "fixtures" / "sample_capture.jsonl"
        if not fixture_path.exists():
            pytest.skip("Sample capture fixture not found")
        return scan_jsonl_file(fixture_path)

    def test_full_coverage_report(self, discovery_result):
        """Generate full coverage report from fixture."""
        from ingestion.coverage_report import generate_coverage_report

        report = generate_coverage_report(discovery_result)

        # Should be valid markdown
        assert report.startswith("#")
        assert "## Coverage Summary" in report
        assert "gameStateUpdate" in report
