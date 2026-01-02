"""Text chunking with markdown awareness."""
import re
from dataclasses import dataclass
from typing import Iterator

try:
    import tiktoken
    ENCODER = tiktoken.get_encoding("cl100k_base")
except ImportError:
    ENCODER = None


@dataclass
class Chunk:
    """A text chunk with metadata."""
    text: str
    source: str
    line_start: int
    line_end: int
    headers: list[str]


def count_tokens(text: str) -> int:
    """Count tokens in text."""
    if ENCODER:
        return len(ENCODER.encode(text))
    # Fallback: rough estimate (4 chars per token)
    return len(text) // 4


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> Iterator[Chunk]:
    """Split text into chunks with overlap.
    
    Args:
        text: Text to chunk
        source: Source file path
        chunk_size: Max tokens per chunk
        chunk_overlap: Token overlap between chunks
    
    Yields:
        Chunk objects with text and metadata
    """
    lines = text.split('\n')
    current_chunk_lines = []
    current_tokens = 0
    line_start = 1
    
    for i, line in enumerate(lines, 1):
        line_tokens = count_tokens(line)
        
        if current_tokens + line_tokens > chunk_size and current_chunk_lines:
            # Yield current chunk
            yield Chunk(
                text='\n'.join(current_chunk_lines),
                source=source,
                line_start=line_start,
                line_end=i - 1,
                headers=[],
            )
            
            # Keep overlap lines
            overlap_lines = []
            overlap_tokens = 0
            for ol in reversed(current_chunk_lines):
                ol_tokens = count_tokens(ol)
                if overlap_tokens + ol_tokens <= chunk_overlap:
                    overlap_lines.insert(0, ol)
                    overlap_tokens += ol_tokens
                else:
                    break
            
            current_chunk_lines = overlap_lines
            current_tokens = overlap_tokens
            line_start = i - len(overlap_lines)
        
        current_chunk_lines.append(line)
        current_tokens += line_tokens
    
    # Yield final chunk
    if current_chunk_lines:
        yield Chunk(
            text='\n'.join(current_chunk_lines),
            source=source,
            line_start=line_start,
            line_end=len(lines),
            headers=[],
        )


def chunk_markdown(
    text: str,
    source: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> Iterator[Chunk]:
    """Chunk markdown with header context preservation.

    Tracks markdown headers and PREPENDS them to chunk text for better retrieval.
    Headers are also stored in metadata for reference.
    """
    lines = text.split('\n')
    current_chunk_lines = []
    current_tokens = 0
    line_start = 1
    current_headers = []  # Stack of (level, text) tuples

    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    def _build_chunk_text(chunk_lines: list, headers: list) -> str:
        """Build chunk text with header context prepended."""
        header_names = [h[1] for h in headers]
        if header_names:
            # Prepend header breadcrumb for better semantic search
            header_prefix = "[" + " > ".join(header_names) + "]\n\n"
            return header_prefix + '\n'.join(chunk_lines)
        return '\n'.join(chunk_lines)

    for i, line in enumerate(lines, 1):
        line_tokens = count_tokens(line)

        # Track headers
        match = header_pattern.match(line)
        if match:
            level = len(match.group(1))
            header_text = match.group(2).strip()
            # Pop headers at same or lower level
            current_headers = [(l, t) for l, t in current_headers if l < level]
            current_headers.append((level, header_text))

        if current_tokens + line_tokens > chunk_size and current_chunk_lines:
            # Yield current chunk with header context PREPENDED
            chunk_text = _build_chunk_text(current_chunk_lines, current_headers)
            yield Chunk(
                text=chunk_text,
                source=source,
                line_start=line_start,
                line_end=i - 1,
                headers=[h[1] for h in current_headers],
            )

            # Keep overlap lines
            overlap_lines = []
            overlap_tokens = 0
            for ol in reversed(current_chunk_lines):
                ol_tokens = count_tokens(ol)
                if overlap_tokens + ol_tokens <= chunk_overlap:
                    overlap_lines.insert(0, ol)
                    overlap_tokens += ol_tokens
                else:
                    break

            current_chunk_lines = overlap_lines
            current_tokens = overlap_tokens
            line_start = i - len(overlap_lines)

        current_chunk_lines.append(line)
        current_tokens += line_tokens

    # Yield final chunk with header context PREPENDED
    if current_chunk_lines:
        chunk_text = _build_chunk_text(current_chunk_lines, current_headers)
        yield Chunk(
            text=chunk_text,
            source=source,
            line_start=line_start,
            line_end=len(lines),
            headers=[h[1] for h in current_headers],
        )


if __name__ == "__main__":
    # Test chunking
    test_md = """# Main Header

Some intro text.

## Section One

Content for section one.
More content here.

### Subsection

Deep content.

## Section Two

Different section.
"""
    print("Testing markdown chunker:")
    for chunk in chunk_markdown(test_md, "test.md", chunk_size=50):
        print(f"  Lines {chunk.line_start}-{chunk.line_end}: {chunk.headers}")
        print(f"    {chunk.text[:50]}...")
