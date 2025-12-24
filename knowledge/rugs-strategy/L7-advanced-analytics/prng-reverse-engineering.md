---
layer: 7
domain: advanced-analytics/prng-reverse
priority: P2
bot_relevant: false
validation_tier: theoretical
source_file: "RAG SUPERPACK/review data/prng_reverse_engineering_plan.md"
cross_refs:
  - L1-game-mechanics/provably-fair.md
  - L7-advanced-analytics/prng-analysis.md
  - L7-advanced-analytics/bayesian-models.md
last_validated: 2025-12-24
status: "RESEARCH-REFERENCE"
---

# Comprehensive PRNG Reverse Engineering Framework

**Note:** This is a research reference document containing statistical testing methodologies and analysis frameworks. The code examples are for analytical purposes only.

## 1. Analysis of System Architecture

Based on analysis of three Rugs.fun verification versions and ML_CORE project findings:

**Surface Layer**
- Provably fair cryptographic system using SHA-256 hash verification
- Server seed + game ID deterministically generates outcomes
- Publicly verifiable algorithm with version differences (v1, v2, v3)

**Technical Differences Between Versions**
- V1: Simple volatility calculation (`0.005 * Math.sqrt(price)`)
- V2: Capped volatility (`0.005 * Math.min(10, Math.sqrt(price))`)
- V3: God Candle feature (0.001% chance, 10x price move)

## 2. Statistical Testing Framework

### 2.1 Test Suite Selection

| Test Suite | Strengths | Implementation |
|------------|-----------|----------------|
| **NIST STS** | Comprehensive statistical tests | Bitstream analysis of server seeds |
| **Dieharder** | Extensive battery, command-line friendly | Stream-based analysis of game outcomes |
| **TestU01** | Catches unique biases | Integration with custom generators |
| **Custom Tests** | Domain-specific pattern detection | Python correlation analysis |

### 2.2 Data Collection Requirements

Minimum sample size requirements for conclusive testing:

- **Statistical Randomness**: 10,000+ game outcomes
- **Pattern Detection**: 8,192+ sequential games (power of 2 for FFT)
- **Meta-algorithm Detection**: 2,000+ games with complete metadata
- **Time-based Seeding**: 1,000+ games with precise timestamps

### 2.3 Core Statistical Tests

**Chi-Squared Test**: Test for uniform distribution
```python
# Observed vs expected frequency distribution
chi2_stat, p_value = chisquare(observed)
# p_value > 0.05 indicates randomness
```

**Runs Test**: Detect sequential dependencies
```python
# Count runs above/below median
# Compare to expected runs under randomness
z_score = (runs - expected_runs) / sqrt(var_runs)
```

**Autocorrelation Analysis**: Detect periodic patterns
```python
# Find significant lags
confidence_interval = 1.96 / sqrt(n)  # 95% CI
significant_lags = [i for i, corr in enumerate(autocorr) if abs(corr) > confidence_interval]
```

**Spectral Analysis (FFT)**: Find hidden periodicities
```python
# Compute power spectrum
power_spectrum = np.abs(fft(values)) ** 2
# Find peaks above 3 standard deviations
```

## 3. Real-Time Monitoring Framework

### 3.1 Key Game Events to Capture

- `gameStateUpdate`: Game state, tick, price, phase
- `gameHistory`: Historical game outcomes
- `newTrade`: Player trading activity

### 3.2 Metrics to Calculate

- Peak multiplier per game
- Final tick (game duration)
- Instarug detection (finalTick < 10)
- Cross-game correlation
- Time-based patterns

## 4. Advanced PRNG Analysis Techniques

### 4.1 Seed Generation Investigation

- Analyze entropy distribution in server seeds
- Test for time-based generation patterns
- Check common hash algorithms (MD5, SHA1, SHA256)

### 4.2 ML-Based Pattern Detection

- LSTM models for sequence prediction
- Feature engineering from game history
- Anomaly detection for pattern changes

## 5. Implementation Plan

### Phase 1: Data Collection (1-2 weeks)
- Set up WebSocket connection
- Collect 10,000+ game outcomes
- Store in structured format (JSONL)

### Phase 2: Basic Statistical Analysis (1 week)
- Run core statistical tests
- Analyze distribution of outcomes
- Validate basic randomness properties

### Phase 3: Meta-Algorithm Investigation (2 weeks)
- Cross-game correlation analysis
- Time-based pattern detection
- Player profiling effects

### Phase 4: Predictive Modeling (2-3 weeks)
- Train pattern detection models
- Implement real-time prediction
- Evaluate accuracy

### Phase 5: Strategy Development (1-2 weeks)
- Develop trading strategies
- Implement risk management
- Back-test on historical data

---

## For Bot Development

**This document is for research reference only.**

**Relevant Findings for Bot**:
- Version differences in volatility calculation
- Statistical test thresholds for pattern detection
- Data collection requirements for analysis

**Integration Points**:
- Data collection infrastructure
- Statistical validation of strategies
- Pattern detection for risk management

---

*Last updated: December 24, 2025 | Migrated to rugs-strategy knowledge base*
