"""Generate coverage verification reports with diff against documentation.

This module generates markdown reports showing:
1. Complete coverage of discovered events and fields
2. Diff against existing FIELD_DICTIONARY.md (validate-and-augment)
3. Identification of undocumented and stale fields

Example:
    >>> from ingestion.event_discovery import scan_recordings
    >>> from ingestion.coverage_report import generate_coverage_report, generate_diff_report
    >>> result = scan_recordings(Path("./raw_captures"))
    >>> report = generate_coverage_report(result)
    >>> print(report)
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Set

from ingestion.event_discovery import DiscoveryResult


def generate_coverage_report(result: DiscoveryResult) -> str:
    """Generate markdown coverage report.

    Creates a comprehensive report showing all discovered events,
    their field counts, frequencies, and sample values.

    Args:
        result: Discovery results from scanning

    Returns:
        Markdown formatted report string
    """
    lines = [
        "# WebSocket Recording Coverage Report",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Coverage Summary",
        "",
        f"- **Files Scanned**: {result.files_scanned} files",
        f"- **Total Events**: {result.total_lines:,} events",
        f"- **Unique Event Types**: {len(result.events)} unique event types",
        f"- **Parse Errors**: {len(result.errors)}",
        "",
    ]

    # Calculate total unique fields
    total_fields = sum(len(e.fields) for e in result.events.values())
    lines.append(f"- **Total Unique Field Paths**: {total_fields:,}")
    lines.append("")

    # Event breakdown table
    lines.append("## Event Types")
    lines.append("")
    lines.append("| Event | Count | % of Total | Unique Fields |")
    lines.append("|-------|------:|:----------:|:-------------:|")

    for name, event in sorted(
        result.events.items(), key=lambda x: -x[1].count
    ):
        pct = (
            (event.count / result.total_lines * 100)
            if result.total_lines
            else 0
        )
        lines.append(
            f"| `{name}` | {event.count:,} | {pct:.1f}% | {len(event.fields)} |"
        )

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
        lines.append("|------------|:----:|------:|---------------|")

        for path, field in sorted(event.fields.items()):
            samples = ", ".join(str(s)[:40] for s in field.sample_values[:3])
            lines.append(
                f"| `{path}` | {field.type} | {field.count:,} | {samples} |"
            )

        lines.append("")

    # Parse errors section
    if result.errors:
        lines.append("## Parse Errors")
        lines.append("")
        for error in result.errors[:20]:
            lines.append(f"- {error}")
        if len(result.errors) > 20:
            lines.append(f"- *... and {len(result.errors) - 20} more*")
        lines.append("")

    return "\n".join(lines)


def parse_field_dictionary(content: str) -> Set[str]:
    """Parse field paths from FIELD_DICTIONARY.md format.

    Extracts field paths from markdown tables in the format:
    | `$.data.fieldName` | type | units | description |

    Args:
        content: Markdown content of FIELD_DICTIONARY.md

    Returns:
        Set of normalized field paths
    """
    fields = set()

    # Match field paths in backticks within table rows
    # Format: | `$.data.someField` | or | `$.data.array[*].field` |
    pattern = r"\|\s*`\$\.([^`]+)`\s*\|"

    for match in re.finditer(pattern, content):
        path = match.group(1)
        # Normalize: [*] -> []
        normalized = path.replace("[*]", "[]")
        fields.add(normalized)

    return fields


def load_field_dictionary(path: Path) -> Set[str]:
    """Load and parse FIELD_DICTIONARY.md.

    Args:
        path: Path to FIELD_DICTIONARY.md

    Returns:
        Set of documented field paths
    """
    if not path.exists():
        return set()

    content = path.read_text(encoding="utf-8")
    return parse_field_dictionary(content)


def generate_diff_report(
    discovered: Set[str],
    documented: Set[str],
) -> str:
    """Generate diff report comparing discovered vs documented fields.

    Identifies:
    - New fields: in recordings but not documented
    - Stale fields: documented but not in recordings
    - Validated fields: in both (matched)

    Args:
        discovered: Set of field paths from discovery
        documented: Set of field paths from FIELD_DICTIONARY.md

    Returns:
        Markdown diff report
    """
    matched = discovered & documented
    undocumented = discovered - documented
    stale = documented - discovered

    total_discovered = len(discovered)
    total_documented = len(documented)
    match_rate = (len(matched) / total_discovered * 100) if total_discovered else 0

    lines = [
        "# Field Coverage Diff Report",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Summary",
        "",
        f"- **Discovered Fields**: {total_discovered}",
        f"- **Documented Fields**: {total_documented}",
        f"- **Matched/Validated**: {len(matched)} ({match_rate:.1f}%)",
        f"- **New (undocumented)**: {len(undocumented)}",
        f"- **Stale (not in recordings)**: {len(stale)}",
        "",
    ]

    # Coverage status
    if len(undocumented) == 0 and len(stale) == 0:
        lines.append("**Status: 100% Coverage Match**")
    elif len(undocumented) > 0:
        lines.append(f"**Status: {len(undocumented)} fields need documentation**")
    lines.append("")

    # New/undocumented fields
    if undocumented:
        lines.append("## New Fields (Need Documentation)")
        lines.append("")
        lines.append("These fields were found in recordings but are not documented:")
        lines.append("")
        for path in sorted(undocumented):
            lines.append(f"- `{path}`")
        lines.append("")

    # Stale fields
    if stale:
        lines.append("## Stale Fields (Not in Recordings)")
        lines.append("")
        lines.append("These fields are documented but were not found in recordings:")
        lines.append("")
        for path in sorted(stale):
            lines.append(f"- `{path}`")
        lines.append("")

    # Matched fields (collapsed for brevity)
    if matched:
        lines.append("## Validated Fields")
        lines.append("")
        lines.append(
            f"<details><summary>{len(matched)} fields validated</summary>"
        )
        lines.append("")
        for path in sorted(matched):
            lines.append(f"- `{path}`")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines)


def generate_full_report(
    result: DiscoveryResult,
    dictionary_path: Path | None = None,
) -> str:
    """Generate combined coverage and diff report.

    Args:
        result: Discovery results
        dictionary_path: Optional path to FIELD_DICTIONARY.md

    Returns:
        Combined markdown report
    """
    # Basic coverage report
    coverage = generate_coverage_report(result)

    # If dictionary provided, add diff
    if dictionary_path and dictionary_path.exists():
        documented = load_field_dictionary(dictionary_path)

        # Get all discovered field paths
        discovered = set()
        for event in result.events.values():
            discovered.update(event.fields.keys())

        diff = generate_diff_report(discovered, documented)

        return coverage + "\n---\n\n" + diff

    return coverage


if __name__ == "__main__":
    import argparse

    from ingestion.event_discovery import scan_recordings, scan_jsonl_file

    parser = argparse.ArgumentParser(
        description="Generate coverage report from WebSocket recordings"
    )
    parser.add_argument(
        "path",
        type=Path,
        help="JSONL file or directory to analyze",
    )
    parser.add_argument(
        "--dictionary",
        type=Path,
        help="Path to FIELD_DICTIONARY.md for diff comparison",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file (default: stdout)",
    )

    args = parser.parse_args()

    # Discover
    if args.path.is_file():
        result = scan_jsonl_file(args.path)
    else:
        result = scan_recordings(args.path)

    # Generate report
    report = generate_full_report(result, args.dictionary)

    # Output
    if args.output:
        args.output.write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}")
    else:
        print(report)
