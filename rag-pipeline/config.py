"""RAG Pipeline Configuration."""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
RAG_ROOT = Path(__file__).parent
CHROMA_PATH = RAG_ROOT / "storage" / "chroma"

# Knowledge sources to index
KNOWLEDGE_PATHS = [
    # Claude-flow core knowledge
    PROJECT_ROOT / "knowledge" / "anthropic-docs",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "commands",
    PROJECT_ROOT / "agents",
    PROJECT_ROOT / "skills",
    # Rugs.fun WebSocket event knowledge
    PROJECT_ROOT / "knowledge" / "rugs-events",
    # Rugs.fun strategy knowledge base (L1-L7 layers)
    PROJECT_ROOT / "knowledge" / "rugs-strategy",
]

# Raw WebSocket captures (indexed separately with event_chunker)
# Check multiple possible locations
_POSSIBLE_CAPTURE_PATHS = [
    PROJECT_ROOT / "rag-pipeline" / "RAW SOCKETS" / "rugs_recordings" / "raw_captures",
    Path.home() / "rugs_recordings" / "raw_captures",
    Path("/home/nomad/rugs_recordings/raw_captures"),
]
RUGS_RAW_CAPTURES_PATH = next(
    (p for p in _POSSIBLE_CAPTURE_PATHS if p.exists()),
    _POSSIBLE_CAPTURE_PATHS[0],  # Default to first if none exist
)

# Generated outputs from WebSocket ingestion
RUGS_GENERATED_PATH = PROJECT_ROOT / "knowledge" / "rugs-events" / "generated"

# Field dictionary for validation
RUGS_FIELD_DICTIONARY = PROJECT_ROOT / "knowledge" / "rugs-events" / "FIELD_DICTIONARY.md"

# REPLAYER event documentation (symlinked or copied)
REPLAYER_EVENTS_SPEC = Path("/home/nomad/Desktop/REPLAYER/docs/specs")

# ChromaDB collection for WebSocket events (separate from main knowledge)
RUGS_EVENTS_COLLECTION = "rugs_events"

# File patterns to include
INCLUDE_PATTERNS = ["*.md", "*.py", "*.yaml", "*.yml", "*.json"]

# JSONL patterns for raw event captures
JSONL_PATTERNS = ["*.jsonl"]

# Chunking settings
CHUNK_SIZE = 512  # tokens
CHUNK_OVERLAP = 50  # tokens

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 dimensions, fast
EMBEDDING_DIMENSIONS = 384

# ChromaDB collection name
COLLECTION_NAME = "claude_flow_knowledge"

# Retrieval defaults
DEFAULT_TOP_K = 5
