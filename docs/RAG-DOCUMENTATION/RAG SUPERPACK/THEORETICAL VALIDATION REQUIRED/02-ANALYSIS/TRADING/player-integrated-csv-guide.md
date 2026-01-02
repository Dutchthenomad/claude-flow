# 👥 PLAYER-INTEGRATED CSV DATA GUIDE

**Complete field reference for `player_integrated_data.csv` - Game + Player Analysis**

---

## 🎯 OVERVIEW

This CSV combines **game-level metrics** with **detailed player behavior analysis** for comprehensive PRNG analysis.

**File**: `player_integrated_data.csv`  
**Records**: 100 games  
**Fields**: 37 comprehensive metrics  
**Analysis Level**: Game + Individual Player Integration  

---

## 📋 COMPLETE FIELD REFERENCE

### 🆔 BASIC IDENTIFIERS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| A | `gameId` | Text | Unique game identifier | Game tracking |
| B | `timestamp` | Text | Game start time | Time-based analysis |

### 🎯 CORE GAME METRICS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| C | `duration_ticks` | Number | **Game length in ticks** | **Primary survival analysis** |
| D | `peak_multiplier` | Number | **Highest multiplier reached** | **Peak performance prediction** |
| E | `final_price` | Number | **Last price before rug** | **Exit timing analysis** |
| F | `is_instarug` | Boolean | **TRUE if < 11 ticks** | **Risk categorization** |

### 💹 TRADING OVERVIEW

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| G | `total_trades` | Number | Total trades executed | Activity level |
| H | `unique_players` | Number | Players who participated | Market size |
| I | `buy_orders` | Number | Total buy orders | Market sentiment |
| J | `sell_orders` | Number | Total sell orders | Profit-taking activity |
| K | `buy_sell_ratio` | Number | Buy orders ÷ Sell orders | Market direction |

### 👥 PLAYER ACTIVITY ANALYSIS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| L | `players_actually_trading` | Number | Players who placed trades | Real participation |
| M | `avg_trades_per_player` | Number | Average trades per active player | Trading intensity |
| N | `avg_volume_per_player` | Number | Average volume per active player | Position sizing |
| O | `top_player_volume_ratio` | Number | **Largest player volume ÷ Total** | **Concentration risk** |

### 💰 PLAYER PROFITABILITY METRICS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| P | `profitable_players` | Number | Number of players with profit | Success count |
| Q | `profitable_player_ratio` | Number | **Profitable players ÷ Total** | **Success rate** |
| R | `total_profits` | Number | Sum of all player profits | Market efficiency |
| S | `total_losses` | Number | Sum of all player losses | Market losses |
| T | `profit_loss_ratio` | Number | Total profits ÷ Total losses | Market balance |

### ⏰ PLAYER TIMING BEHAVIOR

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| U | `early_entry_players` | Number | Players entering first 30% | Early adoption |
| V | `late_entry_players` | Number | Players entering last 30% | FOMO behavior |
| W | `early_entry_ratio` | Number | Early players ÷ Total players | Timing distribution |

### 👨‍💼 PLAYER DEMOGRAPHICS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| X | `avg_player_level` | Number | Average player level/rank | Experience factor |
| Y | `high_level_players` | Number | Players with level > 30 | Expert participation |
| Z | `high_level_ratio` | Number | High-level players ÷ Total | Expertise ratio |

### 🎮 TRADING PATTERN CLASSIFICATION

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| AA | `scalpers` | Number | High-frequency, low-volume traders | Pattern analysis |
| AB | `whales` | Number | Low-frequency, high-volume traders | Market impact |
| AC | `hodlers` | Number | Buy-and-hold players (no sells) | Conviction trading |
| AD | `flippers` | Number | Balanced buy/sell traders | Active trading |
| AE | `early_birds` | Number | Early entry players | Timing strategy |
| AF | `late_joiners` | Number | Late entry players | FOMO trading |
| AG | `regular_traders` | Number | Standard trading patterns | Baseline behavior |

### ⚠️ COMPREHENSIVE RISK ASSESSMENT

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| AH | `duration_risk` | Number | Duration-based risk (0-1) | Time risk factor |
| AI | `concentration_risk` | Number | Player concentration risk (0-1) | Whale risk |
| AJ | `activity_risk` | Number | Activity level risk (0-1) | Volume risk |
| AK | `composite_risk_score` | Number | **Weighted combined risk (0-1)** | **Overall assessment** |

---

## 🧮 ADVANCED GOOGLE SHEETS FORMULAS

### Player Behavior Analysis
```excel
=AVERAGE(Q:Q)                    # Average success rate across games
=CORREL(M:M,D:D)                 # Trading intensity vs peak correlation
=AVERAGEIF(O:O,">0.5",AK:AK)     # Risk in whale-dominated games
```

### Player Type Analysis
```excel
=SUM(AB:AB)/SUM(L:L)             # Percentage of whales across all games
=AVERAGEIF(AC:AC,">0",D:D)       # Peak multiplier in games with hodlers
=CORREL(AA:AA,AK:AK)             # Scalper activity vs risk correlation
```

### Profitability Analysis
```excel
=AVERAGEIFS(Q:Q,C:C,">100",F:F,FALSE)  # Success rate in longer, non-instarug games
=SUMPRODUCT(R:R)/SUMPRODUCT(S:S)        # Overall market profit/loss ratio
=CORREL(X:X,Q:Q)                        # Player experience vs success rate
```

### Risk Assessment
```excel
=COUNTIFS(AK:AK,">0.7",Q:Q,"<0.3")     # High-risk, low-success games
=AVERAGEIF(Z:Z,">0.5",AK:AK)           # Risk in expert-heavy games
=CORREL(O:O,AI:AI)                      # Concentration vs concentration risk
```

### Market Dynamics
```excel
=CORREL(W:W,AK:AK)               # Early adoption vs risk
=AVERAGEIF(K:K,">2",D:D)         # Peak multiplier in buy-heavy markets
=COUNTIFS(AG:AG,">5",AK:AK,"<0.5") # Low-risk games with regular traders
```

---

## 📊 SUGGESTED ANALYSIS WORKFLOWS

### 1. Player Success Prediction
```excel
# Identify factors that predict player success
=CORREL(X:X,Q:Q)  # Experience vs success
=CORREL(W:W,Q:Q)  # Early entry vs success
=CORREL(M:M,Q:Q)  # Trading activity vs success
```

### 2. Whale Impact Analysis
```excel
# Analyze market impact of large players
=AVERAGEIF(AB:AB,">0",AK:AK)     # Risk when whales present
=AVERAGEIF(O:O,">0.3",D:D)       # Peak multiplier with high concentration
=CORREL(AB:AB,T:T)               # Whale presence vs profit/loss ratio
```

### 3. Timing Strategy Optimization
```excel
# Optimal entry timing analysis
=AVERAGEIF(W:W,">0.3",Q:Q)       # Success rate for early adopters
=AVERAGEIF(V:V,">3",AK:AK)       # Risk when many late joiners
=CORREL(U:U,D:D)                 # Early entries vs peak multiplier
```

### 4. Experience Factor Analysis
```excel
# Impact of player experience
=AVERAGEIFS(D:D,Z:Z,">0.5",F:F,FALSE)  # Peak in expert-heavy, non-instarug games
=CORREL(Y:Y,AK:AK)                      # High-level players vs risk
=AVERAGEIF(X:X,">25",Q:Q)               # Success rate with experienced players
```

---

## 🎯 KEY INSIGHTS TO EXPLORE

### Player Behavior Patterns
- **Success Factors**: What player characteristics predict success?
- **Risk Indicators**: Which player patterns signal high risk?
- **Market Dynamics**: How do different player types interact?

### Trading Strategy Analysis
- **Optimal Patterns**: Which trading styles perform best?
- **Risk Management**: How does player concentration affect outcomes?
- **Timing Strategies**: Early vs late entry success rates

### Market Efficiency
- **Profit Distribution**: How are profits/losses distributed?
- **Experience Premium**: Do experienced players perform better?
- **Market Maturity**: How does player composition affect game outcomes?

---

## 📈 VISUALIZATION RECOMMENDATIONS

### Scatter Plots
- **Player Experience vs Success** (X vs Q)
- **Concentration Risk vs Outcomes** (O vs D)
- **Trading Intensity vs Risk** (M vs AK)

### Histograms
- **Player Success Rate Distribution** (Q)
- **Trading Pattern Distribution** (AA through AG)
- **Risk Score Distribution** (AK)

### Correlation Matrices
- **Player Demographics**: X, Y, Z vs outcomes
- **Trading Patterns**: AA-AG vs performance metrics
- **Risk Factors**: AH, AI, AJ, AK relationships

---

## ✅ IMMEDIATE ANALYSIS OPPORTUNITIES

1. **Import** `player_integrated_data.csv` to Google Sheets
2. **Create** player behavior analysis dashboard
3. **Build** risk assessment models using player factors
4. **Develop** success prediction formulas
5. **Optimize** entry/exit strategies based on player patterns

**This integrated dataset provides unprecedented insight into the relationship between individual player behavior and game outcomes!** 🚀