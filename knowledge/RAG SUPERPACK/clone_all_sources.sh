#!/bin/bash
# Clone all RAG knowledge sources for ML/RL/Bayesian knowledge base
# Created: December 31, 2025

set -e

KNOWLEDGE_DIR="/home/nomad/Desktop/claude-flow/knowledge/RAG SUPERPACK"
cd "$KNOWLEDGE_DIR"

echo "=== Cloning RAG Knowledge Sources ==="
echo "Target: $KNOWLEDGE_DIR"
echo ""

# RL Core
echo "[1/4] Cloning RL Core repositories..."
mkdir -p rl-core && cd rl-core
[ ! -d "stable-baselines3" ] && git clone --depth 1 https://github.com/DLR-RM/stable-baselines3.git || echo "  stable-baselines3 exists"
[ ! -d "cleanrl" ] && git clone --depth 1 https://github.com/vwxyzjn/cleanrl.git || echo "  cleanrl exists"
[ ! -d "Gymnasium" ] && git clone --depth 1 https://github.com/Farama-Foundation/Gymnasium.git || echo "  Gymnasium exists"
[ ! -d "spinningup" ] && git clone --depth 1 https://github.com/openai/spinningup.git || echo "  spinningup exists"
[ ! -d "deep-rl-class" ] && git clone --depth 1 https://github.com/huggingface/deep-rl-class.git || echo "  deep-rl-class exists"
cd ..

# Bayesian
echo "[2/4] Cloning Bayesian repositories..."
mkdir -p bayesian && cd bayesian
[ ! -d "pymc" ] && git clone --depth 1 https://github.com/pymc-devs/pymc.git || echo "  pymc exists"
[ ! -d "Probabilistic-Programming-and-Bayesian-Methods-for-Hackers" ] && git clone --depth 1 https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers.git || echo "  Bayesian-Hackers exists"
[ ! -d "arviz" ] && git clone --depth 1 https://github.com/arviz-devs/arviz.git || echo "  arviz exists"
cd ..

# Decision Transformers
echo "[3/4] Cloning Decision Transformer repositories..."
mkdir -p decision-transformers && cd decision-transformers
[ ! -d "decision-transformer" ] && git clone --depth 1 https://github.com/kzl/decision-transformer.git || echo "  decision-transformer exists"
[ ! -d "trl" ] && git clone --depth 1 https://github.com/huggingface/trl.git || echo "  trl exists"
[ ! -d "trajectory-transformer" ] && git clone --depth 1 https://github.com/jannerm/trajectory-transformer.git || echo "  trajectory-transformer exists"
cd ..

# MCP & Claude
echo "[4/4] Cloning MCP repositories..."
mkdir -p mcp && cd mcp
[ ! -d "servers" ] && git clone --depth 1 https://github.com/modelcontextprotocol/servers.git || echo "  mcp-servers exists"
[ ! -d "anthropic-cookbook" ] && git clone --depth 1 https://github.com/anthropics/anthropic-cookbook.git || echo "  anthropic-cookbook exists"
[ ! -d "claude-code" ] && git clone --depth 1 https://github.com/anthropics/claude-code.git || echo "  claude-code exists"
cd ..

echo ""
echo "=== Clone Complete ==="
echo ""
echo "Directory structure:"
find . -maxdepth 2 -type d | head -30
echo ""
echo "Total size:"
du -sh .
