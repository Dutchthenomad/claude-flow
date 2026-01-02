#!/bin/bash
# Clone risk management, position sizing, and backtesting repos
# Created: December 31, 2025

set -e

KNOWLEDGE_DIR="/home/nomad/Desktop/claude-flow/knowledge/RAG SUPERPACK"
cd "$KNOWLEDGE_DIR"

echo "=== Cloning Risk Management Knowledge Sources ==="
echo ""

mkdir -p risk-management && cd risk-management

echo "[1/3] Portfolio Optimization..."
[ ! -d "Riskfolio-Lib" ] && git clone --depth 1 https://github.com/dcajasn/Riskfolio-Lib.git || echo "  Riskfolio-Lib exists"
[ ! -d "PyPortfolioOpt" ] && git clone --depth 1 https://github.com/PyPortfolio/PyPortfolioOpt.git || echo "  PyPortfolioOpt exists"
[ ! -d "skfolio" ] && git clone --depth 1 https://github.com/skfolio/skfolio.git || echo "  skfolio exists"

echo "[2/3] Risk Metrics & Monte Carlo..."
[ ! -d "quantstats" ] && git clone --depth 1 https://github.com/ranaroussi/quantstats.git || echo "  quantstats exists"
[ ! -d "mc_sim_fin" ] && git clone --depth 1 https://github.com/gaugau3000/mc_sim_fin.git || echo "  mc_sim_fin exists"
[ ! -d "empyrical" ] && git clone --depth 1 https://github.com/quantopian/empyrical.git || echo "  empyrical exists"

echo "[3/3] Backtesting Frameworks..."
[ ! -d "vectorbt" ] && git clone --depth 1 https://github.com/polakowo/vectorbt.git || echo "  vectorbt exists"
[ ! -d "backtrader" ] && git clone --depth 1 https://github.com/mementum/backtrader.git || echo "  backtrader exists"
[ ! -d "nautilus_trader" ] && git clone --depth 1 https://github.com/nautechsystems/nautilus_trader.git || echo "  nautilus_trader exists"

cd ..

echo ""
echo "[BONUS] Curated Lists & AI Platforms..."
mkdir -p curated && cd curated
[ ! -d "awesome-quant" ] && git clone --depth 1 https://github.com/wilsonfreitas/awesome-quant.git || echo "  awesome-quant exists"
[ ! -d "qlib" ] && git clone --depth 1 https://github.com/microsoft/qlib.git || echo "  qlib exists"
cd ..

echo ""
echo "=== Risk Management Clone Complete ==="
echo ""
echo "New directories:"
du -sh risk-management/ curated/ 2>/dev/null
echo ""
echo "Total SUPERPACK size:"
du -sh .
