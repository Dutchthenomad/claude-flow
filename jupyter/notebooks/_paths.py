"""
Shared paths and utilities for Claude Flow notebooks.
Import this at the top of every notebook:

    from _paths import *
"""

import os
import sys
from pathlib import Path

# Core paths
CLAUDE_FLOW_ROOT = Path(os.environ.get("CLAUDE_FLOW_ROOT", Path(__file__).parent.parent.parent)).resolve()
CHROMADB_PATH = Path(os.environ.get("CHROMADB_PATH", CLAUDE_FLOW_ROOT / "rag-pipeline/storage/chroma"))
KNOWLEDGE_PATH = Path(os.environ.get("KNOWLEDGE_PATH", CLAUDE_FLOW_ROOT / "knowledge/rugs-events"))

# Data directories
RUGS_DATA_DIR = Path(os.environ.get("RUGS_DATA_DIR", Path.home() / "rugs_data"))
RUGS_RECORDINGS_DIR = Path(os.environ.get("RUGS_RECORDINGS_DIR", Path.home() / "rugs_recordings"))

# Related projects (may be None if not configured)
_rl_bot = os.environ.get("RUGS_RL_BOT_PATH", "")
RUGS_RL_BOT_PATH = Path(_rl_bot) if _rl_bot else None

_vectra = os.environ.get("VECTRA_PLAYER_PATH", "")
VECTRA_PLAYER_PATH = Path(_vectra) if _vectra else None

_replayer = os.environ.get("REPLAYER_PATH", "")
REPLAYER_PATH = Path(_replayer) if _replayer else None

# Add rag-pipeline to path for imports
RAG_PIPELINE_PATH = CLAUDE_FLOW_ROOT / "rag-pipeline"
if str(RAG_PIPELINE_PATH) not in sys.path:
    sys.path.insert(0, str(RAG_PIPELINE_PATH))


def get_chromadb_client():
    """Get ChromaDB client for the knowledge base."""
    import chromadb
    return chromadb.PersistentClient(path=str(CHROMADB_PATH))


def get_knowledge_collection():
    """Get the main knowledge base collection."""
    client = get_chromadb_client()
    return client.get_collection("claude_flow_knowledge")


def load_discovered_schemas():
    """Load discovered event schemas from ingestion pipeline."""
    import json
    schemas_path = KNOWLEDGE_PATH / "generated" / "discovered_schemas.json"
    if schemas_path.exists():
        with open(schemas_path) as f:
            return json.load(f)
    return {}


def load_discovered_fields():
    """Load discovered fields from ingestion pipeline."""
    import json
    fields_path = KNOWLEDGE_PATH / "generated" / "discovered_fields.json"
    if fields_path.exists():
        with open(fields_path) as f:
            return json.load(f)
    return {}


def load_canonical_spec():
    """Load the canonical WebSocket events spec."""
    spec_path = KNOWLEDGE_PATH / "WEBSOCKET_EVENTS_SPEC.md"
    if spec_path.exists():
        return spec_path.read_text()
    return ""


def print_env():
    """Print current environment configuration."""
    print("Claude Flow Notebook Environment")
    print("=" * 40)
    print(f"CLAUDE_FLOW_ROOT:    {CLAUDE_FLOW_ROOT}")
    print(f"CHROMADB_PATH:       {CHROMADB_PATH}")
    print(f"KNOWLEDGE_PATH:      {KNOWLEDGE_PATH}")
    print(f"RUGS_DATA_DIR:       {RUGS_DATA_DIR}")
    print(f"RUGS_RECORDINGS_DIR: {RUGS_RECORDINGS_DIR}")
    print(f"RUGS_RL_BOT_PATH:    {RUGS_RL_BOT_PATH or '(not configured)'}")
    print(f"VECTRA_PLAYER_PATH:  {VECTRA_PLAYER_PATH or '(not configured)'}")
    print(f"REPLAYER_PATH:       {REPLAYER_PATH or '(not configured)'}")
    print("=" * 40)


# Export all
__all__ = [
    'CLAUDE_FLOW_ROOT',
    'CHROMADB_PATH',
    'KNOWLEDGE_PATH',
    'RUGS_DATA_DIR',
    'RUGS_RECORDINGS_DIR',
    'RUGS_RL_BOT_PATH',
    'VECTRA_PLAYER_PATH',
    'REPLAYER_PATH',
    'RAG_PIPELINE_PATH',
    'get_chromadb_client',
    'get_knowledge_collection',
    'load_discovered_schemas',
    'load_discovered_fields',
    'load_canonical_spec',
    'print_env',
]
