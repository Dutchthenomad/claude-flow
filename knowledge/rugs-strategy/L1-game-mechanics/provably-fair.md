---
layer: 1
domain: game-mechanics/provably-fair
priority: P1
bot_relevant: true
validation_tier: canonical
source_file: "RAG SUPERPACK/PROVABLY_FAIR_VERIFICATION.md"
cross_refs:
  - L1-game-mechanics/WHAT-IT-IS-NOT.md
  - L7-advanced-analytics/prng-reverse-engineering.md
last_validated: 2025-12-24
---

# Provably Fair Verification - rugs.fun

**Source**: rugs.fun verification page
**Captured**: December 18, 2025
**Version**: v3

---

## How Provably Fair Works

Rugs.fun uses a provably fair system to ensure game outcomes cannot be manipulated:

1. **Before each game**: The server generates a random server seed and publishes only its hash (the server seed hash).
2. **During the game**: The outcome is determined by combining the server seed with the game ID.
3. **After the game ends**: The server reveals the original server seed.
4. **Verification process**:
   - First, verify that the revealed server seed matches the pre-published hash using SHA-256
   - Second, independently calculate the game outcome using the revealed server seed and game ID
   - If both checks pass, this proves the game outcome was predetermined and not manipulated

### Why Wait for the Server Seed?

The server keeps the actual server seed secret during the game and only reveals it after the game ends. This prevents anyone (including the operator) from knowing the outcome in advance, while still allowing for verification afterward.

---

## Example Verification

| Field | Value |
|-------|-------|
| **Server Seed** | `6500cdbe92a642aac84b178756ceea75665fd5f82ced512ecadb30fefed15755` |
| **Server Seed Hash** | `961079f9f7ebb139fe1c89d74bb16d0b606776c508b1b75c428ff39b077d7a8a` |
| **Game ID** | `20251218-831db215e62e461e` |
| **Hash Verification** | VERIFIED - The hash matches the server seed |
| **Peak Multiplier** | 3.3201x |
| **Game Outcome** | Rugged |

---

## Game Parameters (v3)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `RUG_PROB` | 0.005 | 0.5% chance per tick to rug |
| `DRIFT_MIN` | -0.02 | Minimum price drift per tick |
| `DRIFT_MAX` | 0.03 | Maximum price drift per tick |
| `BIG_MOVE_CHANCE` | 0.125 | 12.5% chance of big move |
| `BIG_MOVE_MIN` | 0.15 | Minimum big move size |
| `BIG_MOVE_MAX` | 0.25 | Maximum big move size |
| `GOD_CANDLE_CHANCE` | 0.00001 | 0.001% chance of god candle |
| `GOD_CANDLE_MOVE` | 10.0 | 10x multiplier on god candle |

---

## Source Code

The verification algorithm matches exactly what's used on the server:

### Price Drift Calculation

```javascript
function driftPrice(
    price,
    DRIFT_MIN,
    DRIFT_MAX,
    BIG_MOVE_CHANCE,
    BIG_MOVE_MIN,
    BIG_MOVE_MAX,
    randFn,
    version = 'v3',
    GOD_CANDLE_CHANCE = 0.00001,
    GOD_CANDLE_MOVE = 10.0,
    STARTING_PRICE = 1.0
) {
    // v3 adds God Candle feature - rare massive price increase
    if (version === 'v3' && randFn() < GOD_CANDLE_CHANCE && price <= 100 * STARTING_PRICE) {
        return price * GOD_CANDLE_MOVE;
    }

    let change = 0;

    if (randFn() < BIG_MOVE_CHANCE) {
        const moveSize = BIG_MOVE_MIN + randFn() * (BIG_MOVE_MAX - BIG_MOVE_MIN);
        change = randFn() > 0.5 ? moveSize : -moveSize;
    } else {
        const drift = DRIFT_MIN + randFn() * (DRIFT_MAX - DRIFT_MIN);

        // Version difference is in this volatility calculation
        const volatility = version === 'v1'
            ? 0.005 * Math.sqrt(price)
            : 0.005 * Math.min(10, Math.sqrt(price));

        change = drift + (volatility * (2 * randFn() - 1));
    }

    let newPrice = price * (1 + change);

    if (newPrice < 0) {
        newPrice = 0;
    }

    return newPrice;
}
```

### Game Verification Function

```javascript
function verifyGame(serverSeed, gameId, version = 'v3') {
    const combinedSeed = serverSeed + '-' + gameId;
    const prng = new Math.seedrandom(combinedSeed);

    let price = 1.0;
    let peakMultiplier = 1.0;
    let rugged = false;

    for (let tick = 0; tick < 5000 && !rugged; tick++) {
        if (prng() < RUG_PROB) {
            rugged = true;
            continue;
        }

        const newPrice = driftPrice(
            price,
            DRIFT_MIN,
            DRIFT_MAX,
            BIG_MOVE_CHANCE,
            BIG_MOVE_MIN,
            BIG_MOVE_MAX,
            prng.bind(prng),
            version
        );

        price = newPrice;

        if (price > peakMultiplier) {
            peakMultiplier = price;
        }
    }

    return {
        peakMultiplier: peakMultiplier,
        rugged: rugged
    };
}
```

---

## Key Insights for ML/RL

1. **Rug is purely random**: 0.5% per tick, independent of price or history
2. **God Candle requires price <= 100x**: Won't trigger at high multipliers
3. **Volatility is capped in v3**: `Math.min(10, Math.sqrt(price))` prevents extreme swings at high prices
4. **Max ticks**: 5000 (game auto-rugs if not rugged naturally)
5. **PRNG is deterministic**: Given seed + gameId, outcome is fully reproducible

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
