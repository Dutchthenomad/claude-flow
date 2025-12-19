"""Main orchestrator for WebSocket recording ingestion.

This module coordinates the full ingestion pipeline:
1. Discovery - Scan all JSONL recordings for events and fields
2. Schema Generation - Create JSON schemas from discoveries
3. Coverage Report - Generate verification reports
4. Diff Analysis - Compare against documented fields
5. Chunking - Prepare for vector embedding (optional)

Example:
    >>> from ingestion.jsonl_ingest import ingest_websocket_recordings
    >>> result = ingest_websocket_recordings(
    ...     recordings_dir=Path("./raw_captures"),
    ...     output_dir=Path("./generated"),
    ... )
    >>> print(f"Discovered {result.events_discovered} events")
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class IngestionResult:
    """Results from an ingestion run.

    Attributes:
        files_scanned: Number of JSONL files processed
        events_discovered: Number of unique event types found
        fields_discovered: Total unique field paths found
        chunks_embedded: Number of chunks created for embedding
        errors: List of error messages encountered
    """

    files_scanned: int
    events_discovered: int
    fields_discovered: int
    chunks_embedded: int
    errors: List[str] = field(default_factory=list)


def ingest_websocket_recordings(
    recordings_dir: Path,
    output_dir: Path,
    dictionary_path: Path | None = None,
    embed: bool = True,
    verbose: bool = True,
) -> IngestionResult:
    """Run full ingestion pipeline on WebSocket recordings.

    Orchestrates the complete pipeline:
    1. Scans all JSONL files in recordings_dir
    2. Discovers all unique events and field paths
    3. Generates JSON schemas for each event type
    4. Creates flat field index for lookups
    5. Generates coverage report
    6. Optionally compares against documented fields
    7. Optionally creates chunks for embedding

    Args:
        recordings_dir: Directory containing JSONL recordings
        output_dir: Directory for generated output files
        dictionary_path: Optional path to FIELD_DICTIONARY.md for diff
        embed: Whether to generate vector embeddings
        verbose: Whether to print progress messages

    Returns:
        IngestionResult with statistics about the run
    """
    from ingestion.event_discovery import scan_recordings, get_all_field_paths
    from ingestion.schema_generator import (
        generate_all_schemas,
        generate_field_index,
    )
    from ingestion.coverage_report import (
        generate_coverage_report,
        generate_diff_report,
        load_field_dictionary,
    )

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: Discovery
    if verbose:
        print(f"Phase 1: Scanning recordings in {recordings_dir}...")

    discovery = scan_recordings(recordings_dir)

    if verbose:
        print(f"  Found {len(discovery.events)} event types")
        print(f"  Scanned {discovery.total_lines:,} events")
        print(f"  Files processed: {discovery.files_scanned}")

    # Count total fields
    total_fields = sum(len(e.fields) for e in discovery.events.values())

    if verbose:
        print(f"  Unique field paths: {total_fields}")

    # Phase 2: Schema Generation
    if verbose:
        print("\nPhase 2: Generating schemas...")

    schemas = generate_all_schemas(discovery)

    schema_path = output_dir / "discovered_schemas.json"
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schemas, f, indent=2)

    if verbose:
        print(f"  Saved {len(schemas)} schemas to {schema_path.name}")

    # Phase 3: Field Index
    if verbose:
        print("\nPhase 3: Generating field index...")

    field_index = generate_field_index(discovery)

    index_path = output_dir / "discovered_fields.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(field_index, f, indent=2)

    if verbose:
        print(f"  Saved {len(field_index)} field paths to {index_path.name}")

    # Phase 4: Coverage Report
    if verbose:
        print("\nPhase 4: Generating coverage report...")

    report = generate_coverage_report(discovery)

    report_path = output_dir / "coverage_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    if verbose:
        print(f"  Saved coverage report to {report_path.name}")

    # Phase 5: Diff Report (optional)
    if dictionary_path and dictionary_path.exists():
        if verbose:
            print(f"\nPhase 5: Comparing with {dictionary_path.name}...")

        documented = load_field_dictionary(dictionary_path)
        discovered = get_all_field_paths(discovery)

        diff = generate_diff_report(discovered, documented)

        diff_path = output_dir / "diff_report.md"
        with open(diff_path, "w", encoding="utf-8") as f:
            f.write(diff)

        undocumented = discovered - documented
        stale = documented - discovered

        if verbose:
            print(f"  Matched: {len(discovered & documented)} fields")
            print(f"  New (need docs): {len(undocumented)} fields")
            print(f"  Stale (not in recordings): {len(stale)} fields")
            print(f"  Saved diff report to {diff_path.name}")

    # Phase 6: Embedding (optional)
    chunks_embedded = 0
    if embed:
        if verbose:
            print("\nPhase 6: Generating embeddings...")

        # TODO: Integrate with ChromaDB embedding
        # For now, just count chunks that would be created
        from ingestion.event_chunker import chunk_discovery_result

        chunks = list(chunk_discovery_result(discovery))
        chunks_embedded = len(chunks)

        if verbose:
            print(f"  Would embed {chunks_embedded} chunks")
            print("  (Embedding not yet implemented)")

    # Summary
    if verbose:
        print("\n" + "=" * 50)
        print("Ingestion Complete")
        print("=" * 50)
        print(f"  Files scanned: {discovery.files_scanned}")
        print(f"  Events discovered: {len(discovery.events)}")
        print(f"  Fields discovered: {total_fields}")
        if discovery.errors:
            print(f"  Parse errors: {len(discovery.errors)}")

    return IngestionResult(
        files_scanned=discovery.files_scanned,
        events_discovered=len(discovery.events),
        fields_discovered=total_fields,
        chunks_embedded=chunks_embedded,
        errors=discovery.errors,
    )


def main():
    """CLI entry point for ingestion pipeline."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest WebSocket recordings into knowledge base"
    )
    parser.add_argument(
        "--recordings",
        type=Path,
        default=Path.home() / "rugs_recordings" / "raw_captures",
        help="Directory containing JSONL recordings",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent.parent
        / "knowledge"
        / "rugs-events"
        / "generated",
        help="Output directory for generated files",
    )
    parser.add_argument(
        "--dictionary",
        type=Path,
        default=None,
        help="Path to FIELD_DICTIONARY.md for comparison",
    )
    parser.add_argument(
        "--no-embed",
        action="store_true",
        help="Skip embedding generation",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    args = parser.parse_args()

    # Check recordings directory
    if not args.recordings.exists():
        print(f"Error: Recordings directory not found: {args.recordings}")
        print("\nExpected JSONL files at this location.")
        print("Set --recordings to specify a different path.")
        return 1

    # Auto-detect dictionary if not specified
    if args.dictionary is None:
        default_dict = (
            Path(__file__).parent.parent.parent
            / "knowledge"
            / "rugs-events"
            / "FIELD_DICTIONARY.md"
        )
        if default_dict.exists():
            args.dictionary = default_dict

    result = ingest_websocket_recordings(
        recordings_dir=args.recordings,
        output_dir=args.output,
        dictionary_path=args.dictionary,
        embed=not args.no_embed,
        verbose=not args.quiet,
    )

    if result.errors:
        print(f"\nWarning: {len(result.errors)} parse errors occurred")
        for error in result.errors[:5]:
            print(f"  - {error}")
        if len(result.errors) > 5:
            print(f"  ... and {len(result.errors) - 5} more")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
