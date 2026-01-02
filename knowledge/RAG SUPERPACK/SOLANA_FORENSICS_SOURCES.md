# Solana Blockchain & Forensics Knowledge Sources

**Created**: December 31, 2025
**Purpose**: Solana programs, transaction analysis, reverse engineering, and blockchain forensics for rugs.fun investigation
**Status**: READY FOR INGESTION

---

## Strategic Objective

Enable reverse engineering of rugs.fun game mechanics by:
1. Understanding Solana program architecture
2. Parsing and analyzing on-chain transactions
3. Correlating transaction data with PRNG verification (serverSeed/serverSeedHash)
4. Identifying the master program through transaction forensics
5. Cross-referencing Bayesian statistical models with on-chain behavior

---

## Layer 1: Solana Core Development

### Official Documentation
- **Solana Docs**: https://solana.com/docs
- **Programs Guide**: https://solana.com/docs/core/programs
- **Rust Development**: https://solana.com/docs/programs/rust
- **Developer Portal**: https://solana.com/developers
- **Courses**: https://solana.com/developers/courses

### Anchor Framework (Primary Framework)
- **URL**: https://www.anchor-lang.com/docs
- **Clone**: `git clone https://github.com/coral-xyz/anchor.git`
- **Purpose**: Most Solana programs use Anchor; its IDL files are key to decoding instructions
- **Key Concept**: IDL = Solana's equivalent of Ethereum's ABI
- **RAG Priority**: HIGH

### solana-labs/solana (Reference Implementation)
- **URL**: https://github.com/solana-labs/solana
- **Clone**: `git clone --depth 1 https://github.com/solana-labs/solana.git`
- **Content**: Validator, runtime, SDK, CLI tools
- **RAG Priority**: MEDIUM (large repo, selective ingestion)

---

## Layer 2: Python SDKs for Solana

### solana-py (Primary Python SDK)
- **URL**: https://github.com/michaelhly/solana-py
- **Clone**: `git clone https://github.com/michaelhly/solana-py.git`
- **Install**: `pip install solana`
- **Features**:
  - JSON RPC API interaction
  - Transaction building and signing
  - SPL Token Program support
  - Uses solders under the hood
- **RAG Priority**: HIGH

### solders (High-Performance Rust-Python Toolkit)
- **URL**: https://github.com/kevinheavey/solders
- **Clone**: `git clone https://github.com/kevinheavey/solders.git`
- **Install**: `pip install solders`
- **Features**:
  - Keypairs, pubkeys, signing
  - Transaction serialization/deserialization
  - Message parsing
  - Written in Rust for performance
- **Docs**: https://kevinheavey.github.io/solders/
- **RAG Priority**: HIGH

### AnchorPy (IDL Client Generator)
- **URL**: https://github.com/kevinheavey/anchorpy
- **Clone**: `git clone https://github.com/kevinheavey/anchorpy.git`
- **Install**: `pip install anchorpy`
- **Features**:
  - Generate Python clients from Anchor IDL
  - Decode program instructions
  - Fetch and serialize accounts
  - Fully typed
- **Command**: `anchorpy client-gen <idl.json> <output_dir>`
- **RAG Priority**: HIGH (critical for decoding rugs.fun)

---

## Layer 3: Reverse Engineering Tools

### Sol-azy (FuzzingLabs)
- **URL**: https://github.com/FuzzingLabs/sol-azy
- **Clone**: `git clone https://github.com/FuzzingLabs/sol-azy.git`
- **Features**:
  - Disassemble Solana BPF bytecode
  - Control flow graph (CFG) generation
  - Fetch on-chain program bytecode by program ID
  - Works with Anchor and native SBF programs
- **Docs**: https://fuzzinglabs.github.io/sol-azy/reverse.html
- **RAG Priority**: HIGH

### Binary Ninja Plugin (bn-ebpf-solana)
- **URL**: https://github.com/anagrambuild/bn-ebpf-solana
- **Purpose**: Blackbox Solana program analysis
- **Features**:
  - Understands Solana ELF format
  - Solana-specific relocations
  - LLIL lifting for EBPF instructions
- **Article**: [Reverse Engineering Solana with Binary Ninja](https://osec.io/blog/2022-08-27-reverse-engineering-solana/)
- **RAG Priority**: MEDIUM

### Solana Data Reverser
- **URL**: https://github.com/accretion-xyz/solana-data-reverser
- **Clone**: `git clone https://github.com/accretion-xyz/solana-data-reverser.git`
- **Features**:
  - Browser-based hex data analysis
  - Deep Solana blockchain integration
  - Account structure examination
  - Pattern discovery in blockchain data
- **RAG Priority**: MEDIUM

---

## Layer 4: Transaction Analysis Tools

### deBridge Solana Transaction Parser
- **URL**: https://github.com/debridge-finance/solana-tx-parser-public
- **Clone**: `git clone https://github.com/debridge-finance/solana-tx-parser-public.git`
- **Language**: TypeScript
- **Features**:
  - Decode arbitrary Solana instructions
  - IDL-based or custom parsing
  - Handles multiple transaction formats
- **RAG Priority**: MEDIUM

### tkhq/solana-parser
- **URL**: https://github.com/tkhq/solana-parser
- **Clone**: `git clone https://github.com/tkhq/solana-parser.git`
- **Features**:
  - Primitive-level transaction inspection
  - Message and signature parsing
- **RAG Priority**: MEDIUM

### Solana Transaction Analyzer (Python)
- **URL**: https://github.com/faradaysage/Solana-Transaction-Analyzer
- **Clone**: `git clone https://github.com/faradaysage/Solana-Transaction-Analyzer.git`
- **Features**:
  - Helius API integration
  - Token transaction classification
  - SOL spent/received tracking
  - CSV report generation
- **RAG Priority**: HIGH (Python-based)

### Solana Bundler Detector
- **URL**: https://github.com/nothingdao/solana-bundler-detector
- **Clone**: `git clone https://github.com/nothingdao/solana-bundler-detector.git`
- **Features**:
  - Detect coordinated buying patterns
  - Suspicious time window analysis
  - Extensible architecture
- **RAG Priority**: MEDIUM (useful for bot detection)

---

## Layer 5: Blockchain Forensics

### On-Chain Investigations Tools List
- **URL**: https://github.com/OffcierCia/On-Chain-Investigations-Tools-List
- **Clone**: `git clone https://github.com/OffcierCia/On-Chain-Investigations-Tools-List.git`
- **Content**: Comprehensive list of investigation tools and manuals
- **RAG Priority**: HIGH (meta-index)

### GraphSense (Open-Source Analytics)
- **URL**: https://github.com/graphsense
- **Features**:
  - Open-source blockchain analytics
  - Web interface + API
  - Address clustering
  - Transaction tracing
- **RAG Priority**: MEDIUM

### Python Forensics Libraries
```python
# Essential libraries for blockchain forensics
pip install requests           # API calls
pip install beautifulsoup4     # HTML parsing
pip install web3              # Ethereum (reference)
pip install solana            # Solana RPC
pip install solders           # Solana primitives
pip install anchorpy          # IDL decoding
pip install python-dotenv     # Credential management
pip install matplotlib        # Visualization
pip install networkx          # Graph analysis
```

---

## Layer 6: Provably Fair / PRNG Verification

### How Provably Fair Works

```
1. Server generates serverSeed (secret)
2. Server publishes SHA256(serverSeed) = serverSeedHash (public)
3. Player provides clientSeed (optional)
4. Game runs using combined seeds
5. After game, server reveals serverSeed
6. Anyone can verify: SHA256(serverSeed) == serverSeedHash
```

### Verification Implementation

```python
import hashlib

def verify_server_seed(server_seed: str, server_seed_hash: str) -> bool:
    """Verify that serverSeed hashes to serverSeedHash."""
    computed_hash = hashlib.sha256(server_seed.encode()).hexdigest()
    return computed_hash == server_seed_hash

def compute_game_outcome(server_seed: str, client_seed: str, nonce: int) -> str:
    """Compute HMAC-SHA256 for game outcome."""
    import hmac
    message = f"{client_seed}:{nonce}"
    return hmac.new(
        server_seed.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
```

### Solana VRF (Verifiable Random Functions)
- **Guide**: https://solana.com/developers/courses/connecting-to-offchain-data/verifiable-randomness-functions
- **Purpose**: On-chain verifiable randomness
- **Providers**: Switchboard, Chainlink VRF
- **Note**: rugs.fun may use custom PRNG, not standard VRF

### Provably Fair Reference Implementations
- **URL**: https://github.com/provably-fair/provably-fair-app
- **Clone**: `git clone https://github.com/provably-fair/provably-fair-app.git`
- **Features**: Verification tools for casino games

---

## Layer 7: Rugs.fun Investigation Strategy

### Phase 1: Program Discovery

```python
# Find the rugs.fun program ID by analyzing known transactions
from solana.rpc.api import Client
from solders.pubkey import Pubkey

client = Client("https://api.mainnet-beta.solana.com")

# Get recent transactions for a known rugs.fun wallet
def get_program_ids_from_wallet(wallet_pubkey: str, limit: int = 100):
    """Extract unique program IDs from wallet transactions."""
    pubkey = Pubkey.from_string(wallet_pubkey)
    signatures = client.get_signatures_for_address(pubkey, limit=limit)

    program_ids = set()
    for sig in signatures.value:
        tx = client.get_transaction(sig.signature, encoding="jsonParsed")
        if tx.value:
            for instruction in tx.value.transaction.message.instructions:
                program_ids.add(str(instruction.program_id))

    return program_ids
```

### Phase 2: IDL Extraction (if Anchor-based)

```bash
# If program is Anchor-based, try to fetch IDL
anchor idl fetch <PROGRAM_ID> --provider.cluster mainnet

# Or use anchorpy
anchorpy fetch-idl <PROGRAM_ID> -o rugs_idl.json
```

### Phase 3: Transaction Pattern Analysis

```python
# Correlate on-chain transactions with gameStateUpdate events
def correlate_transactions_with_games(
    game_history: list,
    transactions: list
) -> dict:
    """
    Match on-chain transactions to gameHistory entries.

    Look for:
    - Timing correlation (game timestamp vs tx timestamp)
    - Amount correlation (sidebet amounts vs tx amounts)
    - Account correlation (player wallets)
    """
    correlations = {}

    for game in game_history:
        game_time = game['timestamp']
        game_id = game['id']

        # Find transactions within time window
        matching_txs = [
            tx for tx in transactions
            if abs(tx['blockTime'] * 1000 - game_time) < 5000  # 5 second window
        ]

        if matching_txs:
            correlations[game_id] = matching_txs

    return correlations
```

### Phase 4: PRNG Reverse Engineering

```python
# Attempt to understand PRNG from transaction data
def analyze_prng_pattern(games: list) -> dict:
    """
    Analyze PRNG patterns from serverSeed/serverSeedHash pairs.

    Look for:
    - Sequential patterns in seeds
    - Correlation with on-chain randomness sources
    - Timing patterns between games
    """
    analysis = {
        'seed_length': set(),
        'hash_matches': 0,
        'sequential_patterns': [],
    }

    for i, game in enumerate(games):
        pf = game.get('provablyFair', {})
        seed = pf.get('serverSeed')
        hash_ = pf.get('serverSeedHash')

        if seed and hash_:
            # Verify hash
            if verify_server_seed(seed, hash_):
                analysis['hash_matches'] += 1

            analysis['seed_length'].add(len(seed))

            # Check for sequential patterns
            if i > 0:
                prev_seed = games[i-1].get('provablyFair', {}).get('serverSeed')
                if prev_seed:
                    # Compute similarity, edit distance, etc.
                    pass

    return analysis
```

### Phase 5: Bayesian Cross-Correlation

```python
# Integrate with Bayesian analysis
import pymc as pm
import numpy as np

def bayesian_rug_timing_model(
    games: list,
    on_chain_data: list
) -> pm.Model:
    """
    Build Bayesian model correlating:
    - Game duration (from prices[])
    - Sidebet activity (from globalSidebets[])
    - On-chain transaction timing
    - PRNG seed patterns
    """

    durations = np.array([len(g['prices']) for g in games])

    with pm.Model() as model:
        # Prior: game duration distribution
        mu = pm.Normal('mu', mu=100, sigma=50)
        sigma = pm.HalfNormal('sigma', sigma=30)

        # Likelihood
        duration = pm.Normal('duration', mu=mu, sigma=sigma, observed=durations)

        # Could add:
        # - Transaction timing as covariate
        # - PRNG seed entropy as feature
        # - Sidebet volume correlations

    return model
```

---

## Clone Script

```bash
#!/bin/bash
# Clone Solana & Blockchain Forensics repos

cd "/home/nomad/Desktop/claude-flow/knowledge/RAG SUPERPACK"

echo "=== Cloning Solana & Forensics Sources ==="

mkdir -p solana && cd solana

echo "[1/4] Solana Core & Anchor..."
[ ! -d "anchor" ] && git clone --depth 1 https://github.com/coral-xyz/anchor.git
[ ! -d "solana" ] && git clone --depth 1 https://github.com/solana-labs/solana.git

echo "[2/4] Python SDKs..."
[ ! -d "solana-py" ] && git clone --depth 1 https://github.com/michaelhly/solana-py.git
[ ! -d "solders" ] && git clone --depth 1 https://github.com/kevinheavey/solders.git
[ ! -d "anchorpy" ] && git clone --depth 1 https://github.com/kevinheavey/anchorpy.git

echo "[3/4] Reverse Engineering..."
[ ! -d "sol-azy" ] && git clone --depth 1 https://github.com/FuzzingLabs/sol-azy.git
[ ! -d "solana-data-reverser" ] && git clone --depth 1 https://github.com/accretion-xyz/solana-data-reverser.git

echo "[4/4] Transaction Analysis..."
[ ! -d "Solana-Transaction-Analyzer" ] && git clone --depth 1 https://github.com/faradaysage/Solana-Transaction-Analyzer.git
[ ! -d "solana-bundler-detector" ] && git clone --depth 1 https://github.com/nothingdao/solana-bundler-detector.git
[ ! -d "solana-tx-parser-public" ] && git clone --depth 1 https://github.com/debridge-finance/solana-tx-parser-public.git

cd ..

mkdir -p forensics && cd forensics

echo "[BONUS] Forensics Tools..."
[ ! -d "On-Chain-Investigations-Tools-List" ] && git clone --depth 1 https://github.com/OffcierCia/On-Chain-Investigations-Tools-List.git
[ ! -d "provably-fair-app" ] && git clone --depth 1 https://github.com/provably-fair/provably-fair-app.git

cd ..

echo ""
echo "=== Solana & Forensics Clone Complete ==="
du -sh solana/ forensics/
```

---

## Integration with Existing Knowledge

```
knowledge/
├── RAG SUPERPACK/
│   ├── rl-core/              # ML/RL algorithms
│   ├── bayesian/             # Statistical inference
│   ├── risk-management/      # Position sizing
│   ├── solana/               # ← NEW: Blockchain layer
│   │   ├── anchor/
│   │   ├── solana-py/
│   │   ├── solders/
│   │   ├── anchorpy/         # Critical for IDL decoding
│   │   ├── sol-azy/          # Reverse engineering
│   │   └── Solana-Transaction-Analyzer/
│   └── forensics/            # ← NEW: Investigation tools
│       ├── On-Chain-Investigations-Tools-List/
│       └── provably-fair-app/
│
├── rugs-events/              # CANONICAL WebSocket spec
│   └── WEBSOCKET_EVENTS_SPEC.md  # provablyFair fields documented here
│
└── HOLDING-CELL/             # PRE-CANON analysis
    └── gameHistory-*.md      # Contains serverSeed/serverSeedHash observations
```

---

## Investigation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RUGS.FUN INVESTIGATION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. COLLECT DATA                                                │
│     ├── WebSocket: gameStateUpdate events                       │
│     ├── On-chain: Solana transactions (solana-py)               │
│     └── Off-chain: Player behavior patterns                     │
│                                                                 │
│  2. IDENTIFY PROGRAM                                            │
│     ├── Analyze known wallet transactions                       │
│     ├── Extract unique program IDs                              │
│     └── Attempt IDL fetch (anchorpy)                            │
│                                                                 │
│  3. REVERSE ENGINEER                                            │
│     ├── If Anchor: Parse IDL, decode instructions               │
│     ├── If Native: Use sol-azy for disassembly                  │
│     └── Map instruction → game state changes                    │
│                                                                 │
│  4. CORRELATE                                                   │
│     ├── Match on-chain tx timestamps ↔ gameHistory              │
│     ├── Match tx amounts ↔ sidebet amounts                      │
│     ├── Match accounts ↔ player wallets                         │
│     └── Verify PRNG: SHA256(serverSeed) == serverSeedHash       │
│                                                                 │
│  5. MODEL                                                       │
│     ├── Bayesian inference on rug timing                        │
│     ├── Statistical patterns in PRNG outputs                    │
│     └── Cross-validate with RL training results                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Questions to Answer

| Question | Investigation Method |
|----------|---------------------|
| What is the rugs.fun program ID? | Transaction analysis on known wallets |
| Is it Anchor-based? | Try `anchor idl fetch` |
| How is PRNG seeded? | Analyze serverSeed entropy sources |
| Are game outcomes on-chain? | Decode program instructions |
| Can we predict rug timing? | Bayesian model + on-chain correlation |
| Is there manipulation? | Statistical anomaly detection |

---

## Sources

- [Solana Docs](https://solana.com/docs)
- [Anchor Framework](https://www.anchor-lang.com/docs)
- [solana-py](https://github.com/michaelhly/solana-py)
- [solders](https://github.com/kevinheavey/solders)
- [AnchorPy](https://kevinheavey.github.io/anchorpy/)
- [Sol-azy](https://fuzzinglabs.github.io/sol-azy/reverse.html)
- [Reverse Engineering Solana (OTSec)](https://osec.io/blog/2022-08-27-reverse-engineering-solana/)
- [On-Chain Investigations Tools](https://github.com/OffcierCia/On-Chain-Investigations-Tools-List)
- [Provably Fair Implementation (Stake.com)](https://stake.com/provably-fair/implementation)
- [Solana VRF Guide](https://solana.com/developers/courses/connecting-to-offchain-data/verifiable-randomness-functions)

---

*Document created December 31, 2025*
*Ready for RAG ingestion and rugs.fun investigation*
