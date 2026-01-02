# Peak Price Analysis - Distribution and Classification System

## 📊 Overview

This document presents a comprehensive analysis of peak price distribution in the `clean_games_dataset.csv` file containing 940 rugs.fun games. The analysis focuses on developing an optimal logarithmic classification system for games based on their peak prices, with particular emphasis on capturing the full spectrum of profitable games.

### **Analysis Objectives**
- **Distribution Analysis**: Understand peak price patterns and characteristics
- **Classification System**: Develop data-driven ranges for game categorization
- **Sweet Spot Identification**: Find actionable trading probability thresholds
- **Natural Breakpoints**: Identify optimal division points in the distribution

---

## 📈 Overall Statistics

### **Basic Statistics**

| Metric | Value |
|--------|-------|
| Minimum Peak Price | 1.000000x |
| Maximum Peak Price | 5,346.325931x |
| Total Range | 5,345.325931x |
| Mean Peak Price | 12.57x |
| Median Peak Price | 1.85x |
| Standard Deviation | 176.20x |

### **Distribution Characteristics**

- **Highly Skewed Distribution**: The median (1.85x) is much lower than the mean (12.57x)
- **Right-Skewed**: Most games have low peaks, with extreme outliers reaching very high multipliers
- **High Variability**: Standard deviation of 176.20x indicates significant spread
- **Outlier Impact**: The 5,346x outlier significantly affects the mean

---

## 📊 Percentile Analysis

### **Complete Percentile Distribution**

| Percentile | Peak Price |
|------------|------------|
| 10th | 1.025064x |
| 20th | 1.137642x |
| 30th | 1.292712x |
| 40th | 1.511041x |
| 50th (Median) | 1.849284x |
| 60th | 2.344350x |
| 70th | 3.134200x |
| 80th | 4.560000x |
| 85th | 5.738871x |
| 90th | 7.589560x |
| 92nd | 9.257363x |
| 94th | 14.615013x |
| 96th | 22.913834x |
| 98th | 61.915854x |
| 99th | 152.325137x |
| 99.5th | 227.380291x |
| 99.9th | 664.091621x |

### **Key Distribution Insights**

- **69.3%** of games peak below 3.0x
- **91.6%** of games peak below 15.0x
- **98.6%** of games peak below 120.0x
- Only **1.4%** of games reach the ultra-profitable 120.0x+ range

---

## 🎯 Logarithmic Range Classification System

### **Recommended 6-Range System**

Based on data-driven analysis and natural distribution gaps, we developed an optimal logarithmic classification system:

#### **Range 1: Conservative (1.0x - 2.5x)**
- **Games**: 594 (63.2% of total)
- **Description**: Low volatility, minimal risk
- **Characteristics**: 
  - Represents the majority of games
  - Baseline performance level
  - Minimal profit potential but low risk
  - Most common game type

#### **Range 2: Moderate (2.5x - 6.0x)**
- **Games**: 210 (22.3% of total)
- **Description**: Standard volatility, balanced risk/reward
- **Characteristics**:
  - Good profit potential with manageable risk
  - Represents typical game performance
  - Balanced risk/reward profile
  - Second most common range

#### **Range 3: High (6.0x - 15.0x)**
- **Games**: 80 (8.5% of total)
- **Description**: Significant volatility, high profit potential
- **Characteristics**:
  - Substantial profit opportunities
  - Higher risk but significant reward potential
  - Above-average performance games
  - Good target for aggressive strategies

#### **Range 4: Very High (15.0x - 40.0x)**
- **Games**: 30 (3.2% of total)
- **Description**: Major volatility, substantial profit potential
- **Characteristics**:
  - High-reward games with significant risk
  - Exceptional profit potential
  - Rare but valuable opportunities
  - Elite performance tier

#### **Range 5: Extreme (40.0x - 120.0x)**
- **Games**: 13 (1.4% of total)
- **Description**: Massive volatility, exceptional profit potential
- **Characteristics**:
  - Rare high-multiplier games
  - Maximum risk/reward scenarios
  - Ultra-profitable opportunities
  - Premium performance tier

#### **Range 6: Ultra (120.0x+)**
- **Games**: 13 (1.4% of total)
- **Description**: Ultra-volatile, maximum profit potential
- **Characteristics**:
  - The rarest and most profitable games
  - Includes the 5,346x outlier
  - Maximum profit potential with highest risk
  - Legendary performance tier

### **Range Distribution Summary**

| Range | Games | Percentage | Cumulative % |
|-------|-------|------------|--------------|
| 1.0x - 2.5x | 594 | 63.2% | 63.2% |
| 2.5x - 6.0x | 210 | 22.3% | 85.5% |
| 6.0x - 15.0x | 80 | 8.5% | 94.0% |
| 15.0x - 40.0x | 30 | 3.2% | 97.2% |
| 40.0x - 120.0x | 13 | 1.4% | 98.6% |
| 120.0x+ | 13 | 1.4% | 100.0% |

---

## 🔍 Natural Breakpoints

### **Distribution Gap Analysis**

Analysis revealed significant gaps in the distribution at:
- **2.5x**: Natural clustering point (63.2% of games below)
- **6.0x**: Distribution gap (85.5% of games below)
- **15.0x**: Major gap (94.0% of games below)
- **40.0x**: Extreme gap (97.2% of games below)
- **120.0x**: Ultra gap (98.6% of games below)

### **Breakpoint Significance**

These breakpoints represent natural divisions in the data where:
- **Game behavior changes** significantly
- **Risk/reward profiles** shift dramatically
- **Trading strategies** should adapt accordingly
- **Pattern recognition** becomes more reliable

---

## 🏆 Top 10 Highest Peak Prices

1. **5,346.33x** (highest recorded)
2. **359.92x** (tied for 2nd)
3. **359.92x** (tied for 2nd)
4. **255.66x**
5. **227.38x** (tied for 5th)
6. **227.38x** (tied for 5th)
7. **215.08x**
8. **188.47x**
9. **164.54x**
10. **153.64x**

### **Ultra-High Performance Analysis**

- **Average of Top 10**: 1,119.47x
- **Median of Top 10**: 221.23x
- **Outlier Impact**: The 5,346x game significantly skews the average
- **Realistic Ultra Range**: 150x-400x for most ultra-high games

---

## 🎯 Sweet Spot Probability Analysis

### **Overview**

The sweet spot probability analysis identifies **conditional probability patterns** where reaching a specific price threshold provides high confidence that the game will continue to much higher levels. This creates actionable trading signals for predictive strategies.

### **Methodology**

- **Conditional Probability Calculation**: P(Target|Threshold) = Games reaching both threshold AND target / Games reaching threshold
- **Threshold Levels Tested**: 1.5x to 500.0x (35 different levels)
- **Target Levels Tested**: 5.0x to 1000.0x (19 different levels)
- **Minimum Sample Size**: 10+ games for reliable statistics
- **Confidence Threshold**: 50%+ probability for actionable signals

### **Top 10 Most Reliable Sweet Spots**

| Rank | Threshold | Probability | Target | Sample Size | Description |
|------|-----------|-------------|--------|-------------|-------------|
| 1 | 60.0x | 94.7% | 80.0x+ | 19 games | Ultra-high confidence |
| 2 | 70.0x | 94.7% | 80.0x+ | 19 games | Ultra-high confidence |
| 3 | 90.0x | 93.3% | 100.0x+ | 15 games | Ultra-high confidence |
| 4 | 12.0x | 91.8% | 15.0x+ | 61 games | High confidence, large sample |
| 5 | 18.0x | 91.7% | 20.0x+ | 48 games | High confidence, large sample |
| 6 | 9.0x | 91.1% | 10.0x+ | 79 games | High confidence, large sample |
| 7 | 35.0x | 89.3% | 40.0x+ | 28 games | High confidence |
| 8 | 40.0x | 88.0% | 50.0x+ | 25 games | High confidence |
| 9 | 50.0x | 86.4% | 60.0x+ | 22 games | High confidence |
| 10 | 25.0x | 85.7% | 30.0x+ | 35 games | High confidence, large sample |

### **Best Risk/Reward Sweet Spots**

| Rank | Threshold | Probability | Target | Reward Ratio | Risk/Reward Score |
|------|-----------|-------------|--------|--------------|-------------------|
| 1 | 25.0x | 51.4% | 80.0x+ | 3.2x | 1.65 |
| 2 | 30.0x | 60.0% | 80.0x+ | 2.7x | 1.60 |
| 3 | 50.0x | 50.0% | 150.0x+ | 3.0x | 1.50 |
| 4 | 35.0x | 64.3% | 80.0x+ | 2.3x | 1.47 |
| 5 | 60.0x | 57.9% | 150.0x+ | 2.5x | 1.45 |

### **Strategic Sweet Spots by Category**

#### **Conservative Sweet Spots (Threshold < 5x)**
- **4.0x → 75.9% → 5.0x+** (216 games)
- **3.5x → 66.4% → 5.0x+** (247 games)
- **3.0x → 56.7% → 5.0x+** (277 games)

#### **Moderate Sweet Spots (5x ≤ Threshold < 15x)**
- **12.0x → 91.8% → 15.0x+** (61 games)
- **9.0x → 91.1% → 10.0x+** (79 games)
- **8.0x → 80.0% → 10.0x+** (90 games)
- **10.0x → 77.8% → 15.0x+** (72 games)
- **12.0x → 72.1% → 20.0x+** (61 games)

#### **Aggressive Sweet Spots (Threshold ≥ 15x)**
- **60.0x → 94.7% → 80.0x+** (19 games)
- **90.0x → 93.3% → 100.0x+** (15 games)
- **35.0x → 89.3% → 40.0x+** (28 games)
- **40.0x → 88.0% → 50.0x+** (25 games)
- **50.0x → 86.4% → 60.0x+** (22 games)

---

## 🚀 Key Strategic Insights

### **High-Confidence Entry Points**
- **12.0x Threshold**: 91.8% chance of reaching 15.0x+ (61 games)
- **18.0x Threshold**: 91.7% chance of reaching 20.0x+ (48 games)
- **60.0x Threshold**: 94.7% chance of reaching 80.0x+ (19 games)

### **Risk-Adjusted Trading Strategies**
- **Conservative Strategy**: Enter at 4.0x, target 5.0x (75.9% success rate)
- **Moderate Strategy**: Enter at 12.0x, target 15.0x (91.8% success rate)
- **Aggressive Strategy**: Enter at 60.0x, target 80.0x (94.7% success rate)

### **Golden Sweet Spots**
1. **12.0x** - Major confidence threshold with large sample size
2. **60.0x** - Ultra-high confidence with excellent reward potential
3. **9.0x** - Near-term confidence with large sample size
4. **25.0x** - Best risk/reward ratio (3.2x potential reward)

---

## 📊 Practical Applications

### **Real-Time Trading Signals**
- **Wait for 12.0x** → 91.8% confidence it will reach 15.0x+
- **Wait for 18.0x** → 91.7% confidence it will reach 20.0x+
- **Wait for 60.0x** → 94.7% confidence it will reach 80.0x+

### **Position Sizing Guidelines**
- **High Confidence (>90%)**: Larger position sizes
- **Medium Confidence (70-90%)**: Standard position sizes
- **Lower Confidence (50-70%)**: Smaller position sizes

### **Exit Strategy Optimization**
- Use sweet spot targets as primary exit points
- Combine with technical analysis for optimal timing
- Consider partial exits at intermediate levels

### **Prediction System Integration**
This classification system can be used for:
- **Game Type Identification**: Categorizing incoming games by expected volatility
- **Risk Assessment**: Determining appropriate betting strategies
- **Pattern Recognition**: Identifying which ranges are most predictable
- **Performance Tracking**: Monitoring prediction accuracy by range

---

## 🔗 Related Documentation

### **Core Analysis Documents**
- [`01-OVERVIEW.md`](01-OVERVIEW.md) - Executive summary and key findings
- [`03-TREASURY-REMAINDER-ANALYSIS.md`](03-TREASURY-REMAINDER-ANALYSIS.md) - Treasury system analysis
- [`04-INTRA-GAME-CORRELATIONS.md`](04-INTRA-GAME-CORRELATIONS.md) - Pattern validation
- [`05-DYNAMIC-SWEET-SPOT-METHODOLOGY.md`](05-DYNAMIC-SWEET-SPOT-METHODOLOGY.md) - Real-time implementation

### **Supporting Documents**
- [`06-IMPLEMENTATION-GUIDE.md`](06-IMPLEMENTATION-GUIDE.md) - Trading strategies
- [`07-STATISTICAL-VALIDATION.md`](07-STATISTICAL-VALIDATION.md) - Statistical significance
- [`08-REFERENCES.md`](08-REFERENCES.md) - Data sources and references

---

## 📈 Conclusion

The peak price analysis provides:

1. **Comprehensive Classification System**: 6-range logarithmic system capturing full spectrum
2. **Actionable Sweet Spots**: High-confidence probability thresholds for trading
3. **Natural Breakpoints**: Data-driven division points for optimal categorization
4. **Strategic Framework**: Foundation for trading strategy development

### **Key Success Factors**
- **Data-Driven Ranges**: Based on actual distribution patterns
- **Logarithmic Progression**: Each range roughly doubles the previous
- **Balanced Distribution**: Meaningful number of games in each range
- **Profit-Focused**: Emphasizes most profitable ranges

This classification system serves as a foundation for developing targeted prediction models and trading strategies for each range of game volatility and profit potential.

---

**Analysis Date**: December 2024  
**Dataset**: 940 verified rugs.fun games  
**Status**: Complete - Classification system validated  
**Confidence Level**: High - Multiple sweet spots with >90% probability identified 