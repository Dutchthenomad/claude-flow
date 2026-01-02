# RAG Knowledge Sources - ML/RL/Bayesian Superpack

**Created**: December 31, 2025
**Purpose**: Curated high-quality sources for RAG ingestion
**Status**: READY FOR INGESTION

---

## Layer 1: RL Fundamentals

### Stable Baselines 3
- **URL**: https://stable-baselines3.readthedocs.io
- **Clone**: `git clone https://github.com/DLR-RM/stable-baselines3.git`
- **Key Docs**:
  - `docs/guide/` - User guide
  - `docs/modules/` - Algorithm reference
- **Algorithms**: PPO, A2C, DQN, SAC, TD3, HER
- **RAG Priority**: HIGH

### Gymnasium (Farama Foundation)
- **URL**: https://gymnasium.farama.org
- **Clone**: `git clone https://github.com/Farama-Foundation/Gymnasium.git`
- **Key Docs**:
  - `docs/api/` - Core API reference
  - `docs/environments/` - Built-in envs
  - `docs/tutorials/` - Custom env creation
- **RAG Priority**: HIGH

### CleanRL
- **URL**: https://github.com/vwxyzjn/cleanrl
- **Clone**: `git clone https://github.com/vwxyzjn/cleanrl.git`
- **Key Files**:
  - `cleanrl/ppo.py` - PPO in ~300 lines
  - `cleanrl/dqn.py` - DQN implementation
  - `cleanrl/sac.py` - SAC implementation
- **RAG Priority**: HIGH (single-file = perfect for RAG)

### OpenAI Spinning Up
- **URL**: https://spinningup.openai.com
- **Clone**: `git clone https://github.com/openai/spinningup.git`
- **Key Docs**:
  - `docs/spinningup/` - Theory explanations
  - `spinup/algos/` - Reference implementations
- **RAG Priority**: MEDIUM (excellent theory)

### Hugging Face Deep RL Course
- **URL**: https://huggingface.co/learn/deep-rl-course
- **Clone**: `git clone https://github.com/huggingface/deep-rl-class.git`
- **Key Content**:
  - Unit 1-8: Progressive RL curriculum
  - Notebooks: Hands-on exercises
- **RAG Priority**: MEDIUM

---

## Layer 2: Bayesian Statistics

### PyMC
- **URL**: https://www.pymc.io/projects/docs
- **Clone**: `git clone https://github.com/pymc-devs/pymc.git`
- **Key Docs**:
  - `docs/source/learn/` - Tutorials
  - `docs/source/api/` - API reference
- **Topics**: MCMC, Variational Inference, GLMs, Time Series
- **RAG Priority**: HIGH

### Stan / PyStan
- **URL**: https://mc-stan.org/users/documentation
- **Clone**: `git clone https://github.com/stan-dev/stan.git`
- **Key Docs**:
  - `stan-reference-manual/` - Language reference
  - `stan-users-guide/` - Modeling guide
- **RAG Priority**: MEDIUM

### Bayesian Methods for Hackers
- **URL**: https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers
- **Clone**: `git clone https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers.git`
- **Key Content**: 6 chapters of practical Bayesian tutorials
- **RAG Priority**: HIGH (excellent pedagogy)

### ArviZ
- **URL**: https://python.arviz.org
- **Clone**: `git clone https://github.com/arviz-devs/arviz.git`
- **Key Docs**: Diagnostics, visualization, model comparison
- **RAG Priority**: MEDIUM

---

## Layer 3: Decision Transformers / Offline RL

### TRL (Transformer Reinforcement Learning)
- **URL**: https://huggingface.co/docs/trl
- **Clone**: `git clone https://github.com/huggingface/trl.git`
- **Key Docs**:
  - PPOTrainer for RLHF
  - RewardTrainer for reward models
  - DPO (Direct Preference Optimization)
- **RAG Priority**: HIGH

### Decision Transformer (Original)
- **URL**: https://github.com/kzl/decision-transformer
- **Paper**: https://arxiv.org/abs/2106.01345
- **Key Files**:
  - `gym/` - Gym environment implementation
  - `atari/` - Atari implementation
- **RAG Priority**: HIGH (core architecture)

### Trajectory Transformer
- **URL**: https://github.com/jannerm/trajectory-transformer
- **Paper**: https://arxiv.org/abs/2106.02039
- **Key Concept**: Planning as sequence modeling
- **RAG Priority**: MEDIUM

---

## Layer 4: MCP Servers & Plugins

### Official MCP Servers
- **URL**: https://github.com/modelcontextprotocol/servers
- **Clone**: `git clone https://github.com/modelcontextprotocol/servers.git`
- **Key Servers**:
  - `src/filesystem/` - File operations
  - `src/github/` - GitHub API
  - `src/postgres/` - Database access
  - `src/puppeteer/` - Browser automation
- **RAG Priority**: HIGH

### MCP Specification
- **URL**: https://spec.modelcontextprotocol.io
- **Key Sections**:
  - Protocol specification
  - Tool definitions
  - Resource handling
- **RAG Priority**: HIGH

### Anthropic Cookbook
- **URL**: https://github.com/anthropics/anthropic-cookbook
- **Clone**: `git clone https://github.com/anthropics/anthropic-cookbook.git`
- **Key Content**:
  - Tool use examples
  - MCP integration patterns
  - Claude best practices
- **RAG Priority**: HIGH

### Awesome MCP Servers
- **URL**: https://github.com/punkpeye/awesome-mcp-servers
- **Content**: Catalog of 2000+ community servers
- **RAG Priority**: LOW (index, not content)

---

## Layer 5: Hugging Face Models

### Recommended Model Searches

```bash
# Decision Transformers
huggingface-cli download edbeeching/decision-transformer-gym-hopper-medium

# Time Series
huggingface-cli download amazon/chronos-t5-small

# Finance/Trading
huggingface-cli download ProsusAI/finbert
```

### Key Model Categories

| Category | Example Model | Use Case |
|----------|---------------|----------|
| Decision Transformer | `edbeeching/decision-transformer-*` | Offline RL |
| Time Series | `amazon/chronos-*` | Forecasting |
| Finance NLP | `ProsusAI/finbert` | Sentiment |
| Embeddings | `sentence-transformers/*` | RAG retrieval |

---

## Ingestion Priority Order

1. **IMMEDIATE** (Week 1):
   - CleanRL single-file implementations
   - SB3 algorithm guides
   - Gymnasium API docs
   - PyMC tutorials

2. **SHORT-TERM** (Week 2-3):
   - Decision Transformer code
   - TRL documentation
   - MCP server implementations
   - Anthropic cookbook

3. **MEDIUM-TERM** (Month 1):
   - Spinning Up theory
   - Stan reference manual
   - Bayesian Methods for Hackers
   - HF Deep RL Course

---

## Clone Script

```bash
#!/bin/bash
# Clone all RAG knowledge sources

KNOWLEDGE_DIR="/home/nomad/Desktop/claude-flow/knowledge/RAG SUPERPACK"
cd "$KNOWLEDGE_DIR"

# RL Core
mkdir -p rl-core && cd rl-core
git clone --depth 1 https://github.com/DLR-RM/stable-baselines3.git
git clone --depth 1 https://github.com/vwxyzjn/cleanrl.git
git clone --depth 1 https://github.com/Farama-Foundation/Gymnasium.git
git clone --depth 1 https://github.com/openai/spinningup.git
cd ..

# Bayesian
mkdir -p bayesian && cd bayesian
git clone --depth 1 https://github.com/pymc-devs/pymc.git
git clone --depth 1 https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers.git
git clone --depth 1 https://github.com/arviz-devs/arviz.git
cd ..

# Decision Transformers
mkdir -p decision-transformers && cd decision-transformers
git clone --depth 1 https://github.com/kzl/decision-transformer.git
git clone --depth 1 https://github.com/huggingface/trl.git
cd ..

# MCP
mkdir -p mcp && cd mcp
git clone --depth 1 https://github.com/modelcontextprotocol/servers.git
git clone --depth 1 https://github.com/anthropics/anthropic-cookbook.git
cd ..

echo "All repositories cloned!"
```

---

## Integration with Existing Knowledge

Your current knowledge structure:

```
knowledge/
├── rugs-events/              # CANONICAL WebSocket spec
├── rugs "gameHistory"/       # Manual captures (PRE-CANON)
├── HOLDING-CELL/             # Session discoveries (5 docs)
└── RAG SUPERPACK/            # THIS COLLECTION
    ├── RAG_KNOWLEDGE_SOURCES.md  # This document
    ├── rl-core/              # Clone target
    ├── bayesian/             # Clone target
    ├── decision-transformers/ # Clone target
    └── mcp/                  # Clone target
```

---

*Document created December 31, 2025*
*Ready for RAG ingestion pipeline*
