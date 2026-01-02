#!/bin/bash
# Clone Solana blockchain & forensics repos for rugs.fun investigation
# Created: December 31, 2025

set -e

KNOWLEDGE_DIR="/home/nomad/Desktop/claude-flow/knowledge/RAG SUPERPACK"
cd "$KNOWLEDGE_DIR"

echo "=== Cloning Solana & Blockchain Forensics Sources ==="
echo ""

# Solana Core & Development
echo "[1/5] Solana Core & Anchor Framework..."
mkdir -p solana && cd solana
[ ! -d "anchor" ] && git clone --depth 1 https://github.com/coral-xyz/anchor.git || echo "  anchor exists"
# Note: solana-labs/solana is HUGE (~2GB), clone separately if needed
# [ ! -d "solana" ] && git clone --depth 1 https://github.com/solana-labs/solana.git
cd ..

# Python SDKs
echo "[2/5] Python SDKs (solana-py, solders, anchorpy)..."
mkdir -p solana-python && cd solana-python
[ ! -d "solana-py" ] && git clone --depth 1 https://github.com/michaelhly/solana-py.git || echo "  solana-py exists"
[ ! -d "solders" ] && git clone --depth 1 https://github.com/kevinheavey/solders.git || echo "  solders exists"
[ ! -d "anchorpy" ] && git clone --depth 1 https://github.com/kevinheavey/anchorpy.git || echo "  anchorpy exists"
cd ..

# Reverse Engineering Tools
echo "[3/5] Reverse Engineering Tools..."
mkdir -p reverse-engineering && cd reverse-engineering
[ ! -d "sol-azy" ] && git clone --depth 1 https://github.com/FuzzingLabs/sol-azy.git || echo "  sol-azy exists"
[ ! -d "solana-data-reverser" ] && git clone --depth 1 https://github.com/accretion-xyz/solana-data-reverser.git || echo "  solana-data-reverser exists"
cd ..

# Transaction Analysis
echo "[4/5] Transaction Analysis Tools..."
mkdir -p tx-analysis && cd tx-analysis
[ ! -d "Solana-Transaction-Analyzer" ] && git clone --depth 1 https://github.com/faradaysage/Solana-Transaction-Analyzer.git || echo "  Solana-Transaction-Analyzer exists"
[ ! -d "solana-bundler-detector" ] && git clone --depth 1 https://github.com/nothingdao/solana-bundler-detector.git || echo "  solana-bundler-detector exists"
[ ! -d "solana-tx-parser-public" ] && git clone --depth 1 https://github.com/debridge-finance/solana-tx-parser-public.git || echo "  solana-tx-parser-public exists"
[ ! -d "solana-parser" ] && git clone --depth 1 https://github.com/tkhq/solana-parser.git || echo "  solana-parser exists"
cd ..

# Blockchain Forensics
echo "[5/5] Blockchain Forensics & Investigation..."
mkdir -p forensics && cd forensics
[ ! -d "On-Chain-Investigations-Tools-List" ] && git clone --depth 1 https://github.com/OffcierCia/On-Chain-Investigations-Tools-List.git || echo "  On-Chain-Investigations-Tools-List exists"
[ ! -d "provably-fair-app" ] && git clone --depth 1 https://github.com/provably-fair/provably-fair-app.git || echo "  provably-fair-app exists"
cd ..

echo ""
echo "=== Solana & Forensics Clone Complete ==="
echo ""
echo "New directories:"
du -sh solana/ solana-python/ reverse-engineering/ tx-analysis/ forensics/ 2>/dev/null
echo ""
echo "Total SUPERPACK size:"
du -sh .
echo ""
echo "=== Python Dependencies ==="
echo "Install with:"
echo "  pip install solana solders anchorpy requests beautifulsoup4 web3 python-dotenv"
