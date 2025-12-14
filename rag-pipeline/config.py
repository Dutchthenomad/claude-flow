"""RAG Pipeline Configuration."""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
RAG_ROOT = Path(__file__).parent
CHROMA_PATH = RAG_ROOT / "storage" / "chroma"

# Knowledge sources to index
KNOWLEDGE_PATHS = [
    PROJECT_ROOT / "knowledge" / "anthropic-docs",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "commands",
    PROJECT_ROOT / "agents",
    PROJECT_ROOT / "skills",
]

# File patterns to include
INCLUDE_PATTERNS = ["*.md", "*.py", "*.yaml", "*.yml", "*.json"]

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
