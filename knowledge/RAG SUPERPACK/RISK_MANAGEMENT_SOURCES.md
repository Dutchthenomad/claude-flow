# Risk Management & Position Sizing Knowledge Sources

**Created**: December 31, 2025
**Purpose**: Advanced risk management, position sizing, and drawdown control for trading bots
**Status**: READY FOR INGESTION

---

## Layer 1: Position Sizing Methods

### Kelly Criterion
- **Theory**: Maximizes geometric growth rate of capital
- **Formula**: `K% = W - (1-W)/R` where W=win rate, R=win/loss ratio
- **Best Practice**: Use fractional Kelly (0.25-0.5x) to reduce volatility
- **Sources**:
  - [PyQuant News - Kelly Criterion](https://www.pyquantnews.com/the-pyquant-newsletter/use-kelly-criterion-optimal-position-sizing)
  - [QuantConnect Research](https://www.quantconnect.com/research/18312/kelly-criterion-applications-in-trading-systems/)
  - [Raposa - Kelly Optimization](https://raposa.trade/blog/optimize-your-trading-strategy-with-python-and-the-kelly-criterion/)

### Optimal F (Ralph Vince)
- **Theory**: Iterative optimization beyond Kelly for actual trade distributions
- **Formula**: Find f that maximizes TWR (Terminal Wealth Relative)
- **Caveat**: Often produces insane allocations (98%+), must be constrained
- **Sources**:
  - [Quant Fiction - Beyond Kelly](https://quantfiction.com/2018/05/06/position-sizing-for-practitioners-part-1-beyond-kelly/)
  - [George Pruitt - Optimal F](https://georgepruitt.com/calculating-position-size-with-optimal-f/)
  - [QuantifiedStrategies - Optimal F](https://www.quantifiedstrategies.com/optimal-f-money-management/)
- **Book**: Ralph Vince - "Portfolio Management Formulas"

### Other Methods
| Method | Use Case | Risk Profile |
|--------|----------|--------------|
| Fixed Fractional | Conservative, consistent | Low |
| Volatility-Based | Adapts to market conditions | Medium |
| Kelly/Optimal F | Maximum growth (theoretical) | High |
| CPPI | Capital protection priority | Low-Medium |
| Anti-Martingale | Increase after wins | Medium |

---

## Layer 2: Portfolio Optimization Libraries

### Riskfolio-Lib (PRIMARY RECOMMENDATION)
- **URL**: https://github.com/dcajasn/Riskfolio-Lib
- **Clone**: `git clone https://github.com/dcajasn/Riskfolio-Lib.git`
- **Features**:
  - 24 convex risk measures
  - Black-Litterman, Risk Factors, Bayesian models
  - Hierarchical Risk Parity (HRP)
  - HERC with 35 risk measures
  - Nested Clustered Optimization (NCO)
- **RAG Priority**: HIGH

### PyPortfolioOpt
- **URL**: https://github.com/PyPortfolio/PyPortfolioOpt
- **Clone**: `git clone https://github.com/PyPortfolio/PyPortfolioOpt.git`
- **Features**:
  - Mean-variance optimization
  - Black-Litterman allocation
  - Hierarchical Risk Parity
  - Modular architecture
- **RAG Priority**: HIGH

### skfolio (New 2025)
- **URL**: https://github.com/skfolio/skfolio
- **Clone**: `git clone https://github.com/skfolio/skfolio.git`
- **Features**:
  - scikit-learn compatible API
  - Cross-validation for financial time series
  - State-of-the-art estimators
- **RAG Priority**: MEDIUM

### QuantLib
- **URL**: https://github.com/lballabio/QuantLib
- **Clone**: `git clone https://github.com/lballabio/QuantLib.git`
- **Features**:
  - Industry-standard pricing library
  - Derivatives, fixed income, FX
  - Risk metrics (VaR, Greeks)
- **RAG Priority**: MEDIUM (large codebase)

---

## Layer 3: Risk Metrics & Analysis

### Risk of Ruin / Monte Carlo
- **mc_sim_fin**: https://github.com/gaugau3000/mc_sim_fin
  - Monte Carlo equity simulator
  - Risk of ruin probability
  - Maximum drawdown distribution
  - 10,000 iteration default
- **Medium Article**: [Risk of Ruin in Trading](https://medium.com/@rgaveiga/risk-of-ruin-in-trading-1-a81fd4cd066d)
  - Python Monte Carlo implementation
  - Shows 21% ruin risk even with edge

### VaR/CVaR Implementation
- **Financial-Risk-Management**: https://github.com/BrunoWan/Financial-Risk-Management
  - VaR calculations
  - Monte Carlo simulation
- **Computational-Finance**: https://github.com/andreachello/Computational-Finance
  - Monte Carlo Methods notebook
  - Historical vs parametric VaR

### QuantStats
- **URL**: https://github.com/ranaroussi/quantstats
- **Clone**: `git clone https://github.com/ranaroussi/quantstats.git`
- **Features**:
  - Portfolio analytics
  - Risk metrics (Sharpe, Sortino, Calmar)
  - Drawdown analysis
  - Tear sheets
- **RAG Priority**: HIGH

---

## Layer 4: Backtesting Frameworks

### VectorBT (Fastest)
- **URL**: https://github.com/polakowo/vectorbt
- **Clone**: `git clone https://github.com/polakowo/vectorbt.git`
- **Features**:
  - Vectorized backtesting (NumPy/Numba)
  - Trailing stops, position sizing
  - Portfolio-level strategies
  - Jupyter notebook native
- **Speed**: 100x+ faster than event-driven
- **RAG Priority**: HIGH

### Backtrader (Most Accessible)
- **URL**: https://github.com/mementum/backtrader
- **Clone**: `git clone https://github.com/mementum/backtrader.git`
- **Features**:
  - Event-driven architecture
  - Live trading (IB, Alpaca, Oanda)
  - Multi-timeframe support
  - Great documentation
- **RAG Priority**: MEDIUM

### Zipline-Reloaded
- **URL**: https://github.com/stefan-jansen/zipline-reloaded
- **Clone**: `git clone https://github.com/stefan-jansen/zipline-reloaded.git`
- **Features**:
  - Original Quantopian engine
  - Factor-based research
  - scikit-learn integration
- **RAG Priority**: MEDIUM

### NautilusTrader (Production-Grade)
- **URL**: https://github.com/nautechsystems/nautilus_trader
- **Clone**: `git clone https://github.com/nautechsystems/nautilus_trader.git`
- **Features**:
  - High-performance (Rust core)
  - Built-in risk controls
  - Live + backtest same code
  - Position management system
- **RAG Priority**: HIGH (production focus)

---

## Layer 5: Curated Resource Lists

### awesome-quant (23.5k stars)
- **URL**: https://github.com/wilsonfreitas/awesome-quant
- **Clone**: `git clone https://github.com/wilsonfreitas/awesome-quant.git`
- **Content**:
  - 200+ Python libraries catalogued
  - Backtesting, risk, ML, data
  - Books, courses, papers
- **RAG Priority**: HIGH (index to everything)

### Microsoft Qlib
- **URL**: https://github.com/microsoft/qlib
- **Clone**: `git clone https://github.com/microsoft/qlib.git`
- **Features**:
  - Full ML pipeline
  - Alpha seeking → Risk modeling → Portfolio optimization → Execution
  - State-of-the-art research
- **RAG Priority**: HIGH

---

## Key Formulas & Concepts

### Position Sizing

```python
# Kelly Criterion
def kelly_fraction(win_rate, win_loss_ratio):
    """Calculate Kelly fraction for position sizing."""
    return win_rate - (1 - win_rate) / win_loss_ratio

# Fractional Kelly (safer)
def safe_kelly(win_rate, win_loss_ratio, fraction=0.25):
    """Use 25% Kelly for reduced volatility."""
    return kelly_fraction(win_rate, win_loss_ratio) * fraction

# Volatility-based sizing
def volatility_position_size(capital, risk_pct, atr, atr_multiplier=2):
    """Position size based on ATR."""
    dollar_risk = capital * risk_pct
    stop_distance = atr * atr_multiplier
    return dollar_risk / stop_distance
```

### Risk Metrics

```python
# Maximum Drawdown
def max_drawdown(equity_curve):
    """Calculate maximum drawdown from equity curve."""
    peak = equity_curve.expanding().max()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()

# Risk of Ruin (simplified)
def risk_of_ruin(win_rate, risk_per_trade, num_trades=1000):
    """Monte Carlo risk of ruin estimation."""
    import numpy as np
    ruin_count = 0
    for _ in range(10000):
        equity = 1.0
        for _ in range(num_trades):
            if np.random.random() < win_rate:
                equity *= (1 + risk_per_trade)
            else:
                equity *= (1 - risk_per_trade)
            if equity <= 0:
                ruin_count += 1
                break
    return ruin_count / 10000

# Sharpe Ratio
def sharpe_ratio(returns, risk_free_rate=0.0):
    """Calculate annualized Sharpe ratio."""
    excess_returns = returns - risk_free_rate
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
```

### Drawdown Control

```python
# Dynamic position sizing based on drawdown
def drawdown_adjusted_size(base_size, current_dd, max_dd_threshold=0.10):
    """Reduce position size as drawdown increases."""
    if current_dd > max_dd_threshold:
        reduction = (current_dd - max_dd_threshold) / max_dd_threshold
        return base_size * max(0.1, 1 - reduction)
    return base_size

# Circuit breaker
def should_halt_trading(current_dd, daily_loss, max_dd=0.15, max_daily=0.03):
    """Stop trading if risk limits exceeded."""
    return current_dd > max_dd or daily_loss > max_daily
```

---

## Books to Reference (Not Cloneable)

| Title | Author | Focus |
|-------|--------|-------|
| Portfolio Management Formulas | Ralph Vince | Optimal f, position sizing |
| The Mathematics of Money Management | Ralph Vince | Advanced money management |
| Quantitative Trading | Ernest Chan | Practical quant strategies |
| Algorithmic Trading | Ernest Chan | Backtesting, execution |
| Active Portfolio Management | Grinold & Kahn | Factor models, risk |
| Dynamic Hedging | Nassim Taleb | Options, risk management |

---

## Clone Script Addition

```bash
#!/bin/bash
# Risk Management & Position Sizing repos

cd "/home/nomad/Desktop/claude-flow/knowledge/RAG SUPERPACK"

mkdir -p risk-management && cd risk-management

# Portfolio Optimization
[ ! -d "Riskfolio-Lib" ] && git clone --depth 1 https://github.com/dcajasn/Riskfolio-Lib.git
[ ! -d "PyPortfolioOpt" ] && git clone --depth 1 https://github.com/PyPortfolio/PyPortfolioOpt.git
[ ! -d "skfolio" ] && git clone --depth 1 https://github.com/skfolio/skfolio.git

# Risk Metrics
[ ! -d "quantstats" ] && git clone --depth 1 https://github.com/ranaroussi/quantstats.git
[ ! -d "mc_sim_fin" ] && git clone --depth 1 https://github.com/gaugau3000/mc_sim_fin.git

# Backtesting
[ ! -d "vectorbt" ] && git clone --depth 1 https://github.com/polakowo/vectorbt.git
[ ! -d "backtrader" ] && git clone --depth 1 https://github.com/mementum/backtrader.git
[ ! -d "nautilus_trader" ] && git clone --depth 1 https://github.com/nautechsystems/nautilus_trader.git

# Curated Lists
[ ! -d "awesome-quant" ] && git clone --depth 1 https://github.com/wilsonfreitas/awesome-quant.git
[ ! -d "qlib" ] && git clone --depth 1 https://github.com/microsoft/qlib.git

cd ..
echo "Risk management repos cloned!"
```

---

## Integration with Rugs.fun Bot

For your specific use case (sidebet timing, rug avoidance):

### Recommended Position Sizing
```python
# Given your empirical data:
# - 38.1% win rate
# - 754% ROI on wins
# - Martingale recovery 100% success

# Kelly calculation
win_rate = 0.381
avg_win = 7.54  # 754% ROI
avg_loss = 1.0

kelly_f = win_rate - (1 - win_rate) / (avg_win / avg_loss)
# kelly_f ≈ 0.30 (30% of bankroll per bet)

# Use quarter Kelly for safety
safe_bet = kelly_f * 0.25  # 7.5% per bet
```

### Drawdown Limits
```python
# Based on your temporal risk model:
DRAWDOWN_LIMITS = {
    'warning': 0.05,      # 5% - reduce size
    'caution': 0.10,      # 10% - half size
    'halt': 0.15,         # 15% - stop trading
}

# Per your 69-tick safe window:
MAX_HOLD_TICKS = 69      # Before caution zone
CRITICAL_TICKS = 138     # Median rug point
```

---

*Document created December 31, 2025*
*Ready for RAG ingestion pipeline*

## Sources

- [PyQuant News - Kelly Criterion](https://www.pyquantnews.com/the-pyquant-newsletter/use-kelly-criterion-optimal-position-sizing)
- [QuantConnect - Kelly Applications](https://www.quantconnect.com/research/18312/kelly-criterion-applications-in-trading-systems/)
- [awesome-quant](https://github.com/wilsonfreitas/awesome-quant)
- [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib)
- [VectorBT Comparison](https://medium.com/@trading.dude/battle-tested-backtesters-comparing-vectorbt-zipline-and-backtrader-for-financial-strategy-dee33d33a9e0)
- [Risk of Ruin](https://medium.com/@rgaveiga/risk-of-ruin-in-trading-1-a81fd4cd066d)
