# ⏱️ TICK-BY-TICK ANALYSIS GUIDE

**Granular analysis of player movements, volatility, and rug timing patterns**

---

## 🎯 OVERVIEW

This dataset provides **tick-level granular analysis** of every price movement, player action, and volatility pattern leading up to each rug event.

**File**: `tick_by_tick_data.csv`  
**Records**: 18,811 individual tick records  
**Games**: 98 games analyzed  
**Fields**: 27 detailed metrics per tick  
**Average**: 191.9 ticks per game  

---

## 🔍 KEY DISCOVERY

**💥 VOLATILITY SPIKE BEFORE RUG: 1.78x HIGHER**
- **Normal volatility**: 0.147
- **Near-rug volatility**: 0.262
- **Spike factor**: 78% increase in volatility within 5 ticks of rug

---

## 📋 COMPLETE FIELD REFERENCE

### 🆔 IDENTIFICATION & TIMING

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| A | `gameId` | Text | Game identifier | Correlation across games |
| B | `tick` | Number | Tick number in game | Time series analysis |
| C | `price` | Number | Price at this tick | Price movement tracking |
| D | `timestamp` | Text | Exact timestamp | Precise timing analysis |

### 📍 POSITION IN GAME

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| E | `tick_position_ratio` | Number | Tick ÷ Final tick (0-1) | Game phase analysis |
| F | `ticks_to_rug` | Number | **Ticks remaining until rug** | **Rug proximity analysis** |
| G | `is_near_rug` | Boolean | **TRUE if ≤ 5 ticks to rug** | **Warning indicator** |
| H | `is_very_near_rug` | Boolean | **TRUE if ≤ 2 ticks to rug** | **Critical warning** |

### 💰 PRICE ANALYSIS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| I | `current_peak_so_far` | Number | Highest price reached so far | Peak tracking |
| J | `peak_ratio` | Number | Current price ÷ Peak so far | Relative position |
| K | `price_change_1tick` | Number | **Price change from previous tick** | **Momentum analysis** |
| L | `price_change_5tick` | Number | **Price change over 5 ticks** | **Trend analysis** |
| M | `price_velocity` | Number | **Acceleration of price changes** | **Volatility prediction** |

### 📊 VOLATILITY METRICS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| N | `rolling_volatility` | Number | **10-tick rolling volatility** | **Primary volatility indicator** |
| O | `rolling_avg_change` | Number | Average price change (10-tick window) | Baseline movement |
| P | `rolling_max_change` | Number | Maximum price change (10-tick window) | Spike detection |

### 👥 TRADING ACTIVITY

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| Q | `buy_orders_at_tick` | Number | **Buy orders placed at this tick** | **Demand pressure** |
| R | `sell_orders_at_tick` | Number | **Sell orders placed at this tick** | **Supply pressure** |
| S | `volume_at_tick` | Number | Total volume traded at this tick | Activity intensity |
| T | `players_active_at_tick` | Number | **Players trading at this tick** | **Participation level** |
| U | `buy_sell_ratio_at_tick` | Number | **Buy ÷ Sell orders at tick** | **Market sentiment** |
| V | `net_order_flow` | Number | Buy orders - Sell orders | Order flow direction |

### ⏰ TIMING ANALYSIS

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| W | `tick_interval` | Number | **Time since previous tick (ms)** | **Timing anomaly detection** |
| X | `interval_deviation` | Number | **Deviation from average interval** | **Suspicious timing** |

### 🎮 GAME CONTEXT

| Column | Field | Type | Description | Analysis Use |
|--------|-------|------|-------------|--------------|
| Y | `final_tick` | Number | Total game duration | Game length reference |
| Z | `peak_multiplier` | Number | Highest multiplier reached | Game performance |
| AA | `is_instarug` | Boolean | Game was instarug | Risk categorization |

---

## 🧮 CRITICAL ANALYSIS FORMULAS

### Rug Proximity Analysis

**Volatility spike detection:**
```excel
=AVERAGEIF(G:G,TRUE,N:N) / AVERAGEIF(G:G,FALSE,N:N)
```

**Trading activity before rug:**
```excel
=AVERAGEIFS(Q:Q,F:F,"<=5") / AVERAGEIFS(Q:Q,F:F,">20")
```

### Price Movement Patterns

**Pre-rug price velocity:**
```excel
=AVERAGEIFS(M:M,G:G,TRUE)
```

**Price change acceleration near rug:**
```excel
=AVERAGEIFS(L:L,F:F,"<=3")
```

### Player Behavior Analysis

**Panic selling detection:**
```excel
=SUMIFS(R:R,F:F,"<=5") / SUMIFS(Q:Q,F:F,"<=5")
```

**Player exodus timing:**
```excel
=AVERAGEIFS(T:T,E:E,">0.8") - AVERAGEIFS(T:T,E:E,"<0.2")
```

---

## 📊 GOOGLE SHEETS ANALYSIS SETUP

### 1. Volatility Warning System

**Create volatility threshold alerts:**
```excel
=IF(N2>AVERAGE(N:N)*1.5,"HIGH_VOLATILITY","NORMAL")
```

**Rolling volatility trend:**
```excel
=AVERAGE(OFFSET(N2,-10,0,10,1))
```

### 2. Rug Prediction Model

**Combine volatility + trading activity:**
```excel
=IF(AND(N2>0.3, U2<0.5, F2<=10), "RUG_WARNING", "SAFE")
```

**Multi-factor rug risk score:**
```excel
=MIN(1, (N2*0.4 + (1-U2)*0.3 + ABS(X2)*0.3))
```

### 3. Player Behavior Tracking

**Activity heat map by tick position:**
```excel
=SUMIFS(T:T, E:E, ">="&ROW()/100-0.05, E:E, "<"&ROW()/100+0.05)
```

**Trading pattern analysis:**
```excel
=CORREL(E:E, T:T)  # Player activity vs game progression
```

---

## 🎯 KEY INSIGHTS TO EXPLORE

### 1. Volatility Patterns
- **Pre-rug spikes**: Volatility increases 78% in final 5 ticks
- **Warning threshold**: Volatility > 0.3 indicates high rug risk
- **Pattern recognition**: Identify volatility signatures of different rug types

### 2. Player Behavior Signals
- **Exodus timing**: When do experienced players exit?
- **Panic selling**: Sell order clustering before rugs
- **Smart money**: Early exit patterns of successful players

### 3. Timing Anomalies
- **Tick interval irregularities**: System issues before rugs?
- **Acceleration patterns**: Games speeding up before rugs
- **Suspicious timing**: Coordinated activity detection

### 4. Price Movement Signatures
- **Velocity spikes**: Rapid price acceleration warnings
- **Peak sustainability**: How long do peaks last?
- **Drop patterns**: Price behavior in final ticks

---

## 📈 VISUALIZATION RECOMMENDATIONS

### Time Series Charts
- **Volatility over time** with rug proximity highlighting
- **Price movement velocity** with trend lines
- **Trading activity** heat maps by tick position

### Correlation Analysis
- **Volatility vs Rug Distance** scatter plot
- **Player Activity vs Price Movement** correlation
- **Buy/Sell Ratio vs Rug Timing** relationship

### Warning Systems
- **Real-time volatility dashboard** with thresholds
- **Rug proximity alerts** based on multiple factors
- **Player behavior anomaly detection**

---

## 🚨 CRITICAL WARNING INDICATORS

### High Priority Signals
1. **Volatility > 0.3** (2x normal)
2. **Buy/Sell ratio < 0.5** (heavy selling)
3. **Player exodus** (active players dropping)
4. **Timing irregularities** (interval deviations > 1.0)

### Rug Prediction Formula
```excel
=IF(AND(rolling_volatility>0.3, buy_sell_ratio<0.5, players_active<3), "IMMINENT_RUG", 
   IF(AND(rolling_volatility>0.2, ticks_to_rug<=10), "HIGH_RISK",
   "NORMAL"))
```

---

## 🔍 ADVANCED ANALYSIS OPPORTUNITIES

### 1. Machine Learning Features
- Use tick-level data to train rug prediction models
- Identify complex patterns human analysis might miss
- Real-time risk scoring based on multiple factors

### 2. Market Microstructure Analysis
- Order flow analysis and market maker behavior
- Price impact of large orders
- Liquidity patterns and market depth

### 3. Behavioral Finance Applications
- Herding behavior detection
- Panic selling cascade analysis
- Smart money vs retail timing differences

---

## ✅ IMMEDIATE ACTION ITEMS

1. **Import** `tick_by_tick_data.csv` to Google Sheets
2. **Create** volatility monitoring dashboard
3. **Build** rug warning system with multiple indicators
4. **Analyze** player behavior patterns near rugs
5. **Develop** real-time risk assessment tools

**This granular data provides unprecedented insight into the precise mechanics of rug events and player behavior patterns!** 🚀

**KEY FINDING**: Volatility increases 78% in the final 5 ticks - a critical early warning signal for rug detection! 💥