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
]

# Raw WebSocket captures (indexed separately with event_chunker)
RUGS_RAW_CAPTURES_PATH = Path("/home/nomad/rugs_recordings/raw_captures")

# REPLAYER event documentation (symlinked or copied)
REPLAYER_EVENTS_SPEC = Path("/home/nomad/Desktop/REPLAYER/docs/specs")

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
